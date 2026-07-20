# Step 1 — Decompose

Run `mbo-gauntlet-r4-adversarial-0f06f1` · branch `gauntlet-r4` · 2026-07-20

## Outputs

| Artifact | Content |
|---|---|
| `research/prompt-decomposition.json` | 25 sub-questions, 25 entities, 5 required H2 headings, 6 time periods, 12 scope conditions |
| `research/temp/coverage-matrix.md` | 58 rows, 0 remaining gaps |
| `research/scaffold.md` | tier rationale confirmed |

## Classification

`pipeline_tier: full` · `response_format: argumentative` · `citation_style: inline`

The tier was user-declared and binding. The classifier reaches it independently: an
existential falsification target, a four-block deliverable contract, and an explicit ban on
snippet-level verdicts are all outside what the light tier's 5-step path can serve.

`citation_style` departs from the `wikilink` default for a mechanical reason — the
deliverable `docs/GAUNTLET_R4.md` sits outside `research/notes/`, so `[[note-id]]` links
would not resolve from it. Secondarily, an audit built on primary-source verification has to
expose venue and year for every source, and three confirmed year traps make an unresolvable
citation apparatus unsafe here.

## The heading contract

Five H2s, no more. The query says "structure your output as exactly these", so inventing
additional top-level sections would itself be an instruction violation. The N6 verdict is
hoisted above deliverable (i) as the query demands.

```
## N6 Verdict: The Crossed Surrogate x Optimizer Factorial
## (i) Claims the Literature Contradicts or That Are Miscited
## (ii) Kills
## (iii) Scope of Novelty, Ranked
## What I could not verify and why
```

## Two gaps found and closed in the self-audit

The coverage matrix caught two false-negatives in the first-pass decomposition. Both would
have cascaded into missing searches and a structurally wrong draft.

1. **"critique EVERY claim" had been narrowed to cited claims.** Every claim is strictly
   wider than every citation — it takes in uncited assertions, the reported effect sizes,
   and the pre-registration outcomes. Left unfixed, the pipeline would have run a
   citation-only verification sweep that never checks the paper's own numbers against the
   literature. Closed with a sub-question scoped to claims *independent of whether they
   carry a citation*.

2. **"something unexplored" had been dropped entirely.** The query names four novelty
   categories, not three: *unexplored*, under-executed, under-explained, plus the
   under-stated hunt specified separately. Left unfixed, deliverable (iii) would only ever
   critique what the paper already attempted, which is precisely not what "a stronger paper
   in this data that is not being written" asks for. Closed with a sub-question and a
   dedicated entity.

## Scope decisions carried forward

- **N6 searches both readings.** The query says "offline MBO **or offline black-box
  optimization** (the exact thing)". The wider reading is a separate search target in step 2,
  not a synonym collapsed into the narrower one.
- **Near-misses get a two-part test.** Each of Hutter / Liang / Moosbauer must be
  re-confirmed as *still* only a near-miss **and** as *not extended* by any successor. The
  second half is the part a re-audit is most likely to skip.
- **Ledger rows are kill targets too.** Deliverable (ii) is "N6 or any specific ledger
  claim", so all 24 rows of `docs/CLAIM_LEDGER.md` are in scope, not N6 alone.
- **Prior verdicts are priors.** `docs/NOVELTY_V3.md` is re-checked, never inherited.
- **No cached verdicts.** The vault is global and holds the previous pass's corpus. Every
  verdict-bearing source is re-fetched and the re-fetch noted.

## Next

Step 2 — width sweep. Academic APIs before web search, on every claim.
