#!/usr/bin/env bash
# 01 — synthetic crossed surrogate x optimizer factorial. THE first run: produces the
# GATE-1 matched-vs-unmatched data AND the synthetic baseline every transfer claim needs.
# CPU-only. Resumable. -> results_camera.json (unmatched) + results_camera_matched.json.
set -u
cd "$(dirname "$0")/../.." || exit 1
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
mkdir -p cloud/queue/logs
JOBS=${JOBS:-$( (nproc 2>/dev/null) || echo 8 )}

echo "[01] synthetic factorial — UNMATCHED  ($(date -u +%FT%TZ), jobs=$JOBS)"
conda run -n main python code/run_all.py --exp mbo --seeds 30 --jobs "$JOBS" \
  2>&1 | tee cloud/queue/logs/01_synth_unmatched.log

echo "[01] synthetic factorial — MATCHED-tuning (GATE-1: freeze GP per-run HPO)"
conda run -n main python code/run_all.py --exp mbo --seeds 30 --jobs "$JOBS" --matched-tuning \
  2>&1 | tee cloud/queue/logs/01_synth_matched.log

echo "[01] done -> results/results_camera.json + results/results_camera_matched.json"
