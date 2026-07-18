# Platform-arm summary — three Design-Bench findings for the paper

macOS / Apple Silicon arm of the platform-variance program. All results at a stamped,
matched engine (X1=on, X3=on unless a sweep says otherwise), torch 2.8.0, python 3.9,
n=16 seeds, Design-Bench subsample 8000. Every record carries the 19-field env+engine meta
block `{platform, os_release, python, torch, numpy, botorch, gpytorch, cma, git_sha, X1, X3,
K, beta, TOP, OPT_STEPS, LR_OPT, n_seeds, seed, timestamp}`. Deterministic GP cells reproduce
`results/results_db.json` to 1.000, which is what makes the neural-surrogate movements below
readable rather than noise. Artifacts:
`results/platform/tfbind8_macos_torch28_n16.json` (finding 1 grid + finding 2),
`results/platform/tfbind8_engine_2x2_n16.json` (finding 1 2x2),
`results/platform/db_freeze_beta_n16.json` + `results/platform/gp_freeze_step1.json`
(finding 3). Companion notes: `docs/DEGENERATE_CELLS.md`, `docs/GP_FREEZE.md`,
pre-registration `docs/PREREGISTRATION_V2.md` (DB1-DB4 + the two dated amendments).

---

## Finding 1 — the 2.20-vs-1.76 gap is engine state (X3), not platform

The macOS `ens:grad` cell on TF-Bind-8 scores 1.7614 ± 0.2018 (n=16) at the audited engine,
against 2.2007 ± 0.031 published in `results/results_db.json` — a ~0.44-unit gap that looked
like cross-platform drift. It is not. The gap reproduces **on one machine** by flipping the
engine switches; a 2x2 over {X1 off/on} x {X3 off/on} for `ens:grad`, TF-Bind-8, n=16:

| corner | X1 | X3 | mean | std | 95% CI | contains 2.20 | matches published 2.2007 |
|---|---|---|---|---|---|---|---|
| off_off | off | off | **2.2037** | 0.0402 | [2.183, 2.224] | **yes** | \|Δ\| = 0.003 |
| on_off | on | off | 2.2285 | 0.0274 | [2.215, 2.242] | no (above) | \|Δ\| = 0.028 |
| off_on | off | on | 1.3925 | 0.2660 | [1.258, 1.527] | no | \|Δ\| = 0.808 |
| on_on | on | on | 1.7614 | 0.2018 | [1.659, 1.864] | no | \|Δ\| = 0.439 |

`on_on` reproduces the cross-platform grid cell byte-for-byte (apparatus check). The 2x2
decomposition: **X3 main effect +0.639 (dominant)**, X1 main effect +0.197, interaction +0.344
(X1 barely moves p100 when X3=off, adds ~0.37 when X3=on). The corner that reproduces the
published number to three decimals with the same tight std is **off_off**, so
`results/results_db.json`'s `ens:grad` cell is the **pre-audit X1=off, X3=off engine**. X3=off
is the pre-audit protocol where gradient returns the final iterate of all 2xTOP inits and
`eval_designs` applies an oracle top-TOP filter, mechanically inflating p100 (a max over
oracle-SELECTED designs) — the "two estimands under one column" the X3 audit removed.

**For the paper:** do not present 1.76-vs-2.20 as OS/library portability. It is engine state.
This also settles the open P0 (the pod's Phase 5.3): the published `ens:grad` cell is the
pre-audit engine. Caveat: this determines the engine of the `ens:grad` cell only; whether the
whole of `results_db.json` is uniformly off_off is not established here. The genuine
cross-platform question (Mac-vs-pod at a matched stamped engine) is separate and still open on
the pod's Linux arm.

---

## Finding 2 — four of nine cells are degenerate constants (dataset-best retrieval)

On TF-Bind-8 at X1/X3=on, four of the nine grid cells return `p100 = 1.0` on **every** seed
with zero variance: `botorchgp:grad`, `botorchgp:perturb`, `botorchgp:cma`, and `ens:perturb`.
This is not a score — it is the normalized dataset reference. Design-Bench scores are min-max
normalized to the offline dataset's own range, so the best design already in D maps to exactly
`y01 = 1.0` (7 of the 8000 rows tie at the max; raw oracle range ymin=0.0, ymax=0.439296;
`oracle(dataset-best)` = 1.0 exactly). A cell pinned at 1.0 has returned a design **no better
than the best already in D — it beats nothing.** The cells that actually optimize exceed it:
`ens:grad` 2.067, `ens:cma` 2.130, `svgp:grad`/`svgp:cma` 2.160 (all p100 max over seeds).

**For the paper:** reporting "1.00" for the four constant cells without stating it is a fixed
dataset-reference value presents a non-result as a score. On the discrete tasks a Friedman
omnibus that ranks cells including several tied constants cannot resolve them by construction,
so `eta2_opt ~ 0` there is partly "the optimizer CANNOT move these cells," not "the optimizer
does not matter." The frozen-cell case and the genuine-equivalence case (continuous tasks,
finding 3) must be reported separately, not pooled under one Contribution-3 claim.

---

## Finding 3 — the freeze has TWO mechanisms across tasks (do not collapse them)

Why do the constant cells return D? Two distinct mechanisms operate, on different tasks. Both
are real; neither label covers both. (Pre-registered DB1-DB4; full verdicts in
`docs/GP_FREEZE.md`.)

**(A) LCB paralysis — UTR (and the beta=0 persistence).** On UTR the BoTorch-GP gradient cell
is frozen at **all** beta with **zero displacement**: `botorchgp:grad` returns disp_from_data
0.0000 and decode_in_D 1.000 at both beta=2 (0.9416 ± 0.0044) and beta=0 (0.9414 ± 0.0044).
The high-dim GP posterior mean is already flat at the data, so the optimizer never leaves,
with or without the sigma term. The design does not move; there is nothing for the decode to
revert. This is LCB / gradient paralysis (M-A) in its pure form.

**(B) Decode snap-back — TF-Bind-8.** On TF-Bind-8 the same cell **does move** in the relaxed
logit space — mean ||x_final - x0|| ~ 0.098 at beta=2 (`gp_freeze_step1.json`), and at beta=0
it moves further (disp_from_data 0.49) and its score shifts off the constant (0.9882 ± 0.0427,
decode_in_D drops to 0.875). But at beta=2 the argmax decode reverts every moved design to the
same top-128 dataset sequences (decode_in_D = 1.000), so the returned p100 stays pinned at the
constant. Here sigma also pins it (removing it at beta=0 unfreezes grad and cma), but the
decisive difference from the continuous control is the decode. This is decode snap-back (M-B).

**The continuous control (Superconductor) separates them.** With no argmax decode, the GP cells
do NOT freeze: `botorchgp:grad` = 1.1818 ± 0.1239 (real variance), disp 0.0250 (> 0), and the
cells differ by optimizer (grad 1.18 vs perturb 1.24). The cleanest single datum:
`botorchgp:perturb` barely moves on BOTH task types (disp 0.0000 discrete, 0.0004 continuous)
yet returns a zero-variance constant ONLY on the discrete task — the one thing that differs is
the decode step. So on continuous inputs an exact-constant freeze needs the decode; on high-dim
discrete inputs paralysis alone can freeze without any movement at all.

A refinement worth stating: the freeze is not purely a GP property. `ens:perturb` also freezes
on the discrete tasks (decode_in_D = 1.000) while `ens:grad` never does (it leaves the data by
disp 2.2-7.2, decode_in_D 0). The freeze is a surrogate x optimizer x decode interaction — a
landscape the optimizer cannot escape (a smooth GP for any optimizer; a jagged ensemble only
for the weak perturb optimizer) plus, on discrete inputs, the argmax.

**Ant is the pod test that decides which mechanism dominates.** Ant is continuous AND degenerate
in Table 3 (1.52 x3). Superconductor (also continuous) does NOT freeze, so if Ant genuinely
returns a zero-variance constant, then LCB paralysis (A) can freeze a continuous task with no
decode — and paralysis, not decode, would be the general mechanism. If Ant instead shows a
tight non-degenerate cluster like Superconductor, its Table-3 look is not a true freeze and
decode snap-back (B) remains the discrete-only mechanism. Ant needs mujoco (pod-only) and could
not be run here. The decisive measurement: Ant GP cells, beta=2, n>=16 — read whether the
variance across the three optimizers is EXACTLY zero (paralysis dominates) or merely small
(decode dominates). A single seed does not decide it; the whole question is whether the
variance is zero.

---

## Provenance and guardrails

Commits on `platform-arm`, authored locally, chronological: cross-platform grid; engine 2x2;
degenerate-cells note; DB1-DB4 pre-registration (before running); GP-freeze Step 1; Step 2
scope amendment; GP-freeze Step 2. `results/results_db.json`, `results/results_camera.json`,
and `paper/aaai27/*.tex` were never touched; the K x beta grid was not started (it is
synthetic and platform-invariant — it belongs on the pod). Everything mujoco (Ant, D'Kitty,
Hopper) is pod-only and untested here.
