# Flaw ledger — "Decomposing the GP Advantage in Offline MBO"

Merged and deduplicated from the implementation audit, the claim-provenance trace,
the artifact inventory, and the adversarial threat list (T1–T12). Sorted by severity,
then by fix cost.

**Evidence rule.** Every row cites `file:line` or a PDF/`.tex` location. Nothing here
is inferred from the manuscript alone. Where an artifact is absent the row says
MISSING rather than reconciling.

Severity: **P0** reject-driver · **P1** major-revision demand · **P2** minor · **P3** polish.

---

## P0 — reject-drivers

### P0-0 · The authors' own control refutes the paper's mechanism, and the paper does not report it
**Claim at risk:** the ensemble×gradient collapse — i.e. the premise of Contribution 2 and the
subject of Figure 4 and all of Section 5.

**This is the most serious finding in this ledger.** It is not an outside objection. It is the
authors' own pre-stated test, run, failed, and unreported.

**Evidence.** `code/gradtune.py:1-5` states its own purpose and decision rule verbatim:

> *"Robustness sweep rebutting the #1 reviewer objection: 'the ensemble's gradient-ascent collapse
> is just an under-tuned optimizer.' … **If even the best-tuned gradient config still underperforms
> perturbation, the collapse is surrogate geometry (genuine), not tuning.**"*

`gradtune.py:22` defines `grad_default = dict(lr=0.05, steps=100)`. That is **exactly** the main
grid's gradient optimizer: `mbo.py:26-27` `OPT_STEPS=100`, `LR_OPT=0.05`, and `mbo.py:166`
`grad_opt(..., steps=OPT_STEPS, lr=LR_OPT, normalize=False, trust=None)`. The comparison is direct.

Means over 15 seeds from `results/results_gradtune.json` (higher is better):

| Task | perturb | grad_default (= the grid's) | best gradient config | verdict by the script's own rule |
|---|---|---|---|---|
| Branin-2D | −0.792 | **−8.174** | **−0.543** (`grad_trust`) | gradient **beats** perturb |
| Styblinski-5D | 33.008 | **5.557** | **34.295** (`grad_besttuned`) | gradient **beats** perturb |
| Rosenbrock-10D | −0.116 | −0.275 | −0.138 (`grad_gentle`) | perturb wins (narrowly) |
| Ackley-20D | −6.405 | −3.767 | **−3.731** (`grad_gentle`) | gradient **beats** perturb decisively |

**By the script's own criterion the collapse is NOT surrogate geometry. It is tuning — on 3 of 4 tasks.**
A single trust-region hyperparameter (`trust=0.1`) moves Branin from −8.17 to −0.54 (**15×**) and
Styblinski from 5.56 to 34.30 (**6×**). The paper's Table 1 reports Branin Ens×Grad = −9.27, consistent
with the untuned `grad_default`.

Commit `cdd5ad8`'s own message records the result: *"Smoke: trust region closes the ensemble gradient
collapse."*

The manuscript never mentions it. The string "trust" does not appear in `main.tex`. The only tuning
control in the paper (`main.tex:94`) is **matched tuning**, which *removes the GP's* hyperparameter
budget and gives the ensemble and the gradient optimizer **nothing** — precisely the asymmetry T1
predicted.

**Reviewer's phrasing:** "The released code contains a gradient-tuning sweep whose stated purpose is to
test whether the collapse is a tuning artifact. It concludes that it is: a trust region closes the gap
on three of four tasks, and on Ackley plain gradient ascent already beats perturbation. This result is
absent from the paper. The central mechanism is an artifact of one untuned optimizer setting."

**Fix.** There is no way to fix this by argument — only by reporting it. Three honest options:
1. **Re-scope.** The finding becomes "the ensemble's gradient collapse is a *trust-region* failure, and
   the LCB premise-coverage diagnostic *predicts which configurations collapse*." That is still a real
   contribution and it makes the diagnostic **predictive**.
2. **Re-run the grid with a tuned gradient optimizer** on the ensemble and report what survives. If
   η²_inter = 0.17 evaporates, say so.
3. **Report the sweep as a limitation.** Weakest option; a reviewer who opens the artifact finds it anyway.

**Cost:** 0 h to disclose. ~1 grid re-run to re-scope properly (combine with P0-2's re-run — one pass).
**Fixable:** yes. **Blocks submission:** **yes — unconditionally.** Shipping a mechanism claim that the
repo's own control refutes, with the refuting result in the released artifact, is the single largest
risk in this project.

**Caveats, stated honestly.** gradtune is 4 tasks × 15 seeds, not 7 × 30; it compares gradient against
`perturb` only, not against the full 3×3 grid; and it uses the grid's default ensemble, so it inherits
P0-2's unnormalized-target problem. None of these caveats rescue the paper — they are reasons the sweep
should be *run properly and reported*, not reasons to omit it.

---

### P0-1 · The identifiability license is factually false against the code
**Claim at risk:** the entire causal attribution — every η², the whole decomposition.

**Evidence.** `main.tex:91` states: *"the data split, candidate budget, input normalization,
and oracle scoring are held identical. This shared closure is what licenses attributing
score differences to the surrogate×optimizer factors rather than to incidental protocol
choices."* `main.tex:93`: *"Each method proposes 128 candidates."*

The code does none of this:
- `mbo.py:384-389` `init_candidates` returns `concat([xt, xp])` = **256** rows (`TOP=128`, `mbo.py:25`).
- `mbo.py:188` gradient returns the **final iterate** of all 256.
- `mbo.py:198-201` perturbation returns **per-slot best-LCB-ever** over 256 slots.
- `mbo.py:292` CMA returns **top-128 by surrogate LCB** — i.e. 128 rows.
- `mbo.py:392-394` `eval_designs` then calls `task.oracle(x_final)` on **whatever it is handed**
  and keeps `np.sort(sc)[-128:]`.

Consequence: gradient and perturbation consume **256 oracle calls** and report the best 128;
CMA consumes **128** and its `[-128:]` slice is the identity. So `p50` is *the median of an
oracle-selected top half* for grad/perturb but *the median of the entire unfiltered proposal
set* for CMA — **two different estimands reported in one column**. The optimizer factor is
confounded with a 2× oracle budget and with the candidate-selection rule.

**Reviewer's phrasing:** "The paper's stated justification for causal attribution is that the
candidate budget and oracle scoring are held identical. They are not. Two of three optimizers
receive twice the oracle budget, and the p50 metric is not the same quantity across the
optimizer axis. The decomposition is not identified."

**Fix:** equalize to 128 proposals per cell, apply one selection rule, and never let the oracle
choose the reported set. Re-run the grid. **Cost:** ~2 h edit + full grid re-run (see P0-2 —
do them in one re-run). **Fixable:** yes. **Blocks submission:** yes.

---

### P0-2 · The ensemble trains on unstandardized targets; both GPs z-score
**Claim at risk:** η²_surr = 0.37 — the headline — and the "inductive bias" mechanism.

**Evidence.**
- `mbo.py:36-37` `Task.__init__`: `s.y = (s.oracle(s.x) + noise)` — **raw** oracle values, never normalized.
- `mbo.py:130-138` `train_ensemble(x, y, ...)`: `TensorDataset(FloatTensor(x), FloatTensor(y))`
  → MSE on **raw** `y`, `lr=3e-3`, `35` epochs unconditional, `weight_decay=1e-4` the only regularizer.
- `mbo.py:255` `botorchgp`: `yt = (yt - yt.mean()) / (yt.std() + 1e-8)` — **standardizes**.
- `mbo.py:311-312` `svgp`: standardizes, and `mbo.py:342` inverts it back.

Target scale varies by ~2.5 orders of magnitude across the suite (Griewank ≈ −2600, Branin ≈ −10;
`mbo.py:41-70`). At fixed `lr` and fixed epoch count with no target normalization, the ensemble's
MSE on Griewank is ~10⁶ and it cannot fit; on Branin it can. **The GP−ensemble gap should therefore
track the task's |y| scale — which is exactly the pattern Table 1 shows.**

`main.tex:93` claims *"all scores are min-max normalized."* That normalization exists only in the
**analysis** (`analysis.task_norm`), not in the training path.

**Why this is the #1 reject risk:** "inductive bias" and "the ensemble was handed unnormalized
targets" are observationally equivalent under every control the paper runs. The β=0 control does
not separate them (standardizing the GP's `y` is an affine monotone transform of its LCB, so β=0
leaves the GP's *ranking* untouched while the ensemble's *training* pathology persists). The
matched-tuning control removes the GP's tuning but never gives the ensemble normalization.

**Reviewer's phrasing:** "The ensemble regresses on raw targets spanning −2613 to +36 while both
GP surrogates standardize. The surrogate main effect may be a target-scaling artifact. Normalize
and re-run before claiming an inductive-bias mechanism."

**Fix:** standardize `y` in `train_ensemble` (2 lines), re-run. **Cost:** ~30 min edit + full grid
re-run. **Fixable:** yes — and this is also the decisive experiment (see PREREGISTRATION.md).
**Blocks submission:** yes. **This must be run before anything else in the paper is trusted.**

---

### P0-3 · Premise coverage is measured for 1 of 9 cells; the cross-proposal claim varies two factors at once
**Claim at risk:** Contribution 2 in full — the 0.73 / 0.41 / 0.97 abstract numbers and the
"ensemble×gradient interaction, not a surrogate defect" attribution.

**Evidence.**
- `mbo.py:583` `run_calibration` hard-codes the **ensemble**; `mbo.py:598` hard-codes **gradient**.
  It takes no surrogate/optimizer argument. `run_all.py:74` passes a single dummy variant `['_']`.
  → coverage exists for **`ens:grad` only**.
- `run_gpcov.py:34` takes ensemble proposals from **gradient**; `run_gpcov.py:35` takes GP proposals
  from **perturbation**. Both factors move together, so the resulting contrast cannot separate
  "ensemble×gradient interaction" from "gradient travels further OOD."
- `run_gpcov.py` uses **sklearn's** GP, not the grid's `botorchgp` — a different model from the one
  the decomposition scores.

**Reviewer's phrasing:** "The interaction claim rests on a comparison in which surrogate and
optimizer change simultaneously, evaluated with a GP that is not the GP in the grid. This is the
exact confound the paper was written to eliminate."

**Fix:** parameterize `run_calibration` over the full 3×3 and recompute. **Cost:** ~3 h edit +
~1 CPU-day. **Fixable:** yes. **Blocks submission:** yes.

---

### P0-4 · Reported numbers whose generating code does not exist in the repo
**Claim at risk:** the η² confidence intervals, the β=0 control, the subsample control, the
GP-coverage panel, the 9-cell stats, the RF-robustness defense.

**Evidence.** `main.tex:137` reports *"task-and-seed bootstrap 95% CIs … (non-overlapping)."*
Nothing in the repo bootstraps seeds or η². Both bootstrap implementations (`stats.py:151`,
`run05.py:99`) resample **task indices only**, on seed-collapsed means, and produce mean-*ranks* —
not η². The values live in `05_findings.json` under keys `bootstrap_ci`, `beta0`,
`subsample_control`, `gp_coverage`, `stats_9cell`, `rf_robustness` — **none of which `run05.py`
ever writes**.

Separately, `run_all.py:60` still writes `rho_knn`, a field absent from both live result files:
**the current code does not reproduce the current artifacts.**

**Reviewer's phrasing:** "We could not reproduce the confidence intervals from the released code.
The described bootstrap resamples seeds; the code resamples tasks."

**Fix:** write the missing generators, or delete the claims. **Cost:** ~4 h. **Fixable:** yes.
**Blocks submission:** yes — an artifact whose code does not produce its own numbers fails the
reproducibility checklist.

---

### P0-5 · A headline coverage claim reverses when a task the supplement itself calls degenerate is removed
**Claim at risk:** "moderately covered in-distribution (0.73, below the nominal 0.90)" and the real-task
coverage story.

**Evidence.** The 0.77 real-task in-distribution coverage is driven by GFP = 0.00, which the supplement
itself describes as a degenerate decode artifact. **Excluding GFP the mean is 0.895 ≈ 0.90** — so
"below the nominal 0.90" **reverses**. Full trace in `docs/PROVENANCE.md`.

Compounding it: `mbo.py:591` draws the "in-distribution" reference set as `np.random.uniform(0,1,(500,dim))`.
Design-Bench data are one-hot cube **vertices** (`db_tasks.py:63`) or normalized real measurements
(`db_tasks.py:66`) — **not** uniform on the cube. The DB "in-distribution" coverage is therefore
measured off-distribution. Valid for synthetic (where the data *are* uniform); invalid for the entire
right panel of Figure 3.

**Reviewer's phrasing:** "The claim that in-distribution coverage falls below nominal is carried
entirely by a task the authors call degenerate, and the in-distribution reference set is not drawn
from the data distribution."

**Fix:** drop or quarantine GFP; sample the reference set from `D`. **Cost:** ~2 h + recompute.
**Fixable:** yes. **Blocks submission:** yes.

---

### P0-6 · Figures 1 and 3 report different Design-Bench mean ranks for the same cells
**Claim at risk:** figure integrity; by extension every rank-based claim.

**Evidence.** 6 of 9 Design-Bench cells disagree between Fig 1 and Fig 3. GP×Pert is **3.4** in Fig 1
but **3.6** in Fig 3, in the body text, and in the supplement (3.57). Both sets sum to ≈45, so these are
two internally-valid but *different* rankings — i.e. two different data sources. Synthetic panels agree
perfectly, which rules out a presentational cause. This hits the paper's headline Design-Bench cell.
Full trace in `docs/PROVENANCE.md` (INC-1).

**Reviewer's phrasing:** "Figures 1 and 3 disagree about the same quantity. Which is correct?"

**Fix:** regenerate both from one source. **Cost:** ~1 h once P0-4's generators exist. **Fixable:** yes.
**Blocks submission:** yes.

---

### P0-7 · A load-bearing sentence states the arithmetic backwards
**Claim at risk:** the RF-oracle defense of the central null — i.e. Contribution 3's validity.

**Evidence.** The paper argues *"the median 9-cell spread (0.34) is no smaller than … (0.39)."*
**0.34 is smaller than 0.39.** The sentence is literally false, in both main and supplement, and it is
the defense of the paper's most attackable claim. (`docs/PROVENANCE.md`, INC-4.)

Related: the RF-oracle defense numbers (p=0.93, 0.34, 0.39) have **no table or figure** anywhere —
body-only. So does TOST ±0.48.

**Reviewer's phrasing:** "The claim's own numbers contradict it."

**Fix:** recompute and rewrite. **Cost:** ~1 h. **Fixable:** yes. **Blocks submission:** yes.

---

## P1 — major revision demands

### P1-1 · Optimizer surrogate-query budgets are unmatched by 6×–59×
**Evidence.** Measured surrogate forward-evaluations per cell: gradient `1×100×256 = 25,600`;
perturbation `(1+5×3)×256 = 4,096`; CMA `popsize×generations` = **432 (d=2) to 3,012 (d≥20)` —
pycma's tolerance criteria halt it well below `maxfevals=3000` at low d. Gradient gets **6.25×**
perturbation and **8.5–59×** CMA. No eval counter or shared budget constant exists anywhere in the repo.
CMA is starved worst on exactly the low-d tasks that carry the headline.

**Reviewer's phrasing:** "'Optimizer' is confounded with search intensity. 'Use a conservative
optimizer' may just mean 'search less.'"

**Fix:** budget-matched arm at equal surrogate queries. **Cost:** ~1 CPU-day. **Fixable:** yes.

### P1-2 · The ANOVA is hand-rolled, has no error term, and leaves `task` unmodeled
**Evidence.** `run05.py:26-48` — no statsmodels anywhere in the repo. η² is computed on **63 cell
means** with `task` unmodeled, so there is no F, no p, no df, and the denominator is inflated by
between-task variance. Two inconsistent normalizations coexist: η² uses 9 cells (`run05.py:35`),
while SEI/OEI, GATE-1, and the rank/CD/TOST matrix use `analysis.task_norm`, which matches any key
containing `':'` and therefore spans **11** cells — silently including the `ens_conformal:*` arms.

**Reviewer's phrasing:** "η² without an error term is not an effect size; and the rank analysis
includes methods the grid section never defines."

**Fix:** proper mixed model or a permutation effect size; unify the normalization. **Cost:** ~4 h.
**Fixable:** yes.

**A citable reviewer objection lands exactly here.** Benavoli, Corani & Mangili, *Should We Really Use
Post-Hoc Tests Based on Mean-Ranks?*, **JMLR 17(5):1-10, 2016**, verbatim:

> "the outcome of the mean-ranks test depends on the pool of algorithms originally included in the
> experiment ... the difference between A and B could be declared significant if the pool comprises
> algorithms C, D, E and not significant if the pool comprises algorithms F, G, H"

Our rank/CD/TOST matrix runs through `analysis.task_norm`, which matches any key containing `':'` and
therefore **silently pools 11 cells, including the `ens_conformal:*` arms the grid section never defines**.
So the CD conclusions demonstrably depend on a pool the paper does not disclose — Benavoli's objection is
not hypothetical here, it is instantiated. Their recommendation is to use tests whose "outcome only
depends on the two algorithms being compared, such as the sign-test or the Wilcoxon signed-rank test."
Demsar's canonical cite is **JMLR 7(1):1-30, 2006**; Garcia & Herrera (**JMLR 9(89):2677-2694, 2008**)
give Holm/Shaffer/Bergmann-Hommel alternatives to Nemenyi for all-pairwise comparisons.

### P1-3 · The ensemble is unregularized, unvalidated, and never early-stopped
**Evidence.** The complete regularization list is `weight_decay=1e-4` (`mbo.py:23,137`). No dropout,
no norm layers, **no validation split of any kind**; `mbo.py:140` `for _ in range(ep):` runs 35 epochs
unconditionally. Members differ **only** by `torch.manual_seed(seed*100+k)` (`mbo.py:135`) — init and
shuffle order; **no bootstrap resampling**, all 5 members see identical data. `sigma = ps.std(0)`
(`mbo.py:155`) with no noise term and **no floor**, while GP and SVGP both clamp (`mbo.py:265,342`).

Held-out predictive error of ensemble vs GP per task is **MISSING** — the repo never computes it.
Without it, "inductive bias" cannot be distinguished from "fits worse." See P0-2.

**Fix:** add a validation split and report held-out NLL/RMSE per task per surrogate. **Cost:** ~3 h.

### P1-4 · Design-Bench significance claims violate the paper's own pre-registration
**Evidence.** `PREREGISTRATION.md:50-52`: *"n=16 … **NO seed-dependent significance claims on DB** —
direction-of-crossover evidence only."* The paper reports Friedman p=0.69/0.93 and a TOST bound on DB.
Also unrun: the pre-registered `n=50` reruns for Rosenbrock-10D / Rastrigin-15D / Ackley-20D
(`PREREGISTRATION.md:14-16`, which states n=30 gives only ~0.72 power there) — grep finds no `--seeds 50`
anywhere. The paper never cites the pre-registration.

**Fix:** honor it, or state the amendment. **Cost:** 0 h to disclose; ~2 CPU-days to run n=50.

### P1-5 · The registered hypothesis was refuted and the paper does not say so
**Evidence.** `SKELETON.md:11,30` registered the headline as *"the acquisition optimizer explains most
of the reported gap."* The paper reports **η²_opt = 0.01** — the opposite. The shipped Contribution 3
(the DB null) replaced a planned offline-to-online protocol contribution (`SKELETON.md:16,26`).

This is a *strength* if disclosed: a refuted pre-registered prediction is evidence of a real test.
Undisclosed, it reads as HARKing to anyone who sees the repo.

**Fix:** one paragraph. **Cost:** ~1 h. **Fixable:** yes — and it *raises* credibility.

### P1-6 · COMs reproduction diverges from official by 1.22 normalized units
**Evidence.** ours 2.21 vs official 0.99 on TF-Bind-8; `main.tex:158` quotes that cell ("2.20 on
TF-Bind-8" — itself a third value). Supplement Table 4's CbAS TF-Bind-8 row computes `2.13 − 2.12 = 0.01`
but the |Δ| column says **0.004** — the single "matches official" number does not verify against its own row.

**Reviewer's phrasing:** "Their baselines are wrong, so the null is theirs, not the field's."

**Fix:** diff against the official repo's hyperparameters. **Cost:** ~1 day. **Fixable:** partly.

### P1-7 · Propositions 1 and 2 carry no content
**Evidence.** `proofs.md:10` — Prop 1's entire proof is *"The two events coincide as subsets of X, so
they have equal probability under any Q."* It is an identity. Prop 2 is textbook split-conformal plus a
**restatement** of Tibshirani et al. 2019's weighted-conformal extension (`proofs.md:20-22`), and the
weighting is never implemented — `proofs.md` concedes the repair is not run.

**Reviewer's phrasing:** "Proposition 1 is a tautology and Proposition 2 is a known result restated.
Neither is a contribution."

**Fix:** either cut to a remark, or find a bound with content (see `docs/MECHANISM_EXPERIMENTS.md` 6.6),
or *implement* the density-ratio repair so Prop 2 earns its place. **Cost:** ~1 day for the density-ratio
classifier.

### P1-8 · Seed 0 fixes one dataset draw for all 30 seeds
**Evidence.** `mbo.py:33-38` — `np.random.seed(0)` in `Task.__init__`; per-seed randomness is training/init
only. Every CI and p-value conditions on a single data draw; data-draw variance is unestimated while the
ANOVA treats tasks as the sampling unit. The paper does disclose the convention.

**Fix:** per-seed draws. **Cost:** full grid re-run. **Fixable:** yes but expensive; defensible as a
disclosed Design-Bench convention if not.

---

## P2 — minor

- **P2-1 · Table 1 caption cites a value present in no cell of its own table.** Caption says Griewank
  `-2612`; that is a truncation of Ens×CMA `-2612.68` (`grid.tex`), which the body renders `-2613`, while
  the body text uses `-2592` (Ens×Grad). The caption also mixes endpoints incoherently — Branin uses Grad
  (`-9.27`) though the true extreme `-14.01` is in the same table. (`PROVENANCE.md` INC-2.) ~1 h.
- **P2-2 · Rounding/consistency drift.** `|Δ|` 1.2 vs 1.22; CD 4.5 vs 4.54; p 6e-5 vs 6.1e-5; q̂ range
  `[1.8,16]` excludes its own max 16.1; main Table 1 GP×Pert Griewank `-269` vs supplement `-270`
  (truth `-269.60`); "restores coverage to 0.90 on every task" vs supp Table 5 showing 0.89. ~2 h.
- **P2-3 · `q̂` and `ĉ_ood` disagree with `proofs.md`.** `proofs.md:24` says q̂ ∈ [2.8, 10.5] and
  ĉ_ood ≈ 0; the paper says [1.8, 16] and 0.41. One is stale. ~1 h.
- **P2-4 · Two unreconciled rank pools** (2.57 vs 2.29); ties bolded inconsistently. ~1 h.
- **P2-5 · Main Table 3 (the 77-value DB grid) has no generator in `tables_v2/`.** ~2 h.
- **P2-6 · "CbAS" is not CbAS.** `mbo.py:503` — a CEM-style elite-resampling loop. `SKELETON.md:41`
  already flagged that it must be relabeled "CEM-style adaptive sampling" unless real CbAS is run. ~0 h
  (relabel).
- **P2-7 · Sparse-GP σ provenance.** `SKELETON.md:41` warns it is "a feature-variance proxy unless a real
  posterior is fit." `mbo.py:311-342` does fit a real SVGP posterior — so the warning appears stale, but
  the paper should say which. ~0 h.
- **P2-8 · RETRACTED — `li2024bnnsurrogates` IS ICLR 2024.** An earlier revision of this ledger claimed
  it was 2023. That was my error. Verified: Li, Rudner & Wilson, *A Study of Bayesian Neural Network
  Surrogates for Bayesian Optimization*, **ICLR 2024**, arXiv:2305.20028, OpenReview `SA19ijj44B`; the
  PDF header reads "Published as a conference paper at ICLR 2024." The bib key is correct. No action.

## P3 — polish

- **P3-1 · 8 stale uncited figures** in `paper/figures_v2/`; one (`fig4_beta_ablation.pdf`) names **two**
  tasks where β=0 is competitive, against the paper's "6 of 7, lone exception Ackley."
- **P3-2 · README.md is stale and ships in the supplement.** It describes the ICML workshop paper as
  "CURRENT", says **n=10 seeds** against the paper's 30, and points at `paper/latex_source/paper.tex`.
  `README.md:54` lists it for the supplement zip. Shipping it hands a reviewer a contradiction.
- **P3-3 · No provenance in any artifact** — zero timestamp / git sha / config block in any result file;
  seeds are positional only (`run_all.py:79`, `range(seeds)`).

---

## Threat-list verdicts (T1–T12)

| ID | Verdict | Basis |
|---|---|---|
| **T1** Crippled baseline | **CONFIRMED — decisively** | Two independent confirmations. (a) The ensemble trains on **raw targets** while both GPs standardize (P0-2). (b) The authors' own `gradtune.py` sweep shows a trust region closes the gradient collapse on 3 of 4 tasks, failing the script's own pre-stated decision rule (P0-0). Matched tuning is asymmetric exactly as hypothesized. No validation split, no early stopping, no bootstrap, σ unfloored. Held-out error per task: **MISSING**. |
| **T2** Mechanism misnamed | **CONFIRMED — and the name is worse than 'wrong'** | Coverage exists for `ens:grad` only, 1 of 9 (P0-3). Ens×CMA coverage: **MISSING**. The cross-proposal claim varies both factors at once and uses a different GP. And P0-0 shows the mechanism is not "ensemble×gradient" at all — it is "ensemble×*untuned* gradient", which a trust region repairs. |
| **T3** Unmatched budget | **CONFIRMED** | 25,600 / 4,096 / 432–3,012 surrogate queries (P1-1). Plus an unmatched **oracle** budget, 256 vs 128 (P0-1). |
| **T4** RF-oracle validity | **PARTIAL** | Circularity: not confirmed — needs the RF-vs-surrogate split check. But DB "in-distribution" coverage is sampled from the **wrong distribution** (P0-5), and the RF defense sentence is arithmetically backwards (P0-7) with no supporting table. |
| **T5** COMs divergence | **CONFIRMED** | 1.22 units on TF-Bind-8; the one "matches official" number fails to verify against its own row (P1-6). |
| **T6** ANOVA assumptions | **CONFIRMED — and worse** | It is not a standard ANOVA at all: hand-rolled, no error term, `task` unmodeled, two normalizations spanning 9 vs 11 cells (P1-2). Robustness profile pending. |
| **T7** Seed-0 dataset | **CONFIRMED** | `mbo.py:33-38` (P1-8). Disclosed by the paper; still unestimated variance. |
| **T8** Trivial propositions | **CONFIRMED** | Prop 1's proof is one line and is an identity; Prop 2 restates Tibshirani 2019 and its repair is never implemented (P1-7). |
| **T9** Weak null | **CONFIRMED — and self-conceded** | The abstract already concedes N=7 underpowered. Compounded: DB significance claims violate the pre-registration (P1-4). |
| **T10** Figure/table integrity | **CONFIRMED — worse** | Not one caption error but **13** inconsistencies, two severe: Fig 1 vs Fig 3 disagree on 6 of 9 DB cells (P0-6); a load-bearing sentence is arithmetically backwards (P0-7). |
| **T11** Title/scope | **PARTIAL** | Synthetic suite runs 2D–30D (`mbo.py:41-70`); the GP wins at 30D too, so "low dimension" is inaccurate. The d>500 separable-CMA path is **not present** in the current grid code. |
| **T12** LCB candidate selection | **CONFIRMED — worse than hypothesized** | Not final-iterate-vs-best-seen: **all three optimizers use different rules**, and the reported set is chosen by the **oracle** post hoc (P0-1). Fatal to the stated protocol as written. |

---

## What this means

Nine P0/P1 rows (P0-1, P0-2, P0-3, P1-1, P1-2, P1-3) share one root: **the grid is not the controlled
experiment the paper says it is.** The optimizer axis carries an unmatched oracle budget and three
different selection rules; the surrogate axis carries an unmatched target normalization. Both headline
effects (η²_surr = 0.37, the ensemble×gradient interaction) are confounded with implementation
asymmetries that the paper explicitly claims are held constant.

The good news is that these are *cheap* to fix and the fixes are *decisive*. Normalizing the ensemble's
targets and equalizing the candidate protocol is under a day of edits plus one grid re-run. If η²_surr
survives, the paper's central claim is established far more strongly than it is now. If it does not, the
authors learn that before a reviewer does.

**Nothing else in this ledger should be acted on until P0-2 is run.** Every downstream number depends
on it.
