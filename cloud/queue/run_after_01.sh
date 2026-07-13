#!/usr/bin/env bash
# Launch 02, 03, 04 CONCURRENTLY after 01 has finished. Safe because: they have no data
# dependency on each other (02 only feeds 05's transfer analysis), and they write DIFFERENT
# result files, so no clobbering. The only limit is CPU/RAM -- don't oversubscribe the cores
# (the load-320-on-112 slowdown we hit before). 02 is heavy + memory-bound (OOM'd above ~32
# jobs) so it keeps the safe cap; 04 is light; 03 is a different (TF) env that self-throttles.
set -u
cd "$(dirname "$0")/../.." || exit 1
mkdir -p cloud/queue/logs
CORES=$( (nproc 2>/dev/null) || echo 16 )
J02=$(( CORES > 36 ? 32 : CORES - 4 )); [ "$J02" -lt 1 ] && J02=1
J04=$(( CORES > 40 ? 8 : 4 ))

if [ ! -f results/results_camera.json ]; then
  echo "results_camera.json (from 01) missing — run 01 first. Aborting."; exit 1
fi
if [ "$CORES" -lt 24 ]; then
  echo "NOTE: only $CORES cores. Concurrent 02+03+04 will oversubscribe; prefer serial:"
  echo "  bash cloud/queue/02_db_factorial.sh && bash cloud/queue/04_calibration.sh && bash cloud/queue/03_official_baselines.sh"
fi
echo "cores=$CORES  ->  02 jobs=$J02 (memory-capped), 04 jobs=$J04, 03 in its own env"

JOBS=$J02 bash cloud/queue/02_db_factorial.sh     > cloud/queue/logs/02.par.log 2>&1 &  P02=$!
JOBS=$J04 bash cloud/queue/04_calibration.sh      > cloud/queue/logs/04.par.log 2>&1 &  P04=$!
          bash cloud/queue/03_official_baselines.sh > cloud/queue/logs/03.par.log 2>&1 &  P03=$!
echo "launched: 02(pid $P02) 04(pid $P04) 03(pid $P03)"
echo "watch:  tail -f cloud/queue/logs/0{2,3,4}.par.log"
wait $P02 $P04 $P03
echo "02/03/04 all done. Next: bash cloud/queue/05_analyze.sh"
