#!/usr/bin/env bash
# 04 — synthetic calibration / coverage diagnostic (Tier-3, exploratory). CPU-only.
# Feeds the in-distribution-coverage-predicts-collapse diagnostic (flagged exploratory,
# n=7 pending held-out replication). Merges into results_camera.json's calibration node.
set -u
cd "$(dirname "$0")/../.." || exit 1
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
mkdir -p cloud/queue/logs
JOBS=${JOBS:-$( (nproc 2>/dev/null) || echo 8 )}

echo "[04] synthetic calibration/coverage  ($(date -u +%FT%TZ), jobs=$JOBS)"
conda run -n main python code/run_all.py --exp calibration --seeds 30 --jobs "$JOBS" \
  2>&1 | tee cloud/queue/logs/04_calibration.log
echo "[04] done -> results/results_camera.json (calibration node)"
