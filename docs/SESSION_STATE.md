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
| P3 K-beta gate | RUNNING | results/kbeta/ | 5 beta grids + kbeta ens sweep + bootstrap + analysis |

**RESUME (P3 if interrupted):** `nohup bash <scratchpad>/run_phase3.sh > logs/pod_phase3.log 2>&1 &`
(run_all merge-safe; kbeta re-runs whole). Then re-run kbeta_analyze.py.

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
