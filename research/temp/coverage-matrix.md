## Coverage Matrix — query phrase → atomic item mapping

Run: `mbo-gauntlet-r4-adversarial-0f06f1`. Every significant noun phrase, proper noun,
technical term and category name in the verbatim query, walked in prompt order.

### Framing and tier

| Query phrase (verbatim) | Mapped atomic item(s) | Scope check | Gap? |
|---|---|---|---|
| "TIER: full. All 16 steps. Do not abbreviate." | `pipeline_tier: "full"` | OK — user-declared and binding, overrides classifier | No |
| "adversarial self-critique of a completed paper, not a novelty scout of an idea" | scope_conditions[0] | OK — findings must be actionable against a submission draft, not idea-stage | No |
| "completed AAAI-27 submission draft on offline model-based optimization" | Entity: main.tex / supplement.tex; scope_conditions[1] | OK — full scope, not narrowed to any one section | No |
| "the reviewer who does the homework the other reviewers won't" | response_format `argumentative`; scope_conditions[3] | OK — adversarial depth is the deliverable, not coverage | No |

### The three verbs of the task

| Query phrase (verbatim) | Mapped atomic item(s) | Scope check | Gap? |
|---|---|---|---|
| "critique EVERY claim against the primary literature" | Sub-Q "Across EVERY substantive claim… including uncited assertions, reported effect sizes, and the pre-registration outcomes" | OK — **broadened after first pass.** Initially narrowed to cited claims only; EVERY claim is wider than every citation | No (was YES) |
| "verify EVERY citation is used for what the cited paper actually says" | Sub-Q on every `\citep` key resolving + used-for-what-source-supports; Entity: references.bib (67 entries) | OK — full bibliography, not just the seven named | No |
| "hunt for any prior work that KILLS a load-bearing claim" | Deliverable (ii); Sub-Q on KILL against N6 or any ledger row | OK — "a load-bearing claim" is not only N6; ledger rows included | No |
| "find whether there is a stronger paper in this data that is not being written" | Deliverable (iii), all four candidate types | OK | No |
| "something unexplored, or explored but under-executed or under-explained" | Sub-Qs: unexplored / under-executed / under-explained; Entity "the unexplored paper" | OK — **broadened after first pass.** "Unexplored" is a FOURTH category the prompt names first; initial decomposition had only under-stated / under-executed / under-explained | No (was YES) |

### Named artifacts

| Query phrase (verbatim) | Mapped atomic item(s) | Scope check | Gap? |
|---|---|---|---|
| "paper/aaai27/main.tex and paper/aaai27/supplement.tex" | Entity: both artifacts, both read in bootstrap | OK — both, not just main | No |
| "docs/CLAIM_LEDGER.md" | Entity: ledger; Sub-Q on KILL against any ledger row | OK — 24 rows, all in scope | No |
| "docs/NOVELTY_V3.md — treat its verdicts as PRIOR, to be re-checked, not trusted" | scope_conditions "prior verdicts… are PRIOR, to be re-checked, not trusted" | OK — re-check, not inherit | No |

### N6 — the existential target

| Query phrase (verbatim) | Mapped atomic item(s) | Scope check | Gap? |
|---|---|---|---|
| "N6 … 'no prior work runs a crossed surrogate x optimizer factorial in offline MBO'" | Entity N6; Sub-Q 1 | OK — verbatim claim preserved | No |
| "Its failure is UNRECOVERABLE — the first contribution collapses" | scope_conditions "N6 is existential and takes priority" | OK | No |
| "Re-verify it against the live literature with fresh fetches" | scope_conditions vault-cache prohibition + FETCH PRIMARY AND GREP | OK — fresh fetch mandated, cached verdict prohibited | No |
| "a prior crossed/factorial surrogate x optimizer decomposition in offline MBO **or offline black-box optimization** (the exact thing)" | Sub-Q 1; scope_conditions[1] | OK — **BOTH readings carried.** Not narrowed to offline MBO alone; offline black-box optimization is a second, wider search target | No |
| "anything published SINCE the last audit (2026 especially)" | Sub-Q 2; time_horizons both entries; time_periods "2026" and "2026-07-18" | OK | No |
| "the field moves; a recent paper could have appeared" | time_periods "2026" publication-year sweep | OK | No |
| "Hutter fANOVA one-way" | Entity hutter2014fanova; Sub-Q 3 | OK — must re-confirm still one-way AND not extended | No |
| "Liang online" | Entity liang2021benchmarking; Sub-Q 4 | OK — must re-confirm still descriptive AND online | No |
| "Moosbauer HPO declining the two-way" | Entity moosbauer2022benchmarkdriven; Sub-Q 5 | OK — must re-confirm the decline stands and no successor ran it | No |
| "confirm each still only NEAR-misses and none has been extended" | Sub-Qs 3/4/5 each carry an "extended since?" required_field | OK — two-part test per near-miss | No |
| "CONFIRMED NONE-FOUND (with the queries) or KILLED (with the paper)" | required_formats "N6 verdict stated as…"; "exact queries run, listed verbatim" | OK — queries are part of the deliverable, not workings | No |

### Deliverable (i) — miscitation and contradiction

| Query phrase (verbatim) | Mapped atomic item(s) | Scope check | Gap? |
|---|---|---|---|
| "SNGP (liu2020sngp) for distance-aware uncertainty" | Entity liu2020sngp | OK | No |
| "Fan (fan2024minucb) for UCB-as-local-search / the LCB-paralysis framing" | Entity fan2024minucb | OK — both uses, the acquisition reading and the freeze framing | No |
| "Shahriari (2016) for the doctrine we scope against" | Entity shahriari2016humanoutoftheloop | OK | No |
| "Li/Rudner/Wilson (2024) for the cross-surrogate comparison" | Entity li2024bnnsurrogates + year trap field | OK | No |
| "Kim (2026) for the attribution-gap concession" | Entity kim2025mbosurvey + venue/year field | OK — bib key says 2025, prose says 2026; internal inconsistency flagged | No |
| "Agarwal + Demsar for the power argument" | Entities agarwal2021precipice, demsar2006statistical | OK — both | No |
| "A citation used for a claim the source doesn't support is a mandatory fix" | required_formats "for every mandatory item: … the required FIX" | OK | No |
| "does anyone show the ensemble's sigma IS an error signal, contradicting the distance-signal claim?" | Sub-Q 15 | OK — verbatim contradiction target | No |
| "does anyone show K-robustness DOWN to K=2, contradicting the K-sensitivity framing?" | Sub-Q 16 | OK — the DOWN-to-K=2 specificity preserved (L/R/W is K∈{5,10}) | No |
| "the claim, the paper's citation/framing, what the source actually says, and the required fix" | required_formats — four-field record per item | OK — all four fields | No |

### Deliverable (ii) — kills

| Query phrase (verbatim) | Mapped atomic item(s) | Scope check | Gap? |
|---|---|---|---|
| "Any prior work that refutes N6 **or any specific ledger claim**" | Sub-Q 19 | OK — not N6-only | No |
| "A single fatal counterexample matters more than a hundred improvements" | scope_conditions[3] | OK — ranking principle recorded | No |

### Deliverable (iii) — scope of novelty

| Query phrase (verbatim) | Mapped atomic item(s) | Scope check | Gap? |
|---|---|---|---|
| "RANKED" | required_formats "deliverable (iii) is RANKED, not merely enumerated" | OK | No |
| "FOLD-INTO-THIS-PAPER / FOLLOW-UP-PAPER / NOT-WORTH-IT" | required_formats tag set | OK — all three tags | No |
| "a claim the paper UNDER-states relative to its own evidence" | Sub-Q 21 | OK | No |
| "the budget-axis separation" | Entity "budget-axis separation" | OK — named candidate, not the only one admissible | No |
| "the two-strengthenings pattern" | Entity "two-strengthenings pattern" | OK | No |
| "are candidates — is either a bigger result than the paper frames?" | Entity required_field "is it bigger than its framing" | OK — candidates, so the hunt is not closed to these two | No |
| "the seven eliminations rule things out but reach no positive mechanism" | Entity "seven eliminations without positive mechanism"; Sub-Q 22 | OK | No |
| "a specific, runnable experiment the literature suggests would convert elimination to mechanism" | Entity required_fields "named runnable experiment" + "motivating literature" | OK — must be specific and runnable, and literature-motivated | No |
| "name the experiment and cite the work that motivates it" | required_formats | OK | No |
| "CHEAP (foldable before deadline) or EXPENSIVE (follow-up)" | required_formats CHEAP/EXPENSIVE sub-tag | OK | No |
| "a finding whose significance the paper states flatly and that the literature would let it frame more sharply" | Sub-Q 23; Entities x0-inversion (D25), frozen cells / LCB paralysis | OK | No |

### Method constraints

| Query phrase (verbatim) | Mapped atomic item(s) | Scope check | Gap? |
|---|---|---|---|
| "this project has caught fabrications — hold the line" | scope_conditions FETCH-PRIMARY-AND-GREP | OK | No |
| "Semantic Scholar / arXiv / OpenAlex BEFORE web search, every claim" | scope_conditions | OK — every claim, not just N6 | No |
| "FETCH PRIMARY AND GREP. Never a novelty or contradiction verdict from a snippet" | scope_conditions | OK — binds both verdict types | No |
| "Li/Rudner/Wilson is ICLR 2024 (S2 says 2023)" | time_periods ICLR 2024; Entity year-trap field | No |
| "Henderson is AAAI 2018 (S2 says 2017)" | time_periods AAAI 2018; Entity henderson2018matters | OK | No |
| "Benavoli is JMLR 2016 (arXiv 2015)" | time_periods JMLR 2016; Entity benavoli2016meanranks | OK | No |
| "Verify years." | Entity required_fields carry year checks | OK | No |
| "The vault at ~/.hyperresearch is GLOBAL and holds the previous pass's corpus — do NOT reuse a cached source for a verdict; re-fetch and note it" | scope_conditions vault-cache prohibition | OK — re-fetch AND note the re-fetch | No |
| "Every one of the 16 steps commits its own docs/hyperresearch/v3/NN_<step>.md" | scope_conditions | OK | No |

### Deliverable contract

| Query phrase (verbatim) | Mapped atomic item(s) | Scope check | Gap? |
|---|---|---|---|
| "docs/GAUNTLET_R4.md" | scope_conditions deliverable target | OK — note: sits outside `research/notes/`, which is why `citation_style` is `inline` not `wikilink` (wikilinks would not resolve from `docs/`) | No |
| "structured as the three deliverables above, N6 verdict first" | required_section_headings — 5 H2s, N6 first | OK — exactly these, no extra H2s invented | No |
| "For each mandatory item: the fix." | required_formats | OK | No |
| "For each ranked-novelty item: the tag." | required_formats | OK | No |
| "Commit continuously on a new branch gauntlet-r4, never to main" | scope_conditions | OK — branch created in bootstrap | No |
| "Authorship: Palaash Gang <palaashgang@gmail.com>" | scope_conditions | OK — verified on bootstrap commit d54a2b9 | No |
| "zero AI/agent/co-authored strings in any commit, file, or the report" | scope_conditions | OK — overrides the default commit trailer | No |
| "Terminal section: 'What I could not verify and why'" | required_section_headings[4], last | OK | No |

---

### Audit result

**Rows: 58. `Gap? = YES` after remediation: 0.**

Two gaps were found on the first pass and closed before this matrix was finalized:

1. **"critique EVERY claim"** was narrowed to cited claims only. EVERY claim is strictly
   wider — it includes uncited assertions, the reported effect sizes, and the
   pre-registration outcomes. A sub-question covering claims *independent of whether they
   carry a citation* was added.
2. **"something unexplored"** was dropped entirely. The prompt names four novelty
   categories, not three: *unexplored* / under-executed / under-explained, plus the
   *under-stated* hunt specified separately. A sub-question and an entity for the
   genuinely unexplored paper were added.

Both would have cascaded: gap 1 into a citation-only verification sweep that never checks
the paper's own numbers against the literature, gap 2 into a deliverable (iii) that only
ever critiques what the paper already attempted.
