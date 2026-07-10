"""Consolidated experiment runner. Writes results/results_camera.json (merge-updates,
so partial runs accumulate and reruns overwrite only what they recompute).

  python run_all.py --exp mbo --seeds 30 --jobs 32
  python run_all.py --exp o2o --seeds 15 --jobs 32
  python run_all.py --exp beta --exp K --exp calibration --seeds 10
  python run_all.py --exp all --seeds 30 --jobs 48
  python run_all.py --smoke                 # ~2 min sanity pass on Branin

Every experiment expands to a flat list of independent (task, variant, seed) CELLS.
Cells run through a ProcessPoolExecutor (--jobs workers) and are folded back by
(exp, task, variant), aggregated over seeds. One code path, embarrassingly parallel,
merge-safe: a killed run resumes because completed cells are already in the JSON and
skipped on rerun (unless --force).
"""
import argparse
import json
import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
import numpy as np
import mbo

RESULTS = os.path.join(os.path.dirname(__file__), '..', 'results')

def out_path(db):
    return os.path.join(RESULTS, 'results_db.json' if db else 'results_camera.json')

def build_task(name, db):
    if db:
        import db_tasks
        # ponytail: reconstructs the DB task per cell (design_bench caches data on disk,
        # so make() is cheap after the first call). If DB task construction dominates
        # wall-time, switch to per-(task,method) workers that loop seeds internally.
        return db_tasks.make_db_tasks([name])[0]
    return mbo.make_tasks([name])[0]

# ---------------- cell worker (module-level = picklable for spawn/fork) ------
def _worker(spec):
    """spec: dict with exp, task, variant, seed, + params. Returns spec + metrics."""
    import torch
    torch.set_num_threads(1)                       # parallelism is across processes
    task = build_task(spec['task'], spec.get('db', False))
    e, seed, ep = spec['exp'], spec['seed'], spec['ep']
    if e == 'mbo':
        r = mbo.run_offline(task, seed, spec['variant'], beta=spec.get('beta', mbo.BETA), ep=ep)
        m = None if r is None else {'p100': r['p100'], 'p50': r['p50']}
    elif e == 'o2o':
        r = mbo.run_o2o(task, seed, k=spec['k'], select=spec['variant'], ep=ep)
        m = {'imp': r['imp'], 'on_p100': r['on_p100'], 'off_p100': r['off_p100']}
    elif e == 'beta':
        m = {'p100': mbo.run_offline(task, seed, 'lcb', beta=float(spec['variant']), ep=ep)['p100']}
    elif e == 'K':
        m = {'p100': mbo.run_offline(task, seed, 'lcb', K=int(spec['variant']), ep=ep)['p100']}
    elif e == 'calibration':
        c = mbo.run_calibration(task, seed, ep=ep)
        m = {'rho_err': c['rho_err'], 'rho_knn': c['rho_knn'], 'q_conformal': c['q_conformal'],
             'cov_conf_indist': c['cov_conf_indist'], 'cov_conf_ood': c['cov_conf_ood']}
        for b, v in c['cov_indist'].items(): m[f'cov_indist@{b}'] = v
        for b, v in c['cov_ood'].items():    m[f'cov_ood@{b}'] = v
    else:
        raise ValueError(e)
    return {**{k: spec[k] for k in ('exp', 'task', 'variant', 'seed')}, 'metrics': m}

# ---------------- per-experiment cell specs ---------------------------------
def variants(exp):
    return {'mbo': mbo.OFFLINE_METHODS,
            'o2o': ['greedy', 'diversity', 'random'],
            'beta': ['0.0', '0.5', '1.0', '2.0', '5.0'],
            'K': ['2', '3', '5', '10'],
            'calibration': ['_']}[exp]

def build_specs(exp, tasks, seeds, ep, k):
    for task in tasks:
        for v in variants(exp):
            for s in range(seeds):
                yield {'exp': exp, 'task': task.name, 'variant': v, 'seed': s, 'ep': ep, 'k': k}

# ---------------- json fold -------------------------------------------------
def agg(vals):
    vals = [v for v in vals if v is not None]
    if not vals: return None
    return {'mean': float(np.mean(vals)), 'std': float(np.std(vals)), 'all': [float(v) for v in vals]}

def load(out):
    if os.path.exists(out):
        with open(out) as f: return json.load(f)
    return {}

def save(R, out):
    tmp = out + '.tmp'
    with open(tmp, 'w') as f: json.dump(R, f, indent=1)
    os.replace(tmp, out)                            # atomic — survives a kill mid-write

def have(R, exp, task, variant, seeds):
    """Cell already complete for all requested seeds? (merge-safe resume)"""
    try:
        node = R[exp][task][variant]
        anymetric = next(iter(node.values()))
        return anymetric.get('all') is not None and len(anymetric['all']) >= seeds
    except (KeyError, StopIteration, AttributeError):
        return False

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--exp', action='append', choices=['mbo', 'o2o', 'beta', 'K', 'calibration', 'all'])
    ap.add_argument('--seeds', type=int, default=30)
    ap.add_argument('--tasks', nargs='*', default=None)
    ap.add_argument('--k', type=int, default=50)
    ap.add_argument('--jobs', type=int, default=max(1, (os.cpu_count() or 2) - 1))
    ap.add_argument('--force', action='store_true', help='recompute cells already in the JSON')
    ap.add_argument('--db', action='store_true', help='run on Design-Bench tasks -> results_db.json')
    ap.add_argument('--smoke', action='store_true')
    a = ap.parse_args()
    out = out_path(a.db)

    if a.smoke:
        tasks, seeds, ep, exps, a.k, a.jobs = mbo.make_tasks(['Branin-2D']), 2, 3, ['mbo', 'o2o', 'beta', 'K', 'calibration'], 10, 2
    elif a.db:
        import db_tasks
        names = a.tasks or list(db_tasks.TASKS)
        tasks, seeds, ep = [type('N', (), {'name': n})() for n in names], a.seeds, mbo.TRAIN_EP  # names only; workers build
        exps = a.exp or ['mbo']
        if 'all' in exps: exps = ['mbo', 'o2o', 'calibration']    # beta/K sweeps are synthetic-only
    else:
        tasks, seeds, ep = mbo.make_tasks(a.tasks), a.seeds, mbo.TRAIN_EP
        exps = a.exp or ['mbo']
        if 'all' in exps: exps = ['mbo', 'o2o', 'beta', 'K', 'calibration']

    R = load(out)
    specs = [{**s, 'db': a.db} for e in exps for s in build_specs(e, tasks, seeds, ep, a.k)]
    if not a.force:
        specs = [s for s in specs if not have(R, s['exp'], s['task'], s['variant'], seeds)]
    # group results as they land: R[exp][task][variant][metric] = agg over seeds
    buf = {}                                        # (exp,task,variant) -> {metric: {seed: val}}
    t0, done = time.time(), 0
    print(f'{len(specs)} cells, {a.jobs} workers', flush=True)
    with ProcessPoolExecutor(max_workers=a.jobs) as ex:
        futs = {ex.submit(_worker, s): s for s in specs}
        for fut in as_completed(futs):
            r = fut.result(); done += 1
            if r['metrics'] is None:                # e.g. gp_grad without botorch
                continue
            key = (r['exp'], r['task'], r['variant'])
            slot = buf.setdefault(key, {})
            for mname, mval in r['metrics'].items():
                slot.setdefault(mname, {})[r['seed']] = mval
            # fold + checkpoint every 25 cells (atomic write => safe)
            if done % 25 == 0 or done == len(specs):
                for (e, tk, v), metrics in buf.items():
                    node = R.setdefault(e, {}).setdefault(tk, {}).setdefault(v, {})
                    for mname, seedmap in metrics.items():
                        node[mname] = agg([seedmap[s] for s in sorted(seedmap)])
                save(R, out)
                print(f'  {done}/{len(specs)}  [{(time.time()-t0)/60:.1f}m]', flush=True)
    save(R, out)
    print(f'done {done} cells in {(time.time()-t0)/60:.1f} min -> {os.path.abspath(out)}', flush=True)

if __name__ == '__main__':
    main()
