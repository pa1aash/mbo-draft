# Pod compute results — consolidated

Self-contained summary of the Linux-pod compute session (branch `pod-compute`). Written for a
reader who has only the paper PDF. Every number carries its engine; every claim traces to an
artifact path. **Engine notation:** X1 = standardize the ensemble's regression targets;
X3 = one matched candidate-selection protocol (top-128 by surrogate LCB) for every optimizer.
off_off = pre-audit engine; on_on = fully audited engine. Both published artifacts
(`results_camera.json`, `results_db.json`) are the **off_off** engine.

Hardware: RunPod ubuntu-2404, 32 vCPU EPYC 9655P. Synthetic env `envs/pod-synth`
(torch 2.11.0+cpu, numpy 2.4.4, sklearn 1.8.0, botorch 0.18.1, gpytorch 1.15.2, cma 4.4.4).
Design-Bench env `dbm` (torch 2.8.0+cpu, numpy 1.23.5, sklearn 1.0.2, botorch 0.10.0,
gpytorch 1.11, design-bench 2.0.20). Torch is a controlled variable and is recorded per file.

---

## Phase 0 — runner safety (code/run_all.py)
Fixed the class of bug behind the lost on_on corner: (1) every result file now carries a
top-level `meta` block + per-cell `_engine` stamp; engine state is recorded, never inferred from
a filename; (2) a run refuses to MERGE cells into a file whose recorded X1/X3 differs (exit 4);
(3) no-op guard (0 cells scheduled -> exit 2); (4) camera guard (refuses results_camera.json /
results_db.json without --i-mean-it, exit 3); (5) loader assertion rejects any file lacking
complete meta. Verified: MBO_X1/MBO_X3 are read from env — ens:perturb Branin off_off = -0.776
(~ published -0.78), X3-on = -4.54. All guards return their documented exit codes.

## Phase 2 — reproduction gate (synthetic, off_off): PASS
Full 9x7x30 off_off grid (`results/corners/pod_off_off.json`) reproduces `results_camera.json`:
published Table 1 **63/63** cells within the pre-registered tolerance; **eta2_surr = 0.3689**
(pub 0.367), eta2_opt 0.0132, eta2_inter 0.1652; **Friedman p = 6.086e-5** (pub 6.09e-5).
ens:cma Branin = -14.010643 vs camera -14.010635 (8.2e-6). Max cross-cell relative drift 1.47%,
confined to SVGP-variational and stochastic-optimizer cells (library-version noise, disclosed) —
not a material divergence. Synthetic is platform-invariant to within library noise. (docs/POD_VERIFICATION.md)

## Phase 3 — K x beta gate (on_on). Pre-registered KB1–KB5 verbatim (commit 6951265). docs/GATE_KBETA.md
- **eta2_surr is jointly K- and beta-dependent:** rises 0.184 (beta=0) -> 0.406 (beta=2), and
  peaks at K=5 (0.408) — exactly the (K=5, beta=2) the paper fixes.
- **KB1 — confirmed, no reversal.** eta2_surr at K=2 (0.326) is materially below K=5 (0.408), but
  the ensemble marginal at K=2 (0.283) stays far below the GP's (0.767): the surrogate effect is
  inflated by fixing K=5 but is NOT a K artifact; headline does not reverse.
- **KB2 — smooth-mean survives.** GP–ensemble gap at beta=0 is 0.378 (does not collapse; kill
  threshold 0.278). The GP's mean is genuinely better independent of pessimism; pessimism
  amplifies the gap to 0.556 at beta=2. (Measured beta=0 gap 0.378 < the paper's cited 0.47, so
  more of the gap is beta-mediated than claimed.)
- **KB3 — GP advantage robust.** The gap does not close at K=2/beta=2 (ens 0.283 vs GP 0.767); a
  small pessimistic ensemble does not catch the GP.
- **KB4 — confound absent in aggregate, present per task.** Median sigma_GP/sigma_ens at K=5 is
  1.19 (~1), but per-task spans 0.07 (Branin) to 1.44 (Styblinski/Rastrigin) — >20x.
- **KB5 — confirmed underpowered.** Task+seed bootstrap (10k) eta2_surr CIs: off_off [0.254,0.559],
  on_off [0.186,0.444], off_on [0.312,0.649], on_on [0.290,0.556]. All four overlap; the on_on CI
  contains every other corner point estimate. 0.405 must not be reported without its CI. (Bootstrap
  validated: off_off width 0.305 ~ the published 0.32.)

## Phase 4 — Design-Bench env. docs/POD_ENV.md
Built env `dbm` from the known-good stack (torch 2.8.0; py3.9 caps torch at 2.8, so latest-torch
== torch28). All 5 non-mujoco tasks import and evaluate. **Finding:** cloud/fix_designbench.sh
installs botorch/gpytorch UNPINNED, which pulls numpy>=1.24 and breaks design-bench 2.0.20 — the
fix script is itself broken for fresh 2026 installs and must pin them.

## Phase 5 — Design-Bench verification. docs/POD_DB_VERIFICATION.md
**results_db.json is the OFF_OFF engine** (determined empirically: off_off mean|Δp100|=0.009 with
discriminating cells matching to 0.0000; on_on mean|Δp100|=0.112). Like the camera file, the DB
artifact is pre-audit, NOT on_on — so the three genuinely missing DB corners are on_off, off_on,
on_on. Reproduction on the 5 non-mujoco tasks: **TFBind8 MATCHES (exact), TFBind10 MATCHES
(exact), Superconductor MATCHES (1.6%), UTR MATCHES (1.4%), GFP DIVERGES (18.1%)** — the GFP
decode artifact, not tuned away.

## Phase 6 — Design-Bench at scale. docs/POD_DB_SCALE.md
- **The DB corners do NOT mirror synthetic — the null lives here.** DB eta2_surr =
  0.001 / 0.032 / 0.002 / 0.018 (off_off/on_off/off_on/on_on) vs synthetic 0.367/0.283/0.450/0.405.
  The surrogate main effect is indistinguishable from zero in every corner (Friedman p 0.19–0.76);
  the optimizer axis carries what little effect exists — the reverse of synthetic. Robust to mujoco
  inclusion (eta2_surr 0.044–0.091) and GFP exclusion (0.001–0.021).
- **6.2 mujoco:** Ant + DKitty ran across all 4 corners via RF oracles (no simulator) — the pod
  reached what macOS never could.
- **6.3 X11 (competing-mechanism kill):** on the EXACT-oracle subset {TFBind8, TFBind10} the
  cross-cell null SURVIVES (Friedman p 0.34–0.51); the RF-oracle subset rejects (p 0.02–0.05) in
  3/4 corners. So the cell differences are an approximate-oracle phenomenon and the null is genuine
  on exact oracles — the "RF oracles manufactured the null" objection is killed. Oracle noise floor
  ~1e-15 (deterministic), so the null is not noise.
- **6.5 GFP quarantine:** excluding GFP flips exactly one below-nominal-0.90 coverage claim
  (botorchgp mean c_in 0.876 -> 0.968); it does not change the eta2 null.

## Phase 7 — confounded / underpowered re-runs (synthetic). docs/POD_PHASE7.md
- **7.1 gradtune 2x2 (P0-0):** collapse-genuine count off_off 2/7, on_off 0/7, off_on 5/7,
  on_on 4/7 — **the collapse's genuineness is driven by X3, not X1**. Under X3-off trust-region
  tuning closes the gap; under X3-on perturbation still wins. Structure confirmed: genuine at
  d<=10, tuning closes at d>=15.
- **7.2 x0 inversion (30 seeds):** ensemble-specific (ens:grad inv 0.55 vs botorchgp 0.12),
  X3-amplified. Branin ens:grad inverts on **100% of seeds under X3-on** (every returned design
  worse than the best x0 in its own pool; ret -7.54 vs x0 -0.41).
- **7.3 coverage, X3-disentangled:** |c_ood(grad) - c_ood(cma)| = 0.010 under X3-on vs 0.117 under
  X3-off — **the grad~cma coverage equivalence is an X3 artifact**, refuting the gradient-specific
  "ensemble x gradient" framing (it is ensemble x any aggressive selector under the matched protocol).
- **7.4 GP coverage (P0-3):** sklearn GP own-proposal coverage 0.97 (reproduces published), grid's
  botorchgp 0.831, ensemble 0.14. The published 0.97 was the sklearn GP, not the grid's GP.
- **7.5 rho_knn:** rho(sigma, |error|) ~ 0.07 but rho(sigma, kNN distance to D) ~ 0.26 (positive
  on 7/7) — **the ensemble's sigma is a distance signal, not an error signal**; the paper measured
  it against the wrong target.
- **7.6 ungenerated numbers (P0-4):** all six now recoverable (bootstrap_ci, beta0, gp_coverage,
  rf_robustness freshly generated; subsample_control, stats_9cell have existing generators).

---

## What most changes the decision
The headline decomposition is real in DIRECTION but not in the magnitude the paper reports and not
where the paper says it lives: (a) synthetic eta2_surr is a joint (K=5, beta=2) maximum and its
four-corner decomposition is statistically unresolvable at n=7 (KB5); (b) on Design-Bench the
surrogate effect is a genuine NULL that survives on exact oracles (X11); (c) the gradient-specific
mechanism is an X3 protocol artifact (grad~cma), while the GP's mean advantage (KB2) and the
ensemble's distance-informative sigma (7.5) are the robust, correctly-attributed effects.
