# Improvement map — what compute can fix, what it cannot

**As of 2026-07-19, against `paper/aaai27/main.tex` at Stage 2.2.** Every limitation the paper
states is listed exactly once, in exactly one of the three lists. The point of list (C) is to
stop us spending pod hours on things pod hours cannot buy.

---

## (A) Fixable by compute

Ordered by how much of a reviewer objection each removes per pod-hour.

### A1. Design-Bench optimizer axis is provisional — **DONE, FOLDED 2026-07-20**

**Status: DONE.** Run as 0-C (`docs/DB_BUDGET_MATCH.md`, `results/db_budget/`, pre-registered
at `100d2ed` before launch). Folded into the paper and the ledger on 2026-07-20: D19 promoted
PROVISIONAL → **LANDED**, §6 gained a matched-budget paragraph plus a validity paragraph, and
the provisional language was struck from §6 and from the limitations paragraph.

**What the paper said before.** "The optimizer half of this section stays provisional: budget
matching ran on the synthetic tasks only, so Design-Bench carries Confound 5 unremoved on
exactly the axis carrying the effect here, and we do not promote it on a synthetic-only arm."
That sentence no longer exists in the paper.

**What it bought — more than was scoped.** The scoping note below predicted the claim bought
would be *unconfounded, not larger*. **The measurement bought both.** Matching roughly doubles
eta2_opt in every corner (0.096→0.180, 0.145→0.255, 0.193→0.282, 0.181→0.281) while eta2_surr
falls in all four, and off_off moves from non-rejecting (p=0.140) to rejecting (p=0.0179), so
all four corners reject where three did. The presumed confound ran **backwards**: gradient's
11.8x native budget was masking the optimizer effect, not manufacturing it. That gives the
paper a second axis on which correcting a confound strengthens the effect, which is now stated
alongside the synthetic 0.37→0.405 result in the limitations section.

**Two scope limits carried into the paper, both mandatory.** (i) Established at **high budget**
— at the matched DOWN level eta2_surr reaches 0.126 in on_off (above the 0.10 floor) and the
two axes tie in off_off (0.085 against 0.081). (ii) **Within-corner CIs overlap**, so the
licensed claim stays point-estimate localization across corners, never a within-corner
separation.

**Also landed:** the GFP budget catch (native CMA 570 queries against gradient's 51,456, a 90x
imbalance, now matched to 25,472) and the native control, which reproduces the published
corners to within 0.004 on every eta2 and the same side of 0.05 on every Friedman p — so the
native-vs-matched contrast is a budget contrast alone, not an RNG-order artifact.

**What it did not buy.** It does not touch the *surrogate* null on DB, which remains
power-bound (see C1).

### A2. The MuJoCo rejection rests on point estimates, not separated intervals

**What the paper says now.** "Our limit: within any one corner the two intervals overlap, so
this localizes point estimates across corners rather than separating the axes inside one."
(§ Design-Bench Results.)

**The experiment.** Raise DB seeds from 16 to 64 on the 7-task set, all four corners. The
bootstrap intervals on eta2_surr and eta2_opt are seed-limited as much as task-limited at
n=16; quadrupling seeds should roughly halve the interval widths.

**What it buys.** If eta2_opt's interval clears eta2_surr's inside a rejecting corner, the
MuJoCo defense upgrades from a cross-corner tracking argument to a within-corner separation,
which is strictly stronger and removes the stated limit.

**Risk.** The intervals may still overlap — the task axis (n=7) contributes variance that
seeds cannot reduce. Worth one run, not three.

### A3. Width sweep stops at w=1024, where the interval is widest

**What the paper says now.** "The interval widens monotonically with w (0.211 -> 0.439),
making w=1024 the least precise point on the curve, so the supported claim is that the gap
*does not close*, not that it is identical there."

**The experiment.** Add seeds at w=1024 only (18 -> 60), and optionally one more rung at
w=2048. Cost is dominated by the wide arm; the narrow rungs are already precise.

**What it buys.** A tighter interval at the widest point makes the non-closure claim harder to
dismiss as an artifact of imprecision at the one rung that matters to the NTK objection.

**What it cannot buy.** The asymptotic claim. See C3 — this is a precision fix at practical
widths only, and the scope sentence stays either way.

### A4. Ant freeze is read on 2 of 3 GP cells, one benchmark

**What the paper says now.** "It is two of three Ant GP cells, not three---the gradient cell
returns 1.3242 +/- 0.1975 and is not frozen."

**The experiment.** Run the frozen-cell detector (exact-constant across seeds, std == 0) across
all Design-Bench tasks x all 9 cells x 4 corners, not just TF-Bind-8 and Ant. Cheap: it is a
read over existing per-seed artifacts plus any missing corners.

**What it buys.** Turns "we found frozen cells on two tasks" into a census with a rate. If the
rate is non-trivial, M-A (LCB paralysis) generalizes from an explanation of two awkward tasks
to a property of the benchmark, which materially raises the finding's value.

### A5. Budget matching has one matched level plus one secondary

**What the paper says now.** "The secondary budget level does not corroborate cleanly (0.066
[0.014, 0.340] at Q=4,352), so the null is established at high budget and underpowered at low."

**The experiment.** Add two intermediate matched levels (Q ~ 12,000 and ~25,000) on the
synthetic grid. Four points instead of two gives a budget-response curve for eta2_opt rather
than two disagreeing endpoints.

**What it buys.** Either the curve is monotone — in which case "established at high budget,
underpowered at low" becomes a stated trend with a shape — or it is not, which is itself worth
knowing before a reviewer finds it.

### A6. Synthetic datasets are drawn once at seed 0

**What the paper says now.** "The synthetic datasets are drawn once at seed 0, so reported
variance is training and optimization variance, not data-draw variance."

**The experiment.** Re-draw the offline dataset at 5 dataset seeds and re-run the on_on corner
only (7 tasks x 9 cells x 5 dataset seeds x 10 training seeds).

**What it buys.** Converts a stated scope limit into a measured variance component. If the
data-draw component is small, the limitation paragraph loses a line; if large, we have found a
real caveat before review did.

**Honest cost note.** This is the most expensive job on the list and the least likely to change
a headline. Schedule it last.

---

## (B) Improvable, but not by compute

### B1. The paper has one figure

Stage 2.2 dropped the width figure and the Design-Bench table to hold 7 pages after adding the
seventh elimination. Both were fully redundant with prose, so nothing was lost in content — but
a 7-page empirical paper carrying one figure and two tables reads thin. **Fix by redesign, not
by re-running:** a single composite figure (width flatness + normRMSE crossover + the
distance/oracle landscape law from the seventh elimination) would restore the visual argument
in the footprint of one float. The landscape scatter over 5,040 optima is the most compelling
image the project has and currently appears nowhere.

### B2. The seventh elimination's landscape law has no figure

rho(distance, oracle) = -0.818 and rho(distance, inflation) = +0.758 over 5,040 returned optima
is a strong, visual result stated only as two numbers. Highest-value single figure available.

### B3. Related work cites the two-axis precedents twice

The introduction names fANOVA / Liang / Moosbauer and Background repeats the pointer. Fine as
is, but if space is needed later this is the cheapest 2 lines in the paper.

### B4. The C2 mechanism section is now seven eliminations long

At seven, the section risks reading as a list. A short framing sentence up front stating what
class of explanation each control belongs to (uncertainty, capacity, effort, accuracy,
geometry, premise, landscape) would make it read as a designed sweep rather than an
accumulation. Pure writing.

### B5. Kim et al. (kim2025mbosurvey) is the load-bearing novelty citation

The N6 claim rests on one survey sentence. A second independent source conceding the same
attribution gap would harden it. This is a literature search, not a run.

### B6. No anonymized artifact link in the submission

The links block is commented out in `main.tex`. AAAI reviewers reward a working anonymous repo.
Decision needed before submission, not compute.

---

## (C) Structural — compute cannot fix these

State these plainly so we stop proposing runs against them.

### C1. n=7 tasks binds the corner decomposition, the optimizer interval, and the DB omnibus

**Why compute cannot fix it.** The bootstrap intervals here are dominated by the *task* axis,
and tasks are not seeds. Adding seeds shrinks within-task variance and leaves the between-task
term alone; the corner CIs (widths 0.26-0.34 against a corner range of 0.167) would not
separate at 1,000 seeds. The only fix is *more tasks*, and the synthetic suite is 7 by design
while Design-Bench ships the tasks it ships.

**What would actually change it.** Adding genuinely new task families — which changes the
benchmark, not the compute budget, and would make the numbers non-comparable to the published
ones the audit is auditing. That trade is not worth it: the paper's job is to audit *this*
comparison.

**Consequence, already in the paper and staying there:** "no detectable difference at this
power, not equivalence," with the power/N specification attached. This sentence is
non-negotiable — Agarwal and Demsar are held by exactly the reviewer pool this paper targets.

### C2. Elimination is not mechanism, and no number of eliminations becomes one

**Why compute cannot fix it.** Seven controls now exclude seven explanations. An eighth
excludes an eighth. Ruling out explanations is *logically* incapable of establishing one, no
matter how many run. The paper says so: "a diagnosis, not a mechanism with a positive causal
test behind it."

**What would actually change it.** A manipulation that moves the proposed causal variable and
moves the gap with it, with the surrogate still predicting. We have tried twice. The smoothness
arm moved roughness by 98% and widened the gap. The phantom-maxima arm's second limb found the
manipulation unavailable at this operating point — the GP is nowhere in a prior-reversion
regime inside the feasible cube, so the knob does not turn. The remaining candidate is the
bidirectional smoothness manipulation's *roughen-the-GP* arm, which is void for a structural
reason (a posterior mean conditioned on ~800 points is smooth from the conditioning, not the
kernel) and not for a budget reason.

**Read this as the finding it is.** A confound taxonomy's job is to remove the explanations a
reader reaches for first. Seven, each with a control and an interval, is that job done about as
far as it goes. The honest ceiling is a *localized* loss — real, at the returned optimum's
oracle quality, at matched distance and matched inflation — and the paper now states it that
way.

### C3. NTK limits are asymptotic; the width sweep is not

**Why compute cannot fix it.** Jacot/Lee are statements about w -> infinity. No finite sweep
reaches an asymptote. A2's extra rung at w=2048 buys precision at practical widths and moves
the claim not one inch toward an asymptotic one.

**Consequence, already in the paper and staying there:** "the sweep stops at 1024 while the
kernel limits are asymptotic, so this answers the objection at practical widths and makes no
asymptotic claim," and "the supported claim is that the gap *does not close*, not that it is
identical there."

### C4. The genre-shape is prior work and always will be

Henderson, Ferrari Dacrema, Musgrave, Lucic and Agarwal own the reality-check shape. No
experiment makes the move novel in kind. The residual is compositional and the paper concedes
the shape by name in the introduction — which is what makes the composition credible. Compute
spent trying to make the shape novel is compute wasted.

### C5. The two-axis novelty claim is a negative literature result

"We know of no prior instance in offline MBO" cannot be *proven* by any run. It is bounded by
search coverage (documented in `docs/NOVELTY_V3.md`), and a single counterexample would sink
it. The mitigation is B5 — more search — not compute.

---

## One-line scheduling call

**A1 is done and folded.** Run **A4** next (cheap, generalizes M-A), then **A2**. Hold A5 and A3
unless a reviewer asks. Do not schedule A6. Never schedule anything against list (C).
