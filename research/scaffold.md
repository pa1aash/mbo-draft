# Scaffold — offline-mbo-novelty-audit-6d8cd4

## User Prompt (VERBATIM — gospel)
Canonical query lives at `research/query-offline-mbo-novelty-audit-6d8cd4.md`. That file is
gospel for every step and every subagent. It contains THE QUESTION, CRITICAL METHOD
REQUIREMENTS, WHAT THE PAPER MEASURES, the nine claims N1–N9, and WHAT I NEED OUT OF THIS.
Do not paraphrase it into subagent prompts — block-quote it.

## Run config
- vault_tag: `offline-mbo-novelty-audit-6d8cd4`
- query_file_path: `research/query-offline-mbo-novelty-audit-6d8cd4.md`
- pipeline_tier: **full** (user-forced: "TIER: full. All 16 steps. Do not abbreviate to light tier.")
- modality: **compare** (per-claim novelty verdicts N1–N9 with proportionate depth + a
  committed recommendation on the strongest publishable contribution among candidates A/C/D)
- response_format: argumentative (defended verdicts, adversarial checks per claim)
- CLI: `/opt/homebrew/Caskroom/miniforge/base/bin/hyperresearch`
- today: 2026-07-18

## Modality rationale
The deliverable is a verdict table (FOUND / NONE FOUND / NOT VERIFIABLE) across nine claims,
each backed by fetched-and-grepped primary sources, PLUS a committed judgement of which of
three candidate papers (A repaired-measurement / C mechanism / D confound-taxonomy) is the
strongest publishable contribution. That is fundamentally a comparison with a required
recommendation — "compare" modality — carried out in an argumentative register because the
user demands each verdict be defended and adversarially stress-tested.

## Wrapper requirements (BINDING — separate contract, NOT part of the query)
- FINAL REPORT save path: `docs/NOVELTY_V3.md` (in addition to the canonical
  `research/notes/final_report_offline-mbo-novelty-audit-6d8cd4.md`; copy final → docs path at ship).
- INTERMEDIATE step outputs: `docs/hyperresearch/v2/NN_<step>.md` (v2 dir; prior run's
  outputs already sit in `docs/hyperresearch/` and must not be overwritten).
- CITATION FORMAT: inline, with venue AND year AND arXiv ID where one exists.
- COMMITS: continuous, as work completes, on branch `hyperresearch-v2`. NEVER main.
- GIT IDENTITY: Palaash Gang <palaashgang@gmail.com> (already set repo-local; verified).
- COMMIT/ARTIFACT HYGIENE (non-negotiable): ZERO mention of Claude, Claude Code, Anthropic,
  "AI-generated", "agent", or any co-authorship trailer in ANY commit message, file, or
  artifact. Commit messages are plain technical imperative. This OVERRIDES the default
  Co-Authored-By trailer — do not append it.
- DO NOT edit `paper/aaai27/*.tex`.
- TERMINAL SECTION of the final report: "What I could not verify and why."

## Method requirements carried into every fetch/depth step
- Academic APIs (Semantic Scholar, arXiv, OpenAlex; PubMed n/a) BEFORE web search, every claim.
- FETCH PRIMARY AND GREP IT — no verdicts from snippets/abstracts. Four fabricated citations
  already caught on this project; zero tolerance.
- ≥1 adversarial search per claim ("criticism of X", "limitations of X", "X does not replicate").
- Citation-date traps to carry: Li/Rudner/Wilson = ICLR 2024 (S2 back-props 2023 from arXiv v1);
  Henderson et al. = AAAI 2018 (S2 says 2017); Benavoli et al. = JMLR 2016 (arXiv 2015).
- Every novelty verdict: PRIOR WORK FOUND (citation + specific overlapping sentence) /
  NONE FOUND (exact queries run) / NOT VERIFIABLE. Never assert an unchecked novelty.

## Tier rationale
User-forced full tier. All 16 steps run: 1→2→3→4→5→6→7→8→9→10→11→12→13→14→15→16.
No downgrade permitted regardless of decompose's own classification. Step 1's independent
classification AGREES: fourteen sub-questions, nine contested novelty claims each requiring
adversarial primary-source verification, a defended recommendation among three candidate
papers, and an explicit demand for evidence-chain rigor → full + argumentative regardless.
citation_style = inline (wrapper override: "inline, with venue AND year AND arXiv ID").

## Prior-run context (treat as UNCHECKED / worthless per user)
- `docs/NOVELTY_CHECK.md`, `docs/NOVELTY_V2.md` = prior hand-written novelty passes; the user
  says they were NOT produced by a real pipeline and to treat every verdict as worthless.
  May be mined for candidate citations to CHECK, never as evidence.
- Repo docs (BUNDLE_PART1/2, FLAW_LEDGER, PROVENANCE, IMPLEMENTATION_AUDIT, MECHANISM_EXPERIMENTS,
  AAAI27_VENUE) describe the paper's own measurements — usable as statements of what WE claim,
  not as external prior art.
