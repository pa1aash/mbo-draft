# Extension ledger

Sorted by acceptance-delta ÷ cost. Ten real options, not forty plausible ones.
Novelty status per `docs/NOVELTY_CHECK.md`. Predictions and kill criteria: `docs/PREREGISTRATION_V2.md`.

| ID | Idea | Type | Novelty | Prediction | Falsifier | CPU | Wall | Δaccept | Risk | Depends | Rec? |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **X1** | **Normalize the ensemble's targets (M0), re-run grid** | experiment | n/a (bug fix) | η²_surr drops materially; gap tracks `log\|y\|` before (ρ>0.6), not after | η²_surr ≈ 0.37 and no `\|y\|` correlation → confound refuted, headline *strengthened* | 1 grid | ~1 day | **HIGH** | none — decisive either way | — | **YES — first** |
| **X2** | **Report gradtune; re-scope the mechanism (P0-0)** | reframe | n/a | — | — | 0 | ~2 h | **HIGH** | reputational if omitted | — | **YES — unconditional** |
| **X3** | **Equalize the candidate/oracle protocol (P0-1)** | experiment | n/a (bug fix) | Ens×CMA improves; η²_inter shrinks | nothing moves → protocol was harmless | fold into X1 | ~2 h | **HIGH** | none | — | **YES — same run as X1** |
| **X4** | **Power analysis: "a discriminative offline-MBO suite needs ≥N tasks"** | reanalysis | **NONE FOUND** (measurement) | N ≫ 7; already have d_z=0.71 vs 0.81-needed from 5.1 | — | **0** | ~4 h | **HIGH** | none | 5.1 (done) | **YES — free** |
| **X5** | **M3 smoothness interpolation family** | experiment | partial — smoothness-helps is known (MS-DDEO 2022, RoMA); the *continuum* is not | gap, η²_surr, ĉ_ood, Friedman p all move together monotonically in α | they move independently → prior-match isn't one axis | 6 grids | ~3 days | **HIGH** | medium | X1 | **YES** |
| **X6** | **M2 roughen the GP (falsification test)** | experiment | NONE FOUND | Matérn-1/2 GP collapses under gradient; its coverage drops from 0.97 | rough GP stays robust → mechanism is not prior smoothness | 2 grids | ~1 day | **HIGH** | **the theory can die — that's the point** | X1 | **YES** |
| **X7** | **Full 3×3 coverage matrix (P0-3)** | reanalysis+exp | NONE FOUND | ĉ_ood correlates with score across 9 cells; Ens×CMA also ≈0.4 | Ens×CMA coverage high → "any aggressive optimizer" refuted | ~1 grid | ~1 day | MED-HIGH | none | X1 | **YES** |
| **X8** | **M5 learn the density ratio (close Prop 2)** | experiment | NONE FOUND (untried here) | partial repair; `w` unbounded, ESS collapses | full repair (good) or nothing (sharper negative) | ~0–1 grid | ~1 day | MED | low — all 3 outcomes publishable | X7 | **YES** |
| **X9** | **Demote Prop 1 to a remark citing Jin et al. 2021** | reframe | **PRIOR WORK FOUND** | — | — | 0 | ~1 h | MED (removes risk) | none | — | **YES — free** |
| **X10** | **M6 non-vacuous coverage bound** | experiment | NOT VERIFIABLE HERE | ĉ_ood degrades ≤ Φ(L, D, β) | bound is vacuous for unregularized ensembles — **likely** | ~0 | 1–2 days | HIGH if lands, **ZERO if not** | **high** | X1, M1 | only if time |

**Rejected, with reasons.** *DKL surrogate* (7.1) — genuinely the interesting one (GP head + neural features sits exactly on the smooth/jagged axis and would separate kernel from representation), but it adds a fourth surrogate to a grid whose existing three are not yet identified; **revisit after X1**. *Offline-RL cross-domain demo* (7.4) — a second paper, not a section. *Pip-installable diagnostic* (7.5) — the diagnostic's core signal is **not oracle-free** (5.1), so a standalone tool would ship something undeployable; **reject until X7 says what it can compute offline**. *TuRBO/Thompson optimizers* (7.2) — adds rows, not mechanism; and X3 already fixes the budget confound that makes the optimizer axis unreadable. *More Design-Bench tasks* (7.3) — X4 shows the suite can't resolve the question at any realistic N; adding 3 tasks doesn't reach the bar.

---

## The top five, with reasoning

**1 · X1 — normalize the targets and re-run.** Everything else is downstream. Right now "the GP's smooth
prior wins" and "the ensemble couldn't fit targets of magnitude 2600" predict the same table, and the
paper's controls cannot separate them (β=0 leaves the GP's *ranking* untouched — standardization is an
affine monotone transform of its LCB — while the ensemble's *training* pathology persists). One config
change, one grid, and the ambiguity is gone permanently. If η²_surr survives, this becomes the strongest
control in the paper. **The best CPU in the repo.**

**2 · X2 — report the gradtune sweep.** Zero cost, unconditional. The authors wrote a script whose stated
purpose was to kill the "under-tuned optimizer" objection, ran it, and it **failed its own pre-stated
decision rule on 3 of 4 tasks**. That result is in the released artifact. There is no version of this
where omission survives contact with a reviewer who opens the repo. Reported, it re-scopes the finding
into something still real and *sharper*: the collapse is a trust-region failure, and the coverage
diagnostic might predict which configurations collapse — which is the first genuinely *predictive* use
of the diagnostic anywhere in the project.

**3 · X4 — the power analysis, free.** 5.1 already produced it as a by-product: at n=14, **even a perfect
selection rule** clears only d_z = 0.71 against always-GP where 0.81 is needed for 80% power. That is not
a limitation paragraph, it is a **specification**: it says what a benchmark suite must be to answer the
question the field keeps asking it. `NOVELTY_CHECK` Q5 says the Design-Bench *complaint* is known but the
*measurement* is not — this is the measurement. It converts Contribution 3 from "we found nothing" into
"here is why nothing is findable here, and here is the N at which it would be." Costs zero CPU.

**4 · X6 — roughen the GP.** The cheapest way to risk the theory. Two grids. The paper currently has four
controls, all subtractive, all confirming. A reviewer reads that as assuming the conclusion. One
falsification test — *the theory forbids a rough GP from being robust* — is worth more than a fifth
confirming control, and if it fails the authors learn it before a reviewer does.

**5 · X5 — the smoothness interpolation family.** The most expensive of the five and still worth it: it
replaces the paper's weakest claim (a **two-point** comparison at N=7 with p=0.69 and a TOST the abstract
already concedes is underpowered) with a **trend across six α-levels** — which needs no equivalence test
and no N=7 apology. It also unifies Contributions 2 and 3 into one curve: Design-Bench stops being a
different world and becomes a point on an axis. The `ScaledAckley` ladder infrastructure for it already
exists in `PREREGISTRATION.md:32-36` and was never run.

**On X4 + X5 together:** they are the two halves of a defensible Contribution 3 — X4 says the current
benchmark *cannot* answer the question, X5 builds a benchmark that *can*. That pairing is a stronger
paper than either alone, and neither depends on the offline-selection idea that 5.1 killed.
