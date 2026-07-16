# Three candidate papers from the same repo

Presented, not chosen. `P(accept)` reasoning is relative to the current draft's baseline, which I
put at **very low** — not because the science is weak but because `docs/FLAW_LEDGER.md` P0-0 means a
reviewer who opens the artifact finds a control refuting the mechanism.

**Identity B is dead.** It was contingent on 5.1, and 5.1 **FAILS** — structurally, not incidentally.
`ĉ_ood` requires evaluating true *f* on the proposals, the one query offline MBO forbids; the
oracle-free feature set spanning all 14 tasks is a single binary flag; and at n=14 no rule could have
been certified regardless. It is documented below for completeness and to record *why* it is dead,
because the reason is itself publishable.

---

## IDENTITY A — Measurement, repaired

**One sentence.** The reported GP advantage in offline MBO is a surrogate-class effect, not an
optimizer effect — measured under a controlled factorial that survives normalizing the ensemble,
equalizing the candidate protocol, and tuning the gradient optimizer.

**Title.** *Decomposing the GP Advantage in Offline Model-Based Optimization*

**Abstract skeleton.** Confound → first controlled surrogate×optimizer factorial → η²_surr vs η²_opt
**after** target normalization and protocol equalization → the pre-registered optimizer hypothesis was
refuted → the ensemble's gradient collapse is a *trust-region* artifact, not surrogate geometry (we
report our own sweep) → coverage diagnostic as a remark → benchmark null with a power specification.

**Sections.** 1 Intro · 2 Related (Li/Rudner/Wilson ICLR 2024 positioned honestly) · 3 Grid · 4 Results
· 5 Coverage remark · 6 Design-Bench null + power analysis · 7 Limitations.

**Survives:** the factorial design (novelty: **NONE FOUND**), the complete 14-task grid, η² (reproduces
to 8dp). **Required:** X1, X2, X3, X4, X9. **Optional:** X7.
**CPU:** ~1–2 grid runs (~2 days incl. edits).

**P(accept): low-to-moderate.** Ceiling is real: `NOVELTY_CHECK` Q1 says Li/Rudner/Wilson already owns
"deep ensembles perform relatively poorly" and "ranking is problem-dependent, suggesting tailored
inductive biases." Strip that and what is new is *the factorial design* and *the offline setting* — a
methodological contribution reviewers describe as "an ablation." The known-accepted pattern for this
genre ("Are GANs Created Equal?", Musgrave's metric-learning reality check, Dacrema's recsys "phantom
progress") is: a *specific, named, falsified belief* + a *reusable protocol*. A has the first if X1
holds. It does not have the second.

---

## IDENTITY B — Diagnostic as method ❌ **DEAD**

**Would have been.** Coverage-driven offline surrogate×optimizer selection; the null becomes the
motivation; the diagnostic becomes the method.

**Why it's dead.** 5.1 ran the pre-registered rule and its kill criterion fired: regret **0.348** vs
the honest fixed-cell baseline's **0.233** — *identical to random* (0.348), 0 wins / 3 losses / 11 ties.
Two structural reasons, either fatal alone:
1. **The signal isn't oracle-free.** `ĉ_ood = mean(f_o >= mu_o - q*sig_o)` with `f_o = task.oracle(xf)`
   (`mbo.py:599`). Oracle-*contaminated* features do carry signal (regret 0.171, 7W/2L, paired CI
   excluding zero) — **the predictive signal lives precisely in the quantity offline MBO cannot compute.**
2. **n=14 cannot resolve it.** A *perfect* rule reaches d_z = 0.71 vs 0.81 needed for 80% power.

**Novelty (moot but recorded).** `NOVELTY_CHECK` Q4: the *problem* is named in the Design-Bench
conclusion and the Kim TMLR survey; offline RL has a mature policy-selection literature; MS-DDEO
(SWEVO 2022) already selects an offline surrogate pool *by smoothness*; CC-Select (2026) uses
calibration as a selection signal outside MBO. Only **joint surrogate+optimizer cell selection via
conformal premise-coverage** was NONE FOUND.

**What to salvage.** Finding (1) is a genuine contribution to state in one paragraph: *the diagnostic
that best predicts which configuration wins is not computable in the setting that needs it.* That is a
real obstruction, not a failed experiment. Finding (2) becomes X4, the power analysis — which is
load-bearing for both A and C.

---

## IDENTITY C — Mechanism

**One sentence.** Prior–task smoothness match is the single axis governing the GP–ensemble gap, the
gradient collapse, the coverage failure, and the synthetic→real transfer — demonstrated by manipulation
in **both** directions and by a continuous interpolation that reproduces the Design-Bench null as a
limit point.

**Title.** *Smoothness Is the Axis: What the GP Advantage in Offline MBO Actually Measures*

**Abstract skeleton.** The GP advantage is attributed to calibration; we show it is prior smoothness →
we *manipulate* it in both directions (smooth the ensemble → gap closes; roughen the GP → GP collapses,
a **risked prediction**) → we build a task family continuously varying prior-match and show gap, η²_surr,
ĉ_ood, and Friedman p move together → **Design-Bench is not a different world; it is a point on this
axis** → the benchmark null follows as a corollary, with the N required to detect it.

**Sections.** 1 Intro · 2 Related · 3 Grid + repairs · 4 The gap tracks smoothness · 5 Manipulation
(both directions) · 6 The interpolation family · 7 Design-Bench as a limit point + power spec · 8 Limits.

**Survives:** everything A survives, plus the coverage instrument as *evidence* rather than as a
contribution. **Required:** X1, X2, X3, X4, X5, X6. **Optional:** X7, X8, X10.
**CPU:** ~9–10 grid runs (~1 week incl. edits). All CPU-only.

**P(accept): moderate-to-good — the highest of the three.** It has what A lacks: a **risked prediction**
(X6 — the theory forbids a rough GP from being robust) and a **mechanism demonstrated by manipulation**
rather than by subtraction. It converts the null from the paper's weakest half into a corollary.

**The honest risk:** `NOVELTY_CHECK` Q2 — "surrogate smoothness helps offline optimization" is
**already established** (MS-DDEO 2022 grades surrogates by smoothness; the Kim survey lists smoothness
priors / RoMA). C's novelty is narrower than it sounds: it is *attribution of the GP's advantage to mean
smoothness rather than calibration*, plus the continuum. That is defensible — but it is **exactly the
claim X1 might destroy**, since unnormalized targets are an alternative explanation for the same table.
**C is a bet on X1's outcome.** Run X1 before committing to C.

---

## What is achievable, and where B and C compose

**A ⊂ C.** C's required set is A's plus X5 and X6. There is no reason to build A and *then* C — build
A's repairs (X1–X3), read the result, and let it decide whether C is available.

**B and C were complementary, not exclusive** — C would have supplied the mechanism explaining *why*
B's selection signal worked. With B dead, C absorbs B's only survivor: the obstruction result (the
signal isn't computable offline) is a natural discussion point in C's coverage section, and B's power
analysis (X4) is load-bearing for C's Section 7.

**Recommended sequencing, deadline-dependent** (see `DECISION_QUEUE.md` D1):

| Time available | Do |
|---|---|
| **< 2 weeks** | Do not submit. X1–X3 alone will not land, and shipping without X2 is the worst option on the board. |
| **~3–4 weeks** | **Identity A.** X1, X2, X3, X4, X9. One grid run. Honest, repaired, thin. |
| **~6–8 weeks** | **Identity C.** X1–X6 (+X7). ~10 grid runs, CPU-only. The paper worth writing. |

**My read:** A is a repair; C is a paper. The gap between them is ~8 grid runs of CPU and one week —
cheap for what it buys. But **X1 gates both**, and X1 can refute C's thesis outright. Run X1 first,
read it honestly, then choose. If X1 shows the gap was target scaling, neither A nor C exists as
drafted — and that is worth knowing in week one rather than in review.

**Venue note.** If the AAAI window is too tight: MLRC 2026 is now an **official NeurIPS track** (via
TMLR, hard deadline 2026-09-30) and states explicitly that *"negative results and partial failures to
reproduce are as valuable as confirmations."* AAAI has **no** negative-results track. That is a real
option for the A-shaped version, and it is a better fit than forcing A through AAAI main.
