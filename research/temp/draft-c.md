# Decomposing the GP Advantage: Adversarial Audit, Round 4

**N6 survives.** No prior work in offline model-based optimization (offline MBO — optimizing a design against a surrogate fitted once on a fixed dataset, with no further oracle queries) runs a crossed surrogate-class × optimizer factorial with a two-way variance decomposition. That held against a 2026 recency sweep, a forward-citation walk over roughly 347 citing papers, a fresh re-confirmation of all three prior near-misses, and an adversarial sweep of the three regions where such an analysis was *most* likely to already exist. One paywalled lead remains unresolved and is named in the verdict rather than buried. The first contribution stands.

**Everything else is a priority ordering, not a defect list.** That is the central finding, and it changes what the author should do with the remaining hours. Every quantitative claim checkable against a repository artifact reproduced — four corner η² values and their intervals, the corner range, the bootstrap-width validation, the pessimism increment with its paired-delta and z-score cross-check, the per-task β=0 gaps, the inversion counts across three surrogate classes, both frozen-cell claims to the individual seed, the two `mbo.py` line traces, and the engine-stamping protocol. Exactly one did not: a parenthetical integer, "five other cells tie it," which should read six. Against that, twelve mandatory items in deliverable (i). **Eleven of the twelve concern what a *source* says. Not one concerns a number the paper computed.**

That asymmetry is actionable in a way a count of twelve is not. It says the pre-deadline effort belongs in related-work and scoping prose, and that nothing needs re-running. It also calibrates severity: these are attribution and framing defects in a paper whose evidence base is unusually clean, not a paper whose evidence is in question.

**And the audit's most useful single output is a boundary condition.** Two positive findings sit unreported in the paper's own artifacts — a significant surrogate × optimizer interaction, and a 7-of-7 attenuation of the surrogate gap under weak search. **Each survives exactly the challenge the other fails.** Reported together, with the floor-effect confound disclosed, they are defensible; either promoted alone is an overclaim. The paper reports neither, which is the largest recoverable value in this document — and it costs zero new computation, because both quantities are already in the released artifacts and one is already printed in Table 2 without comment.

The paper's evidence is sound and its scholarship is not. Fix the scholarship, report the two positives together, do not touch the experiments.

---

## N6 Verdict: The Crossed Surrogate x Optimizer Factorial

**VERDICT: CONFIRMED NONE-FOUND**, with one paywalled lead unresolved and disclosed here rather than in the terminal section, because a reader is entitled to see the residual risk attached to the verdict it qualifies.

### A. What a kill requires

Four conjuncts simultaneously, in an offline / fixed-dataset setting: (a) surrogate **model class** varied across ≥2 genuinely distinct classes; (b) optimizer / search routine varied across ≥2 routines; (c) the two **crossed**, every surrogate run with every optimizer; (d) a **two-way variance decomposition** of the outcome reported. Failing any one makes a paper a near-miss, not a kill. Conjunct (a) matters because a training-objective swap inside one architecture is a different kind of factor; (b) because a bundled end-to-end method is not a clean optimizer level; (c) because a one-factor-at-a-time design cannot estimate the fixed factor's effect; (d) because descriptive per-cell reporting is not an attribution.

### B. The queries run

Across arXiv, OpenAlex and targeted web search. Semantic Scholar returned HTTP 429 for the entire session on both the REST endpoint and the MCP tool, so arXiv and OpenAlex carried all citation chaining; no verdict rests on a Semantic-Scholar-only result.

*Direct-target:* `crossed factorial surrogate optimizer offline model-based optimization`; `two-way ANOVA surrogate optimizer variance decomposition black-box optimization`; `factorial design surrogate model acquisition optimizer offline`; `eta squared surrogate main effect optimizer main effect benchmark`; `attribution surrogate versus optimizer offline MBO`; `crossed design machine learning benchmark two-way ANOVA`; `factorial design deep learning benchmark components`.

*2026 recency frontier:* full-PDF extraction and twelve-term grep (`factorial`, `crossed`, `ANOVA`, `analysis of variance`, `eta squared`, `η²`, `main effect`, `variance decomposition`, `two-way`, `interaction effect`, `attribution`, `OFAT`) across eight offline-MBO / offline-BBO papers from Jan–Jun 2026 [8][9][10][11][12][13][14]. **Zero hits, all eight papers, all twelve terms.**

*Extension check:* forward-citation walks over ~347 citing papers (62 Hutter, 166 Liang, 4 Moosbauer, 115 van Rijn & Hutter), 2023–2026 where volume required. *Adversarial regions*, chosen because a crossed factorial with ANOVA was **more** likely there than in offline MBO: surrogate-assisted evolutionary computation; AutoML / CASH / kernel selection; simulation-optimization. *Interaction-precedent:* `interaction optimizer architecture deep learning benchmark`; `best optimizer depend on architecture`; `component interaction ANOVA machine learning pipeline`; `scaling laws interaction between hyperparameters and architecture`; `how to train your vit data augmentation regularization`.

### C. The near-miss ledger

All three prior near-misses were re-fetched fresh — no cached verdict reused — and all three still only near-miss. None has been extended.

| Near-miss | Status | Failing conjunct |
|---|---|---|
| Hutter et al. 2014 (fANOVA, ICML) | Re-confirmed | (c)/(d): one-way only, "based on data from one SMAC run"; finding was that "the most important hyperparameter was the model class used," range 31%–58%. Zero hits for factorial/crossed/two-way/OFAT/offline. |
| Liang et al. 2021 [4] | Re-confirmed | (d): a genuine surrogate × acquisition grid reporting only Enhancement and Acceleration Factors; zero ANOVA/η² hits; explicitly "closed-loop active learning," so also fails offline. |
| Moosbauer et al. 2022 [3] | Re-confirmed | (c)/(d): names fANOVA and *declines* it — "any interactions between inputs cannot be detected by an OFAT analysis" — with §6.3 confirming OFAT from a single optimized configuration. |
| **Tan et al. 2025 (RaM) Table 3** [2] | **NEW — closest in existence** | (a)/(d): a genuine 9 × 2 crossed grid *in offline MBO*, but the crossed axis is training *loss* (MSE vs. ListNet), never model class; Score±std and %Gain only, zero decomposition-term hits across 171,781 characters. |
| Sun et al. 2026 (DiBO) Table 2 [8] | New, weaker | (b): backbone × training *stage* (DA/SFT/RL); a pipeline stage is not a search routine applied to a frozen surrogate. |
| BOOST [7] | New, structural | (a): kernel × acquisition with an isolating ablation, but Matérn/RBF/RQ are one GP model class, and its "offline" label denotes an internal no-extra-query step inside an online loop. |

Two adversarial-region results carry extra weight. Kudela & Dobrovský's multi-surrogate, multi-algorithm CFD comparison [5] — the most on-target paper in the community with the strongest design-of-experiments culture — returned **zero hits on all nine decomposition terms across 47,342 characters**, verified first-hand rather than by relay. Gorissen et al. [6] genuinely varies model class across SVM, Kriging, RBF and neural networks, satisfying (a) more cleanly than anything else found, but its genetic algorithm is the *fitting* mechanism, not a black-box optimizer searching the design space, so (b) fails outright. **The region where the analysis was most likely to already exist does not contain it** — a stronger negative than a null in a region nobody expected.

### D. The uncomfortable finding, and what it forces N6 to become

Defending N6 against RaM required computing η² from RaM's own published Table 3: **the loss axis carries η² ≈ 0.027 against the method/optimizer axis's η² ≈ 0.577.** That computation *is* a two-way variance decomposition of somebody else's crossed grid, performed from published numbers, in under a day.

This cuts both ways. It strengthens *no prior work **reports** a crossed surrogate × optimizer decomposition* — still true, since RaM reports Score±std and %Gain. It falsifies *no prior work **could have***. **N6 must therefore be a claim about what the literature reports, never about what the design space permits.** The contribution is running the decomposition as the primary analysis on a purpose-built grid, not the arithmetic. That is narrower than the current framing and it is the version that survives contact with Tan et al.

It also produces a free result worth keeping: two crossed grids in the same subfield, decomposed the same way, disagreeing about which axis carries the variance. RaM's loss axis is negligible against its method axis; the paper's surrogate axis dominates its optimizer axis. That is a more interesting sentence than any novelty claim.

### E. The three grounds — one falsified

| Ground | Status |
|---|---|
| **(1) Loss type ≠ model class** | **SURVIVES**, now with domain support. The canonical UQ survey [17] catalogues method family and loss function as orthogonal, separately-tabulated axes. The paper's nearest comparator [18] treats model class as constitutively bound to its own fitting procedure — no GP without marginal-likelihood fitting, no ensemble without per-member MAP training — whereas RaM swaps MSE for ListNet *inside one unchanged MLP*. Statable criterion: a change is model-class if it cannot be instantiated without changing the estimator family; training-objective if it can be applied at fixed family. |
| **(2) Bundled methods ≠ a clean optimizer factor** | **FALSIFIED AS STATED.** RaM's Appendix E.5 describes four of the nine — BO-qEI, CMA-ES, REINFORCE, Gradient Ascent — as "baselines that optimize a trained model." **A clean 4 × 2 crossed sub-grid exists inside Table 3.** The ground survives only for the other five: CbAS and MINs are genuinely aliased in the strict sense [16] (model family and search paradigm co-occur on every run), and Tri-Mentoring, PGS, Match-OPT layer method-specific machinery on top. |
| **(3) Descriptive reporting ≠ a decomposition** | **SURVIVES**, but must be stated as a claim about what RaM *reports*, since the audit itself derived the decomposition from the published table. A reviewer will make this move if the paper does not. |

**Fix (mandatory, cheap).** Relocate `tan2025ltr` out of the "surrogate-class comparisons hold the optimizer constant" bucket — accurate about RaM's main five-surrogate experiment, silent about Table 3 — into a *training-objective comparisons* bucket alongside `trabucco2021coms`. Add a footnote naming RaM Table 3 as the nearest near-miss with the four-versus-five breakdown and the 0.027/0.577 observation. **Conceding the 4 × 2 sub-grid and defending the actual residual is a stronger position than the current one**, which does not survive an appendix read.

### F. The unresolved lead

**Elsayed & Lacor (2014), "Robust parameter design optimization using Kriging, RBF and RBFNN with gradient-based and evolutionary optimization techniques,"** *Applied Mathematics and Computation* 236:325–344, DOI 10.1016/j.amc.2014.03.082. The only title in the entire audit naming **three surrogate classes and two optimizer families explicitly**. Primary text could not be obtained: ScienceDirect, Unpaywall (no OA location), Crossref, Semantic Scholar (publisher-elided abstract), Academia.edu, ResearchGate and the VUB repository all exhausted. Per the method constraint the fetcher refused a snippet verdict.

**The open question is narrow: is the crossing genuine, or sequential** (surrogates compared first, then one winner optimized two ways)? Sequential is not a kill; a genuine crossing with a decomposition would be. Resolvable through institutional access in minutes, and it should be resolved before submission. If it cannot be, the conditional belongs in the paper's prose.

**Three homonym traps caught, and they are method, not trivia.** Liang's full text returns 14 hits for `crossed` — every one the "Crossed barrel" dataset name. Four papers return raw `anova` hits from the surnames *Usmanova* and *Bozhanova* in shared bio-design bibliographies. In a vision-transformer paper, `ANOVA` false-matched inside *Toutanova*. **A grep-count-only methodology would have produced false positives in five separate papers, and would have scored Liang as crossed.**

---

## (i) Claims the Literature Contradicts or That Are Miscited

Twelve mandatory items, ordered by how cleanly a knowledgeable reviewer could use each as a kill.

### A. The triple miscitation: `fan2024minucb` (most severe)

**(1) "The reading of a UCB-style acquisition as local search"** is presented as established prior work [20]. Fan et al.'s own words: "we **propose** our first algorithm... MinUCB, which **replaces** the gradient descent step with a step that minimizes the UCB in GIBO," and "This discovery... **opens up possibilities for new designs**." A 2024 method proposal, not an established reading.

**(2) LCB paralysis — the most serious.** The paper writes that "the GP's lower confidence bound is locally maximal at the data, so the optimizer never leaves... This is the offline instance of a known reading of UCB-style acquisitions as local search [20], applied rather than discovered." Full-text grep of Fan returns **zero hits** for `offline`, `LCB`, `lower confidence bound`, `stuck`, `frozen`, `freeze`, `paralysis`. They define UCB(x) = μ(x) + βσ(x) and *minimize* it because their objective is minimization; they never treat maximization and never mirror-transform. Decisively, **their Theorem 1 proves MinUCB converges to a genuine local optimum**, contingent on an increasing β schedule and continual active resampling every iteration — both structurally impossible on a static offline dataset. **The paper cites a convergence theorem as authority for an "optimizer never leaves" failure mode.**

**(3) The distance-aware co-citation.** Fan has zero hits for `distance-aware` and uses vanilla GP posterior variance throughout.

**FIX (mandatory).** Drop `fan2024minucb` from the LCB-paralysis sentence and the distance-aware co-citation; restate it as a recent method proposal if kept at all. **This costs the paper nothing and removes a reviewer's cleanest kill**, because the frozen-cell evidence — bit-identical constants across sixteen seeds, in two GP classes, on a continuous task with no argmax decode — is stronger unattributed than mis-attributed.

**"Nobody owns it" is also wrong, and this correction matters.** An earlier pass concluded the failure mode unowned after excluding three candidates: TuRBO [21], whose diagnosis is the *opposite* ("an overemphasized exploration that results from global acquisition," "a failure to exploit promising areas") with locality deliberately *imposed* via trust regions; Fan, who proves convergence; and GIBO, whose exploitation step has no confidence bound. Excluding three candidates is not sweeping the vocabulary. Swept, it yields **Yarotsky (2013)** [22], whose Theorem 3 proves that Expected-Improvement-driven BO started at the true optimum has a trajectory converging back to that point and "not dense" — the closest prior formalization of *gets stuck and never leaves*. It differs on three real axes (EI not a confidence bound; online not offline; adversarial worst-case start, not an empirical observation), so it is **a citation obligation, not a kill**. Two adjacent items merit a sentence: Ament et al. (NeurIPS 2023) on EI's vanishing-gradient pathology degenerating the acquisition optimizer into random search, and Kim & Choi [23], which bounds the regret gap between local and global optimizers of PI/EI/GP-UCB — concerning within-round inner-optimization fidelity, not the outer-loop claim.

### B. `liu2020sngp` is cited against its own thesis

**The paper:** "σ is a distance signal, not an error signal... this is the corrected measurement, **bounded by prior work on distance-aware uncertainty** [24][25]."

**SNGP argues the opposite about the exact model class:** "deep ensembles... are based on dense output layers that are **not distance aware**. As a result, both methods quantify their predictive uncertainty based on the distance from the decision boundaries, **assigning low uncertainty to OOD examples even if they are far from the data**" [24]. Its Definition 1 formalises input-distance-awareness as a property standard deep models *lack* — that lack is SNGP's motivation. DUQ corroborates: "DUQ is certain only on the data distribution, and uncertain away from it: the ideal result. **Deep Ensembles is uncertain only along the decision boundary, and certain elsewhere**" [25]. And all SNGP validation is classification; zero regression experiments, against a regression paper.

**FIX.** The claim cannot be "bounded by" a source that predicts the opposite. Best option: **reframe as a contrast** — "unlike the ensembles SNGP and DUQ characterise as distance-unaware, ours shows a modest positive distance correlation (ρ≈0.26)." A result running *against* SNGP is more publishable than one leaning on it, provided it is labelled. State the classification/regression gap either way.

### C. The σ distance-versus-error dichotomy is a false opposition

**Direct contradiction, in regression, peer-reviewed.** Carrete et al. [26], neural-network force fields: "the Spearman correlation coefficient between uncertainty and error over the validation data set is **0.90 for the committee and 0.91 for the bootstrap-aggregation ensemble**" — roughly thirteen times the paper's ρ≈0.07.

**The resolution is scoping, and the scoping is the finding.** Carrete measures in-distribution, where distance and error largely coincide; the paper measures where an optimizer has pushed designs off-support; SNGP and DUQ measure classification on a 2D toy geometry. All three can be right. **That means the dichotomy — σ is a distance signal *not* an error signal — is a false opposition the literature does not support.** SNGP itself ties distance-awareness to calibration rather than opposing them.

**A second, narrower caveat survives, stated precisely because an earlier framing over-reached.** Lakshminarayanan et al. [27] report that an MSE-trained ensemble using cross-member empirical variance as σ "consistently underestimates the true predictive uncertainty" (an 80% nominal interval covering ~20% of test points), where their NLL-trained variant is calibrated — and the paper's ensemble is exactly that construction. But Ghasemipour et al. [39] treat standard init-seed-diversified ensembles as the *reliable* reference, citing Ovadia [28]; what fails in their study is weight-shared approximations the paper does not use. D'Angelo & Fortuin [29] note the absence of diversity guarantees, yet their own table shows standard ensembles winning OOD detection in one setup. **Net: "this specific σ construction has a known calibration caveat," not "MSE ensembles are broken."**

**FIX.** Scope the dichotomy to this grid, and add one paragraph acknowledging ensemble construction as an unexamined alternative explanation for ρ=0.07.

### D. `melis2018sota` cannot carry "audits normally shrink"

**The paper, twice, load-bearing for Contribution 2:** "Audits in this genre **usually shrink** the effect they audit [30]."

**Melis actually found a ranking reversal:** "Once hyperparameters have been properly controlled for, we find that LSTMs outperform the more recent models, contra the published claims" — not a shrinking effect size, and explicitly framed as one instance: "this paper joins other recent papers in warning of the under-acknowledged existence of replication failure in deep learning." No sentence anywhere asserts a genre-wide direction.

**FIX, nearly free.** Recast as an observation over named instances — Melis [30], Lucic [31], Musgrave [32] and Ferrari Dacrema [33] each independently show a claimed advantage shrinking or reversing. **The paper already cites all four elsewhere in its genre paragraph.** As written, one citation certifies a claim about an entire literature: the exact defect this audit was commissioned to find.

Two brackets belong with it. Recht et al. [34] report slopes above one (1.69 CIFAR-10, 1.11 ImageNet), which the paper correctly pre-empts as a relative slope — and Recht's own headline is an 8–11 point accuracy *drop*, squarely in the shrink family. And Maassen et al.'s recomputation of 500 effect sizes across 33 psychology meta-analyses found corrections going up 19 times and down 14, no systematic bias. That leaves the narrow scalar claim intact but kills the *implication* that an upward correction is intrinsically surprising — which the paper half-concedes already, so citing Maassen there converts a hedge into a supported statement at zero cost.

### E. `demsar2006statistical` does not contain the threshold it is cited for

**The paper:** "we are below the threshold for the test we ran: **this omnibus is recommended for more than ten datasets** [36]."

**Verified first-hand from the 30-page JMLR PDF (103,393 characters):** `more than ten` = 0 occurrences; `at least ten` = 0; `ten or more` = 0; `ten data sets` = 2, **both describing Demšar's own power-simulation sampling procedure**.

**This is a fabricated threshold attributed to a real source, and it inverts his reasoning.** He recommends "the Friedman test with the corresponding post-hoc tests for comparison of more classifiers over multiple data sets" with no dataset-count floor anywhere, and his stated context is explicitly small-n: "the number of data sets is usually much less than 30." He recommends the non-parametric route *because* n is small.

**FIX, a net gain.** Delete the clause and the citation. The power limitation is independently established by the rest of the same sentence — the paired-test calculation (|d_z| ≥ 1.27 for 80% power at α=0.05, n=7) and Agarwal's never-claim-equivalence point [37], both verified. **The paper was conceding a methodological weakness it does not have.**

### F. `li2024bnnsurrogates` — the K-range claim is false as written

**The paper (Confound 3):** "Our sweep runs over K∈{2,3,5,10} and therefore **extends below** the K∈{5,10} range over which ensemble surrogates were found robust [18], **sharing its two upper points and adding K=2,3**."

**Verified first-hand from arXiv:2305.20028v2 (39 pages, 111,042 characters): Figure A.7 legend tokens on page 28 are `['2 Models', '5 Models', '10 Models']`**, corroborated independently by rendering the page as an image. Their caption: "the different ensembles perform similarly across many experiments, **showing the robustness of our results to this hyperparameter**." A second K=2 appearance is in Figure A.5.

**The range is {2,5,10}.** The priority claim collapses to "adding K=3." Worse than a wording error: the K-sensitivity framing exists to establish that the headline sits at the maximum of a sensitive curve, and the closest prior work reports the opposite conclusion over an overlapping range including the very endpoint claimed as an addition. A reviewer from that group reads this as the paper claiming credit for their experiment.

**FIX (mandatory, and it must be a real fix).** (1) Correct the range wherever `{5,10}` appears. (2) State the residual, which is real and appears nowhere in the paper: **Li/Rudner/Wilson measure ensemble-BO *performance* robustness; the paper measures whether the *variance attributed to the surrogate axis* is robust.** Different quantities, both can be true — and made explicit the claim survives in a narrower, more interesting form. (3) Keep the K-sensitivity result; delete only the "extends below" priority claim.

### G. `abe2022ensembles` does not support the direction it is cited for

**The paper:** "the decline with K runs against **the direction reported for ensemble quality** [38]." **Abe et al. runs zero ensemble-size ablation** — full text extracted (15,095 words), zero hits for `ensemble size`, `number of models`, `size of the ensemble`. Configurations are fixed at M=4 on CIFAR-10 ("combining 4 out of the 5 random seeds") and M=5 on an ImageNet subset, fixed by seed availability rather than swept; the thesis is ensembles versus a single larger model. **There is no reported direction-with-K to run against.**

**FIX.** Replace with the source that does report it: Lakshminarayanan et al. [27], Table 4, ImageNet M=1→10, monotonic diminishing-but-never-negative improvement (Top-1 error 22.166% → 18.675%): "We observe that as M increases, both the accuracy and the quality of predictive uncertainty improve significantly." State the caveat — classification calibration, not offline-MBO reward, so the transfer must be stated rather than assumed. `abe2022ensembles` can stay for what it does support.

### H. `ghasemipour2022pessimistic` is an over-extended analogy

**The paper (Confound 4):** the incomparability principle "is owned by the interval-validity literature [46] and **its offline-RL instance** [39]." **Their entire scope is one surrogate class (Q-ensembles)**, and their axis is an internal training-procedure choice — shared versus independent Bellman targets, full versus weight-shared ensembles. They never compare across model families, so they are not an instance of a *cross-model-class* principle. Their actual finding is stronger and different in kind: **shared targets can flip the LCB's sign — pessimism becomes optimism** — rather than merely rescaling an interval.

**FIX.** Restate accurately: *a training-procedure choice within one surrogate class can invalidate, not merely miscalibrate, nominal pessimism.* **The accurate version is more useful**, because the same source supplies the only candidate positive mechanism this audit found for the inversion result, and stating what it really shows sets that up.

### I. `rahaman2019spectralbias` motivates the wrong ablation

**The paper (Elimination 2):** "wide networks approach GP behaviour [41] and **finite networks show spectral bias** [40]... so we ran the ablation that does. At fixed K=5, sweeping per-member **width** over a 10.7× range leaves the gap unchanged."

**Three of the four citations verify clean, and the audit should say so** — this is the cluster most likely to be assumed sloppy and it holds up. Jacot [41] supplies the frozen-NTK mechanism and the training-time Gaussian result; Lee 2018 the at-initialization NNGP correspondence; Lee 2019 the load-bearing proof that the output *during* gradient descent converges to a Gaussian in the width limit. Together they cover "wide networks approach GP behaviour." One nuance is elided but not falsified: the training-time GP is not literally Lee 2018's Bayesian NNGP ("noticeably different" predictive distributions, in Lee 2019's own words).

**Rahaman is a different story.** The theorem holds "for **arbitrary width and depth**" — not a width-limit statement. The defining experiment varies training *iterations*, not width. And their own ablation finds: "increasing the depth (for fixed width) significantly improves the network's ability to fit higher frequencies... increasing the width (for fixed depth) also helps, but the effect is **considerably weaker**" — despite width scaling exponentially (16→32→64→128) against depth's linear increase (3→4→5→6). **The paper cites spectral bias to motivate a width ablation, when the source says width is the weak lever — and `main.tex:88` fixes the ensemble at a two-hidden-layer MLP across the entire sweep. It varies the axis Rahaman calls weak and holds fixed the axis Rahaman calls dominant, so the width-only ablation cannot have tested the mechanism it invoked Rahaman to motivate.**

**FIX — the second option is better.** (1) Minimal: drop the citation; the width objection stands on the verified NTK/NNGP lineage. (2) **Better: keep it and state the limit** — spectral bias is reported as primarily a *depth* phenomenon, the ablation sweeps width at fixed depth 2, and the depth-driven version of the objection **remains open**. One clause converts a miscitation into a correctly-scoped limitation and names a follow-up. Note the asymmetry with the paper's own care: it is scrupulous that the sweep "stops at 1024 while the kernel limits are asymptotic," and has not applied that scrupulousness to depth.

**Consequence for the headline framing.** "Seven controls, none survives" is a bare count doing rhetorical work the underlying controls do not fully support: capacity is eliminated *at fixed depth 2*, not eliminated. Stating each control's scope (width at fixed depth; σ at this ensemble construction) costs little and forecloses this line of attack.

### J. `fannjiang2020autofocused` articulated the core diagnosis in 2020, uncited

The sharpest missing-related-work finding, and the one most likely to be raised by a reviewer from the offline-design community. The paper's central diagnosis, offered as its own: "What differs is **which** off-distribution maximizers a surrogate's mean admits." Fannjiang & Listgarten [42], verbatim: "oracle-based design... **will query the oracle in regions of the design space that are not well-represented by the oracle training data**... **its outputs, including its uncertainty estimates, become unreliable beyond the training data**," and "sub-optimality can be extreme due to **pathological behavior of the oracle when the search model... strays too far from the training distribution**." That is the founding articulation, six years earlier, including the uncertainty-estimates clause. **It sits in the paper's own bibliography, uncited.**

**It kills nothing** — no factorial machinery, no surrogate-class comparison. **FIX, and it converts a liability into the paper's best related-work paragraph.** Cite Fannjiang as the origin, then state the refinement: the off-support story is right in aggregate and *insufficient* as an explanation of the class gap, because at matched distance the classes still differ (medians 0.87 / 0.86 / 0.84, ensemble worse in true oracle value by −1.406 [−2.803,−0.375]). **That is a genuine advance on a named prior position**, and far stronger than presenting the diagnosis as unprecedented.

### K. Bibliographic and internal defects

**`kim2025mbosurvey`.** Venue resolved: **TMLR 01/2026** — every page header of v2 reads "Published in Transactions on Machine Learning Research (01/2026)," corroborated by arXiv:2603.04000's bibliography [10]. The prose ("the subfield's 2026 survey") is **accurate**; the bib entry (`year={2025}`, `journal={arXiv preprint}`) is stale. **Fix: update to TMLR 2026.** *Minor contextual over-read:* the quoted sentence about benchmarks not "clarifying whether observed gains stem from superior surrogate modeling, improved optimization strategies, or mere chance" [1] sits in §6 under uncertainty-quantification evaluation, not as a call for a crossed factorial. The quote is verbatim, so this is not a miscitation — but **keep the quote and drop the implication that the survey calls for this specific design.**

**`gao2022reward` — three defects verified against PMLR.** True venue **ICML 2023, PMLR 202:10835–10866**: the key says 2022 while the year field says 2023 (internal disagreement), and **the page range is wrong** (`10909--10934` against `10835--10866`). It is also the sharpest available reframing of Elimination 7 and sits uncited.

**`lu2022revisiting` [44] — uncited, and an N6 risk surface.** Full-text grep (37 pages, 102,811 characters): `factorial`=0, `crossed`=0, `ANOVA`=0, `variance decomposition`=0, `two-way`=0. It varies uncertainty-penalty heuristics and hyperparameters **while holding the policy optimizer fixed** — verbatim: "our implementation uses the same probabilistic dynamics models... and policy optimizer (SAC) as MOPO, differing from MOReL, which uses Natural Policy Gradient," with MOReL's differing optimizer flagged only as an unresolved appendix confound. **N6 stands. Fix (light): name it in related work** — a reviewer who sees a "revisiting design choices in offline model-based RL" paper sitting unengaged in the bibliography will ask why, and naming it *strengthens* the no-prior-instance claim by showing the adjacent field's closest attempt also held an axis fixed.

**The pattern worth stating:** the bibliography contains at least three papers that would *strengthen* the work, uncited — Fannjiang, Gao, Lu. That is the opposite of the usual bibliography defect and it is the cheapest fix on this list.

### L. The one numeric defect, and three presentation reconciliations

**L-1. "Five other cells tie it" should be six.** Applying the paper's own stated criterion (`inversion_rate == 1.0` and `mean_frac_worse == 1.0`) at the audited engine returns **seven** cells: Branin ens:grad plus six others (Branin ens:cma; Styblinski ens:cma, ens:grad, ens:perturb, svgp:cma, svgp:grad). Low severity — a parenthetical, direction unaffected — but it is a bare integer a reviewer with the artifact checks in one line, and this paper's credibility posture rests on such checks passing. **Fix: recount, or state the criterion that excludes the seventh.** Note the inversion artifact carries `git_sha 9843dfc8` while `beta0_reconcile.json` carries `812bcb92`; confirm the count was recomputed on the final run.

**L-2. Three sentences invite a false arithmetic catch.** The pessimism increment (0.203) is a paired bootstrap delta, not 0.525 − 0.319 = 0.206 — the artifact's `gap_delta_b2_minus_b0` is 0.20321, and every adjacent figure verifies exactly. Same for the width shrinkage (−0.006 against endpoints differing by 0.004). **Fix: one clause each stating these are paired bootstrap deltas, hence not differences of marginals.**

**L-3. The budget-matched arm reports 630 cells**, implying 10 seeds where the reader has been given 30. Consistent with the sweep convention, but the arm is presented in the body as a main result. **Fix: state the seed count where it is reported.**

### M. Verified clean — and this belongs in the report

An audit returning twelve mandatory items reads as an indictment by default; the passes are what calibrate it.

- **`shahriari2016humanoutoftheloop` — the paper is NOT over-conceding.** The review states the doctrine twice as its own organizing thesis: "the careful choice of statistical model is often far more important than the choice of acquisition function heuristic," and "[acquisition function design] plays a secondary role to the choice of the underlying surrogate model." The paper's paraphrase *understates* it, and the restriction to online BO is sound — zero hits for `offline` across 137,300 characters.
- **`chemingui2024pggs` — the falsification target is real** [47]: "prior methods that have **focused on improving surrogate models while using fixed search strategies**." Asserted by the source, not fabricated. **`dewolf2022intervals` is correctly and narrowly cited** [46], with zero hits for `acquisition`, `Bayesian optimization`, `pessimis`, `lower confidence bound`, so the paper's residual claim is correctly scoped.
- **All three citation-year traps are handled correctly:** Henderson = AAAI 2018 [48] (from the PDF copyright line; 2017 is the arXiv date); Benavoli = JMLR 17, 2016 [45]; Li/Rudner/Wilson = ICLR 2024 [18]. Recht's slopes are quoted and characterised correctly [34], and Agarwal is cited correctly for never-claim-equivalence [37].
- **The code-level traces resolve exactly**, line for line; the asymmetry Confound 1 alleges is exactly what the code shows. **The most falsifiable class of claim in the paper passes without exception.** And **the engine-stamping protocol is one the paper actually followed** — both checked artifacts carry library versions, git SHA, flags, K, β, TOP, seed range and an ISO timestamp. That is the claim most likely to be assumed rhetorical, and it is not.

---

## (ii) Kills

**No kill.** Neither N6 nor any load-bearing structural claim is refuted by prior work. Stated plainly because the brief is right that one fatal counterexample outweighs a hundred improvements, and none was found across a recency sweep, a ~347-paper forward walk, an adversarial sweep of three previously unsearched regions, and a fresh re-confirmation of every near-miss.

**One specific ledger row is killed, and it is not existential.** The claim that the K-sweep "extends below the K∈{5,10} range... sharing its two upper points and adding K=2,3" is **false as written**: Li/Rudner/Wilson tested K ∈ {2,5,10} and reported robustness across that range [18], verified twice independently from the primary PDF. This kills a priority claim inside Confound 3, not the K-sensitivity measurement, which is real and concerns a different quantity. Fix at (i.F).

**Two near-kills that resolve in the paper's favour — and the reasoning must be on the page.** Hamdan et al. [35] establish that in the one ML literature where "confound removal increased an effect" has been studied, the documented default diagnosis is **leakage artifact, not validity**: "this common deconfounding approach **can leak information such that what are null or moderate effects become amplified to near-perfect prediction**." Different genre, so not a kill — but worse than a kill in one respect, because it hands a reviewer a free alternative explanation for the headline direction. **The paper can rule it out cheaply and convincingly:** its two corrections are a target rescaling and a candidate-selection rule, neither of which regresses a confound out of features, which is the mechanism leakage requires. That argument is currently nowhere on the page. Add `hamdan2022confoundleakage` and dispatch it in two sentences.

Second, an exhaustive fresh sweep for an ML benchmark audit whose corrected effect size *grew* returned **zero grow-direction hits** across fourteen verbatim queries, including the reproducibility-track literature (ML Reproducibility Challenge, ReScience C) as the natural home for such a result. One new on-target reanalysis was found and it runs the other way: Robinson, Glen & Lee (*J. Comput. Aided Mol. Des.* 2020), reanalysing a large-scale deep-learning-versus-ML bioactivity comparison, report "support vector machines achieve competitive performance compared to feed-forward deep neural networks." **The narrow claim stands and is better evidenced than when the paper made it** — three independent, directly-on-target ML benchmark reanalyses (Robinson, Musgrave [32], Ferrari Dacrema [33]), all shrink-direction, zero grow.

**Residual kill risk, stated honestly.** One paywalled paper (Elsayed & Lacor 2014, §F above) has the most N6-shaped title in the corpus and could not be obtained by any free route. If its crossing is genuine rather than sequential, and if it reports a decomposition, N6 falls. That is the only live kill surface this audit leaves open, and it is resolvable in minutes with institutional access.

---

## (iii) Scope of Novelty, Ranked

### A. The boundary condition, first — because it governs everything below

Two positive findings sit in the paper's artifacts, unreported. Both are real. **Each survives exactly what the other fails**, and only the pairing is defensible.

| | **Interaction η²** | **7/7 raw-units attenuation** |
|---|---|---|
| Significant, interval excludes zero | **yes** — all four corners, lower bounds 0.087–0.107 | no — descriptive cell means, no intervals |
| Survives bootstrap bias correction | **yes** — 0.134–0.156 | n/a |
| Survives the min–max normalization challenge | **no** — rides on the endogenous normalizer | **yes** — raw oracle units, pure arithmetic |
| Survives the floor-effect challenge | **yes** — unaffected | **no** — Styblinski points the wrong way |
| Generalises past the synthetic grid | **no** — Design-Bench is 0.006–0.041 | untested on Design-Bench |

**Recommendation: report both together, with the floor-effect confound disclosed as a question the paper poses and tests.** Lead with the interaction, scoped explicitly to the synthetic grid, supported by the formal simple-effects table (which has the intervals the raw-units analysis lacks). Present the raw-units attenuation as its interpretation. **Promoting either alone is an overclaim**, and promoting an unqualified 0.15 into the abstract would import the exact fragility the paper's Discussion warns about.

Three independent routes reached the interaction — two depth investigations and the orchestrator's own artifact work, none prompted by the others. Convergence from independent paths on a quantity the paper prints four times and never discusses is itself a finding.

### B. The ranked list

Ranked by value per pre-deadline hour. Ranks 1–8 require **zero new computation**.

---

**RANK 1 — Interpret the interaction term. `FOLD-INTO-THIS-PAPER / CHEAP`.**

| Corner | η²_surr | η²_opt | **η²_inter** | interaction 95% CI | inter/opt |
|---|---|---|---|---|---|
| off/off | 0.367 | 0.013 | **0.165** | [0.107, 0.260] | 12.4× |
| on/off | 0.283 | 0.036 | **0.146** | [0.088, 0.249] | 4.0× |
| off/on | 0.450 | 0.006 | **0.152** | [0.094, 0.230] | 26.9× |
| on/on | 0.405 | 0.005 | **0.160** | [0.087, 0.236] | 32.8× |

The interval excludes zero in **all four corners**. It is the second-largest effect in every corner, ordered `surrogate > interaction > optimizer` without exception. And it is **the most stable effect in the paper** — range 0.018 across corners against the headline's 0.167, i.e. **9.2× more stable than the number it would sit beside.** The paper's central methodological caution is that any η²_surr is a joint artifact of four operating-point coordinates; it never notices that the interaction is nearly *invariant* to the one coordinate it shows the headline is most sensitive to.

**The word `interaction` appears exactly once in `main.tex`** — in the sentence explaining why Moosbauer *declined* the analysis that finds it [3]. The paper argues that interaction detection justifies its design, runs the design, finds a significant interaction in all four corners, prints it in a column with no interval, and never mentions it again.

Four reasons this is a major result. **(1) It is the strongest available vindication of N6.** The case for a crossed factorial over one-factor-at-a-time is that OFAT cannot estimate interactions — a point the standard reference states in the paper's own notation: "OFAT experimentation leaves us in the dark about factor interactions," and under an interaction the optimal setting of one factor *reverses* depending on the other's level [19]. Every near-miss in the ledger is structurally incapable of producing this number. **It is the answer to "why did anyone need to run this?"** **(2) It reframes the optimizer null, the paper's weakest passage.** The paper warns correctly but without evidence that η²_opt = 0.038 "licenses 'optimizer choice explains little variance' and never 'optimizer choice is arbitrary' — the second reading is false on our own data." **The interaction is that evidence and is not cited there.** The supported statement: optimizer choice has a small *marginal* effect and a substantial *conditional* one, by 4–33× the marginal. **(3) It is a positive, quantitative, significant result in a paper whose mechanism section is seven negatives**, and **(4) it cannot be dismissed as an operating-point artifact** — the paper's own stated vulnerability for every other number. One caution travels with it: interactions are notoriously underpowered, with a median power of .18 to detect a typical-size interaction across 159 preregistered hypotheses [49]. That an interval excludes zero in all four corners here is therefore *more* noteworthy, not less.

**Precedent check — the strongest support for promotion.** A widened sweep across ML benchmarking generally returns **no precedent**. Schmidt et al. [66] show zero hits on all formal terms, offering only qualitative "depends on the problem" language. Choi et al. [67] argue rankings are confounded by asymmetric hyperparameter search spaces, which is not an interaction. Steiner et al. explicitly grid augmentation strength × model size × data budget, call it "interplay," and never compute a formal interaction statistic. **No ML benchmark study reports and interprets a component-by-component interaction — verified across three independent regions.** That raises the cost of leaving it uninterpreted considerably.

**Three sub-items fold in, all free.**

**1a — Connect `tab:cross` to the interaction.** The supplement's coverage table: the ensemble premise holds at 0.73 in-distribution, **0.97 on the GP's proposals** — better than the GP's own 0.93 — and **collapses to 0.41 on its own**. The paper's reading is correct and it does not notice what it has said: *"The ensemble is not miscalibrated in general — only where its own gradient optimizer drives it"* **is a description of an interaction.** Premise validity is not a property of the ensemble; it is a property of the ensemble-optimizer pair. So the paper has, in two tables, a significant interaction it never interprets and a direct mechanistic measurement of what that interaction consists of — and never connects them. **Coverage figures are probabilities, not min–max-normalized scores, so the 0.41-versus-0.97 contrast is untouched by the normalization critique.** The η² establishes the interaction is large; `tab:cross` establishes what it is. One sentence each way.

**1b — Name the normalizer as a fifth operating-point coordinate.** Every η² in the paper is computed on per-task min–max normalized cell means over nine cells, where the min and max are two of the nine arms compared. Jordan et al. [52] name this exact endogenous form as outlier-exploitable, verbatim; Bellemare et al. [53] — the *origin* of the technique — document it flipping a ranking (Zaxxon) and note it "gives no indication of the objective performance of the best algorithm"; and Benavoli [45] closes the obvious escape, since rank statistics are pool-dependent. **A 33-combination recomputation across five alternative normalizers, four corners, five β levels and both budget levels, plus leave-one-task-out, found every combination preserves η²_surr > η²_opt — while magnitudes move.** Direction robust, magnitude fragile. **This lands almost exactly where the paper's framing already sits** — "the direction is invariant to all four... Only the size of the gap moves." The fix is not a retraction; it extends an argument the paper already makes to a fifth axis, supportively. (Honest correction: I raised this alarm on Griewank-30D's 2,780× outlier spread; the recomputation found Griewank is the *smallest* lever on the headline.)

**1c — Report the formal simple-effects table.** Once an interaction is significant, main effects can mislead, and the standard remedy is a simple-effects decomposition (for a 3×3 design, two main effects and six simple effects). Computed from stored per-seed data at the primary corner: **η²_surr | perturbation = 0.007 [0.001, 0.048]; | gradient = 0.735 [0.50, 0.98]; | CMA = 0.762 [0.53, 0.99].** This is the version to report, because it carries intervals. It does not dissolve the floor-effect confound.

**1d — The raw-units form, confound disclosed.** GP-minus-ensemble gap in **raw oracle units**, per optimizer, per task, from the supplement's own `tab:sfull`:

| Task | grad | pert | cma | pert gap as % of the larger aggressive gap |
|---|---|---|---|---|
| Branin-2D | 8.87 | **0.38** | 13.61 | 2.8% |
| Styblinski-5D | 21.20 | **3.07** | 21.44 | 14.3% |
| Levy-8D | 2.09 | **0.16** | 3.14 | 5.1% |
| Rosenbrock-10D | 0.19 | **0.04** | 0.39 | 10.3% |
| Rastrigin-15D | 2.88 | **0.16** | 5.75 | 2.8% |
| Ackley-20D | 3.11 | **0.04** | 3.72 | 1.1% |
| Griewank-30D | 2591.06 | **125.00** | 2612.00 | 4.8% |

**On 7 of 7 tasks, spanning 2D to 30D**, the surrogate gap under perturbation is smaller than under both gradient and CMA — averaging 5.9% of the aggressive-optimizer gap, roughly 17× attenuation. No normalization, no bootstrap.

**It unifies six results the paper reports separately in five sections:** the interaction η²; `tab:cross` coverage; the x0-inversion; Elimination 4 (more budget *widens* the gap — because more budget means more aggressive exploitation); the Design-Bench frozen cells (GP-plus-perturbation is the frozen pairing); and the Design-Bench optimizer inversion. **And it explains the paper's biggest puzzle** — why the optimizer axis is negligible on synthetic tasks but inverts on Design-Bench — as one fact: where perturbation is competitive, the surrogate axis collapses and the optimizer axis surfaces. It is also the only genuinely **practitioner-facing** statement available: *if you must use a neural ensemble surrogate, do not pair it with gradient ascent.*

**I tested the competing explanation and it survived.** Perturbation might attenuate the gap merely because it *underperforms*, compressing everything. **The one task where perturbation is the grid's best optimizer — Styblinski-5D, GP+Pert at 36.15 — is the task with the weakest attenuation (14.3%).** That is exactly what a floor effect predicts. A single contrary point does not settle it, but it is the only case that *discriminates*, and it points the wrong way for the causal reading. **The descriptive fact is solid; the causal reading is not established.** The disentangling analysis is cheap and nameable: compare each optimizer's absolute score against the offline dataset's own best design per task, separating attenuation from under-performance. Both quantities are already stored (`mean_x0_best`, `mean_ret_best` in `x0_inversion.json`), so this is re-analysis, not a new run.

---

**RANK 2 — Report the bootstrap bias correction, and name ε² rather than ω². `FOLD-INTO-THIS-PAPER / CHEAP`.**

η² is positively biased at small n, and the paper reports it at n=7 throughout — abstract, headline, every corner, the β and budget axes — with no caveat. **Its own bootstrap artifacts already contain the bias estimate, unreported:** the bootstrap mean exceeds the point estimate in all four corners, by +0.0099 to +0.0184.

**Bias-corrected, the headline gets stronger.** The reported 0.367 → 0.405 rise of +0.0376 becomes **0.351 → 0.395, a rise of +0.0437.** Direction survives; the effect *grows*. And the interaction survives at **0.134–0.156** — still second-largest in every corner, still an order of magnitude above the optimizer main effect, still tightly stable (range 0.022).

**One correction to the standard advice.** Okada's Monte Carlo study [50] (one million replications per condition) tabulates η² bias as **+0.054 at n=10 per group, falling to +0.005 at n=100** — always positive, shrinking with n — while ε² and ω² are always small and negative. But Okada's own simulation **overturns the folk belief that ω² is the least-biased correction: ε² is.** Liu (2022) [51] states the bias firsthand, attributes the corrections directly (Kelley 1935 for ε², Hays 1963 for ω²), and independently validates the bootstrap route the artifacts already implement: "bootstrap bias correction does not make distributional assumption, and it is easy to implement." **Recommend ε², or both, or simply the bootstrap-corrected values already in hand.** One sentence and one supplementary column buys immunity from the most obvious statistical objection to the central number.

---

**RANK 3 — The budget axis is a contribution to a named line, not a defence. `FOLD-INTO-THIS-PAPER / CHEAP`. The clearest UNDER-STATED finding.**

The paper presents its budget result defensively — "the obvious objection is that the optimizer axis is search intensity wearing a costume." Read against the literature it does not cite, it is not a defence.

COCO/BBOB [54] §3.5 formally names **budget-dependent benchmarking** as an established category with a decade-old apparatus: fixed-budget versus fixed-target views and anytime assessment, adopted precisely because performance comparisons are budget-sensitive. Kazikova et al. [55] confirm from the metaheuristics side that budget-matched comparison is "standard practice" and that raising the budget "may significantly affect the final verdict." And **Lucic et al. [31] — already in the bibliography, cited for the genre but not for this — state the paper's own finding at NeurIPS 2018, verbatim: "bad models can outperform good models given enough computational budget."**

**The budget arm carries the paper's only disjoint bootstrap intervals anywhere in the decomposition** ([0.189,0.355] against [0.421,0.719]) **plus a ranking flip** (gradient leads at low budget, perturbation at high) — and Lucic predicted the flip while COCO's framework anticipates the shape. A result carrying the strongest evidence in the paper is framed as an objection removed. **Fix: reframe as a contribution to a named line, cite COCO [54], Lucic [31] and Kazikova [55], and note that the Design-Bench arm makes the same shape of finding on an independent axis** — matching raises η²_opt by 1.46–1.88× in every corner rather than dissolving it, and moves one corner from failing to reject to rejecting.

---

**RANK 4 — The landscape negative, and the one positive structural statement the audit can offer. `FOLD-INTO-THIS-PAPER / CHEAP`.**

Tested directly against `tab:sfull` under all three optimizers: **no standard landscape covariate predicts the GP-versus-ensemble gap.** Dimension correlates indistinguishably from zero (ρ < 0.11, p > 0.8); textbook multimodality and separability classifications **actively mis-sort** the ordering. A decisive negative from looking, not an absence of looking. **Two or three sentences close a hostile reviewer's "isn't this just landscape?" objection with a falsifiable, already-computed answer** instead of the current one-line hedge.

The literature gap is real. The mature exploratory-landscape-analysis tradition — Rice's framework through SATzilla [57] to Kerschke & Trautmann [56] — has **never been pointed at surrogate-class choice**; it operates at BBOB scale to select *solvers*, and the feature-free successor literature [58] does not contain the word `surrogate` at all. The nearest structural cousin [59] compares true against surrogate landscape features but switches surrogates online, per-iteration, inside a multi-objective EA. Malan's 2021 survey flags surrogate-landscape analysis as unresolved and reports the finding that makes it hard: landscape features computed *through* a surrogate are "more indicative of the surrogate model than the original landscape" — a circularity that bites when the object being selected is itself the instrument of measurement.

**Now the structural statement, which exists only in cross-section and which no single investigation produced.** The per-task gap ranking is **stable across optimizers (Spearman 0.84–0.96)** while the per-task gap *magnitude* **collapses to ≈0.01 under perturbation against 0.4–0.8 under gradient and CMA.** These look contradictory and are not: one measures relative ordering across tasks, the other absolute magnitude within an optimizer. Both hold — tasks keep their rank order under every optimizer while the scale of the gap collapses under the weak one.

**That combination constrains any mechanism account. It rules out a purely optimizer-side story, which would not preserve task ordering, and a purely task-side story, which would not collapse. The mechanism must be multiplicative — a task factor scaled by an optimizer-aggressiveness factor.** For a paper whose mechanism section is seven negatives and no positive causal test, that is worth more than an eighth negative, and it costs two sentences. Weight it honestly: the 0.84–0.96 stability is descriptive at n=7 while the collapse is bootstrapped, so the collapse is the better-evidenced half.

The full landscape study — BBOB/COCO-scale corpora with `flacco`/`pflacco` features across many functions, instances and dimensions — is **`FOLLOW-UP-PAPER / EXPENSIVE`**, and it would inherit the circularity problem the current paper should not.

---

**RANK 5 — Report the TOST bound the paper already computed. `FOLD-INTO-THIS-PAPER / CHEAP`.**

The released `stats.py` already computed a two-one-sided-tests equivalence bound: gap **0.3762**, 90% CI [−0.1078, 0.8602], effect bound **0.4840**, **not equivalent at either a 0.5 or a 0.3 margin.** The supplement's entire treatment is one clause saying such tests "are computed" — no bound, no interval, no verdict. Lakens (2017), the standard paired-means TOST reference covering exactly this design with Cohen's d_z, is absent from the bibliography.

The paper is scrupulous about never claiming equivalence and correctly says a failure to reject is not a demonstration of absence [37]. **It has the actual equivalence test in hand and it is informative:** the data are *not* equivalent at either margin — a positive statement about what the null does and does not license, stronger than the disclaimer currently in its place. A confirmed negative supports the framing: there is no ML-benchmark-specific equivalence-testing literature; searches for equivalence/TOST/non-inferiority in ML benchmarking return only clinical hits. **Fix: report the bound and verdict, cite Lakens, and travel his caution with it** — rejecting small effects in an equivalence test requires large samples.

---

**RANK 6 — Cite Fannjiang and state the refinement. `FOLD-INTO-THIS-PAPER / CHEAP`.** See (i.J). This converts the sharpest missing-related-work liability into the best related-work paragraph. Equally cheap and adjacent: **Gao et al. [43] give closed forms for proxy degradation as a function of distance from the data** — R_bon(d) = d(α − βd), R_RL(d) = d(α − β log d) — with the functional form **differing by optimization method**, while varying only scale within one architecture family. So Elimination 7 is a refinement of Gao's principle onto a new axis (architecture class, not scale) in a new domain, *consistent with* the scaling law rather than a counterexample. That the entry sits uncited in the paper's own bibliography with three defects makes this the cheapest upgrade available. (Rafailov et al. [72] extend the framework to direct alignment algorithms and find degradation "often before even a single epoch of the dataset is completed" — confirmatory framing only; `NOT-WORTH-IT` beyond a one-clause citation.)

**RANK 6b — Give the β=0 decomposition a lineage. `FOLD-INTO-THIS-PAPER / CHEAP`.** The finding that "pessimism amplifies a mean-quality base rather than creating it" (61% of the GP advantage survives at β=0) has a precedent in shape that the paper does not cite. Fujimoto & Gu's TD3+BC ablation [65] shows RL alone is insufficient without the behaviour-cloning term, with performance robust across a broad α range and degrading only at the extremes — the same split of a method's gain between base-model quality and a conservatism term. State the distinction precisely rather than citing loosely, because that distinction is this audit's whole subject: Jin, Yang & Wang's PEVI [64] proves pessimism is *sufficient* for a guarantee and minimax-optimal, but is pure theory with **no empirical base-versus-conservatism ablation**, so it supports the framing without being a precedent for the experiment.

---

**RANK 7 — Give the inversion result its name. `FOLD-INTO-THIS-PAPER / CHEAP`.**

The paper states the inversion flatly: "it is a demonstration within this grid, descriptive at n=7 tasks, not a mechanism." **It is an instance of a named, decade-old failure category.** The offline-RL literature formalises it as **Safe Policy Improvement**: P(ρ(π,M) ≥ ρ(π_b,M) − ζ) ≥ 1 − δ — the requirement that a policy learned offline not be worse than the baseline it was given, with high probability. Thomas, Theocharous & Ghavamzadeh (ICML 2015) is the founding formalization; SPIBB's Theorem 2 [63] proves ζ-approximate safe improvement with high probability.

**The reframing:** the inversion is not an awkward number — it is the observation that **offline MBO optimizers ship with no safe-improvement guarantee, and the absence bites.** The sibling field built algorithms around this property a decade ago; offline MBO has not. Sharper and more transferable than "we count inversions on our grid," at two sentences and two citations. A related formal handle: CQL's Theorem 3.4 [62] proves the *gap-expanding* property — the learned Q-function widens, never narrows or inverts, the in-distribution-versus-OOD gap relative to the truth. The paper's inversion can be re-quantified as a violation of a named provable property, upgrading a descriptive count into a statement about a missing guarantee.

---

**RANK 8 — Advertise the independent replication the paper is obscuring. `FOLD-INTO-THIS-PAPER / CHEAP`.**

0.406 and 0.405 are not one measurement at two precisions. They are **two independent runs at the same operating point**: the β-sweep endpoint at β=2 (`kbeta_analysis.json`, 10 seeds) gives 0.40636; the headline corner (`bootstrap_eta_corners.json`, 30 seeds) gives 0.40455. Run separately, landing 0.0018 apart. **That is a replication and the paper does not say so.** A paper whose central scalar is challenged as an operating-point artifact should be advertising an independent reproduction, not letting a reader assume rounding.

---

**RANK 9 — The under-executed experiments, ranked by cost.**

| # | Experiment | Motivation | Tag |
|---|---|---|---|
| 1 | **Fit the far-field functional form.** Xu et al.'s Theorem 1 proves ReLU MLPs converge to **linear functions along rays from the origin outside the training support**, at rate O(1/t) [60] — the paper's diagnosis made mechanical: an ensemble mean growing linearly without bound admits unbounded maximizers at the box boundary; a GP mean reverting to its prior does not. "Which off-distribution maximizers a surrogate's mean admits" becomes a testable claim about each surrogate's far field. **Runnable on stored trajectories; no new training. The highest-value item here.** | [60][41] | `FOLD-INTO-THIS-PAPER / CHEAP` |
| 2 | **Weight-space sensitivity.** Dao et al.'s (α,ω)-sensitivity perturbs the surrogate's **own parameters** and measures how far the prediction at the found optimum moves [61]. **None of the seven eliminations touches weight-space fragility** — a new axis, computable on trained checkpoints. | [61] | `FOLD-INTO-THIS-PAPER / CHEAP` (arXiv 2025, **venue unverified**) |
| 3 | **Member-independence test.** Ghasemipour et al. prove shared pessimistic targets can render an ensemble **paradoxically optimistic**, with member independence load-bearing [39] — directly on point for a paper whose puzzle is a pessimistic ensemble ranking its own hallucinations above real data. Measure pairwise prediction correlation across the K=5 members at the returned optima and check whether inversion rate tracks it. **The first candidate *positive mechanism* the audit found that the seven eliminations do not already rule out.** Compounds with the Lakshminarayanan caveat [27]: an MSE-trained ensemble taking cross-member variance as σ is the construction most exposed to insufficient diversity, and the paper treats its ensemble as a fixed given. | [39][27][29] | `FOLD-INTO-THIS-PAPER / CHEAP` if per-member predictions were stored; `FOLLOW-UP` otherwise |
| 4 | **Fit R(d) on the 5,040 instrumented optima** — Gao's closed forms are directly fittable to existing distance-versus-oracle-value data. | [43] | `FOLD-INTO-THIS-PAPER / CHEAP` |
| 5 | **The floor-effect disentangling** (Rank 1d). Data already stored. | — | `FOLD-INTO-THIS-PAPER / CHEAP` |
| 6 | **The mixed-effects model with task as a random effect.** The repository's own flaw ledger calls for it; no normalizer check substitutes. **Two independent investigators named this as their falsifier** — the most-cited open item in the audit. | — | `FOLD-INTO-THIS-PAPER / CHEAP-to-MEDIUM` |
| 7 | **A depth sweep at fixed width**, closing the objection Rahaman actually motivates (i.I). | [40] | `FOLD-INTO-THIS-PAPER / MEDIUM` — or state the limit and defer |
| 8 | **The double-dissociation transplant.** An unconstrained deep-kernel GP-with-neural-features should fail like the ensemble; a bi-Lipschitz-constrained variant should recover GP-like behaviour. The cleanest *causal* test available. | [24][25] | `FOLLOW-UP-PAPER / EXPENSIVE` (borderline CHEAP if scoped to one 2D task) |
| 9 | **A graded three-arm battery** varying distributional mismatch, upgrading the binary inversion count into a dose-response curve. Requires new runs. | — | `FOLLOW-UP-PAPER / EXPENSIVE` |

One resolved compatibility question, because it would otherwise read as an internal contradiction: recommending Xu's NTK linear-extrapolation theorem [60] while Elimination 2 cites the NTK lineage to argue width does *not* explain the gap is **not** inconsistent. They are asymptotic in different variables — Xu in far-field distance from the support, Elimination 2 in width, which it explicitly disclaims as an asymptotic claim. **One clarifying sentence is needed if the paper adopts Xu**, because nothing currently distinguishes "NTK regime" from "the kernel limits are asymptotic" for a reader who meets both.

---

**RANK 10 — Venue framing. `FOLD-INTO-THIS-PAPER / CHEAP`, placement held loosely.**

AAAI-27's main track evaluates submissions "for the **significance and novelty** of the contributions" as **one bundled dimension** [68] — no Originality rubric distinct from Significance. It licenses non-method work ("contributions may be... **critical** (e.g., principled analyses and arguments that draw attention to problematic choice of goals, assumptions, or approaches)"), then states a preference for papers that "explore **new territory**... **preferred to** papers that advance the state of the art, but only **incrementally**." No contribution-type rubric exists for the main track. The counterfactual is instructive: NeurIPS's Evaluations & Datasets track [69] separates Originality from Significance, states "Originality **does not necessarily require introducing an entirely new method**," and enumerates a contribution type matching this paper almost exactly — "Reproducibility, Auditing, and Stress-Testing of Evaluations" — with its own rubric line, "**Negative results are valuable when rigorously supported**." NeurIPS did not merely tolerate the genre; it built a track, trained a reviewer pool, and pre-authorized the shape.

**Operational consequence: at AAAI, genre framing is necessary but not sufficient, and leading with a positive result matters more here than elsewhere.** The paper's bibliography names six canonical genre instances — two NeurIPS, one ICLR, one ECCV, one RecSys, and exactly one AAAI [48], from 2018. Two cheap moves: choose `ML: Evaluation, Benchmarking, Datasets & Analysis` as primary topic keyword, which summons a materially more audit-sympathetic reviewer pool; and promote the PGS falsification hook [47] — a named, falsifiable belief held by a paper that appeared **at this venue two years earlier** — from a scope-limiting aside into a framing hook. **Recommend the content firmly and the placement tentatively:** two independent investigations converged on low confidence about abstract-versus-main-text.

---

**RANK 11 — `NOT-WORTH-IT`: reduce the prominence of the N9 "no precedent" claim.** The narrow scalar claim survives everything thrown at it (deliverable ii), but it is now bracketed on both sides — by a documented ML mechanism that produces upward moves illegitimately [35], and by a documented non-ML literature where upward moves are unremarkable — and it requires an affirmative leakage rebuttal to hold its current weight. **The claim is defensible; its prominence is not efficient.** Keeping it as a stated observation with the rebuttal attached costs two sentences; expanding it spends reviewer goodwill on the paper's least robust rhetorical asset while the interaction and the budget axis, both better evidenced, sit under-reported. Downgrade, do not delete. Also `NOT-WORTH-IT` for this submission: the equivalence-testing methodology thread beyond reporting the bound, and the feature-free algorithm-selection literature [58], which is adjacent but selects solvers from raw instance sequences with no surrogate axis at all.

---

**RANK 12 — The conformal transfer clause. `FOLD-INTO-THIS-PAPER / CHEAP`, ranked low because severity is moderate.**

The supplement's Proposition 2 is **formally correct**: it defines w as the true density ratio dΠ/dP, so "weighting by w restores validity" is exactly Tibshirani et al.'s theorem [71]. (An earlier pass recorded this as a missing hypothesis; reading the supplement directly showed that was wrong, and it is withdrawn.) **What is true is that the clause is correct and practically inert in the paper's own setting, and the paper never says so.** Tibshirani's guarantee holds for *known* w; the estimated-ŵ case is supported empirically only, with no theorem bounding the coverage gap, and Angelopoulos & Bates corroborate: "exact when the magnitude of the distribution shift is known." Here Π is the distribution of designs an optimizer proposes after ascending a surrogate — where w is least knowable and arguably not well-defined. Nothing in the paper estimates w or applies weighted conformal, and its own measurements agree: conformal repair "restores in-distribution coverage to its 0.90 target on every task but **leaves OOD coverage erratic**" (0.00 on five tasks). **Fix: one or two sentences saying the clause is stated for completeness rather than applied — then take the free win.** The erratic OOD coverage is *what one should expect* when the repair's precondition is unavailable, not an anomaly, and saying so converts an unexplained table into a correctly-scoped negative result that reinforces the paper's separate argument that premise coverage is separable from optimization outcome [70].

### C. Forward implications

The finding with the longest half-life is neither the headline η² nor the seven eliminations. It is the **conditionality** — that the surrogate-class advantage is largely a property of the surrogate-optimizer *pair* rather than of the surrogate. If that holds beyond this grid, it dissolves the framing question the subfield has been arguing about. The dispute between the surrogate-side lineage and the optimizer-side lineage [47] is not a dispute about which factor matters; it is a dispute about which conditional slice each camp is standing in. A surrogate paper evaluated under gradient ascent and an optimizer paper evaluated on one fixed surrogate are estimating different quantities, and neither is estimating the thing the field reports.

That has immediate consequences for how the next generation is evaluated. The 2026 frontier is generative — diffusion language models [8][9], support-proximity diffusion estimation [11], flow-based domain models [12], meta-learned surrogates [13], ranking-theoretic surrogates [10], conformal per-candidate certification [14]. Almost all bundle the generative model and the search procedure into a single reported number, exactly as the lineage this paper dissects does, and several bundle them *inseparably*: a diffusion policy trained end-to-end through DA/SFT/RL has no clean optimizer factor to vary at all. **If a crossed factorial is going to remain runnable in this subfield, it has to be run now, on the last generation of methods where the two axes are still separable.** That is a timeliness argument the paper does not make and could make in one sentence.

The second implication concerns the instrument rather than the result. This audit's methodology is more portable than its findings: five homonym traps across five papers, four venue attributions caught wrong (two in the audit's *own* recommendations), a fabricated threshold attributed to a real source, and a bibliography holding three papers that would strengthen the work if cited. None is specific to offline MBO. A stability benchmark already exists for offline optimizers [15]; the natural sibling — a benchmark for *attribution* rather than performance, with the two axes shipped separable by construction — does not, and this paper's grid is the closest prototype. That is a follow-up with a clearer contribution than any additional elimination.

---

## What I could not verify and why

Grouped by *why* verification failed, because the reasons differ in how much they should discount a finding.

**A. Paywalled or access-blocked primaries.** **Elsayed & Lacor (2014)** is the one that matters, and it is disclosed in the N6 verdict rather than here, because it is the only live kill surface. Beyond it: Kelley (1935) and Olejnik & Algina (2003) were verified secondhand via the JOSS `effectsize` documentation, though the fix no longer rests on them — two open-access primaries [50][51] were obtained and one refines the recommendation. Montgomery Ch. 5 could not be reached (O'Reilly 403, dokumen.pub 403, Google Books quota exhausted); the positive DOE framing rests instead on NIST/SEMATECH [19] and Box (1989), both open and quoted directly. Yu et al. (2016) on landscape-driven surrogate selection was blocked by an AWS-WAF bot-challenge on IEEE Xplore — a genuine access failure, not a budget decision. Rudolph (1994) returned 403 on three hosts; the safe-policy-improvement framing [63] carries the point instead.

**B. Venue attributions I could not confirm — and two my own subagents got wrong. This is the category that matters most, because the errors were mine, not the paper's.** A depth investigator reported Dao et al. as "arXiv:2503.04181, ICML 2024." **arXiv v1 is dated 2025-03-06 — chronologically impossible** — and OpenAlex has no title match. The venue is withdrawn; cited as arXiv 2025, venue unverified [61]. Two subagents gave two different venues for Ghasemipour et al. (NeurIPS 2022 and ICML 2022); OpenAlex resolves arXiv:2205.13703 to a preprint with no conference venue. Cited as arXiv 2022, venue unverified [39] — which matters more than usual, because Ghasemipour is load-bearing twice, supplying a mandatory fix *and* the candidate positive mechanism. Choi et al. [67] was flagged venue-unverified by its fetcher rather than guessed: no `Comments` or `Journal-ref` field on arXiv, no proceedings footer in the PDF. **The brief says this project has caught fabrications. The fabrications this pass caught were not in the paper under audit — they were in this audit's own relays.** Rule applied to the whole deliverable: every citation recommended for addition carries its arXiv ID, and any venue not verified first-hand is marked unverified rather than guessed.

**C. Tooling and infrastructure.** `hyperresearch fetch` cannot ingest PDFs in this environment — every arXiv PDF URL form returns a junk-content rejection, traced to the post-fetch junk gate rather than extraction (an earlier "missing pymupdf" diagnosis tested the wrong Python and is withdrawn). **Consequence: most vault notes for PDF sources hold only the arXiv abstract page.** All full-text verification ran via ar5iv/HTML mirrors or `curl` plus pymupdf **outside** the vault, so the verdicts do rest on primary full text but a later reader cannot re-grep it from the note. Semantic Scholar returned HTTP 429 for the entire session on both endpoints; arXiv and OpenAlex carried all citation chaining including the N6 forward walks. OpenAlex full-text search is very noisy here — it returned climate models and echocardiography for optimization queries — so its null results are weak evidence of absence and the N6 verdict does not rest on them.

**D. Analyses recommended but not run.** The mixed-effects model with task as a random effect (Rank 9, item 6) — the repair the repository's own flaw ledger calls for, and the item two independent investigators named as their falsifier. The floor-effect disentangling (Rank 1d): the data exists, I did not run it. Bias correction on the interaction was computed for the four corners but not across the β and budget sweeps. **And the η² recomputation from RaM's Table 3 has not been independently reimplemented:** the N6 defence leans on a number (0.027 against 0.577) computed once, and the investigator who computed it flagged the absence of a cross-check. Likewise the corner values, inversion counts, frozen-cell counts and raw-units gaps were each computed once, by one implementation, from the stored JSON.

**E. Questions I raise without resolving.** **The TOST numeric coincidence.** Elimination 3's "the mean gap is still 0.375" and "loses the optimization comparison by roughly 0.48" sit within rounding of the TOST `gap` (0.3762) and `effect_bound` (0.4840). But Elimination 3 is described as a **synthetic-grid** result while TOST comes from **Design-Bench** artifacts. Either a three-significant-figure coincidence across two independent analyses, or a transplanted number in a load-bearing paragraph. **I could not resolve it and am not asserting either reading**; it needs the width-sweep artifact traced to the specific sentence. The author settles it in one lookup, and an audit that has already caught two of its own overstatements should not manufacture a third. Separately: **whether a depth sweep exists unreported.** The Rahaman fix's force depends on the ensemble being fixed at two hidden layers throughout the width sweep, which I read from `main.tex:88`; I did not confirm the *absence* of a depth experiment elsewhere. And `supplement.tex` was not checked for duplicate or contradictory NTK framing.

**F. Scope boundaries I did not cross.** Design-Bench's corrected corner was not re-run through the normalizer zoo. **The paper's code was verified at the line level for Confounds 1 and 2 only** — I did not audit the bootstrap implementation, the ANOVA implementation, or `stats.py`, so **every numeric verdict here assumes those are correct, which is an assumption and not a finding.** And I did not reproduce any experiment: all numeric verification compares the paper's text against its own stored artifacts. **If an artifact is itself wrong, this audit would not detect it.**

**G. Three corrections this audit made to itself.** Each time I tested my own finding, it weakened. (1) The 7/7 raw-units result was promoted as the strongest finding, then demoted when Styblinski supported the floor-effect alternative. (2) The normalization alarm was raised on Griewank-30D's outlier spread; the recomputation found Griewank is the *smallest* lever. (3) The RaM ground-(2) defence was falsified for four of nine methods by RaM's own appendix. In all three cases the corrected position is narrower and more defensible than the one I started with. **Two subagent relays also overstated findings in the direction of severity, and both were caught by reading the primary source directly.** Any verdict resting only on a relayed summary rather than text I read myself is marked as such.

---

## Sources

[1] Kim, Gu, Yuan, Yun, Liu, Bengio & Chen. Offline Model-Based Optimization: Comprehensive Review (TMLR 01/2026, Survey Certification). https://arxiv.org/abs/2503.17286
[2] Tan et al. Offline Model-Based Optimization by Learning to Rank (RaM, ICLR 2025). https://arxiv.org/abs/2410.11502
[3] Moosbauer, Binder, Schneider, Pfisterer, Becker, Lang, Kotthoff & Bischl. Automated Benchmark-Driven Design and Explanation of Hyperparameter Optimizers. https://arxiv.org/abs/2111.14756
[4] Liang et al. Benchmarking the performance of Bayesian optimization across multiple experimental materials science domains (npj Comput. Mater., 2021). https://www.nature.com/articles/s41524-021-00656-9
[5] Kůdela & Dobrovský. Performance Comparison of Surrogate-Assisted Evolutionary Algorithms on Computational Fluid Dynamics Problems. https://arxiv.org/abs/2402.16455
[6] Gorissen, Dhaene & De Turck. Evolutionary Model Type Selection for Global Surrogate Modeling (JMLR 10, 2009). https://biblio.ugent.be/publication/858680
[7] Park, Cheon, Wi & Koh. BOOST: A Data-Driven Framework for the Automated Joint Selection of Kernel and Acquisition Functions in Bayesian Optimization. https://arxiv.org/abs/2508.02332
[8] Sun, Chen, Yuan, Wu, Gu, Pal & Liu. Training Diffusion Language Models for Black-Box Optimization (ICML 2026 Spotlight). https://arxiv.org/abs/2603.17919
[9] Yuan, Chen, Sun, Zhang, Pal & Liu. Diffusion Large Language Models for Black-Box Optimization. https://arxiv.org/abs/2601.14446
[10] Lyu, Tan, Xue, He, Huang, Zhang & Qian. On the Learnability of Offline Model-Based Optimization: A Ranking Perspective. https://arxiv.org/abs/2603.04000
[11] Yang, Yuan, Sun, Du, He, Wu, Chen & Liu. Support-Proximity Augmented Diffusion Estimation for Offline Black-Box Optimization (ICML 2026). https://arxiv.org/abs/2605.11246
[12] Kuba, Miller, Levine & Abbeel. Offline Materials Optimization with CliqueFlowmer. https://arxiv.org/abs/2603.06082
[13] Fadhel, Tran, Hoang & Doppa. Black-Box Optimization From Small Offline Datasets via Meta Learning with Synthetic Tasks (AISTATS). https://arxiv.org/abs/2604.12325
[14] Choi. Conformal Candidate Certification for Offline Model-Based Optimization (ICML 2026 Workshop). https://arxiv.org/abs/2606.15217
[15] Qian, Zhu, Shu, Liu, Wen, An, Lu, Zhou, Tang & Yu. SOO-Bench: Benchmarks for Evaluating the Stability of Offline Black-Box Optimization (ICLR 2025). https://github.com/zhuyiyi-123/SOO-Bench
[16] NIST/SEMATECH e-Handbook of Statistical Methods §5.3.3.4.3, Confounding (also called aliasing). https://www.itl.nist.gov/div898/handbook/pri/section3/pri3343.htm
[17] Abdar et al. A Review of Uncertainty Quantification in Deep Learning: Techniques, Applications and Challenges. https://arxiv.org/abs/2011.06225
[18] Li, Rudner & Wilson. A Study of Bayesian Neural Network Surrogates for Bayesian Optimization (ICLR 2024). https://arxiv.org/abs/2305.20028
[19] NIST/SEMATECH e-Handbook of Statistical Methods §5.2.1.2, One variable at a time. https://www.itl.nist.gov/div898/handbook/pri/section2/pri212.htm
[20] Fan, Wang, Ng & Hu. Minimizing UCB: a Better Local Search Strategy in Local Bayesian Optimization (NeurIPS 2024). https://arxiv.org/abs/2405.15285
[21] Eriksson, Pearce, Gardner, Turner & Poloczek. Scalable Global Optimization via Local Bayesian Optimization (TuRBO, NeurIPS 2019). https://arxiv.org/abs/1910.01739
[22] Yarotsky. Examples of inconsistency in optimization by expected improvement (J. Global Optim. 56(4), 2013). https://arxiv.org/abs/1109.1320
[23] Kim & Choi. On Local Optimizers of Acquisition Functions in Bayesian Optimization (ECML-PKDD 2020). https://arxiv.org/abs/1901.08350
[24] Liu, Lin, Padhy, Tran, Bedrax-Weiss & Lakshminarayanan. Simple and Principled Uncertainty Estimation with Deterministic Deep Learning via Distance Awareness (SNGP, NeurIPS 2020). https://arxiv.org/abs/2006.10108
[25] van Amersfoort, Smith, Teh & Gal. Uncertainty Estimation Using a Single Deep Deterministic Neural Network (DUQ, ICML 2020). https://arxiv.org/abs/2003.02037
[26] Carrete, Montes-Campos, Wanzenböck, Heid & Madsen. Deep Ensembles vs. Committees for Uncertainty Estimation in Neural-Network Force Fields (J. Chem. Phys. 158:204801, 2023). https://arxiv.org/abs/2302.08805
[27] Lakshminarayanan, Pritzel & Blundell. Simple and Scalable Predictive Uncertainty Estimation using Deep Ensembles (NeurIPS 2017). https://arxiv.org/abs/1612.01474
[28] Ovadia et al. Can You Trust Your Model's Uncertainty? Evaluating Predictive Uncertainty Under Dataset Shift (NeurIPS 2019). https://arxiv.org/abs/1906.02530
[29] D'Angelo & Fortuin. Repulsive Deep Ensembles are Bayesian (NeurIPS 2021). https://arxiv.org/abs/2106.11642
[30] Melis, Dyer & Blunsom. On the State of the Art of Evaluation in Neural Language Models (ICLR 2018). https://arxiv.org/abs/1707.05589
[31] Lucic, Kurach, Michalski, Bousquet & Gelly. Are GANs Created Equal? A Large-Scale Study (NeurIPS 2018). https://arxiv.org/abs/1711.10337
[32] Musgrave, Belongie & Lim. A Metric Learning Reality Check (ECCV 2020). https://arxiv.org/abs/2003.08505
[33] Ferrari Dacrema, Cremonesi & Jannach. Are We Really Making Much Progress? A Worrying Analysis of Recent Neural Recommendation Approaches (RecSys 2019). https://arxiv.org/abs/1907.06902
[34] Recht, Roelofs, Schmidt & Shankar. Do ImageNet Classifiers Generalize to ImageNet? https://arxiv.org/abs/1902.10811
[35] Hamdan, Love, von Polier, Weis, Schwender, Eickhoff & Patil. Confound-leakage: Confound Removal in Machine Learning Leads to Leakage. https://arxiv.org/abs/2210.09232
[36] Demšar. Statistical Comparisons of Classifiers over Multiple Data Sets (JMLR 7(1):1–30, 2006). https://www.jmlr.org/papers/v7/demsar06a.html
[37] Agarwal, Schwarzer, Castro, Courville & Bellemare. Deep Reinforcement Learning at the Edge of the Statistical Precipice (NeurIPS 2021, Outstanding Paper). https://arxiv.org/abs/2108.13264
[38] Abe, Buchanan, Pleiss, Zemel & Cunningham. Deep Ensembles Work, But Are They Necessary? (NeurIPS 2022). https://arxiv.org/abs/2202.06985
[39] Ghasemipour, Gu & Nachum. Why So Pessimistic? Estimating Uncertainties for Offline RL through Ensembles, and Why Their Independence Matters (2022; venue unverified). https://arxiv.org/abs/2205.13703
[40] Rahaman, Baratin, Arpit, Draxler, Lin, Hamprecht, Bengio & Courville. On the Spectral Bias of Neural Networks (ICML 2019). https://arxiv.org/abs/1806.08734
[41] Jacot, Gabriel & Hongler. Neural Tangent Kernel: Convergence and Generalization in Neural Networks (NeurIPS 2018). https://arxiv.org/abs/1806.07572
[42] Fannjiang & Listgarten. Autofocused Oracles for Model-Based Design (NeurIPS 2020). https://arxiv.org/abs/2006.08052
[43] Gao, Schulman & Hilton. Scaling Laws for Reward Model Overoptimization (ICML 2023, PMLR 202:10835–10866). https://arxiv.org/abs/2210.10760
[44] Lu, Ball, Parker-Holder & Roberts. Revisiting Design Choices in Offline Model-Based Reinforcement Learning (ICLR 2022 Spotlight). https://arxiv.org/abs/2110.04135
[45] Benavoli, Corani & Mangili. Should We Really Use Post-Hoc Tests Based on Mean-Ranks? (JMLR 17, 2016). https://www.jmlr.org/papers/v17/benavoli16a.html
[46] Dewolf, De Baets & Waegeman. Valid prediction intervals for regression problems (Artificial Intelligence Review 55:577–613, 2022). https://arxiv.org/abs/2107.00363
[47] Chemingui, Deshwal, Hoang & Doppa. Offline Model-Based Optimization via Policy-Guided Gradient Search (AAAI 2024). https://arxiv.org/abs/2405.05349
[48] Henderson, Islam, Bachman, Pineau, Precup & Meger. Deep Reinforcement Learning that Matters (AAAI 2018). https://arxiv.org/abs/1709.06560
[49] Sommet, Weissman, Cheutin & Elliot. How Many Participants Do I Need to Test an Interaction? (Advances in Methods and Practices in Psychological Science, 2023). https://journals.sagepub.com/doi/10.1177/25152459231178728
[50] Okada. Is Omega Squared Less Biased? A Comparison of Three Major Effect Size Indices in One-Way ANOVA (Behaviormetrika 40(2):129–147, 2013). https://doi.org/10.2333/bhmk.40.129
[51] Liu. Bias correction for eta squared in one-way ANOVA (Methodology 18(1):44–57, 2022). https://doi.org/10.5964/meth.7745
[52] Jordan, Chandak, Cohen, Zhang & Thomas. Evaluating the Performance of Reinforcement Learning Algorithms (ICML 2020). https://arxiv.org/abs/2006.16958
[53] Bellemare, Naddaf, Veness & Bowling. The Arcade Learning Environment: An Evaluation Platform for General Agents (JAIR, 2013). https://arxiv.org/abs/1207.4708
[54] Hansen, Auger, Mersmann, Tušar & Brockhoff. COCO: A Platform for Comparing Continuous Optimizers in a Black-Box Setting. https://arxiv.org/abs/1603.08785
[55] Kazíková, Pluháček & Šenkeřík. How does the number of objective function evaluations impact our understanding of metaheuristics behavior? (IEEE Access 9:44032–44048, 2021). https://doi.org/10.1109/ACCESS.2021.3066135
[56] Kerschke & Trautmann. Automated Algorithm Selection on Continuous Black-Box Problems By Combining Exploratory Landscape Analysis and Machine Learning (Evolutionary Computation, 2019). https://arxiv.org/abs/1711.08921
[57] Xu, Hutter, Hoos & Leyton-Brown. SATzilla: Portfolio-based Algorithm Selection for SAT (JAIR 32:565–606, 2008). https://jair.org/index.php/jair/article/view/10556
[58] Alissa, Sim & Hart. Automated Algorithm Selection: from Feature-Based to Feature-Free Approaches (Journal of Heuristics 29:1–38, 2023). https://doi.org/10.1007/s10732-022-09505-4
[59] Rodriguez, Thomson, Alderliesten & Bosman. Temporal True and Surrogate Fitness Landscape Analysis for Expensive Bi-Objective Optimisation. https://arxiv.org/abs/2404.06557
[60] Xu, Zhang, Li, Du, Kawarabayashi & Jegelka. How Neural Networks Extrapolate: From Feedforward to Graph Neural Networks (ICLR 2021). https://arxiv.org/abs/2009.11848
[61] Dao, Nguyen, Truong & Hoang. Boosting Offline Optimizers with Surrogate Sensitivity (2025; venue unverified). https://arxiv.org/abs/2503.04181
[62] Kumar, Zhou, Tucker & Levine. Conservative Q-Learning for Offline Reinforcement Learning (NeurIPS 2020). https://arxiv.org/abs/2006.04779
[63] Laroche, Trichelair & Tachet des Combes. Safe Policy Improvement with Baseline Bootstrapping (ICML 2019). https://arxiv.org/abs/1712.06924
[64] Jin, Yang & Wang. Is Pessimism Provably Efficient for Offline RL? https://arxiv.org/abs/2012.15085
[65] Fujimoto & Gu. A Minimalist Approach to Offline Reinforcement Learning (TD3+BC, NeurIPS 2021 Spotlight). https://arxiv.org/abs/2106.06860
[66] Schmidt, Schneider & Hennig. Descending through a Crowded Valley — Benchmarking Deep Learning Optimizers (ICML 2021, PMLR 139). https://arxiv.org/abs/2007.01547
[67] Choi, Shallue, Nado, Lee, Maddison & Dahl. On Empirical Comparisons of Optimizers for Deep Learning (2019; venue unverified). https://arxiv.org/abs/1910.05446
[68] AAAI-27 Main Technical Track Call for Papers. https://aaai.org/conference/aaai/aaai-27/main-technical-track-call/
[69] NeurIPS Evaluations and Datasets 2026 Reviewing Guidelines. https://neurips.cc/Conferences/2026/EvaluationsDatasetsReviewerGuidelines
[70] Stanton, Maddox & Wilson. Bayesian Optimization with Conformal Prediction Sets. https://arxiv.org/abs/2210.12496
[71] Tibshirani, Barber, Candès & Ramdas. Conformal Prediction Under Covariate Shift (NeurIPS 2019). https://arxiv.org/abs/1904.06019
[72] Rafailov, Chittepu, Park, Sikchi, Hejna, Knox, Finn & Niekum. Scaling Laws for Reward Model Overoptimization in Direct Alignment Algorithms. https://arxiv.org/abs/2406.02900
