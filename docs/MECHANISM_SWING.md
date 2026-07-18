# C2-SWING — bidirectional smoothness manipulation: verdicts and binary call

Branch `c2-swing`. Pre-registered in `docs/PREREGISTRATION_V3.md` (section "C2-SWING"),
committed **before** launch (`52af907`). Engine X1=on X3=on, beta=2, K=5, seeds `0..29`,
7 synthetic tasks, envs/pod-synth, 19-field engine stamp. 210/210 shards complete, 45/45
cells each, zero failures (`logs/swing_run.log`, `EXIT=0`, 9,729 s wall on 30 workers).
Artifacts: `results/swing/shards/*.json`, `results/swing/swing_grid.json`,
`results/swing/swing_analysis.json`.

---

## BINARY CALL: **SHIP-PURE-D**

| arm | verdict | one-line |
|---|---|---|
| **SM1** (smooth the net) | **KILL** | The manipulation landed hard (roughness −98%) and the gap did **not** close — it widened for every variant. |
| **SM2** (roughen the GP) | **VOID** | Not deliverable: no kernel setting raised the GP mean's roughness by the registered 25%. |
| **SM3** (survives NTK) | **UNTESTABLE** | No SM1 winner to carry to w=1024; reported as untestable, not fabricated. |

Per the pre-registered rule, FOLD required all three CONFIRMED. One KILL alone forces
SHIP-PURE-D. **The paper ships as pure Identity D and this branch touches nothing in the
draft.** C2 remains DIAGNOSTIC — no causal upgrade.

The analyzer is not rigged toward this outcome: `code/swing_selftest.py` plants three
synthetic ground truths and confirms the same code emits **FOLD** when smoothing genuinely
closes the gap and roughening genuinely hurts the GP.

---

## SM1 — KILL (the informative one)

The manipulation **landed decisively**. Pooled on-D roughness (`E||d mu/d x|| / std(f)`)
fell against the base ensemble by:

| variant | roughness reduction w=96 | w=1024 |
|---|---|---|
| grad-pen 0.01 | 41.4% | 45.6% |
| grad-pen 0.1 | 84.6% | 85.8% |
| grad-pen 1.0 | **98.0%** | **98.2%** |
| spectral norm | 90.3% | 91.8% |

The outcome did not follow. On the pooled beta-invariant normalizer, base gap = **0.3057**;
every smoothing variant left it **wider**, and no closing CI (Bonferroni 98.75%) excludes 0:

| variant | gap | shrinkage | closing diff, CI98.75 |
|---|---|---|---|
| base | 0.3057 | — | — |
| grad-pen 0.01 | 0.3219 | −5.3% | −0.0161 [−0.113, +0.074] |
| grad-pen 0.1 | 0.3457 | −13.1% | −0.0405 [−0.239, +0.082] |
| grad-pen 1.0 | 0.3415 | −11.7% | −0.0361 [−0.280, +0.157] |
| spectral norm | 0.5517 | −80.5% | −0.2432 [−0.532, +0.046] |

This is a **clean kill, not an underpowered null**: the intervention moved its target by two
orders of magnitude in the intended direction and the effect went the *wrong way*.
Making the ensemble's mean smoother does not transfer the GP's advantage; a
Lipschitz-bounded ensemble is markedly *worse* (normalized score 0.657 → 0.537 at w=96,
→ 0.346 at w=1024, where the constraint bites hardest).

**Two unregistered observations that sharpen the kill.** Reported as observations, not
claims — neither was pre-registered.

1. **Smoothing fixes the premise and not the outcome.** Own-proposal premise coverage
   `c_ood` rises monotonically with smoothing — 0.654 (base) → 0.742 → 0.937 → **0.998**
   (grad-pen 1.0) — i.e. the LCB lower-bound premise can be driven to essentially 100%
   while the optimization gap is untouched. Coverage was C2's proposed mechanism proxy;
   it is separable from the outcome it was supposed to explain. This corroborates the weak
   ρ(coverage, score)=0.19 from `results/coverage33.json` on a fresh axis, and the same
   dissociation appears *between* surrogates: `svgp` has the worst coverage of any GP
   (0.575) and the best score (0.881).
2. **Smoothing makes gradient collapse worse, not better.** SM1's second clause ("stops
   gradient collapse") fails in the opposite direction: the grad-optimizer inversion rate
   *rises* with smoothing, 0.548 → 0.695 (w=96) and 0.676 → 0.733 (w=1024). A flatter mean
   gives gradient ascent less to climb, so the returned set more often fails to beat the
   x0 already in hand. (Formally SM1b is UNTESTABLE — it is defined on an SM1 winner and
   there is none — so this is descriptive.)

---

## SM2 — VOID (not deliverable)

Registered VOID rule: SM2 requires some roughened kernel to raise on-D **or** between-data
roughness by ≥25% (the permissive reading, so VOID cannot be an artifact of the less
sensitive probe). Best observed rise across all variants and both instruments: **+12.6%**.

| variant | roughness rise (on-D) | (between-data) |
|---|---|---|
| `botorchgp_m12L` (ν=0.5, L frozen) | −13.0% | +2.7% |
| `botorchgp_lsL3` (RBF, L/3 frozen) | −33.0% | +12.6% |
| `svgp_m12` (ν=0.5) | −18.5% | −11.8% |

This confirms at 30 seeds what pre-launch calibration predicted on disjoint seeds 100/101,
and it is a **methodological finding, not evidence about C2 in either direction**:

> A GP posterior mean conditioned on ~800 observations is smooth **because of the
> conditioning, not because of the kernel.** Roughness and fit quality are therefore not
> independently manipulable in a fitted GP. Every setting that added short-scale structure
> did so by degrading the mean toward the prior — degeneracy, not roughness.

Two traps this arm had to survive, both documented in the pre-registration and both of
which would have produced a *false* SM2 verdict:

1. **The MLL fit silently reverses the manipulation.** Setting ν=0.5 with hyperparameters
   free lets the marginal likelihood compensate by inflating the lengthscale (Branin
   0.40 → 15.93, Ackley 1.51 → 9.49), returning an effectively *smoother* mean. The naive
   version would have read as a clean "rough GP stays robust" KILL while never having
   roughened anything. Fixed by freezing the lengthscale at the smooth fit's `L`.
2. **An absolute short lengthscale is degenerate in high d.** At `ls=0.05` the Ackley-20D
   posterior mean reverts to the prior between points — measured gradient exactly 0.000.
   That is flat, not rough. Fixed by shortening relatively (`L/3`).

Descriptively, the roughened GPs did trend worse on score (−0.07, −0.20, −0.07 normalized)
but no CI excludes zero and 0/3 showed the registered both-axes (score **and** coverage)
drop. **SM2b:** every roughened GP still beats every ensemble variant (0.827–0.868 vs
0.346–0.666), so nothing resembling "collapse" occurred.

**Incidental correction.** BoTorch 0.18's `SingleTaskGP` default `covar_module` is
**RBFKernel**, not Matérn-5/2. Repo comments describing the incumbent GP as Matérn-5/2 are
wrong; `paper/` makes no kernel claim, so nothing published is affected. RBF is infinitely
differentiable, so the incumbent "smooth GP" is maximally smooth.

---

## SM3 — UNTESTABLE

SM3 is defined on the SM1 winner. SM1 produced none, so per the registered rule SM3 is
reported UNTESTABLE rather than evaluated on a post-hoc substitute. For the record, at
w=1024 the gradient-penalty variants show *positive* point shrinkage (+12.5%, +21.1%,
+9.6%) unlike w=96, but every CI98.75 includes 0 and spectral norm remains catastrophic
(−91.5%). Nothing here supports a width-dependent mechanism; it is noise around a null.

The declared post-hoc pairwise-normalizer robustness check is likewise UNTESTABLE (it is
defined on the winner). Note that the pooled-normalizer concern it was written to catch
cannot have manufactured this result: the concern was *false shrinkage*, and no variant
shrank.

---

## What this does to C2

C2's mean-geometry account now has a **failed causal test to report**. The chain of
eliminations is:

- 0A.1 — the GP advantage survives removing sigma (61% present at beta=0).
- 0A.2 — it survives 10.7× more ensemble width (W1), and the *more accurate* surrogate is
  the one that loses (W2).
- 0A.3 — it survives budget matching (η²_opt 0.038).
- **C2-SWING — it is not mean smoothness.** Smoothing the ensemble's mean by up to 98%
  does not close the gap; it widens it, drives premise coverage to ~1.0 without effect, and
  increases gradient inversion.

The honest statement is now **narrower** than before this arm: the ensemble's disadvantage
is not explained by sigma, width, budget, held-out accuracy, mean gradient magnitude, or
premise coverage. "Mean geometry under optimization" survives only in a weaker,
non-smoothness sense (*which* off-distribution maximizers the mean admits, not how rough it
is), and C2 must be written as diagnostic. Any draft language attributing the GP's
advantage to a "smoother" or "less jagged" mean should be struck — this arm tested that
reading directly and it failed.

**Merge status.** Per the bet's terms this branch does **not** merge to `main`. It stays on
`origin/c2-swing`. Its engine additions are default-off and verified bit-identical on the
incumbent path, so nothing in the Stage-0 corpus is disturbed.
