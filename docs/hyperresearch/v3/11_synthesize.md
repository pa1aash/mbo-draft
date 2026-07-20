# Step 11 — Synthesis

Run `mbo-gauntlet-r4-adversarial-0f06f1` · branch `gauntlet-r4` · 2026-07-20

## Output

`research/notes/final_report_mbo-gauntlet-r4-adversarial-0f06f1.md` — **14,156 body words +
1,551 Sources = 15,707 total**, 108,885 chars, 490 lines.

## Verification gate — every check run, every check passed

| Check | Result |
|---|---|
| Five `required_section_headings` verbatim, in order, + `## Sources` | ✓ |
| Citation integrity | **90 cited / 90 listed, zero orphans, zero gaps** |
| YAML frontmatter | absent |
| Pipeline vocabulary leaks | **0** |
| AI / agent / co-authored strings | **0** (4 regex hits are "language model" inside paper titles) |
| Pass 2 shorter than pass 1 | ✓ (no growth) |
| No content duplication | ✓ (checked for repeated H2s and repeated long lines) |

## The six qualification checks — the ones that actually mattered

I predicted before spawning that the synthesizer's most likely failure was **cutting the
qualifications**, because compression pressure trims exactly the sentences that make findings
smaller and more accurate. All six survived:

| # | Qualification | Status |
|---|---|---|
| 1 | Conformal item = **scoping omission**, not a missing hypothesis, ranked below Demšar and Fan | PASS |
| 2 | RaM characterisation = **incomplete**, not false | PASS |
| 3 | 7/7 attenuation carries the **Styblinski floor-effect confound** | PASS |
| 4 | Griewank named as the **smallest** normalization lever | PASS |
| 5 | **Yarotsky (2013)** credited as closest prior art for acquisition-stalling | PASS |
| 6 | Dao and Ghasemipour marked **venue unverified**, inline and in Sources | PASS |

Plus: the severity split (HIGH to reader trust / NIL to results) is stated and never averaged;
the passing citations are reported in a dedicated table including **Shahriari being
under-cited**; and the terminal section carries the audit's own two caught fabrications, five
self-corrections and the unaudited-bootstrap assumption.

## Two things I checked that the synthesizer did not flag

**A venue assertion it introduced.** Source [6] claims "DiBO, ICML 2026 Spotlight". Nobody in
the audit had verified that. I checked arXiv directly: the comment field reads *"Accepted at
ICML 2026 as a Spotlight Paper (top 2.2% of submissions)."* **Verified.** Worth doing — the
report asserts ~20 venues and every one is a place it could have repeated the exact error it
documents.

**Its own metrics are wrong by ~2×.** The synthesizer reported "~7,900 words / ~57,500
characters, inside the 7,000–8,000 target." The file is **14,156 body words / 108,885
characters**. There is no duplication — I checked — so this is a self-measurement error, not a
content defect.

**Recorded rather than quietly corrected**, because it is the same failure this audit spent
fifty commits documenting: **an unverified self-report accepted at face value.** The report is
~1.8× its target. The pipeline's sanity threshold is 3×, so it passes, and the query said *"Do
not abbreviate"* — but the honest statement is that the length target was missed and the
synthesizer did not know it.

## Length judgment

Accepted. Draft A made the argument independently and it holds: the deliverable structure —
twelve-plus mandatory items each carrying four required fields, seventeen ranked items each
carrying a tag, the N6 verdict with its verbatim queries, and a mandatory terminal section — has
an irreducible size. Further compression would amputate findings rather than prose, and the
findings are what was asked for.

## Next

Step 12 — four adversarial critics, briefed to attack the orchestrator's positions rather than
only the draft.
