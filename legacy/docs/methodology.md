# Methodology: Ensemble LCB for Unified Offline-to-Online Decision-Making (Revised)

## Research Question & Hypothesis
- **Question**: Can ensemble-based Lower Confidence Bound (LCB) conservatism — a principled, theoretically-motivated framework — serve as a unified approach for offline decision-making across BOTH offline RL and offline MBO, and enable a new paradigm of offline-to-online adaptation in MBO?
- **Hypothesis**: (H1) Ensemble LCB provides competitive offline MBO performance relative to domain-specific methods like COMs; (H2) The offline-to-online MBO protocol — where a small budget of online evaluations refines offline-optimized designs — yields significant improvement over offline-only baselines; (H3) The same LCB framework also provides meaningful offline RL results, demonstrating cross-domain applicability.
- **Success criteria (pre-specified)**:
  1. Ensemble LCB matches or exceeds our own COMs re-implementation on ≥4/7 Design-Bench tasks (controlled comparison)
  2. Offline-to-online MBO yields >10% improvement in 100th-percentile score over offline-only, across ≥4/7 tasks
  3. D4RL experiments show improvement over behavior cloning, demonstrating the LCB signal is meaningful for RL
  4. Ablation shows β > 0 (conservatism) outperforms β = 0 (no conservatism) on ≥5/7 MBO tasks

## Revised Method

### Unified LCB Framework

We formalize both settings as instances of maximizing an unknown function from offline data:

**General problem**: Given D = {(x_i, y_i)}_{i=1}^N, find x* = argmax_x f(x)
- **Offline MBO**: x is a design vector, y = f(x) is the objective score, single evaluation step
- **Offline RL**: x = (s,a), y = Q^π(s,a), f is the optimal Q-function, evaluated via Bellman backup

**Ensemble LCB**:
1. Train K independent models: {f_1, ..., f_K}
2. Compute mean: μ(x) = (1/K) Σ_k f_k(x)
3. Compute uncertainty: σ(x) = std({f_1(x), ..., f_K(x)})
4. Conservative estimate: f̂(x) = μ(x) - β · σ(x)

β is a scalar hyperparameter controlling conservatism strength. This is the standard LCB formulation with theoretical backing from Rashidinejad et al. (2021) and Jin et al. (2021).

**For MBO**: x* = argmax_x f̂(x) via gradient ascent on differentiable ensemble
**For RL**: Q̂(s,a) = μ_Q(s,a) - β · σ_Q(s,a); policy extraction via advantage-weighted regression (AWR):
  π(a|s) ∝ π_β(a|s) · exp(Â(s,a)/τ), where Â(s,a) = Q̂(s,a) - V̂(s)

AWR is much cheaper than SAC — it's weighted supervised learning on dataset actions, not iterative policy optimization.

### Offline-to-Online MBO Protocol (Novel Contribution)

The key observation: after offline MBO proposes candidate designs, practitioners typically evaluate a few promising candidates using the real objective function (e.g., wet-lab experiments, physics simulations). This naturally creates an offline-to-online transition that has not been studied algorithmically.

**Protocol**:
1. **Offline phase**: Train ensemble on D, optimize x* = argmax_x [μ(x) - β·σ(x)] to get N=256 candidate designs
2. **Selection**: Rank candidates by f̂(x), select top-k for online evaluation (k ∈ {10, 25, 50})
3. **Online evaluation**: Query oracle f(x) for the k selected designs → get true scores
4. **Dataset expansion**: D' = D ∪ {(x_j, f(x_j))}_{j=1}^k
5. **Retrain**: Train new ensemble on D', re-optimize from warm-started candidate set
6. **Natural conservatism relaxation**: σ(x) decreases near evaluated designs → f̂(x) increases → algorithm trusts these regions more

**Control baselines**:
- **Offline-only**: No online evaluations (vanilla LCB MBO)
- **Naive retraining**: Retrain ensemble on D' without LCB penalty (β=0)
- **Random online**: Evaluate k randomly chosen designs from D instead of optimized candidates
- **COMs + retraining**: COMs baseline also gets k online evaluations and retrains

## Data Sources
- **Design-Bench** (primary): TFBind8, TFBind10, Superconductor, Ant, D'Kitty, HopperController, GFP
- **D4RL** (secondary/illustrative): halfcheetah-medium-v2, hopper-medium-v2, walker2d-medium-v2

## Analysis Pipeline

### Step 1: Offline MBO Experiments (Primary)
- **Method**: K=5 MLP ensemble (3-layer, 256 hidden units each), trained independently with different seeds
- **Optimization**: 200 steps of gradient ascent on f̂(x) starting from 256 initial designs sampled from top-128 in dataset + 128 Gaussian-perturbed variants
- **Baselines (re-implemented under identical conditions)**:
  - Gradient Ascent (β=0): μ(x) only, no conservatism
  - COMs (re-implemented): following Trabucco et al. (2021) algorithm with identical architecture
- **Published baselines (for reference only, not primary comparison)**: MINs, CbAS, RoMA from literature
- **Metrics**: 100th percentile (max) and 50th percentile (median) of oracle score on top-128 proposed designs
- **Pre-specified β grid**: β ∈ {0.0, 0.5, 1.0, 2.0, 5.0}; report all; use β=2.0 as default based on LCB theory

### Step 2: Offline-to-Online MBO (Main Novel Contribution)
- **Method**: Apply the O2O protocol above to all 7 Design-Bench tasks
- **Online budgets**: k ∈ {10, 25, 50} evaluations
- **Baselines**: Offline-only, Naive retraining, Random online, COMs+retraining (all re-implemented)
- **Metrics**: (1) 100th percentile after O2O vs. before, (2) Relative improvement ratio, (3) Evaluation budget efficiency (improvement per online query)
- **Seeds**: 10 random seeds (increased from 5 for higher statistical power)

### Step 3: Offline RL Experiments (Secondary)
- **Method**: K=5 Q-network ensemble with AWR policy extraction
- **Training**: 100K gradient steps on Q-ensemble (feasible on CPU: ~30 min per task)
- **Baselines (re-implemented)**: Behavior Cloning, Ensemble Q + β=0 (no conservatism)
- **Published baselines (reference only)**: CQL, IQL, TD3+BC
- **Metrics**: D4RL normalized return
- **Seeds**: 5 random seeds

### Step 4: Ablation Studies
- **β sensitivity**: β ∈ {0.0, 0.5, 1.0, 2.0, 5.0} on all MBO tasks (pre-specified)
- **Ensemble size**: K ∈ {3, 5, 10} on 3 representative MBO tasks (TFBind8, Superconductor, Ant)
- **Online budget**: k ∈ {10, 25, 50, 100} for O2O MBO

## Controls & Validation
- **Positive control**: Gradient Ascent (β=0) should show known overestimation failure on high-dimensional tasks
- **Negative control**: Random design selection should underperform optimized designs
- **Sanity check**: Ensemble uncertainty should be higher for designs far from training distribution
- **Reproducibility**: All baselines re-implemented in same codebase with identical architecture, optimizer, training epochs

## Statistical Plan
- **Primary analysis**: Per-task comparison of methods across seeds; report mean ± standard error
- **Aggregation**: Average rank across all tasks (lower is better) — non-parametric, no distributional assumptions
- **Effect size**: Report improvement ratio (method score / baseline score) for each task
- **For O2O experiments**: Paired comparison (same seed, same task: before vs. after online evaluation) with bootstrap 95% CI
- **Multiple comparisons**: When testing "method A > method B on ≥k tasks", use binomial test (H0: p=0.5)
- **10 seeds for MBO**: provides adequate power for detecting moderate effect sizes

## Compute Requirements
- **Platform**: Local CPU
- **Estimated duration**: 
  - Design-Bench offline MBO: ~30 min/task × 7 tasks × 6 β values / parallelism = ~3 hours
  - O2O MBO: ~15 min/task × 7 tasks × 3 k-values = ~2.5 hours  
  - D4RL: ~30 min/task × 3 tasks = ~1.5 hours
  - Ablations: ~2 hours
  - **Total**: ~9 hours (can run overnight)
- **Estimated cost**: $0 (local compute)

## Limitations & Assumptions
- **Assumption 1**: Ensemble disagreement is a reliable proxy for epistemic uncertainty (well-supported: Lakshminarayanan et al., 2017)
- **Assumption 2**: Design-Bench oracle faithfully simulates real-world online evaluation
- **Limitation 1**: CPU compute constrains network size and training duration; results may improve with GPU
- **Limitation 2**: D4RL experiments are secondary/illustrative due to compute constraints; AWR-based policy extraction is weaker than full SAC/CQL
- **Limitation 3**: We compare primarily to our own re-implementations; published SOTA (ranking-based methods, Tan et al. 2025) may outperform
- **Limitation 4**: O2O MBO protocol uses a single round of online evaluation; iterative protocols may improve further
- **Limitation 5**: Workshop paper scope limits the number of tasks and ablations
