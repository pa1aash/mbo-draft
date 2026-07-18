#!/usr/bin/env python
"""macOS/arm64 port of cloud/fix_designbench.sh source patches.

Applies to the design_bench INSTALLED in the current interpreter. Idempotent. Run with the
mac-db venv's python AFTER `pip install design-bench==2.0.20 --no-deps` and the minimal deps
(see envs/ENVIRONMENTS.md / envs/mac-db-requirements.lock):

    envs/mac-db/bin/python envs/mac-db-patches/fix_designbench_macos.py

What differs from the Linux fix_designbench.sh:
  - Fix #8 (np.loads -> pickle.loads) uses a python walk, NOT GNU `sed -i` (BSD sed differs).
  - Two EXTRA patches make the deepchem/rdkit molecule-feature import optional, because the
    deepchem->rdkit->torch chain is impractical to install on arm64 and db_tasks.py never uses
    Morgan fingerprints (its tasks are TFBind/Superconductor/GFP/UTR/morphology, not ChEMBL).
  - Fixes #1-5 (version pins, TF removal, HF data) are install-time, handled in ENVIRONMENTS.md;
    this script is only the source patches. Data (incl. GFP/UTR, which the cloud script omits)
    is fetched via huggingface_hub snapshot_download — see ENVIRONMENTS.md.
"""
import os
import sys

import design_bench
SP = os.path.dirname(design_bench.__file__)


def patch(path, old, new, tag):
    p = os.path.join(SP, path)
    s = open(p).read()
    if new.split('\n')[0] in s or tag in s:
        print(f"  [skip] {path} already patched ({tag})"); return
    if old not in s:
        print(f"  [WARN] {path}: pattern not found ({tag})"); return
    open(p, 'w').write(s.replace(old, new)); print(f"  [ok]   {path} ({tag})")


# Patch A: deepchem import optional in morgan_fingerprint_features.py
patch('oracles/feature_extractors/morgan_fingerprint_features.py',
      "from deepchem.feat.smiles_tokenizer import SmilesTokenizer\nimport deepchem.feat as feat",
      ("try:  # macOS patch: deepchem->rdkit->torch chain unavailable on arm64; molecule tasks unused\n"
       "    from deepchem.feat.smiles_tokenizer import SmilesTokenizer\n"
       "    import deepchem.feat as feat\n"
       "except Exception:\n    SmilesTokenizer = None\n    feat = None"),
      'macOS patch: deepchem')

# Patch B: guard MorganFingerprintFeatures.__init__ when deepchem absent
patch('oracles/feature_extractors/morgan_fingerprint_features.py',
      "        # wrap the deepchem featurizer that relies on rdkit\n        self.featurizer = feat.CircularFingerprint(size=size, radius=radius)",
      ("        # macOS patch: deepchem/rdkit unavailable -> disable molecule feature extraction\n"
       "        if feat is None:\n            self.featurizer = None; self.tokenizer = None\n"
       "            self.size, self.radius, self.dtype = size, radius, dtype\n            return\n"
       "        # wrap the deepchem featurizer that relies on rdkit\n"
       "        self.featurizer = feat.CircularFingerprint(size=size, radius=radius)"),
      'macOS patch: deepchem/rdkit unavailable -> disable')

# Fix #7: optional oracle imports in exact/__init__.py (upstream hard-imports gym/mujoco/nasbench)
f7 = os.path.join(SP, 'oracles/exact/__init__.py')
if 'ponytail: optional oracle imports' not in open(f7).read():
    names = [('hopper_controller_oracle', 'HopperControllerOracle'),
             ('ant_morphology_oracle', 'AntMorphologyOracle'),
             ('dkitty_morphology_oracle', 'DKittyMorphologyOracle'),
             ('toy_continuous_oracle', 'ToyContinuousOracle'),
             ('nas_bench_oracle', 'NASBenchOracle'),
             ('tf_bind_8_oracle', 'TFBind8Oracle'),
             ('tf_bind_10_oracle', 'TFBind10Oracle'),
             ('toy_discrete_oracle', 'ToyDiscreteOracle')]
    body = ("for _m,_n in %r:\n    try:\n        globals()[_n]=getattr(__import__("
            "'design_bench.oracles.exact.'+_m,fromlist=[_n]),_n)\n    except Exception:\n        pass\n" % names)
    open(f7, 'w').write("# ponytail: optional oracle imports (upstream hard-imports break headless)\n" + body)
    print("  [ok]   oracles/exact/__init__.py (fix #7)")
else:
    print("  [skip] oracles/exact/__init__.py already patched (fix #7)")

# Fix #8: np.loads -> pickle.loads (macOS: python walk, not GNU sed -i)
n = 0
for root, _, files in os.walk(SP):
    for fn in files:
        if fn.endswith('.py'):
            p = os.path.join(root, fn); s = open(p).read()
            if 'np.loads' in s:
                open(p, 'w').write(s.replace('np.loads', '__import__("pickle").loads')); n += 1
print(f"  [ok]   np.loads -> pickle.loads in {n} file(s) (fix #8)")

print("done. verify: python code/db_tasks.py TFBind8 TFBind10 Superconductor GFP UTR")
