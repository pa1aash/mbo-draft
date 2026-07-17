# 03 · Contradiction graph — where the evidence forks

**Step 3 of the research core.** Explicit opposing claims across the corpus, each with both poles cited,
ranked by **decision-impact** on the accept/reject question. These fights feed the loci analysis (04):
loci are placed where the evidence actually forks, not where intuition suggests.

**Scope honesty.** These are real contradictions in the literature and between the literature and the
artifact — not manufactured tension. Consensus claims (agreed across ≥3 sources) are listed last so the
draft can assert them without hedging.

Severity of decision-impact: **DI-0** decides accept/reject · **DI-1** decides a contribution's survival ·
**DI-2** shapes framing · **DI-3** background.

---

## FIGHT 1 — "A null/measurement paper is publishable at a top venue" vs "only if it diagnoses its own mechanism" · **DI-0**

- **Pole A (publishable):** AAAI has published the no-new-method measurement genre four times on the ML
  main track — Henderson AAAI 2018, Gundersen & Kjensmo AAAI 2018, Kim AAAI 2022, Zeng AAAI 2023 oral
  (`VENUE_NORMS.md`). NeurIPS 2018 accepted *Are GANs Created Equal?* over a reviewer's "main conclusion
  is expected … not very helpful for the practitioner" (`VENUE_NORMS.md`, public reviews).
- **Pole B (conditional):** across the ASAP-Review ICLR corpus, *every* measurement-paper rejection died
  on contribution framing, and the repeated bar is verbatim: "a null is welcome only if it diagnoses its
  own mechanism." The GATS paper (ICLR 2019, **rejected**) drew universal praise for doing negative
  results *and* was rejected because "the limited insight … of the factors that influence performance"
  (`VENUE_NORMS.md`).
- **Resolution / engagement:** not a true contradiction once scoped — both poles agree the *unit of
  acceptance is null + mechanism/artifact*, not the null. This is the paper's central gate. It maps onto
  the A-vs-C identity decision (`PAPER_V2_OUTLINE.md`): Identity A's mechanism section is hollowed out by
  `FLAW_LEDGER.md` P0-0, so A draws the GATS rejection; Identity C *is* the bar these reviewers state.
  **This fight is the reason C outranks A.**

---

## FIGHT 2 — "The ensemble×gradient collapse is surrogate geometry" vs "it is an untuned optimizer" · **DI-0**

- **Pole A (geometry, the paper's claim):** Contribution 2 / Figure 4 / Section 5 attribute the collapse
  to the ensemble's jagged posterior mean — a surrogate-class property.
- **Pole B (tuning, the repo's own control):** `gradtune.py` — released in the artifact — states its own
  decision rule ("if even the best-tuned gradient config still underperforms perturbation, the collapse is
  surrogate geometry") and **fails it on 3 of 4 tasks**: a single `trust=0.1` moves Branin 15× and
  Styblinski 6×; on Ackley plain gradient ascent already beats perturbation (`FLAW_LEDGER.md` P0-0). The
  string "trust" never appears in `main.tex`.
- **Resolution / engagement:** the artifact refutes the manuscript. This is not an outside objection; it
  is the authors' own pre-stated test, run, failed, unreported. It is a **DI-0 reject-driver** because a
  reviewer who opens the repo finds it. The only fix is to report it — re-scope to "the collapse is a
  *trust-region* failure the LCB diagnostic predicts." Corroborated by the field's own reviewer language:
  *Rethinking Pruning* (ICLR 2019) R1 asked the identical question on an accepted paper — "whether a
  carefully tuned learning rate … may get the same or better performance" (`VENUE_NORMS.md`).

---

## FIGHT 3 — "The GP advantage is smooth-mean inductive bias" vs "it is target-scaling / a crippled baseline" · **DI-0**

- **Pole A (inductive bias, the paper's mechanism):** η²_surr=0.37; the GP's smooth Matérn mean is the
  causal axis (Identity C).
- **Pole B (artifact):** the ensemble trains on **raw** targets spanning −2613…+36 while both GPs
  z-score (`FLAW_LEDGER.md` P0-2). "Inductive bias" and "the ensemble was handed unnormalized targets" are
  observationally equivalent under every control the paper runs; the β=0 and matched-tuning controls do
  not separate them.
- **Pole C (literature undercut of the premise):** even granting a fair ensemble, Li/Rudner/Wilson
  (ICLR 2024) attribute surrogate-ranking differences to **calibration/diversity**, not mean smoothness —
  a *different* mechanism for the same "ensembles lose" finding. And "surrogate smoothness helps offline
  optimization" is already established (IGNITE NeurIPS 2024; MS-DDEO SWEVO 2022), so the novel residual is
  only *attribution of the GP's edge to mean smoothness rather than calibration* (`NOVELTY_V2.md`).
- **Resolution / engagement:** **DI-0.** The headline number is confounded until P0-2 is fixed and re-run.
  The mechanism claim is simultaneously (i) empirically at risk from the artifact and (ii) novelty-narrow
  against the literature. This is the single most important experiment: normalize `y`, re-run, and see
  whether η²_surr survives (`FLAW_LEDGER.md`: "nothing else … until P0-2 is run").

---

## FIGHT 4 — "Deep ensembles are strong UQ baselines" vs "ensembles are poor surrogates / capacity-replaceable" · **DI-1**

- **Pole A (strong):** Lakshminarayanan et al. (NeurIPS 2017) — deep ensembles give well-calibrated
  uncertainty "often outperforming approximate Bayesian methods" (`02` E2). This is the reviewer's default
  prior, and it means "the ensemble is a strawman" is a *free* objection.
- **Pole B (weak/replaceable):** Li/Rudner/Wilson (ICLR 2024) — "deep ensembles perform relatively
  poorly" for BO; Abe et al. (NeurIPS 2022) — ensemble gains are replicable by a single larger model
  (Pearson 0.81 ID / 0.76 OOD), "diversity does not meaningfully contribute to OOD detection."
- **Resolution / engagement:** **DI-1** for the surrogate main effect. The literature is genuinely split,
  which *helps* the paper's finding direction (B supports "ensembles lose") — **but only if the ensemble
  is a fair baseline.** With P0-2 unfixed (raw targets, no validation split, σ unfloored — P1-3), Pole A
  becomes the reject route: "you built the strawman Lakshminarayanan warned against." The paper must move
  its ensemble from Pole-A-strawman to Pole-B-fair-and-still-loses.

---

## FIGHT 5 — "The optimizer is the neglected axis that matters" (PGS) vs "η²_opt = 0.01, the optimizer barely matters" · **DI-1**

- **Pole A (optimizer matters):** Chemingui et al., PGS (**AAAI 2024**) — "prior approaches have primarily
  focused on … robust surrogate models … we introduce a learning-to-search perspective" (`NOVELTY_V2.md`).
  A named, falsifiable belief held at the target venue.
- **Pole B (paper's reversal):** η²_opt = 0.01 — "the field has been innovating on the axis that does not
  matter" (`PAPER_V2_OUTLINE.md`).
- **Resolution / engagement:** this is the paper's *best offensive framing* (named belief → refuted) —
  **but it is currently unearned.** η²_opt=0.01 is itself confounded: grad/perturb get 256 oracle calls,
  CMA gets 128, three different selection rules (`FLAW_LEDGER.md` P0-1); surrogate-query budgets differ
  6×–59× (P1-1). You cannot claim "the optimizer doesn't matter" from a grid where optimizers never had
  equal budgets. **DI-1:** the reversal survives only if η²_opt stays ≈0.01 under matched budgets (X1+X3).

---

## FIGHT 6 — "Design-Bench measures offline-MBO progress" vs "Design-Bench cannot discriminate methods" · **DI-1**

- **Pole A (measures progress):** Design-Bench (ICML 2022) is the field's standard benchmark with a
  unified protocol.
- **Pole B (non-discriminative):** its own paper concedes CMA-ES is competitive on 4/8 tasks; the Kim
  survey says benchmarks "make it difficult to distinguish … more sophisticated algorithms"
  (`NOVELTY_V2.md` A6). The paper's Friedman p=0.69 on Design-Bench is a *measurement* of this.
- **Resolution / engagement:** the complaint is ~80% pre-owned (Pole B is near-consensus in the field).
  The paper's surviving contribution is the *paired omnibus measurement* (synthetic p=6e-5 → real p=0.69),
  not the observation. **But** two of the paper's seven DB tasks are ones Design-Bench's authors excluded
  as non-discriminative, so p=0.69 is partly circular (`PAPER_V2_OUTLINE.md`). Re-run on the canonical set
  or make the selection effect the argument.

---

## FIGHT 7 — "Broken Design-Bench oracles explain the synthetic→real gap" vs "prior–task smoothness mismatch explains it" · **DI-1**

- **Pole A (broken oracles, the reviewer's free move):** reviewers already believe Design-Bench oracles
  are broken; that is a competing explanation for the gap that "costs them nothing to raise and that N=7
  cannot rule out" (`VENUE_NORMS.md` central vulnerability). The paper *worsens* this by substituting RF
  oracles on 5 of 7 DB tasks (`FLAW_LEDGER.md` T4).
- **Pole B (smoothness mismatch, the paper's claim):** the gap reflects prior–task mismatch (Identity C).
- **Resolution / engagement:** **DI-1**, and "this is a framing problem, not a measurement problem." The
  cheap answer (X11): show the null survives on the exact-oracle subset (TF-Bind-8/10) or report the oracle
  noise floor against the effect size. Converts a fatal competing hypothesis into a controlled-for one.

---

## FIGHT 8 — "Friedman + Nemenyi CD is the right benchmark-stats procedure" vs "mean-rank CD is pool-dependent and misleading" · **DI-2**

- **Pole A (use CD):** NeurIPS 2025 reviewers explicitly *request* Demšar (2006) Friedman → Wilcoxon-Holm
  → CD diagram (`VENUE_NORMS.md` Asset 1) — the paper's apparatus is what reviewers want.
- **Pole B (CD is flawed here):** Benavoli et al. (JMLR 2016) — the mean-rank test's outcome "depends on
  the pool of algorithms originally included," and the paper's matrix silently pools 11 cells including
  undefined `ens_conformal:*` arms (`FLAW_LEDGER.md` P1-2). Recommends sign/Wilcoxon instead. Agarwal et
  al. (NeurIPS 2021) add: with a handful of samples, point/rank estimates mislead — use interval estimates.
- **Resolution / engagement:** **DI-2** — the paper should lead with the CD apparatus (Asset 1) *and*
  pre-empt Benavoli by fixing the pool and switching to per-pair tests + IQM/bootstrap CIs. Both poles are
  simultaneously true; the fix satisfies both.

---

## FIGHT 9 — "η² is the effect size to report" vs "η² is biased upward; report ω² / a proper model" · **DI-2**

- **Pole A:** η² is the standard ANOVA effect size and the paper's headline currency (0.37 / 0.01 / 0.17).
- **Pole B:** η² overestimates population effect size vs the less-biased ω², "particularly … smaller
  sample sizes" (`02` C5); and the paper's η² is hand-rolled on 63 cell means with `task` unmodeled, no
  error term, no F/p/df (`FLAW_LEDGER.md` P1-2).
- **Resolution / engagement:** **DI-2.** A UQ/stats reviewer reads η²-without-an-error-term as "not an
  effect size." Fix with a proper mixed model or permutation effect size; consider ω². Low cost, closes a
  clean attack.

---

## FIGHT 10 — "AAAI is a poor fit for null/measurement work" vs "AAAI has published this genre four times" · **DI-2**

- **Pole A (poor fit):** AAAI's written guidelines are silent on negative results, have no negative-results
  track, and presume SOTA framing (`VENUE_NORMS.md` table). An earlier session concluded AAAI was the
  worst fit.
- **Pole B (viable):** that conclusion was *retracted* — Henderson/Gundersen/Kim/Zeng are all AAAI main
  track (`VENUE_NORMS.md` correction). "Absence of an explicit welcome is not evidence of rejection — the
  bar is set by precedent."
- **Resolution / engagement:** **resolved in favor of Pole B** — AAAI is viable, gated on shipping an
  artifact and declaring the null. This is now a consensus within the repo docs, retained here only
  because it is the venue-choice premise of the whole dossier.

---

## Consensus claims (≥3 independent agreements — assert without hedging)

1. **The unit of acceptance for this genre is null + a reusable artifact/protocol/mechanism, never a bare
   null.** (Henderson, Kim AAAI'22, Musgrave, Recht, Dodge, Locatello — `VENUE_NORMS.md`.)
2. **Design-Bench's simple baselines are competitive / the benchmark under-discriminates.** (Design-Bench's
   own paper, Kim survey, and the paper's own p=0.69 — Fights 6.)
3. **Offline model/HP selection is a recognized open problem.** (Paine et al.; "When is Offline HP
   Selection Feasible?"; Design-Bench conclusion; Kim survey — `02` E5.)
4. **Unreported implementation details decide results in this genre.** (Henderson; Ferrari Dacrema's
   "confirmation bias"; Lucic's "tuning more than algorithmic changes" — and it is the paper's own
   P0-0/P0-2, one level up.)
5. **A null must be *declared* to be accepted; an undeclared null reads as a study that found nothing.**
   (ICLR 2026 reviewer QIJk2xjJI3; `VENUE_NORMS.md`.)

---

## Ranked for the loci analysis (04)

| Rank | Fight | DI | Why it earns a locus |
|---|---|---|---|
| 1 | F2 (collapse: geometry vs tuning) | DI-0 | Artifact refutes manuscript; unconditional reject-driver. |
| 2 | F3 (GP edge: smoothness vs scaling) | DI-0 | Headline η² confounded; gates every downstream number. |
| 3 | F1 (null publishable, conditionally) | DI-0 | Decides identity (A vs C) and the whole framing. |
| 4 | F5 (optimizer reversal, unearned) | DI-1 | The best offensive framing, gated on X1+X3. |
| 5 | F7 (broken oracles competing hypothesis) | DI-1 | Most likely reject route for Contribution 3; cheap to close. |
| 6 | F4 (ensemble strong vs weak) | DI-1 | Decides whether the surrogate effect reads as strawman or finding. |
| 7 | F8/F9 (stats: CD pool + η² bias) | DI-2 | Clean, citable, low-cost attack surface. |
