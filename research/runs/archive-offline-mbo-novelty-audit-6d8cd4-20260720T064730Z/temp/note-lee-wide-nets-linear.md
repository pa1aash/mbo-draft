**Citation**: Jaehoon Lee, Lechao Xiao, Samuel S. Schoenholz, Yasaman Bahri, Roman Novak, Jascha Sohl-Dickstein, Jeffrey Pennington (Google Brain). "Wide Neural Networks of Any Depth Evolve as Linear Models Under Gradient Descent." NeurIPS 2019. arXiv:1902.06720 (v4, 8 Dec 2019).

Source text: `research/raw/txt/lee-wide-nets-linear-2019.txt` (3713 lines, extracted via pdftotext from arXiv:1902.06720v4 PDF). Title verified against header lines 1-6.

## What the paper actually does

This is the direct empirical follow-up to Jacot et al.'s NTK theory paper, from an overlapping author group (Lee is also first author of the Deep-Neural-Networks-as-Gaussian-Processes paper already in this locus's corpus). They prove that in the infinite-width limit, gradient-descent training dynamics reduce exactly to a linear (first-order Taylor) model around initialization, and that this linearized model's test-time predictions are drawn from a Gaussian process with the NTK as its kernel (their Theorem 2.2, extending Jacot et al.). The paper's main empirical contribution is testing how well this infinite-width theoretical prediction matches *actual finite, practically-sized* networks, across fully-connected, convolutional, and wide-ResNet architectures, multiple optimizers (SGD, momentum, minibatching) and loss functions (MSE, cross-entropy), on MNIST and CIFAR-10.

## Claim relevance

### N5 — does the NTK/spectral-bias REGIME (width thresholds, training-to-convergence) plausibly apply to a typical offline-MBO ensemble surrogate's finite width?

**On what widths were actually tested and found to agree well with the infinite-width theory** — the paper's demonstration figures span a wide range of practical widths, not just extreme toy sizes:

> "Experiment is for 10 class MNIST classification using a ReLU fully connected network with 2 hidden layers of width n = 2048..." (Figure S3 caption, line 1383-1384)

Their width-sweep figure (Figure 3 / S3-analogues) explicitly tests n = 32, 64, 128, 256, 512, 1024, 2048, 4096 for the same fully-connected architecture (lines 1395-1464) — i.e., linearization/GP-agreement is demonstrated across a wide span from very narrow (n=32) to wide (n=4096), not just at extreme widths, though the paper's discussion frames the QUALITY of agreement as improving with width rather than reporting a specific pass/fail threshold.

**Directly on the "does this regime plausibly apply in practice" question** — the paper's own summary statement:

> "Our results suggest that a surprising number of realistic neural networks may be operating in the regime we studied." (Section, Discussion, line 934-935)

But this optimism is immediately and explicitly qualified two sentences later, in a way that is load-bearing for this locus:

> "Some layers of modern neural networks may be operating far from the linearized regime... Furthermore, in Novak et al. [7], it is shown that the comparison of performance between finite- and infinite-width networks is highly architecture-dependent. In particular, it was found that infinite-width networks perform as well as or better than their finite-width counterparts for many fully-connected or locally-connected architectures. However, the opposite was found in the case of convolutional networks without pooling. It is still an open research question to determine the main factors that determine these performance gaps." (Discussion, lines 941-949)

**A second, independently load-bearing quote directly relevant to the offline-MBO SMALL-DATA setting** (the same small-dataset condition Li/Rudner/Wilson invoke for their basin-of-attraction mechanism):

> "Preliminary observations in Lee et al. [5] showed that wide neural networks trained with SGD perform similarly to the corresponding GPs as width increase, while GPs still outperform trained neural networks for both small and large dataset size." (Discussion, lines 942-944)

This is a second, independent primary source (distinct from the Lee et al. 2018 NNGP paper already in the locus corpus) stating that GPs beat trained finite NNs even as width grows, when the dataset is small — which is exactly the offline-MBO/BO regime (Li/Rudner/Wilson: BO problems "rarely exceed about 600 data points").

**What it stops short of**: like Jacot et al. and Lee et al. 2018, this paper is a supervised point-estimate training-dynamics paper — it never constructs an ensemble, never studies acquisition functions, Bayesian optimization, or offline MBO, and never reports a width threshold *specific to ensemble-mean smoothness*. Its architecture-dependence caveat ("highly architecture-dependent," "open research question") is the single most important qualifier for whether the NTK/spectral-bias regime can be invoked as a clean explanation in a specific paper without checking that paper's own architecture.

## Grep evidence

Ran on `research/raw/txt/lee-wide-nets-linear-2019.txt` (3713 lines):
- "width": 71 hits
- "finite width": 24 hits
- "practically-sized": 1 hit (abstract, "excellent empirical agreement... even for finite practically-sized networks")
- "architecture-dependent": 1 hit (Discussion, quoted above)
- "open research question": 1 hit (Discussion, quoted above)
- Widths explicitly tested in figures: n = 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192 (fully-connected and convolutional experiments, lines 672, 809, 1278, 1385, 1395-1464, 2556)
- "ensemble": checked separately — 0 hits; this paper does not study ensembles at all.

The architecture-dependence caveat and the explicit "GPs still outperform trained neural networks for both small and large dataset size" line are the two most load-bearing findings for this locus: they mean the NTK/spectral-bias regime is empirically real but NOT a universal, architecture-independent guarantee, and that the small-data condition (which characterizes offline MBO) is one where GPs are reported to win regardless of NN width — undercutting a pure "just make it wider and the ensemble would match/beat the GP" reading of N5.
