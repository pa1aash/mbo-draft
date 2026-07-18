**Citation**: Zhongxiang Dai, Yao Shu, Bryan Kian Hsiang Low (National University of Singapore), Patrick Jaillet (MIT). "Sample-Then-Optimize Batch Neural Thompson Sampling." **NeurIPS 2022** (36th Conference on Neural Information Processing Systems). arXiv:2210.06850 (v1, 13 Oct 2022). Title-verified against the extracted PDF header. This is the paper Li/Rudner/Wilson (ICLR 2024) cite as "Dai et al. (2022)" for the claim that deep ensembles fail to explore effectively in Bayesian optimization.

## What the paper does

Dai et al. introduce two Thompson-sampling-based Bayesian optimization algorithms — STO-BNTS and STO-BNTS-Linear — that use a single, deterministically-trained neural network (not an ensemble) as the BO surrogate, connected theoretically to the neural tangent kernel (NTK). At each iteration, the algorithm perturbs the NN's initialization/training objective with a random linear term (the "sample-then-optimize" trick of Matthews et al. 2017), trains the perturbed network to convergence, and treats the resulting trained function as one sample from an implicit GP posterior with the NTK as kernel — exact in the infinite-width limit, and provably approximate for finite width. They derive regret upper bounds for both the infinite-width and finite-width regimes (Theorems 1 and 2), and Theorem 2 explicitly states that the finite-width regret bound shrinks as network width m grows, becoming exact as m -> infinity. They validate empirically on a 1D synthetic BO problem, three AutoML hyperparameter-tuning tasks (random forest, XGBoost, CNN), three RL control-tuning tasks (Lunar Lander, robot pushing, rover trajectory planning), and an MNIST image-optimization task, comparing against GP-TS, GP-UCB, Neural UCB, Neural TS, and a "Deep Ensemble" baseline (Lakshminarayanan et al. 2017) throughout.

Critically, the paper runs its own within-paper network-WIDTH ablation (m = 16, 64, 512, against a default of m=64) for its own STO-BNTS/STO-BNTS-Linear surrogate, in the synthetic experiment (Fig. 1d) and again for a CNN surrogate in the image-optimization experiment (Fig. 6/Appendix F.4), and finds wider networks reduce regret / improve performance monotonically, consistent with their Theorem 2. However, this width ablation is applied ONLY to their own single-network NTK-linked surrogate — it is never applied to the "Deep Ensemble" baseline, whose architecture is held fixed (matching whatever default is used, e.g. L=2, m=256 in the real-world tasks) and never swept across widths. The paper also runs a separate depth-and-width architecture search (L in {1,2,8}, m in {64,256,512}) for their own methods (Sec. 5.2, Figs. 2/4) and picks L=2, m=256 as the recommended default, again without applying this search to the Deep Ensemble baseline.

## Claim relevance

### N5 — resolving what Dai et al. (2022) actually claims about "ensembles can't explore effectively"

Li/Rudner/Wilson paraphrase this paper as: "These findings are also supported by results shown in Dai et al. (2022), where deep ensembles do not perform well in Bayesian optimization because they are unable to to explore the space effectively" (L/R/W, Appendix D.3). This IS a fair paraphrase of Dai et al.'s own text, sourced from their synthetic experiment (Fig. 1a-d):

> "The Deep Ensemble method [36] in Fig. 1a can be regarded as a reduced version of our STO-BNTS algorithm (Algo. 1) in which the term <grad_theta f(x;theta_0), theta'_0> (i.e., the second term in line 6 of Algo. 1) is removed. As a result, Deep Ensemble does not enjoy the theoretical guarantees of our algorithms (Sec. 4)... the figures show that compared with the naive baseline of Deep Ensemble, our STO-BNTS and STO-BNTS-Linear are able to display more exploratory behaviors in unexplored regions (e.g., the interval of [0.2, 0.4])." (Section 5.1, p.7)

> "Due to its lack of exploration as illustrated in Fig. 1a, Deep Ensemble fails to reach zero regret in Fig. 1d." (Section 5.1, p.7)

The mechanism Dai et al. name for ensemble underperformance is ALGORITHMIC/theoretical, not width-based: Deep Ensemble is missing a specific NTK-gradient perturbation term that STO-BNTS adds, and this missing term is what breaks the theoretical no-regret guarantee — not insufficient per-member network width or insufficient ensemble cardinality K. Grepping the full text, "ensemble" and "explor[ation]" never co-occur with a width-conditioned claim; the exploration critique of Deep Ensemble is architecture-independent in how it is framed.

### N5 — does Dai et al. run "the decisive missing experiment" (width ablation holding K fixed, inside a BO surrogate comparison vs GP)?

**Partial and NOT the target experiment.** Dai et al. DO run a genuine within-paper width ablation inside a BO surrogate comparison that includes a GP-TS baseline:

> "compared with the green curve for which m = 64, using a wider NN (gray curve, m = 512) substantially improves the performance of STO-BNTS-Linear yet employing a shallower NN (yellow curve, m = 16) significantly degrades the performance. These observations agree with Theorem 2 which states that a larger width m reduces the regret of STO-BNTS-Linear. Similarly, the NN surrogate model of STO-BNTS should also be wide enough since the use of a narrower NN (light blue curve, m = 16) also leads to a worse performance for STO-BNTS." (Section 5.1, p.7)

> "The width m should be chosen to be large enough since our experiments in Sec. 5.1 (Fig. 1d) and Sec. 5.4 (Fig. 6 in Appendix F.4) suggest that a larger width usually improves the performance." (Section 5.5, "Discussion", p.9)

This confirms: wider networks -> better BO performance / lower regret is an established, theoretically-grounded (Theorem 2) and empirically-demonstrated (Figs. 1d, 6) finding in the BO surrogate literature, for a single NTK-linked neural network surrogate, inside a comparison that includes GP-TS.

BUT this is not N5's proposed experiment, for two decisive reasons: (1) the surrogate being width-swept is a SINGLE deterministic network trained via sample-then-optimize (theoretically an implicit GP-posterior sample as width grows), not a K-member deep ensemble — there is no "ensemble size K" to hold fixed because there is no ensemble in the width-swept method; (2) the "Deep Ensemble" baseline that IS present in the same figures (Fig. 1d, Fig. 2, Fig. 4) is never width-ablated — its architecture is fixed at whatever default is used per experiment, so the paper never asks "does widening the Deep Ensemble's members close its gap with GP-TS?" That specific question — vary per-member width of the K-member Deep Ensemble baseline itself, holding K fixed, and check whether its ranking vs. GP-TS changes — is NOT run anywhere in this paper.

**Verdict: NONE FOUND for N5's precise ask, inside Dai et al. (2022).** The paper resolves the citation-provenance question (Dai's own claim about ensembles is algorithmic/exploration-term-based, not width-based) and supplies adjacent-but-distinct evidence that width improves a *non-ensemble* NTK-linked NN surrogate's BO performance — which is suggestive corroboration for N5's underlying width-matters intuition, but does not constitute prior work directly testing N5's ensemble-specific hypothesis.

## Grep evidence

Ran on `research/raw/txt/dai-sto-bnts-neurips2022.txt` (3116 lines, from arXiv:2210.06850 v1 PDF via pdftotext):
- "ensemble": 10 hits (all "Deep Ensemble" as a fixed-architecture baseline; 0 hits combining "ensemble" with a swept width value)
- "width": 47 hits (all describing STO-BNTS/STO-BNTS-Linear/CNN surrogate width, e.g. m=16/64/256/512; 0 hits describing a swept Deep Ensemble width)
- "explor": 17 hits (exploration framing tied to the missing NTK-gradient term, not to width or K)
- "K =" / "ensemble size" / "number of models": 0 hits (Deep Ensemble's member count is never stated as a variable or swept)
- "regret": 60+ hits (Theorems 1 and 2 are regret bounds; Theorem 2's finite-width regret term is the theoretical basis for "wider net -> lower regret")
- "Thompson": 90+ hits (this is a Thompson-sampling paper throughout, matching the citation-trap-adjacent "Sample-Then-Optimize Batch Neural Thompson Sampling" title L/R/W's bibliography lists as "Sample-then-optimize batch neural thompson sampling, 2022")
