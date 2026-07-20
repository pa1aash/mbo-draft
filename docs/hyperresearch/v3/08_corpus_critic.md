# Step 8 — Corpus critic + targeted gap-fill

Run `mbo-gauntlet-r4-adversarial-0f06f1` · branch `gauntlet-r4` · 2026-07-20

## Pre-flight: period-pinned coverage

`prompt-decomposition.json -> time_periods` holds six entries. This query has no fiscal filings;
its period-pinned targets are **venue-year records**, which are the exact analogue — the
authoritative record for a named period that a snippet will misreport. **All six verified
covered** before spawning the critic: the 2026 publication sweep (8 papers), TMLR 01/2026 (Kim),
ICLR 2024 (Li/Rudner/Wilson), AAAI 2018 (Henderson), JMLR 17 2016 (Benavoli), and the
2026-07-18 prior-audit anchor. No `period-pinned-primary` gap was needed.

## Outputs

| Artifact | Content |
|---|---|
| `research/corpus-critic-gaps.json` | 6 gaps — 2 critical, 4 high |
| `research/temp/corpus-critic-results.md` | per-gap results and effect on positions |
| `research/comparisons.md` | annotated with confidence changes |

Both **critical** gaps target N6, the only unrecoverable position.

## The critic's method is worth recording

It verified each candidate gap was genuinely absent from the vault by **inspecting the returned
note IDs**, not by trusting hit counts. Several near-candidates ("surrogate-assisted
evolutionary" as a bare keyword; "interaction effect model architecture optimizer benchmark")
returned coincidental hits on already-known papers. Given that this audit has already been caught
by two homonym traps — `crossed` matching the *Crossed barrel* dataset, `anova` matching the
surnames *Usmanova*/*Bozhanova* — that discipline is not pedantry.

## The result that matters

**The SAEA region is clean, verified first-hand.** Kudela & Dobrovsky (arXiv:2402.16455) is the
most on-target paper from the region most likely to contain a crossed factorial with ANOVA —
surrogate-assisted evolutionary computation has the strongest design-of-experiments culture of
the three unsearched regions. I fetched the PDF and grepped 47,342 characters myself rather than
relying on the vault note, which held only the abstract page.

**Zero hits on all nine decomposition terms.** It compares performance across algorithms; it does
not decompose outcome variance between a surrogate factor and an optimizer factor.

**N6 gains confidence.** An adversarial search designed to overturn it, aimed at the region where
the analysis was most likely to already exist, returned no substantive challenge.

## Still in flight at step close

The N9 exact-framing search, the interaction-precedent widening, the acquisition-stalling
vocabulary sweep, and accessible η²-bias primaries. **None can overturn a position** — each only
narrows or strengthens a secondary claim. Late returns fold in at step 13, which exists for
precisely this.

## Next

Step 9 — evidence digest.
