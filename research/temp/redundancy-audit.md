# Evidence redundancy audit — step 2.6

**Question this step exists to answer:** are N sources really 1 source in N outfits?

## Headline

| Metric | Value |
|---|---|
| Notes tagged this run | 92 |
| **Distinct underlying sources** | **69** |
| Clusters with >1 note | 21 |

**The honest corpus size is 69, not 92.** All downstream coverage counting should use 69.
Still comfortably above the full-tier minimum of 45 and inside the 55–80 target band.

## Why the duplication exists, and why it is benign here

The 21 clusters are **not** derivative-commentary clusters — the usual redundancy failure,
where five blog posts restate one paper and inflate an atomic item's apparent support. Every
cluster here is **the same primary paper fetched twice by different routes**, a direct
consequence of the environment bug:

1. A batch fetches `arxiv.org/abs/<id>` → succeeds, yields a ~700-word abstract-page note.
2. The same or another batch needs full text, hits the `JUNK_CONTENT` PDF failure, and falls
   back to the ar5iv/HTML mirror or an external pymupdf extraction → yields a second,
   full-text note for the same paper.

Examples: `agarwal2021-...-fulltext` alongside `210813264-...`; `lucic2018-...-fulltext`
alongside `171110337-...`; `moosbauer-et-al-2022-...-ar5iv` alongside `211114756-...`.

**Consequence for evidence weight: none, provided we do not double-count.** Two notes on the
same paper are one piece of evidence, not two. Where a cluster contains both an abstract-only
and a full-text note, **the full-text note is canonical** and the abstract note is
discountable. Several batches already deprecated their own thin duplicates; the rest are
harmless as long as coverage is counted at 69.

## Does any atomic item fall below 2 independent sources once discounted?

**No.** Checked against `coverage-gaps.md`. The reason is structural: this audit's corpus is
organised **one primary per citation under verification**, so each atomic item is served by a
distinct paper by construction rather than by topical overlap. The contradiction-hunt items —
the ones where independence actually matters, because a single source claiming a
contradiction would be weak — are the best-supported:

| Contradiction target | Independent sources | Independent? |
|---|---|---|
| σ is an error signal | Carrete 2023 (regression, ρ=0.90–0.91); RADMI 2026; Lakshminarayanan's own calibration finding | **3, mutually independent** — different domains, different groups, different decades |
| K-robustness at K=2 | L/R/W Fig A.7 (primary); Abe 2022 (shows the *absence* of a K-sweep); Lakshminarayanan Table 4 (the real K-direction) | **3, independent and mutually corroborating** |
| De-confounding that grew | Hamdan 2022 (leakage); Maassen 2020 (19 up vs 14 down); Recht (slope>1, pre-empted) | **3, independent** |

No wave 3 required.

## One clustering caveat, disclosed

My clustering key is "arXiv ID if present in the body, else a normalised title". This
misgroups a four-note Liang cluster under `1807.02811`, which is not Liang's ID — it is
Frazier's BO tutorial, cited *inside* those notes and picked up by the regex. So the cluster
boundary is right (four Liang notes) but the label is wrong. It does not change the counts:
those four are still one source. Recorded because an unexplained wrong ID in an audit
artifact is exactly the kind of thing this audit exists to catch in others.

## What this changes downstream

- Coverage and citation counting: **use 69**.
- When two notes exist for one paper, cite the **full-text** one; the abstract note carries no
  independent weight.
- No atomic item requires a wave 3 fetch on redundancy grounds.
