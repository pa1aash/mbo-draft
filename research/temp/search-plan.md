# Search plan — mbo-gauntlet-r4-adversarial-0f06f1

Four lenses. Lens D is repurposed here: this query has no fiscal filings, but it has
**venue-year-pinned primary records** (three confirmed traps), which are the exact analogue —
the authoritative record for a named period that a snippet will misreport. Treated as
mandatory.

Academic APIs (Semantic Scholar / arXiv / OpenAlex) run BEFORE web search on every row.

---

## P0 — N6: the crossed surrogate × optimizer factorial (EXISTENTIAL)

The residual has four conjuncts: **crossed** (both axes manipulated) × **surrogate class**
× **optimizer/search** × **two-way variance decomposition**, in **offline** MBO. A kill needs
all four. Searches are deliberately run at several scope widths so a kill cannot hide in the
gap between "offline MBO" and the wider "offline black-box optimization" reading.

| Atomic item | Search query | Type | Lens | Target |
|---|---|---|---|---|
| Sub-Q1 exact | `factorial design surrogate optimizer offline model-based optimization` | academic | breadth | the exact thing |
| Sub-Q1 exact | `crossed surrogate acquisition ANOVA black-box optimization` | academic | breadth | the exact thing |
| Sub-Q1 exact | `variance decomposition surrogate optimizer contribution optimization` | academic | depth | canonical |
| Sub-Q1 exact | `disentangle surrogate model optimizer contribution performance` | academic | breadth | the exact thing |
| Sub-Q1 exact | `eta squared main effect surrogate optimizer benchmark` | academic | depth | the exact thing |
| Sub-Q1 wider | `offline black-box optimization surrogate search strategy factorial` | academic | breadth | wider reading |
| Sub-Q1 wider | `two-way ANOVA benchmark machine learning components attribution` | academic | depth | wider reading |
| Sub-Q1 wider | `ablation which component matters surrogate acquisition optimizer` | academic | breadth | wider reading |
| Sub-Q2 recency | `offline model-based optimization 2026` | academic | breadth | since-last-audit |
| Sub-Q2 recency | `offline MBO benchmark evaluation 2026 attribution` | academic | breadth | since-last-audit |
| Sub-Q2 recency | arXiv listing sweep `cs.LG` 2026 offline model-based optimization | academic | breadth | since-last-audit |
| Sub-Q2 recency | `design-bench revisited reproducibility 2026` | academic | adversarial | since-last-audit |
| Sub-Q2 recency | forward-citation walk on Kim survey (who cites it in 2026) | academic | depth | since-last-audit |
| Sub-Q2 recency | forward-citation walk on Design-Bench (2026 citers only) | academic | depth | since-last-audit |
| Sub-Q3 Hutter | `fANOVA hyperparameter importance model class` + full-text grep `two-way`/`crossed` | academic | depth | near-miss re-confirm |
| Sub-Q3 Hutter | forward-citation walk on Hutter 2014 → any two-way extension | academic | depth | near-miss extension |
| Sub-Q4 Liang | `Liang benchmarking surrogate acquisition materials Bayesian optimization` + grep `ANOVA` | academic | depth | near-miss re-confirm |
| Sub-Q4 Liang | forward-citation walk on Liang 2021 → any variance-decomposition successor | academic | depth | near-miss extension |
| Sub-Q5 Moosbauer | `Moosbauer benchmark-driven HPO surrogate sampling strategy` + grep `fANOVA`/`OFAT` | academic | depth | near-miss re-confirm |
| Sub-Q5 Moosbauer | forward-citation walk on Moosbauer 2022 → did anyone run the declined analysis | academic | depth | near-miss extension |
| Sub-Q1/2 | `van Rijn Hutter hyperparameter importance across datasets` | academic | depth | fANOVA lineage |
| Sub-Q1/2 | `HPO benchmark component ablation interaction effects` | academic | adversarial | lineage sweep |
| Sub-Q1 | `surrogate assisted evolutionary algorithm factorial comparison` | academic | breadth | adjacent field |
| Sub-Q1 | `AutoML component importance analysis of variance` | academic | breadth | adjacent field |
| Sub-Q1 | `algorithm configuration ablation analysis Fawcett Hoos` | academic | depth | adjacent field |

**Adjacent-field rows are deliberate.** The most dangerous kill is not in offline MBO — it is
a surrogate-assisted-EA or AutoML paper that ran the crossed factorial without using the
offline-MBO vocabulary. N6's phrasing would not surface it; these rows are the hedge.

## P1 — load-bearing citation verification

Each row is fetch-primary-and-grep. A snippet is never sufficient.

| Atomic item | Search query | Type | Lens | Target |
|---|---|---|---|---|
| liu2020sngp | fetch arXiv:2006.10108 full text; grep `distance`, `distance-aware`, `feature space` | academic | depth | primary |
| fan2024minucb | fetch primary; grep `local search`, `UCB`, `minimalist`, `converge` | academic | depth | primary |
| shahriari2016humanoutoftheloop | fetch Proc IEEE 2016; grep `model matters`, `acquisition`, `choice of` | academic | depth | primary |
| li2024bnnsurrogates | fetch arXiv:2305.20028; grep `acquisition`, `offline`, `ensemble size`, `robust`; **confirm ICLR 2024** | academic | depth | primary + year trap |
| kim2025mbosurvey | fetch arXiv:2503.17286; grep the exact quoted sentence; **confirm TMLR 2026 vs bib key 2025** | academic | depth | primary + year trap |
| agarwal2021precipice | fetch NeurIPS 2021; grep `equivalence`, `failure to reject`, `power` | academic | depth | primary |
| demsar2006statistical | fetch JMLR 2006; grep `ten data sets`, `Friedman`, `recommend` | academic | depth | primary |
| melis2018sota | fetch ICLR 2018; grep for whether it establishes audits-SHRINK as a general pattern | academic | depth | **premise check** |
| chemingui2024pggs | fetch primary; grep the "fixed search strategies" local premise verbatim | academic | depth | primary |
| recht2019imagenet | fetch ICML 2019; grep `slope`, `1.69`, `1.11` | academic | depth | primary |
| benavoli2016meanranks | fetch JMLR; grep `mean rank`, `pool`; **confirm JMLR 2016** | academic | depth | primary + year trap |
| henderson2018matters | confirm **AAAI 2018** not 2017 | academic | depth | year trap |
| abe2022ensembles | fetch primary; grep direction of quality vs ensemble count | academic | depth | primary |
| dewolf2022intervals | fetch primary; grep interval-validity across model classes | academic | depth | primary |
| hutter2014fanova | fetch ICML 2014; grep `model class`, `31`, `58`, `one-way` | academic | depth | primary |
| moosbauer2022benchmarkdriven | fetch primary; grep the fANOVA-decline sentence verbatim | academic | depth | primary |
| liang2021benchmarking | fetch npj Comput Mater 2021; grep `ANOVA`, `factorial`, `LCB` | academic | depth | primary |
| bib integrity | resolve all 67 `references.bib` keys; find orphan/unused/undefined `\citep` | local | breadth | integrity |

## P2 — contradiction hunt (deliverable i, second half)

| Atomic item | Search query | Type | Lens | Target |
|---|---|---|---|---|
| σ = error signal? | `deep ensemble variance predicts error correlation regression` | academic | adversarial | **contradiction** |
| σ = error signal? | `ensemble disagreement error correlation uncertainty quality` | academic | adversarial | **contradiction** |
| σ = error signal? | `criticism of deep ensembles uncertainty not calibrated error` | academic | adversarial | contrarian |
| σ = distance? | `distance aware uncertainty neural network feature space` | academic | depth | supports paper |
| K down to 2 | `ensemble size ablation two members Bayesian optimization` | academic | adversarial | **contradiction** |
| K down to 2 | `small ensemble size robustness performance number of members` | academic | adversarial | **contradiction** |
| K down to 2 | `how many ensemble members are enough uncertainty` | academic | adversarial | contrarian |
| audits grow? | `reanalysis effect size larger than originally reported machine learning` | academic | adversarial | **kills N9** |
| audits grow? | `replication effect size increased correction confound suppression` | academic | adversarial | **kills N9** |
| audits grow? | `suppressor variable confound removal increases effect` | academic | depth | statistics |
| frozen cells | `optimizer invariant surrogate frozen Design-Bench degenerate` | academic | adversarial | **contradiction** |
| frozen cells | `Design-Bench criticism flawed benchmark normalization` | academic | adversarial | contrarian |
| LCB paralysis | `acquisition function local optimum stuck at data no exploration` | academic | depth | supports paper |
| general | `criticism of offline model-based optimization benchmarks` | web | adversarial | contrarian |
| general | `limitations Gaussian process advantage neural ensemble comparison` | academic | adversarial | contrarian |

**≥5 adversarial searches:** satisfied many times over — the contradiction hunt is
adversarial by construction, and P0 carries its own adversarial rows.

## P3 — the stronger paper (deliverable iii)

| Atomic item | Search query | Type | Lens | Target |
|---|---|---|---|---|
| under-stated: budget | `search budget confound benchmark comparison compute matched` | academic | depth | framing |
| under-stated: budget | `compute matched comparison optimization algorithms fair` | academic | depth | framing |
| under-stated: two-strength | `confound removal strengthens effect audit direction` | academic | depth | framing |
| under-executed | `positive control mechanism experiment surrogate optimization` | academic | depth | **name the experiment** |
| under-executed | `intervention experiment identify cause performance gap model class` | academic | depth | **name the experiment** |
| under-executed | `kernel interpolation neural network surrogate hybrid controlled` | academic | depth | **name the experiment** |
| under-executed | `posterior mean swap ablation surrogate transplant` | academic | depth | **name the experiment** |
| under-explained | `adversarial example surrogate optimization exploits model error` | academic | depth | sharper frame |
| under-explained | `reward hacking overoptimization proxy objective Goodhart` | academic | depth | sharper frame |
| under-explained | `optimizer exploits surrogate error offline RL extrapolation` | academic | depth | sharper frame |
| unexplored | `what makes a surrogate optimizable rather than accurate` | academic | breadth | **unexplored** |
| unexplored | `optimizability vs accuracy surrogate model selection` | academic | breadth | **unexplored** |

---

## Search gap check against `research/temp/coverage-matrix.md`

Walked all 58 coverage-matrix rows. Every row's atomic item has ≥1 targeting search above.
Gaps found and closed during this check:

1. **"offline black-box optimization" (the wider N6 reading)** initially had no rows of its
   own — every P0 row said "offline MBO". Added four wider-reading rows. Without them a kill
   phrased in the wider vocabulary would have been invisible.
2. **The three near-misses had re-confirm rows but no *extension* rows.** The query asks two
   things: still-only-near-miss, AND not-extended. Added a forward-citation walk per
   near-miss.
3. **Adjacent fields (surrogate-assisted EA, AutoML, algorithm configuration) had no rows.**
   The most dangerous N6 kill is a paper that ran the factorial without offline-MBO
   vocabulary. Added four rows.
4. **`melis2018sota` was listed only as a citation to verify, not as a premise to test.**
   It is load-bearing for the paper's headline direction claim ("audits normally shrink").
   Promoted to a premise check and given its own P2 contradiction rows.
5. **"Unexplored" had no search rows** (it was the category dropped in step 1). Added the
   optimizability-vs-accuracy rows.

**Remaining `Gap? = YES`: none.**

Planned searches: ~70 across four lenses.
