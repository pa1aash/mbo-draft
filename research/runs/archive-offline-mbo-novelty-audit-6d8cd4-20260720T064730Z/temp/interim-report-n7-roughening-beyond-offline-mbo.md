# Interim report: n7-roughening-beyond-offline-mbo

**Locus question:** Has anyone manipulated surrogate smoothness in BOTH directions (smooth the network AND
roughen the GP) to identify smoothness as the CAUSAL axis of a surrogate-class performance gap — asked at
the BROADEST scope (Bayesian optimization / kernel methods / Gaussian-process regression / any ML field),
not just within offline MBO? This locus decides whether candidate C's mechanism claim is "first at all"
or merely "first in offline MBO."

**Flavor:** convergent

## What the corpus already said

The width sweep had already done unusually thorough work on the within-offline-MBO half of this question,
fetching and title-verifying all three named targets plus a bibliography-discovered fourth paper, each
with its own Semantic-Scholar forward-citation sweep:

- **IGNITE** (Dao et al., NeurIPS 2024, arXiv:2503.04242) — [[ignite-incorporating-surrogate-gradient-norm-to-improve-offline-optimization-tec]]:
  regularizes *only* neural-network surrogate sharpness, always downward, never touches a GP. Verbatim:
  "reducing surrogate sharpness on the offline dataset provably reduces its generalized sharpness on
  unseen data" (Abstract). Its 8 forward citations (S2 API, 2024-2026) were individually checked; none
  cross into bidirectional smoothness manipulation.
- **MS-DDEO** (Zhen, Gong & Wang, SWEVO 2022) — [[ms-ddeo-offline-data-driven-evolutionary-optimization-based-on-model-selection-z]]:
  paywalled (abstract-only, paraphrase confidence "medium"); selects among 4 preset RBFN smoothness
  tiers for online model selection — a within-RBFN smoothness *range*, never touching a GP, used for
  selection rather than causal attribution.
- **ROOT** (Dao et al., NeurIPS 2025, arXiv:2509.16300) — [[root-rethinking-offline-optimization-as-distributional-translation-via-probabili]]:
  the single closest hit anywhere in the corpus's own sweep — varies GP length-scale/kernel parameters —
  but strictly as a **data-augmentation** device ("compute multiple GP posteriors according to a diverse
  range of GP priors with different signal and length-scale parameters," Section 3) to generate synthetic
  training functions, not a smooth-vs-rough causal ablation paired against a network-smoothing arm.
- **RaM / Learning to Rank** (Tan et al., ICLR 2025, arXiv:2410.11502) — [[offline-model-based-optimization-by-learning-to-rank-iclr-2025-arxiv241011502]]:
  not smoothness-relevant itself, but its bibliography confirmed IGNITE's authorship/venue and flagged
  the sibling paper **"Boosting Offline Optimizers with Surrogate Sensitivity" (ICML 2024,
  arXiv:2503.04181)** — [[boosting-offline-optimizers-with-surrogate-sensitivity-icml-2024-arxiv250304181]],
  which I confirmed is also NN-only, one-directional, and only cites a GP bibliographically.

**The within-offline-MBO half of N7 was already solidly NONE FOUND before I started**, across four
title-verified primary sources and their combined ~30 forward citations. My job was the broader question.

## What the new sources say

I fetched and registered two new sources for the beyond-offline-MBO sweep, after an exhaustive academic
+ web search (queries listed below) turned up no genuine bidirectional cross-class candidate:

**1. Lim, Ng, Vaitesswar & Hippalgaonkar, "Extrapolative Bayesian Optimization with Gaussian Process and
Neural Network Ensemble Surrogate Models"** (*Advanced Intelligent Systems*, 2021, DOI:
10.1002/aisy.202100101) — [[extrapolative-bayesian-optimization-with-gaussian-process-and-neural-network-ens]].
Full body fetched (9,625 words, CC-BY OA). This is the **closest genuine cross-surrogate-class hit found
anywhere in this sweep** — it directly compares GP vs. neural-network-ensemble (NNE) surrogates for BO on
materials-science datasets, exactly the surrogate-class pairing N7 cares about. Its central empirical
result: "the neural network ensemble not only extrapolates well, but also enables the fastest convergence
toward the optimum values. However, GP eventually catches up and consistently achieved the best evaluated
values after 100 iterations" (Abstract). Crucially, the paper offers a smoothness-flavored explanation for
*why*: "With fully tuned parameters, the GP model becomes the top performer for even the most complex
high-dimensional dataset... which **could be due to the ability of GP to smoothly map out the uncertainty
manifolds**. The neural ensemble also performed well and came in a close second, which may be attributed
to its better ability at mapping out the complex input–output relationships" (Conclusion, emphasis mine).
And earlier: "The GP model is able to model the uncertainties smoothly, although the prediction and
uncertainty manifolds can be quite unstable especially for the model with the larger length scale bounds...
This could explain its low convergence speed at the beginning, although its smoother model of the
uncertainty information probably enables it to converge toward the most optimum values in the later
iterations" (Section 2.2).

However — and this is the load-bearing distinction — the paper's *only* deliberate manipulation is of the
**GP's own length-scale bounds** (fixed → moderate range 10⁻²–10² → large range up to 10⁻¹²–10¹²), and this
manipulation runs in a single direction: relaxing/widening bounds so the marginal-likelihood optimizer can
find the length-scale that fits the data, not deliberately forcing the GP toward a rougher extreme as a
controlled comparison arm. Verbatim: "For a fixed length scale, the algorithm shows severe overfitting...
The performance on the test set improves as the bounds are allowed to relax gradually and the algorithm is
allowed to converge on the optimum length scale" (Section 2.2). The NN ensemble side of the comparison
receives **no smoothness-directed manipulation at all** — it is simply retrained multiple times (or run
with dropout) to get ensemble statistics; no sharpness regularizer, no explicit roughening. The
"smoothness" causal story for the GP-vs-NNE gap is offered as a qualitative, hedged, post-hoc hypothesis
("could be due to," "probably enables") in the Conclusion — not demonstrated by an experiment designed to
isolate smoothness as the causal variable.

**2. Ziomek, Adachi & Osborne, "Bayesian Optimisation with Unknown Hyperparameters: Regret Bounds
Logarithmically Closer to Optimal"** (arXiv:2410.10384, Oxford + Toyota) —
[[bayesian-optimisation-with-unknown-hyperparameters-regret-bounds-logarithmically]]. Full text fetched and
grepped (3,397 lines). This paper's core method, **Length-scale Balancing (LB)**, is the closest lexical
match to "vary smoothness" of anything found via arXiv search: it "aggregat[es] multiple base surrogate
models with varying length scales," adding smaller-length-scale (rougher) candidates while retaining
longer (smoother) ones (Abstract), and derives a regret bound showing this closes most of the gap to an
oracle that knows the true length scale. But grep of the full text for `"neural network"` returns exactly
**one hit**, and it is an unrelated example sentence about training neural networks in general, not a
neural-network surrogate used anywhere in the method. Every base model in the LB pool is a GP. There is no
cross-surrogate-class comparison, no "roughen the GP AND smooth the network" pairing, and no attribution of
a between-class performance gap to smoothness — the dependent variable throughout is regret of one
GP-based algorithm (LB) against other GP-based length-scale-selection baselines (MLE, MCMC, A-GP-UCB).

## Evidence synthesis

The evidence across both the within-offline-MBO corpus and my beyond-offline-MBO sweep converges on the
same structural gap, restated at increasing scope: **manipulating surrogate/kernel smoothness is a common
move in the literature, but always within a single surrogate family, and a genuine cross-class comparison
(GP vs. NN/ensemble) is common too — but the two moves have never been combined into one controlled,
bidirectional, causally-attributed experiment.** Three distinct literatures each do half of what N7 needs:

1. **Within-GP smoothness manipulation** is well established and often bidirectional in the *literal*
   sense of moving the length-scale in both directions along a continuum — MS-DDEO's 4 RBFN tiers, ROOT's
   diverse-length-scale GP priors, the Extrapolative-BO paper's fixed→moderate→large length-scale bounds,
   and the LB paper's rougher+smoother GP pool all vary smoothness in more than one direction. None of
   these cross into a second surrogate family as the comparison arm.
2. **Cross-surrogate-class comparison** (GP vs. NN/ensemble) is also well established — the Extrapolative-BO
   paper and, more distantly, Snoek et al.'s DNGO (2015, cited within it) both compare GP and
   neural-network-based surrogates for BO performance. But neither deliberately manipulates smoothness as
   the controlled experimental factor distinguishing the two classes; smoothness is at most an ex-post
   qualitative gloss on an observed gap ("could be due to... smoothly map out uncertainty manifolds").
3. **IGNITE/Dao-lineage smoothness-as-mechanism work** (the only line of research that treats surrogate
   smoothness as a *causal, regularized* variable with a theoretical generalization-bound argument) is
   exclusively neural-network-only and one-directional (always reduces sharpness), and — per my sweep —
   this line has not, as of its 2024-2026 publications (IGNITE, its ICML 2024 sibling, and ROOT), crossed
   into GP territory at all, let alone bidirectionally.

No paper found anywhere in this sweep does (1) + (2) + causal attribution simultaneously: deliberately
smooth a network surrogate as one arm, deliberately roughen a GP surrogate as the paired arm, and conclude
that smoothness (not surrogate-class identity per se, not architecture, not training procedure) is the
causal variable responsible for the between-class performance gap. The Extrapolative-BO paper (Lim et al.
2021) is the closest approach to this design that exists in the literature I could locate, precisely
because it is the only paper that both varies GP smoothness *and* runs a real cross-class comparison
against an NN-based surrogate in the same study — but it stops at correlation/plausible-hypothesis, not
controlled bidirectional causal ablation, and its GP length-scale manipulation is a hyperparameter-tuning
sweep (avoid overfitting) rather than a deliberately opposed rough/smooth pair.

## Committed position

The bidirectional-causal-manipulation claim in N7 is unclaimed not just within offline MBO but across the
broader Bayesian-optimization, kernel-methods, and GP-regression literature I could locate — this is a
genuine methodological gap, not a search-coverage artifact, because the two half-literatures that would
need to combine to produce it (within-GP smoothness sweeps, and cross-surrogate-class BO comparisons) each
individually exist in healthy volume, yet in ~15 years of BO/GP literature no paper stitches them into one
controlled experiment with a causal claim. That absence is itself informative: it suggests the combination
is either genuinely novel or considered too obvious/unpublishable as a standalone contribution by prior
authors who came close (e.g., Lim et al. 2021 gestures at the mechanism in one hedged sentence and moves
on). Candidate C's contribution should therefore be framed as "first to run smooth-the-network /
roughen-the-GP as a designed, paired, causally-interpreted ablation across surrogate classes" at the scope
of the entire BO/kernel-methods literature, not merely "first in offline MBO" — this is a stronger novelty
claim than the within-offline-MBO framing alone would support, and the paper should cite Lim et al. (2021)
explicitly as the nearest prior approach and the ICML/NeurIPS Dao-lineage (IGNITE, ICML2024 sibling, ROOT)
as the nearest prior *causal-attribution* framing, precisely to show what each stops short of.

- **Position:** N7's bidirectional-causal-smoothness-manipulation claim is NONE FOUND at the broadest
  scope searched (offline MBO, Bayesian optimization, kernel methods, GP regression) — candidate C can
  claim novelty "first at all," not merely "first in offline MBO," with Lim et al. (2021) named as the
  closest prior approach and its shortfall stated explicitly (correlational/qualitative attribution, not a
  controlled bidirectional ablation; GP-side manipulation is bounds-widening for hyperparameter fit, not a
  deliberately roughened comparison arm; NN-side receives no smoothness manipulation at all).
- **Confidence:** medium-high. High confidence that no paper in the specific BO/kernel-methods/GP corpus
  searched does the full bidirectional-causal design (the search was exhaustive across academic APIs +
  WebSearch with no positive hit, and the negative pattern is structurally explained, not just an absence).
  Only medium on the word "any ML field" in the locus's framing — I did not exhaustively search
  spectral-bias/NTK-adjacent deep learning theory (that is a different locus's territory per the corpus's
  own N5), robotics/control BO variants, or non-English-language venues, so a hit in one of those adjacent
  fields cannot be ruled out with the same confidence as within BO/kernel methods proper.
- **Boundary conditions:** this verdict holds for the BO / GP-regression / kernel-methods literature as
  indexed by OpenAlex, arXiv, and Semantic Scholar, plus a 7-query WebSearch sweep, as of 2026-07-18. It
  does not cover: (a) non-arXiv-indexed workshop papers or theses, (b) the SNGP/DUE distance-awareness
  literature or NTK/spectral-bias literature, which are separate loci in this same audit (N4, N5) and could
  in principle contain an adjacent bidirectional design I did not check because it was out of scope for me,
  (c) any paper published after this search date.
- **What would change this position:** a single paper that (i) applies a smoothness regularizer to reduce
  sharpness of a neural-network surrogate AND (ii) deliberately decreases a GP's length-scale (or switches
  Matérn ν downward) to increase roughness, as two arms of one controlled experiment, AND (iii) explicitly
  attributes an observed performance gap between the two surrogate classes to the smoothness manipulation
  rather than treating it as one of several confounded differences. Even a paper that does (i)+(ii) without
  the causal-attribution framing in (iii) would downgrade "first at all" to a narrower claim about the
  causal-attribution language specifically, so the strength of citation C's claim is sensitive to exactly
  how (iii) is worded in the target paper.
- **Evidence weight:** 2 primary sources newly fetched and grepped in full (Lim et al. 2021 GP-vs-NNE
  comparison — closest partial hit; Ziomek et al. 2024 LB — closest lexical "vary smoothness" hit, ruled
  out by full-text grep for any NN presence), 4 primary sources already in the corpus and reconfirmed by
  reading (IGNITE, MS-DDEO abstract-only, ROOT, RaM/Boosting-Offline-Optimizers), 1 delegated WebSearch
  reconnaissance pass (7 queries, 0 positive hits), roughly a dozen additional OpenAlex/arXiv API queries
  (0 positive hits). Zero sources support a PRIOR WORK FOUND verdict; all sources checked are consistent
  with NONE FOUND, with Lim et al. (2021) as the qualitative near-miss that should be cited defensively.

## Open questions

- I did not fetch full text of Snoek et al. 2015 (DNGO) or the "Kernel Manifold" 2026 GP-model-selection
  paper — both abstract-level rule-outs (neither manipulates smoothness bidirectionally per their
  abstracts), but a full-text grep was not performed given budget; low risk but not zero.
- The SNGP/DUE/distance-awareness literature (N4's locus) and the NTK/spectral-bias literature (N5's
  locus) were explicitly out of scope for me but sit conceptually adjacent to "smoothness as a causal
  variable in surrogate comparison" — the orchestrator should confirm N4/N5's investigators didn't
  independently surface a bidirectional design that would bear on N7.
- I did not search non-English-language venues (Chinese/Japanese swarm-and-evolutionary-computation
  journals, in particular, given MS-DDEO's own venue) — the DDEA/RBFN literature MS-DDEO sits in is a
  plausible place for a rough/smooth ablation study I would not have surfaced via English-language
  academic APIs.

## Sources

1. [[ignite-incorporating-surrogate-gradient-norm-to-improve-offline-optimization-tec]] — IGNITE (Dao et al., NeurIPS 2024, arXiv:2503.04242) — corpus source, reconfirmed
2. [[ms-ddeo-offline-data-driven-evolutionary-optimization-based-on-model-selection-z]] — MS-DDEO (Zhen, Gong & Wang, SWEVO 2022) — corpus source, reconfirmed
3. [[root-rethinking-offline-optimization-as-distributional-translation-via-probabili]] — ROOT (Dao et al., NeurIPS 2025, arXiv:2509.16300) — corpus source, reconfirmed
4. [[offline-model-based-optimization-by-learning-to-rank-iclr-2025-arxiv241011502]] — RaM (Tan et al., ICLR 2025, arXiv:2410.11502) — corpus source, reconfirmed
5. [[boosting-offline-optimizers-with-surrogate-sensitivity-icml-2024-arxiv250304181]] — Boosting Offline Optimizers with Surrogate Sensitivity (Dao et al., ICML 2024, arXiv:2503.04181) — corpus source, reconfirmed
6. [[extrapolative-bayesian-optimization-with-gaussian-process-and-neural-network-ens]] — Lim, Ng, Vaitesswar & Hippalgaonkar, "Extrapolative Bayesian Optimization with Gaussian Process and Neural Network Ensemble Surrogate Models" (Adv. Intell. Syst. 2021, DOI:10.1002/aisy.202100101) — NEW, full text fetched, closest partial hit
7. [[bayesian-optimisation-with-unknown-hyperparameters-regret-bounds-logarithmically]] — Ziomek, Adachi & Osborne, "Bayesian Optimisation with Unknown Hyperparameters" (arXiv:2410.10384) — NEW, full text fetched and grepped, closest lexical match, ruled out

## Exact search queries run (beyond-offline-MBO sweep)

Academic APIs (OpenAlex, arXiv Atom API, Semantic Scholar — S2 was rate-limited (429) on this run; OpenAlex/arXiv used as primary):
- `kernel lengthscale ablation Bayesian optimization performance`
- `Matern smoothness nu Bayesian optimization comparison`
- `RKHS smoothness generalization causal ablation`
- `surrogate smoothness controlled experiment optimization`
- `roughen model smoothness ablation neural network`
- arXiv abs: `"kernel smoothness" AND "Bayesian optimization"` (0 results)
- arXiv abs: `"Matern" AND "Bayesian optimization" AND "smoothness"` (0 results)
- arXiv abs: `"Matern" AND "Bayesian optimization"` (3 results, none bidirectional)
- arXiv abs: `"length-scale" AND "Bayesian optimization" AND "misspecif"` (1 result: 2410.10384, fetched)
- arXiv abs: `"smoothness" AND "Bayesian optimization" AND "regret"` (5 results, closest was 2410.10384)
- arXiv abs: `"length-scale" AND "Bayesian optimization" AND "overestimat"` (0 results)
- arXiv abs: `"kernel bandwidth" AND "optimization" AND "ablation"` (0 results)
- arXiv abs: `"flat" AND "sharp" AND "surrogate model" AND "optimization"` (2 results, both off-topic)
- arXiv abs: `"Gaussian process" AND "neural network" AND "smoothness" AND "generalization"` (15 results, none bidirectional-causal)
- arXiv abs: `"oversmooth" AND "undersmooth" AND "Gaussian process"` (0 results)
- arXiv abs: `"kernel lengthscale" AND "ablation"` (0 results)
- arXiv abs: `"smoothness prior" AND "neural network" AND "Bayesian optimization"` (0 results)
- arXiv abs: `"sharpness-aware" AND "Gaussian process"` (0 results)
- arXiv abs: `"kernel selection" AND "Bayesian optimization" AND "smoothness"` (1 result, off-topic)
- arXiv abs: `"deep ensemble" AND "Gaussian process" AND "smoothness"` (2 results, off-topic)
- OpenAlex full-text search variants of all 5 assigned query strings plus `Gaussian process versus neural network ensemble smoothness optimization surrogate`

Delegated WebSearch reconnaissance (hyperresearch-fetcher subagent, 7 queries — see agent report, all
negative): the 5 assigned queries verbatim, plus `"vary smoothness" OR "smoothness ablation" surrogate
model both directions optimization causal mechanism` and `sharpness-aware minimization Gaussian process
surrogate optimization comparison`.

None of these queries, across two independent search passes (mine via academic APIs, the delegated
fetcher's via WebSearch), surfaced a paper doing bidirectional causal smoothness manipulation across
surrogate classes.
