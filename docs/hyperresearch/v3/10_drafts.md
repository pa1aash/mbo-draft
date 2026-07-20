# Step 10 — Triple-draft ensemble

Run `mbo-gauntlet-r4-adversarial-0f06f1` · branch `gauntlet-r4` · 2026-07-20

**Three drafts spawned in parallel. No single-draft shortcut.**

| Draft | Angle | Words | Chars | `[N]` markers | Headings |
|---|---|---|---|---|---|
| A | **Prosecution** — scholarship is unreliable, fixes are severe | 15,609 | 107,536 | 198 | 5 + Sources ✓ |
| B | **Defence** — steelman the minority view that the audit is cosmetic | 11,131 | 77,889 | 247 | 5 + Sources ✓ |
| C | **Synthesis** — boundary conditions and a priority ordering | 14,948 | 102,855 | 206 | 5 + Sources ✓ |

All three emit the five `required_section_headings` **verbatim and in order**. All well above the
1,000-char floor; all *above* the 5,000–10,000 argumentative target, which step 11's synthesizer
compresses rather than pads.

## Why the angles differ in stance, not shape

The deliverable's structure is fixed by the wrapper contract — five H2 headings, N6 first,
terminal section last. Three drafts with the same headings could easily have become three
paraphrases. Assigning **analytical stance** instead of structure is what forced genuine
divergence: A presses the defects in descending severity, B argues the same facts amount to
little, C prices them.

## Draft B is the one that earns its place

The obvious failure mode for a triple-draft ensemble on an audit is three drafts that all agree
the paper is flawed. B was briefed to defend the minority position seriously — and to **concede
what is true while contesting only the weight**. It held that line: the Demšar fabrication, the
Fan inversion and the false K-range claim are conceded flatly with no weight-shifting, and the
RaM ground-(2) falsification is conceded outright.

Its strongest beat is one no prosecution draft would find: **the Demšar fix helps the paper.**
Demšar's actual recommendation *endorses* Friedman at small n ("the number of data sets is
usually much less than 30"), and the power limitation is independently established by the
paired-test calculation in the same sentence. So deleting the fabricated threshold removes a
false warrant **and** an unnecessary self-deprecation. B generalises this: **four of the twelve
fixes leave the paper stronger than the sentence they replace** — which is not what a defect list
normally looks like, and is a framing the synthesis should keep.

B also independently reached the orchestrator's own conclusion on the interaction: recommend it
as an **existence-and-ordering claim scoped to the synthetic grid**, not as a stable 0.15, since
promoting an unqualified magnitude would import the exact normalizer fragility the same draft
warns about.

## Reading discipline

B read all 54 curated IDs (52 direct, 2 via resolved siblings carrying the same body), plus the
query file, decomposition, evidence digest, comparisons, source tensions, the three findings
files, and `main.tex` in full. No vault surveys, no new fetches — the curation held.

## Next

Step 11 — synthesizer subagent, Read+Write locked, two-pass write to the final report.
