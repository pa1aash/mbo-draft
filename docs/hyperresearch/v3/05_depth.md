# Step 5 — Depth investigation

Run `mbo-gauntlet-r4-adversarial-0f06f1` · branch `gauntlet-r4` · 2026-07-20

## Output

**6 of 6 interim notes**, all tagged `mbo-gauntlet-r4-adversarial-0f06f1`, all ending in
`## Committed position` with confidence and falsifiers.

| Locus | Committed position |
|---|---|
| `n6-residual-scoping` (dialectical) | **DEFENSIBLE-BUT-MUST-BE-ARGUED.** Ground (2) falsified; grounds (1) and (3) survive with new support. |
| `minmax-normalization-fragility` (dialectical) | **Methodologically fragile, empirically robust in direction.** 33/33 combinations preserve η²_surr > η²_opt. |
| `interaction-grounding` | **Promote to cited, interpreted main-text finding — not the abstract headline — scoped to the synthetic grid.** |
| `ntk-width-citations` | 3 of 4 faithful; **Rahaman miscited in effect.** |
| `landscape-predicts-winner` | **Decisive quantified negative.** FOLD-IN cheap (report it) + FOLLOW-UP expensive. |
| `aaai-venue-fit` | Genre framing is necessary but not sufficient at AAAI; **lead with a positive result.** |

## Four corrections to the orchestrator

Recording these prominently because they are the clearest evidence the depth phase did
independent work rather than ratifying my priors.

1. **N6 ground (2) was my error.** I claimed the nine RaM Table 3 methods are all bundled and
   not a clean optimizer factor. RaM's own appendix describes **four of them** (BO-qEI, CMA-ES,
   REINFORCE, Grad. Ascent) as *"baselines that optimize a trained model"* — a clean 4×2 crossed
   sub-grid does exist. Withdrawn. Grounds (1) and (3) survive, now with an η² computed from
   RaM's own published table (loss axis 0.027 vs method axis 0.577) and a domain citation
   (Abdar et al. 2021 catalogues method-family and loss-function as orthogonal axes).
2. **The interaction is synthetic-grid-specific.** Design-Bench η²_inter is 0.006–0.041 — an
   order of magnitude smaller and subordinate to η²_opt there. I had been treating it as
   general. It cannot be promoted unscoped. This is consistent with the frozen cells: a frozen
   surrogate cannot interact.
3. **Griewank is the smallest lever, not the largest.** I raised the normalization alarm on
   Griewank-30D's 2,780× outlier spread. Recomputation shows it is empirically the *least*
   influential task on the headline.
4. **My 7/7 raw-units result has a formal counterpart.** Locus 3 computed the per-optimizer
   simple-effects table from stored per-seed data: surrogate effect ≈0.01 under perturbation
   against 0.4–0.8 under gradient/CMA. Bootstrapped, with intervals, which mine lacked. That is
   the version the paper should report — though it does not dissolve the floor-effect confound.

## New citable material the loci found

- **NIST/SEMATECH DOE handbook §5.2.1.2** (one-variable-at-a-time) and **Box 1989, "Do
  Interactions Matter?"** — the positive methodological grounding the paper lacks. It currently
  has only Moosbauer's negative framing and **zero DOE/ANOVA citations anywhere**.
- **Jordan et al. 2020** — names the paper's exact endogenous min–max form as
  outlier-exploitable. **Bellemare et al. 2013 (ALE)** — the technique's origin, documenting it
  flipping a ranking (Zaxxon).
- **McClelland & Judd 1993 / Sommet et al. 2023** on interaction-detection power, which read
  carefully argue *for* trusting this interaction: it is large relative to typical effects and
  sits in a manipulated rather than observational design.
- **Abdar et al. 2021** UQ survey — the domain citation for treating model-class and
  loss-function as orthogonal axes.

## A process note that belongs in the report

Midway through this step I set a waiter for "six `interim-*` notes exist". It fired on **six
stale interim notes from the prior audit run**, whose committed positions are seductively
on-topic (N9 integrity, K-vs-width, σ mechanism scope). Reading them uncritically would have
imported the previous pass's verdicts into this run's synthesis — the exact failure the query's
method constraints forbid. Caught by the filename convention mismatch; every waiter and read now
filters on the vault tag. **The instruction to distrust the prior pass has paid for itself
twice**, here and on RaM Table 3.

## Next

Step 6 — cross-locus reconciliation.
