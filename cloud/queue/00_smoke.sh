#!/usr/bin/env bash
# 00 — sanity gate (~2 min). Verify the env + code self-checks BEFORE burning compute.
set -u
cd "$(dirname "$0")/../.." || exit 1
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
mkdir -p cloud/queue/logs
echo "[00] engine self-checks (analysis + stats)"
conda run -n main python code/analysis.py --results results/results_camera.json >/dev/null 2>&1 \
  && echo "  analysis.py OK" || echo "  analysis.py FAILED (results may be absent — fine pre-run)"
conda run -n main python -c "import stats" 2>/dev/null && echo "  stats import OK" || true
echo "[00] 2-minute smoke run on Branin"
conda run -n main python code/run_all.py --smoke 2>&1 | tee cloud/queue/logs/00_smoke.log | tail -3
echo "[00] done. If green, start 01."
