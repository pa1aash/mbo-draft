# Research Deliberation: Unified Conservative Framework for Offline-to-Online Decision-Making

## Knowledge Consolidation

The literature reveals a deep structural parallel between offline RL and offline MBO that has been recognized informally but not exploited algorithmically in a systematic way:

**What is established:**
- Offline MBO is formally a single-step MDP (select design x, receive reward f(x))
- CQL-style conservatism (learn lower-bounded value functions) transfers directly to COMs (learn lower-bounded surrogates)
- Pessimism is provably minimax-optimal for offline RL (Jin et al., 2021; Rashidinejad et al., 2021)
- Deep ensembles are the dominant UQ method in both fields
- Three paradigms exist in both fields: value/score regularization, policy/design constraints, generative conditioning
- Offline-to-online transition is an active area in RL (Cal-QL, RLPD) but barely explored in MBO

**What is contested:**
- Whether explicit pessimism is necessary or if simple replay design suffices (CQL vs. RLPD)
- Whether regression surrogates or ranking-based models are better for MBO (Tan et al., 2025 challenge the regression paradigm)
- Whether conservatism should be fixed or adaptive

**What is unknown:**
- Whether cross-domain transfer of conservatism strategies (RL→MBO or MBO→RL) yields practical improvements
- How to optimally schedule conservatism during offline-to-online adaptation in EITHER field
- Whether a single algorithm can perform well across both D4RL and Design-Bench

## Knowledge Gaps & Contradictions

- **Gap 1**: No algorithm has been evaluated on BOTH D4RL and Design-Bench benchmarks. The communities are completely siloed in evaluation.
- **Gap 2**: Offline-to-online adaptation is studied in RL but not in MBO. In practice, after offline MBO proposes designs, one often evaluates a few candidates and iterates — this is offline-to-online MBO, but no method addresses it formally.
- **Gap 3**: IQL-style implicit conservatism (expectile regression, never evaluate OOD) has never been applied to MBO, despite being one of the strongest offline RL methods.
- **Contradiction**: RLPD claims pessimism is unnecessary with proper replay; Cal-QL claims calibrated pessimism is essential. Both show strong results. The resolution likely depends on dataset quality and coverage.

## Candidate Hypotheses

### Hypothesis 1: Uncertainty-Guided Adaptive Conservatism (UGAC) transfers across RL and MBO
- **Statement**: A single conservatism mechanism based on ensemble uncertainty that ADAPTS its pessimism level based on local data density can improve performance in both offline RL and offline MBO settings, and the same hyperparameter-free formulation works in both domains.
- **Null hypothesis**: Domain-specific tuning of conservatism (separate α for CQL, separate α for COMs) always outperforms a unified adaptive scheme.
- **Required evidence**: Competitive or superior results on both D4RL and Design-Bench with a SINGLE method/formulation.
- **Feasibility**: HIGH — ensemble uncertainty is standard in both fields; the novel part is the adaptive mechanism.
- **Novelty**: HIGH — no existing method works across both benchmarks; adaptive conservatism is underexplored.
- **If confirmed**: Demonstrates the practical value of unification; opens a new line of research.
- **If refuted**: Still informative about what differs between RL and MBO conservatism.

### Hypothesis 2: IQL-style Implicit Conservatism for MBO
- **Statement**: Expectile regression on the surrogate score function (analogous to IQL) provides a simpler, more effective conservatism mechanism for offline MBO than explicit regularization (COMs).
- **Null hypothesis**: COMs' explicit conservative regularization outperforms expectile-based implicit conservatism on Design-Bench.
- **Required evidence**: Design-Bench performance comparison.
- **Feasibility**: HIGH — straightforward implementation.
- **Novelty**: MEDIUM — it's a direct transfer of IQL to MBO.
- **If confirmed**: Shows cross-domain algorithmic transfer is valuable.
- **If refuted**: Reveals that the single-step vs. multi-step distinction matters for conservatism design.

### Hypothesis 3: Offline-to-Online MBO via Conservative Fine-Tuning
- **Statement**: The offline-to-online transition studied in RL (Cal-QL, RLPD) can be formalized and applied to MBO, where a small budget of online evaluations is used to refine offline-optimized designs, and RL-inspired fine-tuning strategies outperform naive approaches.
- **Null hypothesis**: Simply re-running the surrogate model with the new data (standard retraining) is as effective as RL-inspired fine-tuning.
- **Required evidence**: MBO tasks where we simulate a small online evaluation budget and compare adaptation strategies.
- **Feasibility**: MEDIUM — requires a reasonable simulation setup; Design-Bench tasks have ground-truth oracles.
- **Novelty**: HIGH — offline-to-online MBO is essentially unstudied.
- **If confirmed**: Opens an entirely new problem formulation that bridges the communities.
- **If refuted**: Suggests the offline-to-online challenge is RL-specific.

## Structured Deliberation

| Hypothesis | Strengths | Weaknesses | Key Uncertainty | Information Gain |
|------------|-----------|------------|-----------------|-----------------|
| H1: UGAC | Directly addresses workshop themes; works across both benchmarks; high novelty | Ambitious scope; may be hard to tune the "adaptive" mechanism without per-domain tuning | Whether a single adaptive rule truly generalizes | Very high — if it works, it's a major contribution |
| H2: IQL for MBO | Simple, clean story; easy to implement and compare | Limited novelty (direct transfer); single-domain evaluation | Whether expectile regression makes sense for single-step problems | Medium — useful but incremental |
| H3: O2O MBO | Highest novelty; defines a new problem space; perfect for workshop theme | Requires careful experimental design for "online budget"; less established evaluation protocols | Whether the online budget is too small to help | High — new problem space regardless of outcome |

## Selected Direction

**Chosen hypothesis**: **Combination of H1 and H3** — We propose **UNICORN (UNIfied CONservative Offline-to-online fRamework for decisioN-making)** that:

1. Establishes a **unified mathematical framework** showing offline RL and offline MBO share a common conservatism structure (the "single-step MDP" reduction formalized with shared notation)
2. Proposes an **ensemble-based adaptive conservatism mechanism** that adjusts pessimism level based on local epistemic uncertainty, applicable to both domains
3. Studies **offline-to-online adaptation** in BOTH settings: fine-tuning offline RL policies with online interaction (D4RL) AND refining offline MBO designs with a small online evaluation budget (Design-Bench)
4. Demonstrates that insights transfer: the same adaptive conservatism that helps in RL's offline-to-online transfer also helps in MBO's offline-to-online transfer

**Rationale**: 
- The workshop specifically calls for "synergies between methods for offline RL and offline black-box optimization" and "unification of general principles"
- No existing paper evaluates on both D4RL AND Design-Bench
- The offline-to-online adaptation angle is timely (Cal-QL, RLPD are 2023; Tan et al. ranking is 2025)
- The contribution is conceptual (unification) + algorithmic (adaptive conservatism) + empirical (cross-domain evaluation + new offline-to-online MBO protocol)

**Key risks**:
- The adaptive conservatism mechanism might not generalize across domains with the same hyperparameters
- D4RL and Design-Bench environments may have different sensitivity to conservatism levels
- Implementation complexity of running experiments in both domains

**Pre-specified success criteria**:
1. On Design-Bench (offline MBO): match or exceed COMs performance on at least 4/7 tasks
2. On D4RL (offline RL): match or exceed CQL performance on at least 3/4 locomotion tasks
3. On offline-to-online MBO (new protocol): demonstrate >10% improvement over offline-only baseline with small online budget (k=50 evaluations)
4. On offline-to-online RL (D4RL fine-tuning): competitive with Cal-QL/RLPD

**Fallback plan**: If the unified approach doesn't work across both domains, we pivot to H3 alone (offline-to-online MBO as a new problem formulation), which is novel regardless and perfectly fits the workshop.
