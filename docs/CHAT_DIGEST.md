# Chat digest

For the judgment-layer instance, which has only the compiled PDF. Facts it cannot infer.
Every claim below is verified against code or artifacts; `MISSING` means MISSING.

## What exists

One engine (`code/mbo.py`, 632 LOC) implements all three surrogates, all three optimizers,
the LCB closures, conformal repair, and the evaluation protocol. `run_all.py` drives it;
`run05.py` computes the paper's η²/CD/TOST; `figures.py` and `tables.py` emit
`paper/figures_v2/*` and `paper/tables_v2/*`. The paper is `paper/aaai27/main.tex` (298 LOC).

**The grid is complete and the headline numbers are real.** Synthetic 112/112 cells at exactly
30 seeds; Design-Bench 63/63 grid cells at exactly 16. η² reproduces from the primary artifacts
**to 8 decimal places** (0.36872274336…). This is not a case of invented numbers.

## The ten facts that matter

**1. The repo contains a control that refutes the paper's mechanism, and the paper omits it.**
`code/gradtune.py` exists solely to test "is the ensemble's gradient collapse just an under-tuned
optimizer?" It pre-states the rule: *"If even the best-tuned gradient config still underperforms
perturbation, the collapse is surrogate geometry (genuine), not tuning."* Its own results
(15 seeds, `results/results_gradtune.json`) **fail that rule on 3 of 4 tasks.** `grad_default` is
bit-for-bit the grid's optimizer (`lr=0.05, steps=100`). A trust region moves Branin −8.17 → −0.54
and Styblinski 5.56 → 34.30; on Ackley plain gradient already beats perturbation (−3.77 vs −6.41).
Commit `cdd5ad8`'s message says it outright: *"trust region closes the ensemble gradient collapse."*
The word "trust" appears nowhere in `main.tex`. **This is the single largest risk in the project.**

**2. The ensemble trains on raw targets; both GPs z-score.** `mbo.py:36` stores raw oracle values;
`train_ensemble` (`mbo.py:130`) does MSE on them at `lr=3e-3` for 35 fixed epochs. `botorchgp`
(`mbo.py:255`) and `svgp` (`mbo.py:311`) both standardize. Targets span ~2.5 orders of magnitude
(Griewank ≈ −2600, Branin ≈ −10), so the ensemble's loss on Griewank is ~10⁶. **η²_surr = 0.37 is
confounded with target scaling**, and the GP−ensemble gap tracks |y| scale exactly as Table 1 shows.
`main.tex:93` claims "all scores are min-max normalized" — true only in the *analysis*, not training.

**3. The stated identifiability license is false.** `main.tex:91`: *"candidate budget … and oracle
scoring are held identical. This shared closure is what licenses attributing score differences to
the surrogate×optimizer factors."* In fact `init_candidates` returns **256**, not 128 (`mbo.py:384`);
gradient returns the final iterate, perturbation per-slot best-ever, CMA top-128-by-surrogate — three
different rules. Then `eval_designs` calls the **oracle on all of them** and keeps its top 128
(`mbo.py:392`). So grad/perturb get **256 oracle calls**, CMA gets 128, and `p50` is a top-half
median for two optimizers and a full-set median for the third — **two estimands, one column**.

**4. Optimizer budgets differ by 6×–59×.** Surrogate forward-evals per cell: gradient 25,600;
perturbation 4,096; CMA 432 (d=2) to 3,012. CMA is starved worst on exactly the low-d tasks carrying
the headline. No eval counter exists in the repo.

**5. Coverage is measured for 1 of 9 cells.** `run_calibration` hard-codes ensemble (`mbo.py:583`)
and gradient (`mbo.py:598`). Ens×CMA coverage: **MISSING**. The cross-proposal claim (0.97) comes
from `run_gpcov.py`, which takes ensemble proposals from *gradient* and GP proposals from
*perturbation* — **both factors move together** — and uses **sklearn's GP, not the grid's**.

**6. Six reported quantities have no generator.** `05_findings.json` keys `bootstrap_ci`, `beta0`,
`subsample_control`, `gp_coverage`, `stats_9cell`, `rf_robustness` are **written by nothing in the
repo**. `main.tex:137` describes a *task-and-seed* bootstrap for the η² CIs; both bootstraps in the
repo resample **tasks only**, on seed-collapsed means, and produce mean-*ranks*. Also `run_all.py:60`
writes `rho_knn`, absent from both live artifacts: **the current code does not reproduce the current
artifacts.**

**7. A headline claim reverses.** The "in-distribution coverage below nominal" claim (0.77 real) is
carried entirely by GFP = 0.00, which **the supplement itself calls a degenerate decode artifact**.
Excluding GFP the mean is 0.895 ≈ 0.90. Separately, DB "in-distribution" coverage samples
`uniform(0,1)` (`mbo.py:591`) while DB data are one-hot **vertices** — measured off-distribution.

**8. Offline selection (5.1) FAILS — but for a reason worth publishing.** Ran as pre-registered;
kill criterion fires. Regret 0.348 vs the honest fixed-cell baseline's 0.233 — **identical to random**.
Two reasons, both structural: (a) **`ĉ_ood` is not oracle-free** — it evaluates true *f* on the
proposals, the one query offline MBO forbids (`mbo.py:599`); the oracle-free feature set spanning all
14 tasks is **one binary flag**. Oracle-*contaminated* features *do* carry signal (regret 0.171,
7W/2L). **The predictive signal lives precisely in the quantity offline MBO cannot compute.** (b) At
n=14, even a *perfect* rule reaches d_z = 0.71 vs the 0.81 needed for 80% power — **no rule could have
been certified at this n**. Identity B is dead; but (b) is a *power result* that hands Contribution 3
a real spine.

**9. The pre-registration contradicts the paper.** `PREREGISTRATION.md` registered the headline as
*"the optimizer explains most of the gap"* — the data gave η²_opt = **0.01**, the opposite. It also
forbade DB significance claims (*"NO seed-dependent significance claims on DB"*) which the paper makes
(p=0.69/0.93, TOST), and mandated n=50 reruns on three tasks that were **never run**. The paper never
cites it. Disclosed, the refutation is a credibility asset; discovered, it reads as HARKing.

**10. Novelty is thinner than the draft assumes.** The *factorial design* — NONE FOUND, genuinely
novel. But Li/Rudner/Wilson (**ICLR 2024**, miscited as 2024 in a bib entry keyed `li2024bnnsurrogates`
— verify) already reports "deep ensembles perform relatively poorly" and "ranking is highly
problem-dependent, suggesting the need for tailored inductive biases," with acquisition fixed. Prop 1
is an identity with prior art (Jin et al. 2021) — demote to a remark. Prop 2 restates Tibshirani 2019.
"Surrogate smoothness helps offline optimization" is established (MS-DDEO 2022 grades a surrogate pool
*by smoothness*; the Kim TMLR survey lists smoothness priors/RoMA). **What survives: the factorial
itself, the offline setting, and attribution to mean-smoothness-not-calibration** — and that last one
is exactly what facts 1 and 2 currently undermine.

## What runs, what's reproducible

Runs: the full grid, all controls, the figures/tables. Reproducible: η² exactly; the grid.
**Not** reproducible: the CIs, β=0, subsample, gp_coverage, rf_robustness (no generator);
`rho_knn` (code writes it, artifacts lack it). Zero provenance in any artifact — no timestamp,
git sha, or config block anywhere; seeds are positional (`range(seeds)`).

## Bottom line

The measurement is real and complete. The *controls are asymmetric in the ensemble's disfavour on
both axes simultaneously* — unnormalized targets on the surrogate axis, unequal oracle budget and
three selection rules on the optimizer axis — and the repo's own tuning sweep says the mechanism is
a tuning artifact. Both headline effects are confounded with implementation choices the paper
explicitly claims are held constant. **All of it is cheap to fix**: normalize `y`, equalize the
protocol, re-run once. If η²_surr survives, the paper is far stronger than it reads now. Nothing
downstream should be trusted until that run exists.
