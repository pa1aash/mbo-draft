"""0C step 1 -- MEASURE each optimizer's effective surrogate-query budget on Design-Bench.

The synthetic arm (0A.3) established that the three optimizers spend wildly unequal
surrogate-query budgets and that eta2_opt must be read at a matched budget. That arm ran on
the seven synthetic tasks only, which is why the Design-Bench optimizer axis is still
PROVISIONAL. This probe is the DB counterpart of code/budget_probe.py: it instruments Q
rather than deriving it, because cma_opt's `budget=3000` is a maxfevals CAP that pycma
rarely reaches (it stops on tolfun/tolx/noeffectaxis first) and because CMA's population
size scales with the design dimension, which on DB ranges from 32 (TFBind8) to ~5,000 (GFP).

Q is defined exactly as in the synthetic probe: TOTAL surrogate evaluations per cell,
search plus the final `_select_top` selection pass. Wall-clock per optimizer is recorded
alongside, because on DB the per-query cost is dimension-dependent and the matched level
has to be chosen against a real time budget, not just a query count.

  MBO_X1=1 MBO_X3=1 python db_budget_probe.py --seeds 3 --jobs 8
    -> results/db_budget/query_budget_db.json
"""
import argparse
import json
import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'results', 'db_budget')
NONMUJOCO = ['TFBind8', 'TFBind10', 'Superconductor', 'GFP', 'UTR']
MUJOCO = ['AntMorphology', 'DKitty']
SURR = ['ens', 'botorchgp', 'svgp']
OPT = ['grad', 'perturb', 'cma']
DB_SUB = 8000                      # the corner runs' --db-subsample default


class Counter:
    """Wraps a scorer, counting the points it scores. Same accounting as the synthetic
    probe: the _select_top pass is per-optimizer surrogate cost and is counted."""

    def __init__(s):
        s.n = 0

    def wrap_np(s, f):
        def g(a):
            s.n += len(a)
            return f(a)
        return g

    def wrap_torch(s, f):
        def g(t):
            s.n += t.shape[0]
            return f(t)
        return g


CORNERS = {'off_off': (0, 0), 'on_off': (1, 0), 'off_on': (0, 1), 'on_on': (1, 1)}


def _cell(spec):
    import torch
    torch.set_num_threads(1)
    x1, x3 = CORNERS[spec.get('corner', 'on_on')]
    os.environ['MBO_X1'] = str(x1)
    os.environ['MBO_X3'] = str(x3)
    import importlib
    import mbo
    importlib.reload(mbo)
    assert bool(mbo.X1_STANDARDIZE_Y) == bool(x1) and bool(mbo.X3_MATCHED_PROTOCOL) == bool(x3)
    import run_all
    t = run_all.build_task(spec['task'], True, DB_SUB)
    seed = spec['seed']
    np.random.seed(seed)
    torch.manual_seed(seed)
    x, y = t.data()
    x0 = mbo.init_candidates(x, y, seed)
    out = {}
    for surr in SURR:
        t0 = time.time()
        f_t, f_n, _ = mbo.build_surrogate(surr, x, y, t.dim, seed,
                                          mbo.BETA, mbo.TRAIN_EP, mbo.K_ENS)
        fit_s = time.time() - t0
        if f_n is None:
            continue
        for opt in OPT:
            c = Counter()
            t0 = time.time()
            if opt == 'grad':
                if f_t is None:
                    continue
                mbo.grad_opt(c.wrap_torch(f_t), torch.FloatTensor(x0), steps=mbo.OPT_STEPS)
            elif opt == 'perturb':
                mbo.perturb_opt(c.wrap_np(f_n), x0)
            else:
                if mbo.cma_opt(c.wrap_np(f_n), x0, seed=seed) is None:
                    continue
            out[f'{surr}:{opt}'] = dict(q=int(c.n), secs=round(time.time() - t0, 2),
                                        fit_secs=round(fit_s, 2))
    return spec, dict(dim=int(t.dim), n=int(len(x)), cells=out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seeds', type=int, default=3)
    ap.add_argument('--jobs', type=int, default=8)
    ap.add_argument('--tasks', default='')
    ap.add_argument('--out', default='query_budget_db.json')
    ap.add_argument('--corner', default='on_on')
    a = ap.parse_args()
    tasks = a.tasks.split(',') if a.tasks else NONMUJOCO + MUJOCO
    specs = [dict(task=t, seed=s, corner=a.corner) for t in tasks for s in range(a.seeds)]

    rows, dims = [], {}
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=a.jobs) as ex:
        futs = [ex.submit(_cell, sp) for sp in specs]
        for i, fu in enumerate(as_completed(futs)):
            sp, r = fu.result()
            dims[sp['task']] = dict(dim=r['dim'], n=r['n'])
            for cell, v in r['cells'].items():
                rows.append(dict(task=sp['task'], seed=sp['seed'], cell=cell, **v))
            print(f'[{i+1}/{len(specs)}] {sp["task"]:16s} seed{sp["seed"]} d={r["dim"]:<5d} '
                  + ' '.join(f'{c}={v["q"]}' for c, v in r['cells'].items() if 'cma' in c)
                  + f'  {time.time()-t0:.0f}s', flush=True)

    import run_all
    import mbo

    def q_of(opt, task=None):
        v = [r['q'] for r in rows if r['cell'].endswith(':' + opt)
             and (task is None or r['task'] == task)]
        return v

    agg = {}
    for o in OPT:
        v = q_of(o)
        agg[o] = dict(median=float(np.median(v)), mean=float(np.mean(v)),
                      min=int(np.min(v)), max=int(np.max(v)), n=len(v),
                      median_secs=float(np.median([r['secs'] for r in rows
                                                   if r['cell'].endswith(':' + o)])))
    rep = {'meta': run_all.engine_meta(a.seeds, mbo.BETA, mbo.K_ENS),
           'definition': 'Q = candidate points scored by the surrogate per cell, search plus '
                         'the final _select_top selection pass (identical to '
                         'code/budget_probe.py, so DB and synthetic Q are comparable)',
           'db_subsample': DB_SUB, 'task_dims': dims, 'corner': a.corner,
           'aggregate': agg,
           'per_task': {t: {o: (float(np.median(q_of(o, t))) if q_of(o, t) else None)
                            for o in OPT} for t in tasks},
           'per_task_secs': {t: {o: (float(np.median([r['secs'] for r in rows
                                                      if r['task'] == t
                                                      and r['cell'].endswith(':' + o)]))
                                     if q_of(o, t) else None) for o in OPT} for t in tasks},
           'rows': rows}
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, a.out)
    with open(p, 'w') as f:
        json.dump(rep, f, indent=2)
    print(json.dumps(agg, indent=2))
    print(json.dumps(rep['per_task'], indent=2))
    print('wrote', p)


if __name__ == '__main__':
    main()
