# AAAI-27 venue dossier — topics, reviewer pools, reproducibility, page budget

**Compiled 2026-07-17. FETCH-not-recall discipline:** every AAAI fact below carries the
fetched URL and the year of the page it was read from. Nothing here is asserted from memory.

**Fetch tally:** 5 AAAI pages fetched successfully (4 on the live AAAI-27 site, 1 on the
AAAI-26 site as the labeled fallback for the reproducibility checklist) · 1 NOT FETCHABLE
(`https://aaai.org/authorkit27/` returns a 5.2 MB `application/zip` binary, not text — the
LaTeX kit + checklist live inside that archive and cannot be read as a page).

**Pages read (all navigated from `aaai.org`, not constructed from memory):**

| # | URL | Year of page | Status |
|---|---|---|---|
| 1 | https://aaai.org/conference/aaai/aaai-27/ | AAAI-27 (read 2026-07-17) | FETCHED |
| 2 | https://aaai.org/conference/aaai/aaai-27/areas-and-topics/ | AAAI-27 (read 2026-07-17) | FETCHED |
| 3 | https://aaai.org/conference/aaai/aaai-27/main-technical-track-call/ | AAAI-27 (read 2026-07-17) | FETCHED |
| 4 | https://aaai.org/conference/aaai/aaai-27/submission-instructions/ | AAAI-27 (read 2026-07-17) | FETCHED |
| 5 | https://aaai.org/conference/aaai/aaai-26/reproducibility-checklist/ | **AAAI-26** (read 2026-07-17) | FETCHED (fallback for C.4) |
| — | https://aaai.org/authorkit27/ | AAAI-27 | **NOT FETCHABLE** (ZIP binary) |

AAAI-27 uses OpenReview (`https://openreview.net/group?id=AAAI.org/2027/Conference`), 7 pages
main + up to 2 references, abstract deadline **2026-07-21**, full paper **2026-07-28**, supplementary
**2026-07-31** (source: page 1, AAAI-27, read 2026-07-17). **This means the submission window is
open now** — the page-budget and checklist constraints below are live, not hypothetical.

---

## C.1 — The verbatim AAAI-27 topic list

**Source: https://aaai.org/conference/aaai/aaai-27/areas-and-topics/ (AAAI-27, read 2026-07-17).**

### Top-level areas (17)

Application Domains (APP) · Audio and Speech Processing (AUD) · Cognitive Modeling & Cognitive
Systems (CMS) · Constraint Satisfaction and Optimization (CSO) · Computer Vision (CV) · Data
Mining & Knowledge Management (DMKM) · Game Theory and Economic Paradigms (GTEP) · Humans and AI
(HAI) · Knowledge Representation and Reasoning (KRR) · Multiagent Systems (MAS) · **Machine
Learning (ML)** · Natural Language Processing (NLP) · Philosophy and Ethics of AI (PEAI) ·
Planning, Routing, and Scheduling (PRS) · Intelligent Robotics (ROB) · **Reasoning under
Uncertainty (RU)** · **Search and Optimization (SO)**.

### Machine Learning (ML) — full keyword list, quoted verbatim

> "ML: Adversarial Learning & Robustness, ML: AutoML & Hyperparameter Tuning, ML: Bayesian
> Learning & Uncertainty Quantification, ML: Causal Learning, ML: Classification, Regression &
> Kernel Methods, ML: Clustering & Unsupervised/Self-Supervised Learning, ML: Data-Centric AI,
> Synthetic Data & Data Curation, ML: Deep Generative Models & Autoencoders, ML: Deep Learning
> Algorithms, Architectures & Foundation Models, ML: Deep Learning Theory & Learning Theory, ML:
> Dimensionality Reduction, Manifolds & Matrix/Tensor Methods, ML: Distributed & Federated
> Learning, ML: Efficient, Edge, Green & Hardware-aware ML, ML: Ensemble & Multi-class/Multi-label
> Learning, ML: Ethics, Bias, Fairness & Privacy, **ML: Evaluation, Benchmarking, Datasets &
> Analysis**, ML: Evolutionary Learning, ML: Graph-based Machine Learning, ML: Machine Unlearning,
> Data Deletion & Model Editing, ML: Mixture of Experts (MoE), ML: Multimodal & Large Multimodal
> Models (LMMs), ML: Neuro-Symbolic Learning, ML: Online Learning & Bandits, ML: Optimization for
> ML, ML: Other Foundations of Machine Learning, ML: Post-Training, Fine-Tuning & Model Alignment,
> ML: Probabilistic Circuits & Graphical Models, ML: Quantum Machine Learning, ML: Reasoning &
> Test-Time Compute, ML: Reinforcement, Imitation & Inverse RL, ML: Representation Learning, ML:
> Scalability of ML Systems, ML: Semi-Supervised & Active Learning, ML: Time-Series & Data
> Streams, ML: Transfer, Domain Adaptation & Continual Learning, ML: Transparent, Interpretable &
> Explainable ML, ML: World Models, Simulation & Environment Models"

The four keywords load-bearing for this paper: **ML: Evaluation, Benchmarking, Datasets & Analysis**;
**ML: Bayesian Learning & Uncertainty Quantification**; **ML: Optimization for ML**; **ML: AutoML &
Hyperparameter Tuning**. (Also relevant secondaries: ML: Ensemble & Multi-class/Multi-label Learning.)

### Search and Optimization (SO) — full keyword list, verbatim

> "SO: Algorithm Configuration & Sampling-based Search, SO: Combinatorial & Non-convex
> Optimization, SO: Distributed & Mixed Discrete/Continuous Search, SO: Evolutionary Computation,
> SO: Heuristic, Adversarial & Local Search, SO: Metareasoning, Metaheuristics & Learning to
> Search, SO: Other Foundations of Search & Optimization"

(CMA-ES lands squarely under **SO: Evolutionary Computation**; the gradient/perturbation/CMA sweep
touches **SO: Algorithm Configuration & Sampling-based Search**.)

### Reasoning under Uncertainty (RU) — full keyword list, verbatim

> "RU: Causality, RU: Decision/Utility Theory & Sequential Decision Making, RU: Other Foundations
> of Reasoning under Uncertainty, RU: Probabilistic & Relational Probabilistic Models, RU:
> Probabilistic Inference & Graphical Models, RU: Stochastic Optimization, RU: Uncertainty
> Representations"

(The LCB/coverage/conformal material could route to **RU: Uncertainty Representations** or **RU:
Stochastic Optimization** — see C.3 for why that is dangerous here.)

### AAAI's own rules for choosing topics — quoted verbatim (same page, AAAI-27)

- Number allowed: authors choose **"one primary keyword (mandatory) and (optionally) up to five
  secondary topics."**
- Primary rule: **"The main principle for choosing a paper's primary topic is to identify the
  subarea to which the paper makes its main contribution."** … **"a reviewer who is an expert in
  that subarea will be positioned to evaluate the paper most effectively."**
- Interdisciplinary steer: **"Focus on where the primary contribution lies, and which community
  will benefit the most from reading the paper."**
- Secondary steer: **"When choosing secondary topics, it is helpful to consider two questions.
  First, all things being equal, what beyond the primary topic should the reviewers be expert in?"**
- The double-edged-sword warning (verbatim): **"Adding secondary topics can be a double-edged
  sword. If the paper's contributions are relatively simple from the point of view of an expert
  in a secondary topic, then that expert may give a poor rating, perhaps overlooking the paper's
  value in another domain."**

These four sentences are the decision rules applied in C.2 and C.3. AAAI is explicit that the
primary keyword *summons the reviewer pool* and that a mis-chosen secondary *hands a hostile
expert a veto*. For a confounded measurement paper (`FLAW_LEDGER.md`), that is not boilerplate —
every subarea that could be a secondary is also the subarea that owns one of our confounds.

---

## C.2 — Per-identity primary-topic recommendation

Applied against AAAI-27's stated rule: *identify the subarea to which the paper makes its main
contribution* / *which community will benefit the most* (areas-and-topics, AAAI-27, 2026-07-17).

**Bottom line, all four identities:** the recommended PRIMARY is
**`ML: Evaluation, Benchmarking, Datasets & Analysis`**. It is the literal AAAI keyword for the
genre, and `VENUE_NORMS.md` documents that this venue has published exactly this genre four times
on the ML technical track (Henderson AAAI-18, Gundersen & Kjensmo AAAI-18, Kim AAAI-22, Zeng
AAAI-23-oral). The identities differ not in the primary but in *what the pool will attack* and in
whether the identity can survive that pool. The wrong move — for every identity — is to let the
GP/calibration content or the optimizer content pull the primary into **Bayesian Learning & UQ**,
**Optimization for ML**, or the **SO** area, each of which summons a specialist who owns a P0/P1
flaw. Same manuscript, opposite verdict.

### The three reviewer pools this manuscript can summon, and what each attacks

- **`ML: Evaluation, Benchmarking, Datasets & Analysis`** — *the home pool.* Rewards
  benchmark-validity findings, controlled decompositions, and reusable diagnostics; tolerates a
  declared null (the Henderson/Kim/Zeng precedent). Attacks on **contribution framing, not
  correctness**: "no new SOTA / low technical contribution / so what / confirms what's known"
  (`VENUE_NORMS.md`: every measurement-paper reject in the ~600-review corpus died on framing).
  Will open the artifact and hit **P0-4** (reported CIs/controls with no generating code) and
  **P0-0** (the released `gradtune.py` refutes the mechanism). Will raise the free competing
  explanation — *"Design-Bench oracles are already known to be broken"* — that N=7 cannot rule out
  (`VENUE_NORMS.md` central vulnerability).
- **`ML: Bayesian Learning & Uncertainty Quantification`** — *the audit pool.* Reads the GP line
  by line: ARD Matérn-5/2, marginal-likelihood fit, the LCB/β choice, and the two conformal
  propositions. **This pool kills the paper as-is:** it catches **P0-2** on sight (the ensemble
  regresses on raw targets spanning −2613…+36 while both GPs z-score — the η²_surr headline is
  confounded with target scaling), reads **Prop 1 as a tautology and Prop 2 as a restatement of
  Tibshirani 2019** (**P1-7**; `VENUE_NORMS.md` notes conformal "straightforward application"
  papers are rating-3 rejects), and demands the held-out NLL/RMSE per surrogate that the repo
  never computes (**P1-3**, MISSING) before accepting "inductive bias, not calibration."
- **`ML: Optimization for ML` / the `SO` area (esp. `SO: Evolutionary Computation`)** — *the
  optimizer pool.* Knows gradient ascent needs tuning and knows CMA-ES. Catches **P0-0** (a trust
  region closes the ensemble×gradient collapse on 3 of 4 tasks — the collapse is an *untuned*
  optimizer, not surrogate geometry) and **P1-1** (surrogate-query budgets unmatched 6×–59×, CMA
  starved on exactly the low-d tasks that carry the headline). Reads "use a conservative
  optimizer" as "search less." This pool voids the interaction claim.

### Identity A — Repaired Measurement

- **Primary: `ML: Evaluation, Benchmarking, Datasets & Analysis`.** Main contribution is a
  de-confounded surrogate×optimizer decomposition — a measurement, not a method. AAAI's rule
  ("subarea to which the paper makes its main contribution") points here unambiguously; the
  benefiting community is the offline-MBO/benchmarking audience.
- **Pool it summons & what it attacks:** the home pool. It tolerates the null but demands a
  mechanism. **This is A's fatal weakness:** `VENUE_NORMS.md` (verbatim ICLR reviewer corpus)
  shows a repaired measurement whose mechanism section is hollow gets the GATS rejection —
  *"a null is welcome only if it diagnoses its own mechanism."* A's mechanism is precisely what
  **P0-0** hollows out. **A is the identity that draws the friendliest pool and still loses**,
  because P0-0 is unreported and the pool opens the repo. Recommend A *only* if the grid is
  re-run with a tuned gradient optimizer and P0-0 is disclosed — otherwise A degrades into E by
  accident and without the framing that makes E survivable.

### Identity C — Mechanism (smoothness is the single axis)

- **Primary: `ML: Evaluation, Benchmarking, Datasets & Analysis`** (the keyword's "& Analysis"
  clause is the home for a mechanism-by-manipulation study). **Do NOT** set the primary to
  `ML: Bayesian Learning & UQ` despite the GP/smoothness content — that summons the audit pool
  into a kill zone (P0-2, P1-7, P1-3). The *contribution* is the mechanism (smoothness governs the
  gap, the gradient collapse, the coverage failure, and the synthetic→real transfer, shown by
  bidirectional manipulation); the *community that benefits* is the evaluation/benchmarking one
  that has been comparing surrogates without a mechanism.
- **Pool it summons & what it attacks:** the home pool — which `VENUE_NORMS.md` says states C's
  bar *literally* ("the work would have been much more significant had the authors offered a
  mechanism"; C "is not the ambitious option; it is the minimum"). C is the strongest fit to the
  pool's stated standard. The danger is self-inflicted: the mechanism's own content (posterior-mean
  smoothness, calibration, conformal) is exactly what a UQ reviewer added as a *secondary* would
  audit — so C's topic strength and C's flaw exposure are the same surface. Recommend C's primary
  here **and** keep every UQ/optimization keyword off the secondary list (C.3) until P0-2/P0-0 are
  fixed. C is the recommended identity for this venue *conditional on those fixes*.

### Identity D — Confound Taxonomy ("Reevaluating Evaluation" shape)

- **Primary: `ML: Evaluation, Benchmarking, Datasets & Analysis`** — the cleanest fit of all four.
  The contribution *is* an evaluation artifact: a named three-part confound taxonomy
  (surrogate×optimizer coupling, target scaling, candidate-selection + oracle budget), a
  de-confounding protocol, a diagnostic, and a demonstration that rewarded differences move under
  control. This is the `balduzzi2018reevaluating` / Henderson genre the paper already cites, and
  the benefiting community is unambiguously the benchmarking one.
- **Pool it summons & what it attacks:** the home pool, at its most receptive to *this* shape.
  Attack surface: (i) the paper's own anticipated objection — *"that these benchmarks are imperfect
  is already known"* — so the taxonomy must be the *first controlled measurement*, not a complaint;
  (ii) the free competing mechanism (broken oracles) on Contribution 3, which D must convert to a
  controlled-for variable (the exact-oracle subset check, `VENUE_NORMS.md` X11). D is the
  lowest-variance route to acceptance because its contribution is a *thing* (the protocol +
  diagnostic), which is the "every accepted paper shipped an artifact" rule. **Its risk is
  reflexive:** each of the three named confounds is owned by a P0 flaw in *our own* repo (P0-1/P0-3
  coupling, P0-2 scaling, P0-1 selection+budget), so D must be built on the *fixed* grid or it is a
  taxonomy that indicts its own artifact.

### Identity E — The Reversal (pre-registered-then-refuted)

- **Primary: `ML: Evaluation, Benchmarking, Datasets & Analysis`.** The contribution is
  meta-methodological: offline-MBO evaluation is hard enough that the authors' own pre-registered
  optimizer hypothesis (η²_opt=0.01, refuted — **P1-5**) and its replacement mechanism (refuted by
  the authors' own `gradtune` control — **P0-0**) are the evidence. The benefiting community is
  again evaluation/benchmarking, plus anyone doing pre-registration in ML.
- **Pool it summons & what it attacks:** the home pool, in the mode most tolerant of a null —
  because E *declares* the null and the refutation up front, which `VENUE_NORMS.md` shows is the
  line between an accepted and a rejected null ("a null is acceptable if *declared*"). E is the only
  identity for which **P0-0 is an asset rather than a fatal omission** — a refuted pre-registered
  prediction is evidence of a real test (P1-5: "it *raises* credibility"). Attack surface: "what do
  I take away" / thin constructive deliverable — E must still ship the coverage diagnostic
  (Algorithm 1) as its artifact or it is a confessional with no tool. E is the highest-novelty,
  highest-variance identity; it is the honest fallback if the P0-0 re-run cannot be completed before
  the 2026-07-28 deadline, because it does not *require* the mechanism to survive.

---

## C.3 — Secondary topics, under AAAI's double-edged-sword rule

AAAI-27 allows up to five secondary keywords (areas-and-topics, AAAI-27, 2026-07-17). The rule:
*"If the paper's contributions are relatively simple from the point of view of an expert in a
secondary topic, then that expert may give a poor rating."* For each candidate secondary below I
ask AAAI's own question — **would an expert in THAT subarea find our contribution trivial (or
flawed) from their vantage?** If yes, recommend against.

| Candidate secondary | Would that expert find us trivial/flawed? | Recommendation |
|---|---|---|
| **ML: Bayesian Learning & Uncertainty Quantification** | **Yes — and worse than trivial.** A UQ expert finds "GPs have smooth Matérn priors" trivial *and* catches P0-2 (raw-target ensemble vs z-scored GP) and reads Prop 1/2 as tautology/restatement (P1-7). Trivial-from-their-vantage → poor rating, exactly the failure the rule names. | **Against**, while P0-2 & P1-7 stand. This is the single most damaging secondary. |
| **ML: Optimization for ML** | **Yes.** An optimization expert finds "match your query budgets" and "tune the gradient step" obvious, and reads the ensemble×gradient collapse as an artifact of an untuned optimizer (P0-0) rather than a finding. | **Against**, while P0-0 & P1-1 stand. |
| **SO: Evolutionary Computation** (or SO: Algorithm Configuration) | **Yes.** A CMA-ES expert immediately sees CMA is budget-starved 8.5×–59× (P1-1) on exactly the low-d tasks carrying the headline — a protocol flaw, not a result. | **Against.** Do not summon the evolutionary-computation pool onto a starved CMA. |
| **ML: AutoML & Hyperparameter Tuning** | **Yes.** The matched-tuning control (which gives the ensemble and gradient *zero* tuning while it's the GP that historically got tuned — the P0-0/T1 asymmetry) reads to an AutoML expert as under-tuning, not as a fair control. | **Against**, while the matched arm is asymmetric. |
| **ML: Ensemble & Multi-class/Multi-label Learning** | **Yes.** The ensemble is unregularized, unvalidated, never early-stopped, σ unfloored (P1-3). An ensemble expert reads it as a strawman surrogate and discounts η²_surr. | **Against.** |
| **RU: Uncertainty Representations** / **RU: Stochastic Optimization** | **Partly.** The coverage-diagnostic framing is genuinely novel to this pool, but the conformal props (P1-7) and the "σ is a weak error signal, ρ≈0.1" claim invite the same audit as Bayesian Learning. Double-edged. | **Against for now**; reconsider only if Prop 2's weighted repair is *implemented* (currently not — P1-7). |
| **ML: Data-Centric AI, Synthetic Data & Data Curation** | **No obvious hostile expert.** The synthetic-suite / Design-Bench validity contrast is on-topic here and our contribution is not trivial from this vantage; but it adds little reviewer expertise the primary lacks. | **Weak yes** — the least-hostile secondary if one is needed for reviewer coverage. |

**The sharp finding for C.3:** because the paper's own thesis is a *confound taxonomy*, **every
deep-technical ML/SO subarea that would be a natural secondary is also the subarea that owns one
of our P0/P1 confounds.** A secondary keyword here does not just add expertise — it hands a veto to
the one expert who can kill the corresponding claim. The disciplined move is therefore **minimal
secondaries**: primary `ML: Evaluation, Benchmarking, Datasets & Analysis`, and at most one
low-hostility secondary (`ML: Data-Centric AI, Synthetic Data & Data Curation`), and **only after**
P0-0 and P0-2 are fixed — never `Bayesian Learning`, `Optimization for ML`, or the `SO` keywords
while the ledger stands. This holds for all four identities; C and D can *afford* the Data-Centric
secondary once fixed, A and E should stay single-keyword to avoid drawing the audit pool onto an
unrepaired mechanism.

---

## C.4 — Reproducibility checklist, item by item, against current repo state

**AAAI-27 requirement (verbatim, main-technical-track-call, AAAI-27, 2026-07-17):** *"All authors
must complete a reproducibility checklist to facilitate replication of the reported research."*
The checklist is *"uploaded separately from the main paper in the designated field of the
submission form"* and **does not count toward the page limit** (submission-instructions, AAAI-27,
2026-07-17). Reviewers *"will evaluate the reproducibility of the reported results based on the
materials included in the submission, and this evaluation will contribute to the final paper
decision."*

**The actual AAAI-27 checklist text is NOT FETCHABLE** — it ships only inside the author-kit ZIP
(`https://aaai.org/authorkit27/`, a 5.2 MB binary). **Reconstruction basis: the AAAI-26
Reproducibility Checklist**, fetched verbatim from
`https://aaai.org/conference/aaai/aaai-26/reproducibility-checklist/` (**AAAI-26**, read
2026-07-17). AAAI's checklist has been stable across AAAI-22…-26 (Pineau-derived); AAAI-27's
submission instructions point authors at the same author-kit checklist, so the items below are the
best available proxy. **Treat P0-4 as a live hazard, not a formality:** the checklist is
reviewer-scored, and answering "yes" to the code items while the released repo cannot regenerate
its own numbers is a falsifiable claim the audit pool will check.

### General section (AAAI-26 items)

| # | Item (AAAI-26 verbatim, abbrev.) | Verdict | Basis / fix |
|---|---|---|---|
| G1 | "conceptual outline and/or pseudocode description of AI methods introduced" | **PASS** | Algorithm 1 (coverage diagnostic) + grid described in §3. |
| G2 | "clearly delineates statements that are opinions, hypothesis, and speculation from objective facts" | **FAIL → FIXABLE** | **P0-7**: a load-bearing sentence states the arithmetic backwards ("0.34 no smaller than 0.39") — a false statement presented as fact. **P1-5**: the pre-registered hypothesis was refuted and the paper does not say so. Fix: correct P0-7; add the P1-5 disclosure paragraph. ~2 h. |
| G3 | "well marked pedagogical references for less-familiar readers" | **PASS** | Background §2 cites the standard lineage. |

### Theoretical contributions (Props 1, 2 → "yes")

| # | Item (AAAI-26 verbatim, abbrev.) | Verdict | Basis / fix |
|---|---|---|---|
| T1 | "assumptions and restrictions are stated clearly and formally" | **PASS** | Prop 2 states exchangeability; Prop 1 states σ>0. |
| T2 | "novel claims are stated formally (e.g., in theorem statements)" | **PASS (item) / substance flag** | Formally stated, but **P1-7**: Prop 1 is a tautology and Prop 2 restates Tibshirani 2019 — a *novelty* problem the audit pool reads off the formal statement. Demote to lemma/remark. |
| T3 | "proofs of all novel claims are included" | **FIXABLE** | `proofs.md` exists but must ship in the supplement; Prop 1's proof is one line. |
| T4 | "proof sketches or intuitions for complex/novel results" | **PASS** | One-line identity + intuition given in text. |
| T5 | "appropriate citations to theoretical tools" | **PASS** | Tibshirani et al. 2019 cited for weighted conformal. |
| T6 | "all theoretical claims are demonstrated empirically to hold" | **FAIL → FIXABLE** | **P1-7**: Prop 2's weighted-conformal repair is *never implemented* — the claim is stated but not demonstrated. Fix: implement the density-ratio reweight or scope the claim to split-conformal. ~1 day. |
| T7 | "all experimental code used to eliminate or disprove claims is included" | **FAIL — the sharp one** | **P0-0**: `gradtune.py` *is* included and it *disproves* the paper's mechanism (trust region closes the collapse on 3/4 tasks) — so answering "yes" is truthful *and self-incriminating*, and "no" is false. **P0-4**: the code that would *support* the claims (β=0 control, subsample control, GP-coverage, 9-cell stats, η² CIs, RF-robustness) does not exist in the repo. The only honest checklist answer indicts the manuscript. Fix: report the `gradtune` result (re-scope, P0-0) **and** write the missing generators (P0-4). Unconditional blocker. |

### Datasets ("yes" — 7 synthetic + 7 Design-Bench)

| # | Item (AAAI-26 verbatim, abbrev.) | Verdict | Basis / fix |
|---|---|---|---|
| D1 | "motivation for why experiments are conducted on selected datasets" | **PASS** | Synthetic-vs-Design-Bench contrast is the paper's spine. |
| D2 | "novel datasets introduced are included in a data appendix" | **FIXABLE** | The synthetic suite is generated at a fixed seed-0 draw (**P1-8**); ship the generator + the exact draw so it is reproducible. ~1 h. |
| D3 | "novel datasets made publicly available with research-use license" | **FIXABLE** | Add license to the anonymized code drop. |
| D4 | "existing datasets have appropriate citations" | **PASS** | Design-Bench (`trabucco2022designbench`) cited. |
| D5 | "existing datasets are publicly available" | **PASS** | Design-Bench is public. |
| D6 | "non-public datasets described with explanation" | **NA** | None. |
| — | *Integrity flags this pool will raise* | **FIXABLE** | **P0-5**: DB "in-distribution" reference set is drawn `uniform(0,1)`, not from the data manifold (one-hot vertices) — invalid for the entire right panel of Fig 3. **P2-6**: "CbAS" is a CEM-style loop, mislabeled. Fix: sample reference from `D`; relabel. ~2 h. |

### Computational experiments ("yes")

| # | Item (AAAI-26 verbatim, abbrev.) | Verdict | Basis / fix |
|---|---|---|---|
| C1 | "states number and range of values tried per hyperparameter" | **FAIL → FIXABLE** | The grid HPs are stated, but the gradient-tuning sweep actually run (`gradtune.py`: lr/steps/**trust** variants) is omitted — the string "trust" does not appear in `main.tex` (**P0-0**). Report the swept ranges. |
| C2 | "any code for pre-processing data is included" | **FAIL → FIXABLE** | **P0-2**: `main.tex` claims "all scores are min-max normalized," but that normalization lives only in `analysis`, not in the training path — the ensemble trains on raw targets while the GPs z-score. The released pre-processing does not match the described pre-processing. Fix: standardize `y` in `train_ensemble` (2 lines), re-run. Unconditional blocker. |
| C3 | "all source code for experiments is included" | **FAIL — the P0-4 core** | **P0-4**: generators for `bootstrap_ci`, `beta0`, `subsample_control`, `gp_coverage`, `stats_9cell`, `rf_robustness` are absent; `run_all.py:60` still writes `rho_knn`, a field absent from both live result files — **the current code does not reproduce the current artifacts.** "Yes" here is falsified by cloning the repo. Fix: write the generators or delete the claims. ~4 h. Unconditional blocker. |
| C4 | "source code will be made publicly available with research-use license" | **FIXABLE** | `anonymous.4open.science` link is stubbed in `main.tex` (commented); un-comment + license. |
| C5 | "code implementing new methods has detailed comments" | **PASS → FIXABLE** | Adequate; add comments to the diagnostic. |
| C6 | "method for setting seeds is described for replicability" | **FIXABLE** | Seeds are positional only (**P3-3**); seed-0 fixed-dataset convention (**P1-8**) is disclosed in-paper but should be in the checklist. |
| C7 | "computing infrastructure is specified (hardware, software, versions)" | **FAIL → FIXABLE** | **P3-3**: zero timestamp / git-sha / hardware / version block in any result file. Fix: add a config/provenance block. ~1 h. |
| C8 | "evaluation metrics are formally described with motivation" | **FAIL → FIXABLE** | **P0-1**: the reported 100th-percentile/p50 is *not the same estimand* across the optimizer axis — grad/perturb report the oracle-selected top-128 of 256, CMA reports 128 of 128. Two quantities in one column. Fix: equalize to 128 proposals, one selection rule, re-run. Unconditional blocker. |
| C9 | "number of algorithm runs is stated" | **PASS** | 30 seeds synthetic, 16 Design-Bench (stated in §3). |
| C10 | "analysis includes distributional information beyond averages" | **FAIL → FIXABLE** | CIs are *claimed* (Table 2) but their generator does not exist (**P0-4**), and the two bootstraps in the repo resample *tasks*, not the seeds the text describes. Fix: implement the described seed-and-task bootstrap. |
| C11 | "significance is judged using appropriate statistical tests" | **FAIL → FIXABLE** | **P1-2**: the ANOVA is hand-rolled, has no error term, leaves `task` unmodeled; η² carries no F/p/df; the rank/CD/TOST matrix silently pools 11 cells (Benavoli's mean-rank-pool objection, instantiated). Fix: proper mixed model or permutation effect size; unify normalization. ~4 h. |
| C12 | "all final hyperparameters for each model are listed" | **FIXABLE** | Grid HPs listed in §3; add a complete supplement table. |

**Checklist verdict:** the paper cannot honestly complete the AAAI checklist today. **Four items
force a "no" or a self-incriminating "yes" and each maps to an unconditional-blocker P0**: T7/C3
(P0-4 — released code does not regenerate reported numbers; `gradtune.py` refutes the mechanism),
C2 (P0-2 — pre-processing in the paper ≠ pre-processing in the code), C8 (P0-1 — inconsistent
estimand). Because AAAI-27 makes the checklist reviewer-scored and evidence-based
(main-technical-track-call, AAAI-27, 2026-07-17), a "yes" that the artifact contradicts is *worse*
than a "no": it is the reproducibility-failure the checklist exists to catch, on a paper whose own
thesis is that unreported implementation details decide results. **P0-4 must be closed before the
checklist can be signed**, and P0-4 must be run together with P0-2/P0-1 in one grid re-run
(`FLAW_LEDGER.md` "nothing else should be acted on until P0-2 is run").

---

## C.5 — Page budget: AAAI-27 hard constraints

**All numbers verbatim from AAAI-27 pages read 2026-07-17.**

- **Main content: 7 pages.** *"Submissions are limited to 7 pages of main content, with a maximum
  total length of 9 pages. Any pages beyond page 7 are reserved exclusively for references."*
  (main-technical-track-call, AAAI-27, 2026-07-17). Confirmed by submission-instructions
  (AAAI-27, 2026-07-17): *"The main submission PDF can have up to 9 pages, with pages 8–9 reserved
  exclusively for references. That is, the main paper can have up to 7 pages of non-references
  content."*
- **References: up to 2 pages** (pages 8–9), references only — they may not hold content.
- **Reproducibility checklist: does not count** toward the page limit; *"uploaded separately from
  the main paper in the designated field of the submission form"* (submission-instructions,
  AAAI-27, 2026-07-17).
- **Supplement — reviewers are NOT required to read it (verbatim):** *"Authors may submit
  supplementary material, but please note that reviewers are not required to review this material.
  Any material critical to the evaluation of the paper should be included in the main body of the
  paper."* (main-technical-track-call, AAAI-27, 2026-07-17.) Three supplement types are allowed:
  *"(1) technical supplement; (2) multimedia archive; and (3) code and data archive."*
- **Deadlines (page 1, AAAI-27, 2026-07-17):** abstract **2026-07-21**, full paper **2026-07-28**,
  supplementary/code **2026-07-31**. Anonymous/double-blind; author on **at most 10** AAAI-27
  submissions (main-technical-track-call, AAAI-27, 2026-07-17).

### Hard constraints these impose on the page-allocation work

1. **Everything load-bearing lives in 7 pages.** Because reviewers are *not required* to read the
   supplement, the de-confounding evidence and — for Identity C/D — the mechanism/taxonomy must fit
   in the 7-page body. The coverage-diagnostic artifact (Algorithm 1), the fixed grid table, and
   the controls table cannot be exiled to the appendix and still count.
2. **The current draft over-subscribes 7 pages.** As written it carries 2 large grid tables
   (Table 1 synthetic 8-col, Table 3 Design-Bench 8-col), the ANOVA table, the controls table, an
   algorithm, 2 propositions, and 6 figures (Figs 1–4, 6, 8). That is a >9-page layout compressed;
   the page-allocation task must cut, not merely reflow. Candidates to demote to supplement: one of
   the two full grid tables (keep the decomposition-map figure), Prop 1/2 → lemma/remark (P1-7
   already recommends this), and the β-sweep figure.
3. **References buy no content room.** The 2 reference pages are references-only, so a citation-heavy
   related-work section (needed to cite the Henderson/Kim/Zeng/Musgrave/Dacrema precedent that
   legitimizes the genre — `VENUE_NORMS.md`) competes for the same 7 body pages as the results.
4. **The checklist is free space** — it is separate and un-counted, so the C.4 fixes (provenance,
   HP ranges, seed method) impose no page cost; only the *in-body* corrections (P0-7 sentence,
   P1-5 disclosure paragraph) consume body lines.
5. **Anything critical must be in-body.** AAAI's own sentence ("Any material critical to the
   evaluation of the paper should be included in the main body") means the P0-0 disclosure, the
   re-run η² numbers, and the exact-oracle-subset check (Contribution 3's survival, `VENUE_NORMS.md`
   X11) cannot be supplement-only. Budget body space for them.

---

*AAAI-27 vs AAAI-26 note:* the C.1–C.3 and C.5 facts are read from **live AAAI-27 pages**. Only the
C.4 checklist *item text* is AAAI-26 (the AAAI-27 items are inside the un-fetchable author-kit ZIP);
AAAI-27's submission instructions direct authors to the author-kit checklist, and AAAI's checklist
has been item-stable across recent years, so the AAAI-26 items are the labeled best proxy. Where
AAAI-27 states a number directly (7+2 pages, deadlines, 10-submission cap, supplement-not-required),
those are AAAI-27, not carried over.
