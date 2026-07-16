# Venue norms (verified 2026-07-17)

Bears directly on `DECISION_QUEUE.md` D1 and `PAPER_V2_OUTLINE.md`.

| Venue | Not-SOTA explicitly OK? | Negative results explicitly welcome? |
|---|---|---|
| **ARR (ACL)** | **Yes** (heuristic H5) | **Yes** (H6) — the only venue with both |
| **NeurIPS 2026** | implied | **Yes — a new submission category**, at an explicitly *higher* bar |
| NeurIPS 2023-25 | No (2024 was pro-SOTA) | Silent |
| **TMLR** | **Yes**, verbatim | Silent — permissive by omission |
| ICLR 2023-26 | **Yes**, verbatim FAQ | Silent |
| ICML 2024-25 | Silent | Silent |
| **AAAI** | **Silent — and presumes SOTA framing** | **Silent. No negative-results track.** |

## The finding that matters

**NeurIPS 2026 introduced author-selected Contribution Types**, one of which is **Negative Results**
(https://neurips.cc/Conferences/2026/ReviewerGuidelines). Verbatim:

> "**Negative Results:** The main contribution is in understanding a negative result. (The significance
> and originality bar for these contributions is high.)"
> "it is important that the negative result not be simply an empirical observation that some experiment
> did not turn out as expected or hoped. It is important that a negative result be grounded in deeper
> analysis..."
> "**Originality — Unexpected or surprising in some way.** ... it should run counter to a popularly held
> understanding."

**Double edge.** NeurIPS admits negative results *as a category* while setting a **higher** bar than
General papers on two of four criteria, and requires them to be **surprising**. A well-executed null
that confirms what people already suspected is explicitly excluded.

**Read for this paper.** The Design-Bench null alone would *fail* that bar — "benchmarks don't
discriminate" is not surprising (`NOVELTY_CHECK` Q5: the complaint is known). But **"the GP advantage is
prior smoothness, not calibration"** *does* run counter to a popularly held understanding, and X4's power
specification is the "deeper analysis" the guideline demands. That is Identity C, not the current draft.

**AAAI, by contrast, is silent and its only SOTA reference presumes SOTA framing** ("What are the
limitations in the state of the art that the paper addresses?"). (AAAI text came via WebFetch
summarization, not raw fetch — lower confidence than the others.)

### CORRECTION: AAAI's guidelines are silent, but its record is not

An earlier draft of this file — and my session report — concluded AAAI was the *worst* fit of the venues
surveyed. **That was wrong, and a verified counterexample refutes it at exactly this venue.**

> Henderson, P., Islam, R., Bachman, P., Pineau, J., Precup, D., & Meger, D. (2018). **Deep
> Reinforcement Learning that Matters.** *Proceedings of the AAAI Conference on Artificial
> Intelligence*, **32(1), 3207–3214.** https://doi.org/10.1609/aaai.v32i1.11694
> **AAAI Technical Track: Machine Learning** — the main track. ~2,397 citations (S2).

No new method. Pure measurement. Accepted on the main technical track and now a canonical citation.
**The genre is not disqualified at AAAI; it is under-signalled in AAAI's guidelines.** Absence of an
explicit welcome is not evidence of rejection — it means the bar is set by precedent, and the precedent
is Henderson.

⚠️ **Citation trap:** Semantic Scholar reports `year: 2017` (back-propagated from arXiv v1, 1709.06560)
while still listing venue AAAI and pages 3207–3214. **Cite AAAI 2018, not 2017.** Citation counts
disagree ~57% across sources (S2 2,397 vs OpenAlex 1,526); report a range if quoted.

**What Henderson has that a bare null lacks** — the same anatomy as Recht:

| Element | Henderson et al. |
|---|---|
| **Mechanism** | An explicit seven-factor intrinsic/extrinsic taxonomy (hyperparameters, architecture, reward scale, seeds, environments, codebases, reporting), one section each |
| **Surprise finding** | Same algorithm, same hyperparameters, **only the random seed varies** → statistically different distributions. `t = −9.0916, p = 0.0016` (TRPO, HalfCheetah-v1) |
| **Methodology** | t-test, Kolmogorov–Smirnov, bootstrap percent-difference with 95% CI (10k iters), power analysis |
| **Prescription** | "the most important step to reproducibility is to report all hyperparameters, implementation details, experimental setup, and evaluation methods" |
| **Corrected leaderboard** | **No** — explicitly disclaims one |
| **Scale claim** | **No** — deliberately narrow to policy-gradient continuous control |

**Two consequences for us, and they cut in opposite directions.**

1. **AAAI is viable.** Identity A or C can land here; the venue has published this genre in the main
   track. `PAPER_V2_OUTLINE.md`'s P(accept) reasoning should be read with that precedent in mind, and
   the "AAAI is the worst fit" line in my session report is **retracted**.
2. **Henderson is also a threat, and a mirror.** Its thesis is that unreported implementation details
   determine results. `FLAW_LEDGER.md` P0-0 (an unreported trust-region setting decides the collapse)
   and P0-2 (unreported target normalization decides the surrogate gap) are *Henderson's thesis
   instantiated in our own artifact*. A reviewer who knows this paper — and in offline MBO, many will —
   reads our omissions through it. Note also that Henderson's headline (seeds alone shift the
   distribution) bears directly on **T7**: our seed-0 fixed dataset leaves data-draw variance
   unestimated while the ANOVA treats tasks as the sampling unit.

**The honest read:** Henderson raises AAAI's ceiling for this paper *and* raises the cost of shipping
P0-0 unreported. Both follow from the same citation.

## Alternatives if the AAAI window is tight

- **MLRC 2026 is now an official NeurIPS track**, routed through TMLR. Hard deadline **2026-09-30**.
  "MLRC welcomes rigorous work across the full spectrum of outcomes, including positive confirmations of
  prior results, partial replications, and **failures to reproduce**." Papers publish in TMLR proceedings,
  presented at NeurIPS.
- **TMLR** directly: "novelty of the studied method is not a necessary criteria for acceptance."
  But TMLR explicitly rejects bare nulls without "generalizable insights" / "actionable lessons."

## Pattern across accepted measurement papers

"Are GANs Created Equal?", Musgrave's metric-learning reality check, Dacrema's recsys "phantom progress",
Recht et al. — the shared shape is **a specific, named, falsified belief plus a reusable protocol**.
A bare null has neither.

### The template, verified in detail: Recht et al. (ICML **2019**, oral; PMLR v97:5389-5400)

Exact title: *"Do ImageNet Classifiers Generalize to ImageNet?"* — Recht, Roelofs, Schmidt, Shankar.
~2,201 citations (S2-via-Consensus, refresh date **NOT VERIFIED**; do **not** use OpenAlex, which splits
the record across two IDs and undercounts by >5x). The CIFAR-10 predecessor (arXiv:1806.00451) was
**never peer-reviewed** — it was *subsumed* into the ICML paper, so cite ICML 2019 for both results.

**Correction to how this paper is usually invoked, including by me above.** It is **not a null result.**
It found a *large* difference (11-14% ImageNet accuracy drops) and then showed the **obvious explanation
for that difference was wrong**. Its contribution rests on the gap between two findings pointing in
opposite directions: accuracy drops sharply, *but* "accuracy gains on the original test sets translate to
**larger** gains on the new test sets" — a fitted slope of **1.11 [1.07, 1.19]** on ImageNet, CI
excluding 1.0. Adaptive overfitting predicts *diminishing* returns; they measured the opposite, and so
rejected adaptivity in favour of distribution shift.

Its anatomy is the checklist a measurement paper must pass:

| Element | Recht et al. |
|---|---|
| **Named belief, refuted** | "Conventional wisdom suggests that such drops arise because the models have been adapted to the specific images" → "**Adaptivity is therefore an unlikely explanation**" |
| **Mechanism, shown by manipulation** | Three sampling strategies (`TopImages`/`Threshold0.7`/`MatchedFrequency`) **dial the drop up and down** by varying only annotation difficulty. Not a robustness check — the causal argument. |
| **Artifact released** | ImageNetV2 (3 x 10,000 images), CIFAR-10.1 |
| **Prescriptions** | 5 named, incl. a "super hold-out" kept hidden for years |
| **Scale** | 34 CIFAR-10 + **67** ImageNet models (appendix count; often miscited as 66); 208,145 candidate images |
| **Surprise** | Core of the paper — the result runs counter to the popular understanding |

**Why this matters for us.** The causal move — *vary one knob and watch the effect dial up and down* —
is structurally identical to **X5** (`MECHANISM_EXPERIMENTS.md` M3: sweep α, watch gap / η²_surr / ĉ_ood /
Friedman p move together). That is the strongest evidence this template is the right one to copy, and it
is further reason X5 outranks another subtractive control. Note also that Recht et al. clears NeurIPS
2026's "surprising" bar precisely *because* it refutes a named belief — the Design-Bench null does not,
but "the GP advantage is prior smoothness, not calibration" would.

Standalone negative-results venues fail (JINR: one paper in 18 years; JNRBM: closed 2017). Negative
results survive only when attached to an existing conference (ICBINB: 7 years, 61 papers; Insights:
~118 papers).

**NOT VERIFIED:** ICBINB 2026 PMLR volume; Insights acceptance rates; SIGIR 2026 verbatim scope.

### Verified anatomy of the other two precedents

**Musgrave, Belongie & Lim — "A Metric Learning Reality Check."** ECCV 2020, LNCS **12370:681-699**,
DOI 10.1007/978-3-030-58595-2_41. S2 537 cites (OpenAlex's 68 is a known LNCS consolidation failure —
do not cite it). Contribution: a **new metric** (MAP@R), a **new protocol** (4-fold class-disjoint CV,
50 iters Bayesian opt, 10 runs, 95% CIs), **three named flaws** (unfair comparisons; misleading accuracy
metrics; training with test-set feedback — "breaks one of the most basic commandments of machine
learning"), and a **corrected leaderboard**. Artifact: `powerful-benchmarker` — **not**
`pytorch-metric-learning`, which is a separate arXiv-only paper (2008.09164) by the same authors.

**Ferrari Dacrema, Cremonesi & Jannach — "Are we really making much progress?"** RecSys 2019,
**101-109**, DOI 10.1145/3298689.3347058 — **Best Long Paper**. Follow-up: TOIS 39(2) Art. 20, 2021
(cite **2021**; S2 wrongly dates it 2019). **Surname is "Ferrari Dacrema" — cite under F, not D.**
18 relevant / 7 reproducible (RecSys); 26 / 12 (TOIS). Result is stronger than a null: on Epinions,
non-personalized **TopPopular beat every personalized method**.

**The uncomfortable part.** Dacrema's named mechanism is *our* ledger:

> "**Lack of proper tuning of baselines:** *This is probably the most striking observation of our
> analysis*... Researchers apparently invest significant efforts in optimizing their own new method but
> do not pay the same attention to their baselines... Probably, this behavior might be the result of a
> **confirmation bias**."

`FLAW_LEDGER.md` P0-2 is an unnormalized baseline; P0-0 is an untuned baseline optimizer whose tuning
sweep was run and not reported. The field's canonical measurement paper names this exact failure mode
as its central finding — and our paper is a measurement paper that commits it. Reviewers in this genre
know that sentence. Fixing X1/X2 is not just about being right; it is about not being the example.

TOIS also supplies the prescription template (§5.4, modeled on the Pineau ML Reproducibility Checklist)
and the multiplicity argument we need for X4: "if a researcher collects 10 accuracy metrics and only
reports the significant ones (significance 0.05), then the probability of reporting a progress that is
only virtual jumps from 5% to 40%." (5.1 ran 10 rules and reported all 10 — that discipline is already
in `PREREGISTRATION_V2.md` commitment 5.)
