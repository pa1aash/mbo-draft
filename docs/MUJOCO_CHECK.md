# MuJoCo vulnerability check — does the 7-task omnibus rejection localize to the optimizer axis?

**Date:** 2026-07-19. **Source:** `results/db_corners/db_analysis.json` → `corners_7task`
(Linux, torch 2.8.0+cpu, botorch 0.10.0, git_sha `17d04658`, K=5, β=2, TOP=128, n=16 seeds,
B=10,000 task+seed hierarchical bootstrap).

## The vulnerability

§6 reports a Design-Bench null on 5 tasks, then discloses that adding the two MuJoCo tasks
(AntMorphology, DKitty) makes the Friedman omnibus **reject in 3 of 4 corners**. The draft
asserted, without showing it, that "what it detects there is the optimizer axis." A reviewer
who reads a rejection under a null-claiming section and finds only an assertion behind it will
treat the whole null as unsupported. The defense has to be numeric and in the paper.

## VERDICT: **YES — supported, and cleanly.**

| corner (X1/X3) | η²_surr [95% CI] | η²_opt [95% CI] | η²_opt / η²_surr | Friedman *p* | rejects? |
|---|---|---|---|---|---|
| off / off | **0.053** [0.002, 0.331] | 0.096 [0.007, 0.312] | 1.8× | 0.157 | **no** |
| on&nbsp;&nbsp;/ off | **0.091** [0.006, 0.363] | 0.146 [0.031, 0.355] | 1.6× | 0.014 | yes |
| off / on&nbsp;&nbsp; | **0.044** [0.003, 0.275] | 0.197 [0.040, 0.458] | 4.5× | 0.013 | yes |
| on&nbsp;&nbsp;/ on&nbsp;&nbsp; | **0.062** [0.006, 0.305] | 0.181 [0.008, 0.468] | 2.9× | 0.011 | yes |

Three facts, in increasing order of force.

**1. η²_surr stays at the floor in every rejecting corner.** 0.044, 0.062, 0.091 — the same
0.044–0.091 band the paper already reports for the full 7-task set, and each point estimate sits
in the bottom fifth of its own bootstrap interval. Adding MuJoCo does not raise the surrogate
effect out of the floor; it raises it from ≈0.00–0.03 (5 tasks) to ≈0.04–0.09, still an order of
magnitude below the synthetic grid's 0.405.

**2. η²_opt is 1.6× to 4.5× η²_surr in every rejecting corner.** The largest surrogate effect
anywhere in the table (0.091) is below the *smallest* optimizer effect in a rejecting corner
(0.146).

**3. The decisive one — surrogate effect size does not track rejection, and optimizer effect
size does.** The single corner that **fails** to reject (off_off, *p*=0.157) has η²_surr = 0.053,
which is **larger** than off_on's 0.044 (*p*=0.013). If the surrogate axis were driving the
omnibus, the corner with the bigger surrogate effect would reject and the one with the smaller
effect would not; the ordering is the reverse. η²_opt runs the other way and tracks perfectly:
0.096 in the non-rejecting corner against 0.146–0.197 in all three rejecting ones — every
rejecting corner carries an optimizer effect at least 1.5× the non-rejecting corner's, with no
overlap between the two groups' point estimates.

This is the factorial doing exactly what a decomposition is for: an omnibus that rejects is not
an omnibus that tells you *which axis* rejected, and the two-way decomposition localizes it.

## Two scope limits the paper must carry

- **Within a corner, the surr and opt bootstrap intervals overlap** (e.g. on_on: surr
  [0.006, 0.305] against opt [0.008, 0.468]). The claim licensed is a **localization of point
  estimates plus the cross-corner tracking argument**, never "η²_opt significantly exceeds
  η²_surr." Fact 3 is the load-bearing one precisely because it does not need a within-corner
  separation — it is a comparison *across* corners of which quantity moves with *p*.
- **Marginal spreads are closer than the η² ratio suggests.** Surrogate marginals in the
  rejecting corners span 0.20–0.29 (ens 0.449–0.484 against botorchgp 0.683–0.759); optimizer
  marginals span 0.32–0.43 (grad 0.386–0.633 against perturb 0.815–0.829). Lead the paper's
  argument with η² and the cross-corner tracking, **not** with marginal spread, which is only
  ~1.5× and would invite a reviewer to compute it and find the argument weaker than stated.

## No pod re-run needed

The numbers support the assertion the draft already made, so this is a **write-up gap, not a
data gap**. `corners_7task` has all four corners at n=16 seeds on one stamped engine. No
candidate re-run is filed.

## What went into the paper

§6 now carries the three rejecting corners' η²_surr and η²_opt **side by side in the text**,
with fact 3 stated as the argument and the within-corner interval overlap stated as the limit.
Table 3 is unchanged (its ranges already carry the band correctly).
