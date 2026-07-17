# 11 · Synthesis — one integrated acceptance finding

**Scope note.** Scoped synthesis of the acceptance-strategy finding for "Decomposing the GP Advantage
in Offline MBO" at AAAI-27, integrated from the three angles in `10_triple_draft.md` (reviewer-risk,
contribution-strength, venue-fit). Grounded in the repo evidence base and the live corner ground-truth
in `results/corners/`. The numbered research-core memos 02–09 were absent at read time; sources are
cited directly.

---

## The accept path

The three angles converge on one path, and they agree on its ordering.

**AAAI-27 will publish this genre.** The existential worry ("is a no-new-method measurement paper even
a paper here?") is answered: `VENUE_NORMS.md` documents four main-track precedents (Henderson AAAI-18,
Gundersen & Kjensmo AAAI-18, Kim AAAI-22, Zeng AAAI-23 oral). So acceptance is not gated on genre
legitimacy. It is gated on two things the reviewer corpus states explicitly and one the artifact
forces.

1. **A declared null with a diagnosed mechanism.** From the verbatim ICLR reviewer corpus
   (`VENUE_NORMS.md`), the repeated, cross-accept/reject bar is: *a null is welcome only if it
   diagnoses its own mechanism*, and claims must be *guarded/declared*. This selects **Identity C
   (mechanism — smoothness is the axis)** over Identity A (repaired measurement): A's mechanism
   section is exactly what `FLAW_LEDGER.md` P0-0 hollows out, so A draws the friendliest pool and
   still earns the GATS-style rejection. C is "not the ambitious option; it is the minimum."

2. **A de-confounded artifact.** `AAAI27_VENUE.md` C.4: the reproducibility checklist is
   reviewer-scored, and four items are unconditional-blocker P0s (P0-4 code-does-not-regenerate-numbers;
   P0-2 raw-vs-standardized targets; P0-1 inconsistent estimand; P0-0 the released sweep refutes the
   mechanism). These do not survive an argument; they need one grid re-run and ~1–2 days of edits.

3. **A shipped deliverable.** The genre's iron rule (`VENUE_NORMS.md`): *null + protocol/artifact is
   the unit of acceptance, never a bare null.* The deliverable is **X4 — the task-count power
   specification** (`EXTENSION_LEDGER.md`: NONE FOUND, closes a 20-year gap Demšar left open, costs
   zero CPU, and is the "deeper analysis" the bar demands), paired with the coverage diagnostic
   (Algorithm 1) as the mechanism's instrument.

**Mapped to the four axes the query names.** *Manuscript* — declare the null, correct the integrity
breaks (P0-6 Fig 1 vs Fig 3 disagree on 6/9 DB cells; P0-7 the backward "0.34 no smaller than 0.39"
sentence), and keep the "surrogate×optimizer" novelty qualifier while dropping the unqualified "first
controlled decomposition" (fANOVA owns the method, Li/Rudner/Wilson the findings — `NOVELTY_V2.md` D9).
*Experiments* — the X1/X3 de-confound, plus a budget-matched optimizer arm (P1-1; X3 equalizes the
oracle/candidate budget, not the surrogate-query budget) and the exact-oracle subset (X11).
*Statistics* — replace the hand-rolled, error-term-free ANOVA with a mixed model or permutation effect
size and unify the 9-vs-11-cell normalization (P1-2, Benavoli's pool objection instantiated).
*Artifact* — write the P0-4 generators so the reproducibility checklist can be signed honestly.

Concretely, the accept path is: **run X1+X3 as one grid, report X2 (gradtune), write the P0-4
generators, quarantine GFP (P0-5) and fix the backward sentence (P0-7)** → if η²_surr survives,
**commit to Identity C**, declare the null scoped to Design-Bench at N=7, foreground the reversal
(η²_surr=0.37 ≫ η²_opt=0.01) against the named PGS belief, ship X4 as the deliverable and the
exact-oracle-subset check (X11) as the answer to the "your oracles are broken" competing mechanism.
Route it `ML: Evaluation, Benchmarking, Datasets & Analysis`, minimal secondaries, everything
load-bearing in the 7-page body — which for Identity C means *cutting* to fit: the draft already
over-subscribes 7 pages (two grid tables, ANOVA table, controls table, an algorithm, two propositions,
six figures — `AAAI27_VENUE.md` C.5), so C must demote one grid table and Props 1/2 → lemma/remark
even as it adds the manipulation and interpolation content.

**The path has a live gate.** The corner ground-truth (`results/corners/analysis.json`) shows the
X1/X3 de-confounding grid is **PENDING**: the (on,on) camera corner reproduces the published headline
(η²_surr=0.369≈0.37, η²_opt=0.013≈0.01, η²_inter=0.165≈0.17, Friedman p=6.09e-05), but the X1-OFF
corner is only partial (20/63 cells) and the on_off / off_on corners are unrun. So *whether Identity C
is even available* has not yet been decided by the run that decides it. One yellow flag is visible
already: even in the X1-ON corner, ρ(gap, log|y|)=+0.536 — not the ~0 the X1 confound test predicts —
though at N=7 this is not significant (p=0.215) and the decisive contrast needs the off corners.

---

## The top 3 rejection risks

**Risk 1 — The artifact refutes the paper (P0-0), and the checklist makes reviewers look.**
This is `FLAW_LEDGER.md`'s own "single largest risk in this project": the released `gradtune.py`
fails its own pre-stated decision rule on 3/4 tasks, and `main.tex` never mentions it. Because AAAI-27
scores reproducibility on the submitted materials, "yes" on the code items is self-incriminating and
"no" is false. *Mitigation:* report gradtune (X2) and re-run with a tuned gradient optimizer;
unconditional, ~2 h to disclose.

**Risk 2 — The headline is confounded, so the mechanism (and the reversal) is unearned.**
P0-2 (ensemble on raw targets, GPs z-scored) makes η²_surr=0.37 observationally equivalent to a
target-scaling artifact; P0-1/P1-1 make η²_opt=0.01 a number measured under unequal oracle and
surrogate-query budgets, so the reversal framing ("optimizer doesn't matter") is not yet licensed.
*Mitigation:* X1+X3 in one grid re-run — currently PENDING. This is also the risk that can *kill*
Identity C outright (if the gap was target scaling).

**Risk 3 — The free competing mechanism on Contribution 3 (framing, not correctness).**
`VENUE_NORMS.md` central vulnerability: reviewers already believe Design-Bench oracles are broken, and
we substitute RF oracles on 5/7 tasks — a competing explanation for the synthetic→real gap that N=7
cannot rule out, costing the reviewer nothing to raise. Two of our seven DB tasks are ones
Design-Bench's authors excluded as non-discriminative, making p=0.69 partly circular
(`PAPER_V2_OUTLINE.md`). *Mitigation:* the exact-oracle-subset check (X11) + report the null on the
canonical five; near-zero CPU. Plus X4 answers "N=7 is too small" with a specification rather than an
apology.

**Runner-up (Contribution 3, a distinct route).** The COMs baseline reproduces at 2.21 vs official
0.99 on TF-Bind-8, and the paper quotes a third value (2.20); the one "matches official" number fails
to verify against its own row (`FLAW_LEDGER.md` P1-6; `DECISION_QUEUE.md` D7). "Their baselines are
wrong, so the null is theirs, not the field's" is a separate reject route. *Mitigation:* diff against
the official COMs hyperparameters (~1 day) or report the divergence openly against the published range.

---

## The single highest-leverage acceptance move

**Run the one de-confounding grid (X1 target-normalization + X3 protocol equalization) and report the
gradtune sweep (X2) alongside it.**

This single action is simultaneously (a) the removal of the top reject-driver P0-0 and the
confound-drivers P0-1/P0-2, (b) the unblock of three of the four unconditional reproducibility-checklist
failures (C2, C8, and — with the P0-4 generators folded into the same pass — C3/T7), and (c) the
decision that determines the paper's *identity* and whether the reversal framing is *earned*: if
η²_surr survives normalization it becomes the strongest control in the paper and Identity C is
available; if it evaporates, the honest finding is the opposite of the current draft *and* of PGS —
still a paper, but a different one. Every other acceptance lever (declare the null, foreground the
reversal, ship X4, choose secondaries, sign the checklist) is downstream of this run, which is why
the repo already treats it as the critical path (`DECISION_QUEUE.md` D1; `EXTENSION_LEDGER.md`
X1 "the best CPU in the repo") — and why its current **PENDING** status is the project's binding
constraint against the 2026-07-28 full-paper deadline.

Two caveats keep this honest. The run removes the *confounds*, but not the *statistics* reject-route
(P1-2, the hand-rolled ANOVA — a separate ~4 h fix) nor the *surrogate-query-budget* imbalance
(P1-1 — a separate budget-matched arm; X3 only equalizes the oracle/candidate budget). And it is not
the highest-leverage *free* move: **X4 (the power specification) is zero-CPU, identity-independent,
and should run in parallel now**, not wait on the grid.

**Conditional corollary — three-way, not one-way.** The run decides which paper exists.
**If η²_surr survives normalization → Identity C** (the reviewer-corpus minimum bar), paired with X4.
**If it survives but the mechanism cannot be re-established before the deadline → Identity A**, which
draws the friendliest pool and still risks the GATS "no mechanism" rejection — better routed to
**MLRC 2026** (official NeurIPS track via TMLR, deadline 2026-09-30, negative results welcome —
`VENUE_NORMS.md`) than forced through AAAI. **If η²_surr evaporates → Identity E** (the
reversal/self-demonstrating), the only identity for which the refuted pre-registration (P1-5) and
P0-0 are *assets* rather than fatal omissions (`AAAI27_VENUE.md` C.2). With ~11 days to 2026-07-28 and
the grid PENDING, **E is a live contingency, not a footnote** — it is the honest fallback if the run
cannot complete in time.
