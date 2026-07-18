"""KB5 generator: task-and-seed bootstrap 95% CIs on eta2 (surr / opt / inter).

FLAW_LEDGER P0-4: the two existing bootstraps (stats.py, run05.py) resample TASK INDICES
ONLY, on seed-collapsed means, and report mean-RANKS, not eta2. This one resamples BOTH
tasks (with replacement, 7 draws) AND, within each drawn (task, cell), the per-seed p100
values (with replacement), 10,000 resamples, and recomputes eta2 each time by the paper's
own method (per-task min-max normalize the 9 cells -> 3x3, task-unmodeled marginals --
identical to analyze_corners.eta2_from_means / run05.eta2).

Reads corner files (results/corners/corner_*.json) and any --extra grid file, plus optional
per-beta slices of a swept-beta grid. Every output row carries the source file's engine
meta so no eta2 is ever reported without its engine.

  python bootstrap_eta.py --B 10000 --out results/bootstrap_eta.json
  python bootstrap_eta.py --grids results/corners/pod_on_on_grid.json --by-beta ...
"""
import argparse
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, '..', 'results')
CORN = os.path.join(RES, 'corners')
TASKS = ['Branin-2D', 'Styblinski-5D', 'Levy-8D', 'Rosenbrock-10D',
         'Rastrigin-15D', 'Ackley-20D', 'Griewank-30D']
SURR3 = ['ens', 'botorchgp', 'svgp']
OPT3 = ['perturb', 'grad', 'cma']          # run05/analyze_corners order (rows=surr, cols=opt)
CELLS = [f'{s}:{o}' for s in SURR3 for o in OPT3]


def _eta2_from_taskmeans(taskmeans):
    """taskmeans: (T, 9) array of per-task per-cell scalar means (rows=tasks in CELLS order).
    Replicates run05.eta2 / analyze_corners.eta2_from_means EXACTLY."""
    M = []
    for row in taskmeans:
        a = np.asarray(row, float)
        lo, hi = a.min(), a.max()
        z = (a - lo) / (hi - lo) if hi > lo else np.zeros_like(a)
        M.append(z.reshape(3, 3))
    M = np.array(M)
    g = M.mean(); tot = ((M - g) ** 2).sum()
    if tot == 0:
        return dict(surr=0.0, opt=0.0, inter=0.0)
    om3, sm3 = M.mean(axis=(0, 1)), M.mean(axis=(0, 2))
    inter = M.mean(axis=0) - sm3[:, None] - om3[None, :] + g
    T = len(M)
    return dict(surr=float((T * 3 * ((sm3 - g) ** 2).sum()) / tot),
                opt=float((T * 3 * ((om3 - g) ** 2).sum()) / tot),
                inter=float((T * (inter ** 2).sum()) / tot),
                surr_marg=dict(zip(SURR3, sm3.tolist())),
                opt_marg=dict(zip(OPT3, om3.tolist())))


def load_grid_all(path, node='mbo'):
    """-> seedvals[task][cell] = list of per-seed p100. Returns (data, meta)."""
    R = json.load(open(path))
    meta = R.get('meta')
    d = R[node]
    out = {}
    for t in TASKS:
        out[t] = {}
        for c in CELLS:
            m = d.get(t, {}).get(c, {}).get('p100')
            out[t][c] = list(m['all']) if isinstance(m, dict) and m.get('all') else None
    return out, meta


def bootstrap_eta2(seedvals, B=10000, rng=None):
    """seedvals[task][cell] = list of per-seed p100 (or None). Resamples tasks (7 w/ repl)
    and seeds (w/ repl within each drawn task,cell). Returns point estimate + 95% CIs."""
    rng = rng or np.random.default_rng(0)
    tasks = [t for t in TASKS if all(seedvals[t].get(c) for c in CELLS)]
    if len(tasks) < 2:
        return None
    # point estimate: full means, no resampling
    point = _eta2_from_taskmeans(
        np.array([[float(np.mean(seedvals[t][c])) for c in CELLS] for t in tasks]))
    draws = {'surr': [], 'opt': [], 'inter': []}
    ti = np.arange(len(tasks))
    for _ in range(B):
        bt = rng.choice(ti, size=len(tasks), replace=True)
        rows = []
        for j in bt:
            t = tasks[j]
            row = []
            for c in CELLS:
                v = seedvals[t][c]
                idx = rng.integers(0, len(v), size=len(v))
                row.append(float(np.mean(np.asarray(v)[idx])))
            rows.append(row)
        e = _eta2_from_taskmeans(np.array(rows))
        for k in draws:
            draws[k].append(e[k])
    out = {'n_tasks': len(tasks), 'B': B, 'point': point}
    for k in draws:
        arr = np.array(draws[k])
        out[k] = dict(mean=float(arr.mean()),
                      ci95=[float(np.percentile(arr, 2.5)), float(np.percentile(arr, 97.5))],
                      width=float(np.percentile(arr, 97.5) - np.percentile(arr, 2.5)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--B', type=int, default=10000)
    ap.add_argument('--out', default=os.path.join(RES, 'bootstrap_eta.json'))
    ap.add_argument('--corners', nargs='*',
                    default=['off_off', 'on_off', 'off_on', 'on_on'])
    ap.add_argument('--grids', nargs='*', default=None,
                    help='extra grid JSON files (label=path) to bootstrap as-is')
    a = ap.parse_args()
    rng = np.random.default_rng(12345)
    report = {}
    for tag in a.corners:
        path = os.path.join(CORN, f'corner_{tag}.json')
        if not os.path.exists(path):
            report[tag] = {'status': 'MISSING', 'path': path}
            continue
        sv, meta = load_grid_all(path)
        res = bootstrap_eta2(sv, B=a.B, rng=rng)
        report[tag] = {'source': path, 'engine_meta': meta, 'eta2': res}
        if res:
            print(f"{tag:8} eta2_surr={res['point']['surr']:.3f} "
                  f"CI[{res['surr']['ci95'][0]:.3f},{res['surr']['ci95'][1]:.3f}] "
                  f"width={res['surr']['width']:.3f}", flush=True)
    for spec in (a.grids or []):
        label, _, path = spec.partition('=')
        if not path:
            path = label; label = os.path.basename(path)
        if not os.path.exists(path):
            report[label] = {'status': 'MISSING', 'path': path}
            continue
        sv, meta = load_grid_all(path)
        res = bootstrap_eta2(sv, B=a.B, rng=rng)
        report[label] = {'source': path, 'engine_meta': meta, 'eta2': res}
        if res:
            print(f"{label:16} eta2_surr={res['point']['surr']:.3f} "
                  f"CI[{res['surr']['ci95'][0]:.3f},{res['surr']['ci95'][1]:.3f}]", flush=True)
    json.dump(report, open(a.out, 'w'), indent=1)
    print('wrote', a.out, flush=True)


if __name__ == '__main__':
    main()
