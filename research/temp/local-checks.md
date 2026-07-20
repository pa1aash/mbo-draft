# Local checks — done by the orchestrator without the literature

These need no external source. They are claims-about-the-paper that the paper itself
settles, so they belong in deliverable (i) as internal-consistency items even though no
citation is miscited.

## L1 — Bibliography integrity

Script: regex over `\cite[tp]?` in `main.tex` + `supplement.tex` against `@type{key,` in
`references.bib`.

| Metric | Value |
|---|---|
| Bib entries | 67 |
| Distinct keys cited | 41 |
| **Undefined (cited, not in bib)** | **0** — clean |
| Unused (in bib, never cited) | 26 |

**Undefined = 0 is a genuine pass.** No dangling `\citep`. That is worth stating plainly
because it is the failure mode that most often survives to camera-ready.

The 26 unused entries are mostly harmless offline-RL background (IQL, CQL variants, MOPO,
MOReL, Decision Transformer, Diffuser). Four are not harmless:

### L1a — `lu2022revisiting` is uncited and is an N6 risk surface
Lu, Ball, Parker-Holder, Roberts, "Revisiting Design Choices in Offline Model-Based
Reinforcement Learning", ICLR 2022. A *revisiting-design-choices* paper in offline
*model-based* RL is the closest genre to a crossed decomposition in the closest sibling
field, and it sits in the paper's own bib unengaged. Dispatched for full-text check.
**If it crosses model class against policy-optimization with a decomposition, N6's scoping
needs to address it explicitly** — even if offline model-based RL is formally out of scope,
a reviewer who sees it in the bib and not in the text will ask why.

### L1b — `gao2022reward` is uncited, and carries a year defect
Key says `2022`; the entry's own `year` field says `2023` (ICML, PMLR 10909-10934). The key
and the field disagree inside a single entry. Independently of the year, this is the
sharpest available reframing of the paper's seventh elimination — a functional form for how
true value degrades as a learned proxy is optimized away from the data — and the paper has
it in the bibliography without citing it.

### L1c — `eriksson2019turbo` (TuRBO) is uncited
The paper credits Fan et al. 2024 with "the reading of a UCB-style acquisition as local
search". TuRBO, the canonical local-BO paper, is in the bib and uncited. Attribution
question dispatched.

### L1d — `fannjiang2020autofocused` is uncited
Autofocused Oracles is offline design's own paper on the surrogate being exploited as the
design distribution shifts — the paper's core diagnosis. Uncited.

**Pattern worth stating in the report:** the paper's bibliography contains at least three
papers that would *strengthen* it, uncited. That is the opposite of the usual bibliography
defect and is a cheap fix.

## L2 — Internal arithmetic consistency

Checked every derived figure I could recompute from the paper's own reported numbers.

### Confirmed consistent
| Claim | Check | Result |
|---|---|---|
| `5,040 optima = 7 tasks x 24 arms x 30 seeds` | 7x24x30 | **5,040** ✓ |
| `168 cells, 30 seeds` (elimination 7) | 7x24 | **168** ✓ consistent with above |
| `all 63 cells` (fig:x0) | 7x9 | **63** ✓ |
| `none of the 252 cells` (DB budget match) | 7x9x4 corners | **252** ✓ |
| `61%` of GP advantage survives at beta=0 | 0.319/0.525 | 0.6076 → **61%** ✓ |
| `99.1%` retained across width sweep | 0.476/0.480 | 0.9917 → **99.1%** ✓ |
| `11.8x` budget spread | 51,456/4,352 | 11.82 ✓ |
| K peaks at K=5 | max(0.326,0.366,0.408,0.389) | 0.408 at K=5 ✓ |
| budget intervals disjoint | 0.355 < 0.421 | ✓ genuinely disjoint |
| `10.7x` width sweep | 1024/96 | 10.67 ✓ |

### Discrepancies to resolve — candidate deliverable (i) items

**L2a — the pessimism increment does not equal the difference of the marginals.**
The paper reports the beta=0 gap as `0.319` and the beta=2 gap as `0.525`. Difference =
**0.206**. The paper reports the paired increment as **`0.203` [0.007,0.396], p=0.020**.
A paired per-task increment need not equal the difference of two pooled marginals, so this
may be entirely legitimate — but the paper presents the three numbers in one breath without
noting they are computed differently. **Fix: either reconcile, or state in one clause that
the increment is paired per-task and therefore not the difference of the two marginals.**
Low severity, but it is exactly the arithmetic a hostile reviewer subtracts in the margin.

**L2b — the width shrinkage does not equal the difference of the endpoints.**
Reported: `0.480` at w=96 against `0.476` at w=1024, difference **0.004**; but shrinkage is
reported as **`-0.006` [-0.210,0.161]**. Same class of issue — plausibly a bootstrap point
estimate over per-task pairs rather than the difference of two rounded marginals, but
unexplained on the page. **Fix: same one-clause reconciliation.**

**L2c — beta=2 gives 0.406 in the beta sweep but 0.405 in the corner table.**
The beta sweep reports `0.406 [0.285,0.564]` at beta=2. The corner table's on/on cell — the
audited engine, which is also beta=2 — reports `0.405 [0.290,0.556]`. These should be the
same quantity on the same engine. The gap is within rounding, but the two numbers appear in
the same paper as the headline (0.405) and the beta-axis endpoint (0.406), and the abstract
uses both. **Fix: confirm they are the same run and unify, or state why they differ.**
This one matters more than L2a/L2b because 0.405 is the paper's headline scalar.

**L2d — `630` cells in the synthetic budget-matched arm.**
7 tasks x 9 cells = 63, so 630 implies 10 seeds, not the 30 used elsewhere. The supplement
says "Seeds: 30 synthetic, 16 Design-Bench, 10 for the beta/K/calibration sweeps." So 10
seeds is consistent with the sweep convention — but the budget-matched arm is presented in
the body as a main result, not a sweep. **Fix: state the seed count for the budget-matched
arm where it is reported, since it differs from the 30 the reader has been given.**

## L3 — Citation-year and venue defects visible without fetching

**L3a — `kim2025mbosurvey` key/prose mismatch.** The bib entry is
`@article{kim2025mbosurvey, ..., journal={arXiv preprint arXiv:2503.17286}, year={2025}}`.
The paper's prose calls it "the subfield's **2026** survey" — twice, and the second
contribution's framing leans on its recency. The prior audit records it as TMLR 2026
camera-ready. **Fix: if it is TMLR 2026, the bib entry must become an `@article` with the
TMLR journal and year 2026; if it is still a preprint, the prose must stop calling it a 2026
survey.** As written the paper contradicts itself between prose and bibliography. Dispatched
for venue confirmation.

**L3b — `gao2022reward` key/field mismatch.** See L1b. Key `2022`, field `2023`.

Both are the class of defect this project has caught before. Neither required a fetch.
