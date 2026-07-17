# AAAI-27 Blueprint — "Decomposing the GP Advantage in Offline MBO"

**Version 1 (2026-07-17, experiments in flight).** Part I is marked PENDING where the
four-corners gate has not yet landed; the pieces already on disk (the do-nothing baseline,
the committed (on,on) audited corner, the reproduction tolerance) are filled. Part III (the
decision tree) is **pre-committed here, with a timestamp, BEFORE any corner data was read** —
that is deliberate and is itself a disclosable credibility asset (see Part III).

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

## PART I — GROUND TRUTH (from Phase A)  ·  **v1: PARTIAL, gate in flight**

> **Status:** the four-corners run (`code/run_corners.py`) is executing on the session's
> macOS venv. (on,on) is the committed camera and is analyzed below; (off,off)/(on,off)/(off,on)
> are PENDING. v2 replaces every PENDING with numbers. **No number here is inferred** — PENDING
> means not-yet-computed, not "assumed."

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
- **VERDICT: PENDING** (off,off not yet complete).

### The four corners — full results
**PENDING for off_off / on_off / off_on.** Filled and analyzed in v2. What is already on disk:

**(on,on) — the committed audited camera corner** (`results/results_camera.json`, verified
sha256 73ce3be9…): η²_surr = **0.369**, η²_opt = **0.013**, η²_inter = **0.165**, Friedman
p = **6.09e-5**, ρ(per-task GP-ens gap, log|y|scale) = **+0.536**.
→ **Preview finding (subject to the disentangling corners): the two biggest confounds, once
fixed together, leave the headline surrogate main effect essentially unchanged (0.37 → 0.369).**
This is the "passed control, headline strengthened" branch of the X1 pre-registration — *if*
off_off reproduces 0.37 and the X1-alone corner confirms it. The single-corner number cannot
yet attribute X1 vs X3; that is what on_off / off_on decide.

### Pre-registered ρ test (X1 confound) — verdict PENDING
Prediction (`PREREGISTRATION_V2.md` X1): ρ>0.6 in X1-OFF corners, ρ≈0 in X1-ON corners ⇒
confound confirmed; ρ unchanged ⇒ confound refuted, headline strengthened. The (on,on)
X1-ON corner already shows ρ=+0.536 (not ≈0), which **leans toward "refuted / headline
strengthened"** — but the off_off / off_on (X1-OFF) ρ values are required to close it. PENDING.

### gradtune under X1 (P0-0) — verdict PENDING
`code/gradtune.py` extended to all 7 tasks with `--out`, to be run under MBO_X1=0 and MBO_X1=1
(the 2×2 that makes P0-0's status attributable). Judged against the script's own rule
(`gradtune.py:67`). **P0-0 verdict: PENDING** (CONFIRMED / REFUTED / SCOPED to follow).

### Held-out RMSE/NLL (T1) — PENDING
`code/heldout.py` computes normRMSE / NLL_norm / ρ(σ,|μ−f|) per (task, surrogate, X1). The T1
question — is "inductive bias" separable from "fits worse" — is answered by whether the
ensemble's normRMSE converges to the GP's under X1-on. **PENDING.**

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

### x0 inversion (T12) — PENDING
`code/x0_inversion.py` on the audited (X1,X3-on) engine, ens:grad/perturb + GP contrast.
**PENDING.**

### 3×3 coverage matrix + (ĉ_ood, score) scatter — PENDING
`code/coverage33.py`: full 3×3, grid's botorchgp, reference from D (P0-5 fix), both X1 states.
**PENDING.**

### Post-experiment status of every P0/P1 — PENDING (framework below, filled in v2)
| flaw | pre-experiment | expected resolver | v2 status |
|---|---|---|---|
| P0-0 gradtune refutes mechanism | UNRESOLVED | gradtune 2×2 | PENDING |
| P0-1 candidate/oracle protocol | confound | X3 corner (off_on vs off_off) | PENDING |
| P0-2 target scaling | confound | X1 corner (on_off vs off_off) + heldout | PENDING (preview: (on,on) η²_surr intact) |
| P0-3 1/9 coverage cells | confound | coverage33 | PENDING |
| P0-4 numbers w/o generator | live | (generators now exist for the new arms) | PARTIAL |
| P0-5 uniform reference set | invalid | coverage33 (reference from D) | code-fixed, values PENDING |
| P0-6 Fig1≠Fig3 ranks | integrity | regenerate from one source | not yet |
| P0-7 backwards sentence | false stmt | text fix (not this session) | open |
| P1-1 unmatched query budget | confound | (residual, Part V) | open |
| P1-2 hand-rolled ANOVA | stats | proper effect size | analyzer replicates paper method; proper version TODO |
| P1-3 no held-out error | MISSING | heldout | PENDING |
| P1-5 refuted pre-reg undisclosed | disclosure | one paragraph | trivially fixable |

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

### Scoreboard (for the reader — not a recommendation)
| Identity | Reviewer composite | P(accept) | Novelty | Experiment cost | Key risk |
|---|---|---|---|---|---|
| A Repaired | 4.7 | 0.30 | findings owned | medium | mechanism hollow (P0-0) |
| C Mechanism | 5.3 | 0.35 / 0.12 | cleanest move, fragile | **highest** | M2 refutes |
| D Taxonomy | 5.0 | 0.32 | most exposed | medium | confounds don't move ranking |
| E Reversal | 4.7 | 0.25 / 0.40 hybrid | un-novel, un-exposed | **lowest** | no artifact |

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

**Reading the tree against the preview:** the currently-favored path is *X1 intact →
A/C viable*, with the C-vs-A fork decided by gradtune-under-X1. If gradtune-under-X1 still
closes the collapse, the honest ship is **A + E-framing** (measurement, P0-0 disclosed as a
scoped limitation, reversal foregrounded). If gradtune-under-X1 does NOT close it, **C** opens
up as the highest-ceiling ship. This is a *pre-commitment*, not a prediction — the off_off /
on_off / off_on data (v2) decides.

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

*v1 ends here. v2 fills Part I from the completed corners, gradtune 2×2, held-out, x0-inversion,
and coverage33, and updates the P0/P1 status table, Part III's realized branch, and every
P(accept) that the gate revises.*
