# Interim report: landscape-predicts-which-surrogate-wins

**Locus question:** The per-task GP-vs-ensemble gaps in Table `tab:sfull` span four orders of magnitude
(0.19 to 2591.06) and are not monotone in dimension. Does landscape structure predict which surrogate
wins, and by how much — is the paper sitting on a per-task selection rule it isn't writing?

**Flavor:** convergent

## What the corpus already said

The width sweep did not touch this locus directly — no note in the corpus discusses Exploratory Landscape
Analysis (ELA), the algorithm-selection literature, or Rice's framework. I confirmed this by grepping the
paper's own 67-entry `references.bib` directly: zero hits for `kerschke`, `mersmann`, `satzilla`,
`rice1976`, `smith-miles`, or `flacco`. The paper never engages this literature at all, which is itself
informative — this is genuinely unexplored relative to the paper's own related-work engagement, not merely
under-cited.

Two adjacent corpus notes exist and matter for framing. First, [[a-study-of-bayesian-neural-network-surrogates-for-bayesian-optimization]]
(Li, Rudner & Wilson, ICLR 2024) states in its own abstract: "the ranking of methods is highly problem
dependent, suggesting the need for tailored inductive biases," and its body names *dimensionality* and
*non-stationarity* as the specific problem properties it thinks drive the ranking ("GPs do not scale well
to high-dimensional input spaces without careful human intervention... BNN surrogates can learn the
non-stationarity of the function"). This is a real, if qualitative and hedged, precedent for "surrogate
ranking is problem-dependent" — but it is stated in the online-BO setting, is never formalized into a
feature-based selection rule, and (important below) predicts GPs should *lose* ground in high dimensions,
which is not what this paper's own data shows. Second, a sibling investigator's note
[[interim-report-n7-roughening-beyond-offline-mbo]] (a different locus, on causal smoothness manipulation)
already surfaced [[extrapolative-bayesian-optimization-with-gaussian-process-and-neural-network-ens]] (Lim
et al. 2021), which frames the GP's eventual dominance over an NN ensemble as tied to problem complexity
("even the most complex high-dimensional dataset... GP becomes the top performer") — again a qualitative,
dimension/complexity-linked story, and again in the opposite direction from a naive multimodality
narrative. Neither source does anything at the level of formal ELA features. The [[coco-platform-comparing-continuous-optimizers-black-box-fulltext]]
note (Hansen et al., the BBOB platform paper) was already in the vault as background but does not itself
carry per-function landscape taxonomies.

Also worth noting: the paper already has its own figure literally called `fig:landscape` (Elimination 7),
but it answers a different question — it pools 5,040 returned *optima* across all seven tasks and asks
whether distance-to-training-data discriminates ensemble-quality from GP-quality optima (it does not: "the
classes sit at the same median distance (0.87 against 0.86) and differ in outcome anyway"). That is a
within-task, optimum-level analysis, not a task-level landscape-property analysis. The paper's "landscape"
vocabulary is already spoken for by a different result, which is one more reason the task-level question
this locus asks has genuinely never been asked inside this project.

## What the new sources say

**1. Kerschke & Trautmann, "Automated Algorithm Selection on Continuous Black-Box Problems By Combining
Exploratory Landscape Analysis and Machine Learning"** (Evolutionary Computation 2019, arXiv:1711.08921) —
[[171108921-automated-algorithm-selection-on-continuous-black-box-problems-by-comb]]. This is the canonical
paper the query names. Its abstract states the target precisely: "construct a representative set of
high-performing complementary solvers and present an algorithm selection *model* that... requires less
than half of the resources... [for] selecting the best suited optimization algorithm within the considered
set for unseen problems prior to the optimization itself based on a small sample of function evaluations."
The selected object is a **solver** (a search/optimization algorithm run against the COCO/BBOB suite), not
a surrogate model. This is the single clearest confirmation that the mature ELA + algorithm-selection
tradition targets optimizer choice, and does so at the scale of the full BBOB suite (24 noiseless functions
× many dimensions × many instances), not seven tasks.

**2. Xu, Hutter, Hoos & Leyton-Brown, "SATzilla: Portfolio-based Algorithm Selection for SAT"** (JAIR 2008)
— [[satzilla-portfolio-based-algorithm-selection-for-sat]]. Full text fetched (121K chars). This is the
canonical worked instance of Rice's framework, and it cites Rice directly: "practitioners with hard SAT
problems to solve face a potentially difficult 'algorithm selection problem' (Rice, 1976): which
algorithm(s) should be run in order to minimize some performance objective." SATzilla builds
"empirical hardness models" from per-instance features to choose *among solvers*, exactly the Rice
template Kerschke & Trautmann later re-instantiate for continuous black-box optimization. Confirms the
lineage the query asked me to trace, and confirms — again — that the object being selected is the solver,
never a regression/surrogate model.

**3. Malan, "A Survey of Advances in Landscape Analysis for Optimisation"** (Algorithms 2021, open access,
~131 citations) — [[a-survey-of-advances-in-landscape-analysis-for-optimisation]]. Full text fetched
(77K chars). This gives the standard ELA feature taxonomy directly: "six classes of low level features are
defined: (1) convexity, (2) y-distribution, (3) levelset, (4) meta-model, (5) local search, and (6)
curvature... features are estimations of attributes such as the probability of the objective function
being linear, the skewness of the distribution of the function values, the accuracy of fitted meta models,
the number of local optima identified by local search, estimated numerical gradient." These are exactly
the standard features the query's task (a) asked me to identify (multimodality is captured via local-search
and y-distribution features; funnel/basin structure via dedicated funnel metrics on local-optima networks;
separability and conditioning are named ELA feature groups elsewhere in the survey). The survey documents
`flacco` (Kerschke's R package) as the standard tool for computing these features from a Latin-hypercube
sample. Critically for task (a): grepping this survey's own body for "surrogate model select" or "surrogate
select" returns **zero hits** — landscape analysis has been used to explain algorithm behavior, to design
algorithm-selection models, and (per its citation list) even to select among search *operators*, but the
survey's own reference list surfaces only one paper that gestures at surrogate-model selection specifically:
Yu, Tan, Sun, Zeng & Jin (2016), "An adaptive model selection strategy for surrogate-assisted particle
swarm optimization algorithm" (IEEE SSCI 2016) — cited by the survey in a different context (per-instance
algorithm configuration), not read directly by me (outside my 4-source budget), and flagged here as an
unread lead for a follow-up sweep rather than a verified precedent.

**4. Rodriguez, Thomson, Alderliesten & Bosman, "Temporal True and Surrogate Fitness Landscape Analysis for
Expensive Bi-Objective Optimisation"** (arXiv:2404.06557, 2024) — [[240406557-temporal-true-and-surrogate-fitness-landscape-analysis-for-expensive-b]].
Discovered via the Malan survey's citation of a 2019 predecessor (Werth et al.) on surrogate-model
landscape analysis; this is its freely available 2024 continuation. This is the closest genuine precedent
I found anywhere for "landscape features and surrogate choice" in one paper. Its own abstract states the
gap it is filling: "literature about analysing the fitness landscapes induced by surrogate models is
limited, and even non-existent for multi-objective problems." It compares landscape features of the *true*
function against those of the *surrogate model itself*, across BBOB bi-objective benchmarks, and finds
"both surrogate and true landscape features are capable of predicting algorithm performance," concluding
this "may help to facilitate the design of *surrogate switching* approaches." This is the single closest
match to the locus's question in the literature I could locate — but it is: (a) about the landscape *of the
surrogate's own fitted function*, not the landscape of the true black-box problem predicting which
surrogate *class* to use; (b) in an online, iteratively-updated multi-objective evolutionary setting, not
offline MBO; and (c) about switching within a surrogate-assisted EA loop, not a one-shot GP-vs-ensemble
choice made before optimization starts. It shows the adjacent idea is alive and productive elsewhere, and
that nobody has yet pulled it into offline MBO's GP-vs-ensemble question.

**5. Alissa et al., "Automated Algorithm Selection: from Feature-Based to Feature-Free Approaches"**
(Journal of Heuristics 2023) — [[automated-algorithm-selection-from-feature-based-to-feature-free-approaches]].
Full text fetched (96.7K chars). Restates Rice's framework formally: "Originally formulated by Rice (1976),
the per-instance Algorithm-Selection Problem (ASP) can be defined as: Given a set I of instances of a
problem P, a set a={a1,...,an} of algorithms for P and a metric m: a×I→R... construct a selector S that
maps any problem instance i∈I to an algorithm S(i)∈A such that the overall performance of S on I is
optimized." Ten mentions of Rice throughout, confirming this is still the live organizing framework in
2023. Grep for "surrogate" returns **zero hits** — this modern survey of the entire algorithm-selection
field, feature-based and feature-free alike, has no surrogate-model-selection branch at all. That is a
second independent confirmation (after the Malan survey) that surrogate-class selection is not a
recognized sub-problem of algorithm selection as the field currently organizes it.

## Evidence synthesis

I verified Table `tab:sfull` directly against `paper/aaai27/supplement.tex` (lines 58-80) and reproduced
every one of the seven raw-units gaps the query supplied (Branin 8.87, Styblinski 21.20, Levy 2.09,
Rosenbrock 0.19, Rastrigin 2.88, Ackley 3.11, Griewank 2591.06, all = GP+Grad − Ens+Grad) exactly. I then
went further than the query's own table and computed the same gap under the other two optimizers from the
same table: Perturbation (Branin 0.38, Styblinski 3.07, Levy 0.16, Rosenbrock 0.04, Rastrigin 0.16, Ackley
0.04, Griewank 125.0) and CMA-ES (Branin 13.61, Styblinski 21.44, Levy 3.14, Rosenbrock 0.39, Rastrigin
5.75, Ackley 3.72, Griewank 2612.0).

**Finding 1 — dimension does not predict the gap, robustly.** Spearman rank correlation between task
dimension and gap is 0.107 (p=0.82) under gradient, −0.109 (p=0.82) under perturbation, and 0.071 (p=0.88)
under CMA. All three are statistically indistinguishable from zero at n=7. This is not a fluke of one
optimizer condition; it holds identically under all three. The paper's own claim that the spread is "not
monotone in dimension" is correct and, I can now say, precisely quantified: there is no detectable rank
relationship at all, in either direction, under any optimizer.

**Finding 2 — the per-task ranking is nonetheless a real, robust property.** Spearman correlation between
the gap rankings across optimizer pairs is 0.84 (grad-pert, p=0.019), 0.96 (grad-cma, p<0.001), and 0.91
(pert-cma, p=0.005). Rosenbrock is always the smallest gap; Griewank is always the largest, by a wide
margin, under every optimizer. This means the heterogeneity is not optimizer-dependent measurement noise —
it is a stable, task-intrinsic quantity — but that stable quantity correlates with nothing standard I can
name.

**Finding 3 — textbook multimodality classification does not split the gaps either.** I checked the
standard modality/separability taxonomy directly from the oracle code (`code/mbo.py`, ground truth, not a
secondary description): Rastrigin, Ackley, Griewank and Levy are textbook "many local minima" functions (the
SFU Virtual Library of Simulation Experiments — a standard reference used across the surrogate-optimization
literature — groups exactly these four this way; Rosenbrock is "valley-shaped" i.e. the only strictly
unimodal task in the grid; Branin and Styblinski-Tang fall in the survey's residual "other" category).
Within the four-function "many local minima" bucket the gap spans 2.09 (Levy) to 2591.06 (Griewank) — three
orders of magnitude inside one textbook category. Outside it, Rosenbrock has the smallest gap of all (0.19)
but Styblinski has the second-largest (21.20) — larger than three of the four "many local minima" functions.
Separability fares no better: from the oracle formulas, Styblinski, Levy, and Rastrigin are separable
(sums of independent per-dimension terms) while Branin, Rosenbrock, Ackley, and Griewank are not; the
separable group's gaps (2.09-21.20, ~10x) span a *narrower* range than the non-separable group's (0.19-2591,
~13,600x), which contains both the extreme minimum and the extreme maximum. Neither the modality label nor
separability sorts the table.

**Finding 4 — one honest exception and one refuted hypothesis of my own.** The only clean signal is a
binary one: the single unimodal task (Rosenbrock) has by far the smallest gap under all three optimizers,
consistent with the intuitive idea that a well-behaved unimodal valley gives ensembles the least room to go
wrong. But this signal explains only where the *floor* sits, not the ordering above it, and "unimodal vs.
not" is a one-bit feature that cannot discriminate a 2.09 from a 2591.06. I also tested and refuted my own
initial hypothesis that the tasks' shared normalization onto comparable-looking bounds might be flattening
their native ruggedness (which would make textbook labels inapplicable for a different reason): I read
`code/mbo.py` directly and found each oracle applies an affine map from the shared `[0,1]^d` design space
back to that function's *exact native textbook domain* (Branin → `x1∈[-5,10], x2∈[0,15]`; Styblinski →
`[-5,5]`; Levy → `[-10,10]`; Rastrigin → `[-5.12,5.12]`; Griewank → `[-600,600]`, all matching standard
references exactly; Rosenbrock uses `[-2,2]` and Ackley `[-5,5]`, both common reduced variants in the ML
literature rather than the widest textbook range). The domain-flattening hypothesis is false; the tasks
really do sit on their standard, well-characterized landscapes, which makes the non-result in Findings 1-3
stronger, not weaker — this isn't an artifact of an unusual reparametrization.

**Finding 5 — a documented, counterintuitive property of Griewank that cuts against the naive story.** Via
OpenAlex I retrieved (abstract only; both are paywalled in full text, a genuine access limitation I flag
rather than paper over) Locatelli (2003), "A Note on the Griewank Test Function" (Journal of Global
Optimization, 116 citations) and its 2024 continuation, "Success Rate of Evolution Strategies on the
Multimodal Griewank Function" (IEEE CEC 2024), whose abstract states plainly: "The Griewank function is
known for its counter intuitive behavior of getting simpler to be optimized with increasing dimension,
although the number of local minima increases with the problem dimension." If this well-established
property holds at d=30, the naive "Griewank is highly multimodal, hence hard" story is backwards for this
specific task — Griewank-30D should be comparatively *benign* for a well-calibrated method, which is
consistent with the exact GP landing almost exactly on the true optimum (−0.94 vs. a true minimum of 0) and
inconsistent with attributing the ensemble's catastrophic collapse (−2592, on the same task) to "landscape
ruggedness" at all. The more plausible account, which the paper's own machinery half-supports but never
states, is a surrogate-side extrapolation failure interacting with training-density sparsity in a
high-volume domain (`N=8,000` points spread over a `[-600,600]^30` box), not a landscape property in the
ELA sense. The paper's own text already documents two other per-task anomalies via non-landscape
mechanisms without generalizing them: Branin is flagged elsewhere in the paper (Elimination 7, the
"inversion" analysis) as the one task where the ensemble's optima sit conspicuously farther off-support
(+0.743 vs. −0.022 to +0.060 for the other six) and where "all 30 seeds invert" under ensemble+gradient; and
Ackley is named in the β-sweep ablation as "the exception [where] the uninformative σ makes the penalty
point away from the optimum" — an explicitly landscape-flavored explanation (Ackley's flat outer plateau) for
one specific finding that the paper never connects back to the Table `tab:sfull` heterogeneity it otherwise
calls merely "descriptive."

Taken together: this is a genuine, well-triangulated negative result on the *predictive* question (no
standard off-the-shelf landscape covariate — dimension, textbook modality label, separability — explains
the gap ordering), combined with a genuine positive result on the *structural* question (the heterogeneity
is a real, robust, per-task property, stable across optimizer choice, not noise). Both halves are now
precisely quantified where the paper currently only asserts the first informally ("heterogeneous... at
n=7 this spread is descriptive only") and is silent on the second.

## Committed position

Landscape structure, as captured by any standard off-the-shelf covariate (dimension, textbook
multimodality classification, separability), does **not** predict the GP-vs-ensemble gap in this paper's
own data — I tested this directly against the paper's own Table `tab:sfull` under all three optimizers and
found correlations statistically indistinguishable from zero (dimension) or classifications that actively
mis-sort the ordering (modality, separability); this is a decisive, quantified negative result, not an
absence of looking. But the heterogeneity is not noise either: it is a stable per-task property (Spearman
0.84-0.96 across optimizer pairs) that the paper is currently sitting on without naming, and the mature ELA
/ algorithm-selection literature (Rice 1976 → SATzilla → Kerschke & Trautmann) has never been pointed at
surrogate-class choice — it exists at BBOB scale (dozens of functions × many instances) to select solvers,
not surrogates, and the one paper that gets structurally close (Rodriguez et al. 2024, comparing true vs.
surrogate landscape features to motivate "surrogate switching") does so online, per-iteration, inside a
multi-objective EA, not offline, once, for GP-vs-ensemble. The paper should therefore make two moves, and
only one of them before the deadline: (1) **FOLD-INTO-THIS-PAPER, CHEAP** — add two or three sentences
reporting exactly what I found: the gap ranking is stable across optimizers (cite the three correlations)
but is uncorrelated with dimension, textbook modality class, or separability (cite the checks); this closes
off a hostile reviewer's "have you even checked whether this is just landscape?" objection with a specific,
falsifiable, already-computed answer instead of the current one-line hedge, and costs nothing beyond
writing it — every number is already sitting in Table `tab:sfull`. (2) **FOLLOW-UP-PAPER, EXPENSIVE** — a
genuine test needs the BBOB/COCO-scale corpus Kerschke & Trautmann actually use (dozens of functions, many
instances and dimensions each, not seven hand-picked textbook functions), with `flacco`/`pflacco` ELA
features computed on samples drawn from each task's own domain, correlated against the same 3×3 grid this
paper already runs, extended across instances. This is not foldable before an AAAI deadline; it is a
different paper, with Rodriguez et al. (2024) as the nearest methodological cousin and Kerschke & Trautmann
(2019) as the nearest procedural template. My prior going in was FOLLOW-UP-PAPER; the evidence confirms it
but sharpens the reason — not "too little data to tell" but "the data we have already rules out the simple
versions of the hypothesis," which is a stronger and more useful thing to tell the paper's authors than an
unresolved shrug.

- **Position:** No standard landscape covariate (dimension, textbook multimodality class, separability)
  predicts the per-task GP-ensemble gap in this paper's own data; the heterogeneity is a real, robust,
  per-task property (stable across all three optimizers) that the ELA/algorithm-selection literature has
  never targeted at the surrogate-class level. FOLD-IN a 2-3 sentence negative-result disclosure (cheap,
  no new experiments); a genuine predictive ELA study is FOLLOW-UP-PAPER, EXPENSIVE (needs BBOB-scale n,
  not 7).
- **Confidence:** high on the negative result (dimension/modality/separability fail to predict the gap —
  this is a direct, first-hand computation against the paper's own primary data and code, replicated across
  all three optimizers, not a single fragile test); medium on the "no prior work targets surrogate-class
  selection via landscape" claim (five sources checked, two surveys with zero "surrogate" hits, one
  near-miss found and read in full — but the citation-chain lead to Yu et al. 2016 was not read directly,
  so I cannot rule out a specific niche precedent with full certainty).
- **Boundary conditions:** this verdict applies to the seven synthetic tasks as currently instrumented and
  to the three off-the-shelf covariates I tested. It does not rule out that a *formal*, sampled ELA feature
  vector (convexity, y-distribution, curvature, funnel metrics via `flacco`) computed directly on these
  seven domains might correlate with the gap better than crude labels do — I did not compute those features
  myself (out of scope for a 4-source budget with no landscape-feature-extraction tooling available in this
  session), so that specific, narrower claim is untested, not refuted.
- **What would change this position:** (a) if someone ran `flacco`/`pflacco` on samples from these exact
  seven domains and found a landscape feature (not dimension, not the crude modality label) with a strong,
  significant correlation to the gap even at n=7, the "no landscape covariate predicts it" claim would need
  softening to "no *crude* covariate predicts it, but a formal feature might"; (b) if a BBOB-scale replication
  (Kerschke & Trautmann's own template, dozens of functions) found the same non-correlation at scale, that
  would upgrade this from a n=7 curiosity to a field-level fact and would be worth a paper on its own; (c) if
  Yu et al. (2016) or another unread source turns out to do formal ELA-driven surrogate-class selection
  already, the "field has never targeted this" half of the position weakens to "rare but not unprecedented."
- **Evidence weight:** 3 first-hand quantitative checks against the paper's own primary data support the
  negative result (dimension correlation, modality/separability sort, cross-optimizer stability), all
  computed directly, none secondary; 5 fetched literature sources support the "field targets optimizers, not
  surrogates" claim, 2 of them (both surveys) checked by direct grep for zero "surrogate model selection"
  hits; 1 source (Rodriguez et al. 2024) is a genuine near-miss that partially cuts against a strong version
  of "nobody has looked at surrogate landscapes," so I have downgraded my language from "no one" to "no one
  in this exact offline-MBO, one-shot, GP-vs-ensemble framing"; 1 lead (Yu et al. 2016) is unread and
  explicitly flagged as such rather than silently dropped.

## Open questions

- Would formal ELA features (via `flacco`/`pflacco`, computed by sampling each task's actual affine-mapped
  domain) show a correlation with the gap that the crude covariates I tested miss? Untested here — needs
  landscape-feature-extraction tooling not available in this session's budget.
- Does Yu, Tan, Sun, Zeng & Jin (2016), "An adaptive model selection strategy for surrogate-assisted
  particle swarm optimization algorithm" (IEEE SSCI), actually perform landscape-driven surrogate-class
  selection, or is it about something narrower (e.g., selecting among RBF kernel variants within one
  surrogate family, closer to the within-GP smoothness-tuning literature the sibling N7 locus already
  mapped)? Flagged, not read — would take one more fetch to resolve.
- Is the "training density in a high-volume domain" mechanistic hypothesis I raised for Griewank (as an
  alternative to a landscape-ruggedness account) testable directly on the existing artifacts (e.g., by
  checking whether the ensemble's returned Griewank optima sit at anomalously large radius from the origin
  compared to its optima on other tasks)? This looks CHEAP and could be a second, more specific
  fold-in candidate, but I did not have budget to pull the raw per-seed optimum coordinates in this pass.

## Sources

1. [[171108921-automated-algorithm-selection-on-continuous-black-box-problems-by-comb]] — Kerschke &
   Trautmann (2019), "Automated Algorithm Selection on Continuous Black-Box Problems By Combining
   Exploratory Landscape Analysis and Machine Learning," arXiv:1711.08921. Canonical ELA+ML solver
   selection on COCO/BBOB.
2. [[satzilla-portfolio-based-algorithm-selection-for-sat]] — Xu, Hutter, Hoos & Leyton-Brown (2008),
   "SATzilla: Portfolio-based Algorithm Selection for SAT," JAIR 32. Canonical Rice-framework instance.
3. [[a-survey-of-advances-in-landscape-analysis-for-optimisation]] — Malan (2021), "A Survey of Advances in
   Landscape Analysis for Optimisation," Algorithms 14(2):40. Standard ELA feature taxonomy; source of the
   Yu et al. 2016 lead.
4. [[automated-algorithm-selection-from-feature-based-to-feature-free-approaches]] — Alissa et al. (2023),
   "Automated Algorithm Selection: from Feature-Based to Feature-Free Approaches," Journal of Heuristics.
   Modern Rice-framework restatement; zero "surrogate" hits.
5. [[240406557-temporal-true-and-surrogate-fitness-landscape-analysis-for-expensive-b]] — Rodriguez,
   Thomson, Alderliesten & Bosman (2024), "Temporal True and Surrogate Fitness Landscape Analysis for
   Expensive Bi-Objective Optimisation," arXiv:2404.06557. Closest genuine adjacent precedent (surrogate
   landscape features motivating "surrogate switching," online multi-objective EA setting).
6. [[a-study-of-bayesian-neural-network-surrogates-for-bayesian-optimization]] — Li, Rudner & Wilson (2024),
   "A Study of Bayesian Neural Network Surrogates for Bayesian Optimization," ICLR 2024, arXiv:2305.20028.
   Already in vault (reused, not re-fetched); "ranking of methods is highly problem dependent" precedent.
7. [[extrapolative-bayesian-optimization-with-gaussian-process-and-neural-network-ens]] — Lim, Ng,
   Vaitesswar & Hippalgaonkar (2021), "Extrapolative Bayesian Optimization with Gaussian Process and Neural
   Network Ensemble Surrogate Models," Advanced Intelligent Systems. Surfaced by a sibling locus; GP
   dominance tied qualitatively to problem complexity/dimensionality.
8. [[coco-platform-comparing-continuous-optimizers-black-box-fulltext]] — Hansen et al., "COCO: A Platform
   for Comparing Continuous Optimizers in a Black-Box Setting," arXiv:1603.08785. Already in vault;
   background on the BBOB suite Kerschke & Trautmann and Rodriguez et al. both build on.
9. Locatelli (2003), "A Note on the Griewank Test Function," Journal of Global Optimization (DOI
   10.1023/a:1021956306041), and its 2024 continuation "Success Rate of Evolution Strategies on the
   Multimodal Griewank Function" (IEEE CEC 2024, DOI 10.1109/cec60901.2024.10612209) — retrieved as
   abstracts only via the OpenAlex API (both full texts are paywalled); not saved as vault notes because
   only the abstract, not the primary text, was accessible within budget. Source of the "Griewank gets
   simpler with increasing dimension" counterintuitive-property claim.
10. `paper/aaai27/supplement.tex`, `paper/aaai27/main.tex`, `paper/aaai27/references.bib`, `code/mbo.py` —
    primary repository artifacts, read and grepped directly (not vault notes; the paper under audit and its
    own implementation). Source of Table `tab:sfull`, the affine domain maps, and the zero-hit bibliography
    grep.
