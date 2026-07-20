# Step 9 — Evidence digest

Run `mbo-gauntlet-r4-adversarial-0f06f1` · branch `gauntlet-r4` · 2026-07-20

## Output

`research/temp/evidence-digest.md` — **129 claims**, 702 lines, filtered from **443** across 113
distinct source notes.

Filter: `confidence == high` OR `evidence_type in (empirical, statistical)`, **and** non-empty
verbatim `quoted_support`. Ranked within group by presence of hard numbers. Capped at 10 per
group.

| Group | Claims |
|---|---|
| N6 — the crossed factorial none-found | 10 |
| Citation fidelity — SNGP / distance-aware uncertainty | 8 |
| Citation fidelity — Fan / UCB-as-local-search | 5 |
| Citation fidelity — Demšar / Benavoli / power | 10 |
| Citation fidelity — audit genre and the shrink premise | 10 |
| Contradiction — ensemble σ: error or distance signal | 10 |
| Contradiction — ensemble size K and robustness | 10 |
| Normalization and effect-size methodology | 10 |
| Budget, compute-matching and benchmarking norms | 10 |
| Mechanism — extrapolation, Goodhart, off-support | 10 |
| Mechanism — pessimism, safe improvement, offline RL | 10 |
| Conformal coverage and interval validity | 6 |
| Design of experiments — interaction methodology | 10 |
| Landscape analysis and algorithm selection | 10 |

Plus the 9 `[consensus]` claims with their caveats, and the top 5 `[contested]` fight clusters
with both sides' evidence, the evidence delta and the scope reading.

## Two things the digest surfaced that are worth carrying into the draft

**The homonym trap is now quantified across three papers.** COMs' full text yields *"4 raw
'anova' substring hits, all false positives from author surnames in the bibliography (same
Usmanova/Bozhanova pattern as Design-Bench and the comprehensive review, indicating these three
papers share overlapping bio-design citations)."* A naive grep-count audit would have scored three
offline-MBO papers as containing ANOVA. This is the concrete justification for the
fetch-and-read constraint, and it belongs in the report's methodology note.

**RaM's ablation is a self-ablation, not a field factorial.** *"RaM's ablation studies (Tables
8–10) vary ranking loss function (10 losses tested; ListNet best at average rank 2.0) crossed
with two internal modules — a self-ablation of one method's own components, not a field-wide
surrogate-class × optimizer factorial."* Across 171,781 characters: **zero hits on all N6 target
terms.** That sharpens the N6 defence beyond what step 5 established.

## Known imperfection, disclosed

Grouping is regex-based on claim text, `stance_target`, `quoted_support`, `scope_conditions` and
`entities`, with first-match-wins assignment. It is imperfect — a Safe-Policy-Improvement claim
landed in the N6 group because its `quoted_support` contains a probability expression that
matched a decomposition pattern. This is an **evidence index, not a taxonomy**; the drafters read
it for the quotes, and a misfiled quote is still a correct quote with a correct source id. Noted
rather than hand-corrected because hand-tuning the grouper would not improve the quotes.

## Next

Step 10 — triple draft. Three angle-specific draft orchestrators, mandatory for full tier.
