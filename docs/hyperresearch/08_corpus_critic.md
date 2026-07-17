# 08 · Corpus critic — what source, if found, would overturn the direction?

**Step 8 of the research core.** The adversarial question: given the current corpus and the committed
positions (05), *what source, if it existed, would flip a load-bearing conclusion?* This is the
highest-leverage pre-draft intervention — a missing source found now costs nothing; found by a reviewer it
costs the paper. Each entry states the claim it would overturn, whether it plausibly exists, and whether it
was fetchable this session.

**Scope honesty.** This is a single-pass corpus critique, not a spawned corpus-critic subagent with a
fetch wave. Where a gap is fetchable and high-value, I say so and flag it for the parent to close; I did
*not* run those fetches (they are outside the eight-file deliverable and some hit Semantic Scholar rate
limits this session).

---

## GAP 1 — An NTK / spectral-bias citation grounding "wide nets are smoother than GPs are rough" · **HIGH leverage · fetchable**

**What it would overturn / secure.** L3's committed position leans on "the GP's smooth Matérn mean vs the
ensemble's jagged mean" but the corpus grounds this only at the IGNITE/MS-DDEO level ("smoothness helps"),
not at the mechanism level ("wide nets are spectrally biased toward low frequencies; here is the relation
to a GP prior"). A reviewer in ML: Bayesian Learning would ask for it. **The missing sources are canonical
and almost certainly exist:** Jacot, Gabriel, Hongler — *Neural Tangent Kernel* (NeurIPS 2018); Rahaman et
al. — *On the Spectral Bias of Neural Networks* (ICML 2019); Lee et al. — *Deep Neural Networks as GPs*
(ICLR 2018). **Risk if not found:** the smooth-mean mechanism reads as asserted, not grounded — this is the
single most valuable missing fetch (`04` L3, `05` L3 both flag it).
**Fetchable:** yes, trivially (arXiv + Semantic Scholar). **Recommend the parent fetch before drafting §2.**

**Adversarial twist.** The NTK literature could also *cut against* the paper: infinite-width nets *are* GPs,
and finite ensembles approximate a GP posterior — so "ensemble mean is jagged" is a finite-width /
under-training artifact, not an intrinsic surrogate-class property. If that reading holds, it reinforces
P0-2 (the gap is an implementation artifact) rather than the paper's mechanism. Finding this source is
double-edged and must be engaged either way.

---

## GAP 2 — A published controlled surrogate×optimizer factorial in offline MBO · **DECISIVE leverage · fetchable, likely absent**

**What it would overturn.** The paper's cleanest novelty claim (A1: "first controlled surrogate×optimizer
factorial in offline MBO," **NONE FOUND**). If any prior work crosses the two axes as a control, the
apparatus contribution collapses and the paper is left with only owned findings.

**Current status.** Searched across Semantic Scholar, Consensus, WebSearch in prior passes (`NOVELTY_V2.md`
A1) — the three nearest works each verified *not* to run the cross (Li/Rudner/Wilson fix the acquisition;
Tan varies the surrogate as a method; Chemingui varies the optimizer as a method). **Fetchable:** yes;
targeted queries ("factorial ANOVA surrogate optimizer offline optimization," "decompose surrogate vs
acquisition offline MBO") would re-confirm. **Recommend one more adversarial sweep** because this claim is
load-bearing and a single counterexample is fatal. Highest-value *confirmatory* fetch.

---

## GAP 3 — A paper showing target normalization does *not* change surrogate rankings · **HIGH leverage · fetchable**

**What it would overturn.** L2's committed position is that P0-2 (raw vs z-scored targets) plausibly
explains the whole η²_surr gap. If a source showed that ensemble-vs-GP rankings are *robust* to target
normalization on comparable regression benchmarks, the crippling objection weakens and the paper could
argue the gap is real even before the re-run. Conversely, a source showing normalization *flips* rankings
(likely — Tan et al. discuss z-scoring's effect on regression surrogates, `NOVELTY_V2.md` D3) strengthens
the objection. **Fetchable:** yes. **But note:** no external source substitutes for actually running X1 —
this gap is best closed by the experiment, not the literature (`05` L2). Fetch is secondary.

---

## GAP 4 — Empirical acceptance data on AAAI measurement/null papers (rates, not anecdotes) · **MEDIUM leverage · partly fetchable**

**What it would overturn / secure.** L1 rests on four AAAI precedents + an ICLR/NeurIPS reviewer proxy.
A source with *AAAI-specific* acceptance statistics for the measurement genre would upgrade the venue
judgment from "viable by precedent" to quantified. **Reality:** AAAI reviews are private and no such
statistic is known to exist (`VENUE_NORMS.md` method-ceiling caveat). The one nearby study
(arXiv:2511.15462 on review criteria) was caught fabricating novelty percentages in search summaries —
its only *verified* finding is that novelty criticism is the #1 predictor of review rating (an importance
weight, not a frequency). **Fetchable:** the paper is fetchable but must be grepped, not trusted from
snippets (four fabrications were caught this way — `VENUE_NORMS.md`). **Recommend: do not chase a rate that
likely does not exist; treat the proxy as the ceiling.**

---

## GAP 5 — A source establishing the smooth-mean mechanism is already *published* for the GP-vs-ensemble gap · **HIGH leverage · fetchable**

**What it would overturn.** L3 / `NOVELTY_V2.md` C2 rate bidirectional smoothness manipulation as the
paper's single most novel move (NONE FOUND). If a paper already attributes the GP's offline-MBO advantage
*specifically to mean smoothness* via manipulation, the mechanism contribution is a restatement and
Identity C loses its core. **Current status:** searched (IGNITE/RoMA/MS-DDEO neighborhoods) — none manipulate
smoothness bidirectionally to *identify* it as the causal axis of a surrogate-class gap. **Fetchable:** yes;
one more sweep of the IGNITE/MS-DDEO forward-citation graph (papers citing them in 2025–2026) is the place a
scoop would hide. **Recommend the parent run this forward-citation check** — it is the mechanism analogue of
GAP 2.

---

## GAP 6 — A contemporaneous conformal-for-offline-MBO paper that scoops the coverage diagnostic · **MEDIUM leverage · partly fetched**

**What it would overturn.** The premise-coverage diagnostic (Contribution's instrument). `NOVELTY_V2.md` C4
already found Choi (arXiv:2606.15217, 2026) is contemporaneous and same-setting — "attaches a calibrated
one-sided lower bound … standard conformal … collapses to 0.416 coverage." That is close enough to be a
concurrency risk. Stanton (AISTATS 2023, fetched) and Fannjiang (PNAS 2022) own ~70% of the
coverage-as-validity idea. **Fetchable:** Choi and Stanton are fetchable; the diagnostic should be
positioned as a *diagnostic within a decomposition*, not a novel conformal method (which would lose to
Stanton/Choi). **Recommend: cite Choi as concurrent, scope the claim to the diagnostic's use, not its
theory.**

---

## GAP 7 — A source showing Design-Bench oracles are *reliable* (would defuse the competing hypothesis for free) · **MEDIUM leverage · likely absent**

**What it would overturn.** L4's whole problem is the free "broken oracles" competing explanation. A source
validating Design-Bench oracle fidelity would neutralize it. **Reality:** the literature runs the other way
— the field *believes* the oracles are limited (`VENUE_NORMS.md`), and Design-Bench's own authors excluded
tasks as non-discriminative. **No such defusing source is expected to exist.** The paper cannot outsource
this to the literature; it must run X11 (exact-oracle subset). **Fetchable:** the absence is itself informative.

---

## Summary — the three fetches worth doing before drafting

| Priority | Gap | Why | Effort |
|---|---|---|---|
| 1 | **GAP 1** (NTK / spectral bias) | Grounds the mechanism a UQ reviewer will demand; double-edged so must be engaged | Trivial — arXiv/S2, 3 canonical papers |
| 2 | **GAP 2** (surrogate×optimizer factorial) | Load-bearing novelty claim; one counterexample is fatal | One adversarial sweep to re-confirm NONE FOUND |
| 3 | **GAP 5** (bidirectional smoothness scoop) | Protects Identity C's core novel move | Forward-citation check on IGNITE/MS-DDEO |

**Everything else is better closed by the experiment (X1, X11) than by the literature.** The corpus is not
missing evidence that would *reverse* the direction — it is missing three citations that would *secure* it,
and two experiments that no source can substitute for. That is the honest state: the paper's risks are
predominantly internal (the artifact) rather than external (a scoop).
