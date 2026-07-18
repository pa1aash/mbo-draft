# The Design-Bench GP freeze: mechanism (DB1-DB4)

Pre-registered in `docs/PREREGISTRATION_V2.md` (amendment 2026-07-18) BEFORE running. Data:
`results/platform/db_freeze_beta_n16.json` (macOS, torch 2.8, X1=on X3=on, n=16). Step 1:
`results/platform/gp_freeze_step1.json`. Scope note: TF-Bind-8 has the full 9 cells; UTR and
Superconductor carry the fast grad/perturb cells of the ensemble and the BoTorch GP (cma+svgp
dropped there for compute, per the committed amendment). Metrics per cell: `p100` mean/std
over 16 seeds; `decode_in_D` = fraction of returned designs whose argmax-decoded sequence is
one of the top-128 dataset sequences (discrete only); `disp_from_data` = mean L2 distance of
returned designs to the nearest top-128 dataset point.

## Verdict

**The exact-constant freeze is M-B (decode snap-back), with M-A (LCB paralysis / weak
gradients near the data) as a contributing ingredient. Not M-C.** The pre-registered control
decides it: Superconductor is continuous (no argmax decode) and its GP cells do NOT freeze —
they carry real variance and differ by optimizer — while on the discrete tasks the same
"stuck near the data" behaviour collapses, through the argmax, onto an identical dataset
sequence every seed. The single cleanest datum: `botorchgp:perturb` barely moves on BOTH task
types (disp 0.0000 discrete, 0.0004 continuous), yet returns a zero-variance constant ONLY on
the discrete task. The one thing that differs between those two runs is the decode step.

## The numbers (beta=2 unless noted)

| task | cell | p100 mean±std | decode_in_D | disp_from_data | frozen? |
|---|---|---|---|---|---|
| TF-Bind-8 | botorchgp:grad | 1.0000 ± 0.0000 | 1.000 | 0.0001 | **yes** |
| TF-Bind-8 | botorchgp:perturb | 1.0000 ± 0.0000 | 1.000 | 0.0000 | **yes** |
| TF-Bind-8 | botorchgp:cma | 1.0000 ± 0.0000 | 1.000 | 0.0003 | **yes** |
| TF-Bind-8 | ens:perturb | 1.0000 ± 0.0000 | 1.000 | 0.3835 | **yes** |
| TF-Bind-8 | ens:grad | 1.7614 ± 0.2018 | 0.000 | 2.1813 | no |
| TF-Bind-8 | ens:cma | 1.7151 ± 0.3418 | 0.018 | 2.1366 | no |
| UTR | botorchgp:grad | 0.9416 ± 0.0044 | 1.000 | 0.0000 | **yes** |
| UTR | botorchgp:perturb | 0.9623 ± 0.0029 | 1.000 | 0.0000 | **yes** |
| UTR | ens:perturb | 0.9613 ± 0.0045 | 1.000 | 0.4368 | **yes** |
| UTR | ens:grad | 0.9506 ± 0.0183 | 0.000 | 7.2262 | no (moves, worse) |
| Superconductor | botorchgp:grad | 1.1818 ± 0.1239 | n/a | 0.0250 | **no** |
| Superconductor | botorchgp:perturb | 1.2424 ± 0.0321 | n/a | 0.0004 | **no** |
| Superconductor | ens:perturb | 1.2475 ± 0.0347 | n/a | 0.0239 | **no** |
| Superconductor | ens:grad | 0.9427 ± 0.1224 | n/a | 4.1794 | no |

Beta contrast (BoTorch GP, discrete):

| task | cell | beta=2 | beta=0 |
|---|---|---|---|
| TF-Bind-8 | botorchgp:grad | 1.0000 ± 0.0000 (disp 0.0001) | 0.9882 ± 0.0427 (disp 0.4924, decode 0.875) |
| TF-Bind-8 | botorchgp:cma | 1.0000 ± 0.0000 (disp 0.0003) | 1.0096 ± 0.2696 (disp 0.4778, decode 0.814) |
| TF-Bind-8 | botorchgp:perturb | 1.0000 ± 0.0000 (disp 0.0000) | 1.0000 ± 0.0000 (disp 0.0270) |
| UTR | botorchgp:grad | 0.9416 ± 0.0044 (disp 0.0000) | 0.9414 ± 0.0044 (disp 0.0000) |

## Pre-registered predictions, by name

- **DB1 — SUPPORTED (not killed).** At beta=2 every BoTorch-GP cell returns designs that decode
  to a top-128 dataset sequence on 100% of returned designs, every seed: TF-Bind-8 grad/
  perturb/cma all `decode_in_D = 1.000` (3 of 3); UTR grad/perturb `1.000` (2 of 3, cma not
  run there per the amendment). The kill was "returned designs differ from x0 but still score
  the constant (coincidence, not retrieval)." They do NOT differ — `decode_in_D = 1.0` is
  retrieval. On UTR the frozen value is 0.94/0.96 (not 1.0), yet still `decode_in_D = 1.0`:
  the cells return top-128 dataset designs, and the surrogate simply never ranks the dataset
  max first. Retrieval, confirmed.

- **DB2 — SUPPORTED on TF-Bind-8, task-dependent.** On TF-Bind-8 sigma drives the freeze:
  grad and cma are exact constants at beta=2 but move and lose the constant at beta=0
  (grad 0.988 ± 0.043, cma 1.010 ± 0.270, decode drops below 1.0) — the M-A ingredient,
  confirmed there. Two honest exceptions: `botorchgp:perturb` stays constant even at beta=0
  (perturb is too weak a search to leave the data with or without sigma), and on UTR grad is
  frozen at BOTH betas (disp 0.0000 each) — the high-dim GP posterior mean is already flat at
  the data, so removing sigma changes nothing. So sigma is A cause of the freeze, not the only
  one; DB2's kill ("still constant at beta=0 → M-A refuted") fires on UTR grad and on perturb,
  which is why the verdict is M-B-primary with M-A contributing, not M-A alone.

- **DB3 — SUPPORTED; this is the decisive control.** On Superconductor (continuous, no decode)
  the GP cells do NOT freeze: `botorchgp:grad` = 1.1818 ± 0.1239 (real variance), disp 0.0250
  (> 0); they differ across optimizers (grad 1.18 vs perturb 1.24). The kill was "if
  Superconductor also freezes → M-A, not decode." It does not freeze → the freeze needs the
  decode step → M-B.

- **DB4 — SUPPORTED for the ensemble+gradient; refined for the ensemble+perturb.** The
  ensemble+gradient never freezes: it leaves the data far (disp 2.18 on TF-Bind-8, 7.23 on
  UTR, 4.18 on Superconductor) and returns non-dataset designs (`decode_in_D = 0`) — its jagged
  mean has off-data optima gradient can reach (on TF-Bind-8 it beats the reference, p100 1.76;
  on UTR those off-data optima decode to WORSE sequences, p100 0.95). But `ens:perturb` DOES
  freeze on the discrete tasks (`decode_in_D = 1.0`, TF-Bind-8 1.0000, UTR 0.9613). So the
  freeze is not purely a GP property: it is an interaction of a surrogate the optimizer cannot
  escape (a smooth GP for any optimizer; a jagged ensemble only for the weak perturb optimizer)
  with the decode step. DB4's kill ("ensemble also freezes → protocol property, not surrogate
  property") half-fires: the freeze is a surrogate×optimizer×decode property.

## Why it matters

On the discrete tasks several cells are tied at an identical constant — on TF-Bind-8, four of
nine (`botorchgp:{grad,perturb,cma}`, `ens:perturb`) sit at exactly 1.0000 with zero variance;
on UTR the two BoTorch-GP cells and `ens:perturb` are frozen. A Friedman omnibus that ranks
cells including several tied constants cannot resolve them by construction, so on the discrete
tasks `eta2_opt ~ 0` is partly "the optimizer CANNOT move these cells," not "the optimizer does
not matter." On the continuous task the cells are not frozen (they differ), so there the small
`eta2_opt` is a genuine near-equivalence rather than a freeze artifact. The two cases should be
reported separately, not pooled under one "the optimizer does not matter" claim.

## Untested gap (stated, not resolved)

Ant is continuous AND degenerate in Table 3 (1.52 x3). If that is a genuine freeze on a
continuous task, it cuts against M-B (which predicts no exact-constant freeze without a decode
step). Ant needs mujoco and is pod-only; it could not be run here. The gap is open. It is the
one observation that could complicate the M-B verdict, and it must be checked on the pod before
the mechanism is stated as settled: run Ant's GP cells at beta=2, n>=16, and read whether the
three optimizers return a zero-variance identical constant (M-B is threatened) or merely a
tight non-degenerate cluster like Superconductor (M-B holds). A single seed of the RF-oracle
Ant is not enough — the whole point is whether the variance is exactly zero.
