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

## 0C — Far-field functional form (FF1/FF2) and member independence (MI1)

Six controls have eliminated sigma, width, budget, held-out accuracy, mean smoothness and
premise coverage. What survives is a diagnosis: what differs is WHICH off-distribution
maximizers a surrogate's mean admits. 0B tried to turn that into a causal claim by
manipulating the GP's prior-mean reversion. 0C attacks the same target from the other side —
the FUNCTIONAL FORM the two mean-functions take outside the training support.

**Grounds.** Xu et al. (arXiv:2009.11848), Theorem 1: a ReLU MLP converges to a LINEAR
function along any ray from the origin outside the training support, at rate O(1/t). If that
holds here the diagnosis becomes mechanical rather than descriptive — an ensemble mean growing
linearly without bound admits unbounded maximizers at the box boundary; a GP mean reverting
toward its prior constant does not.

**Compatibility with Elimination 2.** Elimination 2 cites NTK to argue width does not matter.
0C is not inconsistent with it. The two asymptotics are in DIFFERENT variables: Xu is
asymptotic in far-field DISTANCE t along a ray at fixed width; Elimination 2 is asymptotic in
WIDTH at fixed input. A network can be width-insensitive and still linearly extrapolating.
This is recorded here so the pairing is not later read as a contradiction.

**Stated assumption.** The FF1/FF2 verdicts presuppose that the w=96 ensemble is approximately
in the NTK regime, which is what licenses the transfer of Xu's result. Where the artifacts
permit, this is checked directly by measuring ray-linearity AT the training boundary and
reporting it; where they do not, it is carried as a named assumption and not as a finding.

| ID | Prediction |
|---|---|
| **FF1** | Fitting ensemble-mean and GP-mean against a linear function along rays from the data centroid, the ENSEMBLE mean is well-fit by a linear ray-function in the far field (high R2) while the GP mean is NOT (low R2, because it reverts to its prior constant). **KILL:** if both classes are equally linear or equally non-linear far from D, the linear-extrapolation mechanism does not distinguish the classes; the paper stays a pure elimination and the diagnosis ships as a diagnosis. |
| **FF2** | The ensemble's returned optima sit preferentially at the BOX BOUNDARY — where an unbounded-growth mean is maximized — more than the GP's do. **KILL:** equal boundary-proximity between classes -> boundary-seeking is not the mechanism. |
| **MI1** | Pairwise prediction correlation across the K=5 ensemble members, measured AT the returned optima, is LOWER (members disagree more) where inversion occurs — member disagreement tracks the failure. **GROUNDS:** Ghasemipour et al. show shared targets can render an ensemble paradoxically optimistic, so member independence is load-bearing. **KILL:** no relation between member correlation and inversion -> independence is not the axis. |

**Required inputs, fixed in advance.** Each prediction is computable only from the artifact
listed against it. If an input is absent from `results/`, that arm is reported as
NOT-COMPUTABLE and STOPPED. No new training run is launched to manufacture a missing input;
manufacturing the input would make the test a fresh experiment rather than a reanalysis, and
the pre-registered verdict would no longer be the one being tested.

- FF1 requires evaluating each surrogate's posterior/ensemble mean at NEW points along rays
  (points not in D and not among the 128 returned designs). This needs a RECONSTRUCTABLE
  surrogate — ensemble member weights, or a GP fitted state_dict plus its standardization
  constants.
- FF2 requires the COORDINATES of the returned optimum x* per (task, seed, surrogate,
  optimizer), to measure distance to the box boundary. Distance-to-D (`dhat`) is not a
  substitute: it measures off-support-ness, not boundary-proximity, and the two come apart.
- MI1 requires PER-MEMBER predictions at the returned optima — the K=5 individual member
  outputs, not the collapsed ensemble mean and std.

**Decision rules, fixed in advance.**
- The binary is POSITIVE-MECHANISM iff FF1 and FF2 BOTH hold. Anything else is
  KEEP-ELIMINATION.
- A KEEP-ELIMINATION reached because an arm was NOT-COMPUTABLE is reported as
  KEEP-ELIMINATION-BY-DEFAULT and explicitly distinguished from a KEEP-ELIMINATION reached
  because a KILL condition fired on observed data. An untested mechanism is not a refuted
  mechanism, and the write-up must not let the two read alike.
- MI1 is independent of the binary: it neither establishes nor blocks POSITIVE-MECHANISM.
