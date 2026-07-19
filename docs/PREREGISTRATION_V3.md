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

# 0C — Budget-matched optimizer arm on Design-Bench (DBM1/DBM2)

Registered BEFORE the matched run, appended 2026-07-19. Engine: the `dbm` env (python
3.9.23, torch 2.8.0+cpu, numpy 1.23.5, botorch 0.10.0, gpytorch 1.11, cma 4.4.4) — the same
env and the same `--db-subsample 8000` protocol that produced `results/db_corners/`. beta=2,
K=5, TOP=128, 16 seeds (`0..15`), 7 tasks (TFBind8, TFBind10, Superconductor, GFP, UTR +
AntMorphology, DKitty), 9 cells, all four engine corners. Every record carries the 19-field
engine stamp.

**Why this arm exists.** `docs/CLAIM_LEDGER.md` D19 ships the Design-Bench optimizer half as
**PROVISIONAL**: 0-A.3 matched surrogate-query budgets on the seven *synthetic* tasks only, so
on Design-Bench eta2_opt still leads eta2_surr with D08's budget confound unremoved. This arm
removes it, or fails to.

## Measured native budgets — instrumented, not derived

`code/db_budget_probe.py`, 3 seeds x 3 surrogates, Q = candidate points scored by the
surrogate per cell (search plus the `_select_top` pass), the identical definition and counter
used by `code/budget_probe.py`, so DB and synthetic Q are directly comparable.

| task | d | grad | perturb | cma (median) |
|---|---|---|---|---|
| TFBind8 | 32 | 51,456 | 4,352 | 6,532 |
| TFBind10 | 40 | 51,456 | 4,352 | 6,542 |
| DKitty | 56 | 51,456 | 4,352 | 6,528 |
| AntMorphology | 60 | 51,456 | 4,352 | 6,528 |
| Superconductor | 86 | 51,456 | 4,352 | 6,530 |
| UTR | 200 | 51,456 | 4,352 | 6,516 |
| **GFP** | 4,740 | 51,456 | 4,352 | **570** |

Three measured facts that set the design.

1. **grad and perturb spend exactly what they spend on synthetic.** Their query counts are
   fixed by TOP, OPT_STEPS and the round/sigma schedule, none of which depend on the task, so
   the 11.8x imbalance transfers to Design-Bench by construction rather than by coincidence.
2. **X3 changes the accounting, and therefore the target.** Measured in the off_off corner
   (TFBind8, Superconductor): grad **25,600**, perturb **4,096**, cma ~6,530. With X3 on grad
   rescores its whole trajectory pool through `_select_top` (Q = 256(2s+1)); with X3 off it
   returns the final iterate and never rescores (Q = 256s). Matching every corner to one
   global Q would hand grad **2x its native budget** in the X3-off corners — the opposite of
   the synthetic protocol's "grad unchanged". The target is therefore **each corner's own
   measured grad Q**, and the parameters are solved per corner.
3. **GFP's CMA is starved 90x, not 8x.** At d=4,740 `cma_opt` switches to sep-CMA
   (`CMA_diagonal`) and converges after 570 queries against gradient's 51,456. GFP is
   therefore the single largest budget confound anywhere in the Design-Bench grid, and it is
   one of the five tasks the published null rests on.

## Levels (solved per corner, mirroring 0A.3)

| level | rule | X3=on params | X3=off params |
|---|---|---|---|
| **native** (control) | incumbent settings, unmatched | s=100, R=5, cma native | s=100, R=5, cma native |
| **UP** (primary) | everyone gets that corner's native **grad** Q | Q=51,456: s=100, R=66, F=25,472 | Q=25,600: s=100, R=33, F=12,544 |
| **DOWN** (secondary) | everyone gets that corner's native **perturb** Q | Q=4,352: s=8, R=5, F=1,920 | Q=4,096: s=16, R=5, F=1,792 |

CMA cannot spend a large budget by raising `maxfevals` alone — it stops on
noeffectaxis/conditioncov first — so the matched CMA uses the restart loop from
`code/budget_matched.py` verbatim, reseeded at the incumbent best with the remaining budget.

**The native control is not redundant with the published corner files, and is registered as
a required arm.** This runner fits each surrogate once per (task, seed) and hands it to all
three optimizers; `run_all` rebuilds it per cell, so the global-numpy RNG stream `perturb_opt`
draws from differs. Comparing matched numbers against the *published* unmatched ones would
confound budget with call order. All native-vs-matched comparisons are made inside this
runner; the native level is separately reported against the published corners as a validity
check, and any divergence there is disclosed rather than absorbed.

## The predictions

| ID | Prediction |
|---|---|
| **DBM1** | Under matched budget on Design-Bench, the optimizer-axis inversion **PERSISTS**: in every corner that rejects the Friedman omnibus, perturbation still leads the optimizer marginal AND eta2_opt still exceeds eta2_surr. The inversion is not a budget artifact. **KILL:** if matching collapses the inversion, the DB optimizer axis was in part a budget effect and the frozen-cell explanation (`docs/CLAIM_LEDGER.md` D18, M-A) must be restated. |
| **DBM2** | eta2_surr stays at the floor (**< 0.10**) under matched budget in all four corners, so the surrogate null is not a budget artifact either. |

## Decision rules, fixed in advance

Primary task set is the **7-task** one (5 non-mujoco + Ant + DKitty), because the brief scopes
this arm to the full grid including MuJoCo and because `docs/MUJOCO_CHECK.md`'s localization
argument lives there. The 5-task and GFP-dropped sets are reported alongside and do not decide.
Primary level is **UP**. All estimators are imported from `code/analyze_db.py` unchanged, so
matched numbers pass through the identical eta2 / Friedman / bootstrap code as the published
corner numbers.

- **"The rejecting corners"** means those rejecting at Friedman *p* < 0.05 **under the matched
  run**, evaluated on its own terms. The incumbent rejecting set (on_off, off_on, on_on per
  `docs/MUJOCO_CHECK.md`) is reported for comparison but does not define the test set.
- **DBM1 CONFIRMED** iff at least one corner rejects and, in every rejecting corner, the
  optimizer marginal is maximized by `perturb` AND eta2_opt > eta2_surr (point estimates).
- **DBM1 KILL** fires iff any rejecting corner loses either condition, **or** if no corner
  rejects at all. The no-rejection branch is registered as a KILL because the inversion has
  then failed to persist as a detectable effect — but it is reported with Agarwal (2021)
  attached: non-rejection is not evidence of absence, and the eta2 point estimates are
  reported either way.
- **DBM2 CONFIRMED** iff eta2_surr < 0.10 in all four corners at the primary level.
  **KILL** iff eta2_surr >= 0.10 in any corner.
- Within-corner eta2_opt vs eta2_surr bootstrap intervals are expected to overlap, exactly as
  `docs/MUJOCO_CHECK.md` records for the unmatched grid. The claim licensed is a comparison of
  point estimates plus the cross-corner tracking argument, **never** "eta2_opt significantly
  exceeds eta2_surr". No decision rule here depends on a within-corner separation.
- **Achieved-Q audit.** Achieved Q is re-instrumented per cell. If any corner's primary level
  has >5% of cells deviating >5% from target, that corner is reported **UNVALIDATED** and the
  binary call cannot be PROMOTE. A budget-matching arm that did not match is not evidence
  about budget.

**The binary call.**
- **PROMOTE** iff DBM1 CONFIRMED and DBM2 CONFIRMED and the achieved-Q audit passes in all
  four corners. Section 6's optimizer half may then assert rather than qualify, and D19's
  PROVISIONAL status is lifted.
- **KEEP-PROVISIONAL** in every other case. The qualifier stays and this arm is reported with
  its measurements intact.

## Scope and deviations, stated in advance

- The brief says both "at X1=on X3=on" and "all four engine corners". These conflict; all four
  corners are run, since the deliverable is a per-corner table. on_on is the corner comparable
  to the synthetic arm.
- Hopper is in `db_tasks.TASKS` but is **not** part of the published 7-task DB grid and is not
  run here. The grid is the same 7 tasks as `results/db_corners/`.
- MISSING means MISSING. Any cell that fails is reported absent; the analyzer refuses to pair a
  ragged seed axis rather than silently misaligning per-seed lists.
- These verdicts are written before any matched-budget result exists.
