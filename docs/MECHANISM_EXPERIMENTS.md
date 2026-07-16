# Mechanism experiments — from diagnosis to causal test

The paper **claims** the cause is the GP's smooth posterior mean. It never manipulates
smoothness. Every current control is subtractive (β=0, matched tuning, data subsample) —
each consistent with the claim, none forcing it.

**The audit reorders this phase.** Phase 6 as briefed assumed the measurement is sound and
only the mechanism is unproven. It is not: `docs/FLAW_LEDGER.md` P0-2 shows the ensemble
trains on **raw** targets while both GPs standardize (`mbo.py:36-37` vs `mbo.py:255`,
`mbo.py:311`). Until that is removed, "smooth prior" and "the ensemble could not fit targets
of magnitude 2600" are observationally equivalent — and **no manipulation below is
interpretable.** M0 is therefore a gate, not an experiment.

Cost basis: the full synthetic grid is 7 tasks × 9 cells × 30 seeds. All CPU. Wall-clock
assumes the `--jobs` parallelism the runner already supports; single-core figures are given
where they differ materially. Design-Bench arms cost more per cell (oracle calls) and are
priced separately where relevant.

---

## M0 (GATE) · Normalize the ensemble's targets and re-run

**This is not a mechanism test. It is the precondition for every other row.**

**Hypothesis.** η²_surr = 0.37 is substantially a target-scaling artifact.

**PRE-REGISTERED PREDICTION.** Standardizing `y` inside `train_ensemble` will **materially reduce
η²_surr**, and the reduction will be **largest on the large-|y| tasks** (Griewank ≈ −2600,
Rastrigin, Ackley) and near-zero on Branin (≈ −10). Specifically: the per-task GP−ensemble gap
will correlate with `log|y|_scale` **before** the fix (ρ > 0.6) and not after (ρ ≈ 0).

**What falsifies it.** η²_surr stays ≈ 0.37 and the gap does not track `|y|` scale. **That would be
a genuinely good result** — it converts the biggest reject risk into a passed control and makes the
inductive-bias claim far stronger than it is today.

**Implementation.** In `train_ensemble` (`mbo.py:130`), z-score `y` before constructing the
`TensorDataset` and invert on prediction in `ens_lcb_torch`/`ens_lcb_np` (`mbo.py:152-158`) — the
same treatment `svgp` already applies at `mbo.py:311-312` / `mbo.py:342`. ~15 lines.

**Cost.** ~30 min edit. Full synthetic grid re-run. **Retires:** T1, P0-2, and the "underfitting is a
rename of inductive bias" objection — which is the #1 reject risk.

**Acceptance-delta.** Decisive either way. This is the highest-value CPU in the repo.

**Also run in the same pass** (they are free once you re-run): held-out RMSE/NLL per (task, surrogate).
The repo never computes them (`FLAW_LEDGER.md` P1-3), and without them "inductive bias" cannot be
separated from "fits worse" *even after* M0.

---

## M1 · Smooth the ensemble, hold σ fixed

**Hypothesis.** The gap is caused by the roughness of the ensemble's *mean*, not by its uncertainty.

**PRE-REGISTERED PREDICTION.** Constraining the ensemble mean's Lipschitz constant — while leaving
σ's construction untouched — closes most of the residual (post-M0) GP−ensemble gap and stops gradient
ascent from collapsing. Premise coverage on the ensemble's own gradient proposals rises from ≈0.41
toward the GP's ≈0.97.

**What falsifies it.** The gap persists at every smoothness level. Then the mechanism is not mean
roughness and Section 5 must be rewritten, not re-scoped.

**Implementation.** Cheapest first: (a) spectral normalization on the MLP's linear layers; (b) a
gradient penalty `λ‖∂μ/∂x‖²`; (c) input smoothing (average μ over Gaussian jitter). Sweep the
constraint strength — a *single* setting proves nothing; the dose-response is the evidence. Keep σ =
`ps.std(0)` unchanged so the manipulation is clean.

**Cost.** ~4 h edit; sweep of 4 strengths × synthetic grid ≈ 4× a grid run.

**Retires:** the "you never manipulated the thing you named" objection. **Acceptance-delta: HIGH** —
this is what converts a diagnosis into a *fix*. "Here is why the ensemble fails and here is the
one-line change that repairs it" is a different acceptance bracket than "the ensemble fails."

**Note the interaction with M0.** If M0 already closes the gap, M1 is testing a mechanism that no
longer has an effect to explain — run M0 first and re-scope. If M0 does *not* close the gap and M1
does, then undertraining is refuted by construction and the inductive-bias claim is *proven*, not
argued. That ordering is the whole point.

---

## M2 · Roughen the GP (the falsification test)

**Hypothesis.** The GP's robustness comes from prior smoothness, so a rough GP must lose it.

**PRE-REGISTERED PREDICTION.** Under Matérn-1/2 (or a fixed very short lengthscale), the GP **starts to
collapse** under gradient ascent and its premise coverage on its own proposals **drops from 0.97**.

**What falsifies it.** The rough GP stays robust → the mechanism is not prior smoothness; it is
something else the GP has (exact posterior, calibrated σ, the fitting procedure). This is the theory's
sharpest exposure: **the theory forbids a rough GP from being robust.**

**Implementation.** `SingleTaskGP` with a `MaternKernel(nu=0.5)`, and a variant with the lengthscale
fixed short. `mbo.py:250-260`. ~2 h.

**Cost.** ~2 h edit; 2 arms × synthetic grid.

**Acceptance-delta: HIGH per unit cost.** Reviewers reward a risked prediction far more than another
confirming control, and this is the cheapest risked prediction available.

---

## M3 · Smoothness interpolation family (best value in the paper)

**Hypothesis.** Prior-match is a *continuum*, and Design-Bench is not a different world — it is a point
on it.

**PRE-REGISTERED PREDICTION.** Construct `f_α = smooth base + α · high-frequency component` (or draw from
Matérn kernels with varying ν). As α rises: the GP−ensemble gap **shrinks**, η²_surr **falls**, ĉ_ood
**falls**, and the Friedman p **rises toward non-significance** — *all four together, monotonically*.
At high α the synthetic suite reproduces the Design-Bench null **continuously**.

**What falsifies it.** The four quantities move independently, or non-monotonically. Then "prior-match"
is not a single axis and the unification fails.

**Implementation.** New task family in `mbo.py` alongside the existing `ScaledAckley` ladder that
`PREREGISTRATION.md:32-36` already specifies (the ladder infrastructure exists and was never run —
reuse it). Sweep α ∈ {0, 0.25, 0.5, 1, 2, 4}. ~1 day.

**Cost.** ~1 day edit; 6 α-levels × 9 cells × 30 seeds ≈ 6 grid-equivalents. CPU-only.

**Retires:** T9 in its strongest form. Replaces the paper's weakest claim — a **two-point** comparison
at N=7 with p=0.69 — with a **trend**. A trend at 6 α-levels needs no equivalence test and no N=7 apology.

**Acceptance-delta: HIGHEST of the mechanism rows.** It unifies Contributions 2 and 3 into one curve.
This is the row I would spend the CPU on.

---

## M4 · Pessimism as distance regularization — test it, don't assert it

**Hypothesis.** βσ is doing the job of a distance-to-data penalty, not of calibrated uncertainty.

**PRE-REGISTERED PREDICTION.** Replacing `βσ` with an explicit distance penalty (k-NN distance to `D`, or
a KDE term) — **with no uncertainty at all** — matches or beats `βσ`.

**What falsifies it.** The distance penalty underperforms βσ → uncertainty carries information distance
does not, and the paper's ρ≈0.1 argument is incomplete.

**Implementation.** New acquisition in `mbo.py` next to the LCB closures. The paper currently argues this
from ρ≈0.1 and a β-sweep; that is an argument, not a demonstration. ~4 h.

**Cost.** ~4 h edit; 2 arms × grid. **Acceptance-delta: MEDIUM** — a clean standalone practical finding.

---

## M5 · Learn the density ratio (close Prop 2's open loop)

**Hypothesis.** The proposal shift is severe enough that density-ratio weighting cannot repair coverage.

**PRE-REGISTERED PREDICTION.** A logistic-regression / gradient-boosted classifier ratio `w = dΠ/dP`
fit on `D` vs `Π` will **partially but not fully** restore proposal coverage — because the proposals
concentrate on a near-measure-zero region where `w` is unbounded and the effective sample size collapses.

**What falsifies it.** It fully restores coverage (a positive result the paper currently lacks — strictly
good), or it does nothing at all (a sharper negative: the shift defeats density-ratio methods, which is
itself a real finding worth stating).

**All three outcomes are publishable. "We did not try" is the only bad one** — and it is currently the
paper's position (`proofs.md:20` names the repair and never runs it). It is a reviewer's free shot.

**Implementation.** `sklearn.linear_model.LogisticRegression` on `D` vs `Π`, clipped weights, weighted
conformal quantile per Tibshirani et al. 2019. ~1 day including the weighted-quantile plumbing.

**Cost.** ~1 day; cheap to run (no grid re-run — reuses stored proposals **if** they are persisted;
**VERIFY FIRST** — if proposals are not stored, add ~1 grid re-run).

**Acceptance-delta: MEDIUM-HIGH.** Converts Prop 2 from a restatement into a tested claim.

---

## M6 · Make Proposition 1 non-trivial

**Goal.** A statement with content: a bound relating ĉ_ood to *computable* quantities — the surrogate's
local Lipschitz constant `L` along the optimizer trajectory, the displacement budget `D = ‖x_T − x_0‖`,
the density ratio.

**Target shape.** Something of the form: *proposal coverage degrades at most Φ(L, D, β, σ_min) given
displacement D and mean smoothness L* — which would make the diagnostic **predictive** rather than
descriptive and retire the "padding" objection.

**Sketch worth attempting.** If μ is `L`-Lipschitz and `f` is `L_f`-Lipschitz on the segment `x_0 → x_T`,
then `|μ(x_T) − f(x_T)| ≤ |μ(x_0) − f(x_0)| + (L + L_f)·D`. Combined with in-distribution coverage at
`x_0`, this lower-bounds the βσ needed at `x_T`, hence upper-bounds coverage loss as a function of `D`.
All three inputs (`L` empirically along the trace, `D`, `σ`) are **measurable in the existing runs**, so
the bound could be *plotted against the realized ĉ_ood* — a bound that tracks the data is a real
contribution; one that is vacuous is not.

**HONEST STATUS: NOT YET DERIVED.** The sketch above is plausible but I have not verified it is both true
and non-vacuous — the Lipschitz constant of an unregularized ensemble mean may be large enough to make it
trivially loose, which is precisely the failure mode to check first. **Do not put this in the paper until
it is proven and plotted.** Report honestly if no non-vacuous bound exists rather than manufacturing a
theorem. Note that M1 (which *controls* `L`) makes the bound testable by construction — the two rows are
complementary.

**Cost.** ~1-2 days of derivation with a real risk of returning nothing. **Acceptance-delta: HIGH if it
lands, ZERO if it does not.** Do it last, and only if M0-M3 have already secured the paper.

---

## Recommended order and total cost

| # | Row | Edit | CPU | Gate |
|---|---|---|---|---|
| 1 | **M0** normalize ensemble targets | 0.5 h | 1 grid | **Blocks everything** |
| 2 | **M2** roughen the GP | 2 h | 2 grids | Cheapest risked prediction |
| 3 | **M3** smoothness interpolation | 1 day | 6 grids | Best value; unifies C2+C3 |
| 4 | **M1** smooth the ensemble | 4 h | 4 grids | Converts diagnosis → fix |
| 5 | **M5** density ratio | 1 day | ~0-1 grid | Closes Prop 2 |
| 6 | **M4** distance regularization | 4 h | 2 grids | Standalone finding |
| 7 | **M6** non-trivial Prop 1 | 1-2 days | ~0 | Only if time remains |

**M0 → M2 → M3 is the critical path** and buys the most acceptance per CPU-hour. M0 because nothing is
interpretable without it; M2 because it is the cheapest way to risk the theory; M3 because it replaces
the paper's weakest claim with its strongest figure.

Predictions and kill criteria for each row are restated, unamended, in `docs/PREREGISTRATION_V2.md`.
If a result contradicts a prediction, that is a finding to report — not a prediction to quietly revise.
