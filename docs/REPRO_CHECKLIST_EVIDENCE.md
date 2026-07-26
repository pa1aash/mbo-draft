# Reproducibility checklist — evidence and gap register

Companion to `paper/aaai27/ReproducibilityChecklist.tex` (AAAI-27 official template, 31 answer
slots filled). AAAI's template instructs authors to *"Replace ONLY the 'Type your response here'
text"* with one of the listed options, so the submitted `.tex` carries **option words only**.
This file records the evidence behind each answer and the gaps that remain.

Answer distribution (counted from the `.tex`, 2026-07-26): **yes 24 · partial 3 · no 3 · NA 1 = 31.**

> **Correction.** An earlier revision of this file recorded the pre-4.7 distribution as
> "23 yes / 5 partial / 2 no / 1 NA". That was an arithmetic slip: the true pre-flip counts were
> **23 yes / 4 partial / 3 no / 1 NA**. The three `no` answers have always been 2.7, 4.2 and 4.3
> (all one gap — the unattached code appendix, G2). Flipping 4.7 to `yes` gives 24/3/3/1.

---

## 1. General Paper Structure

| # | Question | Answer | Evidence |
|---|---|---|---|
| 1.1 | Conceptual outline / pseudocode of AI methods introduced | **yes** | The paper introduces a measurement protocol, not a new AI method. Figure 1 (`fig:schematic`) is the conceptual outline of the crossed factorial; §4 ¶"The protocol." states the four-step de-confounding procedure; §3 ¶"The grid." specifies surrogates, optimizers, acquisition and scoring. |
| 1.2 | Opinions/hypotheses/speculation delineated from facts | **yes** | §5 "That is a diagnosis, not a mechanism with a causal test"; §4 ¶"The bound:" ("an existence-and-ordering claim under a disclosed normalizer, not the stable quantity 0.15"); §6 "no detectable difference at this power, never equivalence"; §7 ¶"Scope."; §7 ¶"Pre-registered predictions and their outcomes." reports four refuted predictions and two failed mechanism arms. |
| 1.3 | Pedagogical references for background | **yes** | §2 covers LCB/pessimism (`srinivas2010ucb`, `lakshminarayanan2017ensembles`, `jin2021pessimism`), the offline-MBO lineage (`trabucco2021coms`, `trabucco2022designbench`), factorial design and interaction estimation (`nist2012handbook`, `box1978statistics`), and the one-way fANOVA analogue (`hutter2014fanova`). |

## 2. Theoretical Contributions

| # | Question | Answer | Evidence |
|---|---|---|---|
| 2.0 | Makes theoretical contributions? | **yes** | Propositions 1–2, Supplement §Proofs. |
| 2.1 | Assumptions/restrictions stated formally | **yes** | Supplement §Proofs ¶Notation defines $f,\mu,\sigma,L_\beta$ and "valid $(1-\delta)$ lower bound under $Q$". Prop. 2 states exchangeability and the **known** density ratio $w$. Supplement ¶"The shift clause is stated for completeness and is not applied." states the restriction explicitly. |
| 2.2 | Novel claims stated formally | **yes** | Proposition 1 (coverage of the premise = LCB validity) and Proposition 2 (split-conformal repair; shift-limited transfer). |
| 2.3 | Proofs included | **yes** | Both proved in full, Supplement §Proofs. Prop. 1 is a two-line identity; Prop. 2 uses the split-conformal rank argument plus `tibshirani2019conformal`'s weighted-exchangeability extension. |
| 2.4 | Proof sketches/intuitions for complex results | **yes** | Supplement ¶"Sanity checks" after Prop. 1 ($\beta=0$ and $\beta\to\infty$ limits, dimensionlessness); Prop. 2's proof states the rank argument in prose before the bound. |
| 2.5 | Citations to theoretical tools | **yes** | `tibshirani2019conformal` (weighted exchangeability), `angelopoulos2023conformal` (exactness under known shift magnitude), `srinivas2010ucb` (GP-LCB regret). |
| 2.6 | Theoretical claims demonstrated empirically | **partial** | Prop. 1's identity is the measurement basis for every coverage number (Supp. Table S9; §5's 0.97 vs 0.831). Prop. 2's repair is demonstrated — conformal restores in-distribution coverage to its 0.90 target on **every** task (Supp. Table S9). **Not demonstrated:** the weighted/shifted clause, which the supplement explicitly declines to apply because $w$ is unavailable for optimizer-generated proposals. Disclosed, by design — hence *partial*, not *yes*. |
| 2.7 | Experimental code used to eliminate/disprove claims is included | **no** | The code exists (`code/coverage33.py`, `code/gpcov.py`, `code/phantom_maxima.py`, `code/farfield_v2.py`, `code/gradtune.py`) but **is not yet attached** to the submission. See gap G2. |

## 3. Dataset Usage

| # | Question | Answer | Evidence |
|---|---|---|---|
| 3.0 | Relies on datasets? | **yes** | Seven synthetic tasks + seven Design-Bench tasks. |
| 3.1 | Motivation for the selected datasets | **yes** | §3 ¶"The grid." (Branin-2D → Griewank-30D spans 2–30 dimensions); §6 motivates Design-Bench as the suite that "standardizes tasks and documents the confounded status quo" (§2, `trabucco2022designbench`); §6 ¶"Frozen cells" motivates screening the suite before attribution. |
| 3.2 | Novel datasets included in a data appendix | **partial** | The seven synthetic datasets are not shipped as files — they are generated **deterministically** by `code/mbo.py::make_tasks`, drawn once at seed 0 and fixed across seeds (Supplement §Experimental Configuration ¶Tasks, with per-task $N$). The generator *is* the data appendix, and it is not yet attached (gap G2). |
| 3.3 | Novel datasets public on publication under a research license | **yes** | Committed: the task generator ships with the code release. **Blocked on gap G3** — the repository currently carries no `LICENSE` file. |
| 3.4 | Literature datasets cited | **yes** | Design-Bench cited as `trabucco2022designbench` in §1, §2, §3 and §6; the exact task ids and oracle variants (exact vs RandomForest) are recorded in `code/db_tasks.py:15-17` and Supplement §Experimental Configuration ¶Tasks. |
| 3.5 | Literature datasets publicly available | **yes** | Design-Bench is a public, open-source benchmark suite; tasks are obtained through the released `design_bench` package (`code/db_tasks.py`). |
| 3.6 | Non-public datasets described in detail | **NA** | Every dataset is either public (Design-Bench) or generated by released code (synthetic). |

## 4. Computational Experiments

| # | Question | Answer | Evidence |
|---|---|---|---|
| 4.0 | Includes computational experiments? | **yes** | — |
| 4.1 | Ranges tried per hyperparameter + selection criterion | **yes** | Ranges: $K\in\{2,3,5,10\}$ (§3 Confound 3), $\beta\in\{0,0.5,1,2,5\}$ (§4), width $\in\{96,256,512,1024\}$ (§5 Elim. 3, Supp. Fig. S2), $Q\in\{4{,}352;\,51{,}456\}$ (§3 Confound 5, §4). **Selection criterion is stated and unusual:** these were *not tuned*. $K{=}5$ and $\beta{=}2$ are fixed by field convention and then swept as confounds; the paper discloses that the headline therefore sits at the $K$ that **maximizes** the effect (§3 Confound 3; §7 ¶"Pre-registered predictions"). Finals: Supplement §Experimental Configuration. |
| 4.2 | Pre-processing code in the appendix | **no** | Exists (`code/mbo.py` target scaling / normalization; `code/db_tasks.py` relaxation, argmax decode, min–max scaling, score-biased subsampling) but not yet attached. Gap G2. |
| 4.3 | All source code in a code appendix | **no** | Exists (`code/`, 30 scripts) but not yet attached. Gap G2. |
| 4.4 | Source code public on publication under a research license | **yes** | Committed; the anonymized link is already drafted at `paper/aaai27/main.tex:52-54` (currently commented out — gap G4). Blocked on gap G3 (no `LICENSE` file). |
| 4.5 | Code comments referencing the paper | **partial** | Load-bearing scripts carry explanatory docstrings and inline rationale (`code/run_all.py:97-112` on the meta assertion, `code/db_tasks.py:1-17` on the adapter and oracle variants, `code/beta0_reconcile.py:80-96` on the $\beta$-invariant normalizer). Coverage is **not** systematic: many scripts do not cite the paper section each step supports. Gap G5. |
| 4.6 | Seed-setting method described | **yes** | Supplement §Experimental Configuration ¶"Acquisition and protocol." ("Seeds: 30 synthetic, 16 Design-Bench"; sweeps at 30, coverage artifact at 8) and ¶Surrogates ("per-member seed offset"); §3 ¶"The grid." ("drawn once at seed 0"). Enforced mechanically: every result file must carry `n_seeds` and `seed` (e.g. `"0..29"`) in its meta block — `REQUIRED_META`, `code/run_all.py:46-48`. |
| 4.7 | Computing infrastructure (hardware **and** software) | **yes** *(closed 2026-07-26)* | Supplement §Experimental Configuration ¶"Compute and environment." now states all five sub-items. **CPU model:** AMD EPYC 9655P, exposed to the container as 32 vCPUs. **Memory:** 64 GB RAM (plus 30 GB container disk, 200 GB network volume — the volume matters because `design-bench` caches task data and TF-Bind-10 ships 4.16M rows). **GPU:** none — every artifact carries a `+cpu` PyTorch build, no CUDA anywhere. **OS:** x86-64 Linux 6.17.0-35-generic / glibc 2.39 on the provisioned cloud instance (RunPod, `runpod-ubuntu-2404`); the TF-Bind-8 spot-check ran on a separate arm64 macOS 26.3.1 machine, kept distinct in the text. **Libraries:** Python 3.12.3 (synthetic) / 3.9.23 (Design-Bench), with `torch`, `numpy`, `botorch`, `gpytorch`, `cma` versions stamped per artifact and pinned in `requirements.txt`. **Wall-clock is measured, not estimated:** the full 2,520-cell synthetic grid (7 tasks × 12 arms × 30 seeds) completed in 17.1 min on 30 workers — `results/supp_offoff/run.log:2,255`, whose artifact `results/supp_offoff/grid_offoff_b2.0.json` carries the matching Linux meta block. Enforcement unchanged: `REQUIRED_META` (`code/run_all.py:46-48`) + `load_checked` (`run_all.py:97-112`) reject any unstamped file. |
| 4.8 | Evaluation metrics described and motivated | **yes** | §3 ¶"The grid." defines the metric chain: 100th-percentile oracle score over the 128 returned designs → per-task min–max normalized cell means → two-way ANOVA $\eta^2$ → task-and-seed hierarchical bootstrap ($B{=}10{,}000$). §4 ¶"The $\beta$-dependence" motivates *and* discloses the normalizer's endogeneity (`jordan2024position`, `bellemare2013ale`, `balduzzi2018reevaluating`); Supp. §Further Robustness Checks Table S10 recomputes across three normalizers. |
| 4.9 | Number of runs per reported result | **yes** | 30 seeds synthetic / 16 Design-Bench (§3 ¶"The grid."; Supplement §Experimental Configuration); $B{=}10{,}000$ bootstrap resamples on every interval; cell counts stated where they vary (168 cells × 30 seeds for Elim. 7; 630 cells for the matched-budget arm; 252 for the Design-Bench matched arm). |
| 4.10 | Beyond single-dimensional summaries | **yes** | Every $\eta^2$ carries a task-and-seed hierarchical bootstrap 95% CI; the four-corner intervals and their shared region $[0.312,0.443]$ are the basis of the non-resolvability claim (§4); $\epsilon^2$ small-$n$ bias correction disclosed from our own artifacts (Supp. §"Small-$n$ bias in $\eta^2$"); per-width CIs widen with $w$ and that is stated as a scope limit (Table 1 caption). |
| 4.11 | Appropriate statistical tests | **yes** | Friedman omnibus with Nemenyi critical difference, Wilcoxon signed-rank with Holm correction, hierarchical bootstrap, and a two-one-sided-tests equivalence bound (Supp. §Significance Details, `code/stats.py`). Power is stated rather than assumed: at $n{=}7$ a paired test needs $\lvert d_z\rvert\ge1.27$ for 80% power (§6, `agarwal2021precipice`). |
| 4.12 | Final hyperparameters listed | **yes** | Supplement §Experimental Configuration: ensemble ($K{=}5$, 2×96 ReLU, 35 epochs, Adam lr $3\times10^{-3}$, wd $10^{-4}$, batch 256), exact GP (ARD Matérn-5/2, $N_{\max}{=}800$), SVGP (128 inducing points, 250 ELBO steps, lr 0.01, $N_{\max}{=}2000$), optimizers (100 Adam steps lr 0.05; 5 perturbation rounds $\sigma\in\{0.1,0.05,0.02\}$; CMA-ES $\sigma_0{=}0.2$), acquisition ($\beta{=}2$, TOP=128). |

---

## Gaps to address before the 2026-07-28 / 07-31 deadlines

| ID | Gap | Checklist items | Action |
|---|---|---|---|
| **G1** | **CLOSED 2026-07-26.** CPU model (AMD EPYC 9655P / 32 vCPU), RAM (64 GB), disk, GPU-absence, OS, both Python environments, the per-artifact version stamp and a **measured** full-grid wall-clock (2,520 cells in 17.1 min on 30 workers) are all stated in Supplement §Experimental Configuration ¶"Compute and environment." | 4.7 → **yes** | None. |
| **G2** | **Code appendix not attached.** All code exists in `code/` but is not part of the submission package. | 2.7 (*no*), 4.2 (*no*), 4.3 (*no*) | Finalize the reproducible package (Makefile + README + USAGE) for the 07-31 supplement deadline. Three answers flip *no → yes* once attached. |
| **G3** | **No `LICENSE` file in the repository.** 3.3 and 4.4 both promise a research-permissive license. | 3.3, 4.4 (both answered *yes* as forward commitments) | Add a permissive license (MIT/Apache-2.0/BSD-3) at repo root. One-line fix; do before the code release. |
| **G4** | **Code link is commented out** at `paper/aaai27/main.tex:52-54`. | 4.4 | Uncomment the `\begin{links}` block once the anonymized repo is live. **Note:** this adds a links block to page 1 and *will* consume page budget — re-measure content pages after enabling. |
| **G5** | **Code comments are not systematically cross-referenced to paper sections.** | 4.5 (*partial*) | Add section pointers to the header docstrings of the analysis scripts. Optional; *partial* is a defensible answer. |
| **G6** | `newtx` / `ts1-qtmr` **not installed locally**, so `ReproducibilityChecklist.tex` does not compile on this machine. AAAI's *untouched* template fails identically — an environment gap, not a document defect. | — | `tlmgr install newtx`, or compile on any complete TeX Live. The `.tex` is byte-faithful to AAAI's template apart from the 31 answer slots. |

**Not gaps** (answered honestly as *partial*/*NA* by design, no action needed): 2.6 (weighted-conformal clause deliberately not applied and disclosed), 3.2 (synthetic data is generated, not shipped — resolves with G2), 3.6 (no non-public datasets).
