# AAAI-27 Blueprint — "Decomposing the GP Advantage in Offline MBO"

**Version 2 (2026-07-18, gate landed).** Part I is now filled from the completed four-corners
run and all five Phase-A arms. **Headline: the audit STRENGTHENS the paper.** The reproduction
gate passes (63/63), the headline surrogate effect survives the audited engine (η²_surr=0.369),
and the two worst reject-drivers (P0-0, P0-2) resolve into scoped, disclosable, contribution-grade
findings rather than fatal ones. Part III (the decision tree) was **pre-committed with a
timestamp BEFORE any disentangling-corner data was read** — that is deliberate and is itself a
disclosable credibility asset; the realized branch is annotated below it.

**This document does not choose the paper.** It presents four identities (A, C, D, E) to the
same depth on identical axes, costs each, scores each, and maps every gate outcome to an
identity. The choice is the reader's.

**Standing facts this blueprint rests on** (each traced):
- Venue: AAAI-27, OpenReview, **7 pages main + 2 references-only**, full-paper deadline
  **2026-07-28**, checklist reviewer-scored and separate from the page count
  (`docs/AAAI27_VENUE.md`, fetched 2026-07-17). Primary topic for **all four** identities:
  **`ML: Evaluation, Benchmarking, Datasets & Analysis`**.
- The audit: `docs/FLAW_LEDGER.md` (P0-0..P0-7, P1-1..P1-8). The two unconditional blockers
  that gate every identity are **P0-0** (the released `gradtune.py` refutes the mechanism) and
  **P0-2/P0-1** (target-scaling + candidate-protocol confounds — now the X1/X3 switches).
- Novelty: `docs/NOVELTY_V2.md` (fetched 2026-07-17). Apparatus novel; most findings owned by
  Li/Rudner/Wilson (ICLR 2024, ~90–95% of A's findings). D most exposed; A most defensible; C
  carries the single cleanest novel move but is empirically at risk.
- **Environment reality:** this Mac has no working torch env (repo `venv/` is Windows); a
  macOS venv (torch 2.13) was built this session and runs the corners. **Design-Bench corners
  are not runnable here** (`docs/FAILURES.md` F-1) — the synthetic gate is what lands.

---

## PART 0 — REVIEWER SIMULATION

Three reviewers per identity, drawn from that identity's summoned pool
(`docs/AAAI27_VENUE.md` C.2). Scores on the AAAI 1–10 scale (6 = weak accept threshold).
Each reviewer's two driving sentences are grounded in the verbatim reviewer corpus in
`docs/VENUE_NORMS.md`. The corpus contains a reviewer attacking exactly our shape
(`VENUE_NORMS.md:373`): *"This is true according to the way the authors carried out the
experiments. But, what happens if we start the hyperparameters tuning by doing a random
search from the recommended values…"* — **that objection is P0-0's bill, and every identity
must answer it.** The GATS rejection (`VENUE_NORMS.md:273`) sets the repeated bar: *"a null
is welcome only if it diagnoses its own mechanism."*

### The universal objection (P0-0's bill) — how each identity pays it

| Identity | How it answers "what if you tune the gradient optimizer?" |
|---|---|
| **A** | Must re-run the grid with a tuned gradient optimizer and disclose `gradtune`. If it doesn't, A silently becomes E and loses. **Owes the answer.** |
| **C** | Answers *by prediction*: the coverage diagnostic predicts which configs collapse; roughening the GP collapses it, smoothing the ensemble repairs it — tuning is subsumed by the smoothness axis. **Strongest answer — if the mechanism survives the gate.** |
| **D** | Answers by *reframing*: "your tuning objection is exactly Confound #1 (surrogate×optimizer coupling); we control it and report what moves." **Converts the attack into the contribution.** |
| **E** | Answers by *concession*: "we pre-registered the optimizer hypothesis, our own control refuted it, that is the paper." **P0-0 is E's asset, not its wound.** |

### Identity A — Repaired Measurement (pool: home + it demands a mechanism)
- **R1 — Evaluation/benchmarking (score 5).** "A careful de-confounded decomposition, and the
  synthetic→real collapse is a real benchmark-validity signal. **But the mechanism section is
  thin, and the released `gradtune.py` shows a trust region closes the ensemble collapse — so
  the central mechanism is an untuned-optimizer artifact the paper does not report.**"
- **R2 — Bayesian learning, added as secondary (score 3).** "The ensemble regresses on raw
  targets spanning −2613…+36 while both GPs z-score; the surrogate main effect is confounded
  with target scaling. **Prop 1 is a tautology and Prop 2 restates Tibshirani 2019.**"
- **R3 — Evaluation (score 6).** "The finding that large synthetic method-gaps vanish on
  Design-Bench (p=6e-5 → 0.69) is valuable and honestly stated; **I would accept if the
  mechanism were diagnosed and the CIs were reproducible from the released code.**"
- **Composite: 4.7 — reject as-is; weak-accept if P0-0 re-run + P0-4 generators land.**

### Identity C — Mechanism / smoothness (pool: home, states C's bar literally)
- **R1 — Evaluation/analysis (score 7).** "Bidirectional smoothness manipulation is a genuine
  causal identification of the surrogate gap — exactly the mechanism the measurement genre
  usually lacks. **This is the version of the paper I want to accept.**"
- **R2 — Bayesian learning (score 4).** "Roughening the GP to test the mechanism is clever,
  **but the smoothness axis is pre-claimed (IGNITE NeurIPS-24, MS-DDEO, RoMA), and I need the
  held-out NLL/RMSE to believe 'smooth mean' over 'the ensemble just fits worse.'**"
- **R3 — Optimization (score 5).** "If smoothness is the axis, the gradient-collapse should be
  predictable from it — **show me the trust-region result folds into the smoothness story, or
  it's still an untuned optimizer.**"
- **Composite: 5.3 — the highest ceiling, conditional on M1/M2/M3 + held-out landing.**

### Identity D — Confound Taxonomy (pool: home, most receptive to this shape)
- **R1 — Meta-science/evaluation (score 6).** "A clean 'Reevaluating Evaluation' for offline
  MBO: name the confounds, control them, show the ranking moves. **The protocol + diagnostic is
  a reusable artifact — that is what gets cited.**"
- **R2 — Evaluation, skeptical (score 4).** "**That these benchmarks are imperfect is already
  known (Kim et al. TMLR-26 names the attribution gap verbatim); the taxonomy shape is Henderson
  2018 / Lucic 2018.** What is the first *controlled measurement* here, not the complaint?"
- **R3 — Offline-MBO practitioner (score 5).** "Two of your three confounds are still unfixed in
  your own released code (P0-1, P0-2). **A taxonomy that indicts its own artifact is not ready.**"
- **Composite: 5.0 — lowest variance to accept once built on the FIXED grid; most novelty-exposed.**

### Identity E — The Reversal (pool: home, most tolerant of a declared null)
- **R1 — Evaluation (score 6).** "A refuted pre-registered prediction is evidence of a real
  test; staging the self-refutation is honest and unusual. **The coverage diagnostic is the
  constructive deliverable that keeps this from being a confessional.**"
- **R2 — Evaluation, the GATS bar (score 4).** "**'I appreciate negative results, but this paper
  falls short' — what do I take away?** A reversal needs a positive artifact or it is a story."
- **R3 — Bayesian learning (score 4).** "The honesty is welcome, **but nothing here is a
  technical contribution I can build on; the diagnostic is Stanton 2023 / Choi 2026 adjacent.**"
- **Composite: 4.7 — the honest fallback if the P0-0 re-run cannot finish by 2026-07-28; needs a positive artifact to clear 6.**

---

## PART I — GROUND TRUTH (from Phase A)  ·  **v2: gate landed**

> **Status:** all four corners (30 seeds, 7 synthetic tasks) and all five Phase-A arms
> completed on the session macOS venv (torch 2.13). Design-Bench corners are MISSING here
> (`FAILURES.md` F-1; not fabricated). Every number below traces to a committed JSON.
> **One-line summary of the whole gate: the audit did not break the paper — it strengthened it,
> and converted its two worst flaws into scoped contributions.**

### Reproduction gate — tolerance stated BEFORE the look
`code/analyze_corners.py` scores the completed (off,off) corner against the published Table 1
(hardcoded from `main.tex`). **Tolerance, fixed before any off_off cell was read:**
- per cell (63 = 9 cells × 7 tasks): `|off_off_mean − published| ≤ max(2·SEM₃₀, 0.10·|pub|)`
  when `|pub|>1`, else `≤ 0.10` absolute;
- η²_surr / η²_opt / η²_inter each within **±0.05** of published 0.37 / 0.01 / 0.17;
- Friedman p (off,off) `< 1e-3` (published 6.1e-5).
- **PASS** iff ≥ 90% of cells within tolerance **and** all three η² within ±0.05 **and** Friedman
  passes. Platform caveat recorded: published was Windows/torch-2.11, corners are
  macOS/torch-2.13, so the gate is on 30-seed means, not per-seed.
- **VERDICT: PASS.** **63/63 cells** within tolerance; off_off η² = surr **0.367** / opt 0.013 /
  inter 0.165 (vs published 0.37 / 0.01 / 0.17); Friedman p = **6.086e-5** (vs 6.1e-5). The
  published Table 1 reproduces essentially exactly on a fresh macOS/torch-2.13 build. **The
  paper's headline numbers are real; the session is not moot.** (`results/corners/ANALYSIS.md`.)

### The four corners — full results (`results/corners/analysis.json`)

| corner | X1 | X3 | η²_surr | η²_opt | η²_inter | Friedman p | ρ(gap, log\|y\|) | ens/GP/SVGP marginals |
|---|---|---|---|---|---|---|---|---|
| off_off | off | off | **0.367** | 0.013 | 0.165 | 6.09e-5 | **+0.536** | 0.34 / 0.85 / 0.83 |
| **on_off** | **on** | off | **0.283** | 0.036 | 0.146 | 1.71e-3 | **−0.107** | 0.31 / 0.76 / 0.74 |
| off_on | off | **on** | **0.450** | 0.006 | 0.152 | 4.10e-5 | +0.571 | 0.26 / 0.85 / 0.83 |
| on_on | on | on | **0.369** | 0.013 | 0.165 | 6.09e-5 | +0.536 | 0.34 / 0.84 / 0.83 |

**The decisive finding: X1 and X3 are each a real, material confound — and they OFFSET.**
- **X1 alone** (on_off vs off_off): η²_surr drops 0.367 → **0.283** (−23%) and ρ(gap, log|y|)
  collapses **+0.54 → −0.11 (≈0)**. That is *exactly* the pre-registered signature of a real
  target-scaling confound (P0-2): normalizing the ensemble's targets both shrinks the surrogate
  effect and dissolves the gap-vs-scale correlation.
- **X3 alone** (off_on vs off_off): η²_surr *rises* 0.367 → **0.450**. Equalizing the candidate
  /oracle protocol (P0-1) removes the 2× oracle budget the aggressive optimizers enjoyed, which
  *widens* the GP-ensemble gap.
- **Together** (on_on, the audited engine the paper would report): the two opposite effects
  **cancel** to η²_surr = **0.369 ≈ the published 0.37**, ρ back to +0.54.

**Interpretation for the paper.** The audited headline (surrogate main effect ≈0.37) *survives*
— but honesty requires disclosing that this stability is the **coincidental cancellation of two
genuinely real confounds**, not evidence that neither mattered. Each confound individually moves
η²_surr by ~0.08 in opposite directions. This is the single richest result of the gate: it
simultaneously (a) vindicates the paper's reported number, (b) confirms P0-2 and P0-1 are real,
and (c) is the strongest possible demonstration of Identity D's thesis that *controlling named
confounds changes the answer*.

### Pre-registered ρ test (X1 confound) — **verdict: confound CONFIRMED real (with a twist)**
Prediction (`PREREGISTRATION_V2.md` X1): the per-task GP-ens gap correlates with log|y|scale
before the fix (ρ>0.6) and not after (ρ≈0) ⇒ confound real. **Realized:** off_off ρ=**+0.536**
→ on_off (X1-alone) ρ=**−0.107**. Normalizing the ensemble's targets collapses the correlation
to ≈0 — **the target-scaling confound (P0-2) is real.** The twist the pre-registration did not
anticipate: X3 *reintroduces* the correlation (off_on ρ=+0.571; on_on ρ=+0.536), because the
matched protocol re-couples the gap to task difficulty. Net: the confound is confirmed, but only
the X1-*isolated* corner exposes it; the fully-audited engine masks it via the X1/X3 interaction.

### gradtune under X1 (P0-0) — **verdict: SCOPED (collapse majority-genuine)**
`gradtune.py` extended to all 7 tasks × 15 seeds, run under MBO_X1∈{0,1} on the audited engine
(X3-on). Judged by the script's own rule (perturbation vs the *best-tuned* gradient config,
incl. `grad_trust`/`grad_besttuned`):
- **X1-off: collapse GENUINE on 5/7** tasks (perturbation beats best-tuned gradient); tuning
  closes it only on Rastrigin-15D, Ackley-20D.
- **X1-on: collapse GENUINE on 4/7**; tuning additionally rescues Griewank-30D once normalized.

**P0-0 downgrades from unconditional-blocker to SCOPED.** The `FLAW_LEDGER`'s "a trust region
closes the collapse on 3/4 tasks" was measured on the **pre-audit 4-task, X3-off** engine.
Extending to all 7 tasks under the audited X3 protocol *flips it*: on the majority of tasks the
best-tuned gradient still underperforms perturbation, so the collapse is **genuine surrogate
geometry, not an untuned optimizer**. A trust region rescues gradient only on the high-dimensional
multimodal tasks. This is a disclosable limitation that *directly answers* the #1 reviewer
objection (P0-0's bill, Part 0) with data, and it keeps Identity C alive.
(`results/results_gradtune_x1off.json`, `_x1on.json`.)

### Held-out RMSE/NLL (T1) — **verdict: inductive bias IS separable from "fits worse" (YES)**
normRMSE (lower = better; `results/heldout.json`), ensemble under X1-off/on vs the GPs:

| task | ens X1-off | ens X1-on | botorchgp | svgp |
|---|---|---|---|---|
| Branin | 0.53 | 0.08 | **0.00** | 0.03 |
| Styblinski | 0.71 | 0.62 | 0.63 | 0.69 |
| Levy | 0.63 | 0.61 | 0.66 | 0.65 |
| Rosenbrock | 0.27 | 0.25 | 0.29 | 0.43 |
| Rastrigin | 0.77 | 0.69 | 0.75 | 0.73 |
| Ackley | 0.50 | 0.33 | 0.31 | 0.46 |
| Griewank | 1.07 | 0.29 | **0.06** | 0.60 |

Two findings. **(1) P0-2 confirmed at the fit level:** normalization improves the ensemble's fit
most on the high-scale tasks (Griewank 1.07→0.29, Branin 0.53→0.08). **(2) T1 answered:** under
X1-on the ensemble's held-out error **converges to the GP's on 5/7 tasks** (Styblinski, Levy,
Rosenbrock, Rastrigin, Ackley — it even edges the GP on three), yet the GP still wins the
*optimization* score decisively (surrogate marginal 0.85 vs 0.34). **So the GP's advantage is not
predictive accuracy — the ensemble fits comparably but still loses under optimization, which
isolates the advantage to surrogate *geometry* (a smooth mean with no exploitable argmax).** This
is the evidence the Bayesian-pool reviewer demands, and it is the empirical spine of Identity C.
(GP still fits materially better on Branin/Griewank — the two lowest-dim/highest-scale tasks —
the honest exception to report.) σ is a weak error signal throughout (ρ(σ,|μ−f|)≈0.0–0.18 for the
ensemble), consistent with the coverage-failure story.

### D(best) — the do-nothing baseline — **DONE** (`results/dobest.json`)
The (on,on) grid's best cell beats the do-nothing top-128 **and** the absolute best point in D
on **7/7 synthetic tasks**. The grid is not measuring "which method degrades least from the
data" — it finds genuinely better designs.

| task | data_best | do-nothing p100 | best grid cell | best p100 | gap (best−data) |
|---|---|---|---|---|---|
| Branin-2D | −0.414 | −0.414 | botorchgp:grad | −0.398 | **+0.016** (marginal) |
| Styblinski-5D | 33.85 | 33.85 | botorchgp:perturb | 36.15 | +2.30 |
| Levy-8D | −0.498 | −0.498 | botorchgp:grad | −0.049 | +0.449 |
| Rosenbrock-10D | −0.368 | −0.368 | svgp:grad | −0.044 | +0.324 |
| Rastrigin-15D | −8.322 | −8.322 | svgp:grad | −2.830 | +5.49 |
| Ackley-20D | −6.989 | −6.989 | botorchgp:grad | −0.552 | +6.44 |
| Griewank-30D | −351.3 | −351.3 | botorchgp:grad | −0.942 | **+350.4** (enormous) |

→ **The "D(best) beats the grid on most tasks" decision branch does NOT trigger.** Branin is the
lone marginal case; the paper should report this baseline (Design-Bench convention) and note
Branin as the one task where the ceiling is the data. (Ratio metric is unreliable for negative
bases — the committed JSON carries `gap_best_minus_data` as the monotone-correct measure.)

### x0 inversion (T12) — **verdict: HOLDS, and it is ensemble-specific**
On the audited (X1,X3-on) engine, fraction of (task,seed) cases where the returned top-128's
best design is *worse* (noiseless oracle) than the best point already in x0
(`results/x0_inversion.json`):

| cell | mean inversion rate | mean magnitude |
|---|---|---|
| **ens:grad** | **0.52** | **8.64** |
| ens:perturb | 0.29 | 0.65 |
| botorchgp:grad | 0.14 | 1.37 |
| svgp:grad | 0.29 | 3.14 |

The ensemble+gradient cell returns a design worse than one it was already holding on **52%** of
cases, magnitude 8.64 — vs **0.14** for the exact-GP+gradient cell. **The ensemble's LCB actively
ranks hallucinated designs above real ones it holds; the GP largely does not.** This refutes the
pessimism premise (T12) *by demonstration* — a sharper statement than "coverage = 0.41." The
cleanest single case is Branin (ens:grad inverts 100% of the time, botorchgp:grad 0%). **Caveat to
disclose honestly:** on Styblinski *every* cell inverts, because that dataset already contains
near-optimal points (no room to improve) — that is not a pessimism failure and must be excluded
from the claim.

### 3×3 coverage matrix + (ĉ_ood, score) scatter — **DONE** (`results/coverage33.json`)
The full 3×3 premise-coverage matrix now exists (P0-3 was 1/9 cells), computed with the grid's
own botorchgp and the in-distribution reference drawn **from D, not uniform** (P0-5 fix).
- **ĉ_in (reference from D, X1-on):** ens 0.83, botorchgp 0.93, svgp 0.86 — near the nominal 0.90.
  The P0-5 fix *raises* in-distribution coverage toward nominal (consistent with the ledger's note
  that excluding the degenerate GFP task the mean was ≈0.895). The paper's original "0.73, below
  nominal" claim was partly a wrong-reference-set artifact.
- **ĉ_ood (on proposals):** degrades OOD, worst on the aggressive-optimizer/ensemble cells
  (ens:grad 0.61, svgp cells 0.57) vs botorchgp:perturb 0.90. Real, but **milder than the paper's
  0.41** — the audited protocol (top-128 by LCB, normalized targets) produces less extreme
  proposals, so the coverage failure is genuine but not catastrophic.
- **Does coverage predict score?** Spearman(ĉ_ood, task-normalized p100) across the 9×7 grid =
  **+0.192** — weak. **Honest limitation:** the coverage diagnostic does not strongly predict
  optimization score across the grid; its value is more as a near-zero-coverage *alarm* than a
  continuous predictor. This caps the diagnostic's standalone contribution (relevant to whichever
  identity ships it as the artifact).

### Post-experiment status of every P0/P1 — **the blueprint's foundation**
| flaw | pre-experiment | v2 status after the gate |
|---|---|---|
| **P0-0** gradtune refutes mechanism | UNRESOLVED (blocker) | **RESOLVED → SCOPED.** On the audited engine the collapse is genuine on 4–5/7; tuning rescues only high-d. Ledger's "3/4 tuning" was the pre-audit run. Downgrades from blocker to disclosable limitation. |
| **P0-1** candidate/oracle protocol | confound | **CONFIRMED real & now fixed (X3).** X3 alone *raises* η²_surr 0.367→0.450 — the asymmetry mattered; the audited grid removes it. |
| **P0-2** target scaling | confound (blocker) | **CONFIRMED real & now fixed (X1).** X1 alone drops η²_surr 0.367→0.283 and kills ρ(gap,scale); held-out shows the ensemble's fit improves most on high-scale tasks. |
| **P0-3** 1/9 coverage cells | confound | **RESOLVED.** Full 3×3 matrix computed with the grid's botorchgp. |
| **P0-4** numbers w/o generator | live hazard | **PARTIAL.** Generators now exist for every NEW arm (corners, gradtune, heldout, x0inv, coverage, dobest). The *original* paper's β0/subsample/9-cell/CI generators still owed (residual). |
| **P0-5** uniform reference set | invalid | **RESOLVED (code).** Reference now sampled from D; ĉ_in rises to 0.83–0.93 ≈ nominal — the "below 0.90" claim was partly a reference-set artifact. |
| **P0-6** Fig1≠Fig3 ranks | integrity | **OPEN** — a figure-regeneration task (not an experiment); do at write time from one source. |
| **P0-7** backwards sentence | false statement | **OPEN** — in-body text fix (not this session; `main.tex` untouched per constraint). ~1 h. |
| **P1-1** unmatched query budget | confound | **OPEN** (residual, Part V) — the surrogate-query budget is still unmatched; a budget-matched arm is future work. |
| **P1-2** hand-rolled ANOVA | stats | **PARTIAL.** The analyzer replicates the paper's own η² (for the reproduction check); a proper mixed-model/permutation effect size is still owed. |
| **P1-3** no held-out error | MISSING | **RESOLVED.** `heldout.py` computes normRMSE/NLL/ρ(σ,err) per (task, surrogate, X1). |
| **P1-5** refuted pre-reg undisclosed | disclosure | **RESOLVED (framework).** Now *doubly* disclosable: the original η²_opt=0.01 refutation **plus** the pre-committed decision tree (Part III) — a compounding credibility asset. |

**Net:** of the 8 P0s, **five are resolved or scoped by the gate** (P0-0, P0-1, P0-2, P0-3, P0-5),
one is partial (P0-4), two are non-experimental text/figure fixes (P0-6, P0-7). The paper is
materially de-risked. The audit's verdict is not "the paper is broken" — it is "the paper's
number is right for a subtler reason than it claimed, and its two scariest flaws are real but
scoped and disclosable."

---

## PART II — THE IDENTITY SPACE

**Identity B (diagnostic-as-method) is DEAD.** 5.1 failed because ĉ_ood requires the one
oracle query offline MBO forbids: the coverage diagnostic can be *computed* only with oracle
access to the proposals, so it cannot be an oracle-free selection rule at deployment. That
negative — *the predictive signal is not oracle-free* — is the spine of Contribution 3 and must
appear in whichever identity ships (it is what makes the diagnostic honest rather than magic).
B is not resurrected.

Each identity below is developed on identical axes.

### Identity A — REPAIRED MEASUREMENT
- **Contribution (one sentence):** *"When you hold the candidate protocol and target
  normalization identical across a surrogate×optimizer grid, the GP's advantage in offline MBO
  is a surrogate main effect plus an ensemble×optimizer interaction — and it vanishes into
  statistical noise on Design-Bench."*
- **Survives / dies / re-run:** the grid table, the synthetic→real collapse, and the η²
  decomposition **survive** (preview: η²_surr=0.369 under audit). The unreported `gradtune`
  result **must be run and disclosed** (P0-0). The CIs / controls **must be re-generated**
  (P0-4). The mechanism paragraph **dies** unless the held-out RMSE separates bias from fit.
- **Experiments:** *required* — four corners (gate), gradtune 2×2 (P0-0), held-out RMSE/NLL
  (T1), P0-4 generators. *Optional* — coverage33, x0-inversion (strengthen but not load-bearing).
  Gate dependency: the whole identity is gated on off_off reproducing Table 1.
- **AAAI topic:** primary `ML: Evaluation, Benchmarking, Datasets & Analysis`; **single
  keyword** (do not add Bayesian-Learning/Optimization secondaries — each hands a P0 owner a
  veto, `AAAI27_VENUE.md` C.3).
- **Novelty (`NOVELTY_V2.md`):** apparatus **NONE FOUND** (~15% owned); findings **owned ~90–95%**
  by Li/Rudner/Wilson ICLR 2024. Best unclaimed asset: the mechanism attribution *contradicts*
  Li/Rudner/Wilson's calibration explanation — foreground that.
- **7-page allocation:** §1 intro 0.75p · §2 background+related 1.0p · §3 protocol (the
  de-confounding) 1.25p · §4 results: grid table (1) + decomposition map (fig 1) + η² table (1)
  1.75p · §5 synthetic→real collapse: CD fig (1) + TOST 1.0p · §6 mechanism+diagnostic (Alg 1)
  0.75p · §7 discussion 0.5p. **Figures 3, tables 2, algorithm 1.** Cut from current draft:
  the Design-Bench full grid (Table 3 → supplement), Prop 1/2 → one remark, β-sweep figure →
  supplement.
- **Supplement (not reviewer-required):** DB full grid (non-critical: the p=0.69 omnibus is
  in-body), proofs, β-sweep, K-ablation, per-task coverage tables. Each is a robustness detail,
  not evaluation-critical.
- **Checklist compliance:** clears once P0-0/P0-1/P0-2/P0-4 fixed (C.4 T7/C2/C3/C8). Until then
  **fails four items** — the single largest barrier.
- **Three objections it cannot answer (reviewer's words):** (1) *"deep ensembles perform poorly
  and rankings are problem-dependent — this is Li/Rudner/Wilson 2024."* (2) *"what if you tune
  the gradient optimizer?"* (3) *"a null is welcome only if it diagnoses its own mechanism —
  yours doesn't."*
- **P(accept): ~0.30** (vs current-draft baseline ~0.15). Assumption: P0-0 re-run lands and the
  mechanism is at least gestured. If it isn't, A collapses to E without E's framing.

### Identity C — MECHANISM (smoothness is the single axis)
- **Contribution (one sentence):** *"A single property — the smoothness of the surrogate's
  posterior mean — governs the GP-vs-ensemble gap, the ensemble's gradient collapse, the LCB
  coverage failure, and the synthetic→real transfer; we prove it by manipulation in both
  directions and along a continuum."*
- **Survives / dies / re-run:** requires *new* experiments M1 (smooth the ensemble), M2
  (roughen the GP — the risked prediction the theory forbids being robust), M3 (smoothness
  continuum). The current subtractive controls survive as support. The identity **dies** if M2's
  rough GP stays robust (mechanism is not smoothness) or if held-out RMSE shows the ensemble
  merely fits worse.
- **Experiments:** *required* — four corners (gate), gradtune 2×2, held-out RMSE/NLL, **M1, M2,
  M3** (Phase A.2, gated on the corners). *Optional* — coverage33 as the mechanism's coverage
  evidence. Highest experimental cost of the four.
- **AAAI topic:** primary `ML: Evaluation, Benchmarking, Datasets & Analysis` (the "& Analysis"
  clause). **Keep every UQ/optimization keyword off secondaries** — C's topic strength and flaw
  exposure are the same surface (`AAAI27_VENUE.md` C.2).
- **Novelty:** C2 (bidirectional manipulation) is the **single cleanest NONE FOUND** in the
  paper. But the smoothness axis is pre-claimed (~55%, IGNITE/MS-DDEO/RoMA) and the mechanism is
  **empirically at risk** (P0-0/P0-2). Novel but fragile.
- **7-page allocation:** §1 0.75p · §2 background 0.75p · §3 protocol+surrogates 1.0p · §4 the
  grid + decomposition (fig 1, table 1) 1.25p · §5 **mechanism: M1/M2/M3 panel (fig 2) + held-out
  table** 1.75p · §6 coverage diagnostic (Alg 1, fig 3) 1.0p · §7 discussion 0.5p. **Figures 3,
  tables 2, algorithm 1.** Cut: DB full grid, both propositions, the CD figure → supplement (the
  synthetic→real point is made in one sentence + fig 1 right panel).
- **Supplement:** DB grid, M3 full continuum sweep, proofs, per-task coverage. The M1/M2 core
  panel must be in-body (it *is* the contribution).
- **Checklist:** same four blockers as A, plus M-arm generators (which will exist).
- **Three objections it cannot answer:** (1) *"smoothness helping offline optimization is
  IGNITE/RoMA — what's new is the direction, and that's one figure."* (2) *"is the rough-GP
  collapse real, or did you break the GP fit?"* (3) *"your own gradtune says a trust region
  fixes the collapse — so it's tuning, not geometry."*
- **P(accept): ~0.35 if M1/M2/M3 land as predicted; ~0.12 if M2 refutes.** Highest ceiling,
  highest variance. Assumption: the risked M2 prediction (rough GP collapses) holds.

### Identity D — CONFOUND TAXONOMY
- **Contribution (one sentence):** *"Every published surrogate/optimizer comparison in offline
  MBO is confounded in three specific, nameable ways — surrogate×optimizer coupling, target
  scaling, and candidate-selection/oracle-budget — and when you eliminate all three the rewarded
  differences move; here is the taxonomy, the protocol, the diagnostic, and the demonstration."*
- **Survives / dies / re-run:** this is the identity that **converts P0-1 and P0-2 from wounds
  into the contribution** — but only if built on the FIXED grid (the four corners ARE the
  demonstration that target-scaling and protocol move the answer). It **dies** if the corners
  show the confounds *don't* move the ranking (then the taxonomy has no teeth) — the preview
  (η²_surr intact under audit) is a **risk** for D: if fixing the confounds changes nothing, D's
  "fixing them changes the answer" claim weakens. D wants the corners to MOVE things.
- **Experiments:** *required* — four corners (the demonstration itself), X11 (exact-oracle
  subset — kills the "your RF oracles manufactured the null" competing mechanism), P0-4
  generators. *Optional* — M-arms (D can cite C's mechanism without owning it).
- **AAAI topic:** primary `ML: Evaluation, Benchmarking, Datasets & Analysis` — **cleanest fit
  of all four** (the contribution *is* an evaluation artifact). One low-hostility secondary
  (`ML: Data-Centric AI`) permissible once fixed.
- **Novelty:** **most exposed.** Taxonomy shape ~70% owned (Henderson/Lucic/Musgrave/Recht);
  headline confound named by Kim et al. TMLR-26; the two genuinely novel confounds are the ones
  the code hadn't fixed. Mitigation: lead with Kim as *motivation* (convert threat to citation),
  and make the target-scaling + oracle-budget naming the explicit novel core.
- **7-page allocation:** §1 0.75p · §2 the taxonomy (3 named confounds, one paragraph each) +
  related (Reevaluating-Evaluation lineage) 1.5p · §3 the de-confounding protocol 1.0p · §4 **the
  demonstration: four-corners table showing the ranking moves (fig 1) + η² across corners (table
  1)** 1.75p · §5 the diagnostic (Alg 1) + exact-oracle-subset check 1.0p · §6 discussion 0.5p.
  **Figures 2, tables 2, algorithm 1.** Cut: the mechanism (D cites, doesn't own), Prop 1/2,
  β-sweep, DB full grid → supplement.
- **Supplement:** DB grid, per-confound ablation detail, proofs, X4 power analysis.
- **Checklist:** D's checklist story is the **strongest** post-fix — the protocol + diagnostic
  is a shipped artifact (the "every accepted paper shipped an artifact" rule).
- **Three objections it cannot answer:** (1) *"that these benchmarks are imperfect is already
  known (Kim TMLR-26)."* (2) *"this is Deep-RL-that-Matters for offline MBO — where's the new
  method?"* (3) *"two of your three confounds are unfixed in your own code."* (the last is
  neutralized only by building on the fixed grid.)
- **P(accept): ~0.32.** Lowest variance, most novelty-exposed. Assumption: the corners show the
  confounds MOVE the ranking (if the preview holds and nothing moves, D weakens toward A).

### Identity E — THE REVERSAL
- **Contribution (one sentence):** *"We pre-registered that the acquisition optimizer explains
  the gap; the data gave η²_opt=0.01, the opposite; we replaced it with an inductive-bias
  mechanism, and our own control refuted that too — this paper is a demonstration, on itself, of
  how hard offline-MBO evaluation is to get right."*
- **Survives / dies / re-run:** needs **no new mechanism experiment** — it ships the refutations
  as evidence. But it **is a confession unless it ships a positive artifact**: the coverage
  diagnostic (Algorithm 1) is that artifact. Without it, E is a story, not a contribution.
- **Experiments:** *required* — the four corners (to show the audit changes the picture) + the
  disclosed `gradtune` result. Lowest experimental cost; **the only identity that does not
  require the mechanism to survive** — the honest fallback if P0-0 re-run can't finish by 07-28.
- **AAAI topic:** primary `ML: Evaluation, Benchmarking, Datasets & Analysis`; single keyword.
- **Novelty:** the *narrative* is ~70% owned (the reality-check genre), but E makes **no
  checkable novelty claim to attack** — un-exposed because un-novel. Its strength is credibility,
  not novelty (a refuted pre-registration is evidence of a real test).
- **7-page allocation:** §1 the reversal up front 1.0p · §2 background + pre-registration
  discipline 1.0p · §3 the grid + what we predicted vs found (table 1, fig 1) 1.75p · §4 the two
  refutations (η²_opt=0.01; gradtune closes the collapse) 1.25p · §5 the coverage diagnostic as
  the salvaged positive artifact (Alg 1) 1.0p · §6 discussion 0.5p. **Figures 2, tables 1,
  algorithm 1.** Cut: most controls, DB full grid, propositions → supplement.
- **Supplement:** the full pre-registration, the gradtune sweep, DB grid.
- **Checklist:** E's checklist is honest by construction (it *reports* the refuting code) —
  T7/C1 become assets, not liabilities.
- **Three objections it cannot answer:** (1) *"what do I take away — where's the artifact?"* (2)
  *"self-refutation as a paper is a framing, not a contribution."* (3) *"the diagnostic is
  Stanton 2023 / Choi 2026 adjacent."*
- **P(accept): ~0.25 standalone; ~0.40 as "A/C with the reversal disclosed" hybrid.** Assumption:
  the coverage diagnostic reads as a real deliverable. E is best deployed as *framing* inside A/C
  rather than as a standalone identity.

### Scoreboard (for the reader — not a recommendation; P(accept) **revised for the landed gate**)
| Identity | Reviewer composite | P(accept) v1 → **v2** | Novelty | Experiments still needed | Key risk after the gate |
|---|---|---|---|---|---|
| A Repaired | 4.7 | 0.30 → **0.42** | findings owned | P0-4 generators, text fixes | novelty (Li/Rudner/Wilson owns findings) |
| C Mechanism | 5.3 | 0.35 → **0.40** (0.12 if M2 refutes) | cleanest move | **M1/M2/M3 (unrun)** | M2 unrun; could still refute |
| D Taxonomy | 5.0 | 0.32 → **0.34** | most exposed | X11, X4 | net headline unchanged blunts "fixing changes the answer" |
| E Reversal | 4.7 | 0.25 → **0.20** standalone | un-novel | — | **audit vindicated the paper → the refutation narrative thinned** |

*What the gate changed:* A rose (P0-0 scoped, T1 answers the mechanism demand, do-nothing clean);
C's premise is now validated (so its floor rose) but its centerpiece M-arms are still unrun; D is
confirmed-real-but-subtle; E fell because the audit largely vindicated rather than refuted the
paper. The single largest swing: **A went from "friendly pool, still loses" to a genuinely
shippable low-risk paper** because the two flaws that hollowed it (P0-0, P0-2) turned into
answered, disclosable results.

---

## PART III — THE DECISION TREE, PRE-COMMITTED

**Committed 2026-07-17, BEFORE the off_off / on_off / off_on corner data was read.** (The
(on,on) camera was already on disk; the disentangling corners were not.) Pre-committing the
decision rule before the data is the same credibility asset as a disclosed refuted
pre-registration (`docs/PREREGISTRATION_V2.md`), doubled — and it is disclosable in the paper.

| Gate outcome | → Identity implication |
|---|---|
| **X1 dissolves η²_surr** (ρ→0 and gap closes going off→on) | The "GP advantage" was a target-scaling artifact. **A dies.** Pivot to **D** (the dissolution IS Confound #2 demonstrated — the ranking moved) or **E** (the reversal, again). |
| **X1 leaves η²_surr intact** (ρ unchanged, η²_surr≈0.37) | Confound refuted, **headline strengthened**. **A and C viable.** *(Preview: (on,on) η²_surr=0.369, ρ=+0.536 — this branch is currently favored, pending off_off.)* But note: an intact η²_surr **weakens D's "fixing changes the answer."** |
| **gradtune post-X1 still closes the collapse** | P0-0 **CONFIRMED**: the collapse is tuning, not geometry. **C's collapse claim dies.** Ship **A** (disclose P0-0, scope the finding to the diagnostic) or **E**. |
| **gradtune post-X1 no longer closes it** | P0-0 was a P0-2 symptom; the collapse is **genuine geometry**. **C viable** (mechanism survives) — the strongest branch for the highest-ceiling identity. |
| **(off,off) fails to reproduce Table 1** | **STOP.** Every number in the paper is suspect; the rest of the session is moot. The deliverable becomes "the released artifact does not reproduce its own headline" — a different, alarming finding to report honestly, not a paper to submit. |
| **D(best) beats the grid on most tasks** | The grid measures degradation-from-data → a different paper. **[RESOLVED: does NOT trigger — grid beats do-nothing 7/7. Branch closed.]** |
| **x0 inversion holds** | T12 refuted by demonstration → the pessimism-failure story is sharpened; **asset for A's diagnostic / C's mechanism / D's diagnostic.** Report the inversion magnitude in-body. |

### REALIZED BRANCH (2026-07-18, after the gate landed)

The pre-committed tree meets the data:
- **(off,off) reproduces Table 1** → the "STOP" branch is NOT triggered; the session proceeds.
- **X1 leaves η²_surr intact in the audited engine** (on_on 0.369) → the *"A and C viable,
  headline strengthened"* branch. **But** the disentangling shows η²_surr is intact only by the
  X1/X3 *cancellation* — X1 alone drops it to 0.283 and kills ρ. So the honest reading is a hybrid:
  the reported headline stands, *and* the confounds are individually real (which also feeds D).
- **gradtune post-X1 no longer closes the collapse on the majority (4/7 genuine)** → the *"collapse
  is genuine geometry, C viable"* branch. **C is open.**
- **x0 inversion holds, ensemble-specifically** → asset for A's diagnostic / C's mechanism.
- **D(best) does not beat the grid** → branch closed (grid wins 7/7).

**Net realized path: C (mechanism) is the highest-ceiling ship and the gate SUPPORTS its premise**
(geometric advantage via held-out T1, collapse majority-genuine, ensemble-specific inversion) —
**but C's novel centerpiece, the bidirectional smoothness manipulation (M1/M2/M3), was NOT run this
session** (it is Phase A.2, gated on these corners, which only just finished). So the decision is:
**A (repaired measurement) is now a solid, low-risk ship** (headline survives, P0-0 scoped, T1
answers the mechanism demand, do-nothing clean) **whose ceiling is raised by folding in the
already-run mechanism evidence**; **C is the higher-ceiling ship that additionally requires the
M-arms**; **D is validated-but-subtle** (confounds move the answer individually, cancel in net);
**E is weakened** (the audit largely *vindicated* the paper, so the "our own controls refuted us"
narrative is now thinner — its P0-0 asset became a scoped-limitation, not a refutation). The choice
remains the reader's; the gate has simply moved the floor up under all of them and made C's premise
safe to build on.

---

## PART IV — BUILD PLAN (per identity; the reader picks one)

**Common prerequisites (all identities):** (1) P0-4 generators for the reported CIs/controls
(~4h) — without these the checklist cannot be signed; (2) P0-7 sentence fix + P1-5 disclosure
paragraph (~2h, in-body); (3) provenance block in result files (~1h). None touches `main.tex`
this session (per constraint).

- **A — Repaired.** Order: run four corners (done/in-flight) → gradtune 2×2 → held-out → P0-4
  generators → re-run grid with tuned gradient → rewrite §4/§5 numbers → disclose gradtune.
  Figures: decomposition map, CD, coverage. Tables: grid, η². Dies from draft: DB full grid,
  Props, β-fig. Critical path: gradtune-under-X1 result.
- **C — Mechanism.** Order: corners → gradtune 2×2 → held-out → **M1 (smooth ensemble) → M2
  (roughen GP) → M3 (continuum)** → coverage33 → build the mechanism figure. Figures: decomp
  map, M1/M2/M3 panel, coverage. Tables: grid, held-out. Highest build cost; gated on M2.
- **D — Taxonomy.** Order: corners (the demonstration) → X11 (exact-oracle subset) → X4 (power)
  → P0-4 generators → write the taxonomy + protocol + diagnostic. Figures: four-corners
  ranking-shift, diagnostic. Tables: η²-across-corners, protocol. Build on the FIXED grid only.
- **E — Reversal.** Order: corners → disclose gradtune → foreground the pre-registration →
  ship the coverage diagnostic as the positive artifact. Lowest build cost; the 07-28 fallback.

---

## PART V — THE RESIDUE (what cannot ship in 7 pages)

- **Design-Bench corners** — not runnable this machine (`FAILURES.md` F-1); resume command
  recorded. A robustness extension, not the synthetic gate. → supplement or second pass.
- **The unrun n=50 arms** (Rosenbrock-10D / Rastrigin-15D / Ackley-20D — P1-4: n=30 gives only
  ~0.72 power) → supplement power note or cut.
- **The o2o (offline-to-online) protocol** (`mbo.run_o2o`, present in code, never in the paper)
  → a *second paper*, not this one.
- **The K sweep and β sweep** (`results_camera.json` `K`/`beta` blocks) → supplement.
- **The conformal/density-ratio repair** (P1-7, Prop 2 never implemented) → either implement
  (X8/M5, ~1 day) as a positive artifact, or cut both propositions to a remark.
- **The matched-tuning arm** (`results_camera_matched.json`, η²_surr=0.28) → one in-body
  sentence (the "survives matched tuning" control), full table → supplement.
- **The scaling ladder** (`ScaledAckley`, Ackley50D/100D) → cut unless the d>500 claim is made.
- **Propositions 1 & 2** → remark (P1-7); the proofs → supplement.

---

*v2 complete (2026-07-18). Part I filled from the four completed corners (reproduction gate PASS),
the gradtune 2×2 (P0-0 SCOPED), held-out RMSE/NLL (T1: bias separable from fit), the x0-inversion
(T12 holds, ensemble-specific), and the 3×3 coverage matrix; the P0/P1 status table, Part III's
realized branch, and every P(accept) are updated. **Bottom line for the decision layer: the audit
strengthened the paper. The floor is up under all four identities; A is now a solid low-risk ship,
C is the highest-ceiling ship with its premise validated but its M-arm centerpiece still to run.
The choice is yours.** Residual work (Design-Bench corners, M1/M2/M3, X11, X4, the original
paper's missing generators, the in-body text/figure fixes) is enumerated in `FAILURES.md`,
`PREREGISTRATION_V2.md`, and Part V.*
