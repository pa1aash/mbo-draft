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

---

## Late upgrade: X4 is stronger than its row says — it fills a named 20-year-old gap

A ~20-search sweep of the power-analysis literature returns a clean partition by *which sample-size axis*
a paper treats:

| Axis | Owned by |
|---|---|
| # test examples | Card et al., *With Little Power Comes Great Responsibility*, **EMNLP 2020** (2000-sentence MT test sets ≈ **75% power** to detect 1 BLEU) |
| # seeds / runs | Colas et al. (arXiv-only); **AdaStop, TMLR 2024** — *"Researchers in Deep RL often use less than 5 independent executions ... this is not enough in general"* |
| # topics / queries | Sakai (SIGIR 2016; Springer 2018, *topic set size design*); Urbano et al. (SIGIR 2019) |
| **# tasks / datasets** | **NOBODY — VERDICT: NONE FOUND** |

**Demšar (JMLR 2006) — the exact paper our CD diagram cites — identified this gap and left it open.**
He establishes Friedman + Nemenyi over multiple datasets and *observes* that Nemenyi's critical value can
be too large to detect real differences, i.e. that the procedure is underpowered when datasets are few.
**He never turns that observation into a power or sample-size analysis. Nobody has since, in 20 years.**

**So X4 is not a limitation paragraph. It is a contribution that closes a named gap in the canonical
reference this paper already depends on** — and 5.1 has already produced its core number for free
(a *perfect* selection rule reaches d_z = 0.71 where 0.81 is needed for 80% power at n=14).

**Method to borrow:** Sakai's *topic set size design* (Springer 2018, Ch. 7) is the closest template —
topics are to IR test collections what tasks are to a benchmark suite; it determines how many topics a
collection needs from a prior similar experiment. That is exactly the shape of "how many tasks must an
offline-MBO suite have."

**Revised ranking.** X4 moves to **joint-first with X1/X2**: zero CPU, novel, fills a 20-year gap, and
it is the "deeper analysis" NeurIPS 2026's Negative Results bar explicitly demands (`VENUE_NORMS.md`).
It also converts Contribution 3 from the paper's weakest half into a *specification*, and it pairs with
the Design-Bench App. D.3 framing (`NOVELTY_CHECK`): the field deleted GFP/UTR/ChEMBL for showing this
result, without ever computing how many tasks would be needed to detect it.

⚠️ **Bibliographic caution:** the most quotable seed-count sources are the weakest venues — Colas et al.
2018 is **arXiv-only**, Colas et al. 2019 is a **workshop** paper, Picard is arXiv-only. Cite **AdaStop
(TMLR 2024)** and **Card et al. (EMNLP 2020)** as the peer-reviewed anchors. Agarwal et al. (NeurIPS 2021
Outstanding Paper) is *not* a power paper — it argues for quantifying uncertainty at small N rather than
prescribing N, which is the opposite move; cite it for interval estimates/IQM, not for power.

### X4 — one reviewer trap to pre-empt (from an adjacent-literature sweep)

A sweep of the LLM-eval power literature is **tangential** (different field, different axis) and mostly
confirms the partition above: even there, the only papers where power is *the* headline are 2026 ICML
**workshop** posters; everything at main-conference level treats it as supporting. Task-count power stays
unowned. Two items are worth carrying:

**The trap.** *tinyBenchmarks* (Maia Polo et al., **ICML 2024**, PMLR v235:34303-34326, **267 cites**) and
*100 instances is all you need* (arXiv:2409.03563) are sample-size papers that ask the **inverse**
question: how *few* items suffice to estimate **one model's score** cheaply. X4 asks how *many* units are
needed to **detect a difference between methods**. Those are different questions on different axes —
theirs is items-within-a-task, ours is tasks-within-a-suite — but the titles collide, and **a reviewer may
cite "100 instances is all you need" against "your suite is too small."** Pre-empt it in one sentence:
estimation efficiency for a single score is not detection power for a contrast, and item count is not task
count. Do **not** cite them as support; they are the opposing framing.

**A usable anchor.** Miller, *Adding Error Bars to Evals* (arXiv:2411.00640) — *"new evals should contain
at least 1,000 questions in order to have good signaling ability"* — is a signaling-ability threshold,
i.e. a power claim, and is the cleanest citable N in that literature. ⚠️ It is **arXiv-only, never peer
reviewed** (v1, no journal-ref; DBLP files it under "Informal and Other Publications") despite ~96
citations and Anthropic branding. Its peer-reviewed counterpart is Bowyer et al., **ICML 2025 Spotlight**
(PMLR v267:81143-81184), which is narrower — interval validity, not power. Cite Bowyer for the venue and
Miller for the number, and never imply Miller is peer-reviewed.
