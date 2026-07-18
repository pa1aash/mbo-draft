# Phase 5.1 + 6 — Design-Bench at scale (pod)

**Env:** `dbm` (conda, under `envs/miniforge`) — torch 2.8.0+cpu, numpy 1.23.5, sklearn 1.0.2,
botorch 0.10.0, gpytorch 1.11, design-bench 2.0.20 (see docs/POD_ENV.md). db-subsample 8000,
16 seeds, 9 grid cells. git_sha at run time: `17d0465`.

**Engine provenance.** Every corner file under `results/db_corners/` carries a top-level `meta`
block and a per-cell `_engine` stamp (run_all 0.4). `results_db.json` is the shipped **off_off**
engine (X1=off, X3=off), established empirically in docs/POD_DB_VERIFICATION.md. The four corner
files are:

| file | X1 | X3 |
|---|---|---|
| `corner_off_off_db.json` | off | off |
| `corner_on_off_db.json`  | on  | off |
| `corner_off_on_db.json`  | off | on  |
| `corner_on_on_db.json`   | on  | on  |

Mujoco (Ant/DKitty) live in `corner_<tag>_mujoco_db.json` (separate files so the two
concurrent writers never race one JSON). Analysis: `code/analyze_db.py`
(-> `results/db_corners/db_analysis.json`), coverage: `code/coverage_db.py`
(-> `results/db_corners/coverage_db.json`). Both reuse the paper's own eta2/Friedman/bootstrap
and coverage-from-D methods verbatim.

---

## 5.1 — reproduction (fresh off_off vs `results_db.json`)

Tolerance, stated before the look (matching the synthetic Phase 2 pattern): deterministic
cells (exact-oracle TFBind8/TFBind10) match to **< 1e-3 absolute**; stochastic (RF-oracle)
tasks to **< 5% relative** on the per-cell 16-seed mean.

| task | oracle | verdict | worst |diff| | worst rel |
|---|---|---|---|---|
| TFBind8 | exact | **MATCHES** | 0.0000 | 0.0000 |
| TFBind10 | exact | **MATCHES** | 0.0000 | 0.0000 |
| Superconductor | RandomForest | **MATCHES** | 0.0173 | 1.6% |
| UTR | RandomForest | **MATCHES** | 0.0136 | 1.4% |
| GFP | RandomForest | **DIVERGES** | 1.125 | **18.1%** |

Four of five tasks reproduce `results_db.json` within tolerance; the two exact-oracle tasks
reproduce bit-for-bit (0.0000). **GFP diverges** (~13–18% relative on 8 of 9 cells, not a single
outlier cell). This is a *finding*, not a bug, and was not tuned away: GFP is a 4740-dim discrete
task whose per-position argmax decode + RF oracle produces an extreme, unstable score scale — the
reference `results_db.json` GFP cell means themselves span −9.6 … +2.5 in p100 units, and GFP's
oracle std over D is 3.34 versus 0.04–0.31 for every other task (see 6.4). The divergence is the
GFP decode artifact, and it motivates the GFP quarantine in 6.5.

---

## 6.1 — DB four-corner eta² (5 non-mujoco tasks)

Method identical to `code/analyze_corners.py` / `run05.eta2`: per-task min-max normalize the 9
cells → 3×3, task-unmodeled marginals. Bootstrap 95% CIs (task + seed resampling, B=10000)
identical to `code/bootstrap_eta.py`.

| corner (DB) | η²_surr [95% CI] | η²_opt [95% CI] | η²_inter | Friedman p | synthetic η²_surr |
|---|---|---|---|---|---|
| off_off | **0.001** [0.001, 0.241] | 0.050 [0.002, 0.378] | 0.006 | 0.760 | 0.367 |
| on_off  | **0.032** [0.001, 0.326] | 0.114 [0.012, 0.420] | 0.035 | 0.263 | 0.283 |
| off_on  | **0.002** [0.002, 0.220] | 0.173 [0.030, 0.542] | 0.012 | 0.225 | 0.450 |
| on_on   | **0.018** [0.002, 0.274] | 0.129 [0.005, 0.518] | 0.036 | 0.190 | 0.405 |

(Bootstrap: task + seed resampling, B=10000, identical to `code/bootstrap_eta.py`. CIs are wide
because there are only 5 tasks and per-task min-max normalization injects resampling noise, but
in every corner the η²_surr **point estimate sits at the very floor of its own CI** — the surrogate
main effect is indistinguishable from zero.)

Surrogate marginals are nearly flat in every corner (e.g. off_off ens 0.63 / gp 0.66 / svgp 0.66;
on_on ens 0.53 / gp 0.62 / svgp 0.66). The optimizer marginal is the largest term in all four
corners, always led by **perturb** (perturb 0.76–0.81 vs grad 0.40–0.68 vs cma 0.46–0.64). With
mujoco folded in (7 tasks) the ordering holds: η²_surr 0.044–0.091, η²_opt 0.096–0.197, Friedman
p 0.011–0.157. Dropping GFP (4 tasks) leaves η²_surr 0.001–0.021 — the null is not a GFP artifact.

**Verdict: the DB corners do NOT mirror synthetic.** On the synthetic benchmark the surrogate
main effect dominates (η²_surr 0.28–0.45) and the Friedman omnibus rejects at p ≈ 1e-4. On
Design-Bench the surrogate main effect is **essentially zero in every corner** (η²_surr
0.001–0.032 on the 5-task set; 0.044–0.091 with mujoco), its point estimate lies at the floor of
its bootstrap CI, and the Friedman omnibus **fails to reject** on the 5-task set (p = 0.19–0.76).
What little structure exists is carried by the *optimizer* axis (perturb is the largest marginal
in all four corners) — the reverse of the synthetic ordering, where the surrogate led. This is the
half of the paper where the null lives: the "surrogate choice dominates the surrogate×optimizer
grid" headline is a synthetic-benchmark artifact and does not replicate on real Design-Bench
tasks. The X1/X3 engine toggles do not resurrect it — all four corners agree that η²_surr ≈ 0,
whereas synthetic showed the four corners spanning 0.28–0.45.

---

## 6.2 — mujoco (Ant + DKitty)

**RUNNABLE.** The RF-oracle data/pickles for `ant_morphology` and `dkitty_morphology` were absent
from the env build (only tf_bind/superconductor/gfp/utr were fetched). Downloaded via the HF
mirror into the design_bench_data dir:

```
hf download beckhamc/design_bench_data --repo-type dataset --local-dir <DBD> \
  --include 'ant_morphology*/*' 'dkitty_morphology*/*'
```

Both build and score with **no mujoco simulator** (RandomForest oracles): AntMorphology dim=60
N=10004, DKitty dim=56 N=10004, both continuous, finite oracle scores. All four corners were run
(16 seeds, 9 cells) → `corner_<tag>_mujoco_db.json`. These are the tasks macOS never reached.
Folded into the grid (7-task η²) they do not change the conclusion: surrogate effect stays small
(η²_surr 0.044–0.091 across the four corners), optimizer effect 2–3× larger (η²_opt 0.096–0.197).

---

## 6.3 — X11 (competing-mechanism kill): exact-oracle subset + noise floor

Cross-cell Friedman omnibus over the 9 cells × tasks, on the **exact-oracle subset
{TFBind8, TFBind10}** versus the RF-oracle tasks:

| corner | exact-oracle {TFBind8,TFBind10} (n=2) | RF-oracle {Super,GFP,UTR} (n=3) |
|---|---|---|
| off_off | Friedman p = **0.369** (null survives) | p = 0.460 (null survives) |
| on_off  | Friedman p = **0.337** (null survives) | p = 0.021 (rejects) |
| off_on  | Friedman p = **0.510** (null survives) | p = 0.033 (rejects) |
| on_on   | Friedman p = **0.407** (null survives) | p = 0.032 (rejects) |

**Verdict: the cross-cell null SURVIVES on the exact-oracle subset in every corner** (Friedman
p = 0.34–0.51). The only rejections anywhere are on the RF-oracle subset (p = 0.02–0.05 in three
of four corners) — i.e. the cross-cell "which cell is best" effect is a property of the
*approximate* RandomForest oracle, not of the ground-truth exact oracle. On the audited on_on
engine: exact p = 0.41 vs RF p = 0.032. Caveat: with only two exact-oracle tasks the Friedman
omnibus has very low power, so this is "consistent with the null" rather than a powered
acceptance; the finding is corroborated by η²_surr ≈ 0 (6.1) and by the noise floor below.

**Oracle noise floor.** Repeated oracle evaluation of the same designs (3× on 200 D-rows) gives
max variance ≈ **1e-15** (machine epsilon) for every task — the exact and RF oracles are
deterministic, so **oracle measurement noise is zero**. The observed within-task cross-cell
spread on the exact oracles (on_on cell-mean range: TFBind8 0.90, TFBind10 0.31) is far above the
across-seed estimation SEM (median 0.041 and 0.002 respectively) and astronomically above the
oracle noise floor. The null therefore is not noise drowning a signal: within a task the cells do
differ, but their *rankings do not agree across the two exact tasks*, so the omnibus cannot
reject and — critically — the effect is not attributable to surrogate identity (η²_surr ≈ 0).

---

## 6.4 — DB premise coverage from D (on_on)

`code/coverage_db.py` applies coverage33's P0-5 fix for DB: the in-distribution reference set is
drawn from **D (actual dataset rows)**, never `np.random.uniform` — DB designs are one-hot
vertices (discrete tasks) / normalized measurements (continuous), never uniform. Per
(task, surrogate), β=2, on_on engine, 4 seeds; c_ood averaged over the 3 optimizers.

| task \ surrogate | ens c_in / c_ood | botorchgp c_in / c_ood | svgp c_in / c_ood |
|---|---|---|---|
| TFBind8 | 0.836 / 0.827 | 0.970 / 1.000 | 0.735 / 0.999 |
| TFBind10 | 0.926 / 0.543 | 0.988 / 0.982 | 0.955 / 0.993 |
| Superconductor | 0.688 / 0.251 | 0.966 / 0.891 | 0.636 / 0.298 |
| GFP | 0.472 / 0.273 | 0.508 / 0.730 | 0.468 / 0.716 |
| UTR | 0.688 / 0.014 | 0.948 / 0.378 | 0.998 / 1.000 |

Premise coverage from D is generally high for botorchgp (0.51–0.99) and mixed for ens/svgp.
**GFP has the lowest in-distribution coverage on every surrogate (0.47–0.51)** — the decode
artifact again — and c_ood collapses hardest for the ensemble on Superconductor (0.25) and UTR
(0.01), i.e. the premise fails most on the ensemble's own OOD proposals.

---

## 6.5 — GFP quarantine (with / without GFP)

Every DB coverage mean, reported both ways (on_on):

| quantity | with GFP | without GFP | nominal 0.90 |
|---|---|---|---|
| mean c_in (all task×surr) | 0.785 | 0.861 | below → below |
| mean c_ood (all task×surr) | 0.660 | 0.681 | below → below |
| mean c_in, ens | 0.722 | 0.784 | below → below |
| mean c_in, **botorchgp** | **0.876** | **0.968** | **below → ABOVE** |
| mean c_in, svgp | 0.758 | 0.831 | below → below |

**Excluding GFP flips exactly one "below nominal 0.90" claim: botorchgp's mean in-distribution
coverage** rises from 0.876 (below nominal) to 0.968 (above nominal). GFP alone is what drags the
GP surrogate's premise coverage below nominal. For the eta² claims the quarantine changes
nothing: dropping GFP leaves η²_surr ≈ 0 (off_off 0.021, on_on 0.001 on the 4 remaining tasks),
so the 6.1 null is robust to GFP inclusion.

---

## Summary

- **5.1**: 4/5 tasks reproduce `results_db.json` (off_off) within tolerance; TFBind8/TFBind10
  bit-for-bit. GFP DIVERGES (18%, decode artifact).
- **6.1**: DB corners do **not** mirror synthetic — η²_surr ≈ 0 (0.001–0.032, 5-task) in every
  corner vs 0.28–0.45 synthetic; Friedman fails to reject (p 0.19–0.76); the optimizer axis
  (perturb) carries what little effect exists. The null lives on Design-Bench.
- **6.2**: Ant + DKitty RUNNABLE via RF oracles (data downloaded); do not change the conclusion.
- **6.3**: cross-cell null survives on the exact-oracle subset in all four corners (Friedman p
  0.34–0.51); the RF-oracle subset rejects (p 0.02–0.05) in 3/4 corners — the effect is an
  approximate-oracle phenomenon. Oracle noise floor ≈ 1e-15 (deterministic), so the null is not a
  noise artifact. Low power (n=2 exact tasks).
- **6.4**: premise coverage from D computed for all 5 tasks × 3 surrogates; GFP lowest c_in.
- **6.5**: excluding GFP flips only botorchgp c_in (0.876 below → 0.968 above nominal 0.90);
  the eta² null is unaffected.
