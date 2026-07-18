"""0A.2 -- ensemble hidden-width ablation (W1/W2), pre-registered in PREREGISTRATION_V3.md.

Answers N5 (the NTK/spectral-bias objection): if the GP's advantage is really a
finite-width artifact of the ensemble's jagged mean, a wider ensemble should close the
gap. K is held at 5 throughout -- the audit's point was that K != width, so sweeping K
never tested this.

Per (task, seed):
  - GP + SVGP are width-independent: fit ONCE and reused across every w.
  - the ensemble is fit per w in {96, 256, 512, 1024} on the FULL dataset (the incumbent
    grid protocol, so w=96 must reproduce results/kbeta/grid_b2.0.json's ens rows).
  - all 3 optimizers run on every surrogate -> the 3x3 grid at each w.
  - separately, a fresh 80/20 split gives held-out RMSE/NLL per (task, w) and for the GPs
    (W2). The split fit is NOT reused for the grid, so the grid estimand is unchanged.

  MBO_X1=1 MBO_X3=1 python width_ablation.py --seeds 30 --jobs 14
    -> results/width/width_grid.json
"""
import argparse
import json
import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'results', 'width')
TASKS = ['Branin-2D', 'Styblinski-5D', 'Levy-8D', 'Rosenbrock-10D',
         'Rastrigin-15D', 'Ackley-20D', 'Griewank-30D']
WIDTHS = [96, 256, 512, 1024]
OPT3 = ['perturb', 'grad', 'cma']


def _metrics(mu, sd, f):
    """RAW-unit predictive metrics. normRMSE is RMSE/std(f) so tasks are comparable;
    NLL is the Gaussian NLL on standardized targets (same reason)."""
    sd = np.maximum(sd, 1e-8)
    fs = np.std(f) + 1e-12
    rmse = float(np.sqrt(np.mean((mu - f) ** 2)))
    nll = float(np.mean(0.5 * np.log(2 * np.pi * (sd / fs) ** 2)
                        + 0.5 * ((mu - f) / sd) ** 2))
    return dict(rmse=rmse, norm_rmse=float(rmse / fs), nll=nll)


def _run_opts(mbo, t, x0, f_t, f_n, seed):
    """3 optimizers on one surrogate -> {opt: {p100, p50}}. Missing stays MISSING."""
    import torch
    out = {}
    for opt in OPT3:
        if opt == 'grad':
            if f_t is None:
                continue
            xf = mbo.grad_opt(f_t, torch.FloatTensor(x0), steps=mbo.OPT_STEPS)
        elif opt == 'perturb':
            if f_n is None:
                continue
            xf = mbo.perturb_opt(f_n, x0)
        else:
            if f_n is None:
                continue
            xf = mbo.cma_opt(f_n, x0, seed=seed)
        if xf is None:
            continue
        p100, p50 = mbo.eval_designs(t, xf)
        out[opt] = dict(p100=float(p100), p50=float(p50))
    return out


def _cell(spec):
    import torch
    torch.set_num_threads(1)
    os.environ['MBO_X1'] = '1'
    os.environ['MBO_X3'] = '1'
    import importlib
    import mbo
    importlib.reload(mbo)
    assert mbo.X1_STANDARDIZE_Y and mbo.X3_MATCHED_PROTOCOL, 'width ablation must run on_on'
    t = mbo.make_tasks([spec['task']])[0]
    seed = spec['seed']
    beta, K = mbo.BETA, mbo.K_ENS
    np.random.seed(seed)
    torch.manual_seed(seed)
    x, y = t.data()
    x0 = mbo.init_candidates(x, y, seed)
    res = {'cells': {}, 'heldout': {}}

    # ---- width-independent surrogates: fit once, reuse across every w ----
    for name in ('botorchgp', 'svgp'):
        f_t, f_n, _ = mbo.build_surrogate(name, x, y, t.dim, seed, beta, mbo.TRAIN_EP, K)
        if f_n is None:
            continue                                   # dependency missing -> MISSING
        for opt, v in _run_opts(mbo, t, x0, f_t, f_n, seed).items():
            res['cells'][f'{name}:{opt}'] = v

    # ---- ensemble at each width (full-data fit = incumbent grid protocol) ----
    for w in WIDTHS:
        ms = mbo.train_ensemble(x, y, t.dim, seed=seed, K=K, ep=mbo.TRAIN_EP, hid=w)
        f_t = mbo.ens_lcb_torch(ms, beta)
        f_n = mbo.ens_lcb_np(ms, beta)
        for opt, v in _run_opts(mbo, t, x0, f_t, f_n, seed).items():
            res['cells'][f'ens_w{w}:{opt}'] = v

    # ---- held-out predictive quality (W2), on a split never used by the grid ----
    r = np.random.RandomState(50000 + seed)
    idx = r.permutation(len(x))
    cut = int(0.8 * len(x))
    xtr, ytr, xte = x[idx[:cut]], y[idx[:cut]], x[idx[cut:]]
    fte = t.oracle(xte)                                # noiseless oracle on the test split
    for w in WIDTHS:
        ms = mbo.train_ensemble(xtr, ytr, t.dim, seed=seed, K=K, ep=mbo.TRAIN_EP, hid=w)
        with torch.no_grad():
            mu, sd = mbo.ens_moments_raw(ms, torch.FloatTensor(xte))
        res['heldout'][f'ens_w{w}'] = _metrics(mu.numpy(), sd.numpy(), fte)
    gp = mbo.fit_botorch_gp(xtr, ytr, seed)
    if gp is not None:
        ym, ys = float(np.mean(ytr)), float(np.std(ytr) + 1e-8)
        with torch.no_grad():
            post = gp.posterior(torch.DoubleTensor(np.asarray(xte, np.float64)))
            mu = post.mean.squeeze(-1).numpy() * ys + ym
            sd = post.variance.clamp_min(1e-12).sqrt().squeeze(-1).numpy() * ys
        res['heldout']['botorchgp'] = _metrics(mu, sd, fte)
    return spec, res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seeds', type=int, default=30)
    ap.add_argument('--jobs', type=int, default=14)
    a = ap.parse_args()
    specs = [dict(task=t, seed=s) for t in TASKS for s in range(a.seeds)]
    grid, held = {}, {}
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=a.jobs) as ex:
        futs = [ex.submit(_cell, sp) for sp in specs]
        for i, fu in enumerate(as_completed(futs)):
            sp, r = fu.result()
            for c, v in r['cells'].items():
                grid.setdefault(sp['task'], {}).setdefault(c, {}).setdefault('p100', []).append(v['p100'])
                grid[sp['task']][c].setdefault('p50', []).append(v['p50'])
            for k, v in r['heldout'].items():
                for m, val in v.items():
                    held.setdefault(sp['task'], {}).setdefault(k, {}).setdefault(m, []).append(val)
            print(f'[{i+1}/{len(specs)}] {sp["task"]:16s} seed{sp["seed"]:<3d} '
                  f'{len(r["cells"])} cells  {time.time()-t0:.0f}s', flush=True)

    import run_all
    import mbo
    agg = lambda v: dict(mean=float(np.mean(v)), std=float(np.std(v)), all=list(map(float, v)))
    out = {'meta': run_all.engine_meta(a.seeds, mbo.BETA, mbo.K_ENS),
           'widths': WIDTHS,
           'mbo': {t: {c: {m: agg(v) for m, v in d.items()} for c, d in cs.items()}
                   for t, cs in grid.items()},
           'heldout': {t: {k: {m: agg(v) for m, v in d.items()} for k, d in ks.items()}
                       for t, ks in held.items()}}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, 'width_grid.json'), 'w') as f:
        json.dump(out, f, indent=2)
    print('wrote', os.path.join(OUT, 'width_grid.json'))


if __name__ == '__main__':
    main()
