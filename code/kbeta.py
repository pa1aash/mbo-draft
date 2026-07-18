"""Phase 3 K x beta gate runner (on_on engine).

Produces the measurements KB1/KB3/KB4 need, that no existing script writes:
  (b) ensemble rows: K in {2,3,5,10} x beta in {0,0.5,1,2,5} x {grad,perturb,cma} x 7 tasks
      x N seeds. The ensemble is fit ONCE per (task,K,seed) and reused across beta x opt.
  (3.2/KB4) per (task, surrogate, K): mean sigma over the training data (a fixed in-D
      reference of <=500 rows drawn from D) and mean sigma over each optimizer's proposals,
      and the ratio sigma_GP/sigma_ens on the shared reference. GPs are K-independent, fit
      once per (task,seed).

Every record is engine-stamped (X1/X3/K/beta/...). Output: results/kbeta/kbeta_ens.json
(ensemble grid + sigma) and results/kbeta/kbeta_gpsigma.json (GP/SVGP sigma).

  MBO_X1=1 MBO_X3=1 python kbeta.py --seeds 30 --jobs 30
"""
import argparse
import json
import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, '..', 'results', 'kbeta')
KS = [2, 3, 5, 10]
BETAS = [0.0, 0.5, 1.0, 2.0, 5.0]
OPTS = ['grad', 'perturb', 'cma']


def _meta(seeds):
    import run_all
    import mbo
    return run_all.engine_meta(seeds, mbo.BETA, mbo.K_ENS)


def _ref(x, seed, n=500):
    r = np.random.RandomState(1000 + seed)
    idx = r.choice(len(x), min(n, len(x)), replace=False)
    return x[idx]


def _ens_cell(spec):
    """One (task, K, seed): fit ensemble, sweep beta x opt, record p100 + sigma."""
    import torch
    torch.set_num_threads(1)
    os.environ['MBO_X1'] = '1'; os.environ['MBO_X3'] = '1'
    import importlib
    import mbo
    importlib.reload(mbo)
    assert mbo.X1_STANDARDIZE_Y and mbo.X3_MATCHED_PROTOCOL
    t = mbo.make_tasks([spec['task']])[0]
    seed, K = spec['seed'], spec['K']
    np.random.seed(seed); torch.manual_seed(seed)
    x, y = t.data()
    x0 = mbo.init_candidates(x, y, seed)
    ms = mbo.train_ensemble(x, y, t.dim, seed=seed, K=K, ep=mbo.TRAIN_EP)
    ref = _ref(x, seed)
    with torch.no_grad():
        _, sd_ref = mbo.ens_moments_raw(ms, torch.FloatTensor(ref))
    sigma_train = float(sd_ref.mean())
    out = {'sigma_train': sigma_train, 'cells': {}}
    for beta in BETAS:
        f_t = mbo.ens_lcb_torch(ms, beta)
        f_n = mbo.ens_lcb_np(ms, beta)
        for opt in OPTS:
            if opt == 'grad':
                xf = mbo.grad_opt(f_t, torch.FloatTensor(x0), steps=mbo.OPT_STEPS)
            elif opt == 'perturb':
                xf = mbo.perturb_opt(f_n, x0)
            else:
                xf = mbo.cma_opt(f_n, x0, seed=seed)
            if xf is None:
                continue
            p100, p50 = mbo.eval_designs(t, xf)
            with torch.no_grad():
                _, sd_p = mbo.ens_moments_raw(ms, torch.FloatTensor(np.asarray(xf, np.float32)))
            out['cells'][f'b{beta}|{opt}'] = dict(p100=float(p100), p50=float(p50),
                                                  sigma_prop=float(sd_p.mean()))
    return spec, out


def _gp_sigma_cell(spec):
    """One (task, surrogate, seed): fit GP/SVGP, record sigma over ref + own proposals."""
    import torch
    torch.set_num_threads(1)
    os.environ['MBO_X1'] = '1'; os.environ['MBO_X3'] = '1'
    import importlib
    import mbo
    importlib.reload(mbo)
    t = mbo.make_tasks([spec['task']])[0]
    seed, surr = spec['seed'], spec['surr']
    np.random.seed(seed); torch.manual_seed(seed)
    x, y = t.data()
    x0 = mbo.init_candidates(x, y, seed)
    ref = _ref(x, seed)
    if surr == 'botorchgp':
        gp = mbo.fit_botorch_gp(x, y, seed)
        if gp is None:
            return spec, None
        ym, ys = float(np.mean(y)), float(np.std(y) + 1e-8)

        def sig(xx):
            with torch.no_grad():
                post = gp.posterior(torch.DoubleTensor(np.asarray(xx, np.float64)))
                return (post.variance.clamp_min(1e-12).sqrt().squeeze(-1).numpy()) * ys
        f = mbo.botorch_lcb_torch(gp, mbo.BETA)
        f_n = (lambda xx: f(torch.FloatTensor(xx)).detach().numpy())
    elif surr == 'svgp':
        s = mbo.fit_svgp(x, y, t.dim, seed)
        if s is None:
            return spec, None
        m, ym, ys = s['model'], s['ym'], s['ys']; m.eval()

        def sig(xx):
            with torch.no_grad():
                post = m(torch.FloatTensor(xx))
                return (post.variance.clamp_min(1e-12).sqrt() * ys).numpy()
        f_n = mbo.svgp_lcb_np(s, mbo.BETA)
    else:
        raise ValueError(surr)
    sigma_train = float(np.mean(sig(ref)))
    # sigma over the surrogate's own perturb proposals (beta=2), matched to ens measurement
    xf = mbo.perturb_opt(f_n, x0)
    sigma_prop = float(np.mean(sig(xf)))
    return spec, dict(sigma_train=sigma_train, sigma_prop=sigma_prop)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seeds', type=int, default=30)
    ap.add_argument('--jobs', type=int, default=max(1, (os.cpu_count() or 2) - 2))
    ap.add_argument('--tasks', nargs='*', default=None)
    a = ap.parse_args()
    os.makedirs(RES, exist_ok=True)
    import mbo
    tasks = a.tasks or [T().name for T in mbo.ALL_TASKS]
    meta = _meta(a.seeds)
    assert meta['X1'] and meta['X3'], 'kbeta must run on_on; set MBO_X1=1 MBO_X3=1'

    # ---- ensemble grid ----
    ens_specs = [{'task': t, 'K': K, 'seed': s}
                 for t in tasks for K in KS for s in range(a.seeds)]
    ENS = {'meta': meta, 'grid': {}}   # grid[task][K][b{beta}|opt] -> aggregated over seeds
    buf = {}
    t0 = time.time()
    print(f'ensemble: {len(ens_specs)} (task,K,seed) fits, {a.jobs} workers', flush=True)
    with ProcessPoolExecutor(max_workers=a.jobs) as ex:
        done = 0
        for fut in as_completed([ex.submit(_ens_cell, s) for s in ens_specs]):
            spec, out = fut.result()
            done += 1
            key = (spec['task'], spec['K'])
            slot = buf.setdefault(key, {'sigma_train': [], 'cells': {}})
            slot['sigma_train'].append(out['sigma_train'])
            for ck, cv in out['cells'].items():
                slot['cells'].setdefault(ck, {'p100': [], 'p50': [], 'sigma_prop': []})
                for m in ('p100', 'p50', 'sigma_prop'):
                    slot['cells'][ck][m].append(cv[m])
            if done % 50 == 0:
                print(f'  ens {done}/{len(ens_specs)} [{(time.time()-t0)/60:.1f}m]', flush=True)
    for (task, K), slot in buf.items():
        node = ENS['grid'].setdefault(task, {}).setdefault(f'K{K}', {})
        node['_engine'] = {'X1': True, 'X3': True, 'K': K, 'beta': 'sweep',
                           'TOP': mbo.TOP, 'OPT_STEPS': mbo.OPT_STEPS, 'LR_OPT': mbo.LR_OPT}
        node['sigma_train'] = dict(mean=float(np.mean(slot['sigma_train'])),
                                   all=[float(v) for v in slot['sigma_train']])
        for ck, mv in slot['cells'].items():
            node[ck] = {m: dict(mean=float(np.mean(mv[m])), std=float(np.std(mv[m])),
                                all=[float(v) for v in mv[m]]) for m in mv}
    json.dump(ENS, open(os.path.join(RES, 'kbeta_ens.json'), 'w'), indent=1)
    print(f'wrote kbeta_ens.json [{(time.time()-t0)/60:.1f}m]', flush=True)

    # ---- GP/SVGP sigma (K-independent) ----
    gp_specs = [{'task': t, 'surr': su, 'seed': s}
                for t in tasks for su in ('botorchgp', 'svgp') for s in range(a.seeds)]
    GP = {'meta': meta, 'sigma': {}}
    gbuf = {}
    print(f'gp sigma: {len(gp_specs)} fits', flush=True)
    with ProcessPoolExecutor(max_workers=a.jobs) as ex:
        for fut in as_completed([ex.submit(_gp_sigma_cell, s) for s in gp_specs]):
            spec, out = fut.result()
            if out is None:
                continue
            key = (spec['task'], spec['surr'])
            gbuf.setdefault(key, {'sigma_train': [], 'sigma_prop': []})
            gbuf[key]['sigma_train'].append(out['sigma_train'])
            gbuf[key]['sigma_prop'].append(out['sigma_prop'])
    for (task, surr), v in gbuf.items():
        GP['sigma'].setdefault(task, {})[surr] = dict(
            sigma_train=float(np.mean(v['sigma_train'])),
            sigma_prop=float(np.mean(v['sigma_prop'])))
    json.dump(GP, open(os.path.join(RES, 'kbeta_gpsigma.json'), 'w'), indent=1)
    print(f'wrote kbeta_gpsigma.json. total {(time.time()-t0)/60:.1f}m', flush=True)
    print('KBETA_DONE', flush=True)


if __name__ == '__main__':
    main()
