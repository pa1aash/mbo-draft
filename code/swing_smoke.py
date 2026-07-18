"""Pre-launch smoke for C2-SWING. Three things, none of which look at the arm's contrast.

1. REGRESSION: with both smoothness knobs off, train_ensemble / fit_botorch_gp / fit_svgp
   must reproduce results/kbeta/grid_b2.0.json bit-exactly. The knobs are default-off, so
   any drift here means the edit changed the incumbent engine and the whole Stage-0 corpus
   would be invalidated.
2. TIMING: cost per (task, seed) shard, to size the grid honestly before pre-registering.
3. MANIPULATION: does the smoothing knob actually reduce the mean's gradient norm, and
   does the rough kernel raise the GP's? Run on seeds 100/101 -- DISJOINT from the
   analysis seeds 0..29 -- so no pre-registered contrast is looked at before commit.
"""
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def regression():
    """base variant, w=96, seed 0 vs the committed beta=2 grid."""
    import torch
    os.environ['MBO_X1'] = '1'
    os.environ['MBO_X3'] = '1'
    import importlib
    import mbo
    importlib.reload(mbo)
    ref = json.load(open(os.path.join(HERE, '..', 'results', 'kbeta', 'grid_b2.0.json')))
    task = 'Branin-2D'
    t = mbo.make_tasks([task])[0]
    ok = True
    for seed in (0, 1):
        np.random.seed(seed); torch.manual_seed(seed)
        x, y = t.data()
        x0 = mbo.init_candidates(x, y, seed)
        ms = mbo.train_ensemble(x, y, t.dim, seed=seed, K=mbo.K_ENS, ep=mbo.TRAIN_EP)
        f_t = mbo.ens_lcb_torch(ms, mbo.BETA)
        xf = mbo.grad_opt(f_t, torch.FloatTensor(x0), steps=mbo.OPT_STEPS)
        p100, _ = mbo.eval_designs(t, xf)
        want = ref['mbo'][task]['ens:grad']['p100']['all'][seed]
        same = abs(p100 - want) < 1e-9
        ok &= same
        print(f'  REGRESSION ens:grad {task} seed{seed}: got {p100:.10f} want {want:.10f} '
              f'-> {"BIT-IDENTICAL" if same else "DRIFT"}')
    return ok


def timing_and_manipulation():
    import smooth_swing as sw
    for task in ('Branin-2D', 'Ackley-20D'):
        t0 = time.time()
        spec, res = sw._cell(dict(task=task, seed=100))
        dt = time.time() - t0
        print(f'\n  {task}: {len(res["cells"])} cells in {dt:.1f}s')
        r = res['rough_d']
        print('    roughness on D (normalized ||d mu/dx||):')
        for k in sorted(r):
            print(f'      {k:22s} {r[k]:10.4f}')
        base96 = r.get('ens_base_w96')
        print(f'    -- ens smoothing moved roughness: '
              f'{ {k: round(r[k]/base96, 3) for k in r if k.startswith("ens_") and "w96" in k} }')
        print(f'    -- GP rough/smooth ratio: '
              f'm12/botorchgp={r.get("botorchgp_m12", 0)/max(r.get("botorchgp", 1e-9), 1e-9):.3f}, '
              f'ls005/botorchgp={r.get("botorchgp_ls005", 0)/max(r.get("botorchgp", 1e-9), 1e-9):.3f}')
        yield task, dt


if __name__ == '__main__':
    print('== 1. REGRESSION (incumbent path must be bit-identical) ==')
    ok = regression()
    print(f'  -> {"PASS" if ok else "FAIL"}')
    print('\n== 2/3. TIMING + MANIPULATION CHECK (seed 100, disjoint from 0..29) ==')
    times = list(timing_and_manipulation())
    print('\n== summary ==')
    for task, dt in times:
        print(f'  {task}: {dt:.1f}s/shard')
