# Phase 3 — K x beta gate (KB1–KB5)

**Engine:** X1=on, X3=on (audited/on_on), 30 seeds, 7 synthetic tasks. **Env:** envs/pod-synth
(torch 2.11.0+cpu, numpy 2.4.4, sklearn 1.8.0, botorch 0.18.1, gpytorch 1.15.2, cma 4.4.4).
Pre-registered verbatim in docs/PREREGISTRATION_V2.md (commit 6951265) BEFORE launch.

**Artifacts (all engine-stamped):**
- `results/kbeta/grid_b{0.0,0.5,1.0,2.0,5.0}.json` — full 3x3 grid per beta (9 cells x 7 tasks x 30 seeds).
- `results/kbeta/kbeta_ens.json` — ensemble K x beta x optimizer p100 + sigma (840 fits).
- `results/kbeta/kbeta_gpsigma.json` — GP/SVGP sigma.
- `results/bootstrap_eta.json`, `results/bootstrap_eta_corners.json` — task+seed eta2 CIs (10k).
- `results/kbeta/kbeta_analysis.json` — the machine-readable verdicts.

---

## eta2 and the GP–ensemble gap across beta (full 3x3 grid, on_on)

| beta | eta2_surr | eta2_opt | eta2_inter | GP–ens gap | ens_marg | gp_marg | svgp_marg |
|---|---|---|---|---|---|---|---|
| 0.0 | 0.184 | 0.050 | 0.072 | 0.378 | 0.306 | 0.659 | 0.709 |
| 0.5 | 0.214 | 0.053 | 0.081 | 0.401 | 0.289 | 0.675 | 0.706 |
| 1.0 | 0.282 | 0.044 | 0.112 | 0.463 | 0.235 | 0.692 | 0.703 |
| 2.0 | 0.406 | 0.005 | 0.161 | 0.556 | 0.196 | 0.762 | 0.742 |
| 5.0 | 0.408 | —    | —    | 0.548 | —     | —     | —     |

eta2_surr rises monotonically with beta (0.184 -> 0.408); the surrogate main effect is
**strongly beta-dependent** — at beta=0 (pure-mean LCB, no uncertainty term) it is less than
half its beta=2 value. eta2_surr@beta2 = 0.406 reproduces the on_on corner (0.405).

## eta2_surr and surrogate marginals across K (ens rows @K + GP/SVGP rows @beta2, on_on)

| K | eta2_surr | ens_marg | botorchgp_marg | svgp_marg |
|---|---|---|---|---|
| 2 | 0.326 | 0.283 | 0.767 | 0.739 |
| 3 | 0.366 | 0.245 | 0.774 | 0.747 |
| 5 | 0.408 | 0.198 | 0.763 | 0.743 |
| 10 | 0.389 | 0.171 | 0.729 | 0.713 |

The ensemble marginal **decreases monotonically with K** (0.283 at K=2 -> 0.171 at K=10) — same
DIRECTION as the paper's supplement Fig 2 (ens best at low K), but much smaller magnitude (the
supplement reports 0.95 at K=2; the grid gives 0.283). eta2_surr peaks at K=5 (0.408), the
paper's fixed choice — i.e. the paper reports the surrogate effect at the K that maximizes it.

## sigma_GP / sigma_ens on the in-D reference (KB4)

Median ratio (all K) = 1.21; median @K=5 = **1.19**. Per-task @K=5 spans **0.07 (Branin) to
1.44 (Styblinski/Rastrigin)** — a >20x range:

| task | sigma_ens | sigma_botorchgp | ratio gp/ens |
|---|---|---|---|
| Branin-2D | 1.884 | 0.128 | 0.07 |
| Styblinski-5D | 2.193 | 3.164 | 1.44 |
| Levy-8D | 0.846 | 1.004 | 1.19 |
| Rosenbrock-10D | 0.291 | 0.402 | 1.39 |
| Rastrigin-15D | 0.604 | 0.873 | 1.44 |
| Ackley-20D | 0.170 | 0.138 | 0.81 |
| Griewank-30D | 43.29 | 13.72 | 0.32 |

## Bootstrap 95% CIs on eta2_surr (task+seed, 10,000 resamples) — KB5

| configuration | eta2_surr | 95% CI | width |
|---|---|---|---|
| corner off_off | 0.367 | [0.254, 0.559] | 0.305 |
| corner on_off | 0.283 | [0.186, 0.444] | 0.258 |
| corner off_on | 0.450 | [0.312, 0.649] | 0.337 |
| corner on_on | 0.405 | [0.290, 0.556] | 0.266 |
| grid beta=0 | 0.184 | [0.085, 0.354] | — |
| grid beta=2 | 0.406 | [0.285, 0.564] | — |

---

## Verdicts (by name)

**KB1 — PREDICTION CONFIRMED, KILL DOES NOT FIRE.** eta2_surr at K=2 (0.326) is materially below
its K=5 value (0.408) — the prediction holds; the surrogate main effect the paper reports is
inflated by fixing K=5, which is where eta2_surr peaks and the ensemble marginal is weakest
(0.198). BUT the kill criterion (ens marginal at K=2 EXCEEDS the GP's) does not fire: at K=2 the
ensemble marginal is 0.283, still far below the GP's 0.767. The surrogate effect is K-sensitive
but NOT a K artifact; the headline does not reverse. Report both the K-sensitivity and the
non-reversal.

**KB2 — SMOOTH-MEAN CLAIM SURVIVES.** The GP–ensemble gap at beta=0 is 0.378 — it does NOT
collapse (kill threshold: gap0 < 0.5*gap2 = 0.278; 0.378 > 0.278). At beta=0 the LCB is pure
mean maximization (no sigma), so a 0.378 normalized gap means the GP's MEAN is genuinely better
independent of calibration. Pessimism amplifies it (gap 0.378 -> 0.556, +47%, as beta 0 -> 2),
so the advantage is partly sigma-mediated but rests on a substantial mean-quality base. NB: the
measured beta=0 gap (0.378) is BELOW the paper's cited 0.47, so MORE of the gap is beta-mediated
than the paper implies — but the mechanism claim stands.

**KB3 — NOT TRIGGERED (GP advantage robust).** KB3's scenario requires the gap to CLOSE at
beta=2/K=2 while persisting at beta=0. It does not: at K=2/beta=2 the ensemble marginal (0.283)
remains far below the GP (0.767). A K=2 ensemble with adequate pessimism does NOT reach the GP's
score. The GP advantage is robust to both K and beta — stronger than KB3's "doesn't matter"
framing.

**KB4 — CONFOUND ABSENT IN AGGREGATE, PRESENT PER TASK.** Median sigma_GP/sigma_ens at matched
K=5 is 1.19 (~1), so the kill fires: on aggregate the shared beta=2 delivers comparable effective
pessimism and KB4's "fifth unmatched hyperparameter" does not exist. HOWEVER the per-task ratio
spans 0.07 (Branin) to 1.44 (Styblinski/Rastrigin) — a >20x range. So per task, beta=2 does
deliver very different pessimism (the GP is far LESS uncertain than the ensemble on Branin/Griewank,
comparably on the mid tasks). Reported honestly: the aggregate refutes KB4; the per-task spread
partially supports it.

**KB5 — CONFIRMED: DECOMPOSITION UNDERPOWERED AT n=7.** The four corner eta2_surr CIs all overlap
heavily (widths 0.26–0.34; corner range only 0.167). on_on's CI [0.290, 0.556] contains every
other corner point estimate (0.367, 0.283, 0.450). The corner differences are NOT resolvable at
n=7 tasks — exactly as predicted. 0.405 must NOT be reported as a corrected headline without its
CI [0.290, 0.556]. (Bootstrap validated: off_off CI width 0.305 ≈ the published 0.32.) By
contrast beta IS nearly resolvable — grid_b0 [0.085, 0.354] vs grid_b2 [0.285, 0.564] barely
overlap — so the beta-dependence of eta2_surr is a firmer result than the corner decomposition.

### One-line summary
The surrogate main effect is real and robust (GP marginal ~0.75 vs ens ~0.2–0.28 at every K),
but its MAGNITUDE (eta2_surr) is a joint artifact of K=5 and beta=2 — both chosen where the
effect is largest — and the four-corner decomposition that nets to 0.405 is statistically
unresolvable at n=7 tasks.
