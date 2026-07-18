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

## C2-SWING — the bidirectional smoothness manipulation (SM1/SM2/SM3), branch `c2-swing`

Registered BEFORE launch. Same engine and suite as 0A.2/0A.3: X1=on, X3=on, beta=2, K=5,
seeds `0..29`, the 7 synthetic tasks, envs/pod-synth, 19-field engine stamp on every
record, primary metric p100. Runner `code/smooth_swing.py`, analyzer `code/analyze_swing.py`.

**Why this arm exists.** C2 is currently DIAGNOSTIC. The GP beats the ensemble at
optimization while fitting worse on held-out data (0A.2 W2), the advantage survives
removing sigma (0A.1) and survives more search pressure (0A.3). "Mean geometry under
optimization" is the last explanation standing, but every result so far is observational —
we have never MOVED the proposed axis and watched the outcome follow. This arm moves it in
BOTH directions. A one-directional result is a much weaker claim: smoothing the net could
close the gap for reasons unrelated to smoothness (capacity, optimization difficulty), and
a rough GP staying strong would show smoothness was never the operative variable. Only the
bidirectional pair licenses a causal reading, which is why all three predictions must hold.

**Manipulations.** SM1 constrains each ensemble MEMBER's smoothness, leaving the
sigma-formation rule untouched (sigma is still the plain member std,
`mbo.ens_moments_raw`), so any movement in the gap is attributable to mean geometry rather
than to a changed uncertainty. Two mechanisms, because they fail differently: a gradient
penalty `lam * E||d f/d x||^2` (`lam` in {0.01, 0.1, 1.0}, log-spaced across three decades)
trades smoothness against fit through the loss; spectral normalization bounds the Lipschitz
constant architecturally and cannot be traded off.

SM2 roughens the GP by kernel only, holding subsample, standardization, LCB closure and
beta at the smooth-GP baseline. Two corrections to the naive design, both forced by
pre-launch calibration on seeds 100/101 (`code/swing_calib.py`, `code/swing_calib2.py`):

1. The incumbent `botorchgp` is **RBF**, not Matern-5/2 — BoTorch 0.18's `SingleTaskGP`
   default is `RBFKernel` (verified by inspection). RBF is infinitely differentiable, so
   the incumbent "smooth GP" is maximally smooth, which if anything sharpens C2's framing.
   Repo comments calling it Matern-5/2 are wrong; the paper makes no kernel claim.
2. The lengthscale must be **FROZEN** at the smooth GP's fitted value `L`, with only
   outputscale/noise refit. Letting the marginal likelihood refit it UNDOES the
   manipulation: at `nu=0.5` the MLL compensates for the lost smoothness order by inflating
   the lengthscale (Branin 0.40 -> 15.93, Ackley 1.51 -> 9.49), returning a mean that is
   effectively SMOOTHER than baseline. An absolute short lengthscale (0.05) is separately
   DEGENERATE in high d — the mean reverts to the prior between points, so it is flat, not
   rough. Shortening is therefore RELATIVE (`L/3`).

Registered SM2 variants: `botorchgp_m12L` (`nu=0.5`, `L` frozen — isolates smoothness
order), `botorchgp_lsL3` (RBF, `L/3` frozen — isolates lengthscale), `svgp_m12` (`nu=0.5`).
Roughness uses TWO instruments, because at-data gradients understate spikiness (a sum of
sharp bumps is locally flat AT the bump centres): `rough_D` on points drawn from D, and
`rough_seg` on points BETWEEN data (convex combinations of random D pairs).

**Declared prior on SM2, recorded before launch.** Calibration already indicates the SM2
manipulation may not be deliverable at all. Across 18 configurations (`nu` in
{0.5, 1.5, 2.5, inf} x lengthscale in {L, L/3, L/5, 0.05}, plus additive
`RBF@L + a*Matern12@L/m` kernels at `a` in {0.3, 1, 3}), on 3–4 tasks and both instruments,
NO setting raised the mean's roughness by the registered 25% while preserving the fit:
`nu` changes moved roughness 0.78–1.10x, and every setting that roughened between-data
structure did so by degrading the posterior mean's amplitude toward the prior (fit falls to
0.30–0.71x). The apparent reason is structural: **a GP posterior mean conditioned on ~800
observations is smooth because of the conditioning, not because of the kernel**, so
roughness and fit quality are not independently manipulable in a fitted GP — whereas the
ensemble has excess roughness it can afford to lose (0A.2 W2 shows it is the MORE accurate
surrogate). The arm is nevertheless RUN at 30 seeds so that "SM2 is not deliverable" rests
on CIs over scores, coverage and both roughness instruments rather than on a 2-seed probe.
If the registered VOID rule fires, the binary call is SHIP-PURE-D and non-deliverability is
reported as a methodological finding — NOT as evidence for or against C2, which it is not.

This prior is recorded because concealing known calibration results would make the
pre-registration ceremonial. The VOID rule and the binary call were fixed before any of it
was run, and neither is being adjusted now to accommodate the expected outcome.

**Estimand.** Every gap is the beta-invariant/pooled normalizer of `docs/BETA0_RECONCILE.md`
(`analyze_v3.pooled_norm`): ONE per-task min–max fit over the pooled seed-mean cells of
EVERY condition in the comparison set, never refit per condition. CIs are task+seed
hierarchical bootstrap, 10,000 resamples, normalizer refit inside each resample. The
smooth-GP reference is the incumbent `botorchgp`+`svgp` pair, matching `_gp_ens_gap`.

| ID | Prediction |
|---|---|
| **SM1** | Constraining the ensemble mean's smoothness (spectral norm OR gradient penalty per member) toward the GP's, holding sigma formation fixed, CLOSES the GP–ensemble gap and stops gradient collapse. **GROUNDS:** if the GP's advantage is that its mean admits fewer off-distribution maximizers, then making the ensemble's mean comparably smooth should transfer the advantage. **KILL:** gap unchanged -> mean-smoothness is not the axis, C2 stays diagnostic (no causal upgrade), ship pure D. |
| **SM2** | A Matern-1/2 GP (or short fixed lengthscale) COLLAPSES under aggressive optimization and its own-proposal premise coverage drops from the smooth-GP baseline. This is the RISKED prediction — theory FORBIDS a rough GP staying robust. **KILL:** rough GP stays robust -> smoothness-as-causal-axis falsified, ship pure D. |
| **SM3** | SM1 holds at w=1024 (Stage 0's widest ensemble) — the mechanism is not a width confound. **KILL:** SM1 vanishes at wide width -> it was width, ship pure D. |

**Manipulation check (gates everything, fixed in advance).** `roughness` = normalized mean
gradient norm of the surrogate's MEAN function, `E||d mu/d x||_2 / std(f)`, measured on 500
points drawn FROM D (not uniform — the P0-5 fix) and separately on each optimizer's own
proposals. A manipulation that does not move its target is not evidence about the target:

- SM1 is **VOID** (neither confirmed nor killed) unless at least one smoothing variant
  reduces on-D roughness by >=25% vs the `base` ensemble, pooled across tasks.
- SM2 is **VOID** unless at least one roughened kernel raises on-D roughness by >=25% vs
  its own smooth counterpart.
- A VOID arm is reported as VOID and forces SHIP-PURE-D, exactly as a KILL does. It does
  NOT license a retuned second attempt inside this arm.

**Decision rules, fixed in advance.**

- `gap(v)` = mean over tasks of [mean of the 6 normalized smooth-GP cells] − [mean of the 3
  normalized cells of ensemble variant `v`], all on the pooled normalizer.
  `shrinkage(v) = 1 − gap(v)/gap(base)`.
- **SM1 CONFIRMED** iff some smoothing variant `v` has (a) the CI on `gap(base) − gap(v)`
  excluding 0 in the CLOSING direction, and (b) point `shrinkage(v) >= 0.50`. Because 4
  variants are screened, (a) uses a Bonferroni-corrected 98.75% CI (`1 − 0.05/4`). The
  variant satisfying both with the largest shrinkage is the **SM1 winner**, carried to SM3.
- **SM1 PARTIAL** iff some variant closes significantly (a) but no variant reaches 50%
  shrinkage. PARTIAL is NOT confirmation and forces SHIP-PURE-D.
- **SM1 KILL** iff no variant's closing CI excludes 0.
- **SM1b (supporting, not decisive):** the `grad` optimizer's inversion rate — the fraction
  of (task, seed) cells whose returned set is worse than the x0 already held
  (`x0_inversion.py`'s estimand) — falls for the SM1 winner vs `base`. Reported with its CI
  whatever SM1 does; it cannot rescue a KILL and cannot veto a CONFIRM.
- **SM2 CONFIRMED** iff at least 2 of the 3 roughened variants show BOTH (i) a significant
  DROP in normalized p100 vs their smooth counterpart, paired by (task, seed), 95% CI on
  the paired difference excluding 0, and (ii) a significant drop in own-proposal coverage
  `c_ood` on the same cells. Both axes, because a score drop alone is consistent with the
  rough kernel simply fitting worse; the coverage drop is what ties it to the premise.
- **SM2 KILL** iff no roughened variant shows a significant score drop — i.e. the rough GP
  stays robust, which the smoothness account forbids.
- **SM2 PARTIAL** (score drops but coverage does not, or only 1 of 3): forces SHIP-PURE-D.
- **SM2b (supporting):** whether the roughened GP still beats the `base` ensemble. The
  sharpest reading of "collapse" is that it stops doing so; reported, not decisive.
- **SM3 CONFIRMED** iff the SM1 winner, re-evaluated at w=1024 against the same smooth-GP
  reference, again satisfies both SM1 clauses (closing CI excluding 0 at the corrected
  level, and shrinkage >= 0.50).
- **SM3 KILL** iff the SM1 winner's closing CI at w=1024 includes 0. If SM1 itself is
  KILLED or VOID, SM3 is reported UNTESTABLE (there is no winner to carry), and the binary
  call is SHIP-PURE-D regardless.

**The binary call.** `docs/MECHANISM_SWING.md` records the three verdicts and exactly one
of:
- **FOLD** — iff SM1 CONFIRMED **and** SM2 CONFIRMED **and** SM3 CONFIRMED. C2 upgrades to
  a scoped causal section and this branch merges at Gate 2.
- **SHIP-PURE-D** — iff ANY arm is KILLED, PARTIAL, VOID, or UNTESTABLE. The paper ships as
  pure Identity D and this branch touches nothing in the draft.

There is no third outcome and no post-hoc reweighting of the three arms. In particular, SM1
confirming while SM2 kills is SHIP-PURE-D, not "partial mechanism evidence" — that
combination is precisely the falsification the bidirectional design was built to detect.

**Declared post-hoc robustness check (NOT a decision rule).** SM1's pooled normalizer spans
the smooth GPs and all five ensemble variants, and min–max is sensitive to its extremes: a
variant that collapses becomes a task's new minimum and compresses every other condition's
normalized spread, which could manufacture or mask shrinkage. `analyze_swing.py` therefore
also recomputes the SM1 winner's gap on a normalizer pooled over only {smooth GPs, base,
winner}. This was written before launch but is explicitly a robustness check on the
estimand, not a registered criterion: it cannot change a verdict, and if it disagrees with
the pooled-normalizer result that disagreement is reported in `MECHANISM_SWING.md` as a
caveat on the headline.

**Pre-launch calibration (declared).** Knob ranges (`lam` decades, `nu=0.5`, lengthscale
0.05) and the grid's compute size were chosen from a smoke run on seeds **100/101**, which
are DISJOINT from the analysis seeds `0..29`; `code/swing_smoke.py` also asserts that the
default (knobs-off) path reproduces `results/kbeta/grid_b2.0.json` bit-exactly, since both
knobs default to off and any drift would invalidate the Stage-0 corpus. No pre-registered
contrast on seeds 0..29 was computed before this document was committed.

---

## Shared commitments

- MISSING means MISSING. Any cell that fails to run is reported as absent; no imputation,
  no dropping a task to make a curve monotone.
- The verdicts above are written before seeing any 0A.2/0A.3 result. If an outcome falls
  outside the pre-registered decision rules, that is reported as such rather than
  reinterpreted.
- `docs/SESSION_STATE.md` updated after each unit.
