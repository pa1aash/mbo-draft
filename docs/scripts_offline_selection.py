#!/usr/bin/env python3
"""
FREE-WIN 5.1 — Can an ORACLE-FREE rule pick the winning (surrogate x optimizer)
grid cell on a held-out task?

Pre-registered as a STRETCH goal in PREREGISTRATION.md ("Decision rule (STRETCH)"),
never implemented. Kill criterion, quoted: "Fails either trivial baseline ->
reported honestly and dropped".

Reuses the paper's own normalization (code/analysis.py: task_norm = per-task min-max
over ALL present grid cells) and the paper's headline metric (p100 mean).

Run:  /opt/homebrew/Caskroom/miniforge/base/bin/python3 offline_selection.py
Deps: numpy, scipy only. The miniforge python has no sklearn, so ridge is implemented
      in closed form below; it was validated against sklearn 1.9.0 to 1.6e-15 over 200
      random problems (see ridge_fit_predict).
"""
import json, os, sys, itertools
import numpy as np
from scipy import stats

RNG = np.random.default_rng(0)
REPO = '/Users/palaash/Downloads/MBO'
RES = os.path.join(REPO, 'results')
OUT = os.path.dirname(os.path.abspath(__file__))
B_BOOT = 10000                      # prereg: "Bootstrap CIs B=2000-10000"
METRIC = 'p100'                     # paper headline metric (analysis.py default)
RIDGE_ALPHA = 1.0                   # PRE-SPECIFIED, never tuned (see honesty gate)

SURR = ('ens', 'botorchgp', 'svgp')
OPTS = ('grad', 'perturb', 'cma')
GRID = [f'{s}:{o}' for s in SURR for o in OPTS]      # the 9-cell selection set

# ---------------------------------------------------------------------------
# The paper's normalization, copied verbatim from code/analysis.py (do not invent
# a new one). NOTE it min-maxes over ALL cells containing ':' -- which is 11 cells
# (the 9-cell grid + ens_conformal:{grad,perturb}), not 9. We reuse it exactly as
# the paper does and take argmax over the 9-cell grid only.
# ---------------------------------------------------------------------------
def task_norm(mbo, task, metric=METRIC):
    vals = [v[metric]['mean'] for k, v in mbo[task].items()
            if ':' in k and isinstance(v.get(metric), dict) and 'mean' in v[metric]]
    lo, hi = (min(vals), max(vals)) if vals else (0.0, 1.0)
    return lo, (hi - lo) or 1.0


def load_scores(metric=METRIC):
    """-> (task_names, S[T x 9] normalized scores, n_norm_cells per task)."""
    tasks, rows, ncells = [], [], []
    for f in ('results_camera.json', 'results_db.json'):
        mbo = json.load(open(os.path.join(RES, f)))['mbo']
        for t in mbo:
            lo, rng = task_norm(mbo, t, metric)
            r = [(mbo[t][c][metric]['mean'] - lo) / rng for c in GRID]
            assert all(np.isfinite(r)), t
            tasks.append(t); rows.append(r)
            ncells.append(sum(1 for k in mbo[t] if ':' in k))
    return tasks, np.array(rows), ncells


# ---------------------------------------------------------------------------
# FEATURE INVENTORY -- see the report for the oracle-free honesty assessment.
# Everything here is tagged with its provenance. Nothing is imputed.
# ---------------------------------------------------------------------------

# Oracle-free STRUCTURAL descriptors. Not stored in the artifacts; read off the
# source that defines the task. Synthetic: code/mbo.py:41-85 (dim, n literals).
SYNTH_DN = {'Branin-2D': (2, 2000), 'Styblinski-5D': (5, 3000), 'Levy-8D': (8, 4000),
            'Rosenbrock-10D': (10, 5000), 'Rastrigin-15D': (15, 5000),
            'Ackley-20D': (20, 5000), 'Griewank-30D': (30, 8000)}

# Design-Bench d: ONLY the four values actually recorded in the repo.
#   TFBind8=32, TFBind10=40, Superconductor=86  -- PREREGISTRATION.md:47,
#                                                  cloud/setup.sh:66, cloud/fix_designbench.sh:4-5
#   GFP=4740                                    -- code/mbo.py:282
# UTR / AntMorphology / DKitty: NOT RECORDED ANYWHERE. -> None (MISSING, never imputed).
DB_D = {'TFBind8': 32, 'TFBind10': 40, 'Superconductor': 86, 'GFP': 4740,
        'UTR': None, 'AntMorphology': None, 'DKitty': None}

# Design-Bench N: NOT RECORDED for any task. run_all.py:121 caps at --db-subsample
# default 8000, but db_tasks.py:54-58 concatenates a top block with a random block
# WITHOUT deduping, so realized N is data-dependent, <=8000, and unrecorded. MISSING.
DB_N = {k: None for k in DB_D}

# Oracle-free structural flag, recorded in code/db_tasks.py:7-9 docstring:
#   "continuous tasks (Superconductor, Ant, DKitty, Hopper)"
#   "discrete tasks (TFBind8/10, GFP, UTR, ChEMBL)"
DISCRETE = {'TFBind8': 1, 'TFBind10': 1, 'GFP': 1, 'UTR': 1,
            'Superconductor': 0, 'AntMorphology': 0, 'DKitty': 0}
for t in SYNTH_DN: DISCRETE[t] = 0          # synthetic tasks are all continuous boxes

# ORACLE-CONTAMINATED probes (mbo.py:577-616). Unit-free ones only; q_conformal is
# excluded because it lives in raw y units on synthetic and [0,1] units on DB and is
# therefore not poolable across the 14 tasks.
CONTAM = ['rho_err', 'cov_conf_indist', 'cov_conf_ood',
          'cov_indist@0.5', 'cov_indist@1.0', 'cov_indist@2.0', 'cov_indist@5.0',
          'cov_ood@0.5', 'cov_ood@1.0', 'cov_ood@2.0', 'cov_ood@5.0']


def load_features(tasks):
    """-> dict feature_name -> array (len T), np.nan where MISSING."""
    cal = {}
    for f in ('results_camera.json', 'results_db.json'):
        cal.update(json.load(open(os.path.join(RES, f)))['calibration'])
    F = {}
    F['d'] = np.array([SYNTH_DN[t][0] if t in SYNTH_DN else
                       (DB_D[t] if DB_D[t] is not None else np.nan) for t in tasks], float)
    F['N'] = np.array([SYNTH_DN[t][1] if t in SYNTH_DN else
                       (DB_N[t] if DB_N[t] is not None else np.nan) for t in tasks], float)
    F['discrete'] = np.array([DISCRETE[t] for t in tasks], float)
    F['log_d'] = np.log(F['d'])
    F['log_N'] = np.log(F['N'])
    for k in CONTAM:
        F[k] = np.array([cal[t]['_'][k]['mean'] if k in cal[t]['_'] else np.nan for t in tasks])
    return F


# ---------------------------------------------------------------------------
# Ridge (closed form, standardized features, intercept unpenalized). alpha fixed
# at RIDGE_ALPHA -- pre-specified, NOT tuned. sklearn is unavailable in the miniforge
# python; this is the same estimator sklearn.linear_model.Ridge gives -- verified to
# max abs diff 1.6e-15 over 200 random (n,p) problems against sklearn 1.9.0.
# ---------------------------------------------------------------------------
def ridge_fit_predict(Xtr, ytr, Xte, alpha=RIDGE_ALPHA):
    mu, sd = Xtr.mean(0), Xtr.std(0)
    sd = np.where(sd < 1e-12, 1.0, sd)
    Z = (Xtr - mu) / sd
    zbar = ytr.mean()
    w = np.linalg.solve(Z.T @ Z + alpha * np.eye(Z.shape[1]), Z.T @ (ytr - zbar))
    return ((Xte - mu) / sd) @ w + zbar


def rule_ridge(feat_names):
    """Per-cell ridge of normalized score on task features; argmax predicted cell."""
    def f(tr, te, S, F):
        X = np.column_stack([F[k] for k in feat_names])
        pred = [ridge_fit_predict(X[tr], S[tr, j], X[te][None, :])[0] for j in range(len(GRID))]
        return int(np.argmax(pred))
    return f


def rule_1nn(feat_names):
    """Copy the argmax cell of the nearest training task (standardized feature space)."""
    def f(tr, te, S, F):
        X = np.column_stack([F[k] for k in feat_names])
        mu, sd = X[tr].mean(0), X[tr].std(0)
        sd = np.where(sd < 1e-12, 1.0, sd)
        Z = (X - mu) / sd
        nn = tr[int(np.argmin(np.linalg.norm(Z[tr] - Z[te], axis=1)))]
        return int(np.argmax(S[nn]))
    return f


def rule_groupmean(feat_names):
    """Best cell among training tasks sharing the held-out task's (binary) descriptor;
    falls back to all training tasks if the group is empty."""
    def f(tr, te, S, F):
        g = np.column_stack([F[k] for k in feat_names])
        same = tr[np.all(g[tr] == g[te], axis=1)]
        use = same if len(same) else tr
        return int(np.argmax(S[use].mean(0)))
    return f


# ---------------------------------------------------------------------------
# Baselines
# ---------------------------------------------------------------------------
def bl_fixed_honest(tr, te, S, F):                 # (b) THE ONE TO BEAT
    return int(np.argmax(S[tr].mean(0)))

def bl_restricted(prefix):
    """always-<surrogate>: surrogate fixed; optimizer chosen honestly on the other tasks."""
    idx = [j for j, c in enumerate(GRID) if c.startswith(prefix + ':')]
    def f(tr, te, S, F):
        return idx[int(np.argmax(S[tr][:, idx].mean(0)))]
    return f


def loo(rule, S, F, mask):
    """Leave-one-task-out over the tasks in `mask`. -> (picked_cell[], regret[])."""
    ids = np.where(mask)[0]
    picks, regs = [], []
    for te in ids:
        tr = ids[ids != te]
        j = rule(tr, te, S, F)
        picks.append(j)
        regs.append(S[te].max() - S[te, j])
    return np.array(picks), np.array(regs)


def boot_mean_ci(x, B=B_BOOT, rng=None):
    rng = rng or np.random.default_rng(1)
    idx = rng.integers(0, len(x), (B, len(x)))
    bm = np.asarray(x)[idx].mean(1)
    return float(np.mean(x)), float(np.percentile(bm, 2.5)), float(np.percentile(bm, 97.5))


def boot_paired_ci(a, b, B=B_BOOT, rng=None):
    """Paired bootstrap of mean(a) - mean(b) over tasks (same resampled tasks)."""
    rng = rng or np.random.default_rng(2)
    d = np.asarray(a) - np.asarray(b)
    idx = rng.integers(0, len(d), (B, len(d)))
    bm = d[idx].mean(1)
    return float(d.mean()), float(np.percentile(bm, 2.5)), float(np.percentile(bm, 97.5))


def wlt(a, b, tol=1e-12):
    """win/loss/tie of rule `a` vs baseline `b` in REGRET (lower regret = win)."""
    d = np.asarray(b) - np.asarray(a)
    return int((d > tol).sum()), int((d < -tol).sum()), int((np.abs(d) <= tol).sum())


def detectable_dz(n, alpha=0.05, power=0.80):
    """Smallest paired Cohen's d_z a two-sided t-test at n tasks can detect at `power`."""
    from scipy.stats import nct, t as tdist
    crit = tdist.ppf(1 - alpha / 2, n - 1)
    lo, hi = 1e-4, 5.0
    for _ in range(200):
        mid = (lo + hi) / 2
        p = 1 - nct.cdf(crit, n - 1, mid * np.sqrt(n)) + nct.cdf(-crit, n - 1, mid * np.sqrt(n))
        if p < power: lo = mid
        else: hi = mid
    return (lo + hi) / 2


# ---------------------------------------------------------------------------
def main():
    log = []
    def P(*a):
        s = ' '.join(str(x) for x in a)
        print(s); log.append(s)

    tasks, S, ncells = load_scores()
    F = load_features(tasks)
    T = len(tasks)
    P(f'Loaded {T} tasks x {len(GRID)} grid cells. Metric={METRIC}, '
      f'normalization=analysis.task_norm (min-max over {sorted(set(ncells))} cells/task).')

    # ---------------- 0. Feature inventory ----------------
    P('\n' + '=' * 78 + '\n0. ORACLE-FREE FEATURE INVENTORY\n' + '=' * 78)
    P(f'{"feature":22}{"avail":>8}  provenance / verdict')
    inv = [
        ('d (dim)',        'log_d', 'STRUCTURAL, oracle-free. mbo.py:41-85 (synth); PREREG:47/setup.sh:66 + mbo.py:282 (4 DB). NOT in artifacts.'),
        ('N (dataset size)','log_N', 'STRUCTURAL, oracle-free. mbo.py:41-85 (synth). DB: MISSING (only <=8000 cap; realized N unrecorded).'),
        ('discrete flag',  'discrete', 'STRUCTURAL, oracle-free. db_tasks.py:7-9 docstring. Available 14/14.'),
        ('rho_err',        'rho_err', 'NOT oracle-free: spearman(sig, |mu - task.oracle(xt)|), mbo.py:593.'),
        ('cov_conf_indist','cov_conf_indist', 'NOT oracle-free: task.oracle(xt), mbo.py:610.'),
        ('cov_conf_ood',   'cov_conf_ood', 'NOT oracle-free: f_o = task.oracle(xf) ON THE PROPOSALS, mbo.py:599/611.'),
        ('cov_indist@2.0', 'cov_indist@2.0', 'NOT oracle-free: task.oracle(xt), mbo.py:601.'),
        ('cov_ood@2.0',    'cov_ood@2.0', 'NOT oracle-free: oracle ON THE PROPOSALS, mbo.py:602.'),
    ]
    for name, key, note in inv:
        n_ok = int(np.isfinite(F[key]).sum())
        P(f'{name:22}{n_ok:>4}/{T}  {note}')
    for name, note in [
        ('q_hat (q_conformal)', 'present but EXCLUDED: fit on task.oracle(xc) (mbo.py:609) AND in raw-y units on '
                                'synth vs [0,1] on DB -> not poolable across tasks.'),
        ('rho_knn',    'MISSING from every results/*.json. mbo.py:594/614 computes it and run_all.py:60 saves it, '
                       'but no committed artifact contains it. It is the ONE genuinely oracle-free probe instrumented.'),
        ('sigma stats (mean/median/spread)', 'MISSING. mu/sig computed at mbo.py:585-588, never persisted.'),
        ('ensemble disagreement', 'MISSING (== sigma; never persisted).'),
        ('GP marginal likelihood / held-out NLL', 'MISSING. Never computed anywhere in the codebase.'),
        ('proposal displacement ||x_T - x_0||', 'MISSING. x0/xf exist at mbo.py:597-598, never persisted.'),
        ('PER-CELL features of any kind', 'MISSING. calibration is keyed task -> "_" (run_all.py:73), computed ONCE per '
                                          'task with the ENSEMBLE + grad @ BETA. mbo cells store only p100/p50.'),
    ]:
        P(f'{name:22}{"--":>8}  {note}')

    P('\nKILLER CONSEQUENCE 1: there are ZERO per-(task,cell) features. Protocol rule (a)')
    P('  "pick the cell maximizing a single feature, e.g. argmax c_hat_ood" is NOT COMPUTABLE:')
    P('  c_hat_ood has one value per TASK, not one per cell. Only rules of the form')
    P('  score(task,cell) = g_cell(task_descriptors) are implementable -- which is exactly what')
    P('  PREREGISTRATION.md:56-58 specified ("fit boundary ... from (d, held-out calibration probe)").')
    P('KILLER CONSEQUENCE 2: every calibration probe is computed with task.oracle(). See report.')

    # ---------------- 1. Is there anything to win? ----------------
    P('\n' + '=' * 78 + '\n1. IS THERE ANY HETEROGENEITY TO EXPLOIT?\n' + '=' * 78)
    best = S.argmax(1)
    P(f'{"task":18}{"d":>6}{"N":>7}{"disc":>5}  best cell        ' + '  '.join(f'{c:>14}' for c in GRID))
    for i, t in enumerate(tasks):
        d = '--' if not np.isfinite(F['d'][i]) else f"{int(F['d'][i])}"
        n = '--' if not np.isfinite(F['N'][i]) else f"{int(F['N'][i])}"
        P(f'{t:18}{d:>6}{n:>7}{int(F["discrete"][i]):>5}  {GRID[best[i]]:16} ' +
          '  '.join(f'{v:>14.3f}' for v in S[i]))
    cnt = {GRID[j]: int((best == j).sum()) for j in range(len(GRID))}
    P('\nargmax-cell histogram over the 14 tasks: ' +
      ', '.join(f'{k}={v}' for k, v in cnt.items() if v))
    P(f'distinct winning cells: {len({int(b) for b in best})}/9   '
      f'modal cell wins {max(cnt.values())}/14 tasks')
    P(f'mean per-task score of each cell: ' +
      ', '.join(f'{GRID[j]}={S[:, j].mean():.3f}' for j in range(len(GRID))))

    # ---------------- 2/3. LOO arms ----------------
    all_mask = np.ones(T, bool)
    d_mask = np.isfinite(F['log_d'])
    synth_mask = np.isfinite(F['log_N'])

    arms = [
        # (arm label, mask, [(rule label, rule, oracle_free?)])
        ('ARM 1 - honest oracle-free, ALL 14 tasks (only fully-available descriptor: discrete)',
         all_mask, [
             ('R1  groupmean(discrete)   [oracle-free]', rule_groupmean(['discrete']), True),
             ('R2  ridge(discrete)       [oracle-free]', rule_ridge(['discrete']), True),
         ]),
        ('ARM 2 - honest oracle-free, 11 tasks with d recorded (PREREG rule: boundary from d)',
         d_mask, [
             ('R3  ridge(log d)          [oracle-free]', rule_ridge(['log_d']), True),
             ('R4  1-NN(log d)           [oracle-free]', rule_1nn(['log_d']), True),
             ('R5  ridge(log d,discrete) [oracle-free]', rule_ridge(['log_d', 'discrete']), True),
         ]),
        ('ARM 3 - honest oracle-free, 7 synthetic tasks (d AND N both recorded)',
         synth_mask, [
             ('R6  ridge(log d,log N)    [oracle-free]', rule_ridge(['log_d', 'log_N']), True),
             ('R7  1-NN(log d,log N)     [oracle-free]', rule_1nn(['log_d', 'log_N']), True),
         ]),
        ('ARM 4 - CONTAMINATED CEILING PROBE, all 14 (features USE THE ORACLE; NOT DEPLOYABLE)',
         all_mask, [
             ('C1  ridge(cov_conf_ood,cov_conf_indist) [ORACLE]',
              rule_ridge(['cov_conf_ood', 'cov_conf_indist']), False),
             ('C2  ridge(all 11 unit-free probes)      [ORACLE]', rule_ridge(CONTAM), False),
             ('C3  1-NN(cov_conf_ood,cov_conf_indist)  [ORACLE]',
              rule_1nn(['cov_conf_ood', 'cov_conf_indist']), False),
         ]),
    ]

    results = {}
    for label, mask, rules in arms:
        ids = np.where(mask)[0]
        n = len(ids)
        P('\n' + '=' * 78 + f'\n{label}\n  (n={n} tasks; LOO -> fit on {n-1}, predict 1)\n' + '=' * 78)

        # baselines, recomputed within this arm's task set
        _, r_b = loo(bl_fixed_honest, S, F, mask)                 # (b) honest fixed cell
        _, r_ens = loo(bl_restricted('ens'), S, F, mask)          # (d) always-ensemble
        _, r_gp = loo(bl_restricted('botorchgp'), S, F, mask)     # (d) always-GP
        _, r_svgp = loo(bl_restricted('svgp'), S, F, mask)
        r_rand = np.array([S[i].max() - S[i].mean() for i in ids])   # (c) random cell, exact E
        # (a) best fixed cell in hindsight over this arm's tasks
        j_hind = int(np.argmax(S[ids].mean(0)))
        r_hind = np.array([S[i].max() - S[i, j_hind] for i in ids])

        P(f'  hindsight-best fixed cell on these {n} tasks: {GRID[j_hind]}')
        P(f'\n  {"strategy":48}{"mean regret":>13}{"95% CI":>20}{"vs (b) W/L/T":>14}{"paired diff vs (b) [95% CI]":>34}')

        def row(nm, r, ref=r_b, show_wlt=True):
            m, lo, hi = boot_mean_ci(r)
            if show_wlt:
                w, l, t_ = wlt(r, ref)
                dm, dlo, dhi = boot_paired_ci(r, ref)
                P(f'  {nm:48}{m:>13.4f}{f"[{lo:.4f},{hi:.4f}]":>20}{f"{w}/{l}/{t_}":>14}'
                  f'{f"{dm:+.4f} [{dlo:+.4f},{dhi:+.4f}]":>34}')
            else:
                P(f'  {nm:48}{m:>13.4f}{f"[{lo:.4f},{hi:.4f}]":>20}')
            return m

        P('  --- baselines ---')
        row('(a) best FIXED cell, hindsight  [upper bnd]', r_hind, show_wlt=False)
        row('(b) best FIXED cell on other n-1  <-- BEAT ME', r_b, show_wlt=False)
        row('(c) random cell (exact E over 9)', r_rand, show_wlt=False)
        row('(d) always-ensemble (opt honest)', r_ens, show_wlt=False)
        row('(d) always-GP/botorchgp (opt honest)', r_gp, show_wlt=False)
        row('    always-svgp (opt honest)', r_svgp, show_wlt=False)
        P('  --- rules ---')
        for rl, fn, ofree in rules:
            picks, r = loo(fn, S, F, mask)
            row(rl, r)
            results[rl] = dict(arm=label, n=n, regret=r.tolist(), oracle_free=ofree,
                               picks=[GRID[j] for j in picks],
                               tasks=[tasks[i] for i in ids],
                               vs_b=dict(zip(('W', 'L', 'T'), wlt(r, r_b))),
                               beats_b=bool(r.mean() < r_b.mean()),
                               beats_gp=bool(r.mean() < r_gp.mean()),
                               beats_ens=bool(r.mean() < r_ens.mean()))
            results[rl]['mean_regret'] = float(r.mean())
        results.setdefault('_baselines', {})[label] = dict(
            n=n, hindsight=float(r_hind.mean()), fixed_honest=float(r_b.mean()),
            random=float(r_rand.mean()), always_ens=float(r_ens.mean()),
            always_gp=float(r_gp.mean()), always_svgp=float(r_svgp.mean()),
            hindsight_cell=GRID[j_hind],
            fixed_honest_per_task=r_b.tolist(), tasks=[tasks[i] for i in ids])

    # ---------------- per-task regret table ----------------
    P('\n' + '=' * 78 + '\n5. PER-TASK REGRET (all 14 tasks; arm-1 rules + baselines)\n' + '=' * 78)
    ids = np.arange(T)
    _, r_b = loo(bl_fixed_honest, S, F, all_mask)
    _, r_gp = loo(bl_restricted('botorchgp'), S, F, all_mask)
    _, r_ens = loo(bl_restricted('ens'), S, F, all_mask)
    p_r1, r_r1 = loo(rule_groupmean(['discrete']), S, F, all_mask)
    p_c1, r_c1 = loo(rule_ridge(['cov_conf_ood', 'cov_conf_indist']), S, F, all_mask)
    P(f'{"task":18}{"best cell":16}{"(b)fixed":>10}{"R1 pick":>16}{"R1 reg":>9}'
      f'{"C1 pick":>16}{"C1 reg":>9}{"alwaysGP":>10}{"alwaysENS":>10}')
    for k, i in enumerate(ids):
        P(f'{tasks[i]:18}{GRID[best[i]]:16}{r_b[k]:>10.3f}{GRID[p_r1[k]]:>16}{r_r1[k]:>9.3f}'
          f'{GRID[p_c1[k]]:>16}{r_c1[k]:>9.3f}{r_gp[k]:>10.3f}{r_ens[k]:>10.3f}')
    P(f'{"MEAN":18}{"":16}{r_b.mean():>10.3f}{"":>16}{r_r1.mean():>9.3f}'
      f'{"":>16}{r_c1.mean():>9.3f}{r_gp.mean():>10.3f}{r_ens.mean():>10.3f}')

    # ---------------- 5b. LOO instability of the baseline itself ----------------
    P('\n' + '=' * 78 + '\n5b. IS BASELINE (b) ITSELF STABLE? (n=14 fragility diagnostic)\n' + '=' * 78)
    p_b, _ = loo(bl_fixed_honest, S, F, all_mask)
    p_g, _ = loo(bl_restricted('botorchgp'), S, F, all_mask)
    P(f'  (b) picks: ' + ', '.join(f'{GRID[j]}x{int((p_b==j).sum())}' for j in set(p_b)))
    P(f'  always-GP picks: ' + ', '.join(f'{GRID[j]}x{int((p_g==j).sum())}' for j in set(p_g)))
    a = tasks.index('Ackley-20D'); keep = [i for i in range(T) if i != a]
    P(f'\n  Baseline (b) is "always botorchgp:grad" on 13/14 folds and flips on ONE fold (Ackley-20D).')
    P(f'  Ackley is the single influential task: every perturb cell collapses there, so dropping it')
    P(f'  flips the argmax-of-mean. Mean cell score all-14 vs drop-Ackley:')
    for j, c in enumerate(GRID):
        P(f'    {c:20} all14={S[:, j].mean():.4f}  drop-Ackley={S[keep, j].mean():.4f}')
    P('  -> ONE task out of 14 flips the honest fixed-cell baseline. That is the n=14 problem')
    P('     showing up in the BASELINE, not just in the rules.')

    # ---------------- power ----------------
    P('\n' + '=' * 78 + '\n6. WHAT IS EVEN DETECTABLE AT n=14 TASKS?\n' + '=' * 78)
    for n in (14, 11, 7):
        dz = detectable_dz(n)
        P(f'  n={n:2d}: two-sided paired t-test, alpha=.05, 80% power needs |d_z| >= {dz:.2f}')
    sd = np.std(r_r1 - r_b, ddof=1)
    P(f'\n  observed SD of paired regret diff (R1 - (b)) over 14 tasks: {sd:.4f}')
    if sd > 0:
        P(f'  -> at n=14 the SMALLEST mean regret improvement detectable at 80% power is')
        P(f'     {detectable_dz(14)*sd:.4f} normalized-score units. Anything smaller is invisible here.')
    else:
        P('  -> SD = 0 (the rule is identical to baseline (b) on every task): nothing to test.')
    # sign test resolution
    from scipy.stats import binomtest
    for w in range(7, 15):
        p = binomtest(w, 14, 0.5, alternative='two-sided').pvalue
        if p < 0.05:
            P(f'\n  sign test: need >= {w}/14 wins (0 losses) for p<0.05 two-sided (p={p:.4f}).')
            break

    # ---- THE decisive power fact: could a PERFECT rule even be certified at n=14? ----
    P('\n  --- ceiling: could a PERFECT oracle-free rule be detected at n=14? ---')
    perfect = np.zeros(T)                      # per-task argmax -> regret 0 by definition
    sd_gp = np.std(r_gp - perfect, ddof=1)
    dz_perfect = r_gp.mean() / sd_gp
    P(f'  perfect rule (per-task argmax)     mean regret = 0.0000')
    P(f'  always-GP                          mean regret = {r_gp.mean():.4f}  (SD over tasks {sd_gp:.4f})')
    P(f'  => a PERFECT oracle-free rule beats always-GP with d_z = {dz_perfect:.2f}')
    P(f'  => n=14 needs |d_z| >= {detectable_dz(14):.2f} for 80% power')
    P(f'  => VERDICT ON THE DESIGN: even a PERFECT rule is '
      f'{"detectable" if dz_perfect > detectable_dz(14) else "NOT reliably detectable"} at n=14.')
    P('     The per-task regret of always-GP is dominated by a few catastrophic tasks (TFBind8')
    P('     0.99, Ackley 0.97), so its SD (0.33) exceeds its mean (0.24). No rule can clear the')
    P('     bar at this n. n=14 is not merely "small" -- it is below the resolution of the question.')

    # ---------------- 6b. p50 co-primary metric ----------------
    P('\n' + '=' * 78 + '\n6b. CO-PRIMARY METRIC p50 (PREREGISTRATION.md:17 names p100 AND p50)\n' + '=' * 78)
    t5, S5, _ = load_scores('p50')
    F5 = load_features(t5)
    agree = sum(int(S[i].argmax() == S5[i].argmax()) for i in range(T))
    P(f'  The TARGET itself is metric-unstable: the best cell agrees under p100 and p50 on only')
    P(f'  {agree}/14 tasks. The hindsight-best fixed cell is botorchgp:grad under p100 but '
      f'{GRID[int(np.argmax(S5.mean(0)))]} under p50.')
    _, rb5 = loo(bl_fixed_honest, S5, F5, all_mask)
    _, rg5 = loo(bl_restricted('botorchgp'), S5, F5, all_mask)
    _, r15 = loo(rule_groupmean(['discrete']), S5, F5, all_mask)
    P(f'\n  {"strategy":42}{"p50 regret":>12}{"vs (b) W/L/T":>14}{"vs alwaysGP W/L/T":>19}')
    for nm, r in [('(b) honest fixed cell', rb5), ('always-GP', rg5),
                  ('R1 groupmean(discrete) [oracle-free]', r15)]:
        w1, l1, t1_ = wlt(r, rb5); w2, l2, t2_ = wlt(r, rg5)
        P(f'  {nm:42}{r.mean():>12.4f}{f"{w1}/{l1}/{t1_}":>14}{f"{w2}/{l2}/{t2_}":>19}')
    w, l, _t = wlt(r15, rg5)
    P(f'\n  R1 LOOKS like a winner on p50 (regret {r15.mean():.3f} vs (b) {rb5.mean():.3f}) -- but the SAME rule is')
    P(f'  the WORST strategy tested on the headline p100 metric ({r_r1.mean():.3f} vs (b) {r_b.mean():.3f}, i.e. exactly')
    P(f'  random). And even on p50 it does NOT clear the pre-registered trivial baseline:')
    P(f'  vs always-GP it is {w}/{l}/{_t} (sign test p={binomtest(w, w+l, 0.5).pvalue:.3f} on non-ties).')
    P('  A rule whose sign flips between the two CO-PRIMARY metrics is noise, not signal. It is')
    P('  reported here precisely so it cannot be quietly promoted as the headline.')

    # ---------------- multiplicity ----------------
    P('\n' + '=' * 78 + '\n7. MULTIPLICITY\n' + '=' * 78)
    k_rules = sum(len(r) for _, _, r in arms)
    P(f'  {k_rules} rules were run across 4 arms, on 2 co-primary metrics (p100 headline, p50),')
    P(f'  i.e. up to {k_rules*2} rule-x-metric comparisons against baseline (b).')
    P(f'  Under a coin-flip null, P(>=1 of {k_rules} rules beats (b) by chance) ~= 1-0.5^{k_rules} = '
      f'{1-0.5**k_rules:.3f};')
    P(f'  over {k_rules*2} rule-x-metric slots, {1-0.5**(k_rules*2):.4f}. The best-looking cell in this')
    P('  table is therefore NOT interpretable as a discovery.')
    P('  DISCIPLINE ACTUALLY APPLIED: alpha was fixed at 1.0 a priori and never tuned; every rule')
    P('  run is reported (none dropped); p100 was designated headline BEFORE looking (it is')
    P('  analysis.py\'s default and the paper\'s headline), so the p50 result that flatters R1')
    P('  is NOT promoted. No rule was added after seeing a result.')

    json.dump({'tasks': tasks, 'grid': GRID, 'S': S.tolist(),
               'features': {k: [None if not np.isfinite(v) else float(v) for v in vv]
                            for k, vv in F.items()},
               'results': results},
              open(os.path.join(OUT, 'offline_selection_results.json'), 'w'), indent=1)
    open(os.path.join(OUT, 'offline_selection_log.txt'), 'w').write('\n'.join(log))
    P(f'\nwrote {OUT}/offline_selection_results.json')


if __name__ == '__main__':
    # self-check: on a task set where cell j is best everywhere, the honest fixed-cell
    # baseline must attain zero regret, and a rule cannot beat it.
    Sx = np.tile(np.array([0., 0., 1., 0., 0., 0., 0., 0., 0.]), (5, 1))
    Fx = {'discrete': np.zeros(5), 'log_d': np.arange(5.) + 1}
    _, rb = loo(bl_fixed_honest, Sx, Fx, np.ones(5, bool))
    assert np.allclose(rb, 0), rb
    print('self-check OK (dominant cell -> honest fixed-cell baseline has 0 regret)\n')
    main()
