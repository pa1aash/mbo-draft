# Step 15 — Polish

Run `mbo-gauntlet-r4-adversarial-0f06f1` · branch `gauntlet-r4` · 2026-07-20

**20,337 → 19,890 words.** Hedge-stacking, throat-clearing and preamble removed. The auditor
terminated on an API error mid-pass and was resumed; after resuming it made only marginal
further progress, so the orchestrator took over the length **decision** — not the cutting.

## The length decision, and why it is ACCEPT rather than cut

The pipeline default for `argumentative` is 7,000–8,000 words. The report is 19,890. I checked
whether that is bloat before accepting it, and it is not.

**There is zero literal duplication.** A scan for sentences over 100 characters appearing more
than once returned **no repeats at all**. The four passages flagged as repeat offenders — the
RaM analysis, the normalizer critique, the interaction's stability argument, the severity split
— are cross-referenced, not restated.

**Section balance tracks the contract, not authorial indulgence:**

| Section | Words | Per-item |
|---|---|---|
| N6 Verdict | 2,525 | — |
| (i) Miscitations | 5,931 | ~490 across 12 mandatory items × 4 required fields |
| (ii) Kills | 892 | correctly short — the finding is zero |
| (iii) Ranked novelty | 6,735 | ~320 across 21 tagged items |
| Terminal section | 1,543 | 7 categories |
| Sources | 1,746 | 102 entries |

The query says **"Do not abbreviate"** and specifies a per-item field contract. Twelve mandatory
items each carrying claim / framing / what-the-source-says / fix, plus twenty-one tagged ranked
items, plus a verdict carrying its verbatim queries, plus a seven-category terminal section, has
an irreducible size.

**Three independent judgements converged on this before I did.** Draft A flagged its own
over-length rather than silently trimming, on the grounds that further cuts "would have amputated
findings rather than prose." The width critic graded the length "only partly defensible" and
deliberately targeted two consolidatable passages instead of recommending broad cuts. The
patcher, which *grew* the report, flagged that the added mass is evidence the report previously
asserted without showing — the exact defect three depth findings convict it of.

**The standing instruction at every stage was that reaching a word target by removing evidence is
worse than missing the target.** Honouring it means accepting 19,890.

## One hygiene call worth recording

My scan flagged three "width sweep" hits as pipeline vocabulary. I checked each: all three refer
to **the audited paper's own** per-member width ablation in Elimination 2, not to any pipeline
stage. Removing them would have corrupted a technical description. Left in place.

## Integrity at close

102 cited / 102 listed · zero orphans · zero numbering gaps · five H2s verbatim and in order plus
Sources · no YAML · zero pipeline vocabulary · zero AI/agent/authorship strings · Dao,
Ghasemipour and Choi all retain "venue unverified".

No number, interval, verbatim quote, table, citation marker, tag, bolded **Fix**, narrowing
qualification, or falsification record was removed at any point.

## Next

Step 16 — readability audit.
