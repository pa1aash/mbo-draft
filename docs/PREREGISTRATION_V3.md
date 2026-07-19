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

---

# 0B — Positive mechanism for C2: off-support phantom maxima (PM1/PM2/PM3)

Registered BEFORE launch, appended 2026-07-19. Engine: X1=on, X3=on, beta=2, K=5, 30 seeds
(`0..29`), the same 7 synthetic tasks and the same `envs/pod-synth` lock as 0A.2/0A.3. Every
record carries the 19-field engine stamp. Primary metric p100. Gap CIs are task+seed
hierarchical bootstrap, 10,000 resamples, on the condition-invariant (beta-invariant)
normalizer of `docs/BETA0_RECONCILE.md`, normalizer refit inside each resample.

**Why this arm exists.** Six controls have eliminated sigma (0-A.1), member width (0-A.2),
search budget (0-A.3), held-out accuracy (W2), mean smoothness and premise coverage (the M1
manipulation) as explanations of the GP-ensemble gap. The surviving statement is a
*diagnosis*: what differs is WHICH off-distribution maximizers a surrogate's mean admits, not
how rough it is. This arm tries to convert that diagnosis into a positive, measured mechanism.
If it fails, C2 ships as a pure elimination result, unchanged.

**The hypothesis.** The ensemble's mean has spurious local maxima in off-distribution regions
that the GP's posterior mean does not, because the GP's mean is pinned toward the data mean
(prior reversion) far from D while the ensemble's members extrapolate freely and their average
produces high-scoring phantom optima.

## Disclosure — what was looked at before this registration was written

A design probe was run before registering, on **3 tasks (Styblinski-5D, Ackley-20D,
Griewank-30D) at seed 0 only**, to establish that the PM2 manipulation is implementable at
all. The probe computed **one quantity**: the GP's posterior mean at 512 uniform points in the
cube, as a function of the prior-mean constant and of the kernel lengthscale. It established
that (a) at the fitted lengthscale, raising the prior-mean constant by +20 standardized units
moves the far-field posterior mean by less than 0.3 units, and (b) reversion becomes complete
once the lengthscale is scaled to 0.1x its fitted value. Both facts are used below to *build*
the manipulation and to set the MC-1 gate; **that gate is therefore not a neutral test and is
not reported as one**. No optimization score, no p100, no gap, no distance-to-D and no
inflation figure was computed before this file was committed. PM1 is untouched by the probe.

## Measured quantities

Per returned design x (all 128 proposals of every cell), recorded at run time:

- `mu(x)` — the surrogate's **mean** in raw target units (not the LCB the optimizer ascends).
- `sd(x)` — the surrogate's std, raw units.
- `f(x)` — the noiseless oracle value.
- `d10(x)` — mean Euclidean distance to the 10 nearest neighbours of x in the **full offline
  dataset D** (not the GP's 800-point subsample; distance-to-support is a task property and
  must not depend on which surrogate is being scored). The GP's own fit-subset distance is
  recorded alongside as a secondary field.

Derived, per cell, with the per-task constants `rho_tau` and `sd_y` written into the artifact
so every number is re-derivable:

- **Distance** `Dhat(x) = d10(x) / rho_tau`, where `rho_tau` is the median over D of a dataset
  point's own mean 10-NN distance. Dimensionless: `Dhat = 1` means "as far out as a typical
  dataset point sits from its own neighbours". This is what makes 2-D and 30-D poolable.
- **Inflation** `I(x) = (mu(x) - f(x)) / sd_y`, sd_y = std of the offline targets. Positive
  means the surrogate over-predicts: the phantom quantity.
- **Oracle value** `Z(x) = (f(x) - mean(y_D)) / sd_y`.

**The returned optimum** `x*` of a cell is the returned design with the largest `mu` — "the
argmax of the surrogate's mean reached by the optimizer". The argmax of the **LCB** (the point
the pipeline actually acts on) is recorded and reported as a robustness read; `x*` decides.

## Arms

Eight surrogates x three optimizers x 7 tasks x 30 seeds. The four GP rows marked (2x2) are
built by copying the incumbent GP's fitted `state_dict` and overwriting one or both of
(prior-mean constant, lengthscale), so they are exactly crossed and cost no extra MLL fit.

| arm | prior-mean constant | lengthscale | role |
|---|---|---|---|
| `ens` | — | — | incumbent ensemble |
| `svgp` | — | — | third surrogate axis, reported not manipulated |
| `botorchgp` | fitted by MLL | fitted (2x2) | incumbent GP |
| `gpm_ph` | z_max + 20, post hoc | fitted (2x2) | reversion knob alone, kernel identical |
| `gpm_ls` | fitted | 0.1x fitted (2x2) | lengthscale alone |
| `gpm_lssup` | z_max + 20, post hoc | 0.1x fitted (2x2) | the genuinely reversion-removed GP |
| `gpm_max` | z_max, frozen before fit | refit by MLL | PM2 as briefed, dose 1 |
| `gpm_sup` | z_max + 20, frozen before fit | refit by MLL | PM2 as briefed, dose 2 |

`z_max` is the largest standardized target in the GP's own 800-point subsample, so a constant
of `z_max` puts the prior at the data max and `z_max + 20` puts it strictly above every
observation. `gpm_max`/`gpm_sup` freeze the constant and let the MLL choose the kernel — the
literal reading of "refit the GP with an inflated prior-mean constant". `gpm_ph` fixes the
kernel instead, so the two together separate the manipulation from the fit's compensation.

## The predictions

| ID | Prediction |
|---|---|
| **PM1 (phantom maxima exist and are off-support)** | Across all 7 tasks x 30 seeds x 3 optimizers, the ensemble's returned optima `x*` sit at systematically LARGER `Dhat` than the incumbent GP's, AND carry systematically larger inflation `I`. **GROUNDS:** if the surviving diagnosis is right, the two classes differ in *where* their means put their maxima; the ensemble's free extrapolation should place them further out and should over-predict there. **KILL:** if ensemble and GP optima sit at the same distance-to-D with the same inflation — both 95% CIs on the paired difference covering 0 — the phantom off-support maxima account is wrong, C2 stays a pure elimination, and the diagnosis ships unchanged. |
| **PM2 (the mechanism is prior reversion, testable directly)** | A GP whose mean does not revert toward the data mean far from D starts to admit phantom optima (its `x*` move to larger `Dhat` and larger `I`) and its gap over the ensemble SHRINKS. **KILL:** if the reverted and non-reverted GP perform identically — the 95% CI on the gap shrinkage covering 0 — prior reversion is not the mechanism. |
| **PM3 (characterize, don't just detect)** | The joint distribution of (`Dhat`, `Z`, `I`) for returned optima is reported across every cell x task x seed, so the mechanism is a measured landscape property rather than an assertion. |

## Decision rules, fixed in advance

**PM1.** Paired at (task, seed, optimizer), ensemble minus incumbent `botorchgp`; task+seed
hierarchical bootstrap, 10,000 resamples.
- **CONFIRMED** iff `mean(Dhat_ens - Dhat_gp) > 0` with 95% CI excluding 0 **AND**
  `mean(I_ens - I_gp) > 0` with 95% CI excluding 0.
- **KILL** iff both CIs cover 0.
- **PARTIAL** iff exactly one limb holds. PARTIAL is a real pre-registered outcome, reported
  with the surviving limb named; it does **not** count as PM1 holding.
- The pooled `{botorchgp, svgp}` comparison used by the incumbent gap estimator is reported
  as a secondary read. `botorchgp` alone decides, because it is the arm PM2 manipulates.

**PM2.** Primary manipulation `gpm_sup` (the briefed one). Reported for every arm.
- **MC-1, the manipulation check.** Let `FF(arm)` be the arm's mean posterior mean over 512
  uniform points in the cube, in `sd_y` units, and `c` the arm's prior constant in the same
  units. Define the reversion-removal fraction `R = (FF(arm) - FF(botorchgp)) / (c - FF(botorchgp))`.
  MC-1 passes for an arm iff `R >= 0.25` with 95% CI excluding 0.25 — the arm's far field must
  travel at least a quarter of the way from the incumbent's level to its own prior constant.
- **CONFIRMED** iff MC-1 passes **AND** the gap shrinkage `gap(botorchgp) - gap(arm)` is
  positive with 95% CI excluding 0 **AND** the arm's `x*` move off-support (`Dhat` or `I`
  rises vs `botorchgp`, CI excluding 0) **AND** the held-out check below passes.
- **KILL** iff MC-1 passes and the 95% CI on the shrinkage covers 0.
- **UNINFORMATIVE** iff MC-1 fails: the knob did not move the quantity it was built to move,
  so the arm tests nothing. This is a pre-registered outcome, not a retry condition, and it is
  reported with the measured `R` and the fitted lengthscales that explain it.
- **CONFOUNDED** iff the shrinkage CI excludes 0 but the arm's held-out normRMSE exceeds
  1.25x the incumbent GP's with the 95% CI on the ratio excluding 1.0 — a gap that shrinks
  because the surrogate got worse in-distribution is not evidence about reversion.
- Only **CONFIRMED** counts toward the binary call. `gpm_lssup` is expected to be the arm most
  likely to pass MC-1 and the most likely to be CONFOUNDED; both facts are reported, and the
  `gpm_ls` / `gpm_ph` cells exist so that lengthscale and constant can be read separately
  rather than attributed jointly.

**PM3.** DELIVERED iff `results/mechanism/phantom_maxima.json` carries, for every
(task, arm, optimizer) cell, the per-seed values and the summary (mean, sd, and the 10/50/90
percentiles across seeds) of `Dhat`, `Z` and `I` at `x*`, plus the same for the full 128-design
proposal sets. Any cell that fails to run is written as MISSING. PM3 is a completeness
commitment, not a hypothesis, and cannot be "confirmed" — only delivered or not.

**The binary call.**
- **UPGRADE** iff PM1 is CONFIRMED **and** PM2 is CONFIRMED. C2 then becomes a positive
  mechanism: "the GP's prior-mean reversion suppresses the off-support phantom optima the
  ensemble's free extrapolation admits."
- **KEEP-ELIMINATION** in every other case, including PM1 PARTIAL, PM2 UNINFORMATIVE and PM2
  CONFOUNDED. The diagnosis ships unchanged and this arm is reported as a failed upgrade
  attempt with its measurements intact.

The strict reading is registered deliberately: it is the reading that cannot be softened after
the numbers are in.

## Shared commitments

- MISSING means MISSING. No imputation, no dropped task.
- These verdicts are written before any PM1/PM2/PM3 result exists, subject to the disclosure
  above.
- `docs/SESSION_STATE.md` updated when the unit lands.
