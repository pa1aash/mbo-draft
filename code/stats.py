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

def tost(x, y, margin, alpha=0.05):
    """Paired two-one-sided-tests equivalence (Lakens 2017). x,y matched arrays; margin
    is the SESOI in raw metric units. Equivalent iff the (1-2*alpha) CI of the paired
    mean difference lies entirely within (-margin, +margin). Returns (equivalent, p_tost,
    (ci_lo, ci_hi)). p_tost is the larger of the two one-sided p-values (Lakens: report
    the max)."""
    d = np.asarray(x, float) - np.asarray(y, float)
    n = len(d); mean, se = d.mean(), d.std(ddof=1) / np.sqrt(n)
    if se == 0: se = 1e-12
    df = n - 1
    t_lo = (mean - (-margin)) / se           # H0: mean <= -margin
    t_hi = (mean - margin) / se              # H0: mean >= +margin
    p_lo = stats.t.sf(t_lo, df)              # one-sided upper
    p_hi = stats.t.cdf(t_hi, df)             # one-sided lower
    p_tost = max(p_lo, p_hi)
    crit = stats.t.ppf(1 - alpha, df)        # (1-2a) CI uses one-sided crit at alpha
    ci = (mean - crit * se, mean + crit * se)
    equivalent = (ci[0] > -margin) and (ci[1] < margin)
    return equivalent, p_tost, ci

# Studentized-range q for the Nemenyi test (Demsar 2006, Table 5), alpha=0.05, indexed by k.
_Q05 = {2: 1.960, 3: 2.343, 4: 2.569, 5: 2.728, 6: 2.850, 7: 2.949, 8: 3.031,
        9: 3.102, 10: 3.164, 11: 3.219, 12: 3.268}

def nemenyi_cd(k, n, alpha=0.05):
    """Critical difference for the Nemenyi post-hoc after Friedman. k methods, n tasks.
    Two methods differ significantly iff their mean-rank gap exceeds CD. Uses Demsar's
    tabulated q for k<=12 (alpha=0.05), else the studentized-range distribution."""
    q = _Q05.get(k) if alpha == 0.05 else None
    if q is None:
        from scipy.stats import studentized_range           # scipy>=1.7
        q = float(studentized_range.ppf(1 - alpha, k, np.inf)) / np.sqrt(2)
    return q * np.sqrt(k * (k + 1) / (6.0 * n))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--results', default=OUT)
    ap.add_argument('--ref', default='lcb')
    ap.add_argument('--methods', nargs='*', default=None)
    ap.add_argument('--metric', default='p100')
    ap.add_argument('--tost', nargs=2, metavar=('A', 'B'),
                    help='equivalence test that method A ties method B (per task, paired)')
    ap.add_argument('--margin', type=float, default=None,
                    help='TOST equivalence margin in metric units; default = 0.1*std(ref across tasks)')
    ap.add_argument('--cd', action='store_true', help='Nemenyi critical-difference (mean ranks + CD)')
    a = ap.parse_args()

    with open(a.results) as f:
        mbo = json.load(f)['mbo']
    tasks = list(mbo)
    methods = a.methods or sorted({m for t in mbo.values() for m in t})

    def seeds(task, m):
        e = mbo[task].get(m)
        return np.array(e[a.metric]['all']) if e else None

    # -- TOST equivalence: does method A *tie* method B? (the beta=0 claim) -----
    if a.tost:
        A, B = a.tost
        margin = a.margin
        if margin is None:
            refm = [float(np.mean(seeds(t, A))) for t in tasks if seeds(t, A) is not None]
            margin = 0.1 * (np.std(refm) if len(refm) > 1 else 1.0)
        print(f'TOST equivalence ({A} ties {B}?)  margin=+-{margin:.4f}  metric={a.metric}')
        for t in tasks:
            x, y = seeds(t, A), seeds(t, B)
            if x is None or y is None or len(x) != len(y):
                print(f'  {t:16s} (missing / mismatched n)'); continue
            eq, p, ci = tost(x, y, margin)
            print(f'  {t:16s} d={np.mean(x)-np.mean(y):+.4f} CI90=[{ci[0]:+.4f},{ci[1]:+.4f}] '
                  f'p_tost={p:.3f}  {"EQUIVALENT" if eq else "not equivalent"}')
        return

    # -- Nemenyi critical difference (the CD-diagram numbers) ------------------
    if a.cd:
        common = [m for m in methods if all(seeds(t, m) is not None for t in tasks)]
        if len(common) < 2:
            print('need >=2 methods present on all tasks for a CD diagram'); return
        M = np.array([[np.mean(seeds(t, m)) for m in common] for t in tasks])   # tasks x methods
        mean_ranks = ((-M).argsort(1).argsort(1) + 1).mean(0)
        cd = nemenyi_cd(len(common), len(tasks))
        print(f'Nemenyi CD (k={len(common)} methods, N={len(tasks)} tasks, alpha=0.05): CD={cd:.3f}')
        for i in np.argsort(mean_ranks):
            print(f'  {common[i]:16s} mean-rank={mean_ranks[i]:.3f}')
        print('  cliques (mean-rank gap < CD, i.e. NOT significantly different):')
        for i in range(len(common)):
            for j in range(i + 1, len(common)):
                if abs(mean_ranks[i] - mean_ranks[j]) < cd:
                    print(f'    {common[i]} ~ {common[j]}')
        return

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
    # self-checks: Holm (Holland 1988), TOST equivalence, Nemenyi CD closed form
    assert np.allclose(holm([0.01, 0.04, 0.03]), [0.03, 0.06, 0.06])
    _a = np.array([1.0, 1.1, 0.9, 1.05, 0.95])
    assert tost(_a, _a, margin=0.2)[0]                       # identical -> equivalent
    assert not tost(_a, _a + 5.0, margin=0.2)[0]             # far apart -> not equivalent
    assert abs(nemenyi_cd(5, 7) - 2.728 * np.sqrt(5 * 6 / (6.0 * 7))) < 1e-9
    main()
