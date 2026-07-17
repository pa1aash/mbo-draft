# 10 · Triple draft — three acceptance-strategy angles

**Scope.** This is the SYNTHESIS tail (steps 10–16) of a *scoped* hyperresearch pass. The "report"
these steps operate on is one finding: **what it takes for "Decomposing the GP Advantage in Offline
MBO" to be accepted at AAAI-27** across the four axes the query names — manuscript, experiments,
statistics, artifact. This is not a full 16-step multi-agent run; it is a synthesis over the repo's
existing evidence base (`FLAW_LEDGER.md`, `VENUE_NORMS.md`, `NOVELTY_V2.md`, `AAAI27_VENUE.md`,
`PAPER_V2_OUTLINE.md`, `EXTENSION_LEDGER.md`, `DECISION_QUEUE.md`) plus the live corner ground-truth
in `results/corners/`. Of the numbered research-core memos (02–09) only `01_*` existed at read time;
the 02–09 files were being written in parallel and were **absent when these drafts were composed** —
so the drafts cite the source docs directly rather than the (missing) intermediate memos.

Three short drafts follow, each entering the acceptance question from a different door.

---

## Draft (i) — Reviewer-risk-first

Start from what gets this paper desk-rejected, then invert.

The dominant risk is not novelty and not correctness of the null — it is that **the released
artifact contains the evidence against the paper**. `FLAW_LEDGER.md` P0-0: `gradtune.py` is a sweep
whose stated purpose is to kill the "under-tuned optimizer" objection; it *fails its own decision
rule on 3 of 4 tasks* (a trust region moves Branin 15×), and the result is in the repo but absent
from `main.tex`. `AAAI27_VENUE.md` C.4 shows AAAI-27 makes the reproducibility checklist
**reviewer-scored**, and four items force a "no" or a self-incriminating "yes", each mapping to an
unconditional-blocker P0: T7/C3 (P0-4, released code does not regenerate its own numbers), C2 (P0-2,
the ensemble trains on raw targets spanning −2613…+36 while both GPs z-score), C8 (P0-1, the reported
percentile is not the same estimand across the optimizer axis). A reviewer who clones the repo
falsifies a "yes" in minutes.

So the accept path, risk-first, is a sequence of removals. **One de-confounding grid re-run**
(X1 normalize targets + X3 equalize the candidate/oracle protocol, done in a single pass) closes
P0-2, P0-1, C2, and C8 at once and de-confounds the η² headline. **Reporting the gradtune sweep**
(X2, zero CPU) closes P0-0 and re-scopes the mechanism into something sharper (the collapse is a
trust-region failure). **Writing the missing generators** (P0-4, ~4 h) lets the checklist be signed
honestly and reconciles Fig 1 vs Fig 3 (P0-6). **Quarantining GFP** (P0-5) and **fixing the backward
sentence** (P0-7) remove two more reject-drivers for a few hours each.

The residual risk after all removals is the one no edit fixes: `VENUE_NORMS.md` documents that across
~600 real reviews, **every measurement-paper rejection died on contribution framing** ("so what",
"confirms what's known"), and reviewers already believe Design-Bench's oracles are broken — a free
competing explanation for our synthetic→real gap that N=7 cannot rule out. The cheap answer is the
exact-oracle-subset check (X11: run the null on TF-Bind-8/-10, the only exact-oracle DB tasks),
which converts "your oracles are broken" from fatal to controlled-for.

**Risk-first verdict:** the paper is un-submittable today and becomes submittable after one grid
re-run plus ~1–2 days of edits. The gate is compute, not argument.

---

## Draft (ii) — Contribution-strength-first

Start from what is genuinely strong and defend forward.

Three assets survive adversarial scrutiny. **First, the apparatus is novel.** `NOVELTY_V2.md` returns
a clean NONE FOUND for the crossed surrogate×optimizer factorial in offline MBO across Semantic
Scholar, Consensus, and WebSearch; the three nearest works (Li/Rudner/Wilson fix the acquisition;
Tan et al. and Chemingui vary one axis as a proposed method) each verifiably do *not* run the cross.
Apparatus claims are the cleanest to defend because they are checkable by inspection.

**Second, there is a reversal, and the draft under-uses it.** `PAPER_V2_OUTLINE.md`: η²_surrogate=0.37
vs η²_optimizer=0.01 is not "no difference" — it is *the field has been innovating on the axis that
does not matter*, and there is a named target at the venue (PGS, AAAI 2024, whose premise is that the
search strategy is the neglected axis). That is the "named belief, refuted" slot every accepted paper
in this genre fills (`VENUE_NORMS.md`: Recht, Melis, Dacrema, Musgrave).

**Third, X4 is a contribution, not a caveat.** `EXTENSION_LEDGER.md`: the task-count power axis is
NONE FOUND — Demšar (JMLR 2006), the exact paper the CD diagram cites, *observed* the underpower and
never turned it into a sample-size analysis; nobody has in 20 years. The number already exists for
free (a perfect rule reaches d_z=0.71 where 0.81 is needed). It ships the reusable *thing* the genre
requires ("every accepted paper shipped an artifact").

The strongest single contribution is the **mechanism**: `NOVELTY_V2.md` marks C2 (bidirectional
smoothness manipulation — smooth the ensemble, roughen the GP) as the single most novel move in the
paper, and the smoothness-not-calibration attribution directly *contradicts* Li/Rudner/Wilson's
calibration story — an unclaimed contradiction that should be foregrounded.

**Strength-first verdict:** the accept path is Identity C (mechanism) — apparatus + reversal +
manipulation + X4 power spec. But every strength here is downstream of the same grid re-run: the
reversal is unearned while η²_opt is confounded, and C's mechanism is exactly what P0-2 might explain
away as target scaling.

---

## Draft (iii) — Venue-fit-first

Start from what AAAI-27 actually rewards.

`VENUE_NORMS.md` settles the existential worry: AAAI has published the no-new-method measurement genre
**four times on the ML technical track** — Henderson (AAAI-18), Gundersen & Kjensmo (AAAI-18), Kim
(AAAI-22), Zeng (AAAI-23 oral). The genre is not disqualified; it is under-signalled in the
guidelines, with the bar set by precedent (Henderson). `AAAI27_VENUE.md` C.2 fixes the routing:
**primary keyword `ML: Evaluation, Benchmarking, Datasets & Analysis`** for every identity, because
every deep-technical secondary (Bayesian Learning & UQ, Optimization for ML, SO: Evolutionary
Computation) summons a specialist who owns a P0/P1 flaw — the double-edged-sword rule instantiated.
Minimal secondaries; at most `ML: Data-Centric AI` once fixes land.

The decisive venue fact is the acceptance bar itself. `VENUE_NORMS.md`, from the verbatim ICLR
reviewer corpus (the GATS rejection and three more): **a null is welcome only if it diagnoses its own
mechanism.** All reviewers praised negative results, then rejected for "limited insight into the
factors that influence performance." This settles A vs C: Identity A (repaired measurement with a
hollowed-out mechanism section, because P0-0 guts it) *is* the paper that gets that rejection.
**Identity C is literally the bar these reviewers state — not the ambitious option, the minimum.**

Two more venue moves are free and load-bearing. **Declare the null** in the abstract, scoped to
Design-Bench at N=7 (`VENUE_NORMS.md`: an undeclared null reads as a study that found nothing; a
declared one is acceptable). **Never end on the negative** — close on the field's obligation, the
way every accepted abstract in the genre does. And honor the 7-page hard budget (`AAAI27_VENUE.md`
C.5): reviewers are *not required* to read the supplement, so the de-confounding evidence, the
re-run η², Algorithm 1, and the exact-oracle-subset check must live in the body.

**Venue-fit verdict:** AAAI-27 fits this genre and rewards Identity C specifically — but only a
version that (a) reports its mechanism, which requires the P0-0/P0-2 fixes, and (b) declares its null.
The venue's tolerance is real and conditional on exactly the fixes the risk-first draft named.
