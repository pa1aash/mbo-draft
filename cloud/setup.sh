#!/usr/bin/env bash
# Provision the three conda envs on a fresh Linux box. Idempotent + fail-soft:
# each env builds independently, a failure in one is logged and does not abort the
# others. Run from the repo root:  bash cloud/setup.sh
set -u
LOG="cloud/setup.log"; : > "$LOG"
say(){ echo "[$(date -u +%H:%M:%S)] $*" | tee -a "$LOG"; }
have(){ conda env list | grep -qE "^\s*$1\s"; }

# Bootstrap miniconda if absent (bare RunPod/cloud containers have no conda).
if ! command -v conda >/dev/null; then
  say "conda not found — bootstrapping miniconda to \$HOME/miniconda3…"
  curl -fsSL https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -o /tmp/mc.sh \
    && bash /tmp/mc.sh -b -p "$HOME/miniconda3" >>"$LOG" 2>&1 \
    && say "miniconda installed" || { say "miniconda bootstrap FAILED — see $LOG"; exit 1; }
  export PATH="$HOME/miniconda3/bin:$PATH"
fi
source "$(conda info --base)/etc/profile.d/conda.sh"

# Accept channel ToS (newer conda refuses `conda create` otherwise; harmless if already accepted).
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main >>"$LOG" 2>&1 || true
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r    >>"$LOG" 2>&1 || true

# mujoco system deps for Design-Bench Ant/D'Kitty (best-effort; non-mujoco tasks don't need them).
# Package names vary by Ubuntu; try modern then legacy, don't fail the run either way.
if command -v apt-get >/dev/null; then
  say "installing mujoco system deps (best-effort)…"
  apt-get update >>"$LOG" 2>&1 || true
  (apt-get install -y --no-install-recommends libgl1 libglx-mesa0 libosmesa6 patchelf libglew-dev >>"$LOG" 2>&1 \
     || apt-get install -y --no-install-recommends libgl1-mesa-glx libosmesa6 patchelf libglew-dev >>"$LOG" 2>&1) \
    && say "mujoco system deps OK" || say "mujoco system deps skipped — non-mujoco DB tasks still fine"
fi

# --- main: our engine (E1/E4/E5/E6/E8, synthetic + Design-Bench via torch) ------
if have main; then say "main exists, skipping"; else
  say "building main (py3.11)…"
  conda create -y -n main python=3.11 >>"$LOG" 2>&1 \
    && conda run -n main pip install -r requirements.txt >>"$LOG" 2>&1 \
    && conda run -n main python code/mbo.py >>"$LOG" 2>&1 \
    && say "main OK (mbo.py smoke passed — gp_grad/svgp/cma cells now live)" \
    || say "main FAILED — see $LOG"
fi

# --- db: Design-Bench (E2). py3.9; minimal first, then [all]+mujoco best-effort ---
if have db; then say "db exists, skipping"; else
  say "building db (py3.9, design-bench)…"
  conda create -y -n db -c conda-forge python=3.9 rdkit >>"$LOG" 2>&1 \
    && conda run -n db pip install design-bench==2.0.20 torch numpy scipy scikit-learn >>"$LOG" 2>&1 \
    && say "db core OK — trying mujoco tasks (Ant/DKitty; may fail on headless boxes)" \
    && ( conda run -n db pip install "design-bench[all]==2.0.20" morphing-agents==1.5.1 mujoco==2.3.7 >>"$LOG" 2>&1 \
         && say "db[all] OK — morphology tasks available" \
         || say "db[all] FAILED — non-mujoco tasks (TFBind8/10, Superconductor, ChEMBL, GFP, UTR) still usable" ) \
    || say "db FAILED — see $LOG"
  # verify whatever installed
  conda run -n db python code/db_tasks.py TFBind8 Superconductor >>"$LOG" 2>&1 \
    && say "db verify OK (TFBind8 + Superconductor instantiate + oracle-evaluate)" \
    || say "db verify FAILED — check $LOG"
fi

# --- baselines: official design-baselines repo (E3). Hardest; its own TF1-era env ---
if have baselines; then say "baselines exists, skipping"; else
  say "building baselines (design-baselines repo, best-effort)…"
  if [ ! -d cloud/design-baselines ]; then
    git clone https://github.com/brandontrabucco/design-baselines cloud/design-baselines >>"$LOG" 2>&1
  fi
  conda create -y -n baselines python=3.7 >>"$LOG" 2>&1 \
    && conda run -n baselines pip install -e cloud/design-baselines >>"$LOG" 2>&1 \
    && say "baselines OK" \
    || say "baselines FAILED (expected on modern boxes) — fall back to official COMs+CbAS numbers or published tables; see $LOG"
fi

say "done. envs:"; conda env list | tee -a "$LOG"
say "next: conda run -n main python code/run_all.py --exp all --seeds 30 --jobs \$(nproc)"
