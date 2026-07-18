# Step 5 — Depth Investigation (offline-mbo-novelty-audit-6d8cd4)

6 depth investigators, one per locus. Each read full source bodies and fetched gap-sources within
budget (Ovadia 2019, Srinivas GP-UCB 2010, Shahriari 2016, Robinson/Glen/Lee 2019, Lim et al. 2021,
Fort 2019, Lee 2019). Interim notes: `research/notes/interim-report-*.md`. Committed positions:

## L1 — k-and-finite-width-artifact-vs-class-property (N2+N5) → favors D over C (~65%)
The N5 "K-sweep proves finite-width artifact" argument is a **category error: ensemble cardinality
K ≠ per-member width n** (code: each member is a 2-layer MLP, HID=96; NTK/spectral bias is about
width→∞, mentions ensembles 0 times). The K-decline (0.95→0.18 as K rises 2→10) runs *backward*
from Lakshminarayanan's and L/R/W's own K-sweeps → most parsimonious read = small-K σ-estimation
noise, not a width law. **N2 = NONE FOUND** (L/R/W's K-robustness pre-empts it in *strength*, not
existence; verbatim Fig A.7). Draft implication: don't frame the K-sweep as finite-width evidence;
the missing experiment is a *width* ablation (sweep HID). New fetches: Fort 2019 (1912.02757),
Lee 2019 (1902.06720).

## L2 — n4-sigma-mechanism-scope-and-ovadia (N4) → split verdict
DUE scope-catch **holds in the paper's favor** (DUE's "GP not auto variance-growing" is about
deep-kernel GPs; the paper uses vanilla Matérn on raw inputs — verified in code). Raw distance-aware
mechanism = **PRIOR WORK FOUND** (SNGP proof; DUQ two-moons). Causal "LCB + variance growth =
implicit trust region" synthesis = **NONE FOUND**, contradicted by β=0 + TuRBO's explicit-TR fix.
**Ovadia 2019 (fetched) complicates** "ensembles confidently wrong far from data" (its "far" =
corruption severity, not spatial distance). β=0 exact numbers **NOT VERIFIABLE** (repro gave
0.504→0.511, not the cited 0.51→0.47; being recomputed).

## L3 — audit-strengthens-and-n9-integrity (N9) → narrow claim safe (~75-80%)
Integrity fix: unverified citation (Robinson/Glen/Lee, arXiv:1905.11681) **fetched+grepped** →
clean shrink, no fabrication stands. **N9 narrow claim** ("a confound-controlled audit whose
corrected *scalar* effect-size exceeds its published value, within ML/CS") = unclaimed, safe.
**N9 broad claim** ("reality-checks always shrink, ours is the exception") = FALSE — must pre-empt
Recht (relative slope) + Agarwal (power-revealed) directly; Bressan = closest full-shape precedent
but outside ML/CS.

## L4 — n7-roughening-beyond-offline-mbo (N7) → NONE FOUND at broadest scope (med-high)
No paper in BO / kernel methods / GP regression combines within-GP smoothness sweeps and
cross-surrogate-class comparison into one controlled bidirectionally-manipulated causal experiment
(~20 API + 7 WebSearch queries). Closest prior (new find): **Lim et al., Adv. Intell. Syst. 2021**
— a GP-vs-NN-ensemble BO comparison that *hypothesizes* the GP wins "due to the ability of GP to
smoothly map out the uncertainty manifolds" but never manipulates smoothness. → C can claim "first
at all" to manipulate bidirectionally, citing Lim et al. as closest prior.

## L5 — optimizer-reversal-unearned-and-candidate-a-credit → A under-credited; reversal overclaims
No offline-MBO paper owns A's "surrogate effect, not an optimizer effect" attribution (PGS fixes
surrogate; L/R/W fixes acquisition as nuisance + is online BO; Tan/Design-Bench bundle both; Kim
survey names it unresolved) → **A is under-credited** by "just an ablation." BUT **Shahriari et al.
2016** (most-cited BO survey; fetched) already holds *as doctrine* that surrogate > acquisition →
the "reversal" overclaims. Honest framing: falsify **PGS's local premise**, not the field's belief.
**A's one owned sentence:** "the first offline-MBO-specific, ANOVA-quantified attribution of the
surrogate-vs-optimizer variance under a shared protocol."

## L6 — n3-classic-bo-beta-calibration (N3) → NONE FOUND (>80% classic BO)
Srinivas GP-UCB (2010, fetched): β_t is a *single-surrogate, time-indexed* schedule (0 hits
"surrogate"/"ensemble"/"calibrat"). Lu et al. (TPAMI 2023) + Benechehab et al. bring multiple
estimator classes into contact but fuse/winner-pick, never hold one shared β fixed to diagnose the
mismatch. **N3 = NONE FOUND** for the cross-surrogate-class σ-mismatch framing. Open: conformal /
statistical-calibration literature unfetched (adjacent) → terminal "could not verify".
