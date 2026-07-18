# 0A.2 — Ensemble width ablation (W1/W2)

**Verdict: W1 CONFIRMED — the gap does NOT close with width. The NTK/spectral-bias objection
(N5) is empirically answered.** W2 SUPPORTED, and by a stronger route than pre-registered: the
ensemble does not merely tie the GP on held-out accuracy, it **beats** it on 7/7 tasks while
still losing the optimization gap.

Pre-registered verbatim in `docs/PREREGISTRATION_V3.md` (commit `55ced44`) BEFORE launch.

**Engine:** X1=on, X3=on (audited/on_on), K=5 fixed, beta=2, 30 seeds (`0..29`), 7 synthetic
tasks, envs/pod-synth (torch 2.11.0+cpu, numpy 2.4.4, botorch 0.18.1, gpytorch 1.15.2,
cma 4.4.4). **Artifacts:** `results/width/width_grid.json` (210 cells x 18 = 3,780 fits,
engine-stamped), `results/width/width_analysis.json`. **Code:** `code/width_ablation.py`,
`code/analyze_v3.py`.

All gaps are on the **condition-invariant normalizer** of `docs/BETA0_RECONCILE.md`: one
per-task min–max fit ONCE over the pooled cell means of all four widths, so gap(w) values sit
on a single ruler. (Refitting per width — the incumbent `kbeta_analyze` behaviour — would make
the very cross-width comparison W1 asks for uninterpretable; that was the 0A.1 finding.) CIs
are task+seed hierarchical bootstrap, 10,000 resamples, normalizer refit inside each resample.

---

## Validity check: w=96 reproduces the incumbent grid

w=96 is the paper's incumbent `HID`, so its cells must match `results/kbeta/grid_b2.0.json`.

| optimizer | reproduction |
|---|---|
| grad | **bit-exact**, all 7 tasks (\|diff\| = 0.000) |
| cma | **bit-exact**, all 7 tasks (\|diff\| = 0.000) |
| perturb | within noise; median 0.0 SE, max 2.29 SE (Griewank-30D) |

The two deterministic optimizers reproduce exactly. `perturb_opt` draws from the global numpy
RNG without reseeding (`code/mbo.py:257-272`), so its stream position depends on how many draws
preceded it in the worker; this runner fits the GPs before the ensembles, so the position
differs. This is Monte-Carlo noise in the incumbent's own protocol, not a discrepancy in the
width arm. Reported rather than silently smoothed.

---

## W1 — the gap-vs-width curve

| w | GP–ens gap | 95% CI | ens held-out normRMSE |
|---|---|---|---|
| 96 (incumbent) | **0.480** | [0.365, 0.576] | 0.4446 |
| 256 | 0.336 | [0.132, 0.483] | 0.4047 |
| 512 | 0.414 | [0.187, 0.565] | 0.3934 |
| 1024 | **0.476** | [0.208, 0.647] | 0.3877 |

**Shrinkage w=1024 vs w=96: −0.006, 95% CI [−0.210, 0.161]** — indistinguishable from zero. The
gap at w=1024 is **99.1%** of its value at w=96.

- Monotonically non-increasing in w? **No.** The curve dips at w=256 and returns; it is flat
  with noise, not a decay.
- 95% CI on gap(w=1024) excludes zero? **Yes** ([0.208, 0.647]).

Both pre-registered KILL conditions therefore fail (KILL required monotone decrease AND
gap(1024) < 0.5 x gap(96) AND CI containing 0; none of the three holds), and the CONFIRMED
condition is met.

> **W1 CONFIRMED.** Sweeping ensemble member width across a 10.7x range — 96 to 1024, at fixed
> K=5 — leaves the GP–ensemble gap statistically unchanged. The "jagged ensemble mean" is not a
> finite-width artifact. The NTK/spectral-bias objection (Jacot et al. 2018; Lee et al. 2019;
> Rahaman et al. 2019) predicts a wider, better-trained net should approach a GP and close the
> gap; at practical widths it does not. C2's mean-quality claim stands as a **class property**,
> not a capacity artifact.

**Caveat, stated plainly.** The CI widens monotonically with w (width 0.211 at w=96 -> 0.439 at
w=1024): wider ensembles are more variable across tasks and seeds, so the w=1024 estimate is the
least precise point on the curve. The claim supported is "the gap does not close", which the CI
sustains. A claim that the gap is *identical* at w=1024 would not be supported at this precision.
The sweep also does not extend past 1024; NTK limits are asymptotic, so this answers the
objection *at practical widths*, which is the scope C2 needs and all it should assert.

---

## W2 — accuracy is not the bottleneck

Held-out normalized RMSE (RMSE / std of the oracle on a held-out 20% split never seen by the
grid; the grid itself is unchanged, fit on full data as in the incumbent protocol):

| task | w=96 | w=256 | w=512 | w=1024 | GP |
|---|---|---|---|---|---|
| Branin-2D | 0.083 | 0.066 | 0.064 | 0.069 | 0.118 |
| Styblinski-5D | 0.658 | 0.595 | 0.574 | 0.551 | 0.592 |
| Levy-8D | 0.634 | 0.635 | 0.636 | 0.636 | 0.674 |
| Rosenbrock-10D | 0.290 | 0.237 | 0.223 | 0.218 | 0.397 |
| Rastrigin-15D | 0.739 | 0.737 | 0.741 | 0.746 | 0.764 |
| Ackley-20D | 0.371 | 0.312 | 0.301 | 0.301 | 0.435 |
| Griewank-30D | 0.338 | 0.252 | 0.215 | 0.192 | 0.377 |
| **mean** | **0.4446** | **0.4047** | **0.3934** | **0.3877** | **0.4795** |

First clause of W2 holds: **held-out RMSE improves monotonically with w** (0.4446 -> 0.3877,
−12.8%). Second clause holds decisively:

- **Pre-registered test.** W2 was registered to be evaluated only where ensemble and GP RMSE are
  statistically indistinguishable. Two such cells exist (Styblinski-5D at w=256, CI [−0.021,
  0.028]; at w=512, CI [−0.043, 0.010]). Mean gap at those widths is **0.375** — the ensemble
  loses the optimization comparison by a wide margin exactly where its accuracy ties.
  **W2 SUPPORTED** on its registered terms.
- **Stronger, non-registered observation.** The tie condition turns out to be far too weak. The
  ensemble's best width beats the GP's held-out RMSE on **7/7 tasks**, and beats it in **26/28**
  (task, width) cells. Its mean normRMSE is lower than the GP's at *every* width tested
  (0.388–0.445 vs 0.479). So the ensemble is not merely as accurate as the GP off-distribution —
  it is **more** accurate — and still loses the optimization gap by ~0.48.

> **W2 SUPPORTED.** Predictive accuracy is not the bottleneck and cannot explain the gap: the
> more accurate surrogate is the one that loses. What separates them is the geometry of the mean
> under optimization pressure, not its error on held-out draws from D.

**Two caveats.** (i) The 7/7 result is a post-hoc strengthening, not the registered test; it is
reported as such and C2 should cite the registered tie-cell result as primary. (ii) Held-out NLL
is not usable as a second accuracy axis here: the GP's mean NLL is 202.7 against the ensemble's
5.7–6.4, driven by severe overconfidence on a subset of tasks. That is a calibration finding,
not an accuracy one, and it is orthogonal to W2 — noted so the NLL column in the artifact is not
mistaken for support.

---

## What this does to C2

C2's mean-quality claim is **strengthened and re-scoped**:

1. The N5 category error is corrected. The prior sweep varied K, which is ensemble *count*, not
   member capacity; it never tested the NTK objection. This does, at fixed K=5, over a 10.7x
   width range, and the objection does not survive.
2. C2 may now assert mean quality as a **class property at practical widths** rather than
   hedging it as possibly a capacity artifact. It may **not** assert anything asymptotic in w.
3. The mechanism is narrowed. Combined with W2, the GP's advantage is not better fit — the
   ensemble fits better — so C2 should stop describing it as "the GP models the function
   better" and describe it as what the evidence supports: the ensemble's mean, though more
   accurate on-distribution, admits off-distribution maximizers that the oracle scores poorly.
4. Reads directly with 0A.1: the beta=0 result says the advantage survives with sigma removed;
   this says it survives with width raised. The remaining live explanation is mean geometry
   under optimization, which is what C2 claims.
