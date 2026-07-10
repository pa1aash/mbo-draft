Ensemble LCB for Offline Model-Based Optimization
==================================================

Code, results, and manuscript for the offline-MBO study (Ens-LCB vs GP-LCB vs
COMs, offline-to-online protocol, calibration ablations). Target venue: AAAI-27
main technical track.

Layout
------
code/           canonical pipeline (the ONLY code you need to run)
  mbo.py        tasks, surrogates, optimizers, all methods, O2O, calibration
  run_all.py    experiment runner -> results/results_camera.json
  stats.py      Wilcoxon+Holm, Friedman, bootstrap ranks from the results file
results/        experiment outputs (JSON)
paper/          LaTeX source and figures of the manuscript
legacy/         frozen history: superseded scripts, old docs, submission zips.
                Nothing in legacy/ is needed to reproduce the paper going
                forward. Do NOT include legacy/ in any submission supplement.

Setup
-----
python -m venv venv
venv\Scripts\pip install -r requirements.txt
(botorch/gpytorch are only needed for the gp_grad method; everything else
runs without them. On conda pythons, set KMP_DUPLICATE_LIB_OK=TRUE.)

Reproduce
---------
cd code
python mbo.py                                  quick self-check (~2 min)
python run_all.py --smoke                      end-to-end sanity pass
python run_all.py --exp all --seeds 10         full run -> results_camera.json
python stats.py                                significance tests + rank CIs

Provenance
----------
The CURRENT compiled paper (paper/latex_source/paper.tex, ICML 2026 workshop
version) was generated from the legacy pipeline:
  main table + O2O + RL + beta ablation   legacy/run_scripts/run_experiments.py    -> results/results.json      (6 seeds)
  GP-LCB column, K abl, calibration,
  diversity O2O row                       legacy/run_scripts/run_new_experiments.py -> results/results_new.json  (6/4/3 seeds)
  BoTorch GP check, pen sweep, bootstrap  legacy/run_scripts/run_final_experiments.py -> results/results_final.json
  10-seed rerun + extra baselines         legacy/run_scripts/run_revision.py        -> results/results_revision.json (unused by the paper)
  figures                                 legacy/figures/make_figures_v5.py (expects the JSONs in its cwd)

The AAAI submission must be rebuilt from results/results_camera.json produced
by code/run_all.py: one engine, one config (K=5, 96 hidden, 35 epochs, lr 3e-3,
beta=2, 128 candidates, 100 opt steps), one iterative O2O protocol for every
selection rule, n=10 seeds, fixed per-task datasets (seed 0), per-seed
training randomness.

Supplement packaging (AAAI)
---------------------------
Zip exactly: code/ results/results_camera.json requirements.txt README.md
Exclude: legacy/ venv/ paper/ and any git metadata.
