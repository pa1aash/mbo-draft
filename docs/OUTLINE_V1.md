# Outline V1 — AAAI-27, Identity D

**Title working:** *Five Confounds in Offline Model-Based Optimization Surrogate Comparison:
A De-Confounding Protocol and What Survives It*

**Primary topic:** `ML: Evaluation, Benchmarking, Datasets & Analysis`
**Secondary topic:** `SO: Algorithm Configuration & Sampling-based Search`

Primary follows AAAI's rule that a submission is filed under the subarea of its *main*
contribution [40]: the contribution is an evaluation artifact — a named confound set, a removal
protocol, and a variance-attribution instrument. That summons the empirical-rigor pool (readers
of Henderson [2], Musgrave [4], Ferrari Dacrema [3], Lucic [21], Agarwal [22]), whose priors
reward exactly this shape and to whom the strengthening direction reads as a result rather than
an anomaly. Secondary `SO: Algorithm Configuration` summons the AutoML/fANOVA pool (readers of
Hutter [15], van Rijn [46], Moosbauer [43]) who will place the two-way decomposition immediately
and expect it cited — D02 does.

**Deliberately NOT listed as a secondary:** `ML: Bayesian Learning & Uncertainty Quantification`.
That pool holds SNGP [12], Fan [13], the NTK cluster [14][29][30], and above all Li/Rudner/Wilson
[8] — every citation that bounds the mechanism rows. Per AAAI's double-edged-sword rule, an
expert there would find the mechanism content derivative (rules 1 and 3 exist because of them).

**Status of that decision after Gate 0: still OFF, but the reasoning has inverted.** It was held
off *pending* 0-A.2. 0-A.2 has now reported and **W1 CONFIRMED** — the NTK/spectral-bias
objection is answered at practical widths, which is the strongest single argument for listing the
UQ pool. It stays off anyway, for a different reason: **D13-W2 concedes that the ensemble is the
more accurate surrogate**, and a UQ expert is the reader most likely to press that concession
into "so your mechanism is a search artifact, not a surrogate property." The concession is
correct and stays in the paper; we simply do not summon the pool best equipped to attack it in a
7-page body. Revisit only if the mechanism section is expanded beyond 1.0 pg.

**Length:** 7 pages body, AAAI two-column, references excluded.

---

## Gate 0 status — 2026-07-19

**All five Stage 0 blockers have reported. No section carries a blocked row.** The
blocked-row map at the foot of this outline is retired.

| Change | Effect on this outline |
|---|---|
| **D12 unblocked** (0-A.1) | §5 beat 3 rewritten as **BASE-PLUS-AMPLIFICATION**; *Figure 3* is unblocked and panel (a) may now carry the β=0 gap |
| **D13 unblocked** (0-A.2) | §5 beat 4 was **cut-not-hedge**; it is now a **full beat**, and **D13-W2** adds a paper-wide strike order |
| **D18 unblocked** (0-A.5) | §6 beat 3 asserts the mechanism label **M-A (LCB PARALYSIS)**, not M-B |
| **D08 / D23 unblocked** (0-A.3) | §3 beat 6 and §7 beat 2 report **η²_opt = 0.038 [0.003, 0.123]**, replacing the withheld 0.005 |
| **D21 CUT** (0-A.4) | **§6 beat 4 is deleted entirely.** N8 withdrawn; §6 drops from four rows to three |
| **D11 promoted** | §4 beat 4 gains the **budget axis** as a fourth sensitivity coordinate |
| **D19 unchanged** | Still PROVISIONAL — 0-A.3 matched budgets on synthetic tasks only; DB was not re-run |

**Net page effect: −0.15 pg.** §6 loses D21 (≈0.15 pg) and §5 regains D13, which the prior
version had budgeted at zero on the cut-not-hedge rule. §5 also gains D13-W2 and the C2
budget-corroboration paragraph, so §5 is now the section under **page pressure** rather than the
one most exposed to risk. See the reallocation note under §5.

---

## Page budget

| § | Section | Pages | Cumulative |
|---|---|---|---|
| 1 | Introduction | 0.75 | 0.75 |
| 2 | What we concede, and what is left | 0.75 | 1.50 |
| 3 | The grid, and five confounds in it | 1.25 | 2.75 |
| 4 | The de-confounding protocol and its net result | 1.25 | 4.00 |
| 5 | Scoped mechanism: mean quality and σ-as-distance | **1.15** | 5.15 |
| 6 | Design-Bench: a null, and why it is null | **1.10** | 6.25 |
| 7 | Refuted predictions, limitations, and what we do not claim | 0.50 | 6.75 |
| 8 | Conclusion | 0.25 | 7.00 |

Figures/tables consume roughly 2.0 of the 7.0 pages; the allocations above are inclusive.

**Post-Gate-0 reallocation: §6 → §5, 0.15 pg.** §6 sheds D21 and drops to three rows; §5 absorbs
D13 (which the frozen version budgeted at **zero**, on the cut-not-hedge rule), the D13-W2
sub-claim, and the C2 budget-corroboration paragraph. The total is unchanged at 7.00.

**§5 is now the tightest section in the paper** — seven rows and one sub-claim in 1.15 pg. If
compression is needed at draft time, cut in this order: (1) the C2 budget-corroboration paragraph
(it is corroboration, not a load-bearing claim), (2) D17's coverage correction down to one
sentence, (3) D15's per-corner counts to the on_on and on_off corners only. **Do not compress
D13-W2** — it is the concession that makes the mechanism survive contact with the UQ pool.

---

## §1 Introduction — 0.75 pg

**Carries:** D01 (concession, one sentence), D02 (the composition claim), D09 (the headline,
with its CI), D22 (scoped premise falsification).

**Needs:** *Figure 1* — the four-corner η²_surrogate plot with bootstrap 95% CIs, published 0.37
marked as a reference line. This figure must show the overlap, not hide it; it is simultaneously
the headline (D09) and the honesty (D10). One panel, half-column.

**Beats, in order:**
1. Offline MBO compares surrogate classes under one protocol; the field's own most recent
   peer-reviewed survey concedes that benchmarks do not clarify whether gains come from the
   surrogate, the optimizer, or chance [1]. That sentence is the paper's opening warrant.
2. Concede the genre in one sentence (D01).
3. State the composition that is unclaimed (D02).
4. State the result with its interval and its composition in the *same sentence* (D09) — rule 5.
5. State what we do not claim: no field reversal (D22, rule 2), no equivalence on Design-Bench
   (rule 4), no mechanism discovery (rule 3). **Putting the refusals in the introduction is the
   paper's main defensive move**; a reviewer who reads only §1 must already know we are not
   claiming the three things that would sink us.

**Drafter constraint:** η²_surrogate = 0.405 may not appear anywhere in §1 without
[0.290, 0.556] attached (D10).

---

## §2 What we concede, and what is left — 0.75 pg

**Carries:** D01 (full), D02 (full), D03 (mechanism concession, placed early so §5 inherits it).

**Needs:** *Table 1* — the rule-out table. Rows: Li/Rudner/Wilson [8], PGS [33], RaM [34],
Design-Bench [35], Hutter fANOVA [15], Liang [16], Moosbauer [43]. Columns: surrogate class
varied? · optimizer/search varied? · variance decomposition? · offline MBO? This table is
lifted directly from NOVELTY_V3 §N6 and is the single highest-value half-page in the paper —
it is the checkable rule-out that makes D02 survive.

**Beats:**
1. The reality-check genre and its canonical instances [2][3][4][21][22]. Concede fully.
2. Balduzzi [48] ruled out by name as a comparator (benchmark-*suite* redundancy, different axis)
   — pre-empts a reviewer who reaches for it.
3. Table 1. Emphasize Moosbauer [43]: the paper closest to a two-axis design explicitly *declines*
   the two-way decomposition because "interactions between inputs cannot be detected by an OFAT
   analysis." The attribution gap is deliberate and structural, not a search artifact.
4. Hutter [15] cited defensively as the one-way precedent; Liang [16] as the descriptive-online one.
5. **D03 lands here:** SNGP [12] and Fan [13] named as owning distance-aware UQ and
   UCB-as-local-search. Doing this in §2 rather than §5 means §5 opens already-bounded.

---

## §3 The grid, and five confounds in it — 1.25 pg

**Carries:** D04, D05, D06, D07, D08.

**Needs:**
- *Table 2* — the confound taxonomy. Five rows. Columns: confound · code location · what it
  breaks · signed effect on η²_surrogate · corrected? This is the paper's artifact; per
  AAAI27_VENUE's "every accepted paper shipped a thing" rule, Table 2 **is** the thing.
- *Figure 2* — two panels: η²_surrogate versus β (0 → 5) and versus K (2 → 10), each with the
  fixed convention (β=2, K=5) marked. Shows both sensitivities at once and makes D06 and D11
  visually honest.

**Beats:**
1. The grid: 3 surrogates × 3 optimizers × 7 synthetic tasks × 30 seeds, engine-stamped.
2. **D04** target scaling — code trace, 0.367 → 0.283.
3. **D05** candidate/oracle protocol — the stated-versus-actual mismatch, 0.367 → 0.450. Frame as
   two estimands in one column; this is the strongest of the five.
4. **D06** ensemble size K. **Rules 1 and 6 are enforced here in the drafting, not just the
   framing.** Report the sensitivity (0.326→0.408, peaking at the conventional K=5) *and* the
   non-reversal (ens **0.283** vs GP **0.767** at K=2) with **equal prominence** — neither
   subordinated, neither in a footnote. State that our own pre-registered KB1 kill criterion did
   not fire and that the supplement's **0.95-at-K=2 does not reproduce** on the audited engine,
   which gives **0.283**. Scope against [8] by disjoint K range, in the same paragraph.
   **Numeral-collision guard:** D04's corrected η²_surrogate is also 0.283 and appears two beats
   earlier — name the units on both, and never let one appear to corroborate the other.
5. **D07** β–σ mismatch, narrowed to the per-task spread (0.07–1.44) with the aggregate
   refutation (median 1.19) reported first.
6. **D08** search-intensity budget — named, **measured**, and **corrected**. Three drafting
   changes from the frozen version: (i) the spread is **11.8×** (grad 51,456 / perturb 4,352 /
   CMA 932–6,536), *measured* by a counting proxy — the old "6×–59×" was an estimate, and CMA's
   `budget=3000` is a **cap that rarely binds**; (ii) the "256 vs 128 proposals" half of this
   confound **is already fixed by X3**, so the surviving inequality is in *surrogate queries*,
   not proposals — say so, or a reviewer reads it as double-counting against D05; (iii) the
   corrected value **is now asserted**: matching at Q=51,456 moves η²_optimizer from a published
   **0.005 to 0.038 [0.003, 0.123]**, an **~8× understatement disclosed by us**. Point forward
   to §7 for the scoping; §3 states the confound and its magnitude, not the null.

**✅ UNBLOCKED (0-A.3).** The placeholder is removed. **§3 must not state the optimizer null** —
that is D23's job in §7, and the null carries three qualifications (uncomfortable CI upper bound,
the DOWN-level disagreement, the budget-flip) that do not fit here. §3 reports the confound and
the corrected magnitude; §7 reports what the magnitude licenses.

---

## §4 The de-confounding protocol and its net result — 1.25 pg

**Carries:** D09, D10, D11, and the reporting half of D15/D16 attribution machinery.

**Needs:** *Figure 1* is referenced back (not redrawn). *Table 3* — the 2×2 corner table:
off_off / on_off / off_on / on_on × {η²_surr with CI, η²_opt, η²_inter, Friedman p}.

**Beats:**
1. The protocol: standardize ensemble targets; equalize candidate proposal count and impose one
   selection rule; never let the oracle choose the reported set. Stamp the engine.
2. **D09** — the net result, stated with its composition (rule 5) and its interval (D10). Recht [6]
   and Agarwal [22] pre-empted **by name in this paragraph**; Bressan [20] as a one-line
   cross-disciplinary analog; Melis [5] as the genre norm being inverted.
3. **D10** — the underpowered-decomposition constraint, framed as a self-imposed one and traced to
   our own pre-registered KB5 prediction, which confirmed. The bootstrap is validated against the
   published CI width (0.305 ≈ 0.32).
4. **D11** — the β-dependence as the *firmer* half of the sensitivity analysis (β intervals barely
   overlap where the corner intervals do not separate at all). Honest framing: the magnitude of
   η²_surr is a joint artifact of **four** operating-point coordinates, not two — K=5, β=2, the
   **query budget**, and the engine corner. **New from 0-A.3:** η²_surr **more than doubles with
   budget**, 0.243 at Q=4,352 to **0.526** at Q=51,456, so any headline η²_surrogate must state
   its **budget alongside its K and β**. Rule 6 applies to the K half.

   **This strengthens §4 rather than weakening it, and the drafting must make that visible.** A
   fourth sensitivity axis sounds like a fourth admission; it is not. The *direction* is robust at
   every β, K, and budget tested — GP marginal ~0.75–0.85 against ensemble ~0.24–0.36 throughout —
   while only the *magnitude* moves. State the invariance and the sensitivity in the same
   sentence, exactly as rule 5 requires for D09.

**Drafter note:** §4 is where the paper is won or lost with the primary pool. Every number in it
carries an interval. There is no sentence in §4 asserting a corrected value without one.

---

## §5 Scoped mechanism: mean quality and σ-as-distance — 1.15 pg

**Carries:** D03 (inherited from §2), D12, D13 + **D13-W2**, D14, D15, D16, D17.
**No blocked rows.** This section was the most exposed in the frozen version; it is now the
most *complete* — and the tightest on space.

**Needs:**
- *Figure 3* — **now three panels, and unblocked.** (a) ρ(σ, |error|) versus ρ(σ, k-NN distance)
  per task (D14); (b) premise coverage by surrogate on its own proposals, sklearn-GP 0.97 against
  grid-GP 0.831 (D17); **(c) NEW — the gap-versus-width curve**, 0.480 / 0.336 / 0.414 / 0.476 at
  w = 96 / 256 / 512 / 1024, **with CIs drawn**, against the ensemble's held-out normRMSE falling
  monotonically 0.4446 → 0.3877 and the GP's 0.4795 as a reference line. Panel (c) carries W1 and
  W2 in **one image**: the gap is flat while accuracy improves and overtakes the GP.
  **Panel (c) must draw the CIs, and they must be visibly widening with w** — the honest reading
  is "does not close," not "identical," and a CI-free curve overclaims.
- **Do NOT extend panel (a) to carry the β=0 gap.** The frozen version contemplated it; 0-A.1
  makes it a units error waiting to happen, since the β=0 gap lives on the β-invariant normalizer
  and panel (a)'s correlations do not. D12's numbers go in **text**, not into Figure 3.

**Beats:**
1. Open bounded: SNGP [12] owns distance-aware UQ, Fan [13] owns UCB-as-local-search; what
   follows is application and diagnosis in the offline setting (rule 3). **First two sentences.**
2. **D14** σ is a distance signal, not an error signal (0.07 vs 0.26). Frame as correcting a
   measurement made against the wrong target. **Ovadia [28] is not cited here** — citing it in
   support invites a mis-citation flag.
3. **D12 — the β=0 mean-quality base. ✅ UNBLOCKED, rewritten as BASE-PLUS-AMPLIFICATION.**
   The GP family retains **61%** of its advantage with σ removed entirely: **0.319 [0.196, 0.460]**
   at β=0 against **0.525 [0.406, 0.614]** at β=2, increment **0.203 [0.007, 0.396]**, p = 0.020.
   The claim is *"the GP's mean advantage is real and substantial independent of pessimism;
   pessimism amplifies it"* — a base that pessimism **amplifies rather than creates**.
   **Three constraints, none negotiable** (full text: `CLAIM_LEDGER.md` § "D12 — three hard
   constraints"): **(a)** cite **0.319 / 0.525** for every cross-β comparison, **never 0.378 /
   0.556 as a ratio** — those are β-refit, a different ruler per β; 0.378 may appear only as a
   within-β descriptive figure. **(b)** The paper's current passage is **refuted**: strike
   0.51/0.47 (unattributed; **no traced computation reproduces the pair**, and off_off runs *up*,
   0.504→0.511, not down), strike the **[−0.02, 0.10] "indistinguishable from zero"** CI, and
   strike the "**not of σ**" conclusion — at `main.tex:198` **and** `supplement.tex:106`.
   **(c)** The phrase **"independent of pessimism" is dead.** Also note KB2 passes but **not
   comfortably** (0.319 against a 0.263 threshold, margin inside the CI).
4. **D13 — jaggedness as a class property. ✅ UNBLOCKED; W1 CONFIRMED.** Gap **0.480 at w=96**
   against **0.476 at w=1024** over a **10.7× width range at fixed K=5** — **99.1% retained**,
   shrinkage −0.006 [−0.210, 0.161], **flat with noise and non-monotone** (it dips at w=256 and
   returns), so it is not a decay. **The NTK/spectral-bias objection does not survive at practical
   widths.** State with the **CI caveat, not as a footnote**: the CI **widens monotonically with
   w** (0.211 → 0.439), so w=1024 is the least precise point on the curve; the supported claim is
   *"the gap does not close,"* **never** *"the gap is identical at w=1024,"* and **no asymptotic
   claim in w may be written** — NTK limits are asymptotic and the sweep stops at 1024.
   Note the validity check (w=96 reproduces the incumbent grid **bit-exactly** for grad and cma).
5. **D13-W2 — accuracy is not the bottleneck. NEW hardened sub-claim.** The ensemble **beats** the
   GP's held-out normRMSE on **7/7 tasks at every width** (mean 0.388–0.445 against the GP's
   0.479; 26/28 cells) **and still loses** the optimization gap by ~0.48. **The more accurate
   surrogate is the one that loses.** Cite the **registered tie-cell result (mean gap 0.375 at the
   two Styblinski cells where RMSE is statistically indistinguishable) as primary**, and the 7/7
   result as the stronger **post-hoc** observation, labelled as such. **Do not use held-out NLL**
   as a second accuracy axis (GP 202.7 vs ensemble 5.7–6.4) — that is a calibration finding,
   orthogonal to W2.

   > **⚠ PAPER-WIDE STRIKE ORDER.** Every phrasing of the form *"the GP fits better"* / *"the GP
   > models the function better"* / *"the GP is the more accurate surrogate"* is **struck in all
   > sections**, and replaced with: **"the ensemble is more accurate in-distribution but its mean
   > has exploitable off-distribution maxima."** This is not a §5-local edit. Grep the manuscript
   > before submission — a surviving instance directly contradicts our own Table/Figure 3(c).

6. **C2 third-axis corroboration — short paragraph, from the budget arm.** η²_surrogate **more
   than doubles with search budget** (0.243 → **0.526**) because the **ensemble marginal falls**
   as budget rises (0.361 → 0.240) while **both GPs rise** (0.755 → 0.849, 0.713 → 0.794). More
   search pressure finds more off-distribution maxima in the ensemble's mean; the GP's smoother
   mean has less to exploit. **This is the third independent axis** — 0-A.1 removed σ, 0-A.2
   raised width, 0-A.3 raised search pressure, and all three converge on mean geometry.
   **Report as an observation, not a pre-registered result** (the arm was not designed to test
   it), and as corroboration of the *mechanism* only, never as evidence for any η² *magnitude*.
   **First to cut if §5 overruns.**
7. **D15** the gradient collapse is genuine surrogate geometry on the majority of tasks, driven by
   X3 not X1 (4/7 at on_on, 0/7 at on_off). Report the corner that fires against us.
8. **D16** the collapse is not gradient-specific under the matched protocol (0.010 vs 0.117);
   the gradient-specific framing is retracted by name.
9. **D17** the 0.97-versus-0.831 GP identity correction.

**✅ NO BLOCKED ROWS.** Both former blockers reported and both confirmed. The cut-not-hedge
standing order on D13 is **discharged and retired** — D13 is written in full, at the scope 0-A.2
supports and no wider.

**The one way §5 can still fail.** Beats 3, 4, 5 and 6 all argue *against* the ensemble from
different directions, and beat 5 concedes the ensemble is more accurate. Drafted carelessly that
reads as motivated reasoning. The ordering above is the defence: **concede the accuracy result
(beat 5) before offering the corroboration (beat 6)**, so the mechanism is seen surviving its
own strongest counter-evidence rather than being propped up by a fourth friendly number.

---

## §6 Design-Bench: a null, and why it is null — 1.10 pg

**Carries:** D18, D19, D20. **D21 is cut — this section carries three rows, not four.**

**Needs:**
- *Table 4* — DB four-corner η² (surrogate, optimizer, interaction) with CIs and Friedman p,
  reported at 5 tasks, 7 tasks with mujoco, and 4 tasks GFP-dropped. Three task sets in one table
  is what makes the null robust rather than selective.
- *Figure 4* — the degenerate-cell figure: TF-Bind-8's four constant cells at exactly 1.0 against
  the cells that move, plus Ant's two zero-variance GP cells. This figure is the mechanism half of
  the null and is the reason the null is publishable rather than a weakness.

**Beats:**
1. **D19** the null itself: η²_surr ≈ 0 in all four corners, Friedman fails to reject.
   **Rule 4 is enforced in the drafting: the word "equivalent" does not appear in §6.** Agarwal
   [22] and Demšar cited *by us*, converting the strongest rejecting citation into the framing.
   Explicit power/N specification attached. Disclose the 11-cell `analysis.task_norm` pooling and
   unify to 9 cells before any rank claim; cite Benavoli (JMLR 17(5), 2016) and follow his
   recommendation for pairwise tests.
2. **D20** the RF-oracle competing mechanism killed by the pre-registered X11 test, with the
   low-power caveat stated by us.
3. **D18 — the degenerate cells, and the mechanism. ✅ UNBLOCKED as M-A (LCB PARALYSIS).**
   The *fact* first: `botorchgp:perturb` and `botorchgp:cma` both return **1.5287419557571411**
   with std **exactly 0.0** across **16/16 seeds**, `svgp:perturb` hits the same value 10/16, and
   TF-Bind-8 has four cells at exactly 1.0 — three cells across two surrogate classes converging
   on one bit-identical value is **retrieval, not coincidence**. Then the *label*: this is a
   **bit-identical constant on a CONTINUOUS task with no argmax decode**, which fires the
   pre-registered kill against **M-B (decode snap-back)** directly. **The mechanism is M-A:**
   *the GP's LCB is locally maximal at the data, so the optimizer never leaves — a freeze
   occurring even on continuous tasks with no decode step.*
   **Why this matters beyond the label:** it explains §6's most awkward number. If the GP is
   frozen, every optimizer scores it identically, the surviving between-optimizer variance comes
   from the unfrozen ensemble cells, and **the optimizer axis inverts** — perturbation leads on
   Design-Bench not because it searches better but because the GP cannot be moved. **The DB
   inversion and the synthetic optimizer null become one finding seen through a frozen surrogate.**
   Four limits, all ours: `botorchgp:grad` = 1.3242 ± 0.1975 is **not** frozen (2 of 3 cells, not
   3); **M-A is bounded by Fan [13]** under rule 3, cited in the same breath; **fact and label
   stay separable** so that losing the label does not lose the fact; frozen and
   genuine-near-equivalence cells stay **unpooled**.

**✅ NO BLOCKED ROWS. One row deleted:**

> **D21 is CUT — do not write it, do not hedge it, do not reference it.** The frozen version's
> beat 4 (the engine-state attribution as a cross-platform finding) **no longer exists**. N8 is
> **withdrawn**: the 2.20-vs-1.76 gap is **X3 engine state**, main effect **+0.639 reproduced on
> a single machine**, per `PLATFORM_ARM` Finding 1. **No macOS-versus-Linux sentence appears
> anywhere in the paper**, and §6 does not raise the question — it is untested, not answered.
> The surviving idea (a benchmark number is reproducible only against a **stamped engine**) is
> **not orphaned**: D15's X1/X3 corner attribution and D18's engine-stamped Ant read-out both
> assert it on evidence that has not been withdrawn. Nothing is lost by the deletion.
> The ID is **retired, not reused** — stale "D21" references are deleted, never repointed.

---

## §7 Refuted predictions, limitations, and what we do not claim — 0.50 pg

**Carries:** D23, D24, and the terminal restatement of D22.

**Needs:** *Table 5* — "what we do not claim," four rows, one per hard rule 1–4, each with the
citation that would otherwise sink it. Half-column. This table is a defensive asset: it shows the
reviewer we have read their objection before they wrote it.

**Beats:**
1. **D24** — the pre-registration paragraph. Our registered headline (the optimizer explains most
   of the gap) was refuted; three further kill criteria fired against us (K=2 non-reversal, the
   aggregate β–σ refutation, the gradient-specific coverage framing). Each named, each with its
   kill criterion quoted verbatim from `PREREGISTRATION_V2.md`. **This paragraph is what buys D06,
   D07, and D16 their credibility in §3 and §5.**
2. **D23 — the optimizer magnitude. ✅ UNBLOCKED; reported, no longer withheld.** Under a matched
   surrogate-query budget of **Q = 51,456**, **η²_optimizer = 0.038 [0.003, 0.123]** — reported
   in place of the published **0.005**, which understates by **~8×**. Three qualifications belong
   in the **same passage**, none optional: (i) the ~8× correction is **disclosed by us** as a
   consequence of the budget imbalance the audit suspected — the imbalance was real, it simply
   did not change the conclusion; (ii) **the confirmation is not comfortable** — the CI upper
   bound of **0.123** sits inside the pre-registered [0.10, 0.15] inconclusive band, so an effect
   up to ~0.12 is not excluded at n=7 tasks; (iii) the secondary level **does not corroborate
   cleanly** (η²_opt = 0.066 [0.014, 0.340] at Q=4,352), so the null is **"established at high
   budget, underpowered at low"** — never unqualified.

   > **⚠ THE BUDGET-FLIP, AND WHAT A LOW η²_opt LICENSES.** The optimizer **ranking flips with
   > budget**: **grad best at low** budget (0.731), **perturb best at high** (0.732). An 11.8×
   > imbalance hides itself precisely by making gradient look modestly best everywhere. So a low
   > η²_opt licenses **"optimizer choice explains little variance"** and **NOT "optimizer choice
   > is arbitrary."** The second reading is the one a `SO: Algorithm Configuration` reviewer will
   > test first, and it is false on our own data. Assert the flip; do not bury it.

3. **D22** restated terminally: Shahriari [7] owns the general doctrine; we falsify PGS's [33]
   local premise only. **Rule 2 binds harder now that D23 reports a number** — a magnitude for
   *our grid* is not a field claim, and §7 must not let the two blur in the same paragraph.
4. Remaining limitations: n=7 task count; seed-0 single dataset draw; GFP quarantine; the
   synthetic-versus-Design-Bench divergence stated as a finding, not smoothed over — **now
   partly explained by D18's M-A**, which is the better framing: the divergence has a candidate
   mechanism, not merely a caveat. **New limitation to add:** the budget matching covers the
   **seven synthetic tasks only**; Design-Bench was **not** re-run under matched budget, which is
   exactly why D19's optimizer half remains PROVISIONAL. State that ourselves.

**✅ NO BLOCKED ROWS.** §7 grows in content but not in pages — the withheld-magnitude paragraph
is replaced, not supplemented, by the reported magnitude and its three qualifications.

---

## §8 Conclusion — 0.25 pg

**Carries:** D02, D09 restated. No new claims, no new numbers, no number without its interval.

---

## Blocked-row map — RETIRED

**There are no blocked rows. All eight sections are writable end to end.** The map is kept below
only as a record of what each blocker resolved to, so a drafter reading a stale reference can see
where it went.

| Row | § | Blocker | Resolution | Status |
|---|---|---|---|---|
| **D08** | §3 | 0-A.3 matched budget | η²_opt **0.038 [0.003, 0.123]** at Q=51,456; measured spread 11.8×, not 6×–59× | ✅ PROVISIONAL-REPORTABLE |
| **D12** | §5 | 0-A.1 β=0 reconciliation | **0.319 [0.196, 0.460]** at β=0, β-invariant units; base-plus-amplification | ✅ LANDED |
| **D13** | §5 | 0-A.2 width verdict | **W1 CONFIRMED** — 99.1% of the gap retained at 10.7× width; **W2** added | ✅ LANDED |
| **D18** | §6 | 0-A.5 Ant read-out | **M-A (LCB paralysis)**; M-B refuted by a bit-identical constant on a continuous task | ✅ LANDED |
| **D21** | §6 | 0-A.4 platform-vs-engine | **N8 withdrawn** — the gap is X3 engine state (+0.639, one machine) | ❌ **CUT** |
| **D23** | §7 | 0-A.3 matched budget | Magnitude **reported**, with the budget-flip and the low-budget caveat | ✅ PROVISIONAL-REPORTABLE |
| **D19** | §6 | 0-A.3 (DB half) | **NOT discharged** — matching ran on synthetic tasks only | ⚠ PROVISIONAL |

**The paper is now writable at 19 LANDED + 2 PROVISIONAL + 2 PROVISIONAL-REPORTABLE = 23 rows.**
Against the frozen version's fallback plan (15 LANDED + 3 PROVISIONAL, "thinner but unfalsifiable"),
Gate 0 delivered four unblocks and one deletion. §5 goes from the most exposed section to the most
complete one; §6 loses a row and gains a mechanism.

**What Gate 0 cost, stated plainly.** It was not free. It **falsified three claims the manuscript
currently makes** — the β=0 passage at `main.tex:198` and `supplement.tex:106`, every "the GP fits
better" phrasing, and the supplement's 0.95-at-K=2 — and it **octupled** a headline the paper
reports as 0.005. Those are edits to existing text, not additions, and they are listed at the foot
of `docs/CLAIM_LEDGER.md` under **"Three claims that must be struck paper-wide."** **Do the strikes
before drafting new prose**, or the draft will be built on sentences the ledger has already killed.
