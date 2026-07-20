# Findings ledger — running

Orchestrator-level verdicts. Each traces to fetched primary full text or to a repo artifact.

---

## ENVIRONMENT LIMITATION (belongs in "What I could not verify and why")

`hyperresearch fetch` **cannot ingest PDFs in this environment.** Every arXiv PDF URL form
returns `Skipped junk content: Binary PDF garbage in content`:

```
https://arxiv.org/pdf/2111.14756        -> junk
https://arxiv.org/pdf/2111.14756.pdf    -> junk
https://arxiv.org/pdf/2111.14756v1      -> junk
```

One subagent diagnosed this as missing pymupdf. **That diagnosis is wrong** — it tested the
system `python3`. The interpreter hyperresearch actually runs
(`/opt/homebrew/Caskroom/miniforge/base/bin/python3.13`) has PyMuPDF 1.27.2.3 installed and
importable. So the fault is in the fetch/extraction path, not a missing dependency.

**Consequence for this audit, stated plainly:** vault notes for PDF sources contain only the
arXiv *abstract page* (~650-750 words), not full text. Full-text verification was done by
`curl` + `pdftotext -layout` outside the vault, then grepped. **The verdicts below do rest on
primary full text** — the method constraint "FETCH PRIMARY AND GREP" is satisfied — but the
full text is not stored in the vault, so a later reader cannot re-grep it from the note. Any
verdict resting only on a stored note body is weaker than one resting on the external
extraction, and I mark which is which.

---

## MANDATORY FIX 1 — `fan2024minucb` is a triple miscitation (batch 4)

Primary: Fan, Wang, Ng, Hu, "Minimizing UCB: a Better Local Search Strategy in Local
Bayesian Optimization", **arXiv:2405.15285, NeurIPS 2024** (venue/year confirmed, DOI
10.52202/079017-4151). Full text extracted and grepped (1550 lines).

### 1a. "The reading of a UCB-style acquisition as local search" is not established prior work
The paper under audit writes: *"as is the reading of a UCB-style acquisition as local search
\citep{fan2024minucb}"* — presenting it as an **established result** it merely applies.

Fan et al.'s own words: *"we **propose** our first algorithm... MinUCB, which **replaces**
gradient descent step with a step that minimizes the UCB in GIBO"*; *"This discovery is also
meaningful as it **opens up possibilities for new designs**."*

So it is a **method they propose**, not a reading the field had established. The underlying
local-search-via-two-stage-GP premise traces to **GIBO (Müller, von Rohr, Trimpe,
arXiv:2106.11899, NeurIPS 2021)**, which Fan et al. explicitly modify — and GIBO's own
exploitation step is plain gradient descent, with no UCB or LCB anywhere.

**Fix:** either re-attribute the premise to GIBO (and TuRBO for the trust-region/stalling
language), or restate Fan et al. as a *recent method proposal* rather than an established
reading. The phrase "applied and diagnosed rather than discovered" cannot stand against a
2024 method paper.

### 1b. The LCB-paralysis citation inverts the source's central result — most serious
The paper under audit: *"The surviving mechanism is LCB paralysis: the GP's lower confidence
bound is locally maximal at the data, so the optimizer never leaves... This is the offline
instance of a known reading of UCB-style acquisitions as local search \citep{fan2024minucb},
applied rather than discovered."*

Full-text grep of Fan et al.: **0 hits** for `offline`, `LCB`, `lower confidence bound`,
`stuck`, `frozen`, `freeze`, `paralysis`.

Fan et al. define `UCB(x) = μ(x) + βσ(x)` and **minimize** it because their objective is
`min f(x)`. They never treat a maximization setting and never perform the mirror transform.
Decisively: **their Theorem 1 proves MinUCB converges to a genuine local optimum** —
contingent on an *increasing* β schedule and *continual active resampling every iteration*,
both structurally impossible on a static offline dataset. The paper under audit cites this
convergence result as authority for an "optimizer never leaves" **failure** mode.

**Fix (mandatory).** Drop `fan2024minucb` from the LCB-paralysis sentence. The freeze is the
paper's own empirical finding — bit-identical constants across 16 seeds, in two GP classes,
on a continuous task with no decode step — and it is *stronger* unattributed than
mis-attributed. If a precedent is wanted for generic BO stalling, TuRBO's *"shrink [the trust
region] when the optimizer appears stuck"* is closer, though still not the same claim.
**Note this fix costs the paper nothing and removes a reviewer's cleanest kill.**

### 1c. The distance-aware co-citation is unsupported
Scope paragraph: *"Nor do we claim... distance-aware uncertainty as ours
\citep{liu2020sngp,fan2024minucb}."* Fan et al. has **0 hits** for `distance-aware`; it uses
vanilla GP posterior variance and never analyses distance awareness. **Fix: remove
`fan2024minucb` from that co-citation.**

---

## MANDATORY FIX 2 — `liu2020sngp` is cited against its own thesis (batch 3)

Primary: Liu et al., SNGP, arXiv:2006.10108, NeurIPS 2020. Full text extracted and grepped.

The paper under audit: *"σ is a distance signal, not an error signal... this is the corrected
measurement, **bounded by prior work on distance-aware uncertainty**
\citep{liu2020sngp,vanamersfoort2020duq}."*

**SNGP argues the opposite, about the exact model class at issue.** Verbatim from SNGP's
Figure 1 discussion:

> "deep ensembles (Figures 1b, 1g) and MC Dropout... are based on dense output layers that
> are **not distance aware**. As a result, both methods quantify their predictive uncertainty
> based on the distance from the decision boundaries, **assigning low uncertainty to OOD
> examples even if they are far from the data**."

SNGP's Definition 1 formalises input-distance-awareness as a property standard deep models
**lack** — that lack is SNGP's motivation. Independently corroborated by DUQ
(arXiv:2003.02037), verbatim: *"DUQ is certain only on the data distribution, and uncertain
away from it: the ideal result. **Deep Ensembles is uncertain only along the decision
boundary, and certain elsewhere.**"*

Additional scope problem: **all SNGP experiments are classification** (2D toy, Wide-ResNet on
CIFAR, ImageNet, BERT). **Zero regression experiments.** The paper under audit is regression.

**Fix.** The claim cannot be "bounded by" SNGP — SNGP predicts the opposite for ensembles.
Two honest options: (i) reframe as a *contrast* — "unlike the ensembles SNGP and DUQ
characterise as distance-unaware, ours shows a modest positive distance correlation
(ρ≈0.26)", which is a weaker but defensible and genuinely more interesting claim; or (ii)
drop the bounding citation and present ρ≈0.26 as a bare measurement on this grid. Option (i)
is better: a result that runs against SNGP's characterisation is more publishable than one
that leans on it, provided it is labelled as such.

---

## MANDATORY FIX 3 — the σ-distance-vs-error dichotomy is contradicted (batch 3)

Direct contradiction found, in regression, peer-reviewed:

**Carrete et al. 2023**, J. Chem. Phys. 158:204801 (arXiv:2302.08805), neural-network force
fields, a regression task. Verbatim: *"the Spearman correlation coefficient between
uncertainty and error over the validation data set is **0.90 for the committee and 0.91 for
the bootstrap-aggregation ensemble**."*

That is **13×** the paper's ρ≈0.07, in regression. It is measured in-distribution; on their
genuinely OOD test the correlation degrades per-atom while staying informative aggregated —
which is precisely the ID/OOD distinction that matters here.

**Two consequences, and the second is the more useful one:**

1. The framing "σ is a distance signal, **not** an error signal" cannot stand as a general
   property. **Fix: scope it to this grid** — "on our tasks, σ tracks distance more than
   error" — rather than as a correction to a general belief.
2. **A confound the paper should check, flagged by Lakshminarayanan's own paper**
   (arXiv:1612.01474): an ensemble trained with plain MSE using cross-member empirical
   variance as σ *"consistently underestimates the true predictive uncertainty"* (an 80%
   nominal interval covering ~20% of test points), whereas the NLL-trained heteroscedastic
   variant is well calibrated. **The paper's ensemble is exactly the MSE/empirical-variance
   construction** (supplement: "K=5 MLPs... MSE"). So ρ=0.07 may be a property of a
   known-inferior uncertainty construction rather than of ensembles per se. **This is a live
   alternative explanation for Elimination 1 that the paper has not eliminated** — and it is
   cheap to test.

Also worth stating: the literature does **not** treat distance-awareness and error-tracking
as mutually exclusive. SNGP explicitly ties distance-awareness to calibration. The paper's
dichotomy may be a false one, which is a framing fix independent of the numbers.

---

## MANDATORY FIX 4 — the N9 "no precedent" claim has a serious methodological challenge

Two sources bear directly on the paper's second-most load-bearing novelty claim: *"We
searched the ML reality-check and reproducibility literature for a de-confounding audit
reporting a corrected variance-explained statistic above its own published value and found
none."*

### 4a. Confound-leakage — the field's documented base-rate explanation for this exact direction
**Hamdan, Love, von Polier, Weis, Schwender, Eickhoff, Patil, "Confound-leakage: Confound
Removal in Machine Learning Leads to Leakage" (arXiv:2210.09232, 2022).** Verbatim abstract:

> "this common approach to confound removal **biases ML models, leading to misleading
> results**. Specifically, this common deconfounding approach **can leak information such
> that what are null or moderate effects become amplified to near-perfect prediction** when
> nonlinear ML approaches are subsequently applied."

**This is not a kill on N9's novelty — different genre (confound-removal methodology, not a
benchmark reality-check) — but it is worse than a kill in one respect.** It establishes that
in the ML literature where "confound removal increased an effect" has actually been studied,
the documented default diagnosis for that direction is **leakage artifact, not validity**.

**Fix (mandatory, and it is a strengthening if done well).** The paper currently treats the
upward direction as merely *unprecedented* and defends it as *not statistically surprising*
(citing `bressan2019confounds` on suppression). That defence is now insufficient: there is a
named ML failure mode that produces exactly this signature. The paper must **affirmatively
rule out confound-leakage** as the mechanism for its own increase. Cheaply, it can: its
corrections are a target rescaling and a candidate-selection rule, neither of which
regresses out a confound from features, so the leakage mechanism does not apply — but that
argument has to be *made on the page*, because a reviewer who knows this paper will
otherwise supply the leakage explanation for free. **Add `hamdan2022confoundleakage` to the
bibliography and dispatch it in two sentences.**

### 4b. The broader rhetorical framing is contradicted (narrow claim survives)
**Maassen, van Assen, Nuijten, Olsson-Collentine, Wicherts, PLOS ONE 2020** — systematic
recomputation of 500 primary effect sizes across 33 psychology meta-analyses. Verbatim:

> "We did not find any evidence for systematic bias in meta-analytic results; we estimated
> **19 pooled effect sizes to be larger** than originally reported and **14 to be smaller**."

Corrections go up about as often as down, with no systematic bias, in the one large-scale
systematic audit of recomputed effect sizes in a mature empirical science.

**This does not kill the paper's narrow claim**, which is explicitly scoped to "the ML
reality-check and reproducibility literature". It does kill the *implication* the surrounding
prose carries — that an upward correction is an intrinsically surprising direction. The paper
half-anticipates this already ("Nor is the direction statistically surprising"), so the fix
is small. **Fix: cite Maassen et al. at that sentence.** It converts a hedge into a supported
statement and costs nothing.

**Net assessment of N9 after both.** The narrow scalar claim ("no ML de-confounding audit
reports a corrected variance-explained statistic above its published value") is **not killed**
by anything found so far. But it is now bracketed on both sides — by a documented ML
mechanism that produces upward moves illegitimately (4a), and by a documented non-ML
literature where upward moves are unremarkable (4b). The honest framing is narrower and
more defensible than the current one. See the ranked section for whether this claim is worth
its prominence at all.

## MANDATORY FIX 5 — **THE CONTRADICTION LANDS. L/R/W tested K=2 and found robustness.**

This is the single most consequential deliverable-(i) finding so far, and it is exactly the
contradiction the task asked to hunt for.

**The paper's claim (Confound 3):**
> "Our sweep runs over $K\in\{2,3,5,10\}$ and therefore **extends below** the $K\in\{5,10\}$
> range over which ensemble surrogates were found robust \citep{li2024bnnsurrogates},
> **sharing its two upper points and adding $K{=}2,3$**."

**What Li/Rudner/Wilson actually did.** Figure A.7 tests ensemble size at **K = {2, 5, 10}**.
Verified twice over — textually in the full text (16,554 words, fetched via the arXiv HTML
rendering) and visually by rendering PDF page 28, whose legend reads "2 Models / 5 Models /
10 Models" across 15 BO benchmarks. Their verbatim finding:

> "We compare the behavior of ensembles with different numbers of models, and we find that
> **the different ensembles perform similarly across many experiments, showing the robustness
> of our results to this hyperparameter.**"

A second K=2 appearance is in Figure A.5. The main text adds: *"we find that these
hyperparameters generally have minimal effects on the performance."*

**So the range is {2,5,10}, not {5,10}. L/R/W already went down to K=2, and found robustness
there.** The paper's "extends below" claim is false as written, and the specific novelty it
asserts — "sharing its two upper points and adding K=2,3" — collapses to "adding K=3".

**Why this is worse than a wording error.** The paper's K-sensitivity framing exists to
establish that its headline sits at the *maximum* of a sensitive curve. L/R/W is the closest
prior work and it reports the opposite conclusion (robustness) over an overlapping range
including the very endpoint the paper claims to have added. A reviewer from that group — a
live possibility in a small community — reads this as the paper claiming credit for an
experiment they ran.

**Fix (mandatory, and it must be a real fix, not a hedge).**
1. Correct the range to `K∈{2,5,10}` wherever `{5,10}` appears.
2. Restate the residual honestly: the paper adds **K=3**, and, more importantly, reports
   **η²-sensitivity** where L/R/W reports **performance robustness**. Those are different
   quantities — L/R/W measures whether ensemble BO performance changes with model count; the
   paper measures whether the *variance attributed to the surrogate axis* changes. **That
   distinction is the paper's actual defence and it is currently not made anywhere.** Made
   explicitly, the claim survives in a narrower and more interesting form: "L/R/W find
   ensemble *performance* robust to model count over {2,5,10}; we find the *variance
   decomposition* is not robust over {2,3,5,10}, which is a different and complementary
   sensitivity."
3. Do not delete the K-sensitivity result — it is real on this grid. Delete the "extends
   below" priority claim.

## MANDATORY FIX 6 — `abe2022ensembles` does not support the direction it is cited for

**The paper's claim (Confound 3):** *"the decline with $K$ runs against **the direction
reported for ensemble quality** \citep{abe2022ensembles}."*

**What Abe et al. actually did.** Full text extracted (15,095 words). Abe et al.
("Deep Ensembles Work, But Are They Necessary?", NeurIPS 2022, arXiv:2202.06985) runs **zero
ensemble-size ablation**. Their configuration is fixed — M=4 on CIFAR-10 ("combining 4 out of
the 5 random seeds") and M=5 on an ImageNet subset, fixed by seed availability rather than
swept. Their thesis is *ensembles versus a single larger model*, not quality as a function of
K. **There is no reported direction-with-K in this paper to run against.**

**Fix.** Replace with the source that does report it: **Lakshminarayanan, Pritzel & Blundell
(NeurIPS 2017, arXiv:1612.01474), Table 4**, ImageNet M=1→10, monotonic diminishing-but-never-
negative improvement (Top-1 error 22.166% → 18.675%), verbatim: *"We observe that as M
increases, both the accuracy and the quality of predictive uncertainty improve
significantly."* Note the honest caveat: that is classification calibration, not offline-MBO
reward, so the cross-domain transfer must be stated rather than assumed. `abe2022ensembles`
can stay in the paper for what it does support (ensembles vs. a single larger model) or be
dropped.

## MANDATORY FIX 7 — `melis2018sota` cannot carry "audits normally shrink" (H4 confirmed)

**The paper's claim, made twice and load-bearing for Contribution 2:**
> "Audits in this genre **usually shrink** the effect they audit \citep{melis2018sota}."
> "...a direction with no precedent we could find in the ML audit literature, **where audits
> normally shrink** \citep{melis2018sota}."

**What Melis et al. actually says.** Full text verified. Their finding: *"Once hyperparameters
have been properly controlled for, we find that LSTMs outperform the more recent models,
contra the published claims."* That is a **ranking reversal** — an old baseline beating newer
architectures — **not a shrinking effect size**, and certainly not a law about the direction
an entire genre runs. Melis explicitly frames itself as *one instance*: *"this paper joins
other recent papers in warning of the under-acknowledged existence of replication failure in
deep learning."* Full-text search found **no sentence anywhere** asserting a genre-wide
directional pattern.

**Fix.** The generalisation is the paper's own, and it must be labelled as such. Two options:
(i) recast as an observation over named instances — Melis, Ferrari Dacrema, Musgrave, Lucic
each independently show a *claimed advantage* shrinking or reversing, and cite all four for
the pattern rather than one for a law; or (ii) drop the "normally" framing and say only that
the audits the paper surveyed moved downward. **Option (i) is stronger and nearly free** —
the paper already cites all four papers elsewhere in its genre paragraph. As written, one
citation is asked to certify a claim about a literature, which is the exact defect this audit
was commissioned to find.

## VERIFIED CLEAN — citation traps and quoted figures (batch 6)

All checked against primary full text. **These pass and should be reported as passing.**

| Item | Status |
|---|---|
| Henderson = **AAAI 2018** | ✓ confirmed from the PDF copyright line, "Copyright © 2018, AAAI". The 2017 is the arXiv posting date |
| Benavoli = **JMLR vol 17 (2016)**, arXiv 1505.02288 (2015) | ✓ both confirmed; trap real, paper has it right |
| Li/Rudner/Wilson = **ICLR 2024** | ✓ "Comments: ICLR 2024" on the arXiv page; v1 May 2023, v2 camera-ready May 2024 |
| Recht slopes **1.69** (CIFAR-10), **1.11** (ImageNet) | ✓ verbatim from the regression equations, and the paper's characterisation of their meaning is accurate |
| Benavoli cited for "mean-rank conclusions depend on the pool" | ✓ verbatim: *"the outcome of the mean-ranks test depends on the pool of algorithms originally included in the experiment"* |
| Agarwal cited for never-claim-equivalence | ✓ verbatim: *"lack of statistically significant results does not demonstrate the absence of effect"* |

## VERIFIED — the paper's own numbers and code (orchestrator, local)

See `local-checks.md`. Summary: all four corner η² point estimates and CIs, the corner range,
interval widths, Elimination 1's seven figures, the inversion counts (7/7, 3/7, 2/7), the
`mbo.py` line traces for Confounds 1 and 2, and the engine-stamping protocol all reproduce
exactly. **One** figure does not: "five other cells tie it" should be six.

Plus a free win: bootstrap bias correction moves the headline 0.367→0.405 to 0.351→0.395 —
direction survives, effect **grows**.
