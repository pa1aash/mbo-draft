# 0C — Far-field functional form (FF1/FF2) and member independence (MI1)

Pre-registered in `docs/PREREGISTRATION_V3.md` §0C, committed at `44b4268` before any
inspection of outcome data.

**Status: NOT-COMPUTABLE on stored artifacts. Both arms STOPPED.**

**BINARY: KEEP-ELIMINATION-BY-DEFAULT.**

Not KEEP-ELIMINATION-because-killed. No KILL condition fired, because no FF1 or FF2 statistic
could be computed. The linear-extrapolation mechanism is **untested here, not refuted**. The
paper ships the elimination and the diagnosis, exactly as it stood before 0C.

---

## Engine stamp

The artifact inspected is `results/mechanism/phantom_maxima.json`:

| field | value |
|---|---|
| git_sha (of the run that wrote it) | `d88d8b78dc413c3951e2a6a92fc9657a840afcf2` |
| timestamp | 2026-07-19T14:18:35 |
| platform / python | Linux-6.17.0-35-generic-x86_64-with-glibc2.39 / 3.12.3 |
| torch / botorch / gpytorch / numpy | 2.11.0+cpu / 0.18.1 / 1.15.2 / 2.4.4 |
| n_seeds / K / beta / TOP | 30 (0..29) / 5 / 2.0 / 128 |
| X1 / X3 | on / on |

Inspection performed at repo HEAD `23871dd`. No compute was run, so this document reports no
new numbers.

---

## Why both arms stopped

The pre-registration fixed, in advance, the input each prediction requires. All three inputs
are absent. The root cause is single and structural: **the pipeline persists only scalar
summary statistics.** Surrogates are fit, queried, reduced to scalars, and discarded
in-process. Nothing model-shaped and nothing design-shaped survives a run.

### The three required inputs, against what exists

| Prediction | Required input | Present? | Evidence |
|---|---|---|---|
| FF1 | A reconstructable surrogate — ensemble member weights, or GP fitted `state_dict` plus standardization constants — so the mean can be evaluated at NEW points along rays | **NO** | No `.pt`/`.pth`/`.ckpt`/`.pkl`/`.npz`/`.joblib` file exists anywhere outside `envs/`. `git log --diff-filter=A` over those extensions returns nothing, so none was ever committed and later removed. `code/` contains **zero** `torch.save` / `np.save` / `np.savez` / `pickle.dump` / `joblib.dump` call sites; every persistence path in the repo is a `json.dump` of nested scalar dicts. The single `state_dict` reference, `code/phantom_maxima.py:107`, is an in-memory clone between GP arms, not a disk write. |
| FF2 | Coordinates of the returned optimum x* per (task, seed, surrogate, optimizer) | **NO** | A programmatic scan of every JSON under `results/**` for nested numeric arrays — the shape a `128 x d` design matrix would serialize as — returns **0 hits**. In `code/phantom_maxima.py:205-216` the design matrix `xf` is computed, reduced by `_cell_record(...)` to `dhat`/`z`/`infl` scalars, and dropped. The one place `xf` escapes a cell runner (`code/mbo.py:549`) hands it to an in-memory consumer and never serializes it. |
| MI1 | Per-member predictions — the K=5 individual member outputs at the returned optima | **NO** | Members are collapsed at the point of use and never escape. `code/mbo.py:189-199`: `ens_moments_raw` forms the stacked `(K, N)` tensor `ps` and immediately returns `ps.mean(0)`, `ps.std(0)`; `ens_lcb_torch` likewise. Only mean and std survive the function. No key matching `member_*` / `per_member` / `ens_all` / `individual` exists in any result file. `results/kbeta/kbeta_ens.json` varies K over {2,3,5,10} but records only aggregate cell summaries. |

**Per the pre-registered rule, no training run was launched to manufacture any of these.**
Re-running `phantom_maxima.py` with added instrumentation would refit every ensemble and every
GP arm — a fresh experiment, not a reanalysis of stored data, and outside the scope 0C was
registered under.

### The near-miss: the existing far-field block covers only the GP arms

`results/mechanism/phantom_maxima.json` already carries a `farfield` block. It is the closest
existing artifact to FF1 and it still cannot answer it, for two independent reasons.

1. **It is not a functional-form probe.** Per `code/phantom_maxima.py:242-252`, it draws
   `N_FAR=512` uniform points in the box and stores exactly two scalars per arm: `ff`, the
   MEAN of `(mu_far - ym_D)/sd_y` over those points, and `ff_max`, its max. A mean and a max
   over scattered points carry no information about whether the mean function is LINEAR along
   a ray. R2 of a ray-fit is not recoverable from them.
2. **The ensemble is absent from it.** The block is written inside `for name, arm in
   arms.items()` — a loop over the six GP arms only. Verified directly: the arm keys under
   `farfield` are `botorchgp`, `gpm_ls`, `gpm_lssup`, `gpm_max`, `gpm_ph`, `gpm_sup` for all
   seven tasks. There is no `ens` entry and no `svgp` entry. FF1 is a between-class
   comparison; the class it needs was never probed.

For completeness: the stored `star.dhat` statistic is a 10-NN distance to D, normalized by
`rho`. It is a distance-to-support measure, not a distance-to-boundary measure. The
pre-registration named this in advance as **not** a substitute for FF2, and it is not used as
one here.

---

## FF1 — verdict

**NOT-COMPUTABLE.** No surrogate on disk can be reconstructed, so no mean function can be
evaluated along any ray, so no R2 exists to report — for either class, on any of the seven
tasks. Neither the confirmation nor the KILL condition was reached.

## FF2 — verdict

**NOT-COMPUTABLE.** No returned-optimum coordinates are stored, so boundary-proximity cannot
be measured for either class. Neither the confirmation nor the KILL condition was reached.

## MI1 — verdict

**SKIPPED — per-member predictions not retained.** The ensemble collapses its K=5 members to
mean and std inside `ens_moments_raw` before any value is returned, and nothing downstream
ever sees the individual members. Pairwise member correlation at the returned optima cannot be
formed from stored data. Per the pre-registered rule this arm was stopped rather than
regenerated by retraining.

---

## Compatibility note (recorded regardless of outcome)

0C is **not** inconsistent with Elimination 2's use of NTK to argue that width does not matter.
The two results are asymptotic in **different variables**:

- Xu et al. (arXiv:2009.11848) Thm 1 is asymptotic in far-field **DISTANCE** t along a ray
  from the origin, at fixed width — a ReLU MLP tends to a linear function outside the training
  support at rate O(1/t).
- Elimination 2 is asymptotic in **WIDTH** at fixed input.

A network can be width-insensitive and still linearly extrapolating; the two statements
constrain orthogonal limits. This note is recorded here so that a later reader pairing the two
citations does not mistake them for a contradiction.

## Assumption note (carried, not discharged)

The FF1/FF2 predictions presuppose that the w=96 ensemble is approximately in the NTK regime —
that is what licenses transferring Xu's result to this setting. The pre-registration committed
to checking this directly where the artifacts permit, by measuring ray-linearity AT the
training boundary.

**The artifacts do not permit it.** The check needs the same reconstructable surrogate FF1
needs, and for the same reason it is unavailable. The NTK-regime premise is therefore carried
as a **named, undischarged assumption**, not as a verified condition. Any future statement of
the linear-extrapolation mechanism must either discharge it or state it.

---

## What would make 0C computable

Recorded so the requirement is explicit, not as a proposal to run anything now. All three are
instrumentation changes to `code/phantom_maxima.py`; none changes the experiment's semantics,
and each would require a fresh run to take effect.

1. **FF1** — persist per (task, seed) either the ensemble member `state_dict`s and the GP arms'
   fitted `state_dict`s plus `ym`/`ys`, or, far cheaper and sufficient, the mean evaluated on a
   fixed ray grid: sample unit directions `u` from the data centroid, evaluate `mu(centroid +
   t*u)` on a fixed ladder of `t` spanning inside-support to far-field, and store that curve
   per arm. The second option stores kilobytes and answers FF1 directly, including the
   boundary-linearity check that would discharge the NTK assumption.
2. **FF2** — store `xf[argmax(mu)]`, the returned optimum's coordinates. One d-vector per cell.
3. **MI1** — have `ens_moments_raw` optionally return the `(K, N)` stack, and store the K
   member values at the returned optima. K=5 floats per cell.

---

## Bottom line

0C did not run. The mechanism is untested, not refuted, and the paper stays a pure elimination
plus diagnosis. The binary is **KEEP-ELIMINATION-BY-DEFAULT**, and the write-up must not
present it as evidence against linear extrapolation.
