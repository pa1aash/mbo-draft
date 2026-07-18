# Step 2 — Width Sweep (offline-mbo-novelty-audit-6d8cd4)

**Corpus: 38 vault notes (~34 grep-verified primary sources, full body text) + AAAI-27 topics page.**
8 fetcher subagents (5 local-text digesters A–E, 3 web agents W1–W3). Tooling reality: the CLI's
arXiv-PDF extraction fails here, and the arXiv/S2 APIs are flaky, so the corpus was built by
`curl → pdftotext → grep` with automatic title-match verification (guards against wrong-ID
fabrication). Two agents (C, E) hit API connection errors mid-run; their notes had landed and the
one true gap (Tan) was filled directly. Every verbatim quote from the first returned batch was
cross-checked against ground-truth text — no fabrication.

## Corpus by claim (all claims ≥3 grep-verified primaries)
- **N1 confound taxonomy:** Ferrari Dacrema (RecSys19), Balduzzi (NeurIPS18), Henderson (AAAI18), Musgrave (ECCV20), Lucic (NeurIPS18), Agarwal (NeurIPS21); + Islam (ICML17-ws), Machado (JAIR18).
- **N2 K-contingency:** Abe (NeurIPS22), Lakshminarayanan (NeurIPS17), Li/Rudner/Wilson (ICLR24).
- **N3 unmatched pessimism:** Ghasemipour "Why So Pessimistic?" (NeurIPS22), SNGP/DUE (σ-scale).
- **N4 distance-aware / implicit TR:** SNGP (NeurIPS20), DUQ (ICML20), DUE (2021), TuRBO (NeurIPS19).
- **N5 NTK/spectral bias:** Jacot (NeurIPS18), Rahaman (ICML19), Lee (ICLR18), Li/Rudner/Wilson (ICLR24), Abe (NeurIPS22).
- **N6 crossed factorial:** Design-Bench (ICML22), Chemingui/PGS (AAAI24), Tan/RaM (ICLR25), Kim survey (TMLR26), Li/Rudner/Wilson (ICLR24).
- **N7 bidirectional smoothness:** IGNITE (NeurIPS24), MS-DDEO (SWEVO22, closed-access), ROOT (NeurIPS25), Dao "surrogate sensitivity" (ICML24).
- **N8 platform/version dependence:** Gundersen & Kjensmo (AAAI18), Henderson (AAAI18), Nagarajan (2018), Islam (ICML17-ws), Machado ALE (JAIR18).
- **N9 audit-strengthens:** Recht (ICML19), Melis (ICLR18), Agarwal (NeurIPS21), Bressan (Front. Psychol. 2019).

## Provisional per-claim verdicts (to be stress-tested in steps 3–8)
| Claim | Provisional verdict | Load-bearing evidence |
|---|---|---|
| N1 | PRIOR WORK FOUND (the *shape*; Henderson owns it tightest) — residual = offline-MBO confound vocabulary + η²-net-UP | Henderson "implementation differences… can have dramatic impacts"; none run η² decomposition |
| N2 | **NONE FOUND** + tension | L/R/W's K=5-vs-10 ablation found the OPPOSITE (K-robust ranking) → our K-flip contradicts them |
| N3 | **NONE FOUND** (specific σ-across-classes) | Ghasemipour: "effectively optimistic" analog, but mechanism = target independence, not σ-scale |
| N4 | PRIOR WORK FOUND (distance-aware mechanism = SNGP); NONE FOUND for LCB-implicit-TR-in-offline-MBO synthesis | SNGP Def 1; TuRBO uses Thompson not LCB; DUE: GP not automatically variance-growing |
| N5 | (mechanism-objection: established) NTK→GP + spectral bias real → finite-width reading is supported | Jacot/Lee (∞-width→GP), Rahaman (spectral bias toward smooth) |
| N6 | **NONE FOUND** (strong) | 0 "factorial/ANOVA/crossed" hits across all 5 named; Kim survey NAMES the gap |
| N7 | **NONE FOUND** (strong) | IGNITE/MS-DDEO/ROOT/Boosting-sensitivity all one-directional; forward-cite sweep empty |
| N8 | PRIOR WORK FOUND (partial; Henderson/Nagarajan) — residual = offline-MBO + cross-platform axis + stated ratio | Henderson codebase-swap variance ≥ non-sig method effect; Nagarajan GPU-nondeterminism ≈ factors |
| N9 | **NONE FOUND within ML/CS** (exact shape) — partials: Recht (relative), Bressan (psychology) | No ML paper where audited headline EXCEEDS published value |

## Citation-date traps CONFIRMED during fetch
- Li/Rudner/Wilson = **ICLR 2024** (arXiv:2305.20028); Henderson = **AAAI 2018** (arXiv:1709.06560);
  Kim survey = **TMLR 2026** (arXiv v1 2503.17286 posted Mar 2025 — same trap pattern).

## Integrity notes
- W2 caught and REJECTED a fabricated "74–87% GPU-driven std" WebSearch summary (0 grep hits).
- MS-DDEO (SWEVO 2022) is closed-access — body NOT VERIFIABLE at sentence level (→ terminal section).
- Duplicates resolved: NTK raw-dump removed; Tan ×2 deprecated; Henderson kept ×2 (distinct N1 + N8 analyses).

Full search plan → `research/temp/search-plan.md`; corpus manifest → `research/temp/corpus-manifest.md`;
coverage check → `research/temp/coverage-gaps.md`; miss-catcher query logs →
`research/notes/miss-catcher-search-log-n2-n3-n6-n9-n1-residual.md`.
