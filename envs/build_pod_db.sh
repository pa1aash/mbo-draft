#!/usr/bin/env bash
# Phase 4: build the working Design-Bench env `dbm` under our own conda root
# (/workspace/MBO/envs/miniforge). The shared /workspace/miniconda3 and
# /workspace/miniforge3 belong to other projects and are NOT touched.
#
# Key lesson from the first (failed) attempt: design-bench==2.0.20 declares
# tensorflow>=2.2 + deepchem + torchvision as hard deps, and tensorflow>=2.2 needs
# numpy>=1.24 while design-bench's own source needs numpy<1.24 (np.bool). Any
# dependency-resolving install therefore backtracks forever or bumps numpy and breaks
# the import. Likewise cloud/fix_designbench.sh installs botorch/gpytorch UNPINNED,
# which pulls numpy>=1.24 and breaks design-bench. So we reproduce the known-good
# macOS combo (envs/mac-db-requirements.lock) with --no-deps and pin botorch/gpytorch.
set -uo pipefail
export TMPDIR=/workspace/.tmp
export PIP_CACHE_DIR=/workspace/.pip-cache
export CONDA_PKGS_DIRS=/workspace/.conda-pkgs
mkdir -p "$TMPDIR" "$PIP_CACHE_DIR" "$CONDA_PKGS_DIRS"
cd /workspace/MBO
CROOT=/workspace/MBO/envs/miniforge
source "$CROOT/etc/profile.d/conda.sh"

ENV=dbm
if conda env list | grep -qE "/envs/${ENV}\b"; then
  echo "${ENV} env exists, skipping create"
else
  echo "=== create ${ENV} (py3.9 + rdkit) ==="
  conda create -y -n "$ENV" -c conda-forge python=3.9 rdkit
fi

echo "=== torch 2.8.0 CPU build (box is CPU-only) ==="
conda run -n "$ENV" pip install torch==2.8.0 --index-url https://download.pytorch.org/whl/cpu

echo "=== rest of the known-good lock, WITHOUT re-resolving deps ==="
grep -viE '^torch==' envs/mac-db-requirements.lock > "$TMPDIR/dblock.txt"
conda run -n "$ENV" pip install --no-deps -r "$TMPDIR/dblock.txt"

echo "=== source patches (deepchem-optional A/B + fixes #6/#7/#8) ==="
conda run -n "$ENV" python envs/pod-db-patches/apply_db_patches.py

echo "=== data (fix #5): community HF mirror; original hosting is dead ==="
DBD=$(conda run -n "$ENV" python -c 'import sysconfig,os;print(os.path.join(sysconfig.get_paths()["purelib"],"design_bench_data"))')
conda run -n "$ENV" hf download beckhamc/design_bench_data --repo-type dataset \
  --local-dir "$DBD" \
  --include 'tf_bind_8-SIX6_REF_R1/*' 'tf_bind_10-pho4/*' 'tf_bind_10-cbf1/*' \
            'superconductor/*' 'gfp/*' 'utr/*'

echo "=== verify 5 non-mujoco tasks ==="
conda run -n "$ENV" python code/db_tasks.py TFBind8 TFBind10 Superconductor GFP UTR

echo "=== freeze -> lock ==="
conda run -n "$ENV" pip freeze | grep -viE '^-e|pkg-resources' > envs/pod-db-torch28-requirements.lock
echo "POD_DB_BUILD_DONE (env=${ENV})"
