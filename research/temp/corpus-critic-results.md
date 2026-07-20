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

---

## gap-3 (high) — N9 overturning search in its exact framing

**Target position:** no ML reality-check/benchmark audit reports a corrected variance-explained
statistic above its own published value.

Searched separately from the two adjacent literatures already checked (Hamdan's confound-leakage,
which is ML methodology rather than a benchmark audit; Maassen's psychology meta-analysis
recomputation). The distinct framing sought was an **ML benchmark audit whose corrected effect
size grew**, including the reproducibility-track literature (ML Reproducibility Challenge,
ReScience C) as the natural home for such a result.

*Result pending fetcher return; see the final report's N9 section for the verdict and queries.*

## gap-4 (high) — precedent for interpreting a component-by-component interaction

**Target position:** the buried interaction term is worth promoting partly because no prior ML
benchmark study reports and interprets an interaction between two pipeline components.

The locus-3 investigator scoped its precedent search to offline-MBO/BO benchmarks only. This gap
widens it to ML benchmarking generally — optimizer-versus-architecture studies (Schmidt et al.
"Descending through a Crowded Valley"; Choi et al. on optimizer comparisons), and the deep-learning
benchmarking literature.

**Either outcome is useful:** a precedent found narrows the novelty claim and must be cited; none
found strengthens the recommendation and is reported with the queries.

*Result pending fetcher return.*

## gap-5 (high) — the acquisition-stalling vocabulary itself

**Target position:** nobody owns "a confidence-bound acquisition is locally maximal at the data,
so the optimizer never leaves."

Three candidate owners were ruled out in earlier steps — TuRBO (diagnoses the *opposite*,
over-exploration), Fan et al. 2024 (proposes minimizing UCB as a method and proves *convergence*;
0 hits for offline/LCB/stuck/paralysis), and GIBO (no confidence bound in its exploitation step).
**But excluding three specific papers is not the same as sweeping the failure-mode vocabulary**,
which no prior step did. This gap closes that hole, including EI's documented over-exploitation
pathology.

*Result pending fetcher return.*

## gap-6 (high) — accessible primaries for the η² small-n bias

**Target position:** η² is positively biased at small n; ω²/ε² are the corrections
(Mandatory Fix 9).

Currently **secondhand** — Kelley (1935) and Olejnik & Algina (2003) are paywalled everywhere
attempted, so the claim rests on the JOSS `effectsize` documentation quoting them. The empirical
half is first-hand: I computed the bias from the paper's own bootstrap artifacts (+0.0099 to
+0.0184 across four corners). Named accessible candidates: Levine & Hullett (2002), Okada (2013),
Lakens (2013).

*Result pending fetcher return.*

---

## Effect on committed positions

**No position has been overturned by the gap-fill wave so far.** The SAEA check strengthens N6 —
the best remaining candidate region's most on-target paper is clean on all nine decomposition
terms, verified first-hand rather than by relay.

Per the step-8 protocol, positions for which an adversarial search returned no substantive
challenge gain confidence, and `research/comparisons.md` is annotated accordingly.
