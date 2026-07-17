# 07 · Source tensions — expert disagreements, verbatim

**Step 7 of the research core.** Explicit disagreements between named sources, quoted verbatim where the
quote was verified (fetched this session, or carried from a repo doc that fetched and grepped it). This is
the highest-fidelity evidence layer: it shows where experts actually disagree, in their own words.

**Scope honesty.** Quotes marked **[fetched]** were read this session from the primary source (arXiv
abstract, PMLR page, or venue page). Quotes marked **[repo-doc, verified]** are carried from
`VENUE_NORMS.md` / `NOVELTY_V2.md` / `FLAW_LEDGER.md`, which recovered them from primary text and, per
those docs' fabrication-guard discipline, grepped the PDFs. AAAI reviews are private, so all *reviewer*
quotes are an ICLR/NeurIPS proxy (flagged). Where a quote could not be verified verbatim it is paraphrased
and labeled **[paraphrase]**.

---

## TENSION A — Are deep ensembles good uncertainty models? (surrogate axis)

**Lakshminarayanan, Pritzel, Blundell (NeurIPS 2017) — "strong":** deep ensembles produce
"well-calibrated uncertainty estimates … outperforming approximate Bayesian methods such as Monte Carlo
dropout." **[fetched, paraphrase of abstract]**

**Li, Rudner, Wilson (ICLR 2024) — "weak for BO":**
> "(i) the ranking of methods is highly problem dependent, suggesting the need for tailored inductive
> biases; … (iv) deep ensembles perform relatively poorly; (v) infinite-width BNNs are particularly
> promising, especially in high dimensions." **[fetched, verbatim abstract]**

**Abe, Buchanan, Pleiss, Zemel, Cunningham (NeurIPS 2022) — "gains are capacity, not ensembling":**
> ensemble improvements and single-larger-model improvements have "a Pearson's correlation of 0.81 on the
> in-distribution test set … preserved even on out-of-distribution data (Pearson's correlation: 0.76)";
> "ensemble diversity … does not meaningfully contribute to an ensemble's ability to detect
> out-of-distribution data." **[fetched, verbatim from search-of-primary]**

**What the disagreement means for the paper.** The pro-ensemble pole (Lakshminarayanan) makes "your
ensemble is a strawman" a free reviewer objection; the anti-ensemble pole (Li/Rudner/Wilson, Abe) supports
the paper's *finding direction* — but only if the ensemble is built fairly. The paper currently sits on the
wrong side: raw targets, no validation split, σ unfloored (`FLAW_LEDGER.md` P1-3), which makes
Lakshminarayanan's pole the reject route. The paper must cite Li/Rudner/Wilson and Abe to *earn* the
finding, after fixing P0-2.

---

## TENSION B — Is the optimizer or the surrogate the neglected axis? (experiment axis)

**Chemingui, Deshwal, Hoang, Doppa — PGS (AAAI 2024) — "the optimizer/search is neglected":**
> "Prior approaches … have primarily focused on learning robust surrogate models. However, their search
> strategies are derived from the surrogate model rather than the actual offline data. To fill this
> important gap, we introduce a new learning-to-search perspective." **[repo-doc: NOVELTY_V2, verified]**

**The paper — "the optimizer barely matters":** η²_opt = 0.01 vs η²_surr = 0.37 — "the field has been
innovating on the axis that does not matter" (`PAPER_V2_OUTLINE.md`).

**What the disagreement means.** This is the paper's sharpest offensive move: a *named, falsifiable belief
held at the target venue* that the data contradicts. It is also the paper's biggest exposure — PGS's authors
may review AAAI-27. And it is currently unearned: η²_opt=0.01 comes from a grid where optimizers had
unequal oracle budgets (256 vs 128) and unequal surrogate-query budgets (6×–59×) (`FLAW_LEDGER.md`
P0-1/P1-1). Engage PGS directly, and only claim the reversal after matched-budget X3.

---

## TENSION C — What does a null/measurement paper need to be accepted? (venue axis, ICLR/NeurIPS proxy)

**The GATS reviewers (ICLR 2019, REJECTED) — "praise, then reject for no mechanism":**
> R1: "I think publishing negative research results is very important … *if we can learn from those
> results*. But … they do not provide a thorough investigation of the causes which make GATS 'fail'."
> META-REVIEW: "The concern that most strongly affected the final evaluation is the limited insight (and
> evidence) of the factors that influence performance." **[repo-doc: VENUE_NORMS, verified from OpenReview]**

**The GANs reviewer (NeurIPS 2018, ACCEPTED) — "expected conclusion, accepted anyway":**
> "the main conclusion of the paper is expected (that there is really no model that is clearly better than
> others …), but not very helpful for the practitioner." **[repo-doc: VENUE_NORMS, verified]**

**ICLR 2026 reviewer (QIJk2xjJI3) — "a null is fine if declared":**
> "is the purpose of the paper to display a null result (which I think is not an issue, but it should be
> stated as such)?" **[repo-doc: VENUE_NORMS, verified from OpenReview]**

**What the disagreement means.** The three converge, not conflict: a null is publishable (GANs, ICLR 2026)
*iff* it declares itself and diagnoses its mechanism (GATS is the counter-example — praised, undiagnosed,
rejected). The paper's job is to be the GANs/declared case, not the GATS case. This is the entire A-vs-C
decision.

---

## TENSION D — Is the mean-rank / CD procedure the right benchmark statistic? (statistics axis)

**A NeurIPS 2025 reviewer (RCeZ063p33) — "use exactly this procedure":**
> "consider following Demšar (2006) by first performing a Friedman test and then applying a Wilcoxon signed
> rank post hoc test with Holm adjustment … visualized with a Critical Difference diagram."
> **[repo-doc: VENUE_NORMS, verified from OpenReview]**

**Benavoli, Corani, Mangili (JMLR 2016) — "the mean-rank post-hoc test is inconsistent, don't use it":**
> "the outcome of the mean-ranks test depends on the pool of algorithms originally included … the
> difference between A and B could be declared significant if the pool comprises algorithms C, D, E and not
> significant if the pool comprises algorithms F, G, H … we suggest instead to perform the multiple
> comparison using a test whose outcome only depends on the two algorithms being compared, such as the
> sign-test or the Wilcoxon signed-rank test." **[fetched, verbatim abstract]**

**What the disagreement means.** Both are right and the paper is caught in the middle: reviewers *want* the
CD apparatus (Asset 1), but the paper's CD matrix silently pools 11 cells including undefined
`ens_conformal:*` arms, so Benavoli's objection is *instantiated*, not hypothetical (`FLAW_LEDGER.md` P1-2).
The fix satisfies both poles: keep the CD diagram, unify the pool, and add per-pair Wilcoxon/sign tests.

---

## TENSION E — Is a small number of tasks/runs enough for a benchmark claim? (statistics axis)

**Agarwal et al. (NeurIPS 2021) — "point estimates over few runs mislead":**
> most RL benchmark results "compare point estimates of aggregate performance such as mean and median
> scores across tasks, ignoring the statistical uncertainty implied by the use of a finite number of
> training runs"; advocates "interval estimates … performance profiles … interquartile mean." **[fetched,
> paraphrase+verbatim of abstract]**

**An accepted-paper reviewer on small corpora (ICLR 2018, *State of the Art of Evaluation in NLMs*):**
> "the corpus the authors choose are quite small, the variance of the estimate will be quite high, I
> suspect whether the same conclusions could be drawn." **[repo-doc: VENUE_NORMS, verified]**

**Demšar (2006) — the field's own threshold (paraphrase):** the recommended regime for Friedman+CD is
N > 10 datasets and k > 5 methods; the paper's N=7 sits below it (`PAPER_V2_OUTLINE.md`). **[repo-doc]**

**What the disagreement means.** These *agree* that N=7 is under-powered — the tension is between the paper's
current silent point-estimate presentation and the field's demand for interval estimates + a power spec.
The resolution (Tension 3 in 06) is to convert N=7 from a hidden weakness into the declared artifact.

---

## TENSION F — Is the confound already known, or is naming it a contribution? (novelty axis)

**Kim et al. survey (TMLR) — "the attribution gap is a known open problem":**
> gains may stem from "superior surrogate modeling, improved optimization strategies, or mere chance."
> **[repo-doc: NOVELTY_V2, verified]** (survey confirmed fetched this session: TMLR, 20 cites.)

**Design-Bench (Trabucco et al., ICML 2022) — "simple baselines are competitive":**
> "The comparatively high efficacy of even simple baselines such as CMA-ES and naïve gradient ascent
> suggests the need for careful tuning and standardization." **[fetched, verified from search-of-primary]**

**The paper — "we run the controlled measurement the survey only named."**

**What the disagreement means.** The survey and Design-Bench *name* the paper's motivation almost verbatim
— which is a threat to novelty-of-question but a gift to framing. The paper answers a stated open problem
rather than posing a new one; cite both early to convert the pre-ownership into motivation (`NOVELTY_V2.md`
A5/A6).

---

## Orphan tension (did not surface as a locus but matters)

**On the propositions.** `proofs.md` concedes Prop 1's proof is a one-line identity ("the two events
coincide as subsets of X") and Prop 2 restates Tibshirani et al. 2019's weighted conformal without
implementing the reweight (`FLAW_LEDGER.md` P1-7). The corpus's two conformal-analogue papers are
"rating-3 rejects on straightforward application" (`VENUE_NORMS.md` Caution 2). **Tension:** the paper
numbers these as Propositions, inviting a comparison they cannot win, while a UQ reviewer reads them as
padding. Resolution: demote to a cited lemma/remark (Locatello's "(perhaps unsurprisingly)" self-deprecation
move).
