# Step 2.5 — Coverage check (offline-mbo-novelty-audit-6d8cd4)

Corpus = 33 vault notes, ~30 grep-verified primary sources (full body text) + AAAI-27 topics page.
This is a focused prior-art AUDIT: the source-count target table (45+ for full tier) is calibrated
for broad topical sweeps; here every atomic item is a specific novelty claim whose nearest-neighbor
prior art is largely enumerable. The bar that matters: every claim ≥3 relevant primary sources.

| Claim | Sources | Status |
|---|---|---|
| N1 confound-taxonomy shape | Ferrari Dacrema (RecSys19), Balduzzi (NeurIPS18), Henderson (AAAI18), Musgrave (ECCV20), Lucic (NeurIPS18), Agarwal (NeurIPS21) | **Well-covered** (6) |
| N2 K-contingency of ranking | Abe (NeurIPS22), Lakshminarayanan (NeurIPS17), Li/Rudner/Wilson (ICLR24, surrogate compare) | Adequate (3) |
| N3 unmatched effective pessimism | "Why So Pessimistic? …Offline RL through Ensembles", SNGP/DUE (σ-scale), + W3 search log (pending) | Adequate (2-3, pending W3) |
| N4 distance-aware / implicit TR | SNGP (NeurIPS20), DUQ (ICML20), DUE (2021), TuRBO (NeurIPS19) | **Well-covered** (4) |
| N5 NTK / spectral bias | Jacot (NeurIPS18), Rahaman (ICML19), Lee (ICLR18), Li/Rudner/Wilson (ICLR24), Abe (NeurIPS22) | **Well-covered** (5) |
| N6 crossed surrogate×optimizer factorial | Design-Bench (ICML22), Chemingui/PGS (AAAI24), Tan/RaM (ICLR25), Kim survey (TMLR26), Li/Rudner/Wilson (ICLR24) | **Well-covered** (5) |
| N7 bidirectional smoothness manipulation | IGNITE (NeurIPS24), MS-DDEO (SWEVO22), [sibling: Dao et al "surrogate sensitivity" ICML24 — not yet fetched], + W1 forward-cite (pending) | Adequate (2-3) |
| N8 platform/library-version dependence | Gundersen & Kjensmo (AAAI18), Nondeterminism-in-Deep-RL, Reproducibility-of-Benchmarked-Deep-RL, Revisiting-ALE (2018) | **Well-covered** (4) |
| N9 audit that strengthens | Recht (ICML19), Melis (ICLR18), Agarwal (NeurIPS21) + reality-check genre (Ferrari/Musgrave/Lucic) | **Well-covered** (3-6) |

**FINAL (post W1/W3): No `uncovered` atomic items; no `thin` items.** N3 topped up by Ghasemipour
(NeurIPS22); N7 topped up by ROOT (NeurIPS25) + Dao "surrogate sensitivity" (ICML24). N9 gained
Bressan (Front. Psychol. 2019). All nine claims are Adequate-to-Well-covered.
Remaining N7 exposure for step-8 corpus critic: a NON-offline-MBO paper that ROUGHENS a smooth model
to prove a smoothness→performance causal link (BO / kernel-method literature).

**Housekeeping:** duplicate NTK note file (`…neural-network.md` + `…neural-network-2.md`) — leave for
`hyperresearch repair` dedup; does not affect coverage.
