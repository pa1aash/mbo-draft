# Interim report: aaai-venue-fit-for-the-audit-genre

**Locus question:** Does an audit/decomposition paper with no proposed method survive AAAI
main-track review on its own terms, and does diagnosis-by-seven-eliminations read as a
contribution or as a null result?
**Flavor:** convergent

## What the corpus already said

Every venue claim in the paper's "genre-shape is prior work" paragraph was already
independently verified in the vault, each from full-text PDF extraction, before this locus
was opened:

- Henderson et al., "Deep RL that Matters" — **AAAI 2018**, arXiv:1709.06560
  [[deep-reinforcement-learning-that-matters-aaai-2018-arxiv170906560]]
- Agarwal et al., "Deep RL at the Edge of the Statistical Precipice" — **NeurIPS 2021
  Outstanding Paper**, arXiv:2108.13264
  [[210813264-deep-reinforcement-learning-at-the-edge-of-the-statistical-precipice]]
- Ferrari Dacrema et al., "Are We Really Making Much Progress?" — **RecSys 2019**,
  arXiv:1907.06902
  [[are-we-really-making-much-progress-a-worrying-analysis-of-recent-neural-recommen]]
- Musgrave et al., "A Metric Learning Reality Check" — **ECCV 2020**, arXiv:2003.08505
  [[200308505-a-metric-learning-reality-check]]
- Lucic et al., "Are GANs Created Equal?" — **NeurIPS 2018**, arXiv:1711.10337
  [[171110337-are-gans-created-equal-a-large-scale-study]]

A sixth genre instance the paper also cites (`melis2018sota`, in the abstract's
"corrected effect sizes shrink" claim) is Melis et al., **ICLR 2018**
[[on-the-state-of-the-art-of-evaluation-in-neural-language-models-iclr-2018-arxiv1]].
So the paper's own bibliography names **six** canonical genre instances: 2 NeurIPS, 1
ICLR, 1 ECCV, 1 RecSys, and exactly **1 AAAI** (Henderson, 2018). The vault also holds a
second, independent AAAI genre instance not cited by the paper — Gundersen & Kjensmo,
"State of the Art: Reproducibility in AI," **AAAI 2018**
[[state-of-the-art-reproducibility-in-artificial-intelligence-proceedings-of-the-a]] — but
it is a survey of documentation practices across 400 papers, not a decomposition/audit of
one method space, so it is a weaker structural match than the five true canonical
instances. Both known AAAI instances are from the same year, eight cycles ago.

The vault's AAAI-27 official areas-and-topics note
[[aaai-27-areas-and-topics-aaai]] already establishes the topic-keyword landscape and
flags the load-bearing tension: a paper's choice of primary topic keyword determines its
reviewer pool, and `ML: Evaluation, Benchmarking, Datasets & Analysis` summons a different,
more audit-sympathetic set of reviewers than `ML: Bayesian Learning & Uncertainty
Quantification` or `ML: Optimization for ML`.

Outside the vault proper, the repo's own planning document (`docs/PAPER_V2_OUTLINE.md`,
not a fetched source but a prior-session artifact worth citing because it independently
converges on part of this locus's answer) already flagged two things I verified
independently below: (1) "AAAI has **no** negative-results track," contrasted with an
official NeurIPS reproducibility track; and (2) the paper's own optimizer-axis null
(η²_opt small) locally falsifies the stated premise of Chemingui et al., "Offline MBO via
Policy-Guided Gradient Search" (PGS) — confirmed via `references.bib`: `chemingui2024pggs`
is **Proceedings of the AAAI Conference on Artificial Intelligence, 2024**. That is a
named, falsifiable belief held by a paper that appeared at the *same venue two years
earlier*, and the current draft only uses it as a scope-limiting aside, not as a framing
hook.

## What the new sources say

**AAAI-27 Main Technical Track Call** (fetched fresh, `aaai.org`)
[[aaai-27-main-technical-track-call-aaai]]. The operative review-criteria sentence:

> "All submissions will be evaluated and scored for the **significance and novelty** of
> the contributions (research problems or questions addressed, methods, experiments,
> analyses), theoretical and/or empirical soundness of the claims, their relevance to the
> AAAI community, and clarity of exposition."

Novelty and significance are **one bundled scoring dimension**, not two separate boxes —
there is no "Originality" rubric distinct from "Significance" the way NeurIPS separates
them (below). The page does explicitly permit non-method contributions — "contributions
may be theoretical, methodological, algorithmic, empirical, integrative... or **critical**
(e.g., principled analyses and arguments that draw attention to problematic choice of
goals, assumptions, or approaches)" — which is a genuine textual hook for an audit paper.
But it immediately follows with a stated preference:

> "Solid technical papers that explore **new territory** or point out new directions for
> research, introduce new problems, address research questions, or introduce methods that
> are of interest beyond a single sub-area of AI are **preferred to** papers that advance
> the state of the art, but only **incrementally**, or only within a narrow sub-area of AI."

No contribution-type-specific rubric exists for the main track (only the AI-for-Social-
Impact special track gets one, and it explicitly states it is judged "rather than simply
rewarding technical novelty" — implying, by exclusion, that the main track default *does*
reward it). So: an audit paper is licensed to exist at AAAI, but it is scored on the same
"new territory vs. incremental" axis as a method paper, by generalist ML reviewers with no
external signal telling them this genre is supposed to be judged differently.

**NeurIPS Evaluations & Datasets (E&D) 2026 Reviewing Guidelines** (fetched fresh,
`neurips.cc`; this is the track formerly named "Datasets and Benchmarks" —
[[call-for-datasets-benchmarks-2025]] is the stale-named CFP and is superseded by this
page for the actual rubric language)
[[evaluations-and-datasets-2026-reviewing-guidelines]]. This is the direct structural
counterfactual to AAAI's bundled criterion. Its rubric separates Quality, Clarity,
Significance, and Originality, and states plainly:

> "Originality **does not necessarily require introducing an entirely new method**.
> Providing novel insights, exposing failure modes, evaluating existing methods, or
> framing new metrics is equally valuable."

More important than the general statement is that the track enumerates a **named
contribution type matching this paper almost exactly**:

> "Reproducibility, Auditing, and Stress-Testing of Evaluations: Replication studies,
> auditing prior evaluations, stress-testing evaluation pipelines, robustness analyses of
> evaluation claims, meta-analysis of benchmarks."

with its own explicit per-dimension rubric:

> Significance: "The work yields meaningful insights about the robustness or limitations
> of existing evaluations. **Negative results are valuable when rigorously supported.**"
> Originality: "New insights from stress-testing or auditing existing evaluations,
> exposing failure modes, or demonstrating the limits of established evaluation
> practices."

And the sibling "Benchmark Design and Benchmark Analysis" type states: "Originality may be
achieved through novel task design, evaluation setup, or analysis that reveals properties
of existing benchmarks. **Beating a baseline is not required.**"

This is the concrete form of the asymmetry the query asked about. NeurIPS did not merely
tolerate this genre informally — it built a segregated track, trained a reviewer pool
against it, and wrote a rubric that pre-authorizes "negative results... when rigorously
supported" as sufficient for a high Significance score. AAAI's main track has no analogue:
the audit genre is a *topic keyword* inside one generalist track, not a *track* with its
own contribution-type rubric.

## Evidence synthesis

**(a) Venue accuracy.** All five named canonical instances check out exactly as claimed,
plus a sixth (Melis, ICLR 2018) the paper also cites for a related claim. The genre
paragraph is factually sound — no fix needed there. But the same exercise that verifies
the paragraph also exposes what it doesn't say out loud: of six cited canonical instances,
one is AAAI, and it is from 2018. The genre the paper claims membership in has its center
of gravity at NeurIPS/ICLR, not at the paper's actual target venue.

**(b) Elimination-without-mechanism, read against actual rubric text.** The paper's
mechanism section is explicit about its own status — "That is a diagnosis, not a mechanism
with a positive causal test behind it, and we label it as such" (Elimination 7 / "the gap
survives seven controls" passage in `main.tex`). Under the AAAI bundled novelty+
significance criterion with a stated preference against papers that are merely
"incremental," seven eliminations culminating in "none confirmed" is a genuine risk: a
generalist reviewer with no external signal that this genre is supposed to be judged
differently could read "we ruled out σ, width, budget, accuracy, roughness, coverage, and
distance-to-support, and don't have a positive account" as a paper that identified a
puzzle and failed to solve it, rather than as a rigorous negative result of the kind
NeurIPS E&D explicitly pre-authorizes ("negative results are valuable when rigorously
supported"). AAAI gives no such explicit pre-authorization; the paper must earn that
reading itself, unaided, inside a 7-page limit, from a reviewer who may be matched via a
topic keyword with no audit-specific expectations at all.

**(c) The framing fix, given what the paper already has.** I read the current abstract
and contributions list in `main.tex` directly (not secondhand): the paper already leads
with a positive reversal — "audits normally shrink [correction] moves it the other way...
strengthens it" — as contribution #2, ahead of the seven eliminations at #3. That is the
right instinct, already executed. But two stronger positive findings this audit surfaced
are **not** in the abstract or contributions list at all: the interaction term (η²_inter,
significant in all four operating-point corners, 9.2× more stable across corners than the
headline surrogate effect, and the empirical payoff of the crossed design the intro
explicitly argues for by citing Moosbauer's stated reason for declining OFAT) and the 7/7
raw-units finding that the GP's advantage over the ensemble attenuates by roughly 17×
under a weak/perturbation optimizer relative to gradient or CMA. Per `main.tex`,
"interaction" appears exactly once in the whole paper, as a parenthetical inside a related-
work sentence, and is never interpreted. This is the single highest-leverage, zero-cost
fix available: promoting an existing, already-computed, already-significant positive
result into the abstract changes what a reviewer's first three sentences of technical
content are. "We ran seven controls and none explain the gap" is a different first
impression than "surrogate and optimizer are not separable choices — which explains why an
established genre's one-factor-at-a-time designs could never have found this, and it
predicts a practitioner-facing rule: don't pair an ensemble surrogate with gradient
ascent." Both are honest. Only one reads as a contribution to a generalist scorer of
"significance and novelty."

There is a second, cheaper hook already sitting in the paper and currently undersold: the
optimizer-axis null locally falsifies a named, AAAI-venue premise (PGS, Chemingui et al.,
AAAI 2024 — "offline BBO has focused on improving surrogate models while using fixed
search strategies," i.e. the search axis is the neglected one). The current draft states
this only as a limiting scope remark ("falsifies the local premise of one recent paper...
and nothing wider"). Reframed as "a claim made by a paper at this venue two years ago is
directly measured and falsified by our factorial," it is a textbook instance of the
genre's actual accepted shape — Henderson, Musgrave, and Ferrari Dacrema all lead with a
named belief refuted, not with a decomposition offered cold. AAAI reviewers do not need
audit-genre familiarity to recognize "paper X claimed Y, we measured Y directly and it's
false" as a contribution; that argument form is venue-agnostic in a way "seven negative
controls" is not.

## Committed position

An audit-with-no-new-method paper can clear AAAI main-track review, but not on genre
recognition alone, because AAAI — unlike NeurIPS, which segregated exactly this
contribution type into a track with an explicit "negative results are valuable when
rigorously supported" rubric — folds novelty and significance into one bundled criterion
scored by generalist reviewers with a stated institutional preference for "new territory"
over incremental advances, and gives audit/reproducibility work no dedicated rubric to be
graded against. The paper's own genre paragraph is accurate but cannot do the persuading
by itself, because the genre's home institutions (NeurIPS ×2, ICLR ×1 among the six
instances cited) have trained reviewers who default-recognize the form; AAAI's ML-topic-
matched reviewers have no equivalent training. The fix is not to abandon the genre framing
but to stop relying on it and instead lead with the paper's least-genre-dependent,
most-novel-reading assets: (1) promote the interaction term and the 7/7 raw-units
"conditional GP advantage" finding into the abstract and contributions list, ahead of or
interleaved with the seven eliminations, so the mechanism section's positive payoff is
read before its negative residue; and (2) reframe the PGS/AAAI-2024 falsification from a
scope-limiting aside into an explicit "named belief, refuted" hook, since that argument
form requires no genre familiarity to register as a contribution. Both changes are free —
zero new computation, numbers already exist in the paper's own tables — and both target
the specific AAAI risk this locus was opened to check: a bundled novelty+significance
score assigned by a reviewer who has never been told, by the venue itself, that this genre
gets a different bar.

Applying the report's own tagging convention to this locus's findings:

- **FOLD-INTO-THIS-PAPER:** Promote the interaction term (η²_inter, all-corner
  significance, 9.2× cross-corner stability) into the abstract/contributions as an
  explicit positive finding, not a once-mentioned table column. Zero cost.
- **FOLD-INTO-THIS-PAPER:** State the 7/7 raw-units conditional-optimizer finding
  (~17× attenuation of the GP advantage under perturbation) as a named, practitioner-
  facing claim in the contributions list, with the floor-effect caveat already tested
  elsewhere in this audit. Zero cost.
- **FOLD-INTO-THIS-PAPER:** Reframe the PGS/`chemingui2024pggs` (AAAI 2024) falsification
  from the Scope paragraph's limiting aside into an explicit "named belief at this venue,
  refuted by our factorial" sentence near the top of the intro or contributions. Zero
  cost, one sentence.
- **FOLD-INTO-THIS-PAPER (mechanical, free):** Select `ML: Evaluation, Benchmarking,
  Datasets & Analysis` as the AAAI-27 primary topic keyword rather than `ML: Bayesian
  Learning & Uncertainty Quantification`, per the venue-fit note's own reviewer-matching
  logic [[aaai-27-areas-and-topics-aaai]] — this is the only lever available at AAAI for
  approximating what NeurIPS achieves with a segregated track and an explicit rubric.
- **NOT-WORTH-IT:** Do not add meta-commentary citing AAAI's own CFP language ("critical
  contributions," "significance and novelty") into the paper itself. It reads as reviewer-
  gaming and the argument is stronger made on the merits than made by citing the rubric
  that will judge it.
- **FOLLOW-UP-PAPER (real, out of scope for this submission):** Whether AAAI's audit-
  genre acceptance rate has changed since the two 2018 instances is a genuinely open,
  answerable question (search AAAI proceedings 2019-2026 for audit/reproducibility-shaped
  accepted papers) that this locus's 2-source budget did not permit resolving, and that
  would meaningfully sharpen future submission-venue decisions for this research group.

- **Position:** The paper's genre-membership framing is necessary but insufficient at
  AAAI specifically; the decisive lever available before the deadline is promoting the
  two positive, already-computed findings (interaction term; conditional GP advantage)
  and the named-belief-refuted framing (PGS/AAAI-2024) ahead of the seven eliminations,
  not defending or restructuring the elimination section itself.
- **Confidence:** medium-high. High confidence on the facts (venue confirmations, exact
  rubric quotes, bib verification) — all directly fetched/grepped, none inferred. Medium
  confidence on the causal claim that this reframing would materially change a real AAAI
  reviewer's score, since that rests on inference from stated criteria and general genre
  patterns (Henderson/Musgrave/Dacrema all lead with a named-belief-refuted structure),
  not on a controlled test of actual AAAI review behavior.
- **Boundary conditions:** This holds for AAAI's **main technical track** under its
  current (AAAI-27) published call. It does not necessarily hold for AI-for-Social-Impact
  or other special tracks, which have their own, different rubrics, nor does it
  generalize to venues with a segregated audit/benchmark track (NeurIPS E&D, and likely
  similar tracks at ICML/ICLR), where the genre-recognition argument alone would likely
  suffice.
- **What would change this position:** A documented run of AAAI main-track papers from
  2023-2026 that are structurally audit/decomposition papers (no new method) and were
  accepted without a positive-finding reframing would show the bundled-criterion risk is
  smaller in practice than the rubric text implies — this is exactly the FOLLOW-UP-PAPER
  question above, and I could not check it inside a 2-source budget. Conversely, if the
  orchestrator's other loci find that the interaction term or the conditional-optimizer
  finding do not survive further scrutiny (e.g., the normalization-artifact challenge
  referenced in `findings-so-far.md` fully invalidates the interaction, or the floor-
  effect confound is not disentangled), the "lead with positives" recommendation would
  need to fall back to the PGS-falsification hook alone, which is weaker but still
  venue-agnostic.
- **Evidence weight:** 2 fetched primary sources (AAAI-27 CFP, NeurIPS E&D 2026
  guidelines) directly quoted; 6 vault-verified venue confirmations (5 from the paper's
  own citations plus Melis); 1 bib-verified venue fact (chemingui2024pggs = AAAI 2024);
  1 prior-session planning artifact (`docs/PAPER_V2_OUTLINE.md`) independently converging
  on the same "reversal not a null" and "no negative-results track" observations before
  I verified them against primary sources. No source in this set contradicts the
  synthesis; the only genuine gap is the FOLLOW-UP-PAPER question above.

## Open questions

- Has AAAI's main-track acceptance rate/pattern for audit-shaped papers (no new method)
  changed since 2018? Henderson and Gundersen & Kjensmo are both from AAAI-18; a search of
  2023-2026 AAAI proceedings for similar papers was out of scope at this locus's budget.
- Does the interaction term survive the normalization-artifact challenge raised elsewhere
  in this audit (`findings-so-far.md`, "THE DIALECTICAL CHALLENGE")? If it does not
  survive in its current η² form, the "promote to abstract" recommendation would need to
  be restated in the raw-units/`tab:cross` form instead, which this note's synthesis
  already flags as the more robust alternative.
- Whether AAAI reviewer-bidding behavior actually differs by primary-topic-keyword choice
  in practice (as opposed to in the stated matching-guidance text) was not testable within
  this locus's budget; the recommendation to choose `ML: Evaluation, Benchmarking,
  Datasets & Analysis` as primary rests on the venue's own stated matching logic, not on
  an empirical study of reviewer assignment outcomes.

## Sources

1. [[aaai-27-main-technical-track-call-aaai]] — AAAI-27 Main Technical Track Call
   (aaai.org, fetched fresh this locus) — verbatim review-criteria and preference-statement
   quotes.
2. [[evaluations-and-datasets-2026-reviewing-guidelines]] — NeurIPS Evaluations and
   Datasets 2026 Reviewing Guidelines (neurips.cc, fetched fresh this locus) — verbatim
   novelty-optional policy and the "Reproducibility, Auditing, and Stress-Testing of
   Evaluations" contribution-type rubric.
3. [[call-for-datasets-benchmarks-2025]] — NeurIPS Call for Datasets & Benchmarks 2025
   (secondary/superseded — stale track name, gestures at but does not quote the
   track-specific rubric; fetched incidentally while locating source 2).
4. [[aaai-27-areas-and-topics-aaai]] — AAAI-27 Areas and Topics (vault, prior session) —
   topic-keyword landscape and reviewer-matching guidance underlying the primary-topic
   recommendation.
5. [[deep-reinforcement-learning-that-matters-aaai-2018-arxiv170906560]] — Henderson et
   al., AAAI 2018 — venue confirmation.
6. [[210813264-deep-reinforcement-learning-at-the-edge-of-the-statistical-precipice]] —
   Agarwal et al., NeurIPS 2021 Outstanding Paper — venue confirmation.
7. [[are-we-really-making-much-progress-a-worrying-analysis-of-recent-neural-recommen]] —
   Ferrari Dacrema et al., RecSys 2019 — venue confirmation.
8. [[200308505-a-metric-learning-reality-check]] — Musgrave et al., ECCV 2020 — venue
   confirmation.
9. [[171110337-are-gans-created-equal-a-large-scale-study]] — Lucic et al., NeurIPS 2018
   — venue confirmation.
10. [[on-the-state-of-the-art-of-evaluation-in-neural-language-models-iclr-2018-arxiv1]]
    — Melis et al., ICLR 2018 — sixth genre instance cited in the paper's abstract, venue
    confirmation.
11. [[state-of-the-art-reproducibility-in-artificial-intelligence-proceedings-of-the-a]]
    — Gundersen & Kjensmo, AAAI 2018 — second (weaker-match) AAAI genre instance, not
    cited by the paper.
