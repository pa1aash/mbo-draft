# Step 8 — Corpus-critic gap-fill results (offline-mbo-novelty-audit-6d8cd4)

6 gaps identified; 5 fetched/tested (N7 non-English DDEA documented as unsearched-by-design). 3
gap-fill fetchers ran. Net: **two honest verdict downgrades (N3, N4), one refinement (N5), one
strengthened NONE FOUND (N6), one confirmation (N9)**. No verdict was overturned to FOUND; no
contribution collapsed.

## Gap 1 — N6 crossed factorial (CRITICAL, fatal-if-found) → NONE FOUND, STRENGTHENED
Searched the fANOVA/AutoML/hyperparameter-importance neighborhood (21+ queries). No crossed
model-class × optimizer two-way ANOVA/η² decomposition exists.
- **Hutter/Hoos/Leyton-Brown, fANOVA (ICML 2014):** "model class" = most important hyperparameter
  (31–58% variance) but ONE-WAY, on data from one fixed search method (SMAC).
- **Moosbauer et al. (IEEE TEVC 2022):** discusses then rejects fANOVA for OFAT; varies surrogate +
  sampling separately, never a joint factorial.
- **Liang et al. (npj Comp. Materials 2021):** closest structural analog — crossed surrogate ×
  acquisition grid — but descriptive ranking only (0 ANOVA/η² hits) and ONLINE BO.
- **Draft action:** cite Hutter (2014) + Liang (2021) as nearest neighbors; state the residual as
  the crossed surrogate×optimizer factorial *with a two-way ANOVA/η² decomposition, in offline MBO*.

## Gap 2 — N5 width ablation (CRITICAL) → PARTIAL/CONFOUNDED (was: clean gap)
- **Dai et al. 2022 resolved:** "Sample-Then-Optimize Batch Neural Thompson Sampling" (NeurIPS 2022,
  arXiv:2210.06850). Deep-Ensemble critique is *algorithmic* (reduced STO-BNTS w/o linearization,
  loses guarantees); width-sweeps only its own net, never the ensemble.
- **Decisive:** L/R/W Appendix D.1.2 reruns the full comparison including the K=5 ensemble at a
  smaller architecture (width 128→50, K fixed) → "the relative performance of the surrogate models
  mostly remains consistent… HMC often outperforms… deep ensembles."
- **Effect:** (a) partially pre-empts N5's "width untested" framing — the paper's clean width sweep
  must be positioned as a de-confounded version of L/R/W's D.1.2 (which changes width+depth+
  activation together, one alt size); (b) EMPIRICALLY WEAKENS the finite-width objection to C —
  shrinking the net does not rescue the ensemble; ranking is architecture-size-invariant over the
  tested range. Combined with the K≠width category error, the N5 objection to a mechanism paper is
  more answerable than the depth locus assumed.

## Gap 3 — N3 conformal/calibration (HIGH) → PARTIAL (was: clean NONE FOUND, >80%)
- **Dewolf, De Baets, Waegeman, "Valid Prediction Intervals for Regression Problems" (AI Review
  2022, arXiv:2107.00363):** states N3's premise in general statistical form across 4 UQ classes at
  one shared confidence — "uncalibrated models… either underestimate the uncertainty or produce
  overconservative prediction intervals"; normalize nonconformity by a dispersion σ. 0 hits for
  acquisition/BO/pessimism/surrogate/LCB.
- **Effect:** N3's general principle (a shared confidence multiplier yields unequal effective
  coverage across differently-scaled estimators) is OWNED by the conformal/calibration literature.
  N3's residual narrows to the **offline-MBO acquisition-comparison application** (shared β across
  surrogate CLASSES inside LCB). Draft must concede the general principle to Dewolf (2022) /
  Papadopoulos–Vovk–Gammerman (2011) and claim only the application.

## Gap 4 — N4 LCB variance-growth = trust region (HIGH) → PARTIAL (was: clean NONE FOUND)
- **Fan, Wang, Ng, Hu, "Minimizing UCB: a Better Local Search Strategy in Local BO" (NeurIPS 2024,
  arXiv:2405.15285):** derives "minimizing UCB can be viewed as local strategy" (UCB small near
  samples, grows away). "trust region" only as TuRBO citations; "implicit" 0 hits.
- **Effect:** the causal MECHANISM (variance-growth → local/trust-region-like search under LCB/UCB)
  is OWNED by Fan et al. (2024). The specific **"LCB is an implicit trust region" naming + the
  offline-MBO application** remains unclaimed. Draft must cite Fan (2024) and claim only the framing
  + offline-MBO instantiation.

## Gap 5 — N9 forward-citation on Recht (HIGH, verification) → NONE FOUND
~10 OpenAlex cites-filter + WebSearch queries. No third party characterizes Recht 2019's slope>1
"increased advantage" as an "audit that strengthens" instance. Reinforces N9's narrow verdict; Recht
+ Agarwal remain must-pre-empt partials for the broad claim.

## Gap 6 — N7 non-English DDEA/RBFN venues (HIGH) → NOT EXHAUSTIVELY SEARCHED (documented limitation)
The MS-DDEO literature family includes non-English-language DDEA/RBFN venues not searched (language
barrier + closed access). N7 stays NONE FOUND within all English-language BO/kernel/GP/offline-MBO
literature; this residual uncertainty goes to the terminal "could not verify" section.

## Side-finding applied to comparisons.md
Repo commit `14e6bf5` shows the N9 strengthening number (η²_surr=0.405) has LANDED (30-seed run),
not pending; η²_opt (unequal-budget confound unfixed) and exact β=0 numbers remain provisional/NOT
VERIFIABLE. comparisons.md updated accordingly.
