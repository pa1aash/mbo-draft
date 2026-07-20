## Citation
Rishabh Agarwal, Max Schwarzer, Pablo Samuel Castro, Aaron Courville, Marc G. Bellemare. "Deep Reinforcement Learning at the Edge of the Statistical Precipice." NeurIPS 2021. arXiv:2108.13264v4 (5 Jan 2022).

## What the paper does
Argues deep RL benchmark comparisons routinely report point estimates (mean/median scores) over a handful of runs (3–20) without quantifying statistical uncertainty, "exacerbating the statistical uncertainty in point estimates." Builds a case study on the Atari 100k benchmark (5 algorithms: DER, OTR, DrQ(ε), CURL, SPR; 100 independent runs per algorithm/game to enable proper subsampling) and shows that headline point-estimate rankings can reverse or be unsupported once uncertainty is accounted for. Proposes three corrected statistical tools, organized as a named taxonomy in Table 1 ("Desideratum" / "Current Evaluation Protocol" / "Our Recommendation"): (1) uncertainty in aggregate performance — point estimates → stratified-bootstrap confidence intervals; (2) variability in performance across tasks/runs — tables of per-task means → performance profiles (score distributions); (3) choice of aggregate metric — mean (outlier-dominated) / median (needs many runs, blind to near-half-zero scores) → interquartile mean (IQM). Reapplies this corrected methodology to ALE (200M-frame), Procgen, and DeepMind Control Suite benchmarks, releases the `rliable` library, and reports "discrepancies in prior comparisons" across all of them.

## Claim relevance

### N1 — confound taxonomy shape
**PARTIALLY OWNS the shape, in a different domain and with a different confound type than offline-MBO.** Table 1 is explicitly a taxonomy: three named "Desiderata," each paired with a diagnosed flaw in "Current Evaluation Protocol" and a corrective "Recommendation." The paper then reruns published algorithm comparisons under the corrected protocol and reports the resulting **ranking changes**:

> "Figure 9 reveals an interesting limitation of aggregate metrics: depending on the choice of metric, the ordering between algorithms changes (e.g., Median vs. IQM). The inconsistency in ranking across aggregate metrics arises from the fact that such metrics only capture a specific aspect of overall performance across tasks and runs."

> "While M-IQN [109] claimed better performance than Dopamine Rainbow9 [42] in terms of median normalized scores, their interval estimates strikingly overlap. Similarly, while C51 [5] is considered substantially better than DQN [75], the interval estimates as well as performance profiles for DQN (Adam) and C51 overlap significantly."

> "our analysis suggests that DER may in fact be better than OTR, unlike what the reported point estimates suggest."

**Residual for offline-MBO N1:** Agarwal's taxonomy has exactly 3 confound categories, all of a single statistical-methodology type (estimator bias/variance and CI reporting in RL benchmarking) — no experimental-design confounds (architecture, dataset construction, proxy-vs-ground-truth objective mismatch), no domain-specific offline-optimization confounds, and critically **no variance-decomposition / eta^2-style effect-size attribution**: the paper reports CI overlaps and rank instability qualitatively (Figures 8–9), not a quantified "fraction of variance explained by confound k." It is RL-benchmark-specific (Atari 100k, ALE, Procgen, DM Control) and never touches offline model-based optimization, surrogate models, or the eta^2_surr-style effect-size framing central to the offline-MBO paper. So: the general shape (name confounds → protocol → show ranking instability) is prior art here too, but confined to statistical-uncertainty confounds in online RL evaluation, not the offline-MBO-specific confound set or its variance-attribution quantification.

### N9 — direction of correction
**Mixed/ambiguous — does NOT cleanly fit "shrinks."** Agarwal explicitly states point estimates can go either direction after correction:

> "The reported point estimates of median in publications, as shown by dashed lines, do not provide any information about the variability in median scores and severely overestimate or underestimate the expected median."

More importantly, there is one passage where **more rigorous statistical treatment reveals an effect that first appeared absent/insignificant, and shows it is in fact real** — i.e., statistical rigor makes a previously-null-looking result significant, the closest analog in this batch to a "strengthens" direction, though it is about statistical power (more runs) rather than confound removal:

> "while improvement from SPR over DER with 5 to 15 runs is not statistically significant, claiming 'no improvement' would be misleading as evaluating more runs indeed shows that the improvement is significant." (Appendix A.9, comparing performance of two algorithms)

This is NOT the same mechanism as the offline-MBO N9 claim (de-confounding via removing five identified confounds causing eta^2_surr to rise from 0.37→0.405) — it is "more samples reduce estimator variance and reveal a real but small effect," not "controlling for confounds increases an already-detected effect's magnitude." But it is evidence that "reality-check paper, audit reveals effect was UNDERSTATED" is not unprecedented in the broader statistical-rigor-in-ML-evaluation literature; the specific confound-removal-grows-effect-size mechanism claimed by the offline-MBO paper is still NOT demonstrated by this paper. Overall Agarwal's headline framing is "prior comparisons had unjustified confidence" (both over- and under-estimation), not a unidirectional "audit shrinks the effect" story — this nuances but does not satisfy N9 novelty-killing precedent.

## Grep evidence
- "confound": 1 hit (used loosely re: "additional confounding factors" in exploration variance, not a taxonomy term).
- "reproduc": 21 hits.
- "generalization gap": 0 hits.
- "drop": 0 hits (word not used for effect-size direction).
- "decrease"/"overestimate": 1 hit each — the "severely overestimate or underestimate" sentence above.
- "tuning": 4 hits.
- "ranking": 18 hits — includes the algorithm-reordering evidence quoted above.
- "significance"/"significant": 6+ hits, including the SPR-over-DER "evaluating more runs indeed shows that the improvement is significant" passage.
- "confidence interval": 14 hits.
- "widen"/"narrow": 0 hits each.
