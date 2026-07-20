# Synthesis conflicts

No FACTUAL conflicts across drafts — all three cite the same grep-verified quotes and agree on what
each source says. The apparent verdict differences are ANGLE-DRIVEN (by design) and resolve toward the
step-8-calibrated readings:

## Conflict 1: N4 verdict — "mechanism FOUND" (Draft B) vs "PARTIAL" (Drafts A, C)
- Draft B (steelman) says: N4's distance-aware mechanism is FOUND (SNGP) and the UCB-local-search
  mechanism is FOUND (Fan et al. NeurIPS 2024, arXiv:2405.15285).
- Drafts A, C say: PARTIAL — the mechanism is owned, but the "LCB is an implicit trust region" NAMING
  + the offline-MBO instantiation is NONE FOUND; and the σ-mediation is separately undercut by the β=0
  control (so the viable mechanism is the posterior mean, not σ).
- Source check: Fan et al. verbatim "minimizing UCB can be viewed as local strategy"; "trust region"
  appears only as TuRBO citations, "implicit" 0 hits. SNGP owns distance-aware variance growth.
- **Verdict: PARTIAL.** B is right that the mechanism is owned; A/C are right that the naming +
  offline-MBO application remain free. Use PARTIAL and state both halves.

## Conflict 2: N1 verdict — "shape FOUND" (all) but is the residual real? (B downplays, A/C affirm)
- Draft B says: the taxonomy shape is Henderson's genre (FOUND); implies little residual.
- Drafts A, C say: shape FOUND, but the η²-decomposition + offline-MBO-specific confound vocabulary +
  the net-UP direction = NONE FOUND (the residual).
- **Verdict: shape FOUND, residual real.** Concede the genre to Henderson/Musgrave/Dacrema up front;
  claim the composition (five offline-MBO confounds + η² + strengthening). This is D's core.

## Conflict 3: which candidate is strongest — all three say D
- No conflict. A, B, and C independently recommend **D** (confound taxonomy). B reaches it by
  elimination (steelman), A/C by construction. Commit to D; present A as under-credited-but-narrow and
  C as the highest-ceiling bet contingent on unrun manipulation.

## Verdict-vocabulary note
Draft C uses a FOUR-value scale (FOUND / NONE FOUND / PARTIAL / NOT VERIFIABLE). The user's query asks
for FOUND / NONE FOUND / NOT VERIFIABLE (three values). RESOLUTION: keep the three-value verdict in the
table's primary column (map PARTIAL → "PARTIAL (prior work owns X; residual Y NONE FOUND)" as an
explicit hybrid cell), so the table honors the query's vocabulary while preserving the boundary scoping.
