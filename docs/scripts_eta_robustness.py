"""Task A — eta^2 robustness profile for "Decomposing the GP Advantage in Offline MBO".

Reproduces the paper's exact eta^2 (code/run05.py::eta2) then recomputes it under
alternative normalizations, unit choices, assumption checks, and a permutation test.

Run:  python eta_robustness.py
"""
import json, os, sys
import numpy as np
from scipy import stats as sst

REPO = '/Users/palaash/Downloads/MBO'
RES = os.path.join(REPO, 'results')
SURR3 = ['ens', 'botorchgp', 'svgp']
OPT3 = ['perturb', 'grad', 'cma']
CELLS = [f'{s}:{o}' for s in SURR3 for o in OPT3]
METRIC = 'p100'


def load(f):
    return json.load(open(os.path.join(RES, f)))


# ---------------------------------------------------------------- core eta^2
def eta2_from_M(M):
    """M: (T, S, O) array of already-normalized values (T = replicate dim).
    EXACT replica of code/run05.py::eta2's algebra.  eta^2 = SS_effect / SS_total."""
    M = np.asarray(M, float)
    T, S, O = M.shape
    g = M.mean()
    sstot = ((M - g) ** 2).sum()
    om, sm = M.mean(axis=(0, 1)), M.mean(axis=(0, 2))          # optimizer / surrogate marginals
    eta_opt = (T * S * ((om - g) ** 2).sum()) / sstot
    eta_surr = (T * O * ((sm - g) ** 2).sum()) / sstot
    inter = M.mean(axis=0) - sm[:, None] - om[None, :] + g
    eta_inter = (T * (inter ** 2).sum()) / sstot
    return float(eta_surr), float(eta_opt), float(eta_inter)


def paper_eta2(path, metric=METRIC):
    """Verbatim port of code/run05.py::eta2 — the paper's own code path."""
    d = load(path)['mbo']
    used, M = [], []
    for t in d:
        vals = {c: d[t][c][metric]['mean'] for c in CELLS
                if c in d[t] and isinstance(d[t][c].get(metric), dict)}
        if len(vals) < 9:
            continue
        a = np.array([vals[c] for c in CELLS], float)
        lo, hi = a.min(), a.max()
        z = (a - lo) / (hi - lo) if hi > lo else np.zeros_like(a)
        M.append(z.reshape(3, 3)); used.append(t)
    M = np.array(M)
    g = M.mean(); sstot = ((M - g) ** 2).sum()
    om3, sm3 = M.mean(axis=(0, 1)), M.mean(axis=(0, 2))
    eta_opt = (len(used) * 3 * ((om3 - g) ** 2).sum()) / sstot
    eta_surr = (len(used) * 3 * ((sm3 - g) ** 2).sum()) / sstot
    inter = M.mean(axis=0) - sm3[:, None] - om3[None, :] + g
    eta_inter = (len(used) * (inter ** 2).sum()) / sstot
    return used, float(eta_surr), float(eta_opt), float(eta_inter), M


# ---------------------------------------------------------------- data pulls
def raw_cellmeans(path, metric=METRIC):
    """(tasks, R) where R[t] is the (3,3) array of RAW cell means. Only complete grids."""
    d = load(path)['mbo']
    tasks, R = [], []
    for t in d:
        vals = {c: d[t][c][metric]['mean'] for c in CELLS
                if c in d[t] and isinstance(d[t][c].get(metric), dict)}
        if len(vals) < 9:
            continue
        tasks.append(t)
        R.append(np.array([vals[c] for c in CELLS], float).reshape(3, 3))
    return tasks, np.array(R)


def raw_seeds(path, metric=METRIC):
    """(tasks, n_seed, A) where A is (T, n_seed, 3, 3) of RAW per-seed values.
    Requires equal seed counts across the 9 cells of a task."""
    d = load(path)['mbo']
    tasks, A = [], []
    for t in d:
        arrs = {}
        ok = True
        for c in CELLS:
            e = d[t].get(c)
            if not (e and isinstance(e.get(metric), dict) and isinstance(e[metric].get('all'), list)):
                ok = False; break
            arrs[c] = np.array(e[metric]['all'], float)
        if not ok:
            continue
        ns = {len(v) for v in arrs.values()}
        if len(ns) != 1:
            print(f'  !! {t}: unequal seed counts {ns} -> skipped from per-seed arm')
            continue
        n = ns.pop()
        block = np.stack([arrs[c] for c in CELLS], axis=1).reshape(n, 3, 3)   # (seed,3,3)
        tasks.append(t); A.append(block)
    ns = {a.shape[0] for a in A}
    if len(ns) != 1:
        raise RuntimeError(f'tasks disagree on seed count: {ns}')
    return tasks, ns.pop(), np.array(A)     # (T, n_seed, 3, 3)


# ------------------------------------------------------- normalization zoo
def n_minmax(R):
    """paper's: per-task min-max over the 9 cell means -> [0,1]"""
    out = []
    for a in R:
        lo, hi = a.min(), a.max()
        out.append((a - lo) / (hi - lo) if hi > lo else np.zeros_like(a))
    return np.array(out)


def n_rank(R):
    """per-task rank (1..9) of the 9 cell means; ties averaged."""
    return np.array([sst.rankdata(a.ravel()).reshape(3, 3) for a in R])


def n_zscore(R):
    """per-task z-score over the 9 cell means (ddof=0)."""
    out = []
    for a in R:
        s = a.std()
        out.append((a - a.mean()) / s if s > 0 else np.zeros_like(a))
    return np.array(out)


def n_logregret(R):
    """Principled log for negative values: work in REGRET space.
    Every task here is a maximization with per-task-comparable cells, so define
        regret_c = max_over_the_9_cells(y) - y_c   >= 0   (0 for the best cell),
    which is non-negative BY CONSTRUCTION regardless of the raw sign, then take
        z_c = -log1p(regret_c)
    (log1p is finite at regret=0; the minus keeps 'higher = better' orientation).
    Finally min-max within task, so this arm changes ONLY the transform, not the
    paper's comparability step -- an apples-to-apples swap.
    log1p is scale-dependent, so we first divide regret by the task's regret scale
    (its max) to make log1p's unit-knee task-invariant."""
    out = []
    for a in R:
        reg = a.max() - a
        s = reg.max()
        reg = reg / s if s > 0 else reg
        z = -np.log1p(reg)
        lo, hi = z.min(), z.max()
        out.append((z - lo) / (hi - lo) if hi > lo else np.zeros_like(z))
    return np.array(out)


def n_winsor_seeds(A, pct):
    """Winsorize the per-seed pool WITHIN each task at [pct, 100-pct], then take
    cell means, then per-task min-max. This is the arm that directly attacks the
    'one extreme cell compresses the rest' worry, because it clips in raw space
    before the min-max range is computed."""
    out = []
    for block in A:                      # (seed,3,3)
        flat = block.ravel()
        lo_q, hi_q = np.percentile(flat, [pct, 100 - pct])
        w = np.clip(block, lo_q, hi_q)
        cm = w.mean(axis=0)              # (3,3) winsorized cell means
        lo, hi = cm.min(), cm.max()
        out.append((cm - lo) / (hi - lo) if hi > lo else np.zeros_like(cm))
    return np.array(out)


def n_winsor_cellmeans(R, pct):
    """Winsorize the 9 cell means within task at [pct,100-pct], then min-max.
    (weaker: with only 9 points the 5th/10th pct barely clips)"""
    out = []
    for a in R:
        lo_q, hi_q = np.percentile(a.ravel(), [pct, 100 - pct])
        w = np.clip(a, lo_q, hi_q)
        lo, hi = w.min(), w.max()
        out.append((w - lo) / (hi - lo) if hi > lo else np.zeros_like(w))
    return np.array(out)


def n_raw(R):
    """no normalization at all: pool RAW cell means across tasks."""
    return np.array(R, float)


# ---------------------------------------------------- per-seed unit variants
def seeds_normed(A, how='minmax'):
    """A: (T, n_seed, 3, 3) raw. Returns (T*n_seed, 3, 3) with the replicate dim
    flattened over (task, seed) -- so each (task,seed) is one row of the ANOVA.
    Normalization uses the per-task CELL-MEAN lo/hi (exactly analysis.py::task_norm),
    applied to the individual seed values, so seed values may fall outside [0,1]."""
    out = []
    for block in A:                       # (seed,3,3)
        cm = block.mean(axis=0)
        if how == 'minmax':
            lo, hi = cm.min(), cm.max()
            rng = (hi - lo) or 1.0
            z = (block - lo) / rng
        elif how == 'zscore':
            m, s = cm.mean(), cm.std()
            z = (block - m) / (s or 1.0)
        elif how == 'rank':
            # rank the 9 cells WITHIN each (task,seed) row
            z = np.stack([sst.rankdata(b.ravel()).reshape(3, 3) for b in block])
        elif how == 'raw':
            z = block
        else:
            raise ValueError(how)
        out.append(z)
    A2 = np.array(out)                    # (T, seed, 3, 3)
    T, S = A2.shape[0], A2.shape[1]
    return A2.reshape(T * S, 3, 3)


# ---------------------------------------------------------- assumption checks
def assumption_checks(M, label):
    """M: (T,3,3) the paper's normalized design. Model: y_{t,s,o} = cellmean_{s,o} + e.
    Residual = M - cellmean (over tasks). 63 residuals, 9 groups of 7."""
    cm = M.mean(axis=0)
    resid = (M - cm[None, :, :])
    r = resid.ravel()
    sw = sst.shapiro(r)
    # QQ summary
    skew, kurt = float(sst.skew(r)), float(sst.kurtosis(r, fisher=True))
    n = len(r)
    theo = sst.norm.ppf((np.arange(1, n + 1) - 0.5) / n)
    qq_r = float(np.corrcoef(np.sort(r), theo)[0, 1])
    groups = [M[:, i, j] for i in range(3) for j in range(3)]
    lev = sst.levene(*groups, center='median')
    bart = sst.bartlett(*groups)
    ratio = float(max(np.var(g, ddof=1) for g in groups) / max(1e-300, min(np.var(g, ddof=1) for g in groups)))
    return dict(label=label, n_resid=n,
                shapiro_W=float(sw.statistic), shapiro_p=float(sw.pvalue),
                resid_skew=skew, resid_excess_kurtosis=kurt, qq_corr=qq_r,
                levene_W=float(lev.statistic), levene_p=float(lev.pvalue),
                bartlett_T=float(bart.statistic), bartlett_p=float(bart.pvalue),
                var_ratio_max_min=ratio,
                group_vars=[float(np.var(g, ddof=1)) for g in groups])


# ------------------------------------------------------------- permutation
def permutation_test(M, n_perm=20000, seed=0):
    """Permute FACTOR LABELS WITHIN TASK, which is the exchangeability the null
    asserts (under H0_surrogate the 3 surrogate labels are exchangeable within a
    task, holding the optimizer structure).  No distributional assumption at all.
      - surrogate null: independently permute the 3 ROWS within each task
      - optimizer null: independently permute the 3 COLS within each task
      - interaction null: permute all 9 cells within each task
    Note: min-max normalization is label-invariant (it depends only on the SET of
    9 values in a task), so permuting labels after normalizing is identical to
    permuting before -- the normalization cannot leak into the null."""
    rng = np.random.default_rng(seed)
    obs = eta2_from_M(M)
    T = M.shape[0]
    null_s, null_o, null_i = [], [], []
    for _ in range(n_perm):
        Ms = np.stack([M[t][rng.permutation(3), :] for t in range(T)])
        null_s.append(eta2_from_M(Ms)[0])
        Mo = np.stack([M[t][:, rng.permutation(3)] for t in range(T)])
        null_o.append(eta2_from_M(Mo)[1])
        Mi = np.stack([M[t].ravel()[rng.permutation(9)].reshape(3, 3) for t in range(T)])
        null_i.append(eta2_from_M(Mi)[2])
    null_s, null_o, null_i = map(np.array, (null_s, null_o, null_i))

    def pv(null, o):
        return float((1 + (null >= o).sum()) / (1 + len(null)))
    return dict(
        obs=dict(surr=obs[0], opt=obs[1], inter=obs[2]),
        p_surr=pv(null_s, obs[0]), p_opt=pv(null_o, obs[1]), p_inter=pv(null_i, obs[2]),
        null_surr_mean=float(null_s.mean()), null_surr_q95=float(np.percentile(null_s, 95)),
        null_opt_mean=float(null_o.mean()), null_opt_q95=float(np.percentile(null_o, 95)),
        null_inter_mean=float(null_i.mean()), null_inter_q95=float(np.percentile(null_i, 95)),
    )


def bootstrap_ci(M, n_boot=20000, seed=1):
    """Nonparametric CI on eta^2 by resampling TASKS with replacement (the
    replicate unit of the paper's own ANOVA)."""
    rng = np.random.default_rng(seed)
    T = M.shape[0]
    bs, bo, bi = [], [], []
    for _ in range(n_boot):
        idx = rng.integers(0, T, T)
        try:
            s, o, i = eta2_from_M(M[idx])
        except Exception:
            continue
        if np.isfinite(s) and np.isfinite(o) and np.isfinite(i):
            bs.append(s); bo.append(o); bi.append(i)
    q = lambda a: (float(np.percentile(a, 2.5)), float(np.percentile(a, 97.5)))
    return dict(n_ok=len(bs), ci_surr=q(bs), ci_opt=q(bo), ci_inter=q(bi),
                p_surr_gt_opt=float(np.mean(np.array(bs) > np.array(bo))))


# ------------------------------------------------------------------- driver
def main():
    out = {}
    print('=' * 90)
    print('STEP 1 — REPRODUCTION of the paper\'s exact eta^2 via code/run05.py::eta2')
    print('=' * 90)
    TARGET = dict(surr=0.36872274, opt=0.01318917, inter=0.16518057)
    for tag, path in [('SYNTH', 'results_camera.json'), ('REAL', 'results_db.json'),
                      ('SYNTH-matched', 'results_camera_matched.json')]:
        try:
            used, es, eo, ei, M = paper_eta2(path)
        except Exception as ex:
            print(f'  {tag}: ERROR {ex}'); continue
        print(f'  {tag:14} tasks={len(used)}')
        print(f'      eta2_surr = {es!r}')
        print(f'      eta2_opt  = {eo!r}')
        print(f'      eta2_inter= {ei!r}')
        if tag == 'SYNTH':
            print('    vs paper stored:  surr=0.36872274  opt=0.01318917  inter=0.16518057')
            ok = (abs(es - TARGET['surr']) < 5e-9 and abs(eo - TARGET['opt']) < 5e-9
                  and abs(ei - TARGET['inter']) < 5e-9)
            print(f'    EXACT MATCH (to 8dp): {ok}')
            out['reproduction'] = dict(match=bool(ok), surr=es, opt=eo, inter=ei, tasks=used)
        out.setdefault('paper_path', {})[tag] = dict(surr=es, opt=eo, inter=ei, tasks=used)

    # ---------- raw span diagnostic
    print('\n' + '=' * 90)
    print('RAW SPAN DIAGNOSTIC (the motivation for the whole exercise)')
    print('=' * 90)
    tasks, R = raw_cellmeans('results_camera.json')
    print(f'  {"task":16}{"raw min":>13}{"raw max":>11}{"span":>13}{"minmax-compression":>21}')
    spans = {}
    for t, a in zip(tasks, R):
        span = a.max() - a.min()
        spans[t] = float(span)
        # how much of the [0,1] band do the 8 non-extreme cells occupy?
        z = (a - a.min()) / span
        z2 = np.sort(z.ravel())
        occ = z2[-1] - z2[1]
        print(f'  {t:16}{a.min():13.3f}{a.max():11.3f}{span:13.3f}   8 non-min cells span {occ:.3f} of [0,1]')
    print(f'  GLOBAL raw range across tasks: [{R.min():.3f}, {R.max():.3f}]')
    out['raw_spans'] = spans

    # ---------- normalization zoo, per-task-mean units
    print('\n' + '=' * 90)
    print('STEP 2a — eta^2 UNDER ALTERNATIVE NORMALIZATIONS  (unit = PER-TASK MEAN; the paper\'s unit)')
    print('=' * 90)
    tasksS, RS = raw_cellmeans('results_camera.json')
    _, nseed, AS = raw_seeds('results_camera.json')
    print(f'  synthetic: T={len(tasksS)} tasks, {nseed} seeds/cell, 9 cells\n')
    treatments = [
        ('minmax (PAPER)', n_minmax(RS)),
        ('rank (1-9 within task)', n_rank(RS)),
        ('z-score per task', n_zscore(RS)),
        ('log-regret -> minmax', n_logregret(RS)),
        ('winsor 5% (seed pool)', n_winsor_seeds(AS, 5)),
        ('winsor 10% (seed pool)', n_winsor_seeds(AS, 10)),
        ('winsor 5% (cell means)', n_winsor_cellmeans(RS, 5)),
        ('winsor 10% (cell means)', n_winsor_cellmeans(RS, 10)),
        ('RAW (no normalization)', n_raw(RS)),
    ]
    rows = []
    print(f'  {"normalization":28}{"eta2_surr":>11}{"eta2_opt":>10}{"eta2_inter":>12}{"surr/opt":>10}  holds?')
    for name, M in treatments:
        es, eo, ei = eta2_from_M(M)
        ratio = es / eo if eo > 0 else float('inf')
        holds = 'YES' if es > eo else 'NO'
        rows.append(dict(norm=name, unit='task-mean', surr=es, opt=eo, inter=ei,
                         ratio=float(ratio), holds=holds))
        print(f'  {name:28}{es:11.4f}{eo:10.4f}{ei:12.4f}{ratio:10.1f}  {holds}')
    out['taskmean_units'] = rows

    # ---------- per-seed units
    print('\n' + '=' * 90)
    print(f'STEP 2b — eta^2 WITH PER-SEED ROWS  (unit = (task,seed); {len(tasksS)}x{nseed} = '
          f'{len(tasksS)*nseed} rows)')
    print('=' * 90)
    print('  NOTE: the paper uses PER-TASK-MEAN units (run05.py::eta2 reads d[t][c][metric]["mean"]),')
    print('        i.e. it collapses the 30 seeds before the ANOVA. Per-seed rows re-inject')
    print('        within-cell seed noise into SS_total, which MUST deflate every eta^2.')
    rows2 = []
    print(f'\n  {"normalization":28}{"eta2_surr":>11}{"eta2_opt":>10}{"eta2_inter":>12}{"surr/opt":>10}  holds?')
    for how in ['minmax', 'zscore', 'rank', 'raw']:
        Ms = seeds_normed(AS, how)
        es, eo, ei = eta2_from_M(Ms)
        ratio = es / eo if eo > 0 else float('inf')
        holds = 'YES' if es > eo else 'NO'
        rows2.append(dict(norm=how, unit='per-seed', surr=es, opt=eo, inter=ei,
                          ratio=float(ratio), holds=holds))
        print(f'  {how:28}{es:11.4f}{eo:10.4f}{ei:12.4f}{ratio:10.1f}  {holds}')
    out['perseed_units'] = rows2

    # ---------- Design-Bench for contrast
    print('\n' + '=' * 90)
    print('STEP 2c — same zoo on DESIGN-BENCH (results_db.json)')
    print('=' * 90)
    tasksD, RD = raw_cellmeans('results_db.json')
    _, nseedD, AD = raw_seeds('results_db.json')
    print(f'  real: T={len(tasksD)} tasks, {nseedD} seeds/cell\n')
    rows3 = []
    print(f'  {"normalization":28}{"eta2_surr":>11}{"eta2_opt":>10}{"eta2_inter":>12}  surr>opt?')
    for name, M in [('minmax (PAPER)', n_minmax(RD)), ('rank', n_rank(RD)),
                    ('z-score per task', n_zscore(RD)), ('log-regret -> minmax', n_logregret(RD)),
                    ('winsor 5% (seed pool)', n_winsor_seeds(AD, 5)),
                    ('winsor 10% (seed pool)', n_winsor_seeds(AD, 10)),
                    ('RAW (no normalization)', n_raw(RD))]:
        es, eo, ei = eta2_from_M(M)
        rows3.append(dict(norm=name, surr=es, opt=eo, inter=ei, holds='YES' if es > eo else 'NO'))
        print(f'  {name:28}{es:11.4f}{eo:10.4f}{ei:12.4f}  {"YES" if es>eo else "NO"}')
    out['db_units'] = rows3

    # ---------- leave-one-task-out on the paper's arm
    print('\n' + '=' * 90)
    print('STEP 2d — LEAVE-ONE-TASK-OUT on the paper\'s arm (is Griewank-30D driving it?)')
    print('=' * 90)
    Mp = n_minmax(RS)
    loo = []
    print(f'  {"dropped task":18}{"eta2_surr":>11}{"eta2_opt":>10}{"eta2_inter":>12}')
    for i, t in enumerate(tasksS):
        keep = [j for j in range(len(tasksS)) if j != i]
        es, eo, ei = eta2_from_M(Mp[keep])
        loo.append(dict(dropped=t, surr=es, opt=eo, inter=ei))
        print(f'  {t:18}{es:11.4f}{eo:10.4f}{ei:12.4f}')
    out['loo'] = loo

    # ---------- assumption checks
    print('\n' + '=' * 90)
    print('STEP 3 — ASSUMPTION CHECKS on the PAPER\'S ACTUAL ANOVA (minmax, task-mean units)')
    print('=' * 90)
    ac = assumption_checks(Mp, 'SYNTH minmax task-mean (paper)')
    out['assumptions_paper'] = ac
    print(f'  residuals n = {ac["n_resid"]}  (7 tasks x 9 cells, resid = y - cellmean_over_tasks)')
    print(f'  Shapiro-Wilk   W = {ac["shapiro_W"]:.4f}   p = {ac["shapiro_p"]:.3e}   '
          f'{"NORMALITY REJECTED" if ac["shapiro_p"] < 0.05 else "not rejected"}')
    print(f'  residual skew  = {ac["resid_skew"]:+.3f}   excess kurtosis = {ac["resid_excess_kurtosis"]:+.3f}')
    print(f'  QQ corr(sorted resid, normal quantiles) = {ac["qq_corr"]:.4f}   (1.0 = perfectly normal)')
    print(f'  Levene (median) W = {ac["levene_W"]:.4f}   p = {ac["levene_p"]:.3e}   '
          f'{"HOMOSCEDASTICITY REJECTED" if ac["levene_p"] < 0.05 else "not rejected"}')
    print(f'  Bartlett       T = {ac["bartlett_T"]:.4f}   p = {ac["bartlett_p"]:.3e}   '
          f'{"HOMOSCEDASTICITY REJECTED" if ac["bartlett_p"] < 0.05 else "not rejected"}')
    print(f'  max/min group variance ratio across the 9 cells = {ac["var_ratio_max_min"]:.1f}')
    for name, M2, lab in [('rank', n_rank(RS), 'SYNTH rank'), ('z', n_zscore(RS), 'SYNTH z'),
                          ('logreg', n_logregret(RS), 'SYNTH log-regret')]:
        a2 = assumption_checks(M2, lab)
        out.setdefault('assumptions_alt', {})[lab] = a2
        print(f'  [{lab:22}] Shapiro p={a2["shapiro_p"]:.3e}  Levene p={a2["levene_p"]:.3e}  '
              f'Bartlett p={a2["bartlett_p"]:.3e}')

    # ---------- permutation
    print('\n' + '=' * 90)
    print('STEP 4 — PERMUTATION effect-size test (no distributional assumptions), 20k perms')
    print('=' * 90)
    for lab, M2 in [('minmax (PAPER)', Mp), ('rank', n_rank(RS)), ('z-score', n_zscore(RS)),
                    ('log-regret', n_logregret(RS)), ('RAW', n_raw(RS))]:
        pr = permutation_test(M2, n_perm=20000, seed=0)
        out.setdefault('permutation', {})[lab] = pr
        print(f'  [{lab}]')
        print(f'     surr : eta2={pr["obs"]["surr"]:.4f}  perm-null mean={pr["null_surr_mean"]:.4f} '
              f'q95={pr["null_surr_q95"]:.4f}  p={pr["p_surr"]:.5f}')
        print(f'     opt  : eta2={pr["obs"]["opt"]:.4f}  perm-null mean={pr["null_opt_mean"]:.4f} '
              f'q95={pr["null_opt_q95"]:.4f}  p={pr["p_opt"]:.5f}')
        print(f'     inter: eta2={pr["obs"]["inter"]:.4f}  perm-null mean={pr["null_inter_mean"]:.4f} '
              f'q95={pr["null_inter_q95"]:.4f}  p={pr["p_inter"]:.5f}')

    print('\n  bootstrap-over-tasks CIs (2.5/97.5 pct, 20k resamples):')
    for lab, M2 in [('minmax (PAPER)', Mp), ('rank', n_rank(RS)), ('z-score', n_zscore(RS)),
                    ('log-regret', n_logregret(RS)), ('RAW', n_raw(RS))]:
        b = bootstrap_ci(M2, n_boot=20000, seed=1)
        out.setdefault('bootstrap', {})[lab] = b
        print(f'    {lab:16} surr CI=[{b["ci_surr"][0]:.3f},{b["ci_surr"][1]:.3f}]  '
              f'opt CI=[{b["ci_opt"][0]:.3f},{b["ci_opt"][1]:.3f}]  '
              f'inter CI=[{b["ci_inter"][0]:.3f},{b["ci_inter"][1]:.3f}]  '
              f'P(surr>opt)={b["p_surr_gt_opt"]:.4f}')

    # ---------- DB permutation for contrast
    print('\n  Design-Bench permutation (paper arm):')
    prd = permutation_test(n_minmax(RD), n_perm=20000, seed=0)
    out.setdefault('permutation_db', {})['minmax'] = prd
    print(f'    surr : eta2={prd["obs"]["surr"]:.4f} p={prd["p_surr"]:.5f}')
    print(f'    opt  : eta2={prd["obs"]["opt"]:.4f} p={prd["p_opt"]:.5f}')
    print(f'    inter: eta2={prd["obs"]["inter"]:.4f} p={prd["p_inter"]:.5f}')
    bd = bootstrap_ci(n_minmax(RD), n_boot=20000, seed=1)
    out.setdefault('bootstrap_db', {})['minmax'] = bd
    print(f'    bootstrap: surr CI=[{bd["ci_surr"][0]:.3f},{bd["ci_surr"][1]:.3f}] '
          f'opt CI=[{bd["ci_opt"][0]:.3f},{bd["ci_opt"][1]:.3f}] P(surr>opt)={bd["p_surr_gt_opt"]:.4f}')

    # ---------- marginals under each treatment
    print('\n' + '=' * 90)
    print('SUPPORT — surrogate marginals under each treatment (is the ORDERING stable?)')
    print('=' * 90)
    print(f'  {"normalization":28}' + ''.join(f'{s:>13}' for s in SURR3))
    for name, M in treatments:
        sm = M.mean(axis=(0, 2))
        print(f'  {name:28}' + ''.join(f'{v:13.4f}' for v in sm))
    print(f'\n  {"normalization":28}' + ''.join(f'{o:>13}' for o in OPT3))
    for name, M in treatments:
        om = M.mean(axis=(0, 1))
        print(f'  {name:28}' + ''.join(f'{v:13.4f}' for v in om))

    dst = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'eta_robustness_out.json')
    json.dump(out, open(dst, 'w'), indent=1, default=float)
    print(f'\nWROTE {dst}')


if __name__ == '__main__':
    # self-check: an optimizer-driven grid must give eta2_opt >> eta2_surr under every arm
    R = np.array([[[OPT3.index(o) + 0.01 * i for o in OPT3] for s in SURR3] for i in range(3)], float)
    for nm, f in [('minmax', n_minmax), ('rank', n_rank), ('z', n_zscore), ('raw', n_raw)]:
        es, eo, ei = eta2_from_M(f(R))
        assert eo > es, f'{nm}: optimizer-driven grid gave surr={es} opt={eo}'
    # and eta2_from_M must reproduce run05's algebra on the paper's own M
    print('self-check OK (optimizer-driven grid -> eta2_opt > eta2_surr under all arms)\n')
    main()
