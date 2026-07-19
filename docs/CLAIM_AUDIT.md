# Quantitative claim audit — every number in the paper against its artifact

**Date: 2026-07-20.** Triggered by a false arithmetic claim found while building the confound
figure: the paper asserted that the corrected corner's interval `[0.290, 0.556]` "contains every
other corner's point estimate", when `on_off`'s point estimate `0.2828` sits `0.0069` **below**
that interval's lower bound. A paper whose contribution is catching this class of error cannot
ship one. This document is the full sweep.

**Scope:** every quantitative claim in `paper/aaai27/main.tex` (256 lines) and
`paper/aaai27/supplement.tex` (210 lines) — 866 numeric literal occurrences, 458 distinct
values. Six independent auditors covered disjoint line ranges; every reported failure was then
re-verified by hand against `results/*.json` before any edit was made.

**Method.** For each claim: load the source JSON, **compute** the value in Python, compare at the
precision the paper states. Never accept the paper's own number as evidence for itself; never
accept a value quoted in a `docs/*.md` summary where a `results/*.json` exists. Derived
quantities (percentages, ratios, nets) recomputed from components.

---

## Roll-up

| | count |
|---|---|
| Claims checked | **312** |
| PASS | **288** |
| **FAIL — fixed** | **23** |
| UNVERIFIABLE — external (cited from another paper) | 3 |
| UNVERIFIABLE — internal, no artifact anywhere | **1 — resolved** |
| Artifacts recovered from unmerged branches | 2 sets |

Every FAIL is fixed. No FAIL was resolved by weakening a number that was correct.

**Two whole result sets were found to exist only on unmerged branches** and are now on `draft`:
`results/swing/` (Eliminations 5–6, from `origin/c2-swing`) and — in the previous pass —
`results/mechanism/` (Elimination 7, from `origin/mechanism-positive`). Before this audit, six of
the paper's seven eliminations had a committed artifact and two did not.

---

## FAIL 1 — interval containment, and the repeat of the same error in its own fix

| | |
|---|---|
| Artifact | `results/bootstrap_eta_corners.json` |
| Sites | `main.tex` §4 body, `fig:beta` caption, `fig:beta` annotation, ledger D10 |

**Original:** "the corrected corner's interval $[0.290,0.556]$ contains every other corner's point
estimate." **False.** `on_off` point = `0.2827925`; `on_on` lower bound = `0.2896951`. It sits
`0.0069` below.

**The fix repeated the error one endpoint over.** The replacement asserted a shared region
`[0.312, 0.444]` contained by all four intervals. `min` of the four upper bounds is `on_off`'s
`0.4439559`, so a printed `0.444` is **above** it by `4.41e-05`. Nearest-rounding an endpoint of a
containment claim rounds it *out* of the set.

**Rule now enforced:** containment endpoints round **inward** — lower up, upper down. True region
`[0.3115971, 0.4439559]` → printed **`[0.312, 0.443]`**, verified contained by all four.
`code/figures/fig4_confounds.py` computes this with `math.ceil`/`math.floor` and carries an
`assert` so the figure cannot re-introduce it.

## FAIL 2 — "0.405 never appears without its interval" was false when written

`main.tex` asserts this rule about itself. Two bare occurrences existed: the `fig:confounds`
caption and the Discussion's two-confounds paragraph — both introduced in the two preceding
passes. Ledger D10's enumeration ("abstract, intro, table, conclusion") was the bug: it listed
four call sites and the two that failed were not on the list. Interval attached at both; D10's
enumeration replaced with an unconditional rule.

*Not a violation:* the `0.405` at §5 line 177 is a held-out normalized RMSE at `w=256` — a
different quantity that collides on the numeral, like the ledger's existing `0.283` and `0.556`
collisions.

## FAIL 3 — β is not the axis that comes closest to separating

Asserted: β "is the axis the seven tasks come closest to separating." The **query-budget axis
separates outright** on the same grid, same bootstrap: `[0.189,0.355]` at `Q=4,352` against
`[0.421,0.719]` at `Q=51,456` — **disjoint**, gap `+0.066`. β still overlaps by `0.069`.
Rewritten to scope β's superlative to the corner decomposition and to report the budget
separation, which is the stronger true statement.

## FAIL 4 — the marginal bands understate their own spread

Asserted "GP marginals sit at $0.75$–$0.85$ and the ensemble's at $0.24$–$0.36$" across every β,
K, budget and corner. Computed over all 13 conditions carrying marginals:

| | asserted | true | inside asserted band |
|---|---|---|---|
| GP | 0.75–0.85 | **0.659–0.846** | 11 of 26 |
| Ensemble | 0.24–0.36 | **0.171–0.343** | 7 of 13 |

The paper's own headline corner (`on_on`, ens `0.192`) and its own β=0 endpoint (GP `0.659`) both
fall outside. Corrected to the true ranges. **The "never crossing" conclusion is untouched and
comfortable** — smallest gap between the two families is `0.315`. The word "budget" is dropped
from the list of axes: no budget artifact carries per-level surrogate marginals.

## FAIL 5 — the ensemble's training targets

Asserted "raw targets spanning $-2613$ to $+36$". Recomputed the seven task datasets at their
fixed `seed 0` init — the exact `(x,y)` passed to `train_ensemble`: the true span is
**`-1560.07` to `+33.82`**. The quoted `-2613` is not a training target at all; it is the
Ens×CMA Griewank *cell-mean oracle score*, an optimizer output far outside data support, and
`+36` is the botorchgp:perturb Styblinski cell mean. Score-column extremes had been attributed to
the regression targets. Corrected to `-1560` to `+34`.

## FAIL 6–7 — both Confound code traces pointed at unrelated lines

The section's methodological promise is "each is a specific line of the scoring path, not a
judgment call", so a mispointed trace is load-bearing.

| Confound | asserted | actual |
|---|---|---|
| 1 (target scaling) | `mbo.py:36--37,130--138` vs `255,311--312` | `mbo.py:34,157--162,181--187` vs `293,379--381` |
| 2 (candidate/oracle) | `mbo.py:384--389,188,198--201,292,392--394` | `mbo.py:35--40,249--255,269--271` |

The cited lines were, variously, the SVGP class body, a blank line, botorch imports and an
sklearn kwarg. Both corrected against the shipped `code/mbo.py`.

## FAIL 8 — 76% retention is a rounding-chain artifact

`0.27543 / 0.36872 = 74.70%`. The asserted 76% is reachable only by dividing the already-rounded
display values (`0.28/0.37`). Corrected to **75%** in `main.tex` §3 and `supplement.tex` GATE-1.
(A second retention quantity exists — `gate1.retention = 84.2%`, an SEI ratio — and licenses
neither figure.)

## FAIL 9 — the K sweep is not "disjoint" from the cited robustness range

Asserted our sweep `K∈{2,3,5,10}` "is therefore disjoint below the $K\in\{5,10\}$ range". It
**contains** both elements of that range, including the peak at `K=5`. Corrected to "extends
below … sharing its two upper points and adding K=2,3".

## FAIL 10 — "published η²_opt of 0.005" is not the published value

`results/corners/analysis.json` records the prior work's table as `{surr: 0.37, opt: 0.01, inter:
0.17}`. The published η²_opt is **0.01**. The `0.005` is *our own* unmatched-budget corner. The
eightfold ratio is correct against our baseline (`0.0379/0.0049 = 7.8×`) but only `3.8×` against
the genuinely published `0.01`. The paper uses "published 0.37" correctly three times, so the same
word meant two different things. Relabelled to "our own unmatched" at all three sites (§3, §7,
abstract), with the prior `0.01` stated.

## FAIL 11–18 — Design-Bench section

| # | Claim | True value |
|---|---|---|
| 11 | "every point estimate **at the floor** of its own bootstrap interval" | bottom tenth: positions 0.09 / 9.40 / 0.39 / 5.82 % of width; `on_off` is 23.6× its floor |
| 12 | "gradient outspends perturbation $11.8\times$" | 11.8× in X3-on corners; **6.25×** in X3-off — the sentence spans all four |
| 13 | "perturbation $-0.50\%$" achieved-Q | **0.00%** in X3-off, `-0.50%` in X3-on |
| 14 | "roughly **doubles** it in every corner" | **1.46–1.88×** (off_on rises only 46%) |
| 15 | RF-oracle rejections "$p=0.02$ to $0.05$" | **0.021 to 0.033**; no corner lies between 0.034 and 0.05 |
| 16 | GFP matched CMA "51,482 queries" | **51,494**; 51,482 is TFBind10's, picked up as a corner median |
| 17 | "four of nine cells return exactly 1.0" on TF-Bind-8 | four in `off_off`/`on_on`, **three** in the other two — `ens:perturb` is not frozen there |
| 18 | "$\eta^2_{opt}$ runs **two to three times** $\eta^2_{surr}$" | matches no task set: 5-task 3.6–73×, 7-task 1.6–4.5×, matched 4.1–7.7×. It also contradicted line 220 of the same paper. Replaced with "exceeds in every corner of every task set", true everywhere |

## FAIL 19–22 — mechanism section

| # | Claim | True value |
|---|---|---|
| 19 | held-out NLL "**two orders of magnitude** worse" | **32×** (1.5 orders), and carried almost entirely by Branin — the GP is *better* on three of seven tasks, and `results/heldout.json` reverses the direction outright |
| 20 | distance estimate "six of seven **at zero to three decimals**" | none of the six is 0.000; they span `-0.022` to `+0.060`. The load-bearing point (Branin carries the pooled +0.116) survives; the precision claim did not |
| 21 | "the weak $\rho(\text{coverage},\text{score}) = 0.19$" | **0.289** (`coverage33.json`, independently recomputed). The 0.19 is a stale value from `docs/SESSION_STATE.md`. The correlation the paper calls weak is half again stronger than stated |
| 22 | "above 0.28 on the four **mid- and high-dimensional**" tasks | the four are 5D–15D; the two genuinely high-d tasks (Ackley-20D 0.196, Griewank-30D 0.234) are the ones **below** 0.28 |

## FAIL 23 — a superlative with five ties

"**The sharpest cell** is Branin-2D under ensemble gradient ascent." Five other cells also sit at
inversion rate 1.000 with `frac_worse` 1.000, and Styblinski ens:grad has 3× the magnitude (22.0
vs 7.1). Corrected to "one of the sharpest … five other cells tie it". The attached numbers
(30/30 seeds, 100% of returned designs worse) both verify.

## FAIL 24–26 — supplement

- **RF-robustness comparison ran backwards.** Asserted the exact-oracle spread `0.34` "is no
  smaller than" the substituted tasks' `0.39`. `0.34 < 0.39`. The argument needs the *substituted*
  set not to be compressed, which is what the data shows — so the comparison was stated in the
  wrong direction while its conclusion was right. Rewritten in the true direction.
- **"the four substituted tasks (0.39)" is a three-task median.** The artifact key is literally
  `spread_rfsub_exclGFP`. Including GFP the four-task median is `0.512`. Both figures now stated
  with their task counts.
- **β=0 per-task figures came from the wrong engine.** "Griewank $-2701$, Rastrigin $-28.2$ …
  GP $-0.94$" — the Rastrigin value is from `mbo_enssub`, the *matched-subsample control*, not a
  β=0 run at all; the other two are legacy-engine values sitting in a paragraph whose every other
  number is audited-engine. Audited β=0 grid gives **`-42.7` / `-9.5` / `-0.96`** — a 63×
  disagreement on the load-bearing Griewank cell. The qualitative claim (ensemble collapses, GP
  does not) survives on the audited engine; all three printed numbers were wrong.

---

## UNVERIFIABLE

### Internal — 1 (RESOLVED)

**"whose maximum is attained by seven tied rows already in the data"** (`main.tex` §6, TF-Bind-8).
No `results/*.json` records a tie count at the dataset maximum, and the Design-Bench offline set
is not vendored (`code/db_tasks.py` loads it externally), so it cannot be recomputed here. The
only source is narrative in `docs/DEGENERATE_CELLS.md`. **The claims around it do verify** — four
frozen cells, exact value 1.0, zero variance across 16 seeds. Only the tie count was unbacked.

**RESOLVED** — the specific count was dropped: the text now reads "multiple tied rows already in
the data". The verified surrounding claim (four frozen cells returning exactly 1.0 with zero
variance across 16 seeds) is unchanged, and the argument it supports — that a cell reporting
$1.0$ returned nothing better than its input — does not depend on the exact tie count.

### External — 3

Numbers cited from other papers, not checkable against this repo: Recht et al.'s relative slopes
(`1.69` CIFAR-10, `1.11` ImageNet); the published CI width `0.32` (recorded pre-registration in
`docs/PREREGISTRATION_V2.md`, arithmetically self-consistent with a published `[0.25, 0.57]`); and
the withdrawn prior-supplement `0.95 at K=2`, which by construction has no surviving artifact —
only its audited replacement `0.283` is verifiable, and it passes.

---

## Two artifact sets recovered

Both were cited in the paper while living only on unmerged branches:

| Set | Branch | Covers |
|---|---|---|
| `results/swing/` + `docs/MECHANISM_SWING.md` | `origin/c2-swing` | **Eliminations 5–6** — every number verifies: roughness cut `0.980` (gp1.0) and `0.903` (spectral norm), gap range `0.322–0.552`, GP-roughening best rise `0.1255` → +12.6%, `SM1 = KILL`, `SM2 = VOID` |
| `results/mechanism/` | `origin/mechanism-positive` | **Elimination 7** (recovered in the preceding pass) |

Before this audit two of the paper's seven eliminations had no committed artifact. Both now do.

---

## Classes that came back clean

- **All 24 cells of `tab:corners`** — point estimates, CIs, η²_opt, η²_inter, Friedman p.
- **All 84 cells of `tab:sfull`**, all 12 ranks of `tab:srank` (ordering independently
  reproduced), all 18 values of `tab:cc`, all 70 cells of `tab:cov`.
- **Every figure caption number** against what the figure code computes — ρ = −0.818 / +0.758,
  n = 5,040, medians 0.87/0.86/0.84, four-of-five bins, 7/7–2/7–3/7 inversion counts, gap
  0.480→0.476, 99.1% retained, X1 −0.084 / X3 +0.083 / net +0.038.
- **Every strike order** — `0.378` absent; the `0.51`/`0.47` pair absent; `0.556` appears only as
  a CI upper bound, never as a gap; `0.95 at K=2` and `0.97` appear only inside explicit
  withdrawal/attribution disclosures; no "the GP fits better" phrasing survives.
- **Every experimental-configuration number** in the supplement against `code/mbo.py`.
- **Main ↔ supplement agreement** on all 19 shared quantities.
- **All interval containment and exclusion logic** apart from FAIL 1: increment excludes zero,
  shrinkage covers zero, both RMSE tie cells cover zero, w=1024 gap excludes zero, within-corner
  DB intervals overlap.

## What the failure pattern says

The 23 failures are not randomly distributed. Fourteen are **precision or scope** errors on true
findings — a range quoted from one corner and applied to four, a ratio from one task set attached
to another's marginals, a superlative with unchecked ties, a band that omits its own endpoints.
Six are **provenance** errors: a number lifted from the wrong artifact, the wrong engine, or a
stale `docs/` summary that was never refreshed after the results were regenerated. Three are
**rounding-chain** errors, where a figure was derived from already-rounded display values instead
of the underlying floats.

Not one is a fabricated result, and no conclusion in the paper changed. But every one was
checkable from the repository, which is exactly the standard this paper holds its subject to.

**Standing rules this audit adds.** Round containment endpoints inward. Quote a ratio only with
the task set and corner it was computed on. Never derive a percentage from displayed values.
Cite a number from `results/*.json`, never from a `docs/*.md` restatement of it. When a claim
spans conditions, compute the extremes over all of them rather than the two you have to hand.
