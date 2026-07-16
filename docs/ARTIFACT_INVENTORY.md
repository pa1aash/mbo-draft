# Experimental Artifact Inventory — /Users/palaash/Downloads/MBO/results/

Audit date: 2026-07-17. All JSONs parsed successfully with system `python3` stdlib `json`.
**No file was corrupt or unreadable.**

---

## 0. Headline verdicts (detail below)

| Question | Answer |
|---|---|
| Primary artifact (synthetic) | `results/results_camera.json` |
| Primary artifact (Design-Bench) | `results/results_db.json` |
| Are the gitignored files the primary artifacts? | **YES** — proven by code path + numeric match to `main.tex` |
| Full 3x3 grid complete? | **YES** — 9/9 cells x 14 tasks, no missing/under-seeded grid cells |
| Seeds | 30 (synthetic mbo), 16 (Design-Bench), 10 (calibration/beta/K/enssub sweeps) |
| Tasks | 7 synthetic + 7 Design-Bench = **14 distinct, zero overlap** |
| Timestamp / git sha / config block in any record? | **MISSING — none of the 18 artifacts carries any provenance metadata** |

---

## 1. Global schema

All grid-bearing files share one shape (depth 5):

```
{ <block>: { <task>: { <cell>: { "p100"|"p50": { "mean": float,
                                                 "std":  float,
                                                 "all":  [float, ...]  # one entry per seed
                                               } } } } }
```

Example leaf record — `results_camera.json` `/mbo/Branin-2D/ens:perturb/p100`:

| key | type | sample value |
|---|---|---|
| `mean` | float | `-0.7798330307006835` |
| `std` | float | `0.2984145691205014` |
| `all` | list[30] | `[-0.9686107635498047, -0.8322124481201172, ...]` |

**Cell naming.** Grid cells are `<surrogate>:<optimizer>` — surrogates `{ens, botorchgp, svgp}` x optimizers `{perturb, grad, cma}` = the 9-cell 3x3 grid. Non-grid entries (`coms`, `cbas`, `gp`, `grad_ascent`, `sparse_gp`, `ens_conformal:grad`, `ens_conformal:perturb`) are external/reference baselines.

**Seed values.** There is **no explicit seed field anywhere**. `code/run_all.py:79` generates `for s in range(seeds)`, so seed values are **0..N-1**, carried only *positionally* in the `all` arrays. Distinct-seed count is therefore `len(all)`; seed identity is implicit and unverifiable from the artifacts alone.

**Provenance.** A regex scan for `timestamp|git|sha|commit|config|date|host|meta|version|runtime|args` across every file returned **no metadata keys** in any artifact (the single hit, `per_seed` in `results_new.json`, is data, not metadata). **All 18 artifacts are provenance-free.**

---

## 2. Per-file inventory

### 2.1 `results_camera.json` — PRIMARY (synthetic)
- **Size / mtime:** 392,577 B | Jul 15 13:13:23 2026 (**2nd-newest grid file**)
- **Top-level:** dict[6] = `mbo`, `calibration`, `beta`, `K`, `mbo_beta0`, `mbo_enssub`
- **Tasks (7):** Branin-2D, Styblinski-5D, Levy-8D, Rosenbrock-10D, Rastrigin-15D, Ackley-20D, Griewank-30D
- **Cells (16):** all 9 grid cells + `cbas`, `coms`, `gp`, `grad_ascent`, `sparse_gp`, `ens_conformal:grad`, `ens_conformal:perturb`
- **Seeds:** `mbo` = **30** in all 7x16 = 112 cells (uniform, zero exceptions). `mbo_beta0` = 30. `calibration`/`beta`/`K`/`mbo_enssub` = **10**.
- **Coverage data:** YES — `calibration/<task>/_` , 12 keys: `rho_err`, `q_conformal`, `cov_conf_indist`, `cov_conf_ood`, `cov_indist@{0.5,1.0,2.0,5.0}`, `cov_ood@{0.5,1.0,2.0,5.0}`. Task-level (cell key is the placeholder `_`), **not per-grid-cell**, 10 seeds each.
- **Sweep axes:** `beta` ∈ {0.0, 0.5, 1.0, 2.0, 5.0} (p100 only); `K` ∈ {2, 3, 5, 10} (p100 only); `mbo_beta0` = 9 grid cells re-run at β=0; `mbo_enssub` = 3 ens cells on GP's data subsample.
- **Provenance:** MISSING

### 2.2 `results_db.json` — PRIMARY (Design-Bench)
- **Size / mtime:** 141,335 B | Jul 15 05:25:48 2026
- **Top-level:** dict[2] = `mbo`, `calibration`
- **Tasks (7):** TFBind8, TFBind10, Superconductor, GFP, UTR, AntMorphology, DKitty
- **Cells (15):** 9 grid + `cbas`, `coms`, `gp`, `grad_ascent`, `ens_conformal:grad`, `ens_conformal:perturb`. **No `sparse_gp`** (fails-and-skips on DB per commit `ff25b6a`).
- **Seeds:** **16** across all 9 grid cells x 7 tasks. Three **baseline** gaps: `Superconductor/gp` = 7, `Superconductor/grad_ascent` = 14, `GFP/gp` = **MISSING**.
- **Coverage data:** YES — same 12-key `calibration/<task>/_` schema, **16 seeds**.
- **Sweep axes:** none (no beta/K blocks on DB).
- **Provenance:** MISSING

### 2.3 `results_camera_matched.json` — GATE-1 control (synthetic)
- **Size / mtime:** 205,105 B | Jul 14 00:14:15 2026
- **Top-level:** dict[1] = `mbo` only. Same 7 tasks, same 16 cells, **30 seeds, 100% uniform**.
- Matched-tuning arm (GP given the ensemble's zero tuning budget). No coverage, no sweeps, no provenance.

### 2.4 `results_db_matched.json` — GATE-1 control (Design-Bench)
- **Size / mtime:** 108,137 B | Jul 14 00:38:07 2026
- **Top-level:** dict[1] = `mbo`. 7 DB tasks, 15 cells, **16 seeds, 100% uniform** — note this file has *no* gaps: it fills `Superconductor/gp` (16 vs live 7), `Superconductor/grad_ascent` (16 vs 14), and `GFP/gp` (16 vs MISSING).
- No coverage, no sweeps, no provenance.

### 2.5 `results_db.preserved.json` — partial DB snapshot
- **Size / mtime:** 43,417 B | Jul 14 00:14:15 2026
- **Top-level:** dict[1] = `mbo`. Only **3 tasks** (TFBind8, TFBind10, Superconductor), 15 cells, 16 seeds each.
- Rescue copy of the 3 completed DB tasks. **Superseded** by `results_db.json` (7 tasks). Notably it holds `Superconductor/gp` at 16 seeds where the live file has 7.

### 2.6 `results_gradtune.json` — optimizer-tuning robustness
- **Size / mtime:** 10,553 B | Jul 14 00:14:22 2026
- **Schema:** `{ task: { variant: list[15] } }` — flat lists, **not** the mean/std/all shape.
- **Tasks (4):** Branin-2D, Styblinski-5D, Rosenbrock-10D, Ackley-20D
- **Variants (7):** `perturb`, `grad_default`, `grad_gentle`, `grad_long`, `grad_norm`, `grad_trust`, `grad_besttuned`
- **Seeds:** 15. No coverage. No provenance. Backs the "under-tuned optimizer" rebuttal (commit `cdd5ad8`).

### 2.7 `05_findings.json` — DERIVED analysis digest
- **Size / mtime:** 11,454 B | Jul 15 16:11:39 2026 — **NEWEST artifact in the directory**
- **Top-level:** dict[14] = `attribution`, `gate1`, `stats`, `equivalence`, `calibration`, `beta_sweep`, `crosscheck`, `K_ablation`, `beta0`, `subsample_control`, `gp_coverage`, `stats_9cell`, `bootstrap_ci`, `rf_robustness`
- **Not a raw artifact** — `code/run05.py:52-53,63-64,88,124,146,171,189` computes every value from `results_camera.json`, `results_camera_matched.json`, `results_db.json`, `official_baselines.json`. This is the file the paper quotes.
- Provenance: MISSING

### 2.8 `gpcov.json` — cross-proposal coverage
- **Size / mtime:** 3,072 B | Jul 15 12:54:31 2026
- **Schema:** `{ task: { metric: {mean, std} } }` — 7 synthetic tasks x 6 metrics (`gp_indist`, `gp_own`, `ens_indist`, `ens_own`, `ens_on_gp`, `gp_on_ens`). No `all` array, so **seed count is not recoverable from this file**.
- Written by `code/run_gpcov.py:64`; consumed by `code/figures.py:401` (fig8_crossproposal). Mirrored into `05_findings.json['gp_coverage']`.

### 2.9 `official_baselines.json` — external reference numbers
- **Size / mtime:** 2,414 B | Jul 14 21:04:09 2026
- **Schema:** `{ method: { task: { "p100": {mean, std, all, n} } } }` — the only file carrying an explicit `n` field.
- **Methods (2):** `coms_official`, `cbas_official`. **Tasks (3):** Superconductor, TFBind8, GFP. **Seeds: 8.**
- Raw values in §7. Companion tarball `official_baselines_raw.tgz` (190,924 B, Jul 14 21:04:16 2026) — raw upstream dump, not parsed here.

### 2.10 Legacy / superseded files (all git-tracked)

| File | Size | mtime | Top-level | Verdict |
|---|---|---|---|---|
| `results.json` | 33,638 | Jul 10 02:42:09 2026 | `mbo`, `o2o`, `rl`, `abl` | **Oldest.** Pre-grid schema (`p100_m`/`p100_s`, cells `lcb`/`coms`/`grad_ascent`). No 3x3 grid. Superseded. |
| `results_final.json` | 9,085 | Jul 14 00:14:21 2026 | `botorch_gp`, `rank_surrogate`, `temp_calibration`, `o2o_extra`, `bootstrap_ranks`, `profiling`, `pen_sensitivity` | Side-experiment grab-bag. No grid. Superseded. |
| `results_new.json` | 14,743 | Jul 14 00:14:23 2026 | `gp_lcb`, `K_ablation`, `beta_counter`, `calibration`, `o2o_diversity` | Old K/beta ablations + old calibration (`rho_sigma_error`/`rho_sigma_knn` schema). Superseded. |
| `results_revision.json` | 64,630 | Jul 14 00:14:25 2026 | `mbo`, `o2o` | Pre-grid revision run; cells `lcb`/`coms`/`grad_ascent`/`lcb_perturb`/`sparse_gp`/`cbas`. `code/mbo.py:18` names it the canonical *config* reference, but its *data* is superseded. |

`code/run05.py:201` reads all four only for a legacy cross-check block.

---

## 3. CROSS-FILE ANALYSIS

### 3.1 Which file is the paper's PRIMARY source?

**Ranked by recency + completeness:**

| Rank | File | mtime | Grid | Tasks x seeds | Role |
|---|---|---|---|---|---|
| 1 | **`results_camera.json`** | Jul 15 13:13 | 9/9 | 7 x 30 | **PRIMARY — synthetic** |
| 2 | **`results_db.json`** | Jul 15 05:25 | 9/9 | 7 x 16 | **PRIMARY — Design-Bench** |
| 3 | `05_findings.json` | Jul 15 16:11 | derived | — | Newest, but a *derivative* of #1/#2 |
| 4 | `results_camera_matched.json` | Jul 14 00:14 | 9/9 | 7 x 30 | GATE-1 control arm |
| 5 | `results_db_matched.json` | Jul 14 00:38 | 9/9 | 7 x 16 | GATE-1 control arm |
| 6 | `gpcov.json` | Jul 15 12:54 | — | 7 | Fig-8 input |
| 7 | `official_baselines.json` | Jul 14 21:04 | — | 3 x 8 | External cross-check |
| 8 | `results_gradtune.json` | Jul 14 00:14 | — | 4 x 15 | Robustness arm |
| 9 | `results_db.preserved.json` | Jul 14 00:14 | 9/9 | 3 x 16 | Partial, superseded |
| 10-13 | `results_revision/new/final/.json` | Jul 10-14 | none | — | Legacy, pre-grid |

**Evidence — the code path.** Every paper-output generator hardcodes the two gitignored files:

- `code/figures.py:26-27` → `CAM = .../results_camera.json`, `DB = .../results_db.json` — produces `paper/figures_v2/*`
- `code/tables.py:12` → `CAM = .../results_camera.json` — produces `paper/tables_v2/*`
- `code/stats.py:19` → `OUT = .../results_camera.json`
- `code/analysis.py:20` → `DEFAULT = .../results_camera.json`
- `code/run05.py:52-53` → writes `05_findings.json` from `results_camera.json` + `results_db.json`

No paper-facing script reads any git-tracked results file except for the legacy cross-check at `run05.py:201`.

### 3.2 GRID COMPLETENESS MATRIX

**`results_camera.json` — synthetic (seed counts per cell):**

| surrogate x optimizer | Branin-2D | Styblinski-5D | Levy-8D | Rosenbrock-10D | Rastrigin-15D | Ackley-20D | Griewank-30D |
|---|---|---|---|---|---|---|---|
| ens:perturb | 30 | 30 | 30 | 30 | 30 | 30 | 30 |
| ens:grad | 30 | 30 | 30 | 30 | 30 | 30 | 30 |
| ens:cma | 30 | 30 | 30 | 30 | 30 | 30 | 30 |
| botorchgp:perturb | 30 | 30 | 30 | 30 | 30 | 30 | 30 |
| botorchgp:grad | 30 | 30 | 30 | 30 | 30 | 30 | 30 |
| botorchgp:cma | 30 | 30 | 30 | 30 | 30 | 30 | 30 |
| svgp:perturb | 30 | 30 | 30 | 30 | 30 | 30 | 30 |
| svgp:grad | 30 | 30 | 30 | 30 | 30 | 30 | 30 |
| svgp:cma | 30 | 30 | 30 | 30 | 30 | 30 | 30 |
| *cbas* (baseline) | 30 | 30 | 30 | 30 | 30 | 30 | 30 |
| *coms* (baseline) | 30 | 30 | 30 | 30 | 30 | 30 | 30 |
| *gp* (baseline) | 30 | 30 | 30 | 30 | 30 | 30 | 30 |
| *grad_ascent* (baseline) | 30 | 30 | 30 | 30 | 30 | 30 | 30 |
| *sparse_gp* (baseline) | 30 | 30 | 30 | 30 | 30 | 30 | 30 |
| *ens_conformal:grad* | 30 | 30 | 30 | 30 | 30 | 30 | 30 |
| *ens_conformal:perturb* | 30 | 30 | 30 | 30 | 30 | 30 | 30 |

**COMPLETE — 112/112 cells at exactly 30 seeds. Zero missing, zero under-seeded.**

**`results_db.json` — Design-Bench (seed counts per cell):**

| surrogate x optimizer | TFBind8 | TFBind10 | Superconductor | GFP | UTR | AntMorphology | DKitty |
|---|---|---|---|---|---|---|---|
| ens:perturb | 16 | 16 | 16 | 16 | 16 | 16 | 16 |
| ens:grad | 16 | 16 | 16 | 16 | 16 | 16 | 16 |
| ens:cma | 16 | 16 | 16 | 16 | 16 | 16 | 16 |
| botorchgp:perturb | 16 | 16 | 16 | 16 | 16 | 16 | 16 |
| botorchgp:grad | 16 | 16 | 16 | 16 | 16 | 16 | 16 |
| botorchgp:cma | 16 | 16 | 16 | 16 | 16 | 16 | 16 |
| svgp:perturb | 16 | 16 | 16 | 16 | 16 | 16 | 16 |
| svgp:grad | 16 | 16 | 16 | 16 | 16 | 16 | 16 |
| svgp:cma | 16 | 16 | 16 | 16 | 16 | 16 | 16 |
| *cbas* (baseline) | 16 | 16 | 16 | 16 | 16 | 16 | 16 |
| *coms* (baseline) | 16 | 16 | 16 | 16 | 16 | 16 | 16 |
| *gp* (baseline) | 16 | 16 | **7** | **MISSING** | 16 | 16 | 16 |
| *grad_ascent* (baseline) | 16 | 16 | **14** | 16 | 16 | 16 | 16 |
| *ens_conformal:grad* | 16 | 16 | 16 | 16 | 16 | 16 | 16 |
| *ens_conformal:perturb* | 16 | 16 | 16 | 16 | 16 | 16 | 16 |
| *sparse_gp* | **MISSING (all)** | | | | | | |

**9x9 grid COMPLETE — 63/63 grid cells at exactly 16 seeds.**

**Defects, all confined to non-grid baselines:**
1. `Superconductor/gp` = **7/16 seeds** (56% short)
2. `Superconductor/grad_ascent` = **14/16 seeds** (2 short)
3. `GFP/gp` = **MISSING entirely**
4. `sparse_gp` absent on all 7 DB tasks (documented: fails-and-skips, commit `ff25b6a`)

Consequence: `05_findings.json['stats']['REAL']['methods']` lists 14 methods vs SYNTH's 16 — `gp` and `sparse_gp` are dropped from the real-task Friedman/Nemenyi family. Defects 1-3 do **not** touch the 3x3 attribution or the 9-cell stats. `results_db_matched.json` and `results_db.preserved.json` both hold complete 16-seed data for `Superconductor/gp` and `GFP/gp` — the gaps are recoverable.

### 3.3 Do camera + db together cover 14 tasks?

**YES — exactly 14, with zero overlap.**

| # | Task | Source |
|---|---|---|
| 1 | Branin-2D | camera |
| 2 | Styblinski-5D | camera |
| 3 | Levy-8D | camera |
| 4 | Rosenbrock-10D | camera |
| 5 | Rastrigin-15D | camera |
| 6 | Ackley-20D | camera |
| 7 | Griewank-30D | camera |
| 8 | TFBind8 | db |
| 9 | TFBind10 | db |
| 10 | Superconductor | db |
| 11 | GFP | db |
| 12 | UTR | db |
| 13 | AntMorphology | db |
| 14 | DKitty | db |

`set(camera) & set(db) = ∅`. Matches `main.tex`: "7 synthetic and 7 Design-Bench tasks".

### 3.4 Seed count per task — is it 30 synthetic / 16 Design-Bench?

**Verified empirically: YES for the main `mbo` grid — but the sweep/calibration arms run at 10.**

| Block | File | Seeds | Uniform? |
|---|---|---|---|
| `mbo` (the 3x3 grid + baselines) | results_camera.json | **30** | Yes, 112/112 cells |
| `mbo_beta0` | results_camera.json | **30** | Yes, 63/63 |
| `calibration` | results_camera.json | **10** | Yes, 7/7 tasks |
| `beta` sweep | results_camera.json | **10** | Yes |
| `K` sweep | results_camera.json | **10** | Yes |
| `mbo_enssub` | results_camera.json | **10** | Yes |
| `mbo` | results_db.json | **16** | Yes on all 9 grid cells; 3 baseline exceptions (§3.2) |
| `calibration` | results_db.json | **16** | Yes, 7/7 tasks |
| `mbo` | results_gradtune.json | **15** | Yes |
| `p100` | official_baselines.json | **8** | Yes |

**Caveat worth flagging to the audit.** The synthetic **calibration** numbers the abstract quotes (0.73 in-distribution, 0.41 own-proposal, 0.97 on GP proposals) rest on **10 seeds, not 30**. The two-sided `.bak` held 30 calibration seeds; the live one-sided rerun dropped to 10. The paper does not state a calibration seed count, so nothing is misreported — but the coverage claims are 3x less-seeded than the grid claims that surround them.

### 3.5 `.bak` diffs (schema/aggregate level)

**`results_camera.json` vs `results_camera.json.twosided.bak`** (284,070 B, Jul 15 03:15:10):

- Blocks added in live: `mbo_beta0`, `mbo_enssub`. Nothing removed.
- Grid cells: **175 shared, 0 changed.** Every `(n, mean)` pair is bit-identical. **The `mbo` performance data was NOT touched.**
- `calibration`: key `rho_knn` **removed**; **all 12 remaining keys changed value**; seed count **30 → 10**.
  - e.g. Branin-2D `rho_err`: `0.23415883103532412` (bak, n=30) → `0.19934121656486625` (live, n=10)

**`results_db.json` vs `results_db.json.twosided.bak`** (138,515 B, Jul 15 05:25:29):

- Top-level keys identical. Grid cells: **104 shared, 0 changed.**
- `calibration`: `rho_knn` removed; 8 of 12 shared keys changed; seed count **stays 16**.
  - e.g. AntMorphology `rho_err`: `0.33457144228576907` → `0.33774184296737186`

**What the two-sided → one-sided switch actually was.** The filename is accurate but its scope is narrow: the change is **confined entirely to the calibration/coverage block; not one optimization result moved.** `code/mbo.py:364-368` defines the new estimator:

```python
def coverage_of_premise(mu, sigma, f, beta):
    """Empirical P(mu - f <= beta*sigma) = P(f >= mu - beta*sigma) — the ONE-SIDED
    LCB lower-bound premise (Prop 1). Not the two-sided band |mu-f|<=beta*sigma:
    under-prediction (f >> mu) never violates a lower bound and must not count as a miss."""
    return float(np.mean((mu - f) <= beta * sigma))
```

and `code/mbo.py:378` switches the conformal multiplier to a signed one-sided nonconformity `r = (mu_cal - y_cal) / s`. So: every `cov_*` and `q_conformal` was recomputed under the one-sided premise, `rho_knn` was dropped as unused, and the synthetic calibration arm was re-run at 10 seeds instead of 30. This is a **methodological correction**, not a result revision — and it is defensible on its face (a lower bound is not violated by under-prediction).

**One live inconsistency to note.** `code/run_all.py:60` still writes `'rho_knn': c['rho_knn']` and `code/mbo.py:614` still computes it, yet neither live artifact contains the key. The live calibration blocks were therefore **not** produced by the current `run_all.py` path, or were post-processed after writing. Given the total absence of provenance metadata, this cannot be resolved from the artifacts.

**`results_camera.json` vs `results_camera.json.presub.bak`** (383,673 B, Jul 15 11:10:54):

- Only difference: live adds the `mbo_enssub` block (21 cells, 3 ens cells x 7 tasks, 10 seeds).
- **238 shared cells, 0 changed. Calibration identical (all 12 keys, same means, n=10 both).**
- Reads as a pre-submission snapshot taken immediately before the ensemble-subsample control was appended.

**`05_findings.json` vs `05_findings.json.bak`** (9,454 B, Jul 15 11:05:16):

- Blocks added in live (7): `equivalence`, `subsample_control`, `rf_robustness`, `beta0`, `gp_coverage`, `stats_9cell`, `bootstrap_ci`
- Unchanged (5): `K_ablation`, `stats`, `gate1`, `crosscheck`, `beta_sweep`
- **Changed (2): `attribution`, `calibration`**

Interpretation: the `.bak` predates the one-sided recomputation (hence `calibration` moved), and the live file adds the entire rebuttal apparatus — TOST equivalence, 9-cell Nemenyi, bootstrap CIs, RF-oracle robustness, β=0 and subsample controls.

### 3.6 Extracted numerics

**η² / effect sizes** (`05_findings.json['attribution']`):

| Regime | η²_opt | η²_surr | η²_inter |
|---|---|---|---|
| SYNTH (unmatched) | **0.013189173376026025** | **0.36872274336144345** | **0.16518056841213977** |
| SYNTH-matched (GATE-1) | 0.024329542667278076 | 0.27542947156964054 | 0.12247869816619208 |
| REAL (Design-Bench) | 0.08473928568992424 | 0.04677094337600403 | 0.013117026453762042 |

Marginal means — SYNTH: opt `{perturb: 0.708, grad: 0.695, cma: 0.608}`, surr `{ens: 0.34, botorchgp: 0.845, svgp: 0.827}`. SYNTH-matched: opt `{perturb: 0.702, grad: 0.652, cma: 0.55}`, surr `{ens: 0.338, botorchgp: 0.741, svgp: 0.825}`. REAL: opt `{perturb: 0.782, grad: 0.584, cma: 0.526}`, surr `{ens: 0.529, botorchgp: 0.729, svgp: 0.634}`.

**Bootstrap 95% CIs** (`bootstrap_ci`): η²_surr `[0.25, 0.57]`, η²_opt `[0.01, 0.19]`, η²_inter `[0.11, 0.26]`, gap_b2 `[0.43, 0.58]`, gap_b0 `[0.37, 0.57]`, gap_sub `[0.29, 1.32]`, gap_b2_minus_b0 `[-0.02, 0.1]`.

**GATE-1** (`gate1`): sei_unmatched `0.6515004904835162`, sei_matched `0.5487667279082784`, **retention `0.842312071785252`**.
> Discrepancy worth flagging: `main.tex` twice claims the surrogate effect "retains 76%". `gate1.retention` is **0.842**. The 76% figure instead matches η²_surr: 0.27542947 / 0.36872274 = **0.747**. The paper's "76%" rounds the η² ratio (74.7%), not the SEI retention (84.2%). The prose is defensible but the two retention measures are 10 points apart and the paper does not disambiguate.

**Friedman p-values:**

| Family | SYNTH | REAL |
|---|---|---|
| Full method set (`stats`) | **1.075443304569636e-06** (16 methods) | **0.7115487157582647** (14 methods) |
| 9-cell grid (`stats_9cell`) | **6.0862487752768236e-05** | **0.6868961533686879** |
| RF-robustness, 3-task (`rf_robustness`) | — | **0.929** |

`main.tex` quotes the **9-cell** family (`p = 6.1e-5` and `p = 0.69`) — correct and the conservative choice.

**Critical differences (Nemenyi, α=0.05):** `stats.SYNTH.cd` = **8.718713580595622** (16 methods); `stats.REAL.cd` = **7.498917263691774** (14 methods); `stats_9cell.cd` = **4.540863039429524** (both regimes, 9 cells — paper quotes 4.5).

Best cells — SYNTH: `botorchgp:grad`, mean rank **2.2857142857142856**, CI `[1.2857142857142858, 3.5714285714285716]`. REAL: `botorchgp:perturb`, mean rank **3.5714285714285716**, CI `[1.8571428571428572, 5.714285714285714]`.

**TOST bounds** (`equivalence`): best `botorchgp:perturb` vs worst `ens:cma`; gap **0.3762254599365316**; **ci90 `[-0.10776105394391278, 0.860211973816976]`**; **effect_bound `0.4839865138804444`** (paper's "±0.48"); `equiv_margin_0p5 = false`, `equiv_margin_0p3 = false` — **equivalence NOT established at either margin.**

**Coverage — SYNTH means:** `cov_indist@2.0` **0.7291714285714287**, `cov_ood@2.0` **0.4133928571428571**, `cov_conf_indist` **0.9024285714285715**, `cov_conf_ood` **0.5074776785714286**, `rho_err` **0.09605668080100692**.

Per-task (SYNTH), `cov_indist@2.0` / `cov_ood@2.0` / `cov_conf_indist` / `cov_conf_ood` / `rho_err`:

| Task | indist@2 | ood@2 | conf_indist | conf_ood | rho_err |
|---|---|---|---|---|---|
| Branin-2D | 0.7094 | 0.418359375 | 0.9066 | 0.837890625 | 0.19934121656486625 |
| Styblinski-5D | 0.6442 | **0.0** | 0.8958 | **0.0** | 0.08715999663998655 |
| Levy-8D | 0.678 | 0.1109375 | 0.9036 | 0.280078125 | 0.0974695162780651 |
| Rosenbrock-10D | 0.862 | 0.64375 | 0.9022 | 0.662109375 | 0.0820685586742347 |
| Rastrigin-15D | 0.7286 | 0.720703125 | 0.9128 | 0.772265625 | 0.05299220236880947 |
| Ackley-20D | 0.9154 | 1.0 | 0.8934 | 1.0 | 0.07233031414124254 |
| Griewank-30D | 0.5666 | **0.0** | 0.9026 | **0.0** | 0.08103496093984376 |

**Coverage — REAL means:** `cov_indist@2.0` **0.7670714285714286**, `cov_ood@2.0` **0.17689732142857142**, `cov_conf_indist` **0.9012857142857145**, `cov_conf_ood` **0.30674525669642855**, `rho_err` **0.10491519603528769**.

| Task | indist@2 | ood@2 | conf_indist | conf_ood | rho_err |
|---|---|---|---|---|---|
| AntMorphology | 0.9435 | 0.0 | 0.898 | 0.0 | 0.33774184296737186 |
| UTR | 1.0 | 0.0 | 0.913 | 0.0 | **-0.07120832423978705** |
| DKitty | 0.5115 | 0.0 | 0.90325 | 0.0 | **-0.07250733802935211** |
| Superconductor | 1.0 | 0.005615234375 | 0.89925 | 0.005126953125 | 0.6037367309469237 |
| TFBind8 | 0.91775 | 0.70703125 | 0.903375 | 0.7021484375 | **-0.0049916239664958666** |
| GFP | **0.0** | 0.0 | 0.898125 | 0.98779296875 | **-0.015379681490710792** |
| TFBind10 | 0.99675 | 0.525634765625 | 0.894 | 0.4521484375 | **-0.042985233940935764** |

Two oddities the audit should see: **GFP `cov_indist@2.0` = 0.0 while `cov_conf_ood` = 0.988** — a degenerate pattern; and **4 of 7 REAL tasks have negative `rho_err`** (σ anti-correlated with error), which is a stronger anti-calibration statement than the paper's "moderately covered" framing conveys.

**Cross-proposal coverage** (`gp_coverage.mean`, from `gpcov.json`): `gp_indist` **0.9837714285714286**, `gp_own` **0.9734933035714286**, `ens_indist` **0.7342857142857142**, `ens_own` **0.4133928571428571**, `ens_on_gp` **0.9704241071428571**, `gp_on_ens` **0.9265066964285714**. (Paper quotes 0.73 / 0.41 / 0.97.)

**β sweep** (`beta_sweep`): betas `[0.0, 0.5, 1.0, 2.0, 5.0]`, `median_norm_slope` **0.1864586742998922**, `helps_count` **6** of `n` **7**.

**β=0 control** (`beta0`): ens_b2 `0.3395283650696281`, gp_b2 `0.8447656777002787`, svgp_b2 `0.8266593093095068`, ens_b0 `0.3667128385263765`, gp_b0 `0.8319199021547241`, svgp_b0 `0.8306950023881766`, **gap_b2 `0.5052373126306506`**, **gap_b0 `0.46520706362834763`**.

**Subsample control** (`subsample_control`): gp `0.8447656777002787`, ens_full `0.3395283650696281`, ens_sub `0.08136947230312194`, gap_full `0.5052373126306506`, **gap_sub `0.7633962053971567`** (gap widens).

**K ablation** (`K_ablation`, normalized): `2` → **0.9498119122900442**, `3` → **0.516669630587786**, `5` → **0.314807002449946**, `10` → **0.18361987006663957**.

**RF robustness** (`rf_robustness`): spread_nonsub **0.34**, spread_rfsub_exclGFP **0.39**, friedman_3task_p **0.929**.

### 3.7 `official_baselines.json` contents

Two external reference methods — **COMs** and **CbAS** — on **3 Design-Bench tasks**, **8 seeds** each, 100th-percentile only.

| Method | Task | mean | std | n |
|---|---|---|---|---|
| coms_official | Superconductor | **97.13883209228516** | 1.9311698902378291 | 8 |
| coms_official | TFBind8 | **0.4360388517379761** | **0.0** | 8 |
| coms_official | GFP | **2.1457350850105286** | 0.02042702632710025 | 8 |
| cbas_official | GFP | **3.701169401407242** | 0.03612763441691885 | 8 |
| cbas_official | TFBind8 | **0.9334180802106857** | 0.03977850477194052 | 8 |
| cbas_official | Superconductor | **89.5780611038208** | 7.256089337857875 | 8 |

Raw `all` arrays are present for every entry (e.g. coms/Superconductor: `[94.398, 94.521, 96.356, 96.900, 97.701, 97.715, 99.309, 100.212]`). **coms/TFBind8 has std = 0.0 — all 8 seeds returned the identical value `0.4360388517379761`**, i.e. that baseline is deterministic across seeds (or the seeds did not take).

**Cross-check vs our reimplementation** (`05_findings.json['crosscheck']`, computed by `run05.py:170-171` against `results_db.json`):

| Comparison | official_norm | official_raw | ours | abs_diff |
|---|---|---|---|---|
| coms:Superconductor | 1.3126878075233002 | 97.13883209228516 | 1.01354655995965 | 0.2991412475636501 |
| coms:TFBind8 | 0.9925851742969443 | 0.4360388517379761 | 2.21014067530632 | **1.217555501009376** |
| coms:GFP | -8.379941155295537 | 2.1457350850105286 | -9.201119024306536 | 0.8211778690109988 |
| cbas:Superconductor | 1.2105149366480696 | 89.5780611038208 | 1.3638127595186234 | 0.1532978228705537 |
| cbas:TFBind8 | 2.1248036594559974 | 0.9334180802106857 | 2.1206253692507744 | **0.004178290205222979** |
| cbas:GFP | 2.1987514755767723 | 3.701169401407242 | 1.8531188517808914 | 0.3456326237958809 |

CbAS reproduces closely on TFBind8 (Δ 0.004). **COMs on TFBind8 diverges by 1.22 normalized units** — our reimplementation scores 2.21 vs official 0.99, i.e. our COMs is *much better* than the published one. Note `main.tex:158` leans on exactly this task ("2.20 on TF-Bind-8, above every GP cell"). Not necessarily wrong, but the largest single reproduction gap in the file sits under a quoted claim.

---

## 4. Gitignore assessment

`.gitignore:11-13`:
```
# preview/scratch (real results come from the cloud run, frozen later)
results/results_camera.json
results/results_db.json
```

`git check-ignore -v` confirms both are ignored. `git ls-files results/` returns only the four **legacy, superseded, pre-grid** files: `results.json`, `results_final.json`, `results_new.json`, `results_revision.json`.

### ARE THE GITIGNORED FILES THE PRIMARY ARTIFACTS BACKING THE PAPER'S HEADLINE NUMBERS?

## **YES.** Unambiguously.

Three independent lines of evidence:

**1. Code path.** `figures.py:26-27`, `tables.py:12`, `stats.py:19`, `analysis.py:20`, and `run05.py:52-53` all hardcode `results_camera.json` / `results_db.json`. These scripts emit `paper/figures_v2/*` and `paper/tables_v2/*` — the paper's actual figures and tables. Nothing in the paper pipeline reads a tracked results file.

**2. Numeric match.** Every headline number in `paper/aaai27/main.tex` traces to `05_findings.json`, which `run05.py` computes *only* from the two gitignored files plus the two `_matched` files:

| main.tex claim | 05_findings value | Source |
|---|---|---|
| η²_surr = 0.37 vs η²_opt = 0.01 | 0.36872274336144345 / 0.013189173376026025 | results_camera.json |
| η²_inter = 0.17 | 0.16518056841213977 | results_camera.json |
| matched η²_surr = 0.28 | 0.27542947156964054 | results_camera_matched.json |
| Friedman p = 6.1e-5 (synth) | 6.0862487752768236e-05 | results_camera.json |
| Friedman p = 0.69 (real) | 0.6868961533686879 | results_db.json |
| CD = 4.5 | 4.540863039429524 | both |
| coverage 0.73 / 0.41 / 0.97 | 0.7291714 / 0.4133928 / 0.9704241 | results_camera.json calibration + gpcov |
| TOST ±0.48 | 0.4839865138804444 | results_db.json |
| η²_surr ∈ [0.25, 0.57] | [0.25, 0.57] | results_camera.json |
| real η² = 0.05 / 0.08 | 0.04677094 / 0.08473929 | results_db.json |

**3. The tracked alternatives cannot back the paper.** None of the four git-tracked files contains a surrogate x optimizer grid at all — they use the pre-grid `lcb`/`coms`/`grad_ascent` schema with `p100_m`/`p100_s` fields. The paper's central contribution (a 3x3 decomposition) **cannot be reconstructed from anything in version control.**

### Risk

The `.gitignore` comment calls these files "preview/scratch (real results come from the cloud run, frozen later)". **That comment is now false.** These files are the frozen record: `results_camera.json` (Jul 15 13:13) and `results_db.json` (Jul 15 05:25) postdate the last code commit touching them and are what the submitted numbers were computed from. Every headline number in an AAAI-27 submission currently rests on two untracked local files, protected by nothing but this laptop's disk, with:

- **no timestamp, no git sha, no config block** in any record — the run that produced them cannot be identified, let alone reproduced;
- **no seed identifiers** — only positional arrays, so a partial re-run cannot be aligned against the original;
- a **live/code inconsistency** (`run_all.py` writes `rho_knn`; neither artifact has it), meaning the current code does not reproduce the current artifacts;
- **`.bak` siblings that are also untracked** — the only record of the two-sided → one-sided methodology change exists as loose local files.

If this directory is lost, the paper is unreproducible. Recommendation: remove lines 12-13 from `.gitignore` and commit both files (392 KB + 141 KB — trivial for git), or move them to a tagged release / DVC / LFS artifact with a recorded git sha. The `_matched` files (untracked, and the only complete copies of `Superconductor/gp` and `GFP/gp`) warrant the same treatment.

---

## 5. Files not parsed

`official_baselines_raw.tgz` (190,924 B, Jul 14 21:04:16 2026) — compressed raw upstream baseline dump. Not extracted; contents not inventoried.
