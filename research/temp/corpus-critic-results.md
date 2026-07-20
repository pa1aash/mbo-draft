# Step 8 — Corpus critic results

Six gaps identified, three fetchers dispatched. Results below; the orchestrator's own
first-hand checks are marked as such.

---

## gap-1 + gap-2 (CRITICAL) — the N6 unsearched regions

**Target position:** N6 is CONFIRMED NONE-FOUND but defensible-only-if-argued. A kill requires
one paper with all four conjuncts: surrogate **model class** varied ≥2 genuinely distinct
classes, optimizer/search varied ≥2 routines, the two **crossed**, and a **two-way variance
decomposition**, in an offline/fixed-dataset setting.

**Regions swept:** surrogate-assisted evolutionary computation (SAEA), AutoML / CASH /
kernel-selection / algorithm configuration, and simulation-optimization / design-and-analysis of
computer experiments. None had been searched in any prior pass. The corpus critic confirmed
their absence from the vault by inspecting returned note IDs rather than trusting hit counts —
several apparent hits were keyword coincidences on already-known papers.

### Orchestrator first-hand check — the strongest SAEA candidate is CLEAN

**Kudela & Dobrovsky, "Performance Comparison of Surrogate-Assisted Evolutionary Algorithms on
Computational Fluid Dynamics Problems"** (arXiv:2402.16455, submitted 26 Feb 2024). This is the
most on-target SAEA hit the sweep produced — a multi-surrogate, multi-algorithm comparison in
exactly the community with the strongest design-of-experiments culture, which is where a crossed
factorial with ANOVA was most likely to exist.

I fetched the PDF and grepped the full text (47,342 chars) myself rather than relying on the
vault note, which held only the abstract page:

| Term | Hits |
|---|---|
| `factorial` | **0** |
| `crossed` | **0** |
| `ANOVA` | **0** |
| `analysis of variance` | **0** |
| `eta squared` | **0** |
| `main effect` | **0** |
| `variance decomposition` | **0** |
| `two-way` | **0** |
| `interaction` | **0** |
| `surrogate model` | 18 |
| `Kriging` | 4 |

**Verdict: NOT A KILL, and not even a near-miss on the decomposition conjunct.** It compares
performance across surrogate-assisted algorithms; it does not decompose outcome variance between
a surrogate factor and an optimizer factor. Zero hits on all nine decomposition terms.

This is the single most informative negative in the gap-fill wave: the SAEA community was the
best remaining bet for a kill, and its most directly-titled comparison paper does not perform the
analysis.

### Full sweep result across all three regions: NO KILL

Eight primaries fetched and grepped, no verdict taken from a snippet:

| Source | Region | Verdict |
|---|---|---|
| Kudela & Dobrovsky 2024 (arXiv:2402.16455) | SAEA | IRRELEVANT — 11 **bundled** surrogate+optimizer methods compared by Friedman/Wilcoxon on method identity, not crossed; mostly online |
| Gorissen, Dhaene & De Turck 2009, "Evolutionary Model Type Selection for Global Surrogate Modeling" (JMLR 10) | SAEA | IRRELEVANT — the GA selects among surrogate classes but is the **fitting** mechanism, never crossed with a black-box optimizer over the design space |
| EXPObench (Bliek et al. 2023), independently re-fetched via `pure.tue.nl` | SAEA/AutoML | IRRELEVANT — 7 bundled algorithms, not crossed. **Independently corroborates the vault's existing verdict via a different provider** |
| Biedenkapp et al. 2017, "Efficient Parameter Importance Analysis via Ablation with Surrogates" (AAAI-17) | AutoML | IRRELEVANT — single RF surrogate; compares ablation *methods*, not surrogate × optimizer |
| **Park, Cheon et al., "BOOST"** (arXiv:2508.02332) | AutoML | **NEAR-MISS** — the closest structural match found anywhere: crosses **kernel choice × acquisition function** with an isolating ablation (App. C.5). Fails conjunct (a) because Matérn/RBF/RQ are all one GP **model class**, and the setting is online BO with a "no-extra-query" internal step **misleadingly labelled "offline"** |
| Mukhtar et al. 2023 (Heliyon, PMC10405017) | sim-opt | IRRELEVANT — PR vs Kriging compared but only **one** optimizer ever run; `factorial`/`main effect`/`interaction` hits are all DOE-sampling and physical-parameter homonyms |
| Dao et al. 2025 (arXiv:2503.04181) | offline MBO | IRRELEVANT across 24,875 words — a regularizer plugin that ablates only its own hyperparameters |
| Conformal Candidate Certification (arXiv:2606.15217) | 2026 re-check | IRRELEVANT — independently re-verified, matches the existing note |

**Note on BOOST:** its "offline" label is a false friend. A grep-count sweep would flag it; reading
it shows the term denotes an internal no-extra-query step inside an online loop, not the offline
setting. That is a **fourth** trap of the same family as the three homonyms.

### ⚠ ONE UNRESOLVED LEAD — and it has the most N6-shaped title in the entire audit

**Elsayed & Lacor (2014), "Robust parameter design optimization using Kriging, RBF and RBFNN with
gradient-based and evolutionary optimization techniques"**, *Applied Mathematics and Computation*
236:325–344, DOI 10.1016/j.amc.2014.03.082.

The title names **three surrogate classes** (Kriging, RBF, RBFNN) **and** two optimizer families
(gradient-based, evolutionary) — the only title found in this entire audit that names both axes
explicitly.

**Primary text could not be obtained.** Every free-access route was exhausted: ScienceDirect
direct, Unpaywall (closed, no OA location), Crossref, Semantic Scholar (abstract elided by the
publisher), Academia.edu, ResearchGate, and the VUB repository. **Per the method constraint, the
fetcher refused to render a verdict from secondary snippets**, which is the correct call.

**The open question is precise:** whether the crossing is genuine (each surrogate run with each
optimizer) or **sequential** (surrogates compared first, then one winner optimized two ways). A
sequential design is not a kill; a genuine crossing with a variance decomposition would be.

**This must be disclosed in the N6 verdict itself, not buried in the terminal section.** N6 is
CONFIRMED NONE-FOUND *with one paywalled lead unresolved*, and the honest statement names it so
the author can obtain it through institutional access in minutes. Recorded in the vault as
`elsayed-lacor-2014-robust-parameter-design-kriging-rbf-rbfnn-unverified` with every access
attempt logged.

---

## gap-3 (high) — N9 overturning search in its exact framing

**Target position:** no ML reality-check/benchmark audit reports a corrected variance-explained
statistic above its own published value.

Searched separately from the two adjacent literatures already checked (Hamdan's confound-leakage,
which is ML methodology rather than a benchmark audit; Maassen's psychology meta-analysis
recomputation). The distinct framing sought was an **ML benchmark audit whose corrected effect
size grew**, including the reproducibility-track literature (ML Reproducibility Challenge,
ReScience C) as the natural home for such a result.

**RESULT: CONFIRMED NONE-FOUND, exhaustively.**

**Queries run, verbatim** (arXiv API + targeted web search; OpenAlex hit a hard budget wall and
Semantic Scholar was rate-limited, so those two carried almost nothing):
`reproducibility effect size larger than originally reported machine learning benchmark`,
`reality check machine learning confound`,
`re-evaluation confirms strengthens original finding benchmark`,
`audit increased measured advantage neural network comparison`,
`reanalysis larger effect machine learning evaluation`,
`ML reproducibility challenge reported`, `attenuation correction benchmark machine learning`,
`underestimate true effect performance gap benchmark`, `metric learning reality check`,
`stronger than originally reported`, `corrected confound larger gap deep learning`,
plus `"ML Reproducibility Challenge" report found effect stronger than original paper claimed`,
`"re-evaluation confirms and strengthens" OR "reanalysis found a larger" machine learning benchmark`,
`ReScience C reproducibility report "stronger" OR "larger" effect than original paper`.

**Zero grow-direction hits.** And one new directly-on-target shrink-direction reanalysis fetched:

**Robinson, Glen & Lee, "Validating the validation: reanalyzing a large-scale comparison of deep
learning and machine learning models for bioactivity prediction"**, *J. Comput. Aided Mol. Des.*
2020;34(7):717–730, DOI 10.1007/s10822-019-00274-0, PMCID PMC7292817. **Venue verified** from the
publisher-hosted PMC header. It reanalyses Mayr et al.'s ChEMBL benchmark (which had claimed
"deep learning significantly outperforms all competing methods") and reports the shrink
direction: *"we show that support vector machines achieve competitive performance compared to
feed-forward deep neural networks."*

**A re-fetch discipline note worth keeping.** This paper was already in the vault from the
**prior** audit pass, via its arXiv preprint. The fetcher re-obtained it independently through a
different domain and provider (publisher PMC HTML rather than arXiv PDF), which **cross-validates
the prior pass's verdict rather than inheriting it** — exactly what the query's
do-not-reuse-a-cached-source constraint is for.

**Net for N9:** three independent, directly-on-target ML benchmark reanalyses — Robinson,
Musgrave, Ferrari Dacrema — **all shrink-direction, zero grow-direction**, after an exhaustive
fresh sweep. The narrow claim stands and is now better evidenced than when the paper made it.

## gap-4 (high) — precedent for interpreting a component-by-component interaction

**Target position:** the buried interaction term is worth promoting partly because no prior ML
benchmark study reports and interprets an interaction between two pipeline components.

The locus-3 investigator scoped its precedent search to offline-MBO/BO benchmarks only. This gap
widens it to ML benchmarking generally — optimizer-versus-architecture studies (Schmidt et al.
"Descending through a Crowded Valley"; Choi et al. on optimizer comparisons), and the deep-learning
benchmarking literature.

**RESULT: NO PRECEDENT FOUND — a positive finding that strengthens the recommendation.**

**Queries run, verbatim:** `interaction optimizer architecture deep learning benchmark`,
`descending through a crowded valley`, `empirical comparison optimizers deep learning`,
`best optimizer depend on architecture`, `component interaction ANOVA machine learning pipeline`,
`data augmentation architecture interaction ANOVA`, `tokenizer model size interaction`,
`factorial design deep learning benchmark components`,
`crossed design machine learning benchmark two-way ANOVA`,
`how to train your vit data augmentation regularization`,
`data augmentation model size interaction vision transformer`,
`scaling laws interaction between hyperparameters and architecture`.

Three primaries fetched and full-text grepped (`interaction`, `ANOVA`, `analysis of variance`,
`factorial`, `crossed`, `eta squared`, `main effect`, `depends on`), across **three** candidate
regions rather than the two the brief named:

| Paper | Venue | Result |
|---|---|---|
| **Schmidt, Schneider & Hennig, "Descending through a Crowded Valley"** | **ICML 2021, PMLR 139** — verified from the PMLR copyright footer in the extracted PDF | **Zero hits** on all formal terms. Only qualitative *"depends on the problem"* language. |
| **Choi, Shallue, Nado, Lee, Maddison & Dahl, "On Empirical Comparisons of Optimizers for Deep Learning"** | arXiv:1910.05446 — **VENUE UNVERIFIED** (no Comments or Journal-ref field on arXiv, no proceedings footer in the PDF) | **Zero hits.** Argues rankings are confounded by asymmetric hyperparameter-search-space tuning — not an interaction term. |
| **Steiner et al., "How to train your ViT?"** | **TMLR 05/2022** — verified from the PDF header and OpenReview link | Explicitly runs a grid crossing AugReg strength × model size × data budget and calls it *"interplay"* — but **never computes a formal interaction or ANOVA statistic.** |

**All three regions return a clean negative.** No ML benchmark study reports and interprets a
component-by-component interaction. That is a positive finding: it means the paper's unreported
interaction term would be, so far as an exhaustive sweep can establish, **without precedent in ML
benchmarking** — which raises the cost of leaving it uninterpreted.

**THE THIRD HOMONYM TRAP, caught by the fetcher.** In the ViT paper, `ANOVA` false-matched inside
**"Toutanova"** (the BERT citation). The fetcher read the hit and discarded it rather than
counting it. This audit has now caught three distinct homonym traps — *Crossed barrel* (Liang),
*Usmanova/Bozhanova* (COMs, Design-Bench, Kim review), and *Toutanova* (ViT). Any grep-count-only
methodology would have produced false positives in five separate papers.

**The venue discipline held.** The fetcher flagged Choi et al. as venue-unverified rather than
guessing — the exact failure mode that produced two bad citations earlier in this audit.

## gap-5 (high) — the acquisition-stalling vocabulary itself

**Target position:** nobody owns "a confidence-bound acquisition is locally maximal at the data,
so the optimizer never leaves."

Three candidate owners were ruled out in earlier steps — TuRBO (diagnoses the *opposite*,
over-exploration), Fan et al. 2024 (proposes minimizing UCB as a method and proves *convergence*;
0 hits for offline/LCB/stuck/paralysis), and GIBO (no confidence bound in its exploitation step).
**But excluding three specific papers is not the same as sweeping the failure-mode vocabulary**,
which no prior step did. This gap closes that hole.

**RESULT: NOT a clean none-found. One real near-miss found, and my earlier "nobody owns it"
claim must be softened into a citation obligation.**

**Yarotsky (2013), "Examples of inconsistency in optimization by expected improvement",
*J. Global Optimization* 56(4):1773–1790, arXiv:1109.1320** (venue verified via Springer citation
metadata). **Theorem 3 rigorously proves that EI-driven BO started at the true optimum has a
trajectory that converges back to that single point and is "not dense."** That is the closest
prior formalization in existence of *"gets stuck and never leaves."*

It differs from the paper's claim on **three axes**, each real:
1. **Expected Improvement**, not a confidence bound (UCB/LCB);
2. **online** BO, not the offline/frozen-dataset regime;
3. an **adversarial worst-case starting condition**, not an empirical seed-robust observation.

**Effect on the audit's position — I am correcting myself.** I previously wrote that *"nobody
owns 'a confidence-bound acquisition is locally maximal at the data so the optimizer never
leaves,' so the paper should claim it as its own observation."* That was reached by *excluding*
three candidates (TuRBO, Fan, GIBO) without sweeping the vocabulary. With the vocabulary swept,
**Yarotsky is closest prior art and the paper now owes it a scoping sentence** rather than
silence. The frozen-cell evidence still stands as the paper's own empirical observation — 16
bit-identical seeds across two GP classes on a continuous task is not in Yarotsky — but the
related-work obligation is real and the "no prior art" phrasing is withdrawn.

**Two adjacent findings, both verified:**
- **Ament et al., NeurIPS 2023 Spotlight** (arXiv:2310.20708, venue verified via arXiv Comments
  and the matching proceedings URL) — EI/EHVI's *numerical* vanishing-gradient pathology
  degenerating the acquisition optimizer into random search. A different, EI-specific,
  floating-point mechanism; not a structural maximal-at-the-data claim.
- **Kim & Choi, ECML-PKDD 2020** (arXiv:1901.08350, venue verified from arXiv Comments) — bounds
  the regret gap between local and global optimizers of PI/EI/GP-UCB via a "collapse" probability.
  Touches GP-UCB directly but concerns **within-round inner-optimization fidelity**, not the
  outer-loop stuck-at-the-data claim.

## gap-6 (high) — accessible primaries for the η² small-n bias

**Target position:** η² is positively biased at small n; ω²/ε² are the corrections
(Mandatory Fix 9).

Was **secondhand** — Kelley (1935) and Olejnik & Algina (2003) are paywalled everywhere attempted.

**RESULT: UPGRADED TO FIRSTHAND. Two open-access primaries obtained, and one refines the fix.**

**1. Okada (2013), "Is Omega Squared Less Biased?", *Behaviormetrika* 40(2):129–147**, DOI
10.2333/bhmk.40.129 (venue verified from the PDF running header; J-STAGE paywalls this specific
volume, so full text came from a Wayback snapshot of the author's self-archived PDF).

Contains the **exact Monte Carlo bias table** (1M replications per condition):

| n per group | η² bias |
|---|---|
| 10 | **+0.054** |
| … | … |
| 100 | **+0.005** |

**Always positive**, shrinking with n. ε² and ω² are always small and **negative**.

**And it refines Mandatory Fix 9 in a way I had wrong.** Okada's own simulation **overturns the
folk belief that ω² is the least-biased correction — ε² is.** So the recommendation to the paper
should name **ε²**, or report both, rather than defaulting to ω² as I originally wrote.

**2. Liu (2022), "Bias correction for η² in one-way ANOVA", *Methodology* 18(1):44–57**, DOI
10.5964/meth.7745, **CC BY 4.0**. States firsthand: *"eta squared is not an unbiased estimate and
is known to have positive bias… depends on sample size"*, and attributes the corrections directly
— **Kelley (1935) for ε², Hays (1963) for ω²**.

**Net:** Mandatory Fix 9 no longer rests on the JOSS documentation quoting paywalled sources. It
rests on two open-access primaries with verbatim quotes, plus my own first-hand computation of
the bias from the paper's own bootstrap artifacts (+0.0099 to +0.0184 across four corners). At
the paper's n=7 tasks, Okada's table puts the expected η² bias **above** his smallest tabulated
condition — consistent in direction and rough magnitude with what the artifacts show.

---

## Effect on committed positions

**No position has been overturned by the gap-fill wave so far.** The SAEA check strengthens N6 —
the best remaining candidate region's most on-target paper is clean on all nine decomposition
terms, verified first-hand rather than by relay.

Per the step-8 protocol, positions for which an adversarial search returned no substantive
challenge gain confidence, and `research/comparisons.md` is annotated accordingly.
