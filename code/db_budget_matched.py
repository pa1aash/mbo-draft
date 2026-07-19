"""0C -- budget-matched optimizer arm on Design-Bench (DBM1/DBM2).

The synthetic arm (0A.3) equalized surrogate-query budgets on the seven synthetic tasks and
confirmed the optimizer null there. Design-Bench was never re-run under matching, which is
why the DB optimizer axis ships PROVISIONAL: eta2_opt leads eta2_surr in all four corners
with the budget confound (D08) unremoved. This is the DB counterpart.

Protocol, mirroring code/budget_matched.py:
  NATIVE (control) the incumbent settings, unmatched -- the within-runner baseline.
  UP     (primary)  everyone gets THAT CORNER's native gradient budget; grad is unchanged.
  DOWN   (secondary) everyone gets that corner's native perturbation budget.

The NATIVE level is not redundant with the published corner files. This runner fits each
surrogate ONCE per (task, seed) and hands it to all three optimizers, whereas run_all
rebuilds it per cell, so the global-numpy RNG stream perturb draws from differs. Comparing
matched numbers against the published unmatched ones would therefore confound budget with
call order. NATIVE is the control that keeps the comparison inside one protocol; it is also
reported against the published corners as a validity check.

All three levels share one surrogate fit per (task, seed), which is what makes the arm
affordable -- on DB the fits dominate wall-clock and the optimizers are seconds.

The per-corner part matters and is a genuine departure from the synthetic arm, which ran
on_on only. X3 changes the query accounting: with X3 on, grad rescores its whole trajectory
pool through _select_top (Q = 256*(2*steps+1)); with X3 off it returns the final iterate and
never rescores (Q = 256*steps). Matching every corner to a single global Q would hand grad
2x its native budget in the X3-off corners -- the opposite of "grad unchanged". So the target
is each corner's own measured grad Q, and the optimizer parameters are solved per corner.

Achieved Q is instrumented per cell and reported next to the target; cells deviating >5% are
flagged, not silently accepted.

Output is written in the schema analyze_db.py already reads, so the matched numbers go
through the SAME estimators as the published corner numbers with no re-implementation:
  results/db_budget/corner_<tag>_<level>_db.json         (5 non-mujoco tasks)
  results/db_budget/corner_<tag>_<level>_mujoco_db.json  (Ant + DKitty)

  MBO_X1=1 MBO_X3=1 python db_budget_matched.py --corner on_on --level up --seeds 16
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
SURR3 = ['ens', 'botorchgp', 'svgp']
OPT3 = ['perturb', 'grad', 'cma']
DB_SUB = 8000
CORNERS = {'off_off': (0, 0), 'on_off': (1, 0), 'off_on': (0, 1), 'on_on': (1, 1)}

# Query-count identities, verified against the instrumented probe (see DB_BUDGET_MATCH.md).
#   X3 on : grad 256*(2s+1) | perturb 512 + 768R | cma 512 + 2F
#   X3 off: grad 256*s      | perturb 256 + 768R | cma 512 + 2F
# Native (incumbent) settings are steps=100, R=5, and CMA's convergence-limited spend.
NATIVE_GRAD = {1: 51456, 0: 25600}          # keyed by X3
NATIVE_PERTURB = {1: 4352, 0: 4096}


def solve(x3, Q):
    """Optimizer parameters that spend Q under this corner's accounting."""
    if x3:
        return dict(grad_steps=max(1, round((Q / 256 - 1) / 2)),
                    perturb_rounds=max(1, round((Q - 512) / 768)),
                    cma_fevals=max(1, round((Q - 512) / 2)))
    return dict(grad_steps=max(1, round(Q / 256)),
                perturb_rounds=max(1, round((Q - 256) / 768)),
                cma_fevals=max(1, round((Q - 512) / 2)))


def levels_for(corner):
    x3 = CORNERS[corner][1]
    return {'native': dict(Q=None, grad_steps=100, perturb_rounds=5, cma_fevals=None),
            'up': dict(Q=NATIVE_GRAD[x3], **solve(x3, NATIVE_GRAD[x3])),
            'down': dict(Q=NATIVE_PERTURB[x3], **solve(x3, NATIVE_PERTURB[x3]))}


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


def _chunked(score_np, a, chunk=4096):
    """Score a large array in slices. At the UP level CMA's pool reaches ~50k points; on GFP
    (d~4700) scoring that in one call through a GP posterior is a large transient allocation
    and took the pool down in the synthetic arm. Chunking is numerically identical."""
    return np.concatenate([score_np(a[i:i + chunk]) for i in range(0, len(a), chunk)])


def _cma_fixed(mbo, score_np, x0, fevals, seed):
    """CMA spending a FIXED feval budget, via restarts. Disabling tolfun/tolx alone is not
    enough -- a converged CMA still stops on noeffectaxis/conditioncov -- so each stop is
    followed by a fresh run reseeded at the incumbent best with the remaining budget. Ported
    verbatim from code/budget_matched.py so the DB and synthetic arms share one CMA."""
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
        if used == n_before:
            break
        restart += 1
    allc = np.concatenate(pool)
    return allc[np.argsort(_chunked(score_np, allc))[-mbo.TOP:]]


def _cell(spec):
    """One (corner, task, seed). Fits each surrogate once and runs every level's optimizer
    settings against it, so the expensive part is paid once."""
    import torch
    torch.set_num_threads(1)
    x1, x3 = CORNERS[spec['corner']]
    os.environ['MBO_X1'] = str(x1)
    os.environ['MBO_X3'] = str(x3)
    import importlib
    import mbo
    importlib.reload(mbo)
    assert bool(mbo.X1_STANDARDIZE_Y) == bool(x1) and bool(mbo.X3_MATCHED_PROTOCOL) == bool(x3)
    import run_all
    LV = levels_for(spec['corner'])
    t = run_all.build_task(spec['task'], True, DB_SUB)
    seed = spec['seed']
    np.random.seed(seed)
    torch.manual_seed(seed)
    x, y = t.data()
    x0 = mbo.init_candidates(x, y, seed)
    out = {lv: {} for lv in LV}
    for surr in SURR3:
        f_t, f_n, _ = mbo.build_surrogate(surr, x, y, t.dim, seed, mbo.BETA,
                                          mbo.TRAIN_EP, mbo.K_ENS)
        if f_n is None:
            continue                                     # MISSING stays MISSING
        for lv, L in LV.items():
            for opt in OPT3:
                c = Counter()
                t0 = time.time()
                if opt == 'grad':
                    if f_t is None:
                        continue
                    xf = mbo.grad_opt(c.th(f_t), torch.FloatTensor(x0), steps=L['grad_steps'])
                elif opt == 'perturb':
                    xf = mbo.perturb_opt(c.np(f_n), x0, rounds=L['perturb_rounds'])
                elif L['cma_fevals'] is None:            # native CMA = incumbent cma_opt
                    xf = mbo.cma_opt(c.np(f_n), x0, seed=seed)
                else:
                    xf = _cma_fixed(mbo, c.np(f_n), x0, L['cma_fevals'], seed)
                if xf is None:
                    continue
                p100, p50 = mbo.eval_designs(t, xf)
                out[lv][f'{surr}:{opt}'] = dict(p100=float(p100), p50=float(p50),
                                                q=int(c.n), secs=round(time.time() - t0, 1))
    return spec, out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--corner', required=True, choices=list(CORNERS))
    ap.add_argument('--seeds', type=int, default=16)
    ap.add_argument('--jobs', type=int, default=12)
    ap.add_argument('--tasks', default='')
    ap.add_argument('--mujoco', action='store_true', help='write the mujoco files instead')
    a = ap.parse_args()
    tasks = a.tasks.split(',') if a.tasks else (MUJOCO if a.mujoco else NONMUJOCO)
    specs = [dict(task=t, seed=s, corner=a.corner) for t in tasks for s in range(a.seeds)]
    suffix = '_mujoco_db' if a.mujoco else '_db'
    os.makedirs(OUT, exist_ok=True)

    raw = {}
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=a.jobs) as ex:
        futs = [ex.submit(_cell, sp) for sp in specs]
        for i, fu in enumerate(as_completed(futs)):
            sp, r = fu.result()
            for lv, cells in r.items():
                for c, v in cells.items():
                    d = raw.setdefault(lv, {}).setdefault(sp['task'], {}).setdefault(c, {})
                    for m in ('p100', 'p50', 'q', 'secs'):
                        d.setdefault(m, []).append(v[m])
            print(f'[{i+1}/{len(specs)}] {a.corner} {sp["task"]:16s} seed{sp["seed"]:<3d} '
                  f'{sum(len(c) for c in r.values())} cells  {time.time()-t0:.0f}s', flush=True)

    import run_all
    import mbo

    def agg(v):
        return dict(mean=float(np.mean(v)), std=float(np.std(v)), all=list(map(float, v)))

    for lv, tsk in raw.items():
        L = levels_for(a.corner)[lv]
        qa = {}
        for o in OPT3:
            qs = [q for cs in tsk.values() for c, d in cs.items()
                  if c.endswith(':' + o) for q in d['q']]
            if not qs:
                continue
            e = dict(median=float(np.median(qs)), min=int(np.min(qs)), max=int(np.max(qs)),
                     target=L['Q'])
            if L['Q']:
                e['pct_dev_median'] = round(100 * (np.median(qs) - L['Q']) / L['Q'], 2)
                e['frac_cells_over_5pct'] = float(np.mean(
                    np.abs(np.array(qs) - L['Q']) / L['Q'] > 0.05))
            qa[o] = e
        path = os.path.join(OUT, f'corner_{a.corner}_{lv}{suffix}.json')
        new = {t: {c: {m: agg(v) for m, v in d.items()} for c, d in cs.items()}
               for t, cs in tsk.items()}
        # MERGE by task: TFBind10 runs in its own low-concurrency pass (its 4^10 build is
        # hostile to a wide fork pool), so a corner's file is filled by more than one
        # invocation. Task keys are disjoint across passes; a repeated task is overwritten,
        # never blended, so a re-run of one task cannot silently mix two engines' seeds.
        prev = json.load(open(path)) if os.path.exists(path) else {}
        if prev.get('corner') not in (None, a.corner) or prev.get('level') not in (None, lv):
            raise SystemExit(f'{path}: refusing to merge {prev.get("corner")}/'
                             f'{prev.get("level")} with {a.corner}/{lv}')
        merged = {**prev.get('mbo', {}), **new}
        out = {'meta': run_all.engine_meta(a.seeds, mbo.BETA, mbo.K_ENS),
               'level': lv, 'corner': a.corner, 'level_config': L,
               'achieved_q': {**prev.get('achieved_q', {}), **qa},
               'db_subsample': DB_SUB, 'mbo': merged}
        with open(path, 'w') as f:
            json.dump(out, f, indent=2)
        print(f'--- {a.corner}/{lv} target Q={L["Q"]} params={L} ---')
        print(json.dumps(qa, indent=2))
        print('wrote', path)


if __name__ == '__main__':
    main()
