"""0A.1 -- reconcile the two beta=0 GP-ensemble gap computations.

docs/GATE_KBETA.md reports gap=0.378 at beta=0 and 0.556 at beta=2, via
kbeta_analyze._gp_ens_gap. The novelty audit (docs/NOVELTY_V3.md:176) recomputed
0.504 -> 0.511 from the results file via the paper's own normalization helpers
(analysis.task_norm). These are different estimands, not a numerical disagreement.

The decisive difference is the NORMALIZER:
  path A (_gp_ens_gap): min-max over the 9 cells of THAT BETA's grid. The scale is
    re-fit per beta, so gap(beta=0) and gap(beta=2) are expressed in different units
    and their ratio is not interpretable.
  path B (task_norm):   min-max over ALL cells present for the task in ONE file.
  path C (this script, CORRECT for "GP mean-quality independent of sigma"): one
    normalizer per task, fit ONCE over the pooled cells of every beta condition being
    compared, then the gap read off at each beta. Beta-invariant units -> the beta=0
    gap and the beta=2 gap are on the same ruler and their difference is the amount of
    the GP advantage that pessimism actually adds.

Also reports the raw (unnormalized) per-task standardized marginal difference as a
normalization-free check.

Bootstrap: task+seed hierarchical, 10,000 resamples (tasks resampled with replacement;
within each drawn task, seeds resampled with replacement).

  python beta0_reconcile.py   -> results/beta0_reconcile.json
"""
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, '..', 'results')
KB = os.path.join(RES, 'kbeta')
TASKS = ['Branin-2D', 'Styblinski-5D', 'Levy-8D', 'Rosenbrock-10D',
         'Rastrigin-15D', 'Ackley-20D', 'Griewank-30D']
SURR3 = ['ens', 'botorchgp', 'svgp']
OPT3 = ['perturb', 'grad', 'cma']
CELLS = [f'{s}:{o}' for s in SURR3 for o in OPT3]
ENS_IDX = [CELLS.index(f'ens:{o}') for o in OPT3]
GP_IDX = [CELLS.index(f'{s}:{o}') for s in ('botorchgp', 'svgp') for o in OPT3]
BETAS = [0.0, 2.0]
NBOOT = 10000


def load_perseed(beta):
    """-> (T, 9, S) per-seed p100, in the CELLS order."""
    d = json.load(open(os.path.join(KB, f'grid_b{beta}.json')))
    mbo = d['mbo']
    out = []
    for t in TASKS:
        out.append([mbo[t][c]['p100']['all'] for c in CELLS])
    return np.array(out, float), d['meta']


def gap_from_cellmeans(cm, lo, rng):
    """cm: (9,) cell means for one task; (lo,rng) the task's normalizer -> scalar gap."""
    z = (cm - lo) / rng
    return z[GP_IDX].mean() - z[ENS_IDX].mean()


def path_A(per_beta_seeds):
    """GATE_KBETA / kbeta_analyze._gp_ens_gap: normalizer re-fit per (task, beta)."""
    out = {}
    for b, arr in per_beta_seeds.items():
        cm = arr.mean(axis=2)                       # (T,9) mean over seeds FIRST
        gaps = []
        for row in cm:
            lo, hi = row.min(), row.max()
            gaps.append(gap_from_cellmeans(row, lo, (hi - lo) or 1.0))
        out[b] = float(np.mean(gaps))
    return out


def path_C_normalizers(per_beta_seeds):
    """One (lo,rng) per task, fit over the pooled cell means of ALL betas compared."""
    stacked = np.concatenate([per_beta_seeds[b].mean(axis=2) for b in BETAS], axis=1)
    lo = stacked.min(axis=1)
    rng = stacked.max(axis=1) - lo
    rng[rng == 0] = 1.0
    return lo, rng


def path_C(per_beta_seeds, lo, rng):
    out = {}
    for b, arr in per_beta_seeds.items():
        cm = arr.mean(axis=2)
        out[b] = float(np.mean([gap_from_cellmeans(cm[i], lo[i], rng[i])
                                for i in range(len(TASKS))]))
    return out


def path_raw(per_beta_seeds):
    """Normalization-free: per-task z-score by that task's own pooled cell-mean sd."""
    stacked = np.concatenate([per_beta_seeds[b].mean(axis=2) for b in BETAS], axis=1)
    sd = stacked.std(axis=1)
    sd[sd == 0] = 1.0
    out = {}
    for b, arr in per_beta_seeds.items():
        cm = arr.mean(axis=2)
        d = (cm[:, GP_IDX].mean(axis=1) - cm[:, ENS_IDX].mean(axis=1)) / sd
        out[b] = float(np.mean(d))
    return out


def bootstrap(per_beta_seeds, nboot=NBOOT, seed=0):
    """Task+seed hierarchical bootstrap of the path-C gaps and their difference.

    The normalizer is REFIT inside each resample (it is part of the estimator, so its
    sampling variability must be propagated, not conditioned away)."""
    rng_ = np.random.RandomState(seed)
    T = len(TASKS)
    S = per_beta_seeds[BETAS[0]].shape[2]
    draws = {b: [] for b in BETAS}
    diffs = []
    for _ in range(nboot):
        ti = rng_.randint(0, T, T)
        si = rng_.randint(0, S, (T, S))
        cm = {}
        for b in BETAS:
            arr = per_beta_seeds[b]
            cm[b] = np.array([arr[t, :, si[k]].mean(axis=0) for k, t in enumerate(ti)])
        stacked = np.concatenate([cm[b] for b in BETAS], axis=1)
        lo = stacked.min(axis=1)
        rr = stacked.max(axis=1) - lo
        rr[rr == 0] = 1.0
        g = {}
        for b in BETAS:
            g[b] = float(np.mean([gap_from_cellmeans(cm[b][i], lo[i], rr[i])
                                  for i in range(T)]))
            draws[b].append(g[b])
        diffs.append(g[2.0] - g[0.0])
    ci = lambda a: [float(np.percentile(a, 2.5)), float(np.percentile(a, 97.5))]
    return {f'gap_beta{b}_ci': ci(draws[b]) for b in BETAS} | {
        'gap_delta_b2_minus_b0': float(np.mean(diffs)),
        'gap_delta_ci': ci(diffs),
        'p_delta_le_0': float(np.mean(np.asarray(diffs) <= 0)),
        'nboot': nboot}


def main():
    per_beta_seeds, metas = {}, {}
    for b in BETAS:
        per_beta_seeds[b], metas[b] = load_perseed(b)
    rep = {
        'tasks': TASKS, 'cells': CELLS, 'n_seeds': per_beta_seeds[0.0].shape[2],
        'engine': metas[0.0],
        'path_A_per_beta_minmax': path_A(per_beta_seeds),
        'path_raw_task_zscore': path_raw(per_beta_seeds),
    }
    lo, rng = path_C_normalizers(per_beta_seeds)
    rep['path_C_beta_invariant_minmax'] = path_C(per_beta_seeds, lo, rng)
    rep['bootstrap'] = bootstrap(per_beta_seeds)

    # per-task path-C gaps, to expose task heterogeneity
    cmA = {b: per_beta_seeds[b].mean(axis=2) for b in BETAS}
    rep['per_task_pathC'] = {
        TASKS[i]: {f'beta{b}': float(gap_from_cellmeans(cmA[b][i], lo[i], rng[i]))
                   for b in BETAS} for i in range(len(TASKS))}

    os.makedirs(RES, exist_ok=True)
    with open(os.path.join(RES, 'beta0_reconcile.json'), 'w') as f:
        json.dump(rep, f, indent=2)
    print(json.dumps({k: v for k, v in rep.items()
                      if k not in ('engine', 'cells', 'tasks')}, indent=2))


if __name__ == '__main__':
    main()
