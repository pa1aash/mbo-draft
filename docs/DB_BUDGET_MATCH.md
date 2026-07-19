# 0C — Budget-matched optimizer arm on Design-Bench (DBM1/DBM2)

Pre-registered in `docs/PREREGISTRATION_V3.md` §0C, committed **before launch** at `100d2ed`.
Runner `code/db_budget_matched.py`, driver `code/run_db_budget.sh`, analysis
`code/analyze_db_budget.py` (every estimator imported unchanged from `code/analyze_db.py`).
Env `dbm` (python 3.9.23, torch 2.8.0+cpu, numpy 1.23.5, botorch 0.10.0, gpytorch 1.11,
cma 4.4.4), `--db-subsample 8000`, beta=2, K=5, TOP=128, 16 seeds, 7 tasks, 9 cells,
4 corners x 3 levels. **24/24 corner files, 0 failures, 0 missing cells, 0 ragged seed axes.**
Artifacts under `results/db_budget/`.

---

## THE CALL: **PROMOTE**

DBM1 CONFIRMED, DBM2 CONFIRMED, achieved-Q audit clean in all four corners. Section 6's
optimizer half may assert rather than qualify, and `docs/CLAIM_LEDGER.md` D19's PROVISIONAL
status is lifted — subject to the two scope limits in the last section, which are not
optional.

| | verdict |
|---|---|
| **DBM1** | **CONFIRMED** — in every corner that rejects under matched budget, perturbation still leads AND eta2_opt still exceeds eta2_surr |
| **DBM2** | **CONFIRMED** — eta2_surr stays below 0.10 in all four corners at the primary level |

---

## The per-corner table (7-task, primary)

| corner | level | eta2_surr | eta2_opt | eta2_inter | Friedman *p* | rejects? | opt leader |
|---|---|---|---|---|---|---|---|
| off_off | native | 0.051 | 0.096 | 0.016 | 0.140 | no | perturb |
| off_off | **UP** | **0.043** | **0.180** | 0.022 | **0.0179** | **yes** | perturb |
| off_off | down | 0.081 | 0.085 | 0.018 | 0.0489 | yes | perturb |
| on_off | native | 0.094 | 0.145 | 0.041 | 0.0234 | yes | perturb |
| on_off | **UP** | **0.062** | **0.255** | 0.045 | **0.000825** | **yes** | perturb |
| on_off | down | 0.126 | 0.160 | 0.053 | 0.0122 | yes | perturb |
| off_on | native | 0.046 | 0.193 | 0.008 | 0.0139 | yes | perturb |
| off_on | **UP** | **0.037** | **0.282** | 0.018 | **0.00145** | **yes** | perturb |
| off_on | down | 0.040 | 0.111 | 0.007 | 0.0197 | yes | perturb |
| on_on | native | 0.062 | 0.181 | 0.028 | 0.00761 | yes | perturb |
| on_on | **UP** | **0.050** | **0.281** | 0.029 | **0.000570** | **yes** | perturb |
| on_on | down | 0.066 | 0.126 | 0.052 | 0.00736 | yes | perturb |

Achieved Q at the primary level, instrumented per cell: grad exactly on target in every
corner, perturb −0.50%, cma +0.05% to +0.09%; **0% of cells deviate more than 5%** anywhere.
The arm matched what it claimed to match.

---

## DBM1 — CONFIRMED, and the direction is the finding

Perturbation leads the optimizer marginal in **all four corners at all three levels** — 12 of
12. At the primary level its marginal is 0.809–0.863 against gradient's 0.386–0.684 and CMA's
0.400–0.448. eta2_opt exceeds eta2_surr in every corner at the primary level, by 4.2x to 7.6x.

**The load-bearing observation is that matching does not weaken the optimizer axis — it
roughly doubles it.** Going from native to matched budget:

| corner | eta2_opt native → UP | eta2_surr native → UP |
|---|---|---|
| off_off | 0.096 → **0.180** | 0.051 → 0.043 |
| on_off | 0.145 → **0.255** | 0.094 → 0.062 |
| off_on | 0.193 → **0.282** | 0.046 → 0.037 |
| on_on | 0.181 → **0.281** | 0.062 → 0.050 |

The presumed direction of the D08 confound was that gradient's 11.8x budget advantage
manufactured the optimizer effect. The measurement says the opposite: the native imbalance was
**masking** it. Giving perturbation and CMA gradient's budget makes the optimizer axis
*larger* and the surrogate axis *smaller* in all four corners, and moves off_off from
non-rejecting (*p*=0.140) to rejecting (*p*=0.0179) — under matching, **all four corners
reject**, where three did before.

This is the same signature the synthetic arm found from the other side. There, more budget
made the *ensemble* relatively worse and eta2_surr rose; here, more budget makes *gradient and
CMA* relatively worse against perturbation and eta2_opt rises. Both are the behaviour of a
search process that finds more of a surrogate's exploitable optima when given more queries.

---

## DBM2 — CONFIRMED at the primary level, with a real qualification

eta2_surr at the primary level: off_off **0.043**, on_off **0.062**, off_on **0.037**, on_on
**0.050**. All below the 0.10 floor, all with point estimates in the bottom fifth of their own
bootstrap intervals. The surrogate null is not a budget artifact.

**The qualification, which is not optional.** At the secondary DOWN level (everyone gets
perturbation's small budget), eta2_surr rises in three corners and **on_off reaches 0.126 —
above the pre-registered 0.10 floor**. Under the registered rule the primary level decides, so
DBM2 is CONFIRMED; but the honest statement is that the surrogate null on Design-Bench is
**established at high budget and does not hold uniformly at low budget**. This mirrors the
synthetic arm exactly, where BM1's DOWN level put eta2_opt's CI upper bound above its KILL
threshold and the null was described as "established at high budget, underpowered at low
budget". The same sentence is now owed on Design-Bench, with the sign reversed.

At DOWN the optimizer axis also weakens sharply (eta2_opt 0.085–0.160), and in off_off the two
axes are effectively tied (opt 0.085 against surr 0.081). **Neither the null nor the inversion
is a low-budget phenomenon.** Any claim from this arm must state the budget.

---

## Validity: the native control reproduces the published corners

The native level exists because this runner fits each surrogate once per (task, seed) and
reuses it across optimizers, whereas `run_all` rebuilds per cell — so `perturb_opt`'s position
in the global numpy RNG stream differs, and comparing matched numbers against the *published*
unmatched ones would confound budget with call order. Registered as a required arm, and it
lands:

| corner | published eta2_surr / opt / *p* (`docs/MUJOCO_CHECK.md`) | this runner, native |
|---|---|---|
| off_off | 0.053 / 0.096 / 0.157 | 0.051 / 0.096 / 0.140 |
| on_off | 0.091 / 0.146 / 0.014 | 0.094 / 0.145 / 0.023 |
| off_on | 0.044 / 0.197 / 0.013 | 0.046 / 0.193 / 0.014 |
| on_on | 0.062 / 0.181 / 0.011 | 0.062 / 0.181 / 0.0076 |

Every eta2 agrees to within 0.004 and every Friedman *p* falls on the same side of 0.05. The
RNG-order concern that motivated the control turns out to be immaterial at 16 seeds — which is
itself worth recording, because it means the native-vs-matched contrast above is a budget
contrast and nothing else.

---

## Secondary task sets

| set | corner | eta2_surr | eta2_opt | *p* | leader |
|---|---|---|---|---|---|
| 5-task | off_off | 0.001 | 0.180 | 0.178 | perturb |
| 5-task | on_off | 0.013 | 0.278 | 0.0229 | perturb |
| 5-task | off_on | 0.001 | 0.303 | 0.0173 | perturb |
| 5-task | on_on | 0.007 | 0.290 | 0.0147 | perturb |
| noGFP | off_off | 0.041 | 0.256 | 0.0956 | perturb |
| noGFP | on_off | 0.012 | 0.361 | 0.0327 | perturb |
| noGFP | off_on | 0.035 | 0.373 | 0.0331 | perturb |
| noGFP | on_on | 0.011 | 0.360 | 0.0389 | perturb |

On the 5-task set the surrogate effect is at the floor twice over (0.001–0.013) while the
optimizer effect is 0.18–0.30. Dropping GFP does not change the picture. Both sets agree with
the primary; neither was allowed to decide.

**A note on GFP, which the probe flagged as the largest confound in the grid.** Its native CMA
spends **570** queries against gradient's 51,456 — a 90x imbalance, not the 8x seen elsewhere,
because at d=4,740 `cma_opt` switches to sep-CMA and converges almost immediately. Matching
raises it to 25,472 fevals. The 7-task and noGFP results move together, so repairing GFP's
starved CMA did not by itself drive the outcome — but this was the single place where the
confound could plausibly have manufactured the result, and it is now removed rather than
argued away.

---

## Two scope limits that travel with the promotion

1. **Within-corner bootstrap intervals overlap, and always did.** At the primary level:
   off_off surr [0.003, 0.341] against opt [0.055, 0.395]; on_on surr [0.004, 0.339] against
   opt [0.137, 0.490]. This was pre-registered as expected and no decision rule depends on a
   within-corner separation. The claim licensed is **point-estimate localization plus the
   cross-corner tracking argument** of `docs/MUJOCO_CHECK.md` — never "eta2_opt significantly
   exceeds eta2_surr". n=7 tasks is the binding constraint, as everywhere else in this paper.
2. **Every number here is budget-conditional.** The optimizer inversion and the surrogate null
   are both established at the matched high budget (Q = 25,600 X3-off / 51,456 X3-on). At the
   matched low budget the inversion narrows and on_off's eta2_surr breaches the floor. State
   the budget alongside K and beta whenever either quantity is quoted, exactly as 0-A.3
   requires on synthetic.

---

## What this changes

- **D19's optimizer half is no longer gated.** The qualifier "0-A.3 matched budgets on the
  seven synthetic tasks only; Design-Bench was not re-run under matching, so eta2_opt still
  leads in all four DB corners with D08's budget confound unremoved" is now discharged by
  measurement on the full 7-task grid including both MuJoCo tasks.
- **D08 (the budget confound) is removed on Design-Bench**, and the removal runs *against* the
  direction a reviewer would assume: matching strengthens the effect it was supposed to
  explain away.
- **Section 6 gains a sentence it could not previously write:** the Design-Bench omnibus
  rejects in all four corners under matched budget, and the rejection localizes to the
  optimizer axis in every one of them.
- **The low-budget qualification is new and must be carried**, in both directions — the
  optimizer inversion and the surrogate null each weaken at Q≈4,100–4,400.

**Merge recommendation: hold.** The branch carries the pre-registration, the probe, the
runner, the driver, the analyzer and 24 stamped artifacts. Folding this into `main` means
editing D19, §6 and the limitations paragraph together; that is a claim change and should be
made deliberately, not as a side effect of a merge.
