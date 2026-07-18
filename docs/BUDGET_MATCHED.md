# 0A.3 — Budget-matched optimizer arm (BM1)

**Verdict: BM1 CONFIRMED at the primary level — eta2_opt = 0.038, below the pre-registered 0.10
threshold; the KILL does not fire.** A's "optimizer negligible" claim survives budget matching.
But the published figure understates the effect by ~8x, the confirmation is not comfortable
(the 95% CI reaches 0.123), and matching reveals two findings the unmatched grid concealed: the
optimizer *ranking* is budget-dependent, and the surrogate effect **grows** with budget in a way
that corroborates C2's mechanism.

Pre-registered verbatim in `docs/PREREGISTRATION_V3.md` (commit `55ced44`) BEFORE launch.

**Engine:** X1=on, X3=on (on_on), beta=2, K=5, 30 seeds (`0..29`), 7 synthetic tasks,
envs/pod-synth. **Artifacts:** `results/budget/query_budget.json` (native budgets),
`results/budget/budget_matched.json` (420 cells x 9), `results/budget/budget_analysis.json`.
**Code:** `code/budget_probe.py`, `code/budget_matched.py`, `code/analyze_v3.py`.

---

## 1. The query-budget table

Budgets are **measured, not derived** (`code/budget_probe.py`): every optimizer runs against a
counting proxy around the surrogate. This matters because CMA's `budget=3000` maxfevals is a
CAP that rarely binds — pycma stops on tolfun/tolx convergence first
(`code/mbo.py:338-362`). Q = total surrogate evaluations per cell, search plus the
`_select_top` selection pass.

### Native (published-grid) budgets

| optimizer | median Q | min | max | composition |
|---|---|---|---|---|
| **grad** | **51,456** | 51,456 | 51,456 | 100 steps x 256 inits + 25,856-point trajectory rescore |
| **perturb** | **4,352** | 4,352 | 4,352 | 256 + 5 rounds x 3 sigmas x 256 + 256 |
| **cma** | **6,528** | 932 | 6,536 | task-dependent: converges before its cap (Branin median 1,436) |

**Gradient receives 11.8x perturbation's budget and 7.9x CMA's.** That is the confound.

Two clarifications on the audit's framing. (i) The "256 vs 128 proposals" issue is already fixed
by X3 — every optimizer proposes exactly TOP=128 (`code/mbo.py:466-471`); the surviving
inequality is in *surrogate queries*, not proposals. (ii) The trust-region the audit flags is
**not active** in the main grid: `run_grid_cell` calls `grad_opt` with `trust=None`
(`code/mbo.py:513-515`); it exists only for the robustness sweep. BM1 therefore isolates the
budget confound alone.

### Achieved Q under matching

| level | target Q | perturb | grad | cma | cells >5% off target |
|---|---|---|---|---|---|
| **UP** (primary) | 51,456 | 51,200 (−0.50%) | 51,456 (0.00%) | 51,472 (+0.03%) | **0 / 630** |
| **DOWN** (secondary) | 4,352 | 4,352 (0.00%) | 4,352 (0.00%) | 4,372 (+0.46%) | **0 / 630** |

Matching is tight at both levels. Matching CMA *upward* required restarts, not merely disabling
tolerances: a converged CMA also stops on `noeffectaxis`/`conditioncov`, so maxfevals never
binds (5,144 achieved against a 25,472 cap on Branin-2D). `_cma_fixed`
(`code/budget_matched.py`) restarts from the incumbent best until the budget is spent — sigma0
and popsize unchanged, so the only difference from the incumbent `cma_opt` is feval count.

---

## 2. Matched eta2

| configuration | eta2_opt | 95% CI | eta2_surr | 95% CI | eta2_inter |
|---|---|---|---|---|---|
| **unmatched (published)** | **0.0046** | — | 0.4064 | [0.285, 0.564] | 0.1608 |
| **matched UP, Q=51,456 (primary)** | **0.0379** | **[0.0027, 0.1234]** | **0.5256** | [0.421, 0.719] | 0.1103 |
| matched DOWN, Q=4,352 (secondary) | 0.0664 | [0.0138, 0.3398] | 0.2426 | [0.189, 0.355] | 0.1566 |

eta2 is computed with the incumbent estimator (`kbeta_analyze._eta2`, re-implemented in
`code/analyze_v3.py` and verified to reproduce it to 1e-12 on `grid_b2.0.json`: 0.406364 /
0.004564 / 0.160763) so the matched number is directly comparable to the published 0.005. On the
condition-invariant normalizer of `docs/BETA0_RECONCILE.md` the values are essentially identical
(UP 0.0379, DOWN 0.0591), so this conclusion is not a normalization artifact.

### Verdict

> **BM1 CONFIRMED.** At the primary (UP) level eta2_opt = **0.038 < 0.10**. The optimizer null
> survives budget matching; the pre-registered KILL (>0.15) does not fire, and the 95% CI upper
> bound of 0.123 excludes the KILL threshold. A's "optimizer negligible" claim holds under a
> matched surrogate-query budget.

**Three qualifications, none of which overturn the verdict but all of which belong in the paper.**

1. **The published 0.005 understates the optimizer effect ~8x.** Matching raises eta2_opt from
   0.0046 to 0.0379. The budget imbalance *was* suppressing the optimizer main effect, exactly
   as the audit suspected — it simply was not suppressing enough to change the conclusion.
   **0.038 [0.003, 0.123] is the honest number and should replace 0.005 in the paper.**
2. **The confirmation is not comfortable.** The CI upper bound (0.123) lies above the 0.10
   confirm threshold, inside the pre-registered [0.10, 0.15] inconclusive band. The point
   estimate confirms and the KILL is excluded at 95%, but the data cannot rule out an optimizer
   effect up to ~0.12. This is an n=7-tasks precision limit, the same one KB5 identified.
3. **The secondary level does not corroborate cleanly.** At DOWN, eta2_opt = 0.066 with CI
   [0.014, 0.340] — an upper bound well above the KILL threshold. Per the pre-registration the
   primary level decides and the secondary does not override, so BM1 stands as CONFIRMED. But
   the honest statement is that at low budget the data are consistent with a non-negligible
   optimizer effect, and the optimizer null is best described as **established at high budget,
   underpowered at low budget**.

---

## 3. Two findings the unmatched grid concealed

### 3.1 The optimizer ranking is budget-dependent

Optimizer marginals (condition-invariant normalizer, so levels are comparable):

| configuration | perturb | grad | cma | best |
|---|---|---|---|---|
| unmatched (published) | 0.529 | 0.597 | 0.573 | grad |
| matched UP (Q=51,456) | **0.732** | 0.593 | 0.558 | **perturb** |
| matched DOWN (Q=4,352) | 0.524 | **0.731** | 0.573 | **grad** |

The ranking **flips**. Gradient wins at low budget; perturbation wins at high budget. The
unmatched grid sat near the DOWN ordering for perturbation while giving gradient the UP budget,
which is precisely how an 11.8x imbalance hides itself: it made gradient look modestly best
everywhere. eta2_opt stays small because the *spread* is small, but "which optimizer to use"
is budget-dependent and the paper should not imply otherwise. A low eta2_opt licenses "the
optimizer choice explains little variance", **not** "the optimizer choice is arbitrary".

### 3.2 The surrogate effect grows with budget — and this corroborates C2

eta2_surr more than doubles from DOWN to UP (0.243 -> 0.526), driven by the ensemble marginal
falling as budget rises:

| level | ens | botorchgp | svgp |
|---|---|---|---|
| DOWN (Q=4,352) | **0.361** | 0.755 | 0.713 |
| UP (Q=51,456) | **0.240** | 0.849 | 0.794 |

Give every optimizer more surrogate queries and the ensemble gets **relatively worse** while both
GPs get better. That is the direct behavioural signature C2 predicts: if the ensemble's mean has
exploitable off-distribution maxima, then more search pressure finds them, and more budget makes
the ensemble worse rather than better. The GP's smoother mean has less to exploit, so it
converts budget into score.

This is independent corroboration of the mechanism from a different axis than 0A.1 (sigma) or
0A.2 (width), and it was not something the arm was designed to test — it should be reported as
an observation, not as a pre-registered result.

---

## 4. What this does to the paper

1. **Replace eta2_opt = 0.005 with 0.038 [0.003, 0.123]**, described as budget-matched. Cite the
   query-budget table so the matching is auditable.
2. **Keep the optimizer-null claim, but scope it.** "The optimizer main effect is small
   (eta2_opt = 0.038) under a matched surrogate-query budget of 51,456 evaluations" is
   supported. "The optimizer does not matter" is not — the best optimizer changes with budget.
3. **Report the DOWN-level disagreement** as a stated limitation rather than omitting it. The
   optimizer null is established at high budget and underpowered at low budget.
4. **eta2_surr is budget-dependent too** (0.243 to 0.526). Any headline eta2_surr must state its
   budget alongside its K and beta. This adds a fourth axis to the KB1/KB2 finding that the
   surrogate effect's magnitude is a joint artifact of the operating point; the *direction*
   remains robust at every budget tested (GP marginal ~0.75-0.85 vs ensemble ~0.24-0.36).
5. The §3.2 budget-scaling result is worth a short paragraph in C2's mechanism section as
   corroborating evidence.
