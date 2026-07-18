"""0A.3 -- budget-matched optimizer arm (BM1), pre-registered in PREREGISTRATION_V3.md.

The published eta2_opt (~0.005 at beta=2) is measured with wildly unequal surrogate-query
budgets: gradient 51,456 vs perturbation 4,352 vs CMA ~6,528 (measured, budget_probe.py).
Gradient gets 11.8x perturbation's budget, so "the optimizer doesn't matter" may just mean
"the budget imbalance happened to cancel". This reruns the 3x3 with Q equalized.

Two pre-registered levels:
  UP   (primary)   Q = 51,456 -- everyone gets gradient's budget, nobody is crippled.
  DOWN (secondary) Q =  4,352 -- everyone gets perturbation's budget.

Achieved Q is re-instrumented per cell and reported next to the target; cells deviating
>5% are flagged rather than silently accepted.

Note pycma stops on tolfun/tolx convergence long before maxfevals, so a matched CMA needs
those tolerances disabled or the cap never binds. `_cma_fixed` below does that; it is kept
local rather than patched into mbo.cma_opt so the incumbent grid stays byte-identical.

  MBO_X1=1 MBO_X3=1 python budget_matched.py --seeds 30 --jobs 14
    -> results/budget/budget_matched.json
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
SURR3 = ['ens', 'botorchgp', 'svgp']
OPT3 = ['perturb', 'grad', 'cma']

# Pre-registered settings. grad q = 256*(2*steps+1); perturb q = 512 + 3*R*256;
# cma q = 512 + 2*fevals (initial scoring + fevals + final pool rescore).
LEVELS = {
    'up':   dict(Q=51456, grad_steps=100, perturb_rounds=66, cma_fevals=25472),
    'down': dict(Q=4352,  grad_steps=8,   perturb_rounds=5,  cma_fevals=1920),
}


class Counter:
    def __init__(s):
        s.n = 0

    def np(s, f):
        def g(a):
            s.n += len(a)
            return f(a)
        return g

    def th(s, f):
        def g(t):
            s.n += t.shape[0]
            return f(t)
        return g


def _cma_fixed(mbo, score_np, x0, fevals, seed):
    """CMA spending a FIXED feval budget, via restarts.

    Disabling tolfun/tolx alone is not enough: a converged CMA still stops on
    noeffectaxis/noeffectcoord/conditioncov, so on low-dim tasks maxfevals never binds
    (measured: 5,144 achieved against a 25,472 cap on Branin-2D). The standard way to
    spend a large budget with CMA is restarts, so each stop is followed by a fresh run
    reseeded at the incumbent best with the remaining budget, until it is exhausted.
    This is IPOP-style in spirit but keeps sigma0 and popsize fixed, so the only thing
    that differs from the incumbent cma_opt is the number of fevals."""
    try:
        import cma
    except ImportError:
        return None
    dim = x0.shape[1]
    pool = [x0]
    s0 = score_np(x0)
    x_start = x0[int(np.argmax(s0))]
    best_s = float(np.max(s0))
    used, restart = 0, 0
    while used < fevals:
        es = cma.CMAEvolutionStrategy(x_start.tolist(), 0.2, {
            'bounds': [0, 1], 'maxfevals': fevals - used, 'verbose': -9,
            'seed': seed + 1 + 1000 * restart, 'CMA_diagonal': dim > 500,
            'tolfun': 0, 'tolfunhist': 0, 'tolx': 0, 'tolfunrel': 0})
        n_before = used
        while not es.stop():
            sols = es.ask()
            arr = np.clip(np.array(sols, dtype=np.float32), 0, 1)
            sc = score_np(arr)
            es.tell(sols, [-v for v in sc])
            pool.append(arr)
            used += len(arr)
            j = int(np.argmax(sc))
            if sc[j] > best_s:
                best_s, x_start = float(sc[j]), arr[j]
        if used == n_before:                    # degenerate: cannot spend, avoid infinite loop
            break
        restart += 1
    allc = np.concatenate(pool)
    return allc[np.argsort(score_np(allc))[-mbo.TOP:]]


def _cell(spec):
    import torch
    torch.set_num_threads(1)
    os.environ['MBO_X1'] = '1'
    os.environ['MBO_X3'] = '1'
    import importlib
    import mbo
    importlib.reload(mbo)
    assert mbo.X1_STANDARDIZE_Y and mbo.X3_MATCHED_PROTOCOL, 'BM1 must run on_on'
    L = LEVELS[spec['level']]
    t = mbo.make_tasks([spec['task']])[0]
    seed = spec['seed']
    np.random.seed(seed)
    torch.manual_seed(seed)
    x, y = t.data()
    x0 = mbo.init_candidates(x, y, seed)
    out = {}
    for surr in SURR3:
        f_t, f_n, _ = mbo.build_surrogate(surr, x, y, t.dim, seed, mbo.BETA,
                                          mbo.TRAIN_EP, mbo.K_ENS)
        if f_n is None:
            continue                                     # MISSING stays MISSING
        for opt in OPT3:
            c = Counter()
            if opt == 'grad':
                if f_t is None:
                    continue
                xf = mbo.grad_opt(c.th(f_t), torch.FloatTensor(x0), steps=L['grad_steps'])
            elif opt == 'perturb':
                xf = mbo.perturb_opt(c.np(f_n), x0, rounds=L['perturb_rounds'])
            else:
                xf = _cma_fixed(mbo, c.np(f_n), x0, L['cma_fevals'], seed)
                if xf is None:
                    continue
            p100, p50 = mbo.eval_designs(t, xf)
            out[f'{surr}:{opt}'] = dict(p100=float(p100), p50=float(p50), q=int(c.n))
    return spec, out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seeds', type=int, default=30)
    ap.add_argument('--jobs', type=int, default=14)
    ap.add_argument('--levels', default='up,down')
    a = ap.parse_args()
    levels = a.levels.split(',')
    specs = [dict(task=t, seed=s, level=lv)
             for lv in levels for t in TASKS for s in range(a.seeds)]
    acc = {}
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=a.jobs) as ex:
        futs = [ex.submit(_cell, sp) for sp in specs]
        for i, fu in enumerate(as_completed(futs)):
            sp, r = fu.result()
            for c, v in r.items():
                d = acc.setdefault(sp['level'], {}).setdefault(sp['task'], {}).setdefault(c, {})
                for m in ('p100', 'p50', 'q'):
                    d.setdefault(m, []).append(v[m])
            print(f'[{i+1}/{len(specs)}] {sp["level"]:4s} {sp["task"]:16s} '
                  f'seed{sp["seed"]:<3d} {len(r)} cells  {time.time()-t0:.0f}s', flush=True)

    import run_all
    import mbo
    agg = lambda v: dict(mean=float(np.mean(v)), std=float(np.std(v)), all=list(map(float, v)))
    out = {'meta': run_all.engine_meta(a.seeds, mbo.BETA, mbo.K_ENS), 'levels': LEVELS,
           'runs': {}}
    for lv, tasks in acc.items():
        out['runs'][lv] = {'mbo': {t: {c: {m: agg(v) for m, v in d.items()}
                                       for c, d in cs.items()} for t, cs in tasks.items()}}
        # achieved-Q audit, per the pre-registration
        tgt = LEVELS[lv]['Q']
        qa = {}
        for o in OPT3:
            qs = [q for t, cs in tasks.items() for c, d in cs.items()
                  if c.endswith(':' + o) for q in d['q']]
            if qs:
                qa[o] = dict(median=float(np.median(qs)), min=int(np.min(qs)),
                             max=int(np.max(qs)), target=tgt,
                             pct_dev_median=round(100 * (np.median(qs) - tgt) / tgt, 2),
                             frac_cells_over_5pct=float(np.mean(
                                 np.abs(np.array(qs) - tgt) / tgt > 0.05)))
        out['runs'][lv]['achieved_q'] = qa
        print(f'--- achieved Q, level {lv} (target {tgt}) ---')
        print(json.dumps(qa, indent=2))
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, 'budget_matched.json'), 'w') as f:
        json.dump(out, f, indent=2)
    print('wrote', os.path.join(OUT, 'budget_matched.json'))


if __name__ == '__main__':
    main()
