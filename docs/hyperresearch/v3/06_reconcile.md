# Step 6 — Cross-locus reconciliation

Run `mbo-gauntlet-r4-adversarial-0f06f1` · branch `gauntlet-r4` · 2026-07-20

## Output

`research/comparisons.md` — **5 named cross-locus tensions**, each with locus references, the
dynamic, engagement guidance, and a calibration note drawn from the investigators' stated
confidences and falsifiers.

| # | Tension | Type |
|---|---|---|
| 1 | The interaction is promotable as a **direction**, not a magnitude | composition |
| 2 | The audit proved the decomposition is **derivable from a competitor's published table** | complication |
| 3 | The venue advice is right in direction but its named assets are all qualified | complication |
| 4 | A **stable per-task ranking** coexists with a **collapsing per-task magnitude** | apparent conflict, resolved |
| 5 | **Elimination 2 is not as eliminated as the count implies** | complication |

## The two that only exist in cross-section

Most of this audit's findings came from a single locus or from artifact work. Two came from
putting positions together, and they are the ones the report would otherwise miss.

**Tension 2 is the uncomfortable one.** To *defend* N6, locus 1 computed η² from RaM's own
published Table 3 (loss axis 0.027, method axis 0.577). That computation **is** a two-way
decomposition of a competitor's crossed grid, done from published numbers. The audit therefore
demonstrated — while defending the novelty claim — that the decomposition is derivable from data
already in print. N6 survives as a claim about **what the literature reports**; it does not
survive as a claim about what the design space permitted. That distinction has to be on the page.

**Tension 4 yields the only positive structural statement the audit can offer.** Locus 5 found
the per-task gap ranking stable across optimizers (Spearman 0.84–0.96); locus 3 found the
surrogate effect collapsing to ≈0.01 under perturbation. Both hold, because one measures ordering
and the other magnitude. Together they constrain any mechanism: **it must be multiplicative — a
task factor scaled by an optimizer-aggressiveness factor.** A purely optimizer-side account would
not preserve task ordering; a purely task-side account would not collapse under perturbation. No
single locus proposed this; it follows only from the pair.

For a paper whose mechanism section is seven negatives, a constraint derived from its own data is
worth more than another elimination.

## Calibration discipline applied

Where two positions disagreed, the report weights by stated confidence. Two cases mattered:

- **Placement of the interaction.** Locus 6 (2-source budget, self-described as the weaker half)
  and locus 3 (~65% on abstract-versus-main-text) converge on *low* confidence about placement
  while both being high-confidence on content. The report therefore recommends the content firmly
  and the placement tentatively.
- **Ranking stability vs magnitude collapse.** Locus 5's ρ is descriptive at n=7; locus 3's
  simple-effects figures are bootstrapped. The collapse is better evidenced than the stability,
  and tension 4 says so rather than treating them as equals.

Two investigators independently named the same falsifier — the absence of a mixed-effects model
with task as a random effect, which `docs/FLAW_LEDGER.md` P1-2 already calls for. That is a
genuine open question and is flagged as such rather than buried.

## Next

Step 7 — source tensions.
