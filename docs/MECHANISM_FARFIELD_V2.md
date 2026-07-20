# 0D — Far-field functional form, instrumented (FF1/FF2/FF3)

**BINARY: KEEP-ELIMINATION.** FF1 fired its pre-registered KILL condition. Section 5 ships as
seven eliminations; the linear-extrapolation mechanism is **refuted as a discriminator between
the surrogate classes**, not merely untested.

Pre-registered verbatim in `docs/PREREGISTRATION_V3.md` §0D, commit `8bf1140`, BEFORE the run.
One attempt, as registered. The diagnostic was not re-specified after seeing the numbers.

| | verdict |
|---|---|
| **FF1** far-field linearity separates the classes | **KILL** — it does not. Both classes extrapolate near-linearly; neither GP reverts anywhere in the probed range. |
| **FF2** ensemble optima sit closer to the box boundary | **CONFIRMED** — 6/7 tasks, effect grows with dimension. |
| **FF3** ensemble already linear at the training boundary (NTK premise) | **DISCHARGED** — median R2 0.947–0.995 across all 7 tasks. |

The headline is a genuine split: **the phenomenon FF2 predicted is real and large, but FF1
removes the explanation that was proposed for it.** Boundary-seeking is differential; "because
the ensemble alone extrapolates linearly while the GP reverts" is false. A confirmed FF2 with a
killed FF1 is a described phenomenon without a mechanism, which is exactly what the
pre-registered binary refuses to promote.

---

## Engine stamp (19 fields, `run_all.REQUIRED_META`)

| field | value | | field | value |
|---|---|---|---|---|
| platform | Linux-6.17.0-35-generic-x86_64-with-glibc2.39 | | X1 / X3 | true / true |
| os_release | 6.17.0-35-generic | | K / beta | 5 / 2.0 |
| python | 3.12.3 | | TOP | 128 |
| torch | 2.11.0+cpu | | OPT_STEPS | 100 |
| numpy | 2.4.4 | | LR_OPT | 0.05 |
| botorch | 0.18.1 | | n_seeds / seed | 30 / `0..29` |
| gpytorch | 1.15.2 | | git_sha | `8bf1140aced7e24480aaf40a75769b5f59b3bcfc` |
| cma | 4.4.4 | | timestamp | 2026-07-20T15:12:47 |

**Env:** `envs/pod-synth`. **Tasks:** the 7 synthetic tasks. **Runtime:** 14.4 min, 30 workers.
**Code:** `code/farfield_v2.py` (runner), `code/farfield_selftest.py` (reproduction check),
`code/analyze_farfield_v2.py` (verdicts). **Artifacts:** `results/mechanism/farfield_v2/` —
`rays_<task>.json` (7 files, ~0.9 MB each: 30 seeds x 3 classes x 16 rays x 61 radii of stored
mu), `grid_ff2.json`, `farfield_analysis.json`, `selftest_repro.json`.

---

## Validity: the incumbent engine is untouched and still reproduces the published grid

`code/mbo.py` was **not modified**; all instrumentation lives in the new `code/farfield_v2.py`,
which imports `mbo` read-only. The instrumentation is therefore default-OFF for every existing
caller by construction. Both pre-registered checks pass:

1. **Static.** `git diff main -- code/mbo.py` is empty.
2. **Empirical.** `code/farfield_selftest.py` re-runs the published grid through
   `run_all._worker` — the same function that WROTE `grid_b2.0.json` — at beta=2, 30 seeds,
   7 tasks, and compares every cell:

| optimizer | reproduction of `results/kbeta/grid_b2.0.json` |
|---|---|
| grad | **BIT-EXACT**, 630/630 cells, max\|diff\| 0.000e+00 |
| perturb | **BIT-EXACT**, 630/630 cells, max\|diff\| 0.000e+00 |
| cma | **BIT-EXACT**, 630/630 cells, max\|diff\| 0.000e+00 |

Additionally the *instrumented* runner's own grid pass reproduces the published grid bit-exactly
on all 1,890 cells for all three optimizers, because it replicates `run_offline`'s per-cell
seeding (`code/mbo.py:528-538`) exactly.

This is **stronger than the precedent it was held to.** `docs/WIDTH_ABLATION.md` could only
achieve bit-exactness for grad and cma, with perturb "within noise", because that runner fit the
GPs before the ensembles in one worker and `perturb_opt` draws from the global numpy RNG without
reseeding (`code/mbo.py:257-272`). 0D re-seeds per cell exactly as `run_offline` does, so the
perturb stream position matches too. The pre-registered standard allowed perturb to differ within
noise; it did not need the allowance.

---

## FF1 — KILL. Far-field linearity does not distinguish the classes

Least-squares fit of `mu ~ a + b*s` on the FAR segment `s in [1.5, 3.0]`, where `s=1` is exactly
the box face and the training support is the box (data is `uniform(0,1)^d`). Medians over
16 rays x 30 seeds = 480 curves per (task, class). Slope in sd_y per unit s.

| task | ens R2 | ens \|slope\| | ens label | botorchgp R2 | gp \|slope\| | gp label | svgp R2 | svgp \|slope\| | svgp label |
|---|---|---|---|---|---|---|---|---|---|
| Branin-2D | 0.9990 | 1.676 | LINEAR-GROWING | 0.7901 | 1.260 | OTHER | 0.8993 | 0.397 | OTHER |
| Styblinski-5D | 0.9999 | 6.430 | LINEAR-GROWING | 0.8118 | 0.423 | OTHER | 0.9385 | 1.026 | LINEAR-GROWING |
| Levy-8D | 0.9998 | 3.873 | LINEAR-GROWING | 0.9905 | 2.634 | LINEAR-GROWING | 0.9502 | 1.341 | LINEAR-GROWING |
| Rosenbrock-10D | 0.9981 | 2.706 | LINEAR-GROWING | 0.9946 | 2.612 | LINEAR-GROWING | 0.9807 | 1.659 | LINEAR-GROWING |
| Rastrigin-15D | 0.9983 | 3.170 | LINEAR-GROWING | 0.9931 | 2.879 | LINEAR-GROWING | 0.9544 | 1.541 | LINEAR-GROWING |
| Ackley-20D | 0.9989 | 4.592 | LINEAR-GROWING | 0.9930 | 4.447 | LINEAR-GROWING | 0.9227 | 1.865 | LINEAR-GROWING |
| Griewank-30D | 0.9809 | 4.118 | LINEAR-GROWING | 0.9965 | 5.934 | LINEAR-GROWING | 0.9685 | 1.779 | LINEAR-GROWING |

- `ens` LINEAR-GROWING on **7/7** — Xu et al. Thm 1 is confirmed for the ensemble, cleanly
  (median R2 >= 0.98 on every task).
- `botorchgp` REVERTING on **0/7**, LINEAR-GROWING on **5/7**.
- `svgp` REVERTING on **0/7**, LINEAR-GROWING on **6/7**.

The pre-registered KILL condition — "either GP class is LINEAR-GROWING on a majority" — fires
on both GP classes. **FF1 = KILL.**

**The reversion premise is not merely weak, it is absent.** `frac_constant`, the share of ray
curves whose far-field range fell below 0.01 sd_y (the DEGENERATE-CONSTANT convention registered
precisely to catch reversion), is **0.000 for every class on every task** — 0 of 3,360 GP curves
had reverted anywhere in `s in [1.5, 3.0]`, i.e. out to three times the box exit radius. Where
the GP slope is smaller than the ensemble's (Branin, Styblinski) it is smaller by a factor of
~1.3–15, not by reversion to zero; and on Griewank-30D the GP's far-field slope is **steeper**
than the ensemble's (5.934 vs 4.118).

**Why the DEGENERATE-CONSTANT convention mattered.** A reverted mean is perfectly fit by a
zero-slope line, so its R2 is `0/0`. Had R2 been the sole statistic, a reverting GP and a
linearly-growing ensemble could both have scored "high R2" and FF1 would have been unreadable.
Registering the slope as a co-primary is what makes this verdict decidable — and, as it turns
out, what shows the GPs are growing rather than flat.

---

## FF2 — CONFIRMED. Ensemble optima do sit closer to the box boundary

`d_bnd(x*) = min_i min(x*_i, 1 - x*_i)`, where x* is the proposal maximizing the surrogate MEAN
(the definition 0B registered). Median over 30 seeds x 3 optimizers. Range `[0, 0.5]`; lower is
closer to a face.

| task | ens | botorchgp | svgp | ens strictly closest? |
|---|---|---|---|---|
| Branin-2D | **0.00000** | 0.12384 | 0.12979 | yes |
| Styblinski-5D | 0.33155 | 0.22485 | 0.22192 | **no** |
| Levy-8D | **0.36783** | 0.44592 | 0.45796 | yes |
| Rosenbrock-10D | **0.23246** | 0.32994 | 0.35246 | yes |
| Rastrigin-15D | **0.26345** | 0.45601 | 0.46373 | yes |
| Ackley-20D | **0.24854** | 0.48107 | 0.48002 | yes |
| Griewank-30D | **0.14530** | 0.49670 | 0.47482 | yes |

**6/7 >= the registered 5/7 majority. FF2 = CONFIRMED.** The separation widens sharply with
dimension: at 30-D the GPs' returned optima sit essentially at the box centre in the
min-coordinate sense (0.497 of a possible 0.500) while the ensemble's sit at 0.145. On Branin the
ensemble's optimum is exactly ON a face (`d_bnd` = 0, `frac_at_bound` = 0.750). The one failure
is Styblinski-5D, where the ordering reverses.

**Two honest qualifications, neither optional.**

1. **The effect is optimizer-dependent.** It is carried by grad and cma; perturb separates the
   classes far more weakly. Ackley-20D: ens/gp = 0.262/0.484 (grad), 0.275/0.484 (cma), but
   0.214/0.226 (perturb). Griewank-30D: 0.173/0.497 (grad), 0.180/0.497 (cma), 0.117/0.153
   (perturb). The registered statistic pooled over optimizers, and that pooled statistic is what
   the verdict rests on; the breakdown is reported because it qualifies how general the
   phenomenon is.
2. **`frac_at_bound` is 0.000 everywhere except Branin.** No coordinate of any returned optimum
   in 5-D through 30-D lands within 0.01 of a face. "Closer to the boundary" here means a
   systematically smaller minimum coordinate, **not** designs pinned against the box. The
   unbounded-growth picture — a mean maximized at the corner — is not what the coordinates show
   in high dimension.

---

## FF3 — the NTK-regime premise is DISCHARGED

0C flagged as an undischarged assumption that the w=96 ensemble is approximately in a regime
where Xu's far-field result transfers. FF3 measures it directly: linearity of the ensemble mean
on the NEAR segment `s in [0.6, 1.0]`, i.e. just inside and at the support edge.

| task | median R2 | median \|slope\| |
|---|---|---|
| Branin-2D | 0.9873 | 1.437 |
| Styblinski-5D | 0.9474 | 2.113 |
| Levy-8D | 0.9907 | 1.363 |
| Rosenbrock-10D | 0.9862 | 0.777 |
| Rastrigin-15D | 0.9918 | 1.113 |
| Ackley-20D | 0.9952 | 1.987 |
| Griewank-30D | 0.9954 | 0.948 |

The ensemble mean is **already in a linear-ray regime at the training boundary** on all 7 tasks
(median R2 0.947–0.995). The assumption 0C carried is now measured rather than assumed, and the
write-up no longer needs to state it as a caveat. Per the pre-registration FF3 does not gate the
binary, and it does not rescue FF1. The ensemble's linearity was never what FF1 doubted; what
FF1 killed is the claim that this linearity **distinguishes** the ensemble from a GP.

---

## Compatibility with Elimination 2 (recorded in advance, unchanged by the outcome)

0D is **not** inconsistent with Elimination 2's use of NTK to argue that width does not matter.
The asymptotics are in **different variables**:

- Xu et al. (arXiv:2009.11848) Thm 1 — asymptotic in far-field **DISTANCE** along a ray, at
  fixed width; a ReLU MLP tends to a linear function outside the training support at rate O(1/t).
- Elimination 2 — asymptotic in **WIDTH**, at fixed input.

A network can be width-insensitive and still linearly extrapolating; the two constrain orthogonal
limits and must not be read as contradictory. FF1's confirmation of ray-linearity for the
ensemble (7/7) and Elimination 2's width-invariance finding are both true, simultaneously.

---

## Post-hoc observation, explicitly NOT part of the verdict

The FAR segment was registered as `s in [1.5, 3.0]`. Within it no GP curve reverts. A GP with a
`ConstantMean` and a Matern kernel **must** revert eventually, so reversion presumably begins at
some larger radius; the fitted ARD lengthscales are evidently long enough relative to the box that
`s = 3` is still inside the kernel's influence.

This is recorded as an observation, not a finding, and it does **not** change the verdict. Three
reasons, all registered in advance: the segment was fixed before the run; 0D was registered as
one attempt with no re-specification after seeing numbers; and — decisively — a mechanism that
only separates the classes at radii the optimizer never visits cannot explain optimizer
behaviour inside the box. The optimizers are clamped to `[0,1]^d` (`code/mbo.py:227-256`), so
`s > 1` is already unreachable; whatever happens at `s > 3` is further still from anything the
pipeline does. Testing reversion radius would be a different question under a new
pre-registration, and would not revive FF1 as an explanation of the gap.

---

## What this does and does not license the paper to say

**Licensed.**
- The ensemble mean extrapolates approximately linearly along rays out of the training support,
  on 7/7 tasks (median R2 >= 0.98), and is already linear at the support edge (FF3). Xu's result
  is empirically confirmed in this setting.
- The exact GP and the SVGP **also** extrapolate approximately linearly over the same range and
  do not revert within it.
- The ensemble's returned optima sit closer to the box boundary than either GP's on 6/7 tasks,
  by a margin that widens with dimension — as a **described phenomenon**, with the
  optimizer-dependence and the `frac_at_bound` = 0 qualification stated alongside.

**Not licensed.**
- Any claim that the ensemble's mean "grows without bound where the GP's reverts". Measured:
  false in the probed range, on 0/7 tasks for both GP classes.
- Any claim that linear extrapolation is the mechanism behind the GP–ensemble gap, or that it
  explains the boundary-seeking in FF2. FF1 removes exactly that inference.
- Promoting section 5 from elimination to positive mechanism. The registered binary requires FF1
  and FF2 both; FF1 killed.

**Consequence for section 5.** It ships as seven eliminations plus the diagnosis, unchanged. If
FF2 is used at all it must be reported as a phenomenon whose proposed explanation was tested and
refuted in the same run — reporting the confirmation without the kill would invert the meaning of
the experiment.
