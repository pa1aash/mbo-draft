# Environments — macOS (arm64) build + usage guide

Two environments, because they are **mutually exclusive** (see "Why not one env"). Built and
verified 2026-07-18 on Apple Silicon / macOS 26.3.1. The built envs live under `envs/` and are
**gitignored**; the `.lock` files and the `mac-db-patches/` are committed and reproduce them.

Interpreter used to create both: `/Library/Frameworks/Python.framework/Versions/3.13/bin/python3`
(mac-synth, py3.13) and `/usr/bin/python3` (mac-db, py3.9 — Design-Bench requires 3.9).

## Which env runs which experiment
| env | python | runs | key pins |
|---|---|---|---|
| `envs/mac-synth` | 3.13 | the synthetic grid (`code/run_all.py`, `mbo.py`, all Phase-A arms) | torch 2.13, numpy 2.5.1, sklearn 1.9.0, botorch 0.18.1, gpytorch 1.15.2, cma 4.4.4 |
| `envs/mac-db` | 3.9 | Design-Bench tasks (`--db`) via `db_tasks.py` + the same grid | design-bench 2.0.20, numpy 1.23.5, sklearn 1.0.2, torch 2.8.0, botorch 0.10.0, gpytorch 1.11 |

## Why not one env (they cannot be merged)
Design-Bench 2.0.20 calls `np.NINF` and `np.bool` (removed in numpy 2.0) and loads
RandomForest-oracle pickles written by scikit-learn <1.4 (fail to unpickle on ≥1.4). It therefore
needs **numpy 1.23.5 + sklearn 1.0.2**. The synthetic grid uses **numpy 2.5.1 + sklearn 1.9.0**.
numpy 2 and numpy 1.23.5 cannot coexist in one interpreter. This is confirmed from the actual pins
(`requirements.txt` vs `cloud/fix_designbench.sh`), and is why `cloud/setup.sh` builds separate
`main` and `db` conda envs. See `docs/ENV_RECON.md` §1.4.

## Build mac-synth (from the lock)
```bash
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 -m venv envs/mac-synth
envs/mac-synth/bin/python -m pip install -r envs/mac-synth-requirements.lock
```
Verify: `cd code && ../envs/mac-synth/bin/python run_all.py --smoke --out /tmp/smoke.json`
(reproduces `results_camera.json` — which is the **off_off** engine, see ENV_VERIFICATION.md — 9/9
on Branin in off_off mode).

## Build mac-db (from the lock + patches + data)
```bash
/usr/bin/python3 -m venv envs/mac-db                       # py3.9
envs/mac-db/bin/python -m pip install -r envs/mac-db-requirements.lock
# apply the macOS source patches to the installed design_bench (idempotent):
envs/mac-db/bin/python envs/mac-db-patches/fix_designbench_macos.py
# download task data from the live HF mirror (incl. GFP/UTR beyond the cloud script's 3 tasks):
envs/mac-db/bin/python - <<'PY'
from huggingface_hub import snapshot_download
DBD="envs/mac-db/lib/python3.9/site-packages/design_bench_data"
snapshot_download("beckhamc/design_bench_data", repo_type="dataset", local_dir=DBD,
  allow_patterns=['tf_bind_8-SIX6_REF_R1/*','tf_bind_10-pho4/*','superconductor/*','gfp/*','utr/*'])
PY
```
Verify: `cd code && ../envs/mac-db/bin/python db_tasks.py TFBind8 TFBind10 Superconductor GFP UTR`
(all print `dim=…` and an oracle vector).

## What fails on arm64 and why (Stage 3)
- **mujoco (Ant, D'Kitty, Hopper):** these tasks import `morphing-agents`→mujoco at IMPORT even
  with the RandomForest oracle (the RF oracle removes mujoco only at *evaluation*). mujoco-py is
  dead on arm64. NOT built here — **run these three on the RunPod Linux pod** (`cloud/setup.sh`).
- **deepchem / rdkit:** patched out (Morgan-fingerprint molecule features, unused by db_tasks).
- **tensorflow:** not installed; the GFP/UTR RandomForest oracles avoid the TF exact oracles.
- **multiprocessing fork:** macOS + torch + design_bench crash forked workers
  (`BrokenProcessPool`). Runs MUST set `MBO_SPAWN=1` (run_all.py honors it) or run single-process.

## Commands for the four-corner Design-Bench program (Stage-2 tasks, on this Mac)
Each corner writes its own file; `MBO_SPAWN=1` is mandatory; keep TFBind10 in a low-concurrency
pass. **Never write to `results/` directly** — these use `--out` to a corners dir.
```bash
DB="ens:grad ens:perturb ens:cma botorchgp:grad botorchgp:perturb botorchgp:cma svgp:grad svgp:perturb svgp:cma"
S2="TFBind8 Superconductor GFP UTR"     # fast Stage-2 tasks
# per corner tag/x1/x3 in {off_off:0/0, on_off:1/0, off_on:0/1, on_on:1/1}:
MBO_SPAWN=1 MBO_X1=<x1> MBO_X3=<x3> envs/mac-db/bin/python code/run_all.py \
  --exp mbo --db --db-subsample 8000 --seeds 16 --jobs 4 --tasks $S2 \
  --out results/corners/corner_<tag>_db.json --methods $DB
# TFBind10 separately, low concurrency (per-worker 4^10 rebuild):
MBO_SPAWN=1 MBO_X1=<x1> MBO_X3=<x3> envs/mac-db/bin/python code/run_all.py \
  --exp mbo --db --db-subsample 8000 --seeds 16 --jobs 2 --tasks TFBind10 \
  --out results/corners/corner_<tag>_db_tfb10.json --methods $DB
```
Wall-clock: ~3–8 h per corner on this 8-core Mac (ENV_VERIFICATION.md §4.3); budget ~1–1.5 days
for all four Stage-2 corners, or use the pod. **Verification caveat:** the deterministic GP cells
reproduce `results_db.json` exactly; the neural-ensemble cells drift (macOS-vs-Linux training RNG)
— a real, disclosable portability property, not an env bug.
