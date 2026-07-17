# 13 · Gap-fetch — N/A, with reason

**Verdict: no new source fetched. This step is legitimately N/A for a scoped synthesis, and the file
explains why (the blueprint permits an N/A file that explains itself).**

Step 13's job is narrow: if a critic said "the synthesis ignored topic X" *and the vault has zero
sources on X*, fetch the missing source so the patcher has something to cite. That precondition is not
met here. Every material finding the critics (`12_critics.md`) raised is one of two kinds, and neither
is a source gap:

**(1) Non-citational gaps — they need a compute run or an internal restructure, not a citation.**
No paper can fill these; only the repo can.

| Critic finding | Why no citation fills it |
|---|---|
| D1 (three-way identity branch), D2 (E as fallback) | Resolved only by the PENDING X1/X3 grid run (`results/corners/`). A source cannot tell us whether η²_surr survives normalization. |
| DP1 (statistics fix is separate), DP2 (query-budget arm) | These are experiments/edits owed inside our own artifact (`FLAW_LEDGER.md` P1-2, P1-1), not literature gaps. |
| W1 (7-page budget vs Identity C) | A layout/cut decision, internal to `AAAI27_VENUE.md` C.5. |
| W2 (COMs divergence) | Resolved by diffing our repo against the official COMs hyperparameters (`DECISION_QUEUE.md` D7), not by a new citation. |
| I1 (four-axis structure), I2 (name X4 as the free move) | Restructuring of the synthesis itself. |

**(2) Already-covered gaps — the relevant source is present and verified in the repo docs.**
Fetching again would be redundant.

- **W3 (MLRC 2026 as fallback venue):** already fetched and recorded in `VENUE_NORMS.md` (official
  NeurIPS track via TMLR, hard deadline 2026-09-30, welcomes negative results). No gap.
- **W4 (novelty phrasing constraint):** the ownership analysis and the fANOVA / Li-Rudner-Wilson
  citations are already in `NOVELTY_V2.md` (D9). No gap.
- **The reviewer-corpus bar, the four AAAI precedents, the genre template:** all fetched and verified
  in `VENUE_NORMS.md` and `AAAI27_VENUE.md` (fetch dates 2026-07-17). The load-bearing external anchors
  (Henderson AAAI-18 arXiv:1709.06560; Kim TMLR survey arXiv:2503.17286) are recorded as re-fetched
  this session in `NOVELTY_V2.md`'s verification-provenance line.

**One genuinely missing source that is unfillable, flagged not fetched.** AAAI-specific reviewer
behavior / acceptance-rate data for the measurement genre does not exist publicly — `VENUE_NORMS.md`
states the ceiling verbatim: *"AAAI reviews are not public. All phrasings are an ICLR/NeurIPS proxy."*
There is no source to fetch; the gap is a permanent property of the venue, already disclosed in the
synthesis's inherited caveat (`12_critics.md` D3).

**Fetch attempt this session:** a confirmatory Semantic Scholar lookup for the two load-bearing
precedents (Henderson; Kim survey) returned HTTP 429 (rate-limited — a parallel agent was likely
hitting the same API). No re-fetch was needed regardless, because both records were already verified
this session per `NOVELTY_V2.md`. No claim in the synthesis rests on an unverified snippet — the
`VENUE_NORMS.md` fabrication-hazard rule (four search-layer fabrications caught this project) was
respected: nothing here is sourced from an un-fetched summary.

**Net:** N/A. The patcher (`14_patcher.md`) has all the citations it needs already in the repo docs;
the critics' material findings are addressed by restructuring the synthesis, not by adding sources.
