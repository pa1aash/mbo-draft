"""A.1.5 -- the x0 inversion probe (T12), on the AUDITED engine (X1 on, X3 on).

Under X3, grad/perturb pool every iterate PLUS the init candidates x0 (mbo.py grad_opt
seeds `pool=[x0]`), then return the top-TOP by SURROGATE LCB. So x0 is IN the pool. If the
ensemble's LCB still ranks hallucinated high-LCB / low-oracle designs above the real x0
points it is holding, the returned set is WORSE (by the noiseless oracle) than designs the
method already had -- a sharp, by-demonstration statement of the pessimism failure.

Per (task, cell) over seeds, with the noiseless oracle:
  inversion_rate  = P(best returned oracle < best x0 oracle)   [returned worse than held]
  mean_magnitude  = mean(best_x0_oracle - best_returned_oracle) when inverted
  frac_worse      = mean fraction of the returned TOP that scores below best_x0_oracle
GP/SVGP grad cells are included as a CONTRAST -- if only the ensemble inverts, the failure
is surrogate-geometry-specific, not a generic optimizer artifact.

  python x0_inversion.py --seeds 8 --jobs 6   -> results/x0_inversion.json
"""
import argparse
import json
import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

import numpy as np

# All 9 grid cells (Phase 7.2), both X3 states. X1 held on (audited engine); the probe is
# about X3's candidate-pooling (grad_opt pools x0 under X3-on).
CELLS = [f'{s}:{o}' for s in ('ens', 'botorchgp', 'svgp') for o in ('grad', 'perturb', 'cma')]
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'results', 'x0_inversion.json')


def _cell(spec):
    import torch
    torch.set_num_threads(1)
    os.environ['MBO_X1'] = '1'; os.environ['MBO_X3'] = '1' if spec['x3'] else '0'
    import importlib
    import mbo
    importlib.reload(mbo)
    assert mbo.X1_STANDARDIZE_Y and mbo.X3_MATCHED_PROTOCOL == bool(spec['x3'])
    t = mbo.make_tasks([spec['task']])[0]
    seed = spec['seed']
    np.random.seed(seed); torch.manual_seed(seed)
    x, y = t.data()
    x0 = mbo.init_candidates(x, y, seed)
    surr, opt = spec['cell'].split(':')
    f_torch, f_np, _ = mbo.build_surrogate(surr, x, y, t.dim, seed, mbo.BETA, mbo.TRAIN_EP, mbo.K_ENS)
    if opt == 'grad':
        if f_torch is None:
            return {**spec, 'metrics': None}
        xf = mbo.grad_opt(f_torch, torch.FloatTensor(x0), steps=mbo.OPT_STEPS)
    elif opt == 'cma':
        if f_np is None:
            return {**spec, 'metrics': None}
        xf = mbo.cma_opt(f_np, x0, seed=seed)
        if xf is None:
            return {**spec, 'metrics': None}
    else:
        if f_np is None:
            return {**spec, 'metrics': None}
        xf = mbo.perturb_opt(f_np, x0)
    x0o = t.oracle(x0); xfo = t.oracle(xf)
    x0_best = float(x0o.max()); ret_best = float(xfo.max())
    inv = ret_best < x0_best
    return {**spec, 'metrics': dict(
        x0_best=x0_best, ret_best=ret_best, ret_p50=float(np.median(xfo)),
        inversion=bool(inv), magnitude=float(x0_best - ret_best) if inv else 0.0,
        frac_worse=float(np.mean(xfo < x0_best)))}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seeds', type=int, default=8)
    ap.add_argument('--jobs', type=int, default=max(1, (os.cpu_count() or 2) - 2))
    ap.add_argument('--out', default=OUT)
    a = ap.parse_args()
    import mbo, run_all
    tasks = [T().name for T in mbo.ALL_TASKS]
    specs = [{'task': tk, 'cell': c, 'seed': s, 'x3': x3}
             for tk in tasks for c in CELLS for x3 in (0, 1) for s in range(a.seeds)]
    R = {}
    t0 = time.time()
    print(f'{len(specs)} cells, {a.jobs} workers', flush=True)
    with ProcessPoolExecutor(max_workers=a.jobs) as ex:
        for fut in as_completed([ex.submit(_cell, s) for s in specs]):
            r = fut.result()
            if r['metrics'] is None:
                continue
            key = f"{r['task']}|{r['cell']}|x3={r['x3']}"
            R.setdefault(key, []).append(r['metrics'])
    agg = {}
    for key, vs in R.items():
        agg[key] = dict(
            n=len(vs),
            inversion_rate=float(np.mean([v['inversion'] for v in vs])),
            mean_magnitude=float(np.mean([v['magnitude'] for v in vs])),
            mean_frac_worse=float(np.mean([v['frac_worse'] for v in vs])),
            mean_x0_best=float(np.mean([v['x0_best'] for v in vs])),
            mean_ret_best=float(np.mean([v['ret_best'] for v in vs])))
    agg['meta'] = run_all.engine_meta(a.seeds, mbo.BETA, mbo.K_ENS)  # X1 stamp; X3 is per-key
    json.dump(agg, open(a.out, 'w'), indent=1)
    print(f'done in {(time.time()-t0)/60:.1f} min -> {a.out}')
    print(f'\n{"task":16}{"cell":18}{"x3":>4}{"inv_rate":>9}{"magnitude":>11}{"x0_best":>10}{"ret_best":>10}')
    for tk in tasks:
        for c in CELLS:
            for x3 in (0, 1):
                v = agg.get(f'{tk}|{c}|x3={x3}')
                if v:
                    print(f'{tk:16}{c:18}{x3:>4}{v["inversion_rate"]:9.2f}{v["mean_magnitude"]:11.2f}'
                          f'{v["mean_x0_best"]:10.2f}{v["mean_ret_best"]:10.2f}')


if __name__ == '__main__':
    main()
