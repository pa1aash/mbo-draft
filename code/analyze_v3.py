"""Analysis for 0A.2 (W1/W2) and 0A.3 (BM1), per docs/PREREGISTRATION_V3.md.

Both arms are read on the CONDITION-INVARIANT normalizer established in
docs/BETA0_RECONCILE.md: one per-task min-max fit ONCE over the pooled cell means of
every condition being compared (the 4 widths; the 2 budget levels), so numbers are on a
single ruler and cross-condition differences are interpretable. The incumbent per-condition
refit estimator (kbeta_analyze) is also reported wherever the pre-registration asks for
comparability with a published figure.

CIs: task+seed hierarchical bootstrap, 10,000 resamples, normalizer refit inside each
resample.

  python analyze_v3.py --which width|budget|both  -> results/{width,budget}/*_analysis.json
"""
import argparse
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, '..', 'results')
TASKS = ['Branin-2D', 'Styblinski-5D', 'Levy-8D', 'Rosenbrock-10D',
         'Rastrigin-15D', 'Ackley-20D', 'Griewank-30D']
OPT3 = ['perturb', 'grad', 'cma']
NBOOT = 10000


# ---------------------------------------------------------------- estimators
def _minmax(row, lo, rng):
    return (row - lo) / rng


def gap(cm, lo, rng, ens_idx, gp_idx):
    z = _minmax(cm, lo, rng)
    return z[gp_idx].mean() - z[ens_idx].mean()


def eta2(cm_by_task):
    """Incumbent estimator, kbeta_analyze._eta2 (code/kbeta_analyze.py:29-43), re-implemented
    here so this module has no import-time dependency on that script's file layout.
    cm_by_task: (T,9) seed-mean cell values, surrogate-major."""
    M = []
    for row in cm_by_task:
        a = np.asarray(row, float)
        lo, hi = a.min(), a.max()
        z = (a - lo) / (hi - lo) if hi > lo else np.zeros_like(a)
        M.append(z.reshape(3, 3))
    M = np.array(M)
    g = M.mean()
    tot = ((M - g) ** 2).sum()
    if tot == 0:
        return dict(surr=0.0, opt=0.0, inter=0.0)
    om3, sm3 = M.mean(axis=(0, 1)), M.mean(axis=(0, 2))
    T = len(M)
    inter = M.mean(axis=0) - sm3[:, None] - om3[None, :] + g
    return dict(surr=float((T * 3 * ((sm3 - g) ** 2).sum()) / tot),
                opt=float((T * 3 * ((om3 - g) ** 2).sum()) / tot),
                inter=float((T * (inter ** 2).sum()) / tot))


def eta2_fixed_norm(cm_by_task, lo, rng):
    """eta2 on a condition-invariant normalizer supplied from outside."""
    M = np.array([_minmax(np.asarray(r, float), lo[i], rng[i]).reshape(3, 3)
                  for i, r in enumerate(cm_by_task)])
    g = M.mean()
    tot = ((M - g) ** 2).sum()
    if tot == 0:
        return dict(surr=0.0, opt=0.0, inter=0.0)
    om3, sm3 = M.mean(axis=(0, 1)), M.mean(axis=(0, 2))
    T = len(M)
    inter = M.mean(axis=0) - sm3[:, None] - om3[None, :] + g
    return dict(surr=float((T * 3 * ((sm3 - g) ** 2).sum()) / tot),
                opt=float((T * 3 * ((om3 - g) ** 2).sum()) / tot),
                inter=float((T * (inter ** 2).sum()) / tot))


def ci(a):
    return [float(np.percentile(a, 2.5)), float(np.percentile(a, 97.5))]


def load_perseed(mbo_node, cells, metric='p100'):
    """-> (T, len(cells), S) per-seed values. Raises on any missing cell (MISSING stays
    MISSING: we refuse to silently drop or impute)."""
    out = []
    for t in TASKS:
        row = []
        for c in cells:
            v = mbo_node.get(t, {}).get(c, {}).get(metric, {}).get('all')
            if v is None:
                raise KeyError(f'MISSING cell {t}/{c}/{metric}')
            row.append(v)
        out.append(row)
    return np.array(out, float)


def pooled_norm(mats):
    """One (lo,rng) per task from the pooled seed-mean cells of every condition."""
    stacked = np.concatenate([m.mean(axis=2) for m in mats], axis=1)
    lo = stacked.min(axis=1)
    rng = stacked.max(axis=1) - lo
    rng[rng == 0] = 1.0
    return lo, rng


def boot_indices(T, S, nboot, seed=0):
    r = np.random.RandomState(seed)
    for _ in range(nboot):
        yield r.randint(0, T, T), r.randint(0, S, (T, S))


# ---------------------------------------------------------------- 0A.2 width
def analyze_width(path):
    d = json.load(open(path))
    widths = d['widths']
    gp_cells = [f'{s}:{o}' for s in ('botorchgp', 'svgp') for o in OPT3]
    per_w = {}
    for w in widths:
        cells = [f'ens_w{w}:{o}' for o in OPT3] + gp_cells
        per_w[w] = load_perseed(d['mbo'], cells)
    ens_idx, gp_idx = [0, 1, 2], [3, 4, 5, 6, 7, 8]
    lo, rng = pooled_norm([per_w[w] for w in widths])

    point = {w: float(np.mean([gap(per_w[w].mean(axis=2)[i], lo[i], rng[i], ens_idx, gp_idx)
                               for i in range(len(TASKS))])) for w in widths}

    T, S = len(TASKS), per_w[widths[0]].shape[2]
    draws = {w: [] for w in widths}
    shrink = []
    for ti, si in boot_indices(T, S, NBOOT):
        cm = {w: np.array([per_w[w][t, :, si[k]].mean(axis=0) for k, t in enumerate(ti)])
              for w in widths}
        st = np.concatenate([cm[w] for w in widths], axis=1)
        l2 = st.min(axis=1)
        r2 = st.max(axis=1) - l2
        r2[r2 == 0] = 1.0
        g = {}
        for w in widths:
            g[w] = float(np.mean([gap(cm[w][i], l2[i], r2[i], ens_idx, gp_idx)
                                  for i in range(T)]))
            draws[w].append(g[w])
        shrink.append(g[widths[-1]] - g[widths[0]])

    gaps = {str(w): dict(gap=point[w], ci=ci(draws[w])) for w in widths}
    wmax, wmin = widths[-1], widths[0]
    monotone = all(point[widths[i + 1]] <= point[widths[i]] for i in range(len(widths) - 1))
    ci_max = ci(draws[wmax])
    excludes0 = ci_max[0] > 0
    halved = point[wmax] < 0.5 * point[wmin]
    if monotone and halved and ci_max[0] <= 0 <= ci_max[1]:
        verdict = ('W1 KILL FIRES — gap closes with width; the mean-smoothness advantage is a '
                   'finite-width artifact and the NTK objection is CONFIRMED')
    elif excludes0:
        verdict = ('W1 CONFIRMED — the gap persists at w=%d (95%% CI excludes 0); the NTK/'
                   'spectral-bias objection is empirically answered and C2 mean-quality is a '
                   'class property at practical widths' % wmax)
    else:
        verdict = 'W1 PARTIAL — see shrinkage fraction; neither pre-registered branch fires cleanly'

    # ---- W2: held-out RMSE vs w, and the RMSE-tie subset ----
    ho = d['heldout']
    rm = {}
    for k in [f'ens_w{w}' for w in widths] + ['botorchgp']:
        vals = {t: ho[t][k]['norm_rmse'] for t in TASKS if k in ho.get(t, {})}
        rm[k] = dict(per_task={t: v['mean'] for t, v in vals.items()},
                     mean=float(np.mean([v['mean'] for v in vals.values()])))
    ties = []
    for t in TASKS:
        if 'botorchgp' not in ho.get(t, {}):
            continue
        g_all = np.array(ho[t]['botorchgp']['norm_rmse']['all'])
        for w in widths:
            e_all = np.array(ho[t][f'ens_w{w}']['norm_rmse']['all'])
            # paired over seeds (same seed -> same split and same training subset)
            dif = e_all - g_all
            bs = np.random.RandomState(0).randint(0, len(dif), (2000, len(dif)))
            c = ci(dif[bs].mean(axis=1))
            if c[0] <= 0 <= c[1]:
                ties.append(dict(task=t, w=w, ens_rmse=float(e_all.mean()),
                                 gp_rmse=float(g_all.mean()), diff_ci=c))
    rep = dict(widths=widths, gap_by_width=gaps,
               shrinkage=dict(delta_wmax_minus_wmin=float(np.mean(shrink)),
                              ci=ci(shrink),
                              frac_of_w96=float(point[wmax] / point[wmin]) if point[wmin] else None),
               monotone_nonincreasing=bool(monotone),
               gap_wmax_ci_excludes_zero=bool(excludes0),
               W1_verdict=verdict,
               heldout_norm_rmse=rm,
               rmse_tie_cells=ties,
               n_seeds=S, nboot=NBOOT, engine=d['meta'])
    if not ties:
        rep['W2_verdict'] = ('W2 UNTESTABLE — no (task, w) cell where ensemble held-out RMSE '
                             'is statistically indistinguishable from the GP\'s')
    else:
        gap_at_ties = [point[c['w']] for c in ties]
        rep['W2_verdict'] = (
            'W2 %s — %d RMSE-tie cells; mean gap at those widths %.3f'
            % ('SUPPORTED' if np.mean(gap_at_ties) > 0 else 'NOT SUPPORTED',
               len(ties), float(np.mean(gap_at_ties))))
    return rep


# --------------------------------------------------------------- 0A.3 budget
def analyze_budget(path):
    d = json.load(open(path))
    cells = [f'{s}:{o}' for s in ('ens', 'botorchgp', 'svgp') for o in OPT3]
    levels = list(d['runs'])
    mats = {lv: load_perseed(d['runs'][lv]['mbo'], cells) for lv in levels}
    lo, rng = pooled_norm([mats[lv] for lv in levels])
    T, S = len(TASKS), mats[levels[0]].shape[2]

    out = {'levels_config': d['levels'], 'n_seeds': S, 'nboot': NBOOT, 'engine': d['meta'],
           'achieved_q': {lv: d['runs'][lv].get('achieved_q') for lv in levels}, 'by_level': {}}
    draws = {lv: {'opt': [], 'surr': []} for lv in levels}
    for ti, si in boot_indices(T, S, NBOOT):
        for lv in levels:
            cm = np.array([mats[lv][t, :, si[k]].mean(axis=0) for k, t in enumerate(ti)])
            e = eta2(cm)
            draws[lv]['opt'].append(e['opt'])
            draws[lv]['surr'].append(e['surr'])
    for lv in levels:
        cm = mats[lv].mean(axis=2)
        inc = eta2(cm)
        fix = eta2_fixed_norm(cm, lo, rng)
        o = inc['opt']
        if o < 0.10:
            v = 'BM1 CONFIRMED — eta2_opt < 0.10 under matched budget'
        elif o > 0.15:
            v = ('BM1 KILL FIRES — eta2_opt > 0.15 under matched budget; the optimizer null '
                 'was a budget artifact and A\'s "optimizer negligible" claim does not hold')
        else:
            v = 'BM1 INCONCLUSIVE — eta2_opt in the pre-registered [0.10, 0.15] band'
        out['by_level'][lv] = dict(
            eta2_incumbent_norm=inc, eta2_condition_invariant_norm=fix,
            eta2_opt_ci=ci(draws[lv]['opt']), eta2_surr_ci=ci(draws[lv]['surr']),
            verdict=v)
    out['primary_level'] = 'up'
    out['BM1_verdict'] = out['by_level'].get('up', {}).get('verdict', 'primary level MISSING')
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--which', default='both')
    a = ap.parse_args()
    if a.which in ('width', 'both'):
        p = os.path.join(RES, 'width', 'width_grid.json')
        if os.path.exists(p):
            r = analyze_width(p)
            json.dump(r, open(os.path.join(RES, 'width', 'width_analysis.json'), 'w'), indent=2)
            print(json.dumps({k: v for k, v in r.items() if k != 'engine'}, indent=2)[:4000])
        else:
            print('MISSING', p)
    if a.which in ('budget', 'both'):
        p = os.path.join(RES, 'budget', 'budget_matched.json')
        if os.path.exists(p):
            r = analyze_budget(p)
            json.dump(r, open(os.path.join(RES, 'budget', 'budget_analysis.json'), 'w'), indent=2)
            print(json.dumps({k: v for k, v in r.items() if k != 'engine'}, indent=2)[:4000])
        else:
            print('MISSING', p)


if __name__ == '__main__':
    main()
