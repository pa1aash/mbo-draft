#!/usr/bin/env bash
# 05 — analysis + statistics + figures. NO GPU. Re-run this anytime after any sim lands
# to see the current picture. Consumes 01-04. Everything here is deterministic post-hoc.
set -u
cd "$(dirname "$0")/../.." || exit 1
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
mkdir -p cloud/queue/logs
LOG=cloud/queue/logs/05_analyze.log; : > "$LOG"
R=results
run(){ echo "== $* =="; conda run -n main python "$@" 2>&1; }

{
  # --- attribution: SEI/OEI + fixed-optimizer gap collapse ---
  run code/analysis.py --results $R/results_camera.json
  [ -f $R/results_db.json ] && run code/analysis.py --results $R/results_db.json

  # --- GATE-1: does the surrogate effect survive matched tuning? ---
  [ -f $R/results_camera_matched.json ] && run code/analysis.py --gate $R/results_camera.json $R/results_camera_matched.json
  [ -f $R/results_db_matched.json ]     && run code/analysis.py --gate $R/results_db.json     $R/results_db_matched.json

  # --- synthetic -> real transfer ---
  [ -f $R/results_db.json ] && run code/analysis.py --transfer $R/results_camera.json $R/results_db.json

  # --- statistics: Wilcoxon+Holm, CD diagram, TOST for the beta=0 ties ---
  [ -f $R/results_db.json ] && run code/stats.py --results $R/results_db.json --ref ens:grad
  [ -f $R/results_db.json ] && run code/stats.py --results $R/results_db.json --cd
  [ -f $R/results_db.json ] && run code/stats.py --results $R/results_db.json --tost grad_ascent ens:grad

  # --- figures (best-effort; may need results-schema updates) ---
  run code/figures.py || echo "(figures.py skipped/failed — non-fatal)"
} | tee "$LOG"
echo "[05] done -> $LOG"
