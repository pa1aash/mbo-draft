# code/run_scripts/

Driver scripts that launch batches of experiments and save output to `../../results/`.
These accumulated over several rounds of the project; **all iterations are kept** so the
full experimental history is preserved. Filenames are unchanged.

## Files (grouped by iteration, roughly oldest → newest)

| File                        | Description                                                                              |
|-----------------------------|------------------------------------------------------------------------------------------|
| `run_quick.py`              | Quick smoke-test run of the pipeline (small budget) — earliest driver.                   |
| `run_experiments.py`        | First full experiment batch driver.                                                      |
| `run_remaining.py`          | Fills in experiments not covered by the first batch.                                     |
| `run_rl_abl.py`             | Offline RL ablation runs.                                                                |
| `run_new_experiments.py`    | Second-round experiments (revised methods/tasks).                                        |
| `run_remaining_new.py`      | Fills in the gaps from the second round.                                                 |
| `run_final_experiments.py`  | "Final" pre-submission experiment batch.                                                 |
| `run_missing.py`            | Re-runs specific missing/failed configurations.                                          |
| `run_pen_sweep.py`          | Penalty (conservatism strength β) sweep / ablation.                                      |
| `run_revision.py`           | Revision-round experiments addressing reviewer concerns (more seeds, extra baselines, O2O on all tasks). Writes `results_revision.json`. |
| `run_revision2.py`          | Follow-up revision experiments.                                                          |

## Typical output mapping

- Early/mid drivers → `results/results.json`, `results/results_new.json`
- `run_final_experiments.py` → `results/results_final.json`
- `run_revision.py` / `run_revision2.py` → `results/results_revision.json`

> These scripts import the engines in `../experiments/`. If run from this folder, adjust
> import paths accordingly — the code was originally run with all files in one directory,
> so paths were flat. Reorganization did not modify the scripts.
