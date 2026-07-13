#!/usr/bin/env bash
# Run the whole queue in dependency order: 00 -> 01 -> [GATE-1 verdict] -> 02 -> 03 -> 04 -> 05.
# Each step is resumable, so a killed spot instance can just re-run this. Set STOP_AFTER=NN
# to halt after a step (e.g. STOP_AFTER=01 to run only the gate before committing real compute).
set -u
cd "$(dirname "$0")" || exit 1
STOP_AFTER=${STOP_AFTER:-05}
step(){ echo; echo "############### STEP $1 ###############"; bash "$1"_*.sh || { echo "STEP $1 FAILED"; exit 1; }; [ "$STOP_AFTER" = "$1" ] && { echo "STOP_AFTER=$1 reached."; exit 0; } || true; }

step 00
step 01

echo; echo "########## GATE-1 VERDICT (synthetic) ##########"
cd ../.. && conda run -n main python code/analysis.py \
  --gate results/results_camera.json results/results_camera_matched.json 2>&1 | tee cloud/queue/logs/gate1.log
cd cloud/queue
echo "^ If SURVIVES: proceed. If NOT: the headline reframes to a tuning-budget artifact"
echo "  (still publishable; 02 still runs). Ctrl-C now to pause and decide."
[ "$STOP_AFTER" = "01" ] && exit 0 || true

step 02
step 03
step 04
step 05
echo; echo "ALL STEPS DONE. Results in results/, analysis in cloud/queue/logs/05_analyze.log."
