## Citation
Matthew C. Robinson, Robert C. Glen, Alpha A. Lee. "Validating the Validation: Reanalyzing a large-scale comparison of Deep Learning and Machine Learning models for bioactivity prediction." arXiv:1905.11681v2 [cs.LG], 9 Jun 2019.

Source text: `research/raw/txt/robinson-glen-lee-validating-the-validation.txt` (pdftotext extraction from `research/raw/pdf/1905.11681.pdf`, 6375 words, full body). Title verified against header lines 1-6 (exact match to arXiv abstract page title, independently confirmed via `curl` against `https://arxiv.org/abs/1905.11681`).

## What the paper actually does
Reanalyzes the data underlying Mayr et al.'s large-scale ChEMBL bioactivity-prediction benchmark (~456,000 compounds, >1300 assays), which had concluded "deep learning methods significantly outperform all competing methods" based on Wilcoxon signed-rank test p-values (p=1.985e-7 for FNN>SVM; p=8.491e-88 for FNN>RF). Robinson/Glen/Lee argue this conclusion "obscures much of the variability from assay to assay" and rerun the comparison with attention to per-assay heterogeneity, statistical vs. practical significance, and metric choice (AUC-ROC vs. AUC-PRC). They also run numerical experiments on the reliability of scaffold-split nested cross-validation for uncertainty estimation.

## Claim relevance

### N9 — direction of correction (this is the paper the miss-catcher log flagged as "checked via search summary only" — RESOLVED by full fetch + grep in this pass)
**Direction is unambiguously SHRINKS.** The paper's own conclusion section states directly:

> "We build on the recent large-scale benchmarking study by Mayr and coworkers and reanalysed the reported performance data of different machine learning models, arriving at a different conclusion to Mayr and coworkers. We show that support vector machines achieve competitive performance with feed-forward deep neural networks." (Conclusion, lines 606-611)

And in the introduction, the explicit reversal of the original headline claim:

> "Our key conclusion is an alternative interpretation of their results that considers both statistical and practical significance — we argue that deep learning methods do not significantly outperform all competing methods." (lines 82-84)

This is a clean instance of the standard reality-check direction: the original paper's headline claim (deep learning "significantly outperforms all competing methods," backed by very small p-values) is walked back to "SVM is competitive with deep learning" after the reanalysis accounts for per-assay variability and practical vs. statistical significance. No effect-size number is shown growing past its originally published value anywhere in the text — grep for "confound" returns 0 hits (the paper does not use this framing at all; its critique is about aggregate-statistic misuse and metric choice, not a named confound-removal protocol), and grep for "larger"/"stronger"/"increase" (30 hits) turns up no instance where a corrected effect exceeds the original.

**Assessment for N9 novelty:** confirms the miss-catcher log's search-summary characterization exactly — this is a conventional shrink/nullify-direction ML/CS reality-check paper, not a counter-example to N9's "unclaimed" framing. It strengthens the general pattern (yet another named ML/CS reality-check paper in the shrink direction) rather than complicating it.

## Grep evidence (full text, 6375 words)
- "outperform": 6 hits — all either quoting/characterizing Mayr et al.'s original overclaim or explicitly rejecting it ("deep learning methods do not significantly outperform all competing methods").
- "competitive": 3 hits — the paper's own replacement framing ("performance of support vector machines is competitive with that of deep learning methods").
- "confound": 0 hits.
- "larger"/"stronger"/"increase": 30 combined hits, none referring to a corrected effect size exceeding an original published value (uses are about dataset size, confidence interval width, precision-recall improvements from metric choice, and cross-validation variance).
- "overestimate"/"underestimate": 4 hits — "estimates of machine learning performance would overestimate the true...", "cross-validation underestimates error" — both about measurement bias, not audit-direction.
