# Failures log — resume commands

Every unit that could not complete is logged here with a resume command, per the session
contract (API failure: retry 3×, then log + continue; MISSING means MISSING).

## F-1 · Design-Bench corners not runnable this machine — **RESOLVED (Stage 2) 2026-07-18**
**Original claim (superseded):** `design_bench` impractical to install on this Mac (thought to
need TF 1.x + mujoco).
**Resolution:** `envs/mac-db` (py3.9, design-bench 2.0.20, numpy 1.23.5, sklearn 1.0.2, torch 2.8,
botorch 0.10, gpytorch 1.11) now builds and runs the **five non-mujoco Design-Bench tasks**
(TFBind8, TFBind10, Superconductor, GFP, UTR — including both exact-oracle tasks) with the full
9-cell grid. Build recipe + patches: `docs/ENVIRONMENTS.md`, `envs/mac-db-requirements.lock`,
`envs/mac-db-patches/fix_designbench_macos.py`. Verification: `docs/ENV_VERIFICATION.md` (GP cells
reproduce `results_db.json` exactly; ensemble cells drift by platform RNG — a disclosable finding).
**Still MISSING (Stage 3):** Ant, D'Kitty, Hopper (mujoco at import via morphing-agents; arm64
hard). Run those on the RunPod Linux pod (`cloud/setup.sh`). Not fabricated.
**Resume (DB four corners, Stage-2 tasks):** commands in `docs/ENVIRONMENTS.md` (require
`MBO_SPAWN=1`; TFBind10 in a low-concurrency pass; ~3–8 h/corner).
**Resume (on a box with design_bench):**
```
# per corner tag in {off_off, on_off, off_on}:
MBO_X1=<0|1> MBO_X3=<0|1> python code/run_all.py --exp mbo --db --db-subsample 8000 \
  --seeds 16 --jobs <N> --out results/corners/corner_<tag>_db.json \
  --methods ens:grad ens:perturb ens:cma botorchgp:grad botorchgp:perturb botorchgp:cma \
            svgp:grad svgp:perturb svgp:cma
```
Impact on the gate: the reproduction gate and the X1/X3 disentangling run on **synthetic**
(the paper's headline η² is synthetic); the DB corner is a robustness extension, not the
gate itself. Recorded as a residual in the blueprint (Part V).

## F-2 · Background jobs killed mid-run (~22:38); resumed
**What:** the harness-tracked corners job and the post-corner chain were both `killed`
simultaneously (not a crash — disk 7.2 GiB free, no error in logs). Likely a system sleep or
a background-job reap. State at kill: off_off complete (repro PASS holds), on_off ~8% done,
off_on not started.
**Recovery:** `run_all.py` is merge-safe, so on_off resumed from its 150 completed cells with
no loss. Relaunched via an **idempotent** driver detached with `nohup`
(`<scratchpad>/run_all_arms.sh`): it skips complete corners (run_all `have()` check) and any
arm whose output JSON already exists, so a further kill costs at most one in-flight arm.
**Resume (if killed again):** just re-run
`nohup bash <scratchpad>/run_all_arms.sh > logs/all_arms.log 2>&1 &` — it picks up where it
left off. All arm outputs land in `results/` and `results/corners/`.
