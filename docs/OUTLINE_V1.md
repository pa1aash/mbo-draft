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
Keep it off until 0-A.2 reports.

**Length:** 7 pages body, AAAI two-column, references excluded.

---

## Page budget

| § | Section | Pages | Cumulative |
|---|---|---|---|
| 1 | Introduction | 0.75 | 0.75 |
| 2 | What we concede, and what is left | 0.75 | 1.50 |
| 3 | The grid, and five confounds in it | 1.25 | 2.75 |
| 4 | The de-confounding protocol and its net result | 1.25 | 4.00 |
| 5 | Scoped mechanism: mean quality and σ-as-distance | 1.00 | 5.00 |
| 6 | Design-Bench: a null, and why it is null | 1.25 | 6.25 |
| 7 | Refuted predictions, limitations, and what we do not claim | 0.50 | 6.75 |
| 8 | Conclusion | 0.25 | 7.00 |

Figures/tables consume roughly 2.0 of the 7.0 pages; the allocations above are inclusive.

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
4. **D06** ensemble size K. **Rule 1 is enforced here in the drafting, not just the framing.**
   Report the sensitivity (0.326→0.408, peaking at the conventional K=5) *and* the non-reversal
   (ens 0.283 vs GP 0.767 at K=2) with equal prominence. State that our own pre-registered kill
   criterion did not fire and that the supplement's 0.95-at-K=2 does not reproduce on the audited
   engine. Scope against [8] by disjoint K range, in the same paragraph, not in a footnote.
5. **D07** β–σ mismatch, narrowed to the per-task spread (0.07–1.44) with the aggregate
   refutation (median 1.19) reported first.
6. **D08** search-intensity budget — named and quantified (6×–59×), correction deferred.

**⚠ BLOCKED:** **D08's corrected value** — 0-A.3 (matched budget). The drafter writes the
confound's existence and the 6×–59× spread; the sentence "after equalizing budgets, η²_optimizer
is X" cannot be written. Leave the placeholder explicit.

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
   η²_surr is a joint artifact of K=5 and β=2, both conventions chosen where the effect is largest.

**Drafter note:** §4 is where the paper is won or lost with the primary pool. Every number in it
carries an interval. There is no sentence in §4 asserting a corrected value without one.

---

## §5 Scoped mechanism: mean quality and σ-as-distance — 1.00 pg

**Carries:** D03 (inherited from §2), D12, D13, D14, D15, D16, D17.

**Needs:** *Figure 3* — two panels: (a) ρ(σ, |error|) versus ρ(σ, k-NN distance) per task, the
D14 result; (b) premise coverage by surrogate on its own proposals, with the sklearn-GP 0.97 and
grid-GP 0.831 values side by side (D17). *This figure cannot be finalized until 0-A.1 reports* if
panel (a) is extended to carry the β=0 gap.

**Beats:**
1. Open bounded: SNGP [12] owns distance-aware UQ, Fan [13] owns UCB-as-local-search; what
   follows is application and diagnosis in the offline setting (rule 3). **First two sentences.**
2. **D14** σ is a distance signal, not an error signal (0.07 vs 0.26). Frame as correcting a
   measurement made against the wrong target. **Ovadia [28] is not cited here** — citing it in
   support invites a mis-citation flag.
3. **D12** the β=0 mean-quality base. ⚠ BLOCKED.
4. **D13** jaggedness as a class property. ⚠ BLOCKED.
5. **D15** the gradient collapse is genuine surrogate geometry on the majority of tasks, driven by
   X3 not X1 (4/7 at on_on, 0/7 at on_off). Report the corner that fires against us.
6. **D16** the collapse is not gradient-specific under the matched protocol (0.010 vs 0.117);
   the gradient-specific framing is retracted by name.
7. **D17** the 0.97-versus-0.831 GP identity correction.

**⚠ BLOCKED — two of seven rows:**
- **D12** (β=0 reconciliation, 0-A.1). Three numbers exist for one quantity: 0.47 cited,
  0.504→0.511 recomputed, 0.378 on the grid. The drafter cannot write the mean-quality sentence
  until one is chosen and the other two explained. **All three agree on direction**, so the
  *direction* sentence ("the gap does not collapse when σ is removed") is writable now; only the
  magnitude is blocked.
- **D13** (width verdict, 0-A.2). **If 0-A.2 does not report, cut D13 entirely — do not hedge.**
  A hedged width claim hands the Bayesian-deep-learning pool exactly the K≠width category error
  that rule 1 exists to prevent, and that error is catchable in one line. §5 loses ~0.15 pg and
  reallocates it to §6.

---

## §6 Design-Bench: a null, and why it is null — 1.25 pg

**Carries:** D18, D19, D20, D21.

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
3. **D18** the degenerate cells — why the null is partly structural. Frozen cells and genuine
   near-equivalence reported **separately, never pooled**.
4. **D21** the engine-state attribution: benchmark numbers are reproducible only against a stamped
   engine, and the published cell is identifiable as a specific pre-audit protocol state.

**⚠ BLOCKED — two of four rows:**
- **D18's mechanism label** (0-A.5, Ant freeze read-out). The degenerate-cell *fact* is landed and
  writable now, including Ant: `botorchgp:perturb` and `botorchgp:cma` return 1.5287419557571411
  with exactly zero variance on 16/16 seeds, and `svgp:perturb` hits the same value 10/16 —
  three cells across two surrogate classes on one bit-identical value. What is blocked is the
  *mechanism label*: `GP_FREEZE` concluded M-B (decode snap-back), which predicts no exact-constant
  freeze without a decode step, and Ant is continuous with no decode. **The pre-registered kill
  fires against M-B, 2 of 3 cells.** The drafter may not write "the freeze is decode snap-back"
  until 0-A.5 confirms 1.5287419557571411 is Ant's normalized dataset-best and reports
  `disp_from_data` for those cells.
- **D21's cross-platform half** (0-A.4). The engine-state attribution is landed and is what §6
  asserts. **No macOS-versus-Linux portability sentence may be written** — the prior framing was
  refuted by our own 2×2, and the genuine cross-platform question is declared open.

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
2. **D23** — the optimizer magnitude withheld by name, with the budget confounds stated.
   ⚠ BLOCKED on 0-A.3.
3. **D22** restated terminally: Shahriari [7] owns the general doctrine; we falsify PGS's [33]
   local premise only.
4. Remaining limitations: n=7 task count; seed-0 single dataset draw; GFP quarantine; the
   synthetic-versus-Design-Bench divergence stated as a finding, not smoothed over.

**⚠ BLOCKED:** D23 (0-A.3).

---

## §8 Conclusion — 0.25 pg

**Carries:** D02, D09 restated. No new claims, no new numbers, no number without its interval.

---

## Blocked-row map for the drafter

| Row | Section | Blocker | What is writable now | What is not |
|---|---|---|---|---|
| **D08** | §3 | 0-A.3 matched budget | The confound's existence; the 6×–59× spread | Any corrected η²_optimizer |
| **D12** | §5 | 0-A.1 β=0 reconciliation | The *direction* — the gap does not collapse at β=0 (all three numbers agree) | The *magnitude*; any figure panel carrying the β=0 gap |
| **D13** | §5 | 0-A.2 width verdict | Nothing | The whole row. **Cut, do not hedge, if 0-A.2 misses.** |
| **D18** | §6 | 0-A.5 Ant read-out | The degenerate-cell fact, TF-Bind-8 and Ant, with all numbers | The M-B mechanism label — the Ant data fires the pre-registered kill *against* it |
| **D21** | §6 | 0-A.4 platform-vs-engine | The engine-state attribution (X3 +0.639 vs X1 +0.197) | Any macOS-versus-Linux portability sentence. Prior N8 framing is **refuted**, not pending. |
| **D23** | §7 | 0-A.3 matched budget | The withholding itself, as a stated limitation | The number 0.01 |

**Three of eight sections carry a blocked row** (§3, §5, §6, §7 — four, counting D23). §5 is the
most exposed: two of its seven rows are blocked, and one of those (D13) is a cut-not-hedge.

**If Stage 0 reports nothing at all**, the paper is still writable at 15 LANDED + 3 PROVISIONAL
rows: §1–§4 are complete, §5 loses D12's magnitude and all of D13, §6 loses D18's mechanism label
and D21's cross-platform half, §7 loses D23. That version is thinner but contains no sentence a
reviewer can falsify — which is the standard Identity D was chosen to meet.
