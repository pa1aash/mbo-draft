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

## VERIFIED — the paper's own numbers and code (orchestrator, local)

See `local-checks.md`. Summary: all four corner η² point estimates and CIs, the corner range,
interval widths, Elimination 1's seven figures, the inversion counts (7/7, 3/7, 2/7), the
`mbo.py` line traces for Confounds 1 and 2, and the engine-stamping protocol all reproduce
exactly. **One** figure does not: "five other cells tie it" should be six.

Plus a free win: bootstrap bias correction moves the headline 0.367→0.405 to 0.351→0.395 —
direction survives, effect **grows**.
