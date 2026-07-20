# Coverage check — step 2.5

Corpus: **92 non-deprecated notes**, 67 claims files, tagged
`mbo-gauntlet-r4-adversarial-0f06f1`. Full-tier minimum is 45; target 55–80. We are above
target, which is acceptable here because the query demands *per-citation* primary
verification across a 67-entry bibliography rather than topical coverage.

Coverage classes: **Well-covered** (4+), **Adequate** (2–3), **Thin** (1), **Uncovered** (0).

## Deliverable N6 — the existential axis

| Atomic item | Sources | Status |
|---|---|---|
| Exact crossed factorial in offline MBO | 8× 2026 frontier + Design-Bench, RaM, SOO-Bench, COMs, RoMA | **Well-covered** |
| Published since last audit (2026) | 8 papers Jan–Jun 2026, all full-text grepped | **Well-covered** |
| Hutter near-miss re-confirm + extension | Hutter full PDF (47,266 w) + 62 forward citers | **Well-covered** |
| Liang near-miss re-confirm + extension | Liang full text (10,591 w) + 166 forward citers | **Well-covered** |
| Moosbauer near-miss re-confirm + extension | Moosbauer ar5iv (19,701 w) + 4 forward citers + Bischl survey | **Well-covered** |
| Adjacent fields (AutoML, HPO, surrogate-EA) | EXPObench, Bischl 2023, PED-ANOVA, van Rijn & Hutter, CART-ANOVA, ISA | **Well-covered** |
| Wider "offline black-box optimization" reading | SOO-Bench, SPADE, OptBias, DiBO, dLLM | **Well-covered** |

## Deliverable (i) — citation verification

| Citation | Sources | Status |
|---|---|---|
| `liu2020sngp` | SNGP full text + DUQ + Lakshminarayanan + Ovadia + Fort | **Well-covered** |
| `fan2024minucb` | Fan full text (1,550 lines) + GIBO + TuRBO + Wu et al. | **Well-covered** |
| `shahriari2016humanoutoftheloop` | Full PDF, 137,300 chars | **Adequate** (single source, but it *is* the primary) |
| `li2024bnnsurrogates` | Full text 16,554 w + rendered Fig A.7 page | **Well-covered** |
| `kim2025mbosurvey` | Full text + independent TMLR venue corroboration | **Adequate** |
| `agarwal2021precipice` | Full text 16,257 w | **Adequate** |
| `demsar2006statistical` | Full 30-page PDF + Benavoli rebuttal | **Adequate** |
| `melis2018sota` | Full text + Ferrari Dacrema + Musgrave + Lucic | **Well-covered** |
| `chemingui2024pggs` | Full text 13,841 w | **Adequate** |
| `benavoli2016meanranks` | JMLR + arXiv preprint (trap confirmed both sides) | **Adequate** |
| `henderson2018matters` | Full text + PDF copyright line | **Adequate** |
| `recht2019imagenet` | Full text, both slope figures verbatim | **Adequate** |
| `abe2022ensembles` | Full text 15,095 w + Lakshminarayanan Table 4 | **Adequate** |
| `hutter2014fanova` / `liang2021benchmarking` / `moosbauer2022benchmarkdriven` | see N6 block | **Well-covered** |
| `tibshirani2019conformal` (supplement proof) | **in flight (B10)** | **PENDING** |
| `dewolf2022intervals` | — | **UNCOVERED** — see gaps |
| `ghasemipour2022pessimistic` | — | **UNCOVERED** — see gaps |
| `vanamersfoort2020duq` | DUQ full text | **Adequate** |

## Deliverable (i) — contradiction hunt

| Target | Sources | Status |
|---|---|---|
| σ IS an error signal? | Carrete 2023 (ρ=0.90–0.91, regression) + RADMI + Lakshminarayanan calibration caveat | **Well-covered — CONTRADICTION FOUND** |
| K-robustness down to K=2? | L/R/W Fig A.7 (K={2,5,10}) + Abe + Lakshminarayanan Table 4 | **Well-covered — CONTRADICTION FOUND** |
| De-confounding audit whose effect GREW? | Confound-leakage (Hamdan 2022) + Maassen 2020 + Recht + 4 genre audits | **Well-covered** |
| Frozen/optimizer-invariant cells on Design-Bench? | Design-Bench, SOO-Bench, RaM, COMs, RoMA | **Adequate** — no prior report found |

## Deliverable (iii) — the stronger paper

| Target | Sources | Status |
|---|---|---|
| Under-stated: budget axis | COCO/BBOB + Lucic + Kazikova 2021 + Melis | **Well-covered** |
| Under-stated: two-strengthenings | Maassen + Hamdan + Bressan-class suppression | **Adequate** |
| Under-executed: elimination → mechanism | Xu 2021, Dao 2024, Gao, CQL, Manheim, DKL/DUE, BCQ (8 primaries) | **Well-covered** |
| Under-explained: inversion framing | **in flight (B10)** — safe policy improvement, elitism | **PENDING** |
| Under-explained: LCB paralysis / frozen cells | TuRBO, GIBO, Wu et al. local-BO convergence | **Adequate** |
| Unexplored: optimizability vs accuracy | Dao 2024 sensitivity, RaM (MSE↔ranking correlation), Xu 2021 | **Adequate** |
| η² as an effect size at small n | JOSS effectsize + Kelley/Olejnik-Algina (secondhand) + Benavoli power | **Adequate** |

## Genuine gaps after wave 1

**No atomic item is at zero except these three. Two are minor; one is recorded honestly.**

1. **`dewolf2022intervals` — UNCOVERED.** Cited in Confound 4 for "the general principle that
   a fixed multiplier on an uncalibrated interval is not comparable across model classes is
   owned by the interval-validity literature". Not verified. **Wave 2 target.**
2. **`ghasemipour2022pessimistic` — UNCOVERED.** Cited alongside it as "its offline-RL
   instance". Not verified. **Wave 2 target.** Both are low-severity: they support a claim the
   paper has already *narrowed* (Confound 4's aggregate kill fired), so a miscitation here
   affects a withdrawn claim. Still worth checking.
3. **Kelley (1935) and Olejnik & Algina (2003) — verified only secondhand.** Both are
   paywalled (APA/JMLR/ResearchGate/academia.edu all blocked). The η²-bias claim rests on the
   JOSS `effectsize` documentation quoting them verbatim, plus my own direct computation from
   the paper's bootstrap artifacts. **The empirical half is first-hand and decisive; the
   citation half is secondhand.** Recorded for "What I could not verify and why."

## Items pending in-flight batches

- **B10** — the conformal proof condition check (`tibshirani2019conformal`), the inversion
  framing (safe policy improvement / elitism), and pessimism-decomposition precedent.
- **B11** — `lu2022revisiting` (N6 risk surface in the paper's own uncited bibliography),
  `gao2022reward` venue/year, TuRBO attribution, `fannjiang2020autofocused`.

**Wave 2 is warranted and small:** two uncovered citations (`dewolf2022intervals`,
`ghasemipour2022pessimistic`) plus a TOST/equivalence-testing thread that returned nothing
on-topic in wave 1. Dispatch after B10/B11 land, so wave 2 can also fill anything they miss.

## Method limitations affecting coverage

- **Semantic Scholar returned HTTP 429 for the entire session**, across every batch and every
  retry schedule. arXiv and OpenAlex carried all citation-chaining. The N6 forward-citation
  walks ran on OpenAlex.
- **`hyperresearch fetch` cannot ingest PDFs in this environment** (systemic false-positive
  `JUNK_CONTENT`). All full-text verification ran via `curl` + pymupdf/pdftotext outside the
  vault, or via arXiv/ar5iv HTML mirrors. Verdicts rest on primary full text; the full text is
  mostly not stored in the notes.
- **Two homonym traps caught**, both of which would have produced false KILLs on a naive grep:
  Liang's 14 `crossed` hits are the *Crossed barrel dataset*; four papers' `anova` hits are the
  surnames *Usmanova* / *Bozhanova*. Recorded because they justify the fetch-and-read
  constraint.
