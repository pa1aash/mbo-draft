# 16 · Readability audit — recommendations for `11_synthesize.md`

Structural-readability pass on the synthesis (recommendations only; not applied, to keep the synthesis
and its audit separable). The synthesis is already sectioned (accept path / top-3 risks / single move)
and uses bold lead-ins, so the audit is light. Ordered by leverage.

## Recommended — would materially improve scan-ability

1. **Add a decision table for the three-way branch (make-table).** The corollary in the single-move
   section is the synthesis's payload and is currently a dense prose block. Convert to a 3-row table:
   columns *X1/X3 outcome → identity → venue → deliverable*. Rows: η²_surr survives → C → AAAI-27 → X4;
   survives-but-no-mechanism → A → MLRC 2026 → X4; η²_surr evaporates → E → AAAI-27 (declared) →
   coverage diagnostic. This is the single highest-value readability change — a reviewer of *this dossier*
   should see the branch at a glance.

2. **Promote the "single highest-leverage move" to the top as a one-line TL;DR (add-whitespace /
   reorder).** The move is the deliverable of the whole file but sits third. Add a bold one-sentence
   banner under the H1 ("**Bottom line:** run the X1+X3 de-confounding grid + report gradtune; it is the
   one move that gates identity, checklist, and framing") so the answer survives a 10-second read.

3. **Tabulate the top-3 risks + runner-up (make-table).** Four risks each follow a *claim → evidence →
   mitigation* shape already; a 4-row table (Risk | Reject route | Mitigation | Cost) would let a reader
   compare mitigations by cost without re-reading prose.

## Optional — minor

4. **Bold the effect sizes on first appearance (bold-keyterms).** η²_surr=0.37, η²_opt=0.01, ρ=0.536,
   Friedman p=6.09e-05 are the load-bearing numbers; bold them once so the quantitative spine is
   scannable. Do not bold on every recurrence.

5. **Split the long gate sentence (split-sentence).** In "The path has a live gate", the sentence
   ending "…decided by the run that decides it" packs the reproduction result, the partial-corner
   status, and the availability conclusion into one breath. Split after the parenthetical η² values.

6. **The four-axis paragraph (H1 patch) could become a labeled list (make-list).** It currently runs
   *Manuscript … Experiments … Statistics … Artifact* as inline italic run-ons; a four-item bulleted
   list keyed on the axis names would mirror the query's own four-part structure and read faster.

## Explicitly leave alone

- **Do not merge the scope note into the body.** The honest "this is a scoped synthesis / memos 02–09
  absent at read time" disclosure must stay visually separate at the top; it is a load-bearing caveat,
  not throat-clearing.
- **Keep the em-dash-heavy voice.** It suits an argumentative dossier; flattening it would cost
  precision. No sentence-simplification pass recommended beyond item 5.
- **No horizontal-rule removal needed** — the three `---` breaks map to the three real sections and aid
  navigation.
