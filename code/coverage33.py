"""A.1.6 -- the full 3x3 premise-coverage matrix (surrogate x optimizer).

FLAW_LEDGER P0-3: the repo measures premise coverage for ens:grad only (1 of 9 cells) and
with sklearn's GP, not the grid's botorchgp. This parameterizes coverage over the full 3x3
using the grid's own surrogates, and P0-5's fix: the in-distribution reference set is drawn
from D (the actual dataset), NOT np.random.uniform -- DB data are cube vertices / normalized
measurements, not uniform, and synthetic data are the uniform sample itself.

Per (task, surrogate, optimizer, X1-state), over seeds:
  c_in  = P(mu - f <= beta*sigma) on a reference sample from D            [premise, in-dist]
  c_ood = P(mu - f <= beta*sigma) on the optimizer's own proposals        [premise, OOD]
All moments are RAW oracle units; beta=2. The surrogate is fit ONCE per (task,surr,x1,seed)
and all three optimizers run on it. Also correlates c_ood with the camera cell's normalized
p100 across the 9x7 synthetic grid (does coverage predict score?).

  python coverage33.py --seeds 4 --jobs 6   -> results/coverage33.json
"""
import argparse
import json
import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'results', 'coverage33.json')
CAMERA = os.path.join(HERE, '..', 'results', 'results_camera.json')
SURR = ['ens', 'botorchgp', 'svgp']
OPT = ['grad', 'perturb', 'cma']


def _fit_surrogate(mbo, surr, x, y, dim, seed, beta):
    """returns (moment_raw_fn(x)->(mu,sd), f_torch|None, f_np|None) all in raw units."""
    import torch
    if surr == 'ens':
        ms = mbo.train_ensemble(x, y, dim, seed=seed)

        def mom(xx):
            with torch.no_grad():
                mu, sd = mbo.ens_moments_raw(ms, torch.FloatTensor(xx))
            return mu.numpy(), sd.numpy()
        return mom, mbo.ens_lcb_torch(ms, beta), mbo.ens_lcb_np(ms, beta)
    if surr == 'botorchgp':
        gp = mbo.fit_botorch_gp(x, y, seed)
        if gp is None:
            return None, None, None
        # recover raw-unit moments: botorch posterior is standardized by the subsample y.
        # refit-free: read the training targets botorch standardized on is not exposed, so
        # standardize by the full-data y here for the coverage scale (consistent within cell).
        ym, ys = float(np.mean(y)), float(np.std(y) + 1e-8)

        def mom(xx):
            with torch.no_grad():
                post = gp.posterior(torch.DoubleTensor(np.asarray(xx, np.float64)))
                mu = post.mean.squeeze(-1).numpy()
                sd = post.variance.clamp_min(1e-12).sqrt().squeeze(-1).numpy()
            return mu * ys + ym, sd * ys           # standardized -> raw (full-data scale)
        f = mbo.botorch_lcb_torch(gp, beta)
        return mom, f, (lambda xx: f(torch.FloatTensor(xx)).detach().numpy())
    if surr == 'svgp':
        s = mbo.fit_svgp(x, y, dim, seed)
        if s is None:
            return None, None, None
        m, ym, ys = s['model'], s['ym'], s['ys']; m.eval()

        def mom(xx):
            with torch.no_grad():
                post = m(torch.FloatTensor(xx))
                mu = (post.mean * ys + ym).numpy()
                sd = (post.variance.clamp_min(1e-12).sqrt() * ys).numpy()
            return mu, sd
        return mom, mbo.svgp_lcb_torch(s, beta), mbo.svgp_lcb_np(s, beta)
    raise ValueError(surr)


def _cell(spec):
    import torch
    torch.set_num_threads(1)
    os.environ['MBO_X1'] = '1' if spec['x1'] else '0'
    os.environ['MBO_X3'] = '1' if spec['x3'] else '0'
    import importlib
    import mbo
    importlib.reload(mbo)
    t = mbo.make_tasks([spec['task']])[0]
    seed = spec['seed']
    np.random.seed(seed); torch.manual_seed(seed)
    x, y = t.data()
    x0 = mbo.init_candidates(x, y, seed)
    mom, f_torch, f_np = _fit_surrogate(mbo, spec['surr'], x, y, t.dim, seed, mbo.BETA)
    if mom is None:
        return {**spec, 'metrics': None}
    # in-distribution reference sampled from D (P0-5 fix), not uniform
    ref = x[np.random.choice(len(x), min(500, len(x)), replace=False)]
    mu_r, sd_r = mom(ref)
    c_in = mbo.coverage_of_premise(mu_r, sd_r, t.oracle(ref), mbo.BETA)
    out = {}
    for opt in OPT:
        if opt == 'grad':
            xf = None if f_torch is None else mbo.grad_opt(f_torch, torch.FloatTensor(x0), steps=mbo.OPT_STEPS)
        elif opt == 'perturb':
            xf = None if f_np is None else mbo.perturb_opt(f_np, x0)
        else:
            xf = None if f_np is None else mbo.cma_opt(f_np, x0, seed=seed)
        if xf is None:
            continue
        mu_o, sd_o = mom(xf)
        out[opt] = dict(c_in=float(c_in),
                        c_ood=float(mbo.coverage_of_premise(mu_o, sd_o, t.oracle(xf), mbo.BETA)))
    return {**spec, 'metrics': out}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seeds', type=int, default=4)
    ap.add_argument('--jobs', type=int, default=max(1, (os.cpu_count() or 2) - 2))
    ap.add_argument('--out', default=OUT)
    a = ap.parse_args()
    import mbo, run_all
    tasks = [T().name for T in mbo.ALL_TASKS]
    specs = [{'task': tk, 'surr': s, 'x1': x1, 'x3': x3, 'seed': sd}
             for tk in tasks for s in SURR for x1 in (0, 1) for x3 in (0, 1) for sd in range(a.seeds)]
    R = {}
    t0 = time.time()
    print(f'{len(specs)} fits, {a.jobs} workers', flush=True)
    with ProcessPoolExecutor(max_workers=a.jobs) as ex:
        for fut in as_completed([ex.submit(_cell, s) for s in specs]):
            r = fut.result()
            if not r['metrics']:
                continue
            for opt, mv in r['metrics'].items():
                key = f"{r['task']}|{r['surr']}:{opt}|x1={r['x1']}|x3={r['x3']}"
                R.setdefault(key, {'c_in': [], 'c_ood': []})
                R[key]['c_in'].append(mv['c_in']); R[key]['c_ood'].append(mv['c_ood'])
    agg = {k: {'c_in': float(np.mean(v['c_in'])), 'c_ood': float(np.mean(v['c_ood']))}
           for k, v in R.items()}
    # does c_ood predict normalized score across the 9x7 synthetic grid (X1-on, camera)?
    cam = json.load(open(CAMERA))['mbo']
    coods, scores = [], []
    for tk in tasks:
        cells = {c: cam[tk][c]['p100']['mean'] for c in [f'{s}:{o}' for s in SURR for o in OPT]
                 if c in cam.get(tk, {}) and isinstance(cam[tk][c].get('p100'), dict)}
        if len(cells) < 9:
            continue
        lo, hi = min(cells.values()), max(cells.values()); rng = (hi - lo) or 1
        for c in cells:
            k = f'{tk}|{c}|x1=1|x3=1'                 # camera engine = on_on
            if k in agg:
                coods.append(agg[k]['c_ood']); scores.append((cells[c] - lo) / rng)
    from scipy.stats import spearmanr
    rho = float(spearmanr(coods, scores).statistic) if len(coods) > 3 else float('nan')
    result = {'meta': run_all.engine_meta(a.seeds, mbo.BETA, mbo.K_ENS),
              'per_cell': agg, 'cood_vs_normscore_spearman_x1x3on': rho, 'n_scatter': len(coods)}
    json.dump(result, open(a.out, 'w'), indent=1)
    print(f'done in {(time.time()-t0)/60:.1f} min -> {a.out}')
    print(f'\nc_ood (on_on) by cell:  [Spearman(c_ood, normscore) over grid = {rho:+.3f}]')
    print(f'{"task":16}' + ''.join(f'{s[:4]+":"+o[:3]:>11}' for s in SURR for o in OPT))
    for tk in tasks:
        row = ''.join(f'{agg.get(f"{tk}|{s}:{o}|x1=1|x3=1", {}).get("c_ood", float("nan")):11.2f}'
                      for s in SURR for o in OPT)
        print(f'{tk:16}{row}')


if __name__ == '__main__':
    main()
