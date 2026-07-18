# Pre-staged synthesis thesis (for step 11) — offline-mbo-novelty-audit-6d8cd4

## Single strongest thesis across all 3 angles
The genuinely novel, defensible contribution is the **confound-taxonomy + strengthening-direction
(candidate D)**: the first crossed surrogate×optimizer ANOVA decomposition in offline MBO (N6 NONE
FOUND), five offline-MBO-specific confounds whose removal MOVES the published ranking, and — uniquely
within ML/CS — a de-confounding audit whose corrected effect GREW (N9 narrow NONE FOUND; η²_surr
0.37→0.405 landed). The mechanism paper (C) has the highest novelty ceiling (N7 bidirectional
smoothness = first-at-all) but is a BET on unrun experiments and is undercut by its own K-sweep being
a K≠width category error. The repaired-measurement paper (A) is under-credited but narrow.

## Final per-claim verdicts (the table)
- **N1**: PRIOR WORK FOUND (shape → Henderson AAAI 2018); the η²-decomposition + offline-MBO confound
  vocabulary residual = NONE FOUND.
- **N2**: NONE FOUND (L/R/W ICLR 2024 found K-robustness over {5,10}; our K=2 flip is unreported and
  most likely small-K σ-noise — assert the observation, not a "law").
- **N3**: PARTIAL (general principle → Dewolf AI Review 2022 / Papadopoulos-Vovk-Gammerman 2011;
  offline-MBO acquisition-comparison application = NONE FOUND).
- **N4**: PARTIAL (distance-aware mechanism → SNGP NeurIPS 2020; UCB-local-search → Fan NeurIPS 2024;
  the "implicit trust region" NAMING + offline-MBO instantiation = NONE FOUND; σ-mediation undercut
  by β=0 → the viable mechanism is the posterior MEAN, not σ).
- **N5**: PARTIAL (NTK/spectral theory real but the paper's K-sweep is a K≠width category error;
  L/R/W App D.1.2 architecture-size ranking-invariance ANSWERS the objection; clean width sweep NONE
  FOUND but the missing experiment).
- **N6**: NONE FOUND (strongest verdict; Kim TMLR 2026 names the gap; nearest-miss Hutter fANOVA ICML
  2014 one-way + Liang npj 2021 crossed-but-descriptive-online).
- **N7**: NONE FOUND at broadest scope (Lim Adv. Intell. Syst. 2021 hypothesizes smoothness but never
  manipulates; IGNITE/MS-DDEO/ROOT one-directional).
- **N8**: PARTIAL (phenomenon → Henderson AAAI 2018 + Nagarajan 2018; offline-MBO + macOS-vs-Linux
  cross-platform axis + stated ratio = NONE FOUND).
- **N9**: NONE FOUND within ML/CS narrow (a corrected scalar effect EXCEEDS its published value);
  Recht ICML 2019 (relative) / Bressan 2019 (psychology) / Agarwal NeurIPS 2021 (power) = partials to
  pre-empt.

## A/C/D one-sentence tests
- **A** OWNS: "the GP advantage in offline MBO is a surrogate-class effect, not an optimizer effect,
  established by the first offline-MBO-specific crossed surrogate×optimizer ANOVA under a shared
  protocol" (PGS fixes the surrogate axis; L/R/W fixes the optimizer as a nuisance — neither makes
  the attribution).
- **C** would own (only if the bidirectional manipulation is RUN): "surrogate-posterior smoothness,
  not calibration, is the causal axis of the GP-ensemble gap, shown by manipulating it in both
  directions" — novel (N7 first-at-all) but currently unearned + undercut by the K-sweep category error.
- **D** OWNS the strongest: "five previously-unreported offline-MBO confounds, removed under one
  protocol, move the published ranking AND increase the surrogate effect size (0.37→0.405) — a
  reality-check whose audit strengthens rather than shrinks, which no prior ML/CS reality-check reports."

## Three strongest rejecting citations
1. **Li/Rudner/Wilson (ICLR 2024, arXiv:2305.20028)** — compares surrogate classes in BO, found the
   OPPOSITE K result, and pre-answered the finite-width objection (App D.1.2). Hits N2, N5, N6, A-credit.
2. **Shahriari et al. (2016, Proc. IEEE)** — surrogate>acquisition is textbook doctrine → the
   "reversal" confirms the field. Hits the reversal framing.
3. **Kim survey (TMLR 2026) + Agarwal (NeurIPS 2021)/Demšar** — the reality-check genre is established
   and the Design-Bench null at N=7 is underpowered (below Demšar's N>10). Hits N1 + the null.

## Venue fit
- **D / A → `ML: Evaluation, Benchmarking, Datasets & Analysis`** (empirical-rigor / reality-check
  reviewer pool). Cross-list `SO: Algorithm Configuration & Sampling-based Search`.
- **C → `ML: Bayesian Learning & Uncertainty Quantification`** (GP/BO/uncertainty methodologists —
  the most demanding pool; the N5 objection lands hardest here). Cross-list `RU: Stochastic Optimization`.

## Terminal "What I could not verify and why"
MS-DDEO body (closed-access); exact β=0 numbers (repro 0.504→0.511 vs cited 0.51→0.47, being
recomputed); η²_opt magnitude (unequal-oracle-budget confound unfixed → reversal provisional); N7
non-English DDEA/RBFN venues; exhaustive N3 conformal forward-citation sweep (S2 rate-limited); N9
beyond-ML/CS scope (Bressan is psychology).

## Contentious beats the final MUST visibly engage
C-vs-D recommendation; whether N5 sinks C; reversal overclaim vs PGS-specific; N9 narrow-vs-broad.
