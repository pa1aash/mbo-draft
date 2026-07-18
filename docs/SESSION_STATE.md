# Session state — Blueprint session (Phases A–E)

Started 2026-07-17. Updated after every unit. Format: `unit | status | path | sha/note`.

---

## POD COMPUTE SESSION (branch pod-compute, started 2026-07-18)

Linux pod (RunPod ubuntu-2404, 32 vCPU EPYC 9655P, 64 GB). Env: envs/pod-synth
(torch 2.11.0+cpu, numpy 2.4.4, sklearn 1.8.0, botorch 0.18.1, gpytorch 1.15.2, cma 4.4.4).

| unit | status | path | sha/note |
|---|---|---|---|
| P0 runner safety | DONE | code/run_all.py | f947783; guards tested (no-op=2, camera=3, engine-match=4, meta+loader OK) |
| P0 X1/X3 switch proof | DONE | (test) | off_off ens:perturb Branin=-0.776~=-0.78; X3-on=-4.54 |
| P1 pod-synth env + lock | DONE | envs/pod-synth-requirements.lock | ce6dabb |
| P2 reproduction gate | **PASS** | results/corners/pod_off_off.json | eta2_surr=0.3689 (pub 0.367), Friedman p=6.086e-5 (pub 6.09e-5), published 63/63; camera bit-diff <=1.47% rel on svgp/cma cells only (disclosed) |
| P3 K-beta gate | **DONE** | docs/GATE_KBETA.md | KB1 confirmed/no-reverse; KB2 smooth-mean survives; KB3 GP robust; KB4 median ratio 1.19 (per-task 0.07-1.44); KB5 corners overlap (underpowered) |
| P4 Design-Bench env | **DONE** | docs/POD_ENV.md, envs/pod-db-*.lock | env `dbm` torch 2.8; 5 non-mujoco tasks verified; unpinned-botorch fix bug documented |
| P5 DB verification | **DONE** | docs/POD_DB_VERIFICATION.md | results_db.json is OFF_OFF (empirically); TFBind8/10, Superconductor, UTR match; GFP diverges 18% (decode artifact) |
| P6 DB at scale | **DONE** | docs/POD_DB_SCALE.md | DB four corners eta2_surr~0.001-0.03 (NULL, unlike synthetic 0.28-0.45); mujoco ran; X11 null survives on exact-oracle subset |
| P7 synthetic re-runs | **DONE** | docs/POD_PHASE7.md | gradtune 2x2 X3-driven; x0 inversion ens-specific; grad~cma is X3 artifact; sigma=distance not error |
| P8 report | DONE | docs/POD_RESULTS.md | consolidated |

**RESUME commands (if any unit interrupted):** run_phase3.sh / run_phase7.sh for the synthetic
grids (merge-safe); envs/build_pod_db.sh for the DB env; the DB corner runs are merge-safe under
results/db_corners/. All launch commands are in logs/ headers.

## Environment reality (load-bearing)
- This macOS machine had **no working torch/sklearn/botorch env** at session start. The
  repo `venv/` is a **Windows** venv (`venv/Scripts/python.exe`, torch 2.11.0 Windows
  binaries) — non-functional here. The camera results were generated off-machine.
- Built a macOS venv for this session: `<scratchpad>/venv_mac` (Python 3.13.7, torch
  **2.13.0**, botorch 0.18.1, gpytorch 1.15.2, sklearn, scipy, cma, pandas). Log:
  `logs/pip_install.log`. All corner/analysis runs use this interpreter.
- **Platform-shift caveat for the reproduction gate:** the published Table 1 was produced
  on Windows/torch 2.11; corners here run on macOS-arm64/torch 2.13. Per-seed RNG will
  differ; the gate is therefore evaluated on **30-seed means** with an explicit tolerance
  stated before the look (see PART III / decision tree).
- `design_bench` is NOT installed and is not installable here (disk was ~8 GiB free at
  start; DB needs TF1.x + mujoco). **Design-Bench corners are MISSING this session** — see
  FAILURES.md. Synthetic corners proceed.

## The four corners
- **(on,on)** = committed `results/results_camera.json` (sha256 73ce3be9…, 392577 bytes,
  = `git show HEAD:` — verified byte-identical). NOT re-run.
- **(off,off) / (on,off) / (off,on)** = launched via `code/run_corners.py`, 9 grid cells,
  30 seeds, 7 synthetic tasks → `results/corners/corner_*.json`.

## RESUME — how to finish v2 (if this session is interrupted)

Everything is file-first; v2 is a mechanical fill from artifacts on disk. Steps:
1. Check the driver finished: `grep "ALL POST-CORNER ARMS DONE" logs/all_arms.log`.
   The active driver is the **idempotent** `<scratchpad>/run_all_arms.sh` (launched via nohup;
   venv `<scratchpad>/venv_mac/bin/python`). If it died mid-run (see FAILURES.md F-2), just
   relaunch: `nohup bash <scratchpad>/run_all_arms.sh > logs/all_arms.log 2>&1 &` — it resumes
   corners (merge-safe) and skips any arm whose output JSON already exists.
2. Re-run the analyzer for the complete four-corners table:
   `cd code && <venv> analyze_corners.py` → `results/corners/analysis.json` + `ANALYSIS.md`.
3. Read the arm results: `results/corners/ANALYSIS.md`, `results/results_gradtune_x1off.json` +
   `_x1on.json` (+ `logs/gradtune_x1{off,on}.log` for the VERDICT lines), `results/heldout.json`
   (+ `logs/heldout.log` table), `results/x0_inversion.json` (+ log), `results/coverage33.json`
   (+ log), `results/dobest.json`.
4. Fill `docs/AAAI_BLUEPRINT.md` Part I: four-corners table, ρ test verdict, P0-0 verdict from
   gradtune-under-X1 (compare gradtune_x1on best-grad vs perturb per the script's own rule),
   held-out T1 verdict (does ens normRMSE converge to GP under X1-on?), x0-inversion (does it
   hold, and only for ens?), the 3×3 coverage + (ĉ_ood,score) Spearman, and the full P0/P1
   status table. Update Part III's realized branch and each P(accept).
5. Commit as blueprint v2, push. Then curation: `hyperresearch sync && hyperresearch lint -j`.

## Unit ledger
| unit | status | path | note |
|---|---|---|---|
| A.0 run_all `--out`/`--methods` | DONE | code/run_all.py | safety flag; default path unchanged |
| A.0 mbo X1/X3 env switches | DONE | code/mbo.py | `MBO_X1`/`MBO_X3`; unset ⇒ both True (camera engine) |
| A.0 gradtune `--out` + 7 tasks | DONE | code/gradtune.py | adds Levy/Rastrigin/Griewank |
| A.0 corners driver | DONE | code/run_corners.py | 3 missing corners |
| A.0 camera byte-verify | DONE | results/results_camera.json | sha matches HEAD |
| A.1.1 four corners run | RUNNING | results/corners/ | off_off DONE (repro PASS 63/63); on_off/off_on in flight |
| Reproduction gate | **PASS** | results/corners/ANALYSIS.md | off_off η²_surr=0.367 vs pub 0.37; Friedman 6.09e-5 |
| Four corners (all 4) | **DONE** | results/corners/analysis.json | see below — X1 & X3 real but OFFSETTING |
| Post-corner arms | **ALL DONE** | results/ | gradtune, heldout, x0inv, coverage all landed |
| A.1.3 held-out (T1) | DONE | results/heldout.json | bias SEPARABLE from fit (ens≈GP 5/7, still loses opt) |
| A.1.5 x0 inversion (T12) | DONE | results/x0_inversion.json | HOLDS ensemble-specific (ens:grad 0.52 vs GP 0.14) |
| A.1.6 3×3 coverage | DONE | results/coverage33.json | matrix complete; ĉ_in 0.83–0.93 from D; ρ(cov,score)=0.19 |
| Phase E blueprint v2 | **DONE** | docs/AAAI_BLUEPRINT.md | Part I filled; realized branch; P(accept) revised |
| A.1.2 gradtune 2×2 (P0-0) | **DONE → SCOPED** | results/results_gradtune_x1{off,on}.json | genuine 5/7 (X1off), 4/7 (X1on) |

**P0-0 verdict = SCOPED.** On the AUDITED engine (X3-on), the ensemble×gradient collapse is
GENUINE (perturb beats best-tuned grad incl. trust-region) on 5/7 tasks X1-off, 4/7 X1-on.
Tuning rescues gradient only on the high-d multimodal tasks (Rastrigin-15D, Ackley-20D,
Griewank-30D-under-X1). The ledger's "trust closes it 3/4" was the PRE-AUDIT 4-task run; the
audit flips it. Collapse is majority-genuine surrogate geometry, not an untuned optimizer.

**Four-corners verdict (η²_surr / ρ(gap,log|y|)):** off_off 0.367/+0.54 · on_off(X1) **0.283/−0.11** ·
off_on(X3) 0.450/+0.57 · **on_on 0.405/+0.50 (TRUE, corrected)**. X1 alone drops η²_surr ~23% and
kills the scale-correlation (P0-2 CONFIRMED real); X3 alone raises it; the fully-audited engine nets
UP to **0.405 > published 0.37** (not a cancellation — that was a mislabeled-camera error; see
ENV_VERIFICATION.md). The audit STRENGTHENS the headline; both confounds move the answer → validates D.
NB: `results_camera.json` is the OFF_OFF engine, NOT on_on (env-build finding, 2026-07-18).
| A.1.4 do-nothing baseline | DONE | results/dobest.json | grid beats do-nothing 7/7 |
| Gate analyzer | DONE | code/analyze_corners.py | now reads corner_on_on.json (camera was off_off) |
| A.1.2 gradtune 2×2 (script) | READY | code/gradtune.py | run after corners |
| A.1.3 held-out RMSE/NLL (script) | READY | code/heldout.py | run after corners |
| A.1.5 x0 inversion (script) | READY | code/x0_inversion.py | run after corners |
| A.1.6 3×3 coverage (script) | READY | code/coverage33.py | run after corners |
| Phase C venue | DONE | docs/AAAI27_VENUE.md | 4 AAAI-27 pages fetched |
| Phase D novelty | DONE | docs/NOVELTY_V2.md | Li/Rudner/Wilson owns ~90% of A findings |
| Phase B hyperresearch 2-16 | RUNNING | docs/hyperresearch/ | 2 agents |
| A.2 prereg contingent arms | DONE | docs/PREREGISTRATION_V2.md | M1/X11/X4 added, timestamped |
| Phase E blueprint v1 | DONE | docs/AAAI_BLUEPRINT.md | Part I PENDING; Part III pre-committed |

---

## Stage-0 experiments (branch `stage0-experiments`, 2026-07-18)

| unit | status | artifact | one-line |
|---|---|---|---|
| 0A.1 beta=0 reconciliation | **DONE** | docs/BETA0_RECONCILE.md, results/beta0_reconcile.json | disagreement was ENGINE (off_off vs on_on), not estimator |
| 0A.2 width ablation (W1/W2) | **DONE** | docs/WIDTH_ABLATION.md, results/width/ | W1 CONFIRMED: gap does not close with width |
| 0A.3 budget-matched (BM1) | RUNNING | code/budget_matched.py -> results/budget/budget_matched.json | 2 levels x 7 tasks x 30 seeds |
| V3 pre-registration | **DONE** | docs/PREREGISTRATION_V3.md (commit 55ced44) | committed BEFORE both launches |

**0A.1 verdict.** GATE_KBETA's 0.378 and the novelty audit's 0.504->0.511 are the same
estimator on different engines. Holding the estimator fixed and switching engine flips the
direction (off_off 0.496->0.516); holding engine fixed and switching estimator moves it
<0.02. Cause is X1: off_off the ensemble regresses raw y while both GPs z-score, which
handicaps it most at beta=0 where the mean fit is all that matters. on_on is correct.

`_gp_ens_gap` refits its min-max normalizer per beta, so 0.378 and 0.556 are in different
units. On a beta-invariant normalizer: gap(beta=0) = **0.319 [0.196, 0.460]**,
gap(beta=2) = **0.525 [0.406, 0.614]**, increment **0.203 [0.007, 0.396]**, p(<=0)=0.020
(task+seed bootstrap, 10k, normalizer refit inside each resample).

**Effect on C2.** Mean-quality base SURVIVES (CI excludes zero; 61% of the advantage is
present with sigma fully removed). "Independent of pessimism" DOES NOT: the increment is
significant. `paper/aaai27/main.tex:198` claims the paired difference has 95% CI
[-0.02, 0.10], "indistinguishable from zero" — refuted on the audited engine; that passage
and `supplement.tex:106` need rewriting to a base-plus-amplification claim. The cited
"0.51 -> 0.47" pair is reproduced by no traced computation and should be struck.

**Carry-forward.** Both V3 arms report on the beta-invariant normalizer for the same reason;
the incumbent per-condition estimator is reported alongside only where comparability with a
published figure is required.

**0A.2 verdict.** W1 CONFIRMED. At fixed K=5, sweeping member width 96 -> 1024 (10.7x) leaves
the GP-ensemble gap statistically unchanged: 0.480 [0.365, 0.576] at w=96 vs 0.476
[0.208, 0.647] at w=1024; shrinkage -0.006 [-0.210, 0.161], 99.1% of the w=96 value. The curve
is flat with noise, not a monotone decay, and no pre-registered KILL condition fires. The
NTK/spectral-bias objection (N5) is answered at practical widths; C2 mean-quality is a class
property, not a capacity artifact. Caveat: CI widens with w (0.211 -> 0.439), so "does not
close" is supported but "identical at w=1024" is not; nothing asymptotic in w may be claimed.

W2 SUPPORTED. Held-out normRMSE improves monotonically with w (0.4446 -> 0.3877). On the
registered tie-cell test (Styblinski-5D at w=256/512) the gap is 0.375. Non-registered but
stronger: the ensemble BEATS the GP's held-out RMSE on 7/7 tasks and 26/28 (task,w) cells and
at every width (0.388-0.445 vs 0.479) while still losing the optimization gap - the more
accurate surrogate is the one that loses, so accuracy is not the bottleneck. NLL is NOT a usable
second axis (GP mean NLL 202.7 vs ensemble 5.7-6.4 is a calibration artifact, not accuracy).

Validity: w=96 reproduces results/kbeta/grid_b2.0.json bit-exactly for grad and cma; perturb
differs within noise (median 0.0 SE, max 2.29 SE) because perturb_opt draws from the global
numpy RNG without reseeding, so its stream position depends on call order.

**C2 consequence.** Stop describing the GP advantage as "fits the function better" - it does not.
Describe it as: the ensemble's mean, though more accurate on-distribution, admits
off-distribution maximizers the oracle scores poorly. Combined with 0A.1 (survives sigma removal)
and 0A.2 (survives width increase), mean geometry under optimization is the remaining live
explanation.

