# Frozen claim ledger — AAAI-27, Identity D (confound taxonomy + scoped mechanism)

**Status: FROZEN as of 2026-07-18.** Every sentence the paper asserts appears here as one row.
A sentence not in this ledger does not go in the paper. A sentence in this ledger goes in
**verbatim as written in column 1** — the scoping in column 5 is load-bearing and is not the
drafter's to renegotiate.

Sources: `docs/NOVELTY_V3.md` (citations `[n]` throughout), `docs/GATE_KBETA.md`,
`docs/POD_PHASE7.md`, `docs/POD_DB_SCALE.md`, `docs/PLATFORM_ARM_SUMMARY.md`,
`docs/GP_FREEZE.md`, `docs/DEGENERATE_CELLS.md`, `docs/FLAW_LEDGER.md`,
`docs/PREREGISTRATION_V2.md`, `docs/PREREGISTRATION_V3.md`, and the three Gate 0 reports:
`docs/BETA0_RECONCILE.md` (0-A.1), `docs/WIDTH_ABLATION.md` (0-A.2),
`docs/BUDGET_MATCHED.md` (0-A.3).

**Row count: 24.** LANDED 21 · PROVISIONAL 1 · PROVISIONAL-REPORTABLE 2 · **BLOCKED 0.**

**D25 added 2026-07-20** (x0-inversion, §5). It is a descriptive within-grid demonstration, not a
mechanism, and it carries its counting rule inside the asserted sentence.

**D13 carries two asserted sentences** — W1 (the width result) and **D13-W2** (accuracy is not the
bottleneck). W2 is a **sub-claim of D13, not a 24th row**: it has no independent status, it falls
if W1 falls, and it is counted inside D13's LANDED. It is broken out because it carries a
paper-wide strike order that no other row carries.

**Gate 0 is closed. No row is blocked; every remaining row is writable.** D21 has been **cut
entirely** — not hedged, not narrowed — because its surviving half (the engine-state
attribution) is asserted by D15/D18's engine-stamping argument and its blocked half (the
cross-platform sentence) rests on a withdrawn finding. Row 24 no longer exists.

`PROVISIONAL-REPORTABLE` is a new status introduced by the 0-A.3 read-out (D08, D23): the
corrected magnitude **is** reported, with its interval and an explicit statement of the regime
where it is underpowered. It is distinct from `PROVISIONAL` (D07), where a number is
asserted only in a narrowed form because the broader form is refuted or ungated.

---

## The six hard rules this ledger enforces

Every row was checked against these. They are enforcement rules, not style preferences; each
one exists because a specific citation would otherwise sink the row.

1. **K is a confound, NEVER a mechanism.** No row may present the K=2 flip as a discovery.
   Li/Rudner/Wilson found K-robustness over K∈{5,10} [8], and the K-sweep is a K≠width category
   error against Jacot/Lee/Rahaman [14][29][30]. **Reinforced by our own data:** the K=2 flip
   *does not reproduce on the audited engine at all* (D06) — the kill criterion did not fire.
2. **NEVER claim field-reversal.** No sentence of the form "surrogate matters more than
   optimizer" as a general result. Shahriari et al. [7] own that doctrine (~5,900 citations).
   Scope every optimizer-axis claim to falsifying **PGS's local premise** [33] only.
3. **C2's mechanism is APPLICATION + DIAGNOSIS in offline MBO, not discovery.** SNGP [12] owns
   distance-aware UQ; Fan et al. [13] own UCB-as-local-search. Both are cited **up front, in the
   mechanism section's first two sentences**, not buried in related work.
4. **The DB null is "no detectable difference at this power," NEVER "equivalence."** Agarwal
   et al. [22] + Demšar (JMLR 7(1), 2006): n=7 is under the Friedman threshold of >10 datasets.
   The word "equivalent" does not appear in the paper's Design-Bench sections.
5. **The strengthening (0.37→0.405) is the net of the TWO protocol confounds; K pushes the other
   way.** Never "de-confounding always strengthens" — that broad claim is false [5][6]. State the
   composition precisely, every time, in the same sentence.
6. **K-PROMINENCE: sensitivity and non-reversal travel together, at equal weight.** Any row,
   sentence, figure caption, or table note that touches ensemble size **must** state both halves
   in the same breath, neither subordinated to the other, neither in a footnote:
   - **K-SENSITIVITY** — η²_surrogate is K-dependent (0.326 / 0.366 / 0.408 / 0.389 at
     K = 2 / 3 / 5 / 10), **peaking at exactly the K=5 the field fixes by convention**.
   - **NON-REVERSAL** — the ranking does **not** flip at K=2: the ensemble marginal is **0.283**
     against the GP's **0.767**, and our pre-registered KB1 kill criterion **did not fire**.

   Stating the sensitivity alone reads as a discovered mechanism and violates rule 1. Stating the
   non-reversal alone conceals that the headline operating point is the effect's maximum. Both,
   every time. **Flag for deletion:** any claim resting on the supplement's **0.95 at K=2** — that
   figure does **not** reproduce on the audited engine, where the grid gives **0.283**. Every
   appearance of 0.95 must be struck, and the non-reproduction stated by us.

   > **Numeral collision, drafter beware.** D04's corrected η²_surrogate is **0.283** and D06's
   > K=2 ensemble marginal is also **0.283**. These are different quantities — a variance-explained
   > statistic and a normalized cell marginal. They must never appear in the same paragraph without
   > their units named, and neither may be cited as corroborating the other.

---

## Stage 0 (0-A): RESOLVED — how each blocker was discharged

All five blockers have reported. **Four resolved in favour of the row; one (0-A.4) withdrew the
finding the row rested on, and that row is cut.** Every resolution below was pre-registered
before launch (`docs/PREREGISTRATION_V3.md`, commit `55ced44`) except 0-A.5, which is a read-out
of existing pod data against a kill criterion registered in `docs/GP_FREEZE.md`.

| ID | Blocker | Resolution | Effect on rows |
|---|---|---|---|
| **0-A.1** | **β=0 reconciliation.** Three mutually inconsistent numbers for one quantity: manuscript 0.51→0.47; recomputation 0.504→0.511; grid 0.378 vs 0.556. | **RECONCILED — the disagreement was the *engine*, not the estimator.** 0.504→0.511 is `off_off` (pre-audit, superseded by X1); 0.378/0.556 is `on_on` (audited) but in **β-refit units**, one normalizer per β, so the two are not on one ruler. On the β-invariant normalizer the gap is **0.319 [0.196, 0.460] at β=0** and **0.525 [0.406, 0.614] at β=2**, increment **0.203 [0.007, 0.396]**, p = 0.020. Holding the estimator fixed and flipping only the engine flips the *direction*; holding the engine fixed and flipping the estimator moves the number by <0.02. | **D12 UNBLOCKED** → rewritten as BASE-PLUS-AMPLIFICATION. **D11 gate discharged** → LANDED. |
| **0-A.2** | **Width verdict.** Width ablation at fixed K, sweeping per-member hidden units (96, far below Lee et al.'s n≥512 range [41]). Never run. | **W1 CONFIRMED.** Gap **0.480 at w=96** vs **0.476 at w=1024** — **99.1% retained**, shrinkage −0.006 [−0.210, 0.161], flat with noise and *non-monotone* (dips at w=256, returns). All three pre-registered KILL conditions fail. **W2 SUPPORTED, by a stronger route than registered:** the ensemble **beats** the GP's held-out normRMSE on **7/7 tasks** and in 26/28 (task, width) cells, and still loses the optimization gap. | **D13 UNBLOCKED** → LANDED, plus **W2 added as a hardened sub-claim** that strikes "the GP fits better" paper-wide. |
| **0-A.3** | **Matched-budget verdict.** Surrogate-query budgets unmatched — gradient 51,456 / perturbation 4,352 / CMA 932–6,536 (**measured, not derived**; the published 6×–59× figures were estimates). | **BM1 CONFIRMED at the primary level.** Matched at **Q = 51,456**, η²_opt = **0.038 [0.003, 0.123]** — below the 0.10 confirm threshold, KILL (>0.15) excluded at 95%. But the published **0.005 understates the effect ~8×**, and at the secondary (DOWN, Q=4,352) level η²_opt = 0.066 [0.014, 0.340]. Two findings the unmatched grid concealed: the **optimizer ranking flips with budget**, and **η²_surr more than doubles with budget** (0.243→0.526). | **D08, D23 UNBLOCKED** → PROVISIONAL-REPORTABLE. **D19's DB optimizer half was gated here and is now discharged by 0-C** — see below. |
| **0-A.4** | **Platform-vs-engine at matched engine.** The macOS↔Linux comparison at one stamped engine. | **FINDING WITHDRAWN, NOT ANSWERED.** N8's 2.20-vs-1.76 gap is **X3 engine state** — main effect **+0.639** reproduced on a single machine (`PLATFORM_ARM` Finding 1). There is no cross-platform result to report, hedged or otherwise. | **D21 CUT ENTIRELY.** The row is removed, not narrowed. |
| **0-A.5** | **Ant freeze read-out.** `GP_FREEZE` states M-B cannot be called settled until Ant's GP cells are read for exactly-zero variance. | **M-B REFUTED; the mechanism is M-A (LCB PARALYSIS).** `botorchgp:perturb` and `botorchgp:cma` both return **1.5287419557571411 with std exactly 0.0 across 16/16 seeds** — a bit-identical constant on a **continuous** task with **no argmax decode**. That fires the pre-registered kill against decode-snap-back directly. | **D18 UNBLOCKED** → LANDED as **M-A**, not M-B. |

> **The gate 0-A.3 did not discharge — now closed by 0-C.** BM1 matched budgets on the
> **seven synthetic tasks** only, which left D19's optimizer half PROVISIONAL. **0-C matched
> budgets on the full seven-task Design-Bench grid, both MuJoCo tasks included, and discharged
> it.** The result runs against the direction the gate assumed: matching **roughly doubles**
> η²_optimizer in every corner while η²_surrogate falls, and moves off_off from non-rejecting
> to rejecting, so **all four corners reject** where three did. The presumed confound was
> **masking** the effect, not manufacturing it. D19 is promoted subject to the two scope limits
> in its row — high-budget-only, and no within-corner separation.

---

## Part I — Framing and concession (§1–§2)

| # | The sentence the paper asserts | Number + artifact | Bounding citation | Reviewer objection it must survive | How it is scoped to survive | Status |
|---|---|---|---|---|---|---|
| **D01** | "The move we make — name unreported implementation choices, give the protocol that removes them, show the ranking moves — is an established genre, and we claim no credit for its shape." | n/a (concession) | Henderson AAAI 2018 [2]; Ferrari Dacrema RecSys 2019 [3]; Musgrave ECCV 2020 [4]; Lucic [21]; Agarwal [22] | "We ran a reality check" is not a contribution; the genre's canonical instance was published at this very venue [2]. | Conceded in the first paragraph of §2, by name, before any novelty claim is made. Conceding the shape is what makes the residual credible. Balduzzi [48] is explicitly ruled out as a comparator (benchmark-*suite* redundancy, a different confound axis). | **LANDED** |
| **D02** | "What is unclaimed is the composition: a five-confound set specific to offline-MBO surrogate comparison, a removal protocol, and a two-way crossed surrogate×optimizer variance decomposition — an instrument no paper in this genre has used." | Five confounds enumerated in Part II below; η² instrument per `code/analyze_corners.py` | Kim TMLR 2026 [1] concedes the gap verbatim; Hutter ICML 2014 [15] owns the **one-way** fANOVA; Liang [16] crosses both axes but is descriptive + online; Moosbauer [43] varies both and *declines* the decomposition | "A residual of composition, not of kind." Also: "Hutter already decomposed model class." | Claim the **two-way crossed** decomposition in **offline MBO** — never η²/ANOVA as such. Cite Hutter (one-way, one fixed SMAC run) and Liang (descriptive, online) *defensively* as the precedents improved on. Moosbauer is the sharpest asset: the paper closest to the two-axis design consciously refuses the two-way decomposition. | **LANDED** |
| **D03** | "Distance-aware GP uncertainty and the local-search reading of a UCB acquisition are prior results we apply and diagnose in the offline setting; we do not claim either as a discovery." | n/a (concession) | Liu/SNGP NeurIPS 2020 [12]; Fan NeurIPS 2024 [13] | "SNGP owns distance-awareness; Fan proves UCB-as-local-search. Your mechanism is known." | **Rule 3.** Both citations appear in the mechanism section's first two sentences. The paper never uses the phrase "implicit trust region" as a claimed coinage — a naming novelty is thin ground, and TuRBO [26] argues the acquisition alone does *not* produce a trust region. | **LANDED** |

## Part II — The five confounds (§3)

| # | The sentence the paper asserts | Number + artifact | Bounding citation | Reviewer objection it must survive | How it is scoped to survive | Status |
|---|---|---|---|---|---|---|
| **D04** | "**Confound 1 (target scaling).** The ensemble regresses on raw targets spanning −2613 to +36 while both GP surrogates z-score their targets; correcting this alone moves η²_surrogate from 0.367 to 0.283." | 0.367 [0.254, 0.559] → 0.283 [0.186, 0.444]; `results/bootstrap_eta_corners.json`, `docs/GATE_KBETA.md` §KB5; code trace `mbo.py:36-37,130-138` vs `mbo.py:255,311-312` | Genre-shape [2][3][4]; no analog of this confound in any of them | "This is just a bug, not a taxonomy entry." | Framed as a *measurement* confound with a code-line trace and a signed effect, not as a bug report. The paper's own `main.tex:93` claimed min-max normalization that exists only in analysis, never in the training path — the gap between claimed and actual protocol is the finding. | **LANDED** |
| **D05** | "**Confound 2 (candidate/oracle protocol).** Two of three optimizers propose 256 designs and report the oracle-selected best 128 while the third proposes 128, so p50 is two different estimands in one column; correcting this alone moves η²_surrogate from 0.367 to 0.450." | 0.367 → 0.450 [0.312, 0.649]; `results/bootstrap_eta_corners.json`; code trace `mbo.py:384-389, 188, 198-201, 292, 392-394` | Genre-shape [2]; Kim [1] on unclarified attribution | "You are reporting your own implementation error as a discovery." | Scoped as *the protocol the manuscript states it holds identical and does not* (`main.tex:91`). The identifiability license is the claim under test; the confound is that the license is false. This is the strongest of the five because it is a stated-versus-actual mismatch, not a judgment call. | **LANDED** |
| **D06** | "**Confound 3 (ensemble size K).** η²_surrogate is K-sensitive — 0.326 / 0.366 / 0.408 / 0.389 at K = 2 / 3 / 5 / 10 — peaking at exactly the K=5 the field fixes by convention; but the ranking does **not** reverse at K=2, where the ensemble marginal (0.283) remains far below the GP's (0.767)." | K-sweep table, `results/kbeta/kbeta_analysis.json`, `results/kbeta/kbeta_ens.json`, `docs/GATE_KBETA.md` §KB1 | Li/Rudner/Wilson ICLR 2024 [8] found K-robustness over {5,10}; Lakshminarayanan [10] reports quality *improving* with M; Abe [9] never touches a GP or a ranking | **The single most dangerous row.** "L/R/W already showed ensemble performance is robust to model count." Plus: "your K-decline runs backward from Lakshminarayanan, so K=2 is a small-sample σ-estimation artifact." | **Rule 1, doubly enforced.** (a) K is presented as one of five confounds to control, never as a discovered mechanism. (b) **The non-reversal is reported as prominently as the sensitivity** — our own pre-registered kill criterion (KB1: "if the ensemble marginal at K=2 exceeds the GP's, the headline reverses") **did not fire**. The manuscript's supplement figure (0.95 at K=2) does *not* reproduce on the audited engine, which we state. Disjoint-K-range scoping vs [8] stated explicitly and up front. | **LANDED** |
| **D07** | "**Confound 4 (β–σ mismatch).** A shared β=2 delivers comparable effective pessimism *in aggregate* (median σ_GP/σ_ens = 1.19 at matched K=5) but not per task, where the ratio spans 0.07 (Branin) to 1.44 (Styblinski, Rastrigin)." | 1.19 median @K=5; 1.21 all-K; per-task table in `docs/GATE_KBETA.md` §KB4; `results/kbeta/kbeta_gpsigma.json` | Dewolf AI Review 2022 [11] owns the general uncalibrated-interval principle; Ghasemipour [23] owns nominal≠effective *within* class; Srinivas [24] β_t is single-surrogate | "The shared-multiplier problem is owned by the calibration literature [11]." Also: "your own aggregate refutes your confound." | **We report the refutation.** Our pre-registered KB4 kill fired on aggregate — the "fifth unmatched hyperparameter" does not exist grid-wide. The claim is narrowed to the per-task spread and labelled as such. Novelty claimed only as the **offline-MBO acquisition-comparison application** [11][23], never the principle. Reporting our own killed prediction is an asset (cf. D24). | **PROVISIONAL** — aggregate refutes, per-task supports; the row survives only in its narrowed per-task form |
| **D08** | "**Confound 5 (search-intensity budget).** Surrogate-query budgets are unmatched by 11.8× across the optimizer axis — gradient 51,456, perturbation 4,352, CMA 932–6,536 measured — and equalizing them at Q = 51,456 raises the optimizer main effect from a published η²_optimizer of 0.005 to **0.038 [0.003, 0.123]**, an eightfold understatement that nonetheless leaves the optimizer null standing." | Native Q: grad 51,456 / perturb 4,352 / CMA median 6,528 (min 932, max 6,536) — **measured** by a counting proxy, `code/budget_probe.py`. Matched UP Q=51,456: achieved 51,200 / 51,456 / 51,472, **0 of 630 cells >5% off target**. η²_opt 0.0046 unmatched → **0.0379 [0.0027, 0.1234]** matched; η²_surr 0.4064 → 0.5256; η²_inter 0.1608 → 0.1103. Secondary (DOWN, Q=4,352): η²_opt 0.0664 [0.0138, 0.3398]. `results/budget/{query_budget,budget_matched,budget_analysis}.json`; `code/budget_matched.py`, `code/analyze_v3.py`; estimator reproduces `kbeta_analyze._eta2` to 1e-12. `docs/BUDGET_MATCHED.md` | Genre-shape [2]; Kim [1] | "'Optimizer' is confounded with search intensity — 'use a conservative optimizer' may just mean 'search less.'" Now also: **"your own matched arm octupled the effect you called negligible."** | **Report 0.038, never 0.005.** The published figure is disclosed **by us** as an ~8× understatement caused by the budget imbalance — the audit's suspicion is confirmed in direction and refuted in consequence. Three corrections the taxonomy now owns: (i) the "6×–59×" spread was an *estimate*; the measured spread is 11.8× over grad:perturb, because CMA's `budget=3000` is a **cap that rarely binds** — pycma stops on tolfun/tolx first. (ii) The "256 vs 128 proposals" half of this confound **is already fixed by X3**; the surviving inequality is in *surrogate queries*, not proposals. (iii) The trust region flagged in the audit is **not active** in the main grid (`run_grid_cell` passes `trust=None`), so BM1 isolates budget alone. The null is stated as **"established at high budget, underpowered at low"** — never unqualified. | **PROVISIONAL-REPORTABLE** — the corrected magnitude is asserted with its interval; the DOWN-level disagreement is asserted alongside it, not omitted |

## Part III — The de-confounding result (§4)

| # | The sentence the paper asserts | Number + artifact | Bounding citation | Reviewer objection it must survive | How it is scoped to survive | Status |
|---|---|---|---|---|---|---|
| **D09** | "Correcting the two measurement/protocol confounds — target scaling and the candidate/oracle protocol — does not shrink but strengthens the rewarded surrogate advantage, moving η²_surrogate from a published 0.37 to a corrected 0.405, against the reality-check genre's shrink direction; the ensemble-size confound moves it the other way, so the strengthening is the net of the two protocol confounds and not a property of de-confounding in general." | 0.37 → 0.405 [0.290, 0.556]; four-corner table `docs/GATE_KBETA.md` §KB5, `results/bootstrap_eta_corners.json`; cross-check η²_surr@β=2 = 0.406 reproduces the on_on corner | Melis ICLR 2018 [5] states the shrink norm; Recht ICML 2019 [6] and Agarwal [22] are the two ML/CS partials; Bressan [20] is the psychology full-shape precedent | **"Audits always shrink" is false, and Recht already showed a relative slope > 1 (1.69 CIFAR-10, 1.11 ImageNet) — 'the opposite of the standard overfitting scenario.'** Also: "noncollapsibility means this is statistically unsurprising." | **Rule 5, in one sentence.** The composition ("net of the two protocol confounds… K moves it the other way") is inside the asserted sentence, not in a footnote. Recht and Agarwal are pre-empted **explicitly by name in the same paragraph**; Bressan cited as a one-line cross-disciplinary analog. The claim is the exact scalar form — "no ML/CS de-confounding audit has been shown to produce a variance-explained effect-size statistic exceeding its own published value" — never "audits always shrink, we are the exception." Novelty is *unprecedented as an ML benchmark-audit instance*, not *surprising*. | **LANDED** |
| **D10** | "The four-corner decomposition is not resolvable at n=7 tasks: the corner bootstrap CIs overlap heavily (widths 0.26–0.34 against a corner range of only 0.167), and all four intervals share a common region [0.312, 0.443] that every one of them contains, so 0.405 is never reported without its interval." | Corner CIs `docs/GATE_KBETA.md` §KB5; `results/bootstrap_eta.json`, `results/bootstrap_eta_corners.json` (task+seed, B=10,000); off_off CI width 0.305 ≈ published 0.32. **CORRECTION 2026-07-20:** this row previously asserted that the on_on interval [0.290, 0.556] contains every other corner **point estimate**. It does **not** — on_off's point is **0.2828**, which sits **0.0069 below** on_on's lower bound of **0.28970**. The overlap statement that *is* true, and is strictly stronger for the non-resolvability argument, is the shared region **[0.3115971, 0.4439559]** = [max of the four lower bounds, min of the four upper bounds], which is non-empty and contained in all four intervals. **Printed endpoints must be rounded INWARD** (lower up, upper down) → **[0.312, 0.443]**. Nearest-rounding the upper endpoint to 0.444 puts it 4.4e-05 *above* on_off's upper bound of 0.4439559 and makes the containment claim false again — that error was made in the first correction and caught by the 2026-07-20 claim audit. Both call sites in `main.tex` (§4 body and the Figure~1 caption) and the figure annotation were corrected | Agarwal NeurIPS 2021 [22]; Demšar JMLR 7(1) 2006 | "You are reporting a corrected headline your own CIs cannot resolve." | **This row is a self-imposed constraint, and it is the reason D09 survives.** Our own pre-registered KB5 predicted the overlap and it confirmed. Every appearance of 0.405 in the paper carries [0.290, 0.556] — **all of them**, not the four sites this row used to enumerate (abstract, intro, table, conclusion). That enumeration was the bug: the figure caption and the Discussion's two-confounds paragraph both quoted 0.405 bare until the 2026-07-20 audit. The rule is unconditional; do not re-list call sites. The bootstrap is validated against the published CI width. | **LANDED** |
| **D11** | "η²_surrogate is strongly β-dependent, rising monotonically from 0.184 at β=0 to 0.406 at β=2, and it is **budget-dependent as well**, more than doubling from 0.243 at Q=4,352 to 0.526 at Q=51,456; this dependence is a firmer result than the four-corner decomposition — the β=0 and β=2 intervals barely overlap where the corner intervals do not separate at all — so any headline η²_surrogate must state its β, its K, **and its query budget**." | β grid 0.184 / 0.214 / 0.282 / 0.406 / 0.408 at β = 0 / 0.5 / 1 / 2 / 5; CIs [0.085, 0.354] vs [0.285, 0.564]; `results/kbeta/grid_b*.json`, `docs/GATE_KBETA.md`. **Budget axis:** η²_surr 0.243 (DOWN) → 0.526 (UP), `results/budget/budget_analysis.json`, `docs/BUDGET_MATCHED.md` §2 | Srinivas [24] (β_t single-surrogate); Dewolf [11] | "Your headline η² is an artifact of the β you happened to fix, just as it is of the K you fixed." Now a **fourth** axis exists, so the objection is stronger, not weaker. | Reported as a **sensitivity the taxonomy owns**, not hidden. The honest framing: the magnitude of η²_surr is a joint artifact of **four** chosen operating-point coordinates — K=5, β=2, Q, and the engine corner — and we say so in the asserting sentence. **Rule 6 applies:** the K half must carry the non-reversal (ens 0.283 vs GP 0.767 at K=2, KB1 did not fire) at equal prominence. The *direction* is robust at every β, K and corner tested (GP marginal **0.66–0.85** vs ensemble **0.17–0.35**, smallest gap 0.32); only the *magnitude* moves. **CORRECTED 2026-07-20:** this row previously stated the bands as 0.75–0.85 and 0.24–0.36; the true ranges are wider on both sides (GP low is β=0 botorchgp 0.6586; ensemble low is K=10 0.1707), and the budget arm carries no per-level surrogate marginals at all, so "budget" is dropped from the list of axes this claim ranges over. The non-crossing conclusion is unaffected and comfortable. Because β is nearly resolvable at n=7 where the corners are not, β is presented as the *firmer* half of the sensitivity analysis. | **LANDED** — 0-A.1 discharged the gate on its use inside the mechanism argument (D12); the budget axis is added from 0-A.3 |

## Part IV — Scoped mechanism (§5)

| # | The sentence the paper asserts | Number + artifact | Bounding citation | Reviewer objection it must survive | How it is scoped to survive | Status |
|---|---|---|---|---|---|---|
| **D12** | "With the pessimism term removed entirely (β=0, pure posterior-mean maximization) the GP family retains **61% of its advantage** over the deep ensemble — **0.319 [0.196, 0.460]** against **0.525 [0.406, 0.614]** at β=2 — so the surrogate-class effect rests on a substantial mean-quality base that pessimism **amplifies rather than creates**; the amplification is itself significant (**increment 0.203 [0.007, 0.396]**, p = 0.020), so the mechanism is not purely a mean-geometry one." | **β-invariant units** — one per-task min–max normalizer fit **once** over the pooled cell means of *both* β conditions, so the two gaps sit on one ruler (`code/beta0_reconcile.py:80-96`). Task+seed hierarchical bootstrap, B=10,000, **normalizer refit inside each resample** so its sampling variability is propagated. p(increment ≤ 0) = **0.020**. Normalization-free cross-check (per-task z-score): 0.904 sd @ β=0 vs 1.473 sd @ β=2 — **same 0.61 ratio**, so the conclusion is not a min–max artifact. `code/beta0_reconcile.py` → `results/beta0_reconcile.json` (X1=on, X3=on, K=5, TOP=128, 30 seeds `0..29`, 7 tasks, git_sha `812bcb9`). Per-task gaps are **heterogeneous** (Branin 0.664@β=0 *exceeds* its 0.468@β=2; Griewank-30D 0.098 vs 0.665) — descriptive only at n=7. `docs/BETA0_RECONCILE.md` | SNGP [12] and Fan [13] bound the *mechanism*; TuRBO [26] argues the acquisition alone does not produce a trust region | **"Three different numbers exist in your own record for this quantity"** — 0.47 (manuscript), 0.504→0.511 (recomputation), 0.378 (grid). Also: "your own paper says the paired difference is indistinguishable from zero; now you say it excludes zero." | **Rule 3.** SNGP and Fan cited first; the claim is *application + diagnosis in offline MBO*, never discovery. **Three hard constraints, none of which the drafter may soften — see the boxed block below this table.** In substance: (a) cite **0.319 / 0.525 only** for any cross-β comparison; (b) the paper's current β=0 passage is **refuted** and must be struck, not hedged; (c) the phrase **"independent of pessimism" is dead** — 61% surviving is base-plus-amplification, and "independent" asserts a no-dependence the data reject at p = 0.020. **KB2's kill does not fire** (0.319 > 0.5 × 0.525 = 0.263) — but it passes *far* less comfortably than the β-refit numbers implied (0.378 vs 0.278) and the margin sits inside the bootstrap CI. State that. | **LANDED** — rewritten as **BASE-PLUS-AMPLIFICATION** |
| **D13** | "The ensemble's posterior mean is jagged where the GP's is smooth, and this is a property of the surrogate class rather than of finite width: sweeping per-member width over a **10.7× range at fixed K=5** — 96 to 1024 hidden units — leaves the GP–ensemble gap statistically unchanged at **0.480 → 0.476**, **99.1% retained**, with a shrinkage of −0.006 [−0.210, 0.161] indistinguishable from zero." | Gap by width: **0.480** [0.365, 0.576] @ w=96 · 0.336 [0.132, 0.483] @ w=256 · 0.414 [0.187, 0.565] @ w=512 · **0.476** [0.208, 0.647] @ w=1024. Curve is **non-monotone** (dips at 256, returns) — flat with noise, not a decay. All on the **condition-invariant normalizer** of 0-A.1, fit once over pooled cell means of all four widths. `results/width/{width_grid,width_analysis}.json` (210 cells × 18 = 3,780 fits, engine-stamped), `code/width_ablation.py`. **Validity check:** w=96 reproduces the incumbent `grid_b2.0.json` **bit-exactly** for grad and cma on all 7 tasks. `docs/WIDTH_ABLATION.md` | Jacot NeurIPS 2018 [14]; Lee ICLR 2018 [29]; Rahaman ICML 2019 [30]; Lee et al. NeurIPS 2019 [41] (width 96 ≪ n≥512 agreement range); L/R/W's smaller-net ablation [8] | "A jagged finite-width ensemble is an under-parameterization artifact. Wide networks are GPs. Your K-sweep does not test width — K is cardinality, not per-member width n. This is a category error." | **Rule 1.** The K-sweep is *never* offered as evidence here; we state the category error ourselves, and 0-A.2 is the ablation that actually tests the objection — at **fixed K=5**, varying only per-member capacity. All three pre-registered KILL conditions fail (KILL required monotone decrease **and** gap(1024) < 0.5·gap(96) **and** a CI containing 0; none holds), and the CONFIRMED condition is met. **Two scope limits, both stated by us, neither optional:** (i) **the CI widens monotonically with w** (0.211 @ w=96 → 0.439 @ w=1024), so w=1024 is the *least* precise point on the curve — the supported claim is "the gap does not close", **not** "the gap is identical at w=1024"; (ii) the sweep stops at 1024 and **NTK limits are asymptotic**, so this answers the objection **at practical widths** only. **No asymptotic claim in w may be written.** **Rule 6** applies to the fixed-K=5 framing. | **LANDED** — W1 CONFIRMED; the NTK/spectral-bias objection does not survive at practical widths |
| **D13-W2** | "Predictive accuracy is not the bottleneck and cannot explain the gap: at every width tested the ensemble's held-out normalized RMSE is **lower** than the GP's — it beats the GP on **7/7 tasks** and in 26/28 (task, width) cells — and it still loses the optimization comparison by ~0.48. The more accurate surrogate is the one that loses." | Held-out normRMSE (RMSE / oracle std, 20% split never seen by the grid), mean over 7 tasks: **0.4446** @ w=96 · 0.4047 @ w=256 · 0.3934 @ w=512 · **0.3877** @ w=1024, against the **GP's 0.4795**. Monotone improvement with w (−12.8%). **Pre-registered test:** W2 was registered to be read only where ensemble and GP RMSE are statistically indistinguishable; two such cells exist (Styblinski-5D @ w=256, CI [−0.021, 0.028]; @ w=512, CI [−0.043, 0.010]) and the mean gap at those widths is **0.375**. `results/width/width_analysis.json`, `docs/WIDTH_ABLATION.md` §W2 | Jacot [14]; Lee [29][41]; Rahaman [30]; SNGP [12] (the mechanism this hands off to) | "You claim the GP models the function better — but your own held-out numbers say the ensemble fits better. Which is it?" | **This sub-claim exists to make that objection unavailable, by conceding it first and turning it into the mechanism.** It carries a **paper-wide strike order:** every phrasing of the form *"the GP fits better"* / *"the GP models the function better"* / *"the GP is the more accurate surrogate"* is **struck**, in all sections, and replaced with: **"the ensemble is more accurate in-distribution but its mean has exploitable off-distribution maxima."** Two caveats stated by us: (i) the 7/7 result is a **post-hoc strengthening**, not the registered test — **§5 must cite the tie-cell result (0.375) as primary** and 7/7 as the stronger observation; (ii) held-out **NLL is not usable** as a second accuracy axis (GP mean NLL 202.7 vs ensemble 5.7–6.4) — that is a **calibration** finding, orthogonal to W2, and the NLL column in the artifact must not be mistaken for support. | **LANDED** — W2 SUPPORTED on registered terms, and by a stronger post-hoc route |
| **D14** | "The ensemble's σ is a distance signal, not an error signal: its correlation with pointwise absolute error is ≈0.07, while its correlation with k-NN distance to the training data is ≈0.26 — three to four times larger and positive on all seven tasks." | ρ(σ,\|error\|) ≈ 0.07; ρ(σ, kNN dist) ≈ 0.26 (>0.28 on the four mid/high-d tasks); `results/calibration_on_on.json`, `docs/POD_PHASE7.md` §7.5 | **SNGP [12] owns distance-aware UQ outright**; DUQ [25] confirms the ensemble failure mode | "SNGP already proved GP variance is distance-aware and ensembles are not. This is their result." Also: "do not cite Ovadia [28] here — they measured corruption severity, not spatial distance, and found ensembles among the *better* estimators." | **Rule 3.** Framed as *diagnosis of a measurement error in the prior analysis*: the manuscript concluded σ is uninformative by measuring it against the wrong target. The contribution is the corrected measurement in offline MBO, explicitly bounded by SNGP. **Ovadia is not cited in support anywhere** — doing so invites a mis-citation flag. | **LANDED** |
| **D15** | "The ensemble's gradient-ascent collapse is genuine surrogate geometry on the majority of tasks under the audited engine, and its genuineness is driven by the candidate/oracle protocol (X3) rather than by target scaling (X1)." | Genuine-collapse count by corner: off_off 2/7, on_off 0/7, off_on 5/7, on_on 4/7, by `gradtune.py:73`'s own >5% rule; `results/results_gradtune_{off_off,on_off,off_on,on_on}.json`; `docs/POD_PHASE7.md` §7.1 | Genre-shape [2]; the optimizer/SO reviewer pool | **"Your own released `gradtune.py` concludes the collapse is a tuning artifact — a trust region closes it on 3 of 4 tasks. That result is absent from the paper."** (FLAW_LEDGER P0-0, rated an unconditional submission blocker.) | The sweep is **reported in full, including the corner where it fires against us** (on_off: 0/7 genuine). The pre-audit (X3-off) engine is where the original "tuning closes it" verdict came from — we confirm that and show it does not hold on the audited engine. Disclosure converts P0-0 from a reject-driver into a 2×2 attribution result. The pre-registered structure (genuine at d≤10, tuning closes at d≥15) is reported as holding. | **LANDED** |
| **D16** | "Under the matched protocol the ensemble's coverage collapse is not gradient-specific: gradient and CMA proposals differ in out-of-distribution coverage by 0.010 under X3-on versus 0.117 under X3-off, because both optimizers pool every iterate and return the top-128 by surrogate LCB." | 0.010 (X3-on) vs 0.117 (X3-off); `results/coverage33.json`, `docs/POD_PHASE7.md` §7.3 | Genre-shape [2]; our own pre-registration X7 | "You framed this as an ensemble×gradient interaction; now you say it is not." | **We report our own X7 prediction as refuted.** The claim is narrowed to "ensemble × any aggressive selector under the matched protocol," and the gradient-specific framing is retracted by name. A refuted pre-registered prediction is evidence of a real test (cf. D24). | **LANDED** |
| **D17** | "The premise-coverage value of 0.97 in the prior analysis is the scikit-learn exact GP, not the differentiable GP the grid actually scores, whose real coverage is 0.831 and falls to 0.38 on Styblinski." | sklearn GP 0.97 (reproduces published), grid botorchgp 0.831 mean / 0.38 Styblinski, ensemble 0.14 own-proposal; `results/gpcov.json`, `results/coverage33.json`, `docs/POD_PHASE7.md` §7.4 | Genre-shape [2]; FLAW_LEDGER P0-3 | "The interaction claim rests on a comparison where surrogate and optimizer move together, evaluated with a GP that is not the GP in the grid." | Both numbers reported side by side, with the model each belongs to named. This settles P0-3 rather than arguing it. | **LANDED** |

| **D25** | "The candidate/oracle correction leaves each cell's seed designs---the top-128 of the offline data plus perturbed copies---inside the returned pool, so a cell returning something worse than what it was handed has had its own acquisition rank an invented design above a real one it was holding; on the audited engine the ensemble does this on at least one optimizer on **7/7** tasks, against **3/7** for SVGP and **2/7** for the exact GP, and on Branin-2D under ensemble gradient ascent all **30/30** seeds invert with **100%** of the 128 returned designs worse than the best design the cell started with." | Inversion rate per (task, surrogate, optimizer, X3) over 30 seeds; `results/x0_inversion.json` (`code/x0_inversion.py`, X1/X3 on, K=5, β=2, TOP=128, git_sha `9843dfc8`). Task counts read on the **ANY-optimizer** rule, stated as such. Branin ens:grad `inversion_rate` 1.0, `mean_frac_worse` 1.0. GP inversions are Styblinski-5D + Rastrigin-15D (exact GP) and Branin-2D + Styblinski-5D + Rastrigin-15D (SVGP) | SNGP [12]; Fan [13] (UCB-as-local-search) bounds any acquisition-geometry reading | "You are counting a task as inverting if *any* of three optimizers does. Under an ALL-optimizer rule your own numbers are 3/7, 1/7, 2/7 and the contrast largely disappears." Also: "n=7, descriptive, no test." | **The counting rule is named in the same breath as the counts**, and the figure shows every one of the 63 cells so a reader can apply either rule. The claim is asserted as a **demonstration within this grid, descriptive at n=7**, never as a mechanism or a field result — the paper says so in the asserting paragraph. It is placed as a **concretization of Elimination 7's localization** (the loss sits at the returned optimum's oracle quality), not as independent evidence for any η² magnitude. **Rule 2 binds:** no sentence generalizes this beyond our grid. | **LANDED** — descriptive; added 2026-07-20 |

### D12 — three hard constraints the drafter may not soften

These are not guidance. Each one exists because the paper currently asserts its opposite.

**(a) UNITS — 0.319 / 0.525, never 0.378 / 0.556 as a ratio.**
Cite **0.319 and 0.525** for *any* cross-β comparison: the "61% survives" claim, the increment
**0.203 [0.007, 0.396]**, and p = 0.020. **0.378 and 0.556 are β-refit** — `kbeta_analyze`
fits its min–max normalizer *separately at each β*, so the two numbers are on **different
rulers per β** and their ratio is not interpretable. This matters precisely because KB2's kill
criterion (`gap0 < 0.5·gap2`) is a ratio. **0.378 may appear ONLY as a within-β descriptive
figure — never set against 0.556.** A sentence containing both 0.378 and 0.556 is a defect.

> **Doc-table trap, carried forward from 0-A.1.** `docs/GATE_KBETA.md`'s adjacent `gp_marg`
> column is the **botorchgp marginal alone**. A reader subtracting the printed columns gets
> 0.659 − 0.306 = 0.353, not 0.378. The gap is `(botorchgp_marg + svgp_marg)/2 − ens_marg`
> = (0.6586 + 0.7087)/2 − 0.3055 = 0.37817. Do not reproduce the trap in our own tables.

> **Second numeral collision (cf. rule 6's 0.283 case).** **0.556** is *both* the β-refit β=2
> gap **and** the upper bound of D09/D10's η²_surrogate interval **[0.290, 0.556]**. These are
> unrelated quantities — a normalized gap and a variance-explained CI bound. Since D12 must not
> cite the β-refit 0.556 at all, **every surviving 0.556 in the paper is D09/D10's CI bound**.
> Any draft that uses 0.556 as a gap has reintroduced the units error constraint (a) forbids.

**(b) THE REFUTED PASSAGE — strike, do not hedge.**
`paper/aaai27/main.tex:198` currently states the gap is "essentially unchanged — **0.51** at β=2
versus **0.47** at β=0 … the paired difference has 95% CI **[−0.02, 0.10], indistinguishable
from zero**" and concludes "The advantage is a property of the GP's smooth mean, **not of σ**."
`paper/aaai27/supplement.tex:106` repeats it ("pessimism is not the source of the GP advantage").
On the audited engine the paired increment is **0.203 [0.007, 0.396]**, which **excludes zero —
the opposite of the paper's stated CI and the opposite of its conclusion.**

Three separate things must go, at **both** call sites:
1. **The numbers 0.51 and 0.47.** Unattributed. **No traced computation reproduces the pair.**
   The 0.51 magnitude resembles the `off_off` botorchgp 3-optimizer figure (0.504), but even
   there the **direction is wrong** — off_off runs **UP** (0.504 → 0.511), not down to 0.47.
   The 0.47 is reproduced by nothing at all. **Flag both for deletion.**
2. **The "[−0.02, 0.10] / indistinguishable from zero" CI.** False on the audited engine.
3. **The "not of σ" conclusion.** Refuted: σ contributes a significant 39% of the β=2 gap.

Replace all three with the base-plus-amplification sentence in D12 column 1. **Same edit to
`supplement.tex:106`** — an unstruck supplement is a live contradiction with the main text.

**(c) THE DEAD PHRASE.** *"Independent of pessimism"* does not appear in the paper. 61% surviving
is a **base**, not an independence; "independent" asserts a no-dependence the data reject at
p = 0.020. `docs/NOVELTY_V3.md:176` is also stale — its "not reconciled" status is resolved, and
its use of the off_off recomputation reaches the right conclusion **by the wrong route**.

### C2 mechanism — third-axis corroboration from the budget arm

Applies to **D12 and D13/D13-W2** (the mean-geometry rows), as a short paragraph in §5.

η²_surrogate **more than doubles with search budget**, 0.243 at Q=4,352 to **0.526** at
Q=51,456 — and the composition of that rise is the load-bearing part. The **ensemble marginal
falls** as budget rises (0.361 → **0.240**) while **both GPs rise** (botorchgp 0.755 → 0.849,
svgp 0.713 → 0.794).

| level | ens | botorchgp | svgp | η²_surr |
|---|---|---|---|---|
| DOWN (Q=4,352) | **0.361** | 0.755 | 0.713 | 0.243 |
| UP (Q=51,456) | **0.240** | 0.849 | 0.794 | 0.526 |

Give every optimizer more surrogate queries and the ensemble gets **relatively worse** while the
GPs convert budget into score. That is the direct behavioural signature the mean-geometry
mechanism predicts: **if the ensemble's mean has exploitable off-distribution maxima, more search
pressure finds more of them.** The GP's smoother mean has less to exploit.

This is **independent support from a third axis** — 0-A.1 removed σ, 0-A.2 raised width, and this
raises search pressure; all three converge on mean geometry as the surviving explanation. Two
constraints: it was **not what the arm was designed to test**, so it is reported as an
**observation, not a pre-registered result**; and it is corroboration of a *mechanism*, never
independent evidence for the *magnitude* of any η².

## Part V — Design-Bench: the null and its mechanism (§6)

| # | The sentence the paper asserts | Number + artifact | Bounding citation | Reviewer objection it must survive | How it is scoped to survive | Status |
|---|---|---|---|---|---|---|
| **D18** | "Several Design-Bench cells are frozen at a fixed dataset reference rather than scoring an optimization result: four of nine TF-Bind-8 cells return exactly 1.0 — the normalized dataset best — on every seed with zero variance, and on Ant two of three GP cells return the bit-identical constant 1.5287419557571411 on all sixteen seeds, so on those tasks η²_optimizer ≈ 0 is partly 'the optimizer cannot move these cells,' not 'the optimizer does not matter.'" | TF-Bind-8: 4/9 cells at p100=1.0, std 0.0, n=16; raw oracle ymax=0.439296, 7 tied rows (`results/platform/tfbind8_macos_torch28_n16.json`, `docs/DEGENERATE_CELLS.md`). **Ant (read out during this ledger pass):** `botorchgp:perturb` and `botorchgp:cma` = 1.5287419557571411, std **exactly 0.0**, 16/16 seeds; `svgp:perturb` hits the same value 10/16; `botorchgp:grad` = 1.3242 ± 0.1975 (not frozen) — `results/db_corners/corner_on_on_mujoco_db.json` (Linux, torch 2.8, git_sha 17d0465, X1/X3 on, β=2, n=16) | Trabucco Design-Bench ICML 2022 [35]; Agarwal [22] on power; Fan [13] (UCB-as-local-search) bounds the M-A mechanism | "You report 1.00 as a score when it is a fixed normalization constant." And, against the *mechanism*: "`GP_FREEZE` concludes M-B (decode snap-back), but Ant is continuous with no decode and freezes anyway — so your mechanism verdict is wrong." | The **degenerate-cell fact** is asserted (three cells across two surrogate classes converging on one bit-identical value is retrieval, not coincidence). **The mechanism label is now asserted too, as M-A (LCB PARALYSIS) — and M-B (decode snap-back) is reported by us as REFUTED.** See the mechanism block below this table. The frozen-cell case and the genuine-near-equivalence case (continuous, non-frozen) are still reported **separately, never pooled** under one claim. | **LANDED** — the fact, and the mechanism label as **M-A**, not M-B |
| **D19** | "On Design-Bench the surrogate main effect is essentially zero in all four engine corners — η²_surrogate 0.001 to 0.032 across five tasks, with every point estimate at the floor of its own bootstrap interval — and the Friedman omnibus fails to reject at p = 0.19 to 0.76; we therefore report no detectable difference at this power, not equivalence. **Equalizing surrogate-query budgets on the full seven-task grid does not weaken the optimizer axis but roughly doubles it — η²_optimizer 0.096→0.180, 0.145→0.255, 0.193→0.282, 0.181→0.281 — while η²_surrogate falls in every corner, and all four corners reject the omnibus where three did before.**" | 5-task η²_surr 0.001 / 0.032 / 0.002 / 0.018 by corner; Friedman p 0.760 / 0.263 / 0.225 / 0.190; 7-task with mujoco η²_surr 0.044–0.091; GFP-dropped (4 tasks) 0.001–0.021; `results/db_corners/db_analysis.json`. **Matched arm (0-C):** 7-task primary (UP) η²_opt **0.180 / 0.255 / 0.282 / 0.281**, η²_surr **0.043 / 0.062 / 0.037 / 0.050**, Friedman p **0.0179 / 0.000825 / 0.00145 / 0.000570** — all four reject; perturbation leads 12/12 corner×level. Achieved Q on target (grad exact, perturb −0.50%, cma +0.05–0.09%; **0 of 252 cells >5% off**) at Q = 25,600 (X3-off) / 51,456 (X3-on). Native control reproduces the published corners to **≤0.004 on every η²** and the same side of 0.05 on every p. `results/db_budget/db_budget_analysis.json`, `code/{db_budget_matched,analyze_db_budget}.py`, env `dbm` (torch 2.8.0+cpu, botorch 0.10.0), git_sha `100d2edc`, 16 seeds. `docs/DB_BUDGET_MATCH.md` | **Agarwal NeurIPS 2021 [22]** — "the lack of statistically significant results does not demonstrate the absence of effect"; **Demšar JMLR 7(1) 2006** — >10 datasets for Friedman; Benavoli JMLR 17(5) 2016 on mean-rank pool dependence | **"With N=7 you are below the threshold for the test you ran; you have shown no *detectable* difference at this power, not equivalence."** Plus Benavoli: "your mean-rank conclusions depend on an undisclosed pool." Against the promotion: **"the optimizer axis is confounded with search intensity, and gradient's 11.8× native budget manufactured it."** | **Rule 4.** The word "equivalent" appears nowhere in §6. Agarwal + Demšar are cited *by us*. The 11-cell pooling bug is disclosed and the analysis unified to 9 cells before any rank claim. **On the promotion:** the budget objection is answered by measurement, and it ran **backwards** — the native imbalance was *masking* the optimizer effect, not creating it. **Two scope limits travel with it and are not optional:** (i) **ESTABLISHED AT HIGH BUDGET.** At the matched DOWN level the picture weakens both ways — η²_surr reaches **0.126** in on_off, above the pre-registered 0.10 floor, and η²_opt falls to **0.085** against η²_surr's **0.081** in off_off, effectively tied. The primary level decides per pre-registration, so the result stands, but the phrasing is "established at high budget," mirroring 0-A.3's own DOWN-level disagreement on synthetic. (ii) **WITHIN-CORNER CIs OVERLAP,** and always did (on_on: surr [0.004, 0.339] against opt [0.137, 0.490]). The licensed claim is **point-estimate localization across corners plus the cross-corner tracking argument** of `docs/MUJOCO_CHECK.md` — **never** "η²_opt significantly exceeds η²_surr" within one corner. n=7 binds. **Scoping note:** "all four reject" is the **7-task primary** set; on the 5-task and GFP-dropped sets three of four reject under matching, with the same direction and larger η²_opt. | **LANDED** — the null at this power, **and the optimizer half, now ESTABLISHED at high budget** (0-C, 2026-07-20); the PROVISIONAL gate is discharged by measurement |
| **D20** | "This null is not manufactured by approximate oracles: it survives on the exact-oracle subset in every corner (Friedman p = 0.34 to 0.51), while the only rejections anywhere are on the RandomForest-oracle subset (p = 0.02 to 0.05 in three of four corners), and repeated oracle evaluation gives a variance of ≈1e-15, so the null is not noise drowning a signal." | Exact-oracle p 0.369/0.337/0.510/0.407; RF-oracle p 0.460/0.021/0.033/0.032; noise floor ≈1e-15 on 3×200 D-rows; `docs/POD_DB_SCALE.md` §6.3; pre-registered as X11 | Agarwal [22]; Trabucco [35]; Kim [1] (TF-Bind-8 has "overly constrained search spaces") | "Your RF oracles manufactured the null." Counter-objection: "with only two exact-oracle tasks your subset test has almost no power." | The competing mechanism is killed by a **pre-registered** test (X11), not a post-hoc one. The low-power caveat is stated **by us**: "consistent with the null" rather than a powered acceptance, corroborated by η²_surr ≈ 0 and the noise floor. Kim [1] is cited as the field's own concession that TF-Bind-8 is constrained. | **LANDED** |
### D18 — the mechanism label is M-A (LCB PARALYSIS), not M-B

**The asserted mechanism sentence:**

> The GP's LCB is **locally maximal at the data**, so the optimizer never leaves — a freeze that
> occurs **even on continuous tasks with no decode step**, which is why the optimizer axis
> inverts on Design-Bench: perturbation leads not because it searches better, but because the
> GP is frozen and cannot be moved by any of them.

**Why M-B is refuted, in one line.** `botorchgp:perturb` and `botorchgp:cma` **both** return
**1.5287419557571411** with std **exactly 0.0** across **16/16 seeds** — a **bit-identical
constant**, on a **continuous** task, with **no argmax decode anywhere in the path**. M-B
(decode snap-back) predicts that an exact-constant freeze **requires** a decode step to snap back
through. Ant has none. **The pre-registered kill against M-B fires directly**, on 2 of 3 cells,
and we report it as ours.

**What M-A buys the paper that a blocked row did not.** It converts §6's most awkward number —
η²_optimizer leading on Design-Bench while the synthetic grid says the optimizer is negligible —
from an unexplained inconsistency into a **predicted consequence**. If the GP is frozen, every
optimizer scores the GP identically, the *between-optimizer* variance that survives comes almost
entirely from the unfrozen ensemble cells, and the axis inverts. **The DB optimizer-axis
inversion and the synthetic optimizer null are the same finding seen through a frozen surrogate.**

**Four scope limits, all stated by us.**
1. **Two of three Ant GP cells, not all three.** `botorchgp:grad` = 1.3242 ± 0.1975 is **not**
   frozen; `svgp:perturb` hits the same constant on 10/16 seeds, not 16/16. Report the counts.
2. **M-A is bounded by Fan [13]** (UCB-as-local-search) under **rule 3** — application and
   diagnosis in offline MBO, never discovery. Cite Fan in the same breath as the label.
3. The **fact** and the **label** remain separable: the degenerate-cell fact stands even if a
   reviewer disputes M-A. Draft them so that losing the label does not lose the fact.
4. Frozen cells and genuine near-equivalence cells stay **unpooled**, as before.

### D21 — CUT (row removed, 2026-07-19)

**There is no D21.** The row asserted that the 2.20-versus-1.76 TF-Bind-8 discrepancy is a
cross-platform finding. **N8 is withdrawn.** `PLATFORM_ARM` Finding 1 attributes that gap to **X3
engine state** — main effect **+0.639, reproduced on a single machine** — so there is no
platform result to state, hedge, or scope. The row is **removed, not narrowed**: a hedged
cross-platform sentence would assert a comparison our own 2×2 refuted.

**No macOS-versus-Linux sentence appears anywhere in the paper.** The genuine cross-platform
question is untested, not answered, and §6 does not raise it.

The surviving material — that a benchmark number is reproducible only against a **stamped
engine** — is not orphaned: it is carried by **D15**'s X1/X3 corner attribution and by **D18**'s
engine-stamped Ant read-out, both of which assert it on evidence that is not withdrawn. D21's
removal costs the paper no claim it can still support. The row ID is **retired, not reused** —
downstream references to "D21" are stale and must be deleted, not repointed.

## Part VI — The optimizer axis and what we refuse to claim (§7)

| # | The sentence the paper asserts | Number + artifact | Bounding citation | Reviewer objection it must survive | How it is scoped to survive | Status |
|---|---|---|---|---|---|---|
| **D22** | "Our decomposition falsifies the motivating premise of Policy-Guided Gradient Search — that offline black-box optimization 'has focused on improving surrogate models while using fixed search strategies' — by holding one shared protocol and varying both axes; we make no claim about the field's general beliefs regarding surrogates versus acquisition." | η²_opt magnitude withheld pending 0-A.3; the *design* claim is independent of the number | **Shahriari Proc. IEEE 2016 [7]** — "the careful choice of statistical model is often far more important than the choice of acquisition function heuristic"; PGS AAAI 2024 [33] is the local premise falsified | **"Your headline directional result is the organizing thesis of the most-cited BO survey ever written; it is a decade old."** | **Rule 2, absolutely.** The paper contains **no** field-reversal sentence. Shahriari is cited *up front* and scoped precisely: his doctrine governs *online* BO and the acquisition-**function-family** choice (EI/PI/UCB), not the numerical optimizer/search axis (gradient ascent, hill-climbing, CMA-ES) in the *offline* setting. The residual claimed is the offline/optimizer-axis one only, against PGS's verbatim premise. Design claim and magnitude are kept strictly separate. | **LANDED** (the design claim) |
| **D23** | "Under a matched surrogate-query budget of 51,456 evaluations per cell, the optimizer main effect is small — **η²_optimizer = 0.038 [0.003, 0.123]** — so optimizer choice explains little of the variance in this grid; but the null is **established at high budget and underpowered at low**, and the *best* optimizer changes with budget, so this licenses 'the optimizer explains little variance', **never** 'the optimizer is arbitrary'." | **0.038 [0.003, 0.123]** at matched Q=51,456, replacing the published **0.005**. Secondary DOWN level (Q=4,352): 0.066 [0.014, 0.340], upper bound above the KILL threshold. **Budget-flip:** optimizer marginals — unmatched perturb 0.529 / grad **0.597** / cma 0.573 (grad best); matched UP perturb **0.732** / grad 0.593 / cma 0.558 (**perturb best**); matched DOWN perturb 0.524 / grad **0.731** / cma 0.573 (**grad best**). `results/budget/budget_analysis.json`, `docs/BUDGET_MATCHED.md` §2–3.1 | Shahriari [7]; Kim [1] | "You assert an optimizer null while your own ledger shows the optimizer axis carries an unmatched budget and three different selection rules." Now: **"your CI upper bound of 0.123 sits above your own 0.10 confirm threshold."** | The magnitude is **reported, not withheld** — 0-A.3 discharged the block. **Rule 2 still binds absolutely:** this is a magnitude for *our grid*, never a field claim. Three qualifications the paper must carry in the same passage, none optional: (i) **the published 0.005 understates by ~8×**, disclosed by us as a consequence of the budget imbalance the audit suspected; (ii) **the confirmation is not comfortable** — the CI upper bound (0.123) lies inside the pre-registered [0.10, 0.15] inconclusive band, so an optimizer effect up to ~0.12 cannot be ruled out at n=7 tasks (the same precision limit KB5 identified); (iii) **the DOWN level does not corroborate cleanly**, and per the pre-registration the primary level decides and the secondary does not override — so BM1 stands, but the honest phrasing is "established at high budget, underpowered at low." **The budget-flip finding is asserted, not buried**: an 11.8× imbalance hides itself precisely by making gradient look modestly best everywhere. | **PROVISIONAL-REPORTABLE** — magnitude asserted with its interval, its uncomfortable upper bound, and the budget-flip |
| **D24** | "Our own pre-registered prediction — that the acquisition optimizer explains most of the reported gap — was refuted by the data, and three further pre-registered kill criteria (the K=2 reversal, the aggregate β–σ mismatch, the gradient-specific coverage framing) fired against us; we report all four." | η²_opt refutation per `SKELETON.md:11,30` and FLAW_LEDGER P1-5; KB1 non-reversal (D06); KB4 aggregate refutation (D07); X7 refutation (D16); `docs/PREREGISTRATION_V2.md` | Genre-shape [2]; Agarwal [22]; the reproducibility pool generally | "Undisclosed, this reads as HARKing to anyone who opens the repo." | Disclosure is the claim. FLAW_LEDGER P1-5 rates this as *raising* credibility when disclosed. Placed in §7 as a standalone paragraph, with each refuted prediction named and its kill criterion quoted verbatim from the pre-registration. This row is what buys D06, D07, and D16 their credibility elsewhere in the paper. | **LANDED** |

---

## Enforcement index — which rule guards which row

| Hard rule | Rows it governs |
|---|---|
| 1 — K is a confound, never a mechanism | **D06**, D13 |
| 2 — never claim field-reversal | **D22**, D23 |
| 3 — C2 mechanism is application + diagnosis | **D03**, D12, D14, **D18** (M-A bounded by Fan [13]) |
| 4 — DB null is "not detectable at this power" | **D19**, D20 |
| 5 — strengthening is the net of two protocol confounds | **D09**, D10, D11 |
| 6 — K-prominence: sensitivity **and** non-reversal, equal weight | **D06**, D09, D11, D13 |

## Status roll-up (24 rows, one status each)

- **LANDED — 21:** D01, D02, D03, D04, D05, D06, D09, D10, **D11**, **D12**, **D13** (incl. the
  D13-W2 sub-claim), D14, D15, D16, D17, **D18**, **D19**, D20, D22, D24, **D25**.
- **PROVISIONAL — 1:** D07 (survives only narrowed to its per-task form; the aggregate refutes
  it).
- **PROVISIONAL-REPORTABLE — 2:** D08, D23 (η²_optimizer = **0.038 [0.003, 0.123]** asserted,
  with the ~8× correction to the published 0.005, the uncomfortable CI upper bound, and the
  budget-flip all stated in the same passage).
- **BLOCKED — 0.** Gate 0 is closed.
- **CUT — 1:** D21, removed 2026-07-19 on the withdrawal of N8. ID retired, not reused.

**Every row in this ledger is writable.** No section carries a blocked row, and the
blocked-row map is retired.

### What changed at Gate 0, in one table

| Row | Was | Is | The number that moved |
|---|---|---|---|
| **D08** | BLOCKED (0-A.3) | PROVISIONAL-REPORTABLE | η²_opt 0.005 → **0.038 [0.003, 0.123]** |
| **D11** | PROVISIONAL | LANDED | budget axis added: η²_surr 0.243 → 0.526 |
| **D12** | BLOCKED (0-A.1) | LANDED | gap **0.319 [0.196, 0.460]** @ β=0, β-invariant units |
| **D13** | BLOCKED (0-A.2) | LANDED | gap 0.480 → **0.476** across a 10.7× width range |
| **D18** | BLOCKED (0-A.5) | LANDED | mechanism **M-A**, not M-B; std exactly 0.0, 16/16 seeds |
| **D19** | PROVISIONAL | **LANDED** (0-C) | η²_opt matched: 0.096→**0.180**, 0.145→**0.255**, 0.193→**0.282**, 0.181→**0.281** |
| **D21** | BLOCKED (0-A.4) | **CUT** | N8 withdrawn; X3 main effect +0.639 on one machine |
| **D23** | BLOCKED (0-A.3) | PROVISIONAL-REPORTABLE | η²_opt reported, not withheld |

### Three claims that must be struck paper-wide

Gate 0 did not only unblock rows; it **falsified text the paper currently contains**. Each of
these is a deletion, not a hedge, and each has at least one known call site.

1. **"The paired difference is [−0.02, 0.10], indistinguishable from zero"** and the numbers
   **0.51 / 0.47** — `main.tex:198`, `supplement.tex:106`. The increment is **0.203 [0.007,
   0.396]**, which excludes zero. **No traced computation reproduces 0.51 → 0.47.** (D12(b))
2. **"The GP fits better"** in every phrasing — the ensemble beats the GP's held-out normRMSE on
   **7/7 tasks at every width** and still loses. Replace with *"the ensemble is more accurate
   in-distribution but its mean has exploitable off-distribution maxima."* (D13-W2)
3. **"0.95 at K=2"** — the supplement's figure **does not reproduce** on the audited engine,
   where the grid gives **0.283**. Any claim resting on it falls with it. (Rule 6)
