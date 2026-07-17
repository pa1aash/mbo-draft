# Four-corners analysis (Part I ground truth)

## Reproduction gate: **PASS**

Tolerance (stated before the look): per-cell |diff|<=max(2*SEM,0.10*|pub|) if |pub|>1 else 0.10 abs; eta2 within +/-0.05 each; Friedman p<1e-3; PASS if >=90% cells + eta2 + Friedman

- cells within tolerance: **63/63** (OK)
- eta2 (off,off) = {'n_tasks': 7, 'surr': 0.36694780380066677, 'opt': 0.013264829388685806, 'inter': 0.16458084353792354, 'surr_marg': {'ens': 0.3433, 'botorchgp': 0.8463, 'svgp': 0.8278}, 'opt_marg': {'perturb': 0.7091, 'grad': 0.6982, 'cma': 0.6102}}  vs published {'surr': 0.37, 'opt': 0.01, 'inter': 0.17, 'friedman_p': 6.1e-05} -> OK
- Friedman p (off,off) = 6.086248775276825e-05 -> OK

## Corners

| corner | X1 | eta2_surr | eta2_opt | eta2_inter | Friedman p | rho(gap,log|y|) |
|---|---|---|---|---|---|---|
| off_off | off | 0.367 | 0.013 | 0.165 | 6.09e-05 | +0.536 |
| on_off | — | PARTIAL (1/63 cells @30 seeds) | | | | |
| off_on | — | MISSING (not yet run) | | | | |
| on_on | on | 0.369 | 0.013 | 0.165 | 6.09e-05 | +0.536 |

## Pre-registered X1 confound test (rho of per-task GP-ens gap vs log10 |y|-scale)
X1 prediction: rho>0.6 in X1-OFF corners (off_off, off_on), rho~0 in X1-ON corners (on_off, on_on). rho unchanged across X1 => confound refuted, headline strengthened.

