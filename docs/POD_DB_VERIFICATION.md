# Phase 5 — Design-Bench verification (pod)

**Env:** `dbm` (conda, under envs/miniforge) — torch 2.8.0+cpu, numpy 1.23.5, sklearn 1.0.2,
botorch 0.10.0, gpytorch 1.11, design-bench 2.0.20 (see docs/POD_ENV.md). db-subsample 8000.

## 5.3 — results_db.json ENGINE STATE, determined EMPIRICALLY

results_db.json ships with **no meta block**; its engine (X1/X3) was unverified. The camera
file taught that engine state cannot be inferred from a filename, so it was determined the same
way: run known cells under each engine and see which reproduces.

Ran TFBind8 + Superconductor, all 9 grid cells, seeds 0-3, under off_off and on_on; compared
per-seed means (seeds 0-3) to results_db.json's `all`[0:4].

| candidate engine | mean \|Δp100\| | mean \|Δp50\| | max \|Δp100\| |
|---|---|---|---|
| **off_off (X1=0,X3=0)** | **0.009** | 0.021 | 0.045 |
| on_on (X1=1,X3=1) | 0.112 | 0.087 | 0.447 |

Discriminating cells (TFBind8, seed 0-3 mean p100) reproduce off_off to **0.0000**:

| cell | pod off_off | results_db | diff |
|---|---|---|---|
| ens:grad | 2.2053 | 2.2053 | 0.0000 |
| ens:cma | 2.1207 | 2.1207 | 0.0000 |
| svgp:perturb | 1.5241 | 1.5241 | 0.0000 |

**VERDICT: results_db.json is the OFF_OFF engine (X1=off, X3=off)** — the pre-audit engine,
the SAME engine as results_camera.json. This is a finding: like the camera file, the DB
"camera-equivalent" is off_off, NOT the audited on_on. It also means results_db.json is
faithfully REPRODUCED on the pod (exact match on the discriminating cells).

### Consequence for Phase 6
Phase 6.1 assumed results_db.json was on_on and named the three missing corners as
(off_off, on_off, off_on). That is inverted: results_db.json IS off_off, so the three
genuinely missing DB corners are **on_off, off_on, on_on**. Phase 6 runs those.

## 5.1 — reproduction on the 5 non-mujoco tasks

Tolerance (stated before the look): with results_db.json now known to be off_off, a faithful
pod off_off run reproduces it to within library-version drift — PASS if the discriminating
(deterministic) cells match to < 1e-3 and stochastic (SVGP/CMA) cells to < 5% relative, as on
synthetic (Phase 2). TFBind8 + Superconductor: **MATCHES** (0.0000 on the deterministic cells;
see above). TFBind10, GFP, UTR: verified in the full off_off DB corner run (Phase 6 driver);
see results/db_corners/ and the Phase 6 report for per-task MATCHES/DIVERGES/UNRUNNABLE.
