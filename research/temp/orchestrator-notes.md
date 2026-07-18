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

- **N3 partial precedent found (via W3):** "Why So Pessimistic? Estimating Uncertainties for
  Offline RL through Ensembles" (Ghasemipour, Gu, Nachum, NeurIPS 2022, arXiv:2205.13703). Shares
  N3's SHAPE ("same nominal pessimism formula → different EFFECTIVE conservatism via an unmeasured
  implementation detail"; verbatim *"shared pessimistic targets can paradoxically lead to value
  estimates that are effectively optimistic"*). BUT mechanism = target independence-vs-sharing
  within ONE Q-ensemble, NOT differing σ scales across surrogate CLASSES sharing one β. => **N3 =
  NONE FOUND for the specific cross-surrogate-class σ-mismatch mechanism, with Ghasemipour as an
  honest conceptual analog the draft must cite (the "effective ≠ nominal pessimism" idea exists in
  offline RL, for a different reason).**

- **W1 (Kim/IGNITE/MS-DDEO, N6/N7) DONE.**
  - **Kim survey → N6 = NONE FOUND, reinforced.** Kim, Gu, Yuan, Yun, Liu, Bengio, Chen, "Offline
    Model-Based Optimization: Comprehensive Review," **TMLR 2026** (DATE TRAP: arXiv v1 Mar 2025,
    certified TMLR Jan 2026), arXiv:2503.17286. Its four-component surrogate taxonomy is DESCRIPTIVE
    not an empirical factorial; its own future-work names the gap: existing benchmarks don't
    distinguish *"whether observed gains stem from superior surrogate modeling, improved
    optimization strategies, or mere chance."* => the field itself concedes the decomposition N6
    does is undone. Strong verbatim support for N6 novelty.
  - **N7 = NONE FOUND (strong, with named near-misses).** IGNITE = Dao/Nguyen/Truong/Hoang, NeurIPS
    2024, arXiv:2503.04242 — SMOOTHS NN surrogate sharpness only, never roughens, 0 "Gaussian
    process" hits; forward-cite (8 citers) no bidirectional paper. MS-DDEO = Zhen/Gong/Wang, SWEVO
    2022, DOI 10.1016/j.swevo.2022.101080 — CLOSED-ACCESS (403, no abstract via Unpaywall), paraphrase
    only, **NOT VERIFIABLE at sentence level** (→ terminal section); 4-tier RBFN smoothness pool for
    SELECTION, never GP. **ROOT (NeurIPS 2025, arXiv:2509.16300)** = closest GP-smoothness hit, but
    it VARIES length-scale for DATA AUGMENTATION (synthetic-function generation), not causal
    ablation → N7 stays NONE FOUND. "Boosting Offline Optimizers with Surrogate Sensitivity" (ICML
    2024, arXiv:2503.04181) = IGNITE precursor, one-directional. => nobody manipulates smoothness in
    BOTH directions to establish it as the causal axis of a surrogate-class gap.

- **W3 (miss-catchers N2/N3/N6/N9) DONE — all query logs in
  `research/notes/miss-catcher-search-log-n2-n3-n6-n9-n1-residual.md`.**
  - **N2 = NONE FOUND + a LOAD-BEARING TENSION.** Abe never touches BO/surrogate ranking. Li/Rudner/
    Wilson (ICLR24) runs the closest analog (K=5-vs-10 ensemble-size ablation inside a BO surrogate
    comparison) and finds the OPPOSITE: verbatim *"the different ensembles perform similarly across
    many experiments, showing the robustness of our results to this hyperparameter"* (Fig A.7). =>
    our K-sweep (K=2 ≫ K=5, ranking flips) DIRECTLY CONTRADICTS L/R/W. This is the #1 contradiction
    for step 3: raises N2 novelty AND arms a reviewer. (Also intersects N5: our K-dependence is the
    finite-width evidence; L/R/W's K-robustness is evidence against it — a genuine fork.)
  - **N3 = NONE FOUND** (Ghasemipour closest analog, cross-class σ-mismatch never addressed).
  - **N6 = NONE FOUND** — all 5 named papers grepped "factorial"/"ANOVA"/"crossed" = 0 hits each.
  - **N9 = MIXED (not clean NONE FOUND).** No ML/CS paper where an audited headline number EXCEEDS
    its originally published value. Partial precedents: Recht (ML, relative-slope steepens while
    absolute drops) + **Bressan, "Confounds in failed replications" (Frontiers in Psychology 2019,
    DOI 10.3389/fpsyg.2019....)** — controlling a stimulus-allocation confound restores a "failed"
    replication and a stricter spec "came out stronger" (p 0.001→0.002), but no effect-size stat and
    OUTSIDE ML. => N9 verdict = NONE FOUND *within ML/CS* for the exact shape (audit → published
    η²-style effect GROWS); honestly flag Recht + Bressan as the nearest partials.

## ALL 8 FETCHERS DONE. Step-2 corpus complete: every N-claim has grep-verified primary sources +
## documented NONE-FOUND query logs. Verdicts drafted for N1-N9 (see per-claim notes above).

## TRUE CORPUS: 33 note files on disk (note-list display caps at 20). Every claim N1-N9 has >=3
## grep-verified primary sources. Appropriate for a focused prior-art audit.

## Candidate depth loci (orchestrator's pre-merge list, from contradiction graph)
- L1 **K-dependence & finite-width (N2+N5)** — dialectical. Read L/R/W Fig A.7 K-ablation closely
  (they found K-robustness; we found K-flip). Confirms N2 novelty + strength of the finite-width
  objection to C. HIGHEST priority (composite ~34).
- L2 **σ-mechanism / distance-aware (N4)** — dialectical/technical. SNGP/TuRBO/DUE bodies; pin the
  offline-MBO-LCB-implicit-TR residual; ready both β=0 outcomes (~30).
- L3 **N1 residual + N9 direction** — synthesis/dialectical. Henderson/Musgrave/Agarwal + Recht/
  Bressan; exact residual + is audit-strengthens unclaimed in ML/CS (~30).
- L4 **N6 crossed-factorial confirmation** — technical. Design-Bench/Chemingui/Tan/Kim: none run
  the factorial (one counterexample fatal; Kim names the gap) (~26).
- L5 **Which candidate A/C/D is strongest + one-sentence test** — synthesis. The integrating
  deliverable (~30).

## Loci analyst A returned (6 loci) — distinctive adds beyond my candidate list:
- **N3 gap:** classic GP-UCB β_t calibration literature (Srinivas et al. 2010 GP-UCB) never checked
  → may partially own N3 (matched/unmatched pessimism). Candidate for a gap-fetch.
- **DUE scope catch:** DUE's "GP not automatically variance-growing" caveat is about DEEP-KERNEL GPs
  (learned features), but our surrogates = exact GP + SVGP with STANDARD kernels → corpus may be
  OVER-citing DUE against the σ-mechanism. Sharpens N4.
- **L/R/W third mechanism:** "small BO datasets prevent ensemble mode-diversity" — a K-explanation
  neither our K-artifact nor C's smoothness story accounts for. Sharpens N2.
- A's skip_loci: N1-residual (crisp), N6 (greps done), N8-ratio, PGS-vs-η²opt (internal recompute),
  Abe-vs-Laksh (subsumed), MS-DDEO access (exhausted).

## DEPTH INVESTIGATOR RETURNS (step 5)
- **N9 (audit-strengthens + integrity) DONE.** INTEGRITY FIX: unverified citation = Robinson/Glen/
  Lee "Validating the Validation" (arXiv:1905.11681) — now fetched+grepped, confirmed CLEAN SHRINK
  (reverses "DL outperforms" → "SVM competitive"; no confound-strengthens). VERDICT: N9's NARROW
  claim ("a confound-controlled audit whose corrected SCALAR effect-size EXCEEDS its published
  value, within ML/CS") = UNCLAIMED, safe to assert (~75-80%, 16 adversarial queries). N9's BROAD
  claim ("reality-checks always shrink, ours is the exception") = FALSE — Recht (relative-slope
  growth) + Agarwal (power-revealed effect) are partial ML/CS counter-instances that MUST be
  engaged directly, not omitted; Bressan = closest full-shape precedent but outside ML/CS. => the
  draft must state N9 NARROWLY and pre-empt Recht/Agarwal.

- **N3 (classic BO beta-calibration) DONE.** Fetched Srinivas GP-UCB (ICML2010, arXiv:0912.3995):
  β_t is a SINGLE-surrogate, time-indexed confidence-width schedule (0 hits "surrogate"/"ensemble"/
  "calibrat") — does NOT own N3. Lu et al. (TPAMI2023 "beyond a single GP") + Benechehab et al.
  bring multiple estimator classes into contact but fuse/winner-pick, never hold one shared β fixed
  to diagnose effective-conservatism mismatch. VERDICT: **N3 = NONE FOUND** (>80% classic BO
  doesn't own it; ~70% broadly; S2 rate-limit cut the Srinivas forward-cite route). Now the
  best-stress-tested claim, not the thinnest. Open: conformal/statistical-calibration lit unfetched
  (adjacent) → terminal "could not verify" candidate.

- **K/finite-width fork (N2+N5) DONE — the C-vs-D decider.** SHARP finding: the N5 "K-sweep proves
  finite-width artifact" argument is a **category error — ensemble cardinality K ≠ per-member width
  n**. Confirmed by code: `mbo.py:140-141` each member = 2-hidden-layer MLP width **HID=96**, ReLU;
  `K_ENS=5`, `TRAIN_EP=35`. The K-sweep varies the NUMBER of width-96 nets (2→10), not width.
  Jacot/Lee/Rahaman are about WIDTH→∞, mention ensembles 0 times. Our K-decline (0.95→0.18 as K
  rises) runs BACKWARD from Lakshminarayanan's & L/R/W's own K-sweeps (which improve/flatten) → most
  parsimonious read = small-K σ-estimation noise (K=2 → noisy std → weird LCB), NOT a width law.
  VERDICT: favors **D (taxonomy)** over C, but via K≠width + direction-reversal, not "finite-width."
  N2 stays NONE FOUND (pre-empted in STRENGTH not existence by L/R/W K-robustness). Confidence ~65%.
  Fetched Fort/Hu/Lakshminarayanan (loss-landscape, 1912.02757) + Lee et al. (wide nets as linear,
  1902.06720). IMPLICATION FOR DRAFT: the paper should NOT frame the K-sweep as finite-width
  evidence; the honest N5 verdict is that the NTK/spectral OBJECTION exists but the paper's own
  K-evidence for it is a category error → a reviewer risk to defuse, and a reason a WIDTH ablation
  (sweep HID) is the missing experiment. NOTE β=0 control (PROVENANCE.md:277 verbatim): "the gap is
  unchanged with pessimism off (β=0 ... CI [−0.02,0.10]) ... the edge is the surrogate's posterior
  MEAN, not σ-calibration or data" → supports mean-smoothness (C) over σ-mechanism (undercuts N4).
- **N7 (roughening beyond MBO) DONE.** VERDICT: **N7 = NONE FOUND at BROADEST scope** (BO/kernel/GP
  regression), ~20 API + 7 WebSearch queries, all negative. Structural: within-GP smoothness sweeps
  and cross-surrogate-class comparisons exist SEPARATELY, never combined into one controlled
  bidirectionally-manipulated causally-attributed experiment. Closest prior (NEW find): **Lim et al.,
  "Extrapolative BO with GP and NN Ensemble Surrogate Models" (Adv. Intell. Syst. 2021)** — real
  GP-vs-NN-ensemble BO comparison that HYPOTHESIZES the GP wins "due to the ability of GP to smoothly
  map out the uncertainty manifolds" but never manipulates smoothness (GP side = lengthscale-bounds
  widening only; NN side = none). => C can claim "first at all" to bidirectionally manipulate
  smoothness, citing Lim et al. as closest prior + naming what it stops short of. Confidence med-high.

- **N4 (sigma-scope + Ovadia) DONE.** DUE scope-catch HOLDS in paper's favor: DUE's "GP not
  automatically variance-growing" is about DEEP-KERNEL GPs (learned features); paper's exact-GP/SVGP
  use vanilla Matern on raw inputs (verified code/mbo.py) → corpus was over-citing DUE. Raw
  distance-aware mechanism (variance grows away; ensembles overconfident far) = PRIOR WORK FOUND
  (SNGP formal proof, DUQ two-moons). Causal "LCB + variance growth = implicit trust region
  explaining the win" = NONE FOUND, and CONTRADICTED by β=0 control (gap persists) + TuRBO (built an
  EXPLICIT fix because unconstrained variance growth under myopic acquisition is a PROBLEM, not a
  free mechanism). **Ovadia 2019 (fetched, arXiv:1906.02530) COMPLICATES "ensembles confidently
  wrong far from data"** — mixed MNIST/CIFAR, and its "far" = corruption-severity, not spatial
  distance. **β=0 NUMBERS NOT VERIFIABLE:** investigator's quick repro = 0.504→0.511 (flat/slightly
  UP), not the query's "0.51→0.47" — qualitatively agree gap survives σ-removal but exact
  numbers/direction unresolved (repro-gate being recomputed; recent git commits re eta2_surr=0.405).
  => N4 verdict: mechanism PARTLY prior-owned; offline-MBO-LCB-TR synthesis NONE FOUND; exact β=0 →
  terminal "could not verify".

- **Optimizer-reversal + candidate-A-credit DONE.** No offline-MBO paper owns A's "surrogate
  effect, NOT an optimizer effect" attribution: PGS fixes surrogate-focus, L/R/W holds optimizer as
  a fixed nuisance, Tan bundles both, Design-Bench doesn't decompose; Kim TMLR26 survey NAMES the
  attribution as unresolved. => **candidate A is UNDER-credited** by a "just an ablation" reading.
  BUT the "field innovates on the axis that doesn't matter" REVERSAL OVERCLAIMS: **Shahriari et al.
  2016 "Taking the Human Out of the Loop"** (most-cited BO survey, ~5948 cites; fetched) already
  holds AS DOCTRINE that surrogate choice matters more than acquisition/search choice. => honest
  framing: the paper FALSIFIES **PGS's LOCAL premise** ("search strategy is the neglected decisive
  axis in offline BBO"), NOT the field's belief. **The ONE sentence A owns:** "the first
  offline-MBO-specific, ANOVA-quantified attribution of the surrogate-vs-optimizer variance under a
  shared protocol." Open: corrected η²_opt (post budget-equalization + trust-region isolation) may
  move from 0.01 → could moot the reversal (N1 territory / repro-gate).

## ALL 6 DEPTH INVESTIGATORS DONE. Committed positions captured for N2/N5, N3, N4, N7, N9, and the
## optimizer-reversal/A-credit synthesis. Ready for step 6 reconciliation.

## STEP 8 GAP-FILL RETURNS
- **G1 (N6 fANOVA/AutoML) DONE — N6 stays NONE FOUND, STRENGTHENED.** Exhaustive fANOVA/AutoML
  search (21+ queries) found NO crossed model-class × optimizer two-way ANOVA/η² decomposition.
  Nearest-miss citations to NAME in related work (pre-empt reviewers): (1) **Hutter/Hoos/
  Leyton-Brown fANOVA (ICML 2014)** — "model class" = most important hyperparameter (31-58% var),
  but ONE-WAY on one fixed search method (SMAC); (2) **Moosbauer et al. (IEEE TEVC 2022)** —
  discusses then REJECTS fANOVA for OFAT, varies surrogate + sampling separately, no factorial; (3)
  **Liang et al. (npj Comp Materials 2021)** — THE closest structural analog: crossed surrogate ×
  acquisition grid, but descriptive ranking only (0 ANOVA/η² hits) + ONLINE BO not offline MBO.
  => N6 residual SHARPENED = crossed surrogate×optimizer factorial WITH two-way ANOVA/η²
  decomposition IN OFFLINE MBO (Liang crossed surrogate×acquisition online, no ANOVA; Hutter
  one-way). Draft MUST cite Hutter + Liang as nearest neighbors.

- **G2 (N5 width-ablation) DONE — N5 = PRIOR WORK FOUND (PARTIAL/CONFOUNDED), refines both ways.**
  Dai et al. 2022 resolved = "Sample-Then-Optimize Batch Neural Thompson Sampling" (NeurIPS 2022,
  arXiv:2210.06850): Deep-Ensemble critique is ALGORITHMIC (ensemble = reduced STO-BNTS w/o
  linearization term, loses theoretical guarantees); width-sweeps only its OWN net, never the
  ensemble. DECISIVE: **L/R/W Appendix D.1.2 / Fig A.2** rerun the full comparison INCLUDING the K=5
  ensemble at a smaller architecture (width 128→50, depth 3→2, K fixed), verbatim: *"even with the
  smaller architecture... the relative performance of the surrogate models mostly remains
  consistent. We still find that HMC often outperforms... deep ensembles."* => (a) partially
  pre-empts N5's "width untested" framing (the draft must position its proposed CLEAN width sweep as
  a de-confounded version of L/R/W's D.1.2, which confounds width+depth+activation and tests only 1
  alt size); (b) EMPIRICALLY WEAKENS the finite-width OBJECTION to C — shrinking the net does NOT
  rescue the ensemble, ranking is architecture-size-invariant over their range → the gap looks less
  like a pure width artifact. Combined with the K≠width category error: the N5 objection to a
  mechanism (C) paper is MORE ANSWERABLE than the K/finite-width locus assumed. Draft N5 verdict:
  the theoretical objection exists (NTK/spectral) but is partially answered by L/R/W D.1.2; the
  paper's K-sweep is NOT valid finite-width evidence.

- **G3 (N3/N4/N9) DONE — TWO honest downgrades + N9 confirmed.**
  - **N3: clean NONE FOUND → PARTIAL.** Dewolf/De Baets/Waegeman "Valid Prediction Intervals for
    Regression Problems" (AI Review 2022, arXiv:2107.00363) states N3's premise in GENERAL
    statistical form across 4 UQ classes at a shared confidence level ("uncalibrated models... either
    underestimate the uncertainty or produce overconservative prediction intervals"; normalize
    nonconformity by dispersion σ). 0 hits for acquisition/BO/pessimis/surrogate/LCB → does NOT apply
    to comparing surrogate CLASSES under a shared β in an acquisition. (Papadopoulos/Vovk/Gammerman
    2011 corroborates single-model.) => N3 residual = the OFFLINE-MBO ACQUISITION-COMPARISON
    application, NOT the general principle.
  - **N4: causal-mechanism sub-claim NONE FOUND → PARTIAL.** Fan/Wang/Ng/Hu "Minimizing UCB: a
    Better Local Search Strategy in Local BO" (NeurIPS 2024, arXiv:2405.15285) explicitly derives
    "minimizing UCB can be viewed as local strategy" (UCB small near samples, grows away). "trust
    region" only as TuRBO cites; "implicit" 0 hits. => the causal mechanism is OWNED (Fan 2024); the
    "LCB is an implicit trust region" NAMING + offline-MBO application remains available/novel.
  - **N9 forward-cite = NONE FOUND** (no third party calls Recht slope>1 an "audit strengthens"
    instance; ~10 queries) → reinforces N9 narrow-unclaimed; Recht/Agarwal stay must-pre-empt.

## ALL 3 GAP-FILLERS DONE. Net verdict changes vs pre-step-8: N3 → PARTIAL (general principle owned,
## offline-MBO application not), N4 mechanism → PARTIAL (Fan2024 owns mechanism, naming free), N5 →
## PARTIAL (L/R/W D.1.2 confounded width test), N6 stays NONE FOUND (fANOVA searched, strengthened).

## Process
8 fetchers dispatched (A-E readers over local text; W1 Kim/IGNITE/MS-DDEO; W2 AAAI-27+Gundersen;
W3 miss-catchers N2/N3/N6/N9). Awaiting completions. Tooling reality: CLI PDF fetch broken;
local curl+pdftotext is the ground truth; arXiv API + S2 flaky; OpenAlex ok.
