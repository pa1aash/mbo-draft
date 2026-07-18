## Citation

Srinivas, N., Krause, A., Kakade, S. M., & Seeger, M. (2010). "Gaussian Process Optimization in the Bandit Setting: No Regret and Experimental Design." *Proceedings of the 27th International Conference on Machine Learning (ICML 2010)*. arXiv:0912.3995v4 [cs.LG], revised 9 Jun 2010. Source PDF: `research/raw/pdf/0912.3995.pdf`, extracted text: `research/raw/txt/srinivas-gp-ucb.txt`.

## What the paper does

The paper formalizes GP optimization (Bayesian optimization) as a multi-armed bandit problem where the payoff function `f` is either sampled from a Gaussian process (GP) or has bounded RKHS norm, and derives the first sublinear cumulative-regret bounds for this nonparametric setting. It analyzes the GP-UCB (Gaussian Process Upper Confidence Bound) algorithm, which at each round `t` selects `x_t = argmax_x μ_{t-1}(x) + β_t^{1/2} σ_{t-1}(x)`, where `μ_{t-1}` and `σ_{t-1}` are the posterior mean and standard deviation of a single GP surrogate conditioned on the first `t-1` observations. The central technical contribution is a family of confidence-interval-width schedules `β_t` (Theorem 1 for finite decision sets, Theorem 2 for continuous compact decision sets with a smoothness condition on the kernel, Theorem 3 for the agnostic RKHS case) that are proved, via a union bound over `t` and a Gaussian tail bound, to keep `|f(x) − μ_{t-1}(x)| ≤ β_t^{1/2} σ_{t-1}(x)` simultaneously for all `x` and all `t` with probability at least `1 − δ`. It then connects cumulative regret `R_T` to the maximum information gain `γ_T` of the kernel, giving regret bounds of the form `R_T = O*(√(T β_T γ_T))`, and bounds `γ_T` explicitly for the Linear, Squared-Exponential, and Matérn kernel families. Experimentally, GP-UCB (with `β_t` from Theorem 1, empirically scaled down by a factor of 5 via cross-validation) is compared against Expected Improvement (EI), Most Probable Improvement (MPI), and greedy mean/variance heuristics — all of these comparator methods operate on the *same* GP posterior (`μ_{t-1}`, `σ_{t-1}`) on synthetic squared-exponential-kernel data and real Intel Berkeley sensor-network temperature data; no comparison across structurally different surrogate model classes is performed.

## Claim relevance — N3

**Verdict: The paper does NOT touch N3. It owns only a single-surrogate, over-time β schedule; N3's claim is about a shared β applied across structurally different surrogate classes with different intrinsic σ magnitudes — a scenario this paper never discusses or gestures at.**

The paper's `β_t` is a scalar sequence indexed purely by *round number t* (and, depending on the theorem, by `δ`, `|D|`, dimension `d`, kernel-smoothness constants `a, b, r`, or the information-gain/RKHS-norm bound `B, γ_t`), applied to **one single GP surrogate** whose posterior evolves as more data arrive. It is never applied to, or discussed in the context of, two or more *different* surrogate model classes (e.g., a GP vs. a deep ensemble vs. an SNGP) with different intrinsic uncertainty scales being compared under one nominal `β`.

Exact `β_t` definitions extracted verbatim from the theorems/lemma:

- Theorem 1 (finite `D`): `β_t = 2 log(|D|t²π²/6δ)`. (Lemma 5.1 gives the closely related general form: `β_t = 2 log(|D|π_t/δ)`, with `Σ_{t≥1} π_t^{-1} = 1, π_t > 0`.)
- Theorem 2 (continuous compact `D`, derivative tail-bound constants `a, b, r`): `β_t = 2 log(t²2π²/(3δ)) + 2d log(t²dbr log(4da/δ))`.
- Theorem 3 (agnostic RKHS case, `‖f‖²_k ≤ B`): `β_t = 2B + 300γ_t log³(t/δ)`.

In every case the arguments are `t` (round index), `δ` (confidence parameter), and quantities intrinsic to the *decision space / kernel* (`|D|`, `d`, `a, b, r`, `γ_t`, `B`) — never a surrogate-class identity or a surrogate-specific σ-scale calibration term. This is confirmed by grep: 0 hits for "surrogate," "ensemble," "different models," or "calibrat" anywhere in the 6-page paper.

The single most load-bearing sentence defining what `β_t` is calibrated to guarantee (Lemma 5.1, the proof engine behind Theorems 1–3):

> "Lemma 5.1 Pick δ ∈ (0, 1) and set βt = 2 log(|D|πt/δ), where Σ(t≥1) πt−1 = 1, πt > 0. Then, |f(x) − µt−1(x)| ≤ βt^(1/2) σt−1(x) holds with probability ≥ 1 − δ. ∀x ∈ D ∀t ≥ 1"

and the resulting regret-bound statement (Theorem 1):

> "Pr {RT ≤ C1 √(T βT γT) ∀T ≥ 1} ≥ 1 − δ. where C1 = 8/ log(1 + σ⁻²)."

Both quotes make explicit that `β_t` is calibrated against a *single* posterior `(μ_{t-1}, σ_{t-1})` produced by one GP over a growing dataset, to guarantee (a) a uniform-in-t confidence-interval-coverage property and (b) a cumulative-regret bound for the algorithm run on that one surrogate. Nothing in the derivation, the discussion of "Choice of βt" (Section 6, where the authors note "the choice of βt as recommended by Theorem 1 leads to competitive performance of GP-UCB, we find (using cross-validation) that the algorithm is improved by scaling βt down by a factor 5"), or the experiments section addresses what happens when the *same nominal* `β` is applied to two surrogates whose `σ` outputs live on different scales (e.g., a poorly calibrated ensemble vs. a well-calibrated GP). All experimental comparisons (GP-UCB vs. EI vs. MPI vs. max-mean vs. max-variance) hold the surrogate (a single GP posterior) fixed and vary only the acquisition rule built on top of it — the opposite axis of variation from N3's claim.

What it stops short of: the paper never poses, models, or empirically tests the scenario of two structurally different uncertainty estimators (e.g., GP vs. neural-network ensemble) being compared or combined under one shared nominal `β`; it has no notion of "effective conservatism" varying by surrogate class, and no cross-model calibration analysis. N3's claim — that a shared nominal `β` across surrogate classes with different intrinsic σ magnitudes produces different *effective* conservatism, undermining acquisition-function comparisons across surrogate classes — is a distinct, unaddressed problem from this paper's single-surrogate, time-indexed `β_t` schedule.

## Grep evidence (against `research/raw/txt/srinivas-gp-ucb.txt`, 13,433 words, 6 pages)

Literal ASCII-keyword grep counts as specified in the task (note: the PDF-extracted text renders the beta symbol as Unicode "β" with no underscore, e.g. "βt", not ASCII "beta_t"; similarly δ renders as Unicode, not ASCII "delta"):

| keyword | hits |
|---|---|
| `beta_t` (literal ASCII) | 0 (paper uses Unicode "βt"; see note below) |
| `\beta_t` (literal ASCII) | 0 |
| `confidence` | 15 |
| `scale` | 3 (all refer to kernel "lengthscale," not surrogate-uncertainty scale) |
| `different models` | 0 |
| `surrogate` | 0 |
| `compare`/`compar-` | 8 lines (all comparing GP-UCB to other *acquisition rules* on the *same* GP posterior — EI, MPI, max-mean, max-variance — never comparing surrogate *model classes*) |
| `ensemble` | 0 |
| `GP-UCB` | 32 |
| `regret bound` | 26 |
| `delta` (literal ASCII) | 0 (paper uses Unicode "δ", 77 occurrences) |
| `calibrat` | 0 |

Supplementary greps run to resolve the Unicode-symbol issue: `β` (Unicode) = 113 hits, `δ` (Unicode) = 77 hits — confirming `β_t`/`δ` are used extensively but exclusively in the single-GP, time-indexed sense (see the βt formulas in Theorems 1–3 and Lemma 5.1 above).
