# Valid prediction intervals for regression problems

**Full citation:** Nicolas Dewolf, Bernard De Baets, Willem Waegeman, "Valid prediction intervals for
regression problems," *Artificial Intelligence Review* 55, 577-613 (2022). arXiv:2107.00363 (v4, 1 Apr
2024 — the arXiv preprint predates and matches the published AI Review 2022 version; no citation-date
trap identified, both years cited here). DOI: 10.1007/s10462-022-10178-5.

## What the paper actually does

An independent comparative review and empirical benchmark of four classes of regression prediction-interval
methods — Bayesian methods (incl. Gaussian processes, mean-variance estimation), ensemble methods (deep
ensembles, random forests with out-of-bag variance), direct interval-estimation methods (quantile
regression), and conformal prediction — evaluated on the SAME real-world benchmark datasets under a
shared nominal confidence level (predominantly 90%). The paper's central empirical finding, reported in
Fig. 1/Fig. 2 and the accompanying text, is that **without a post-hoc calibration step, the four method
classes do not deliver matched effective coverage at the identical nominal confidence level**: some are
"overconservative" (wider intervals than needed), others "underestimate the uncertainty" (narrower than
needed / undercoverage), even though all were run at nominal 0.9. The paper explicitly frames conformal
prediction's normalization step as the general fix for this: raw (unnormalized) interval-construction
procedures give "uniform (or homoscedastic) prediction intervals," and the paper states this is "in
stark contrast with most bona fide interval estimators" — i.e., a single width/threshold applied
uniformly does not track the true local uncertainty scale, so the field's standard correction is to
"normalize the nonconformity measure by a dispersion function σ : X → R." The paper reviews and cites the
foundational normalized/locally-adaptive conformal prediction literature (Papadopoulos et al.) as the
origin of this fix. Table 1 in the paper's Section 3.5 summarizes validity, scalability, and other
properties across all four method classes.

## Claim relevance

**N3** — "A shared beta across surrogate CLASSES with different sigma scales delivers different effective
conservatism (the LCB was never matched)." **Verdict: PARTIAL — the general statistical premise is owned,
the cross-surrogate-class acquisition-function application is NOT.**

The paper states, in general statistical/UQ form, exactly N3's underlying mechanism: applying one
fixed/uniform confidence-construction rule (structurally the same move as sharing one multiplier — a
"beta" — across differently-scaled uncertainty estimators) does NOT produce matched effective coverage or
conservatism when the underlying methods' uncertainty estimates are not calibrated to a common scale.
Verbatim (Section 3.4, on why raw nonconformity measures are insufficient):

> "The above procedure gives uniform (or homoscedastic) prediction intervals, which is in stark contrast
> with most bona fide interval estimators. Although computationally simple, it ought to be clear that this
> is not the generic situation. Different modifications to obtain heteroscedastic models have been
> proposed in the literature, the main one being to normalize the nonconformity measure by a dispersion
> function σ : X → R."

And, from the empirical cross-method comparison at fixed nominal 90% (Section 4, discussing Fig. 2):

> "the uncalibrated models do not approximately saturate the validity constraint. They either underestimate
> the uncertainty or produce overconservative prediction intervals. When comparing between the models
> trained on half of the data set and the full data set..."

This is N3's premise stated generally and demonstrated empirically ACROSS METHOD CLASSES (Bayesian,
ensemble, direct-interval, conformal) at one shared nominal confidence level: uncalibrated cross-class
comparison at a fixed nominal setting yields unmatched effective conservatism (some over-, some
under-conservative), exactly the "the LCB was never matched" mechanism N3 names.

**What it stops short of:** the paper never applies this to COMPARING surrogate classes under a shared
beta inside an acquisition function / sequential-decision / Bayesian-optimization context. It is entirely
about static regression-uncertainty-quantification VALIDITY (marginal coverage), never about downstream
optimization behavior, exploration/exploitation, or "effective pessimism" as a search-quality concept.
Grep confirms zero hits anywhere in the ~17,800-word body for "acquisition," "Bayesian optimization,"
"pessimis," "surrogate model," "lower confidence bound," or "upper confidence bound." The paper's fix
(normalize per-instance by a dispersion function, or conformal-calibrate per method) is also the OPPOSITE
move from N3's diagnostic framing — Dewolf et al. show how to REPAIR the shared-threshold problem
per-method, not how a downstream comparison under one un-repaired shared multiplier miscalibrates a
cross-class RANKING or acquisition decision.

**Net effect on N3 verdict:** upgrades from clean NONE FOUND to a defensible PARTIAL. The paper to cite
in the draft, scoped precisely: "the general statistical principle that one shared confidence-construction
rule miscalibrates effective coverage/conservatism across differently-scaled uncertainty estimators is
established in the UQ/conformal-prediction literature (Dewolf et al. 2022; foundational instance in
Papadopoulos, Vovk & Gammerman 2011's normalized nonconformity measures), but its extension to comparing
SURROGATE CLASSES under one shared beta inside an LCB/UCB acquisition function in Bayesian optimization or
offline MBO is, to our knowledge, unclaimed."

## Grep evidence

- `normali` / `heteroscedast` / `conservat` / `coverage` / `scale`: dozens of hits throughout Sections
  3.4-4 (dispersion-function normalization, cross-method coverage comparison).
- `acquisition`, `bayesian optimization`, `pessimis`, `surrogate model`, `lower confidence bound`,
  `upper confidence bound`: **0 hits** (confirmed via `grep -in` across the full 17,767-word extracted
  text) — establishes the paper never crosses into the optimization/acquisition-function framing N3
  needs for a full PRIOR WORK FOUND verdict.
- Companion foundational source checked (not separately registered, cited within this note): Papadopoulos,
  Vovk & Gammerman, "Regression Conformal Prediction with Nearest Neighbours," JAIR 40 (2011): 815-840,
  arXiv:1401.3880 — establishes that an unnormalized (single shared-threshold) nonconformity measure gives
  regions of "roughly the same width for all examples" regardless of local difficulty, and that
  normalizing by a local difficulty estimate (`λ_ki`, a k-NN-based dispersion proxy) is required to make
  region size track true local uncertainty — the same shared-threshold-mismatch principle at the
  single-model, per-instance level rather than the cross-model-class level.
