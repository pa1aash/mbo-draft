#!/usr/bin/env bash
# LOCAL run queue — remaining results producible from THIS machine (no design_bench/pod).
# Everything here is merge-safe + resumable: re-run after any crash, done cells are skipped.
# The only pod-dependent run is DB coverage (design_bench), handled separately.
#
#   bash cloud/local_queue.sh [SEEDS] [JOBS]      # defaults: 30 seeds, 1 job (serial)
#   bash cloud/local_queue.sh 30 8                # parallel (Windows uses spawn; resumable)
#
# jobs=1 (serial) is bulletproof everywhere. jobs>1 parallelises via spawn on Windows /
# fork on Linux; if a worker crashes, just re-run — completed cells persist and are skipped.
set -u
cd "$(dirname "$0")/.."
PY=${PY:-./venv/Scripts/python.exe}; [ -x "$PY" ] || PY=python
SEEDS=${1:-30}; JOBS=${2:-1}
say(){ echo "[$(date +%H:%M:%S)] $*"; }

# ── 1  DECISIVE SIM — beta=0 grid ────────────────────────────────────────────────────
# GP vs ensemble with the pessimism term OFF. If GP still wins -> its edge is posterior-
# mean smoothness / inductive bias, not sigma-calibration (critique #22 -> Section 5 must
# say so). Reuses run_all._worker; writes results_camera.json['mbo_beta0']. READY + smoked.
say "1  beta=0 grid  (seeds=$SEEDS jobs=$JOBS)"
MBO_SPAWN=1 "$PY" code/run_beta0.py --seeds "$SEEDS" --jobs "$JOBS"

# ── ON DECK — wired up on request (not written speculatively) ─────────────────────────
# 2  interaction eta2 (#1) + TOST equivalence (#5)   re-analysis, seconds, on the frozen
#      grid. stats.py already has tost(); analysis.py needs the interaction term added.
#      RUN AFTER the pod DB coverage is merged (else 05_findings mixes old/new regimes).
# 3  GP/SVGP own-proposal coverage (#2)              extend mbo.run_calibration
# 4  cross-proposal coverage (#3)                    extend mbo.run_calibration
# 5  score-biased-subsample control (#11)            matched-subsample grid variant
say "step 1 done. steps 2-5: say the word and I implement + queue them."
