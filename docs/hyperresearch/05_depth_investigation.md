# 05 · Depth investigation — committed positions per locus

**Step 5 of the research core.** Each of the five loci from 04 investigated against the fetched corpus (02)
and the already-grounded repo docs, ending in one **Committed Position** — a defensible judgment the draft
can build on, stated with its uncertainty.

**Scope honesty.** A full pipeline spawns one depth-investigator subagent per locus with an independent
fetch budget. Here the investigation is inline; where a locus needed a fetch the corpus did not already
cover, that is flagged as an open fetch (carried to 08). Committed Positions are argued, not hedged into
mush — but each states what would overturn it.

---

## L2 (highest budget) — Is the ensemble-crippling objection fatal, or answerable?

**Evidence.**
- The confound is real and specific: `mbo.py:36-37` trains the ensemble on raw `y`; `mbo.py:255` and
  `mbo.py:311-312` z-score for both GPs. Targets span ~2.5 orders of magnitude across the suite (Griewank
  ≈ −2600, Branin ≈ −10). At fixed lr and 35 unconditional epochs with no target normalization, the
  ensemble's MSE on Griewank is ~10⁶ and it cannot fit (`FLAW_LEDGER.md` P0-2). The GP−ensemble gap should
  therefore track task |y| scale — which is what Table 1 shows.
- The baseline is additionally weak on every standard axis: `weight_decay=1e-4` is the *entire*
  regularization list, no validation split, no early stopping, σ unfloored, members differ only by seed
  (no bootstrap) (`FLAW_LEDGER.md` P1-3). Held-out NLL/RMSE per surrogate is **MISSING**.
- The literature makes "ensemble is a strawman" a *free* objection: Lakshminarayanan et al. (NeurIPS 2017)
  established ensembles as strong, often-better-than-Bayesian UQ baselines (fetched). A reviewer's default
  prior is that a properly-built ensemble is competitive.
- **But** the literature also supports the finding's *direction* once the baseline is fair: Li/Rudner/Wilson
  (ICLR 2024, fetched) find "deep ensembles perform relatively poorly" for BO; Abe et al. (NeurIPS 2022,
  fetched) find ensemble gains are capacity effects a single larger model replicates. So "a fair ensemble
  still loses to a GP at low dim" is a *plausible and literature-supported* outcome — the paper just hasn't
  earned it yet.
- The optimizer half is symmetric: `gradtune.py` shows a `trust=0.1` region closes the ensemble×gradient
  collapse on 3/4 tasks (`FLAW_LEDGER.md` P0-0), and budgets are unmatched 6×–59× (P1-1). So η²_opt=0.01 is
  also unearned until X1+X3.

**Committed Position.** *The objection is answerable, not fatal — but only by running the experiment, and
the honest expected outcome is a weaker headline.* Normalizing the ensemble's targets, equalizing the
candidate protocol (128 proposals, one selection rule, no oracle-selected reporting set), and tuning the
gradient optimizer is under a day of edits plus one grid re-run. Three outcomes, all publishable: (a)
η²_surr survives → the paper's central claim is established *far more strongly* than now, and the "fair
ensemble still loses" framing (Li/Rudner/Wilson-supported) becomes a genuine finding; (b) η²_surr shrinks
but survives → re-scope to a smaller, honest effect; (c) η²_surr evaporates → the finding reverses, which
is itself a paper (and better learned in week one than in review). **What would overturn this position:**
if the re-run showed η²_surr survives *and* η²_opt stays ≈0.01 under matched budgets, the "crippling"
objection would be fully defused rather than merely answerable. Until the run exists, treat the headline as
**confounded, not established.** This is the critical path; nothing else in the paper is trustworthy before
it (`FLAW_LEDGER.md`).

---

## L1 (high budget) — Does AAAI reward a benchmark-validity / measurement finding, and under what conditions?

**Evidence.**
- Four AAAI main-track precedents with no new method: Henderson (AAAI 2018, ~2,397 cites — pure
  measurement + taxonomy), Gundersen & Kjensmo (AAAI 2018 — counting things about 400 papers), Kim (AAAI
  2022 — null + PA%K protocol), Zeng (AAAI 2023 oral — "we question the validity of this line of research")
  (`VENUE_NORMS.md`). AAAI's *written* guidance presumes SOTA framing and has no negative-results track, but
  precedent, not guidance, sets the bar (`AAAI27_VENUE.md`; the earlier "AAAI is the worst fit" claim is
  retracted).
- The condition is sharp and comes from real review text (ASAP-Review ICLR corpus, an AAAI proxy): "a null
  is welcome only if it diagnoses its own mechanism." The GATS paper (ICLR 2019) was *praised by all three
  reviewers and the AC for doing negative results* and still rejected for "limited insight … of the factors
  that influence performance" (`VENUE_NORMS.md`). Accepted nulls (*Rethinking Pruning*, Melis, GANs) share
  scope discipline + an explained mechanism + guarded claims + a shipped artifact.
- NeurIPS 2026's new Negative Results contribution type sets an *explicitly higher* bar and requires
  surprise (fetched) — evidence the field is formalizing exactly this condition. AAAI has no such track, so
  the paper must self-supply the framing.
- The AAAI-27 mechanics are constraining but navigable: 7 body pages, reviewers not required to read the
  supplement, a reviewer-scored reproducibility checklist (`AAAI27_VENUE.md` C.4–C.5). The
  benchmark-validity keyword exists literally: **ML: Evaluation, Benchmarking, Datasets & Analysis**.

**Committed Position.** *AAAI-27 will reward this paper's genre — conditional on three things the current
draft does not yet have: (1) a declared null, (2) a diagnosed mechanism (not a hollow one refuted by the
repo's own control), and (3) a shipped artifact/protocol.* The venue is viable and the primary keyword is
unambiguous. The binding risk is not "wrong genre for AAAI" but "right genre, mechanism hollowed out by
P0-0" — which draws the exact GATS rejection. **What would overturn this:** if the P0-0/P0-2 re-runs cannot
complete before 2026-07-28, the honest fallback is Identity E (declare the reversal, ship the diagnostic)
or a TMLR/MLRC route (`PAPER_V2_OUTLINE.md`) — not forcing an unrepaired Identity A through AAAI main.

---

## L3 (high budget) — Is the smooth-mean / inductive-bias mechanism a contribution or a restatement?

**Evidence.**
- The *finding* that surrogate smoothness helps offline optimization is established: IGNITE (NeurIPS 2024)
  regularizes toward smoothness with a provable generalization bound; MS-DDEO (SWEVO 2022) selects a
  surrogate pool *by smoothness*; RoMA (NeurIPS 2021) is in the same axis (`NOVELTY_V2.md` C1, ~50–60%
  owned).
- The *competing mechanism* for "ensembles lose" is calibration/diversity, not mean smoothness:
  Li/Rudner/Wilson (ICLR 2024, fetched) attribute ranking differences to inductive bias broadly and their
  ensemble result to poor approximate inference — a different story from "the mean is jagged." This
  contradiction is the paper's asset (it is unclaimed) *and* its risk (a UQ reviewer may prefer the
  calibration story).
- The genuinely novel move is C2: bidirectional manipulation (smooth the ensemble → gap closes; roughen
  the GP → GP collapses, a *risked prediction*) plus a smoothness continuum reproducing the DB null as a
  limit point — **NONE FOUND** (`NOVELTY_V2.md` C2, the single most novel item in the paper).
- **Open fetch (flagged):** the NTK / spectral-bias grounding (wide nets are biased toward low-frequency
  functions; the relation to a GP prior) was *not fetched fresh this session*. The mechanism claim leans on
  it but is currently carried only at the IGNITE/MS-DDEO level. This is the highest-value missing citation
  (carried to 08).

**Committed Position.** *The mechanism is a contribution only in its narrow, correctly-scoped form —
"the GP's advantage is attributable to posterior-**mean** smoothness rather than calibration, shown by
bidirectional manipulation" — and it is empirically at risk from P0-2.* The bidirectional-manipulation
identification (C2) is the paper's strongest novel move and clears the "diagnose your own mechanism" bar
(L1). But it must (a) be scoped narrowly (the smoothness *axis* is pre-claimed — do not claim "smoothness
helps offline MBO" as new), (b) foreground the contradiction with Li/Rudner/Wilson's calibration story as
the *point of novelty*, and (c) survive the P0-2 re-run, because unnormalized targets are an alternative
explanation for the same manipulation result. **What would overturn this:** if smoothing the (normalized)
ensemble does *not* close the gap after X1, the mechanism is wrong and C collapses to A.

---

## L4 (medium budget) — Can the paper survive the broken-oracles competing explanation?

**Evidence.**
- The competing hypothesis is real, standard, and free: reviewers already believe Design-Bench oracles are
  broken (`VENUE_NORMS.md`), and the paper *hands them the ammunition* by substituting RF oracles on 5/7 DB
  tasks (`FLAW_LEDGER.md` T4, `db_tasks.py:22`). N=7 cannot statistically distinguish "prior mismatch" from
  "broken oracles."
- Two of the seven DB tasks are ones Design-Bench's authors excluded as non-discriminative, so p=0.69 is
  partly circular (`PAPER_V2_OUTLINE.md`); and the DB "in-distribution" coverage is measured off the data
  manifold — `uniform(0,1)` reference vs one-hot vertices (`FLAW_LEDGER.md` P0-5).
- The counter is cheap and reuses the grid (X11, `VENUE_NORMS.md`): show the null survives on the
  exact-oracle subset (TF-Bind-8/10, the only two DB tasks with exact oracles) or report the oracle noise
  floor against the effect size. Near-zero CPU.

**Committed Position.** *Contribution 3 is salvageable but only as a controlled-for claim, never as an
unqualified one.* The paper must (a) run X11 (exact-oracle subset), (b) re-run on the canonical DB set or
make the task-selection effect an explicit argument, (c) fix the off-manifold reference set (P0-5), and
(d) fix the arithmetically-backwards RF-defense sentence (P0-7). With those, "we cannot resolve method
differences on Design-Bench, and here is the power required to" becomes an *asset* (the Yauney/Agarwal
template). Without them it is the most likely reject route. **What would overturn this:** if the null does
*not* survive on the exact-oracle subset, the finding is an oracle artifact and Contribution 3 should be
cut, not defended.

---

## L5 (medium-low budget) — Is the statistics apparatus an asset or a liability?

**Evidence.**
- Asset side: reviewers *request* exactly this apparatus. NeurIPS 2025 reviewer RCeZ063p33 asked for
  "Demšar (2006) … Friedman … Wilcoxon signed rank … Holm … Critical Difference diagram" (`VENUE_NORMS.md`
  Asset 1) — which the repo already built.
- Liability side, each cheap to fix: the ANOVA is hand-rolled with no error term, `task` unmodeled, η² on
  63 cell means, no F/p/df (`FLAW_LEDGER.md` P1-2); η² is upward-biased vs ω², worse at small N (fetched);
  the CD matrix silently pools 11 cells, instantiating Benavoli's exact objection (fetched, JMLR 2016);
  N=7 sits below Demšar's own N>10, k>5 rule (`PAPER_V2_OUTLINE.md`); TOST needs ~N=30/condition and the
  paper has 7 tasks (`VENUE_NORMS.md` Asset 2); Agarwal et al. (NeurIPS 2021, fetched) prescribe interval
  estimates / IQM / bootstrap for exactly this small-N regime.
- The CIs the paper reports have no generating code (P0-4), and the two bootstraps in the repo resample
  tasks, not the seeds the text describes.

**Committed Position.** *The apparatus is a net asset once four cheap fixes land; as shipped it is a net
liability because its headline numbers (η² CIs) are not reproducible from the released code.* Minimal
defensible-stats package: (1) proper mixed model or permutation effect size, optionally ω², with F/p/df and
a real error term; (2) per-pair Wilcoxon/sign tests + Holm, and unify the pool to the defined cells
(defuses Benavoli); (3) IQM + task-and-seed bootstrap CIs (Agarwal) and *write the generator* (closes
P0-4/C10); (4) declare N=7 as below-threshold and report the power spec (turns the weakness into the Yauney
artifact). Lead with the CD apparatus; pre-empt Benavoli in the same breath. **What would overturn this:**
nothing in the evidence — this locus is low-uncertainty; the only risk is not doing the fixes.
