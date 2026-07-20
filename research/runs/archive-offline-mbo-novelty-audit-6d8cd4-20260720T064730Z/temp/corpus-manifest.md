# Corpus manifest — offline-mbo-novelty-audit-6d8cd4

## Locally cached full-text (20 papers, all TITLE_OK verified)
Path: `research/raw/txt/<slug>.txt` (body) · `research/raw/pdf/<arxivid>.pdf` (source)

| slug | arXiv | Venue (CORRECTED) | words | claims |
|---|---|---|---|---|
| ferrari-dacrema-recsys2019 | 1907.06902 | RecSys 2019 | 8660 | N1 |
| balduzzi-reeval-neurips2018 | 1806.02643 | NeurIPS 2018 | 10717 | N1 |
| henderson-deeprl-aaai2018 | 1709.06560 | **AAAI 2018** (S2 trap:2017) | 12189 | N1 |
| musgrave-metric-eccv2020 | 2003.08505 | ECCV 2020 | 8420 | N1 |
| lucic-gans-neurips2018 | 1711.10337 | NeurIPS 2018 | 12988 | N1 |
| agarwal-precipice-neurips2021 | 2108.13264 | NeurIPS 2021 | 15696 | N1, N9 |
| abe-ensembles-neurips2022 | 2202.06985 | NeurIPS 2022 | 15305 | N2, N5 |
| lakshminarayanan-ensembles-neurips2017 | 1612.01474 | NeurIPS 2017 | 9291 | N1(iv), N2 |
| jacot-ntk-neurips2018 | 1806.07572 | NeurIPS 2018 | 10803 | N5 |
| rahaman-spectralbias-icml2019 | 1806.08734 | ICML 2019 | 13659 | N5 |
| lee-dnngp-iclr2018 | 1711.00165 | ICLR 2018 | 9189 | N5 |
| li-rudner-wilson-bnn-iclr2024 | 2305.20028 | **ICLR 2024** (S2 trap:2023) | 18095 | N5, N6 |
| liu-sngp-neurips2020 | 2006.10108 | NeurIPS 2020 | 14547 | N4 |
| vanamersfoort-duq-icml2020 | 2003.02037 | ICML 2020 | 8707 | N4 |
| vanamersfoort-due-2021 | 2102.11409 | arXiv 2021 | 9575 | N4 |
| eriksson-turbo-neurips2019 | 1910.01739 | NeurIPS 2019 | 9290 | N4 |
| trabucco-designbench-icml2022 | 2202.08450 | ICML 2022 | 14562 | N6, N8 |
| chemingui-pgs-aaai2024 | 2405.05349 | AAAI 2024 | 9292 | N6 |
| tan-rank-iclr2025 | 2410.11502 | **ICLR 2025** | 18269 | N6 |
| recht-imagenet-icml2019 | 1902.10811 | ICML 2019 | 30154 | N9 |
| melis-lstm-iclr2018 | 1707.05589 | ICLR 2018 | 4806 | N9 |

## Still to fetch (web resolution)
| target | for claim | note |
|---|---|---|
| Kim et al. 2025 offline-MBO survey | N6 | resolve arXiv/venue via WebSearch/OpenAlex |
| IGNITE | N7 | NeurIPS 2024; resolve exact title+ID |
| MS-DDEO | N7 | Swarm & Evol. Comput. 2022; may be paywalled → abstract |
| Gundersen & Kjensmo | N8 | AAAI 2018, doi 10.1609/aaai.v32i1.11503, no arXiv → proceedings body |
| AAAI-27 areas-and-topics | venue fit | fetch LIVE, do not recall |

## Nearest-neighbor adversarial searches (miss-catchers) — W3
N2 ranking-flip-by-K · N3 matched pessimism across surrogates · N6 crossed surrogate×optimizer factorial in offline MBO · N9 reproducibility audit that grows the effect · N1 "reality check" genre already inside offline MBO.
