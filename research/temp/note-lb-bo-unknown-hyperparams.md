## Full citation

Juliusz Ziomek, Masaki Adachi, Michael A. Osborne.
**"Bayesian Optimisation with Unknown Hyperparameters: Regret Bounds Logarithmically Closer to Optimal."**
University of Oxford (Machine Learning Research Group) + Toyota Motor Corporation.
arXiv:2410.10384v3 [stat.ML], v1 posted 14 Oct 2024, this version 22 Nov 2024.

Downloaded and title-verified locally: `research/raw/pdf/2410.10384.pdf` →
`research/raw/txt/lb-bo-unknown-hyperparams.txt` (3397 lines, full body extracted via pdftotext).

## What the paper actually does

The paper addresses length-scale (smoothness-hyperparameter) misspecification in single-GP Bayesian
optimization. Standard BO fits the GP length-scale by maximizing marginal likelihood on observed data,
which risks misspecification if the true objective is less smooth in unexplored regions. The prior
theoretical fix, A-GP-UCB (Berkenkamp et al. 2019), progressively *decreases* the length scale
(monotonically roughens the model over time) but has no stopping rule, causing over-exploration. This
paper proposes **Length-scale Balancing (LB)**: aggregate multiple base GP surrogate models at different
length scales simultaneously, intermittently adding smaller-length-scale (rougher) candidates while
retaining longer-length-scale (smoother) ones, to balance exploration/exploitation. It derives a regret
bound showing LB is only O(log g(T)) away from the oracle-length-scale regret, versus A-GP-UCB's O(g(T)),
and empirically shows LB beats A-GP-UCB, MLE, and MCMC length-scale-selection baselines on synthetic and
real benchmarks.

## Claim relevance

### N7 (bidirectional smoothness manipulation, beyond offline MBO) — NONE FOUND; this is a within-GP-family
### length-scale ADAPTATION paper, not a cross-surrogate-class causal ablation

LB is the closest arXiv hit to "vary smoothness" language found in this entire beyond-offline-MBO sweep
because its core mechanism literally sweeps the length-scale hyperparameter (which "defines the
smoothness of the functions the optimizer will consider," per its own abstract) toward *both* smaller
(rougher) and larger (smoother) ends of a pool of candidate GPs simultaneously. But it fails N7's bar on
every count that matters:

1. **Single surrogate family throughout.** Every base model in the LB pool is a GP; grep of the full
   extracted text for "neural network" returns exactly one hit, and it is an unrelated example sentence
   ("a generic algorithm for optimizing neural networks could enable people to train...", line 3296), not
   a neural-network surrogate used anywhere in the method or experiments. There is no NN-surrogate arm at
   all, so there is no "smooth the network AND roughen the GP" pairing — only "vary the GP's own
   length-scale."
2. **No surrogate-class performance gap is the object of study.** The paper's dependent variable is
   cumulative regret of one optimization algorithm (LB) against length-scale-selection baselines (MLE,
   MCMC, A-GP-UCB) — all still GP-based. It never asks "why does surrogate class X outperform surrogate
   class Y" and never attributes any performance gap to smoothness as a causal mechanism distinguishing
   two model families.
3. **Adaptive aggregation, not controlled ablation.** LB's mechanism is an online ensembling/scheduling
   trick (add small-length-scale candidates over time while keeping large ones) aimed at *regret
   minimization under an unknown true smoothness*, not a designed experiment that deliberately sets
   smoothness to two opposite extremes to isolate its causal effect.

Grep evidence (full text, 3397 lines): `"neural network"` → 1 hit (irrelevant, see above); `"ensemble"` →
0 hits in the GP-vs-NN sense (the paper's own multi-GP "aggregation" is not called an ensemble);
`"roughen"` → 0 hits; `"both direction"` → 0 hits; `"causal"` → 0 hits; `"surrogate class"` → 0 hits.

**Verdict: NONE FOUND for N7.** This paper establishes that GP length-scale (smoothness) misspecification
matters causally for BO regret — a useful adjacent fact — but entirely within one surrogate family and
without any cross-class comparison or deliberate bidirectional roughen/smooth ablation.

## Search discovery path

Found via arXiv Atom API query `abs:"smoothness" AND abs:"Bayesian optimization" AND abs:"regret"` during
the beyond-offline-MBO sweep for N7 (locus n7-roughening-beyond-offline-mbo).
