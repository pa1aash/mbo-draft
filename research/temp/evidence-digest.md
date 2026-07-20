# Evidence digest — mbo-gauntlet-r4-adversarial-0f06f1

High-fidelity evidence index for the drafters. **129 claims** filtered from 443 (kept: high
confidence OR empirical/statistical evidence type, AND non-empty verbatim `quoted_support`),
grouped by atomic item, ranked within group by presence of hard numbers.

Read this rather than the fetcher summaries. Every quote below is verbatim from primary text.

---

### N6 — the crossed factorial none-found

- Safe Policy Improvement (SPI) is formally defined as a probabilistic guarantee that the trained policy's true performance is at least the baseline's performance minus a slack zeta, with probability at least 1-delta.  `1-delta, zeta`
  > P(rho(pi,M) >= rho(pi_b,M) - zeta | M ~ P_mdp(.|D)) >= 1-delta, where P_mdp(.|D) is the posterior probability of the MDP parameters, 1-delta is the high probability meta-parameter, and zeta is the approximation meta-parameter.
  [171206924-safe-policy-improvement-with-baseline-bootstrapping-2]

- COMs' full text contains zero genuine occurrences of factorial, crossed, eta-squared, variance-decomposition, main-effect, or two-way terminology, and its 4 raw 'anova' hits are false positives from author surnames in the bibliography (same Usmanova/Bozhanova pattern as Design-Bench and the comprehensive review, indicating these three papers share overlapping bio-design citations).  `113,284 characters extracted, 4 raw 'anova' substring hits, all false positives, 4 hits for 'ablation'`
  > 0 hits: factorial, crossed, analysis of variance, eta squared, variance decomposition, main effect, two-way
  [210706882-conservative-objective-models-for-effective-offline-model-based-optimi]

- RaM's ablation studies (Tables 8-10) vary ranking loss function (10 losses tested; ListNet best at average rank 2.0, RankCosine runner-up at 3.2) crossed with two internal modules (data augmentation, output adaptation) -- a self-ablation of one method's own components, not a field-wide surrogate-class x optimizer factorial with formal variance decomposition.  `10 losses tested, ListNet average rank 2.0, RankCosine average rank 3.2, 11 total 'ablation' hits in full text`
  > The results in Table 8 in Appendix F.2 show that ListNet is the best-performing loss with an average rank of 2.0 over 10 losses, and RankCosine is the runner-up with an average rank of 3.2. Ablation of main modules. To better validate the effectiveness of the two moduels, data augmentation and output adaptation, of our method, we perform ablation studies based on the top-performing loss functions.
  [offline-model-based-optimization-by-learning-to-rank]

- RaM's full text contains zero occurrences of factorial, crossed, ANOVA, eta-squared, variance-decomposition, main-effect, or two-way terminology despite being a 171,781-character paper with an extensive ablation appendix.  `171,781 characters extracted, 0 hits for all N6 target terms`
  > 0 hits for: factorial, crossed, ANOVA, analysis of variance, eta squared, variance decomposition, main effect, two-way
  [offline-model-based-optimization-by-learning-to-rank]

- Dao, Nguyen, Truong, and Hoang define an (alpha, omega)-sensitivity measure for an offline-MBO surrogate as the probability that a Gaussian perturbation of the surrogate's own parameters changes its average prediction by more than a threshold alpha.  `alpha, omega_mu, omega_sigma`
  > "The (alpha, omega)-sensitivity of a model g(x; phi) on the offline dataset D is defined as S_phi(alpha, omega) := Pr_{gamma~N(omega_mu, omega_sigma^2 I)}[A(phi, gamma) >= alpha], where A(phi, gamma) := E_{x~D}[g(x; phi+gamma)] - E_{x~D}[g(x; phi)]"
  [250304181-boosting-offline-optimizers-with-surrogate-sensitivity-batch8]

- High (alpha, omega)-sensitivity implies there exists a neighborhood of input at which the surrogate's prediction is brittle against small perturbations of its own parameters.  `delta`
  > "Suppose S_phi(alpha,omega) >= 1-delta with delta in (0,1). Then, with probability at least 1-delta over the space of random perturbation gamma, there exists x in D such that |g(x;phi+gamma) - g(x;phi)| >= alpha"
  [250304181-boosting-offline-optimizers-with-surrogate-sensitivity-batch8]

- Henderson et al. show that splitting 10 identical-hyperparameter random-seed trials into two groups of 5 produces statistically different score distributions on HalfCheetah, purely from seed variation.  `10, 5`
  > "We perform 10 experiment trials, for the same hyperparameter configuration, only varying the random seed... we find that the performance of algorithms can be drastically different. We demonstrate that the variance between runs is enough to create statistically different distributions just from varying random seeds."
  [henderson2018-deep-rl-that-matters-fulltext]

- Tan et al.'s Table 3 ('Versatility of ranking loss', ICLR 2025, arXiv:2410.11502) crosses 9 distinct methods/optimizers (BO-qEI, CMA-ES, REINFORCE, Grad. Ascent, CbAS, MINs, Tri-Mentoring, PGS, Match-OPT) against 2 surrogate training-loss types (MSE vs. ListNet) in a genuine 9x2=18-cell controlled factorial grid, with every method run under both loss types.  `9 methods, 2 loss types, 18 cells, 5 tasks`
  > In order to adapt the same parameters of the online optimizers (e.g., BO-qEI, Gradient Ascent) that optimize the trained model for a fair comparison, we also perform an output adaptation for ranking-based model after it is trained. All the replacements are conducted fixing their open-source codes by replacing MSE with ListNet when training the forward model.
  [241011502-offline-model-based-optimization-by-learning-to-rank]

- Table 3's crossed 9x2 grid reports only descriptive Score+/-std and a color-coded percentage 'Gain' per cell; exhaustive grep of the 18303-word extracted PDF text of arXiv:2410.11502v3 for factorial, crossed, ANOVA, analysis of variance, eta squared, main effect, variance decomposition, two-way, interaction effect, and attribution returns zero hits for every term -- confirming this is a NEAR-MISS   `0 hits across 10 statistical/factorial search terms, e.g. CMA-ES +12.3% gain on Ant, REINFORCE +28.2% gain on Ant`
  > Table 3: 100th percentile normalized score of different methods combined with the MSE or ListNet loss in Design-Bench, where positive and negative gain rates are Blue and Red.
  [241011502-offline-model-based-optimization-by-learning-to-rank]

- Table 3 excludes several forward methods (COMs, RoMA, IOM, BDI, ICT) from the MSE-vs-ListNet crossing because their loss functions structurally depend on prediction-value scales or per-sample weighting that cannot be substituted with a ranking loss, meaning the crossing is not comprehensive across all Design-Bench baselines.  `5 excluded methods: COMs, RoMA, IOM, BDI, ICT`
  > We exclude many forward methods due to the inapplicability of directly replacing MSE with ListNet. For example, COMs (Trabucco et al., 2021), RoMA (Yu et al., 2021), IOM (Qi et al., 2022) use the prediction values to calculate the loss function... while BDI (Chen et al., 2022) and ICT (Yuan et al., 2023) assign weight to each sample, thus MSE in these methods cannot be directly replaced with a ranking loss like ListNet.
  [241011502-offline-model-based-optimization-by-learning-to-rank]


### Citation fidelity — SNGP / distance-aware uncertainty

- A bootstrap ensemble of 32 networks (resampled data plus randomized initializations) tends to underestimate uncertainty and produce overconfident predictions in out-of-support regions far from the training data, on a toy 1D illustration, whereas a quantized normalized-maximum-likelihood (NML) estimator correctly outputs diffuse, high-uncertainty predictions there.  `32 ensemble members, 1-dimensional illustration`
  > Predictions from a bootstrap ensemble of 32 models. In out-of-support regions far from the data, the bootstrap ensemble tends to underestimate uncertainty and produce overconfident predictions.
  [210207970-offline-model-based-optimization-via-normalized-maximum-likelihood-est]

- SNGP defines 'input distance awareness' as the property that a model's uncertainty summary statistic u(x) equals a monotonic function of the distance between x and the training data domain, u(x) = v(d(x, X_IND)).
  > We say p(y|x) is input distance aware if there exists u(x) a summary statistic of p(y|x) that quantifies model uncertainty (e.g., entropy, predictive variance, etc) that reflects the distance between x and the training data with respect to ||.||_X, i.e., u(x) = v(d(x, X_IND))
  [200610108-simple-and-principled-uncertainty-estimation-with-deterministic-deep-l]

- SNGP's own experiments assert that standard deep ensembles are NOT input distance aware, and instead assign low uncertainty to OOD points that are far from training data.
  > deep ensembles (Figures 1b, 1g) and MC Dropout (Figures 1c, 1h) are based on dense output layers that are not distance aware. As a result, both methods quantify their predictive uncertainty based on the distance from the decision boundaries, assigning low uncertainty to OOD examples even if they are far from the data.
  [200610108-simple-and-principled-uncertainty-estimation-with-deterministic-deep-l]

- All SNGP empirical validation is on classification tasks (2D toy classification, CIFAR-10/100, ImageNet, CIFAR-10-C corruption, and BERT-based language understanding tasks) using Wide-ResNet and BERT architectures; the paper contains no regression experiments.
  > On a suite of vision and language understanding tasks and on modern architectures (Wide-ResNet and BERT), SNGP is competitive with deep ensembles in prediction, calibration and out-of-domain detection
  [200610108-simple-and-principled-uncertainty-estimation-with-deterministic-deep-l]

- DUQ's own figure and text state that standard Deep Ensembles fail to produce meaningful distance-aware uncertainty, becoming uncertain only near the decision boundary rather than far from training data.
  > DUQ is certain only on the data distribution, and uncertain away from it: the ideal result. Deep Ensembles is uncertain only along the decision boundary, and certain elsewhere.
  [200302037-uncertainty-estimation-using-a-single-deep-deterministic-neural-networ]

- DUQ attributes deep ensembles' failure to be distance-aware to a lack of diversity among ensemble members on simple, low-dimensional datasets.
  > Deep Ensembles are not able to obtain meaningful uncertainty on this dataset, because of a lack of diversity in the different models in the ensemble... even though Deep Ensembles have been successfully applied to many large datasets, they fail to estimate uncertainty well on the two moons dataset.
  [200302037-uncertainty-estimation-using-a-single-deep-deterministic-neural-networ]

- DUQ explicitly distinguishes its distance-based approach from ensemble/Monte Carlo methods, describing ensembles as methods that 'aim to find different explanations for the data and increase uncertainty when these disagree' rather than measuring distance to training data directly.
  > Our approach is distinct from both ensembles/Monte Carlo methods, which aim to find different explanations for the data and increase uncertainty when these disagree, and generative models which model the data distribution directly.
  [200302037-uncertainty-estimation-using-a-single-deep-deterministic-neural-networ]

- DUQ's uncertainty metric for its own model is distance to the closest class centroid in feature space, explicitly labeled a distance-based approach, unlike deep ensembles which use predictive entropy of the averaged output.
  > The uncertainty for DUQ is quantified as the distance to the closest centroid (max over the kernel distances), the uncertainty for Deep Ensembles is computed as the predictive entropy of the average output
  [200302037-uncertainty-estimation-using-a-single-deep-deterministic-neural-networ]


### Citation fidelity — Fan / UCB-as-local-search

- ELA characterizes problem landscapes via six low-level feature classes (y-Distribution, Meta-Model, Convexity, Local Search, Levelset, Curvature) computed via the flacco R package, from which high-level properties like multimodality, separability, and basin-size homogeneity are inferred.  `50 numerical measures, six categories of low-level features`
  > Six low-level feature classes were introduced, i.e., measures related to the distribution of the objective function values (y-Distribution), estimating meta-models such as linear or quadratic regression models on the sampled data (Meta-Model) and the level of convexity (Convexity).
  [171108921-automated-algorithm-selection-on-continuous-black-box-problems-by-comb]

- TuRBO's locality is not a diagnosed intrinsic property of acquisition functions but a deliberately imposed algorithmic mechanism (explicit trust regions with Nelder-Mead-style expand/shrink heuristics), drawing on a pre-existing class of trust-region methods from classical stochastic optimization.  `reference [57] = classical stochastic-optimization trust-region methods`
  > "To achieve principled local optimization in the gradient-free setting, we draw inspiration from a class of TR methods from stochastic optimization [57]."
  [191001739-scalable-global-optimization-via-local-bayesian-optimization]

- Fan et al. (2024) present MinUCB as their own novel algorithmic proposal (replacing GIBO's gradient-descent step with a UCB-minimization step), not as a report of a pre-existing 'reading of UCB-style acquisition as local search' that the audited paper can cite as an established prior finding.  `arXiv:2405.15285, published 24 May 2024, 5 hits for 'local search' in full text, 26 hits for 'minimizing UCB'`
  > "In this work, we develop the relationship between the steps of the gradient descent method and one that minimizes the Upper Confidence Bound (UCB)... Through this insight, we propose a new local Bayesian optimization algorithm, MinUCB, which replaces the gradient descent step with minimizing UCB in GIBO." (Abstract) / "This discovery is also meaningful as it opens up possibilities for new designs on local Bayesian optimization algorithms." (Introduction, line ~94-95)
  [240515285-minimizing-ucb-a-better-local-search-strategy-in-local-bayesian-optimi]

- Fan et al.'s UCB is defined as U CB(x) = mu_D(x) + beta*sigma_D(x) and is MINIMIZED because their primal objective is min f(x); the paper never discusses a lower confidence bound (LCB) or a maximization objective at all, so the audited paper's claim about an offline LCB being 'locally maximal at the data' cannot be directly attributed to Fan et al.'s stated results without an unstated mirror-trans  `UCB(x) = mu_D(x) + beta*sigma_D(x), eq (3) and (4) in paper, beta=3 in illustrative example`
  > "In this paper, we focus on the problem of minimizing a black-box function f(·): min_{x∈X} f(x)" (Sec 3.1, line 180-181) and "A commonly used concept in Bayesian Optimization is the upper confidence bound (UCB), which is defined as followed: UCB(x) = µ_D(x) + βσ_D(x)" (Sec 4, line 275-277) and "Previous work mainly focused on maximizing UCB to find the maximum value of a function [28]. However, it should be noted that UCB is also a natural bound for function f(·)... if we select x to be x* = arg min µ_D(x) + βσ_D(x
  [240515285-minimizing-ucb-a-better-local-search-strategy-in-local-bayesian-optimi]

- Fan et al.'s Theorem 1 proves MinUCB achieves a polynomial convergence rate to a genuine local optimum (gradient norm approaching 0), contingent on an INCREASING beta_t and batch-size schedule combined with continual active resampling every iteration -- i.e., the paper's central theoretical result is that the method does NOT get permanently stuck, which is the opposite of a 'paralysis' finding, an  `polynomial convergence rate O(sigma*d^1.5*T^-0.5*log^0.5(delta^-1)), Theorem 1, Assumption 1 and 2`
  > "According to Theorem 1, we need to iteratively increase the UCB coefficient βt and batch size b(1)t , b(2)t to guarantee the convergence of MinUCB." (Section 6, line 415-417) and "MinUCB will achieve the convergence rate of O(σd^(3/2) T^(-1/2) log^(1/2) δ^(-1))..." (Theorem 1 statement, line 392-397)
  [240515285-minimizing-ucb-a-better-local-search-strategy-in-local-bayesian-optimi]


### Citation fidelity — Demsar / Benavoli / power

- A preregistered metastudy of 159 interaction hypotheses from 82 recent psychology articles found the overall median statistical power to detect a typical-size interaction was .18.  `.18 median power, 159 studies, 82 articles, 194 interaction hypotheses, 17% at or above .80 power, 2017-2021`
  > The overall median power to detect interactions of a typical size is .18. ... Overall, only 17% of the studies had a power at or above .80, and the median power was .18
  [how-many-participants-do-i-need-to-test-an-interaction-conducting-an-appropriate]

- Median statistical power to detect the hypothesized interaction varied sharply by interaction shape: .87 for reversed interactions, .36 for fully attenuated interactions, and .11 for partially attenuated interactions.  `.87 median power (reversed, n=23), .36 median power (fully attenuated, n=54), .11 median power (partially attenuated, n=74), 65%, 19%, 0%`
  > the power to detect a +0.35 |−0.35 reversed interaction was at or above .80 in 65% of the cases, and the median power was = .87. ... the power to detect a +0.35|0.00 fully attenuated interaction was at or above .80 in 19% of the cases, and the median power was .36. ... the power to detect a +0.35|+0.20 (or, equivalently, a +0.35|+0.50) partially attenuated interaction was at or above .80 in none of the cases, and the median power was .11.
  [how-many-participants-do-i-need-to-test-an-interaction-conducting-an-appropriate]

- Only 4% of the 159 studies in the metastudy reported an adequate (shape-aware) power analysis for their interaction hypothesis; 45% reported no power analysis at all.  `4%, 45%, 65 studies with no analysis, 159 total studies`
  > Less than 5% of the studies used an adequate power analysis. Out of the 159 studies, 45% did not report a power/sensitivity analysis—specifically, 65 did not report any analysis, three did not specify the type of analysis, and three reported an incorrect “post hoc” power analysis
  [how-many-participants-do-i-need-to-test-an-interaction-conducting-an-appropriate]

- The authors developed three preregisterable methods to increase statistical power for detecting interactions without increasing sample size: one-tailed tests (+21% power gain), mixed within/between designs (+75% gain), and contrast analysis for fully attenuated interactions (+62% gain), validated via ~900 million simulated data sets.  `+21%, +75%, +62%, ~900,000,000 simulated datasets, 12 interaction types`
  > we use simulations (≈900,000,000 data sets) to generate power curves for the 12 types of interactions and test three approaches to increase power without increasing sample size: (a) preregistering one-tailed tests (+21% gain), (b) using a mixed design (+75% gain), and (c) preregistering contrast analysis for a fully attenuated interaction (+62% gain)
  [how-many-participants-do-i-need-to-test-an-interaction-conducting-an-appropriate]

- If focusing on larger versions of hypothesized interactions, the proportion of adequately powered studies rises to 27% and the median power rises to .25, still far below conventional .80 standard.  `27%, .25 median power`
  > If we repeat the analysis while focusing on larger versions of the hypothesized interactions (i.e., +0.50|−0.50, +0.50|0.00, and +0.50|+0.20), 27% of the studies had a power at or above .80, and the median power was .25.
  [how-many-participants-do-i-need-to-test-an-interaction-conducting-an-appropriate]

- With 5 runs, an improvement of SPR over DrQ on Atari 100k is not statistically significant, but the effect is real and becomes significant once more runs are evaluated, so claiming 'no improvement' from the low-n result would be misleading.  `5, 15`
  > "while improvement from SPR over DER with 5 to 15 runs is not statistically significant, claiming 'no improvement' would be misleading as evaluating more runs indeed shows that the improvement is significant."
  [210813264-deep-reinforcement-learning-at-the-edge-of-the-statistical-precipice]

- Benavoli, Corani, and Mangili's mean-ranks critique was published in the Journal of Machine Learning Research, volume 17, in 2016, not 2015.  `17, 2016`
  > "Journal of Machine Learning Research 17 (2016) 1-10" ... "Submitted 11/14; Revised 3/15; Published 3/16"
  [should-we-really-use-post-hoc-tests-based-on-mean-ranks]

- Benavoli et al. show concretely that for any pool of algorithms, the Wilcoxon-signed-rank-based decision about a specific pairwise comparison stays fixed, while the mean-ranks-test decision for the identical pair changes depending on which other algorithms are in the pool.  `0.0002`
  > "for any pool of algorithms C2, C4, Cx, Cy, we always report the same decision: C2, C4 are [significantly different]" [via Wilcoxon] versus the mean-ranks conclusion which "clearly depends on the pool of alternative classifiers"
  [should-we-really-use-post-hoc-tests-based-on-mean-ranks]

- In a worked example, the two-sided sign test comparing algorithms A and B has statistical power 0.94, while the mean-ranks post-hoc test comparing the identical A vs B (embedded in a larger algorithm pool) has power only 0.046 -- a roughly 20-fold power collapse purely from using mean-ranks instead of a pairwise test.  `0.94, 0.046, 0.05`
  > "the power of the two-sided sign test with alpha=0.05 is very high: 0.94... The power of the mean-ranks test is instead only 0.046."
  [should-we-really-use-post-hoc-tests-based-on-mean-ranks]

- Demšar's paper recommending Wilcoxon signed-rank and Friedman-plus-post-hoc mean-ranks tests for ML benchmark comparisons was published in JMLR volume 7, issue 1, in 2006 -- a decade before, and a distinct paper from, Benavoli et al.'s 2016 JMLR 17 rebuttal.  `7, 1, 30, 2006`
  > "Statistical Comparisons of Classifiers over Multiple Data Sets. Janez Demšar; 7(1):1-30, 2006."
  [statistical-comparisons-of-classifiers-over-multiple-data-sets]


### Citation fidelity — audit genre and the shrink premise

- Musgrave et al. find that metric-learning papers have drastically overstated improvements over classic contrastive/triplet losses, with some papers claiming relative improvements exceeding 100%, while controlled re-evaluation shows only marginal or flat progress from 2006 to 2019.  `100`
  > "papers have drastically overstated improvements over the two classic methods... with some claiming relative improvements exceeding 100% when compared with the contrastive loss... The trend appears to be a relatively flat line, indicating that the methods perform similarly to one another, whether they were introduced in 2006 or 2019."
  [200308505-a-metric-learning-reality-check]

- In a systematic recomputation of 500 primary-study effect sizes from 33 psychology meta-analyses, recomputed pooled effect sizes came out larger than originally reported in 19 cases and smaller in 14 cases, with the authors finding no evidence of systematic bias in either direction.  `19, 14, 33, 500`
  > "We did not find any evidence for systematic bias in meta-analytic results; we estimated 19 pooled effect sizes to be larger than originally reported and 14 to be smaller than originally reported."
  [reproducibility-of-individual-effect-sizes-in-meta-analyses-in-psychology-plos-o]

- 114 of 500 (23%) recalculated primary-study effect sizes showed discrepancies from the values reported in their source meta-analyses, with 31 (27% of discrepant cases) classified as large discrepancies.  `114, 500, 23, 62, 54, 21`
  > "In total, 114 out of 500 recalculated primary study effect sizes (23%) showed effect size discrepancies compared to the primary study effect sizes as reported in the meta-analytic articles. Of those 114 discrepancies, 62 were small (54%), 21 were moderate (18%), and 31 were large (27%)."
  [reproducibility-of-individual-effect-sizes-in-meta-analyses-in-psychology-plos-o]

- 14 of 33 (42%) reproduced meta-analyses showed discrepancies in their pooled effect size estimate, confidence interval, or heterogeneity estimate after recomputation.  `14, 33, 42`
  > "14 out of 33 meta-analyses (42%) showed discrepancies in either the pooled effect size estimate, its confidence interval, or" [heterogeneity estimate]
  [reproducibility-of-individual-effect-sizes-in-meta-analyses-in-psychology-plos-o]

- Recht et al. report a linear-fit slope of 1.69 for new-vs-original test accuracy on CIFAR-10.  `1.69, 72.7, 1.63, 1.76`
  > "accnew = 1.69 * accorig - 72.7%" ... "Computing a 95% confidence interval from 100,000 bootstrap samples gives [1.63, 1.76] for the slope"
  [190210811-do-imagenet-classifiers-generalize-to-imagenet]

- Recht et al. report a linear-fit slope of 1.11 for new-vs-original top-1 test accuracy on ImageNet.  `1.11, 20.2, 1.07, 1.19`
  > "accnew = 1.11 * accorig - 20.2%" ... "[1.07, 1.19] and [-26.0, -17.8] respectively for ImageNet" [slope and offset 95% CIs]
  [190210811-do-imagenet-classifiers-generalize-to-imagenet]

- A slope greater than 1 in Recht et al.'s regression means models with higher original accuracy see a smaller accuracy drop on new test sets -- i.e. higher-accuracy models are more robust to distribution shift between old and new test sets, not that any single model's claimed advantage over another model grew.  `1.69, 1.11`
  > "On both datasets, the slope of the linear fit is greater than 1. So models with higher original accuracy see a smaller drop on the new test sets. In other words, model robustness improves with increasing accuracy."
  [190210811-do-imagenet-classifiers-generalize-to-imagenet]

- Recht et al.'s own headline finding is a large accuracy drop (8-11 percentage points for common architectures) on replicated test sets relative to the original ones, placing this paper itself within the 'audits shrink the claimed effect' family rather than illustrating a growth pattern.  `8, 11`
  > "All models see a large drop in accuracy from the original test sets to our new test sets. For widely used architectures such as VGG and ResNet, the drop is 8% on CIFAR-10 and 11% on ImageNet."
  [190210811-do-imagenet-classifiers-generalize-to-imagenet]

- Henderson et al.'s 'Deep Reinforcement Learning that Matters' was published at AAAI 2018, not 2017, despite Semantic Scholar and many citing papers listing it as 2017.  `2018`
  > "Copyright c 2018, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved."
  [170906560-deep-reinforcement-learning-that-matters]

- The '2017' date commonly attached to Henderson et al. traces to the arXiv preprint posting date (Sept 2017), which is also the version Melis et al. (2017/2018) cite in their own reference list.  `1709.06560, 2017, 2018`
  > Melis et al. reference list: "Peter Henderson, Riashat Islam, Philip Bachman, Joelle Pineau, Doina Precup, and David Meger. Deep reinforcement learning that matters. arXiv preprint arXiv:1709.06560, 2017."
  [170906560-deep-reinforcement-learning-that-matters]


### Contradiction — ensemble sigma: error signal or distance signal

- The URL assigned for the 'loss landscape perspective' deep-ensembles paper (arXiv:2007.05134) actually resolves to a different paper, 'Revisiting One-vs-All Classifiers for Predictive Uncertainty and OOD Detection in Neural Networks' (Padhy, Nado, Ren, Liu, Snoek, Lakshminarayanan), not Fort/Huang/Lakshminarayanan's loss-landscape paper (correct ID: arXiv:1912.02757).  `arXiv:2007.05134, arXiv:1912.02757`
  > Title: Revisiting One-vs-All Classifiers for Predictive Uncertainty and Out-of-Distribution Detection in Neural Networks. Authors: Shreyas Padhy, Zachary Nado, Jie Ren, Jeremiah Liu, Jasper Snoek, Balaji Lakshminarayanan
  [200705134-revisiting-one-vs-all-classifiers-for-predictive-uncertainty-and-out-o]

- In a regression setting (neural-network force fields predicting atomic forces), ensemble/committee uncertainty correlates strongly with actual error on in-distribution validation data: Spearman rho = 0.90 (committee) and 0.91 (bootstrap-aggregation ensemble).  `0.90, 0.91`
  > the Spearman correlation coefficient between uncertainty and error over the validation data set is 0.90 for the committee and 0.91 for the bootstrap-aggregation ensemble.
  [230208805-deep-ensembles-vs-committees-for-uncertainty-estimation-in-neural-netw]

- Lakshminarayanan, Pritzel & Blundell (NeurIPS 2017) run a genuine ensemble-size (M) ablation and find that classification accuracy and uncertainty quality improve MONOTONICALLY as M increases from 1 to at least 10 networks, with diminishing but never negative returns.  `M=1: Top-1 22.166%, M=2: 20.462%, M=3: 19.709%, M=4: 19.334%, M=5: 19.104%, M=6: 18.986%`
  > We observe that as M increases, both the accuracy and the quality of predictive uncertainty improve significantly.
  [simple-and-scalable-predictive-uncertainty-estimation-using-deep-ensembles-full]

- Out-of-distribution predictive entropy (a proxy for uncertainty quality on unseen classes) improves as ensemble size increases, tested explicitly at M in {1, 5, 10}, on the MNIST-vs-NotMNIST and SVHN-vs-CIFAR10 OOD tasks.  `M in {1, 5, 10} (Figure 3/5)`
  > We observe that the predictive uncertainty improves on unseen classes, as the ensemble size increases.
  [simple-and-scalable-predictive-uncertainty-estimation-using-deep-ensembles-full]

- In the original deep-ensembles paper's own 1D toy regression benchmark, an NLL-trained ensemble's predictive standard deviation grows specifically as inputs move farther from the observed training data, demonstrating ensemble sigma CAN behave as a distance signal in at least one regression setting.  `5 networks`
  > ensemble combination improves performance, especially as we move farther from the observed training data.
  [161201474-simple-and-scalable-predictive-uncertainty-estimation-using-deep-ensem]

- In a seismic-facies semantic segmentation task, a 30-member deep ensemble's predictive-entropy uncertainty correlates with actual per-pixel prediction error at Pearson r=0.715 (+/-0.081) and Spearman rho=0.568 (+/-0.108).  `0.715, 0.081, 0.568, 0.108, 0.661, 0.114`
  > Deep Ensemble [10] 0.715 ± 0.081 0.568 ± 0.108 0.661 ± 0.114 [Table 2, Agreement with Prediction Error]
  [260501502-radmi-latent-information-aggregation-as-a-proxy-for-model-uncertainty]

- This result is domain-mismatched relative to the audited paper (dense per-pixel classification/segmentation, not scalar regression) and comes from a very recent (2026), not-yet-heavily-cited conference paper, warranting lower evidentiary weight than a peer-reviewed regression benchmark.  `2026`
  > Citation W. Stevens, M. Prabhushankar, and G. AlRegib, "RADMI: Latent Information Aggregation as a Proxy for Model Uncertainty," in IEEE International Conference on Image Processing (ICIP), Tampere, Finland, 2026. Review Date of Acceptance: April 30th 2026
  [260501502-radmi-latent-information-aggregation-as-a-proxy-for-model-uncertainty]

- Abe et al.'s central empirical claim is that ensemble diversity does not meaningfully contribute to OOD uncertainty quantification beyond what is explained by the relative improvement of an equivalent single larger model -- a claim about ensembles-vs-single-model, not small-K-vs-large-K.
  > ensemble diversity, by any metric, does not meaningfully contribute to an ensemble's uncertainty quantification on out-of-distribution (OOD) data, but is instead highly correlated with the relative improvement of a single larger model
  [deep-ensembles-work-but-are-they-necessary-full-text]

- Standard deep ensembles and weight-space Bayesian methods fail to properly account for uncertainty, especially 'in-between uncertainty', relative to function-space methods (SVGD, WGD) that more closely approach the HMC posterior, in a 1D BNN regression illustration.
  > The function-space methods (SVGD and WGD) approach the HMC posterior more closely, while the standard deep ensembles and weight-space methods fail to properly account for the uncertainty, especially the in-between uncertainty.
  [210611642-repulsive-deep-ensembles-are-bayesian]

- This paper -- not Abe et al. 2022 -- is the primary literature source that actually documents a specific, quantified direction ('quality improves with M') for ensemble size, making it the more accurate citation for any claim about 'the direction reported for ensemble quality' as a function of K.
  > We observe that as M increases, both the accuracy and the quality of predictive uncertainty improve significantly.
  [simple-and-scalable-predictive-uncertainty-estimation-using-deep-ensembles-full]


### Contradiction — ensemble size K and robustness

- Abe et al. 2022 does NOT run an ensemble-size (K) ablation anywhere in the paper -- zero hits for 'ensemble size', 'number of models', or 'size of the ensemble' across the full 35-page text.  `0 hits: 'ensemble size', 0 hits: 'number of models', 0 hits: 'size of the ensemble'`
  > We form homogeneous deep ensembles by combining 4 out of the 5 random seeds.
  [deep-ensembles-work-but-are-they-necessary-full-text]

- Heterogeneous ensembles (mixing different architectures at similar accuracy) and implicit ensembles (MC Dropout, BatchEnsemble, MIMO) are also examined by Abe et al., but again at fixed configurations, not swept ensemble sizes -- confirming the paper's axis of comparison is ensemble TYPE/composition, not ensemble CARDINALITY.  `12 implicit models (ImageNet), 6 implicit models (CIFAR10)`
  > The number of implicit models considered for ImageNet is 12 (2 MC dropout models, and 10 for MIMO models)... In total, we considered 6 implicit ensemble models (3 MC dropout models and 3 MIMO models).
  [deep-ensembles-work-but-are-they-necessary-full-text]

- Gao, Schulman, and Hilton give an empirically-validated closed-form functional relationship between gold (true) reward and distance from the initial policy as a policy is optimized against a proxy reward model, differing by optimization method.  `d := sqrt(KL(pi||pi_init)), alpha_bon, beta_bon, alpha_RL, beta_RL`
  > "We find empirically that for best-of-n (BoN) sampling, R_bon(d) = d(alpha_bon - beta_bon*d), and for reinforcement learning, R_RL(d) = d(alpha_RL - beta_RL*log(d))"
  [221010760-scaling-laws-for-reward-model-overoptimization]

- The paper attributes the nonmonotonic decay term (beta) in its scaling laws specifically to extremal Goodhart (out-of-distribution proxy failure), and the near-origin slope term (alpha) to regressional Goodhart (selection on correlated noise).  `beta term, alpha term`
  > "We expect extremal Goodharting to be primarily responsible for the nonmonotonicity of the gold RM scores in this paper, and is mostly responsible for the beta term, which in the limit of optimization, results in an unbounded loss of utility."
  [221010760-scaling-laws-for-reward-model-overoptimization]

- Deep ensembles were found to be the most robust UQ method to dataset shift among all methods benchmarked, with a small ensemble size (M=5) often sufficient.  `M=5`
  > Deep ensembles seem to perform the best across most metrics and be more robust to dataset shift. We found that relatively small ensemble size (e.g. M = 5) may be sufficient
  [190602530-can-you-trust-your-models-uncertainty-evaluating-predictive-uncertaint]

- L/R/W's default/main-result ensemble configuration uses 5 models, each trained on a random 80% subsample of the function evaluations -- this is the baseline against which their K=2/K=10 robustness check is a deviation, not a novel extension by the audited paper.  `5 models, 80% subsample`
  > ensemble: We use an ensemble of 5 models, each with the architecture explained above. Each model is trained on a random 80% of the function evaluations.
  [a-study-of-bayesian-neural-network-surrogates-for-bayesian-optimization]

- Larger ensemble size (4 to 64 members) yields no noticeable performance gain on D4RL Gym tasks with low data diversity, but yields a clear upward trend on the harder, more data-diverse antmaze-large tasks.  `ensemble sizes 1, 4, 16, 64`
  > In domains such as D4RL Gym where offline datasets are qualitatively similar to imitation learning datasets, larger ensembles do not result in noticeable gains. In domains such as D4RL antmaze which contain more data diversity, larger ensembles significantly improve the performance of agents.
  [220513703-why-so-pessimistic-estimating-uncertainties-for-offline-rl-through-ens]

- Li, Rudner & Wilson's 'A Study of Bayesian Neural Network Surrogates for Bayesian Optimization' (arXiv:2305.20028) was published at ICLR 2024, not 2023.  `v1: 31 May 2023, v2: 8 May 2024`
  > Comments: ICLR 2024. Code available at this https URL
  [230520028-a-study-of-bayesian-neural-network-surrogates-for-bayesian-optimizatio]

- On MNIST and SVHN classification, the paper sweeps ensemble size up to 14 networks (Figure 2) and finds ensembles significantly outperform MC-dropout at every matched M, with predictive uncertainty (NLL, Brier score, classification error) all improving as the number of networks increases.  `M swept 1-14 (Figure 2)`
  > Evaluating predictive uncertainty as a function of ensemble size M (number of networks in the ensemble or the number of MC-dropout samples): Ensemble variants significantly outperform MC-dropout performance with the corresponding M in terms of all 3 metrics.
  [simple-and-scalable-predictive-uncertainty-estimation-using-deep-ensembles-full]

- Abe et al. find that OOD performance improvements from ensembling are strongly determined by in-distribution (InD) performance, and are therefore not indicative of any distinct 'effective robustness' property of ensembles.
  > the OOD performance afforded by ensembles is strongly determined by their in-distribution (InD) performance, and -- in this sense -- is not indicative of any "effective robustness"
  [deep-ensembles-work-but-are-they-necessary-full-text]


### Normalization and effect-size methodology

- Jordan et al. explicitly identify min-max normalization over algorithms' own mean scores -- g(i,j) = (mu_ij - min_i' mu_i'j) / (max_i' mu_i'j - min_i' mu_i'j) -- as a normalization technique that does not correct for nonlinear scaling and is not robust to a single outlier algorithm setting the min or max.  `0, 1`
  > This normalization technique does not correct for nonlinear scaling of performance. As a result algorithms could be near 0 or 1 if there is an outlier algorithm that does very well or poorly. For example, one could introduce a terrible algorithm that just chooses one action the whole time. This makes the environment seem easier as all scores would be near 1 except for this bad algorithm. We would like the evaluation procedure to be robust to the addition of poor algorithms.
  [200616958-evaluating-the-performance-of-reinforcement-learning-algorithms-2]

- Fixed [0,1] range normalization based on absolute min/max scores per environment causes normalized performances to cluster in different (non-comparable) regions of [0,1] across environments, since the min/max endpoints (e.g., -100 to 10 vs. 10 to 1000) are arbitrary per-environment quantities unrelated to actual task difficulty.  `-100, 10, 1000, 20`
  > On the first environment, algorithms will tend to have a normalized performance near 1 and in the second case most algorithms will have a normalized performance near 0. So in the second environment algorithms will likely appear worse than algorithms in the first regardless of how close to optimal they are. This means the normalized performances are not really comparable.
  [200616958-evaluating-the-performance-of-reinforcement-learning-algorithms-2]

- The performance-ratio normalization technique is sensitive to the location and scale of the raw performance metric on each environment -- e.g., an environment with scores in [0,1] produces larger apparent differences than one with scores in [1000,1001] -- and combined with an arithmetic mean it can produce arbitrary rankings depending on which algorithm is used as the denominator.  `0, 1, 1000, 1001`
  > This ratio is sensitive to the location and scale of the performance metric on each environment, such that an environment with scores in the range [0,1] will produce larger differences than those on the range [1000,1001]. ... A critical flaw in the performance ratio is that it can produce an arbitrary ordering of algorithms when combined with the arithmetic mean, meaning a different algorithm in the denominator could change the relative rankings.
  [200616958-evaluating-the-performance-of-reinforcement-learning-algorithms-2]

- A subset of ImageNet ensembles used M=5 models (fixed by available seed count for those architectures), not as a systematic K-sweep against the M=4 CIFAR10 setup.  `M=5 (ImageNet subset)`
  > Finally, we show percentage increases for Imagenet on analogous M = 5 ensembles of AlexNet, ResNet 50, and ResNet 101 models
  [deep-ensembles-work-but-are-they-necessary-full-text]

- Semantic Scholar's paper-search and citation APIs returned HTTP 429 (Too Many Requests) on every attempt during this session, forcing exclusive reliance on OpenAlex for the forward-citation walk -- a methodological deviation from the ideal Semantic-Scholar-first protocol, noted for reproducibility.  `429 error code`
  > Semantic Scholar API response: {"message": "Too Many Requests. Please wait and try again or apply for a key for higher rate limits.", "code": "429"}, persisted across multiple retries with cooldowns.
  [n6-extension-check-synthesis-r4-adversarial]

- A performance measure should assume a wide variation of values and not cluster in a narrow range (e.g., 0.98 to 1.0), because narrow-range magnitude measures lose interpretability -- an implicit critique of raw-score/min-max-style measures that can compress most entrants into a narrow band.  `0.98, 1.0`
  > assuming a wide variation of values such that, for example, typical values do not only range between 0.98 and 1.0
  [160503560-coco-performance-assessment-2]

- A worked rock-paper-scissors example shows that merely adding a redundant duplicate copy of one agent to the comparison population shifts other agents' Elo ratings by 63 points in opposite directions, despite no change in the true underlying skill of any agent -- demonstrating that composition-sensitive aggregation statistics can be manipulated or accidentally distorted by duplicate/near-duplicate  `63, -63, 0`
  > The three agents exhibit rock-paper-scissors dynamics; their Elo ratings (normalized to sum to zero) are all zero. However, adding a second copy of agent C decreases the Elo rating of agent A and increases the Elo rating of agent B... That is, the Elo ratings of agents A and B are easily manipulated by changing the structure of the population.
  [180602643-re-evaluating-evaluation]

- Normalizing the nonconformity measure by a k-NN-distance-based expected-accuracy estimate produces predictive regions that are, in general, much tighter than those produced by the standard (unnormalized) regression nonconformity measure.  `six benchmark datasets, six novel nonconformity measures`
  > As a result, the predictive regions produced by our measures are in general much tighter than those produced by the standard regression measure.
  [14013880-regression-conformal-prediction-with-nearest-neighbours]

- The paper demonstrates extrapolation error positively via a graded battery of three dataset-construction protocols (final buffer, concurrent, imitation) that vary the distributional mismatch between the batch and the evaluation policy, showing the DDPG value estimate diverges (to 10^4-10^5 scale) as mismatch increases.  `10^4, 10^5, three batch protocols`
  > "These experiments show extrapolation error can be highly problematic"
  [181202900-off-policy-deep-reinforcement-learning-without-exploration]

- The ALE paper defines 'inter-algorithm normalization,' the min-max formula z_{g,i} = (s_{g,i} - min_i s_{g,i}) / (max_i s_{g,i} - min_i s_{g,i}) using only the score range of the compared algorithms/methods themselves -- this is the origin of the exact min-max-over-compared-entities normalization technique later critiqued as outlier-fragile by Jordan et al. 2020.  `0, 1`
  > A third alternative is to normalize using the scores achieved by the algorithms themselves. Given n algorithms, each achieving score s_{g,i} on game g, we define the inter-algorithm score using the score range [min_i s_{g,i}, max_i s_{g,i}]. By definition, z_{g,i} in [0,1].
  [12074708-the-arcade-learning-environment-an-evaluation-platform-for-general-agen]


### Budget, compute-matching and benchmarking norms

- Kerschke & Trautmann build an automated algorithm-selection model for continuous black-box optimization that selects among a portfolio of OPTIMIZERS (solvers), not among surrogate/objective models, using Exploratory Landscape Analysis (ELA) features.  `requires less than half of the resources of the portfolio's single best solver`
  > the model allows for selecting the best suited optimization algorithm within the considered set for unseen problems prior to the optimization itself based on a small sample of function evaluations.
  [171108921-automated-algorithm-selection-on-continuous-black-box-problems-by-comb]

- Prior reported results on the Atari 100k benchmark are computed mostly from 3-5 runs per algorithm, while reliably detecting statistically significant performance differences requires roughly 50-100 runs.  `3, 5, 10, 20, 50, 100`
  > "Prior reported results on this benchmark have been computed mostly from 3 ... or 5 runs ..., and more rarely, 10 ... or 20 runs" and separately "we find that this number is closer to 50-100 runs in Atari [for reliably assessing performance differences]".
  [210813264-deep-reinforcement-learning-at-the-edge-of-the-statistical-precipice]

- This 2024 paper computes fitness-landscape features on both the true objective and a Kriging surrogate model during surrogate-assisted multi-objective evolutionary optimization, finding surrogate-landscape features differ significantly from true-landscape features yet remain highly correlated.  `only 33 out of 55 bbob-biobj functions retained when Kriging surrogate used (Figure 2)`
  > Our results indicate that surrogate landscape features differ significantly from the true landscape features and that these features vary during the course of a run. Despite these differences, the surrogate and true landscape often show a high correlation.
  [240406557-temporal-true-and-surrogate-fitness-landscape-analysis-for-expensive-b]

- DAA methods can deteriorate before even a single epoch of the offline preference dataset is completed, indicating overoptimization can occur very early in offline-style training without iterated online sampling against a static proxy.  `one epoch`
  > "we find that DAA methods deteriorate not only across a wide range of KL budgets but also often before even a single epoch of the dataset is completed"
  [240602900-scaling-laws-for-reward-model-overoptimization-in-direct-alignment]

- The paper cites prior ELA-based selection work distinguishing 'funnel-shaped' landscapes with global structure from randomly-arranged local optima via nearest-better clustering, and shows this distinction is achievable with a budget as low as 50xd sample points.  `50 x d observations`
  > even low budgets of 50xd observations (d being the problem dimensionality) -- i.e., a sample size that is close to the size of an evolutionary algorithm's initial population -- is sufficient for such a distinction.
  [171108921-automated-algorithm-selection-on-continuous-black-box-problems-by-comb]

- This paper does not measure or discuss input-space distance-to-training-data as a construct at all (only cosmetic mentions of KL-divergence between output distributions in an ablation), and offers no direct evidence on whether ensemble sigma correlates with distance vs. error.
  > we also computed the KL-divergence and other distances between the output probability [distributions, for simplicity]
  [191202757-deep-ensembles-a-loss-landscape-perspective]

- Comparing metaheuristics based on an equal number of objective function evaluations is described as 'standard practice' in the metaheuristics/swarm-optimization literature, establishing budget-matched comparison as a field-wide norm rather than an ad hoc control this batch is only inferring.
  > "Comparing various metaheuristics based on an equal number of objective function evaluations has become standard practice."
  [how-does-the-number-of-objective-function-evaluations-impact-our-understanding-o]

- COCO/BBOB prescribes reporting both fixed-target and fixed-budget views and an anytime assessment over the entire run, rather than measuring at one chosen budget, precisely because runtime/performance comparisons can be budget-sensitive.
  > "There is no predefined budget... the experimental procedure is budget-free... This also implies an anytime assessment approach: the performance is not (only) measured after some given runtime or fixed budget or after reaching some given target but over the entire run of the solver."
  [coco-platform-comparing-continuous-optimizers-black-box-fulltext]

- When given more function-query data, deep ensemble BO performance improves substantially, consistent with the data-diversity (not ensemble-size) explanation for their baseline underperformance.
  > the performance of deep ensembles is greatly improved, consistent with the explanation that their poor performance on many tasks is due to limited data.
  [a-study-of-bayesian-neural-network-surrogates-for-bayesian-optimization]

- Raising the evaluation budget can significantly affect the final verdict of a metaheuristics comparison, i.e. which algorithm is judged best changes with the number of function evaluations allowed.
  > "Even though the final impact varies based on current algorithm selection, it may significantly affect the final verdict of metaheuristics comparison."
  [how-does-the-number-of-objective-function-evaluations-impact-our-understanding-o]


### Mechanism — extrapolation, Goodhart, off-support

- At initialization, in the infinite-width limit, the output functions of a depth-L fully-connected network converge in law to iid centered Gaussian processes (Proposition 1).  `depth L, n_1,...,n_{L-1}→∞`
  > "the output functions f_θ,i for i = 1,...,n_L tend to iid Gaussian processes in the infinite-width limit... Proposition 1. For a network of depth L at initialization, with a Lipschitz nonlinearity σ, and in the limit as n_1,...,n_{L-1}→∞, the output functions f_θ,k... tend (in law) to iid centered Gaussian processes of covariance Σ^(L)."
  [180607572v4-neural-tangent-kernel-convergence-and-generalization-ntk-adversarial]

- Empirically, increasing network width from n=500 to n=10000 makes the NTK show less variance, greater smoothness, and greater stability ('less inflation') across 200 steps of training.  `n=500, n=10000, 200 steps`
  > "For the wider network, the NTK shows less variance and is smoother... After 200 steps of training, we observe that the NTK tends to 'inflate'. As expected, this effect is much less apparent for the wider network (n=10000) where the NTK stays almost fixed, than for the smaller network (n=500)."
  [180607572v4-neural-tangent-kernel-convergence-and-generalization-ntk-adversarial]

- The paper contains zero mentions of ensembles, acquisition functions, surrogates, or Thompson sampling -- it supplies no direct argument about Bayesian-ensemble posterior jaggedness or model-based optimization.  `0 hits (ensemble), 0 hits (acquisition), 0 hits (surrogate), 0 hits (Thompson), 2 hits (posterior)`
  > Grep of research/raw/txt/1806.07572-ar5iv-v4-adversarial-refetch.txt: "ensemble", "acquisition", "surrogate", "Thompson" each return 0 hits; "posterior" returns only 2 hits.
  [180607572v4-neural-tangent-kernel-convergence-and-generalization-ntk-adversarial]

- Conservative Q-Learning (CQL) is proven to be 'gap-expanding': at large enough regularization strength, the learned Q-function widens (never narrows or inverts) the gap between in-distribution and out-of-distribution action values relative to the true gap.  `alpha_k`
  > "Theorem 3.4 (CQL is gap-expanding). At any iteration k, CQL expands the difference in expected Q-values under the behavior policy pi_beta(a|s) and mu_k... for large enough values of alpha_k"
  [200604779-conservative-q-learning-for-offline-reinforcement-learning]

- In deterministic finite MDPs, extrapolation error can be formally decomposed via a Bellman-like recursive equation in terms of the divergence between the true and batch-empirical transition distributions, and batch-constrained Q-learning is proven to converge to the optimal value function under the batch-induced MDP.  `epsilon_MDP(s,a) = Q^pi(s,a) - Q^pi_B(s,a)`
  > "Theorem 1. Performing Q-learning by sampling from a batch B converges to the optimal value function under the MDP M_B."
  [181202900-off-policy-deep-reinforcement-learning-without-exploration]

- The audited AAAI-27 paper's bib entry for gao2022reward contains a page-range error independent of the year/key mismatch: it lists pages 10909-10934, but the true PMLR v202 pages (verified against proceedings.mlr.press/v202/gao23h.html) are 10835-10866.  `true pages 10835-10866, audited bib pages 10909-10934, ICML 2023, PMLR vol 202`
  > PMLR record: 'Proceedings of the 40th International Conference on Machine Learning, PMLR 202:10835-10866, 2023.' BibTeX: '@InProceedings{pmlr-v202-gao23h, ... pages = {10835--10866}, year = {2023}, ...}'
  [scaling-laws-for-reward-model-overoptimization]

- A two-layer ReLU MLP trained by gradient descent in the NTK regime converges, along any ray from the origin outside the training support, to a linear function of distance along that ray, at rate O(1/t).  `O(1/t) convergence rate, two-layer network`
  > "As t -> infinity, f(x0 + hv) - f(x0) -> beta_v * h for any h > 0, where beta_v is a constant linear coefficient... for t = O(1/epsilon), we have |f(x0+hv)-f(x0))/h - beta_v| < epsilon."
  [200911848-how-neural-networks-extrapolate-from-feedforward-to-graph-neural-net]

- For least-squares regression, the infinite-width network function f_θ(t) follows a linear differential equation, so it remains Gaussian at every training time t, not just at initialization.
  > "For a least-squares regression loss, the network function f_θ follows a linear differential equation in the infinite-width limit, and the eigenfunctions of the Jacobian are the kernel principal components of the input data."
  [180607572v4-neural-tangent-kernel-convergence-and-generalization-ntk-adversarial]

- Prior offline RL methods that do not explicitly constrain or regularize the Q-function may fail to be gap-expanding, allowing out-of-distribution actions to have higher learned values than the true gap would justify.
  > "When function approximation or sampling error makes OOD actions have higher learned Q-values, CQL backups are expected to be more robust... prior offline RL methods that do not explicitly constrain or regularize the Q-function may not enjoy such robustness properties."
  [200604779-conservative-q-learning-for-offline-reinforcement-learning]

- The same paper shows this uncertainty-error correlation degrades substantially when evaluated on genuinely out-of-distribution structures (4x1 surface reconstructions structurally distinct from the bulk training data), especially at the level of individual atoms rather than aggregated layers.
  > the correlation between uncertainty and error within the topmost layers is not good enough to identify the most problematic atoms directly... the skill of the uncertainty in the forces as a proxy for error improves with the cardinal of the set of atoms considered: it is still good when applied to a whole layer, but less so for individual atoms.
  [230208805-deep-ensembles-vs-committees-for-uncertainty-estimation-in-neural-netw]


### Mechanism — pessimism, safe improvement, offline RL

- SPIBB's Theorem 2 proves the trained policy pi_spibb is a zeta-approximate safe policy improvement over the baseline pi_b with high probability 1-delta, where zeta is given in closed form depending on the bootstrapping threshold N_wedge and the empirical value gap in the MLE MDP.  `N_wedge, 1-delta`
  > Theorem 2 (Safe policy improvement). ... pi_spibb is a zeta-approximate safe policy improvement over the baseline pi_b with high probability 1-delta.
  [171206924-safe-policy-improvement-with-baseline-bootstrapping-2]

- Lyu, Tan, Xue, He, Huang, Zhang & Qian (arXiv:2603.04000, March 2026) prove that pairwise ranking losses admit strictly tighter generalization bounds than MSE regression for the optimization-oriented ranking error in offline MBO.  `Theorem 5, Theorem 7, Lemma 6`
  > By comparing Theorem 5 and 7, we can find that the pairwise ranking loss provably outperforms MSE in offline MBO, when the following conditions are satisfied...
  [260304000-on-the-learnability-of-offline-model-based-optimization-a-ranking-pers]

- The bib entry cites this work as NeurIPS 2022, matching the actual publication venue (arXiv submitted May 2022, accepted NeurIPS 2022); no citation-year trap exists for ghasemipour2022pessimistic.  `arXiv:2205.13703`
  > N/A -- bibliographic metadata cross-check (arXiv:2205.13703, submitted 2022-05-27; audited paper's references.bib lists booktitle={Advances in Neural Information Processing Systems (NeurIPS)}, year={2022}).
  [220513703-why-so-pessimistic-estimating-uncertainties-for-offline-rl-through-ens]

- Bootstrap and permutation significance tests are unreliable and produce inflated false-positive rates at small sample sizes, because the sample is used as a noisy estimate of the true underlying distribution.  `N = 50, N = 10`
  > it seems clear that the bootstrap test should never be used for sample sizes below N = 50 and the permutation test should never be used for sample sizes below N = 10. The bootstrap test in particular, uses the sample as an estimate of the true performance distribution. A small sample is a very noisy estimate, which leads to very high false positive rates.
  [a-hitchhikers-guide-to-statistical-comparisons-of-reinforcement-learning-algorit]

- Welch's t-test is the most robust test to assumption violations among those studied but still exceeds the nominal false-positive rate (alpha* > alpha, approx 0.1 vs 0.05) whenever at least one compared distribution is skewed or bimodal, especially at small sample sizes (N<10).  `alpha = 0.05, alpha* approx 0.1, N < 10`
  > The t-test and the Welch's t-test were found to be more robust than others to violations of their assumptions. However, alpha* was found to be slightly above the required level (alpha* > alpha) when at least one of the two distributions is skewed (alpha* approx 0.1) no matter the sample size, and when one of the two distributions is bimodal, for small sample sizes N < 10.
  [a-hitchhikers-guide-to-statistical-comparisons-of-reinforcement-learning-algorit]

- The paper never discusses acquisition functions, Bayesian optimization, pessimism, lower/upper confidence bounds, or surrogate models in an optimization-search context anywhere in its ~23,000-word body (0 grep hits for all these terms).  `0 hits across 6 search terms, 23271 words total`
  > N/A -- grep-based absence finding, not a quotable passage; confirmed via `grep -in` for 'acquisition', 'bayesian optimization', 'pessimis', 'surrogate model', 'lower confidence bound', 'upper confidence bound' returning 0 hits.
  [valid-prediction-intervals-for-regression-problems]

- Chemingui et al.'s Related Work section names the specific prior methods it characterizes as fixed-search-strategy-with-improving-surrogate: Trabucco et al. 2021 (COMs), Yu et al. 2021a, and Fu and Levine 2021.
  > The second family learns a surrogate model from the offline data which is then optimized directly using gradient updates (Trabucco et al. 2021; Yu et al. 2021a; Fu and Levine 2021). Conservative regularizers are typically designed to avoid overestimation for inputs which are far away from the offline training data.
  [offline-model-based-optimization-via-policy-guided-gradient-search]

- Thomas, Theocharous & Ghavamzadeh's HCPI algorithm guarantees that, for any user-chosen performance lower bound and confidence level, the probability the algorithm returns a policy performing below that lower bound is at most the chosen confidence level -- the founding formal instantiation of a 'no regression below a bound, with high confidence' guarantee for offline/batch policy improvement.
  > the user may select any performance lower-bound and confidence level and our algorithm will ensure that the probability that it returns a policy with performance below the lower bound is at most the specified confidence level.
  [high-confidence-policy-improvement]

- Jin, Yang & Wang decompose offline-RL suboptimality into three sources: intrinsic uncertainty (dataset fails to cover the optimal trajectory), spurious correlation (dataset covers an unrelated, high-reward trajectory by chance, misleading the learned policy), and optimization error.
  > two challenges arise: (i) the intrinsic uncertainty, that is, the dataset possibly fails to cover the trajectory induced by the optimal policy ... and (ii) the spurious correlation, that is, the dataset possibly happens to cover a trajectory unrelated to the optimal policy, which by chance induces a large cumulative reward and hence misleads the learned policy.
  [201215085-is-pessimism-provably-efficient-for-offline-rl-2]

- Training each ensemble member's target network completely independently (no shared targets), then aggregating via mean-minus-standard-deviation (MSG algorithm), restores genuine pessimism and matches or significantly exceeds prior SOTA on challenging D4RL antmaze tasks and RL Unplugged.
  > Crucially, ensembles trained with independent target values will always provide pessimistic value estimates. The pessimistic lower-confidence bound (LCB) value estimate ... is then used to update the policy being trained ... MSG matches, and in the more challenging domains such as antmazes, significantly exceeds the prior state-of-the-art.
  [220513703-why-so-pessimistic-estimating-uncertainties-for-offline-rl-through-ens]


### Conformal coverage and interval validity

- This vault already contains 3 other independently-fetched copies of this exact paper from a prior audit pass, all of which analyzed only the paper's separate 'five surrogates, gradient-ascent held fixed' Spearman-correlation study (a different experiment, near line 283 of the PDF) and none of which mention or analyze Table 3 -- meaning the prior audit pass's N6 verification of this paper was incom  `3 prior duplicate notes, 1 new finding (Table 3) not covered by any of them`
  > N/A (vault search result, not a quoted passage from the source)
  [241011502-offline-model-based-optimization-by-learning-to-rank]

- Conformal Bayesian optimization is motivated by 'feedback covariate shift': because BayesOpt adaptively selects queries, the query (test) distribution differs systematically from the training distribution, and UCB-style acquisition can select points in regions where the surrogate model's predictions have no coverage guarantee.  `alpha=1/sqrt(8) (example)`
  > The upper-confidence bound (UCB) acquisition function selects the next query far from any training data, where we cannot guarantee reliable predictions. ... conformal UCB directs the search to the region where conformal predictions are guaranteed coverage of at least (1-alpha).
  [221012496-1-introduction]

- The naive heuristic of training an ensemble via MSE and using the empirical variance across members as the uncertainty estimate significantly underestimates true predictive uncertainty compared to an ensemble that learns a heteroscedastic NLL-based variance.  `80%, 20%, 5 networks`
  > the empirical variance obtained from NNs which do not learn the predictive variance (specifically, five NNs trained to minimize MSE) consistently underestimates the true predictive uncertainty. For instance, the 80% prediction interval contains only 20% of the test observations
  [161201474-simple-and-scalable-predictive-uncertainty-estimation-using-deep-ensem]

- Stanton, Maddox & Wilson correctly cite Tibshirani et al. (2019) specifically for the importance-weighting mechanism used to correct feedback-induced covariate shift in conformal Bayesian optimization, matching the actual content of Tibshirani et al.'s weighted conformal prediction result.
  > The importance weights w account for covariate shift (Tibshirani et al., 2019), and w_i=1/(n+1) for all i in the special case where D union {(x_n,y_n)} is fully exchangeable (e.g. IID).
  [221012496-1-introduction]

- The tutorial generalizes to distribution drift and states that weighted conformal procedures always satisfy marginal coverage as an upper bound property, but are only EXACT (i.e., achieve the nominal 1-alpha coverage tightly) when the magnitude of the distribution shift is known.
  > The following theory provides some justification for such weighted conformal procedures; in particular, they always satisfy marginal coverage, and are exact when the magnitude of the distribution shift is known.
  [a-gentle-introduction-to-conformal-prediction-and-distribution-free-uncertainty]

- Lemma 2 shows that independent draws Z_i ~ P_i where each P_i is absolutely continuous w.r.t. P_1 are weighted exchangeable with weight functions equal to the Radon-Nikodym derivatives (likelihood ratios) dP_i/dP_1 -- this is the formal bridge connecting covariate shift to weighted exchangeability.
  > Let Z_i ~ P_i, i=1,...,n be independent draws, where each P_i is absolutely continuous with respect to P_1, for i>=2. Then Z_1,...,Z_n are weighted exchangeable, with weight functions w_1=1, and w_i = dP_i/dP_1, i>=2.
  [190406019-conformal-prediction-under-covariate-shift-2]


### Design of experiments — interaction methodology

- SGD-trained finite-width network test performance empirically approaches NNGP test performance as width increases, but the authors state this would only be 'guaranteed' if the network were trained in a fully Bayesian fashion rather than by SGD.  `MNIST, CIFAR-10`
  > "were the neural networks trained in a fully Bayesian fashion, rather than by SGD, the approach to NNGP in the large width limit would be guaranteed. There is recent work suggesting that SGD can implement approximate Bayesian inference..."
  [171100165-deep-neural-networks-as-gaussian-processes]

- RoMA (Yu, Ahn, Song, Shin, NeurIPS 2021) is the 'Yu et al. 2021a' work Chemingui 2024 and the 2025 Comprehensive Review both name as an example of the surrogate-focused, smoothness-prior family; RoMA uses a local smoothness prior to adapt the proxy model, then searches via gradient ascent -- confirming the family characterization.  `7 hits for 'smoothness prior', 4 hits for 'gradient ascent'`
  > We consider the problem of searching an input maximizing a black-box objective function given a static dataset of input-output queries. A popular approach to solving this problem is maintaining a proxy model, e.g., a deep neural network (DNN), that approximates
  [211014188-roma-robust-model-adaptation-for-offline-model-based-optimization]

- L/R/W attribute deep ensembles' poor BO performance to a data-diversity mechanism: in low-data regimes the loss landscape is smooth so independently trained models converge to similar (non-diverse) basins, and this is remediated with more training data.  `~600 data points typical BO benchmark ceiling, 50,000 training points typical deep-ensemble use case (CIFAR-10)`
  > With minimal training data, the loss landscape is relatively smooth, and separately-trained models are less diverse... As we increase the number of datapoints, the loss landscape becomes less smooth and models are able to find diverse basins of attraction.
  [a-study-of-bayesian-neural-network-surrogates-for-bayesian-optimization]

- Chemingui et al. 2024 (PG-GS) explicitly assert, in their own Summary/Future Work section, that prior offline BBO methods focused on improving surrogate models while using fixed search strategies -- confirming the falsification-target premise the audited paper attributes to this source.
  > This perspective is aimed at improving the search strategy in offline BBO, which complements prior methods that have focused on improving surrogate models while using fixed search strategies.
  [offline-model-based-optimization-via-policy-guided-gradient-search]

- The paper concludes with an explicit caution against naive use of standard confound-removal approaches in ML workflows, given the risk of leakage-driven inflation of apparent effects.
  > "Our results have wide-reaching implications for implementation and deployment of ML workflows and beg caution against naive use of standard confound removal approaches."
  [221009232-confound-leakage-confound-removal-in-machine-learning-leads-to-leakage]

- The NIST/SEMATECH e-Handbook defines the One-Factor-at-a-Time (OFAT) experimental method as holding all inputs fixed except one, finding its best value, fixing it there, then varying the next input in turn.
  > Hold all inputs but one fixed, and see the best result when the one free input is varied. Fix that input at that ‘best’ value. Then vary one other input... This is called a ‘One factor at a time’ (OFAT) experiment, and is practiced widely.
  [5212-one-variable-at-a-time]

- When the true model contains an interaction term (Y = X1 + X2 + X1*X2), OFAT experimentation will not work because the best setting of one factor depends on the level of the other factor, and OFAT cannot discover this joint dependence.
  > OFAT experiments will not work if the true model inside the black box looks something like: ... Interactions Model: Y = X1 + X2 + X1*X2 ... In a model with many inputs, the two-factor interactions such as X1*X2 are usually of interest, as they might point the way to a better product with minimal additional expense. OFAT experimentation leaves us in the dark about factor interactions.
  [5212-one-variable-at-a-time]

- In the presence of an interaction, the optimal setting of factor X1 reverses depending on whether X2 is fixed at its lowest or highest value, illustrating that the two factors' effects on the response cannot be chosen independently of each other.
  > In this model, if one started experimenting with X2 set at its lowest value, X1 would have to be moved toward its lowest value to get a high Y. On the other hand, if one started out with X2 fixed at its highest value, X1 would have to be moved up to get a high Y. We do not know if X1 and X2 both set at low will give a better Y that X1 and X2 both set high.
  [5212-one-variable-at-a-time]

- The paper's only task-dependence language is qualitative ('Optimizer performance varies greatly across tasks'; 'performance... depends on the problem'), never operationalized as a variance-decomposition or interaction effect size.
  > "Optimizer performance varies greatly across tasks." / "performance highly depends on the problem (see Figure 4)."
  [200701547-descending-through-a-crowded-valley-benchmarking-deep-learning-optimiz]

- Table 4 is a single-factor ablation on GP design choices (kernel/acquisition function) used only in the Sim4Opt synthetic-task-generation procedure, not a surrogate-class x optimizer cross applied to the main offline optimization task.
  > Table 4: Ablation study on GP design choices used in the Sim4Opt synthetic task generation procedure. Results ... box function optimization. BO relies on two key elements
  [260412325-black-box-optimization-from-small-offline-datasets-via-meta-learning-w]


### Landscape analysis and algorithm selection

- Alissa, Sim & Hart propose feature-free algorithm selection using recurrent neural networks (LSTM/GRU) trained on raw instance sequences to select among heuristics/solvers, contrasting with typical feature-based algorithm selection requiring hand-derived instance features -- the neural network here is the SELECTOR, not a surrogate objective model.  `within 5% of oracle performance on 80.88% to 97.63% of instances, depending on dataset`
  > we train two types of recurrent neural networks to predict a packing heuristic in online bin-packing, selecting from four well-known heuristics. As input, the RNN methods only use the sequence of item-sizes.
  [automated-algorithm-selection-from-feature-based-to-feature-free-approaches]

- The word 'surrogate' does not appear anywhere in this 2023 Journal of Heuristics survey of feature-based vs. feature-free algorithm selection, and 'landscape' appears only twice, both in bibliography citations (to Kerschke et al.'s ELA survey and a MAX-SAT landscape paper) rather than in the main text's methodology.  `0 occurrences of 'surrogate', 2 occurrences of 'landscape' (both in references)`
  > bining exploratory landscape analysis and machine learning. Evol. Comput. 27(1), 99-127 (2019)
  [automated-algorithm-selection-from-feature-based-to-feature-free-approaches]

- NLL and Brier score on ImageNet improve in lockstep with Top-1/Top-5 error as M increases from 1 to 10, confirming the monotonic-improvement pattern holds across multiple calibration metrics simultaneously, not just accuracy.  `M=1: NLL 0.959, Brier 0.317, M=10: NLL 0.789, Brier 0.275`
  > Top-1 error, Top-5 error, NLL, Brier Score
  [simple-and-scalable-predictive-uncertainty-estimation-using-deep-ensembles-full]

- The paper's proposed regularizer only ever reduces surrogate sensitivity and is demonstrated exclusively on neural-network surrogates; it runs no experiment applying the sensitivity measure to, or manipulating the sensitivity of, a Gaussian process.
  > "This raises the following questions: (1) how to regulate the sensitivity of a surrogate model; and (2) whether conditioning an offline optimizer with such less sensitive surrogate will lead to better optimization performance."
  [250304181-boosting-offline-optimizers-with-surrogate-sensitivity-batch8]

- The paper's only use of the word 'surrogate' refers to a surrogate-assisted CMA-ES variant (saACM-ES) that is itself one candidate optimizer inside the selection portfolio, not a surrogate model being selected between.
  > population self-adaptive surrogate-assisted CMA-ES (BIPOP-s*aACM-ES-k, Loshchilov...) ... A sequential, model-based [algorithm] ... from surrogate models and line searches simultaneously.
  [171108921-automated-algorithm-selection-on-continuous-black-box-problems-by-comb]

- Key landscape features from both the surrogate and true landscape were identified with the capability to predict algorithm PERFORMANCE (not to predict which surrogate type is superior), during the course of optimization.
  > This work also evaluates how these different features impact the actual search and identified key landscape features from both the surrogate and the true landscape with the capability to predict algorithm performance.
  [240406557-temporal-true-and-surrogate-fitness-landscape-analysis-for-expensive-b]

- Malan explicitly flags landscape analysis of surrogate functions as an unresolved open research problem as of 2021, stating initial investigations were not very successful and further work is needed to find landscape techniques suitable for characterizing surrogate functions.
  > Initial investigations into landscape analysis of surrogate functions were not very successful and further work is needed to identify landscape analysis techniques that are suitable for characterising surrogate functions so that the analysis is indicative of the characteristics of the actual landscape.
  [a-survey-of-advances-in-landscape-analysis-for-optimisation]

- Feature-free RNN-based selectors are shown to outperform classical machine learning models trained on hand-engineered instance features for the online bin-packing selection task.
  > They are also shown to outperform classical machine learning models trained
  [automated-algorithm-selection-from-feature-based-to-feature-free-approaches]

- SATzilla addresses censored runtime data (extremely long-running SAT instances) as a core methodological challenge distinct from surrogate-model-selection concerns in continuous optimization.
  > SAT algorithms tend to solve some instances very quickly, while taking an extremely long amount of time to solve other instances... The common solution to this problem is to "censor" some runs
  [satzilla-portfolio-based-algorithm-selection-for-sat]

- The paper cites Werth et al. (2019/2020) and Harrison et al. as the two prior works considering surrogate fitness landscapes explicitly, positioning this 2024 paper as a direct continuation of that narrow sub-literature rather than of the broader ELA/algorithm-selection tradition (Kerschke et al.).
  > Werth et al. explore this direction, comparing surrogate landscapes with those of the true... Harrison et al. analyse the surrogate landscape for single-objective... surrogate landscapes.
  [240406557-temporal-true-and-surrogate-fitness-landscape-analysis-for-expensive-b]


---

## [consensus] Settled ground — assert without hedging

- **No prior work in offline MBO or offline black-box optimization runs a crossed surrogate-class x optimizer factorial with a two-way variance decomposition of the outcome.**  _(13 independent sources, very high -- this is the audit's central negative result and it survived a recency sweep, a near-miss re-confirmation, an extension check, and an adjacent-field sweep)_
  - Caveat: Assert with the residual's three grounds stated (loss type != model class; bundled methods != a clean optimizer factor; descriptive reporting != a decomposition), because RaM Table 3 is a genuine 9x2 crossed grid in offline MBO and is the closest competitor.

- **The offline-MBO literature evaluates surrogate and optimizer as one bundled atomic method per baseline, never crossing them independently.**  _(6 independent sources, very high)_
  - Caveat: This is the confounded status quo the paper says it dissects, and it is well supported. The Kim survey's own sentence corroborates it, though that sentence sits in a section about uncertainty-quantification evaluation rather than being a call for a crossed factorial.

- **In the canonical ML reality-check audits, a claimed advantage shrank or reversed once evaluation was properly controlled.**  _(5 independent sources, high as a set of INSTANCES)_
  - Caveat: CRITICAL SCOPING. Five instances agreeing is not a law, and none of the five states a genre-wide directional rule. The paper currently cites ONE of them (Melis) for the general claim 'audits normally shrink'. Cite the set for the pattern, never one for a law -- and note Maassen et al. 2020 finds corrections going up about as often as down (19 vs 14) in a large systematic audit outside ML.

- **Standard deep ensembles are not input-distance-aware in the SNGP sense; their uncertainty reflects distance from decision boundaries rather than distance from the data manifold.**  _(3 independent sources, high)_
  - Caveat: All three are CLASSIFICATION results; none runs regression experiments. This is the basis for Mandatory Fix 2: the paper cites SNGP to bound a claim that its ensemble's sigma IS a distance signal, which inverts the source. State the classification/regression gap explicitly when using this.

- **A failure to reject a null hypothesis is not a demonstration that an effect is absent, particularly at small sample sizes.**  _(3 independent sources, very high)_
  - Caveat: The paper's handling of this is CORRECT and well-cited; it reports the Design-Bench result as no-detectable-difference and never as equivalence. The only defect is the fabricated 'more than ten datasets' threshold attributed to Demsar, whose removal strengthens rather than weakens the passage.

- **Computational budget is not a nuisance parameter in optimizer comparison: equalizing it can change which method wins, and budget-dependent benchmarking is an established methodological category.**  _(4 independent sources, very high)_
  - Caveat: This is the settled ground that makes the paper's budget finding a CONTRIBUTION TO A NAMED LINE rather than a defence against an objection. The paper's own budget result carries its only disjoint bootstrap intervals and a ranking flip, and cites none of these four.

- **Eta-squared and partial eta-squared are positively biased estimators of variance explained; omega-squared and epsilon-squared are the bias-corrected alternatives, and the bias matters most at small n.**  _(3 independent sources, high, with a provenance caveat)_
  - Caveat: The two foundational statistics sources were verified SECONDHAND (paywalled everywhere attempted). The empirical half is first-hand and decisive -- I computed the bias directly from the paper's own artifacts. Bias-correcting moves the headline 0.367->0.405 to 0.351->0.395, so the direction survives and the effect grows.

- **Optimizing against a learned surrogate drives designs off-support, where the surrogate over-predicts and true value degrades.**  _(4 independent sources, very high)_
  - Caveat: Settled ground the paper can assert without defence. What is NOT settled, and is the paper's genuine contribution, is that this law does not DISCRIMINATE between surrogate classes at matched distance. Frame the paper's Elimination 7 as a refinement of this consensus rather than as an independent discovery -- Fannjiang stated the diagnosis in 2020 and is uncited.

- **The standard Bayesian-optimization review asserts that the choice of statistical model often matters more than the choice of acquisition heuristic, and does so as an organizing thesis.**  _(2 independent sources, very high (two independent statements within the canonical review, plus corroboration of the complementary premise))_
  - Caveat: Verified because I hypothesised the paper might be OVER-conceding priority here. It is not -- the review states the doctrine twice, and more strongly than the paper's paraphrase. The paper's restriction of the doctrine to online BO is also sound: zero hits for 'offline' in 137,300 characters.

---

## [contested] Top fight clusters — both sides with evidence

### Is a deep ensemble's sigma a distance signal that is uninformative about pointwise error, or does ensemble disagreement genuinely track predictive error?

**Side A —** Ensemble sigma tracks DISTANCE to the training data, not error. The paper measures rho=0.07 against pointwise absolute error but rho=0.26 against k-NN distance, and frames the low error-correlation as a corrected measurement rather than a defect.
  > The ensemble's sigma correlates with pointwise absolute error at only rho~0.07, but with k-NN distance to the training data at rho~0.26, three to four times larger and positive on all seven tasks.
  > The prior analysis concluded sigma was uninformative by measuring it against the wrong target.

**Side B —** Ensemble/committee uncertainty DOES track error in regression, strongly, when measured in-distribution. And separately, the two sources the paper cites to bound its claim say deep ensembles are NOT distance-aware at all.
  > Carrete et al. 2023 (J. Chem. Phys. 158:204801): 'the Spearman correlation coefficient between uncertainty and error over the validation data set is 0.90 for the committee and 0.91 for the bootstrap-aggregation ensemble' -- 13x the paper's rho=0.07, in regression.
  > SNGP (Liu et al. 2020): 'deep ensembles ... are based on dense output layers that are not distance aware ... assigning low uncertainty to OOD examples even if they are far from the data.'

**Evidence delta:** Side B is stronger and more diverse: one peer-reviewed regression benchmark with a directly comparable statistic, two papers whose central empirical argument is about the exact model class, and the ensemble method's own originating paper on the exact construction under audit. Side A is a single measurement on one grid. Note however that side B's Carrete figure is IN-DISTRIBUTION while the paper's rho=0.07 is measured
**Scope:** PARTLY scoped differently, and the scoping is the resolution. Carrete measures in-distribution, where distance and error largely coincide; the paper measures where an optimizer has pushed designs off-support. SNGP/DUQ measure classification with a 2D toy geometry. So all three can be right. But that means the paper's DICHOTOMY -- distance signal 'not' error signal -- is a false opposition, and its 'bounded by prior w

### Has the K=2 endpoint already been tested for ensemble surrogates in Bayesian optimization, and does it show robustness or sensitivity?

**Side A —** The paper claims its K sweep 'extends below' the range over which ensemble surrogates were found robust, characterising the prior range as K in {5,10} and claiming K=2,3 as its own addition.
  > Our sweep runs over K in {2,3,5,10} and therefore extends below the K in {5,10} range over which ensemble surrogates were found robust (li2024bnnsurrogates), sharing its two upper points and adding K=2,3.

**Side B —** Li/Rudner/Wilson tested K = {2, 5, 10} and reported ROBUSTNESS across that range, K=2 included.
  > Figure A.7 legend tokens, extracted first-hand from arXiv:2305.20028v2 page 28: '2 Models', '5 Models', '10 Models'.
  > Verbatim caption: 'We compare the behavior of ensembles with different numbers of models, and we find that the different ensembles perform similarly across many experiments, showing the robustness of our results to this hyperparameter.'

**Evidence delta:** Side B is decisive and verified twice independently -- by the orchestrator extracting legend tokens from the PDF, and by a subagent rendering the same page as an image. Side A's characterisation of the prior range is simply incorrect.
**Scope:** GENUINE contradiction on the factual claim about the prior range. But a real distinction survives and the paper does not draw it: L/R/W measure PERFORMANCE robustness of ensemble BO; the paper measures SENSITIVITY OF THE VARIANCE DECOMPOSITION (eta^2_surr) to K. Those are different quantities and can both be true. That distinction is the paper's only defence and it appears nowhere.

### Do corrective audits normally shrink the effect they audit, and is an audit whose corrected effect GREW unprecedented -- or is it a documented artifact signature?

**Side A —** Audits in this genre usually shrink; a corrected variance-explained statistic above its published value has no precedent in the ML audit literature.
  > Audits in this genre usually shrink the effect they audit (melis2018sota). This one strengthens it.
  > We searched the ML reality-check and reproducibility literature for a de-confounding audit reporting a corrected variance-explained statistic above its own published value and found none.

**Side B —** Three separate problems. (1) Melis never claims a genre-wide direction -- it reports a ranking reversal in one setting and self-describes as one instance. (2) In the one large systematic audit of recomputed effect sizes, corrections go up about as often as down. (3) In the one ML literature where confound removal INCREASING an effect has 
  > Melis et al.: 'Once hyperparameters have been properly controlled for, we find that LSTMs outperform the more recent models, contra the published claims' -- a ranking reversal, not a shrinking variance-explained scalar; and 'this paper joins other recent papers in warning of ... replication failure'.
  > Maassen et al. 2020 (PLOS ONE, 500 effect sizes across 33 meta-analyses): 'We did not find any evidence for systematic bias ... we estimated 19 pooled effect sizes to be larger than originally reported and 14 to be smaller.'

**Evidence delta:** Side B is stronger on every limb. Its (1) is a direct reading of the single citation side A rests on; its (2) is a large systematic study; its (3) is a peer-reviewed ML methodology paper naming the exact directional signature. Side A's narrow scalar claim nonetheless SURVIVES -- nobody found an ML benchmark audit reporting a corrected variance-explained statistic above its published value.
**Scope:** SCOPED DIFFERENTLY, and the paper's narrow scoping is what saves it. Maassen is psychology meta-analysis, not ML benchmark audits. Hamdan is confound-removal methodology, not a reality-check audit. So the exact scalar claim stands. What does NOT stand is the surrounding rhetoric: 'audits normally shrink' as a law, and the implication that an upward correction is intrinsically surprising. Hamdan additionally imposes a

### Is 'a UCB-style acquisition behaves as local search and gets trapped near the data' an established reading in the literature, and who owns it?

**Side A —** It is an established reading which the paper applies rather than discovers, owned by Fan et al. 2024.
  > as is the reading of a UCB-style acquisition as local search (fan2024minucb)
  > The surviving mechanism is LCB paralysis ... This is the offline instance of a known reading of UCB-style acquisitions as local search (fan2024minucb), applied rather than discovered.

**Side B —** Nobody owns it. Fan proposes it as a novel method and proves CONVERGENCE; TuRBO diagnoses the opposite failure; GIBO's exploitation step involves no UCB at all.
  > Fan et al.: 'we propose our first algorithm ... MinUCB, which replaces gradient descent step with a step that minimizes the UCB in GIBO'; 'This discovery is also meaningful as it opens up possibilities for new designs.'
  > Fan et al. full-text grep: 0 hits for 'offline', 'LCB', 'lower confidence bound', 'stuck', 'frozen', 'paralysis'. Their Theorem 1 proves convergence to a local optimum under an increasing beta schedule and continual active resampling -- conditions a static offline dataset cannot meet.

**Evidence delta:** Side B is decisive: zero-hit greps on the exact terms, plus a theorem that runs the opposite direction, plus an independent check that the proposed alternative owner diagnoses the opposite failure mode.
**Scope:** NOT a scoping difference -- a straightforward attribution error, in three places (the mechanism framing, the LCB-paralysis mechanism, and the distance-aware co-citation). The paper's own empirical freeze finding is unaffected and is strong; it simply has no prior owner to cite.

### Is distance-from-data the driver of surrogate unreliability under optimization, or does it fail to discriminate between surrogate classes?

**Side A —** Distance drives oracle unreliability -- the founding framing of offline model-based design, and the premise behind autofocusing.
  > Fannjiang & Listgarten 2020: 'oracle-based design ... will query the oracle in regions of the design space that are not well-represented by the oracle training data ... its outputs, including its uncertainty estimates, become unreliable beyond the training data.'
  > Gao et al.: proxy-reward degradation is a function of KL distance from the data, R_bon(d)=d(alpha-beta*d).

**Side B —** Distance predicts aggregate loss but does NOT discriminate between surrogate classes at matched distance -- the paper's seventh elimination.
  > Across 5,040 optima, distance predicts over-prediction (rho=+0.758) and true loss (rho=-0.818), but the classes sit at matched median distance (0.87 / 0.86 / 0.84) and the ensemble is still worse in true oracle value by -1.406 [-2.803,-0.375].
  > The ensemble's optima are +0.116 [-0.004,0.333] further out and +0.043 [-0.652,1.085] more inflated -- both intervals covering zero.

**Evidence delta:** Both sides are empirically solid and NOT actually in conflict once stated precisely. Side A is about the aggregate distance-unreliability law, which side B independently confirms (rho=-0.818). Side B adds that the law does not explain the CLASS gap.
**Scope:** COMPLEMENTARY, not contradictory -- and this is the paper's best unexploited opportunity. Gao's degradation is explicitly class-dependent by optimization method but he varies only scale within one architecture family. So the paper's finding is a genuine REFINEMENT onto a new axis (architecture class) in a new domain (offline MBO). Framing it as a refinement of a named prior position is stronger than presenting the di

---

## Ungrouped

- PG-GS reformulates offline optimization as an offline RL problem, learning a policy that outputs a direction vector to replace the fixed step-size in a standard gradient update, explicitly to correct for non-smooth/sub-optimal surrogate gradients.
  > The key idea behind PGS is to reformulate the step-size in the standard gradient update into a direction vector. Such direction vector can be viewed as an output alpha = pi(x_k) of a guiding policy pi to direct the search space exploration from x_k in the direction of the high-performing input regions.
  [offline-model-based-optimization-via-policy-guided-gradient-search]

- Standard deep ensembles, while allowing averaging of predictions over several hypotheses, do not offer any guarantees for the diversity between those hypotheses nor do they provably converge to the true Bayesian posterior under any meaningful limit.
  > That being said, while they might allow for the averaging of predictions over several hypotheses, they do not offer any guarantees for the diversity between those hypotheses nor do they provably converge to the true Bayesian posterior under any meaningful limit.
  [210611642-repulsive-deep-ensembles-are-bayesian]

- In one of two experimental setups (weight-space regularization comparison), the standard (non-repulsive) deep ensemble achieves the best OOD detection performance using predictive entropy, despite the paper's overall thesis that standard deep ensembles lack diversity guarantees -- the empirical OOD-
  > Nevertheless, all our repulsive ensembles improve functional diversity, accuracy, and OOD detection when compared to standard SVGD, whereas the standard deep ensemble achieves the best OOD detection using the entropy.
  [210611642-repulsive-deep-ensembles-are-bayesian]

- Table 3 is explicitly captioned 'Main loss functions used by ensemble techniques for UQ' and Table 4 is captioned 'Main loss functions used by deep ensemble techniques for UQ', confirming loss function is catalogued as a standalone table axis distinct from the method-family taxonomy sections.
  > TABLE 3: Main loss functions used by ensemble techniques for UQ. ... TABLE 4: Main loss functions used by deep ensemble techniques for UQ.
  [a-review-of-uncertainty-quantification-in-deep-learning-techniques-applications]

- The survey's Section 6 subsections (6.1 Deep Ensemble, 6.2 Deep Ensemble Bayesian, 6.3 UQ in Traditional Machine Learning domain using Ensemble Techniques) are organized by model/method family and reference each family's own loss-function table separately, rather than treating loss function choice a
  > As shown in previous section, in the following, we summarise few loss functions of deep ensembles in Table 4.
  [a-review-of-uncertainty-quantification-in-deep-learning-techniques-applications]

- Deep Kernel Learning replaces a GP kernel's raw-input evaluation with evaluation on a deep-network feature extractor's output, while retaining the standard GP posterior mean/variance machinery and training the whole system jointly via the GP marginal likelihood.
  > "k(xi, xj|theta) -> k(g(xi, w), g(xj, w)|theta, w), where g(x, w) is a non-linear mapping given by a deep architecture"
  [151102222-deep-kernel-learning]

- This paper's own venue is unverifiable: the arXiv abstract page carries no Comments or Journal-ref field, and the extracted PDF text contains no proceedings/copyright footer for its own publication (only for cited works), unlike the companion Schmidt et al. ICML 2021 paper.
  > Grep for "Proceedings of", "International Conference", "workshop", "copyright" in the extracted text returns only reference-list occurrences describing other cited papers' venues, never this paper's own.
  [191005446-on-empirical-comparisons-of-optimizers-for-deep-learning]

- Uncertainty quality (calibration) consistently degrades with increasing dataset shift regardless of UQ method, and good i.i.d. calibration does not transfer to good calibration under shift.
  > Along with accuracy, the quality of uncertainty consistently degrades with increasing dataset shift regardless of method. Better calibration and accuracy on the i.i.d. test dataset does not usually translate to better calibration under dataset shift
  [190602530-can-you-trust-your-models-uncertainty-evaluating-predictive-uncertaint]
