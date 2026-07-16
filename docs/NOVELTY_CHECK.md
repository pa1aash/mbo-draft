# Prior-Art / Novelty Check — "Decomposing the GP Advantage in Offline MBO" (AAAI-27)

Adversarial prior-art review. Verdicts: **PRIOR WORK FOUND** / **NONE FOUND** / **NOT VERIFIABLE HERE**.

**Bottom line up front:** the paper's *problem statements* are all pre-claimed in print (Design-Bench 2022 named offline model selection as future work; the TMLR 2026 survey named the surrogate-vs-optimizer attribution gap and the non-discrimination complaint almost verbatim). What survives is *measurement and mechanism*, not discovery. Contribution 2 (conformal/LCB) is the weakest and should be demoted. The proposed new direction is novel **only** in its specific combination — the components all exist.

---

## Q4 (HIGHEST PRIORITY). Offline model selection for offline MBO

### (a) Is it a RECOGNIZED OPEN PROBLEM? — **VERDICT: PRIOR WORK FOUND (the problem is explicitly named)**

Not by the Kim et al. survey — by **Design-Bench itself**, in its conclusion:

> "The comparatively high efficacy of even simple baselines such as CMA-ES and naïve gradient ascent suggests the need for careful tuning and standardization of methods in this area. **An interesting avenue for future work in offline MBO is to devise methods that can be used to perform model and hyperparameter selection. One promising approach to address this problem is to devise methods for offline evaluation of produced solutions.**"
> — Trabucco, Geng, Kumar, Levine, *Design-Bench: Benchmarks for Data-Driven Offline Model-Based Optimization*, ICML 2022, [arXiv:2202.08450](https://arxiv.org/abs/2202.08450), §Conclusion (verified in extracted PDF text, p.~10)

Design-Bench Appendix F ("Hyperparameter Selection Workflow") also formalizes the offline constraint:

> "Care must be taken when tuning each of the prescribed algorithms so that only offline information about the task is used for hyperparameter selection. Formally, this means that the hyperparameters, H, are conditionally independent of the particular value of the performance metric M, given the offline task dataset D."

**Kim et al. 2025/2026 survey** (*Offline Model-Based Optimization: Comprehensive Review*, Kim, Gu, Yuan, Yun, Liu, Bengio, Chen; TMLR 2026 w/ Survey Certification; [arXiv:2503.17286](https://arxiv.org/abs/2503.17286)) does **NOT** list model selection among its five future directions. Its §6 directions are verbatim: *Robust and Realistic Benchmarking; Uncertainty Estimation of Surrogate Model; Graphical Surrogate Model; Advanced Generative Modeling; Application to LLM Alignment and AI Safety.*

**But** its §6 contains the single most dangerous sentence for this paper — it names contribution 1's gap:

> "Moreover, existing benchmarks often emphasize overall optimization performance **without clarifying whether observed gains stem from superior surrogate modeling, improved optimization strategies, or mere chance. This lack of distinction underscores the need for independent and rigorous evaluations** of the uncertainty estimation capabilities of the surrogate model in newly developed algorithms."

**Assessment:** Good news and bad news. The problem is *recognized and citable* (strong motivation — quote Design-Bench directly). But the authors cannot claim to have identified the problem. Frame as "answering a question Trabucco et al. (2022) posed."

### (b) Offline RL prior art — **VERDICT: PRIOR WORK FOUND (a mature literature)**

Offline policy selection / offline hyperparameter selection is a well-developed subfield. The paper MUST cite these or a reviewer will:

| Work | Venue | Key point |
|---|---|---|
| Paine, Paduraru, Michi, Gulcehre, Zolna, Novikov, Wang, de Freitas, *Hyperparameter Selection for Offline Reinforcement Learning*, [arXiv:2007.09055](https://arxiv.org/abs/2007.09055) (2020) | arXiv/DeepMind | Canonical statement of the problem; OPE as selection proxy |
| Zhang & Jiang, *Towards Hyperparameter-free Policy Selection for Offline RL*, NeurIPS 2021, [arXiv:2110.14000](https://arxiv.org/abs/2110.14000) | NeurIPS | BVFT-based selection; notes OPE-based selection has its own hyperparameters — "chicken-and-egg" |
| Tang & Wiens, *Model Selection for Offline RL: Practical Considerations for Healthcare Settings*, MLHC 2021, [arXiv:2107.11003](https://arxiv.org/abs/2107.11003) | PMLR v149 | OPE as validation proxy pipeline |
| Kurenkov & Kolesnikov, *Showing Your Offline RL Work: Online Evaluation Budget Matters*, ICML 2022, [arXiv:2110.04156](https://arxiv.org/abs/2110.04156) | ICML | Expected Online Performance; critique of unlimited-budget selection |
| Yang et al., *Pessimistic Model Selection for Offline Deep RL*, [arXiv:2111.14346](https://arxiv.org/abs/2111.14346) | PMLR v216 | Pessimism-based selection |
| Fu et al., *Benchmarks for Deep Off-Policy Evaluation*, ICLR 2021 | ICLR | OPE benchmark |
| *Model Selection for Off-policy Evaluation: New Algorithms and Experimental Protocol*, [arXiv:2502.08021](https://arxiv.org/abs/2502.08021) (2025) | — | States model selection for offline evaluation is "under-investigated" |

**Assessment:** The *idea* "select offline using oracle-free proxies" is standard in offline RL. Novelty cannot rest on it.

### (c) CALIBRATION / COVERAGE as the selection signal — **VERDICT: PRIOR WORK FOUND (outside offline MBO)**

- **CC-Select** — *Conformal Prediction Assessment: A Framework for Conditional Coverage Evaluation and Selection*, [arXiv:2603.27189](https://arxiv.org/abs/2603.27189) (Mar 2026). Selects models by optimizing **conditional coverage**; introduces Worst-Slab Coverage (WSC) and a "Conditional Validity Index (CVI)... as a proxy for the unobservable conditional coverage probability, enabling model selection through a reliability estimator." This is *coverage-driven model selection*, explicitly.
- **CROMS** — Bao, Hu, Ren, Zhao, Zou, *Optimal Model Selection for Conformalized Robust Optimization*, [arXiv:2507.04716](https://arxiv.org/abs/2507.04716) (2025). Model selection for conformal robust *decision-making*: "the downstream decisions critically depend on model selection." Selects to minimize decision risk (not coverage per se), but couples conformal validity to a downstream optimizer's decision quality — conceptually adjacent.
- Coverage-matched hyperparameter tuning appears in the conformal literature generally (tune to match a target leave-one-out coverage).

**Assessment:** "Use coverage as a model-selection signal" is **not novel in general**. It is novel *as applied to offline MBO cell selection*.

### (d) Offline surrogate/optimizer selection for offline MBO — **VERDICT: PRIOR WORK FOUND (nearest neighbor is in evolutionary computation, not deep-learning MBO)**

**This is the biggest under-the-radar threat.** The evolutionary-computation "offline data-driven evolutionary optimization" (offline DDEO) community has been doing oracle-free offline surrogate selection since 2022, and the Design-Bench-lineage MBO literature almost never cites it.

1. **MS-DDEO** — *Offline data-driven evolutionary optimization based on model selection*, **Swarm and Evolutionary Computation, 2022**, DOI [10.1016/j.swevo.2022.101080](https://doi.org/10.1016/j.swevo.2022.101080) (25 citations). **The closest prior work to the paper's proposed direction.**
   - Builds a **model pool of four RBF models with different smoothness degrees** and selects among them offline.
   - Two **oracle-free** selection criteria: **Model Error Criterion** (uses ranking-top data as a held-out test set to test ability to predict the optimum) and **Distance Deviation Criterion** (estimates reliability via distance between the predicted solution and ranking-top data — *this is essentially "proposal displacement"*).
   - Reported framing: "four RBF models with different hyper-parameters construct the model pool with different smoothness, where more smoothness means the model has less multimodal, which also means there is less high-frequency information in the frequency domain." **This also touches Q2's mechanism.**
2. **IBEA-MS** — *Performance Indicator-Based Adaptive Model Selection for Offline Data-Driven Multiobjective Evolutionary Optimization*, **IEEE Trans. Cybernetics, 2022**, DOI [10.1109/TCYB.2022.3170344](https://doi.org/10.1109/tcyb.2022.3170344) (42 citations). Code: https://github.com/HandingWangXDGroup/IBEA-MS
3. *Offline evolutionary optimization with problem-driven model pool design and weighted model selection indicator* (**MSEA**), Swarm and Evolutionary Computation, 2025, [S2210650225001920](https://www.sciencedirect.com/science/article/abs/pii/S2210650225001920) — "significant improvements over MS-DDEO"; replaces the RBF-smoothness-based pool.
4. Wang, Jin et al., *Offline Data-Driven Evolutionary Optimization Using Selective Surrogate Ensembles*, IEEE TEVC 2019, DOI 10.1109/TEVC.2018.2834881.

**CRISP VERDICT ON THE PROPOSED DIRECTION:**

> **Partially novel — the framing is novel, the ingredients are not.** "Coverage-driven offline surrogate×optimizer selection for offline MBO" is **not** a green field. Specifically:
> - Offline oracle-free **surrogate** selection for offline optimization: **DONE** (MS-DDEO 2022, IBEA-MS 2022, MSEA 2025).
> - **Coverage/conformal** as a model-selection signal: **DONE** (CC-Select 2026; CROMS 2025).
> - Oracle-free proxies for offline method selection: **DONE, mature** (offline RL, 2020–2025).
> - Selecting the **optimizer** jointly with the surrogate, for offline MBO, using **conformal premise-coverage** specifically: **NONE FOUND.** This joint cell-selection framing is where novelty lives.
>
> **Nearest prior work: MS-DDEO (Swarm Evol. Comput. 2022).** A reviewer from the EC community will find it immediately. It already does offline model selection over a smoothness-graded surrogate pool using a displacement-like criterion — i.e. two of the paper's four proposed oracle-free quantities, in the same problem class.
>
> **Recommendation:** cite MS-DDEO/IBEA-MS explicitly and differentiate on (i) selecting the *optimizer* as well as the surrogate, (ii) *distribution-free conformal* coverage rather than heuristic criteria, (iii) deep-learning surrogates + Design-Bench rather than RBF + EC benchmarks. Do **not** claim "first offline model selection for offline MBO" — that claim is refutable with one citation.

---

## Q1. Controlled factorial decomposition surrogate × acquisition optimizer

**VERDICT: NONE FOUND for the factorial itself; PRIOR WORK FOUND for a large share of the *finding*.**

### What Li / Rudner / Wilson actually owns

**Correction the authors need: the paper is ICLR 2024, not ICLR 2023.** (arXiv May 2023; published *Proceedings of ICLR 2024*.)
Yucen Lily Li, Tim G. J. Rudner, Andrew Gordon Wilson, *A Study of Bayesian Neural Network Surrogates for Bayesian Optimization*, **ICLR 2024**, [arXiv:2305.20028](https://arxiv.org/abs/2305.20028).

Verified from the full HTML text:

- **Acquisition is FIXED, and there is no optimizer factor.** > "We use Monte-Carlo based Expected Improvement (Balandat et al., 2020) as our acquisition function **for all problems**." Confirmed again in Appendix C.1: "We also use Monte-Carlo based Expected Improvement as our acquisition function." **No acquisition-optimizer variation anywhere in the paper.** → *The factorial design is genuinely not theirs.*
- **It is online/sequential BO, not offline MBO.** Different problem: they get to query the oracle; the paper's setting forbids it.
- **It DOES own the two headline findings' direction:**
  > "(i) the ranking of methods is highly problem dependent, suggesting the need for tailored inductive biases; ... (iv) deep ensembles perform relatively poorly"
  > "While deep ensembles often provide good accuracy and well-calibrated uncertainty estimates in other settings [Lakshminarayanan et al., 2017], **we show they can perform relatively poorly for Bayesian optimization.**"
- **Crucially, its MECHANISM is DIFFERENT from the paper's — this is the paper's opening.** LRW attribute the deep-ensemble failure to **lack of functional diversity in the low-data regime**, i.e. an uncertainty/diversity story:
  > "With minimal training data, the loss landscape is relatively smooth, and separately-trained models are less diverse." / "in the low-data regime, models have more similar weights and therefore are less diverse." / "This behavior suggests that the basins are not particularly d[istinct]..."
- **It discusses smoothness — but of the prior/function draws, not of the posterior mean as an optimization surface:**
  > "The choice of activation function in a neural network determines important characteristics of the function class, such as smoothness or periodicity... function draws from the ReLU BNN appearing **more jagged** and function draws from the tanh BNN more closely resembling the draws from a GP with a Squared Exponential [kernel]."
  > and on stationarity: "because the covariance between two values only depends on their distance..., this setup assumes the function is stationary and has similar mean and smoothness throughout the input space."

### Other near misses (none is a factorial)

- Kim et al. TMLR 2026 survey §6 — *names the gap* ("whether observed gains stem from superior surrogate modeling, improved optimization strategies, or mere chance") but performs no experiment.
- **fANOVA** — Hutter, Hoos, Leyton-Brown, *An Efficient Approach for Assessing Hyperparameter Importance*, ICML 2014, [PMLR v32](https://proceedings.mlr.press/v32/hutter14.html). The canonical **variance-decomposition-of-design-choices** methodology (variance explained by components + low-order interactions). Methodological precedent the paper should cite; a reviewer may ask "why not fANOVA?"
- *An Empirical Study of Bayesian Optimization: Acquisition Versus Partition*, JMLR 22 (2021), https://www.jmlr.org/papers/v22/18-220.html — an empirical decomposition of BO into components (acquisition vs partition), not surrogate × optimizer.
- HEBO — Cowen-Rivers et al., JAIR 74 (2022), [arXiv:2012.03826](https://arxiv.org/abs/2012.03826) — large ablations over surrogates/acquisitions/acquisition-maximisers ("robust acquisition maximisers afford empirical advantages relative to their non-robust counterparts"), but not a clean factorial and not offline.
- Design-Bench itself compares CMA-ES / gradient ascent / REINFORCE / BO-qEI as *whole methods*, never crossing surrogate with optimizer.

### How much of contribution 1 survives

**Survives:** the factorial design itself; the *offline MBO* setting; the η² quantification (surrogate 0.37 / optimizer 0.01 / interaction 0.17); and — most importantly — the **mechanism attribution to posterior-mean smoothness rather than calibration**, which *directly contradicts* LRW's diversity/calibration explanation. That contradiction is the paper's best asset and should be foregrounded.

**Does NOT survive:** "deep ensembles are poor surrogates" (LRW own it) and "ranking is problem-dependent → inductive biases matter" (LRW own it, nearly in the paper's words). Claiming either as a discovery is refutable with one citation.

**Recommended claim wording:** *"first controlled surrogate×optimizer factorial in offline MBO"* — defensible. Drop *"first controlled factorial decomposition"* unqualified, and never imply the deep-ensemble finding is new.

---

## Q2. GP smooth posterior mean vs jagged ensemble mean → optimizer exploitation

**VERDICT: see delegated findings below (integrated).** Independent of that: note that **MS-DDEO (2022) already grades an offline surrogate pool by smoothness** ("more smoothness means the model has less multimodal... less high-frequency information in the frequency domain") and selects on it — so "smoothness of the surrogate is the axis that matters for offline optimization" has a 2022 precedent in the EC literature. Also, the Kim TMLR survey already lists **"smoothness priors (Yu et al., 2021)"** [RoMA] among established offline-MBO remedies, so "surrogate smoothness helps offline optimization" is established; the paper's specific contribution must be *attribution of the GP's advantage to mean smoothness rather than calibration*, not the value of smoothness per se.

<!-- Q2_AGENT_FINDINGS -->

---

## Q3. Coverage / conformal diagnosis of LCB pessimism

**VERDICT: PRIOR WORK FOUND — this is the paper's weakest contribution. Both propositions are restatements.**

### Proposition 1 (premise coverage == bound validity)

The identity P(f ≥ μ − βσ) = P(μ − f ≤ βσ) is trivial, and the substantive content — *pessimism is only sound if the penalty is a valid confidence bound* — is a **stated assumption** in the offline-RL pessimism literature:

- **Jin, Yang, Wang, *Is Pessimism Provably Efficient for Offline RL?*, ICML 2021**, [PMLR v139](https://proceedings.mlr.press/v139/jin21e.html). PEVI's guarantee is conditioned on the penalty being a **ξ-uncertainty quantifier** — i.e. the entire suboptimality bound holds *if and only if* the bound is valid with the stated probability. That is Proposition 1's content, as a formal assumption, since 2021.
- Stanton, Maddox, Wilson (below) state the motivating version for BO directly.

**Assessment: PRIOR WORK FOUND.** Do **not** present this as a proposition. Demote to a remark with a citation to Jin et al. 2021. Labelling a one-line identity "Proposition 1" invites a reviewer to call the paper's theory padding — a real AAAI risk.

### Proposition 2 (split conformal + weighted conformal under covariate shift)

Essentially a restatement of two known results, and it has been *specifically* done for design and for offline MBO:

1. **Fannjiang, Bates, Angelopoulos, Listgarten, Jordan, *Conformal prediction under feedback covariate shift for biomolecular design*, PNAS 119(43):e2204569119, 2022**, [arXiv:2202.03613](https://arxiv.org/abs/2202.03613) / [PNAS](https://www.pnas.org/doi/abs/10.1073/pnas.2204569119). Provides "confidence sets for designed objects with **finite-sample guarantees of statistical validity for any design algorithm involving any learned regression model**" under the covariate shift *induced by the design algorithm itself*. **This is Proposition 2's setting, published in PNAS four years earlier.**
2. **Tibshirani, Barber, Candès, Ramdas, *Conformal Prediction Under Covariate Shift*, NeurIPS 2019** — the weighted-conformal result the paper already cites. Proposition 2's second half is this theorem applied.
3. **Stanton, Maddox, Wilson, *Bayesian Optimization with Conformal Prediction Sets*, AISTATS 2023**, PMLR v206, [arXiv:2210.12496](https://arxiv.org/abs/2210.12496). Owns the *coverage-as-validity-diagnostic-for-acquisition-decisions* framing:
   > "In practice, subjectively implausible outcomes can occur regularly for two reasons: 1) model misspecification and 2) covariate shift. Conformal prediction is an uncertainty quantification method with **coverage guarantees even for misspecified models and a simple mechanism to correct for covariate shift**. We propose conformal Bayesian optimization, which **directs queries towards regions of search space where the model predictions have guaranteed validity**... In many cases we find that **query coverage can be significantly improved** without harming sample-efficiency."
4. **Choi, Seungjin, *Conformal Candidate Certification for Offline Model-Based Optimization*, ICML 2026 Workshop (Decision-Making from Offline Datasets to Online Adaptation), submitted 13 Jun 2026**, [arXiv:2606.15217](https://arxiv.org/abs/2606.15217). **Contemporaneous and nearly the same construction, in the same setting:**
   > "Because candidates are deliberately out-of-distribution, surrogate rankings are least reliable exactly where the optimizer is most aggressive... We propose Conformal Candidate Certification (CCC), a post-hoc wrapper that **attaches a calibrated one-sided lower bound to each candidate**... We show that entropy-regularized surrogate maximization induces a Gibbs-tilted proposal, so the same surrogate supplies importance weights for **weighted conformal prediction** without a separate density-ratio estimation step. In a controlled synthetic study, CCC certifies 16.7% of an aggressive proposal pool with **empirical coverage 0.990 at nominal 0.90, while standard conformal prediction ignoring the covariate shift collapses to 0.416 coverage**."
   - One-sided *lower* bound: same. Weighted conformal for the design-induced shift: same. Empirical coverage as the diagnostic: same. Offline MBO: same.
   - Mitigating factors: it is a **workshop paper by a single author**, public only since June 2026, and does **not** do surrogate×optimizer selection. It is contemporaneous with an AAAI-27 submission — but it is public, so a reviewer can cite it.

Also relevant (calibration-improves-decisions lineage the paper should cite): Kuleshov, Fenner, Ermon, *Accurate Uncertainties for Deep Learning Using Calibrated Regression*, ICML 2018, [PMLR v80](https://proceedings.mlr.press/v80/kuleshov18a.html); Malik et al., *Calibrated Model-Based Deep RL*, ICML 2019, [arXiv:1906.08312](https://arxiv.org/abs/1906.08312); Deshpande & Kuleshov, *Online Calibrated and Conformal Prediction Improves Bayesian Optimization*, AISTATS 2024, [arXiv:2112.04620](https://arxiv.org/abs/2112.04620); Gibbs & Candès, *Adaptive Conformal Inference Under Distribution Shift*, NeurIPS 2021.

### How much of contribution 2 survives

**Very little as stated.** Proposition 1 is a known assumption (Jin et al. 2021). Proposition 2 is split conformal + Tibshirani et al. 2019, already instantiated for design in PNAS 2022 (Fannjiang et al.) and for offline MBO in arXiv 2606.15217 (Choi 2026). Coverage-as-validity-diagnostic for optimizer-driven queries is Stanton et al. AISTATS 2023.

**Recommendation:** stop presenting this as a theoretical contribution. Reframe "premise coverage" as an **empirical diagnostic instrument** used to support contribution 1's calibration-vs-smoothness argument (its actual job in the paper), cite Fannjiang/Tibshirani/Stanton/Choi as the machinery, and claim only the *diagnostic use*. As written, contribution 2 is the most likely single point of reviewer attack.

---

## Q5. Synthetic → Design-Bench validity collapse / non-discriminativeness

**VERDICT: PRIOR WORK FOUND for the complaint; NONE FOUND for the measurement.**

1. **Kim et al., TMLR 2026 survey** ([arXiv:2503.17286](https://arxiv.org/abs/2503.17286)), §6 "Robust and Realistic Benchmarking" — **the most dangerous citation**:
   > "Current benchmarks in offline MBO face two major challenges. First, some benchmarks—such as TFB8 and TFB10 (Barrera et al., 2016a)—offer overly constrained search spaces where even simple gradient ascent methods can achieve impressive results, **making it difficult to distinguish the performance of more sophisticated algorithms.** Second, benchmarks like superconductor (Hamidieh, 2018) often rely on learned oracles for evaluation, which can be vulnerable to manipulation and may not accurately reflect true performance."
   Plus the attribution sentence quoted under Q4(a) ("...or mere chance").
2. **Design-Bench itself** (Trabucco et al., ICML 2022), abstract + results:
   > "The comparatively high efficacy of even simple baselines such as CMA-ES and naïve gradient ascent suggests the need for careful tuning and standardization of methods in this area."
   > "a classical CMA-ES baseline is competitive with several highly sophisticated MBO methods in 4 out of 8 tasks... a naive gradient ascent baseline is competitive with complex approaches utilizing generative modelling on 4 of the 8 tasks."
   → "simple baselines are competitive" is **2022 canon, from the benchmark authors**. Design-Bench also already uses Agarwal et al. (2021) IQM + stratified bootstrap CIs, so "they ignored uncertainty" is not an available criticism.
3. **Surana, Grinsztajn, Atkinson, Duckworth, Barrett, *Overconfident Oracles: Limitations of In Silico Sequence Design Benchmarking*, ICML 2024 AI4Science Workshop**, [arXiv:2502.17246](https://arxiv.org/abs/2502.17246) — a *different* failure mode (oracle instability, not non-discrimination):
   > "we examine 12 sequence design methods... and find that there are **significant challenges with their cross-consistency and reproducibility**. Indeed, oracles differing by architecture, or even just training seed, are shown to **yield conflicting relative performance**"
4. **SOO-Bench, ICLR 2025** — good news: it justifies itself on **stability**, not discrimination: "Although benchmarks called Design-Bench already exist in this emerging field, it can hardly evaluate the **stability** of offline optimization." Not a scoop.
5. Broader ML precedent for the statistical argument: Agarwal, Schwarzer, Castro, Courville, Bellemare, *Deep RL at the Edge of the Statistical Precipice*, NeurIPS 2021, [arXiv:2108.13264](https://arxiv.org/abs/2108.13264).

**How much survives:** **Dead** — "simple baselines are competitive" and "Design-Bench is hard to distinguish methods on." Both are in print, the latter in the field's canonical review from six months ago. **Alive** — the *quantification*: no source runs an omnibus test on Design-Bench, and none stages the **paired synthetic-vs-real contrast** (p=6e-5 → p=0.69) as a validity collapse. The synthetic arm is the real defense: it rules out "your protocol is underpowered."

**Recommended reframe:** drop "null result / we discovered." Adopt: *"the field has suspected this (Trabucco et al. 2022; Kim et al. 2026); we are the first to measure it, and the synthetic control shows the collapse is a property of the benchmark, not of our power."* Cite Kim et al. early — pre-empting converts the biggest threat into motivation. Contribution 3 survives as **quantification + attribution**, not as complaint.

---

## Q6. Known criticisms of deep-ensemble uncertainty quality

**VERDICT: PRIOR WORK FOUND (abundant — for related work).**

<!-- Q6_AGENT_FINDINGS -->

---

## Q7. ANOVA/η² on normalized scores; Friedman/Nemenyi; TOST with tiny N

**VERDICT: PRIOR WORK FOUND (abundant — the paper must preempt these).**

<!-- Q7_AGENT_FINDINGS -->

---

## Summary table

| # | Claim | Verdict | Nearest prior work | Survives? |
|---|---|---|---|---|
| Q4 | Coverage-driven offline surrogate×optimizer selection | **PRIOR WORK FOUND (partial)** | MS-DDEO (SWEVO 2022); CC-Select (2026); Design-Bench §Conclusion (2022) | Joint surrogate+optimizer cell selection via conformal coverage: novel. Everything else: taken. |
| Q1 | First surrogate×optimizer factorial in offline MBO | **NONE FOUND** (design) / **PRIOR WORK FOUND** (finding) | Li, Rudner & Wilson, **ICLR 2024** (not 2023) | Factorial + offline setting + smoothness-not-calibration mechanism survive. "Ensembles are poor," "ranking is problem-dependent" do not. |
| Q2 | GP smooth mean → optimizer exploitation | see integrated section | RoMA (smoothness priors); offline-RL model exploitation; MS-DDEO smoothness pool | Mechanism *attribution* is the live part |
| Q3 | LCB premise-coverage; Props 1 & 2 | **PRIOR WORK FOUND** | Jin et al. ICML 2021; Fannjiang et al. PNAS 2022; Stanton et al. AISTATS 2023; Choi arXiv:2606.15217 (2026) | Weakest contribution. Demote to diagnostic. |
| Q5 | Synthetic→Design-Bench validity collapse | **PRIOR WORK FOUND** (complaint) / **NONE FOUND** (measurement) | Kim et al. TMLR 2026 §6; Design-Bench 2022 | Quantification survives; complaint does not |
| Q6 | Deep-ensemble uncertainty criticisms | **PRIOR WORK FOUND** | see section | Related work only |
| Q7 | Stats methodology criticisms | **PRIOR WORK FOUND** | see section | Preempt required |
