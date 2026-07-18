# Step 2.6 — Evidence redundancy audit (offline-mbo-novelty-audit-6d8cd4)

30 `claims-*.json` files across ~34 primary sources. This is a prior-art audit: each source is a
DISTINCT primary paper (the target of a novelty check), not derivative commentary on a shared
upstream. Independent-source redundancy is therefore inherently low. Clusters checked:

| Cluster | Members | Canonical upstream | Action |
|---|---|---|---|
| Deep-RL reproducibility | Henderson (AAAI18), Islam (ICML17-ws), Nagarajan (2018), Machado ALE (JAIR18) | Islam→Henderson→Nagarajan citation chain | KEEP all — each contributes a *distinct* confound axis (codebase-swap, hyperparam under-reporting, GPU-nondeterminism, ALE-determinism). Not derivative for N8. |
| Distance-aware uncertainty | SNGP, DUQ, DUE | SNGP (distance-awareness formalism) | KEEP all — DUQ (feature collapse), DUE (deep-kernel caveat) each add independent evidence for N4. |
| NTK/GP equivalence | Jacot, Lee | Neal 1996 (uncited leaf) | KEEP both — Jacot (NTK dynamics), Lee (∞-width→GP) are complementary for N5. |
| One-directional smoothing (offline MBO) | IGNITE, MS-DDEO, ROOT, Boosting-sensitivity (Dao ICML24) | Dao author lineage (IGNITE↔Boosting) | KEEP — corroborate N7's "nobody roughens" from independent angles; note IGNITE and Boosting share authors (partial dependence), so count as ~1.5 independent for N7. |
| Exact-duplicate paper fetches | Tan ×3, Henderson ×2, NTK ×2 | — | RESOLVED: NTK raw-dump deleted; 2 Tan copies deprecated; Henderson kept ×2 as distinct N1 + N8 analyses. |

**No atomic item drops below 2 independent sources after discounting.** N7's independent count is the
thinnest (IGNITE + MS-DDEO + ROOT ≈ 3, minus IGNITE/Boosting author-overlap) but remains ≥2. No Wave 3
needed. Flag for step 8 corpus critic: is there a NON-offline-MBO paper that roughens a smooth model to
prove a smoothness→performance causal link (e.g., in BO or kernel-method literature)? That is N7's
sharpest remaining exposure.
