# Novelty Check V2 — "Decomposing the GP Advantage in Offline MBO" (AAAI-27)

Fresh adversarial novelty pass, structured **per paper identity** and **per claim**. This
refreshes and, where needed, corrects `docs/NOVELTY_CHECK.md` — it is not a copy of it.

**Hard rule applied to every row.** Exactly one verdict per claim:
- **PRIOR WORK FOUND** — with citation, the specific overlapping sentence/result, and a quantified estimate of how much of the claim the prior work owns.
- **NONE FOUND** — states what was searched.
- **UNVERIFIED** — could not check this session; flagged, never asserted away.

**Overlap quantities are estimates of ownership**, not measured quantities. "Owns ~90%" means a
reviewer could reproduce ~90% of the claim's content from the cited prior work alone.

**Verification provenance for this pass.** Re-fetched this session (2026-07-17): Li/Rudner/Wilson
abstract (arXiv:2305.20028), Tan et al. (arXiv:2410.11502), Chemingui et al. (arXiv:2405.05349),
SOO-Bench (Semantic Scholar record), IGNITE (arXiv:2503.04242), MS-DDEO (secondary confirmation),
Henderson (arXiv:1709.06560), Musgrave (arXiv:2003.08505), and the four reality-check vault notes
(Lucic 1711.10337, Rendle 1905.01395, Ferrari Dacrema 1907.06902, Rendle 2005.09683). Items marked
**[carried from NOVELTY_CHECK]** were verified in the prior pass from full source text and not
re-fetched here; they are flagged rather than re-asserted as first-hand.

---

## Bottom line up front

- **The apparatus is novel; most of the findings are owned.** A crossed surrogate×optimizer
  factorial *in offline MBO* returns **NONE FOUND** as a design — but the two headline findings it
  produces ("ensembles are poor surrogates," "ranking is problem-dependent → tailored inductive
  biases") are owned almost verbatim by Li, Rudner & Wilson (ICLR 2024).
- **The single biggest threat to Identity A is Li/Rudner/Wilson (ICLR 2024)** — it owns the
  *findings* but not the *factorial design* and not the *smoothness-not-calibration mechanism*.
- **Identity D is the most novelty-exposed** of the four: its taxonomy *shape* is the mature
  "reality-check" genre (Henderson 2018; Lucic 2018; Rendle 2019; Musgrave 2020; Recht 2019), and
  its headline confound was already named in print by the field's own TMLR survey (Kim et al. 2025).
- **Identity C carries the cleanest novel move** (bidirectional smoothness manipulation as causal
  identification — **NONE FOUND**), but it is doubly undercut: the smoothness *axis* is pre-claimed
  (RoMA, IGNITE, MS-DDEO), and `FLAW_LEDGER.md` P0-0/P0-2 show the authors' own controls currently
  refute the mechanism it rests on.
- **D9 resolved:** the grounding report is genuinely absent from disk; the "first controlled
  decomposition" claim is defensible **only** in its narrow form ("first controlled surrogate×optimizer
  factorial in offline MBO"), and the DECISION_QUEUE's "ICLR 2023" for Li/Rudner/Wilson is a
  citation error — it is **ICLR 2024**.

---

## Identity A — REPAIRED MEASUREMENT

*Contribution claim:* a de-confounded decomposition of the GP-vs-ensemble advantage in offline MBO
(surrogate main effect + ensemble×optimizer interaction; unresolved on Design-Bench).

| Claim | Verdict | Citation | Overlapping sentence / result | Quantified overlap |
|---|---|---|---|---|
| A1. First *controlled surrogate×optimizer factorial* in offline MBO (the de-confounding design itself) | **NONE FOUND** | Searched: Semantic Scholar ("learning-to-rank surrogate offline MBO," "policy-guided gradient search offline MBO"), Consensus ("decomposing surrogate vs acquisition optimizer offline MBO"), WebSearch. Nearest: Li/Rudner/Wilson (ICLR 2024); Tan et al. (ICLR 2025); Chemingui et al. (AAAI 2024) | Li/Rudner/Wilson **fix** the acquisition ("Monte-Carlo based Expected Improvement … for all problems") — no optimizer factor, and it is *online* BO. Tan et al. vary the surrogate as a *proposed method*; Chemingui vary the optimizer as a *proposed method*. None crosses the two axes as a control. | Prior work owns the *"compare surrogates"* premise only, **~15%**. The crossed factorial under one score-closure protocol is unclaimed. |
| A2. Deep ensembles are the poor surrogate; GP/SVGP win at low dim | **PRIOR WORK FOUND** | Li, Rudner & Wilson, ICLR 2024 (arXiv:2305.20028) | Verbatim (abstract, re-fetched): *"(iv) deep ensembles perform relatively poorly."* And [carried from NOVELTY_CHECK]: *"we show they can perform relatively poorly for Bayesian optimization."* | **~90%** of this sub-claim. Only the offline-MBO *setting* is new. |
| A3. Ranking is problem-dependent → tailored inductive biases needed | **PRIOR WORK FOUND** | Li, Rudner & Wilson, ICLR 2024 | Verbatim (abstract, re-fetched): *"(i) the ranking of methods is highly problem dependent … suggesting the need for tailored inductive biases."* | **~95%** — near-verbatim to the paper's framing. Claiming this as a discovery is refutable with one citation. |
| A4. η² decomposition into surrogate main effect (0.37) + surrogate×optimizer interaction (0.17) | **NONE FOUND** (for the offline-MBO instantiation) | Methodological precedent: Hutter, Hoos & Leyton-Brown, "An Efficient Approach for Assessing Hyperparameter Importance" (fANOVA), ICML 2014 | fANOVA is the canonical variance-decomposition-of-design-choices method (main effects + low-order interactions). A reviewer may ask "why not fANOVA?" | Methodology precedent only, **~10%**. The specific main-effect-plus-interaction numbers in offline MBO are new. |
| A5. The GP-LCB "advantage" is confounded (surrogate class coupled with acquisition optimizer) | **PRIOR WORK FOUND** (named as open problem, not measured) | Kim et al., "Offline Model-Based Optimization: Comprehensive Review," TMLR 2026 (arXiv:2503.17286) [carried from NOVELTY_CHECK] | *"without clarifying whether observed gains stem from superior surrogate modeling, improved optimization strategies, or mere chance."* | **~40%** — the survey *names* the attribution gap almost exactly; it runs no experiment. The paper answers a stated question rather than posing a new one. |
| A6. Method differences are statistically unresolved on Design-Bench (Friedman p=0.69) | **PRIOR WORK FOUND** (complaint) / **NONE FOUND** (omnibus measurement) | Trabucco et al., Design-Bench, ICML 2022; Kim et al., TMLR 2026 [carried from NOVELTY_CHECK] | Design-Bench: *"simple baselines such as CMA-ES and naïve gradient ascent … the need for careful tuning and standardization."* Kim: benchmarks *"make it difficult to distinguish the performance of more sophisticated algorithms."* | Complaint **~80% owned**; the *paired omnibus measurement* (synthetic p=6e-5 → real p=0.69) is **NONE FOUND** and is the surviving contribution. |

**Identity A verdict.** The measurement *apparatus* survives (NONE FOUND for A1, A4-measurement,
A6-measurement). The *findings it reports* are largely owned by Li/Rudner/Wilson (A2 ~90%, A3 ~95%).
The paper's best asset is that its **mechanism attribution (posterior-mean smoothness, not
calibration) directly contradicts** Li/Rudner/Wilson's diversity/calibration explanation — that
contradiction is unclaimed and should be foregrounded.

---

## Identity C — MECHANISM

*Contribution claim:* smoothness of the surrogate's mean is the single axis governing the gap, the
ensemble's gradient-ascent collapse, the LCB coverage failure, and synthetic→real transfer — shown by
bidirectional manipulation (smooth the ensemble / roughen the GP) + a smoothness continuum.

| Claim | Verdict | Citation | Overlapping sentence / result | Quantified overlap |
|---|---|---|---|---|
| C1. Surrogate-mean *smoothness* governs offline optimization performance | **PRIOR WORK FOUND** | (i) Dao, Nguyen, Truong & Hoang, "Incorporating Surrogate Gradient Norm to Improve Offline Optimization Techniques" (IGNITE), NeurIPS 2024 (arXiv:2503.04242); (ii) Zhen, Wang & Jin, "Offline data-driven evolutionary optimization based on model selection" (MS-DDEO), *Swarm and Evolutionary Computation* 2022, DOI 10.1016/j.swevo.2022.101080; (iii) Yu et al., RoMA, NeurIPS 2021 | IGNITE (re-fetched): *"reducing surrogate sharpness on the offline dataset provably reduces its generalized sharpness on unseen data."* MS-DDEO (re-confirmed): model pool of four RBFs *"with different smoothness, where more smoothness means the model has less multimodal … less high-frequency information in the frequency domain,"* selected offline. | **~50–60%.** "Surrogate smoothness helps offline optimization" is established. What is *not* owned: attributing the *GP-vs-ensemble gap specifically* to mean smoothness. |
| C2. Smoothness is *the single causal axis*, established by **bidirectional manipulation** (smooth the ensemble / roughen the GP) + a smoothness **continuum** | **NONE FOUND** | Searched: WebSearch (bidirectional smoothness manipulation / roughen GP / smooth ensemble), Consensus, IGNITE/RoMA/MS-DDEO citation neighbourhoods | No prior work manipulates surrogate smoothness *in both directions* to identify it as the causal axis of a surrogate-class gap. IGNITE regularizes toward smoothness (one direction, as a method); MS-DDEO grades a pool by smoothness (selection, not causal identification). | Prior work owns **~5%.** This is the identity's strongest, cleanest novel move. |
| C3. The ensemble's gradient-ascent collapse (optimizer exploits an over-estimated argmax) | **PRIOR WORK FOUND** | Fu & Levine, NEMO, ICLR 2021 (arXiv:2102.07970) [carried from NOVELTY_CHECK]; Trabucco et al., COMs, ICML 2021 | NEMO: *"In out-of-support regions far from the data, the bootstrap ensemble tends to underestimate uncertainty and produce overconfident predictions."* Model-exploitation is the founding premise of the whole COMs lineage. | **~60%** of the *phenomenon* (over-estimation exploited by search). The *ensemble×optimizer interaction framing* and the direct coverage measurement are new. |
| C4. LCB coverage failure diagnosis (premise coverage = bound validity; collapses on own proposals) | **PRIOR WORK FOUND** | Stanton, Maddox & Wilson, "Bayesian Optimization with Conformal Prediction Sets," AISTATS 2023 (arXiv:2210.12496); Fannjiang et al., PNAS 2022 (arXiv:2202.03613); Choi, arXiv:2606.15217 (2026) [all carried from NOVELTY_CHECK] | Stanton: conformal *"directs queries towards regions … where the model predictions have guaranteed validity … query coverage can be significantly improved."* Choi (contemporaneous, same setting): *"attaches a calibrated one-sided lower bound to each candidate … standard conformal … collapses to 0.416 coverage."* | **~70%.** Coverage-as-validity for optimizer-driven queries is Stanton 2023; the design-shift conformal is Fannjiang 2022 / Choi 2026. Prop. 1 is a known assumption (Jin et al., ICML 2021); Prop. 2 restates Tibshirani et al. 2019. See Identity-A-adjacent note: this is the paper's weakest sub-claim as *theory*. |
| C5. Synthetic→real transfer explained by prior-task smoothness match | **NONE FOUND** (the smoothness-match attribution) / **PRIOR WORK FOUND** (the "benchmarks don't discriminate" premise) | Kim et al., TMLR 2026; Design-Bench, ICML 2022 | See A6. The *attribution* to a Matérn-prior/task-smoothness match is unclaimed; the *observation* that the benchmarks fail to separate methods is owned. | Premise **~80% owned**; the unifying smoothness-match *explanation* is **NONE FOUND**. |

**Identity C verdict.** C2 (bidirectional manipulation) is the single most novel item in the entire
paper — **NONE FOUND**. But the identity is fragile on two axes that are *not* novelty: (a) the
smoothness axis it builds on is pre-claimed (C1 ~55%, C4 ~70%), and (b) `FLAW_LEDGER.md` P0-0 shows
the repo's own `gradtune.py` control refutes the ensemble×gradient collapse on 3 of 4 tasks, and P0-2
shows the ensemble trains on unstandardized targets while both GPs z-score — so the mechanism C2
identifies may be a target-scaling artifact, not smoothness. **Novel, but empirically at risk.**

---

## Identity D — CONFOUND TAXONOMY

*Contribution claim:* every published surrogate/optimizer comparison in offline MBO is confounded in
three nameable ways (surrogate×optimizer coupling; target-scaling; candidate-selection + oracle-budget),
and fixing them changes the ranking — taxonomy + de-confounding protocol + diagnostic + demonstration.

| Claim | Verdict | Citation | Overlapping sentence / result | Quantified overlap |
|---|---|---|---|---|
| D1. The taxonomy **shape** (name the confounds → de-confounding protocol → ranking changes) | **PRIOR WORK FOUND** | Henderson et al., "Deep Reinforcement Learning that Matters," AAAI 2018 (arXiv:1709.06560); Lucic et al., "Are GANs Created Equal?," NeurIPS 2018 (arXiv:1711.10337); Musgrave et al., "A Metric Learning Reality Check," ECCV 2020 (arXiv:2003.08505); Rendle et al., arXiv:1905.01395 (2019); Recht et al., "Do ImageNet Classifiers Generalize to ImageNet?," ICML 2019 | Henderson (re-fetched): names *"non-determinism in standard benchmark environments"* + *"variance intrinsic to the methods"* and pairs the taxonomy with reproducibility guidelines. Musgrave (re-fetched): *"We find flaws in the experimental methodology of numerous metric learning papers, and show that the actual improvements over time have been marginal at best."* Lucic (vault): *"most models can reach similar scores with enough hyperparameter optimization … improvements can arise from a higher computational budget and tuning more than fundamental algorithmic changes."* | **~70% of the shape.** Identity D is structurally *"Deep RL that Matters / Are GANs Created Equal, for offline MBO."* A meta-science reviewer places it instantly. |
| D2. Confound #1 — surrogate×optimizer coupling | **PRIOR WORK FOUND** (named) | Kim et al., TMLR 2026 | *"whether observed gains stem from superior surrogate modeling, improved optimization strategies, or mere chance."* | **~50%.** Named as an open problem by the field's survey; the paper *measures* it. |
| D3. Confound #2 — target-scaling (surrogates trained on differently-normalized targets) | **NONE FOUND** as a *named cross-method comparison confound* in offline MBO | Adjacent: Tan et al., ICLR 2025 (ranking surrogates) discusses z-score normalization affecting regression surrogates, but as a *modeling choice*, not as a confound that invalidates cross-method comparisons | Tan et al. (WebSearch): regression surrogates *"preserve … zero mean and unit standard deviation … within the training distribution"* — a modeling observation, not a comparison-validity claim. | Prior work owns **~20%.** Naming target-scaling as a *confound that flips rankings* is unclaimed. (Note: this is also `FLAW_LEDGER.md` P0-2 — inside the paper the confound is currently *unfixed*, so the demonstration is owed.) |
| D4. Confound #3 — candidate-selection + oracle-budget asymmetry | **NONE FOUND** as a named confound | Design-Bench, ICML 2022 documents the 128-candidate / 100th-percentile protocol and (App. F) a hyperparameter-selection conditional-independence rule, but not the budget asymmetry as a cross-method confound | Design-Bench formalizes the protocol; it does not flag that optimizers consuming unequal oracle/candidate budgets are non-comparable. | Prior work owns **~10%.** The specific confound is unclaimed. (Also `FLAW_LEDGER.md` P0-1 — currently unfixed in the paper's own code.) |
| D5. Fixing the confounds *changes the ranking* (the demonstration) | **NONE FOUND** in offline MBO / **PRIOR WORK FOUND** for the general pattern | Lucic et al. 2018; Rendle et al. 2019; Ferrari Dacrema et al., RecSys 2019 (arXiv:1907.06902) | Ferrari Dacrema: of 18 neural recommenders, *"Only 7 … could be reproduced … 6 of them can often be outperformed with comparably simple heuristic methods."* Rendle: a well-tuned baseline *"even outperform[s] the reported results of any newly proposed method."* | The *pattern* "control the confound and the ranking reverses" is **~40% owned** by the reality-check genre; its offline-MBO instantiation is new. |

**Identity D verdict.** The taxonomy *shape* is a mature, named genre (D1 ~70%) and the headline
confound is pre-claimed (D2 ~50%). The genuinely novel parts (D3, D4 naming; D5 instantiation) are
the *narrowest* and, per the flaw ledger, are the confounds the paper's own code has **not yet fixed**.
This is the **most novelty-exposed** identity — see the bottom line.

---

## Identity E — THE REVERSAL

*Contribution claim:* a self-demonstrating account of how hard offline-MBO evaluation is to get right
(pre-registered hypotheses refuted by the authors' own controls).

| Claim | Verdict | Citation | Overlapping sentence / result | Quantified overlap |
|---|---|---|---|---|
| E1. A self-demonstrating account that offline-MBO evaluation is hard to get right | **PRIOR WORK FOUND** (the genre) | Henderson 2018; Lucic 2018; Musgrave 2020; Recht 2019; Balduzzi et al., "Re-evaluating Evaluation," NeurIPS 2018 (arXiv:1806.02643) | The entire reality-check genre *is* "the field's own evaluation refuted its claimed progress." Lucic: improvements come from *"tuning more than fundamental algorithmic changes."* | **~70%** of the *narrative*. The genre owns "evaluation is harder than the field assumes." What is unusual is staging it *within one paper via the authors' own pre-registered refutation*. |
| E2. Pre-registered hypotheses refuted by the authors' own controls | **NONE FOUND** as a published *offline-MBO* framing / **PRIOR WORK FOUND** for pre-registration-in-ML as a practice | Pre-registration in ML is an established practice (NeurIPS pre-registration workshops, 2020–2021); `FLAW_LEDGER.md` P1-5 records the internal refutation (registered η²_opt-dominant → measured η²_opt=0.01) | The refutation-by-own-controls is *honest reporting*, not a novel contribution type. No prior offline-MBO paper stages self-refutation as its identity. | Pre-registration practice **~60% owned**; the specific self-demonstration is presentationally novel but carries **no technical artifact**. |

**Identity E verdict.** E has **no measurable novel artifact** — it is a framing/rhetorical stance.
Its "novelty" (no one has framed *this* result this way) is trivially true and un-attackable, but for
the same reason it is the **thinnest as a standalone contribution**. Its honest strength is credibility
(a refuted pre-registration is evidence of a real test), not novelty.

---

## Adversarial checks — the 7 named works, quantified

| # | Work | Full citation | How much of *our* contribution it owns | Overlapping sentence (verbatim where verified) | Verdict |
|---|---|---|---|---|---|
| 1 | Li, Rudner & Wilson (biggest threat to Identity A) | Yucen Lily Li, Tim G. J. Rudner, Andrew Gordon Wilson, "A Study of Bayesian Neural Network Surrogates for Bayesian Optimization," **ICLR 2024**, arXiv:2305.20028 | Owns the two headline **findings** (~90–95%) but **not** the factorial design, **not** the offline setting, **not** the smoothness-vs-calibration mechanism (which it *contradicts*) | *"(i) the ranking of methods is highly problem dependent … suggesting the need for tailored inductive biases … (iv) deep ensembles perform relatively poorly"* (abstract, re-fetched). Acquisition is fixed (MC-EI, all problems); no optimizer factor; online BO [carried from NOVELTY_CHECK] | **PRIOR WORK FOUND** for A2/A3; **NONE FOUND** for the factorial and mechanism |
| 2 | Tan et al. (surrogate-class comparison, optimizer fixed) | Rong-Xi Tan, Ke Xue, Shen-Huan Lyu, Haopu Shang, Yao Wang, Yaoyuan Wang, Sheng Fu, Chao Qian, "Offline Model-Based Optimization by Learning to Rank," **ICLR 2025**, arXiv:2410.11502 | Owns "a ranking surrogate can beat an MSE surrogate under a fixed optimizer" (~25% of A1's premise). Does **not** decompose surrogate vs optimizer, does **not** run a controlled cross | *"train a regression-based surrogate model by minimizing mean squared error … then find the best design within this surrogate model by different optimizers (e.g., gradient ascent) … we propose learning a ranking-based model"* (re-fetched). It proposes a method; it does not isolate surrogate from optimizer | **NONE FOUND** for the decomposition; a method paper, not a control |
| 3 | Chemingui et al. (optimizer-as-contribution) | Yassine Chemingui, Aryan Deshwal, Trong Nghia Hoang, Janardhan Rao Doppa, "Offline Model-Based Optimization via Policy-Guided Gradient Search," **AAAI 2024**, arXiv:2405.05349 | Owns "the search strategy is under-explored relative to the surrogate" (~30% of the paper's motivation) but proposes a *method* (learned policy) rather than *decomposing*. Premise is partly the **antithesis** of our conclusion (it argues optimizers matter; we find η²_opt=0.01) | *"Prior approaches … have primarily focused on learning robust surrogate models. However, their search strategies are derived from the surrogate model rather than the actual offline data. To fill this important gap, we introduce a new learning-to-search perspective"* (re-fetched) | **NONE FOUND** for the decomposition; must be engaged directly (AAAI-27 reviewers may include its authors) |
| 4 | SOO-Bench (benchmark-validity axis) | Hong Qian, Yiyi Zhu, Xiang Shu, Shuo Liu, Yaolin Wen, Xin An, Huakang Lu, Aimin Zhou, Ke Tang, Yang Yu, "SOO-Bench: Benchmarks for Evaluating the Stability of Offline Black-Box Optimization," **ICLR 2025** | Owns a *complementary* benchmark-validity axis (**stability**, ~30% adjacency) — **not** discrimination/non-separability | Its axis is optimizer *stability across instances*, not "the benchmark cannot distinguish methods." [carried from NOVELTY_CHECK: *"it can hardly evaluate the stability of offline optimization"*] | **NONE FOUND** for the non-discrimination finding; not a scoop |
| 5 | Kim et al. survey (does it pre-name our findings?) | Kim, Gu, Yuan, Yun, Liu, Bengio, Chen, "Offline Model-Based Optimization: Comprehensive Review," **TMLR 2026** (Survey Certification), arXiv:2503.17286 | Owns the *problem statements* almost verbatim (~50%): the surrogate-vs-optimizer attribution gap **and** the non-discrimination complaint. Runs **no** experiment | *"without clarifying whether observed gains stem from superior surrogate modeling, improved optimization strategies, or mere chance"*; benchmarks *"make it difficult to distinguish the performance of more sophisticated algorithms"* [carried from NOVELTY_CHECK] | **PRIOR WORK FOUND** — the single most dangerous citation for *motivation ownership*; cite it early to convert threat into motivation |
| 6 | Trabucco et al., Design-Bench (is the confound documented there?) | Brandon Trabucco, Xinyang Geng, Aviral Kumar, Sergey Levine, "Design-Bench: Benchmarks for Data-Driven Offline Model-Based Optimization," **ICML 2022**, arXiv:2202.08450 | Owns "simple baselines are competitive / methods hard to distinguish" (~80% of A6 complaint) and the offline model-selection *future-work* pointer. Does **not** cross surrogate×optimizer; does **not** name target-scaling or oracle-budget as confounds | *"The comparatively high efficacy of even simple baselines such as CMA-ES and naïve gradient ascent suggests the need for careful tuning and standardization."* App. F formalizes offline hyperparameter selection (conditional independence of H from M given D) [carried from NOVELTY_CHECK] | **PRIOR WORK FOUND** for the complaint; **NONE FOUND** for the surrogate×optimizer / target-scaling confound documentation |
| 7 | Reality-check lineage (does it own Identity D's *shape*?) | Henderson et al., AAAI 2018 (arXiv:1709.06560); Balduzzi et al., NeurIPS 2018 (arXiv:1806.02643); Musgrave et al., ECCV 2020 (arXiv:2003.08505); Recht et al., ICML 2019 (arXiv:1902.10811); Lucic et al., NeurIPS 2018 (arXiv:1711.10337); Rendle et al., arXiv:1905.01395 (2019); Ferrari Dacrema et al., RecSys 2019 (arXiv:1907.06902) | **Owns the taxonomy shape (~70%).** Identity D *is* "that genre, for offline MBO": name the confounds, control them, show gains shrink/rankings flip, ship a reusable protocol | Henderson: *"non-determinism … variance intrinsic to the methods … Without significance metrics and tighter standardization … it is difficult to determine whether improvements … are meaningful."* Musgrave: *"flaws in the experimental methodology … actual improvements … marginal at best."* Lucic: *"improvements can arise from a higher computational budget and tuning more than fundamental algorithmic changes."* | **PRIOR WORK FOUND** — Identity D's shape is not novel; only the offline-MBO instantiation and the specific three-confound naming are |

---

## D9 resolution

**The provenance question.** `paper/SKELETON.md:3,35,44` grounds the manuscript's positioning —
including the load-bearing "first controlled decomposition" claim — in
`research/notes/final_report_mbo-decomposition-prior-art-579ba4.md` ("the R1 novelty verdict").
`docs/DECISION_QUEUE.md` (D9), `docs/REPO_MAP.md`, and `docs/BUNDLE_PART1.md` all reference it.

**Disk state (verified this session).** The file **does not exist**. `research/notes/` contains
exactly four notes (the reality-check papers), none matching. `find … -iname "*579ba4*"` returns
nothing; `find … -iname "final_report*"` returns nothing anywhere in the repo. The companion note
`research/notes/baseline-numbers-designbench.md` (R2) is likewise absent. **Confirmed: the novelty
claim traces to a deleted document.** The claim was therefore never independently verifiable from the
repo before this pass — this pass supplies the missing verification.

**Re-run verdict on "first controlled decomposition."**
- As stated in the manuscript — *"the first controlled surrogate$\times$optimizer decomposition"*
  (abstract) and *"To our knowledge this is the first controlled measurement disentangling the
  surrogate and optimizer contributions in offline MBO"* (Contribution 3) — the claim is **NONE
  FOUND / defensible in this narrow form.** No prior work crosses surrogate class with acquisition
  optimizer as a control in offline MBO (adversarial checks 1–3, 6 above; Consensus + Semantic
  Scholar + WebSearch all negative).
- The unqualified phrasing *"the first controlled decomposition of offline-MBO performance"*
  (`SKELETON.md:14,52`) is **exposed**: (a) the *decomposition-of-design-choices* methodology is
  fANOVA (Hutter et al., ICML 2014); (b) the *findings* are owned by Li/Rudner/Wilson; (c) the
  taxonomy *shape* is the reality-check genre. Keep the surrogate×optimizer qualifier; drop
  "first controlled decomposition" unqualified.

**Citation-error correction (must fix before submission).** `docs/DECISION_QUEUE.md` (D9) states
Li/Rudner/Wilson is *"ICLR 2023, not 2024 as cited."* **That is backwards.** The paper is **ICLR
2024** (arXiv posted May 2023; *published as a conference paper at ICLR 2024*; OpenReview
`SA19ijj44B`). `main.tex` cites it correctly (`li2024bnnsurrogates`); `FLAW_LEDGER.md` P2-8 already
retracted the "2023" claim. The DECISION_QUEUE line is stale and should not be trusted.

**Net D9 status:** the missing report is a real provenance hole, now closed. The narrow novelty claim
survives; the broad one does not. The manuscript's actual wording is on the safe side of that line.

---

## Novelty bottom line per identity

**Most defensible on novelty: Identity A (repaired measurement).** Its core claim is a *design/apparatus*
claim — the de-confounded surrogate×optimizer factorial in offline MBO — and that returns a clean
**NONE FOUND** across Semantic Scholar, Consensus, and WebSearch, with the three nearest works
(Li/Rudner/Wilson fix the acquisition; Tan and Chemingui vary one axis as a proposed method) each
verified to *not* run the cross. Apparatus claims are the cleanest to defend because they are checkable
by inspection, and A's exposure is confined to its *findings* (A2/A3, owned by Li/Rudner/Wilson), which
the paper can concede and cite rather than claim. Identity C is a close second — its bidirectional
smoothness manipulation (C2) is the single most novel move in the paper — but C is undercut on two
fronts that A is not: the smoothness axis is pre-claimed (RoMA/IGNITE/MS-DDEO), and the mechanism is
empirically contradicted by the repo's own controls (`FLAW_LEDGER.md` P0-0/P0-2).

**Most exposed on novelty: Identity D (confound taxonomy).** Its central move — "every published
comparison is confounded in three nameable ways; here is the taxonomy, the protocol, and the
demonstration that fixing them flips the ranking" — is the **mature reality-check genre** (Henderson
2018; Lucic 2018; Rendle 2019; Ferrari Dacrema 2019; Musgrave 2020; Recht 2019; Balduzzi 2018), which
owns roughly 70% of the *shape*. Worse, its headline confound (surrogate-vs-optimizer attribution) was
already named in print by the field's own TMLR-certified survey (Kim et al. 2025), and its two novel
confounds (target-scaling; candidate-selection + oracle-budget) are precisely the ones the paper's own
code has **not yet controlled** (`FLAW_LEDGER.md` P0-1, P0-2). So Identity D makes the most sweeping,
most concrete novelty claim while standing on the most pre-owned ground — a reviewer from meta-science
or offline MBO will recognize both the template and the pre-claimed confound immediately. (Identity E
is *thinner* still, but it makes essentially no checkable novelty claim to attack — it is a framing, not
a contribution; it is un-exposed precisely because it is un-novel.)

---

## Full citation list

1. Yucen Lily Li, Tim G. J. Rudner, Andrew Gordon Wilson. "A Study of Bayesian Neural Network Surrogates for Bayesian Optimization." ICLR 2024. arXiv:2305.20028. OpenReview SA19ijj44B.
2. Rong-Xi Tan, Ke Xue, Shen-Huan Lyu, Haopu Shang, Yao Wang, Yaoyuan Wang, Sheng Fu, Chao Qian. "Offline Model-Based Optimization by Learning to Rank." ICLR 2025. arXiv:2410.11502.
3. Yassine Chemingui, Aryan Deshwal, Trong Nghia Hoang, Janardhan Rao Doppa. "Offline Model-Based Optimization via Policy-Guided Gradient Search." AAAI 2024. arXiv:2405.05349.
4. Hong Qian, Yiyi Zhu, Xiang Shu, Shuo Liu, Yaolin Wen, Xin An, Huakang Lu, Aimin Zhou, Ke Tang, Yang Yu. "SOO-Bench: Benchmarks for Evaluating the Stability of Offline Black-Box Optimization." ICLR 2025.
5. Minsu Kim, Jiwoo Son, Hyeonah Kim, Jinkyoo Park (and coauthors per survey record: Kim, Gu, Yuan, Yun, Liu, Bengio, Chen). "Offline Model-Based Optimization: Comprehensive Review." TMLR 2026 (Survey Certification). arXiv:2503.17286. *(Manuscript cites as `kim2025mbosurvey`; verify author list against the TMLR record before final submission.)*
6. Brandon Trabucco, Xinyang Geng, Aviral Kumar, Sergey Levine. "Design-Bench: Benchmarks for Data-Driven Offline Model-Based Optimization." ICML 2022. arXiv:2202.08450.
7. Peter Henderson, Riashat Islam, Philip Bachman, Joelle Pineau, Doina Precup, David Meger. "Deep Reinforcement Learning that Matters." AAAI 2018. arXiv:1709.06560.
8. David Balduzzi, Karl Tuyls, Julien Perolat, Thore Graepel. "Re-evaluating Evaluation." NeurIPS 2018. arXiv:1806.02643.
9. Kevin Musgrave, Serge Belongie, Ser-Nam Lim. "A Metric Learning Reality Check." ECCV 2020. arXiv:2003.08505.
10. Benjamin Recht, Rebecca Roelofs, Ludwig Schmidt, Vaishaal Shankar. "Do ImageNet Classifiers Generalize to ImageNet?" ICML 2019. arXiv:1902.10811.
11. Mario Lucic, Karol Kurach, Marcin Michalski, Sylvain Gelly, Olivier Bousquet. "Are GANs Created Equal? A Large-Scale Study." NeurIPS 2018. arXiv:1711.10337.
12. Steffen Rendle, Li Zhang, Yehuda Koren. "On the Difficulty of Evaluating Baselines: A Study on Recommender Systems." 2019. arXiv:1905.01395.
13. Maurizio Ferrari Dacrema, Paolo Cremonesi, Dietmar Jannach. "Are We Really Making Much Progress? A Worrying Analysis of Recent Neural Recommendation Approaches." RecSys 2019. arXiv:1907.06902.
14. Steffen Rendle, Walid Krichene, Li Zhang, John Anderson. "Neural Collaborative Filtering vs. Matrix Factorization Revisited." RecSys 2020. arXiv:2005.09683.
15. Manh Cuong Dao, Phi Le Nguyen, Thao Nguyen Truong, Trong Nghia Hoang. "Incorporating Surrogate Gradient Norm to Improve Offline Optimization Techniques" (IGNITE). NeurIPS 2024. arXiv:2503.04242.
16. Pengfei Zhen, Handing Wang, Yaochu Jin (author order per journal record). "Offline data-driven evolutionary optimization based on model selection" (MS-DDEO). Swarm and Evolutionary Computation, 2022. DOI 10.1016/j.swevo.2022.101080.
17. Sihyun Yu, Sungsoo Ahn, Le Song, Jinwoo Shin. "RoMA: Robust Model Adaptation for Offline Model-Based Optimization." NeurIPS 2021.
18. Samuel Stanton, Wesley Maddox, Andrew Gordon Wilson. "Bayesian Optimization with Conformal Prediction Sets." AISTATS 2023. arXiv:2210.12496.
19. Clara Fannjiang, Stephen Bates, Anastasios N. Angelopoulos, Jennifer Listgarten, Michael I. Jordan. "Conformal prediction under feedback covariate shift for biomolecular design." PNAS 119(43):e2204569119, 2022. arXiv:2202.03613.
20. Ryan J. Tibshirani, Rina Foygel Barber, Emmanuel J. Candès, Aaditya Ramdas. "Conformal Prediction Under Covariate Shift." NeurIPS 2019.
21. Ying Jin, Zhuoran Yang, Zhaoran Wang. "Is Pessimism Provably Efficient for Offline RL?" ICML 2021. PMLR v139.
22. Seungjin Choi. "Conformal Candidate Certification for Offline Model-Based Optimization." arXiv:2606.15217, 2026 (workshop, single author, contemporaneous).
23. Justin Fu, Sergey Levine. "Offline Model-Based Optimization via Normalized Maximum Likelihood Estimation" (NEMO). ICLR 2021. arXiv:2102.07970.
24. Brandon Trabucco, Aviral Kumar, Xinyang Geng, Sergey Levine. "Conservative Objective Models for Effective Offline Model-Based Optimization" (COMs). ICML 2021.
25. Frank Hutter, Holger Hoos, Kevin Leyton-Brown. "An Efficient Approach for Assessing Hyperparameter Importance" (fANOVA). ICML 2014. PMLR v32.
26. Rishabh Agarwal, Max Schwarzer, Pablo Samuel Castro, Aaron Courville, Marc G. Bellemare. "Deep Reinforcement Learning at the Edge of the Statistical Precipice." NeurIPS 2021 (Outstanding Paper). arXiv:2108.13264.

*Author lists for items 5, 16, 17, 23 were not all re-verified first-hand this session — confirm
against the source record before they enter `references.bib`.*
