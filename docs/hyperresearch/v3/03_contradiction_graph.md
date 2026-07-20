# Step 3 — Contradiction graph

Run `mbo-gauntlet-r4-adversarial-0f06f1` · branch `gauntlet-r4` · 2026-07-20

## Outputs

| Artifact | Content |
|---|---|
| `research/temp/contradiction-graph.json` | **12 ranked fight clusters** (9 high relevance, 2 medium, 1 low) |
| `research/temp/consensus-claims.json` | **9 consensus claims**, each with 2–13 independent sources |

Input: **293 claims** across **80 claims files**, from 69 distinct sources.

## The shape this graph takes, and why it differs from the default

The standard contradiction graph pairs source against source. Here the dominant axis is
**paper-claim against literature** — the query is an audit, so the contested question is
usually "does the corpus support what the submission asserts?" rather than "do two papers
disagree?" Each cluster therefore fields the paper's own position as `side_a` where that is
the live disagreement.

Genuine source-vs-source fights do exist and are recorded as such — the sharpest is
`sigma-distance-vs-error`, where Carrete's ρ=0.90–0.91 in regression sits against SNGP's and
DUQ's claim that ensembles lack distance-awareness entirely, and neither aligns with the
paper's framing.

## The nine high-relevance fights

1. **`sigma-distance-vs-error`** — the distance-not-error dichotomy is a false opposition, and
   SNGP is cited against its own thesis.
2. **`K-robustness-vs-K-sensitivity`** — L/R/W tested K={2,5,10} and found robustness;
   verified first-hand.
3. **`audit-direction`** — the narrow scalar claim survives; the surrounding rhetoric does not,
   and confound-leakage imposes a new burden of proof.
4. **`ucb-local-search-ownership`** — nobody owns the reading: Fan proposes and proves
   convergence, TuRBO diagnoses the opposite, GIBO uses no UCB.
5. **`distance-explains-off-support-failure`** — complementary, not contradictory; the paper's
   Elimination 7 refines a named prior position it does not cite.
6. **`budget-dissolves-or-strengthens`** — the paper argues defensively where the literature
   would let it argue positively. Clearest under-stated result.
7. **`pessimism-creates-or-amplifies`** — Ghasemipour supplies a candidate positive mechanism
   the seven eliminations do not rule out.
8. **`eta2-at-small-n`** — both corrections improve the paper.
9. **`n6-residual-width`** — survives on three grounds, none currently on the page.

## Two observations worth carrying forward

**Several "fights" resolve in the paper's favour, and that is information.** The
`surrogate-vs-optimizer-doctrine` cluster is recorded as a fight with a null outcome: I
hypothesised the paper might be over-conceding priority to Shahriari, and the primary refuted
that decisively. A negative result on a hypothesised fight is evidence about the corpus, not
an absence of evidence, so it stays in the graph rather than being silently dropped.

**Most fixes make the paper stronger, not weaker.** Removing the Demšar threshold removes an
unnecessary self-deprecation, since Demšar endorses Friedman at small n. Bias-correcting η²
grows the headline effect. Citing Fannjiang converts a priority liability into a refinement
claim. Framing the budget result against COCO and Lucic promotes it from defence to
contribution. That pattern should shape the report's tone: this is a list of upgrades that
happen to be mandatory, not a list of damage.

## Next

Step 4 — loci analysis. The fight clusters feed it directly, so loci emerge from where the
evidence actually forks. At least one dialectical locus is mandatory; clusters 3, 6 and 9 are
the natural candidates.
