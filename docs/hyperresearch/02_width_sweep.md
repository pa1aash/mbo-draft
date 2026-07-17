# 02 · Width sweep — source corpus across the four acceptance axes

**Step 2 of the research core.** A broad, honestly-scoped source sweep for the question *"what does it
take for THIS paper to be accepted at AAAI-27?"* organized by the four thematic clusters that map onto
the paper's four evaluation axes (manuscript, experiments, statistics, artifact/reproducibility).

**Scope honesty.** This is a grounded memo, not a 40–100-source multi-fetcher wave. Roughly half the
corpus was fetched fresh this session (WebSearch / WebFetch / Semantic Scholar — marked **[fetched]**);
the other half is carried, with verbatim quotes and arXiv IDs, from four already-grounded repo docs
(`FLAW_LEDGER.md`, `VENUE_NORMS.md`, `NOVELTY_V2.md`, `AAAI27_VENUE.md`) that did their own FETCH-not-recall
discipline (marked **[repo-doc]** with the doc that carries the primary quote). Where a fact is only
weakly grounded it is flagged. **28 distinct sources.**

Citation-trap notes propagated from the repo docs are preserved inline (they are decision-relevant): cite
**Li/Rudner/Wilson as ICLR 2024** (Semantic Scholar back-propagates year 2023 from the arXiv v1);
cite **Henderson as AAAI 2018** (S2 says 2017); **Benavoli as JMLR 2016** (arXiv 2015).

---

## Axis A — Manuscript: AAAI measurement / benchmark-validity precedents (the genre bar)

The load-bearing question for the manuscript axis is whether AAAI's main technical track accepts a
no-new-method measurement paper, and what such a paper must carry. The answer is yes, four times, plus
the wider reality-check canon.

| # | Source | Venue / ID | 1-line relevance |
|---|---|---|---|
| A1 | Henderson, Islam, Bachman, Pineau, Precup, Meger — *Deep Reinforcement Learning that Matters* | **AAAI 2018**; arXiv:1709.06560 **[repo-doc: VENUE_NORMS]** | The proof AAAI accepts pure measurement on the ML main track (~2,397 S2 cites); seven-factor taxonomy + seed-variance finding (`t=−9.09, p=0.0016`). Our closest venue precedent — and a mirror threat (its thesis = unreported details decide results = our P0-0/P0-2). |
| A2 | Gundersen & Kjensmo — *State of the Art: Reproducibility in AI* | **AAAI 2018** **[repo-doc: VENUE_NORMS]** | Zero-method AAAI paper whose entire contribution is counting things about 400 IJCAI/AAAI papers — proof the genre floor at AAAI is very low. |
| A3 | Kim et al. — *Towards a Rigorous Evaluation of Time-Series Anomaly Detection* | **AAAI 2022** **[repo-doc: VENUE_NORMS]** | "even a random anomaly score can easily turn into a SOTA TAD method" — null + a minimal positive deliverable (PA%K protocol). The structural twin of our target shape. |
| A4 | Zeng et al. — *Are Transformers Effective for Time Series Forecasting?* | **AAAI 2023, ORAL** **[repo-doc: VENUE_NORMS]** | An AAAI oral that opens "we question the validity of this line of research" and sells its baseline as "embarrassingly simple" — anti-novelty as a weapon. |
| A5 | Recht, Roelofs, Schmidt, Shankar — *Do ImageNet Classifiers Generalize to ImageNet?* | **ICML 2019, oral**; PMLR v97:5389 **[repo-doc: VENUE_NORMS]** | The template: a *reversal*, not a null — accuracy drops but the obvious explanation (adaptivity) is refuted by a manipulation (sampling knobs dial the drop). Structurally identical to the paper's would-be X5. |
| A6 | Musgrave, Belongie, Lim — *A Metric Learning Reality Check* | **ECCV 2020**; arXiv:2003.08505 **[repo-doc: NOVELTY_V2]** | New metric (MAP@R) + new protocol + three named flaws + corrected leaderboard. The "cite the genre to legitimize the genre" move (its §1.6). |
| A7 | Ferrari Dacrema, Cremonesi, Jannach — *Are We Really Making Much Progress?* | **RecSys 2019, Best Long Paper**; arXiv:1907.06902 **[vault note]** | 18 neural recommenders, 7 reproduced, 6 beaten by tuned heuristics. Its named mechanism ("lack of proper tuning of baselines … confirmation bias") **is the paper's own ledger** (P0-0/P0-2). |
| A8 | Lucic, Kurach, Michalski, Gelly, Bousquet — *Are GANs Created Equal?* | **NeurIPS 2018**; arXiv:1711.10337 **[vault note]** | "most models can reach similar scores with enough hyperparameter optimization … improvements can arise from a higher computational budget and tuning more than fundamental algorithmic changes." Has public reviews showing our exact objection survived (see 07). |
| A9 | Schaeffer, Miranda, Koyejo — *Are Emergent Abilities of LLMs a Mirage?* | **NeurIPS 2023, Outstanding Paper**; arXiv:2304.15004 **[repo-doc: VENUE_NORMS]** | Won on "it's the metric" — "largely due to the choice of (discontinuous/nonlinear) metrics and underpowered analyses." The offensive template: name the artifact that manufactures the believed effect. |
| A10 | Yauney, Warraich, Swayamdipta — *How Reliable is LM Micro-Benchmarking?* | **ICLR 2026**; arXiv:2510.08730 **[repo-doc: PAPER_V2_OUTLINE]** | Power-analysis-as-headline clears a top venue when shipped with an instrument + a reversal (random ≈ sophisticated) + a prescription. The four-month-old template for the paper's power-spec artifact. |
| A11 | Balduzzi, Tuyls, Perolat, Graepel — *Re-evaluating Evaluation* | **NeurIPS 2018**; arXiv:1806.02643 **[repo-doc: NOVELTY_V2]** | The taxonomy-shape precedent the paper already cites for Identity D; grounds "name the confounds → protocol → ranking changes." |

**Axis-A takeaway:** the genre is not disqualified at AAAI; it is *under-signalled* in AAAI's written
guidelines (which presume SOTA framing) but established by precedent A1–A4. Every accepted instance shipped
an artifact (a protocol/metric/diagnostic) — a bare null is not the unit of acceptance.

---

## Axis B — Experiments: offline-MBO evaluation norms and the nearest prior art

| # | Source | Venue / ID | 1-line relevance |
|---|---|---|---|
| B1 | Trabucco, Geng, Kumar, Levine — *Design-Bench* | **ICML 2022**; arXiv:2202.08450 **[fetched]** | The benchmark under test. Its own paper: "a classical CMA-ES baseline is competitive with several highly sophisticated MBO methods in 4 of 8 tasks … the need for careful tuning and standardization." The non-discrimination complaint is ~80% pre-owned here. |
| B2 | Kim, Gu, Yuan, Yun, Liu, Bengio, Chen — *Offline MBO: Comprehensive Review* | **TMLR** (Survey Certification); arXiv:2503.17286 **[fetched, S2: 20 cites]** | The field's own survey names the paper's headline confound almost verbatim: gains may stem from "superior surrogate modeling, improved optimization strategies, or mere chance." Cite early to convert threat → motivation. |
| B3 | Li, Rudner, Wilson — *A Study of BNN Surrogates for Bayesian Optimization* | **ICLR 2024**; arXiv:2305.20028 **[fetched, S2: 65 cites]** | The single biggest novelty threat to Identity A. Abstract owns two headline findings: "(i) the ranking of methods is highly problem dependent … tailored inductive biases; … (iv) deep ensembles perform relatively poorly." But fixes the acquisition (MC-EI), is online BO, and its calibration explanation *contradicts* the paper's smoothness mechanism. |
| B4 | Tan, Xue, Lyu, Shang, Wang, Wang, Fu, Qian — *Offline MBO by Learning to Rank* | **ICLR 2025**; arXiv:2410.11502 **[repo-doc: NOVELTY_V2]** | Varies the surrogate (ranking vs MSE) as a *proposed method* under a fixed optimizer — does not cross the two axes. Adjacent, not a scoop. |
| B5 | Chemingui, Deshwal, Hoang, Doppa — *Offline MBO via Policy-Guided Gradient Search* (PGS) | **AAAI 2024**; arXiv:2405.05349 **[repo-doc: NOVELTY_V2]** | The *named belief* the paper's η²_opt=0.01 reversal targets: "prior approaches have primarily focused on … robust surrogate models … we introduce a learning-to-search perspective." AAAI-27 reviewers may include its authors — must be engaged directly. |
| B6 | Qian et al. — *SOO-Bench: Stability of Offline Black-Box Optimization* | **ICLR 2025** **[repo-doc: NOVELTY_V2]** | A complementary benchmark-validity axis (stability across instances), not non-discrimination — not a scoop, but a related-work must-cite. |
| B7 | Fu & Levine — *NEMO: Offline MBO via NML Estimation* | **ICLR 2021**; arXiv:2102.07970 **[repo-doc: NOVELTY_V2]** | Founding statement of model-exploitation: ensembles "underestimate uncertainty and produce overconfident predictions" OOD — owns ~60% of the paper's gradient-collapse phenomenon. |
| B8 | Trabucco, Kumar, Geng, Levine — *COMs* | **ICML 2021** **[repo-doc: FLAW_LEDGER]** | The reproduction target with the 1.22-normalized-unit divergence (P1-6); model-exploitation is the founding premise of the lineage. |
| B9 | Dao, Nguyen, Truong, Hoang — *IGNITE (surrogate gradient norm)* | **NeurIPS 2024**; arXiv:2503.04242 **[repo-doc: NOVELTY_V2]** | Pre-claims the smoothness axis (one direction, as a method): "reducing surrogate sharpness … provably reduces its generalized sharpness on unseen data." |
| B10 | Zhen, Wang, Jin — *MS-DDEO (model selection by smoothness)* | **Swarm & Evol. Comput. 2022**; DOI 10.1016/j.swevo.2022.101080 **[repo-doc: NOVELTY_V2]** | Already selects an offline surrogate pool *by smoothness* — the nearest pre-claim to the paper's mechanism and to any smoothness-driven selection rule. |

---

## Axis C — Statistics: what a stats-literate reviewer will demand and cite

| # | Source | Venue / ID | 1-line relevance |
|---|---|---|---|
| C1 | Benavoli, Corani, Mangili — *Should We Really Use Post-Hoc Tests Based on Mean-Ranks?* | **JMLR 2016** (arXiv 2015); 17(5):1-10 **[fetched, S2: 467 cites]** | The instantiated objection: mean-rank test outcome "depends on the pool of algorithms originally included" — and the paper's rank/CD matrix silently pools 11 cells (P1-2). Recommends sign-test / Wilcoxon. |
| C2 | Demšar — *Statistical Comparisons of Classifiers over Multiple Data Sets* | JMLR 2006; 7(1):1-30 **[repo-doc: FLAW_LEDGER]** | The canonical Friedman+CD procedure the paper uses — and the source of the "N>10 datasets, k>5 methods" rule of thumb the paper's N=7 sits below. |
| C3 | Agarwal, Schwarzer, Castro, Courville, Bellemare — *Deep RL at the Edge of the Statistical Precipice* (rliable) | **NeurIPS 2021, Outstanding Paper**; arXiv:2108.13264 **[fetched]** | Directly on point for the N=7 problem: point estimates over a handful of runs mislead; use interval estimates, IQM, performance profiles, bootstrap CIs. Its "lack of significance ≠ absence of effect" line is the paper's honest TOST framing. |
| C4 | García & Herrera — *Extension of Multiple-Comparison Procedures* | JMLR 2008; 9(89):2677 **[repo-doc: FLAW_LEDGER]** | Holm/Shaffer/Bergmann-Hommel alternatives to Nemenyi for all-pairwise — the fix path for P1-2. |
| C5 | Effect-size methodology: ω² vs η² bias (effectsize R pkg / CRAN vignette; Lakens 2013) | CRAN `effectsize`; Lakens 2013 *Front. Psychol.* **[fetched]** | η² overestimates population effect size vs the less-biased ω², "particularly for studies with smaller sample sizes" — bears on the headline η²_surr=0.37 computed on 63 cell means (P1-2). Cohen's 0.01/0.06/0.14 benchmarks are contested. |
| C6 | Hutter, Hoos, Leyton-Brown — *fANOVA* | ICML 2014; PMLR v32 **[repo-doc: NOVELTY_V2]** | The canonical variance-decomposition-of-design-choices method; a reviewer may ask "why not fANOVA?" of the paper's hand-rolled η². |

---

## Axis D — Artifact / reproducibility + null-result acceptance norms

| # | Source | Venue / ID | 1-line relevance |
|---|---|---|---|
| D1 | AAAI-27 main-technical-track-call + submission-instructions + AAAI-26 reproducibility checklist | aaai.org (AAAI-27 live; checklist AAAI-26 proxy) **[repo-doc: AAAI27_VENUE, fetched pages]** | Checklist is reviewer-scored and evidence-based; 7+2 page budget; reviewers not required to read supplement. Four checklist items force a "no" or self-incriminating "yes" against current repo state. |
| D2 | Pineau et al. — *Improving Reproducibility in ML Research (NeurIPS 2019 Reproducibility Program)* | **JMLR v22(164) 2021**; arXiv:2003.12206 **[fetched]** | The origin of the ML Reproducibility Checklist, "subsequently adopted … by AAAI." Grounds why AAAI's checklist is Pineau-derived and stable across years. |
| D3 | NeurIPS 2026 Reviewer Guidelines + "A choice of contribution types" blog | neurips.cc/Conferences/2026/ReviewerGuidelines; blog.neurips.cc 2026-04-16 **[fetched]** | NeurIPS 2026 adds an author-selected **Negative Results** contribution type — but "the significance and originality bar … is high" and it must be "surprising." A well-executed-but-unsurprising null is explicitly excluded. Contrast: AAAI has no such track. |
| D4 | TMLR acceptance criteria / MLRC 2026 (NeurIPS track via TMLR) | jmlr.org/tmlr; MLRC 2026 (deadline 2026-09-30) **[repo-doc: VENUE_NORMS]** | The honest fallback venues if the AAAI window is tight — TMLR ("novelty … not a necessary criterion") but rejects bare nulls without "generalizable insights." |
| D5 | ASAP-Review ICLR 2017–2020 corpus (5,192 papers, full reviews) + archived OpenReview JSON | ASAP-Review dataset **[repo-doc: VENUE_NORMS, offline copies in scratchpad]** | The empirical basis for what real reviewers say to null/measurement papers — "a null is welcome only if it diagnoses its own mechanism." The GATS rejection (ICLR 2019) is the load-bearing datum. |

---

## Axis-adjacent — deep-ensemble UQ criticism (grounds the surrogate mechanism dispute)

| # | Source | Venue / ID | 1-line relevance |
|---|---|---|---|
| E1 | Abe, Buchanan, Pleiss, Zemel, Cunningham — *Deep Ensembles Work, But Are They Necessary?* | **NeurIPS 2022**; arXiv:2202.06985 **[fetched]** | A single larger model replicates ensemble gains (Pearson 0.81 ID / 0.76 OOD); "ensemble diversity does not meaningfully contribute to OOD detection." Undercuts "ensembles are strong UQ baselines" — but cuts both ways for the paper (see 03/06). |
| E2 | Lakshminarayanan, Pritzel, Blundell — *Simple and Scalable Predictive Uncertainty Estimation using Deep Ensembles* | NeurIPS 2017; arXiv:1612.01474 **[fetched]** | The canonical "ensembles give well-calibrated UQ, often beating approximate Bayesian methods" claim — the pro-ensemble pole of the contradiction the paper must survive. |
| E3 | Stanton, Maddox, Wilson — *Bayesian Optimization with Conformal Prediction Sets* | **AISTATS 2023**; PMLR v206:959 **[fetched]** | Coverage-as-validity for optimizer-driven queries; owns ~70% of the paper's premise-coverage diagnostic. "guaranteed validity … query coverage can be significantly improved." |
| E4 | Deshpande & Kuleshov — *Online Calibrated and Conformal Prediction Improves BO* | **AISTATS 2024**; PMLR v238 **[fetched]** | Calibration improves BO — online scope; the nearest prior art the paper must distinguish from its offline coverage claim. |
| E5 | Paine et al. — *Hyperparameter Selection for Offline RL* + *When is Offline HP Selection Feasible?* | arXiv:2007.09055; OpenReview Hvcmr6FSIX8 **[fetched]** | Offline model/HP selection is a *recognized open problem*: "existing methods break the offline assumption … little understanding of the fundamental limitations." Grounds the paper's dead Identity-B obstruction as a real, publishable difficulty. |
| E6 | Tibshirani, Barber, Candès, Ramdas — *Conformal Prediction Under Covariate Shift* | NeurIPS 2019 **[repo-doc: NOVELTY_V2]** | The result Prop 2 restates (weighted conformal) — grounds the "straightforward application" triviality flag (P1-7). |

---

## Coverage check and honest gaps

- **Well covered:** AAAI genre precedent (A1–A11), offline-MBO prior art (B1–B10), the statistics attack
  surface (C1–C6), reproducibility norms (D1–D5), and the ensemble-UQ dispute (E1–E6).
- **Thin, and flagged:** the *NTK / spectral-bias* grounding for the smooth-mean mechanism (sub-Q2) was
  not fetched fresh this session — the mechanism claim is carried at the level of IGNITE/MS-DDEO/RoMA
  (B9/B10), which pre-claim "smoothness helps" but not "the GP's *mean* smoothness is *the* axis." A
  reviewer-grade NTK citation (e.g., Rahaman et al. spectral bias; Jacot et al. NTK) would strengthen
  Section 2 of the manuscript and is the highest-value missing fetch (see 08).
- **Method-ceiling caveat (from VENUE_NORMS):** AAAI reviews are not public, so all reviewer-behavior
  evidence (D5, and 07) is an ICLR/NeurIPS proxy. Treat phrasings as indicative, not AAAI-verbatim.

**Fetched-source tally this session: 14 fresh (WebSearch/WebFetch/Semantic Scholar).** Total distinct
sources in the sweep: **28**, of which 14 are carried from the four already-grounded repo docs with their
primary quotes intact.
