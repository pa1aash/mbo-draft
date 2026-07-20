# Step 16 — Readability audit + ship

Run `mbo-gauntlet-r4-adversarial-0f06f1` · branch `gauntlet-r4` · 2026-07-20

**21 recommendations. 9 applied (all high-severity), 12 declined.** 19,890 → 19,937 words (+47,
list markers and table scaffolding). Nothing cut.

Applied by exact-substring Edit with a uniqueness check — every anchor had to match exactly once
before replacement. **All nine matched exactly once; zero skipped.**

The load-bearing one is the r2+r3 pair, applied together as required: RANK 1's "Four reasons it
is major rather than technical" was a single ~1,900-character paragraph carrying the strongest
promotion case in the deliverable, and was the least scannable passage in a document the author
must triage under deadline. Now bullets, with zero wording change.

The 12 declined are paragraph breaks and sentence splits in already-navigable passages; applying
them would add churn to a document already through a patcher and two polish runs.

## The recommender's scope judgements, accepted

It checked and deliberately did **not** flag the two things most worth checking: the twelve
mandatory items in (i) already carry a consistent four-field shape (eleven of twelve open with a
bolded claim, all twelve close with a bolded **Fix**), and all twenty-one ranked items already
carry their contract tag bolded in the lead sentence. Triage was already solid. The one exception
— a `NOT-WORTH-IT` block holding five decisions in flat prose — became r6.

## Final integrity gate

| Check | Result |
|---|---|
| Four critic findings JSONs | present |
| patch-log / polish-log / readability-recommendations / readability-decisions | present |
| H2 structure | 5 required verbatim and in order, + Sources |
| Citations | **102 cited / 102 listed, zero orphans, zero gaps** |
| YAML frontmatter | absent |
| Pipeline vocabulary | **0** |
| AI / agent / authorship strings | **0** (report and all 58 commit messages) |
| Contract tags in (iii) | 26 |
| CHEAP / EXPENSIVE tags | 27 |
| "venue unverified" retained | 5 |
| Falsification records | 12 |
| Commit authorship | Palaash Gang <palaashgang@gmail.com>, sole author, 284 files |

## The two lint errors are false positives — verified, not dismissed

`hyperresearch lint` returns 169 issues, 2 at error severity. Both are matcher artifacts:

**`locus-coverage`: "6 of 6 loci have no interim note."** All six exist. The linter does not
recognise the `interim-report-<locus-name>` naming convention; each file was confirmed present by
direct filesystem check against `loci.json`.

**`instruction-coverage`: "20 atomic entities missing from the final report."** All are covered.
The linter searches for literal bibliography keys; the report covers them by name — SNGP appears
6 times, Fan 21, Li/Rudner/Wilson 228, Kim 7. Most bib keys appear too (`liu2020sngp` ×2,
`fan2024minucb` ×2, `li2024bnnsurrogates` ×3).

Checked rather than waved through, because "the linter is wrong" is exactly the claim an audit
should be made to prove.

## Shipped

`docs/GAUNTLET_R4.md` — byte-identical to the vault copy, 19,937 words, 137,335 chars.
