"""Consolidated experiment runner. Writes results/results_camera.json (merge-updates,
so partial runs accumulate and reruns overwrite only what they recompute).

  python run_all.py --exp mbo --seeds 10
  python run_all.py --exp o2o --seeds 10
  python run_all.py --exp beta --exp K --exp calibration
  python run_all.py --exp all --seeds 10
  python run_all.py --smoke          # ~2 min sanity pass on Branin
"""
import argparse
import json
import os
import time
import numpy as np
import mbo

OUT = os.path.join(os.path.dirname(__file__), '..', 'results', 'results_camera.json')

def load():
    if os.path.exists(OUT):
        with open(OUT) as f: return json.load(f)
    return {}

def save(R):
    with open(OUT, 'w') as f: json.dump(R, f, indent=1)

def agg(vals):
    return {'mean': float(np.mean(vals)), 'std': float(np.std(vals)), 'all': [float(v) for v in vals]}

def exp_mbo(R, tasks, seeds, ep):
    R.setdefault('mbo', {})
    for task in tasks:
        R['mbo'].setdefault(task.name, {})
        for m in mbo.OFFLINE_METHODS:
            t0 = time.time(); p100s, p50s = [], []
            for s in range(seeds):
                r = mbo.run_offline(task, s, m, ep=ep)
                if r is None:
                    print(f'  {task.name} {m}: SKIPPED (botorch not installed)'); break
                p100s.append(r['p100']); p50s.append(r['p50'])
            if p100s:
                R['mbo'][task.name][m] = {'p100': agg(p100s), 'p50': agg(p50s)}
                print(f'  {task.name:16s} {m:12s} p100={np.mean(p100s):9.3f}±{np.std(p100s):.3f}  [{time.time()-t0:.0f}s]')
            save(R)

def exp_o2o(R, tasks, seeds, k, ep):
    R.setdefault('o2o', {})
    for task in tasks:
        R['o2o'].setdefault(task.name, {}).setdefault(str(k), {})
        for sel in ('greedy', 'diversity', 'random'):
            t0 = time.time()
            runs = [mbo.run_o2o(task, s, k=k, select=sel, ep=ep) for s in range(seeds)]
            R['o2o'][task.name][str(k)][sel] = {
                'imp': agg([r['imp'] for r in runs]),
                'on_p100': agg([r['on_p100'] for r in runs]),
                'off_p100': agg([r['off_p100'] for r in runs])}
            print(f'  {task.name:16s} k={k} {sel:9s} p100={np.mean([r["on_p100"] for r in runs]):9.3f}  [{time.time()-t0:.0f}s]')
            save(R)

def exp_beta(R, tasks, seeds, ep):
    R.setdefault('beta', {})
    for task in tasks:
        R['beta'].setdefault(task.name, {})
        for b in (0.0, 0.5, 1.0, 2.0, 5.0):
            vals = [mbo.run_offline(task, s, 'lcb', beta=b, ep=ep)['p100'] for s in range(seeds)]
            R['beta'][task.name][str(b)] = agg(vals)
            save(R)
        print(f'  {task.name}: ' + ', '.join(f'b={b}:{R["beta"][task.name][str(b)]["mean"]:.2f}' for b in (0.0, 0.5, 1.0, 2.0, 5.0)))

def exp_K(R, tasks, seeds, ep):
    R.setdefault('K', {})
    for task in tasks:
        R['K'].setdefault(task.name, {})
        for K in (2, 3, 5, 10):
            vals = [mbo.run_offline(task, s, 'lcb', K=K, ep=ep)['p100'] for s in range(seeds)]
            R['K'][task.name][str(K)] = agg(vals)
            save(R)
        print(f'  {task.name}: ' + ', '.join(f'K={K}:{R["K"][task.name][str(K)]["mean"]:.2f}' for K in (2, 3, 5, 10)))

def exp_calibration(R, tasks, seeds, ep):
    R.setdefault('calibration', {})
    for task in tasks:
        rs = [mbo.run_calibration(task, s, ep=ep) for s in range(seeds)]
        R['calibration'][task.name] = {
            'rho_err': agg([r['rho_err'] for r in rs]),
            'rho_knn': agg([r['rho_knn'] for r in rs])}
        print(f'  {task.name}: rho_err={R["calibration"][task.name]["rho_err"]["mean"]:.3f}')
        save(R)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--exp', action='append', choices=['mbo', 'o2o', 'beta', 'K', 'calibration', 'all'], default=None)
    ap.add_argument('--seeds', type=int, default=10)
    ap.add_argument('--tasks', nargs='*', default=None, help='task names, default all 7')
    ap.add_argument('--k', type=int, default=50, help='O2O online budget')
    ap.add_argument('--smoke', action='store_true')
    a = ap.parse_args()

    if a.smoke:
        tasks, seeds, ep = mbo.make_tasks(['Branin-2D']), 1, 3
        exps = ['mbo', 'o2o', 'beta', 'K', 'calibration']
        a.k = 10
    else:
        tasks = mbo.make_tasks(a.tasks)
        seeds, ep = a.seeds, mbo.TRAIN_EP
        exps = a.exp or ['mbo']
        if 'all' in exps: exps = ['mbo', 'o2o', 'beta', 'K', 'calibration']

    R = load()
    t0 = time.time()
    for e in exps:
        print(f'== {e} ==', flush=True)
        # ponytail: O2O/ablations on 4-5 tasks by default would be a judgment call;
        # runner takes whatever --tasks says, paper decides the subset.
        {'mbo': exp_mbo, 'o2o': exp_o2o, 'beta': exp_beta, 'K': exp_K,
         'calibration': exp_calibration}[e](R, tasks, seeds, **({'k': a.k, 'ep': ep} if e == 'o2o' else {'ep': ep}))
    print(f'done in {(time.time()-t0)/60:.1f} min -> {os.path.abspath(OUT)}')

if __name__ == '__main__':
    main()
