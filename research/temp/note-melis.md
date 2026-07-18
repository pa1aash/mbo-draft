## Citation
Gábor Melis, Chris Dyer, Phil Blunsom. "On the State of the Art of Evaluation in Neural Language Models." ICLR 2018 (under review; arXiv v1 posted 2017, published version ICLR 2018 conference track). arXiv:1707.05589v2 (20 Nov 2017).

## What the paper does
Argues that language-model architecture comparisons (LSTM vs. Recurrent Highway Networks (RHN) vs. Neural Architecture Search (NAS)-derived cells) on Penn Treebank, Wikitext-2, and Hutter Prize/enwik8 have been confounded by inconsistent, under-controlled hyperparameter tuning across papers/codebases. Uses large-scale black-box hyperparameter optimization (a single, standardized tuning protocol/budget applied uniformly to all architecture families) to compare LSTM, RHN, and NAS cells under matched parameter budgets and tuning effort. Central finding: once hyperparameters are properly and equally tuned, plain LSTMs — the oldest of the three architecture families compared — outperform the more recently published, architecturally novel RHN and NAS models, reversing the field's published ranking. Establishes new SOTA perplexity numbers on Penn Treebank and Wikitext-2 with the properly-tuned LSTM, and strong (near-SOTA) baselines on Hutter Prize/enwik8.

## Claim relevance

### N9 — direction of correction (PRIMARY ASSIGNED CLAIM)
**Direction is unambiguously SHRINKS: tuned baselines OVERTURN claimed SOTA of newer architectures.** This is a clean confirming instance of the standard reality-check direction described in the prompt. Verbatim (Abstract):

> "We reevaluate several popular architectures and regularisation methods with large-scale automatic black-box hyperparameter tuning and arrive at the somewhat surprising conclusion that standard LSTM architectures, when properly regularised, outperform more recent models."

Verbatim (Introduction, Section 1):

> "Once hyperparameters have been properly controlled for, we find that LSTMs outperform the more recent models, contra the published claims. Our result is therefore a demonstration that replication failures can happen due to poorly controlled hyperparameter variation..."

Verbatim (Conclusion) — explicit statement that effect sizes SHRINK once methodological care improves and architectures are compared on a level footing:

> "During the transitional period when deep neural language models began to supplant their shallower predecessors, effect sizes tended to be large, and robust conclusions about the value of the modelling innovations could be made, even in the presence of poorly controlled 'hyperparameter noise.' However, now that the neural revolution is in full swing, researchers must often compare competing deep architectures. In this regime, effect sizes tend to be much smaller, and more methodological care is required to produce reliable results."

**Assessment for N9 novelty:** Melis is a textbook instance of the "audit shrinks the effect" direction the offline-MBO paper explicitly says is the norm (and which its own eta^2_surr result, 0.37 → 0.405, contradicts). The claimed advantage of RHN and NAS architectures over plain LSTM is not merely diminished but reversed (LSTM becomes SOTA once fairly tuned) — this is a shrink-to-negative case, the strongest form of the standard direction. Melis provides ZERO precedent for an audit that strengthens an already-published effect; it reinforces that the offline-MBO paper's growing-effect direction (N9) is atypical among reality-check papers, consistent with the prompt's framing.

### N1 — confound taxonomy shape
NOT assigned as primary claim, but for completeness: Melis names exactly ONE confound category — hyperparameter-tuning inconsistency across codebases/papers ("uncontrolled sources of experimental variation") — and applies a single corrective protocol (uniform black-box hyperparameter search under matched budgets) rather than a taxonomy of multiple distinct confound types. This is a narrower, single-confound instance of the shape, not a multi-confound taxonomy like Musgrave's or Agarwal's Table 1. Weak overlap with N1 at most — the paper doesn't attempt to enumerate or decompose several independent sources of bias, just tuning variance.

## Grep evidence
- "tuning": 3 hits.
- "SOTA": 0 hits (paper says "state of the art" in full, never the acronym).
- "state of the art" / "state-of-the-art": 4 hits.
- "outperform": 2 hits, both central to the direction-of-correction finding above.
- "overturn": 0 hits (concept present but not this exact word — "contra the published claims" is the paper's own phrasing).
- "reproduc": 1 hit ("replication failures," Introduction).
- "ranking": 0 hits.
- "significance": 0 hits (no formal significance-testing language; comparisons are made via perplexity numbers under matched tuning budget).
- "drop": 24 hits — but predominantly refers to "dropout" (regularization technique), NOT effect-size direction; must be manually filtered.
- "increase": 1 hit.
