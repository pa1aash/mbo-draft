# 09 · Evidence digest — the load-bearing evidence index

**Step 9 of the research core.** The top ~15 claims the acceptance judgment rests on, each with its
verbatim quote (where verified), citation, and the decision it drives. This is the single high-fidelity
index a downstream drafter reads as primary evidence — higher fidelity than the summaries in 02.

**Provenance codes:** **[F]** fetched from primary this session · **[R]** carried from a repo doc that
fetched+grepped the primary · **[A]** artifact fact (file:line in the repo) · **[P]** paraphrase (quote not
verified verbatim). AAAI reviews are private; all reviewer quotes are an ICLR/NeurIPS proxy.

---

### E1 — AAAI accepts the no-new-method measurement genre on its main track · drives venue viability
> Henderson, Islam, Bachman, Pineau, Precup, Meger, *Deep Reinforcement Learning that Matters*,
> **AAAI 2018** (arXiv:1709.06560). Pure measurement + a seven-factor taxonomy; seeds alone shift the
> distribution: "t = −9.0916, p = 0.0016" (TRPO, HalfCheetah-v1). ~2,397 S2 cites. **[R]**
> Plus Gundersen & Kjensmo (AAAI 2018), Kim (AAAI 2022), Zeng (AAAI 2023 oral). **[R]**
**Drives:** L1 — AAAI is viable; "AAAI is the worst fit" is retracted.

### E2 — A null is welcome only if it diagnoses its own mechanism · drives identity (A vs C)
> GATS (ICLR 2019, **REJECTED**), meta-review: "The concern that most strongly affected the final
> evaluation is the limited insight (and evidence) of the factors that influence performance." All three
> reviewers praised negative results; the paper was rejected anyway. **[R, OpenReview]**
**Drives:** L1, Tension 2 — Identity A (hollow mechanism) draws this rejection; Identity C is the bar.

### E3 — A null is acceptable only if declared · drives abstract framing
> ICLR 2026 reviewer (QIJk2xjJI3): "is the purpose of the paper to display a null result (which I think is
> not an issue, but it should be stated as such)?" **[R, OpenReview]**
**Drives:** declare the null in the abstract, scoped to Design-Bench at N=7.

### E4 — The repo's own control refutes the paper's mechanism · drives the P0-0 reject-driver
> `gradtune.py:1-5` states the decision rule: "If even the best-tuned gradient config still underperforms
> perturbation, the collapse is surrogate geometry (genuine), not tuning." It **fails on 3/4 tasks**:
> `trust=0.1` moves Branin −8.17 → −0.54 (15×), Styblinski 5.56 → 34.30 (6×); on Ackley plain gradient
> already beats perturbation. The string "trust" never appears in `main.tex`. **[A]** `FLAW_LEDGER.md` P0-0.
**Drives:** L2, Tension 2 — unconditional blocker; must be reported; re-scope Contribution 2.

### E5 — The ensemble trains on raw targets while both GPs z-score · drives the headline confound
> `mbo.py:36-37` raw `y`; `mbo.py:255` / `311-312` standardize. Targets span Griewank ≈ −2600 to Branin
> ≈ −10; at fixed lr/epochs the ensemble cannot fit the large-scale tasks. "inductive bias" and
> "unnormalized targets" are observationally equivalent under every control the paper runs. **[A]**
> `FLAW_LEDGER.md` P0-2.
**Drives:** L2, Tension 1 — η²_surr=0.37 is confounded; run X1 first; "nothing else until P0-2 is run."

### E6 — Deep ensembles perform relatively poorly for BO (literature supports the finding direction) · drives surrogate axis
> Li, Rudner, Wilson, *A Study of BNN Surrogates for Bayesian Optimization*, **ICLR 2024**
> (arXiv:2305.20028, S2: 65 cites): "(i) the ranking of methods is highly problem dependent, suggesting the
> need for tailored inductive biases; … (iv) deep ensembles perform relatively poorly." **[F, verbatim
> abstract]** Cite as ICLR 2024 (S2 back-propagates year 2023 from arXiv).
**Drives:** L2, Tension 4 — owns the paper's findings ~90–95%; concede+cite, don't claim; its calibration
mechanism *contradicts* the paper's smoothness mechanism (the point of novelty).

### E7 — Ensemble gains are a capacity effect a single larger model replicates · drives ensemble-fairness
> Abe, Buchanan, Pleiss, Zemel, Cunningham, *Deep Ensembles Work, But Are They Necessary?*, **NeurIPS
> 2022** (arXiv:2202.06985): ensemble vs single-larger-model improvements correlate "0.81 on the
> in-distribution test set … 0.76" OOD; "ensemble diversity … does not meaningfully contribute to … OOD
> detection." **[F]**
**Drives:** L2, Tension A — strengthens "ensembles lose" if the baseline is fair; but see E8 (the free
strawman objection).

### E8 — Deep ensembles are strong, often-better-than-Bayesian UQ baselines · drives the strawman risk
> Lakshminarayanan, Pritzel, Blundell, *Simple and Scalable Predictive Uncertainty Estimation using Deep
> Ensembles*, **NeurIPS 2017** (arXiv:1612.01474): well-calibrated uncertainty "often outperforming
> approximate Bayesian methods." **[F, P]**
**Drives:** L2 — makes "your ensemble is a strawman" a free objection given P1-3 (no validation split, σ
unfloored). The paper must move the ensemble from strawman to fair-and-still-loses.

### E9 — The optimizer/search is the neglected axis (the named belief the reversal targets) · drives offensive framing
> Chemingui, Deshwal, Hoang, Doppa, PGS, **AAAI 2024** (arXiv:2405.05349): "Prior approaches … have
> primarily focused on learning robust surrogate models … we introduce a new learning-to-search
> perspective." **[R, verified]** The paper's η²_opt = 0.01 contradicts this.
**Drives:** L2/Tension B — the best "named belief, refuted" slot; unearned until matched-budget X3; PGS
authors may review.

### E10 — η²_opt=0.01 is confounded (unequal budgets) · drives "the reversal is unearned"
> grad/perturb consume 256 oracle calls and report the best 128; CMA consumes 128 (`FLAW_LEDGER.md` P0-1).
> Surrogate-query budgets: gradient 25,600 vs perturbation 4,096 vs CMA 432–3,012 — 6×–59× (P1-1). **[A]**
**Drives:** L2 — cannot claim "optimizer doesn't matter" from unmatched budgets; run X1+X3 before the
reversal framing.

### E11 — Design-Bench's simple baselines are competitive / it under-discriminates · drives Contribution 3 novelty
> Trabucco, Geng, Kumar, Levine, *Design-Bench*, **ICML 2022** (arXiv:2202.08450): "a classical CMA-ES
> baseline is competitive with several highly sophisticated MBO methods in 4 of 8 tasks … the need for
> careful tuning and standardization." **[F]** Kim survey: benchmarks "make it difficult to distinguish …
> more sophisticated algorithms." **[R]**
**Drives:** L4/Tension F — the non-discrimination complaint is ~80% pre-owned; the surviving contribution is
the paired omnibus measurement, not the observation.

### E12 — The field's survey names the paper's confound almost verbatim · drives motivation (threat→asset)
> Kim, Gu, Yuan, Yun, Liu, Bengio, Chen, *Offline MBO: Comprehensive Review*, **TMLR** (arXiv:2503.17286,
> S2: 20 cites): gains may stem from "superior surrogate modeling, improved optimization strategies, or
> mere chance." **[F for record; R for quote]**
**Drives:** Tension F — cite early; the paper answers a stated open problem rather than posing a new one.

### E13 — The mean-rank CD test is pool-dependent (Benavoli), and the paper instantiates the flaw · drives statistics fix
> Benavoli, Corani, Mangili, *Should We Really Use Post-Hoc Tests Based on Mean-Ranks?*, **JMLR 2016**
> (arXiv 2015, S2: 467 cites): "the outcome of the mean-ranks test depends on the pool of algorithms
> originally included … significant if the pool comprises C, D, E and not significant if … F, G, H … use …
> the sign-test or the Wilcoxon signed-rank test." **[F, verbatim abstract]** The paper's CD matrix pools 11
> cells including undefined `ens_conformal:*` arms (`FLAW_LEDGER.md` P1-2). **[A]**
**Drives:** L5/Tension D — unify the pool, add per-pair tests; keep the CD diagram reviewers request.

### E14 — Point estimates over few runs mislead; use interval estimates / IQM · drives the N=7 artifact
> Agarwal, Schwarzer, Castro, Courville, Bellemare, *Deep RL at the Edge of the Statistical Precipice*,
> **NeurIPS 2021, Outstanding Paper** (arXiv:2108.13264, `rliable`): most results "compare point estimates
> … ignoring the statistical uncertainty implied by … a finite number of training runs"; advocate "interval
> estimates … performance profiles … interquartile mean." **[F]** Demšar's own N>10, k>5 rule places N=7
> below threshold. **[R]** Yauney (ICLR 2026) ships power-as-headline with an instrument. **[R]**
**Drives:** L5/Tension 3 — convert N=7 from hidden weakness into the declared power-spec artifact (X4).

### E15 — The released code does not reproduce its own reported numbers · drives the reproducibility-checklist failure
> Generators for `bootstrap_ci`, `beta0`, `subsample_control`, `gp_coverage`, `stats_9cell`, `rf_robustness`
> are absent from the repo; both bootstraps resample *tasks*, not the *seeds* the text describes;
> `run_all.py:60` still writes `rho_knn`, absent from both live result files. **[A]** `FLAW_LEDGER.md` P0-4.
> AAAI-27's checklist is reviewer-scored and evidence-based (`AAAI27_VENUE.md` C.4). Fig 1 vs Fig 3 disagree
> on 6/9 DB cells (P0-6); a load-bearing RF-defense sentence is arithmetically backwards ("0.34 no smaller
> than 0.39", P0-7). **[A]**
**Drives:** artifact axis — four checklist items force a "no" or self-incriminating "yes"; P0-4 must close
before the checklist can be signed.

---

## Coverage integrity (which axis each datum serves)

| Axis | Load-bearing evidence |
|---|---|
| **Manuscript** | E1, E2, E3, E6, E9, E12 |
| **Experiments** | E4, E5, E7, E8, E10, E11 |
| **Statistics** | E13, E14 (+E10, E11) |
| **Artifact/reproducibility** | E15 (+E4 the artifact refutation) |

**Two things no citation can supply, restated for the drafter (from 08):** (1) whether η²_surr survives
target normalization (X1) and (2) whether the DB null survives the exact-oracle subset (X11). The paper's
decisive evidence is *experimental and unrun*, not *bibliographic and missing*. Every external claim above
either concedes a finding to prior work (E6, E11, E12) or supplies an attack the paper must pre-empt (E8,
E13, E14) — none of them, found or not, changes the direction. The direction is set by the artifact (E4,
E5, E10, E15), and the fix is the re-run.
