# Session state — Blueprint session (Phases A–E)

Started 2026-07-17. Updated after every unit. Format: `unit | status | path | sha/note`.

## Environment reality (load-bearing)
- This macOS machine had **no working torch/sklearn/botorch env** at session start. The
  repo `venv/` is a **Windows** venv (`venv/Scripts/python.exe`, torch 2.11.0 Windows
  binaries) — non-functional here. The camera results were generated off-machine.
- Built a macOS venv for this session: `<scratchpad>/venv_mac` (Python 3.13.7, torch
  **2.13.0**, botorch 0.18.1, gpytorch 1.15.2, sklearn, scipy, cma, pandas). Log:
  `logs/pip_install.log`. All corner/analysis runs use this interpreter.
- **Platform-shift caveat for the reproduction gate:** the published Table 1 was produced
  on Windows/torch 2.11; corners here run on macOS-arm64/torch 2.13. Per-seed RNG will
  differ; the gate is therefore evaluated on **30-seed means** with an explicit tolerance
  stated before the look (see PART III / decision tree).
- `design_bench` is NOT installed and is not installable here (disk was ~8 GiB free at
  start; DB needs TF1.x + mujoco). **Design-Bench corners are MISSING this session** — see
  FAILURES.md. Synthetic corners proceed.

## The four corners
- **(on,on)** = committed `results/results_camera.json` (sha256 73ce3be9…, 392577 bytes,
  = `git show HEAD:` — verified byte-identical). NOT re-run.
- **(off,off) / (on,off) / (off,on)** = launched via `code/run_corners.py`, 9 grid cells,
  30 seeds, 7 synthetic tasks → `results/corners/corner_*.json`.

## Unit ledger
| unit | status | path | note |
|---|---|---|---|
| A.0 run_all `--out`/`--methods` | DONE | code/run_all.py | safety flag; default path unchanged |
| A.0 mbo X1/X3 env switches | DONE | code/mbo.py | `MBO_X1`/`MBO_X3`; unset ⇒ both True (camera engine) |
| A.0 gradtune `--out` + 7 tasks | DONE | code/gradtune.py | adds Levy/Rastrigin/Griewank |
| A.0 corners driver | DONE | code/run_corners.py | 3 missing corners |
| A.0 camera byte-verify | DONE | results/results_camera.json | sha matches HEAD |
| A.1.1 four corners run | RUNNING | results/corners/ | off_off in flight; (on,on)=camera done |
| A.1.4 do-nothing baseline | DONE | results/dobest.json | grid beats do-nothing 7/7 |
| Gate analyzer | DONE | code/analyze_corners.py | (on,on) preview η²_surr=0.369, ρ=+0.536 |
| A.1.2 gradtune 2×2 (script) | READY | code/gradtune.py | run after corners |
| A.1.3 held-out RMSE/NLL (script) | READY | code/heldout.py | run after corners |
| A.1.5 x0 inversion (script) | READY | code/x0_inversion.py | run after corners |
| A.1.6 3×3 coverage (script) | READY | code/coverage33.py | run after corners |
| Phase C venue | DONE | docs/AAAI27_VENUE.md | 4 AAAI-27 pages fetched |
| Phase D novelty | DONE | docs/NOVELTY_V2.md | Li/Rudner/Wilson owns ~90% of A findings |
| Phase B hyperresearch 2-16 | RUNNING | docs/hyperresearch/ | 2 agents |
| A.2 prereg contingent arms | DONE | docs/PREREGISTRATION_V2.md | M1/X11/X4 added, timestamped |
| Phase E blueprint v1 | DONE | docs/AAAI_BLUEPRINT.md | Part I PENDING; Part III pre-committed |
