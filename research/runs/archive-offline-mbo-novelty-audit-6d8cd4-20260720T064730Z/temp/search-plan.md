# Step 2 — Multi-perspective search plan (offline-mbo-novelty-audit-6d8cd4)

This is a **targeted prior-art audit**, not an open topic sweep. The corpus is a mostly-
enumerable set of named papers (each claim names its nearest-neighbor prior art) PLUS
adversarial nearest-neighbor searches to catch an *unknown* paper that already owns a claim.

## Lens A — Breadth coverage (the named papers, per claim)
| Atomic item | Target paper(s) | Type | Lens | Status |
|---|---|---|---|---|
| N1 reality-check shape | Ferrari Dacrema RecSys2019; Balduzzi NeurIPS2018; Henderson AAAI2018; Musgrave ECCV2020; Lucic NeurIPS2018; Agarwal NeurIPS2021 | academic | breadth | 6/6 cached |
| N2 K-contingency | Abe NeurIPS2022; Lakshminarayanan NeurIPS2017 | academic | breadth | 2/2 cached |
| N4 distance-aware uncertainty | Liu SNGP NeurIPS2020; van Amersfoort DUQ ICML2020; van Amersfoort DUE 2021; Eriksson TuRBO NeurIPS2019 | academic | breadth | 4/4 cached |
| N5 NTK / spectral bias | Jacot NeurIPS2018; Rahaman ICML2019; Lee ICLR2018; Li/Rudner/Wilson ICLR2024 | academic | breadth | 4/4 cached |
| N6 offline-MBO factorial | Trabucco Design-Bench ICML2022; Chemingui AAAI2024; Tan ICLR2025; Kim survey 2025 | academic | breadth | 3/4 cached (Kim → web) |
| N7 smoothness manipulation | IGNITE NeurIPS2024; MS-DDEO SWEVO2022 | academic | breadth | 0/2 → web |
| N8 platform/version dependence | Gundersen & Kjensmo AAAI2018 | academic | breadth | metadata only → web |
| N9 audit that strengthens | Recht ImageNet ICML2019; Melis LSTM ICLR2018 | academic | breadth | 2/2 cached |
| Venue fit | AAAI-27 areas-and-topics page | web | breadth | → web (fetch, don't recall) |

## Lens B — Citation-chain depth (canonical/upstream)
- N5: chase NTK→GP equivalence chain (Neal 1996 / Lee 2018 / Matthews infinite-width) inside the cached PDFs.
- N4: chase "deep ensembles confidently wrong far from data" upstream (Ovadia 2019 / Nalisnick / D'Angelo) — surface from SNGP + Abe reference lists.
- N6: chase Design-Bench → COMs/grad-ascent baseline lineage; check whether any cited work crosses surrogate × optimizer.

## Lens C — Adversarial / contrarian (nearest-neighbor MISS-catchers)
At least 5 adversarial searches — each targets a paper that could already OWN a claim:
1. N2: "ensemble size dependence surrogate ranking Bayesian optimization" / "number of ensemble members model comparison" (does K flip a *ranking*, not just accuracy?)
2. N3: "matched acquisition function pessimism surrogate comparison" / "beta calibration LCB different surrogates" / "conservatism offline model-based optimization unfair comparison"
3. N6: "factorial ANOVA surrogate optimizer", "decompose surrogate versus acquisition", "which component matters black-box optimization", "ablation surrogate optimizer offline optimization"
4. N7: forward-citations of IGNITE / MS-DDEO 2025-2026 for bidirectional smoothness manipulation
5. N8: "platform dependence deep learning benchmark", "library version reproducibility numerical determinism GPU", "RNG portability results"
6. N9: "reproducibility study effect size increased", "reanalysis strengthened finding", "audit larger effect" (adversarial — precedent for de-confounding that grows the effect)
7. N1 residual: "reality check offline model-based optimization", "are we making progress black-box optimization" (does the reality-check genre already exist IN offline MBO?)

## Lens D — Period-pinned primary sources
- AAAI-27 areas-and-topics page — MUST be fetched live (query time_periods entry), not recalled.

## Search-gap check vs coverage-matrix
Every coverage-matrix row maps to ≥1 plan row. The nine claims + venue fit + the two synthesis
deliverables are all covered. No query phrase left with zero plan rows.
