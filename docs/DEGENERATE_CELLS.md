# Degenerate cells on TF-Bind-8 (constant 1.0000)

Source: `results/platform/tfbind8_macos_torch28_n16.json` (TF-Bind-8, 3x3 grid, n=16 seeds,
X1=on/X3=on, torch 2.8; subsample 8000). Date: 2026-07-18.

Four of the nine grid cells return `p100 = 1.0` on **every** one of the 16 seeds, with zero
variance: `botorchgp:grad`, `botorchgp:perturb`, `botorchgp:cma`, and `ens:perturb`. This
is not a score the optimizer earned — it is the normalized dataset reference. TF-Bind-8
scores are min-max normalized to the offline dataset's own range (`db_tasks.py`: raw oracle
range on this build is ymin=0.0, ymax=0.439296), so the best design already present in D
maps to exactly `y01 = 1.0`; 7 rows of the 8000-row offline set tie at that maximum, and
`oracle(dataset-best design)` returns exactly 1.0. A cell whose best proposal scores 1.0 has
therefore produced a design **no better than the best sequence already in D** — it beats
nothing in the data and never leaves the reference. The four constant cells are exactly
these: the reported "1.00" is a degenerate constant, not evidence of optimization. By
contrast, the cells that actually move the design off the data report `p100 > 1.0` (max over
the 16 seeds): `ens:grad` 2.067, `ens:cma` 2.130, `svgp:grad` 2.160, `svgp:cma` 2.160, and
`svgp:perturb` up to 1.724 (it beats the reference on some seeds and ties it on others,
min 1.0). Reporting 1.00 for the four constant cells without stating that it is a fixed
dataset-reference value presents a non-result as a score.

| cell | p100 (all 16 seeds) | std | beats D? |
|---|---|---|---|
| botorchgp:grad | 1.0 (constant) | 0.0 | no |
| botorchgp:perturb | 1.0 (constant) | 0.0 | no |
| botorchgp:cma | 1.0 (constant) | 0.0 | no |
| ens:perturb | 1.0 (constant) | 0.0 | no |
| svgp:perturb | 1.0 – 1.724 | 0.250 | sometimes |
| ens:cma | 1.207 – 2.130 | 0.342 | yes |
| ens:grad | 1.230 – 2.067 | 0.202 | yes |
| svgp:grad | 1.249 – 2.160 | 0.321 | yes |
| svgp:cma | 1.249 – 2.160 | 0.341 | yes |

Normalized dataset-best in D (subsample 8000): `y01_max = 1.0` (7 tied rows; raw oracle
max 0.439296, min 0.0).
