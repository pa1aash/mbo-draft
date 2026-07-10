# Literature Review: Unified Conservative Framework for Offline-to-Online Decision-Making

## Summary

This review synthesizes findings across five facets of the research landscape at the intersection of offline reinforcement learning (RL), offline model-based optimization (MBO), uncertainty quantification, and LLM alignment — the core themes of the ICML 2026 Workshop on Decision-Making from Offline Datasets.

**The central insight across all facets is that pessimism/conservatism under distributional shift is the dominant unifying principle.** In offline RL, CQL (Kumar et al., 2020) learns Q-functions that provably lower-bound true policy values; in offline MBO, COMs (Trabucco et al., 2021) learn surrogates that lower-bound true objective values on OOD inputs. These are structurally identical — offline MBO can be viewed as a single-step MDP where the "action" is the design and the "reward" is the objective. Despite this deep parallel, **no formal theoretical framework unifies both settings under shared optimality guarantees**, and algorithms have been developed largely independently.

Three algorithmic paradigms appear across both fields: (1) **value/score regularization** (CQL → COMs), (2) **policy/design constraints** (BEAR, TD3+BC → CbAS, RoMA), and (3) **generative/conditioning-based methods** (Decision Transformer, Diffuser → DDOM, BONET). The theoretical foundations for pessimism are well-established in offline RL (Jin et al., 2021; Rashidinejad et al., 2021) but nascent in offline MBO.

**Uncertainty quantification** is the mechanism enabling conservatism: deep ensembles remain the workhorse (Lakshminarayanan et al., 2017), while emerging conformal prediction methods (Taufiq et al., 2022) offer distribution-free guarantees not yet applied to MBO. A critical gap is **calibration-aware conservatism** — no method jointly optimizes uncertainty calibration with the degree of pessimism.

**LLM alignment** provides a massive-scale application of these principles: DPO/KTO/SimPO are offline preference optimization, reward overoptimization (Gao et al., 2022) mirrors surrogate overestimation, and KL penalties serve as conservatism. Yet the offline MBO toolkit (COMs, adaptive trust regions, learned lower bounds) has not been systematically applied to alignment.

**The offline-to-online transition** is the key emerging challenge: Cal-QL (Nakamoto et al., 2023) shows calibrated conservatism helps, RLPD (Ball et al., 2023) shows simple replay design may suffice, and in LLMs, iterative DPO (Xiong et al., 2024) bridges offline preference learning to online RLHF. No unified framework addresses this transition across both RL and MBO.

## Key Findings by Facet

### Facet 1: Conservative Methods in Offline RL
- CQL adds a Q-value regularizer that provably lower-bounds policy value (~2500+ citations)
- IQL avoids OOD evaluation entirely via expectile regression (~1370 citations)
- TD3+BC: minimalist behavior cloning term matches complex methods (~1100 citations)
- Model-based pessimism (MOPO, MOReL, COMBO) uses ensemble uncertainty or value regularization on model rollouts
- Theoretical: PEVI (Jin et al., 2021) proves minimax optimality of pessimism; LCB (Rashidinejad et al., 2021) achieves adaptive 1/N rates for near-expert data
- Offline-to-online: Cal-QL introduces calibrated conservatism; RLPD shows symmetric replay may make explicit pessimism unnecessary

### Facet 2: Offline Model-Based Optimization (MBO)
- COMs (Trabucco et al., 2021) learn conservative surrogates directly inspired by CQL
- Three paradigms: forward-model (COMs, RoMA, BDI), inverse-model (MINs), conditioning-based (CbAS, DDOM)
- Design-Bench provides standardized evaluation across biology, materials, robotics
- Recent: ranking-based methods (Tan et al., 2025, ICLR 2025) outperform 20+ methods; diffusion-based DDOM competitive at ICML 2023
- First comprehensive survey published (Kim et al., 2025)
- Explicit connection: offline MBO = single-step MDP, conservatism transfers from offline RL

### Facet 3: Unification Attempts between RL and MBO
- COMs paper (Trabucco et al., 2021) explicitly cites CQL and draws the conservatism parallel
- PGGS (Chemingui et al., 2024, AAAI) most explicit unification: reformulates MBO gradient search as offline RL
- Generative models (Diffuser, Decision Transformer, DDOM, BONET) provide a shared algorithmic substrate
- Return-conditioned supervised learning (RCSL) theory (Brandfonbrener et al., 2022) directly applicable to score-conditioned MBO
- **GAP: No unified theoretical framework with shared optimality guarantees across both settings**

### Facet 4: Uncertainty Quantification for Decision-Making
- Deep ensembles (Lakshminarayanan et al., 2017; 7300+ citations) dominate in practice
- MOPO/MOReL use ensemble disagreement for pessimistic rewards; EDAC scales to 10+ Q-ensemble members
- Epistemic vs. aleatoric decomposition (Kendall & Gal, 2017) — conservatism should target only epistemic uncertainty
- Conformal prediction for bandits (COPP; Taufiq et al., 2022) offers distribution-free guarantees
- COMBO avoids explicit UQ entirely via value regularization
- **GAP: Conformal methods not applied to MBO; calibration-conservatism tradeoff poorly understood**

### Facet 5: LLM Alignment as Offline Optimization
- DPO (Rafailov et al., 2023) = closed-form solution to KL-constrained offline RL
- Reward overoptimization (Gao et al., 2022) structurally identical to surrogate overestimation in MBO
- Reward model ensembles reduce overoptimization by ~70% (Coste et al., 2024)
- Best-of-N = offline black-box optimization with proxy scoring (BoNBoN, BOND)
- Pessimistic DPO (Houliston et al., 2024) explicitly draws on offline RL pessimism
- **GAP: No systematic application of MBO methods (COMs, CbAS, RoMA) to alignment; no formal theory connecting overoptimization scaling laws to MBO surrogacy theory**

## Identified Gaps & Opportunities

1. **No unified framework**: Despite structural parallels, no paper provides a single mathematical framework that subsumes offline RL conservatism (CQL/IQL) and offline MBO conservatism (COMs/RoMA) with shared theoretical guarantees.

2. **Adaptive conservatism across domains**: Cal-QL (RL) and fixed-α COMs (MBO) both use static conservatism levels. Data-dependent, state/design-adaptive pessimism is underexplored in both fields.

3. **Offline-to-online transfer is studied separately**: Cal-QL/RLPD (RL) and iterative DPO (LLMs) address offline-to-online transition but there's no cross-domain framework for when and how to relax conservatism during online adaptation.

4. **Uncertainty calibration gap**: Deep ensembles are miscalibrated (Guo et al., 2017); conformal prediction offers guarantees but hasn't been applied to MBO or multi-step RL. Epistemic-only pessimism (penalizing only model uncertainty, not data noise) is theoretically motivated but rarely implemented.

5. **Cross-pollination of algorithmic ideas**: RL→MBO transfer is limited to CQL→COMs. Missing: IQL-style implicit conservatism for MBO, OptiDICE-style distribution correction for MBO, ensemble Q-learning (EDAC) for design scoring. MBO→RL transfer is even more sparse.

6. **Benchmarks are siloed**: D4RL (RL) and Design-Bench (MBO) are separate ecosystems. A unified benchmark covering the single-step to multi-step spectrum would accelerate cross-community research.

7. **LLM alignment as a testbed**: The workshop specifically highlights LLM connections. Applying offline MBO methods to preference optimization and vice versa is a clear, unexplored direction with high impact potential.

## Complete References
[See individual facet BibTeX entries — over 75 unique papers cited across all facets]
