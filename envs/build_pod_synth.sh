#!/usr/bin/env bash
# Build the pod synthetic environment under /workspace/MBO/envs/pod-synth.
# CPU torch (DEVICE=cpu in mbo.py). Caches on the network volume, not container disk.
set -euo pipefail
export PIP_CACHE_DIR=/workspace/.pip-cache
export TMPDIR=/workspace/.tmp
mkdir -p "$PIP_CACHE_DIR" "$TMPDIR"
cd /workspace/MBO
python3 -m venv envs/pod-synth
source envs/pod-synth/bin/activate
python -m pip install --upgrade pip setuptools wheel
# torch pinned (controlled variable), CPU build
pip install torch==2.11.0 --index-url https://download.pytorch.org/whl/cpu
# rest from PyPI, versions per requirements.txt
pip install numpy==2.4.4 scipy==1.17.1 scikit-learn==1.8.0 matplotlib==3.10.8 botorch gpytorch cma
echo "BUILD_OK"
python - <<'PY'
import torch, numpy, sklearn, botorch, gpytorch, cma, scipy
print("VERIFY torch", torch.__version__, "numpy", numpy.__version__,
      "sklearn", sklearn.__version__, "scipy", scipy.__version__,
      "botorch", botorch.__version__, "gpytorch", gpytorch.__version__,
      "cma", cma.__version__)
PY
