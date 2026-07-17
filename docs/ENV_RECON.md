# Environment reconnaissance — building macOS envs (synthetic + Design-Bench)

Recon done 2026-07-18 BEFORE installing anything. Every later decision depends on the
arm64/Intel split recorded in §1.

## 1.1 The machine
- **Architecture: `arm64` (Apple Silicon).** This is load-bearing: mujoco-py and TF1-era
  wheels do not exist for arm64; every "hard" item below traces to this line.
- macOS **26.3.1** (build 25D771280a).
- Xcode Command Line Tools: present (`/Library/Developer/CommandLineTools`).
- Homebrew: present (`/opt/homebrew/bin/brew`, 6.0.9).
- Pythons available:
  - `/usr/bin/python3` → **3.9.6** (system) — the version design-bench wants (py3.9).
  - `/Library/Frameworks/Python.framework/Versions/3.13/bin/python3` → 3.13.7.
  - `/Library/Frameworks/…/3.14/…` → 3.14.2.
  - `/opt/homebrew/Caskroom/miniforge/base/bin/python` → 3.13.12 (**DO NOT install here** —
    pinned to numpy 2.4.4 for other projects).

## 1.2 The cloud recipe and the 8 Design-Bench fixes (portability to macOS)
`cloud/setup.sh` builds THREE conda envs on Linux: `main` (py3.11, synthetic grid via
`requirements.txt`), `db` (py3.9, design-bench 2.0.20 + `numpy<2` + old sklearn), `baselines`
(py3.7, official design-baselines — TF1-era, "expected to fail on modern boxes").
`cloud/fix_designbench.sh` applies 8 fixes to make design-bench 2.0.20 work in 2026:

| # | Fix | What/why | Portable to macOS? |
|---|---|---|---|
| 1 | `scikit-learn==1.0.2` | old RF-oracle pickle needs sklearn<1.4 | **Portable** (arm64/py3.9 wheel exists) |
| 2 | `gym==0.23.1` | exact-oracle Hopper import needs gym | **Portable** (pure-python) |
| 3 | remove `tensorflow`/`keras` | unused + version conflicts | **Portable** (uninstall step) |
| 4 | `numpy==1.23.5` (installed LAST so it wins) | `np.NINF`/`np.bool` removed in numpy≥1.24/2.0 | **Portable** (arm64/py3.9 wheel exists) |
| 5 | HF-mirror data download (`hf download beckhamc/design_bench_data`) | original GCS/Drive hosting is dead | **Portable IF mirror live** — verify in Phase 3. **Gap:** the cloud `--include` pulls only `tf_bind_8*`, `tf_bind_10*`, `superconductor*`. **GFP + UTR must be added** to reach the blueprint's Stage-2 (5 tasks). |
| 6 | seed `smiles_vocab.txt` | ChEMBL tokenizer needs a vocab at import (even unused) | **Portable** (writes a file) |
| 7 | patch `oracles/exact/__init__.py` → optional oracle imports | upstream hard-imports gym/mujoco/nasbench; breaks headless | **Portable** (done in python, not sed) |
| 8 | `np.loads` → `pickle.loads` in `approximate_oracle.py` | `np.loads` removed | **NOT portable as-is** — uses GNU `sed -i`; macOS BSD sed needs `sed -i ''`. Will reimplement in python for portability. |

Additional (mujoco / Stage 3): `design-bench[all]`, `morphing-agents==1.5.1`, `mujoco==2.3.7`.
`morphing-agents` historically depends on `mujoco-py` (**dead on arm64**); the modern DeepMind
`mujoco` package has arm64 wheels but morphing-agents may not use it. This is the Stage-3 risk.

## 1.3 The untouchable `venv/` (READ ONLY — collaborator's Windows env)
`venv/pyvenv.cfg`: `home = C:\Users\arjun\anaconda3`, `version = 3.13.9`, created under
`C:\Users\arjun\Downloads\…\NeurIPS MBO\MBO\venv`. **This is a Windows venv belonging to
collaborator "arjun"** — Windows layout (`Include/ Lib/ Scripts/`), not runnable on macOS.
Pinned versions (from `Lib/site-packages/*.dist-info`): **torch 2.11.0, numpy 2.4.4,
scikit-learn 1.8.0, scipy 1.17.1, botorch 0.18.1, gpytorch 1.15.2, cma 4.4.4** — these match
`requirements.txt` and are the environment the published synthetic numbers came from.
**Baseline fingerprint locked for the untouched-check: 29735 files, 957776 KB, pyvenv mtime
1783713294.** Not touched, not installed into, not moved.

## 1.4 Why two envs are mandatory (confirmed from code, not assumed)
- **Synthetic grid** (`requirements.txt`, `venv/` pins): **numpy 2.4.4**, scikit-learn 1.8.0,
  torch 2.11. `code/mbo.py` uses modern numpy/sklearn/botorch APIs.
- **Design-Bench** (`fix_designbench.sh`): **numpy 1.23.5** (design-bench calls `np.NINF` and
  `np.bool`, both removed in numpy 2.0) and **scikit-learn 1.0.2** (the RF-oracle pickles were
  written by sklearn<1.4 and fail to unpickle on ≥1.4).
- **numpy 2.4.4 vs numpy 1.23.5 cannot coexist in one interpreter.** Confirmed from the actual
  pins in both files — not an assumption. Hence `envs/mac-synth` (numpy 2) and `envs/mac-db`
  (numpy 1.23.5) are separate, exactly as the cloud builds `main` vs `db`.

## 1.5 Per-DB-task dependency map (`code/db_tasks.py`)
`db_tasks.py` deliberately picks oracles that minimize simulator deps:
| task | oracle variant | mujoco? | TF? | data source | Stage |
|---|---|---|---|---|---|
| TFBind8 | `TFBind8-Exact-v0` | no | no | HF mirror `tf_bind_8-SIX6_REF_R1` | 2 |
| TFBind10 | `TFBind10-Exact-v0` | no | no | HF mirror `tf_bind_10-*` | 2 |
| Superconductor | `Superconductor-RandomForest-v0` | no | no | HF mirror `superconductor` | 2 |
| GFP | `GFP-RandomForest-v0` | no | **RF, not TF** | HF mirror `gfp-*` (must add to download) | 2 |
| UTR | `UTR-RandomForest-v0` | no | **RF, not TF** | HF mirror `utr-*` (must add to download) | 2 |
| AntMorphology | `AntMorphology-RandomForest-v0` | **RF oracle avoids mujoco at EVAL, but the morphology design space imports morphing-agents→mujoco at IMPORT** | no | mirror | 3 |
| DKitty | `DKittyMorphology-RandomForest-v0` | same as Ant | no | mirror | 3 |
| Hopper | `HopperController-RandomForest-v0` | same | no | mirror | 3 |

**Key point (as db_tasks.py's own comment states):** the RandomForest-oracle substitution
removes the mujoco/TF requirement at **evaluation** for Ant/DKitty/Hopper — but the morphology
**task/design-space** still imports `morphing-agents` (→ mujoco) at **import** time. So Stage 3's
mujoco pain is unavoidable for those three; Stage 2 (5 tasks, including both exact-oracle tasks
X11 needs) has no mujoco/TF dependency at all and is the realistic macOS target.

## Plan that follows from this recon
- `envs/mac-synth`: promote the working scratchpad recipe; pin to `requirements.txt`/`venv`
  versions where arm64 wheels allow (torch 2.11 → fall back to 2.13, already reproduction-verified).
- `envs/mac-db`: **py3.9** (system 3.9.6 or a fresh 3.9 venv), design-bench 2.0.20, numpy 1.23.5,
  sklearn 1.0.2; port fixes 1–8 (rewriting #8 in python, extending #5 to GFP/UTR). Target Stage 2;
  Stage 3 (mujoco) best-effort, recommend cloud pod if arm64 defeats it.
