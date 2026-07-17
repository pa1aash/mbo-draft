# 06 · Cross-locus reconciliation — named tensions and engagement guidance

**Step 6 of the research core.** The committed positions from 05 do not sit independently — they pull on
each other. This file names the cross-locus tensions and gives the draft explicit engagement guidance, so
the paper's argument has density rather than five parallel claims.

**Scope honesty.** In a full pipeline this is `research/comparisons.md`, reconciling parallel
depth-investigator outputs. Here it reconciles the inline investigations of 05. Four named tensions, each
with a resolution the paper should adopt.

---

## TENSION 1 — "Run the decisive experiment" (L2) vs "the decisive experiment might delete the paper" (L2/L3)

**The pull.** L2's committed position is that the ensemble objection is *answerable only by running X1+X3*,
and the honest expected outcome is a weaker headline. L3's position is that the smooth-mean mechanism is *a
bet on X1's outcome* — if smoothing the normalized ensemble doesn't close the gap, Identity C collapses to
A. So the single re-run that rescues the paper's credibility can also destroy its thesis.

**Why it is not a contradiction.** Both positions agree the current headline is *confounded, not
established*. The re-run does not create the risk; it *reveals* a risk that is already there and that a
reviewer will find in the artifact (P0-2, P0-0) whether or not the authors look. Running it is strictly
dominant: it converts an undisclosed liability into either a stronger paper or an earlier, cheaper pivot.

**Engagement guidance for the draft.**
- Sequence X1 (normalize) + X3 (matched budgets/protocol) **first**, before committing to any identity.
- Write the paper's claim *conditionally* until the numbers land: the abstract's η² values must be the
  post-normalization values, not the current confounded ones (`PAPER_V2_OUTLINE.md` A abstract skeleton).
- Pre-register the three outcomes (survive / shrink / reverse) so a reversal reads as a real test, not a
  failure — this is also the P1-5 credibility asset (a refuted pre-registered prediction *raises*
  credibility).

---

## TENSION 2 — "Diagnose your own mechanism or be rejected" (L1) vs "your mechanism is refuted by your own repo" (L2)

**The pull.** L1's hard condition, from real review text, is that a null is welcome *only if it diagnoses
its own mechanism* (the GATS rejection). L2 shows the paper's current mechanism for Contribution 2 is
refuted by the authors' own `gradtune.py` (the collapse is a trust-region artifact on 3/4 tasks). So the
paper is caught between a bar it must clear and a control that says its current mechanism is wrong.

**Why it is not a contradiction.** The mechanism that survives is a *better* one: "the ensemble's gradient
collapse is a trust-region failure, and the LCB premise-coverage diagnostic *predicts which configurations
collapse*" (`FLAW_LEDGER.md` P0-0 fix option 1). That is a *predictive* diagnostic — strictly stronger than
"the mean is jagged," and it is exactly the "diagnose your own mechanism" the bar demands. The repo's
refutation is not a dead end; it points at the real mechanism.

**Engagement guidance for the draft.**
- Report the `gradtune` sweep in-body (it is critical material; AAAI reviewers are not required to read the
  supplement — `AAAI27_VENUE.md` C.5). Answering the reproducibility checklist honestly *requires* it (T7).
- Re-scope Contribution 2 from "surrogate geometry causes the collapse" to "the collapse is a trust-region
  failure the coverage diagnostic predicts." This makes the diagnostic (the paper's artifact) *predictive*,
  which is the strongest version of the "ship an artifact" rule (consensus claim 1, `03`).
- Frame the pre-registration refutation (P1-5) as evidence of a real test, not as HARKing.

---

## TENSION 3 — "N=7 is a fatal weakness" (L4/L5) vs "N=7 is the artifact" (L1/L5)

**The pull.** L4 and L5 treat N=7 as the paper's statistical soft underbelly: it can't rule out the
broken-oracles hypothesis, it sits below Demšar's N>10 threshold, and TOST needs ~N=30/condition. But L1
and L5's asset side say the *power specification for N=7* is precisely the shippable artifact that clears
the genre bar — the Yauney (ICLR 2026) and Agarwal (NeurIPS 2021) template turns "we found no difference"
into "here is the N required to detect one."

**Why it is not a contradiction.** The weakness and the artifact are the *same object* viewed twice. A bare
"p=0.69, no difference" is the fatal version; "p=0.69, and here is the power analysis showing why 7 tasks
cannot resolve a difference of this size, and how many are needed" is the asset version. The difference is
entirely in whether the paper *declares and quantifies* the limitation.

**Engagement guidance for the draft.**
- Make X4 (the power specification) a named, in-body deliverable — "the power spec *is* the artifact"
  (`VENUE_NORMS.md`). Cite Yauney for task-axis power-as-headline and Agarwal/rliable for the small-N
  toolkit (IQM, interval estimates, bootstrap).
- Declare the null explicitly and scope it to Design-Bench at N=7 (the ICLR 2026 "state it as such" datum).
- Pair the power spec with X11 (exact-oracle subset, L4) so the null is both *declared* and *controlled-for*.

---

## TENSION 4 — "The literature already owns most findings" (novelty) vs "the apparatus and the reversal are unowned" (contribution)

**The pull.** Across L2/L3, the paper's *findings* are heavily pre-owned: "ensembles perform poorly" and
"ranking is problem-dependent → tailored inductive biases" are ~90–95% owned by Li/Rudner/Wilson (ICLR
2024); the non-discrimination complaint is ~80% owned (Design-Bench, Kim survey); the smoothness axis is
pre-claimed (IGNITE, MS-DDEO). Yet L1's genre analysis says the paper can still land because the *apparatus*
(the de-confounded surrogate×optimizer factorial — NONE FOUND) and the *reversal* (η²_opt=0.01 contradicts
PGS's named belief) are unowned.

**Why it is not a contradiction.** In this genre, novelty of *findings* is not the currency — novelty of
*method-of-measurement* and a *named-belief reversal* are (Musgrave cites the genre to legitimize the
genre; every accepted instance re-derives a "known" result under control and the contribution is the
control). The paper should *concede and cite* the owned findings rather than claim them, and spend its
novelty budget on the apparatus + the reversal.

**Engagement guidance for the draft.**
- Cite Li/Rudner/Wilson early and honestly as prior work that found "ensembles lose" and "ranking is
  problem-dependent"; position the contribution as *the controlled decomposition that isolates why*, and as
  the *contradiction* of its calibration mechanism (`NOVELTY_V2.md` Identity A verdict).
- Cite the Kim survey to convert the pre-owned attribution gap from a threat into stated motivation.
- Lead with the reversal against PGS (AAAI 2024) as the "named belief, refuted" slot — but only after X1+X3
  earn η²_opt=0.01 (Tension 1). Keep the "first controlled surrogate×optimizer factorial in offline MBO"
  claim in its narrow, defensible form; drop any unqualified "first controlled decomposition."

---

## Net reconciliation for the draft

The four tensions collapse to one operating principle: **every one of the paper's live risks is resolved by
the same two moves — run X1+X3, and declare/scope honestly.** The re-run decides the headline, the
mechanism, and the reversal simultaneously (Tension 1); the honest disclosure of `gradtune` and the
pre-registration converts the repo's self-refutation into the predictive diagnostic the genre demands
(Tension 2); declaring and quantifying N=7 converts the statistical weakness into the shippable artifact
(Tension 3); and conceding owned findings while claiming the apparatus + reversal spends the novelty budget
where it is unowned (Tension 4). The paper that does these is Identity C (or, if the deadline forbids the
full re-run, a declared Identity E). The paper that does none of them is an unrepaired Identity A that
draws the GATS rejection.
