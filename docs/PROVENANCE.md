# Claims Inventory — "Decomposing the GP Advantage in Offline MBO"

Forensic quantitative claim extraction for provenance audit.
Repo: `/Users/palaash/Downloads/MBO`

## Source files audited

| File | Lines | Role |
|---|---|---|
| `/Users/palaash/Downloads/MBO/paper/aaai27/main.tex` | 298 | AAAI submission body |
| `/Users/palaash/Downloads/MBO/paper/aaai27/supplement.tex` | 206 | Supplementary material |
| `/Users/palaash/Downloads/MBO/paper/aaai27/main.pdf` | 8 pages | Rendered body (cross-checked) |
| `/Users/palaash/Downloads/MBO/paper/aaai27/supplement.pdf` | 4 pages | Rendered supplement (cross-checked) |
| `/Users/palaash/Downloads/MBO/paper/tables_v2/grid.tex` | 19 | Generated 9-cell synthetic grid (full precision) |
| `/Users/palaash/Downloads/MBO/paper/tables_v2/grid_full.tex` | 22 | Generated 12-method synthetic grid (full precision) |
| `/Users/palaash/Downloads/MBO/paper/tables_v2/grid_rank.tex` | 18 | Generated 9-cell avg rank |
| `/Users/palaash/Downloads/MBO/paper/tables_v2/grid_full_rank.tex` | 21 | Generated 12-method avg rank |
| `/Users/palaash/Downloads/MBO/paper/aaai27/figures/*.pdf` | — | Figure text layers extracted via pymupdf |

**Note on `tables_v2/`:** these are the *generator-emitted* tables and are NOT `\input` by `main.tex` or `supplement.tex` (both hard-code their table bodies). `tables_v2/` therefore functions as the higher-precision upstream reference against which the hand-transcribed paper tables can be diffed. This is itself a provenance risk (see §8, PR-1).

## Float numbering map (rendered PDF)

**main.pdf**

| Rendered | LaTeX label | Source line | Graphic file |
|---|---|---|---|
| Table 1 | `tab:grid` | main.tex:98–119 | — |
| Table 2 | `tab:attr` | main.tex:135–149 | — |
| Table 3 | `tab:dbgrid` | main.tex:167–191 | — |
| Table 4 | `tab:controls` | main.tex:204–218 | — |
| Algorithm 1 | `alg:diag` | main.tex:261–277 | — |
| Figure 1 | `fig:heatmap` | main.tex:124–129 | `figures/fig1_grid_heatmap` |
| Figure 2 | `fig:optbysurr` | main.tex:151–156 | `figures/fig2_optimizer_spread` |
| Figure 3 | `fig:cd` | main.tex:160–165 | `figures/fig6_cd_diagram` |
| Figure 4 | `fig:cross` | main.tex:220–225 | `figures/fig8_crossproposal` |
| Figure 5 | `fig:coverage` | main.tex:238–243 | `figures/fig3_coverage` |
| Figure 6 | `fig:beta` | main.tex:245–250 | `figures/fig4_beta_sweep` |

**supplement.pdf**

| Rendered | LaTeX label | Source line | Graphic file |
|---|---|---|---|
| Table 1 | `tab:sfull` | supplement.tex:58–80 | — |
| Table 2 | `tab:srank` | supplement.tex:82–98 | — |
| Table 3 | `tab:cross` | supplement.tex:112–124 | — |
| Table 4 | `tab:cc` | supplement.tex:144–160 | — |
| Table 5 | `tab:cov` | supplement.tex:165–190 | — |
| Figure 1 | `fig:calib` | supplement.tex:130–134 | `figures/fig5_calibration_vs_benefit` |
| Figure 2 | `fig:k` | supplement.tex:135–139 | `figures/fig7_k_ablation` |

---

# 1. INTERNAL INCONSISTENCIES (HIGHEST PRIORITY)

Ordered by severity.

## INC-1 (SEVERE) — Figure 1 and Figure 3 report *different* Design-Bench mean ranks for the same 9 cells

Both figures claim to show "mean rank across tasks" over the identical 9-cell grid on the identical 7 Design-Bench tasks. **6 of 9 cells disagree.** The synthetic panels agree perfectly, which rules out a benign presentational difference and points to two different underlying data sources or two different rank computations.

Extracted text layers:
- `figures/fig1_grid_heatmap.pdf` → DB panel: `5.1 4.1 6.1 / 4.1 3.4 5.4 / 6.0 4.9 5.7`
- `figures/fig6_cd_diagram.pdf` → DB panel: `GP+Pert (3.6) GP+Grad (4.3) Ens+Pert (4.4) SVGP+Pert (4.7) (6.1) Ens+CMA (5.9) SVGP+Grad (5.7) SVGP+CMA (5.1) Ens+Grad (5.1) GP+CMA`

| Cell | Fig 1 (heatmap) | Fig 3 (CD diagram) | Body text (main.tex:158) | Supplement (:193) | Agree? |
|---|---|---|---|---|---|
| GP × Pert | **3.4** | **3.6** | "mean rank $3.6$" | "mean rank 3.57" | **NO — Fig 1 is the outlier** |
| GP × Grad | **4.1** | **4.3** | — | — | **NO** |
| Ens × Pert | **4.1** | **4.4** | — | — | **NO** |
| SVGP × Pert | **4.9** | **4.7** | — | — | **NO** |
| GP × CMA | **5.4** | **5.1** | — | — | **NO** |
| SVGP × Grad | **6.0** | **5.9** | — | — | **NO** |
| Ens × Grad | 5.1 | 5.1 | — | — | yes |
| SVGP × CMA | 5.7 | 5.7 | — | — | yes |
| Ens × CMA | 6.1 | 6.1 | — | — | yes |

Both sets sum to ≈45 (44.8 and 44.9 vs. the 45 expected for 9 tie-free ranks), so both are internally plausible rankings — they are simply **not the same ranking**. Figure 1 contradicts the body text, the supplement, *and* Figure 3 on the paper's headline Design-Bench cell (GP×Pert: 3.4 vs. 3.6/3.57).

Synthetic panels, for contrast, agree exactly and match `grid_rank.tex`:

| Cell | Fig 1 | Fig 3 | `grid_rank.tex` |
|---|---|---|---|
| GP+Grad | 2.3 | 2.3 | 2.29 |
| SVGP+Grad | 3.1 | 3.1 | 3.14 |
| GP+CMA | 3.3 | 3.3 | 3.29 |
| SVGP+CMA | 4.1 | 4.1 | 4.14 |
| GP+Pert | 4.7 | 4.7 | 4.71 |
| SVGP+Pert | 4.9 | 4.9 | 4.86 |
| Ens+Pert | 6.9 | 6.9 | 6.86 |
| Ens+Grad | 7.1 | 7.1 | 7.14 |
| **Ens+CMA** | **8.6** | **8.6** | **8.57** |

## INC-2 (SEVERE) — Table 1 caption `-2612` vs. table body `-2613` / `-2592` (the suspected one — CONFIRMED, and worse than suspected)

`main.tex:100` (Table 1 caption), verbatim:
> "Within the ensemble rows the optimizer swings the score enormously (Branin $-0.78\!\to\!-9.27$; Griewank $-395\!\to\!-2612$)"

Ground truth from `tables_v2/grid.tex:9–11`:
- Ens+Grad Griewank = `-2592.24`
- Ens+Pert Griewank = `-395.43`
- Ens+CMA Griewank = `-2612.68`

So the caption's `-2612` is a **truncation of Ens×CMA `-2612.68`**, while the same table's body renders that cell as `-2613` (correct rounding). The caption number matches **no cell in its own table**.

Compounding this, the caption is internally incoherent about *which* endpoint it uses:

| Caption pair | Endpoint 1 | Endpoint 2 | Which optimizer is endpoint 2? |
|---|---|---|---|
| Branin $-0.78 \to -9.27$ | Ens×Pert | Ens×Grad | **Gradient** (but the true Branin extreme is Ens×CMA `-14.01`, also in the table) |
| Griewank $-395 \to -2612$ | Ens×Pert | Ens×CMA (truncated) | **CMA-ES** |

The caption uses Grad as the Branin extreme (understating the swing: `-14.01` is worse) and CMA as the Griewank extreme. The body text at `main.tex:131` uses Grad for *both*:
> "(Branin $-0.78$ for perturbation vs.\ $-9.27$ for gradient; Griewank $-395$ vs.\ $-2592$)"

Net: three different Griewank ensemble-worst numbers circulate — caption `-2612`, table body `-2613`, body text `-2592`.

## INC-3 (MODERATE) — main.tex Table 1 vs. supplement Table 1: GP+Pert Griewank `-269` vs. `-270`

Same cell, same data, two values across the two documents.

| Location | Value | Source truth (`grid.tex:13`) | Correct rounding |
|---|---|---|---|
| `main.tex:112` (Table 1, GP × Pert, Griewank) | `-269` | `-269.60` | `-270` — **main.tex is wrong (truncated)** |
| `supplement.tex:70` (Table 1, GP+Pert, Griewank) | `-270` | `-269.60` | `-270` — correct |

This also exposes an **inconsistent rounding convention inside main.tex Table 1 itself**: `-2612.68` → `-2613` (rounds) but `-269.60` → `-269` (truncates). `-274.62` → `-275` in both docs (rounds). So main.tex Table 1 truncates exactly one cell.

## INC-4 (MODERATE) — "no smaller than" contradicts its own numbers (0.34 vs 0.39)

`main.tex:285`, verbatim:
> "the omnibus stays flat (Friedman $p{=}0.93$) and the median 9-cell spread ($0.34$) is no smaller than on the substituted tasks ($0.39$)"

`supplement.tex:195`, verbatim:
> "the median per-task method spread (0.34 normalized) is no smaller than on the four substituted tasks (0.39)"

**0.34 IS smaller than 0.39.** The stated relation is literally false as written, in both documents. The *underlying inference* survives (RF-substituted tasks show a *larger* spread, so RF substitution is not flattening the surface), but the sentence asserts the opposite of what its own numbers show. Correct phrasing would be "is no larger" / "the substituted tasks do not show a smaller spread". This is the paper's defense of the RF oracle substitution, so the wording error sits on a load-bearing claim.

## INC-5 (MODERATE) — "restores ... on every task" vs. table cells at 0.89

`main.tex:259`, verbatim:
> "Replacing $\beta\sigma$ by $\hat q\sigma$ restores in-distribution coverage to its $0.90$ target on every task (mean $0.90$ synthetic and real)"

`supplement.tex:163`, verbatim:
> "Conformal restores in-distribution coverage to its $0.90$ target on every task"

But supplement Table 5 (`supplement.tex:178, 182`) shows $c^{\text{cf}}_{\text{in}}$ = **0.89** for **Ackley** and **0.89** for **TF-Bind-10** — below the 0.90 target. The means (0.9014 synthetic, 0.90 real — verified) are correct; the universal quantifier "on every task" is not.

## INC-6 (MODERATE) — supplement Table 4 |Δ| column inconsistent with its own Official/Ours columns

`supplement.tex:156` (Table 4, CbAS / TF-Bind-8): Official `2.13`, Ours `2.12`, |Δ| `**0.004**`.

`2.13 − 2.12 = 0.01`, not `0.004`. The |Δ| is computed at full precision while Official/Ours are rendered at 2 dp, so the row does not verify against itself. Every other row does: `1.31−1.01=0.30` ✓, `0.99−2.21=1.22` ✓, `−8.38−(−9.20)=0.82` ✓, `1.21−1.36=0.15` ✓, `2.20−1.85=0.35` ✓. The single headline "our CbAS matches the official scores" number is the one that cannot be reproduced from the displayed values.

## INC-7 (MINOR) — main body |Δ|=1.2 vs. supplement |Δ|=1.22

| Location | Value | Quote |
|---|---|---|
| `main.tex:287` | `1.2` | "our COMs and official COMs diverge ($|\Delta|{=}1.2$, a reduced-epoch official run and a different oracle variant)" |
| `supplement.tex:142` | `1.22` | "COMs diverges (TF-Bind-8 $|\Delta|{=}1.22$)" |
| `supplement.tex:153` (Table 4) | `1.22` | table cell |

## INC-8 (MINOR) — Nemenyi CD: body `4.5` vs. supplement/figure `4.54`

| Location | Value |
|---|---|
| `main.tex:158` | "against a Nemenyi critical difference of $4.5$" |
| `supplement.tex:193` | "Nemenyi critical difference $4.54$" |
| `figures/fig6_cd_diagram.pdf` (both panels) | `CD = 4.54` |

## INC-9 (MINOR) — abstract `6×10⁻⁵` vs. body/table `6.1×10⁻⁵`

| Location | Value |
|---|---|
| `main.tex:49` (abstract) | "Friedman $p{=}6\times10^{-5}$" |
| `main.tex:66` (contribution 3) | "Friedman $p{=}6\times10^{-5}$" |
| `main.tex:144` (Table 2), `main.tex:158`, `main.tex:163`, `supplement.tex:193` | `6.1\times10^{-5}` |

## INC-10 (MINOR) — q̂ range upper bound `16` vs. table `16.1`

`main.tex:259`: "synthetic $\hat q\in[1.8,16]$". Supplement Table 5 (`supplement.tex:179`) Griewank $\hat q$ = **`16.1`**. Lower bound `1.8` matches Ackley exactly (`supplement.tex:178`). The interval as stated does not contain its own maximum.

## INC-11 (MINOR/AMBIGUITY) — two different "GP+Grad mean rank" numbers in the supplement, pool never disclosed

| Location | Value | Pool |
|---|---|---|
| `supplement.tex:90` (Table 2, `tab:srank`) | GP+Grad = `2.57` | 12 methods (= `grid_full_rank.tex` exactly) |
| `supplement.tex:193` (Significance Details) | "best cell GP+Grad, mean rank 2.29" | 9 cells (= `grid_rank.tex` exactly) |
| `main.tex:158` | "mean rank $2.3$" | 9 cells |
| `figures/fig1_grid_heatmap.pdf`, `fig6_cd_diagram.pdf` | `2.3` | 9 cells |

Not a contradiction (different pools), but the supplement never states that Table 2 is a 12-method pool while §8's 2.29 is a 9-cell pool. A reader diffing 2.57 against 2.29 has no way to reconcile them from the text. Same applies to every row: Ens+CMA `10.71` (12-pool, Table 2) vs `8.6` (9-pool, Fig 1).

## INC-12 (MINOR) — ties not bolded, in violation of the tables' own "Bold = best per task" rule

**main.tex Table 1** (`tab:grid`, caption: "\textbf{Bold} = best per task"):

| Task | Max value | Cells at max | Bolded |
|---|---|---|---|
| Branin | `-0.40` | GP×Grad, GP×Pert, GP×CMA, SVGP×Pert (4-way) | only GP×Grad |
| Levy | `-0.05` | GP×Grad, GP×CMA (2-way) | only GP×Grad |
| Rosenbrock | `-0.04` | SVGP×Grad, SVGP×CMA (2-way) | only SVGP×Grad |

**main.tex Table 3** (`tab:dbgrid`, "Bold = best per task including the COMs/CbAS baselines"):

| Task | Max value | Cells at max | Bolded |
|---|---|---|---|
| GFP | `2.48` | Ens×Pert, SVGP×CMA (2-way) | only SVGP×CMA |
| UTR | `1.01` | Ens×Grad, COMs | both ✓ (correct) |

Ties may be broken at hidden precision, but the tables are inconsistent with themselves about whether to bold a tie (UTR bolds both; GFP/Branin/Levy/Rosenbrock bold one). Same pattern in supplement Table 1.

## INC-13 (LOW / FLAG FOR CODE DIFF) — suspicious exact duplications across the β=0 control and the β=2 grid

Not provable inconsistencies from the manuscript alone, but they should be diffed against the code:

| Value | Appears as | Appears as | Concern |
|---|---|---|---|
| `-2701` | β=0 ensemble×gradient Griewank (`main.tex:198`, `supplement.tex:106`) | `Grad.\ Asc.` baseline Griewank at β=2 (`supplement.tex:77`; `grid_full.tex:20` = `-2701.00`) | Plausibly the same run (gradient ascent with no pessimism *is* ensemble×grad at β=0), but the paper presents them as independent evidence in two places without noting the identity. |
| `-0.94` | β=0 GP Griewank (`main.tex:198`: "the GP's $-0.94$") | β=2 GP×Grad Griewank (Table 1, `main.tex:111`) | Identical to 2 dp across a β change that the paper argues is consequential elsewhere. |

---

# 2. TABLES AND FIGURES — number, verbatim caption, data shown

## main.pdf

### Table 1 (`tab:grid`, main.tex:98–119)
**Caption (verbatim):** "Offline MBO on synthetic tasks: 100th-percentile score by surrogate$\times$optimizer (30 seeds; higher is better). \textbf{Bold} = best per task. Within the ensemble rows the optimizer swings the score enormously (Branin $-0.78\!\to\!-9.27$; Griewank $-395\!\to\!-2612$); within the GP rows it is nearly inert (Branin all $\approx-0.40$). This interaction, not a surrogate-only or optimizer-only main effect, is the source of the reported GP-LCB ``advantage.''"
**Shows:** 9 surrogate×optimizer cells × 7 synthetic tasks, raw (un-normalized) 100th-percentile oracle score, 30 seeds.

Full body, with `tables_v2/grid.tex` ground truth for Griewank:

| Cell | Branin | Styblinski | Levy | Rosenbrock | Rastrigin | Ackley | Griewank (paper) | Griewank (grid.tex) |
|---|---|---|---|---|---|---|---|---|
| Ens × Grad | −9.27 | 6.37 | −2.14 | −0.28 | −7.71 | −3.66 | **−2592** | −2592.24 |
| Ens × Pert | −0.78 | 33.08 | −0.40 | −0.12 | −8.44 | −6.32 | −395 | −395.43 |
| Ens × CMA | **−14.01** | 5.21 | −3.19 | −0.48 | −10.81 | −4.31 | **−2613** | −2612.68 |
| GP × Grad | **−0.40** | 27.57 | **−0.05** | −0.09 | −4.83 | **−0.55** | **−0.94** | −0.94 |
| GP × Pert | −0.40 | **36.15** | −0.24 | −0.08 | −8.28 | −6.28 | **−269** ⚠ | −269.60 |
| GP × CMA | −0.40 | 26.65 | −0.05 | −0.09 | −5.06 | −0.59 | −1.00 | −1.00 |
| SVGP × Grad | −0.45 | 11.83 | −0.08 | **−0.04** | **−2.83** | −0.69 | −2.11 | −2.11 |
| SVGP × Pert | −0.40 | 34.35 | −0.25 | −0.08 | −8.27 | −6.14 | −275 | −274.62 |
| SVGP × CMA | −0.53 | 11.60 | −0.08 | −0.04 | −3.00 | −0.73 | −2.17 | −2.17 |

All non-Griewank cells match `grid.tex` exactly.

### Table 2 (`tab:attr`, main.tex:135–149)
**Caption (verbatim):** "Two-way ANOVA attribution ($\eta^2$, fraction of task-normalized variance explained by each term) across regimes. The surrogate main effect dominates on synthetic tasks and survives the matched-tuning control; the surrogate$\times$optimizer interaction is itself an order of magnitude above the optimizer main effect. On Design-Bench neither factor explains much variance and the (small) ordering reverses. Task-and-seed bootstrap $95\%$ CIs (synthetic, unmatched): $\eta^2_{\text{surr}}\in[0.25,0.57]$, $\eta^2_{\text{opt}}\in[0.01,0.19]$ (non-overlapping), $\eta^2_{\text{inter}}\in[0.11,0.26]$."
**Shows:** η² decomposition across 3 regimes + Friedman p.

| Regime | η²_surr | η²_opt | η²_inter | Friedman p |
|---|---|---|---|---|
| Synthetic (unmatched) | **0.37** | 0.01 | 0.17 | 6.1×10⁻⁵ |
| Synthetic (matched tuning) | **0.28** | 0.02 | 0.12 | — |
| Design-Bench | 0.05 | 0.08 | 0.01 | 0.69 |

### Table 3 (`tab:dbgrid`, main.tex:167–191)
**Caption (verbatim):** "Offline MBO on Design-Bench (16 seeds; normalized 100th-percentile score, higher is better; random-forest oracles for the non-exact tasks). \textbf{Bold} = best per task including the COMs/CbAS baselines. Unlike the synthetic grid, the methods cluster tightly and the per-task winner is split across surrogates and optimizers (Friedman $p{=}0.69$ over the grid); the ensemble/COMs gradient-ascent collapse persists only on GFP."
**Shows:** 9 cells + 2 baselines × 7 Design-Bench tasks, normalized 100th-percentile, 16 seeds. **No `tables_v2/` counterpart exists — see PR-2.**

| Cell | TF-Bind-8 | TF-Bind-10 | Superconductor | GFP | UTR | Ant | D'Kitty |
|---|---|---|---|---|---|---|---|
| Ens × Grad | 2.20 | 1.34 | 0.99 | −9.61 | **1.01** | 0.92 | 0.74 |
| Ens × Pert | 1.00 | 1.31 | 1.29 | 2.48 | 0.98 | 1.29 | 1.05 |
| Ens × CMA | 2.06 | 1.15 | 1.18 | −5.63 | 0.99 | 0.89 | 0.72 |
| GP × Grad | 1.00 | 1.31 | 1.24 | 2.45 | 0.99 | 1.52 | 1.06 |
| GP × Pert | 1.00 | 1.31 | 1.31 | 2.45 | 0.99 | 1.52 | **1.11** |
| GP × CMA | 1.00 | 1.00 | 1.26 | 2.46 | 0.99 | 1.52 | 1.02 |
| SVGP × Grad | 1.84 | 1.11 | 1.07 | 1.80 | 0.99 | 0.99 | 1.02 |
| SVGP × Pert | 1.45 | 1.31 | 1.25 | 2.45 | 0.99 | 1.52 | 1.09 |
| SVGP × CMA | 1.83 | 1.11 | 1.26 | **2.48** | 0.93 | 0.91 | 1.02 |
| COMs (baseline) | **2.21** | **1.35** | 1.01 | −9.20 | **1.01** | 0.98 | 0.95 |
| CbAS (baseline) | 2.12 | 1.28 | **1.36** | 1.85 | 0.99 | **1.53** | 1.02 |

### Table 4 (`tab:controls`, main.tex:204–218)
**Caption (verbatim):** "Gap controls (synthetic; task-normalized GP $-$ ensemble marginal, with 10-seed task$+$seed bootstrap $95\%$ CIs). The gap is unchanged with pessimism off ($\beta{=}0$; the paired $\beta{=}2$ vs.\ $\beta{=}0$ difference has CI $[-0.02,0.10]$) and \emph{widens} when the ensemble is given the GP's score-biased subsample: the edge is the surrogate's posterior mean, not $\sigma$-calibration or data."
**Shows:** GP−ensemble marginal gap under 3 settings.

| Setting | gap | 95% CI |
|---|---|---|
| β=2 (pessimism on) | 0.51 | [0.43, 0.58] |
| β=0 (pessimism off) | 0.47 | [0.37, 0.57] |
| ensemble on the GP's 800-pt subsample | 0.76 | [0.29, 1.32] |

### Algorithm 1 (`alg:diag`, main.tex:261–277)
**Caption:** "Coverage diagnostic and conformal-LCB repair". Inputs: surrogate (μ,σ), data D, level δ, proposals Π. Outputs: q̂, (ĉ_in, ĉ_ood), flag. Flags when ĉ_ood < 1−δ.

### Figure 1 (`fig:heatmap`, main.tex:124–129)
**Caption (verbatim):** "Decomposition map: mean rank (over tasks, $1{=}$best) of every surrogate$\times$optimizer cell. \textbf{Left (synthetic):} the GP / SVGP surrogate is best regardless of optimizer (dark cells), while the ensemble is poor and swings with the optimizer (bright cells)---the surrogate main effect plus the ensemble$\times$optimizer interaction. \textbf{Right (Design-Bench):} the same grid collapses to a near-uniform mid-rank field, mirroring the statistically non-significant omnibus."
**Shows:** two 3×3 heatmaps of mean rank (1–9 colorbar). In-figure title: "Surrogate class dominates on synthetic tasks; the grid flattens on Design-Bench".

| | Gradient | Perturbation | CMA-ES |
|---|---|---|---|
| **Synthetic** — Ensemble | 7.1 | 6.9 | **8.6** |
| Exact GP | **2.3** | 4.7 | 3.3 |
| SVGP | 3.1 | 4.9 | 4.1 |
| **Design-Bench** — Ensemble | 5.1 | 4.1 | 6.1 |
| Exact GP | 4.1 | **3.4** ⚠ | 5.4 |
| SVGP | 6.0 | 4.9 | 5.7 |

### Figure 2 (`fig:optbysurr`, main.tex:151–156)
**Caption (verbatim):** "Optimizer-induced spread by surrogate class (synthetic; per-seed task-normalized 100th-percentile score, higher is better; boxes span the interquartile range). The three optimizers produce sharply different distributions on the ensemble surrogate but nearly identical, tightly-clustered distributions on the GP and SVGP surrogates: the acquisition optimizer matters enormously for ensembles and negligibly for the GP and SVGP surrogates, whose smooth posterior mean (not calibration) is the cause (Section~\ref{sec:mech})."
**Shows:** boxplots, 3 surrogates × 3 optimizers, task-normalized score 0–1. **No numeric labels in the figure text layer.** In-figure title: "The acquisition optimizer swings ensemble outcomes but is nearly inert for calibrated posteriors" — note the title says "calibrated posteriors" while the caption and §5 argue calibration is *not* the cause.

### Figure 3 (`fig:cd`, main.tex:160–165)
**Caption (verbatim):** "Critical-difference diagram (Nemenyi, $\alpha{=}0.05$) over the 9 grid cells. Synthetic tasks separate the cells sharply (Friedman $p{=}6.1\times10^{-5}$); Design-Bench does not ($p{=}0.69$), all cells falling within one critical difference. Method rankings do not transfer from synthetic to real."
**Shows:** two CD diagrams, CD = 4.54 both panels.
- Synthetic: GP+Grad (2.3), SVGP+Grad (3.1), GP+CMA (3.3), SVGP+CMA (4.1), GP+Pert (4.7), SVGP+Pert (4.9), Ens+Pert (6.9), Ens+Grad (7.1), Ens+CMA (8.6)
- Design-Bench: GP+Pert (3.6), GP+Grad (4.3), Ens+Pert (4.4), SVGP+Pert (4.7), Ens+Grad (5.1), GP+CMA (5.1), SVGP+CMA (5.7), SVGP+Grad (5.9), Ens+CMA (6.1)

### Figure 4 (`fig:cross`, main.tex:220–225)
**Caption (verbatim):** "Premise coverage $\Pr(f\ge\mu-\beta\sigma)$ at $\beta{=}2$ (synthetic mean), each surrogate on in-distribution points, its own proposals, and the other surrogate's proposals. The ensemble premise collapses ($0.41$) \emph{only} on the designs its own gradient ascent returns; on the GP's proposals it is well covered ($0.97$), and the GP premise holds everywhere. The failure is the ensemble$\times$gradient interaction, not a surrogate defect."
**Shows (labeled bars):** Ensemble 0.73 / 0.41 / 0.97; GP 0.98 / 0.97 / 0.93; nominal 0.90 line. Matches supplement Table 3 exactly.

### Figure 5 (`fig:coverage`, main.tex:238–243)
**Caption (verbatim):** "Coverage of the pessimism premise $\mu{-}f\le\beta\sigma$ vs.\ $\beta$ on synthetic (left) and Design-Bench (right) tasks: in-distribution (solid) and on the optimizer's OOD proposals (dashed), with $\pm1$ s.d.\ bands across tasks and the split-conformal repair shown as stars ($\star$). Ensemble in-distribution coverage is moderate, but proposal (OOD) coverage is far lower and task-dependent---near zero on the tasks where gradient ascent collapses; conformal recalibration lifts in-distribution coverage to its $0.90$ target (upper star) but leaves the OOD coverage the bound actually needs far below it (lower star)."
**Shows:** coverage vs β ∈ [1,5] (axis ticks 1–5), two panels, ±1 s.d. bands, conformal stars. **No numeric data labels in the text layer** — only "nominal 0.90". Visual read: synthetic in-dist rises ≈0.58→0.87, OOD ≈0.36→0.50; DB in-dist ≈0.72→0.82, OOD ≈0.17→0.20; DB conformal OOD star ≈0.31.

### Figure 6 (`fig:beta`, main.tex:245–250)
**Caption (verbatim):** "Pessimism sweep: per-task normalized 100th-percentile score vs.\ $\beta$ (faint lines, individual synthetic tasks; bold line, mean). Score rises with $\beta$ on 6 of 7 tasks even though $\sigma$ is an uninformative error signal ($\rho\approx0.1$)---pessimism acts as distance-regularization. Ackley is the single task where the penalty points the wrong way."
**Shows:** β ∈ {0,1,2,3,4,5} axis, normalized score 0–1, per-task faint lines + mean. In-figure title: "Pessimism helps on 6/7 tasks despite an uninformative σ: regularization, not calibration". **No numeric labels** — the "+0.19 median slope" is not readable from the figure.

## supplement.pdf

### Table 1 (`tab:sfull`, supplement.tex:58–80)
**Caption (verbatim):** "Full synthetic grid, 100th-percentile score (30 seeds), including domain baselines. \textbf{Bold} = best per task."
**Shows:** 9 cells + COMs + CbAS + Grad.Asc. × 7 synthetic tasks. Identical to main Table 1 for the 9 cells **except GP+Pert Griewank = −270 (main says −269)**. Extra rows:

| Method | Branin | Styblinski | Levy | Rosenbrock | Rastrigin | Ackley | Griewank | (`grid_full.tex`) |
|---|---|---|---|---|---|---|---|---|
| COMs | −9.73 | 8.50 | −4.44 | −1.31 | −6.97 | −4.49 | −2078 | −2077.78 |
| CbAS | −5.64 | 33.85 | −0.21 | −0.05 | −8.02 | −5.10 | −276 | −276.02 |
| Grad. Asc. | −8.35 | 3.49 | −2.43 | −0.31 | −9.08 | −3.04 | −2701 | −2701.00 |

### Table 2 (`tab:srank`, supplement.tex:82–98)
**Caption (verbatim):** "Average rank over the 7 synthetic tasks (from Table~\ref{tab:sfull}; lower is better)."
**Shows:** 12-method average rank. **Byte-identical to `tables_v2/grid_full_rank.tex`.**

| Method | Rank | Method | Rank |
|---|---|---|---|
| GP+Grad | 2.57 | GP+Pert | 5.71 |
| SVGP+Grad | 3.29 | SVGP+Pert | 5.86 |
| GP+CMA | 3.57 | CbAS | 6.00 |
| SVGP+CMA | 4.29 | Ens+Pert | 8.14 |
| Ens+Grad | 8.57 | COMs | 9.43 |
| Grad.Asc. | 9.86 | Ens+CMA | 10.71 |

### Table 3 (`tab:cross`, supplement.tex:112–124)
**Caption (verbatim):** "Premise coverage at $\beta{=}2$ (synthetic mean), each surrogate on in-distribution points, its own proposals, and the other surrogate's proposals."

| Premise | in-dist | own prop. | other's prop. |
|---|---|---|---|
| Ensemble | 0.73 | 0.41 | 0.97 |
| GP | 0.98 | 0.97 | 0.93 |

### Table 4 (`tab:cc`, supplement.tex:144–160)
**Caption (verbatim):** "Official vs.\ reimplemented baselines (normalized 100th-percentile)."

| Method | Task | Official | Ours | \|Δ\| | Verifies? |
|---|---|---|---|---|---|
| COMs | Superconductor | 1.31 | 1.01 | 0.30 | ✓ |
| COMs | TF-Bind-8 | 0.99 | 2.21 | 1.22 | ✓ |
| COMs | GFP | −8.38 | −9.20 | 0.82 | ✓ |
| CbAS | Superconductor | 1.21 | 1.36 | 0.15 | ✓ |
| CbAS | TF-Bind-8 | 2.13 | 2.12 | **0.004** | **✗ (implies 0.01)** |
| CbAS | GFP | 2.20 | 1.85 | 0.35 | ✓ |

"Ours" column cross-checks against main Table 3 exactly (COMs Super 1.01, TFB8 2.21, GFP −9.20; CbAS Super 1.36, TFB8 2.12, GFP 1.85). ✓

### Table 5 (`tab:cov`, supplement.tex:165–190)
**Caption (verbatim):** "One-sided coverage of the premise $\mu{-}f\le\beta\sigma$ (i.e.\ $f\ge\mu-\beta\sigma$) at $\beta{=}2$ (nominal $0.90$). $c_{\text{in}}/c_{\text{ood}}$: coverage in-distribution / on proposals; $\hat q$: signed split-conformal multiplier (negative $\Rightarrow$ the mean already over-covers); $c^{\text{cf}}$: coverage after replacing $\beta$ with $\hat q$."

| Task | c_in | c_ood | q̂ | c^cf_in | c^cf_ood |
|---|---|---|---|---|---|
| Branin | 0.71 | 0.42 | 6.2 | 0.91 | 0.84 |
| Styblinski | 0.64 | 0.00 | 7.5 | 0.90 | 0.00 |
| Levy | 0.68 | 0.11 | 6.0 | 0.90 | 0.28 |
| Rosenbrock | 0.86 | 0.64 | 2.5 | 0.90 | 0.66 |
| Rastrigin | 0.73 | 0.72 | 4.8 | 0.91 | 0.77 |
| Ackley | 0.92 | 1.00 | **1.8** | **0.89** ⚠ | 1.00 |
| Griewank | 0.57 | 0.00 | **16.1** | 0.90 | 0.00 |
| TF-Bind-8 | 0.92 | 0.71 | 1.7 | 0.90 | 0.70 |
| TF-Bind-10 | 1.00 | 0.53 | −1.6 | **0.89** ⚠ | 0.45 |
| Superconductor | 1.00 | 0.01 | −2.0 | 0.90 | 0.01 |
| GFP | **0.00** | 0.00 | **88.4** | 0.90 | 0.99 |
| UTR | 1.00 | 0.00 | −2.5 | 0.91 | 0.00 |
| Ant | 0.94 | 0.00 | 1.2 | 0.90 | 0.00 |
| D'Kitty | 0.51 | 0.00 | 8.0 | 0.90 | 0.00 |

**Verified means (recomputed):** synthetic c_in **0.73** ✓, c_ood **0.4129→0.41** ✓, c^cf_in **0.9014→0.90** ✓, c^cf_ood **0.5071→0.51** ✓. Real c_in **0.7671→0.77** ✓, c_ood **0.1786→0.18** ✓, c^cf_in **0.90** ✓, c^cf_ood **0.3071→0.31** ✓. **All eight aggregate coverage numbers in the body reproduce exactly from this table.**

### Figure 1 (`fig:calib`, supplement.tex:130–134)
**Caption (verbatim):** "Calibration quality vs.\ pessimism benefit. Each point is a synthetic task; the $\sigma$--error rank correlation $\rho$ (x-axis) does not predict the gain from pessimism (y-axis), consistent with a regularization rather than calibration effect."
**Shows:** scatter, 7 labeled synthetic tasks. x-axis "error rank correlation ρ (calibration quality)" ticks 0.05–0.20; y-axis "Task-normalized pessimism benefit (β=5 vs. β=0)" −1.0 to 1.0. This is the only visible support for "ρ≈0.1"; no per-task ρ values are printed.

### Figure 2 (`fig:k`, supplement.tex:135–139)
**Caption (verbatim):** "Ensemble-size ablation. Task-normalized score decreases with $K$."
**Shows:** K ∈ {2,3,5,10} axis, normalized score 0–1, mean across tasks. In-figure title: "More ensemble members shrink σ and weaken the penalty: score falls with K". No numeric labels.

---

# 3. EXACT CLAIMS: PROPOSITIONS, SCOPE, CONTROLS, ORACLE

## 3.1 Proposition 1 — verbatim (main.tex:229–232)

> **Proposition 1** (Coverage of the premise is LCB validity).
> For any $Q,\beta,\delta$, $\;\Pr_{x\sim Q}(f(x)\ge L_\beta(x))=\Pr_{x\sim Q}(\mu(x)-f(x)\le\beta\sigma(x))$. Hence $L_\beta$ is a valid $(1{-}\delta)$ lower bound under $Q$ iff the premise $\{\mu-f\le\beta\sigma\}$ has $Q$-probability at least $1{-}\delta$.

Setup (main.tex:227): "Write $L_\beta(x)=\mu(x)-\beta\sigma(x)$; call $L_\beta$ a valid $(1{-}\delta)$ lower bound under a distribution $Q$ if $\Pr_{x\sim Q}(f(x)\ge L_\beta(x))\ge 1{-}\delta$."

Supplement restatement (supplement.tex:35–39) is identical in content. Proof (supplement.tex:40–42), verbatim:
> "Since $\sigma>0$, pointwise $f(x)\ge\mu(x)-\beta\sigma(x)\iff\mu(x)-f(x)\le\beta\sigma(x)$. The two events coincide as subsets of $\X$ and hence have equal probability under any $Q$."

Sanity checks (supplement.tex:43): "$\beta{=}0$ gives $\Pr(f\ge\mu)=\Pr(\mu-f\le0)$; $\beta\to\infty$ gives coverage $\to1$. The identity is dimensionless and uses $\sigma>0$ once."

## 3.2 Proposition 2 — verbatim (main.tex:254–257)

> **Proposition 2** (Conformal repair; shift-limited transfer).
> Let $\{(x_i,f(x_i))\}_{i=1}^n$ be exchangeable from $P$, $r_i=(\mu(x_i)-f(x_i))/\sigma(x_i)$ the signed one-sided nonconformity, and $\hat q$ the $\lceil(n{+}1)(1{-}\delta)\rceil$-th smallest $r_i$. Then for a fresh $x\sim P$, $\Pr(f(x)\ge\mu(x)-\hat q\,\sigma(x))\ge 1{-}\delta$. Under a shifted proposal $\Pi\neq P$ with density ratio $w=d\Pi/dP$, validity is restored by weighting the calibration quantile by $w$ (weighted conformal; \citealp{tibshirani2019conformal}).

Supplement version (supplement.tex:45–49) is titled "Split-conformal repair; shift-limited transfer" (main says "Conformal repair; shift-limited transfer") and adds "for a fresh $x_{n+1}\sim P$ **exchangeable with the calibration set**" — a hypothesis the main-paper statement omits. Proof at supplement.tex:50–52.

## 3.3 The "low dimensional" scope claim

| Location | Quote | Note |
|---|---|---|
| main.tex:49 (abstract) | "GP-LCB) outperforms neural-ensemble LCB **at low dimension** because the GP posterior is better calibrated" | framed as the intuition being tested |
| main.tex:58 | "GP-LCB) is preferable to neural-ensemble LCB **at low dimension**, on the grounds that the GP posterior is better calibrated" | |
| main.tex:281 | "(i) On smooth, **low-to-moderate-dimensional** problems, a GP/SVGP surrogate is robust to the acquisition optimizer" | the guidance actually issued |
| main.tex:291 (conclusion) | "The reported **low-dimensional** advantage of GP-LCB in offline MBO is not a clean surrogate-class effect" | |

**Tension:** the synthetic suite runs to **Griewank-30D**, and the CMA-ES config anticipates **d>500** (main.tex:86), while Design-Bench GFP relaxed to per-position logits is far higher-dimensional still. "Low dimension" is never numerically defined anywhere in either document. The paper never states Design-Bench task dimensions at all.

## 3.4 The matched-tuning control

main.tex:94, verbatim:
> "\paragraph{Matched tuning (identifiability control).} Exact and sparse GPs, unlike ensembles, can spend per-run hyperparameter-optimization budget. The \mdemph{matched} arm freezes GP hyperparameter fitting so every surrogate gets the same zero per-run tuning budget, isolating the surrogate-class effect from a GP-tuning advantage."

main.tex:133: "Under \mdemph{matched} tuning the surrogate effect persists ($\eta^2_{\text{surr}}{=}0.28$, retaining $76\%$ of its unmatched $0.37$), so it is not merely a per-run tuning budget the ensemble lacks."

main.tex:64: "a matched-tuning control shows the surrogate effect is not a GP-tuning artifact (it retains $76\%$)."

supplement.tex:101 (§3, "GATE-1"), verbatim:
> "The surrogate main effect on synthetic tasks is $\eta^2_{\text{surr}}{=}0.37$ unmatched and $0.28$ matched---a $76\%$ retention. The optimizer main effect stays small in both ($\eta^2_{\text{opt}}{=}0.01\to0.02$) and the interaction stays large ($\eta^2_{\text{inter}}{=}0.17\to0.12$). The GP advantage is therefore a surrogate-class property, not a per-run tuning artifact."

Arithmetic: 0.28/0.37 = 0.7568 → "76%" ✓. **No matched-tuning per-task table or figure exists** — only the Table 2 row. See PR-3.

## 3.5 The β=0 control

main.tex:198, verbatim:
> "If the GP's edge were a calibrated LCB, removing the pessimism term should erase it. It does not. Re-running the full grid at $\beta{=}0$ (posterior-mean maximization, no $\sigma$ penalty), the GP--ensemble marginal gap is essentially unchanged---$0.51$ at $\beta{=}2$ versus $0.47$ at $\beta{=}0$ (task-normalized, averaged over optimizers; the paired difference has $95\%$ CI $[-0.02,0.10]$, indistinguishable from zero; Table~\ref{tab:controls})---and the ensemble still collapses under gradient ascent with no pessimism at all (Griewank $-2701$ vs.\ the GP's $-0.94$). The advantage is a property of the GP's smooth mean, not of $\sigma$."

supplement.tex:106, verbatim:
> "Re-running the full $3\times3$ grid at $\beta{=}0$ (no $\sigma$ penalty), the GP--ensemble marginal gap is $0.47$, essentially the $\beta{=}2$ value of $0.51$: pessimism is not the source of the GP advantage. Per-task, the ensemble$\times$gradient cell still collapses without pessimism (Griewank $-2701$, Rastrigin $-28.2$) while the GP does not (Griewank $-0.94$)."

Rastrigin −28.2 appears **only** in supplement.tex:106 — no table, no figure. See PR-4. Also see INC-13 for the −2701 / −0.94 duplication concern.

## 3.6 The RF-oracle substitution and its defense

**The substitution** (main.tex:92): "7 Design-Bench tasks (TF-Bind-8/10 with exact oracles; Superconductor, GFP, UTR, Ant, D'Kitty with random-forest oracles to remove simulator/framework dependencies)."

**The scoping admission** (main.tex:285), verbatim:
> "First, for the non-exact tasks we substitute a random-forest oracle to remove simulator and framework dependence---a genuine substitution on GFP, UTR, Ant, and D'Kitty (the native oracle is an RF only for Superconductor), so a different oracle could re-separate methods. But it does not manufacture the null: on the three tasks with no smoothing RF substitution (TF-Bind-8/10 exact, Superconductor native RF), the omnibus stays flat (Friedman $p{=}0.93$) and the median 9-cell spread ($0.34$) is no smaller than on the substituted tasks ($0.39$)."

**The supplement version** (supplement.tex:195), verbatim:
> "Because four of the seven Design-Bench tasks use a substituted random-forest oracle (GFP, UTR, Ant, D'Kitty), we check that the null is not manufactured by RF-flattened surfaces. Restricted to the three tasks whose oracle is \emph{not} a smoothing RF substitution---TF-Bind-8/10 (exact oracles) and Superconductor (native random-forest oracle)---the Friedman omnibus over the 9 cells is $p{=}0.93$, and the median per-task method spread ($0.34$ normalized) is no smaller than on the four substituted tasks ($0.39$). The synthetic-to-real collapse of method separation is therefore a property of the real tasks, not an artifact of the oracle substitution."

Task accounting is consistent: 5 RF oracles = 4 substituted + 1 native (Superconductor); 3 non-substituted = 2 exact + 1 native RF. ✓
**But the defense's key sentence contradicts its own numbers — see INC-4.** And the entire defense (p=0.93, 0.34, 0.39) has no table or figure — see PR-5.

Also framed as an abstract-level claim (main.tex:66): "a gap we show is not an artifact of the random-forest oracles."

## 3.7 The TOST / equivalence claim

main.tex:158, verbatim:
> "We are careful not to overstate the null: a paired equivalence test (TOST) on the best-versus-worst cells does \mdemph{not} establish equivalence---the $90\%$ CI on their gap is $\pm0.48$ normalized units---so the real-task result is that method choice is unresolved and \mdemph{underpowered at $N{=}7$ tasks}, not that the methods are provably equal."

main.tex:283: "It is a significance collapse, not a claim of equivalence---the differences are unresolved, not provably zero (underpowered at $N{=}7$)."
main.tex:49 (abstract): "an equivalence test is underpowered at $N{=}7$".
supplement.tex:193: "paired TOST equivalence tests are computed by the released \texttt{stats.py}" — **no ±0.48 in the supplement.** See PR-6.

---

# 4. STATED EXPERIMENTAL CONFIGURATION (as the PAPER claims it)

For later diff against code. main.tex and supplement.tex **agree on every config value below** — no inconsistencies found in §4.

## 4.1 Surrogates

| Parameter | main.tex:84 | supplement.tex:198 |
|---|---|---|
| Ensemble K | `K=5` | `K=5` |
| Architecture | "two-hidden-layer MLPs (width 96, ReLU)" | "two hidden layers of width 96, ReLU" |
| Loss | "trained by MSE" | "MSE" |
| Epochs | `35 epochs` | `35 epochs` |
| Optimizer / lr | "Adam, lr $3\times10^{-3}$" | "Adam (lr $3\times10^{-3}$, weight decay $10^{-4}$)" |
| Weight decay | **not stated** | `10^{-4}` |
| Batch size | **not stated** | `256` |
| Seeding | **not stated** | "per-member seed offset" |
| μ, σ definition | "the member mean and standard deviation" | — |
| Exact GP kernel | "differentiable single-task GP (ARD Matérn-$5/2$)" | "ARD Matérn-$5/2$" |
| Exact GP fit | "fit by marginal likelihood on a score-biased subsample" | "marginal-likelihood fit (frozen under matched tuning)" |
| Exact GP N_max | `800` | `800` |
| SVGP inducing points | `128` | `128` |
| SVGP kernel | "ARD Matérn-$5/2$" | "ARD Matérn-$5/2$" |
| SVGP steps | "250 ELBO steps" | "250 variational-ELBO steps" |
| SVGP lr | **not stated** | "Adam lr 0.01" |
| SVGP N_max | `2000` | `2000` |

## 4.2 Optimizers

| Parameter | main.tex:86 | supplement.tex:199 |
|---|---|---|
| Gradient steps | "100 Adam steps on $x$" | "100 Adam steps on $x$" |
| Gradient lr | `0.05` | `0.05` |
| Gradient constraint | "box-clipped to $[0,1]^d$" | "box-clipped" |
| Perturbation rounds | `5 rounds` of Gaussian hill-climbing | `5 rounds` |
| Perturbation σ | `{0.1, 0.05, 0.02}` | `{0.1, 0.05, 0.02}` |
| Perturbation accept rule | **not stated** | "elementwise accept-if-better" |
| CMA-ES initial σ | `0.2` | `0.2` |
| CMA-ES bounds | **not stated** | `[0,1]` |
| CMA-ES separable | "separable variant when $d{>}500$" | "separable (diagonal) covariance when $d{>}500$" |

## 4.3 Acquisition, protocol, seeds

| Parameter | main.tex | supplement.tex:200 |
|---|---|---|
| Acquisition | "LCB $\mu(x)-\beta\sigma(x)$ with $\beta{=}2$" (:88) | "LCB $\mu-\beta\sigma$, $\beta{=}2$" |
| β=0 meaning | "$\beta{=}0$ recovers pure surrogate maximization" (:88) | — |
| Candidate budget | "collect the 128 proposed designs" (:90); "Each method proposes 128 candidates" (:92) | "Candidate budget $128$ (top-$128$ dataset points plus $\sigma{=}0.05$ perturbations as starts; top-$128$ by surrogate score evaluated by the oracle)" |
| Init perturbation σ | **not stated** | `0.05` |
| Metric | "100th-percentile (max) oracle score, following Design-Bench" (:92) | "$100$th- and $50$th-percentile normalized scores" |
| Seeds synthetic | `30` (:92) | `30` |
| Seeds Design-Bench | `16` (:92) | `16` |
| Seeds β/K/calibration sweeps | **not stated** | `10` |
| Grid size | "a full $3\times3$ grid of 9 cells, plus the COMs, CbAS, and gradient-ascent baselines" (:86) | — |
| Held identical | "the data split, candidate budget, input normalization, and oracle scoring are held identical" (:90) | — |

## 4.4 Tasks and dimensions

| Task | Dim | N (dataset size) | Oracle | Source |
|---|---|---|---|---|
| Branin | 2D | 2000 | synthetic | supplement.tex:201 |
| Styblinski | 5D | 3000 | synthetic | supplement.tex:201 |
| Levy | 8D | 4000 | synthetic | supplement.tex:201 |
| Rosenbrock | 10D | 5000 | synthetic | supplement.tex:201 |
| Rastrigin | 15D | 5000 | synthetic | supplement.tex:201 |
| Ackley | 20D | 5000 | synthetic | supplement.tex:201 |
| Griewank | 30D | 8000 | synthetic | supplement.tex:201 |
| TF-Bind-8 | **not stated** | ≤8000 (subsampled) | exact | main.tex:92 |
| TF-Bind-10 | **not stated** | ≤8000 | exact | main.tex:92 |
| Superconductor | **not stated** | ≤8000 | **native RF** | main.tex:285 |
| GFP | **not stated** | ≤8000 | **substituted RF** | main.tex:285 |
| UTR | **not stated** | ≤8000 | **substituted RF** | main.tex:285 |
| Ant | **not stated** | ≤8000 | **substituted RF** | main.tex:285 |
| D'Kitty | **not stated** | ≤8000 | **substituted RF** | main.tex:285 |

**No Design-Bench dimension is stated anywhere in either document.** Given the "low dimension" framing (§3.3) this is a notable omission.

Other task-protocol claims:
- main.tex:92 / supplement.tex:201: "dataset drawn once at seed 0 and fixed across seeds"; main.tex:287: "The synthetic datasets are fixed across seeds (seed-0), so reported variance is training/optimization, not data-draw."
- main.tex:92: "Discrete designs are relaxed to per-position class logits and decoded by argmax; continuous inputs and all scores are min-max normalized."
- supplement.tex:201: "raw rows score-biased-subsampled to $8000$ before encoding."

## 4.5 Calibration measurement (supplement.tex:202 only)

> "One-sided premise coverage $\widehat{\Pr}(\mu-f\le\beta\sigma)$ (the LCB lower-bound event $f\ge\mu-\beta\sigma$) estimated in-distribution on uniform test points and out-of-distribution on the gradient-ascent proposals, at $\beta\in\{0.5,1,2,5\}$. Split-conformal multiplier $\hat q$ from the signed nonconformity $(\mu-f)/\sigma$ with a relative $\sigma$ floor ($5\%$ of the calibration-fold mean), fit at $\delta{=}0.1$ on a held-out fold; $\rho_{\text{err}}=$ Spearman$(\sigma,|\mu-f|)$."

| Parameter | Value |
|---|---|
| In-dist eval points | "uniform test points" |
| OOD eval points | "the gradient-ascent proposals" |
| β grid (coverage) | `{0.5, 1, 2, 5}` |
| β grid (score sweep, supplement.tex:127) | `{0, 0.5, 1, 2, 5}` |
| σ floor | "5% of the calibration-fold mean" (relative) |
| δ | `0.1` (→ nominal 0.90) |
| ρ_err | Spearman(σ, \|μ−f\|) |
| K sweep | `{2, 3, 5, 10}` (supplement.tex:128) |

**Note:** Figure 6 (`fig4_beta_sweep`) x-axis renders ticks 0–5 and the coverage figure (Figure 5, `fig3_coverage`) renders ticks 1–5, consistent with the two different β grids above.

## 4.6 Statistical machinery

main.tex:96, verbatim:
> "Per task we min-max normalize the grid and compute a two-way ANOVA: $\eta^2_{\text{surr}}$ and $\eta^2_{\text{opt}}$ are the fractions of normalized-score variance explained by the surrogate and optimizer main effects. Significance uses Wilcoxon signed-rank with Holm correction, an omnibus Friedman test, Nemenyi critical differences, and bootstrap rank confidence intervals."

supplement.tex:193: "bootstrap $95\%$ CI $[1.29,3.57]$ over **10,000 task resamples**"; "Per-task Wilcoxon signed-rank tests with Holm correction and paired TOST equivalence tests are computed by the released `stats.py`; at the reported seed counts no Design-Bench pairwise comparison is significant after correction, and the omnibus null is not rejected."

**Seed-count mismatch to flag:** Table 4 (gap controls) caption says "**10-seed** task+seed bootstrap 95% CIs" while Table 1 is 30 seeds. The config paragraph allots 10 seeds only to "the β/K/calibration sweeps" — the **matched-subsample control is not in that list**, yet its CI is 10-seed. So the headline gap `0.51` in Table 4 is likely NOT derived from the 30-seed Table 1 grid. See PR-7.

---

# 5. FULL QUANTITATIVE INVENTORY — main.tex

Every number, in source order. (Table/figure bodies already itemized in §2; this section covers prose, captions, and config.)

| Value | Location | Verbatim claim text (short) | Purports to measure |
|---|---|---|---|
| 7 / 7 | main.tex:49 | "on 7 synthetic and 7 Design-Bench tasks" | task counts |
| η²=0.37 | main.tex:49 | "the surrogate main effect dominates ($\eta^2{=}0.37$ vs.\ $0.01$ for the optimizer)" | surrogate main effect, synthetic |
| η²=0.01 | main.tex:49 | same | optimizer main effect, synthetic |
| η²=0.17 | main.tex:49 | "a large surrogate$\times$optimizer interaction ($\eta^2{=}0.17$)" | interaction, synthetic |
| β=0 | main.tex:49 | "unchanged when the pessimism term is removed ($\beta{=}0$)" | pessimism control |
| 0.73 | main.tex:49 | "moderately covered in-distribution ($0.73$, below the nominal $0.90$)" | ensemble in-dist premise coverage, synthetic |
| 0.90 | main.tex:49 | same | nominal coverage target |
| 0.41 | main.tex:49 | "collapses on the designs its own gradient ascent returns ($0.41$)" | ensemble own-proposal coverage |
| 0.97 | main.tex:49 | "while remaining well covered ($0.97$) on the GP's proposals" | ensemble coverage on GP proposals |
| 0.90 | main.tex:49 | "restores in-distribution coverage to its $0.90$ target" | conformal repair target |
| p=6×10⁻⁵ | main.tex:49 | "highly significant on synthetic benchmarks (Friedman $p{=}6\times10^{-5}$)" | synthetic omnibus ⚠ INC-9 |
| p=0.69 | main.tex:49 | "unresolved on Design-Bench ($p{=}0.69$...)" | DB omnibus |
| N=7 | main.tex:49 | "an equivalence test is underpowered at $N{=}7$" | task count for TOST |
| 7 / 7 | main.tex:64 | "on 7 synthetic and 7 Design-Bench tasks under one score-closure protocol" | task counts |
| 0.37 / 0.01 | main.tex:64 | "The surrogate main effect dominates on synthetic tasks ($\eta^2{=}0.37$ vs.\ $0.01$)" | ANOVA |
| 0.17 | main.tex:64 | "a large surrogate$\times$optimizer \mdemph{interaction} ($\eta^2{=}0.17$)" | ANOVA |
| 76% | main.tex:64 | "a matched-tuning control shows the surrogate effect is not a GP-tuning artifact (it retains $76\%$)" | matched-tuning retention |
| 0.41 | main.tex:65 | "collapses only on the ensemble's own gradient proposals (coverage $0.41$)" | coverage |
| 0.97 | main.tex:65 | "while holding on the GP's ($0.97$)" | coverage |
| p=6×10⁻⁵ | main.tex:66 | "Method choice is highly significant on synthetic benchmarks (Friedman $p{=}6\times10^{-5}$)" | omnibus ⚠ INC-9 |
| p=0.69, N=7 | main.tex:66 | "statistically unresolved on Design-Bench ($p{=}0.69$; a paired equivalence test is underpowered at $N{=}7$ tasks)" | omnibus + power |
| K=5, 96, 35, 3e-3 | main.tex:84 | "$K{=}5$ two-hidden-layer MLPs (width 96, ReLU), trained by MSE for 35 epochs (Adam, lr $3\times10^{-3}$)" | ensemble config |
| Matérn-5/2, 800 | main.tex:84 | "a differentiable single-task GP (ARD Mat\'ern-$5/2$), fit by marginal likelihood on a score-biased subsample ($N_{\max}{=}800$)" | exact GP config |
| 128, 250, 2000 | main.tex:84 | "128 inducing points, ARD Mat\'ern-$5/2$, 250 ELBO steps ($N_{\max}{=}2000$)" | SVGP config |
| 100, 0.05, [0,1]^d | main.tex:86 | "100 Adam steps on $x$ (lr $0.05$), box-clipped to $[0,1]^d$" | gradient optimizer |
| 5, {0.1,0.05,0.02} | main.tex:86 | "5 rounds of Gaussian hill-climbing ($\sigma\in\{0.1,0.05,0.02\}$)" | perturbation optimizer |
| 0.2, d>500 | main.tex:86 | "population search (initial $\sigma{=}0.2$, separable variant when $d{>}500$)" | CMA-ES config |
| 3×3, 9 | main.tex:86 | "a full $3\times3$ grid of 9 cells, plus the COMs, CbAS, and gradient-ascent baselines" | grid size |
| β=2, β=0 | main.tex:88 | "All cells maximize the LCB $\mu(x)-\beta\sigma(x)$ with $\beta{=}2$; $\beta{=}0$ recovers pure surrogate maximization" | acquisition |
| 128 | main.tex:90 | "collect the 128 proposed designs, and score them with the ground-truth oracle" | candidate budget |
| 7, 2D, 30D, seed 0 | main.tex:92 | "7 synthetic functions (Branin-2D through Griewank-30D; fixed dataset drawn once at seed 0)" | synthetic suite |
| 7 | main.tex:92 | "7 Design-Bench tasks (TF-Bind-8/10 with exact oracles; Superconductor, GFP, UTR, Ant, D'Kitty with random-forest oracles...)" | DB suite + oracle assignment |
| 128, 100th | main.tex:92 | "Each method proposes 128 candidates; we report the 100th-percentile (max) oracle score, following Design-Bench" | budget + metric |
| 30, 16 | main.tex:92 | "We run 30 seeds on synthetic and 16 on Design-Bench." | seed counts |
| 30 seeds | main.tex:100 | Table 1 caption "(30 seeds; higher is better)" | Table 1 provenance |
| −0.78, −9.27 | main.tex:100 | "(Branin $-0.78\!\to\!-9.27$..." | ensemble Branin swing ⚠ INC-2 |
| −395, **−2612** | main.tex:100 | "...Griewank $-395\!\to\!-2612$)" | ensemble Griewank swing ⚠ **INC-2 — matches no table cell** |
| ≈−0.40 | main.tex:100 | "within the GP rows it is nearly inert (Branin all $\approx-0.40$)" | GP Branin inertness |
| −0.78, −9.27 | main.tex:131 | "(Branin $-0.78$ for perturbation vs.\ $-9.27$ for gradient..." | body restatement |
| −395, **−2592** | main.tex:131 | "...Griewank $-395$ vs.\ $-2592$)" | body restatement ⚠ differs from caption |
| ≈−0.40 | main.tex:131 | "Within the \mdemph{GP} rows the same optimizer switch barely moves the score (Branin all $\approx-0.40$)" | GP inertness |
| 0.37, 0.01 | main.tex:133 | "($\eta^2_{\text{surr}}{=}0.37$ vs.\ $\eta^2_{\text{opt}}{=}0.01$)" | ANOVA |
| 0.28, 76%, 0.37 | main.tex:133 | "the surrogate effect persists ($\eta^2_{\text{surr}}{=}0.28$, retaining $76\%$ of its unmatched $0.37$)" | matched tuning |
| 0.17 | main.tex:133 | "the surrogate$\times$optimizer \mdemph{interaction} is $\eta^2_{\text{inter}}{=}0.17$, an order of magnitude above the optimizer main effect" | interaction |
| [0.25,0.57] | main.tex:137 | Table 2 caption "$\eta^2_{\text{surr}}\in[0.25,0.57]$" | bootstrap CI ⚠ PR-8 |
| [0.01,0.19] | main.tex:137 | "$\eta^2_{\text{opt}}\in[0.01,0.19]$ (non-overlapping)" | bootstrap CI ⚠ PR-8 |
| [0.11,0.26] | main.tex:137 | "$\eta^2_{\text{inter}}\in[0.11,0.26]$" | bootstrap CI ⚠ PR-8 |
| 9, 7, 6.1e-5 | main.tex:158 | "a Friedman omnibus over the 9 cells and 7 tasks gives $p{=}6.1\times10^{-5}$" | synthetic omnibus |
| 2.3, [1.3,3.6] | main.tex:158 | "with the best cell (GP$\times$gradient) at mean rank $2.3$ (bootstrap $95\%$ CI $[1.3,3.6]$)" | best synthetic cell rank |
| **4.5** | main.tex:158 | "against a Nemenyi critical difference of $4.5$" | CD ⚠ INC-8 |
| 0.69 | main.tex:158 | "On Design-Bench the same analysis yields $p{=}0.69$: no cell is distinguishable from any other" | DB omnibus |
| **3.6**, [1.9,5.7] | main.tex:158 | "(best cell GP$\times$perturbation at mean rank $3.6$, CI $[1.9,5.7]$...)" | best DB cell rank ⚠ **INC-1 — Fig 1 says 3.4** |
| 0.05 | main.tex:158 | "on real tasks the (small) surrogate advantage shrinks ($\eta^2_{\text{surr}}{=}0.05$)" | DB ANOVA |
| 0.08 | main.tex:158 | "the optimizer explains marginally more ($\eta^2_{\text{opt}}{=}0.08$)" | DB ANOVA |
| **±0.48**, 90% | main.tex:158 | "the $90\%$ CI on their gap is $\pm0.48$ normalized units" | TOST bound ⚠ PR-6 |
| N=7 | main.tex:158 | "\mdemph{underpowered at $N{=}7$ tasks}" | power |
| 2.20 | main.tex:158 | "(e.g.\ $2.20$ on TF-Bind-8, above every GP cell)" | Ens×Grad TFB8 ✓ Table 3 |
| α=0.05, 9 | main.tex:163 | Fig 3 caption "Critical-difference diagram (Nemenyi, $\alpha{=}0.05$) over the 9 grid cells" | CD config |
| 6.1e-5, 0.69 | main.tex:163 | Fig 3 caption "(Friedman $p{=}6.1\times10^{-5}$); Design-Bench does not ($p{=}0.69$)" | omnibus |
| 16 seeds, 0.69 | main.tex:169 | Table 3 caption "(16 seeds; ...)" / "(Friedman $p{=}0.69$ over the grid)" | Table 3 provenance |
| 0.51, 0.47 | main.tex:198 | "$0.51$ at $\beta{=}2$ versus $0.47$ at $\beta{=}0$" | GP−ens marginal gap ✓ Table 4 |
| [−0.02,0.10] | main.tex:198 | "the paired difference has $95\%$ CI $[-0.02,0.10]$, indistinguishable from zero" | paired β diff CI |
| −2701, −0.94 | main.tex:198 | "(Griewank $-2701$ vs.\ the GP's $-0.94$)" | β=0 collapse ⚠ PR-4, INC-13 |
| 800 | main.tex:200 | "The GP fits a score-biased $800$-point subsample while the ensemble uses all data." | subsample control |
| 0.51 → 0.76 | main.tex:200 | "it \mdemph{widens} it, from $0.51$ to $0.76$" | subsample control ✓ Table 4 |
| 0.73, 0.90 | main.tex:202 | "moderately covered for the ensemble in-distribution ($0.73$, below the nominal $0.90$)" | coverage ✓ derived from supp Table 5 |
| 0.41, 0.00 | main.tex:202 | "collapses on the designs its \mdemph{own} gradient ascent returns ($0.41$ mean; $0.00$ on the collapse tasks)" | coverage ✓ |
| 0.97 | main.tex:202 | "On the \mdemph{GP's} proposals, however, the ensemble premise is well covered ($0.97$)" | coverage ✓ |
| 0.98, 0.97 | main.tex:202 | "The GP's premise holds both in-distribution ($0.98$) and on its own proposals ($0.97$)" | coverage ✓ |
| **10-seed**, 95% | main.tex:206 | Table 4 caption "with 10-seed task$+$seed bootstrap $95\%$ CIs" | Table 4 provenance ⚠ PR-7 |
| [−0.02,0.10] | main.tex:206 | Table 4 caption, paired β diff CI | — |
| β=2, 0.41, 0.97 | main.tex:223 | Fig 4 caption "The ensemble premise collapses ($0.41$) \emph{only} on the designs its own gradient ascent returns; on the GP's proposals it is well covered ($0.97$)" | coverage |
| 0.73/0.41 | main.tex:234 | "At $\beta{=}2$, ensemble coverage is $0.73$ in-distribution / $0.41$ on proposals (synthetic)" | coverage ✓ |
| **0.77/0.18** | main.tex:234 | "and $0.77$ / $0.18$ (real), below the nominal $0.90$ exactly on the proposals where the bound must hold" | real coverage ✓ arithmetic, ⚠ **but see PR-9 (GFP artifact)** |
| ρ≈0.1 | main.tex:236 | "Spearman $\rho$ between $\sigma$ and $|\mu-f|$ is only $\approx0.1$" | calibration quality ⚠ PR-10 |
| 6 of 7 | main.tex:236 | "increasing $\beta$ improves the score on $6$ of $7$ synthetic tasks" | β benefit |
| **+0.19** | main.tex:236 | "(Figure~\ref{fig:beta}; median normalized slope $+0.19$)" | β slope ⚠ PR-11 |
| K=5 | main.tex:236 | "Ensemble size is the standard $K{=}5$" | ensemble config |
| ±1 s.d., 0.90 | main.tex:241 | Fig 5 caption "with $\pm1$ s.d.\ bands across tasks"; "lifts in-distribution coverage to its $0.90$ target" | — |
| 6 of 7, ρ≈0.1 | main.tex:248 | Fig 6 caption "Score rises with $\beta$ on 6 of 7 tasks even though $\sigma$ is an uninformative error signal ($\rho\approx0.1$)" | — |
| **[1.8,16]** | main.tex:259 | "the fitted multiplier varies widely across tasks (synthetic $\hat q\in[1.8,16]$)" | conformal multiplier range ⚠ INC-10 (table max is 16.1) |
| 0.90, 0.90 | main.tex:259 | "restores in-distribution coverage to its $0.90$ target on every task (mean $0.90$ synthetic and real)" | conformal repair ⚠ INC-5 |
| 0.51 / 0.31 | main.tex:259 | "on the shifted proposal $\Pi$ coverage stays low ($0.51$ / $0.31$ mean, near zero on the sharpest-shift tasks)" | conformal OOD ✓ derived |
| N=7 | main.tex:283 | "(underpowered at $N{=}7$)" | power |
| p=0.93 | main.tex:285 | "the omnibus stays flat (Friedman $p{=}0.93$)" | RF-defense omnibus ⚠ PR-5 |
| **0.34, 0.39** | main.tex:285 | "the median 9-cell spread ($0.34$) is no smaller than on the substituted tasks ($0.39$)" | RF-defense spread ⚠ **INC-4 (0.34 < 0.39)**, PR-5 |
| 7 | main.tex:285 | "the real-task omnibus is over 7 tasks" | task count |
| \|Δ\|=0.004 | main.tex:287 | "our CbAS matches the official scores ($|\Delta|{=}0.004$ on TF-Bind-8)" | baseline cross-check ⚠ INC-6 |
| **\|Δ\|=1.2** | main.tex:287 | "our COMs and official COMs diverge ($|\Delta|{=}1.2$, a reduced-epoch official run and a different oracle variant)" | baseline cross-check ⚠ INC-7 (supp: 1.22) |
| seed-0 | main.tex:287 | "The synthetic datasets are fixed across seeds (seed-0)" | data-draw variance |

# 5b. FULL QUANTITATIVE INVENTORY — supplement.tex (prose only)

| Value | Location | Verbatim claim text (short) | Purports to measure |
|---|---|---|---|
| 1–2, 7-page | supplement.tex:29 | "the proofs of Propositions~1--2 ... not part of the 7-page body" | scope |
| 0.37, 0.28, 76% | supplement.tex:101 | "$\eta^2_{\text{surr}}{=}0.37$ unmatched and $0.28$ matched---a $76\%$ retention" | matched tuning |
| 0.01→0.02 | supplement.tex:101 | "The optimizer main effect stays small in both ($\eta^2_{\text{opt}}{=}0.01\to0.02$)" | matched tuning |
| 0.17→0.12 | supplement.tex:101 | "the interaction stays large ($\eta^2_{\text{inter}}{=}0.17\to0.12$)" | matched tuning |
| 3×3, 0.47, 0.51 | supplement.tex:106 | "the GP--ensemble marginal gap is $0.47$, essentially the $\beta{=}2$ value of $0.51$" | β=0 control |
| −2701, **−28.2**, −0.94 | supplement.tex:106 | "(Griewank $-2701$, Rastrigin $-28.2$) while the GP does not (Griewank $-0.94$)" | β=0 per-task ⚠ PR-4 |
| 800, 0.76 | supplement.tex:108 | "the GP's score-biased $800$-point subsample rather than all data \emph{widens} the gap to $0.76$" | subsample control |
| **0.34 → 0.08** | supplement.tex:108 | "(the ensemble marginal falls from $0.34$ to $0.08$)" | ensemble marginal ⚠ PR-12 |
| 0.73, 0.97, 0.41, 0.97 | supplement.tex:110 | "The ensemble premise holds in-distribution ($0.73$) and on the GP's proposals ($0.97$) but collapses on its own ($0.41$); the GP premise holds on both ($0.97$)" | coverage ✓ Table 3 |
| {0,0.5,1,2,5} | supplement.tex:127 | "Sweeping $\beta\in\{0,0.5,1,2,5\}$" | β grid |
| 6 of 7, +0.19 | supplement.tex:127 | "improves the final score on 6 of 7 synthetic tasks (median normalized slope $+0.19$)" | β benefit ⚠ PR-11 |
| {2,3,5,10} | supplement.tex:128 | "Sweeping $K\in\{2,3,5,10\}$" | K grid |
| **0.95, 0.52, 0.32, 0.18** | supplement.tex:128 | "task-normalized score is monotonically \emph{decreasing} in $K$ ($0.95,0.52,0.32,0.18$)" | K ablation ⚠ PR-13 |
| 0.004, 1.22 | supplement.tex:142 | "CbAS matches closely (TF-Bind-8 $|\Delta|{=}0.004$); COMs diverges (TF-Bind-8 $|\Delta|{=}1.22$)" | cross-check ✓ Table 4 |
| 0.90 | supplement.tex:163 | "Conformal restores in-distribution coverage to its $0.90$ target on every task" | conformal ⚠ INC-5 |
| 9, 7, 6.1e-5 | supplement.tex:193 | "Over the 9 grid cells and 7 tasks the synthetic Friedman omnibus gives $p{=}6.1\times10^{-5}$" | omnibus |
| **4.54** | supplement.tex:193 | "(Nemenyi critical difference $4.54$" | CD ⚠ INC-8 |
| 2.29, [1.29,3.57], 10,000 | supplement.tex:193 | "best cell GP+Grad, mean rank $2.29$, bootstrap $95\%$ CI $[1.29,3.57]$ over 10{,}000 task resamples)" | synthetic best cell |
| 0.69, **3.57**, [1.86,5.71] | supplement.tex:193 | "gives $p{=}0.69$ (best cell GP+Pert, mean rank $3.57$, CI $[1.86,5.71]$...)" | DB best cell ⚠ INC-1 |
| α=0.05 | supplement.tex:193 | "the synthetic omnibus stays far below and the Design-Bench omnibus far above $\alpha{=}0.05$" | — |
| 4 / 7 | supplement.tex:195 | "four of the seven Design-Bench tasks use a substituted random-forest oracle (GFP, UTR, Ant, D'Kitty)" | oracle accounting |
| **p=0.93** | supplement.tex:195 | "the Friedman omnibus over the 9 cells is $p{=}0.93$" | RF defense ⚠ PR-5 |
| **0.34, 0.39** | supplement.tex:195 | "the median per-task method spread ($0.34$ normalized) is no smaller than on the four substituted tasks ($0.39$)" | RF defense ⚠ INC-4, PR-5 |

---

# 6. TARGETED VALUE HUNT — the audit's watchlist

Every requested value **FOUND**. Nothing MISSING.

| Requested | Status | Primary location(s) |
|---|---|---|
| η² 0.37 | FOUND | main.tex:49, :64, :133, Table 2 (:144); supplement.tex:101 |
| η² 0.01 | FOUND | main.tex:49, :64, :133, Table 2 (:144, synthetic opt); Table 2 (:146, DB inter); supplement.tex:101 |
| η² 0.17 | FOUND | main.tex:49, :64, :133, Table 2 (:144); supplement.tex:101 |
| η² 0.28 | FOUND | main.tex:64→"76%", :133, Table 2 (:145); supplement.tex:101 |
| η² 0.12 | FOUND | Table 2 (:145); supplement.tex:101 |
| η² 0.05 | FOUND | main.tex:158, Table 2 (:146) |
| η² 0.08 | FOUND | main.tex:158, Table 2 (:146) |
| η² 0.01 (2nd) | FOUND | Table 2 (:146) DB interaction |
| Friedman 6.1e-5 | FOUND | main.tex:144, :158, :163; supplement.tex:193; fig6_cd_diagram. **Abstract/:66 say 6×10⁻⁵** ⚠ INC-9 |
| Friedman 0.69 | FOUND | main.tex:49, :66, :146, :158, :163, :169; supplement.tex:193; fig6_cd_diagram |
| Friedman 0.93 | FOUND | main.tex:285; supplement.tex:195. **No table/figure** ⚠ PR-5 |
| coverage 0.73 | FOUND | main.tex:49, :65?, :202, :234; supp Table 3, fig8. Derived mean of supp Table 5 ✓ |
| coverage 0.41 | FOUND | main.tex:49, :65, :202, :223, :234; supp Table 3, fig8 ✓ |
| coverage 0.97 | FOUND | main.tex:49, :65, :202, :223; supp Table 3 (2×: ens-other, GP-own), fig8 ✓ |
| coverage 0.98 | FOUND | main.tex:202; supp Table 3, fig8 ✓ |
| coverage 0.77 | FOUND | main.tex:234 ("0.77 / 0.18 (real)"). Derived ✓ but ⚠ PR-9 |
| coverage 0.18 | FOUND | main.tex:234 ✓ derived |
| coverage 0.90 | FOUND | main.tex:49 (×2), :202, :234, :241, :259 (×2); supp Table 5 caption, :163 |
| coverage 0.51 | FOUND (2 senses) | (a) conformal OOD synthetic mean, main.tex:259 ✓ derived; (b) D'Kitty c_in, supp Table 5 (:187). Also (c) the β=2 gap 0.51 — a *third*, unrelated 0.51. |
| coverage 0.31 | FOUND | main.tex:259 ✓ derived |
| gap 0.51 | FOUND | main.tex:198, :200, Table 4 (:213); supplement.tex:106 |
| gap 0.47 | FOUND | main.tex:198, Table 4 (:214); supplement.tex:106 |
| gap 0.76 | FOUND | main.tex:200, Table 4 (:215); supplement.tex:108 |
| gap CIs | FOUND | Table 4: [0.43,0.58], [0.37,0.57], [0.29,1.32]; paired diff [−0.02,0.10] (main.tex:198, :206) |
| q̂ ∈ [1.8, 16] | FOUND | main.tex:259. ⚠ INC-10: supp Table 5 max is **16.1** (Griewank); min 1.8 = Ackley ✓ |
| ρ ≈ 0.1 | FOUND | main.tex:236, :248; supp fig:calib x-axis 0.05–0.20. ⚠ PR-10 (no exact value anywhere) |
| median slope +0.19 | FOUND | main.tex:236; supplement.tex:127. ⚠ PR-11 (no table; not readable from Fig 6) |
| CD = 4.54 | FOUND | supplement.tex:193; fig6_cd_diagram (both panels). ⚠ INC-8: main.tex:158 says **4.5** |
| TOST ±0.48 | FOUND | main.tex:158 **only**. ⚠ PR-6 (absent from supplement, no table) |
| \|Δ\| = 0.004 | FOUND | main.tex:287; supplement.tex:142, Table 4 (:156). ⚠ INC-6 |
| \|Δ\| = 1.2 | FOUND | main.tex:287. ⚠ INC-7: supplement says **1.22** |
| Branin Ens×Grad −9.27 | **CONFIRMED** | main.tex:108, supplement.tex:66, grid.tex:9 — all agree |
| Branin Ens×CMA −14.01 | **CONFIRMED** | main.tex:110, supplement.tex:68, grid.tex:11 — all agree. **Note: caption INC-2 ignores this, the true Branin extreme** |
| Griewank Ens×Grad −2592 | **CONFIRMED** | main.tex:108 (−2592), supplement.tex:66 (−2592), grid.tex:9 (−2592.24), main.tex:131 body (−2592) |
| Griewank Ens×Grad −2612? | **NO** — −2612 is **Ens×CMA** (−2612.68), appearing only in the Table 1 **caption** (main.tex:100) ⚠ **INC-2** |
| Griewank Ens×CMA −2613 | **CONFIRMED** | main.tex:110, supplement.tex:68 = −2613; grid.tex:11 = −2612.68 (rounds to −2613 ✓) |
| Fig 1 Ens×CMA = 8.6 | **CONFIRMED** | fig1_grid_heatmap synthetic panel = 8.6; fig6_cd_diagram = 8.6; grid_rank.tex = 8.57 ✓ |
| seeds 30 | FOUND | main.tex:92, :100 (Table 1 caption); supplement.tex:59, :200 |
| seeds 16 | FOUND | main.tex:92, :169 (Table 3 caption); supplement.tex:200 |
| seeds 10 | FOUND | main.tex:206 (Table 4 caption); supplement.tex:200 ("10 for the β/K/calibration sweeps") ⚠ PR-7 |
| tasks 14 | FOUND (implicit) | 7 + 7; never stated as "14" |
| tasks 7 | FOUND | main.tex:49, :64, :66, :92 (×2), :158, :283, :285; supplement.tex:83, :193, :195 |
| tasks 3 | FOUND | main.tex:285 "the three tasks with no smoothing RF substitution"; supplement.tex:195 |
| dims per task | FOUND (synthetic only) | supplement.tex:201: Branin-2D/2000, Styblinski-5D/3000, Levy-8D/4000, Rosenbrock-10D/5000, Rastrigin-15D/5000, Ackley-20D/5000, Griewank-30D/8000. **Design-Bench dims: NOT STATED ANYWHERE** |

---

# 7. UNUSED / STALE FIGURE ASSETS (not cited by either .tex)

Present in `figures/` but never `\includegraphics`'d. Several contain numbers contradicting or superseding the current paper — relevant if any were ever cited in a prior draft.

| File | Contents | Note |
|---|---|---|
| `fig1_offline_mbo.pdf` | "Offline MBO: 100th Percentile Oracle Score (**6 tasks**...)"; series Ens-LCB (Ours), COMs, Grad. Ascent, GP-LCB | **6 tasks**, not 7; "Ens-LCB (**Ours**)" framing contradicts the current decomposition framing |
| `fig1_optimizer_by_surrogate.pdf` | Grouped bars, mean rank: 7.1 / 2.3 / 3.1, 6.9 / 4.7 / 4.9, 8.6 / 3.3 / 4.1 | Same synthetic ranks as Fig 1 ✓; title says "barely matters for GP surrogates". **Tracked as modified in git status** |
| `fig2_avg_rank.pdf` | "Average Rank (**6 tasks**)": Ens-LCB 2.33, COMs 2.83, Grad. Asc. 3.00, GP-LCB **1.83** | 6 tasks; 4-method pool |
| `fig3_o2o_mbo.pdf` | "O2O MBO: Improvement vs. Budget"; online budget 10–50 | Online-to-offline experiment — **no trace in the current paper** |
| `fig4_beta_ablation.pdf` | Two-panel β ablation; "Tasks where pessimism helps" (Styblinski, Rosenbrock, Rastrigin) vs "Tasks where β=0 is competitive" (Levy, Ackley) | **2 tasks listed as β=0-competitive (Levy, Ackley)** — the current paper claims only **1** exception (Ackley), "6 of 7" |
| `fig5_rl.pdf` | "Offline RL: Episode Return"; LQR-4D, Control-6D; Ens-LCB / No Conserv. / BC | Offline-RL experiment — **no trace in the current paper** |
| `fig6_k_ablation.pdf` | K ablation over K=2..10, 5 tasks (Branin, Styblinski, Rosenbrock, Rastrigin, Ackley) | Superseded by `fig7_k_ablation` |
| `fig7_calibration.pdf` | "Ensemble Calibration Diagnostics": Spearman ρ(σ,\|error\|) and ρ(σ,dkNN) over **6 tasks**, y-axis 0.00–0.25 | Closest visible support for "ρ≈0.1"; **6 tasks**, and the current paper's calibration figure (`fig5_calibration_vs_benefit`) has **7** |

`fig4_beta_ablation.pdf` is the most substantive: it names **two** tasks where β=0 is competitive, against the paper's "6 of 7 ... the lone exception (Ackley)".

---

# 8. PROVENANCE RISKS — numbers stated with no visible source

Numbers appearing in prose/captions with **no table, no figure, and no derivable path** from published values.

| ID | Value(s) | Location | Risk |
|---|---|---|---|
| **PR-1** | Table 1 / Table 3 bodies | main.tex:104–118, :173–190; supplement.tex:62–79 | Paper tables are **hand-transcribed**, not `\input` from `tables_v2/`. INC-2 and INC-3 are exactly the failure mode this creates. `tables_v2/*.tex` and the paper are also **both dirty in git** (`M paper/tables_v2/grid.tex` etc. per git status), so even the "upstream" reference is uncommitted. |
| **PR-2** | Entire Design-Bench grid (main Table 3, 77 values) | main.tex:177–188 | **No `tables_v2/` counterpart exists** for the Design-Bench grid — only synthetic grids are generated. The single largest block of numbers in the paper has no traceable generator output in `paper/`. Candidate sources in `results/`: `results_db.json`, `results_db_matched.json`, `results_db.preserved.json`, `results_db.json.twosided.bak`. |
| **PR-3** | 0.28, 0.02, 0.12 (matched tuning) | Table 2 row (:145); supplement.tex:101 | Matched-tuning arm has **no per-task table and no figure** — only the one ANOVA row. The "76% retention" load-bearing control cannot be inspected. |
| **PR-4** | −2701, **−28.2**, −0.94 (β=0 per-task) | main.tex:198; supplement.tex:106 | β=0 per-task values appear **only in prose**. No β=0 grid table exists despite the text saying "Re-running the **full grid** at β=0". Also see INC-13 (−2701 duplicates `Grad.Asc.` Griewank; −0.94 duplicates β=2 GP×Grad Griewank). |
| **PR-5** | **p=0.93, 0.34, 0.39** | main.tex:285; supplement.tex:195 | The **entire RF-oracle defense** — the paper's answer to the most obvious reviewer attack on its central null — rests on three numbers with no table, no figure, and no per-task breakdown. Compounded by INC-4 (the sentence contradicts the numbers). |
| **PR-6** | **±0.48** (90% TOST CI) | main.tex:158 **only** | Appears **once**, in the body, nowhere else. Not in the supplement's "Significance Details" §8, which mentions TOST but gives no number. No table. Which pair is "best-versus-worst" is not specified. |
| **PR-7** | 0.51 / 0.47 / 0.76 + CIs at **10 seeds** | Table 4 caption (main.tex:206) | Table 4 is a **10-seed** bootstrap while Table 1 is **30 seeds**. The config paragraph (supplement.tex:200) allots 10 seeds only to "the β/K/calibration sweeps" — the **matched-subsample control is not in that list**. So the headline gap 0.51 is likely not derived from the published 30-seed grid, and the discrepancy is never explained. |
| **PR-8** | [0.25,0.57], [0.01,0.19], [0.11,0.26] | Table 2 caption (main.tex:137) | η² bootstrap CIs live **only in a caption**. The "(non-overlapping)" claim — which does real work separating the surrogate from the optimizer effect — is asserted, not shown. |
| **PR-9** | **0.77** (real in-dist coverage) | main.tex:234 | Arithmetically correct (0.7671 ✓) **but** driven by GFP = 0.00, which the supplement itself (:163) calls "**degenerate**... a decode artifact rather than a calibration signal". **Excluding GFP the mean is 0.895 ≈ 0.90** — i.e. *at* nominal, not "below the nominal 0.90". The main text's claim that real in-dist coverage is below nominal is an artifact of a datapoint the supplement disclaims. Main.tex:287 concedes the softness ("notably GFP") but the 0.77 claim at :234 is not qualified. |
| **PR-10** | **ρ ≈ 0.1** | main.tex:236, :248 | No exact ρ is printed anywhere. `fig5_calibration_vs_benefit` x-axis spans 0.05–0.20 with 7 unlabeled points. The number supports "σ is a weak error signal", a core mechanism claim. |
| **PR-11** | **+0.19** (median normalized slope) | main.tex:236; supplement.tex:127 | No table. Figure 6 has no numeric labels and plots score-vs-β curves, not slopes. Slope definition (OLS? endpoint difference? per-task normalization?) never given. |
| **PR-12** | **0.34 → 0.08** (ensemble marginal) | supplement.tex:108 **only** | Ensemble marginal under the subsample control appears once, in prose. No table. (Note the collision: "0.34" here is a *different* quantity from the "0.34" median spread in PR-5.) |
| **PR-13** | **0.95, 0.52, 0.32, 0.18** (K sweep) | supplement.tex:128 **only** | Four numbers in prose; `fig7_k_ablation` has no numeric labels. Main.tex:236 leans on this ("improving the ensemble on its own $K$-sweep") to corroborate the regularization reading. |
| **PR-14** | Figure 2 / 5 / 6 / supp Fig 1 / supp Fig 2 | — | Five of the eight cited figures carry **zero numeric labels** in their text layers. Any claim sourced "see Figure N" for these is unverifiable from the PDF alone. |

---

# 9. SUMMARY STATISTICS

- **Distinct numeric claims catalogued:** ~330
  - main.tex prose + captions: ~120
  - main.tex table bodies: 63 (Table 1) + 12 (Table 2) + 77 (Table 3) + 6 (Table 4) = 158
  - supplement.tex prose: ~45
  - supplement.tex table bodies: 84 (Table 1) + 12 (Table 2) + 6 (Table 3) + 18 (Table 4) + 70 (Table 5) = 190
  - figure-embedded values: 18 (Fig 1) + 18 (Fig 3) + 6 (Fig 4) = 42
- **Internal inconsistencies:** 13 (INC-1 … INC-13) — 2 severe, 4 moderate, 5 minor, 1 ambiguity, 1 flagged-for-code-diff
- **Provenance risks:** 14 (PR-1 … PR-14)
- **Requested watchlist values not found:** 0
- **Values fully verified by recomputation:** 8 coverage aggregates (all ✓), 76% retention (✓), 5 of 6 |Δ| rows (✓), Fig 1/Fig 3 synthetic rank agreement vs `grid_rank.tex` (✓, all 9)
