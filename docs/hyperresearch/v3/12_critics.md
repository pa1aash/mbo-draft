# Step 12 — Adversarial critics

Run `mbo-gauntlet-r4-adversarial-0f06f1` · branch `gauntlet-r4` · 2026-07-20

| Critic | Findings | Severity |
|---|---|---|
| dialectic | 12 | 3 critical, 7 major, 2 minor |
| depth | 12 | 10 major, 2 minor |
| instruction | 8 | 1 critical, 6 major, 1 minor |
| width | 10 | 6 major, 4 minor |
| **total** | **42** | **4 critical, 29 major, 9 minor** |

All four valid JSON. Zero requiring orchestrator restructure — every finding is a surgical
Edit hunk.

## The critics were briefed to attack the orchestrator, not the draft

The default brief is "find what the draft got wrong." That was the wrong instrument here: this
report's likeliest defect was **inheriting my errors**, since I called four of four early
findings correctly and flagged that at the time as a warning sign. Each critic was pointed at
the positions the audit was most confident about.

**It worked, and the highest-value finding in the entire run came out of it.**

## The dialectic critic falsified the audit's own lead recommendation

Rank 1 asserted `surrogate > interaction > optimizer` **"without exception."** The critic
observed that the 33-combination normalizer sweep verified only `η²_surr > η²_opt` — a
*different proposition* — and predicted rank normalization could invert the three-way ordering.

I ran the test across four corners × three normalizers. **It inverts.** In the on/off corner
under rank normalization the optimizer main effect is **0.075** against an interaction of
**0.049**. Eleven of twelve hold; one does not.

What survives, stated precisely: `η²_surr > η²_opt` in all twelve; surrogate largest in all
twelve; interaction above the optimizer effect in **11 of 12**, by 1.1× to 71.3×. The promotion
survives, the absolutism does not, and the failure is not random — it is the corner where the
optimizer axis is most competitive under every normalizer.

**This is the same defect class the audit convicts the paper of**: a warrant that tests a
different proposition than the claim attached to it. The audit committed it in its own lead
recommendation. Full table in `research/temp/interaction-ordering-test.md`.

## The other three critical findings

- **The pairing table double-counts.** The interaction's normalizer-immune form (the raw-units
  contrast) is the *same measurement* as the 7/7 attenuation, so "each survives exactly what the
  other fails" leans on one dataset twice. And "the interaction survives the floor-effect
  challenge" is asserted, never argued — plausibly backwards, since a floor effect under
  perturbation would *generate* an interaction of this shape.
- **The N6 "free result" is a non-sequitur.** RaM's η²≈0.577 sits on a **bundled-method** axis
  the report elsewhere insists is not a clean factor. Using it to argue about model-class
  swaps contradicts the report's own conjunct (b).
- **`UNEXPLORED` appears zero times** — the fourth novelty category the query names, **dropped
  for the second time** after step 1's coverage matrix caught it once already.

## What the critics confirmed was fine

**The five withdrawn claims all stayed withdrawn** in the body — verified individually by the
dialectic critic. Structural mirror check passed cleanly. All seven named citation checks
addressed; both named contradiction hunts land; all three year traps correct. No interim note
was skipped. The depth critic's own summary: *"These are refinements to a strong draft, not a
rescue."*

## The pattern worth carrying into the patch

Three depth findings share one shape: **the report shows the number that failed and asserts the
numbers that passed.** The off-by-one recount appears; the verified 7/7 → 3/7 → 2/7 ladder does
not. Elimination 1 shows the figure that looks like an arithmetic error (0.203) but not the
z-score cross-check that vindicates it. Since the front-matter thesis is "severity to the results
is NIL," those omissions undercut the exact claim they exist to support.

And the width critic's structural finding: **deliverable (iii) names experiments without the
motivating primary the vault holds** — which the query explicitly mandates. Two were synthesis
losses (draft A carried the attributions; the synthesizer kept the substance and dropped the
citation). One is a self-contradiction: the terminal section says Montgomery "could not be
reached" while the vault holds the excerpt.

## Next

Step 13 — gap-fetch. Expected to be near-empty: the critics found the needed sources are
**already in the vault**, so the gap is attribution, not acquisition.
