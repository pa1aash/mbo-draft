# Evidence digest — offline-mbo-novelty-audit-6d8cd4

Primary evidence index for the drafters. Every quote below is verbatim and grep-verified against the
fetched source body. Post-step-8 verdicts in brackets. Source note ids in [[...]].

---

### N1 — Confound taxonomy [PRIOR WORK FOUND (shape); residual = offline-MBO vocabulary + η²-net-up]
- Henderson owns the shape most tightly (RL-specific taxonomy; rankings reverse):
  > "We find that implementation differences which are often not reflected in publications can have dramatic impacts on performance."
  [[deep-reinforcement-learning-that-matters-aaai-2018-arxiv170906560]]
- Ferrari Dacrema names the confounds (recsys):
  > "Different factors contribute to such phenomena, including (i) weak baselines; (ii) establishment of weak methods as new baselines; and (iii) difficulties in comparing or reproducing results across papers."
  [[are-we-really-making-much-progress-a-worrying-analysis-of-recent-neural-recommen]]
- Musgrave (metric learning):
  > "the actual improvements over time have been marginal at best."
  [[a-metric-learning-reality-check-eccv-2020-arxiv200308505]]
- Lucic (GANs):
  > "most models can reach similar scores with enough hyperparameter optimization and random restarts."
  [[are-gans-created-equal-a-large-scale-study-neurips-2018-arxiv171110337]]
- Residual (NONE of them own): a two-way η² variance decomposition, and offline-MBO-specific confounds (target scaling, candidate/oracle protocol, ensemble size K, β-pessimism σ-mismatch). Confounds that net UP (P0-2 target scaling: raw targets "−2613 to +36" per FLAW_LEDGER P0-2).

### N2 — K-contingency of surrogate-class ranking [NONE FOUND; tension with L/R/W]
- L/R/W found the OPPOSITE (robustness), K∈{5,10}:
  > "the different ensembles perform similarly across many experiments, showing the robustness of our results to this hyperparameter." (Fig A.7)
  [[a-study-of-bayesian-neural-network-surrogates-for-bayesian-optimization-iclr-202]]
- Our K-sweep: task-normalized ensemble 0.95/0.52/0.32/0.18 at K=2/3/5/10 (flip at K=2, not tested by L/R/W).
- Abe (capacity, not ranking): a single larger model reproduces ensemble accuracy gains.
  [[deep-ensembles-work-but-are-they-necessary-neurips-2022-arxiv220206985]]

### N3 — Unmatched effective pessimism [PARTIAL: general principle owned; offline-MBO application NONE FOUND]
- General principle OWNED (conformal/calibration):
  > "the uncalibrated models do not approximately saturate the validity constraint. They either underestimate the uncertainty or produce overconservative prediction intervals." (+ normalize nonconformity by a dispersion σ)
  [[valid-prediction-intervals-for-regression-problems-artificial-intelligence-revie]]
- Closest offline-RL analog (different mechanism = target independence):
  > "shared pessimistic targets can paradoxically lead to value estimates that are effectively optimistic."
  [[why-so-pessimistic-estimating-uncertainties-for-offline-rl-through-ensembles-and]]
- Classic BO β_t is single-surrogate (does not own cross-class): Srinivas GP-UCB (0 hits surrogate/ensemble/calibrat).
  [[gaussian-process-optimization-in-the-bandit-setting-no-regret-and-experimental-d]]

### N4 — Distance-aware uncertainty / implicit trust region [PARTIAL: mechanism owned; naming+offline-MBO app free]
- Distance-aware mechanism OWNED:
  > SNGP: variance "increases monotonically toward 1 as x* moves further away from X_IND"; ensembles "assign low uncertainty to OOD examples even if far from the data."
  [[simple-and-principled-uncertainty-estimation-with-deterministic-deep-learning-vi]]
  > DUQ: "Deep Ensembles is uncertain only along the decision boundary, and certain elsewhere."
  [[uncertainty-estimation-using-a-single-deep-deterministic-neural-network-duq]]
- UCB-as-local-search MECHANISM OWNED (Fan et al. NeurIPS 2024):
  > "minimizing UCB can be viewed as local strategy." (UCB small near samples, grows away)
  [[minimizing-ucb-a-better-local-search-strategy-in-local-bayesian-optimization-neu]]
- DUE caveat is deep-kernel-specific (does NOT apply to the paper's vanilla-Matérn exact-GP/SVGP):
  > unconstrained deep-kernel GP is "certain even far away from the training data."
  [[on-feature-collapse-and-deep-kernel-learning-for-single-forward-pass-uncertainty]]
- Ovadia COMPLICATES "ensembles confidently wrong far from data" (its "far" = corruption severity, not spatial): deep ensembles are near-best under shift.
  [[can-you-trust-your-models-uncertainty-evaluating-predictive-uncertainty-under-da]]
- Paper's own β=0 control (undercuts σ-mediation): "the gap is unchanged with pessimism off (β=0 ... CI [−0.02,0.10]) ... the edge is the surrogate's posterior mean, not σ-calibration or data." (PROVENANCE.md:277) — exact numbers NOT VERIFIABLE.

### N5 — NTK / spectral bias finite-width objection [PARTIAL: objection real but K-sweep invalid + answered by L/R/W]
- Theory (width→∞): Jacot NTK [[180607572-neural-tangent-kernel-convergence-and-generalization-in-neural-network]]; Lee ∞-width→GP [[deep-neural-networks-as-gaussian-processes-iclr-2018-arxiv171100165]]; Rahaman spectral bias toward smooth [[on-the-spectral-bias-of-neural-networks-icml-2019-arxiv180608734]].
- Category error: K (ensemble cardinality) ≠ n (per-member width). Code: each member = 2-layer MLP, HID=96; K_ENS=5 (code/mbo.py:140-141,20-22). NTK/spectral papers mention ensembles 0 times.
- L/R/W already ran a K-fixed architecture-SIZE test and found ranking-invariance (answers the objection):
  > "even with the smaller architecture, we find that the relative performance of the surrogate models mostly remains consistent. We still find that HMC often outperforms other approximate inference methods such as deep ensembles." (App D.1.2)
  [[a-study-of-bayesian-neural-network-surrogates-for-bayesian-optimization-iclr-202]]
- Dai et al. 2022 critique of ensembles is algorithmic, not width-based; width-sweeps only its own net.
  [[sample-then-optimize-batch-neural-thompson-sampling-neurips-2022-arxiv221006850]]

### N6 — Crossed surrogate × optimizer factorial in offline MBO [NONE FOUND, strengthened]
- The field itself names the gap:
  > Kim survey: existing benchmarks do not distinguish "whether observed gains stem from superior surrogate modeling, improved optimization strategies, or mere chance."
  [[offline-model-based-optimization-comprehensive-review-kim-et-al-tmlr-2026-arxiv2]]
- Nearest neighbors (name to pre-empt): Hutter fANOVA (one-way; "model class" 31–58% variance, one fixed search method)
  [[an-efficient-approach-for-assessing-hyperparameter-importance-icml-2014-hutterho]];
  Liang et al. 2021 (crossed surrogate×acquisition, descriptive ranking only, online BO)
  [[benchmarking-the-performance-of-bayesian-optimization-across-multiple-experiment]].
- Tan/Chemingui/Design-Bench: 0 "factorial"/"ANOVA"/"crossed" hits. Tan varies 5 surrogates with gradient ascent FIXED.
  [[offline-model-based-optimization-by-learning-to-rank-iclr-2025-arxiv241011502]]

### N7 — Bidirectional smoothness manipulation [NONE FOUND at broadest scope]
- IGNITE smooths the NN only (one direction), never a GP:
  [[ignite-incorporating-surrogate-gradient-norm-to-improve-offline-optimization-tec]]
- Closest prior HYPOTHESIZES but never manipulates:
  > Lim et al. 2021: the GP's win "could be due to the ability of GP to smoothly map out the uncertainty manifolds."
  [[extrapolative-bayesian-optimization-with-gaussian-process-and-neural-network-ens]]
- MS-DDEO smooth-selects (closed-access → NOT VERIFIABLE at sentence level):
  [[ms-ddeo-offline-data-driven-evolutionary-optimization-based-on-model-selection-z]]

### N8 — Platform / library-version dependence [PARTIAL: phenomenon owned; offline-MBO + cross-platform residual]
- Henderson: implementation-swap variance ≥ a non-significant inter-algorithm effect (quote in N1).
- Nagarajan:
  > GPU-op nondeterminism variance "looks similar to the curves for exploration and weight initialization."
  [[the-impact-of-nondeterminism-on-reproducibility-in-deep-reinforcement-learning-n]]
- Gundersen (only a cited caveat, no own measurement):
  > "differences in software and hardware could have significant impact on results because of rounding errors in floating point arithmetic (Hong et al. 2013)."
  [[state-of-the-art-reproducibility-in-artificial-intelligence-proceedings-of-the-a]]
- Residual = offline MBO + the specific macOS-vs-Linux cross-platform axis + a stated same-order ratio.

### N9 — De-confounding direction (audit that strengthens) [NONE FOUND within ML/CS narrow]
- Genre norm runs the OTHER way:
  > Melis: "LSTMs outperform the more recent models, contra the published claims"; "effect sizes tend to be much smaller."
  [[on-the-state-of-the-art-of-evaluation-in-neural-language-models-iclr-2018-arxiv1]]
  > Robinson/Glen/Lee: clean shrink (DL→SVM competitive).
  [[validating-the-validation-reanalyzing-a-large-scale-comparison-of-deep-learning]]
- Partial precedents to PRE-EMPT:
  > Recht (relative, not absolute): "see diminishing returns but an increased advantage over earlier models."
  [[do-imagenet-classifiers-generalize-to-imagenet-icml-2019-arxiv190210811]]
  > Bressan (psychology; no effect-size stat): a stricter spec "came out stronger."
  [[confounds-in-failed-replications-bressan-frontiers-in-psychology-2019-doi103389f]]
- Our result (LANDED per commit 14e6bf5): η²_surr 0.37 → 0.405 after fixing target scaling + candidate protocol.

### Candidate contributions + the reversal
- PGS local premise (the named belief to falsify):
  > "offline BBO has focused on improving surrogate models while using fixed search strategies."
  [[offline-model-based-optimization-via-policy-guided-gradient-search-aaai-2024-arx]]
- Shahriari 2016 caps the reversal (surrogate > acquisition is already doctrine): [[taking-the-human-out-of-the-loop-a-review-of-bayesian-optimization-shahriari-et]]
- A's uniquely-owned sentence: "the first offline-MBO-specific, ANOVA-quantified attribution of the surrogate-vs-optimizer variance under a shared protocol" (no offline-MBO paper crosses both axes; L/R/W fixes optimizer as nuisance).

### AAAI-27 venue (fetched live)
- Verbatim topics: `ML: Evaluation, Benchmarking, Datasets & Analysis`; `ML: Bayesian Learning & Uncertainty Quantification`; `SO: Algorithm Configuration & Sampling-based Search`; `RU: Stochastic Optimization`. AAAI rule: pick the subarea of the MAIN contribution. [[aaai-27-areas-and-topics-aaai]]

---

## Consensus (assert confidently — 3+ independent sources)
1. The reality-check SHAPE is an established, accepted genre (Ferrari Dacrema, Henderson, Musgrave, Lucic, Agarwal, Melis).
2. Standard deep nets/ensembles are overconfident far from data; GP-style distance-aware variance grows away (SNGP, DUQ, DUE) — with the DUE deep-kernel caveat.
3. ∞-width nets → GPs; finite nets spectrally biased toward smooth (Jacot, Lee, Rahaman).
4. No offline-MBO work runs a crossed surrogate×optimizer factorial; the Kim survey names the gap (Design-Bench, Chemingui, Tan, Kim).
5. Implementation/environment variance ≈ method-difference variance in deep-RL benchmarks (Henderson, Nagarajan, Islam, Machado).

## Top contested pairs (both sides, for the Source Tensions section)
- L/R/W K-robustness vs. our K-flip (N2).
- SNGP/DUQ "ensembles confidently wrong far from data" vs. Ovadia's mixed shift results (N4).
- PGS "search strategy neglected" vs. Shahriari "surrogate > acquisition" doctrine (reversal).
- Agarwal "absence of significance ≠ absence of effect" (+Demšar N>10) vs. the paper's Design-Bench null (p=0.69, N=7).
- Reality-check "audit shrinks" (Melis/Musgrave/Lucic/Robinson) vs. our "audit strengthens" (0.405).
