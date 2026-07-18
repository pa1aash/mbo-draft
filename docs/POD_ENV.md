# Pod Design-Bench environment (Phase 4)

RunPod box: ubuntu-2404, 32 vCPU, CPU-only, 30 GB container disk, `/workspace` on a
large network volume. Conda root is our own miniforge at
`/workspace/MBO/envs/miniforge` (the shared `/workspace/miniconda3` and
`/workspace/miniforge3` belong to other projects and are not touched).

Working env name: **`dbm`** (`/workspace/MBO/envs/miniforge/envs/dbm`).
Use it via `conda run -n dbm ...`.

## 1. Build recipe that worked

The upstream `design-bench==2.0.20` metadata declares `tensorflow>=2.2`, `deepchem`,
and `torchvision` as hard runtime deps. `tensorflow>=2.2` transitively requires
`numpy>=1.24`, but design-bench's own source relies on numpy aliases that numpy later
removed (`np.NINF` etc.) and on scikit-learn 0.23-era pickles, so it needs the old
`numpy<1.24` / `scikit-learn==1.0.2` combo. As a result *any* dependency-resolving
`pip install design-bench==2.0.20` (verified: pip backtracks indefinitely trying to
satisfy `tensorflow>=2.2` against `numpy<1.24`), and any unpinned
`pip install botorch gpytorch ...`, bump numpy/sklearn and break design-bench at
task-build time. The fix is to reproduce the known-good macOS combo
(`envs/mac-db-requirements.lock`) with `--no-deps` so nothing re-resolves.

```bash
export TMPDIR=/workspace/.tmp PIP_CACHE_DIR=/workspace/.pip-cache CONDA_PKGS_DIRS=/workspace/.conda-pkgs
source /workspace/MBO/envs/miniforge/etc/profile.d/conda.sh
cd /workspace/MBO

# 1. Fresh env; rdkit from conda (design-bench needs it at import).
conda create -y -n dbm -c conda-forge python=3.9 rdkit

# 2. Torch CPU build first (box is CPU-only).
conda run -n dbm pip install torch==2.8.0 --index-url https://download.pytorch.org/whl/cpu

# 3. Everything else from the known-good macOS lock, WITHOUT re-resolving deps.
#    --no-deps is essential: the lock is a complete freeze, and letting pip resolve
#    design-bench's declared deps pulls tensorflow/deepchem/torchvision -> numpy>=1.24 -> breakage.
grep -viE '^torch==' envs/mac-db-requirements.lock > /workspace/.tmp/dblock.txt
conda run -n dbm pip install --no-deps -r /workspace/.tmp/dblock.txt

# 4. Source + data patches (see section 2). Applied by editing the installed package
#    files directly (the deepchem-optional patch must land before `import design_bench`
#    can succeed, because this env deliberately has no deepchem).
conda run -n dbm python envs/pod-db-patches/apply_db_patches.py   # patches A,B,#6,#7,#8

# 5. Data (fix #5): community HF mirror; original GCS/Drive hosting is dead.
DBD=/workspace/MBO/envs/miniforge/envs/dbm/lib/python3.9/site-packages/design_bench_data
conda run -n dbm hf download beckhamc/design_bench_data --repo-type dataset \
  --local-dir "$DBD" \
  --include 'tf_bind_8-SIX6_REF_R1/*' 'tf_bind_10-pho4/*' 'tf_bind_10-cbf1/*' \
            'superconductor/*' 'gfp/*' 'utr/*'

# 6. Verify.
conda run -n dbm python code/db_tasks.py TFBind8 TFBind10 Superconductor GFP UTR
```

Note: the first pod build attempt used `cloud/fix_designbench.sh`, whose steps 1-4
`pip install ... botorch gpytorch` **unpinned**, pulling latest botorch/gpytorch that
bump numpy/scikit-learn off the versions design-bench needs. That is why this build
pins botorch==0.10.0 / gpytorch==1.11 (via the mac lock) and never runs those steps.

## 2. Audit of the 8 `cloud/fix_designbench.sh` fixes (ubuntu-2404 / py3.9, 2026)

The macOS port `envs/mac-db-patches/fix_designbench_macos.py` was the reference for the
source patches. On this pod the source patches are applied by a path-based script
(`apply_db_patches.py`) rather than by importing design_bench, because with no deepchem
installed `import design_bench` fails until the deepchem-optional patch is in place.

| # | Fix in fix_designbench.sh | Still needed in 2026? | Notes |
|---|---------------------------|-----------------------|-------|
| 1 | Pin `scikit-learn==1.0.2`, `gym==0.23.1` | NEEDED | design-bench's old RF pickle + gym API. Supplied by the mac lock, not by the script's own `pip install`. |
| 2 | `pip install botorch gpytorch cma` **unpinned** | HARMFUL / must be pinned | This is the step that broke the first attempt: unpinned botorch/gpytorch pull numpy>=1.24 and break design-bench. Replaced by pinned botorch==0.10.0 / gpytorch==1.11 / cma==4.4.4 from the mac lock. |
| 3 | `pip uninstall tensorflow keras` | NOT NEEDED here | We never install tensorflow (mac lock has none; `--no-deps` keeps it out). design-bench's TF oracles are import-guarded ("Skipped loading some Tensorflow models"). |
| 4 | `pip install numpy==1.23.5` LAST | NEEDED (as a pin) | numpy 1.23.5 is required for `np.bool`. Provided by the mac lock; no "install last" ordering needed because `--no-deps` never bumps it. |
| 5 | HF-mirror data download (`beckhamc/design_bench_data`) | NEEDED | Original GCS bucket + Google Drive hosting are dead. Extended the `--include` patterns beyond the script's tf_bind_8/tf_bind_10/superconductor to also cover `gfp/*` and `utr/*` (Phase 5 needs GFP+UTR). |
| 6 | Write `smiles_vocab.txt` | NEEDED | ChEMBL SMILES tokenizer is constructed at `design_bench.__init__` import even though ChEMBL is unused; without the vocab file the import raises. |
| 7 | Make `oracles/exact/__init__.py` optional-import | NEEDED | Upstream hard-imports every exact oracle (gym/mujoco/nasbench); headless box has no mujoco, so the eager import must be wrapped in try/except. |
| 8 | `np.loads` -> `pickle.loads` | NEEDED | `np.loads` was removed from modern numpy; approximate_oracle.py still calls it. Patched in 1 file. |
| A | (macOS extra) deepchem import optional | NEEDED here | This env has no deepchem (avoids the tensorflow chain). `morgan_fingerprint_features.py` hard-imports deepchem at module load; made optional so `import design_bench` succeeds. |
| B | (macOS extra) guard MorganFingerprint `__init__` | NEEDED here | Same reason as A: when deepchem is absent the featurizer/tokenizer are set to None and `__init__` returns early. |

## 3. Key finding: fix_designbench.sh's unpinned botorch/gpytorch is broken in 2026

`cloud/fix_designbench.sh` line 22 runs `pip install -q 'scikit-learn==1.0.2'
'gym==0.23.1' botorch gpytorch cma ...` with botorch/gpytorch **unpinned**. On a fresh
2026 install the modern botorch/gpytorch pull a numpy>=1.24 / scikit-learn>=1.x stack.
The script then tries to re-pin numpy==1.23.5 "last", but modern botorch expects the
newer numpy, while design-bench needs the old numpy and needs scikit-learn 1.0.2 to
unpickle its RandomForest oracles. The constraints are mutually exclusive. Empirically
(see the `dbm2` experiment, section 6) the unpinned install does not even converge, and
the partial result it produced already carried numpy 2.0.2 + scikit-learn 1.6.1 — both
design-bench-incompatible. botorch/gpytorch **must be pinned** (0.10.0 / 1.11), which is
what the mac lock does. Recommendation: patch fix_designbench.sh to pin these, or install
from `envs/pod-db-torch28-requirements.lock` and skip steps 1-4 of the script entirely.

## 4. Final versions (env `dbm`)

| package | version |
|---------|---------|
| python | 3.9 |
| torch | 2.8.0+cpu |
| numpy | 1.23.5 |
| scipy | 1.13.1 |
| scikit-learn | 1.0.2 |
| botorch | 0.10.0 |
| gpytorch | 1.11 |
| linear-operator | 0.5.1 |
| design-bench | 2.0.20 |
| gym | 0.23.1 |
| rdkit | 2025.03.5 (conda-forge) |

No tensorflow, no deepchem, no torchvision (deliberately excluded; not needed for the
RF/exact-oracle task set used by `code/db_tasks.py`).

## 5. Tasks verified

`conda run -n dbm python code/db_tasks.py TFBind8 TFBind10 Superconductor GFP UTR`
exits 0 with all five printing a `dim=` line and finite oracle scores (no traceback):

| task | design_bench id | dim | N | discrete |
|------|-----------------|-----|---|----------|
| TFBind8 | TFBind8-Exact-v0 | 32 | 32,898 | yes |
| TFBind10 | TFBind10-Exact-v0 | 40 | 4,161,482 | yes |
| Superconductor | Superconductor-RandomForest-v0 | 86 | 17,014 | no |
| GFP | GFP-RandomForest-v0 | 4,740 | 5,000 | yes |
| UTR | UTR-RandomForest-v0 | 200 | 140,000 | yes |

All 5 non-mujoco Phase-5 tasks: **VERIFIED**. (Mujoco Ant/DKitty not attempted; not
required for Phase 5.) The RandomForest oracles emit a benign sklearn
"unpickle estimator from version 0.23.1 when using 1.0.2" UserWarning and design-bench
emits a benign `np.bool` DeprecationWarning under numpy 1.23.5 — neither is an error.

## 6. Second env with latest torch (pod-db-requirements.lock)

A second env `dbm2` was built to test whether design-bench 2.0.20 can run on the
**latest** torch (unpinned). Empirical findings:

1. **"Latest torch" on Python 3.9 collapses to torch 2.8.0.** design-bench 2.0.20 is a
   py3.9-era package (its numpy<1.24 / sklearn-1.0.2 / gym-0.23.1 pins are not
   satisfiable on py3.10+ in a way that keeps design-bench importable). On Python 3.9,
   `pip install torch --index-url .../whl/cpu` (unpinned) resolves to **torch 2.8.0+cpu**:
   torch stopped publishing cp39 wheels after 2.8, so there is no newer torch available.
   The primary `dbm` (torch 2.8.0) env therefore already *is* the latest-torch build for
   this Python; there is no distinct "newer torch" to lock.

2. **The unpinned surrounding stack does not resolve/work.** Mimicking
   `cloud/fix_designbench.sh`'s unpinned `pip install ... botorch gpytorch ...`, the
   command `pip install numpy scipy scikit-learn pandas transformers ... gym==0.23.1
   botorch gpytorch cma pyro-ppl` backtracked for 15+ minutes without converging (the
   old `gym==0.23.1` against latest everything is a hard constraint set). The packages it
   did place before being stopped were already design-bench-incompatible:
   **numpy 2.0.2** (gym 0.23.1 explicitly does not support NumPy 2.0) and
   **scikit-learn 1.6.1** (cannot unpickle design-bench's RandomForest oracles, which are
   pickled with sklearn 0.23.1 and require sklearn 1.0.2 to load). botorch never finished
   resolving. (Note: numpy 2.0 re-introduced `np.bool`, so that specific break does not
   apply under 2.0.2 — but np.NINF and other removed aliases, the sklearn pickle, and the
   gym/NumPy-2.0 incompatibility all still make the latest stack unusable.)

**Conclusion: latest-torch is not a meaningful separate build for design-bench 2.0.20 on
this platform.** It reduces to torch 2.8.0, and the rest of the stack must be pinned to
the known-good versions regardless. Accordingly `envs/pod-db-requirements.lock` is a copy
of `envs/pod-db-torch28-requirements.lock` with this note in its header. The `dbm2` test
env was removed after the experiment.
