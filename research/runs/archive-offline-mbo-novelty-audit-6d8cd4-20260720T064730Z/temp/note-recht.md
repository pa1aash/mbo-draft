## Citation
Benjamin Recht, Rebecca Roelofs, Ludwig Schmidt, Vaishaal Shankar. "Do ImageNet Classifiers Generalize to ImageNet?" ICML 2019. arXiv:1902.10811v2 (12 Jun 2019).

## What the paper does
Rebuilds new test sets for CIFAR-10 and ImageNet by closely replicating the original dataset-creation pipelines (same source pool — Tiny Images for CIFAR-10, Flickr via original query terms for ImageNet — same human annotation/labeling process via MTurk). Evaluates ~40+ published classification models on the new test sets to test whether a decade of "held-out test set" progress reflects genuine generalization or adaptive overfitting to the reused test set. Finds "accuracy drops of 3%–15% on CIFAR-10 and 11%–14% on ImageNet" — on ImageNet this is characterized as "approximately five years of progress" lost. Tests the "adaptive overfitting" hypothesis (models tuned, explicitly or implicitly via community-wide iteration, to the specific original test set) against a "distribution gap" hypothesis (the new test set is intrinsically harder/differently distributed). Key diagnostic: fits a linear model of new-test accuracy vs. original-test accuracy per model; the fitted slope is >1 on both datasets (1.69 for CIFAR-10, 1.11 for ImageNet), meaning relative ordering is preserved and there are no diminishing returns — evidence against adaptive overfitting and in favor of a distribution-gap explanation.

## Claim relevance

### N9 — direction of correction (PRIMARY ASSIGNED CLAIM)
**Direction is genuinely mixed/two-track, not a clean single-direction "shrink."** This is the most important nuance for the offline-MBO N9 novelty question.

**Track 1 — absolute accuracy: SHRINKS (standard reality-check direction).** Verbatim abstract:

> "We evaluate a broad range of models and find accuracy drops of 3% – 15% on CIFAR-10 and 11% – 14% on ImageNet."

> "On ImageNet, the accuracy loss amounts to approximately five years of progress in a highly active period of machine learning research."

**Track 2 — relative/marginal gains between models: GROWS (non-standard, strengthens direction).** Verbatim (Section 2.1/Introduction and Section 5.3 "Adaptivity Gap"):

> "Moreover, there are no diminishing returns in accuracy. In fact, every percentage point of accuracy improvement on the original test set translates to a larger improvement on our new test sets. So although later models could have been adapted more to the test set, they see smaller drops in accuracy."

> "Later models do not see diminishing returns but an increased advantage over earlier models."

> "On both datasets, the slope of the linear fit is greater than 1, i.e., each point of accuracy improvement on the original test set translates to more than 1% on the new test set. This is the opposite of the standard overfitting scenario."

**Assessment for N9 novelty:** Recht is genuinely ambiguous as "reality-check precedent for effect-shrinks." The *absolute* headline number (accuracy) drops after the audit — matching the framing in the prompt ("Recht et al. (ImageNet)... audit, effect shrinks"). But the *relative* effect the paper is actually most interested in mechanistically — how much better later/improved models are than earlier ones — is shown to GROW under the audited test set (slope > 1, "increased advantage," "no diminishing returns"). This is structurally close to but not identical to the offline-MBO N9 claim: Recht's "grows" finding is about relative model-to-model gaps surviving distribution shift, not about a variance-explained statistic (eta^2) growing after confound-removal. It is NOT a case where "we identified confounds, controlled for them, and a previously-published headline effect got larger" — it's a case where a new, harder test set was substituted and the *primary* metric (accuracy) still dropped while a *secondary* diagnostic (slope of the accuracy-transfer relationship) exceeded 1. Whether this counts as "growing effect" precedent for N9 is a judgment call the drafter should make explicitly rather than citing Recht as unambiguously "shrinks" — the query's framing itself ("Recht: did accuracy drop") is technically correct for the primary metric, but incomplete: Recht is not a pure "audit shrinks, full stop" case if one credits the slope-based generalization finding.

### N1 — confound taxonomy shape
NOT assigned as primary claim for this paper, but for completeness: Recht names two competing candidate explanations for the accuracy drop ("Potential Causes of Accuracy Drops," Section 2.1: adaptive overfitting vs. distribution gap) and designs experiments (Threshold0.7, TopImages test-set variants; selection-frequency analysis) to adjudicate between them — this is closer to a hypothesis-testing structure than a confound-taxonomy-and-removal-protocol structure. It does not name multiple independent confounds and remove them one at a time the way Musgrave or the offline-MBO paper does; it isolates one binary causal question (adaptivity vs. distribution shift) via a single new-test-set intervention. Weak/partial overlap with N1 shape at most.

## Grep evidence
- "drop": 73 hits — dominant framing word, almost entirely "accuracy drop(s)."
- "decrease": 4 hits.
- "overestimate": 0 hits.
- "gain": 12 hits — includes "accuracy gains on the original test sets translate to larger gains on the new test sets" (abstract).
- "grew": 0 hits (paper uses "increased advantage," "larger improvement," "translate to more than 1%" instead).
- "increase": 6 hits, including "increased advantage over earlier models."
- "confound": 0 hits.
- "ranking": 10 hits (mostly "relative order"/ranking-preservation language, not a confound taxonomy).
- "confidence interval": 26 hits (bootstrap CIs for the linear-fit slope/offset).
