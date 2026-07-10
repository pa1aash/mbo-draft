# code/figures/

Scripts that turn the result JSON files in `../../results/` into the figures used in the
paper (`../../paper/figures/`). Both iterations are kept.

| File                 | Description                                                                 |
|----------------------|-----------------------------------------------------------------------------|
| `make_figures.py`    | Original figure-generation script.                                          |
| `make_figures_v5.py` | Updated (v5) figure generator matching the revised results. This is the one aligned with the current figures (`fig1`–`fig7`). |

## Figures produced

The generated figures (found in `../../paper/figures/`) are:

- `fig1_offline_mbo` — offline MBO main comparison
- `fig2_avg_rank` — average rank across tasks
- `fig3_o2o_mbo` — offline-to-online MBO results
- `fig4_beta_ablation` — conservatism strength (β) ablation
- `fig5_rl` — offline RL results
- `fig6_k_ablation` — ensemble size (K) ablation
- `fig7_calibration` — uncertainty calibration

> Paths in the scripts were originally flat (all files in one directory). Reorganizing into
> folders did not edit the scripts, so update input/output paths if running from this folder.
