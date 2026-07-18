# Pre-registration — revision experiments

Written BEFORE the runs. If a result contradicts a prediction here, that is a finding to
report, not a prediction to revise. Amendments require a dated entry at the bottom, not a
silent edit. Companion to `docs/MECHANISM_EXPERIMENTS.md` and `docs/EXTENSION_LEDGER.md`.

Precedent: the original `PREREGISTRATION.md` registered "the optimizer explains most of the
gap." The data gave eta2_opt = 0.01 — refuted. That refutation is an asset if disclosed. This
file exists so the same thing can happen again, visibly.

| ID | Prediction | Kill criterion |
|---|---|---|
| **X1** (M0, normalize ensemble targets) | eta2_surr drops materially from 0.37. The per-task GP-ensemble gap correlates with log\|y\|_scale BEFORE the fix (rho > 0.6) and not after (rho ~ 0). | If eta2_surr stays ~0.37 AND the gap does not track \|y\| scale, the target-scaling confound is REFUTED and the headline stands strengthened. Report as a passed control. |
| **X3** (equalize candidate/oracle protocol) | Ens x CMA improves relative to Ens x Grad once CMA stops being scored on a full-set median against a top-half median; eta2_inter shrinks. | If nothing moves, the protocol asymmetry was harmless. Report it and stop citing it as a flaw. |
| **X6** (M2, roughen the GP) | A Matern-1/2 GP (or fixed short lengthscale) COLLAPSES under gradient ascent; its premise coverage on its own proposals drops from 0.97. | If the rough GP stays robust, the mechanism is NOT prior smoothness. Identity C's thesis dies. Report it. |
| **X5** (M3, smoothness interpolation) | As alpha rises, all four move together and monotonically: gap shrinks, eta2_surr falls, c_ood falls, Friedman p rises toward non-significance. Design-Bench is reproduced as a limit point. | If the four move independently or non-monotonically, prior-match is not one axis and the unification fails. |
| **X7** (full 3x3 coverage) | The ensemble's premise coverage is ALSO low (~0.4) on CMA proposals; c_ood correlates with normalized score across all 9 cells. | If Ens x CMA coverage is high, "any aggressive optimizer exploits a jagged mean" is refuted and the gradient-specific framing is vindicated. |
| **X8** (M5, density ratio) | The learned ratio PARTIALLY but not fully restores proposal coverage; w is unbounded on the proposal region and ESS collapses. | Full restoration = a positive result the paper lacks. No effect = the shift defeats density-ratio methods, a sharper negative. All three outcomes are publishable; only "we did not try" is not. |
| **X10** (M6, coverage bound) | A bound of the form c_ood degradation <= Phi(L, D, beta, sigma_min) is derivable and TRACKS the realized c_ood when plotted. | If the bound is vacuous for unregularized ensembles — the LIKELY outcome — report that no non-vacuous bound was found. Do NOT manufacture a theorem. |
| **M1** (smooth the ensemble, hold sigma) | Spectral-norm / gradient-penalty / input-smoothing regularization of the ensemble RAISES its premise coverage on its own gradient proposals and SHRINKS the ensemble x gradient collapse, WITHOUT closing the sigma gap — isolating smoothness from calibration. | If smoothing the ensemble does NOT reduce the collapse, smoothness of the MEAN is not the operative axis (Identity C's forward direction fails). Report it. |
| **X11** (null on the exact-oracle subset) | On TF-Bind-8/10 (exact oracles, no RF surrogate), the Design-Bench cross-cell null PERSISTS and the effect size is small relative to the oracle noise floor — killing the "your RF oracles manufactured the null" competing mechanism. | If the exact-oracle subset shows LARGE, resolvable cell differences, the null IS an RF-oracle artifact; concede it and re-scope Contribution 3. |
| **X4** (power over task count) | A power analysis at the observed synthetic effect sizes shows N=7 tasks is underpowered to resolve the Design-Bench grid (power well below 0.8), quantifying the "underpowered at N=7" claim rather than asserting it. | If N=7 is already adequately powered at the observed effect size, the "underpowered" framing is wrong and the DB result is a genuine equivalence, not an unresolved one — a DIFFERENT (stronger) claim. Report which. |

## Standing commitments

1. **X1 runs before anything else is interpreted.** No result below it is trusted until it lands.
2. **The gradtune sweep is reported regardless of outcome** (`FLAW_LEDGER.md` P0-0). It already ran
   and already failed its own pre-stated rule; that is not renegotiable.
3. **GFP is quarantined from headline coverage claims** unless the degenerate decode is fixed.
4. **No DB seed-dependent significance claims**, per the original `PREREGISTRATION.md:50-52`, which
   the current draft violates.
5. **Multiplicity is disclosed.** 5.1 ran 10 rules on n=14 and reported all 10. Any future rule
   search reports every rule tried, not the best.
6. **5.1 is reported as a dropped stretch goal**, per its own kill criterion — including the
   obstruction finding (the predictive signal is not oracle-free), which is the part worth keeping.

## Amendment — 2026-07-17 (blueprint session)

Added M1 (smooth-the-ensemble forward test), X11 (exact-oracle-subset null + oracle noise
floor), and X4 (power over task count) as pre-registered CONTINGENT arms, BEFORE any of them
runs. These are Phase A.2 arms whose launch is gated on the four-corners result: M1/M2(X6)/
M3(X5) form the smoothness-mechanism triad (Identity C); X11 kills the RF-oracle competing
mechanism for the Design-Bench null (Identity A/D Contribution 3); X4 quantifies the N=7
underpowered claim. The four-corners gate itself (X1/X3) was launched this session; its
result and the resulting Part-III decision rule are committed with a timestamp in
docs/AAAI_BLUEPRINT.md Part III BEFORE the corner data was read.

## Amendment — 2026-07-18 (GP-freeze mechanism, platform-arm session)

Registered BEFORE Step 1 runs. On most Design-Bench tasks the BoTorch/exact GP returns the
same score regardless of which optimizer drives it (Table 3: TF-Bind-8 1.00 x3, UTR 0.99 x3,
Ant 1.52 x3, GFP ~2.45 x3), and on TF-Bind-8 that 1.00 is exactly the normalized dataset best
(`docs/DEGENERATE_CELLS.md`). If the GP never leaves the data, `eta2_opt ~ 0` on Design-Bench
means "the optimizer CANNOT matter" (frozen cells), not "the optimizer does not matter"
(method equivalence), and the Friedman p=0.69 omnibus may be a power artifact of cells tied at
an identical constant. Three candidate mechanisms, to be SEPARATED, not confirmed: M-A LCB
paralysis (GP sigma ~ 0 at the data and grows away, so LCB = mu - beta*sigma is locally
maximal AT the top-128 init points, mbo.py init_candidates); M-B decode snap-back (movement in
the relaxed logit space that argmax-decodes back to x0 unchanged, db_tasks.py); M-C neither.
Control that separates them: Superconductor is CONTINUOUS (86-dim, no argmax decode) and its GP
cells are NOT degenerate (1.24/1.31/1.26 differ); TF-Bind-8 and UTR are discrete and ARE
degenerate. A freeze that is M-A should not care whether the task is discrete; M-B can only
occur with a decode step. Known complication, stated not argued away: Ant is continuous AND
degenerate (1.52 x3), which cuts against M-B, but Ant needs mujoco and is pod-only, so it
cannot be tested on this machine. The gap is noted, not resolved by argument.

| ID | Prediction | Kill criterion |
|---|---|---|
| **DB1** | At beta=2 on TF-Bind-8 and UTR, all three botorchgp cells return designs whose DECODED form is identical to their x0 initialization on >90% of the 128 returned designs, every seed. | If the returned designs differ from x0 but still score exactly 1.00, the constant is a coincidence of normalization, not retrieval, and this whole line dies. |
| **DB2** | At beta=0 the GP cells stop being constant: they differ across optimizers by more than seed noise, and p100 != 1.00. | If the GP cells are STILL constant at beta=0, sigma is not the cause and M-A is refuted. |
| **DB3** | On Superconductor (continuous, non-degenerate) GP displacement at beta=2 is already >0 and the cells already differ — i.e. no freeze without a decode step. | If Superconductor's GP also freezes, the mechanism is M-A (LCB paralysis) and is not decode-related at all. That is the more interesting outcome. |
| **DB4** | The ensemble does NOT freeze anywhere (it scores 2.20 on TF-Bind-8, well above the dataset best), because its jagged mean has spurious optima away from the data that gradient ascent can reach. | If the ensemble also freezes at beta=2, the freeze is a protocol property, not a surrogate property. |

Step order committed: Step 1 (botorchgp:grad displacement + decode-identity on TF-Bind-8,
beta=2, X1/X3 on, n=16) reports M-A vs M-B BEFORE Step 2 (beta contrast over
TF-Bind-8 / UTR / Superconductor, all 9 cells, beta in {0, 2}, n=16) launches.
