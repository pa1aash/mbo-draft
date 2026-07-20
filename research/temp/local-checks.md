# Local checks — done by the orchestrator without the literature

These need no external source. They are claims-about-the-paper that the paper itself
settles, so they belong in deliverable (i) as internal-consistency items even though no
citation is miscited.

## L1 — Bibliography integrity

Script: regex over `\cite[tp]?` in `main.tex` + `supplement.tex` against `@type{key,` in
`references.bib`.

| Metric | Value |
|---|---|
| Bib entries | 67 |
| Distinct keys cited | 41 |
| **Undefined (cited, not in bib)** | **0** — clean |
| Unused (in bib, never cited) | 26 |

**Undefined = 0 is a genuine pass.** No dangling `\citep`. That is worth stating plainly
because it is the failure mode that most often survives to camera-ready.

The 26 unused entries are mostly harmless offline-RL background (IQL, CQL variants, MOPO,
MOReL, Decision Transformer, Diffuser). Four are not harmless:

### L1a — `lu2022revisiting` is uncited and is an N6 risk surface
Lu, Ball, Parker-Holder, Roberts, "Revisiting Design Choices in Offline Model-Based
Reinforcement Learning", ICLR 2022. A *revisiting-design-choices* paper in offline
*model-based* RL is the closest genre to a crossed decomposition in the closest sibling
field, and it sits in the paper's own bib unengaged. Dispatched for full-text check.
**If it crosses model class against policy-optimization with a decomposition, N6's scoping
needs to address it explicitly** — even if offline model-based RL is formally out of scope,
a reviewer who sees it in the bib and not in the text will ask why.

### L1b — `gao2022reward` is uncited, and carries a year defect
Key says `2022`; the entry's own `year` field says `2023` (ICML, PMLR 10909-10934). The key
and the field disagree inside a single entry. Independently of the year, this is the
sharpest available reframing of the paper's seventh elimination — a functional form for how
true value degrades as a learned proxy is optimized away from the data — and the paper has
it in the bibliography without citing it.

### L1c — `eriksson2019turbo` (TuRBO) is uncited
The paper credits Fan et al. 2024 with "the reading of a UCB-style acquisition as local
search". TuRBO, the canonical local-BO paper, is in the bib and uncited. Attribution
question dispatched.

### L1d — `fannjiang2020autofocused` is uncited
Autofocused Oracles is offline design's own paper on the surrogate being exploited as the
design distribution shifts — the paper's core diagnosis. Uncited.

**Pattern worth stating in the report:** the paper's bibliography contains at least three
papers that would *strengthen* it, uncited. That is the opposite of the usual bibliography
defect and is a cheap fix.

## L2 — Internal arithmetic consistency

Checked every derived figure I could recompute from the paper's own reported numbers.

### Confirmed consistent
| Claim | Check | Result |
|---|---|---|
| `5,040 optima = 7 tasks x 24 arms x 30 seeds` | 7x24x30 | **5,040** ✓ |
| `168 cells, 30 seeds` (elimination 7) | 7x24 | **168** ✓ consistent with above |
| `all 63 cells` (fig:x0) | 7x9 | **63** ✓ |
| `none of the 252 cells` (DB budget match) | 7x9x4 corners | **252** ✓ |
| `61%` of GP advantage survives at beta=0 | 0.319/0.525 | 0.6076 → **61%** ✓ |
| `99.1%` retained across width sweep | 0.476/0.480 | 0.9917 → **99.1%** ✓ |
| `11.8x` budget spread | 51,456/4,352 | 11.82 ✓ |
| K peaks at K=5 | max(0.326,0.366,0.408,0.389) | 0.408 at K=5 ✓ |
| budget intervals disjoint | 0.355 < 0.421 | ✓ genuinely disjoint |
| `10.7x` width sweep | 1024/96 | 10.67 ✓ |

### Discrepancies to resolve — candidate deliverable (i) items

**L2a — RESOLVED IN THE PAPER'S FAVOUR. The pessimism increment is correct as reported.**
I flagged that `0.525 - 0.319 = 0.206`, not the reported `0.203`. Checked against
`results/beta0_reconcile.json`: the artifact's `gap_delta_b2_minus_b0` is **0.20321**, i.e.
the paper reports the artifact's own paired bootstrap delta, not a subtraction of two point
estimates. Every adjacent figure also verifies exactly:

| Paper | Artifact | ✓ |
|---|---|---|
| beta=0 gap `0.319 [0.196,0.460]` | 0.31922, CI [0.19636, 0.45950] | ✓ |
| beta=2 gap `0.525 [0.406,0.614]` | 0.52519, CI [0.40641, 0.61389] | ✓ |
| increment `0.203 [0.007,0.396]`, `p=0.020` | 0.20321, [0.00716, 0.39552], p=0.0204 | ✓ |
| z-score cross-check `0.904` vs `1.473` | 0.90374, 1.47272 | ✓ |
| "the same 0.61 ratio" | 0.319/0.525 = 0.608; 0.904/1.473 = 0.614 | ✓ |
| Branin beta=0 `0.664` vs beta=2 `0.468` (supp.) | 0.66394, 0.46821 | ✓ |
| Griewank beta=0 `0.098` (supp.) | 0.09845 | ✓ |

**Residual, minor:** the point estimates and the paired delta sit in the same sentence, so a
reader who subtracts gets 0.206 and thinks they have caught an error. **Fix (one clause):
say the increment is a paired bootstrap delta, hence not the difference of the two
marginals.** This is a presentation fix, not a correctness fix.

**L2b — the width shrinkage does not equal the difference of the endpoints.**
Reported: `0.480` at w=96 against `0.476` at w=1024, difference **0.004**; but shrinkage is
reported as **`-0.006` [-0.210,0.161]**. Same class of issue — plausibly a bootstrap point
estimate over per-task pairs rather than the difference of two rounded marginals, but
unexplained on the page. **Fix: same one-clause reconciliation.**

**L2c — RESOLVED, and it is an UNDER-STATED result rather than a defect.**
`0.406` and `0.405` are not the same measurement reported twice. They are two independent
runs:

| | Source artifact | Seeds | eta2_surr |
|---|---|---|---|
| beta-sweep endpoint at beta=2 | `results/kbeta/kbeta_analysis.json` | 10 | **0.40636** |
| headline corner on/on (beta=2) | `results/bootstrap_eta_corners.json` | 30 | **0.40455** |

Same operating point, different seed counts, run separately — landing 0.0018 apart.

**That is a replication, and the paper does not say so.** As written, a reader assumes
0.405 and 0.406 are one number at two precisions; they are two estimates that agree.
**Fix, and it is a gain not a cost: state that the beta-sweep endpoint (10 seeds)
independently reproduces the headline corner (30 seeds) to within 0.002.** A paper whose
central scalar is challenged as an operating-point artifact should be advertising an
independent reproduction of it, not obscuring it.

All four corners verify exactly against the artifact, incidentally:

| Corner | Paper | Artifact point | Paper CI | Artifact CI |
|---|---|---|---|---|
| off/off | 0.367 | 0.36695 | [0.254,0.559] | [0.25405,0.55871] |
| on/off | 0.283 | 0.28279 | [0.186,0.444] | [0.18578,0.44396] |
| off/on | 0.450 | 0.45015 | [0.312,0.649] | [0.31163,0.64914] |
| on/on | **0.405** | 0.40455 | [0.290,0.556] | [0.28972,0.55606] |

Corner range 0.1674 → paper's "0.167" ✓. Interval widths 0.258-0.338 → paper's "0.26-0.34" ✓.
Uncorrected width 0.30466 → paper's "0.305" ✓. Common shared region computes to
[0.3116, **0.4440**]; the paper states [0.312, **0.443**] — a truncation rather than a round,
which understates the shared region slightly. Conservative, so harmless.

## L2.6 — A FREE ROBUSTNESS WIN THE PAPER IS LEAVING ON THE TABLE

`eta^2` is a **positively biased** estimator of variance explained at small n. The paper
reports point estimates at n=7 tasks and never addresses the bias. Its own bootstrap
artifacts contain the bias estimate, unreported: `mean(theta*) - theta_hat` is **positive in
all four corners**.

| Corner | point | bootstrap mean | est. bias | bias-corrected (2*pt - mean) |
|---|---|---|---|---|
| off/off | 0.3669 | 0.3830 | **+0.0160** | 0.3509 |
| on/off | 0.2828 | 0.3011 | **+0.0184** | 0.2644 |
| off/on | 0.4501 | 0.4624 | **+0.0123** | 0.4379 |
| on/on | 0.4045 | 0.4144 | **+0.0099** | 0.3946 |

The headline claim is "a published 0.367 rises to a corrected 0.405", a rise of **+0.0376**.
Under bootstrap bias correction it becomes **0.351 → 0.395, a rise of +0.0437**.

**The direction survives, and the effect gets LARGER.** This is the single cheapest
strengthening available to the paper: it costs one sentence and one supplementary row, it
pre-empts the most obvious statistical objection to reporting eta^2 at n=7, and it makes the
headline claim stronger rather than weaker. Whether the literature prefers omega^2/epsilon^2
here is out for verification (batch 9), but the bias direction is already established from
the paper's own artifacts.

**Tag: FOLD-INTO-THIS-PAPER / CHEAP.**

**L2d — `630` cells in the synthetic budget-matched arm.**
7 tasks x 9 cells = 63, so 630 implies 10 seeds, not the 30 used elsewhere. The supplement
says "Seeds: 30 synthetic, 16 Design-Bench, 10 for the beta/K/calibration sweeps." So 10
seeds is consistent with the sweep convention — but the budget-matched arm is presented in
the body as a main result, not a sweep. **Fix: state the seed count for the budget-matched
arm where it is reported, since it differs from the 30 the reader has been given.**

## L2.5 — The code-level traces VERIFY (a pass worth reporting)

The paper makes falsifiable line-number claims about its own scoring path. I checked them
against `code/mbo.py` (715 lines) in this repo. **All of them resolve to exactly what the
paper says they do.**

### Confound 1 — target scaling. Claimed trace: `mbo.py:34,157--162,181--187` against `mbo.py:293,379--381`
| Line | Actual content | Supports the claim? |
|---|---|---|
| 34 | `X1_STANDARDIZE_Y = os.environ.get('MBO_X1','1') != '0'` | ✓ the X1 switch |
| 157-162 | `if X1_STANDARDIZE_Y: ym, ys = y.mean(), y.std()+1e-8; y_fit = (y-ym)/ys` `else: ym, ys, y_fit = 0.0, 1.0, y` | ✓ ensemble trains on RAW y when X1 off |
| 181-187 | `m._ym, m._ys = ym, ys` … `def ens_scale(ms)` | ✓ the scale carried back |
| 293 | `normalize_y=True, alpha=1e-6` | ✓ GP standardizes (scikit-learn GP) |
| 379-381 | `ym, ys = yt.mean(), yt.std()+1e-8; yt = (yt-ym)/ys` | ✓ GP standardizes (torch GP) |

The asymmetry the confound alleges — ensemble on raw targets, both GPs on standardized —
is exactly what the code shows. **VERIFIED.**

Incidental corroboration: line 293 is a *scikit-learn* GP and 379-381 a *torch* GP, two
distinct GP implementations in one file. That independently supports the paper's separate
disclosure that "the premise-coverage value of 0.97 in the prior analysis belongs to a
scikit-learn exact GP, not the differentiable GP the grid scores."

### Confound 2 — candidate/oracle protocol. Claimed trace: `mbo.py:35--40,249--255,269--271`
Lines 35-40 are a source comment that states the defect in more detail than the paper does:
> "Pre-audit, grad returned the final iterate of all 2*TOP inits and perturb the per-slot
> best of 2*TOP, while cma returned top-TOP by surrogate LCB -- so grad/perturb spent 2x
> cma's ORACLE budget and eval_designs' oracle top-k made p50 a top-half median for two
> optimizers and a full-set median for the third. **Two estimands, one column.**"

Lines 249-255 and 269-271 are the matching `if not X3_MATCHED_PROTOCOL: return ...` branches
that implement the pre-audit behaviour. **VERIFIED**, and the paper's phrase "two estimands
in one column" is lifted from its own source comment, which is fair.

**Why this matters for the report.** The task is to critique every claim. Most of what an
adversarial audit produces is negative, which can leave the impression that nothing checks
out. Here the single most falsifiable class of claim in the paper — "this specific line of
code does this specific thing" — passes without exception. That is unusual and should be
stated, both because it is true and because it calibrates the severity of everything else:
the defects found elsewhere are framing and attribution defects, not fabricated evidence.

## L2.7 — The inversion result (D25) verifies, with one off-by-one

Checked `results/x0_inversion.json` (engine-stamped, `git_sha 9843dfc8`, X1/X3 both on) at
the audited engine `x3=1`.

**Verified exactly** — the figure caption's headline counts:

| Claim (fig:x0 caption) | Artifact | ✓ |
|---|---|---|
| ensemble inverts on ≥1 optimizer on **7/7** tasks | 7/7 (all seven) | ✓ |
| SVGP **3/7** | 3/7 (Branin, Rastrigin, Styblinski) | ✓ |
| exact GP **2/7** | 2/7 (Rastrigin, Styblinski) | ✓ |
| Branin-2D ens:grad — all 30 seeds invert | `inversion_rate: 1.0` | ✓ |
| …and every one of the 128 returned designs is worse | `mean_frac_worse: 1.0` | ✓ |

**L2.7a — DISCREPANCY: "five other cells tie it" should be six.**
The paper writes: "One of the sharpest cells is Branin-2D under ensemble gradient ascent
---**five** other ensemble and SVGP cells tie it---where all 30 seeds invert and, on average,
every one of the 128 returned designs scores below the best design the cell started with."

Applying that stated criterion (`inversion_rate == 1.0` AND `mean_frac_worse == 1.0`) at
x3=1 returns **seven** cells, i.e. Branin ens:grad plus **six** others:

| Task | Cell | mean magnitude |
|---|---|---|
| Branin-2D | ens:cma | 6.890 |
| Styblinski-5D | ens:cma | 22.312 |
| Styblinski-5D | ens:grad | 22.018 |
| Styblinski-5D | ens:perturb | 4.190 |
| Styblinski-5D | svgp:cma | 22.737 |
| Styblinski-5D | svgp:grad | 22.466 |

**Fix: recount and change "five" to "six", or state the additional criterion that excludes
the seventh cell.** Severity is low — the claim is a parenthetical and the direction is
unaffected — but it is a bare integer that a reviewer with the released artifact can check
in one line, and the paper's whole credibility posture rests on such checks passing. It is
also the only figure I found in the entire numeric sweep that does not reproduce.

**Note for the author:** the discrepancy may be a stale count from before a re-run. The
inversion artifact carries `git_sha 9843dfc8` while `beta0_reconcile.json` carries
`812bcb92` — different commits, as expected for different experiments, but worth confirming
the count was recomputed on the final one.

## L2.8 — The engine-stamping claim VERIFIES

The paper asserts as part of its protocol: "Stamp the engine---library versions, flags,
commit---with every number." Checked: `beta0_reconcile.json` and `x0_inversion.json` both
carry a `meta`/`engine` block with platform, OS release, Python, torch, numpy, botorch,
gpytorch and cma versions, `git_sha`, the X1/X3 flags, K, beta, TOP, seed range and an ISO
timestamp. **The protocol the paper prescribes is one it actually followed.** Worth stating
in the report — it is the claim most likely to be assumed rhetorical and it is not.

## L2.9 — The frozen-cell claims verify to the seed

These are the most striking factual claims in the Design-Bench section, and the ones most
exposed to a reviewer with the artifacts. **Every one reproduces exactly.**

### Ant (from `results/db_corners/corner_on_on_mujoco_db.json`, p100, 16 seeds)

The paper: *"On Ant, two of three GP cells return the bit-identical constant
`1.5287419557571411` with standard deviation exactly `0.0` across all sixteen seeds, and a
third (SVGP with perturbation) hits it on **ten of sixteen**."* And its own correction: *"It is
two of three Ant GP cells, not three---the gradient cell returns `1.3242 ± 0.1975` and is not
frozen."*

| Cell | Exact hits on 1.5287419557571411 | Distinct values | Verdict |
|---|---|---|---|
| `botorchgp:perturb` | **16/16** | 1 | frozen ✓ |
| `botorchgp:cma` | **16/16** | 1 | frozen ✓ |
| `botorchgp:grad` | 0/16 | 16 | **not** frozen ✓ — mean 1.32417, sd 0.198, matching the paper's `1.3242 ± 0.1975` |
| `svgp:perturb` | **10/16** | 5 | ✓ — the paper's "ten of sixteen" is exact |

**"Ten of sixteen" is exactly right.** That is a claim the authors could easily have rounded
or approximated, and did not.

### TF-Bind-8 (all four corners, p100, 16 seeds)

The paper: *"the three exact-GP cells return exactly `1.0` on all 16 seeds with zero variance
**in every corner**, and ensemble-with-perturbation joins them **in two of the four** — four
frozen cells of nine there, three in the others."*

| Corner | Frozen cells | Which |
|---|---|---|
| off/off | **4/9** | ens:perturb, botorchgp:grad, botorchgp:perturb, botorchgp:cma |
| off/on | **3/9** | the three exact-GP cells |
| on/off | **3/9** | the three exact-GP cells |
| on/on | **4/9** | ens:perturb + the three exact-GP cells |

All three exact-GP cells frozen at exactly 1.0 in **all four** corners ✓. `ens:perturb` joins
in **exactly two** of four ✓. Four-of-nine there, three elsewhere ✓.

## L2.10 — The pattern across all local verification, and what it means for the report

Every quantitative claim I could check against a repo artifact reproduced, with one
exception (L2.7a, "five other cells" should be six). That covers: four corner η² values and
their CIs, corner range, interval widths, the bootstrap-width validation, Elimination 1's
seven figures including the paired delta and the z-score cross-check, per-task β=0 gaps, the
inversion counts across three surrogate classes, both frozen-cell claims to the seed, the
`mbo.py` line traces for two confounds, and the engine-stamping protocol.

**This should be stated explicitly in the report, near the front.** An audit that returns nine
mandatory fixes reads, by default, as an indictment. The correct reading here is narrower and
more useful to the author: **the defects are concentrated almost entirely in citation
attribution and framing, and essentially absent from the evidence.** Of the nine mandatory
items, eight concern what a *source* says and one concerns an integer recount. None concerns a
number the paper computed.

That distinction is actionable. It says the remaining pre-deadline effort belongs in the
related-work and scoping prose, not in re-running anything.

## L2.11 — TOST verified, plus a numeric coincidence I could NOT resolve

**Verified from `docs/ARTIFACT_INVENTORY.md`**, which reports the released `stats.py` output:
> TOST bounds (`equivalence`): best `botorchgp:perturb` vs worst `ens:cma`; gap
> **0.3762254599365316**; ci90 **[−0.10776105394391278, 0.860211973816976]**; effect_bound
> **0.4839865138804444**; `equiv_margin_0p5 = false`, `equiv_margin_0p3 = false` —
> **equivalence NOT established at either margin.**

The supplement's entire treatment is one clause: *"Per-task Wilcoxon signed-rank tests with
Holm correction and paired TOST equivalence tests are computed by the released `stats.py`."*
**No bound, no interval, no verdict.** Fix already logged: report them, and cite Lakens (2017).

### The coincidence — flagged, NOT asserted as a finding

Two quantities in the paper sit within rounding of two TOST outputs, and they come from
different analyses:

| Paper's text | Value | Artifact quantity | Value |
|---|---|---|---|
| Elimination 3: *"the mean gap is still 0.375"* | 0.375 | TOST `gap` (Design-Bench, best vs worst cell) | 0.3762 |
| Elimination 3: *"loses the optimization comparison by roughly 0.48"* | 0.48 | TOST `effect_bound` (Design-Bench) | 0.4840 |

Elimination 3's figures are described as **synthetic-grid** quantities from the width/RMSE
analysis. The TOST figures are **Design-Bench** quantities from `results_db.json`. If the two
pairs are genuinely independent, this is a coincidence of two numbers to three significant
figures, which is possible but notable. If instead a Design-Bench TOST figure has been
transplanted into a synthetic-grid sentence, that is a real error in a load-bearing paragraph.

**I could not resolve this**, and I am not asserting it either way. Resolving it needs the
width-sweep artifact traced to the specific sentence, which I did not do. **It goes in the
terminal section as an open item for the author, phrased as a question rather than a finding**
— the author can settle it in one lookup, and an audit that has already caught two of its own
overstatements should not manufacture a third.

## L3 — Citation-year and venue defects visible without fetching

**L3a — `kim2025mbosurvey` key/prose mismatch.** The bib entry is
`@article{kim2025mbosurvey, ..., journal={arXiv preprint arXiv:2503.17286}, year={2025}}`.
The paper's prose calls it "the subfield's **2026** survey" — twice, and the second
contribution's framing leans on its recency. The prior audit records it as TMLR 2026
camera-ready. **Fix: if it is TMLR 2026, the bib entry must become an `@article` with the
TMLR journal and year 2026; if it is still a preprint, the prose must stop calling it a 2026
survey.** As written the paper contradicts itself between prose and bibliography. Dispatched
for venue confirmation.

**L3b — `gao2022reward` key/field mismatch.** See L1b. Key `2022`, field `2023`.

Both are the class of defect this project has caught before. Neither required a fetch.
