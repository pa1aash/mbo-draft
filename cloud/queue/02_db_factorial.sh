#!/usr/bin/env bash
# 02 — real Design-Bench crossed factorial: the 4-task core (TFBind8/10, Ant, DKitty)
# + Superconductor. Unmatched + matched. Needs the `db` env + mujoco (Ant/DKitty).
# Its transfer claim is only meaningful after 01. Resumable. -> results_db*.json
set -u
cd "$(dirname "$0")/../.." || exit 1
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
mkdir -p cloud/queue/logs
JOBS=${JOBS:-32}        # DB tasks are memory-heavier than synthetic; cap to avoid OOM
TASKS="TFBind8 TFBind10 Superconductor AntMorphology DKitty"

if [ ! -f results/results_camera.json ]; then
  echo "[02] WARNING: results_camera.json (from 01) missing — the synthetic->real transfer"
  echo "     analysis in 05 needs it. Real runs will still produce valid real-task data."
fi

echo "[02] real DB factorial — UNMATCHED  ($(date -u +%FT%TZ), jobs=$JOBS)"
echo "     tasks: $TASKS   (Ant/DKitty need mujoco; they fail-soft if headless mujoco is unavailable)"
conda run -n db python code/run_all.py --exp mbo --db --tasks $TASKS --seeds 16 --jobs "$JOBS" \
  2>&1 | tee cloud/queue/logs/02_db_unmatched.log

echo "[02] real DB factorial — MATCHED-tuning"
conda run -n db python code/run_all.py --exp mbo --db --tasks $TASKS --seeds 16 --jobs "$JOBS" --matched-tuning \
  2>&1 | tee cloud/queue/logs/02_db_matched.log

echo "[02] done -> results/results_db.json + results/results_db_matched.json"
