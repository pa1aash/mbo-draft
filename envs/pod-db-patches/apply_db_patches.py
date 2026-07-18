#!/usr/bin/env python
"""Apply Design-Bench source patches to the dbm env WITHOUT importing design_bench
(the deepchem-optional patch must land before import can succeed, since this env has
no deepchem). Locates the package via sysconfig. Idempotent."""
import os
import sysconfig

SP = os.path.join(sysconfig.get_paths()["purelib"], "design_bench")
DBD = os.path.join(sysconfig.get_paths()["purelib"], "design_bench_data")
os.makedirs(DBD, exist_ok=True)
print("design_bench=", SP)
print("design_bench_data=", DBD)


def patch(path, old, new, tag):
    p = os.path.join(SP, path)
    s = open(p).read()
    if new.split("\n")[0] in s or tag in s:
        print(f"  [skip] {path} already patched ({tag})"); return
    if old not in s:
        print(f"  [WARN] {path}: pattern not found ({tag})"); return
    open(p, "w").write(s.replace(old, new)); print(f"  [ok]   {path} ({tag})")


# Patch A: make deepchem import optional (deepchem absent in this env)
patch("oracles/feature_extractors/morgan_fingerprint_features.py",
      "from deepchem.feat.smiles_tokenizer import SmilesTokenizer\nimport deepchem.feat as feat",
      ("try:  # patch: deepchem absent; molecule/ChEMBL tasks unused by db_tasks.py\n"
       "    from deepchem.feat.smiles_tokenizer import SmilesTokenizer\n"
       "    import deepchem.feat as feat\n"
       "except Exception:\n    SmilesTokenizer = None\n    feat = None"),
      "patch: deepchem absent")

# Patch B: guard MorganFingerprintFeatures.__init__ when deepchem absent
patch("oracles/feature_extractors/morgan_fingerprint_features.py",
      "        # wrap the deepchem featurizer that relies on rdkit\n        self.featurizer = feat.CircularFingerprint(size=size, radius=radius)",
      ("        # patch: deepchem/rdkit featurizer unavailable -> disable molecule features\n"
       "        if feat is None:\n            self.featurizer = None; self.tokenizer = None\n"
       "            self.size, self.radius, self.dtype = size, radius, dtype\n            return\n"
       "        # wrap the deepchem featurizer that relies on rdkit\n"
       "        self.featurizer = feat.CircularFingerprint(size=size, radius=radius)"),
      "patch: deepchem/rdkit featurizer unavailable")

# Fix #7: optional oracle imports in exact/__init__.py (upstream hard-imports gym/mujoco/nasbench)
f7 = os.path.join(SP, "oracles/exact/__init__.py")
if "ponytail: optional oracle imports" not in open(f7).read():
    names = [("hopper_controller_oracle", "HopperControllerOracle"),
             ("ant_morphology_oracle", "AntMorphologyOracle"),
             ("dkitty_morphology_oracle", "DKittyMorphologyOracle"),
             ("toy_continuous_oracle", "ToyContinuousOracle"),
             ("nas_bench_oracle", "NASBenchOracle"),
             ("tf_bind_8_oracle", "TFBind8Oracle"),
             ("tf_bind_10_oracle", "TFBind10Oracle"),
             ("toy_discrete_oracle", "ToyDiscreteOracle")]
    body = ("for _m,_n in %r:\n    try:\n        globals()[_n]=getattr(__import__("
            "'design_bench.oracles.exact.'+_m,fromlist=[_n]),_n)\n    except Exception:\n        pass\n" % names)
    open(f7, "w").write("# ponytail: optional oracle imports (upstream hard-imports break headless)\n" + body)
    print("  [ok]   oracles/exact/__init__.py (fix #7)")
else:
    print("  [skip] oracles/exact/__init__.py already patched (fix #7)")

# Fix #8: np.loads -> pickle.loads (removed in modern numpy)
n = 0
for root, _, files in os.walk(SP):
    for fn in files:
        if fn.endswith(".py"):
            p = os.path.join(root, fn); s = open(p).read()
            if "np.loads" in s:
                open(p, "w").write(s.replace("np.loads", '__import__("pickle").loads')); n += 1
print(f"  [ok]   np.loads -> pickle.loads in {n} file(s) (fix #8)")

# Fix #6: smiles_vocab.txt (ChEMBL tokenizer needs it at import even if unused)
V = os.path.join(DBD, "smiles_vocab.txt")
if not os.path.exists(V):
    toks = ['[PAD]', '[unused1]', '[UNK]', '[CLS]', '[SEP]', '[MASK]',
            'C', 'N', 'O', 'S', 'P', 'F', 'I', 'H', 'c', 'n', 'o', 's', 'B', 'r', 'l',
            '(', ')', '[', ']', '=', '#', '-', '+', '/', '\\', '@',
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.', '%']
    open(V, "w").write("\n".join(toks) + "\n")
    print("  [ok]   smiles_vocab.txt written (fix #6)")
else:
    print("  [skip] smiles_vocab.txt exists (fix #6)")

print("done source patches")
