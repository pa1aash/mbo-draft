# The interaction-ordering test — run because a critic demanded it, and it partially FAILS

**This is a correction to the audit's own lead recommendation, found by the dialectic critic and
confirmed by computation. It must reach the final report.**

## What the report claims

Rank 1 asserts the interaction is *"the second-largest effect in every corner"*, ordering
`surrogate > interaction > optimizer` **"without exception"**, and offers this as one of two
reasons the interaction is safe to promote.

## What was actually tested before now

The 33-combination normalizer sweep verified **only** `η²_surr > η²_opt`. It never tested the
three-way ordering. The interaction-grounding interim note names this exact check as its
falsifier and states it did not run. The dialectic critic caught the gap and predicted the
failure mode: Rank 5 concedes rank normalization roughly halves the interaction while η²_opt
rises ~3.4×, arithmetic that could invert the ordering.

## The test, run on the four corner artifacts

Two-way ANOVA on per-task normalized cell means, three normalizers × four engine corners.

| Corner | Normalizer | η²_surr | η²_opt | η²_inter | inter/opt | Ordering holds? |
|---|---|---|---|---|---|---|
| off/off | min–max | 0.367 | 0.013 | 0.165 | 12.4× | YES |
| off/off | z-score | 0.426 | 0.019 | 0.193 | 10.0× | YES |
| off/off | rank | 0.487 | 0.050 | 0.053 | 1.1× | YES (barely) |
| on/off | min–max | 0.283 | 0.036 | 0.146 | 4.0× | YES |
| on/off | z-score | 0.347 | 0.042 | 0.189 | 4.5× | YES |
| **on/off** | **rank** | **0.318** | **0.075** | **0.049** | **0.6×** | **NO — INVERTS** |
| off/on | min–max | 0.450 | 0.006 | 0.152 | 26.9× | YES |
| off/on | z-score | 0.494 | 0.008 | 0.167 | 20.6× | YES |
| off/on | rank | 0.524 | 0.021 | 0.062 | 2.9× | YES |
| on/on | min–max | 0.405 | 0.005 | 0.160 | 32.8× | YES |
| on/on | z-score | 0.454 | 0.003 | 0.179 | 71.3× | YES |
| on/on | rank | 0.388 | 0.017 | 0.071 | 4.1× | YES |

**11 of 12 hold. One inverts.** Under rank normalization in the on/off corner, the **optimizer
main effect (0.075) exceeds the interaction (0.049)**.

## What survives, stated precisely

- **`η²_surr > η²_opt` holds in all 12** — the original sweep's finding is untouched.
- **`η²_surr` is the largest effect in all 12** — the paper's headline ordering is safe.
- **The interaction exceeds the optimizer main effect in 11 of 12**, by 1.1× to 71.3×.
- **"Without exception" is FALSE** and must be struck.
- The failure is not random: it is the **rank** normalizer, which discards magnitude entirely, in
  the **on/off** corner — target scaling corrected, candidate protocol not. That corner also has
  the largest optimizer main effect under every normalizer (0.036 / 0.042 / 0.075), so it is the
  corner where the optimizer axis was always most competitive.

## The required fix to the report

1. **Strike "without exception."** Replace with: *the interaction exceeds the optimizer main
   effect in 11 of 12 corner-by-normalizer combinations, inverting only under rank normalization
   in the on/off corner, where the optimizer effect is largest under every normalizer.*
2. **Report this table.** It is a robustness check the paper does not have and can now cite, and
   it converts Rank 1 from an assertion into a tested claim.
3. **Keep the recommendation.** The interaction is still large, still second-largest in 11 of 12,
   still an order of magnitude above the optimizer effect in most combinations, and still
   uninterpreted in the paper. **The promotion survives; the absolutism does not.**

## Why this belongs in the report's methodology note

The critic did not find this by reading more sources. It found it by noticing that a claim's
supporting evidence tested a *different* proposition than the claim asserted — `η²_surr > η²_opt`
standing in for a three-way ordering. That is the same defect class the audit convicts the paper
of throughout: **a warrant that does not cover the claim it is attached to.** The audit committed
it in its own lead recommendation, and it took an adversarial critic plus fifteen lines of
computation to surface.
