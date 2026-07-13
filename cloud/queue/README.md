# Run queue — AAAI-27 attribution study

Numbered, dependency-ordered. **Lower number = produces data that later steps need.**
Every sim is merge-safe and resumable (re-running skips completed cells), so a killed
spot instance just picks up where it left off. Thread-pinned (`OMP_NUM_THREADS=1`) to
avoid the oversubscription slowdown.

## The dependency DAG

```
01 synth factorial  ──► (GATE-1 verdict) ──► 02 real DB factorial ──► 05 analyze
   (unmatched+matched)                          (needs 01 for transfer)   (needs 01-04)
        │                                    03 official baselines ──────►┤
        └──► 04 calibration (synthetic) ─────────────────────────────────┘
```

Run order and *why that order*:

| # | Script | Produces | Needs | Env | Est. GPU/CPU-h |
|---|--------|----------|-------|-----|----------------|
| 00 | `00_smoke.sh` | sanity (2 min) — env + self-checks | — | main | trivial |
| 01 | `01_synth_factorial.sh` | **GATE-1 data** + synthetic SEI/OEI + transfer baseline. `results_camera.json` (unmatched) + `results_camera_matched.json` | — | main | ~30-60 CPU-h |
| 02 | `02_db_factorial.sh` | real SEI/OEI + β=0 ties + real ranking. `results_db.json` + `results_db_matched.json` | 01 (for transfer) | db (+mujoco) | ~120-200 CPU-h |
| 03 | `03_official_baselines.sh` | official COMs/CbAS/… on the core tasks | — (independent env) | baselines | best-effort |
| 04 | `04_calibration.sh` | Tier-3 coverage diagnostic (synthetic) | — | main | ~10-20 CPU-h |
| 05 | `05_analyze.sh` | SEI/OEI tables, GATE verdict, transfer, Welch+Holm, TOST, CD, figures. NO GPU. | 01-04 | main | minutes |

**Start with 01.** It is the single most load-bearing run: it produces the GATE-1
matched-vs-unmatched comparison that decides whether the paper's headline holds or
reframes, *and* the synthetic baseline every transfer claim compares against. 02 can
only make its transfer claim once 01 exists. 05 consumes everything and is re-runnable
after each sim finishes (run it incrementally to watch results land).

## GATE-1 (read this before committing the real runs)

After 01, `run_queue.sh` prints the GATE-1 verdict (`analysis.py --gate`). It answers:
**does the surrogate-class effect survive matched tuning?**
- **SURVIVES** → proceed to 02+ as planned; the attribution headline holds.
- **DOES NOT SURVIVE** → the surrogate effect was a tuning-budget artifact. Do NOT
  panic — the paper reframes to "reported surrogate-class gains are a fair-tuning
  artifact," which is *still* the paper, and 02 still runs (the reframe needs the same
  real data). But you'll want to know before spending the real-task compute.

## Running it

```bash
bash cloud/queue/run_queue.sh            # 00 → 05 in order, GATE-1 surfaced after 01
# or individually, one at a time:
bash cloud/queue/01_synth_factorial.sh
bash cloud/queue/05_analyze.sh           # re-run anytime to see current results
JOBS=48 bash cloud/queue/02_db_factorial.sh   # override worker count
```

Logs land in `cloud/queue/logs/`. Envs are built by `cloud/setup.sh` (+ `fix_designbench.sh`).
Mujoco (Ant/DKitty in 02) is best-effort on headless boxes; if it fails those two tasks
fail-soft and the core drops to TFBind8/10 + Superconductor.
