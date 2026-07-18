**Citation**: Stanislav Fort (Google Research), Huiyi Hu (DeepMind), Balaji Lakshminarayanan (DeepMind). "Deep Ensembles: A Loss Landscape Perspective." arXiv:1912.02757 (v1: 5 Dec 2019; v2: 25 Jun 2020). Not published at a peer-reviewed venue as of extraction; widely cited workshop/arXiv report from the same DeepMind group that wrote the "field-standard K=5" ensemble paper (Lakshminarayanan et al. 2017).

Source text: `research/raw/txt/fort-loss-landscape-2019.txt` (875 lines, extracted via pdftotext from arXiv:1912.02757v2 PDF). Title verified against header lines 1-8.

## What the paper actually does

Fort, Hu & Lakshminarayanan investigate *why* deep ensembles trained with independent random initialization outperform single-mode approximate-Bayesian methods (MC-dropout, variational Gaussian approximations, subspace sampling) at uncertainty quantification and robustness. Their central empirical method is to visualize and quantify similarity **in function space** (not weight space) between (a) checkpoints along a single SGD training trajectory, (b) samples from four different "subspace sampling" approximate-Bayesian methods anchored at one optimum, and (c) independently-trained ensemble members starting from different random initializations. They find that random initializations land in qualitatively different loss-landscape modes whose function-space predictions are far apart, while trajectory/subspace samples anchored at one optimum stay clustered within a single functional mode despite sometimes-large weight-space movement. They introduce a "diversity-accuracy plane" and show random-initialization ensembling Pareto-dominates every subspace-sampling method tested (MC-dropout, diagonal Gaussian, low-rank Gaussian, random-subspace sampling) on CIFAR-10/100 and ImageNet.

## Claim relevance

### N5 — is "ensemble diversity" reducible to width/capacity, or is it a distinct mode-diversity mechanism?

This paper never once uses the words "width" or "capacity" (0 hits each on full-text grep) — its explanatory mechanism for ensemble behavior is entirely orthogonal to network width. The load-bearing mechanism claim:

> "One possible hypothesis is that ensembles tend to sample from different modes in function space, whereas variational Bayesian methods... might fail to explore multiple modes even though they are effective at capturing uncertainty within a single mode." (Section 1, Introduction, lines ~110-114)

> "Through extensive experiments, we show that trajectories of randomly initialized neural networks explore different modes in function space, which explains why deep ensembles trained with just random initializations work well in practice." (Section 6, Discussion, line 553-555)

> "random initializations explore entirely different modes, while functions along an optimization trajectory or sampled from the subspace thereof cluster within a single mode predictions-wise, while often deviating significantly in the weight space." (Abstract)

This directly complicates a pure "jaggedness is a finite-width/undertraining artifact" reading of ensemble behavior: Fort et al.'s mechanism for why ensemble MEMBERS disagree with each other is mode diversity from independent random initialization — a property of the loss landscape's multimodality under gradient descent, not a property that a wider network (still trained once, from one initialization) would fix. Their own related-work sentence acknowledges ensembles can underperform "for small ensemble sizes" (line 104) when bootstrap resampling is used, but this is about resampling noise, not width.

**What it stops short of**: Fort et al. never construct a Gaussian-process baseline, never discuss NTK theory or infinite-width GP-equivalence, never vary network width as an independent variable, and never study Bayesian optimization, acquisition functions, or offline MBO. It cannot directly adjudicate whether an ensemble's *posterior MEAN* (as opposed to member-to-member disagreement) is "jagged" in a width-dependent way — it studies functional disagreement among members, not the smoothness of the averaged mean function itself.

## Grep evidence

Ran on `research/raw/txt/fort-loss-landscape-2019.txt` (875 lines):
- "width": 0 hits
- "capacity": 0 hits
- "ensemble size": 2 hits (both about small-ensemble-size caveats for bootstrap resampling, not width)
- "mode": 45 hits
- "diversity": 35 hits
- "function space": 19 hits
- "random initialization": 21 hits
- "Bayesian": 26 hits
- "single model": 0 hits
- "Gaussian process": 0 hits (checked separately — not a GP-comparison paper)
- "neural tangent kernel" / "NTK" / "spectral": 0 hits

Zero hits for "width," "capacity," "Gaussian process," and "NTK"/"spectral" confirm this paper's mechanism for ensemble behavior (loss-landscape mode diversity from random initialization) is a genuinely distinct axis from the NTK/spectral-bias width story — it is evidence that "why do ensemble members disagree" and "why is a single finite network's function jagged/undertrained" are two different, non-reducible mechanisms in the literature, which matters for whether N5's width-artifact reading is the WHOLE story or only part of it.
