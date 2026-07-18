# Step 1 — Decompose (offline-mbo-novelty-audit-6d8cd4)

**Tier:** full (user-forced; decompose independently agrees) · **response_format:** argumentative · **citation_style:** inline (venue + year + arXiv ID)

## Atomic structure
- **14 sub-questions**: the nine per-claim novelty verdicts (N1–N9), plus the A/C/D one-sentence-owned test, the three strongest rejecting citations, and the AAAI-27 venue-fit mapping (topics page must be fetched, not recalled).
- **9 claim entities** (N1–N9), each with a required verdict field (FOUND / NONE FOUND / NOT VERIFIABLE) and an overlapping-sentence-or-queries field. N1 additionally requires an offline-MBO residual; N4 requires readiness for both β=0 control outcomes.
- **3 candidate-paper entities**: A (repaired measurement), C (mechanism / smoothness causal axis), D (confound taxonomy).
- **~24 papers-to-fetch**, each tagged with its venue/year and any citation-date trap.

## Required section-heading contract (drives instruction-following)
```
## Verdict Summary — N1-N9 Novelty Table
## N1 - Confound Taxonomy: Prior-Art Overlap and the Offline-MBO Residual
## N2 - K-Contingency of the Surrogate-Class Ranking
## N3 - Unmatched Effective Pessimism
## N4 - Distance-Aware Uncertainty and the Implicit Trust Region
## N5 - NTK / Spectral Bias and the Finite-Width Objection
## N6 - The Crossed Surrogate x Optimizer Factorial
## N7 - Bidirectional Smoothness Manipulation
## N8 - Platform and Library-Version Dependence of Benchmark Results
## N9 - The De-Confounding Direction: an Audit That Strengthens
## Candidate Contributions: The One Sentence Each Owns (A / C / D)
## The Three Strongest Rejecting Citations
## AAAI-27 Venue Fit and Reviewer Pool
## What I Could Not Verify and Why
```

## Citation-date traps carried into every downstream step
- Li/Rudner/Wilson = **ICLR 2024** (S2 back-propagates 2023 from arXiv v1)
- Henderson et al. = **AAAI 2018** (S2 says 2017)
- Benavoli et al. = **JMLR 2016** (arXiv 2015)

## Method contract (from CRITICAL METHOD REQUIREMENTS)
Academic APIs (Semantic Scholar → arXiv → OpenAlex) before web search, every claim. Fetch primary and grep it — no verdict from a snippet. ≥1 adversarial search per claim. Four fabricated citations already caught on this project: zero tolerance.

## Coverage matrix
`research/temp/coverage-matrix.md` — 31 verbatim query phrases mapped, **zero Gap=YES rows**. Wrapper requirements (save paths, git rules, terminal section) correctly held out of the decomposition and parked in the scaffold.
