# Step 4 — Loci analysis

Run `mbo-gauntlet-r4-adversarial-0f06f1` · branch `gauntlet-r4` · 2026-07-20

## Output

`research/loci.json` — **6 loci** (2 dialectical), 15 skip_loci, total source budget 40.

| # | Locus | Flavor | Score | Budget |
|---|---|---|---|---|
| 1 | `n6-residual-scoping-legitimate-or-gerrymandered` | **dialectical** | 33 | 12 |
| 2 | `minmax-normalization-outlier-fragility` | **dialectical** | 29 | 9 |
| 3 | `interaction-term-buried-and-its-methodological-grounding` | convergent | 28 | 8 |
| 4 | `ntk-width-citations-never-verified` | convergent | 22 | 5 |
| 5 | `landscape-predicts-which-surrogate-wins` | convergent | 21 | 4 |
| 6 | `aaai-venue-fit-for-the-audit-genre` | convergent | 19 | 2 |

Two analysts, 9 loci proposed, 6 retained, 2 merges. **The dialectical invariant is satisfied
twice over, once from each analyst, and neither was suggested by my briefing.**

## What the two analysts did differently

A was pointed at the audit's existing fault lines; B was told to look where nobody had looked.
The split worked. A's value was finding what had **slipped through** — most importantly that
Jacot, Lee (×2) and Rahaman, which carry Elimination 2's entire motivation, were never fetched
anywhere in this audit, a gap no tracking file had flagged including my own
`coverage-gaps.md`. B's value was two previously-unflagged numerical facts read straight out of
the paper.

Both independently surfaced the **interaction term**, which I had also found from the
artifacts. Three-way convergence on a result the paper never discusses is itself evidence that
it is the buried finding.

## The orchestrator's own work during this step

Rather than wait idle, I chased the interaction lead through the artifacts and it became the
audit's strongest result:

- **η²_inter is 0.146–0.165 with intervals excluding zero in all four corners**, second-largest
  effect throughout, 4–33× the optimizer main effect, and **9.2× more stable across corners
  than the headline**. Survives bias correction at 0.134–0.156.
- **`tab:cross` is the mechanism**, and it is stated in probabilities rather than normalized
  scores: the ensemble's premise coverage is 0.41 on its own proposals and 0.97 on the GP's.
  The paper holds the effect in one table and its mechanism in another and never connects them.
- **The sharpest form, 7/7 in raw oracle units**: the GP-vs-ensemble gap under perturbation is
  smaller than under both gradient and CMA on every task, averaging **5.9%** of the aggressive-
  optimizer gap. The GP's advantage is almost entirely conditional on an aggressive optimizer.

## The dialectic that improved the finding

B challenged it directly: every η² in the paper rides on per-task min–max normalization over
n=9 cells, and on Griewank-30D that normalizer's range is set by a **2,780× outlier spread**,
compressing the three perturbation cells into a 0.048 band despite a 46% raw difference.

I verified the arithmetic and **the challenge holds for the η² magnitude while the finding
survives in raw units.** That is a better outcome than either position alone: it identifies a
**fifth operating-point coordinate the paper does not name** — the per-task normalizer, the
only one of the five that is an analysis rather than an experimental choice, applied to every
number in the paper.

This is what running two analysts is for. Neither the finding nor its qualification came from
my briefing.

## Next

Step 5 — depth investigation, one investigator per locus with `source_budget > 0`. Six
investigators.
