# Paper skeleton — AAAI-27 main track

Manuscript plan. Grounded in the R1 novelty verdict (`research/notes/final_report_mbo-decomposition-prior-art-579ba4.md`) and the confirmed preview findings. Every claim here traces to a result or a citation; fill numbers from the frozen cloud run. AAAI format: 7 pp body + refs, two-column, `aaai27.sty` (grab from author kit / Overleaf).

## Working title (pick at freeze)
1. **"Where Does GP-LCB's Advantage in Offline Model-Based Optimization Come From? Decomposing Surrogate, Optimizer, and Calibration"** ← lead candidate (names the finding)
2. "The Optimizer, Not the Surrogate: A Controlled Decomposition of Offline Model-Based Optimization"
3. "Pessimism Without Calibration: Why Ensemble-LCB Fails in Offline MBO and What Actually Drives Performance"

## Abstract (draft skeleton — fill bracketed numbers at freeze)
Offline MBO trains a surrogate on a fixed dataset and optimizes it to propose designs. A recurring empirical claim is that Gaussian-process LCB beats neural-ensemble LCB at low dimension. We show this comparison is **confounded**: the GP and neural pipelines differ in *both* the surrogate and the acquisition optimizer. We run the first controlled **surrogate × optimizer** decomposition — {deep ensemble, exact GP, SVGP} × {gradient ascent, perturbation, CMA-ES} — on [7] synthetic and [N] Design-Bench tasks. We find [the acquisition optimizer explains most of the reported gap: on the ensemble surrogate, switching gradient→perturbation changes mean rank by [X], while on the GP the optimizer changes rank by [Y≈0]]. We trace the mechanism to a calibration failure: the pessimism guarantee's premise (|μ−f| ≤ βσ) holds only [~50%] of the time in-distribution and [~3%] on the OOD designs LCB proposes; repairing calibration with split-conformal restores valid coverage in-distribution ([0.95]) but not under the proposal's covariate shift. We conclude with practitioner guidance and a unified offline-to-online protocol. [Optional: our findings recontextualize N published GP-vs-neural comparisons.]

## Contributions (intro, enumerated — exact wording from R1)
1. **The first controlled decomposition** of offline-MBO performance into surrogate class × acquisition optimizer, isolating a confound that the field's standard comparisons (Design-Bench baselines; COMs lineage) leave entangled. Prior systematic surrogate studies vary the model with the optimizer fixed (Li et al. 2024); the conservative-surrogate lineage varies the regularizer with gradient ascent fixed (Trabucco et al. 2021); PGS (Chen et al., AAAI 2024) argues search strategy is under-explored but proposes a method rather than decomposing. **We decompose.**
2. **A calibration-failure mechanism** for why gradient ascent on ensembles underperforms: we measure the coverage of the LCB pessimism premise in-distribution vs. on the OOD designs the optimizer actually reaches, and show a split-conformal repair recovers coverage only where exchangeability holds (connecting to, and distinct from, the post-hoc certification of Choi 2026 and the global-scalar conformal-LCB of UNIQ 2026).
3. **A unified offline-to-online (O2O) protocol** with diversity-aware selection, evaluated identically across selection rules (fixing a protocol confound in prior single-method O2O reports) on synthetic and Design-Bench tasks.

## Section plan (7 pp)
| § | Title | Content | Figure/Table |
|---|---|---|---|
| 1 | Introduction | The confound; 3 contributions; headline result sentence | — |
| 2 | Background & Related Work | LCB/pessimism premise; surrogate-class studies (Li 2024); COMs lineage; conformal-BO cluster (Stanton, Deshpande-Kuleshov, CCC, UNIQ); the factorial gap | — |
| 3 | The Decomposition Grid | surrogates × optimizers defined; shared score-closure protocol; tasks; metrics (p100/p50 normalized); n=30 | Table: grid design |
| 4 | Results: what drives performance | main grid; optimizer-gap-by-surrogate; rank-vs-dimension; significance (Wilcoxon+Holm, Friedman, CD diagram) | **F1** (grid bars), **F2** (rank-vs-dim), **F6** (CD), Table 1 (full grid) |
| 5 | Mechanism: the calibration failure | premise coverage in-dist vs OOD; conformal repair + covariate-shift break; Prop 1; σ–error correlation | **F3** (coverage), **F4** (calib↔benefit), Prop 1 |
| 6 | Offline-to-online | unified protocol; selection-rule comparison; budget curves; DB tasks | **F5** (O2O curves), Table 2 |
| 7 | Discussion & Limitations | practitioner guidance (decision tree F7); scope (synthetic + N DB tasks, CPU-scale); honest limits | **F7** (decision tree) |

## Confirmed findings feeding the narrative (preview, ep=35, n=3 — replace with n=30 cloud)
- **Optimizer-gap-by-surrogate (the headline):** on the deep ensemble the three optimizers span mean-rank ~5–9 (gradient worst — it exploits OOD surrogate error → boundary collapse, e.g. Branin ens:grad −6.6 vs ens:perturb −1.0); on the GP the three optimizers are tight (rank ~2–3, all ≈ −0.40). *Optimizer choice matters enormously for ensembles, negligibly for GPs.* → F1.
- **Mechanism (confirmed 6 tasks):** premise coverage at β=2 is 0.27–0.77 in-distribution and 0.00–0.11 on LCB's OOD designs. Conformal multiplier q=2.8–10.5 (vs β=2), restoring 0.95–0.97 in-distribution coverage but 0.00–1.00 (erratic) on OOD — the covariate-shift break. σ–error ρ=0.06–0.17 (matches original paper's ~0.08). → F3.
- **Proposition 1 (mechanism, formal):** the LCB lower bound μ−βσ is valid only if βσ ≥ |μ−f| with prob ≥1−δ (coverage). Measured in-distribution coverage ≪ nominal at the default β; split-conformal restores it *on exchangeable data by construction* but the proposal distribution violates exchangeability. Proof sketch in appendix.

## Related-work paragraph (from R1 corpus — cite all)
Surrogate-class comparison: Li-Rudner-Wilson 2024 (BNN surrogates for BO, optimizer fixed). Acquisition optimization: Wilson et al. 2018. Conservative offline MBO: Trabucco 2021 (COMs), + RoMA/BDI/ICT/tri-mentoring/RaM/DEMO/GAMBO/Cliqueformer/PGS/GTG/BRAID. Optimizer-as-contribution: PGS (AAAI 2024), GAMBO (NeurIPS 2024). Theory: Match-OPT 2024 (gradient-field discrepancy bound). Calibration/conformal: Kuleshov 2018, Malik 2019, Stanton 2022 (BO+conformal), Deshpande-Kuleshov 2024 (calibration improves BO, online), **CCC/Choi 2026 (conformal certification, offline MBO)**, **UNIQ 2026 (conformal-LCB, offline RL, global scalar)**, foundations Gibbs-Candès 2021 / Tibshirani 2019 / jackknife+. Benchmark: Design-Bench (Trabucco 2022) — documents the confounded status quo.

## Kill list (from repo audit — enforce while writing)
- No RL section (legacy toy-RL was mislabeled: linear "Control-6D", non-BC "BC" — cut entirely).
- O2O described exactly as `mbo.run_o2o` does it (iterative, retrain every 10 picks, 60 re-opt steps) — no protocol confound.
- Dataset fixed across seeds (seed-0 generation) — stated explicitly.
- Baselines honestly labeled: "CbAS" → real CbAS if E3 runs it, else "CEM-style adaptive sampling"; sparse-GP uncertainty is a feature-variance proxy unless a real posterior is fit.
- Every number traces to the frozen results JSON (number-trace audit gate).

## Baseline strategy (from R2 — `research/notes/baseline-numbers-designbench.md`)
- **Run ourselves (design-baselines repo, one protocol):** Grad. Ascent, COMs, CbAS, CMA-ES, BO-qEI. **Report our own COMs beside the published range** — published COMs varies ±0.1 across re-runs, so our number anchors the comparison.
- **Cite from published tables:** DDOM, BONET, ExPT, BDI, RoMA, RaM/LTR, Match-OPT (diffusion/transformer/ranking — expensive to reproduce). Cross-check appendix table = Tables A+B from the R2 note.
- **Protocol (state exactly):** 100th-pct (max) headline + 50th-pct (median); **N=128** oracle budget; `y_norm=(y−y_min)/(y_max−y_min)` with y_min/max from the **full unobserved dataset** (Design-Bench App. C.1); 8 trials standard.
- **Landscape for positioning:** current published leaders are ranking-based **RaM/LTR**, then BDI/Tri-Mentoring/ICT/COMs. GFP/UTR are saturated (~0.86/0.69, being retired). Superconductor has no clear winner (0.40–0.52). Note published-number disagreements (RoMA 0.43–0.92; BONET Q=256 double-budget; DDOM Ant/D'Kitty splits differ) in the appendix — motivates our controlled single-protocol run.
- **Appendix ID fix:** BONET = arXiv 2206.10786 (not 2301.10123).

## Novelty one-liner (for intro + rebuttal)
"We present the first controlled decomposition of offline-MBO performance into surrogate class, acquisition optimizer, and uncertainty calibration. Prior work varies one axis at a time — surrogates with the optimizer fixed (Li et al. 2024), optimizers as a proposed method (PGS 2024), or calibration on a fixed GP+EI pipeline (the conformal-BO line) — and the surrogate–optimizer confound has not been isolated."
