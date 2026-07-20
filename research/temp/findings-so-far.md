# Findings ledger — running

Orchestrator-level verdicts. Each traces to fetched primary full text or to a repo artifact.

---

## N6 — INTERIM VERDICT: NO KILL FOUND, but the near-miss list must expand

Batch 1 swept the 2026 recency frontier: eight offline-MBO / offline-BBO papers from Jan–Jun
2026, full PDFs extracted and grepped for all twelve decomposition terms (`factorial`,
`crossed`, `ANOVA`, `analysis of variance`, `eta squared`, `η²`, `main effect`, `variance
decomposition`, `two-way`, `interaction effect`, `attribution`).

**Result: 0 hits, all 8 papers, all 12 terms.** Verdicts: 6 IRRELEVANT (single surrogate, or
single fixed optimizer, or bundled whole-system leaderboards), 1 survey, 1 NEAR-MISS. None of
Hutter / Liang / Moosbauer is cited or extended by any of the eight.

**No paper satisfies all four conjuncts. N6 is not killed by the 2026 frontier.**

### But two NEW near-misses were found, both closer than the prior pass's three

**NM-A — Tan et al., RaM (arXiv:2410.11502, ICLR 2025), Table 3 "Versatility of ranking
loss".** A genuine **9 × 2 crossed grid** in offline MBO: nine methods/optimizers against two
surrogate-loss types (MSE vs ListNet), verbatim *"fixing their open-source codes by replacing
MSE with ListNet when training the forward model"*. Reporting is descriptive only — Score±std
and %Gain, zero ANOVA or variance-decomposition language.

**This is the most important N6 finding of the session, for three reasons:**

1. **It is the closest near-miss that exists.** Hutter is one-way and not offline; Liang is
   online and descriptive; Moosbauer is HPO and declines the analysis. RaM Table 3 is
   *offline MBO*, *genuinely crossed*, and *contemporaneous*. Only the two-way decomposition
   is missing.
2. **The paper cites `tan2025ltr` and its characterisation is incomplete rather than false.**
   *(I overstated this on first pass and am correcting it — the distinction matters.)* The
   intro says: *"surrogate-class comparisons **hold the optimizer constant**
   \citep{tan2025ltr,li2024bnnsurrogates}."* That is **accurate about RaM's main experiment**
   — the 5-surrogate Spearman comparison does hold gradient ascent fixed. Table 3 is a
   *separate* versatility check in the same paper. So the sentence is not false; it is
   **incomplete in the one way that matters**, because the same paper it cites for
   one-axis-at-a-time also contains a crossed grid it does not mention.
3. **The prior audit missed it.** The vault holds three earlier fetches of this same paper
   from the previous pass; none mentions Table 3. All three analysed only the main
   experiment. **This is the concrete demonstration that the prior audit's verdicts had to be
   re-checked rather than trusted** — the instruction to treat NOVELTY_V3 as prior rather
   than fact paid for itself here.

**The residual survives on THREE grounds, not one — and none of them is currently on the page.**

| Ground | Why RaM Table 3 is not a kill |
|---|---|
| **Loss type ≠ model class** | Table 3 swaps the surrogate *training objective* (MSE vs ListNet). N6 is about surrogate *model class* (GP posterior vs ensemble disagreement). A loss swap inside one model family is not a class comparison. |
| **Bundled methods ≠ an optimizer factor** | The nine are whole *methods* — BO-qEI, CMA-ES, REINFORCE, Grad. Ascent, CbAS, MINs, Tri-Mentoring, PGS, Match-OPT. CbAS is generative, MINs is inverse modelling, PGS is policy search. These bundle a search routine with a modelling strategy; they are not nine settings of a clean optimizer factor. The paper's own grid deliberately isolates three *numerical search routines* against one shared protocol. |
| **Descriptive reporting** | Score±std and %Gain per cell. Zero ANOVA, zero variance decomposition (0 grep hits). |

**Fix (mandatory, and it is a strengthening).** Name RaM Table 3 explicitly as the nearest
crossed design in offline MBO, and state the three grounds above. This is *better* for the
paper than silence: a residual defended on three independent grounds against the closest real
competitor reads as rigour, whereas an unmentioned near-miss discovered by a reviewer reads as
an omission. The reviewer most likely to find it is Tan et al.

**NM-B — DiBO (arXiv:2603.17919, 2026), Table 2.** Crosses backbone (diffusion vs
autoregressive) × training stage (DA / SFT / RL) in a genuine 2×3 grid. Descriptive only
(mean±std). Weaker than NM-A because a training *stage* is not an optimizer routine, but it
belongs in the near-miss list as the 2026 entry.

### The three prior near-misses: ALL RE-CONFIRMED, AND NONE EXTENDED

Batch 2 re-fetched all three fresh (no cached verdicts) and ran the extension check.

| Near-miss | Re-confirmed as near-miss? | Verbatim evidence |
|---|---|---|
| **Hutter 2014** (fANOVA, ICML) | ✓ **one-way only** | Table 1 caption: fANOVA computed *"based on data from one SMAC run"*. Finding: *"the most important hyperparameter was the model class used"*, range **31%–58%** (YEAST 31, AMAZON 58, MNIST-BASIC 55, KDD09 41, CIFAR-10 53). Zero hits for factorial/crossed/two-way/OFAT/offline. |
| **Liang 2021** (npj Comput Mater) | ✓ **crossed but descriptive, and online** | Genuine surrogate × acquisition grid; **zero** ANOVA/fANOVA/eta-squared hits; reports only Enhancement Factor / Acceleration Factor; explicitly *"closed-loop active learning"*. |
| **Moosbauer 2022** (IEEE TEVC) | ✓ **names fANOVA and declines it** | Verbatim: *"any interactions between inputs cannot be detected by an OFAT analysis"* — appearing immediately after they name ANOVA/fANOVA as the standard method and decline it on cost grounds. §6.3 confirms their actual methodology is OFAT from one optimized configuration. |

**A false-positive worth recording.** Liang's full text returns 14 hits for `crossed` — all of
them the **"Crossed barrel" dataset name**, a homonym, not evidence of a crossed design. This
is precisely the trap that makes grep-count-only verdicts unsafe, and it is why the method
constraint forbids snippet-level conclusions. Anyone re-running this audit with a naive grep
would score Liang as crossed.

**THE EXTENSION CHECK — the half a re-audit usually skips.** Forward-citation walk over
**~347 citing papers** (62 Hutter, 166 Liang, 4 Moosbauer, 115 van Rijn & Hutter; restricted
to 2023–2026 where volume required). Six candidates deep-verified, two fetched in full:

- **EXPObench (2023)** — 6 surrogate algorithms × 4 real problems; zero ANOVA/factorial hits;
  its "offline" refers to offline surrogate *training*, not offline MBO. **NOT A KILL.**
- **Bischl et al. 2023 HPO survey** (836 citations, the highest-cited Moosbauer citer) — zero
  ANOVA/factorial hits; cites Moosbauer only as related work. **NOT A KILL.**
- **PED-ANOVA**, quantum-NN fANOVA lineage, CART-ANOVA transfer learning, Instance Space
  Analysis — all extend fANOVA *within one algorithm's hyperparameter space*, or apply
  crossed ANOVA in unrelated domains. Never surrogate × optimizer in offline MBO. **NOT KILLS.**

Semantic Scholar returned HTTP 429 throughout (shared rate limit across concurrent batches);
OpenAlex carried the walk. Recorded as a method limitation, not a gap in the conclusion.

### The offline-MBO field's own benchmarks: no kill surface either

Batch 7 swept Design-Bench, RaM, SOO-Bench, COMs, RoMA and the Kim review for the seven
decomposition terms. **Every paper returned 0 genuine hits.** A handful of raw `anova`
substring matches across four papers are all false positives — the author surnames
*Usmanova* / *Bozhanova* recurring in shared bio-design bibliographies. Another homonym trap.

**SOO-Bench characterisation VERIFIED.** Its actual contribution is a *stability indicator*
tracking whether an algorithm degrades relative to the offline dataset during optimization.
The paper's description — "stress-tests optimizer **stability** rather than attribution" — is
accurate. Design-Bench, RaM, COMs and RoMA all treat surrogate+optimizer as **one bundled
atomic method per baseline**, never crossed independently, which is exactly the confounded
status quo the paper says it dissects.

### Kim survey — venue RESOLVED, and a contextual over-read found

**Venue confirmed: Transactions on Machine Learning Research, 01/2026.** Every page header of
v2 (6 Jan 2026) reads "Published in Transactions on Machine Learning Research (01/2026)",
independently corroborated by arXiv:2603.04000's bibliography citing it as TMLR 2026.

So the paper's prose ("the subfield's 2026 survey") is **accurate**, and the **bib entry is
stale**: `@article{kim2025mbosurvey, journal={arXiv preprint arXiv:2503.17286}, year={2025}}`.
**Fix: update to TMLR 2026.** This resolves L3a in the paper's favour — the prose was right
and the bibliography was wrong, not the other way round.

**Contextual over-read (minor but real).** The quoted sentence — *"existing benchmarks often
emphasize overall optimization performance without clarifying whether observed gains stem
from superior surrogate modeling, improved optimization strategies, or mere chance"* — sits in
§6 under "Uncertainty Estimation of Surrogate Model", framed around **uncertainty-quantification
evaluation gaps**, not as a call for a crossed factorial. The paper presents it as *"the field
certifying that the attribution is unresolved"*. The quote is verbatim and does say what it
says, so this is not a miscitation — but the framing implies a stronger, more targeted
endorsement than its context supports. **Fix (light): keep the quote, drop the implication
that the survey is calling for this specific design.**

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
mis-attributed. **Note this fix costs the paper nothing and removes a reviewer's cleanest kill.**

**Correction to my own earlier suggestion.** I first proposed TuRBO as a closer precedent for
generic BO stalling. **A later check shows that is wrong and I withdraw it.** TuRBO's grep
counts: `trapped`=0, `greedy`=0, `local search`=2, `trust region`=20. Its diagnosis of vanilla
global BO is the **opposite** of trapped-near-the-data — verbatim: *"an overemphasized
exploration that results from global acquisition"* and *"a failure to exploit promising
areas."* TuRBO's locality is a mechanism it deliberately **imposes** (explicit trust regions
borrowed from stochastic-optimization TR methods), not an intrinsic acquisition behaviour it
diagnoses.

**So no one owns "LCB is locally maximal at the data so the optimizer never leaves."** Not Fan
(who proves convergence), not TuRBO (who diagnoses the opposite), not GIBO (whose exploitation
step is plain gradient descent). **The right move is to claim it as the paper's own observation
on its own grid** — which the evidence fully supports — rather than hunting for a citation that
does not exist. That is a *better* outcome for the paper than the fix I first proposed.

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

**VERIFIED FIRST-HAND BY THE ORCHESTRATOR — this finding is not relay-dependent.** I fetched
arXiv:2305.20028v2 directly (39 pages, 111,042 chars) and extracted the Figure A.7 legend
tokens from page 28: `['2 Models', '5 Models', '10 Models']`. Independently, the batch reached
the same result by rendering that page as an image. Corroborating grep counts on the same
full text: `offline` = **0**, `ANOVA` = 0, `factorial` = 0, `crossed` = 0, `variance
decomposition` = 0 — which simultaneously confirms the paper's N6 defence (L/R/W is online BO
with no decomposition) and refutes its K-range claim.

Their verbatim finding, from the Figure A.7 caption on the same page:

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

## FIX 7.5 (MODERATE — corrected downward after I checked the primary myself)

**I initially recorded this as the audit's most serious finding, on a subagent's report that
the proposition omits a load-bearing hypothesis. I then read the supplement myself and the
report was overstated. Correcting, because propagating an overstatement is precisely the
failure this audit exists to catch.**

**What the supplement actually says** (`supplement.tex:48`):
> "Under a shifted proposal $\Pi\neq P$ **with density ratio $w=d\Pi/dP$**, validity is
> restored by weighting the calibration quantile by $w$ (weighted conformal)."

It defines $w$ as **the true density ratio**, not an estimate. So the statement *"weighting by
$w$ restores validity"* is exactly Tibshirani et al.'s Theorem 2 and is **formally correct as
written. The proposition is not missing a hypothesis, and it is not wrong.** My earlier
framing was wrong and is withdrawn.

**What is genuinely true, and still worth a fix.** The clause is **formally correct and
practically inert in the paper's own setting**, and the paper never says so.

Verified against the primaries: Tibshirani et al.'s exact guarantee holds for **known** $w$;
their abstract separates the estimated-$\hat w$ case (*"known — or, in practice, can be
estimated accurately"*) and supports it **empirically only** (91.0% vs 90% nominal, airfoil,
5,000 splits), with **no theorem bounding the $\hat w$ coverage gap**. Angelopoulos & Bates
corroborate verbatim: *"This algorithm addresses a somewhat restricted case—that of a known
covariate shift"*; *"exact when the magnitude of the distribution shift is known."*

In this paper $\Pi$ is the distribution of designs an optimizer proposes after ascending a
surrogate — the setting where $w$ is least knowable, and arguably not well-defined, since the
proposals are the output of a deterministic optimization concentrated on a low-dimensional
set. So the shift-limited transfer clause is **stated but never operationalized**: nothing in
the paper estimates $w$ or applies weighted conformal. The supplement's own measurements are
consistent with that — conformal repair *"restores in-distribution coverage to its 0.90 target
on every task but **leaves OOD coverage erratic**"* (0.00 on Styblinski, Griewank, UTR, Ant,
D'Kitty).

**Fix (moderate, one or two sentences).** Note after Proposition 2 that the covariate-shift
clause requires a known or reliably estimable $w$, that no such estimate is available for
optimizer-generated proposals, and that the clause is therefore stated for completeness rather
than applied. **Then take the free win:** the erratic OOD coverage the supplement already
reports is *what one should expect* when the repair's precondition is unavailable — not an
anomaly. Saying so converts an unexplained table into a correctly-scoped negative result, and
it reinforces the paper's separate argument that premise coverage is separable from
optimization outcome.

**Severity: moderate, not severe.** It is a scoping omission around a correct proposition, not
a defect in a proof. Ranked in deliverable (i) below the Demšar fabrication and the Fan
inversion, not above them.

**Process note worth carrying into the report's methodology section.** Two of the subagent
relays in this audit overstated a finding in the direction of severity (this one, and the RaM
"false vs incomplete" item). Both were caught by reading the primary source directly. Any
verdict in the final report that rests only on a relayed summary, and not on text I read
myself, is marked as such.

## MANDATORY FIX 8 — `demsar2006statistical` does not contain the threshold it is cited for

**The paper's claim (§Design-Bench Results, `main.tex:220`):**
> "we are below the threshold for the test we ran: **this omnibus is recommended for more
> than ten datasets** \citep{demsar2006statistical}"

**What Demšar 2006 actually contains.** Full 30-page JMLR PDF extracted and grepped. **There
is no "more than ten datasets" recommendation anywhere in the paper.** The only occurrences of
"ten data sets" describe **Demšar's own power-simulation sampling procedure** — the setup of
his simulation study — not a usage threshold for the Friedman test.

**VERIFIED FIRST-HAND by the orchestrator**, not via relay. I fetched the JMLR PDF (30 pages,
103,393 chars) and grepped it directly:

| Pattern | Occurrences |
|---|---|
| `more than ten` | **0** |
| `at least ten` | **0** |
| `ten or more` | **0** |
| `ten data sets` | 2 — **both describing Demšar's own simulation sampling** ("samples of ten data sets were randomly selected…", "1000 random selections of ten data sets") |

**This is a fabricated threshold attributed to a real source** — not an over-read of something
stated loosely, but a specific numeric recommendation the source does not make.

**And it inverts Demšar's actual rationale, which is the part that matters.** What he does
recommend, verbatim:

> "we recommend a set of simple, yet safe and robust non-parametric tests… **the Friedman test
> with the corresponding post-hoc tests for comparison of more classifiers over multiple data
> sets**"

No dataset-count floor is attached anywhere. And his stated design context is explicitly the
*small-n* regime:

> "The nature of our problems does not give any provisions for normality and **the number of
> data sets is usually much less than 30**."

**Demšar recommends the non-parametric route precisely because n is small.** The paper cites
him as establishing that the omnibus needs n > 10 — the opposite of his reasoning.

**Fix (mandatory), and it is a net gain for the paper.** Delete "recommended for more than ten
datasets" and the Demšar citation from that clause. Then note that the *conclusion* is
unaffected and better supported without it:

- The power limitation is real and independently established by the rest of the same sentence
  — the paired-test calculation (`|d_z| ≥ 1.27` for 80% power at α=0.05, n=7) and Agarwal's
  never-claim-equivalence point, both verified.
- Demšar's recommendation, correctly read, **endorses** using Friedman at n=7 rather than
  disqualifying it. The paper was conceding a methodological weakness it does not have.

So the fix removes a false warrant *and* removes an unnecessary self-deprecation. **The claim
survives; the paper's standing improves.**

## MANDATORY FIX 9 — η² is a biased estimator at n=7 and the paper never says so

Two independent lines converged on this, one from the paper's own artifacts and one from the
literature.

**From the literature (batch 9).** η² and partial-η² are **positively biased** estimators of
variance explained; **ω² and ε² are the bias-corrected alternatives** and are the recommended
reporting choice at small n (Kelley 1935; Olejnik & Algina 2003, ~1,647 citations; verified
via the JOSS `effectsize` documentation, which quotes both — the primary sources are paywalled,
recorded as a limitation).

**From the paper's own bootstraps (orchestrator, local — see `local-checks.md` §L2.6).** The
bootstrap mean exceeds the point estimate in **all four corners**, by +0.0099 to +0.0184. That
is the bias, and the paper's artifacts already estimate it.

**The paper reports η² at n=7 throughout — in the abstract, the headline, every corner, the β
axis and the budget axis — with no bias caveat and no bias-corrected alternative.**

**Fix, and it is a strengthening not a concession.** Report ω² or ε² alongside η², or report
the bootstrap-bias-corrected values. **I checked what happens: the headline claim gets
stronger.** Bias-corrected, the two protocol confounds move the surrogate effect
**0.351 → 0.395**, a rise of **+0.0437**, against the reported **0.367 → 0.405** rise of
**+0.0376**. Direction survives; magnitude of the *change* grows. One sentence plus one
supplementary column buys immunity from the single most obvious statistical objection to the
paper's central number. **Tag: FOLD-INTO-THIS-PAPER / CHEAP.**

## H5 CONFIRMED — the budget axis is an instance of a NAMED line, and the paper doesn't know it

**COCO/BBOB (Hansen et al. 2016) §3.5 formally names budget-dependent benchmarking** as an
established methodological category, with a decade-old apparatus: the fixed-budget vs
fixed-target views, and anytime assessment. The paper's budget finding — the only disjoint-
interval separation it has, plus a *ranking flip* (gradient leads at low budget, perturbation
at high) — is an instance of this named line, and COCO is uncited.

**A direct precedent, also uncited: Lucic et al. 2018** (already in the paper's bibliography
and cited for the genre, but not for this). Verbatim: **"bad models can outperform good models
given enough computational budget."** That is the paper's own finding, stated at NeurIPS 2018.

**A sibling-field confirmation:** Kazikova et al. 2021 (IEEE Access) — budget-matched
comparison is "standard practice" in metaheuristics, and raising the budget "may significantly
affect the final verdict."

**What this changes.** The paper currently presents its budget result defensively, as an
objection it has removed ("the obvious objection is that the optimizer axis is search
intensity wearing a costume"). Read against COCO and Lucic, it is not a defence — it is a
**contribution to an established line, carrying the strongest evidence in the paper**
(disjoint intervals) and a ranking reversal that Lucic predicted and COCO's framework
anticipates. See the ranked section; this is the clearest UNDER-STATED finding.

## Deliverable (iii) UNDER-EXECUTED — the runnable experiments, ranked by cost (batch 8)

The task asked for a *specific, runnable* experiment the literature motivates that converts
elimination into positive mechanism, with the motivating citation and a CHEAP/EXPENSIVE tag.
Eight primaries were fetched. Ranked by value-per-cost:

**1. Xu et al., "How Neural Networks Extrapolate" (arXiv:2009.11848, ICLR 2021) — CHEAP, and
it is the mechanism the paper is missing.**
Their Theorem 1 (NTK regime): ReLU MLPs **provably converge to linear functions along rays
from the origin outside the training support**, at rate O(1/t). This yields a positive,
falsifiable geometric prediction that is *exactly* the paper's own diagnosis made mechanical:
**an ensemble mean that grows linearly without bound far from support admits unbounded
maximizers at the box boundary; a GP posterior mean, which reverts toward its prior, does
not.** "Which off-distribution maximizers a surrogate's mean admits" stops being a diagnosis
and becomes a testable claim about the functional form of each surrogate's far field.
**Runnable now:** fit lines to existing model outputs along the existing optimization
trajectories, already stored. No new training. **This is the single highest-value finding in
deliverable (iii).**

**2. Dao et al., "Boosting Offline Optimizers with Surrogate Sensitivity" (arXiv:2503.04181,
ICML 2024) — CHEAPEST.**
Their (α,ω)-sensitivity (Definition 3.1): perturb the trained surrogate's own **parameters**
and measure how much the prediction at the found optimum moves. **None of the seven
eliminations touches weight-space fragility** — it is a genuinely new axis, and it is
computable on already-trained checkpoints with zero new training.

**3. Gao, Schulman, Hilton, "Scaling Laws for Reward Model Overoptimization" — CHEAP.**
Closed-form `R(d) = d(α − βd)` for true-reward degradation as a proxy is optimized away from
the data, parameterised in KL distance. Directly fittable to the paper's existing
distance-vs-oracle-value data across its 5,040 instrumented optima. Note: this is the paper's
own uncited bibliography entry (see L1b).

**4. Kumar et al., CQL Theorem 3.4 ("gap-expanding") — CHEAP.**
A formal, named robustness property. The paper's inversion result can be re-quantified as a
violation of it, which upgrades a descriptive count into a statement about a provable property.

**5. Manheim & Garrabrant, "Categorizing Variants of Goodhart's Law" (arXiv:1803.04585) —
CHEAP, framing only.** Gives precise existing vocabulary for the paper's under-named
diagnosis: **"Extremal Goodhart — Model Insufficiency."**

**6. Deep Kernel Learning (Wilson et al.) + DUE — CHEAP-to-MEDIUM.**
A double-dissociation transplant: an unconstrained GP-with-neural-features should fail like
the ensemble; a bi-Lipschitz-constrained DUE should recover GP-like behaviour. Confined to one
2D benchmark it is affordable; it is the cleanest *causal* test available.

**7. BCQ (Fujimoto et al.) three-arm graded battery — EXPENSIVE.**
The right template for upgrading the binary inversion result into a dose-response curve, but
it requires new runs, not re-analysis. **FOLLOW-UP-PAPER.**

## Deliverable (iii) UNDER-EXPLAINED — the inversion has a name, and a candidate mechanism

**The paper states its inversion result flatly**, as a within-grid demonstration: *"A cell
that returns something worse than what it was handed has had its own acquisition rank a
design it invented above a real design it was already holding. We call that an inversion…
it is a demonstration within this grid, descriptive at $n{=}7$ tasks, not a mechanism."*

**It is an instance of a named, decades-old failure category.** The offline-RL literature
formalises exactly this property as **Safe Policy Improvement**:

> `P( ρ(π, M) ≥ ρ(π_b, M) − ζ ) ≥ 1 − δ`

— the requirement that a policy learned offline not be worse than the baseline it was given,
with high probability. **Thomas, Theocharous & Ghavamzadeh (ICML 2015)** is the founding
formalization; **Laroche, Trichelair & Des Combes, SPIBB (arXiv:1712.06924)** Theorem 2 proves
their algorithm is a ζ-approximate SPI over the baseline with high probability.

**The reframing this licenses.** The paper's inversion is not merely an awkward number — it is
the observation that **offline MBO optimizers ship with no safe-improvement guarantee, and
that the absence bites.** The offline-RL sibling field considered this property important
enough to build algorithms around it a decade ago; offline MBO has not. That is a sharper,
more transferable claim than "we count inversions on our grid", it costs two sentences and two
citations, and it converts a descriptive count into a statement about a missing guarantee.
**Tag: FOLD-INTO-THIS-PAPER / CHEAP.**

**And a candidate MECHANISM, which the paper currently lacks entirely.**
**Ghasemipour, Gu & Nachum, "Why So Pessimistic? Estimating Uncertainties for Offline RL
through Ensembles, and Why Their Independence Matters" (ICML 2022, arXiv:2205.13703)** prove
that **shared pessimistic targets across ensemble members can render an ensemble
paradoxically OPTIMISTIC.** Member independence is the load-bearing condition.

This is directly on point for a paper whose central puzzle is that a pessimistic
(LCB-penalised) ensemble ranks its own hallucinations above real data. If insufficient member
independence converts intended pessimism into effective optimism, that is a *positive
mechanism* for the inversion — the first one this audit has found that the seven eliminations
do not already rule out. **It is also testable on data the paper has**: measure member
independence (pairwise prediction correlation across the K=5 members) at the returned optima
and check whether inversion rate tracks it. **Tag: FOLD-INTO-THIS-PAPER / CHEAP** if the
per-member predictions were stored; FOLLOW-UP if not.

Note this compounds with the Lakshminarayanan finding (Mandatory Fix 3): an MSE-trained
ensemble taking cross-member empirical variance as σ is precisely the construction most
vulnerable to insufficient diversity. **Two independent sources now point at ensemble
construction as an unexamined confound**, and the paper treats its ensemble as a fixed given.

## Deliverable (iii) — precedent for the pessimism decomposition

The paper's β=0 result — *"pessimism amplifies a mean-quality base rather than creating it"* —
has a precedent in shape, which it does not cite.

**Fujimoto & Gu, TD3+BC (arXiv:2106.06860)**: their ablation shows RL alone is insufficient
without the behaviour-cloning term, and performance is robust across a broad α range,
degrading only at the extremes. That is the same decomposition — a method's gain split between
base-model quality and a regularisation/conservatism term. **A cheap citation that gives the
paper's β=0 finding a lineage.**

**Jin, Yang & Wang, PEVI (arXiv:2012.15085)** — verified, but note the limitation: it is a
pure theory paper decomposing offline-RL suboptimality into intrinsic uncertainty, spurious
correlation and optimization error, and proving pessimism eliminates spurious correlation and
is minimax-optimal. **It contains no empirical base-vs-conservatism ablation**, so it supports
the framing but is not a precedent for the experiment. Worth stating precisely rather than
citing loosely — that distinction is the whole subject of this audit.

## MANDATORY FIX 10 — `fannjiang2020autofocused` articulated the core diagnosis in 2020, uncited

**The sharpest missing-related-work finding in the audit**, and the one most likely to be
raised by a reviewer from the offline-design community.

The paper's central diagnosis, offered as its own: *"What differs is **which** off-distribution
maximizers a surrogate's mean admits"* — the optimizer pushes designs where the surrogate is
unconstrained and its uncertainty estimates stop meaning anything.

**Fannjiang & Listgarten, "Autofocused Oracles for Model-Based Design" (NeurIPS 2020,
arXiv:2006.08052)**, verbatim:

> "oracle-based design… **will query the oracle in regions of the design space that are not
> well-represented by the oracle training data**… **its outputs, including its uncertainty
> estimates, become unreliable beyond the training data**"
> "sub-optimality can be extreme due to **pathological behavior of the oracle when the search
> model… strays too far from the training distribution**"

That is the founding articulation, from 2020, of substantially the paper's own diagnosis —
including the uncertainty-estimates clause. **It sits in the paper's bibliography, uncited.**

**It does not kill anything.** No factorial machinery, no surrogate-class comparison, so N6 is
untouched, and no numeric claim is threatened.

**But it does two things the paper must handle.** First, it dents any implicit novelty in the
*diagnostic vocabulary* — a reviewer will note the paper describes as its own contribution a
framing Fannjiang published six years earlier. Second, and more usefully: **Fannjiang's fix
implicitly treats distance-from-data as the driver of oracle unreliability, and the paper's
Elimination 7 complicates exactly that.** Distance predicts aggregate loss (ρ=−0.818) but
**does not discriminate between surrogate classes at matched distance** (medians 0.87 / 0.86 /
0.84, ensemble still worse by −1.406).

**Fix, and it converts a liability into the paper's best related-work paragraph.** Cite
Fannjiang as the origin of the diagnosis, then state the refinement: the off-support story is
right in aggregate and *insufficient* as an explanation of the class gap, because at matched
distance the classes still differ. **That is a genuine advance on a named prior position** and
is far stronger than presenting the diagnosis as unprecedented. **Tag: FOLD-INTO-THIS-PAPER /
CHEAP.**

## `lu2022revisiting` — N6 NOT killed, but name it

Full-text grep (37 pages, 102,811 chars): `factorial`=0, `crossed`=0, `ANOVA`=0, `analysis of
variance`=0, `eta squared`=0, `variance decomposition`=0, `main effect`=0, `two-way`=0.

It varies uncertainty-penalty heuristics and hyperparameters (model count, rollout horizon)
**while holding the policy optimizer fixed** — verbatim (Appendix G): *"our implementation uses
the same probabilistic dynamics models… and policy optimizer (SAC) as MOPO, differing from
MOReL, which uses Natural Policy Gradient."* MOReL's differing optimizer is flagged only as an
unresolved implementation confound in an appendix, never crossed. Their Bayesian optimization
is used purely as a **hyperparameter tuner within one fixed algorithm**, not to compare
optimizer classes.

**Verdict: one-factor-at-a-time within a fixed optimizer family — structurally the same pattern
the paper already cites and excludes, just in offline model-based RL.** N6 stands.

**Fix (light): name it in related work.** It is the closest sibling-genre "revisiting design
choices" study, it is in the bibliography already, and naming it *strengthens* the no-prior-
instance claim by showing the adjacent field's closest attempt also held an axis fixed.

## `gao2022reward` — three bib defects, and a sharper frame the paper is not using

**Bib defects (all three verified against PMLR).** True venue: **ICML 2023, PMLR
202:10835–10866**.
1. Citation key says `gao2022`; the year is 2023.
2. The `year` field is correct at 2023, so key and field disagree internally.
3. **The page range in the bib is wrong**: `10909--10934` against the true `10835--10866`.
   *(This third defect was not on my list; the batch found it independently.)*

**The substantive point.** Gao et al. give closed forms for proxy-reward overoptimization with
`d := sqrt(KL(π‖π_init))`:
> `R_bon(d) = d(α_bon − β_bon·d)` and `R_RL(d) = d(α_RL − β_RL·log(d))`

Degradation is **class-dependent** — the functional form differs by optimization method (RL vs
best-of-n) — but Gao et al. vary only *scale within one architecture family* (the GPT-3
series), never across architectures.

**So the paper's Elimination 7 is a refinement of Gao's principle onto a new axis (surrogate
architecture class, not scale) in a new domain (offline MBO) — consistent with the scaling
law, not a counterexample.** Two surrogate classes at matched distance-to-data with different
true loss is exactly what a class-dependent degradation curve predicts, and the paper has
5,040 instrumented optima to fit it on. **Tag: FOLD-INTO-THIS-PAPER / CHEAP** — the citation
and framing cost two sentences; fitting the curve is the CHEAP experiment already logged above.

## VERIFIED CLEAN — Shahriari and Chemingui (batch 7)

**`shahriari2016humanoutoftheloop` — the paper is NOT over-disclaiming.** I flagged the risk
that the paper concedes priority to a source that never claimed the doctrine. It does not.
Shahriari states it **twice**, as the review's own organizing thesis:

> "We will see that **the careful choice of statistical model is often far more important than
> the choice of acquisition function heuristic**." *(Overview)*
> "...we have taken the perspective that the importance of [acquisition function design]
> **plays a secondary role to the choice of the underlying surrogate model**." *(Conclusion)*

Zero hits for `offline` across the full 137,300-character text (25 for "sequential"). **The
paper's scope-restriction is accurate and non-strained**, and its paraphrase ("matters more")
*understates* Shahriari's own wording ("far more important"). No fix needed. Worth reporting
as a pass — this is the disclaimer the paper's whole no-field-reversal posture rests on.

**`chemingui2024pggs` — the falsification target is real.** Verbatim from PG-GS's
Summary/Future Work: *"This perspective is aimed at improving the search strategy in offline
BBO, which complements prior methods that have **focused on improving surrogate models while
using fixed search strategies**."* Near-identically restated in the abstract. **The premise the
paper claims to falsify is asserted by the source, not fabricated.** No fix needed.

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
