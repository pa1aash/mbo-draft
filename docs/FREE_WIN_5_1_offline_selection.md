# Free Win 5.1 — Oracle-free selection of the winning (surrogate × optimizer) cell

**Verdict: FAILS.** The pre-registered decision rule does not beat its pre-registered trivial
baselines. The kill criterion in `PREREGISTRATION.md:59` — *"Fails either trivial baseline ->
reported honestly and dropped"* — **fires**. Report and drop.

Two separate findings make this a *strong* negative rather than a weak one, and they must be
reported together because either alone would be misleading:

1. **The feature the idea depends on is not oracle-free.** Every calibration probe in the
   artifacts is computed with `task.oracle(...)`. `c_hat_ood` in particular requires evaluating
   *f* on the proposals — precisely the query offline MBO forbids. The idea's premise is broken
   at the source, not at the statistics.
2. **n=14 is below the resolution of the question.** Even a **perfect** oracle-free rule (regret
   exactly 0 on every task) beats always-GP with only d_z = 0.71, while n=14 needs |d_z| ≥ 0.81
   for 80% power. **No rule can clear the bar at this n**, so this negative result must not be
   over-read as proof that no such rule exists.

Reproduce: `/opt/homebrew/Caskroom/miniforge/base/bin/python3 offline_selection.py`
(scratchpad; numpy+scipy only). Raw log: `offline_selection_log.txt`; machine-readable:
`offline_selection_results.json`.

*Environment note:* `/Users/palaash/Downloads/MBO/venv` is a Windows-layout venv (`Include/Lib/
Scripts/`) with no usable macOS python, and the miniforge python that does have numpy/scipy has no
sklearn — so ridge is implemented in closed form in numpy. **Validated against sklearn 1.9.0**
(available in a scratchpad venv from an earlier session): max |numpy ridge − `sklearn.Ridge`| =
**1.6e-15** over 200 random problems. The estimator is not a home-grown approximation.

---

## 1. Feature inventory and the oracle-free honesty assessment

Sources inspected: `/Users/palaash/Downloads/MBO/results/results_camera.json` (synthetic, 7
tasks × 30 seeds), `/Users/palaash/Downloads/MBO/results/results_db.json` (Design-Bench, 7 tasks
× 16 seeds). Grid verified complete: **9/9 cells per task on all 14 tasks**, at exactly 30 (synth)
/ 16 (DB) seeds.

### 1a. What the artifacts actually contain

`mbo[task][cell]` holds **only** `p100` and `p50` → `{mean, std, all[]}`. No diagnostics.
`calibration[task]` holds **one** record under the literal key `"_"` (`code/run_all.py:73`).

### 1b. The honesty assessment — which features survive at selection time?

This is the load-bearing section. A feature is *oracle-free* only if it is computable at
deployment time in a **truly offline** setting, i.e. from the labelled offline dataset alone,
with **zero** new queries to *f*.

| Feature | Avail. | Computed how | **Oracle-free?** |
|---|---|---|---|
| `cov_ood@{0.5,1,2,5}` (`c_hat_ood`) | 14/14 | `coverage_of_premise(mu_o, sig_o, f_o, b)` where **`f_o = task.oracle(xf)`**, `mbo.py:599,602` | **NO — fatal.** Requires *f* at the LCB proposals. That is the exact query offline MBO cannot make. Not reconstructible by any offline means. |
| `cov_conf_ood` | 14/14 | `np.mean(f_o >= mu_o - q*sig_o)`, `mbo.py:611` | **NO — fatal.** Same oracle-on-proposals dependency. |
| `rho_err` | 14/14 | `spearman(sig, |mu - task.oracle(xt)|)`, `mbo.py:593` | **NO as computed.** See 1c. |
| `cov_indist@{0.5,1,2,5}` (`c_hat_in`) | 14/14 | `coverage_of_premise(mu, sig, task.oracle(xt), b)`, `mbo.py:601` | **NO as computed.** See 1c. |
| `cov_conf_indist` | 14/14 | `task.oracle(xt)`, `mbo.py:610` | **NO as computed.** See 1c. |
| `q_conformal` (`q_hat`) | 14/14 | `fit_conformal_multiplier(mu_c, sig_c, task.oracle(xc))`, `mbo.py:609` | **NO as computed**, and **excluded anyway**: it lives in raw-y units on synthetic but [0,1] units on DB, so it is not poolable across the 14 tasks. |
| `d` (task dimension) | **11/14** | Structural. `mbo.py:41-85` (synth); `PREREGISTRATION.md:47`, `cloud/setup.sh:66` (TFBind8=32, TFBind10=40, Superconductor=86); `mbo.py:282` (GFP=4740) | **YES.** Not in the artifacts — read off the source. **MISSING for UTR, AntMorphology, DKitty** — recorded nowhere in the repo. Not imputed. |
| `N` (dataset size) | **7/14** | Structural. `mbo.py:41-85` (synth: 2000–8000) | **YES for synthetic. MISSING for all 7 DB tasks.** Only the `--db-subsample` cap (default 8000, `run_all.py:121`) is recorded; `db_tasks.py:54-58` concatenates a top-block with a random block **without deduping**, so realized N is data-dependent, ≤8000, and unrecorded. Not imputed. |
| discrete/continuous flag | 14/14 | Structural. `db_tasks.py:7-9` docstring | **YES.** The **only** genuinely oracle-free feature available on all 14 tasks. |

**MISSING entirely — absent from every artifact, not imputed:**

| Feature | Status |
|---|---|
| `rho_knn` = `spearman(sig, 5-NN train distance)` | **MISSING** from every `results/*.json` (checked all 10). Bitter irony: this is **the one genuinely oracle-free probe the codebase instruments** (`mbo.py:594,614`), and `run_all.py:60` *does* save it — but no committed artifact contains it. The calibration blocks predate that save, or were merged from an older file. |
| σ statistics (mean/median/spread) | **MISSING.** `mu/sig` computed at `mbo.py:585-588`, never persisted. |
| ensemble disagreement | **MISSING** (≡ σ; never persisted). |
| GP marginal likelihood / held-out NLL | **MISSING.** Never computed anywhere in the codebase. |
| proposal displacement ‖x_T − x_0‖ | **MISSING.** `x0`/`xf` exist at `mbo.py:597-598`, never persisted. |
| **any per-(task, cell) feature** | **MISSING.** See 1d. |

### 1c. The one genuine subtlety: "oracle-free" vs "oracle-free-*reconstructible*"

The in-distribution probes deserve a fair hearing rather than a blanket dismissal, and the answer
differs between the two halves of the benchmark:

- **Synthetic (7 tasks): reconstructible.** The offline dataset is `np.random.uniform(0,1,(n,dim))`
  (`mbo.py:37`) and the probe points are `np.random.uniform(0,1,(n_test,dim))` (`mbo.py:591`) —
  **exchangeable**. So `rho_err`, `cov_indist@*`, `cov_conf_indist`, `q_conformal` could be
  obtained from a held-out split of the *labelled offline data*, with no new oracle queries. As
  literally coded they call `task.oracle`, but they extract no information a deployed practitioner
  lacks. Call these **oracle-free-reconstructible** (modulo one wrinkle: offline `y` carries
  observation noise, `mbo.py:38`, while `oracle(xt)` is noiseless).
- **Design-Bench (7 tasks): NOT reconstructible.** The probe is still uniform on the cube, but the
  DB offline data is *not*. For the discrete tasks it sits on one-hot simplex vertices
  (`db_tasks.py:60-63`) — **mutually singular** with the dense cube. Uniform probe points are
  designs the dataset never contains, so labelling them is a genuine oracle query. Not
  reconstructible by any offline means.
- **On-proposal probes (`cov_ood@*`, `cov_conf_ood`): NEVER reconstructible, on either half.**

**So the honest bottom line: the oracle-free feature set that spans all 14 tasks is a single
binary flag.** `d` covers 11/14, `N` covers 7/14. Everything the paper names as a calibration
feature is oracle-contaminated on at least the DB half, and the on-proposal features — the ones
the mechanism story says should matter — are contaminated everywhere.

### 1d. Killer consequence: there are ZERO per-cell features

`calibration` is keyed `task -> "_"` — computed **once per task**, with the **ensemble** surrogate
and **grad** at fixed `BETA` (`mbo.py:597-598`). It does not vary by cell.

**Protocol step 3(a) — "pick the cell maximizing a single feature, e.g. argmax c_hat_ood" — is
NOT COMPUTABLE.** `c_hat_ood` has one value per *task*, not one per *cell*; there is no argmax to
take. Only rules of the form `score(task, cell) = g_cell(task_descriptors)` are implementable.

This is not a defect in the protocol: it is exactly what `PREREGISTRATION.md:56-58` specified
("fit boundary on all-but-one task from (d, held-out calibration probe); predict held-out task's
better arm"). The prereg's own design is the only implementable one. It is reported here so the
gap between the free-win brief and the artifact is on the record.

---

## 2. Target and normalization (reused, not invented)

Per-(task, cell) **normalized score**, using the paper's own convention copied verbatim from
`code/analysis.py:29-34` (`task_norm`), the same function `code/run05.py:81` calls:

> per-task **min–max over ALL present grid cells** of the `p100` **mean**.

One inherited quirk, preserved deliberately: `task_norm` min-maxes over every key containing `':'`
— **11 cells** (the 9-cell grid + `ens_conformal:{grad,perturb}`), not 9. I reuse it exactly as
the paper does and take the **argmax over the 9-cell grid** as the selection set. Consequence:
per-task max over the 9 grid cells can be < 1.0.

**Metric.** `p100` is the headline (the `analysis.py` default, and the paper's headline).
`PREREGISTRATION.md:17` names p100 **and** p50 as co-primary, so p50 is reported in §6 — as a
co-primary, **not** as a second chance to win.

**Regret** = (best achievable grid cell on t) − (selected cell's score on t). CIs: bootstrap over
the 14 held-out tasks, B=10000 (`PREREGISTRATION.md:29`: "Bootstrap CIs B=2000-10000").

---

## 3. Is there anything to win in the first place?

| task | d | N | disc | best cell | ens:grad | ens:perturb | ens:cma | gp:grad | gp:perturb | gp:cma | svgp:grad | svgp:perturb | svgp:cma |
|---|--|--|--|---|--|--|--|--|--|--|--|--|--|
| Branin-2D | 2 | 2000 | 0 | botorchgp:grad | 0.348 | 0.972 | 0.000 | **1.000** | 1.000 | 1.000 | 0.996 | 1.000 | 0.991 |
| Styblinski-5D | 5 | 3000 | 0 | botorchgp:perturb | 0.038 | 0.901 | 0.000 | 0.723 | **1.000** | 0.693 | 0.214 | 0.942 | 0.207 |
| Levy-8D | 8 | 4000 | 0 | botorchgp:grad | 0.336 | 0.888 | 0.000 | **1.000** | 0.938 | 0.999 | 0.991 | 0.937 | 0.990 |
| Rosenbrock-10D | 10 | 5000 | 0 | svgp:grad | 0.462 | 0.834 | 0.000 | 0.900 | 0.918 | 0.884 | **1.000** | 0.924 | 0.998 |
| Rastrigin-15D | 15 | 5000 | 0 | svgp:grad | 0.388 | 0.297 | 0.000 | 0.749 | 0.317 | 0.721 | **1.000** | 0.319 | 0.979 |
| Ackley-20D | 20 | 5000 | 0 | botorchgp:grad | 0.472 | 0.020 | 0.361 | **1.000** | 0.027 | 0.993 | 0.977 | 0.051 | 0.970 |
| Griewank-30D | 30 | 8000 | 0 | botorchgp:grad | 0.008 | 0.849 | 0.000 | **1.000** | 0.897 | 1.000 | 1.000 | 0.895 | 1.000 |
| TFBind8 | 32 | — | 1 | ens:grad | **0.989** | 0.000 | 0.873 | 0.000 | 0.000 | 0.000 | 0.688 | 0.370 | 0.682 |
| TFBind10 | 40 | — | 1 | ens:grad | **1.000** | 0.912 | 0.428 | 0.912 | 0.912 | 0.000 | 0.318 | 0.912 | 0.315 |
| Superconductor | 86 | — | 0 | botorchgp:perturb | 0.000 | 0.960 | 0.608 | 0.802 | **1.000** | 0.868 | 0.242 | 0.818 | 0.858 |
| GFP | 4740 | — | 1 | svgp:cma | 0.000 | 0.997 | 0.328 | 0.994 | 0.994 | 0.995 | 0.941 | 0.994 | **0.997** |
| UTR | — | — | 1 | ens:grad | **0.985** | 0.649 | 0.755 | 0.719 | 0.719 | 0.719 | 0.719 | 0.719 | 0.000 |
| AntMorphology | — | — | 0 | botorchgp:perturb | 0.048 | 0.622 | 0.000 | 0.995 | **1.000** | 1.000 | 0.158 | 0.990 | 0.030 |
| DKitty | — | — | 0 | botorchgp:perturb | 0.055 | 0.850 | 0.000 | 0.860 | **1.000** | 0.771 | 0.775 | 0.956 | 0.775 |

(`—` = MISSING, never imputed. `gp` = `botorchgp`.)

**Yes, there is heterogeneity**: 5 distinct cells win across the 14 tasks; the modal cell wins only
4/14. So the question is not vacuous — a good rule *could* in principle pay off. Mean per-task
score by cell: `botorchgp:grad` 0.832, `svgp:perturb` 0.773, `botorchgp:perturb` 0.766,
`botorchgp:cma` 0.760, `svgp:grad` 0.716, `svgp:cma` 0.699, `ens:perturb` 0.696, `ens:grad` 0.366,
`ens:cma` 0.239.

---

## 4. Method

**Rules** (all pre-specified; ridge `alpha=1.0` fixed a priori and **never tuned**; every rule run
is reported, none dropped):

| ID | Rule | Features | Oracle-free? |
|---|---|---|---|
| R1 | per-cell group mean, argmax | discrete | yes |
| R2 | per-cell ridge, argmax | discrete | yes |
| R3 | per-cell ridge, argmax | log d | yes (prereg's "boundary from d") |
| R4 | 1-NN on task descriptors | log d | yes |
| R5 | per-cell ridge, argmax | log d, discrete | yes |
| R6 | per-cell ridge, argmax | log d, log N | yes |
| R7 | 1-NN on task descriptors | log d, log N | yes |
| C1 | per-cell ridge, argmax | cov_conf_ood, cov_conf_indist | **NO — ceiling probe** |
| C2 | per-cell ridge, argmax | all 11 unit-free calibration probes | **NO — ceiling probe** |
| C3 | 1-NN | cov_conf_ood, cov_conf_indist | **NO — ceiling probe** |

Because `d` is MISSING for 3 tasks and `N` for 7, the LOO runs in **arms** on the largest complete-case
task set each feature set supports (14 / 11 / 7). The **C\*** arm is a deliberate
**oracle-contaminated ceiling probe**: if features that *cheat* cannot predict the winner, the
oracle-free version is dead twice over. It is **not deployable** and is never counted as a result.

**Baselines**, all recomputed inside each arm: (a) best fixed cell in hindsight; **(b) best fixed
cell on the other n−1 tasks — the honest bar**; (c) random cell (exact expectation over the 9);
(d) always-ensemble and always-GP, each with the optimizer chosen honestly on the other n−1 tasks.

---

## 5. Per-task regret (headline metric p100, n=14)

| task | best cell | **(b) fixed** | R1 pick | **R1 reg** | C1 pick *(oracle)* | C1 reg | always-GP | always-ens |
|---|---|--|---|--|---|--|--|--|
| Branin-2D | botorchgp:grad | 0.000 | botorchgp:grad | 0.000 | svgp:grad | 0.004 | 0.000 | 0.028 |
| Styblinski-5D | botorchgp:perturb | 0.277 | botorchgp:grad | 0.277 | botorchgp:perturb | 0.000 | 0.277 | 0.099 |
| Levy-8D | botorchgp:grad | 0.000 | botorchgp:grad | 0.000 | botorchgp:grad | 0.000 | 0.000 | 0.112 |
| Rosenbrock-10D | svgp:grad | 0.100 | botorchgp:grad | 0.100 | svgp:grad | 0.000 | 0.100 | 0.166 |
| Rastrigin-15D | svgp:grad | 0.251 | botorchgp:grad | 0.251 | svgp:grad | 0.000 | 0.251 | 0.703 |
| Ackley-20D | botorchgp:grad | 0.949 | botorchgp:perturb | 0.973 | svgp:perturb | 0.949 | 0.973 | 0.980 |
| Griewank-30D | botorchgp:grad | 0.000 | botorchgp:grad | 0.000 | botorchgp:perturb | 0.103 | 0.000 | 0.151 |
| TFBind8 | ens:grad | 0.989 | botorchgp:grad | 0.989 | botorchgp:grad | 0.989 | 0.989 | 0.989 |
| TFBind10 | ens:grad | 0.088 | svgp:grad | 0.682 | botorchgp:grad | 0.088 | 0.088 | 0.088 |
| Superconductor | botorchgp:perturb | 0.198 | botorchgp:grad | 0.198 | botorchgp:perturb | 0.000 | 0.198 | 0.040 |
| GFP | svgp:cma | 0.003 | ens:grad | 0.997 | svgp:cma | 0.000 | 0.003 | 0.000 |
| UTR | ens:grad | 0.266 | svgp:perturb | 0.266 | botorchgp:perturb | 0.266 | 0.266 | 0.336 |
| AntMorphology | botorchgp:perturb | 0.005 | botorchgp:grad | 0.005 | botorchgp:perturb | 0.000 | 0.005 | 0.378 |
| DKitty | botorchgp:perturb | 0.140 | botorchgp:grad | 0.140 | botorchgp:perturb | 0.000 | 0.140 | 0.150 |
| **MEAN** | | **0.233** | | **0.348** | | *0.171* | 0.235 | 0.302 |

---

## 6. Baseline comparison

### ARM 1 — honest oracle-free, all 14 tasks (only fully-available descriptor: discrete)

Hindsight-best fixed cell: `botorchgp:grad`.

| strategy | mean regret | 95% CI | vs (b) W/L/T | paired diff vs (b) [95% CI] |
|---|--|---|--|---|
| (a) best fixed cell, hindsight *(upper bound)* | 0.1655 | [0.0598, 0.3130] | — | — |
| **(b) best fixed cell on other 13 — BEAT ME** | **0.2333** | [0.0861, 0.4131] | — | — |
| (c) random cell (exact E over 9) | 0.3480 | [0.2860, 0.4112] | — | — |
| (d) always-ensemble | 0.3015 | [0.1455, 0.4825] | — | — |
| (d) always-GP | 0.2350 | [0.0861, 0.4168] | — | — |
| always-svgp | 0.2841 | [0.1248, 0.4632] | — | — |
| **R1 groupmean(discrete)** *oracle-free* | **0.3484** | [0.1667, 0.5513] | **0/3/11** | **+0.1151 [+0.0000, +0.2858]** |
| **R2 ridge(discrete)** *oracle-free* | **0.3484** | [0.1667, 0.5513] | **0/3/11** | **+0.1151 [+0.0000, +0.2858]** |

**R1/R2 lose to every baseline.** Mean regret 0.348 is *identical to picking a cell at random*
(0.348) and worse than (b) by +0.115. Win/loss/tie vs (b): **0 wins, 3 losses, 11 ties**. vs
always-GP: **0/2/12**. The point estimate goes the **wrong way**.

### ARM 2 — 11 tasks with d recorded (the prereg's actual rule)

| strategy | mean regret | 95% CI | vs (b) W/L/T | paired diff vs (b) |
|---|--|---|--|---|
| (a) hindsight fixed | 0.1732 | [0.0446, 0.3539] | — | — |
| **(b) honest fixed cell — BEAT ME** | 0.3607 | [0.1442, 0.5953] | — | — |
| (c) random | 0.3420 | [0.2675, 0.4221] | — | — |
| (d) always-ensemble | 0.3052 | [0.1049, 0.5373] | — | — |
| **(d) always-GP** | **0.1732** | [0.0446, 0.3539] | — | — |
| R3 ridge(log d) *oracle-free* | 0.4162 | [0.1961, 0.6478] | 1/1/9 | +0.0555 [−0.0152, +0.1818] |
| R4 1-NN(log d) *oracle-free* | 0.3312 | [0.1077, 0.5908] | 3/4/4 | −0.0295 [−0.3431, +0.2924] |
| R5 ridge(log d, discrete) *oracle-free* | 0.2957 | [0.1208, 0.4853] | 4/2/5 | −0.0650 [−0.2905, +0.1418] |

**Read this arm carefully — it is where over-claiming would happen.** R4 and R5 nominally beat (b).
That is meaningless: **always-GP (0.173) beats all three rules outright**, and it is precisely the
baseline `PREREGISTRATION.md:59` names as disqualifying. Both paired CIs span zero. R3 — the
prereg's literal rule, ridge on d — is the **worst** strategy in the arm.

### ARM 3 — 7 synthetic tasks (d and N both recorded)

| strategy | mean regret | 95% CI | vs (b) W/L/T | paired diff vs (b) |
|---|--|---|--|---|
| (a) hindsight fixed | 0.0897 | [0.0142, 0.1757] | — | — |
| **(b) honest fixed cell — BEAT ME** | 0.1624 | [0.0142, 0.3870] | — | — |
| (c) random | 0.3284 | [0.2427, 0.4232] | — | — |
| (d) always-ensemble | 0.3200 | [0.0995, 0.5840] | — | — |
| **(d) always-GP** | **0.0897** | [0.0142, 0.1757] | — | — |
| R6 ridge(log d, log N) *oracle-free* | 0.1657 | [0.0176, 0.3870] | 0/3/4 | +0.0033 [+0.0000, +0.0099] |
| **R7 1-NN(log d, log N)** *oracle-free* | **0.0799** | [0.0045, 0.1608] | 2/3/2 | −0.0824 [−0.2311, +0.0082] |

**R7 is the single best-looking oracle-free number in this entire report (0.0799, nominally beating
both (b) 0.162 and always-GP 0.0897). It is not a finding.** It **loses more folds than it wins
(2W/3L)**; its paired CI spans zero; n=7 requires |d_z| ≥ 1.27 to detect anything; and it is **1 of
10 rules tried**. Promoting it would be exactly the failure mode this analysis exists to avoid.

### ARM 4 — CONTAMINATED CEILING PROBE (features use the oracle; **NOT DEPLOYABLE**)

| strategy | mean regret | 95% CI | vs (b) W/L/T | paired diff vs (b) |
|---|--|---|--|---|
| (b) honest fixed cell | 0.2333 | [0.0861, 0.4131] | — | — |
| C1 ridge(cov_conf_ood, cov_conf_indist) *ORACLE* | 0.1713 | [0.0213, 0.3666] | 7/2/5 | −0.0619 [−0.1223, −0.0077] |
| C2 ridge(all 11 probes) *ORACLE* | 0.1302 | [0.0314, 0.2792] | 8/4/2 | −0.1031 [−0.2553, +0.0015] |
| C3 1-NN(cov_conf_ood, cov_conf_indist) *ORACLE* | 0.1738 | [0.0790, 0.2851] | 5/4/5 | −0.0594 [−0.2662, +0.1268] |

**This is the most scientifically interesting row in the report, and it must be stated carefully.**
C1's paired CI vs (b) excludes zero (−0.122, −0.008), and vs always-GP it is 8W/2L, diff −0.0637
[−0.1237, −0.0094]. So there is a *hint* that the calibration probes carry real signal about which
cell wins — and mechanistically that is coherent with the paper's own story: `cov_conf_ood` measures
how badly the ensemble's uncertainty breaks **on its own proposals**, which is exactly what should
predict whether the ensemble or the GP wins.

**But: (i)** the sign tests are not significant (C1 vs (b): 7W/2L, **p=0.180**; C2: 8W/4L,
**p=0.388**); **(ii)** these are 3 of 10 rules; and **(iii) — decisively — these features require
querying *f* on the proposals, so no deployable rule can ever use them.** The ceiling probe does not
rescue the idea. It diagnoses *why* it fails: **the predictive signal lives precisely in the
quantity offline MBO cannot compute.**

---

## 7. What is even detectable at n=14?

| n | |d_z| needed for 80% power (two-sided paired t, α=.05) |
|--|--|
| 14 | **0.81** |
| 11 | 0.94 |
| 7 | 1.27 |

- Observed SD of the paired regret difference (R1 − (b)) over 14 tasks: **0.2982**. So the smallest
  mean regret improvement detectable at 80% power is **0.2416 normalized-score units**. Anything
  smaller is invisible here.
- Sign test: a rule needs **≥12/14 wins with 0 losses** for p<0.05 two-sided (p=0.0129). The best
  oracle-free rule managed 4 wins.

### The decisive design fact

| | mean regret | SD over tasks |
|---|--|--|
| perfect oracle-free rule (per-task argmax) | 0.0000 | — |
| always-GP | 0.2350 | 0.3326 |

A **perfect** rule beats always-GP with **d_z = 0.71**, but n=14 needs **|d_z| ≥ 0.81**.

> **Even a perfect oracle-free selection rule could not be certified as better than always-GP at
> n=14.** always-GP's per-task regret is dominated by a couple of catastrophic tasks (TFBind8 0.989,
> Ackley 0.973), so its SD (0.33) exceeds its mean (0.24). **n=14 is not merely "small" — it is
> below the resolution of the question.**

This cuts both ways and must be reported both ways: it means the negative result **cannot** be
strengthened into "no oracle-free rule exists", *and* it means no amount of rule engineering on
these 14 tasks could have produced a defensible positive.

---

## 8. Co-primary metric p50 — the trap, reported so it cannot be sprung

`PREREGISTRATION.md:17` names p100 **and** p50. On p50:

| strategy | p50 regret | vs (b) W/L/T | vs always-GP W/L/T |
|---|--|--|--|
| (b) honest fixed cell | 0.3120 | 0/0/14 | 4/7/3 |
| always-GP | 0.2192 | 7/4/3 | 0/0/14 |
| **R1 groupmean(discrete)** *oracle-free* | **0.0742** | **9/3/2** | 3/0/11 |

**On p50, R1 looks like a clear winner** (0.074 vs (b) 0.312, diff −0.238 [−0.473, −0.038]) — while
**the same rule is the worst strategy tested on the headline p100 metric** (0.348 vs 0.233, i.e.
exactly random). Two reasons this is noise, not a result:

1. **It fails the trivial baseline even on p50.** vs always-GP: 3W/0L/**11 ties**, diff
   −0.145 [−0.359, **+0.000**] — the CI touches zero, sign test **p=0.250**. `PREREGISTRATION.md:59`
   still fires.
2. **The target itself is metric-unstable.** The best cell agrees under p100 and p50 on only
   **8/14 tasks**. The hindsight-best fixed cell is `botorchgp:grad` under p100 but `svgp:grad`
   under p50. A rule whose sign flips between two co-primary metrics of the same runs is
   fitting metric noise.

Reported explicitly so this number cannot later be quietly promoted to the headline.

---

## 9. A note on baseline (b) itself

(b) picks `botorchgp:grad` on **13/14 folds** and flips to `svgp:perturb` on exactly one:
**Ackley-20D**. Ackley is a single influential task where *every* perturb cell collapses
(ens:perturb 0.020, gp:perturb 0.027, svgp:perturb 0.051); dropping it flips the argmax-of-mean
(`botorchgp:grad` 0.832→0.820 vs `svgp:perturb` 0.773→0.829).

So **baseline (b) is essentially "always use a BoTorch GP with gradient ascent"**, and (b) ≈
always-GP is not a coincidence — they are nearly the same strategy. And **one task out of 14 flips
the honest baseline**: the n=14 problem shows up in the *baseline*, not just in the rules.

---

## 10. Multiplicity

10 rules × 2 co-primary metrics = up to **20 rule×metric comparisons** against (b). Under a
coin-flip null, P(≥1 of 10 rules beats (b) by chance) ≈ 1 − 0.5¹⁰ = **0.999**; over 20 slots,
**0.9999**. The best-looking cell in these tables is **not** interpretable as a discovery.

**Discipline actually applied:** ridge alpha fixed at 1.0 a priori and never tuned; every rule run
is reported and none dropped; p100 designated headline *before* looking (it is `analysis.py`'s
default and the paper's headline), so the p50 result that flatters R1 is **not** promoted; no rule
was added after seeing a result.

---

## 11. Blunt verdict

**FAILS. The pre-registered kill criterion fires. Drop it.**

- On the headline metric p100, **no oracle-free rule beats baseline (b)**, and the best-looking ones
  (R4, R5, R7) are beaten outright by **always-GP** — the trivial baseline
  `PREREGISTRATION.md:59` explicitly names as disqualifying. The prereg's literal rule (ridge on d,
  R3) is the **worst** strategy in its arm.
- The headline rule available on all 14 tasks (R1/R2) achieves regret **0.348 — identical to random
  cell choice** — vs 0.233 for (b) and 0.235 for always-GP. **0 wins, 3 losses, 11 ties** vs (b).
- The p50 co-primary does **not** rescue it: the rule that wins there fails always-GP (3W/0L/11T,
  p=0.250) and is the worst rule on p100.

**Three things must be said alongside the verdict, or the negative result is itself misleading:**

1. **The idea's premise is broken at the source, not at the statistics.** `c_hat_ood` — the feature
   the brief leads with — is computed as `np.mean(f_o >= mu_o - q*sig_o)` with
   `f_o = task.oracle(xf)`. **It requires evaluating the true objective on the proposals**, the one
   query offline MBO forbids. It is not oracle-free and cannot be made so. The genuinely oracle-free
   feature set spanning all 14 tasks is **one binary flag**.
2. **The instrumentation, not just the result, is the finding.** `rho_knn` — the *one* genuinely
   oracle-free probe the codebase computes (`mbo.py:594`) and `run_all.py:60` saves — **is absent
   from every committed artifact**. σ statistics, ensemble disagreement, GP marginal likelihood, and
   proposal displacement were never persisted. `d` is unrecorded for 3/14 tasks; `N` for 7/14. And
   **no per-cell feature exists at all**, which makes the brief's own rule (a) uncomputable. This
   analysis is a fair test of *what was instrumented*; it is not a fair test of *the idea*.
3. **n=14 could not have certified a win even if one existed** (perfect rule: d_z = 0.71 < 0.81
   needed). So this must be reported as **"ran as pre-registered, failed its trivial baselines,
   dropped"** — **not** as evidence that oracle-free selection is impossible. The honest claim is
   about *this rule, on this instrumentation, at this n*.

**Does the paper change category?** **No.** This is a **dropped stretch goal**, reported honestly
per the pre-registration — worth a short, unembarrassed paragraph, not a section. Nothing here
touches the paper's main factorial claims.

**If anyone wants to revive it** (out of scope here, stated so the negative result is actionable
rather than merely discouraging): the minimum viable version needs (i) `rho_knn` + σ statistics +
proposal displacement persisted **per cell**, not per task — all are oracle-free and already
computed or trivially computable; (ii) conformal `q̂` refit on a held-out split of the **offline
dataset** rather than on `task.oracle(xc)` at uniform points, which would make it genuinely
oracle-free on both halves; (iii) `d`/`N` recorded for the DB tasks (one run of
`python code/db_tasks.py ...` in the `db` env); and (iv) **far more than 14 tasks** — the power
analysis says n=14 cannot resolve this question regardless of how good the rule is. Absent (iv),
(i)–(iii) would still not yield a publishable positive.
