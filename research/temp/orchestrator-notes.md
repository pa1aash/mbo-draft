# Orchestrator notes — offline-mbo-novelty-audit-6d8cd4

## Candidate papers (from repo PAPER_V2_OUTLINE.md — statements of what WE claim)
- **A "Measurement, repaired"** = query candidate A. One-sentence: *the reported GP advantage in
  offline MBO is a surrogate-class effect, not an optimizer effect, measured under a controlled
  factorial that survives normalizing the ensemble, equalizing the candidate protocol, tuning the
  gradient optimizer.* Repo's own read: factorial design = NONE FOUND, BUT Li/Rudner/Wilson (ICLR
  2024) already owns "deep ensembles perform relatively poorly" + "ranking is problem-dependent →
  tailored inductive biases." Residual after stripping that: the factorial design + the offline
  setting — "an ablation." Repo self-rates P(accept) low-to-moderate.
- **C "Mechanism"** = query candidate C. One-sentence: *prior-task smoothness match is the single
  axis governing the GP-ensemble gap, gradient collapse, coverage failure, synthetic→real transfer
  — demonstrated by manipulation in BOTH directions + a continuous interpolation reproducing the
  Design-Bench null as a limit point.* KEY: the bidirectional manipulation = M1 (smooth the net) +
  M2 (roughen the GP) from MECHANISM_EXPERIMENTS.md — as of that doc these are PLANNED, not yet run
  ("It never manipulates smoothness"). C is a BET on X1 (target-scaling fix). Repo's own risk note:
  MS-DDEO 2022 grades surrogates by smoothness; Kim survey lists smoothness priors/RoMA — so C's
  novelty narrows to *attribution of the GP advantage to mean smoothness rather than calibration* +
  the continuum. => N5 (finite-width objection) + N7 (bidirectional manipulation) are the load-
  bearing novelty tests for C.
- **D "Confound taxonomy"** = query candidate D. Five named confounds (target scaling / candidate-
  oracle protocol / optimizer tuning / ensemble size K / effective pessimism) + protocol that
  removes them + demonstration the ranking MOVES when controlled. Maps onto the reality-check genre
  (Dacrema RecSys19, Musgrave ECCV20, Lucic NeurIPS18, Henderson AAAI18). Differentiator vs that
  genre = N9 (the audit STRENGTHENS: η²_surr 0.37 → 0.405). If N9 shape is unclaimed, D is the
  strongest of the three because it converts "yet another ablation" into "a reality-check that runs
  the OTHER way."

## Strategic read forming (pre-evidence, to be tested by fetchers)
- The whole audit hinges on 3 pivots: (1) N6 — is the crossed factorial in offline MBO truly
  NONE FOUND? (2) N1 residual — what does the reality-check genre NOT own that is offline-MBO
  specific? (3) N9 — is "audit that grows the effect" genuinely unclaimed? If all three hold, D is
  the publishable core and A/C are subsets/bets.
- N5 is the sharpest self-inflicted risk: our own K-sweep (K=2 ≫ K=5) is EVIDENCE that ensemble
  jaggedness is a finite-width artifact (Jacot/Lee: infinite width → GP; Rahaman: finite nets are
  spectrally biased toward smooth). This cuts AGAINST C (mechanism = surrogate-class property) and
  FOR D (taxonomy = it was a tuning/capacity confound). The audit should say this out loud.
- N4: repo's β=0 control (gap 0.51→0.47) argues AGAINST a σ-mediated (distance-aware) mechanism —
  so even the "GP variance grows away from data = implicit trust region" story is weakly supported
  by our own data. Keep both outcomes ready (control is being recomputed per query).

## Extra citations named by prior (worthless) passes — ensure the corpus/critic covers
Ovadia 2019 (ensembles under shift → N4), RoMA/Yu, NEMO/Fu&Levine, Fannjiang (autofocus),
Stanton, Jin (data-driven eDDEO → N7), Yauney ICLR2026 (micro-benchmark power → N8-adjacent),
Demšar N>10 rule. Kim survey should enumerate the offline-MBO method landscape for N6.

## Fetcher returns (running log)
- **Batch B (N1 pt2 + N9) DONE.** N1: Musgrave OWNS a variant of the taxonomy shape (3 flaw
  categories + corrected protocol + 14 reruns "marginal at best"); Agarwal Table 1 = 3-item
  taxonomy with ranking reversals. Residual for both: NO variance-decomposition/η² machinery, NO
  offline-MBO-specific confounds (proxy/ground-truth mismatch, distribution shift). N9 (KEY nuance):
  Melis = CLEAN SHRINK ("LSTMs outperform the more recent models, contra the published claims").
  **Recht = MIXED — absolute accuracy DROPS but RELATIVE gains GROW** (slope >1: 1.69 CIFAR-10,
  1.11 ImageNet; "Later models... increased advantage over earlier models"). Agarwal = power-driven
  strengthen (more runs→significant), NOT confound-removal-driven. => N9 forming as NONE FOUND for
  the exact shape (identify confounds→control→published η²-style effect GROWS), with **Recht a
  partial precedent** (a reanalysis where a *relative/secondary* effect grew) that the draft must
  engage honestly rather than claim pure novelty.

## AAAI-27 venue (fetched LIVE, source https://aaai.org/conference/aaai/aaai-27/areas-and-topics/)
Conf Feb 16-23 2027 Montréal; abstracts due Jul 21 2026, full papers Jul 28 2026.
Submission Areas (verbatim, top level): APP, AUD, CMS, **CSO (Constraint Satisfaction and
Optimization)**, CV, DMKM, GTEP, HAI, KRR, MAS, **ML (Machine Learning)**, NLP, PEAI, PRS, ROB,
**RU (Reasoning under Uncertainty)**, **SO (Search and Optimization)**. Venue-fit mapping (to
finalize): D/A → ML (evaluation/methodology) with SO as cross-area (offline MBO = black-box opt);
C → ML or RU (uncertainty/GP mechanism) with SO cross-listing. VENUE-FIT MAPPING (grounded in verbatim AAAI-27 sub-topics):
- **D (confound taxonomy)** → PRIMARY `ML: Evaluation, Benchmarking, Datasets & Analysis`
  (exact AAAI-27 topic string). Reviewer pool = empirical-rigor / reality-check reviewers who
  reward Dacrema/Musgrave/Lucic-style audits. Cross-list `SO: Algorithm Configuration &
  Sampling-based Search` (offline MBO = black-box opt).
- **A (repaired measurement)** → same PRIMARY (ML: Evaluation...) OR `SO: Algorithm Configuration
  & Sampling-based Search` if pitched as an optimization ablation. Same pool as D; higher risk of
  "this is an ablation" reception.
- **C (mechanism)** → PRIMARY `ML: Bayesian Learning & Uncertainty Quantification` (or
  `ML: Classification, Regression & Kernel Methods`). Reviewer pool = GP/BO/uncertainty
  methodologists who KNOW Li/Rudner/Wilson, SNGP, NTK — a MORE demanding pool for a mechanism
  claim; N5 objection lands hardest here. Cross `RU: Stochastic Optimization`.
- Supporting topics in play: `ML: AutoML & Hyperparameter Tuning` (N1 iii/iv), `ML: Deep Learning
  Theory & Learning Theory` (N5), `ML: Ensemble & Multi-class/Multi-label Learning`, `SO:
  Evolutionary Computation` (CMA-ES).

- **Batch D (N4 distance-aware) DONE.** SNGP OWNS the raw mechanism (Def 1 input-distance
  awareness; GP-RBF variance "increases monotonically toward 1" away from X_IND; ensembles "assign
  low uncertainty to OOD examples even if far from the data"). DUQ: "Deep Ensembles is uncertain
  only along the decision boundary, and certain elsewhere." DUE: an unconstrained deep-kernel GP is
  "certain even far away from the training data" → a GP does NOT automatically get variance growth
  (needs bi-Lipschitz features) — independent support that the σ-mechanism is not automatic (helps
  the β=0-cuts-against-σ reading). TuRBO: explicit hyperrectangle TR + Thompson Sampling (0 LCB
  hits); treats unchecked GP-variance growth as a PROBLEM. => **N4 verdict forming: the distance-
  aware "ensembles confidently wrong far from data / GP variance grows away" mechanism is PRIOR
  WORK FOUND (SNGP+DUQ); but the specific "LCB + growing GP variance = implicit trust region IN
  OFFLINE MBO" synthesis is NONE FOUND — ingredients owned, combination unclaimed.** Cuts against
  C-mechanism-novelty on the σ side; supports the taxonomy framing.

- **Batch C (N5) & E (N2/N6): API-failed mid-run but notes landed.** C completed all 4 (Jacot,
  Rahaman, Lee, Li/Rudner/Wilson — Jacot note has proper Claim-relevance body). E completed Abe,
  Lakshminarayanan, Design-Bench, Chemingui; died entering Tan → orchestrator filled the Tan note
  directly (grep-verified: Tan varies 5 surrogates with gradient ascent FIXED, 0 factorial/ANOVA
  hits → N6 stays NONE FOUND; Tan biblio confirms IGNITE=Dao et al NeurIPS2024 + sibling "Boosting
  offline optimizers with surrogate sensitivity" ICML2024).
- **W1 resolved N7/N6 web targets:** IGNITE = "Incorporating Surrogate Gradient Norm to Improve
  Offline Optimization Techniques" (Dao/Nguyen/Truong/Hoang, NeurIPS 2024); MS-DDEO (evolutionary,
  model-selection by smoothness); Kim survey = "Offline Model-Based Optimization: Comprehensive
  Review" TMLR 2026 (arXiv). (+wenyin-gong author page, low value.)
- **W3 miss-catcher extra finds:** "Why So Pessimistic? Estimating Uncertainties for Offline RL
  through Ensembles" (N3-relevant — pessimism/ensembles offline RL); plus N8 reproducibility set:
  "Impact of Nondeterminism on Reproducibility in Deep RL", "Reproducibility of Benchmarked Deep RL
  Tasks for Continuous Control", "Revisiting the Arcade Learning Environment". Awaiting W1/W3
  completion summaries for the NONE-FOUND query logs (N2/N3/N6/N9) + N7 forward-citation result.

- **W2 (N8 + venue) DONE.** N8 = PRIOR WORK FOUND (PARTIAL). Gundersen&Kjensmo: only a cited
  caveat ("differences in software and hardware could have significant impact on results because of
  rounding errors in floating point arithmetic (Hong et al. 2013)") — no own measurement, no
  magnitude vs method-difference. STRONGEST matches via citation-chase: **Henderson (AAAI18)** —
  swapping ONLY codebase/implementation of the identical algo gives return spreads ≥ a
  non-significant inter-algorithm effect; verbatim *"implementation differences which are often not
  reflected in publications can have dramatic impacts on performance."* **Nagarajan (2018)** —
  GPU-op nondeterminism alone gives variance that "looks similar to the curves for exploration and
  weight initialization." => N8 residual = the OFFLINE-MBO domain + the specific cross-platform
  (macOS vs Linux) axis + a stated same-order ratio; the general "implementation/environment
  variance ≈ method-difference variance" phenomenon is OWNED by the deep-RL reproducibility genre.
  INTEGRITY: W2 caught + rejected a fabricated "74-87% GPU-driven std" WebSearch summary (0 grep
  hits) — did not cite it. Venue: AAAI's own rule = pick the subarea of the MAIN contribution;
  confirms D/A→`ML: Evaluation, Benchmarking, Datasets & Analysis`, C→`ML: Bayesian Learning &
  Uncertainty Quantification`. (Henderson now has 2 notes: N1 + N8 analysis — merge in curation.)

- **Batch A (N1 pt1) DONE.** Ferrari Dacrema=PARTIAL (weak baselines/protocols; 6/7 neural lose to
  simple baselines; no η²). Balduzzi=DOES-NOT-TOUCH (Nash averaging = benchmark-aggregation bias, a
  different axis). **Henderson (AAAI18)=OWNS the shape most tightly** (taxonomy: hyperparams/arch/
  reward-scale/seeds/env/codebases; rankings reverse; "implementation differences... can have
  dramatic impacts"). Lucic=PARTIAL single-confound (compute/HP budget; "no algorithm clearly
  dominates... with enough hyperparameter optimization"). Phase-2 chased Islam ICML17-ws + Machado
  JAIR18. **N1 RESIDUAL (crisp): the reality-check SHAPE is an established genre since 2017 (verdict
  = PRIOR WORK FOUND for the shape); the two things NONE of them own = (a) offline-MBO-specific
  confound vocabulary (target scaling / candidate-oracle protocol / ensemble-size K / β-pessimism
  σ-mismatch), and (b) a quantitative η²-variance-decomposition where confounds net UP when
  combined.** (b) is the bridge to N9. => confirms D's differentiation from the genre.

## TRUE CORPUS: 33 note files on disk (note-list display caps at 20). Every claim N1-N9 has >=3
## grep-verified primary sources. Appropriate for a focused prior-art audit.

## Process
8 fetchers dispatched (A-E readers over local text; W1 Kim/IGNITE/MS-DDEO; W2 AAAI-27+Gundersen;
W3 miss-catchers N2/N3/N6/N9). Awaiting completions. Tooling reality: CLI PDF fetch broken;
local curl+pdftotext is the ground truth; arXiv API + S2 flaky; OpenAlex ok.
