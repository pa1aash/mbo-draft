"""Statistical analysis for the paper. Reads results/results_camera.json and prints
every number the stats sections need: per-task Wilcoxon vs a reference method with
Holm-Bonferroni correction, Friedman test, bootstrap mean-rank CIs.

  python stats.py                     # ref=lcb, all methods present in the file
  python stats.py --ref gp --methods lcb lcb_perturb gp gp_grad

Verified against the published Table 4: this procedure reproduces all 14 legacy
p-values, Friedman p=0.565, and the bootstrap rank CIs exactly when pointed at
the legacy results files' seed arrays.
"""
import argparse
import itertools
import json
import os
import numpy as np
from scipy import stats

OUT = os.path.join(os.path.dirname(__file__), '..', 'results', 'results_camera.json')

def holm(pvals):
    """Holm-Bonferroni adjusted p-values, input order preserved."""
    n = len(pvals)
    order = np.argsort(pvals)
    adj = np.empty(n)
    running = 0.0
    for rank, i in enumerate(order):
        running = max(running, (n - rank) * pvals[i])
        adj[i] = min(1.0, running)
    return adj

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--results', default=OUT)
    ap.add_argument('--ref', default='lcb')
    ap.add_argument('--methods', nargs='*', default=None)
    ap.add_argument('--metric', default='p100')
    a = ap.parse_args()

    with open(a.results) as f:
        mbo = json.load(f)['mbo']
    tasks = list(mbo)
    methods = a.methods or sorted({m for t in mbo.values() for m in t})

    def seeds(task, m):
        e = mbo[task].get(m)
        return np.array(e[a.metric]['all']) if e else None

    # -- pairwise Wilcoxon vs ref, Holm-corrected per comparison family --------
    print(f'Wilcoxon signed-rank vs {a.ref} (two-sided), Holm-corrected per family')
    for m in methods:
        if m == a.ref: continue
        rows = [(t, seeds(t, a.ref), seeds(t, m)) for t in tasks]
        rows = [(t, x, y) for t, x, y in rows if x is not None and y is not None and len(x) == len(y)]
        if not rows: continue
        praw = []
        for t, x, y in rows:
            try: praw.append(stats.wilcoxon(x, y).pvalue)
            except ValueError: praw.append(1.0)   # identical samples
        padj = holm(praw)
        print(f'  vs {m}:')
        for (t, _, _), pr, pa in zip(rows, praw, padj):
            print(f'    {t:16s} p={pr:6.3f}  p_adj={pa:6.3f}{"  *" if pa < 0.05 else ""}')

    # -- Friedman over methods common to all tasks (task means as blocks) ------
    common = [m for m in methods if all(seeds(t, m) is not None for t in tasks)]
    if len(common) >= 3:
        blocks = [[float(np.mean(seeds(t, m))) for t in tasks] for m in common]
        fr = stats.friedmanchisquare(*blocks)
        print(f'\nFriedman over {common} on {len(tasks)} tasks: chi2={fr.statistic:.2f} p={fr.pvalue:.3f}')

    # -- bootstrap mean-rank CIs ------------------------------------------------
    if len(common) >= 2:
        M = np.array([[np.mean(seeds(t, m)) for m in common] for t in tasks])  # tasks x methods
        ranks = (-M).argsort(1).argsort(1) + 1
        rng = np.random.default_rng(0)
        boots = np.array([ranks[rng.integers(0, len(tasks), len(tasks))].mean(0) for _ in range(10000)])
        print('\nBootstrap mean ranks (10k resamples over tasks):')
        for i, m in enumerate(common):
            lo, hi = np.percentile(boots[:, i], [2.5, 97.5])
            print(f'  {m:12s} {ranks[:, i].mean():.2f}  [{lo:.2f}, {hi:.2f}]')

if __name__ == '__main__':
    # self-check: Holm on a known example (Holland 1988 style)
    assert np.allclose(holm([0.01, 0.04, 0.03]), [0.03, 0.06, 0.06])
    main()
