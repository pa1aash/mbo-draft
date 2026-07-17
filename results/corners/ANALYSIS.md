# Four-corners analysis (Part I ground truth)

## Reproduction gate: **PENDING (off,off corner not yet complete)**

Tolerance (stated before the look): n/a

## Corners

| corner | X1 | eta2_surr | eta2_opt | eta2_inter | Friedman p | rho(gap,log|y|) |
|---|---|---|---|---|---|---|
| off_off | — | PARTIAL (20/63 cells @30 seeds) | | | | |
| on_off | — | MISSING (not yet run) | | | | |
| off_on | — | MISSING (not yet run) | | | | |
| on_on | on | 0.369 | 0.013 | 0.165 | 6.09e-05 | +0.536 |

## Pre-registered X1 confound test (rho of per-task GP-ens gap vs log10 |y|-scale)
X1 prediction: rho>0.6 in X1-OFF corners (off_off, off_on), rho~0 in X1-ON corners (on_off, on_on). rho unchanged across X1 => confound refuted, headline strengthened.

