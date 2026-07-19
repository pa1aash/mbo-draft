# 0B — Positive mechanism for C2: the attempt, and why it failed

Pre-registered in `docs/PREREGISTRATION_V3.md` §0B, committed **before launch** at `e1e185d`.
Run: `code/phantom_maxima.py`, X1=on X3=on, beta=2, K=5, 30 seeds, 7 synthetic tasks, 8
surrogate arms x 3 optimizers = **168 cells, 0 missing, 0 ragged**. Artifacts:
`results/mechanism/phantom_maxima.json` (per-seed, 3.6 MB) and
`results/mechanism/phantom_analysis.json` (verdicts). Engine stamp: 19 fields, `git_sha`
`d88d8b7`, `envs/pod-synth` (torch 2.11.0+cpu, botorch 0.18.1, gpytorch 1.15.2, cma 4.4.4).

**Validity.** The incumbent `ens`, `botorchgp` and `svgp` cells reproduce
`results/kbeta/grid_b2.0.json` **bit-exactly** at seed 0, including `perturb`. The instrumented
runner is the same engine, not a re-implementation of it.

---

## THE CALL: **KEEP-ELIMINATION**

PM1 KILL fires. PM2 is UNINFORMATIVE. Under the pre-registered rule — UPGRADE requires PM1 and
PM2 to *both* hold — C2 ships unchanged as an elimination result. This arm is reported as a
**failed upgrade attempt with its measurements intact**, and it adds one further elimination
rather than a mechanism.

| | verdict |
|---|---|
| **PM1** | **KILL FIRES** — the ensemble's returned optima do not sit further off-support than the GP's, and are not more inflated |
| **PM2** | **UNINFORMATIVE** — the prior-mean knob does not move the quantity it was built to move (R = 0.009 against a 0.25 threshold) |
| **PM3** | **DELIVERED** — 168/168 cells, per-seed, with the landscape characterization below |

---

## PM1 — KILL FIRES

Paired at (task, seed, optimizer), ensemble minus incumbent `botorchgp`, task+seed
hierarchical bootstrap, 10,000 resamples. Distance `Dhat` is the returned optimum's 10-NN
distance to the full offline D, divided by the median within-D 10-NN distance, so 2-D pools
with 30-D. Inflation `I` is (surrogate mean − true oracle) / sd(y_D).

| statistic | ensemble | GP | difference | 95% CI | |
|---|---|---|---|---|---|
| distance `Dhat` at x* | 0.987 | 0.871 | **+0.116** | [−0.004, +0.333] | covers 0 |
| inflation `I` at x* | −0.459 | −0.502 | **+0.043** | [−0.652, +1.085] | covers 0 |

Both pre-registered limbs cover zero, so the KILL branch fires exactly as written. It is not a
near miss on one limb: the inflation interval is two orders of magnitude wider than its point
estimate.

**The distance limb is one task, not a trend.** Per-task differences: Branin-2D **+0.743**,
Styblinski-5D +0.060, Levy-8D +0.006, Rosenbrock-10D −0.022, Rastrigin-15D −0.009,
Ackley-20D −0.005, Griewank-30D +0.039. Six of seven tasks are at zero to three decimal
places. The pooled +0.116 is Branin alone. Inflation has no consistent sign either
(Ackley +2.94, Levy −0.86, Griewank −0.79).

**Robustness.** Reading x* as the argmax of the LCB the pipeline actually ascends rather than
the argmax of the mean: distance +0.102 [−0.006, +0.295], inflation +0.038 [−0.665, +1.099] —
same verdict. Pooling `{botorchgp, svgp}` as the GP family: +0.131 [−0.001, +0.349] and
+0.118 [−0.620, +1.213] — same verdict.

### What is true instead, and it is worth more than the prediction was

The gap itself reproduces: the ensemble's returned optima are genuinely **worse in true
oracle value** — −1.406 [−2.803, −0.375] in sd(y_D) units, CI excluding zero, ensemble 2.671
against GP 4.077. So the ensemble does lose, and it loses at the point PM1 measured. It just
does not lose *by being further out* or *by over-predicting more*.

Binning both arms on their pooled distance-to-D, the ensemble is worse in **4 of 5 bins** and
tied in the fifth, and is **not** the more inflated arm in the two nearest bins:

| distance bin | n ens/GP | Z ens | Z GP | ΔZ | I ens | I GP |
|---|---|---|---|---|---|---|
| [0.70, 0.80] | 113 / 139 | 5.31 | 6.53 | **−1.22** | −2.03 | −1.04 |
| [0.80, 0.85] | 143 / 109 | 3.62 | 7.46 | **−3.84** | −0.88 | −2.79 |
| [0.85, 0.90] | 114 / 138 | 2.22 | 3.30 | **−1.08** | −0.09 | +0.24 |
| [0.90, 0.95] | 109 / 143 | 1.84 | 1.82 | +0.01 | +0.10 | +0.53 |
| [0.95, 2.13] | 151 / 101 | 0.75 | 1.31 | **−0.56** | +0.44 | +0.24 |

**The ensemble loses at matched distance-to-data and matched inflation.** That is a seventh
elimination, and a sharper one than the six before it: distance-to-support and surrogate
over-prediction are now *measured* non-explanations, not unexamined ones.

---

## PM2 — UNINFORMATIVE

The manipulation check MC-1 was registered as: the arm's far-field posterior mean must travel
at least a quarter of the way from the incumbent's level to its own prior constant
(`R >= 0.25`, CI excluding 0.25). Far field = mean posterior mean over 512 uniform points in
the cube, in sd(y_D) units.

| arm | prior constant | lengthscale | R | 95% CI | MC-1 | held-out normRMSE vs incumbent |
|---|---|---|---|---|---|---|
| `botorchgp` | fitted | fitted | — | — | reference | 1.00x |
| `gpm_max` | z_max, frozen, kernel refit | refit | 0.045 | [0.022, 0.071] | **fails** | 4.22x |
| `gpm_sup` | z_max+20, frozen, kernel refit | refit | **0.009** | [0.006, 0.013] | **fails** | 4.91x |
| `gpm_ph` | z_max+20, post hoc | incumbent | 0.012 | [0.007, 0.018] | **fails** | 3.72x |
| `gpm_ls` | fitted | 0.1x fitted | undefined | — | control | 104.75x |
| `gpm_lssup` | z_max+20, post hoc | 0.1x fitted | 0.859 | [0.581, 0.999] | passes | **210.95x** |

**The briefed manipulation is not available at this operating point.** Raising the GP's prior
mean by 20 standardized units — strictly above every observation — moves its far-field
posterior mean from +0.067 to +0.319, about 1% of the distance to the constant. The reason is
that the fitted lengthscales are on the order of the domain diameter, so **there is no point
inside the feasible cube where this GP is in a prior-reversion regime**. The prior-mean
constant is very nearly unidentifiable here. PM2's premise does not hold; it is not that the
prediction was tested and survived.

**MC-1 was not the wrong statistic.** The obvious objection is that MC-1 averages over the
cube while an optimizer hunts the maximum, so the manipulation might have moved the tail
without moving the mean. It did not: reading the same fraction on the far-field **maximum**
gives R_max = 0.037 for `gpm_ph`, −0.734 for `gpm_max` and −0.064 for `gpm_sup`. `gpm_sup`'s
far-field maximum falls, from +2.298 to +0.770.

**The one arm that does remove reversion destroys the surrogate.** `gpm_lssup` passes MC-1
convincingly (R = 0.859, far field +23.09 against a constant of +26.04) and its gap over the
ensemble does shrink, +0.274 [+0.136, +0.428] — the direction PM2 predicted. It is reported as
**CONFOUNDED** under the registered rule, because its held-out normRMSE is **211x** the
incumbent GP's. Its gap against the ensemble is −0.164 [−0.276, −0.065]: it does not merely
lose its advantage, it ends up worse than the ensemble. A surrogate that has stopped predicting
is not evidence about reversion.

**Why the arms' optima moved anyway.** `gpm_sup`'s returned optima do sit further off-support
(median `Dhat` 1.56 against the incumbent's 0.86) with inflation +4.49. That is not reversion:
freezing the constant and refitting the kernel drives the MLL to much longer lengthscales, and
the optimizer wanders because the surrogate became a flatter, worse-fitting function — the
4.91x held-out degradation. The registered MC-1 / CONFOUNDED machinery separates these two
routes, which is what it was for.

**Ruler sensitivity, disclosed.** The registered normalizer pools all eight arms per task. An
arm whose scores collapse stretches that range and compresses every other arm's gap toward
zero, which would *flatter* a shrinkage claim. Each shrinkage is therefore also reported on a
per-comparison ruler pooling only `{ens, botorchgp, X}`; every pairwise-ruler shrinkage is
larger, not smaller. No verdict turns on the choice, because every arm fails MC-1 or the
held-out check first. Note that the incumbent gap on the 8-arm ruler is +0.110 [+0.047,
+0.181], not the 0.48 of `docs/WIDTH_ABLATION.md` — same data, wider ruler. The two are not
comparable and neither is quoted for the other's purpose.

---

## PM3 — DELIVERED

168/168 cells present, per-seed, no imputation. `results/mechanism/phantom_maxima.json` carries
for every (task, arm, optimizer) the per-seed `Dhat`, `Z` and `I` at x*, the same at the LCB
argmax, and the same summarized over all 128 returned designs.

The landscape law is real, and it is what makes PM1's null informative rather than empty.
Pooled over 5,040 returned optima, distance-to-support predicts both over-prediction and true
loss, strongly and monotonically:

- Spearman(`Dhat`, `Z`) = **−0.818** — further out is worth less.
- Spearman(`Dhat`, `I`) = **+0.758** — further out is over-predicted more.

The ensemble's own deciles show it cleanly: from decile 1 to decile 10, `Dhat` 0.75 → 2.05,
`Z` +5.28 → +0.85, `I` −1.99 → +0.28.

| arm | `Dhat` p10/p50/p90 | `Z` mean | `I` mean | ρ(`Dhat`,`Z`) |
|---|---|---|---|---|
| `ens` | 0.79 / 0.87 / 1.37 | 2.67 | −0.46 | −0.834 |
| `botorchgp` | 0.78 / 0.86 / 0.97 | 4.08 | −0.50 | −0.758 |
| `svgp` | 0.73 / 0.84 / 0.93 | 3.98 | −0.65 | −0.092 |
| `gpm_max` | 0.85 / 0.98 / 1.25 | 0.25 | +2.14 | −0.874 |
| `gpm_sup` | 1.03 / 1.56 / 1.89 | −3.50 | +4.49 | −0.552 |
| `gpm_lssup` | 1.05 / 1.28 / 1.77 | −2.39 | +27.32 | −0.275 |

So "off-support maxima are inflated and worthless" is a **confirmed property of the landscape**
— it is simply not a property that separates the ensemble from the GP. The two incumbent arms
sit at the same place on the law (median `Dhat` 0.87 against 0.86) and differ in outcome
anyway. The manipulated arms are the ones that move along it, and they move because they were
damaged.

---

## What this changes

Nothing in the paper's claims, by design. C2 remains the elimination result at
`paper/aaai27/main.tex:180`, and the surviving sentence — *what differs is which
off-distribution maximizers a surrogate's mean admits, not how rough it is* — stands as written.

Three things are now available that were not:

1. **A seventh elimination**, stronger than the six: not distance-to-data, not surrogate
   inflation. Both were the natural next reader's hypothesis and both are now measured nulls
   with intervals, at matched distance.
2. **A measured landscape**, so "off-distribution maximizers" is no longer an assertion. The
   distance→inflation→loss law is quantified (ρ = +0.758 and −0.818 over 5,040 optima).
3. **A negative structural fact about the GP** worth stating in its own right: at this
   operating point the exact GP is nowhere in a prior-reversion regime inside the feasible set,
   so any account of its advantage that leans on reversion to the data mean is unavailable —
   not merely untested. This closes a mechanism the paper might otherwise have been tempted to
   assert.

The honest limitation is that this arm was designed to *find* a mechanism and did not. The
surviving statement is still a diagnosis with seven eliminations behind it and no positive
causal test in front of it, and `main.tex:232`'s limitation paragraph remains accurate. It
should gain the sentence that the one positive account we pre-registered and tested — off-support
phantom maxima under prior reversion — was refuted on its first limb and untestable on its
second.

**Merge recommendation: do not fold into `main` as a claim change.** The branch carries the
pre-registration, the runner, the analyzer and the artifacts; the paper edit it licenses is an
addition to the eliminations list and the limitations paragraph, not a rewrite of C2.
