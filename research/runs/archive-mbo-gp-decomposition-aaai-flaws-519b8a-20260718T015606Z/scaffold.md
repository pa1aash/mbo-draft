# Scaffold — mbo-gp-decomposition-aaai-flaws-519b8a

PRIVATE PLANNING DOCUMENT. Must not appear in the final report.

## Run config

- vault_tag: `mbo-gp-decomposition-aaai-flaws-519b8a`
- query_file_path: `research/query-mbo-gp-decomposition-aaai-flaws-519b8a.md`
- modality: **synthesize** (defended thesis with evidence chains)
- tier: (filled after step 1)

## Modality classification rationale

The query is not enumerative (not `collect`), not a head-to-head of named entities
(not `compare`), and makes no predictive time-horizon claims (not `forecast`). It
asks for a defended judgment — "is this paper acceptable at AAAI, and where is it
wrong" — supported by evidence chains from both the literature and the artifact.
That is `synthesize`. Findings must be argued and severity-rated, not listed.

## Wrapper requirements (BINDING, not part of the query)

This run is wrapped by a repository-audit session. Requirements:

- Per-step outputs are additionally copied to `docs/hyperresearch/NN_<step-name>.md`
  and committed atomically by the wrapping session. The pipeline itself writes to
  its normal `research/` locations; the wrapper handles the copy.
- Severity taxonomy is fixed and binding: P0 (reject-driver), P1 (major revision),
  P2 (minor), P3 (polish). Every finding carries one.
- Every finding must carry: evidence (file:line or PDF location), the reviewer's
  phrasing of the objection, cost to fix (hours/CPU), fixable-pre-deadline yes/no.
- Novelty claims must be marked `prior work found` / `none found` /
  `NOT VERIFIABLE HERE`. Never assert unchecked novelty.
- Hard constraint from the wrapper: no fabricated numbers. MISSING means MISSING.

## Repository context the pipeline should know (established pre-run, verbatim facts)

These are facts established by direct inspection of the artifact before this run.
They are inputs, not findings — but they sharpen the adversarial searches.

- The manuscript is `paper/aaai27/main.tex` (298 LOC) + `supplement.tex` (206 LOC),
  AAAI-27 anonymous submission format.
- `PREREGISTRATION.md` exists in the repo and **contradicts the shipped paper**:
  it pre-registered the hypothesis that the *optimizer* explains the gap; the paper
  reports the opposite (η²_opt = 0.01). The paper never cites the pre-registration.
- `paper/SKELETON.md` shows the planned Contribution 3 was an offline-to-online
  protocol, which was cut; the shipped Contribution 3 is the Design-Bench null.
- The pre-registration declared n=50 reruns for three crossover-boundary tasks.
  Grep shows they were never run.
- The pre-registration declared a leave-one-task-out offline decision rule as a
  stretch goal. Grep shows it was never implemented.
- `paper/proofs.md` reports q̂ ∈ [2.8, 10.5] and ĉ_ood ≈ 0; the paper reports
  q̂ ∈ [1.8, 16] and ĉ_ood = 0.41. These disagree.
- Prop 1's proof is one line: the two events are the same subset of X. It is an
  identity. Prop 2 is split-conformal + a restatement of Tibshirani et al. 2019.

## Tier rationale

`full` + `argumentative` + `inline` citations.

The query asks "evaluate whether" — a defended judgment on acceptance, not a lookup.
It carries 14 sub-questions across four evaluation levels, names ~15 entities that
each need prior-art checks, and explicitly demands adversarial search against every
core claim. Several sub-questions are genuinely contested (is offline model selection
an open problem; is the smooth-mean mechanism already established), so evidence will
fork and needs dialectical reconciliation rather than summary. That is `full`.

`inline` overrides the `wikilink` default: the report's consumer is a separate
reasoning instance with no access to this vault, so `[[note-id]]` markers would not
resolve. Numbered citations plus a Sources list travel.

## Notes

The literature questions that matter most for the wrapper's decision are, in order:
1. Is coverage-driven **offline model selection** for offline MBO novel + is it a
   recognized open problem? (Determines whether the paper can change category.)
2. Is the smooth-mean / inductive-bias mechanism already established? (Determines
   whether the mechanism story is a contribution or a restatement.)
3. Is the Design-Bench non-discriminativeness result already published? (Determines
   whether Contribution 3 is novel or a known complaint.)
