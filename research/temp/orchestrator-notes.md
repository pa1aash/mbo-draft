# Orchestrator notes — mbo-gauntlet-r4-adversarial-0f06f1

## Step 2, wave 1 dispatch (10 fetchers)

| Batch | Theme | Why it exists |
|---|---|---|
| 1 | N6 kill hunt, 2026 frontier | Existential |
| 2 | Three near-misses: re-confirm AND extension-check | The extension half is what a re-audit skips |
| 3 | SNGP + sigma-as-error-signal contradiction | Suspect miscitation |
| 4 | Fan minUCB + LCB paralysis | Suspect sign/direction mismatch |
| 5 | Li/Rudner/Wilson + K-robustness-to-K=2 | Most dangerous pre-emption |
| 6 | Audit genre + the "audits shrink" premise | N9's single load-bearing citation |
| 7 | Shahriari doctrine + offline-MBO field | Over-disclaiming check |
| 8 | Elimination → mechanism experiments | Deliverable (iii) under-executed |
| 9 | Budget-matching norms + small-n statistics | Deliverable (iii) under-stated |
| 10 | Pessimism/conformal + inversion framing | Deliverable (iii) under-explained |

## Hypotheses forming before evidence returns

Recording these now so I can check later whether the evidence moved me or I moved the
evidence. Each is a prediction I can be wrong about.

**H1 — N6 survives, but the framing is the weak point, not the fact.** Nothing in my own
orchestrator-level sweeps (S2, arXiv, OpenAlex, ~15 queries across four scope widths)
surfaced a crossed factorial in offline MBO. The 2026 arXiv frontier in offline MBO is
dominated by diffusion/generative methods and ranking losses — method papers, not
decomposition papers. My prediction: CONFIRMED NONE-FOUND on the fact. The vulnerability is
that N6's residual has FOUR conjuncts (crossed × surrogate class × optimizer × two-way
decomposition, offline). A hostile reviewer calls that gerrymandering. The paper's defence
has to be that each conjunct is load-bearing rather than decorative — and I am not yet sure
all four are.

**H2 — the SNGP citation is inverted.** This is my strongest a-priori suspicion. SNGP's
thesis is that ordinary deep networks LACK distance awareness, which is the deficiency SNGP
was built to repair. The paper cites it to *bound* a claim that its ensemble's sigma IS a
distance signal. If SNGP says ensembles are not distance-aware, the citation is being used
against its own direction. Two possible outcomes: a genuine miscitation, or a defensible
"bounded by" reading that still needs rewording. Batch 3 decides.

**H3 — the Fan citation has a sign problem.** Fan et al. is *Minimizing* UCB in *local* BO.
The paper's LCB-paralysis mechanism is a *maximized* LCB that is locally maximal at the data.
Minimizing an upper bound and maximizing a lower bound are not the same operation, and the
paper asserts the transfer without arguing it. Also, the scope paragraph lumps Fan with SNGP
as owning "distance-aware uncertainty", which Fan almost certainly says nothing about. I
expect at least one mandatory fix here.

**H4 — melis2018sota does not support "audits normally shrink" as a general pattern.** Melis
is one paper about LM evaluation showing a tuned baseline matches newer architectures. That
is a RANKING reversal, not a corrected variance-explained scalar. The paper leans on it twice
for a claim about the direction of an entire genre. Even if no counterexample exists, the
premise is carried by a citation that cannot bear it. This may be the highest-yield finding
of the whole audit, because it undercuts the framing of contribution 2 without touching any
number.

**H5 — the budget axis is under-stated and it is the paper's best result.** It is the only
disjoint-interval separation in the entire paper, it changes which optimizer wins, and it is
buried mid-paragraph in a section led by beta. If the optimization-benchmarking community
(COCO/BBOB fixed-budget vs fixed-target) already formalises this, the paper is sitting on a
contribution to a named line and framing it as an aside.

## Hypothesis scoring (written after batches 3,4,5,6 returned; predictions were recorded before)

| | Prediction | Outcome | Verdict |
|---|---|---|---|
| H1 | N6 survives on fact; framing is the weak point | still open — B1/B2/B7/B11 out | PENDING |
| H2 | SNGP citation is inverted | **Confirmed, and stronger than predicted.** SNGP names deep ensembles as *not* distance-aware and that lack is its motivation; DUQ says so independently; all SNGP experiments are classification | **HIT** |
| H3 | Fan citation has a sign problem | **Confirmed, and it is three problems not one.** Also: their Theorem 1 proves *convergence*, so the paper cites a positive convergence result as authority for a failure mode | **HIT, understated** |
| H4 | melis2018sota cannot bear "audits normally shrink" | **Confirmed.** Ranking reversal, one instance, explicitly self-described as joining a line rather than stating a law | **HIT** |
| H5 | budget axis is under-stated and is the best result | pending B9 | PENDING |

Four for four on the ones that have returned. **That is a warning sign, not a comfort.** I
wrote these predictions from reading the paper and knowing the sources by reputation, and
the fetchers then confirmed all four. Two readings: either the defects were genuinely
visible from the paper's own text (plausible — miscitation of the SNGP/Fan kind shows up as
a mismatch between what a sentence needs and what a source of that title could supply), or I
briefed the fetchers toward my priors. I did tell each batch what claim was under audit and
what to check, which is confirmation-seeking by construction.

**Mitigation, applied:** the K=2 finding is the control. I did *not* predict it — I framed
batch 5 around the acquisition-fixed defence of N6 and listed the K-range check as one task
among six, expecting it to confirm the paper. It came back contradicting the paper instead,
on a point the paper states confidently. A briefed-toward-priors fetcher does not do that.
Similarly, batch 6 returned Maassen et al., which *weakens* a finding I was inclined to
credit. So the wave is capable of returning against the brief.

**Standing correction for later steps:** the critics in step 12 must be pointed at my
findings, not just at the draft, with an explicit instruction to attack the ones I predicted.

## The thesis that has emerged (written at end of step 2, before steps 3-9)

Recording this now so later steps can attack it rather than inherit it.

**The paper's evidence is sound and its scholarship is not.** Every quantitative claim I could
check against a repo artifact reproduced — four corner η² values and CIs, Elimination 1's
seven figures, both frozen-cell claims *to the seed* including "ten of sixteen", the inversion
counts across three surrogate classes, the `mbo.py` line traces, the engine stamps. One
integer recount is wrong. That is an extraordinarily clean record for a paper this
numerically dense.

Against that, **nine mandatory citation fixes**, of which two are severe:
- `demsar2006statistical` is cited for a "more than ten datasets" threshold **that does not
  exist in the paper**. A fabricated numeric warrant attributed to a real source.
- `fan2024minucb` is cited three ways, all wrong, and one of them **inverts the source's
  central theorem** — a convergence result cited as authority for a failure mode.
- `liu2020sngp` is cited to bound a claim SNGP's own Figure 1 contradicts.
- `li2024bnnsurrogates` — the K-range claim is simply false; they tested K=2.
- `abe2022ensembles` — runs no K-sweep at all.
- `melis2018sota` — one instance asked to certify a genre-wide law.

**This asymmetry is the report's most useful finding**, more useful than any single fix. It
tells the author exactly where the remaining pre-deadline hours belong: in related work and
scoping prose, not in re-running anything. And it means none of the nine fixes threatens a
result — every one of them can be fixed by rewriting a sentence.

**The one exception, and it is not a citation problem:** the RaM Table 3 near-miss. That is a
substantive scoping issue, because the closest crossed design in offline MBO sits inside a
paper the submission already cites, and the submission does not mention it. N6 survives on
three grounds, but all three have to be argued on the page.

**Where I might be wrong.** The strongest counter-reading is that I am grading scholarship
harshly because it is the easy thing to grade — citation checking is mechanical and always
yields hits, whereas the hard question (is the decomposition *right*?) resists a literature
audit. A reviewer who does not care about attribution would find this report beside the
point. Mitigation: deliverable (iii) has to carry real weight, not be a coda. The Xu et al.
extrapolation result and the budget-axis reframing are the two items that would change the
paper rather than merely correct it, and they should be ranked above the citation fixes in
the "stronger paper" section even though the citation fixes are mandatory.

## Risks I am tracking

- **S2 rate-limited early.** Both the REST endpoint and the MCP tool returned 429. arXiv and
  OpenAlex carried the load. If a verdict ends up resting on an S2-only result, that is a
  "could not verify" item, not a finding.
- **OpenAlex full-text `search=` is very noisy** on this topic — it returned climate models
  and echocardiography for optimization queries. Its null results are near-worthless as
  evidence of absence. arXiv field-scoped queries and forward-citation walks are the
  load-bearing instruments for N6, not OpenAlex keyword nulls. The N6 verdict must be honest
  that absence-of-evidence from a noisy index is weak.
- **Two agents (B2, B7) died mid-response on API errors.** Both are on load-bearing axes —
  B2 is the near-miss extension check, B7 is the Shahriari over-disclaiming check. Neither
  can be dropped; resuming both.
- **Fabrication risk is highest exactly where the answer is "none found".** A none-found is
  unfalsifiable from the inside. Every N6-adjacent verdict must carry its queries so the
  author can re-run them.
