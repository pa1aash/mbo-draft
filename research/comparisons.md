# Cross-locus comparisons

Six committed positions from step 5, read in cross-section. Five dynamics survive as genuine —
each must become a visible argumentative beat in the report, not a one-line gesture.

---

## Tension 1: The interaction is promotable as a direction, not as a magnitude

- **Locus 3** ([[interim-report-interaction-term-buried-and-its-methodological-grounding]])
  commits: promote the interaction to a cited, interpreted **main-text** finding — not the
  abstract headline — scoped explicitly to the synthetic grid. Confidence ~80% on "interpret
  with citation", ~65% on placement.
- **Locus 2** ([[interim-report-minmax-normalization-outlier-fragility]]) commits: the
  decomposition is **methodologically fragile but empirically robust in direction**. All 33
  normalizer combinations preserve η²_surr > η²_opt; **magnitudes do not survive** a change of
  normalizer. Confidence high on both halves.

**The cross-locus dynamic.** The interaction *is* an η², so locus 2's magnitude-fragility verdict
applies directly to the number locus 3 wants to promote. These do not contradict — they
compose into a sharper instruction than either gives alone. Locus 2's 33-combination sweep
establishes that **direction** survives; locus 3's simple-effects table and significance testing
establish that the interaction **exists and is large relative to the optimizer main effect**.
What neither supports is promoting "0.15" as a stable quantity.

**How the draft should engage this.** The recommendation must be to report the interaction as
**an existence-and-ordering claim** ("surrogate and optimizer are not separable; the interaction
exceeds the optimizer main effect in every corner") with the point estimate and interval given
as *measured under the stated normalizer*, exactly as the paper already qualifies its headline.
Recommending an unqualified 0.15 would import the fragility the audit is simultaneously warning
about — an internal inconsistency a critic would catch.

**Calibration note.** Both investigators are high-confidence on the halves that matter here, and
neither names the other's finding as a falsifier. Locus 2 explicitly flags that no mixed-effects
model with task as a random effect was fitted — the repair `FLAW_LEDGER.md` P1-2 actually calls
for — so both positions rest on the same unfitted-model limitation.

---

## Tension 2: The audit proved the decomposition is derivable from a competitor's published table — which cuts both ways for N6

- **Locus 1** ([[interim-report-n6-residual-scoping-legitimate-or-gerrymandered]]) commits: N6 is
  **DEFENSIBLE-BUT-MUST-BE-ARGUED**. Ground (2) is falsified — a clean 4×2 crossed
  optimizer × training-loss sub-grid **does** exist in RaM Table 3. Grounds (1) and (3) survive.
  Confidence high.
- **Locus 3** commits: a significant interaction is the specific payoff a crossed design buys
  over one-factor-at-a-time, and the paper should say so.

**The cross-locus dynamic.** This is the sharpest dynamic in the set, and it is uncomfortable.
To defend N6, locus 1 **computed η² directly from RaM's own published Table 3** — obtaining 0.027
on the loss axis against 0.577 on the method axis. That computation *is* a two-way variance
decomposition of somebody else's crossed grid, performed from the published numbers. So the
audit has demonstrated, in the act of defending the claim, that **the decomposition N6 claims as
novel is derivable from a competitor's already-published table.**

This strengthens one reading of N6 and weakens another. It strengthens *"no prior work **reports**
a crossed surrogate × optimizer decomposition"* — still true, since RaM reports Score±std and
%Gain. It weakens *"no prior work **could have**"* — demonstrably false, and the audit proved it
in under a day.

**How the draft should engage this.** N6 must be stated as a claim about **what the literature
reports**, never about what the design space permits, and the RaM footnote should say so plainly.
The honest framing is that the contribution is running the decomposition **as the primary
analysis on a purpose-built grid**, not the arithmetic itself. This is a narrower claim than the
paper currently makes and it is the one that survives contact with Tan et al.

**Calibration note.** Locus 1 flags two open items that bear directly on this: the AutoML /
kernel-selection literature was not searched (could attack ground 1), and the η² computation has
not been cross-checked by a second implementation. The second matters here — the report is
leaning on a number the audit itself computed once.

---

## Tension 3: The venue advice is right in direction but its named assets are all qualified

- **Locus 6** ([[interim-report-aaai-venue-fit-for-the-audit-genre]]) commits: AAAI folds
  novelty and significance into one bundled criterion with **no audit/reproducibility rubric**,
  unlike NeurIPS's dedicated track. Genre framing is necessary but not sufficient. Lead with
  positive findings — the interaction and the 7/7 raw-units result — ahead of the seven
  eliminations.
- **Locus 3** commits: the interaction is **synthetic-grid-specific** (Design-Bench η²_inter is
  0.006–0.041, subordinate to η²_opt there).
- **Locus 2** commits: magnitudes are normalizer-dependent.
- **The orchestrator** established that the 7/7 raw-units result has a **live floor-effect
  confound** — the one task where perturbation is the grid's best optimizer (Styblinski) shows
  the weakest attenuation, which is what a floor effect predicts.

**The cross-locus dynamic.** Locus 6 wrote its recommendation against the findings ledger as it
stood before three of the four qualifications landed. Its *direction* survives all of them —
leading with a positive result rather than seven negatives is correct regardless of which
positive leads. But every asset it named is more qualified than it knew.

The resolution is that the two candidate assets fail **different** challenges, which is why they
must be reported together:

| | Interaction η² | 7/7 raw-units attenuation |
|---|---|---|
| Significant, interval excludes zero | **yes**, all four corners | no — descriptive, no intervals |
| Survives bias correction | **yes** (0.134–0.156) | n/a |
| Survives the normalizer challenge | **no** — rides on min–max | **yes** — raw oracle units |
| Survives the floor-effect challenge | **yes** — unaffected | **no** — Styblinski points the wrong way |
| Generalises beyond the synthetic grid | **no** — DB is 0.006–0.041 | untested on DB |

**How the draft should engage this.** Recommend leading with the **interaction**, scoped to the
synthetic grid, supported by locus 3's formal simple-effects table (which has the intervals the
raw-units analysis lacks), and present the raw-units attenuation as its **interpretation with the
floor-effect confound disclosed as an open question**. Do not recommend promoting either alone.

**Calibration note.** Locus 6 is explicitly low-budget (2 sources) and describes its own
placement advice as the weaker half. Locus 3 is ~65% confident on abstract-versus-main-text.
Converging low confidence on placement means the report should recommend the *content* firmly and
the *placement* tentatively.

---

## Tension 4: A stable per-task ranking coexists with a collapsing per-task magnitude

- **Locus 5** ([[interim-report-landscape-predicts-which-surrogate-wins]]) commits: no standard
  landscape covariate predicts the gap (dimension ρ < 0.11, p > 0.8; modality and separability
  actively mis-sort) — **but the per-task gap ranking is highly stable across optimizers,
  Spearman 0.84–0.96.**
- **Locus 3** + orchestrator: the surrogate effect **collapses to ≈0.01 under perturbation**
  against 0.4–0.8 under gradient and CMA.

**The cross-locus dynamic.** These look contradictory and are not, and the reconciliation is
itself informative. Locus 5 measures the **relative ordering** of tasks; locus 3 measures the
**absolute magnitude** within each optimizer. Both hold: the tasks keep their rank order under
every optimizer while the overall scale of the gap collapses under the weak one. Whatever makes
Griewank a worse case than Rosenbrock is a **task property that persists across optimizers**,
even where the optimizer flattens the gap toward zero.

That combination is a real constraint on any mechanism account. It rules out a purely
optimizer-side story (which would not preserve task ordering) and a purely task-side story
(which would not collapse under perturbation). **The mechanism has to be multiplicative — a task
factor scaled by an optimizer-aggressiveness factor.** No locus proposed that, and it follows only
from putting the two together.

**How the draft should engage this.** Name it explicitly in the mechanism discussion as a
constraint the paper's own data imposes on any surviving explanation — the one positive structural
statement the audit can offer about a section that is otherwise seven negatives.

**Calibration note.** Locus 5's ρ 0.84–0.96 is computed on n=7 tasks, so the ranking-stability
claim is descriptive. Locus 3's simple-effects figures are bootstrapped. Weight accordingly: the
collapse is better evidenced than the stability.

---

## Tension 5: Elimination 2 is not as eliminated as the count implies

- **Locus 4** ([[interim-report-ntk-width-citations-never-verified]]) commits: 3 of 4 citations
  faithful, but **`rahaman2019spectralbias` is miscited in effect** — its theorem holds "for
  arbitrary width and depth" and its own ablation finds **depth dominant, width considerably
  weaker** — while `main.tex:88` fixes the ensemble at a **two-hidden-layer MLP** across the
  entire width sweep.
- **Locus 3** commits: the crossed design's value is what it can detect that OFAT cannot.

**The cross-locus dynamic.** The paper's headline framing is "seven controls, none survives." But
Elimination 2 swept the axis its own cited source calls **weak** and held fixed the axis that
source calls **dominant**. So the capacity explanation is eliminated *at fixed depth 2*, not
eliminated. **The count of seven is doing rhetorical work the underlying controls do not fully
support** — at least one of the seven is narrower than stated.

This compounds with tension 2: the paper's two headline structural claims (a novel crossed
design, seven eliminations) both turn out to need narrowing after primary-source contact, and in
both cases the narrowed version is defensible while the stated version is not.

**How the draft should engage this.** Deliverable (i) must carry the Rahaman fix; deliverable
(iii) should note that the eliminations' *framing* — a bare count — is more brittle than the
eliminations themselves, and that stating each control's scope (width at fixed depth; σ at this
ensemble construction) costs little and forecloses this line of attack.

**Calibration note.** Locus 4 explicitly did not check `supplement.tex` for duplicate or
contradictory NTK framing, and flags that a depth sweep may exist unreported. Both go to the
terminal section: the depth confound is asserted from the main text's architecture description,
not from confirmed absence of a depth experiment.

---

## The convergence worth stating separately

Three independent routes reached the interaction term: analyst A, analyst B, and the
orchestrator's own artifact work — none prompted by the others. Convergence from independent
paths on a quantity the paper prints four times and never discusses is itself a finding, and the
report should say so when introducing it.
