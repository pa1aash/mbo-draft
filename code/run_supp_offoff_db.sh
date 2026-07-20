#!/usr/bin/env bash
# Design-Bench half of tab:cov, on the stamped X1-off/X3-off engine.
# Separate env: the DB stack is python 3.9 / torch 2.8 / botorch 0.10 (see
# results/db_corners/coverage_db.json meta), not the synthetic pod-synth stack.
# 16 seeds to match the existing DB block and enginemap row "Design-Bench | 16".
set -euo pipefail
cd "$(dirname "$0")"
PY=/workspace/MBO/envs/miniforge/envs/dbm/bin/python
OUT=../results/supp_offoff
mkdir -p "$OUT"

export MBO_X1=0 MBO_X3=0

# TFBind10 is run separately under MBO_SPAWN=1: its 4^10 oracle build crashes
# forked workers (db_tasks.py:24-26).
$PY run_all.py --exp calibration --db \
  --tasks TFBind8 Superconductor GFP UTR AntMorphology DKitty \
  --seeds 16 --jobs 14 \
  --out "$OUT/calibration_db_off_off.json"

MBO_SPAWN=1 $PY run_all.py --exp calibration --db \
  --tasks TFBind10 --seeds 16 --jobs 4 \
  --out "$OUT/calibration_db_off_off.json"

echo "=== DB DONE ==="
