# Pre-registration V3 — width ablation (W1/W2) and budget-matched optimizer arm (BM1)

Registered BEFORE launch. Engine: X1=on, X3=on (audited/on_on), 30 seeds (`0..29`), 7
synthetic tasks (Branin-2D, Styblinski-5D, Levy-8D, Rosenbrock-10D, Rastrigin-15D,
Ackley-20D, Griewank-30D), envs/pod-synth (torch 2.11.0+cpu, numpy 2.4.4, sklearn 1.8.0,
botorch 0.18.1, gpytorch 1.15.2, cma 4.4.4). Every record carries the 19-field engine
stamp. Primary metric p100 (best of the 128 proposals), as in the camera grid.

Both arms report the GP–ensemble gap on the **beta-invariant normalizer** established in
`docs/BETA0_RECONCILE.md` (one per-task min–max fit over the pooled cell means of every
condition being compared), NOT the per-condition refit normalizer of
`kbeta_analyze._gp_ens_gap`. All CIs are task+seed hierarchical bootstrap, 10,000
resamples, normalizer refit inside each resample.

---

## 0A.2 — Width ablation (answers the NTK objection, N5)

**RUN:** 3x3 grid (surrogate x optimizer), X1=on X3=on, K=5 fixed, beta=2, ensemble member
hidden width w in {96, 256, 512, 1024}, 30 seeds, 7 tasks. Architecture is the existing
2-hidden-layer MLP (`code/mbo.py:137-142`); w sets both hidden layers. w=96 is the paper's
incumbent (`HID = 96`, `code/mbo.py:22`) and must reproduce the existing beta=2 numbers.
GP/SVGP rows are width-independent and are fit once per (task, seed) and reused across all
w. Also record held-out RMSE and NLL per (task, w) on a held-out split of D.

| ID | Prediction |
|---|---|
| **W1** | Holding K=5 fixed and sweeping ensemble member hidden width w in {96, 256, 512, 1024}, the GP–ensemble gap does NOT close as w grows. **GROUNDS:** the NTK/spectral-bias objection (Jacot et al. 2018; Lee et al. 2019; Rahaman et al. 2019) says a wider, better-trained net should have a smoother mean and approach a GP — so if "jagged ensemble mean" is really a finite-width artifact, a wide ensemble should catch the GP. **KILL:** if the gap closes monotonically toward zero as w -> 1024, the mean-smoothness advantage is a width artifact (favors reframing C2 as "controlled ensembles need adequate width", not a class property) and the NTK objection is CONFIRMED. If the gap persists at w=1024, the objection is empirically answered and C2's mean-quality claim is a genuine class property at practical widths. |
| **W2** | The ensemble's held-out RMSE improves with w but its optimization score does not catch the GP even where RMSE ties — i.e. accuracy is not the bottleneck, the mean's off-distribution geometry is. |

**Decision rules, fixed in advance.**
- W1 KILL fires iff the gap is monotonically non-increasing across w in {96, 256, 512, 1024}
  AND gap(w=1024) < 0.5 x gap(w=96) AND the 95% CI on gap(w=1024) includes 0.
- W1 CONFIRMED (objection answered) iff the 95% CI on gap(w=1024) excludes 0.
- Intermediate outcomes (gap shrinks materially but CI still excludes 0) are reported as
  PARTIAL, with the shrinkage fraction stated and C2 scoped accordingly. No post-hoc
  redefinition of "closes".
- W2 is evaluated only on (task, w) pairs where the ensemble's held-out RMSE is statistically
  indistinguishable from the GP's (overlapping 95% CIs). If no such pair exists, W2 is
  reported UNTESTABLE, not silently dropped.

---

## 0A.3 — Budget-matched optimizer arm (de-provisionalizes eta2_opt)

**Measured native budgets** (instrumented, not derived — `code/budget_probe.py`,
`results/budget/query_budget.json`; Q = total surrogate evaluations per cell, search plus
the `_select_top` selection pass; 3 seeds x 7 tasks x 3 surrogates):

| optimizer | median Q | min | max | note |
|---|---|---|---|---|
| grad | 51,456 | 51,456 | 51,456 | 100 steps x 256 inits + 25,856-point trajectory rescore; deterministic |
| perturb | 4,352 | 4,352 | 4,352 | 256 + 5 rounds x 3 sigmas x 256 + 256; deterministic |
| cma | 6,528 | 932 | 6,536 | `budget=3000` maxfevals is a CAP that rarely binds — pycma stops on tolfun/tolx convergence first (Branin median 1,436) |

Gradient receives **11.8x** perturbation's budget and **7.9x** CMA's. This is the confound
BM1 tests. Note the audit's "256 vs 128 proposals" framing is already fixed by X3 (every
optimizer proposes exactly TOP=128, `code/mbo.py:466-471`); the surviving inequality is in
surrogate queries, not proposals. Note also that the trust-region the audit flags is NOT
active in the main grid — `run_grid_cell` calls `grad_opt` with `trust=None`
(`code/mbo.py:513-515`); it exists only for the robustness sweep. BM1 therefore tests the
budget confound alone.

**RUN:** rerun the 3x3 at X1=on X3=on, beta=2, K=5, 30 seeds, 7 tasks, with Q equalized
across the three optimizers at **two levels**, both pre-registered:

- **Level UP (primary), Q = 51,456** — everyone gets gradient's budget. grad unchanged;
  perturb rounds R=66 (256 + 3x66x256 + 256 = 51,200); cma maxfevals 25,472 with
  tolfun/tolx/tolfunhist/tolstagnation disabled so the cap binds (512 + 2x25,472 = 51,456).
  Primary because it equalizes without crippling any optimizer.
- **Level DOWN (secondary), Q = 4,352** — everyone gets perturbation's budget. perturb
  unchanged; grad steps=8 (256x(2x8+1) = 4,352); cma maxfevals 1,920 (512 + 2x1,920 = 4,352).

Reporting both levels also tests whether eta2_opt is budget-LEVEL dependent, not just
budget-BALANCE dependent. Achieved Q is re-instrumented during the run and reported
alongside the target; any cell whose achieved Q deviates >5% from target is flagged, not
silently accepted.

| ID | Prediction |
|---|---|
| **BM1** | Under a matched surrogate-query budget across all three optimizers (equalize total surrogate evaluations: gradient's 100 steps, perturbation's rounds, CMA's pop x gens all set to the same query count Q), eta2_opt on synthetic stays small (< 0.10). **GROUNDS:** the current eta2_opt=0.01 is confounded — the audit flags unequal budgets (256 vs 128 proposals) AND a trust-region constraint suppressing gradient collapse. **KILL:** if eta2_opt rises above 0.15 under matched budget, the optimizer null was a budget artifact and A's "optimizer negligible" claim does not hold; report the matched number as the honest one. |

**Decision rules, fixed in advance.**
- BM1 CONFIRMED iff eta2_opt < 0.10 at the primary (UP) level.
- BM1 KILL fires iff eta2_opt > 0.15 at the primary level.
- 0.10 <= eta2_opt <= 0.15 is reported as INCONCLUSIVE — pre-registered as a real outcome,
  not resolved by choosing a favourable secondary level.
- The primary level decides the verdict. The secondary (DOWN) level is reported in full and
  its disagreement, if any, is stated as a limitation; it does NOT override the primary.
- eta2_opt is computed by the incumbent estimator (`kbeta_analyze._eta2`,
  `code/kbeta_analyze.py:29-43`) so the matched number is directly comparable to the
  published 0.005/0.01, and additionally on the beta-invariant normalizer. Both reported.

---

## Shared commitments

- MISSING means MISSING. Any cell that fails to run is reported as absent; no imputation,
  no dropping a task to make a curve monotone.
- The verdicts above are written before seeing any 0A.2/0A.3 result. If an outcome falls
  outside the pre-registered decision rules, that is reported as such rather than
  reinterpreted.
- `docs/SESSION_STATE.md` updated after each unit.
