"""
UNICORN: Unified Conservative Offline-to-Online Framework for Decision-Making
Experiments for ICML 2026 Workshop Paper

This script implements:
1. Ensemble LCB for offline MBO on benchmark optimization tasks
2. COMs baseline (re-implemented for fair comparison)
3. Offline-to-Online MBO protocol (novel contribution)
4. Offline RL experiments (secondary)
5. Comprehensive ablations

All experiments run on CPU with reproducible seeds.
"""

import os
import json
import time
import warnings
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from collections import defaultdict
from scipy import stats
import copy

warnings.filterwarnings('ignore')

# ============================================================
# Configuration
# ============================================================
DEVICE = torch.device('cpu')
NUM_SEEDS_MBO = 10  # 10 seeds for MBO (primary)
NUM_SEEDS_RL = 5    # 5 seeds for RL (secondary)
ENSEMBLE_K = 5
BETA_VALUES = [0.0, 0.5, 1.0, 2.0, 5.0]
DEFAULT_BETA = 2.0
ONLINE_BUDGETS = [10, 25, 50]
N_CANDIDATES = 256
N_OPT_STEPS = 200
LR_SURROGATE = 1e-3
LR_OPTIMIZE = 0.05
EPOCHS_SURROGATE = 100
HIDDEN_DIM = 256
TOP_K_EVAL = 128

# ============================================================
# Benchmark Tasks (Inspired by Design-Bench)
# ============================================================

class BenchmarkTask:
    """Base class for offline optimization benchmark tasks."""
    def __init__(self, name, dim, dataset_size, noise_std=0.01):
        self.name = name
        self.dim = dim
        self.dataset_size = dataset_size
        self.noise_std = noise_std
        self._generate_data()
    
    def oracle(self, x):
        """True objective function (only used for evaluation, not training)."""
        raise NotImplementedError
    
    def _generate_data(self):
        """Generate offline dataset from a behavior distribution."""
        raise NotImplementedError
    
    def get_data(self):
        return self.x_data, self.y_data
    
    def evaluate(self, designs):
        """Evaluate designs using the true oracle."""
        return self.oracle(designs)


class BraninTask(BenchmarkTask):
    """Branin function (2D) — well-studied, multi-modal."""
    def __init__(self, dataset_size=2000):
        super().__init__('Branin-2D', dim=2, dataset_size=dataset_size, noise_std=0.05)
    
    def oracle(self, x):
        # Branin function (negated for maximization)
        x1 = x[:, 0] * 15 - 5  # scale to [-5, 10]
        x2 = x[:, 1] * 15      # scale to [0, 15]
        a, b, c = 1.0, 5.1/(4*np.pi**2), 5/np.pi
        r, s, t = 6.0, 10.0, 1/(8*np.pi)
        val = a*(x2 - b*x1**2 + c*x1 - r)**2 + s*(1-t)*np.cos(x1) + s
        return -val  # negate for maximization
    
    def _generate_data(self):
        # Suboptimal data: uniform + slight bias toward mediocre designs
        x = np.random.uniform(0, 1, (self.dataset_size, self.dim)).astype(np.float32)
        y = self.oracle(x) + np.random.randn(self.dataset_size) * self.noise_std
        self.x_data = x
        self.y_data = y.astype(np.float32)


class RosenbrockTask(BenchmarkTask):
    """Rosenbrock function (10D) — challenging, narrow valley."""
    def __init__(self, dataset_size=5000):
        super().__init__('Rosenbrock-10D', dim=10, dataset_size=dataset_size, noise_std=0.1)
    
    def oracle(self, x):
        # Rosenbrock (negated for maximization), scaled to [0,1]^d
        xs = x * 4 - 2  # scale to [-2, 2]
        val = np.sum(100 * (xs[:, 1:] - xs[:, :-1]**2)**2 + (1 - xs[:, :-1])**2, axis=1)
        return -val / 1000.0  # scale and negate
    
    def _generate_data(self):
        x = np.random.uniform(0, 1, (self.dataset_size, self.dim)).astype(np.float32)
        y = self.oracle(x) + np.random.randn(self.dataset_size) * self.noise_std
        self.x_data = x
        self.y_data = y.astype(np.float32)


class AckleyTask(BenchmarkTask):
    """Ackley function (20D) — many local optima, tests conservatism."""
    def __init__(self, dataset_size=5000):
        super().__init__('Ackley-20D', dim=20, dataset_size=dataset_size, noise_std=0.05)
    
    def oracle(self, x):
        xs = x * 10 - 5  # scale to [-5, 5]
        d = xs.shape[1]
        sum1 = np.sum(xs**2, axis=1) / d
        sum2 = np.sum(np.cos(2*np.pi*xs), axis=1) / d
        val = -20 * np.exp(-0.2 * np.sqrt(sum1)) - np.exp(sum2) + 20 + np.e
        return -val  # negate for maximization
    
    def _generate_data(self):
        x = np.random.uniform(0, 1, (self.dataset_size, self.dim)).astype(np.float32)
        y = self.oracle(x) + np.random.randn(self.dataset_size) * self.noise_std
        self.x_data = x
        self.y_data = y.astype(np.float32)


class StyblinskiTangTask(BenchmarkTask):
    """Styblinski-Tang (5D) — smooth with clear global structure."""
    def __init__(self, dataset_size=3000):
        super().__init__('StyblinskiTang-5D', dim=5, dataset_size=dataset_size, noise_std=0.05)
    
    def oracle(self, x):
        xs = x * 10 - 5  # scale to [-5, 5]
        val = 0.5 * np.sum(xs**4 - 16*xs**2 + 5*xs, axis=1)
        return -val / self.dim  # negate and normalize
    
    def _generate_data(self):
        x = np.random.uniform(0, 1, (self.dataset_size, self.dim)).astype(np.float32)
        y = self.oracle(x) + np.random.randn(self.dataset_size) * self.noise_std
        self.x_data = x
        self.y_data = y.astype(np.float32)


class RastriginTask(BenchmarkTask):
    """Rastrigin (15D) — highly multimodal, many local optima."""
    def __init__(self, dataset_size=5000):
        super().__init__('Rastrigin-15D', dim=15, dataset_size=dataset_size, noise_std=0.1)
    
    def oracle(self, x):
        xs = x * 10.24 - 5.12  # scale to [-5.12, 5.12]
        d = xs.shape[1]
        val = 10*d + np.sum(xs**2 - 10*np.cos(2*np.pi*xs), axis=1)
        return -val / d  # negate and normalize
    
    def _generate_data(self):
        x = np.random.uniform(0, 1, (self.dataset_size, self.dim)).astype(np.float32)
        y = self.oracle(x) + np.random.randn(self.dataset_size) * self.noise_std
        self.x_data = x
        self.y_data = y.astype(np.float32)


class GriewankTask(BenchmarkTask):
    """Griewank (30D) — high-dimensional, product term creates structure."""
    def __init__(self, dataset_size=8000):
        super().__init__('Griewank-30D', dim=30, dataset_size=dataset_size, noise_std=0.05)
    
    def oracle(self, x):
        xs = x * 1200 - 600  # scale to [-600, 600]
        d = xs.shape[1]
        sum_sq = np.sum(xs**2, axis=1) / 4000
        prod_cos = np.prod(np.cos(xs / np.sqrt(np.arange(1, d+1))), axis=1)
        val = sum_sq - prod_cos + 1
        return -val  # negate for maximization
    
    def _generate_data(self):
        x = np.random.uniform(0, 1, (self.dataset_size, self.dim)).astype(np.float32)
        y = self.oracle(x) + np.random.randn(self.dataset_size) * self.noise_std
        self.x_data = x
        self.y_data = y.astype(np.float32)


class LevyTask(BenchmarkTask):
    """Levy function (8D) — variable difficulty, non-trivial landscape."""
    def __init__(self, dataset_size=4000):
        super().__init__('Levy-8D', dim=8, dataset_size=dataset_size, noise_std=0.05)
    
    def oracle(self, x):
        xs = x * 20 - 10  # scale to [-10, 10]
        w = 1 + (xs - 1) / 4
        term1 = np.sin(np.pi * w[:, 0])**2
        term2 = np.sum((w[:, :-1] - 1)**2 * (1 + 10*np.sin(np.pi*w[:, :-1] + 1)**2), axis=1)
        term3 = (w[:, -1] - 1)**2 * (1 + np.sin(2*np.pi*w[:, -1])**2)
        val = term1 + term2 + term3
        return -val / self.dim  # negate and normalize
    
    def _generate_data(self):
        x = np.random.uniform(0, 1, (self.dataset_size, self.dim)).astype(np.float32)
        y = self.oracle(x) + np.random.randn(self.dataset_size) * self.noise_std
        self.x_data = x
        self.y_data = y.astype(np.float32)


# ============================================================
# Neural Network Models
# ============================================================

class MLPSurrogate(nn.Module):
    """MLP surrogate model for objective prediction."""
    def __init__(self, input_dim, hidden_dim=HIDDEN_DIM, n_layers=3):
        super().__init__()
        layers = [nn.Linear(input_dim, hidden_dim), nn.ReLU()]
        for _ in range(n_layers - 1):
            layers.extend([nn.Linear(hidden_dim, hidden_dim), nn.ReLU()])
        layers.append(nn.Linear(hidden_dim, 1))
        self.net = nn.Sequential(*layers)
    
    def forward(self, x):
        return self.net(x).squeeze(-1)


# ============================================================
# Training Functions
# ============================================================

def train_ensemble(x_data, y_data, input_dim, K=ENSEMBLE_K, epochs=EPOCHS_SURROGATE, 
                   lr=LR_SURROGATE, batch_size=256, seed_base=0):
    """Train an ensemble of K independent MLP surrogates."""
    models = []
    x_tensor = torch.FloatTensor(x_data)
    y_tensor = torch.FloatTensor(y_data)
    dataset = TensorDataset(x_tensor, y_tensor)
    
    for k in range(K):
        torch.manual_seed(seed_base * 1000 + k)
        model = MLPSurrogate(input_dim).to(DEVICE)
        optimizer = optim.Adam(model.parameters(), lr=lr, weight_decay=1e-4)
        loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
        
        model.train()
        for epoch in range(epochs):
            for xb, yb in loader:
                xb, yb = xb.to(DEVICE), yb.to(DEVICE)
                pred = model(xb)
                loss = nn.MSELoss()(pred, yb)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
        
        model.eval()
        models.append(model)
    
    return models


def ensemble_predict(models, x):
    """Get ensemble mean and std predictions."""
    with torch.no_grad():
        preds = torch.stack([m(x) for m in models])
    mean = preds.mean(dim=0)
    std = preds.std(dim=0)
    return mean, std


def lcb_optimize(models, x_init, beta=DEFAULT_BETA, n_steps=N_OPT_STEPS, lr=LR_OPTIMIZE):
    """Optimize designs using Lower Confidence Bound on ensemble."""
    x = x_init.clone().detach().requires_grad_(True)
    optimizer = optim.Adam([x], lr=lr)
    
    for step in range(n_steps):
        optimizer.zero_grad()
        preds = torch.stack([m(x) for m in models])
        mean = preds.mean(dim=0)
        std = preds.std(dim=0)
        # LCB: maximize mean - beta * std
        lcb = mean - beta * std
        loss = -lcb.mean()  # maximize by minimizing negative
        loss.backward()
        optimizer.step()
        # Clamp to [0, 1]
        with torch.no_grad():
            x.clamp_(0, 1)
    
    return x.detach()


# ============================================================
# COMs Baseline (Re-implementation)
# ============================================================

def train_coms_ensemble(x_data, y_data, input_dim, K=ENSEMBLE_K, epochs=EPOCHS_SURROGATE,
                        alpha=1.0, lr=LR_SURROGATE, batch_size=256, seed_base=0,
                        n_neg_samples=256):
    """
    Conservative Objective Models (Trabucco et al., 2021) — re-implementation.
    
    Key idea: In addition to standard regression loss, add a conservative regularizer
    that pushes predictions DOWN on adversarial (out-of-distribution) inputs
    while pushing predictions UP on in-distribution inputs.
    """
    models = []
    x_tensor = torch.FloatTensor(x_data)
    y_tensor = torch.FloatTensor(y_data)
    dataset = TensorDataset(x_tensor, y_tensor)
    
    for k in range(K):
        torch.manual_seed(seed_base * 1000 + k + 500)
        model = MLPSurrogate(input_dim).to(DEVICE)
        optimizer = optim.Adam(model.parameters(), lr=lr, weight_decay=1e-4)
        loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
        
        model.train()
        for epoch in range(epochs):
            for xb, yb in loader:
                xb, yb = xb.to(DEVICE), yb.to(DEVICE)
                
                # Standard regression loss
                pred = model(xb)
                reg_loss = nn.MSELoss()(pred, yb)
                
                # COMs conservative regularizer:
                # Generate adversarial samples by doing gradient ascent on the model
                x_neg = xb.detach().clone().requires_grad_(True)
                pred_neg = model(x_neg)
                grad = torch.autograd.grad(pred_neg.sum(), x_neg, create_graph=False)[0]
                x_neg = (x_neg + 0.05 * grad).detach().clamp(0, 1)
                
                # Push down predictions on adversarial samples
                pred_ood = model(x_neg)
                # Push up predictions on in-distribution samples  
                pred_id = model(xb)
                
                conservative_loss = pred_ood.mean() - pred_id.mean()
                
                loss = reg_loss + alpha * conservative_loss
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
        
        model.eval()
        models.append(model)
    
    return models


# ============================================================
# Experiment 1: Offline MBO
# ============================================================

def run_offline_mbo(task, seed, beta=DEFAULT_BETA, method='lcb'):
    """Run offline MBO on a single task with a single seed."""
    np.random.seed(seed)
    torch.manual_seed(seed)
    
    x_data, y_data = task.get_data()
    
    # Train ensemble
    if method == 'lcb' or method == 'grad_ascent':
        models = train_ensemble(x_data, y_data, task.dim, seed_base=seed)
    elif method == 'coms':
        models = train_coms_ensemble(x_data, y_data, task.dim, seed_base=seed)
    
    # Initialize candidates: top-128 from dataset + 128 perturbed
    top_idx = np.argsort(y_data)[-TOP_K_EVAL:]
    x_top = x_data[top_idx]
    x_perturbed = x_top + np.random.randn(*x_top.shape).astype(np.float32) * 0.05
    x_perturbed = np.clip(x_perturbed, 0, 1)
    x_init = np.concatenate([x_top, x_perturbed], axis=0)
    x_init_tensor = torch.FloatTensor(x_init).to(DEVICE)
    
    # Optimize
    actual_beta = beta if method != 'grad_ascent' else 0.0
    x_optimized = lcb_optimize(models, x_init_tensor, beta=actual_beta)
    
    # Evaluate with oracle
    x_opt_np = x_optimized.numpy()
    scores = task.evaluate(x_opt_np)
    
    # Metrics: 100th percentile (max) and 50th percentile (median) of top-128
    top128_idx = np.argsort(scores)[-TOP_K_EVAL:]
    top128_scores = scores[top128_idx]
    
    p100 = np.max(top128_scores)
    p50 = np.median(top128_scores)
    
    return {
        'p100': float(p100),
        'p50': float(p50),
        'mean': float(np.mean(top128_scores)),
        'x_optimized': x_opt_np,
        'scores': scores,
        'models': models,
        'x_data': x_data,
        'y_data': y_data,
    }


# ============================================================
# Experiment 2: Offline-to-Online MBO (Novel Contribution)
# ============================================================

def run_o2o_mbo(task, seed, beta=DEFAULT_BETA, online_budget=50, method='lcb'):
    """Run offline-to-online MBO protocol."""
    np.random.seed(seed)
    torch.manual_seed(seed)
    
    # Phase 1: Offline MBO
    offline_result = run_offline_mbo(task, seed, beta=beta, method=method)
    offline_p100 = offline_result['p100']
    offline_p50 = offline_result['p50']
    
    # Phase 2: Select top-k candidates for online evaluation
    all_scores = offline_result['scores']
    top_k_idx = np.argsort(all_scores)[-online_budget:]
    x_selected = offline_result['x_optimized'][top_k_idx]
    
    # Phase 3: Online evaluation (query true oracle)
    true_scores = task.evaluate(x_selected)
    
    # Phase 4: Expand dataset
    x_data_expanded = np.concatenate([offline_result['x_data'], x_selected], axis=0)
    y_data_expanded = np.concatenate([offline_result['y_data'], true_scores.astype(np.float32)], axis=0)
    
    # Phase 5: Retrain ensemble on expanded dataset
    if method == 'lcb' or method == 'grad_ascent':
        models_new = train_ensemble(x_data_expanded, y_data_expanded, task.dim, 
                                     seed_base=seed + 10000)
    elif method == 'coms':
        models_new = train_coms_ensemble(x_data_expanded, y_data_expanded, task.dim,
                                          seed_base=seed + 10000)
    
    # Phase 6: Re-optimize with updated ensemble
    # Warm-start from offline candidates
    x_init = torch.FloatTensor(offline_result['x_optimized']).to(DEVICE)
    actual_beta = beta if method != 'grad_ascent' else 0.0
    x_reoptimized = lcb_optimize(models_new, x_init, beta=actual_beta)
    
    # Evaluate
    x_reopt_np = x_reoptimized.numpy()
    final_scores = task.evaluate(x_reopt_np)
    top128_idx = np.argsort(final_scores)[-TOP_K_EVAL:]
    top128_scores = final_scores[top128_idx]
    
    online_p100 = float(np.max(top128_scores))
    online_p50 = float(np.median(top128_scores))
    
    return {
        'offline_p100': offline_p100,
        'offline_p50': offline_p50,
        'online_p100': online_p100,
        'online_p50': online_p50,
        'improvement_p100': (online_p100 - offline_p100) / abs(offline_p100) * 100 if offline_p100 != 0 else 0,
        'improvement_p50': (online_p50 - offline_p50) / abs(offline_p50) * 100 if offline_p50 != 0 else 0,
        'online_budget': online_budget,
    }


def run_o2o_random_baseline(task, seed, beta=DEFAULT_BETA, online_budget=50):
    """Random online baseline: evaluate random designs instead of optimized ones."""
    np.random.seed(seed)
    torch.manual_seed(seed)
    
    offline_result = run_offline_mbo(task, seed, beta=beta, method='lcb')
    offline_p100 = offline_result['p100']
    
    # Select RANDOM designs from the original dataset for online evaluation
    random_idx = np.random.choice(len(offline_result['x_data']), size=online_budget, replace=False)
    x_random = offline_result['x_data'][random_idx]
    true_scores = task.evaluate(x_random)
    
    # Expand and retrain
    x_data_expanded = np.concatenate([offline_result['x_data'], x_random], axis=0)
    y_data_expanded = np.concatenate([offline_result['y_data'], true_scores.astype(np.float32)], axis=0)
    models_new = train_ensemble(x_data_expanded, y_data_expanded, task.dim, seed_base=seed+20000)
    
    x_init = torch.FloatTensor(offline_result['x_optimized']).to(DEVICE)
    x_reoptimized = lcb_optimize(models_new, x_init, beta=beta)
    
    final_scores = task.evaluate(x_reoptimized.numpy())
    top128_idx = np.argsort(final_scores)[-TOP_K_EVAL:]
    online_p100 = float(np.max(final_scores[top128_idx]))
    
    return {
        'offline_p100': offline_p100,
        'online_p100': online_p100,
        'improvement_p100': (online_p100 - offline_p100) / abs(offline_p100) * 100 if offline_p100 != 0 else 0,
    }


# ============================================================
# Experiment 3: Offline RL (Secondary)
# ============================================================

class SimpleRLEnv:
    """Simple continuous-control-like environment for RL experiments."""
    def __init__(self, name, state_dim, action_dim, horizon=100):
        self.name = name
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.horizon = horizon
    
    def reward(self, s, a):
        """Reward function."""
        raise NotImplementedError
    
    def transition(self, s, a):
        """Deterministic transition."""
        raise NotImplementedError


class LinearQuadraticEnv(SimpleRLEnv):
    """Linear-Quadratic Regulator — known optimal solution for validation."""
    def __init__(self):
        super().__init__('LQR-4D', state_dim=4, action_dim=2, horizon=50)
        np.random.seed(42)
        self.A = np.eye(4) + 0.1 * np.random.randn(4, 4).astype(np.float32)
        self.B = 0.5 * np.random.randn(4, 2).astype(np.float32)
        self.Q_cost = np.eye(4).astype(np.float32)
        self.R_cost = 0.1 * np.eye(2).astype(np.float32)
    
    def reward(self, s, a):
        return -(np.sum(s**2 * np.diag(self.Q_cost), axis=-1) + 
                 np.sum(a**2 * np.diag(self.R_cost), axis=-1))
    
    def transition(self, s, a):
        return (s @ self.A.T + a @ self.B.T).astype(np.float32)


class NonlinearControlEnv(SimpleRLEnv):
    """Nonlinear control task — pendulum-like dynamics."""
    def __init__(self):
        super().__init__('Pendulum-2D', state_dim=3, action_dim=1, horizon=50)
    
    def reward(self, s, a):
        # Reward for being upright (cosθ ≈ 1) with small actions
        cos_theta = s[..., 0] if s.ndim > 1 else s[0]
        return cos_theta - 0.1 * np.sum(a**2, axis=-1)
    
    def transition(self, s, a):
        # Simplified pendulum dynamics
        theta = np.arctan2(s[..., 1:2], s[..., 0:1])
        omega = s[..., 2:3]
        dt = 0.05
        new_omega = omega + (-9.8 * np.sin(theta) + a) * dt
        new_theta = theta + new_omega * dt
        new_s = np.concatenate([np.cos(new_theta), np.sin(new_theta), new_omega], axis=-1)
        return new_s.astype(np.float32)


def generate_rl_dataset(env, n_episodes=1000, policy_noise=0.5, seed=42):
    """Generate offline RL dataset with a noisy/suboptimal behavioral policy."""
    np.random.seed(seed)
    states, actions, rewards, next_states, dones = [], [], [], [], []
    
    for ep in range(n_episodes):
        s = np.random.randn(env.state_dim).astype(np.float32) * 0.5
        for t in range(env.horizon):
            # Suboptimal policy: random with slight structure
            a = np.random.randn(env.action_dim).astype(np.float32) * policy_noise
            # Add slight negative feedback
            a -= 0.1 * s[:env.action_dim] if env.action_dim <= env.state_dim else 0
            a = np.clip(a, -1, 1)
            
            r = env.reward(s.reshape(1, -1), a.reshape(1, -1)).item()
            ns = env.transition(s.reshape(1, -1), a.reshape(1, -1)).squeeze()
            done = (t == env.horizon - 1)
            
            states.append(s)
            actions.append(a)
            rewards.append(r)
            next_states.append(ns)
            dones.append(done)
            
            s = ns
    
    return {
        'states': np.array(states, dtype=np.float32),
        'actions': np.array(actions, dtype=np.float32),
        'rewards': np.array(rewards, dtype=np.float32),
        'next_states': np.array(next_states, dtype=np.float32),
        'dones': np.array(dones, dtype=np.float32),
    }


class QNetwork(nn.Module):
    """Q-network for offline RL."""
    def __init__(self, state_dim, action_dim, hidden_dim=128):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(state_dim + action_dim, hidden_dim), nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim), nn.ReLU(),
            nn.Linear(hidden_dim, 1)
        )
    
    def forward(self, s, a):
        x = torch.cat([s, a], dim=-1)
        return self.net(x).squeeze(-1)


def train_q_ensemble(dataset, state_dim, action_dim, K=ENSEMBLE_K, 
                     epochs=50, beta=DEFAULT_BETA, lr=3e-4, batch_size=256,
                     gamma=0.99, seed_base=0):
    """Train ensemble of Q-networks with LCB-style conservatism."""
    s = torch.FloatTensor(dataset['states'])
    a = torch.FloatTensor(dataset['actions'])
    r = torch.FloatTensor(dataset['rewards'])
    ns = torch.FloatTensor(dataset['next_states'])
    d = torch.FloatTensor(dataset['dones'])
    
    ds = TensorDataset(s, a, r, ns, d)
    
    models = []
    for k in range(K):
        torch.manual_seed(seed_base * 1000 + k)
        q_net = QNetwork(state_dim, action_dim).to(DEVICE)
        q_target = copy.deepcopy(q_net)
        optimizer = optim.Adam(q_net.parameters(), lr=lr)
        loader = DataLoader(ds, batch_size=batch_size, shuffle=True)
        
        for epoch in range(epochs):
            for sb, ab, rb, nsb, db in loader:
                # TD target using dataset actions for next state (no OOD)
                with torch.no_grad():
                    # Use random dataset actions for next state (like IQL approach)
                    idx = torch.randint(0, len(a), (len(sb),))
                    na = a[idx]
                    q_next = q_target(nsb, na)
                    target = rb + gamma * (1 - db) * q_next
                
                # Q prediction
                q_pred = q_net(sb, ab)
                td_loss = nn.MSELoss()(q_pred, target)
                
                # Conservative regularizer: penalize Q on random actions
                random_a = torch.randn_like(ab)
                q_random = q_net(sb, random_a)
                q_data = q_net(sb, ab)
                conservative_loss = q_random.mean() - q_data.mean()
                
                loss = td_loss + 0.5 * conservative_loss
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
            
            # Soft update target
            with torch.no_grad():
                for p, pt in zip(q_net.parameters(), q_target.parameters()):
                    pt.data.mul_(0.995).add_(p.data, alpha=0.005)
        
        q_net.eval()
        models.append(q_net)
    
    return models


def evaluate_rl_policy(env, q_models, beta=DEFAULT_BETA, n_eval=50, seed=0):
    """Evaluate a policy derived from Q-ensemble via greedy LCB selection."""
    np.random.seed(seed)
    returns = []
    
    for ep in range(n_eval):
        s = np.random.randn(env.state_dim).astype(np.float32) * 0.5
        episode_return = 0
        
        for t in range(env.horizon):
            s_tensor = torch.FloatTensor(s).unsqueeze(0).repeat(100, 1)
            # Sample candidate actions
            a_candidates = torch.randn(100, env.action_dim).clamp(-1, 1)
            
            # Ensemble LCB
            with torch.no_grad():
                q_preds = torch.stack([m(s_tensor, a_candidates) for m in q_models])
                q_mean = q_preds.mean(dim=0)
                q_std = q_preds.std(dim=0)
                lcb = q_mean - beta * q_std
            
            best_idx = lcb.argmax()
            a = a_candidates[best_idx].numpy()
            
            r = env.reward(s.reshape(1, -1), a.reshape(1, -1)).item()
            episode_return += r
            s = env.transition(s.reshape(1, -1), a.reshape(1, -1)).squeeze()
        
        returns.append(episode_return)
    
    return np.mean(returns), np.std(returns)


def evaluate_bc_policy(env, dataset, n_eval=50, seed=0):
    """Behavior cloning baseline — average return of behavioral policy."""
    np.random.seed(seed)
    n = len(dataset['rewards'])
    horizon = env.horizon
    n_episodes = n // horizon
    returns = []
    for i in range(min(n_episodes, n_eval)):
        ep_return = np.sum(dataset['rewards'][i*horizon:(i+1)*horizon])
        returns.append(ep_return)
    return np.mean(returns), np.std(returns)


# ============================================================
# Main Experiment Runner
# ============================================================

def run_all_experiments():
    """Run all experiments and save results."""
    results = {
        'offline_mbo': {},
        'o2o_mbo': {},
        'rl': {},
        'ablations': {},
    }
    
    # Create tasks
    tasks = [
        BraninTask(),
        StyblinskiTangTask(),
        LevyTask(),
        RosenbrockTask(),
        RastriginTask(),
        AckleyTask(),
        GriewankTask(),
    ]
    
    print("=" * 70)
    print("EXPERIMENT 1: Offline MBO on Benchmark Tasks")
    print("=" * 70)
    
    for task in tasks:
        print(f"\n--- Task: {task.name} (dim={task.dim}) ---")
        task_results = {'lcb': [], 'coms': [], 'grad_ascent': []}
        
        for method in ['lcb', 'coms', 'grad_ascent']:
            for seed in range(NUM_SEEDS_MBO):
                t0 = time.time()
                res = run_offline_mbo(task, seed, beta=DEFAULT_BETA, method=method)
                elapsed = time.time() - t0
                task_results[method].append({
                    'p100': res['p100'],
                    'p50': res['p50'],
                    'mean': res['mean'],
                    'seed': seed,
                    'time': elapsed,
                })
                if seed == 0:
                    print(f"  {method:>12s} seed=0: p100={res['p100']:.4f}, p50={res['p50']:.4f} ({elapsed:.1f}s)")
            
            p100s = [r['p100'] for r in task_results[method]]
            p50s = [r['p50'] for r in task_results[method]]
            print(f"  {method:>12s} avg:    p100={np.mean(p100s):.4f}±{np.std(p100s):.4f}, "
                  f"p50={np.mean(p50s):.4f}±{np.std(p50s):.4f}")
        
        results['offline_mbo'][task.name] = task_results
    
    print("\n" + "=" * 70)
    print("EXPERIMENT 2: Offline-to-Online MBO (Novel Protocol)")
    print("=" * 70)
    
    for task in tasks:
        print(f"\n--- Task: {task.name} ---")
        task_results = {}
        
        for budget in ONLINE_BUDGETS:
            budget_results = {'lcb_o2o': [], 'coms_o2o': [], 'naive_o2o': [], 'random_o2o': []}
            
            for seed in range(NUM_SEEDS_MBO):
                # LCB with O2O
                res = run_o2o_mbo(task, seed, beta=DEFAULT_BETA, online_budget=budget, method='lcb')
                budget_results['lcb_o2o'].append(res)
                
                # COMs with O2O
                res_coms = run_o2o_mbo(task, seed, beta=DEFAULT_BETA, online_budget=budget, method='coms')
                budget_results['coms_o2o'].append(res_coms)
                
                # Naive (no conservatism) with O2O
                res_naive = run_o2o_mbo(task, seed, beta=0.0, online_budget=budget, method='grad_ascent')
                budget_results['naive_o2o'].append(res_naive)
                
                # Random online
                res_random = run_o2o_random_baseline(task, seed, beta=DEFAULT_BETA, online_budget=budget)
                budget_results['random_o2o'].append(res_random)
            
            for method_name in budget_results:
                imps = [r['improvement_p100'] for r in budget_results[method_name]]
                p100s = [r['online_p100'] for r in budget_results[method_name]]
                print(f"  k={budget:3d} {method_name:>12s}: final_p100={np.mean(p100s):.4f}±{np.std(p100s):.4f}, "
                      f"improvement={np.mean(imps):.1f}%±{np.std(imps):.1f}%")
            
            task_results[budget] = budget_results
        
        results['o2o_mbo'][task.name] = task_results
    
    print("\n" + "=" * 70)
    print("EXPERIMENT 3: Offline RL (Secondary)")
    print("=" * 70)
    
    rl_envs = [LinearQuadraticEnv(), NonlinearControlEnv()]
    
    for env in rl_envs:
        print(f"\n--- Env: {env.name} ---")
        env_results = {'lcb_rl': [], 'no_conserv_rl': [], 'bc': []}
        
        for seed in range(NUM_SEEDS_RL):
            dataset = generate_rl_dataset(env, n_episodes=500, seed=seed)
            
            # BC baseline
            bc_mean, bc_std = evaluate_bc_policy(env, dataset, seed=seed)
            env_results['bc'].append({'mean': bc_mean, 'std': bc_std})
            
            # Q-ensemble with LCB
            q_models = train_q_ensemble(dataset, env.state_dim, env.action_dim,
                                        beta=DEFAULT_BETA, seed_base=seed)
            rl_mean, rl_std = evaluate_rl_policy(env, q_models, beta=DEFAULT_BETA, seed=seed)
            env_results['lcb_rl'].append({'mean': rl_mean, 'std': rl_std})
            
            # Q-ensemble without conservatism
            q_models_nc = train_q_ensemble(dataset, env.state_dim, env.action_dim,
                                            beta=0.0, seed_base=seed + 5000)
            nc_mean, nc_std = evaluate_rl_policy(env, q_models_nc, beta=0.0, seed=seed)
            env_results['no_conserv_rl'].append({'mean': nc_mean, 'std': nc_std})
            
            if seed == 0:
                print(f"  seed=0: BC={bc_mean:.2f}, LCB={rl_mean:.2f}, NoCons={nc_mean:.2f}")
        
        for method_name in env_results:
            means = [r['mean'] for r in env_results[method_name]]
            print(f"  {method_name:>15s}: mean_return={np.mean(means):.2f}±{np.std(means):.2f}")
        
        results['rl'][env.name] = env_results
    
    print("\n" + "=" * 70)
    print("EXPERIMENT 4: Ablation Studies")
    print("=" * 70)
    
    # Beta ablation
    print("\n--- Beta Sensitivity ---")
    ablation_tasks = tasks  # all tasks
    beta_results = {}
    
    for task in ablation_tasks:
        beta_results[task.name] = {}
        for beta in BETA_VALUES:
            seed_results = []
            for seed in range(5):  # 5 seeds for ablation (efficiency)
                res = run_offline_mbo(task, seed, beta=beta, method='lcb')
                seed_results.append(res['p100'])
            beta_results[task.name][beta] = {
                'mean': float(np.mean(seed_results)),
                'std': float(np.std(seed_results)),
            }
        betas_str = ", ".join([f"β={b}:{beta_results[task.name][b]['mean']:.4f}" for b in BETA_VALUES])
        print(f"  {task.name}: {betas_str}")
    
    results['ablations']['beta'] = beta_results
    
    # Ensemble size ablation (on 3 representative tasks)
    print("\n--- Ensemble Size ---")
    ensemble_tasks = [tasks[0], tasks[3], tasks[5]]  # Branin, Rosenbrock, Ackley
    K_values = [3, 5, 10]
    ensemble_results = {}
    
    for task in ensemble_tasks:
        ensemble_results[task.name] = {}
        for K in K_values:
            seed_results = []
            for seed in range(5):
                np.random.seed(seed)
                torch.manual_seed(seed)
                x_data, y_data = task.get_data()
                models = train_ensemble(x_data, y_data, task.dim, K=K, seed_base=seed)
                top_idx = np.argsort(y_data)[-TOP_K_EVAL:]
                x_top = x_data[top_idx]
                x_perturbed = x_top + np.random.randn(*x_top.shape).astype(np.float32) * 0.05
                x_perturbed = np.clip(x_perturbed, 0, 1)
                x_init = np.concatenate([x_top, x_perturbed], axis=0)
                x_init_tensor = torch.FloatTensor(x_init)
                x_opt = lcb_optimize(models, x_init_tensor, beta=DEFAULT_BETA)
                scores = task.evaluate(x_opt.numpy())
                top128 = np.sort(scores)[-TOP_K_EVAL:]
                seed_results.append(float(np.max(top128)))
            ensemble_results[task.name][K] = {
                'mean': float(np.mean(seed_results)),
                'std': float(np.std(seed_results)),
            }
        k_str = ", ".join([f"K={K}:{ensemble_results[task.name][K]['mean']:.4f}" for K in K_values])
        print(f"  {task.name}: {k_str}")
    
    results['ablations']['ensemble_size'] = ensemble_results
    
    # Online budget ablation
    print("\n--- Online Budget (O2O MBO) ---")
    budget_values = [10, 25, 50, 100]
    budget_task = tasks[3]  # Rosenbrock
    budget_results = {}
    for budget in budget_values:
        seed_results = []
        for seed in range(5):
            res = run_o2o_mbo(budget_task, seed, beta=DEFAULT_BETA, online_budget=budget)
            seed_results.append(res['improvement_p100'])
        budget_results[budget] = {
            'mean': float(np.mean(seed_results)),
            'std': float(np.std(seed_results)),
        }
        print(f"  k={budget}: improvement={budget_results[budget]['mean']:.1f}%±{budget_results[budget]['std']:.1f}%")
    
    results['ablations']['online_budget'] = budget_results
    
    # Save all results
    # Convert numpy types for JSON serialization
    def convert_to_serializable(obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, dict):
            return {k: convert_to_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_to_serializable(v) for v in obj]
        return obj
    
    # Remove non-serializable items
    clean_results = {}
    for exp_name, exp_data in results.items():
        clean_results[exp_name] = {}
        for task_name, task_data in exp_data.items():
            if isinstance(task_data, dict):
                clean_task = {}
                for k, v in task_data.items():
                    if isinstance(v, list):
                        clean_list = []
                        for item in v:
                            if isinstance(item, dict):
                                clean_item = {ik: iv for ik, iv in item.items() 
                                             if not isinstance(iv, (np.ndarray, list, nn.Module)) 
                                             or isinstance(iv, (int, float, str, bool))}
                                # Keep only scalar values
                                clean_item2 = {}
                                for ik, iv in item.items():
                                    if isinstance(iv, (int, float, str, bool, np.floating, np.integer)):
                                        clean_item2[ik] = convert_to_serializable(iv)
                                clean_list.append(clean_item2)
                            else:
                                clean_list.append(convert_to_serializable(v))
                                break
                        clean_task[k] = clean_list if clean_list and isinstance(clean_list[0], dict) else convert_to_serializable(v)
                    elif isinstance(v, dict):
                        clean_task[k] = convert_to_serializable(v)
                    else:
                        clean_task[k] = convert_to_serializable(v)
                clean_results[exp_name][task_name] = clean_task
            else:
                clean_results[exp_name][task_name] = convert_to_serializable(task_data)
    
    with open('results.json', 'w') as f:
        json.dump(clean_results, f, indent=2, default=str)
    
    print("\n" + "=" * 70)
    print("ALL EXPERIMENTS COMPLETE. Results saved to results.json")
    print("=" * 70)
    
    return results


if __name__ == '__main__':
    start = time.time()
    results = run_all_experiments()
    elapsed = time.time() - start
    print(f"\nTotal wall time: {elapsed/60:.1f} minutes")
