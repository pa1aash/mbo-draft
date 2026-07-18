# Minimizing UCB: a Better Local Search Strategy in Local Bayesian Optimization

**Full citation:** Zheyi Fan, Wenyu Wang, Szu Hui Ng, Qingpei Hu, "Minimizing UCB: a Better Local Search
Strategy in Local Bayesian Optimization," *Advances in Neural Information Processing Systems 37* (NeurIPS
2024). arXiv:2405.15285 (v1, 24 May 2024). Published version confirmed via OpenAlex
(doi:10.52202/079017-4151, host venue "Advances in Neural Information Processing Systems 37",
`is_published: true`) — this is a peer-reviewed NeurIPS 2024 paper, not merely an arXiv preprint.

## What the paper actually does

Develops a new local Bayesian-optimization algorithm, MinUCB, for high-dimensional black-box
minimization. Starting from the approximate-gradient-descent family of local BO methods (GIBO, Müller et
al.), the paper proves a formal relationship between (a) taking a gradient-descent step using the GP
posterior-mean gradient and (b) taking a step that minimizes the confidence-bound acquisition
UCB(x) = μ_D(x) + βσ_D(x) (β>0) directly. It shows minimizing this bound gives a tighter, better-informed
descent step than approximate gradient descent because it "fully utilizes the posterior distribution,"
and derives convergence guarantees for MinUCB matching GIBO's rate. It then extends to a look-ahead
variant, LA-MinUCB, and validates empirically on synthetic functions and a real-world trajectory-planning
task, showing MinUCB/LA-MinUCB outperform GIBO, MPD, TuRBO, and ARS as local-search baselines.

The key theoretical/illustrative content for this audit is Section 4 and Figure 1: the paper explicitly
characterizes minimizing the confidence-bound acquisition as an emergent LOCAL search strategy, and
grounds this characterization directly in the fact that the bound is small near sampled points and grows
with distance from them — i.e., posterior-variance growth away from data is the stated mechanism by
which a confidence-bound acquisition confines its own effective search radius.

## Claim relevance

**N4** — "The GP wins because its posterior variance grows away from the data, which makes LCB an
implicit trust region." **Verdict: PARTIAL — the causal mechanism is stated explicitly for a UCB/LCB-style
confidence-bound acquisition in a local-BO paper, but the paper uses "local strategy" language, not
"(implicit) trust region" language, for its own method.**

The paper's own confidence-bound-minimization step (mu + beta*sigma minimized for a MINIMIZATION problem)
is the mirror image of the audited paper's LCB (mu - beta*sigma, maximized for a maximization/pessimism
problem) — same acquisition family, same beta-weighted-sigma structure, opposite sign convention because
of minimize-vs-maximize framing. Verbatim, describing Figure 1's illustrative 1-D example:

> "The right figure illustrates UCB across the design space. Here we see that it is small only near the
> sampled point, and increases as it moves further away, indicating that minimizing UCB can be viewed as
> local strategy."

And from the main text (Section 4, deriving why the confidence-bound step behaves as it does):

> "The standard deviation term σ_D(x) has an upper bound and will not grow faster than the quadratic
> function, which means the UCB will not change drastically."

This is the precise causal chain N4 hypothesizes — posterior sigma is small near data and grows away from
it, so an acquisition function built from mu +/- beta*sigma is effectively confined to behave locally
near the current data — stated explicitly and derived formally (Theorem 1 and the surrounding convergence
analysis), in a 2024 NeurIPS paper that is NOT one of the four papers (SNGP, DUQ, DUE, TuRBO) already
exhaustively checked by the corpus's prior N4 locus.

**What it stops short of:** the paper never uses the phrase "trust region" (or "implicit trust region") to
describe its OWN mechanism — "trust region" appears only 3 times in the paper, all as citations to TuRBO
and other EXPLICIT trust-region baselines in the related-work/experiments sections (grep-verified). MinUCB's
own framing is "local search strategy" / "local exploitation," never "(implicit) trust region." So the
literal phrase-level synthesis in the audited paper's hypothesis ("...makes LCB an implicit trust region")
remains a novel naming/framing move — no prior paper found calls a bare LCB/UCB acquisition an "implicit
trust region" — but the underlying MECHANISM (variance-growth-away-from-data confines an unconstrained
confidence-bound acquisition to local/near-data behavior) is independently derived and stated, with a
supporting theorem, in this adjacent local-BO literature. This narrows N4's available novelty claim to the
naming/synthesis level ("implicit trust region" as a label) rather than the causal-mechanism level (bound
narrow near data, wide far from data, confines effective search) — that mechanism itself is now PARTIAL,
not NONE FOUND, once the search widens beyond the SNGP/DUQ/DUE/TuRBO four-paper set.

Also relevant to the paper's own beta=0 control (reported elsewhere in this audit as "the gap barely
moves"): this paper's Theorem 1 and convergence analysis depend on β being nonzero (β multiplies σ_D(x) in
the confidence bound that defines the local step); the paper does not analyze a β=0 case, so it offers no
direct evidence either for or against the audited paper's own beta=0 ablation finding.

## Grep evidence

- `trust region`: 3 hits (lines 52, 214, 218), all citations to prior work (TuRBO [7], MPD [23], and
  general "trust region methods" as a class) in the related-work/background sections — never used to
  describe MinUCB's own mechanism.
- `implicit`: 0 hits — the paper never uses the word "implicit" anywhere in the body.
- `variance`: multiple hits (Section 4, Theorem statements) — all in service of proving the confidence
  bound behaves locally because the GP posterior variance is bounded and grows with distance from sampled
  points.
- `local search` / `local strategy` / `trustworthy`: multiple hits — this is the paper's own preferred
  vocabulary for the phenomenon N4 calls an "implicit trust region."
- Full-text word count: 12,584 words (10-page NeurIPS paper + appendix/proofs).
