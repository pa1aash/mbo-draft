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
