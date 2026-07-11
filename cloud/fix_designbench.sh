#!/usr/bin/env bash
# Make Design-Bench 2.0.20 actually work in 2026. The upstream data hosting is DEAD
# (GCS bucket deleted, Google Drive dead) and the package predates modern numpy/sklearn.
# This applies the 8 fixes that get TFBind8 (d=32), TFBind10 (d=40), Superconductor
# (d=86) instantiating + oracle-evaluating. Idempotent. Run inside the `db` env's repo:
#   conda run -n db bash cloud/fix_designbench.sh
set -u
run(){ python -c "$1"; }
SP=$(python -c 'import design_bench,os;print(os.path.dirname(design_bench.__file__))')
DBD=$(python -c 'import design_bench_data,os;print(os.path.dirname(design_bench_data.__file__))')
echo "design_bench=$SP"; echo "design_bench_data=$DBD"

# 1-4: version pins design-bench needs (np.NINF/np.bool -> numpy<1.24; old RF pickle ->
# sklearn<1.4; exact-oracle Hopper import -> gym; TF unused + conflicts -> remove).
pip install -q 'numpy==1.23.5' 'scikit-learn==1.0.2' 'gym==0.23.1' huggingface_hub 2>&1 | tail -1 || true
pip uninstall -y tensorflow tensorflow-cpu keras 2>/dev/null | grep -i uninstall || true

# 5: data from a community mirror (original hosting is gone). Only the tasks we use.
hf download beckhamc/design_bench_data --repo-type dataset --local-dir "$DBD" \
  --include 'tf_bind_8-SIX6_REF_R1/*' 'tf_bind_10-*/*' 'superconductor/*' >/dev/null 2>&1 \
  && echo "data downloaded" || echo "WARN data download failed — check HF mirror"

# 6: ChEMBL SMILES tokenizer needs a vocab at import even though we never use ChEMBL.
V="$DBD/smiles_vocab.txt"
[ -f "$V" ] || printf '%s\n' '[PAD]' '[unused1]' '[UNK]' '[CLS]' '[SEP]' '[MASK]' \
  C N O S P F I H c n o s B r l '(' ')' '[' ']' = '#' - + / '\' '@' 1 2 3 4 5 6 7 8 9 0 . '%' > "$V"

# 7: exact/__init__.py hard-imports every oracle (gym/mujoco/nasbench) — make optional.
python - "$SP" << 'PYEOF'
import sys, io
f = sys.argv[1] + "/oracles/exact/__init__.py"
patched = "getattr(__import__('design_bench.oracles.exact."
if patched not in open(f).read():
    names = [('hopper_controller_oracle','HopperControllerOracle'),
             ('ant_morphology_oracle','AntMorphologyOracle'),
             ('dkitty_morphology_oracle','DKittyMorphologyOracle'),
             ('toy_continuous_oracle','ToyContinuousOracle'),
             ('nas_bench_oracle','NASBenchOracle'),
             ('tf_bind_8_oracle','TFBind8Oracle'),
             ('tf_bind_10_oracle','TFBind10Oracle'),
             ('toy_discrete_oracle','ToyDiscreteOracle')]
    body = "for _m,_n in %r:\n    try:\n        globals()[_n]=getattr(__import__('design_bench.oracles.exact.'+_m,fromlist=[_n]),_n)\n    except Exception:\n        pass\n" % names
    open(f,'w').write("# ponytail: optional oracle imports (upstream hard-imports break headless)\n"+body)
    print("patched exact/__init__.py")
else:
    print("exact/__init__.py already patched")
PYEOF

# 8: approximate_oracle.py uses np.loads (removed) — swap for pickle.loads.
grep -rl 'np\.loads' "$SP" 2>/dev/null | xargs -r sed -i 's/np\.loads/__import__("pickle").loads/g' && echo "np.loads patched"

echo "== verify =="
cd "$(dirname "$0")/.." && python code/db_tasks.py TFBind8 TFBind10 Superconductor 2>&1 | grep -E 'dim=' || echo "VERIFY FAILED"
