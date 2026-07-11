Pre-registered experimental contract (frozen before the n=30 runs)
===================================================================
Committed per plan section 5 Phase 0. Changes after data lands require a
logged amendment in this file, not silent drift.

Headline factorial
------------------
Grid: {ens, botorchgp, svgp} x {grad, perturb, cma} + ens_conformal:{grad,perturb}
      + baselines {coms, cbas, sparse_gp, grad_ascent, gp}  (mbo.OFFLINE_METHODS)
Tasks: Branin-2D, Styblinski-5D, Levy-8D, Rosenbrock-10D, Rastrigin-15D,
       Ackley-20D, Griewank-30D  (fixed datasets, seed-0 generation; per-seed
       randomness is training/init only — Design-Bench convention)
Seeds: n=30 floor, all cells.
       n=50 for pre-declared crossover-boundary tasks: Rosenbrock-10D,
       Rastrigin-15D, Ackley-20D (close comparisons need ~0.91 power; n=30
       gives ~0.72 there). Rerun at 50 recomputes those cells fully.
Metric: 100th-percentile (max) + 50th-percentile of top-128 oracle scores,
        128-candidate budget. Continuous metric for law analysis: normalized
        regret vs task optimum (ladder family exposes .optimum).
Commands:
  python run_all.py --exp all --seeds 30 --jobs 96
  python run_all.py --exp mbo --seeds 50 --jobs 96 --tasks Rosenbrock-10D Rastrigin-15D Ackley-20D

Statistics
----------
Pairwise: Wilcoxon signed-rank + Holm per family (powered by seeds).
Rank apparatus: Friedman + Nemenyi CD, INTERNAL 9-cell grid only, powered by
task count not seeds; pre-registered as possibly-null (CD ~3.0-3.8 vs spread ~8).
Never run CD against the cited SOTA zoo. Bootstrap CIs B=2000-10000.

Scaling-law ladder (STRETCH, gated)
-----------------------------------
Family: ScaledAckley, d in {2,5,10,20,50,100}, N = 250*d clamped [2000,25000];
density knob instrumented (Ackley{d}D-x{m}) but NOT run unless the dimension
law passes. Config diversity across ladder points via ensemble K in {3,5,10}
(existing K exp) — not pure seed replication. GP-kernel diversity: skipped.
Gate (all must pass before the law gets main-text space):
 (i) ladder run clean; (ii) same runs re-scored on normalized regret
 (continuous-metric falsification); (iii) mediation at d=5,10 — conformal
 repair (ens_conformal:*) must move the ens-vs-GP optimizer gap in the
 predicted direction; (iv) only then full sweep/density.
Crossover statistic: log ensemble/GP optimizer-spread ratio (bounded
transform preferred; raw ratio has denominator instability).

Design-Bench arm
----------------
Subset: TFBind8 (d=32), TFBind10 (40), Superconductor (86), + Hopper (5126)
as the high-d anchor if the env builds. n=16 (community standard; DB oracle
calls are the costly step). NO seed-dependent significance claims on DB —
direction-of-crossover evidence only. Baselines run by us: coms, cbas, cma,
grad_ascent (+ BO-qEI if design-baselines env builds). DDOM/BONET/RaM/ExPT:
cited, not re-run.

Decision rule (STRETCH)
-----------------------
Two axes only ({GP, ensemble} x {grad, perturb}); fit boundary on all-but-one
task from (d, held-out calibration probe); predict held-out task's better arm;
report hit-rate vs always-GP and always-ensemble, leave-one-task-out. Fails
either trivial baseline -> reported honestly and dropped.

Washout contingency (pre-committed)
-----------------------------------
If the n=30 optimizer x surrogate interaction is small/non-significant, the
headline pivots to the calibration mechanism (coverage collapse + conformal
repair breaking under proposal shift), which is independent of crossover
magnitude; the factorial is then reported as a powered controlled null.
