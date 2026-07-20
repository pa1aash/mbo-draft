#!/usr/bin/env bash
# Regenerate the supplement's tab:sfull and tab:cov source data on the stamped
# X1-off/X3-off (uncorrected) engine. See docs/SUPP_ENGINE_FIX.md.
set -euo pipefail
cd "$(dirname "$0")"
PY=/workspace/MBO/envs/pod-synth/bin/python
OUT=../results/supp_offoff
mkdir -p "$OUT"

export MBO_X1=0 MBO_X3=0

TASKS="Branin-2D Styblinski-5D Levy-8D Rosenbrock-10D Rastrigin-15D Ackley-20D Griewank-30D"

echo "=== [1/2] tab:sfull grid: 9 grid cells + 3 domain baselines, 30 seeds, off_off ==="
$PY run_all.py --exp mbo --tasks $TASKS --seeds 30 --jobs 30 \
  --methods ens:grad ens:perturb ens:cma \
            botorchgp:grad botorchgp:perturb botorchgp:cma \
            svgp:grad svgp:perturb svgp:cma \
            coms cbas grad_ascent \
  --out "$OUT/grid_offoff_b2.0.json"

echo "=== [2/2] tab:cov synthetic calibration, 30 seeds, off_off ==="
$PY run_all.py --exp calibration --tasks $TASKS --seeds 30 --jobs 30 \
  --out "$OUT/calibration_off_off.json"

echo "=== DONE ==="
