# Scaffold — mbo-gauntlet-r4-adversarial-0f06f1

**PRIVATE PLANNING DOCUMENT. MUST NOT APPEAR ANYWHERE IN THE FINAL REPORT.**

## Run config

| Field | Value |
|---|---|
| `vault_tag` | `mbo-gauntlet-r4-adversarial-0f06f1` |
| `query_file_path` | `research/query-mbo-gauntlet-r4-adversarial-0f06f1.md` |
| `modality` | **synthesize** (defended thesis with evidence chains) |
| `pipeline_tier` | **full** — user-declared, binding. All 16 steps. |
| `git branch` | `gauntlet-r4` (never main) |
| `deliverable path` | `docs/GAUNTLET_R4.md` |
| Today | 2026-07-20 |

## User Prompt (VERBATIM — gospel)

See `research/query-mbo-gauntlet-r4-adversarial-0f06f1.md`. That file is gospel and is
passed verbatim, block-quoted, into every subagent spawn.

## Modality classification rationale

This is **synthesize**, not collect or compare. The deliverable is not an enumeration of
sources but a set of *defended verdicts*: N6 is CONFIRMED or KILLED; each citation is
FAITHFUL or MISCITED; each novelty finding is FOLD-IN / FOLLOW-UP / NOT-WORTH-IT. Every
verdict is a committed position backed by an evidence chain that terminates in fetched
primary text. The adversarial framing (find the paper that kills us) makes this
argumentative, not descriptive.

Sub-modality note: deliverable (iii) is **compare**-shaped (ranked findings with tags), so
that section gets proportionate per-finding depth plus a committed ranking.

## Tier rationale

User declared `TIER: full. All 16 steps. Do not abbreviate.` This is binding and overrides
step 1's own classifier if they disagree. Justification independent of the declaration: the
query is argumentative, has an existential falsification target (N6), requires adversarial
review, and demands primary-source verification of ~15 load-bearing citations across a
67-entry bibliography. This is exactly the full-tier profile.

**Step 1 confirmation (2026-07-20).** The classifier agrees with the declaration
independently. `pipeline_tier: full`, `response_format: argumentative`. The query decomposes
to 25 sub-questions and 25 entities across four deliverable blocks, carries an
unrecoverable-failure target, and explicitly forbids snippet-level verdicts — none of which
the light tier's 5-step path can serve. No tier conflict to resolve.

`citation_style: inline` rather than the `wikilink` default. The deciding reason is
mechanical: the deliverable is `docs/GAUNTLET_R4.md`, which sits outside `research/notes/`,
so `[[note-id]]` wikilinks would not resolve from it. The supporting reason is that an audit
whose whole method is primary-source verification must expose venue and year for every
source it leans on — three confirmed year traps make an unnumbered, unresolvable citation
apparatus actively unsafe here.

## Wrapper requirements (BINDING, separate from the query)

1. **Save path:** `docs/GAUNTLET_R4.md` — NOT the default
   `research/notes/final_report_<vault_tag>.md`. The pipeline writes to the default path;
   the orchestrator copies to `docs/GAUNTLET_R4.md` at ship time. Both must exist and match.
2. **Required top-level structure — exactly three deliverables, in this order, with the
   N6 verdict FIRST (before deliverable (i)):**
   - N6 verdict (existential; CONFIRMED NONE-FOUND with queries, or KILLED with the paper)
   - (i) MANDATORY — claims the literature contradicts or that are miscited. Each item
     carries: the claim, the paper's citation/framing, what the source actually says, the
     required **fix**.
   - (ii) MANDATORY — KILLS. Prior work refuting N6 or any ledger claim.
   - (iii) RANKED — scope of novelty. Each item tagged **FOLD-INTO-THIS-PAPER** /
     **FOLLOW-UP-PAPER** / **NOT-WORTH-IT**; under-executed items additionally tagged
     **CHEAP** / **EXPENSIVE**.
3. **Terminal section:** `## What I could not verify and why` — mandatory, last.
4. **Per-step commits:** every one of the 16 steps commits `docs/hyperresearch/v3/NN_<step>.md`.
5. **Authorship:** `Palaash Gang <palaashgang@gmail.com>`. **Zero AI / agent / assistant /
   co-authored / generated-with strings** in any commit message, any file, or the report.
   This overrides the default commit trailer. Check before every commit.
6. **Branch discipline:** commit continuously to `gauntlet-r4`. Never to `main`.

## Method constraints (binding, from the query)

- Academic APIs (Semantic Scholar / arXiv / OpenAlex) BEFORE web search, every claim.
- **FETCH PRIMARY AND GREP.** No novelty or contradiction verdict from a snippet, ever.
- **Vault-cache prohibition:** the vault is GLOBAL and holds the previous pass's corpus.
  Do NOT issue a verdict from a cached source. Re-fetch and note the re-fetch.
- **Confirmed citation-year traps** (this project has caught fabrications):
  - Li/Rudner/Wilson = **ICLR 2024** (S2 says 2023)
  - Henderson = **AAAI 2018** (S2 says 2017)
  - Benavoli = **JMLR 2016** (arXiv 2015)
  - Kim et al. survey = **TMLR 2026** camera-ready (arXiv v1 back-propagates 2025; note the
    bib key is `kim2025mbosurvey` while the paper prose says "2026 survey" — flag this
    internal inconsistency as a candidate finding)
- Prior verdicts in `docs/NOVELTY_V3.md` are **PRIOR, to be re-checked, not trusted.**

## Priority-ordered targets

### P0 — N6 (existential)
Claim: "no prior work runs a crossed surrogate × optimizer factorial in offline MBO."
Failure mode is UNRECOVERABLE. Must re-verify with fresh fetches against:
- an exact crossed/factorial surrogate × optimizer decomposition in offline MBO or offline
  black-box optimization;
- **anything published since the last audit — 2026 especially**;
- the three near-misses, each re-confirmed as still-only-near: Hutter fANOVA (one-way,
  SMAC fixed), Liang (crossed but descriptive + online), Moosbauer (two-axis but explicitly
  *declines* the two-way fANOVA).

### P1 — load-bearing citation verification (deliverable i)
Fetch-and-grep each primary: `liu2020sngp` (distance-aware UQ), `fan2024minucb`
(UCB-as-local-search / LCB-paralysis), `shahriari2016humanoutoftheloop` (the doctrine
scoped against), `li2024bnnsurrogates` (cross-surrogate comparison + K-robustness),
`kim2025mbosurvey` (attribution-gap concession), `agarwal2021precipice` +
`demsar2006statistical` (the power argument), `melis2018sota` (audits-shrink premise —
load-bearing for the N9 direction claim), `moosbauer2022benchmarkdriven`,
`hutter2014fanova`, `liang2021benchmarking`, `chemingui2024pggs` (the local premise
falsified), `recht2019imagenet`, `bressan2019confounds`, `benavoli2016meanranks`,
`abe2022ensembles`, `dewolf2022intervals`.
Note: `liang2021benchmarking`, `bressan2019confounds`, `abe2022ensembles`,
`dewolf2022intervals`, `vanamersfoort2020duq`, `ghasemipour2022pessimistic`,
`jacot2018ntk` etc. appear in prose — cross-check every `\citep` key resolves in
`references.bib` (67 entries) and that no key is cited for a claim its source lacks.

### P2 — contradiction hunt (deliverable i, second half)
- Does anyone show the ensemble's σ **IS** an error signal? (contradicts the
  distance-signal claim, main.tex §Isolating the Source)
- Does anyone show K-robustness **down to K=2**? (contradicts the K-sensitivity framing,
  Confound 3) — L/R/W is K∈{5,10}; find anything reaching K=2.
- Does anyone report a de-confounding audit whose corrected effect size **grows**?
  (would kill the "no precedent" claim in Contribution 2 / N9 — the paper's second-most
  load-bearing none-found)
- Does anyone already report LCB-paralysis-style frozen cells / optimizer-invariant
  surrogate cells on Design-Bench?

### P3 — the stronger paper (deliverable iii)
- **Under-stated:** the budget-axis separation ($0.243 \to 0.526$, disjoint intervals
  $[0.189,0.355]$ vs $[0.421,0.719]$ — the *only* outright separation in the paper, buried
  in a paragraph) and the two-strengthenings pattern (§Discussion). Is either a bigger
  result than its framing?
- **Under-executed:** seven eliminations, no positive mechanism. What runnable experiment
  does the literature motivate that converts elimination → mechanism? Name it, cite the
  motivating work, tag CHEAP or EXPENSIVE.
- **Under-explained:** the x0-inversion result (D25) and the frozen-cells/LCB-paralysis
  reading are stated flatly; does the literature license a sharper frame?

## Loci pre-seeds (advisory to step 4 — analysts decide, this does not bind them)

At least one **dialectical** locus is mandatory. Candidates:
- D1: Is N6's residual scoped so narrowly that it is unfalsifiable-by-construction? (The
  hostile-reviewer read: "crossed × two-way ANOVA × offline MBO" has four conjuncts; a
  reviewer may call that gerrymandering. Defend or concede.)
- D2: Does the "audits usually shrink" premise (`melis2018sota`) actually hold in the
  literature, or is the paper's headline direction-claim built on a premise that a broader
  read contradicts?
- D3: Elimination-by-seven vs. positive mechanism — is a diagnosis-without-mechanism paper
  publishable at AAAI, or does the elimination framing read as a null result?

## Artifact locations (this run)

Standard V8 paths. Per-step commit target: `docs/hyperresearch/v3/NN_<step>.md`.
