#!/usr/bin/env bash
# 0C driver: the four engine corners x three budget levels on the full 7-task DB grid.
# Each invocation of db_budget_matched.py runs all three levels off one surrogate fit and
# merges into that corner's per-level files by task key.
#
# TFBind10 gets its own low-concurrency pass: its 4^10 landscape build is hostile to a wide
# fork pool (db_tasks.py:24-26). GFP is left in the main pass -- it is slow but stable.
set -u
cd "$(dirname "$0")"
PY=/workspace/MBO/envs/miniforge/envs/dbm/bin/python
LOG=/workspace/MBO/logs
SEEDS=${SEEDS:-16}
JOBS=${JOBS:-16}
JOBS_TF10=${JOBS_TF10:-4}

echo "###### 0C START $(date) seeds=$SEEDS jobs=$JOBS ######"
for corner in off_off on_off off_on on_on; do
  for pass in "main:TFBind8,Superconductor,GFP,UTR:$JOBS" \
              "tf10:TFBind10:$JOBS_TF10" \
              "mujoco::$JOBS"; do
    name="${pass%%:*}"; rest="${pass#*:}"; tasks="${rest%%:*}"; jobs="${rest##*:}"
    args="--corner $corner --seeds $SEEDS --jobs $jobs"
    [ -n "$tasks" ] && args="$args --tasks $tasks"
    [ "$name" = "mujoco" ] && args="$args --mujoco"
    echo "=== [$(date +%H:%M:%S)] $corner / $name (jobs=$jobs) ==="
    $PY -u db_budget_matched.py $args > "$LOG/db_budget_${corner}_${name}.log" 2>&1
    rc=$?
    if [ $rc -ne 0 ]; then
      echo "!!! FAILED $corner/$name rc=$rc — see $LOG/db_budget_${corner}_${name}.log"
      grep -viE "UserWarning|warnings.warn|scikit|np.bool|Deprecat|^\s*$" \
        "$LOG/db_budget_${corner}_${name}.log" | tail -15
    else
      grep -E "^wrote" "$LOG/db_budget_${corner}_${name}.log"
    fi
  done
done
echo "###### 0C ALL CORNERS DONE $(date) ######"
