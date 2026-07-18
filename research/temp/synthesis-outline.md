# Synthesis outline

## Executive summary
The direct answer: 3 of 9 claims are clean NONE FOUND (N6, N7, N9-narrow), 5 are PARTIAL (N1, N3, N4,
N5, N8), N2 is NONE FOUND-but-pre-empted; the strongest publishable contribution is D (the five named
offline-MBO confounds + protocol + two-way η² + the strengthening 0.37→0.405). Lead with this verdict.

## Verdict Summary — N1-N9 Novelty Table
A compact table: claim | verdict (FOUND / NONE FOUND / NOT VERIFIABLE, PARTIAL as hybrid) | citation
(venue+year+arXiv) | the specific overlapping sentence OR the exact NONE-FOUND queries. This is the
highest-value artifact — complete and exact.

## N1 — Confound Taxonomy: Prior-Art Overlap and the Offline-MBO Residual
Shape FOUND (Henderson AAAI 2018, "implementation differences... dramatic impacts"; Ferrari Dacrema,
Musgrave, Lucic); residual (η² decomposition + five offline-MBO confounds + net-UP) NONE FOUND.

## N2 — K-Contingency of the Surrogate-Class Ranking
NONE FOUND; engage L/R/W's opposite result (K-robust over {5,10}; our flip at K=2); frame as observation
(small-K σ-noise), not a discovered law. Abe = capacity, not ranking.

## N3 — Unmatched Effective Pessimism
PARTIAL — Dewolf (AI Review 2022, arXiv:2107.00363) owns the general principle; Ghasemipour closest
offline-RL analog (different mechanism); Srinivas GP-UCB single-surrogate; offline-MBO acquisition-
comparison application NONE FOUND.

## N4 — Distance-Aware Uncertainty and the Implicit Trust Region
PARTIAL — SNGP owns distance-awareness; Fan et al. (NeurIPS 2024) owns UCB-as-local-search; "implicit
trust region" naming + offline-MBO app NONE FOUND; β=0 relocates the mechanism to the mean; Ovadia
complicates "confidently wrong far from data"; DUE caveat is deep-kernel-specific (doesn't apply).

## N5 — NTK / Spectral Bias and the Finite-Width Objection
PARTIAL — theory real (Jacot/Lee/Rahaman) but the K-sweep is a K≠width category error; L/R/W App D.1.2
(ranking-invariant to architecture size) partially answers the objection; clean width sweep is the
missing experiment.

## N6 — The Crossed Surrogate x Optimizer Factorial
NONE FOUND (strongest). Kim survey names the gap; 0 factorial/ANOVA hits across Design-Bench/Chemingui/
Tan; Hutter fANOVA (one-way) + Liang npj 2021 (crossed-but-descriptive-online) nearest misses.

## N7 — Bidirectional Smoothness Manipulation
NONE FOUND at broadest scope; Lim et al. (2021) hypothesizes GP-smoothness but never manipulates; IGNITE/
MS-DDEO/ROOT one-directional. C's "first at all" ceiling, contingent on running M1+M2.

## N8 — Platform and Library-Version Dependence of Benchmark Results
PARTIAL — Henderson + Nagarajan own "implementation/environment variance ≈ method-difference variance";
offline-MBO + macOS-vs-Linux cross-platform axis + a stated ratio NONE FOUND.

## N9 — The De-Confounding Direction: an Audit That Strengthens
NONE FOUND within ML/CS narrow (a corrected scalar effect EXCEEDS its published value; 0.405 landed);
pre-empt Recht (relative), Agarwal (power), Bressan (psychology).

## Candidate Contributions: The One Sentence Each Owns (A / C / D)
A owns the offline-MBO-specific ANOVA attribution (under-credited, narrow); C would own the
smoothness-causal-axis sentence only if the bidirectional manipulation is run (a bet); D owns the
five-confound + strengthening-direction sentence (strongest). Recommend D.

## The Three Strongest Rejecting Citations
1. L/R/W (ICLR 2024) — surrogate comparison + opposite K + D.1.2 finite-width control. 2. Shahriari
(2016) — surrogate>acquisition doctrine caps the reversal. 3. Kim survey (TMLR 2026) + Agarwal/Demšar —
genre established + Design-Bench null underpowered (N=7 < Demšar N>10).

## AAAI-27 Venue Fit and Reviewer Pool
D/A → ML: Evaluation, Benchmarking, Datasets & Analysis (reality-check reviewers). C → ML: Bayesian
Learning & Uncertainty Quantification (GP/BO methodologists; N5 lands hardest). Cross-list SO:
Algorithm Configuration & Sampling-based Search.

## What I Could Not Verify and Why
MS-DDEO body (closed-access); exact β=0 numbers (0.504→0.511 repro vs 0.51→0.47 cited); η²_opt magnitude
(unequal-budget confound unfixed); N7 non-English DDEA/RBFN; N3 conformal forward-cite (S2 rate-limited);
N9 beyond ML/CS (Bressan is psychology).

## Sources
Inline style: numbered [N], deduplicated, each "[N] Authors. Title. Venue Year. arXiv:ID / DOI."
