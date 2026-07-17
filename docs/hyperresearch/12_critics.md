# 12 · Four adversarial critiques of the synthesis (`11_synthesize.md`)

Four independent adversarial reads, each in the role the full pipeline assigns
(dialectic / depth / width / instruction-adherence). Findings are numbered and severity-tagged
so the patcher (`14_patcher.md`) can consume them. A finding is **[material]** if it should change
the synthesis, **[note]** if it should be acknowledged but not necessarily patched.

Scope caveat inherited: this is a scoped synthesis, not a full run; critics judge the synthesis
against the repo evidence base, not against a freshly fetched corpus.

---

## Critic 1 — Dialectic (where it hedges, over-claims, or straw-mans counter-evidence)

- **D1 [material] — The Identity-C corollary is optimistic against the synthesis's own gate.**
  The synthesis names the yellow flag (ρ=+0.536 in the X1-ON corner) and then still closes with
  "commit to Identity C." `PAPER_V2_OUTLINE.md` states the harder truth outright: *"If X1 shows the
  gap was target scaling, neither A nor C exists as drafted."* The synthesis should carry the
  three-way branch (C survives / A-only / neither) with roughly equal weight, not fold the downside
  into "still a paper."

- **D2 [material] — Identity E is under-weighted given the deadline.** `AAAI27_VENUE.md` C.2 calls E
  "the honest fallback if the P0-0 re-run cannot be completed before the 2026-07-28 deadline" and "the
  only identity for which P0-0 is an asset rather than a fatal omission." With the grid PENDING and
  ~11 days to the full-paper deadline, E is not a footnote — it is the live contingency if the run
  does not clear. The synthesis mentions E only implicitly.

- **D3 [note] — "AAAI will publish this genre" inherits an unrestated ceiling.** `VENUE_NORMS.md`:
  *"AAAI reviews are not public. All phrasings are an ICLR/NeurIPS proxy."* The four precedents are
  real, but the reviewer-corpus bar ("null must diagnose its mechanism") is imported from ICLR/NeurIPS.
  The synthesis states the bar as if AAAI-native; it should flag the proxy.

- **D4 [note] — Over-reads a single partial corner.** The ρ=0.536 flag comes from one corner (on,on);
  the decisive X1-OFF vs X1-ON contrast is unrun. The synthesis is right to surface it but should not
  let it imply the confound is likely real *or* likely absent — it is undetermined.

---

## Critic 2 — Depth (technical substance the evidence supports but the synthesis skates)

- **DP1 [material] — "One de-confounding grid" silently absorbs the statistics fix, which is separate.**
  `FLAW_LEDGER.md` P1-2: the ANOVA is hand-rolled, has no error term, leaves `task` unmodeled, and the
  rank/CD/TOST matrix silently pools 11 cells (Benavoli's mean-rank-pool objection *instantiated*, not
  hypothetical). Fixing the confound (X1/X3) does not fix the inferential apparatus (mixed model /
  permutation effect size + unified normalization, ~4 h). The "single move" removes the confounds but
  not the statistics reject-route; the synthesis should say so.

- **DP2 [material] — X1+X3 do not earn the reversal by themselves.** `FLAW_LEDGER.md` P1-1: surrogate-
  *query* budgets are unmatched 6×–59×, with CMA starved on exactly the low-d tasks that carry the
  headline. X3 equalizes the *oracle/candidate* budget (P0-1), not the surrogate-query budget — a
  budget-matched optimizer arm is a *separate* experiment. So "run X1+X3 and the reversal is earned" is
  incomplete; η²_opt=0.01 is not fully de-confounded until the query-budget arm exists.

- **DP3 [note] — The X4 deliverable carries its own defense burden.** `EXTENSION_LEDGER.md` flags the
  tinyBenchmarks / "100 instances is all you need" inverse-framing trap (estimation efficiency for one
  score ≠ detection power for a contrast) that a reviewer can cite against X4, and that the quotable
  seed-count anchors are weak venues (cite AdaStop TMLR-2024 / Card EMNLP-2020, not the arXiv-only
  ones). The synthesis treats X4 as free of risk.

---

## Critic 3 — Width (acceptance-relevant topics the synthesis omits)

- **W1 [material] — The 7-page budget conflicts with Identity C.** `AAAI27_VENUE.md` C.5: the current
  draft already over-subscribes 7 pages (two grid tables, ANOVA table, controls table, an algorithm,
  two propositions, six figures — a >9-page layout compressed). Identity C *adds* content (bidirectional
  manipulation, the interpolation family, X6). The synthesis recommends "everything load-bearing in the
  body" without confronting that C must simultaneously *cut* (demote a grid table, Props→lemma/remark,
  β-sweep figure). Page discipline is an acceptance constraint, not a formatting detail.

- **W2 [material] — The COMs baseline divergence is a distinct Contribution-3 reject route.**
  `FLAW_LEDGER.md` P1-6 / `DECISION_QUEUE.md` D7: our COMs reproduces at 2.21 vs official 0.99 on
  TF-Bind-8 (the paper quotes a third value, 2.20), and the one "matches official" number fails to
  verify against its own row. "Their baselines are wrong, so the null is theirs, not the field's" is a
  reject route absent from the top-3 risks.

- **W3 [material] — The venue alternative (MLRC 2026) is unstated despite the PENDING gate.**
  `VENUE_NORMS.md` / `PAPER_V2_OUTLINE.md`: MLRC 2026 is an official NeurIPS track (via TMLR, hard
  deadline 2026-09-30) that explicitly welcomes negative results — a better fit for the A-shaped
  version and it buys the C program time. With the grid PENDING ~11 days from AAAI's deadline, a
  synthesis about acceptance should surface the fallback venue, not assume AAAI-27 or bust.

- **W4 [note] — The novelty phrasing constraint is unmentioned.** `NOVELTY_V2.md` D9: keep the
  "surrogate×optimizer" qualifier; drop the unqualified "first controlled decomposition" (fANOVA owns
  the method; Li/Rudner/Wilson owns the findings). The apparatus is NONE FOUND only in its narrow form.

---

## Critic 4 — Instruction-adherence (against the task spec and the query's own axes)

- **I1 [material] — The four query axes are not visible as structure.** The query names four evaluation
  axes — **manuscript, experiments, statistics, artifact**. The synthesis covers experiments (X1/X3)
  and artifact (checklist) heavily, statistics only glancingly (P1-2 absent), and manuscript-level
  findings (framing, prose, the Fig 1 vs Fig 3 integrity break P0-6, the backward sentence P0-7,
  related-work positioning) barely. The accept path should be legible across all four axes.

- **I2 [material] — Distinguish the highest-leverage acceptance move from the highest-leverage free
  move.** The synthesis picks the X1+X3+X2 run (correctly, as the P(accept)-gating move), but X4 is the
  highest-leverage *zero-cost* move and is identity-independent. The task asked for a single move; the
  synthesis should name the run as the gate *and* flag X4 as the free move that should run in parallel,
  so a reader under deadline pressure does the free thing immediately.

- **I3 [note] — Scoping and absent-memo disclosure: satisfied.** The synthesis is honest that this is a
  scoped pass and that memos 02–09 were absent at read time. Good; keep it.

- **I4 [note] — Corner ground-truth surfaced well.** Using `results/corners/analysis.json` as primary
  evidence (PENDING gate, reproduced headline, ρ flag) is the right move and is calibrated; retain.

---

## Patcher-facing summary

**Material findings to fold in:** D1 (three-way branch), D2 (elevate E as deadline fallback),
DP1 (statistics fix is separate), DP2 (query-budget arm separate from X3), W1 (page budget vs C),
W2 (COMs divergence as a risk), W3 (MLRC fallback venue), I1 (make the four axes legible),
I2 (name X4 as the parallel free move). **Notes to acknowledge:** D3, D4, DP3, W4, I3, I4.
