# Step 2 — Width sweep

Run `mbo-gauntlet-r4-adversarial-0f06f1` · branch `gauntlet-r4` · 2026-07-20

## Outputs

| Artifact | Content |
|---|---|
| `research/temp/search-plan.md` | ~70 planned searches across four lenses; gap check closed five holes |
| `research/temp/scored-urls.md` | superseded — batches were themed by *claim under audit* rather than by URL utility |
| `research/temp/coverage-gaps.md` | 92 notes / **69 distinct sources**; two uncovered citations sent to wave 2 |
| `research/temp/redundancy-audit.md` | 21 duplicate clusters, all same-paper-twice; no wave 3 needed |
| `research/temp/local-checks.md` | orchestrator's own verification against repo artifacts |
| `research/temp/findings-so-far.md` | running verdict ledger |
| `research/temp/orchestrator-notes.md` | hypotheses, scoring, emerging thesis, risks |

**Corpus: 69 distinct sources, 92 notes, 70+ claims files.** Full-tier minimum is 45.

## How this sweep departed from the default

The standard step 2 partitions a URL queue by utility score for topical coverage. That is the
wrong shape here. This query does not want breadth over a topic — it wants **one primary
fetched and grepped per claim under audit**. So batches were themed by *claim*, each carrying
the specific sentence from the paper it had to test, the exact grep terms, and an explicit
statement of what would count as a kill.

Twelve batches ran (10 wave-1 + 1 added mid-wave + 1 wave-2 gap-fill). Utility scoring was
skipped deliberately; `scored-urls.md` would have added nothing over the claim-indexed plan.

## Search-plan gap check — five holes closed before fetching

1. The wider **"offline black-box optimization"** reading of N6 had no rows of its own; every
   P0 row said "offline MBO". A kill phrased in the wider vocabulary would have been invisible.
2. The three near-misses had **re-confirm** rows but no **extension** rows. The query asks two
   things; the second is the one a re-audit skips.
3. **Adjacent fields** (surrogate-assisted EA, AutoML, algorithm configuration) had no rows.
   The most dangerous kill is a paper that ran the factorial without offline-MBO vocabulary.
4. `melis2018sota` was listed only as a citation to verify, not as a **premise to test**.
5. The **"unexplored"** novelty category — the one dropped in step 1 — had no search rows.

## What the sweep produced

Ten mandatory fixes and a set of ranked opportunities, recorded in `findings-so-far.md`.
Headline: **N6 is not killed** — eight 2026 papers grepped clean on twelve decomposition
terms, all three near-misses re-confirmed, ~347 forward citations walked with no extension —
but the near-miss list must expand to include **RaM Table 3**, a genuine 9×2 crossed grid in
offline MBO sitting inside a paper the submission already cites.

## Method notes that belong in the final report

**Two subagent relays overstated findings in the direction of severity.** Both were caught by
reading the primary myself:
- The conformal proposition was reported as missing a load-bearing hypothesis. It is not — it
  defines `w` as the true density ratio, making it formally correct. Downgraded to a scoping
  omission.
- RaM was reported as making the paper's characterisation "false". It makes it *incomplete* —
  RaM's main experiment does hold gradient ascent fixed.

**Rule adopted:** any verdict in the final report resting only on a relayed summary, rather
than text the orchestrator read, is marked as such.

**One suggestion of mine was withdrawn.** I proposed TuRBO as a closer precedent for BO
stalling; TuRBO diagnoses the opposite (over-exploration). Nobody owns the LCB-paralysis
reading, which is a better outcome for the paper than the fix I first proposed.

**Two homonym traps caught**, each of which would have produced a false KILL on a naive grep:
Liang's 14 `crossed` hits are the *Crossed barrel dataset*; four papers' `anova` hits are the
surnames *Usmanova* / *Bozhanova*.

## Environment limitations (carried to "What I could not verify and why")

- **`hyperresearch fetch` cannot ingest PDFs here.** Every arXiv PDF URL form returns
  `JUNK_CONTENT: Binary PDF garbage in content`. One batch traced it into
  `hyperresearch/web/crawl4ai_provider.py` and found `_fetch_pdf()` works when called directly
  — the fault is the post-fetch `looks_like_junk()` gate misfiring, not PDF extraction. An
  earlier batch misdiagnosed it as missing pymupdf by testing the system `python3`; the
  interpreter hyperresearch runs has PyMuPDF 1.27.2.3. All full-text verification ran via
  arXiv/ar5iv HTML mirrors or `curl` + pymupdf outside the vault. **Verdicts rest on primary
  full text; most of that text is not stored in the notes.**
- **Semantic Scholar returned HTTP 429 for the entire session**, on both the REST endpoint and
  the MCP tool, across every retry schedule. arXiv and OpenAlex carried all citation chaining,
  including the N6 forward-citation walks.
- **OpenAlex full-text `search=` is very noisy on this topic** — it returned climate models and
  echocardiography for optimization queries. Its null results are near-worthless as evidence of
  absence, and the N6 verdict does not rest on them.
- Concurrent batches caused occasional sqlite `IntegrityError` and sync id-collisions; resolved
  by deprecating true duplicates.

## Next

Step 3 — contradiction graph.
