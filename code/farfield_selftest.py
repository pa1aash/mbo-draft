"""0D validity check: the INCUMBENT engine path still reproduces results/kbeta/grid_b2.0.json.

0D adds instrumentation in code/farfield_v2.py and does not touch code/mbo.py, so the default
path is unchanged by construction. This script verifies that empirically rather than asserting
it, replicating what docs/WIDTH_ABLATION.md did for the width arm.

It runs the published grid through run_all._worker -- the same function run_beta0.py and the
kbeta phase-3 driver used to WRITE grid_b2.0.json -- and compares every (task, cell, seed)
p100 against the published file.

Pre-registered standard (docs/PREREGISTRATION_V3.md 0D): grad and cma bit-exact on all 7
tasks; perturb within noise, because perturb_opt draws from the global numpy RNG without
reseeding (mbo.py:257-272) so its stream position depends on call order.

  MBO_X1=1 MBO_X3=1 python farfield_selftest.py --seeds 30 --jobs 30
    -> results/mechanism/farfield_v2/selftest_repro.json
"""
import argparse
import json
import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'results', 'mechanism', 'farfield_v2')
REF = os.path.join(HERE, '..', 'results', 'kbeta', 'grid_b2.0.json')
TASKS = ['Branin-2D', 'Styblinski-5D', 'Levy-8D', 'Rosenbrock-10D',
         'Rastrigin-15D', 'Ackley-20D', 'Griewank-30D']
GRID = [f'{s}:{o}' for s in ('ens', 'botorchgp', 'svgp') for o in ('grad', 'perturb', 'cma')]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seeds', type=int, default=30)
    ap.add_argument('--jobs', type=int, default=30)
    a = ap.parse_args()
    os.environ['MBO_X1'] = '1'
    os.environ['MBO_X3'] = '1'
    import run_all
    import mbo
    assert mbo.X1_STANDARDIZE_Y and mbo.X3_MATCHED_PROTOCOL, 'selftest must run on_on'

    ref = json.load(open(REF))
    specs = [{'exp': 'mbo', 'task': t, 'variant': v, 'seed': s, 'ep': mbo.TRAIN_EP, 'k': 50,
              'beta': 2.0, 'db': False, 'db_sub': None, 'matched': False}
             for t in TASKS for v in GRID for s in range(a.seeds)]
    got = {}
    t0 = time.time()
    print(f'selftest: {len(specs)} incumbent cells, {a.jobs} workers -> vs grid_b2.0.json',
          flush=True)
    with ProcessPoolExecutor(max_workers=a.jobs) as ex:
        for i, fu in enumerate(as_completed([ex.submit(run_all._worker, s) for s in specs])):
            r = fu.result()
            if r['metrics'] is not None:
                got.setdefault(r['task'], {}).setdefault(r['variant'], {})[r['seed']] = \
                    r['metrics']['p100']
            if (i + 1) % 200 == 0:
                print(f'  {i+1}/{len(specs)} [{(time.time()-t0)/60:.1f}m]', flush=True)

    rep = {}
    for tk in TASKS:
        for cell in GRID:
            pub = ref['mbo'][tk][cell]['p100']['all']
            mine = [got[tk][cell][s] for s in range(a.seeds)]
            d = np.abs(np.asarray(pub[:a.seeds], float) - np.asarray(mine, float))
            se = float(np.std(pub[:a.seeds], ddof=1) / np.sqrt(a.seeds)) + 1e-300
            rep.setdefault(tk, {})[cell] = dict(
                max_abs_diff=float(d.max()), n_exact=int((d == 0).sum()), n=int(d.size),
                max_diff_in_se=float(d.max() / se))

    opt_roll = {}
    for tk, cells in rep.items():
        for cell, v in cells.items():
            o = cell.split(':')[1]
            s = opt_roll.setdefault(o, {'max_abs_diff': 0.0, 'n_exact': 0, 'n': 0,
                                        'max_diff_in_se': 0.0})
            s['max_abs_diff'] = max(s['max_abs_diff'], v['max_abs_diff'])
            s['max_diff_in_se'] = max(s['max_diff_in_se'], v['max_diff_in_se'])
            s['n_exact'] += v['n_exact']
            s['n'] += v['n']

    verdict = {o: ('BIT-EXACT' if s['n_exact'] == s['n'] else
                   f"within noise (max {s['max_diff_in_se']:.2f} SE)")
               for o, s in opt_roll.items()}
    out = {'meta': run_all.engine_meta(a.seeds, 2.0, mbo.K_ENS),
           'reference': 'results/kbeta/grid_b2.0.json',
           'reference_meta': ref['meta'],
           'by_optimizer': opt_roll, 'verdict': verdict, 'by_cell': rep}
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, 'selftest_repro.json')
    json.dump(out, open(p, 'w'), indent=1)
    print(json.dumps(verdict, indent=1), flush=True)
    for o, s in opt_roll.items():
        print(f"  {o:8s} exact {s['n_exact']}/{s['n']}  max|diff| {s['max_abs_diff']:.3e}",
              flush=True)
    print('wrote', p, flush=True)
    print('SELFTEST_DONE', flush=True)


if __name__ == '__main__':
    main()
