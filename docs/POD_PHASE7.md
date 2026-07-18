# Phase 7 — confounded / underpowered re-runs (pod, synthetic)

Env: envs/pod-synth (torch 2.11.0+cpu). All outputs engine-stamped. Tasks: the 7 synthetic.

## 7.1 GRADTUNE 2x2 (P0-0) — all 7 tasks, 15 seeds, per gradtune.py's OWN rule

"COLLAPSE GENUINE" = perturbation beats the best-tuned gradient config by >5% of |perturb|
(gradtune.py:73). Count of genuine-collapse tasks per corner:

| corner (X1,X3) | genuine / 7 | tasks |
|---|---|---|
| off_off | **2/7** | Levy, Rosenbrock |
| on_off | **0/7** | — |
| off_on | **5/7** | Branin, Styblinski, Levy, Rosenbrock, Griewank |
| on_on | **4/7** | Branin, Styblinski, Levy, Rosenbrock |

**P0-0 VERDICT — the collapse's genuineness is driven by X3, not X1.** At X3-OFF (off_off, on_off)
trust-region tuning closes the gap on 5/7 and 7/7 tasks; at X3-ON (off_on, on_on) perturbation
still beats the best-tuned gradient on 5/7 and 4/7. The ledger's original "trust closes it 3/4"
was the pre-audit (X3-off) engine — CONFIRMED. The audited-engine (X3-on) collapse is genuine
surrogate geometry on the majority of tasks. The 2x2 now attributes the P0-0 result (the prior
"5/7 vs 4/7" were BOTH X3-on; the X1 axis barely moves it). The pre-registered structure holds
for on_on: genuine at d<=10 (Branin, Styblinski, Levy, Rosenbrock), tuning closes at d>=15
(Rastrigin, Ackley, Griewank). Artifacts: results/results_gradtune_{off_off,on_off,off_on,on_on}.json.

## 7.2 x0 INVERSION — 30 seeds, 9 cells, both X3 states

inversion_rate = P(best returned oracle < best x0 oracle), noiseless oracle. Mean over 7 tasks:

| cell | X3=0 inv_rate | X3=1 inv_rate | mean frac_worse (X3=1) |
|---|---|---|---|
| ens:grad | 0.31 | **0.55** | 0.63 |
| ens:perturb | 0.23 | 0.30 | 0.94 |
| ens:cma | 0.60 | 0.60 | 0.60 |
| botorchgp:grad | 0.12 | 0.12 | 0.12 |
| svgp:grad | 0.24 | 0.27 | 0.27 |

**Ensemble-specific and X3-amplified.** The ensemble inverts far more than the GP
(ens:grad 0.55 vs botorchgp:grad 0.12 under X3-on). **Branin-2D ens:grad inverts on 100% of
seeds under X3-on** (frac_worse=1.00: every returned design is worse than the best x0 the method
was holding; ret_best=-7.54 vs x0_best=-0.41). Under X3-off the same cell inverts on 73%.
So the pooling+top-128-by-LCB rule (X3) makes the ensemble rank hallucinated high-LCB designs
above the real best-x0 point in its own pool — a by-demonstration pessimism failure, holding at
30 seeds. Artifact: results/x0_inversion.json.

## 7.3 COVERAGE 3x3 WITH X3 DISENTANGLED — both X1 x both X3, 8 seeds

Mean |c_ood(ens:grad) - c_ood(ens:cma)| over tasks:
- X3-OFF (x1=1,x3=0): **0.117**
- X3-ON (x1=1,x3=1): **0.010**

**The grad ~ cma coverage equivalence is an X3 ARTIFACT.** Under X3 both optimizers pool every
iterate and return the top-128 by surrogate LCB, so they hand in near-identical designs -> near-
identical c_ood (0.010 apart). Under X3-off, where they use different selection rules, their
coverage differs by 0.117. This REFUTES the gradient-specific "ensemble x gradient interaction"
framing (pre-registration X7): the collapse is ensemble x ANY aggressive selector under the
matched protocol, not gradient-specific. Artifact: results/coverage33.json.

## 7.4 THE GP's REAL COVERAGE (P0-3)

Premise coverage on each surrogate's OWN proposals, on_on:
- **sklearn exact GP (run_gpcov): 0.97** (reproduces the published Table 3 value of 0.97).
- **grid's botorchgp (coverage33): 0.831** mean (Styblinski 0.38 — the low tail).
- **ensemble: 0.14** (own_own) / 0.10 (in-dist) — the collapse.
- cross: ensemble on GP proposals = 0.14; GP on ensemble proposals = 0.94.

**P0-3 SETTLED:** the published 0.97 is the SKLEARN GP, not the differentiable grid GP the paper
actually scores. The grid's botorchgp real coverage is 0.831 (lower, and 0.38 on Styblinski).
Report both. Artifacts: results/gpcov.json, results/coverage33.json.

## 7.5 rho_knn RECOVERY (sigma vs DISTANCE vs sigma vs ERROR) — ensemble, on_on, 30 seeds

| task | rho(sigma, \|error\|) | rho(sigma, kNN dist to D) |
|---|---|---|
| Branin-2D | +0.076 | +0.051 |
| Styblinski-5D | +0.163 | +0.332 |
| Levy-8D | +0.135 | +0.362 |
| Rosenbrock-10D | +0.121 | +0.341 |
| Rastrigin-15D | +0.000 | +0.282 |
| Ackley-20D | -0.019 | +0.196 |
| Griewank-30D | -0.008 | +0.234 |
| **mean** | **~0.07** | **~0.26** |

**The ensemble's sigma is a DISTANCE signal, not an error signal.** rho(sigma, |mu-f|) ~ 0.07
(the paper's "sigma uninformative" number, reproduced), but rho(sigma, distance-to-data) ~ 0.26
(3-4x larger, positive on 7/7 tasks, >0.28 on the 4 mid/high-d tasks). The paper concluded
sigma is uninformative by measuring it against the wrong target: sigma tracks OOD-ness (kNN
distance) even though it does not track pointwise error. This reframes the mechanism — the
ensemble's uncertainty IS informative about extrapolation, just not calibrated to error
magnitude. Artifact: results/calibration_on_on.json.

## 7.6 THE UNGENERATED NUMBERS (P0-4) — recoverability audit

| number | generator | status |
|---|---|---|
| bootstrap_ci | code/bootstrap_eta.py (NEW, task+seed 10k) | GENERATED (results/bootstrap_eta*.json) |
| beta0 | code/run_beta0.py + kbeta grid_b0.0 (full 3x3 at beta=0) | GENERATED (results/kbeta/grid_b0.0.json; gap=0.378) |
| gp_coverage | code/run_gpcov.py + code/coverage33.py | GENERATED (0.97 sklearn / 0.831 botorchgp) |
| subsample_control | code/run_subsample.py (writes mbo_enssub, present in results_camera.json) | RECOVERABLE (generator exists) |
| stats_9cell | code/analyze_corners.py / code/stats.py (Friedman + eta2 over 9 cells) | RECOVERABLE (analyze_corners reproduces it) |
| rf_robustness | Design-Bench X11 (docs/POD_DB_SCALE.md) | GENERATED (exact vs RF oracle subset) |

**All six P0-4 numbers are recoverable**; four were freshly generated this session, two have
existing in-repo generators. None is orphaned.
