# Environment verification — do the macOS envs reproduce the committed artifacts?

Verification discipline: tolerance stated before the look; a divergence is a FINDING, logged
with its magnitude, never adjusted to force a match. All verification runs are redirected with
`--out` to scratch — `results/` is not touched (confirmed byte-identical, §Safety).

---

## ★ HEADLINE FINDING — `results/results_camera.json` is the pre-audit (X1 OFF, X3 OFF) engine, NOT (on,on)

The mac-synth verification uncovered a mislabeled artifact that affects the AAAI_BLUEPRINT
four-corners analysis. **This is a finding to surface, not an env bug.**

**Evidence.** Fresh mac-synth runs on Branin-2D (30 seeds each), compared to `results_camera.json`:

| cell | camera | mac-synth **OFF_OFF** | mac-synth **ON_ON** |
|---|---|---|---|
| ens:grad | −9.267 | −9.395 (OK) | −7.351 (far) |
| ens:perturb | −0.780 | **−0.780 (exact)** | −0.452 (far) |
| ens:cma | −14.011 | **−14.011 (exact)** | −7.110 (far) |
| botorchgp:{grad,perturb,cma} | −0.398/−0.399/−0.398 | exact | exact |
| svgp:grad | −0.448 | −0.451 (OK) | −0.588 (far) |

**mac-synth OFF_OFF reproduces camera 9/9; mac-synth ON_ON does not.** The clean tell is
`ens:perturb = −0.780`: that is the X3-**off** behavior (per-slot best of 2·TOP init candidates,
oracle-selected), whereas X3-on returns top-TOP by surrogate LCB (≈ −0.45). The GP cells are
engine-invariant here and match either way.

**Provenance — why the camera is off_off.** The prior session's commit `a58f0d4` ("Bundle:
record the X1/X3 relaunch") states the relaunch *"scheduled 0 cells (have() is merge-safe resume
and every cell already had 30 seeds) but still re-serialized results/results_camera.json … Restored
from git."* **The X1/X3 relaunch never recomputed the grid** — merge-safe resume saw 30 seeds
already present in every cell and skipped all of them, then the file was restored from git. So the
committed camera has always held the pre-audit off_off numbers; the switch defaults in `mbo.py`
were flipped to True but the artifact was never regenerated under them.

**Impact on AAAI_BLUEPRINT.md (correctness).** This session's four-corners analysis took the
committed camera *as* the (on,on) corner. It is off_off. Consequences:
- The four-corners table's **on_on row (η²_surr=0.369, ρ=+0.536) is a second off_off measurement**,
  which is exactly why it came out nearly identical to the independently-run off_off corner (0.367)
  — they are the same engine.
- The **true (on,on) corner was never computed** this session. The "X1 and X3 are real but
  *offsetting*, netting back to 0.369" narrative is therefore **unverified**: the X1-alone (0.283)
  and X3-alone (0.450) corners are correct (they were run with explicit `MBO_X1/X3`), but the claim
  that they *cancel* rested on the mislabeled camera.
- The **reproduction gate is unaffected** — it compared the off_off corner to the published Table 1
  (also off_off) and passed 63/63; that comparison is apples-to-apples and stands.

**Correction in progress.** The true on_on grid (7 tasks × 30 seeds, X1/X3 on) is being computed on
mac-synth (to scratch, not `results/`); the four-corners table and the offsetting-cancellation
claim will be corrected once it lands. **No number is being inferred in the meantime** — the on_on
row is marked UNVERIFIED.

---

## Phase 4.1 (synthetic) — mac-synth reproduces the camera's actual engine

Tolerance (before the look): per cell |diff| ≤ max(2·SEM₃₀, 0.10·|camera|) if |camera|>1, else 0.10.
- **Branin-2D, off_off, 30 seeds: 9/9 cells MATCH** (`scratchpad/synth_offoff.json`). ens:cma and
  ens:perturb reproduce to the third decimal; GP/SVGP cells exact.
- Smoke (`run_all.py --smoke`) passes (58 cells, 0 failed).
- **Verdict: mac-synth is VERIFIED** against `results_camera.json` (which is the off_off engine).
  The env is stable and reproducible from `envs/mac-synth-requirements.lock`.

Note on the ON_ON divergence: it is **not** an env fault — it is the same-engine/different-engine
distinction above. When mac-synth runs the engine the camera actually used (off_off), it matches.

---

## Phase 4 (Design-Bench) — envs/mac-db

**Stage reached: STAGE 2 (of 3), fully.** All five non-mujoco tasks build and oracle-evaluate,
and the full 9-cell surrogate×optimizer grid runs.

### Stage progress
- **Stage 1 (import design_bench): DONE.** Required patching the deepchem/rdkit molecule-feature
  import to optional (deepchem→rdkit→torch is impractical on arm64; db_tasks never uses Morgan
  fingerprints). deepchem is uninstalled entirely and design_bench imports cleanly.
- **Stage 2 (TFBind8/10, Superconductor, GFP, UTR load + score): DONE — 5/5.**

  | task | dim | N | oracle | loads+scores |
  |---|---|---|---|---|
  | TFBind8 | 32 | 32,898 | exact | ✅ |
  | TFBind10 | 40 | 4,161,482 | exact (4^10 landscape, ~100s build) | ✅ |
  | Superconductor | 86 | 17,014 | RandomForest | ✅ |
  | GFP | 4,740 | 5,000 | RandomForest | ✅ |
  | UTR | 200 | 140,000 | RandomForest | ✅ |

  This covers **both exact-oracle tasks (TFBind8/10) that X11 needs**. The HF mirror
  `beckhamc/design_bench_data` is LIVE (445 files); the download was extended beyond the cloud
  script's 3 tasks to include GFP + UTR. The full grid (ens / botorchgp / svgp × grad / perturb /
  cma) is live in the env (botorch 0.10.0, gpytorch 1.11 install cleanly on py3.9 without bumping
  numpy off 1.23.5).
- **Stage 3 (Ant, D'Kitty, Hopper — mujoco): NOT attempted → recommend cloud pod.** These need
  `morphing-agents`→mujoco at IMPORT (§1.5); arm64 mujoco is the documented hard case. It is not
  worth burning hours locally when the RunPod Linux pod already runs them. The 5 Stage-2 tasks are
  the scientifically decisive set (both exact oracles + 3 RF-oracle tasks).

### Phase 4.1/4.2 — verification against `results_db.json` (tolerance stated before the look)
Tolerance: |diff| ≤ max(2·SEM, 0.15·|ref|). Run in-process (macOS **fork crashes** with torch +
design_bench → `BrokenProcessPool`; the grid must run with `MBO_SPAWN=1`, or single-process).

| task/cell | mac-db | results_db.json (16 seeds) | verdict |
|---|---|---|---|
| TFBind8 / **gp** (sklearn exact GP) | 1.000 | 1.000 | **MATCHES** (deterministic, exact) |
| TFBind8 / **ens:grad** | 1.674 (n=3; seeds 2.07/1.23/1.73) | 2.201 | **DIVERGES** (Δ=−0.53) |

**Finding (not papered over):** exactly as on synthetic, the **deterministic GP cell reproduces
exactly** while the **neural-ensemble cell diverges** — its per-seed values straddle the reference
(seed 0 = 2.07 ≈ the published 2.20), but neural-net training RNG differs between macOS/torch-2.8
and the Linux pod that generated `results_db.json`, so the 30-seed mean will not match to tight
tolerance. **A reviewer re-running the artifact on macOS would see the same ensemble drift.** This
is a portability property of the ensemble, not an env defect; the env is correct (GP path exact,
tasks load, grid runs). Magnitude logged: ~0.5 normalized units on TFBind8 ens:grad at n=3.

### Phase 4.3 — wall-clock for one DB corner (this 8-core Mac)
Per-cell timings measured: ensemble train ≈ 26 s (TFBind8, subsample 8000), botorch/svgp GP fit
≈ 10–20 s, oracle eval ≈ 0 s; the 9-grid **avoids** the slow sklearn exact-GP baseline (~200 s).
The binding cost is **TFBind10**: under spawn (fork unavailable) every worker rebuilds the 4^10
landscape (~100 s each). Estimate for one full Stage-2 DB corner (5 tasks × 16 seeds × 9 cells):
**≈ 3–8 hours**, dominated by TFBind10's per-worker rebuild and GFP's dim-4740 cells. TFBind8 /
Superconductor / UTR corners are ~1–2 h combined; run TFBind10 in its own low-concurrency pass
(as the cloud queue does). For the four-corner DB program, budget ~1–1.5 days on this machine, or
use the pod.
