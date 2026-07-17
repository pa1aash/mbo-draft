# Failures log — resume commands

Every unit that could not complete is logged here with a resume command, per the session
contract (API failure: retry 3×, then log + continue; MISSING means MISSING).

## F-1 · Design-Bench corners not runnable this machine
**What:** Phase A.1.1 also calls for Design-Bench @16 seeds across the four corners, and
A.1.5/A.1.6 reference DB. `design_bench` is not installed and is impractical to install
here (needs TensorFlow 1.x + mujoco; ~8 GiB disk free at session start).
**Status:** MISSING. Not fabricated. The (on,on) DB numbers already in the manuscript come
from `results/results_db.json` (generated off-machine); the three missing DB corners are
NOT computed.
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
