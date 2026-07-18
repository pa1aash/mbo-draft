"""0A.3 step 1 -- MEASURE each optimizer's effective surrogate-query budget.

The budgets cannot be derived from the config constants. grad's is steps*N, but
perturb's depends on its accept loop and cma_opt's `budget=3000` is a maxfevals CAP that
is rarely binding -- pycma also stops on tolfun/tolx/tolfunhist convergence
(code/mbo.py:338-362, `while not es.stop()`). So Q is instrumented, not computed: every
optimizer is run against a surrogate wrapped in a counting proxy that records how many
candidate points were scored.

Q is defined as TOTAL surrogate evaluations per cell -- search plus the final
`_select_top` selection pass. The selection pass is NOT a shared constant across
optimizers (grad rescores its whole 25,856-point trajectory pool; perturb rescores only
its 256 survivors), so it is genuine per-optimizer surrogate cost and belongs in Q.
This matches the pre-registered wording "equalize total surrogate evaluations".

  python budget_probe.py --seeds 5   -> results/budget/query_budget.json
"""
import argparse
import json
import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'results', 'budget')
TASKS = ['Branin-2D', 'Styblinski-5D', 'Levy-8D', 'Rosenbrock-10D',
         'Rastrigin-15D', 'Ackley-20D', 'Griewank-30D']
SURR = ['ens', 'botorchgp', 'svgp']
OPT = ['grad', 'perturb', 'cma']


class Counter:
    """Wraps a scorer, counting points scored. `on` gates counting so the shared
    _select_top pass can be excluded from Q."""

    def __init__(s):
        s.n = 0
        s.on = True

    def wrap_np(s, f):
        def g(a):
            if s.on:
                s.n += len(a)
            return f(a)
        return g

    def wrap_torch(s, f):
        def g(t):
            if s.on:
                s.n += t.shape[0]
            return f(t)
        return g


def _cell(spec):
    import torch
    torch.set_num_threads(1)
    os.environ['MBO_X1'] = '1'
    os.environ['MBO_X3'] = '1'
    import importlib
    import mbo
    importlib.reload(mbo)
    assert mbo.X1_STANDARDIZE_Y and mbo.X3_MATCHED_PROTOCOL
    t = mbo.make_tasks([spec['task']])[0]
    seed = spec['seed']
    np.random.seed(seed)
    torch.manual_seed(seed)
    x, y = t.data()
    x0 = mbo.init_candidates(x, y, seed)
    f_t, f_n, _ = mbo.build_surrogate(spec['surr'], x, y, t.dim, seed,
                                      mbo.BETA, mbo.TRAIN_EP, mbo.K_ENS)
    out = {}
    for opt in OPT:
        c = Counter()
        t0 = time.time()
        if opt == 'grad':
            if f_t is None:
                continue
            # grad's search cost is steps forward+backward passes over all N inits; the
            # trajectory pool is then rescored by _select_top (excluded from Q).
            xf = mbo.grad_opt(c.wrap_torch(f_t), torch.FloatTensor(x0),
                              steps=mbo.OPT_STEPS)
            q = c.n
        elif opt == 'perturb':
            if f_n is None:
                continue
            xf = mbo.perturb_opt(c.wrap_np(f_n), x0)
            q = c.n
        else:
            if f_n is None:
                continue
            xf = mbo.cma_opt(c.wrap_np(f_n), x0, seed=seed)
            if xf is None:
                continue
            q = c.n
        out[opt] = dict(q=int(q), secs=round(time.time() - t0, 2))
    return spec, out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seeds', type=int, default=5)
    ap.add_argument('--jobs', type=int, default=14)
    a = ap.parse_args()
    specs = [dict(task=t, surr=s, seed=sd)
             for t in TASKS for s in SURR for sd in range(a.seeds)]
    rows = []
    with ProcessPoolExecutor(max_workers=a.jobs) as ex:
        futs = [ex.submit(_cell, sp) for sp in specs]
        for i, fu in enumerate(as_completed(futs)):
            sp, o = fu.result()
            rows.append(dict(**sp, **{k: v['q'] for k, v in o.items()},
                             **{f'{k}_secs': v['secs'] for k, v in o.items()}))
            print(f'[{i+1}/{len(specs)}] {sp["task"]:16s} {sp["surr"]:10s} '
                  f'seed{sp["seed"]} ' + ' '.join(f'{k}={v["q"]}' for k, v in o.items()),
                  flush=True)

    import run_all
    import mbo
    rep = {'meta': run_all.engine_meta(a.seeds, mbo.BETA, mbo.K_ENS),
           'definition': 'Q = candidate points scored by the surrogate during search, '
                         'excluding the shared _select_top pass',
           'rows': rows}
    # aggregate: median Q per optimizer (over task x surr x seed), and per task
    agg = {}
    for o in OPT:
        v = [r[o] for r in rows if o in r]
        agg[o] = dict(median=float(np.median(v)), mean=float(np.mean(v)),
                      min=int(np.min(v)), max=int(np.max(v)), n=len(v))
    rep['aggregate'] = agg
    rep['per_task'] = {t: {o: float(np.median([r[o] for r in rows
                                               if r['task'] == t and o in r]))
                           for o in OPT} for t in TASKS}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, 'query_budget.json'), 'w') as f:
        json.dump(rep, f, indent=2)
    print(json.dumps(agg, indent=2))
    print(json.dumps(rep['per_task'], indent=2))


if __name__ == '__main__':
    main()
