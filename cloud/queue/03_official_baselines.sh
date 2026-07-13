#!/usr/bin/env bash
# 03 — OFFICIAL baselines (COMs, CbAS, MINs, ...) via the design-baselines repo, so the
# paper compares against the authors' implementations, not ours. Independent `baselines`
# env (TF1-era; brittle on modern boxes). BEST-EFFORT with an explicit fallback.
# Design-Bench task IDs match code/db_tasks.py:TASKS.
set -u
cd "$(dirname "$0")/../.." || exit 1
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
mkdir -p cloud/queue/logs results/official
LOG=cloud/queue/logs/03_official_baselines.log
: > "$LOG"
CORE_IDS="TFBind8-Exact-v0 TFBind10-Exact-v0 Superconductor-RandomForest-v0 AntMorphology-Exact-v0 DKittyMorphology-Exact-v0"

if ! conda env list | grep -qE '^\s*baselines\s'; then
  echo "[03] baselines env absent. Build it: bash cloud/setup.sh (best-effort TF1 env)." | tee -a "$LOG"
  echo "[03] FALLBACK: cite published COMs/CbAS numbers + ROOT (NeurIPS'25) Table 1 for the" | tee -a "$LOG"
  echo "     modern diffusion baselines. The paper's plan already sanctions citing ROOT." | tee -a "$LOG"
  exit 0
fi

# The design-baselines console entrypoint differs by commit; discover it, don't guess.
CLI=$(conda run -n baselines bash -lc 'command -v design-baselines || true')
echo "[03] design-baselines CLI: ${CLI:-<not found>}" | tee -a "$LOG"

if [ -z "$CLI" ]; then
  echo "[03] CLI not found. On the pod, inspect: conda run -n baselines design-baselines --help" | tee -a "$LOG"
  echo "     then fill the COMs/CbAS invocations below. FALLBACK for now: published + ROOT numbers." | tee -a "$LOG"
  exit 0
fi

# TEMPLATE (verify flags against `design-baselines --help` on the pod before trusting):
#   for each method in {coms-original, cbas} and each task id, run and collect the score json.
for METHOD in coms-original cbas; do
  for TID in $CORE_IDS; do
    OUT="results/official/${METHOD}__${TID}"
    echo "[03] $METHOD on $TID -> $OUT" | tee -a "$LOG"
    conda run -n baselines design-baselines "$METHOD" --local-dir "$OUT" --task "$TID" \
      >>"$LOG" 2>&1 || echo "  ($METHOD/$TID failed — TF1 env is brittle; fall back to published)" | tee -a "$LOG"
  done
done
echo "[03] done (best-effort). Merge official scores into the tables in 05, or cite published." | tee -a "$LOG"
