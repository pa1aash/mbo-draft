# Supplement engine fix: stamped regeneration of `tab:sfull` and `tab:cov`

Branch `supp-engine-fix`, off `origin/main` @ `bf8d8d2`.
**Data only. No `.tex` was edited in this pass** — the `.tex` edits happen in a controlled
Mac pass so they can be re-verified against this report.

---

## 1. Which corner, and why

**Decision: the uncorrected corner, X1 off / X3 off — regenerated so that it now carries a
full 19-field stamp and reproduces bit-exactly.**

This is the *second* branch of the brief ("if they must stay off_off for a stated reason").
The reason is stated, and it is load-bearing rather than decorative. `bf8d8d2` — the commit
titled *"Stage 2.5: post-fold re-audit + tab:sfull corner disclosure"* — had already
converted the corner from an undisclosed fact into a documented design choice:

- `supplement.tex:60` — *"Both tables are on the uncorrected engine … they are the grid as
  previously published, **retained so that the corrections in the body can be read against
  what they corrected**. Every number the body asserts is on the audited engine instead."*
- `supplement.tex:255` — *"Two of the tables predate the corrections and are retained
  deliberately---they are what the body's corrections corrected."*
- A new `\section{Engine Map for Every Supplementary Number}` (`sec:enginemap`,
  `supplement.tex:250–283`) pins **tab:srank, matched tuning, tab:cross, tab:cov and the
  synthetic Friedman** to tab:sfull's engine. Moving tab:sfull moves all of them.

Switching these tables to on_on would also **falsify a claim that is currently true**.
`supplement.tex:216` says OOD coverage is *"near zero exactly on the tasks where gradient
ascent collapses."* On the audited engine (`results/calibration_on_on.json`) Levy's `c_ood`
goes 0.11 → 1.00 and Griewank's 0.00 → 0.59, leaving no near-zero synthetic task but
Styblinski. The same move turns tab:cross's *"collapses on its own (0.41)"* into 0.57, which
is not a collapse. So on_on would destroy the contrast the body's corrections are read
against, and break three sentences to do it.

**What was actually missing was not the corner — it was the stamp**, exactly as the brief
diagnosed. That is what this pass fixes.

---

## 2. What was regenerated

| New artifact | Contents | Stamp |
|---|---|---|
| `results/supp_offoff/grid_offoff_b2.0.json` | tab:sfull: 7 tasks × **12 methods** (9 grid + COMs, CbAS, Grad.Asc.) × 30 seeds | 19/19, `X1=false X3=false`, β=2, K=5, `git_sha bf8d8d2` |
| `results/supp_offoff/calibration_off_off.json` | tab:cov synthetic block: 7 tasks × **30 seeds** | 19/19, `X1=false X3=false` |
| `results/supp_offoff/calibration_db_off_off.json` | tab:cov Design-Bench block: 7 tasks × 16 seeds | 19/19, `X1=false X3=false` (py3.9/torch2.8 DB stack) |
| `results/supp_offoff/_verify_branin.json` | reproduction gate (§3) | 19/19 |

Reproduced by `code/run_supp_offoff.sh` (synthetic) and `code/run_supp_offoff_db.sh` (DB).
Per-cell `_engine` sub-blocks are present on every variant node. The synthetic runs use
`envs/pod-synth`, whose versions match the incumbent stamp exactly; the DB run uses
`envs/miniforge/envs/dbm`, which matches the DB stamp exactly (these are deliberately two
different engines, as `results/db_corners/*` already records).

The worktree was **tracked-clean at `bf8d8d2`** during every run, so the `git_sha` field is
honest. (Note: the primary tree at `/workspace/MBO` is *not* — it has an unresolved merge, so
a run from there would stamp `def2b2d` against a tree that does not match it.)

### Why this was not just "point at the file that already exists"

`results/corners/pod_off_off.json` was already a stamped 30-seed off_off run — but it holds
**only the 9 grid cells**. The three domain-baseline rows of tab:sfull (COMs, CbAS,
Grad. Asc.) had **no stamped source at any corner**. They existed only inside the unstamped
`results_camera.json`. That gap is why a regeneration was needed rather than a repoint, and
it is the reason the `1.5%` disclosure could not simply be deleted before this pass.

---

### Verified against the repo's own gate

All four new files pass `run_all.load_checked()` / `require_meta()` — the loader assertion the
codebase uses to refuse unstamped provenance. The two files they replace **fail it**:

```
PASS  grid_offoff_b2.0.json / calibration_off_off.json / calibration_db_off_off.json / _verify_branin.json
FAIL  results_camera.json  -> "result file lacks a complete engine meta block (missing [...])"
FAIL  results_db.json      -> "result file lacks a complete engine meta block (missing [...])"
```

That is the whole fix in two lines: the tables' source data now passes the paper's own
reproducibility gate, where before it could not be loaded by the checked loader at all.

---

## 3. Reproduction gate

Re-running Branin-2D at off_off on `envs/pod-synth` reproduced `pod_off_off.json`
**9/9 cells bit-exact across all 30 per-seed values** (`maxabsdiff = 0.000e+00` on every
cell). The engine reproduces; the diffs in §4 are therefore real measurements, not drift.

The published `1.5%` disclosure was also verified before being acted on: max per-cell
relative deviation of `results_camera.json` against `pod_off_off.json` is **1.472%**
(`Ackley-20D / svgp:grad`, −0.6871 vs −0.6972). The claim is accurate and tight.

**Validation of the diff itself.** Before comparing, the OLD side was checked against the
table as actually printed in `supplement.tex`: **84/84 tab:sfull cells** and **12/12
tab:srank ranks** and **35/35 tab:cov entries** reproduce. The diffs below are trustworthy.

---

## 4. Per-cell diff — `tab:sfull`

`old` = `results_camera.json` (unstamped). `new` = `grid_offoff_b2.0.json` (stamped).
**50 of 84 cells are bit-exact**; the rest differ in the random stream, as the supplement
already predicted.

**Only 12 of 84 cells change at printed precision, and every change is ≤ 0.29:**

| Method | Task | printed now | stamped | Δ |
|---|---|---|---|---|
| Ens+Grad | Styblinski | 6.37 | **6.34** | −0.03 |
| Ens+Pert | Styblinski | 33.08 | **33.03** | −0.05 |
| Ens+CMA | Styblinski | 5.21 | **5.15** | −0.06 |
| SVGP+Grad | Ackley | −0.69 | **−0.70** | −0.01 |
| SVGP+Grad | Griewank | −2.11 | **−2.09** | +0.02 |
| SVGP+Pert | Styblinski | 34.35 | **34.31** | −0.04 |
| SVGP+CMA | Styblinski | 11.60 | **11.53** | −0.07 |
| SVGP+CMA | Rastrigin | −3.00 | **−2.99** | +0.01 |
| SVGP+CMA | Ackley | −0.73 | **−0.74** | −0.01 |
| SVGP+CMA | Griewank | −2.17 | **−2.15** | +0.02 |
| COMs | Styblinski | 8.50 | **8.21** | −0.29 |
| Grad. Asc. | Styblinski | 3.49 | **3.51** | +0.02 |

The other 72 cells are unchanged at printed precision. Styblinski-5D carries 6 of the 12
changes — consistent with it being the task with the largest seed-to-seed spread.

### Quantities that do NOT move

- **Bold / best-per-task: unchanged on all 7 tasks.** (GP+Grad ×4, GP+Pert, SVGP+Grad ×2.)
- **`tab:srank`: all 12 average ranks identical to 2 d.p.** (Δ = +0.00 for every method.)
  The rank table needs **no edit at all**.
- **Synthetic Friedman: `p = 6.086e-05` → `6.086e-05`**, best cell GP+Grad, mean rank 2.29 —
  identical. The `6.1×10⁻⁵`, the CD `4.54` and the mean rank `2.29` at `supplement.tex:246`
  all stand.
- **With baselines in the pool: `p = 3.458e-06` → `3.458e-06`** — identical, so
  `supplement.tex:246`'s "adding the domain baselines … leaves both conclusions unchanged"
  stands.

---

## 5. Per-cell diff — `tab:cov` (synthetic block)

> **RESOLVED — ships at 30 seeds (Option A2).** The synthetic block was run at 30 seeds on the
> stamped off_off engine and is now the shipped source: `results/supp_offoff/calibration_off_off.json`,
> 7 tasks × 30 seeds, 19-field stamp (`X1=false X3=false`, β=2, K=5, `git_sha bf8d8d2`),
> passes `run_all.load_checked()`. This matches what `enginemap` row 275 and the config
> paragraph (`supplement.tex:287`) already claim ("30 seeds each"); the 10-seed column below is
> retained only as the historical record of what was there before. Re-running the 30-seed
> calibration reproduced this file **bit-exactly** (91 cells × 30 seeds, max abs diff 0.000e+00).
>
> **Resolved answer for `supplement.tex:56`: `cf_ood == 0.00` on `N = four` of the fourteen
> tasks** (Superconductor, UTR, Ant, D'Kitty) at 30 seeds across the full synthetic + DB set.
> **"Spanning $0.00$ to $1.00$" holds** — `cf_ood` min = 0.0000, max = 1.0000 exactly.

The seed complication that forced this decision, for the record:

**The tab:cov synthetic block as previously printed was 10 seeds, not 30.** But `enginemap` row
(`supplement.tex:275`) says *30*, and the config paragraph (`supplement.tex:287`) says the
calibration measurement is *"also 30 seeds each."* **The paper already claims 30.** So the
previously printed table understated its own stated protocol; running at 30 pays that off.

I therefore ran 30 seeds and report **both** — `new10` is the seeds-0..9 prefix of the same
run, which isolates the engine/stream effect from the seed-count effect:

| Task | `c_in` old→10→30 | `c_ood` old→10→30 | `q̂` old→10→30 | `cf_in` old→10→30 | `cf_ood` old→10→30 |
|---|---|---|---|---|---|
| Branin | 0.71→0.71→0.71 | 0.42→0.42→**0.35** | 6.2→6.3→**6.6** | 0.91→0.91→**0.90** | 0.84→0.84→**0.77** |
| Styblinski | 0.64→0.64→**0.66** | 0.00→0.00→0.00 | 7.5→7.5→**7.2** | 0.90→0.89→0.90 | 0.00→0.00→**0.02** |
| Levy | 0.68→0.68→0.68 | 0.11→**0.12**→**0.10** | 6.0→6.0→6.0 | 0.90→0.90→0.90 | 0.28→**0.44**→**0.40** |
| Rosenbrock | 0.86→0.86→0.86 | 0.64→0.64→**0.69** | 2.5→**2.4**→2.5 | 0.90→0.90→0.90 | 0.66→0.66→**0.71** |
| Rastrigin | 0.73→0.73→0.73 | 0.72→**0.76**→**0.79** | 4.8→4.8→4.8 | 0.91→0.91→**0.90** | 0.77→**0.79**→**0.83** |
| Ackley | 0.92→0.92→0.92 | 1.00→1.00→1.00 | 1.8→1.8→**1.9** | 0.89→0.89→**0.90** | 1.00→1.00→1.00 |
| Griewank | 0.57→0.57→0.57 | 0.00→0.00→0.00 | 16.1→16.1→**15.9** | 0.90→0.90→0.90 | 0.00→0.00→**0.07** |

The `10` column (seeds-0..9 prefix of the same run) isolates the engine/stream effect from the
seed-count effect: at matched seed count **7 of 35 entries shift** vs the old print, all small
except Levy `cf_ood` 0.28 → 0.44 (Δ0.16). So the engine/stream move is minor; the larger
changes in the shipped `30` column are a **seed-count** effect, not an engine effect — which is
why the shipped decision was to run the full 30 the protocol already claims rather than relabel.

### The one claim that breaks: the "five of the fourteen" count

`supplement.tex:56`: *"…leaving out-of-distribution coverage erratic---spanning $0.00$ to
$1.00$ there, with exactly $0.00$ on **five of the fourteen** tasks."*

Counted across all 14 rows (synthetic + Design-Bench), `cf_ood == 0.00` at printed precision:

| reading | zeros / 14 | which |
|---|---|---|
| **old (as printed)** | **5** | Styblinski, Griewank, UTR, Ant, D'Kitty |
| new, A1 (synthetic at 10 seeds) | 6 | + Superconductor |
| **new, A2 — SHIPPED (synthetic at 30 seeds)** | **4** ✓ | Superconductor, UTR, Ant, D'Kitty |

**The count changed regardless of the seed decision, so this sentence had to be edited; the
shipped 30-seed answer is `four`.** Two independent causes:

- At 30 seeds the synthetic zeros disappear (Styblinski 0.00 → **0.02**, Griewank 0.00 →
  **0.07**).
- Independently, on the Design-Bench side **Superconductor's `cf_ood` moves 0.01 → 0.00**,
  adding a zero under *both* readings.

**"Spanning $0.00$ to $1.00$" survives intact.** Min is exactly 0.0000 and max exactly 1.0000
on all three readings — the Design-Bench zeros hold the floor even when the synthetic ones
lift. Only the *count* needs changing, not the span.

**The seed fork — resolved:**

- **Option A2 (30 seeds) — SHIPPED.** Makes `enginemap` row 275 and the config paragraph
  (`supplement.tex:287`, "30 seeds each") *true* rather than relabeling a 10-seed table as 30;
  count becomes **four of the fourteen**. This is the delivered `calibration_off_off.json`.
- Option A1 (10 seeds) — *not taken*. Would have left synthetic values essentially put but
  forced `enginemap` row 275 ("30") and `supplement.tex:287` ("30 seeds each") to be corrected
  down to 10; count would have been six of the fourteen.

The 30-seed synthetic values that ship (the `30` column of the table above), for the `.tex`
pass:

| Task | `c_in` | `c_ood` | `q̂` | `cf_in` | `cf_ood` |
|---|---|---|---|---|---|
| Branin | 0.71 | 0.35 | 6.6 | 0.90 | 0.77 |
| Styblinski | 0.66 | 0.00 | 7.2 | 0.90 | 0.02 |
| Levy | 0.68 | 0.10 | 6.0 | 0.90 | 0.40 |
| Rosenbrock | 0.86 | 0.69 | 2.5 | 0.90 | 0.71 |
| Rastrigin | 0.73 | 0.79 | 4.8 | 0.90 | 0.83 |
| Ackley | 0.92 | 1.00 | 1.9 | 0.90 | 1.00 |
| Griewank | 0.57 | 0.00 | 15.9 | 0.90 | 0.07 |

### Claims that survive

- *"near zero exactly on the tasks where gradient ascent collapses"* (`supplement.tex:216`) —
  `c_ood < 0.05` on **Styblinski and Griewank** both before and after. **Holds.** (This is the
  claim that would have been falsified by a move to on_on.)
- *"Conformal restores in-distribution coverage to its 0.90 target on every task"* — `cf_in`
  spans 0.90–0.90 after regeneration. **Holds, and tightens.**

---

## 5b. Per-cell diff — `tab:cov` (Design-Bench block)

`old` = `results_db.json` (unstamped; **also off_off** — it sits 2.9% from
`corner_off_off_db.json` with 18 cells exact, not near any audited file).
`new` = `calibration_db_off_off.json`, 16 seeds, 19-field stamp, on the py3.9/torch2.8 DB
stack whose 8 version fields match the incumbent `db_corners` stamp exactly.

Validation: **35/35 entries of the printed DB block reproduce** from `results_db.json`.

| Task | `c_in` | `c_ood` | `q̂` | `cf_in` | `cf_ood` |
|---|---|---|---|---|---|
| TF-Bind-8 | 0.92 | 0.71 | 1.7 | 0.90 | 0.70 |
| TF-Bind-10 | 1.00 | 0.53→**0.51** | −1.6 | 0.89 | 0.45→**0.44** |
| Superconductor | 1.00 | 0.01 | −2.0→**−2.1** | 0.90 | 0.01→**0.00** |
| GFP | 0.00 | 0.00 | 88.4→**67.4** | 0.90 | 0.99→**1.00** |
| UTR | 1.00 | 0.00 | −2.5→**−2.6** | 0.91 | 0.00 |
| Ant | 0.94→**0.96** | 0.00 | 1.2→**0.9** | 0.90 | 0.00 |
| D'Kitty | 0.51→**0.53** | 0.00 | 8.0→**7.7** | 0.90 | 0.00 |

**11 of 35 entries change at printed precision.** Two are worth calling out:

- **GFP `q̂` 88.4 → 67.4** is by far the largest single move in either table. It does not
  threaten a claim: `supplement.tex:216` already declares GFP *"degenerate --- coverage is
  measured on relaxed logits and is a decode artifact rather than a calibration signal,"* and
  a wildly unstable conformal multiplier is exactly what that sentence predicts. But it is a
  printed number and must be updated.
- **Superconductor `cf_ood` 0.01 → 0.00** is what shifts the "five of the fourteen" count
  under both seed options (§5).

Claims that hold: the negative-`q̂` set is unchanged (TF-Bind-10, Superconductor, UTR), so
`supplement.tex:216`'s *"on several real tasks above nominal … giving negative $\hat q$"*
stands.

---

## 6. Knock-on: `tab:cross`

Not in the brief, but it is mechanically coupled and would otherwise be missed. The ensemble
row's first two cells are **column means of tab:cov's synthetic block**, so regenerating
tab:cov moves them:

| tab:cross cell | printed | new (10 seeds) | new (30 seeds) |
|---|---|---|---|
| Ensemble, in-distribution | 0.73 | 0.729 | **0.7325** |
| Ensemble, own proposals | 0.41 | **0.4199** | **0.4180** |

The in-distribution cell still rounds to **0.73** and needs no edit. The own-proposals cell
**rounds to 0.42 on both new readings**, so `0.41` needs a one-digit edit. The narrative
("holds in-distribution, collapses on its own") is unaffected — 0.42 is still a collapse.

Two pre-existing problems with tab:cross, surfaced while tracing it and **not** created by
this pass:

1. Its **GP row is a scikit-learn GP artifact** (`results/gpcov.json`: 0.9838 / 0.9688 /
   0.9369), which has no X1/X3 corner at all. `enginemap` row 270 labels the whole table
   "uncorrected / 30"; that is wrong for the GP row (engine-free) and for the ensemble row
   (10-seed, not 30).
2. The ensemble row's **third cell (`0.97`) could not be reconciled with any artifact** in
   `results/`. The nearest candidate, `gpcov.json`'s `ens_on_gp`, has mean **0.1429** (six of
   seven tasks at 0.0). This is a standing liability independent of the regeneration and
   should be chased down separately.

---

## 7. Cross-references that must change

### MUST EDIT

| # | Location | Change |
|---|---|---|
| 1 | `supplement.tex:66–80` (**tab:sfull** body) | 12 cell values per §4. |
| 2 | `supplement.tex:172` (**tab:cross**) | ensemble "own proposals" `0.41` → `0.42`. |
| 3 | `supplement.tex:116`, `:118` | restated `0.41` → `0.42` (twice at `:118`). |
| 4 | `supplement.tex:283` (**provenance paragraph**) | Now obsolete as written — see §8. |
| 5 | `supplement.tex:275` (`enginemap` tab:cov row) | Seed count "30" is now **correct** — source is the shipped 30-seed `calibration_off_off.json`. No edit. |
| 6 | `supplement.tex:56` | "exactly 0.00 on **five** of the fourteen tasks" → **four** (resolved, 30 seeds; §5). The "spanning 0.00 to 1.00" clause is correct as-is — leave it. |
| 7 | **tab:cov synthetic rows** `supplement.tex:176–182` | Set to the shipped 30-seed values in the §5 table. |
| 8 | **tab:cov Design-Bench rows** `supplement.tex:184–190` | 11 entries per §5b, incl. GFP `q̂` 88.4→67.4. Required under **both** options. |

### MUST RE-VERIFY (recompute; expected to hold)

| # | Location | Note |
|---|---|---|
| 8 | `supplement.tex:130` (tab:simple off/off row `0.004 / 0.666 / 0.814`) | Same off_off per-seed grid. |
| 9 | `main.tex:159` (tab:corners off/off row `0.367 / 0.013 / 0.165 / 6.1e-5`) | Legitimately off_off; must stay numerically consistent with whichever file tab:sfull cites. |
| 10 | `main.tex:183–185` (tab:normrob off/off rows) | "recomputed from the stored per-seed grids". |
| 11 | `supplement.tex:159` + `main.tex:284` (ε² bias, first entry of each list) | off_off corner entry only. |
| 12 | `main.tex:95/97/115/116` (`0.367` baseline) | The off_off η² baseline. |
| 13 | `supplement.tex:105` (matched tuning `0.37`/`0.28`) | `:105` already narrows this to a **ratio** claim, so it should survive a level shift. |

### CONFIRMED NO CHANGE — do not touch

- **`tab:srank`** (`supplement.tex:88–101`) — all 12 ranks identical. Despite `:87` deriving it
  from tab:sfull, it needs no edit.
- **Friedman block** (`supplement.tex:246`) — `6.1×10⁻⁵`, CD `4.54`, mean rank `2.29`, and the
  four-corner list all unchanged; "adding the domain baselines … unchanged" verified.
- **Bold markers** in tab:sfull — best-per-task unchanged on all 7 tasks.
- `main.tex:240`, `:242`, `supplement.tex:141–154` (**tab:rawgap**) — audited engine.
- `main.tex:258` — `0.831`, `0.38`, `0.010`, `0.117` come from `coverage33.json`; `0.97` from
  `gpcov.json` (sklearn GP). Neither is tab:cov's file.
- `main.tex:242`'s `35.9` is the **audited** Styblinski value, deliberately *not* tab:sfull's
  `36.15`. **Do not "fix" it to match.**
- **tab:cov Design-Bench rows** — regenerated at off_off/16 seeds; see the companion diff.

### RESOLVED — previously flagged as at-risk

`main.tex:210` and `main.tex:225` both claim bit-exact reproduction of *"the incumbent grid."*
These trace to `width_grid.json` and `phantom_maxima.json`, **both stamped `X1=true X3=true`**
— audited-engine artifacts. An off_off regeneration cannot touch them.

---

## 8. The provenance paragraph is now obsolete

`supplement.tex:283` currently reads:

> *"The uncorrected grid is read from a stored results file that predates the engine-stamping
> protocol … it carries no stamp of its own; it reproduces the separately stamped
> X1-off/X3-off run to within 1.5% on every cell rather than bit-exactly … Every
> audited-engine artifact in this paper carries the full 19-field stamp."*

After this pass **there is no unstamped file in the pipeline**: tab:sfull, tab:srank and
tab:cov all read from 19-field-stamped artifacts that reproduce bit-exactly. The paragraph
should be replaced with a statement that the uncorrected grid is *also* fully stamped — which
is strictly stronger, and removes the paper's last self-declared reproducibility gap.

Note the final sentence is scoped to *audited-engine* artifacts, and its implicature ("only
audited artifacts are stamped") was **already** false before this pass — `pod_off_off.json`
carried the identical 19-field stamp while being off_off. The replacement should drop that
asymmetry rather than restate it.

---

## 9. Out of scope — flagged, not acted on

1. **`main.tex:210` width claim looks over-stated.** It says `w=96` *"reproduces the incumbent
   grid bit-exactly for the gradient and CMA cells on all seven tasks."* Measured at seed 0,
   `ens_w96` matches `grid_b2.0.json` on **4 of 7 tasks** (Levy, Rosenbrock, Ackley, Griewank
   exact; Branin, Styblinski, Rastrigin differ) and `corner_on_on.json` on 0/7. The phrase
   "incumbent grid" is ambiguous between those two files, so this may be a wording problem
   rather than a data problem — but it needs an owner. **Audited-engine claim, untouched by
   this pass.**
2. **`cbas` mixes standardized and raw targets under X1.** It reads raw member output
   (`mbo.py:601`, z-space) and concatenates it with raw-unit `y` (`mbo.py:603`) with no
   inverse map, where `run_calibration` explicitly guards this via `ens_moments_raw`
   (`mbo.py:665–671`). Affects the CbAS row in the X1-on corners. Pre-existing.
3. **`results_db.json` is off_off**, closest to `corner_off_off_db.json` (2.9% mean, 18 cells
   exact). `enginemap` row 277 labels Design-Bench "audited"; that is right for the body's DB
   results (`corner_on_on_db.json`) but not for the file tab:cov's DB rows come from. The row
   conflates two different DB artifacts.
4. **The primary tree has an unresolved merge.** `/workspace/MBO` sits mid-merge
   (`MERGE_HEAD 86ed91e`, live conflict markers in `docs/PREREGISTRATION_V3.md`) with
   farfield-v2 work staged. That work is safe on `origin/mechanism-farfield-v2`. This pass
   used a separate worktree and left the merge untouched; it still needs finishing.
