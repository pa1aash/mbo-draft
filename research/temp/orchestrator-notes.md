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

## Tension to resolve in step 6 (cross-locus reconcile)

**Locus 6 (AAAI venue fit) recommends promoting the 7/7 raw-units finding into the abstract,
ahead of the seven eliminations. I downgraded that finding an hour later, after testing the
floor-effect alternative and finding it survives.**

The investigator was working from `findings-so-far.md` as it stood before my downgrade, so this
is a genuine sequencing artifact, not an error on its part. Step 6 must reconcile rather than
silently prefer one.

**My provisional resolution, to be tested in step 6:** the venue argument is sound and its
*direction* survives the downgrade — leading with a positive result rather than seven negatives
is right regardless of which positive result leads. But the specific item promoted should be
the **interaction term**, not the 7/7 attenuation:

| | Interaction η² | 7/7 raw-units attenuation |
|---|---|---|
| Significant | yes, all four corners, CI excludes zero | descriptive only, no intervals |
| Survives bias correction | yes (0.134–0.156) | n/a |
| Survives normalization challenge | **no** — rides on min–max | **yes** — raw oracle units |
| Survives floor-effect challenge | **yes** — unaffected | **no** — Styblinski points the wrong way |

Each survives the challenge the other fails, which is why they should be reported **together**
and neither alone: the interaction establishes that the effect is real and significant, the
raw-units analysis shows what it consists of in units immune to the normalizer critique, and
the floor-effect confound is disclosed as the open question it is. That is a defensible package;
either half promoted alone is an overclaim.

Also actionable and cost-free from locus 6: AAAI-27's main track bundles novelty and
significance into one scored criterion with **no audit/reproducibility rubric**, whereas
NeurIPS's Evaluations & Datasets track has a named "Reproducibility, Auditing, and
Stress-Testing" contribution type that pre-authorises negative results. So the paper's
genre-membership framing is **necessary but not sufficient** at this venue — which raises the
stakes on leading with something positive.

## NEAR-MISS: the global-vault trap almost caught me, on the exact axis the query warned about

I set a background waiter for "six `interim-*` notes exist", it fired, and I began reading
committed positions. **Six of the seven files were stale interim notes from the PRIOR audit
run** — `n3-classic-bo-beta-calibration`, `n4-sigma-mechanism-scope-and-ovadia`,
`n7-roughening-beyond-offline-mbo`, `k-and-finite-width-artifact-vs-class-property`,
`audit-strengthens-and-n9-integrity`, `optimizer-reversal-unearned-and-candidate-a-credit`.
Only `aaai-venue-fit` was from this run.

Their committed positions are *seductively relevant* — they discuss N9's integrity, the K/width
question, σ mechanism scope, N7's roughening gap. Read carelessly, I would have reconciled the
**previous pass's verdicts** into this run's step 6 and presented them as freshly established.
That is precisely the failure the query's method constraints forbid: *"The vault at
~/.hyperresearch is GLOBAL and holds the previous pass's corpus — do NOT reuse a cached source
for a verdict; re-fetch and note it."*

**What caught it:** the filenames follow the prior run's `nN-` claim-numbering convention rather
than this run's locus names, which did not match the six loci I dispatched. Checking the tag
confirmed it.

**Fix applied:** every waiter and every read now filters on
`grep -l 'mbo-gauntlet-r4-adversarial-0f06f1'`, not on a filename glob. The vault-tag exists for
exactly this reason and I had stopped using it.

**Worth reporting in the deliverable's methodology note.** The instruction to distrust the prior
pass has now paid for itself twice: once when RaM Table 3 turned out to have been missed by
three prior fetches of the same paper, and once here.

## Synthesis planning (written during step 10, before the drafts return)

### The thesis the final report should commit to

**Sound evidence, unsound scholarship — and the asymmetry is the actionable finding.** Twelve
mandatory fixes; eleven concern what a *source* says; **none** concerns a number the paper
computed. Every quantitative claim checkable against a repo artifact reproduced, including two
frozen-cell claims to the seed. That tells the author exactly where the remaining hours go:
related-work and scoping prose, not re-running anything.

Draft A will press the defects, Draft B will press the verification, Draft C will price them.
The synthesis should take **C's frame** — a priority ordering — while retaining **A's severity
grading** on the two genuinely serious items (the Demšar fabrication, the Fan inversion) and
**B's insistence** that severity be graded by what a fix costs the *results*, which is nothing.

### Argumentative beats the final report must commit to, not gesture at

1. **N6: CONFIRMED NONE-FOUND, with the Elsayed & Lacor lead named inside the verdict.** A
   none-found that conceals its one unchecked lead is not a none-found. State the three surviving
   grounds, state that ground (2) was falsified on contact, state the queries.
2. **The Demšar threshold does not exist, and removing it *helps* the paper** — he recommends
   Friedman *because* n is small. The paper is conceding a weakness it does not have.
3. **The Fan citation inverts a convergence theorem into a failure mode**, and the fix costs
   nothing because the paper's own frozen-cell evidence is stronger than the borrowed authority
   — though it now owes Yarotsky (2013) a scoping sentence.
4. **The interaction is the buried result**, with the boundary-condition table showing why it and
   the raw-units analysis must be reported together.
5. **Bias correction strengthens the headline** (0.351→0.395), and the correction to name is ε²
   not ω².
6. **The multiplicative-mechanism constraint** — the one positive structural statement, visible
   only in cross-section.

### Things the synthesis must NOT do

- **Must not re-inflate the five withdrawn claims.** The conformal proposition is formally
  correct; RaM's characterisation is incomplete not false; the 7/7 attenuation has a live
  floor-effect confound; Griewank is the *smallest* normalization lever; "nobody owns
  acquisition-stalling" is withdrawn in favour of Yarotsky.
- **Must not present relay-only findings as first-hand.** Mark the two venue-unverified citations
  (Dao, Ghasemipour) as such.
- **Must not bury the audit's own error rate.** Five self-corrections and two subagent
  fabrications caught belong in the methodology note — a report about citation fidelity that
  hides its own misses has no standing.

### Where the drafts will likely conflict, and how to resolve

- **Severity of the citation defects.** A will call them severe, B cosmetic. Resolve by
  distinguishing *severity to the reader's trust* (high — a fabricated threshold is the worst
  class) from *severity to the results* (nil). Both are true and the report should say both.
- **Whether to promote the interaction to the abstract.** Locus 3 says main text, ~65%
  confidence; locus 6 says abstract. Resolve toward main text with the synthetic-grid scoping,
  since Design-Bench η²_inter is an order of magnitude smaller and an unscoped abstract claim
  would be the same overreach the audit criticises elsewhere.
- **How hard to push the "stronger paper" framing.** C will push hardest. Keep it, but the
  ranked section must stay honest that the strongest candidate (the raw-units attenuation) has an
  unresolved confound.

## What the step-12 critics must be pointed at (written while the synthesizer runs)

The default critic brief attacks the draft. That is not enough here, because the draft's most
likely failure mode is **inheriting my errors**, not making new ones. I predicted four of four
early findings correctly, which I flagged at the time as a warning sign rather than a comfort.
The critics must be pointed at *my* positions, with an explicit instruction to attack the ones I
was most confident about.

### Specific things to attack, ranked

1. **The five withdrawn claims — check they stayed withdrawn.** The synthesis brief forbids
   re-inflating them, and a re-inflation is the single most likely defect because the withdrawn
   versions are more dramatic. Check specifically: the conformal proposition is described as a
   *scoping omission*, not a missing hypothesis; RaM is *incomplete*, not false; the 7/7
   attenuation carries its floor-effect confound; Griewank is named as the *smallest* lever;
   Yarotsky is credited as closest prior art for acquisition-stalling.

2. **The interaction finding — is it over-promoted?** Three independent routes converged on it,
   which is exactly the condition under which I would over-weight something. It is
   synthetic-grid-specific (Design-Bench 0.006–0.041), rides on min–max, and survives the
   floor-effect challenge only because it is a different quantity from the raw-units analysis.
   A critic should test whether the report's enthusiasm exceeds that evidence.

3. **The severity split — is it a dodge?** I instructed the synthesizer to report both "high to
   reader trust" and "nil to results". A hostile reading is that this lets the report have it
   both ways. Test whether the split is doing analytical work or providing cover.

4. **N6's three grounds — is the residual gerrymandered?** One ground was falsified on contact.
   The other two now carry all the weight, and one of them (loss type ≠ model class) rests on a
   single domain citation (Abdar 2021) plus an η² I computed once from RaM's table without a
   second implementation. That is thinner than the confident verdict suggests.

5. **Citation count discipline.** The report recommends adding roughly fifteen citations. Every
   one needs an identifier, and the two venue-unverified ones (Dao, Ghasemipour) must be marked.
   A report about citation fidelity that ships a bad citation is self-refuting.

6. **Did the passes survive?** Constraint 4 requires reporting Shahriari, Chemingui, Dewolf and
   the three year traps as passing. If the synthesizer dropped them for length, the severity
   grading loses its calibration and the report reads as an indictment.

### The failure mode I most expect

**Length.** Inputs were 11k–15.6k words against a 7–8k target. The compression has to come from
somewhere, and the first things a synthesizer cuts are the qualifications — which here are
load-bearing. If the report is 8,000 words of confident findings with the caveats trimmed, it is
worse than a 10,000-word report that keeps them.

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
