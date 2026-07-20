# Synthesis plan

## Core thesis (1-2 sentences)
Of the paper's nine claims, three survive as clean NONE FOUND (N6 crossed surrogate×optimizer factorial
in offline MBO; N7 bidirectional smoothness manipulation; N9's narrow "audit that strengthens" within
ML/CS), four are PARTIAL (N1/N3/N4/N5/N8: a prior work owns the general form, an offline-MBO-specific
residual is unclaimed), and N2 is NONE FOUND but pre-empted in strength by Li/Rudner/Wilson's opposite
K-result. The strongest publishable contribution is candidate D — the named five-confound set + removal
protocol + two-way η² attribution + the strengthening direction (η²_surr 0.37→0.405) — because it is the
intersection of what is genuinely unclaimed AND already executed, unlike A (under-credited but narrow)
or C (highest ceiling via N7 but contingent on an unrun bidirectional manipulation and undercut by a
K≠width category error).

## The strongest argumentative beats
1. **N6 lands NONE FOUND three ways** (Draft A) — the field NAMES the gap (Kim TMLR 2026: gains
   undistinguished between "superior surrogate modeling, improved optimization strategies, or mere
   chance"), every offline-MBO candidate fixes one axis or bundles both (0 factorial/ANOVA hits), and
   the two nearest misses fall short the same way (Hutter fANOVA ICML 2014 one-way; Liang npj 2021
   crossed-but-descriptive-online). Load-bearing for candidates A and D.
2. **The N4→N5 convergence** (Draft C) — the β=0 control (gap survives σ removal) and the K-sweep's
   invalidity as width evidence both point away from σ AND away from cardinality, converging on the
   posterior MEAN's smoothness as C's only surviving mechanism — which relocates C from an owned
   distance-aware-σ story to an unclaimed mean-smoothness story while exposing C's current evidence as
   a category error.
3. **L/R/W App D.1.2 as the three-pillar rejection** (Draft B) — it already ran the paper's "missing"
   finite-width control (ranking-invariant to architecture size), simultaneously pre-empting N2
   (K-robustness), answering N5 (finite-width objection), and supplying a rival mechanism. This is the
   #1 rejecting citation.
4. **The reversal is capped by Shahriari 2016** (all drafts) — surrogate>acquisition is doctrine, so
   η²_opt=0.01 confirms the field; frame it as falsifying PGS's LOCAL premise, not a field reversal.
5. **N9 narrow-not-broad** (Draft A) — the strengthening direction is unclaimed only in the narrow
   scalar-effect-size form within ML/CS; Recht (relative) and Agarwal (power) must be pre-empted.
6. **D is the recommendation, by convergence** — all three angles reach D independently.

## Section structure (use required_section_headings verbatim, in order)
Verdict Summary table → N1..N9 (one H2 each) → Candidate Contributions (A/C/D one-sentence) → Three
Strongest Rejecting Citations → AAAI-27 Venue Fit and Reviewer Pool → What I Could Not Verify and Why →
Sources (inline style).

## Per-section commitments
- **Verdict table:** three-value verdicts (FOUND / NONE FOUND / NOT VERIFIABLE) with PARTIAL rendered
  as a hybrid cell ("PARTIAL — prior work owns X; residual Y NONE FOUND"). Each row: claim, verdict,
  citation (venue+year+arXiv), the specific overlapping sentence or the exact NONE-FOUND queries.
- **N1:** concede the shape to Henderson (AAAI 2018) up front; claim the η²+offline-MBO-confound residual.
- **N2:** NONE FOUND, but engage L/R/W's K-robustness (they tested {5,10}, our flip is K=2); frame as
  observation not law (small-K σ-noise).
- **N3:** PARTIAL — Dewolf (AI Review 2022) owns the general principle; offline-MBO acquisition-comparison
  application NONE FOUND.
- **N4:** PARTIAL per Conflict 1; the viable mechanism is the mean, not σ (β=0).
- **N5:** PARTIAL — K≠width category error; L/R/W D.1.2 answers the objection; clean width sweep is the
  missing experiment.
- **N6:** NONE FOUND (strongest); cite Hutter + Liang nearest-miss.
- **N7:** NONE FOUND broad; Lim 2021 hypothesizes only.
- **N8:** PARTIAL — Henderson/Nagarajan own the phenomenon; offline-MBO + cross-platform residual.
- **N9:** NONE FOUND narrow; pre-empt Recht/Agarwal/Bressan.
- **Candidates:** commit to D; A under-credited-but-narrow; C high-ceiling-but-a-bet.
- **Rejecting citations:** L/R/W (ICLR 2024), Shahriari (2016), Kim survey (TMLR 2026)+Agarwal/Demšar.
- **Venue:** D/A → ML: Evaluation, Benchmarking, Datasets & Analysis; C → ML: Bayesian Learning &
  Uncertainty Quantification; cross-list SO: Algorithm Configuration & Sampling-based Search.
- **Terminal:** MS-DDEO closed-access; β=0 exact numbers; η²_opt magnitude; N7 non-English DDEA; N3
  conformal forward-cite; N9 beyond-ML/CS.

## Where drafts disagreed
See synthesis-conflicts.md. All resolved toward the step-8-calibrated PARTIAL readings; B's adversarial
"owned" lean is used to harden the rejecting-citations section, not to overturn the calibrated verdicts.

## Length target
- response_format: argumentative
- Pass 1 target: ~8500 words
- Pass 2 final target: ~7000-7500 words (cut redundancy across the three drafts; one voice)
