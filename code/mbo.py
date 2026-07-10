"""Single source of truth for the offline-MBO paper.

Everything here is ported from the legacy scripts that generated the existing
results (legacy/run_scripts/run_revision.py primarily, GP baseline from
legacy/run_scripts/run_new_experiments.py) so numbers stay comparable with
results/results_revision.json. Config below == the revision config.

Design note: both optimizers act on a *score closure*, so every surrogate
(ensemble, exact GP, BoTorch GP) can be paired with every optimizer. That
2x2 (surrogate x optimizer) is the paper's de-confounding grid.
"""
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

# ---------------- config (canonical: matches results_revision.json) --------
K_ENS = 5
HID = 96
TRAIN_EP = 35
LR = 3e-3
WD = 1e-4
BETA = 2.0
TOP = 128
OPT_STEPS = 100
LR_OPT = 0.05
DEVICE = torch.device('cpu')

# ---------------- tasks ----------------------------------------------------
class Task:
    """Offline dataset is FIXED across seeds (np.random.seed(0) at init);
    per-seed randomness lives in training/init only. State this in the paper."""
    def __init__(s, name, dim, n, noise):
        s.name, s.dim, s.noise = name, dim, noise
        np.random.seed(0)
        s.x = np.random.uniform(0, 1, (n, dim)).astype(np.float32)
        s.y = (s.oracle(s.x) + np.random.randn(n) * noise).astype(np.float32)
    def data(s): return s.x.copy(), s.y.copy()

class Branin(Task):
    def __init__(s): super().__init__('Branin-2D', 2, 2000, 0.05)
    def oracle(s, x):
        x1, x2 = x[:, 0]*15-5, x[:, 1]*15
        return -(1*(x2-5.1/(4*np.pi**2)*x1**2+5/np.pi*x1-6)**2+10*(1-1/(8*np.pi))*np.cos(x1)+10)

class Styblinski(Task):
    def __init__(s): super().__init__('Styblinski-5D', 5, 3000, 0.05)
    def oracle(s, x):
        xs = x*10-5
        return -0.5*np.sum(xs**4-16*xs**2+5*xs, 1)/s.dim

class Levy(Task):
    def __init__(s): super().__init__('Levy-8D', 8, 4000, 0.05)
    def oracle(s, x):
        xs = x*20-10; w = 1+(xs-1)/4
        return -(np.sin(np.pi*w[:, 0])**2
                 + np.sum((w[:, :-1]-1)**2*(1+10*np.sin(np.pi*w[:, :-1]+1)**2), 1)
                 + (w[:, -1]-1)**2*(1+np.sin(2*np.pi*w[:, -1])**2))/s.dim

class Rosenbrock(Task):
    def __init__(s): super().__init__('Rosenbrock-10D', 10, 5000, 0.1)
    def oracle(s, x):
        xs = x*4-2
        return -np.sum(100*(xs[:, 1:]-xs[:, :-1]**2)**2+(1-xs[:, :-1])**2, 1)/1000

class Rastrigin(Task):
    def __init__(s): super().__init__('Rastrigin-15D', 15, 5000, 0.1)
    def oracle(s, x):
        xs = x*10.24-5.12; d = xs.shape[1]
        return -(10*d+np.sum(xs**2-10*np.cos(2*np.pi*xs), 1))/d

class Ackley(Task):
    def __init__(s): super().__init__('Ackley-20D', 20, 5000, 0.05)
    def oracle(s, x):
        xs = x*10-5; d = xs.shape[1]
        return -(-20*np.exp(-0.2*np.sqrt(np.sum(xs**2, 1)/d))
                 - np.exp(np.sum(np.cos(2*np.pi*xs), 1)/d)+20+np.e)

class Griewank(Task):
    def __init__(s): super().__init__('Griewank-30D', 30, 8000, 0.05)
    def oracle(s, x):
        xs = x*1200-600; d = xs.shape[1]
        return -(np.sum(xs**2, 1)/4000-np.prod(np.cos(xs/np.sqrt(np.arange(1, d+1))), 1)+1)

ALL_TASKS = [Branin, Styblinski, Levy, Rosenbrock, Rastrigin, Ackley, Griewank]

def make_tasks(names=None):
    tasks = [T() for T in ALL_TASKS]
    return tasks if not names else [t for t in tasks if t.name in names]

# ---------------- ensemble surrogates --------------------------------------
class MLP(nn.Module):
    def __init__(s, d, hid=HID):
        super().__init__()
        s.net = nn.Sequential(nn.Linear(d, hid), nn.ReLU(),
                              nn.Linear(hid, hid), nn.ReLU(), nn.Linear(hid, 1))
    def forward(s, x): return s.net(x).squeeze(-1)

def train_ensemble(x, y, d, seed=0, K=K_ENS, ep=TRAIN_EP, coms_alpha=None):
    """coms_alpha=None -> plain MSE ensemble; float -> COMs conservative term.
    Seed conventions preserved from legacy (coms members offset by +500)."""
    ds = TensorDataset(torch.FloatTensor(x), torch.FloatTensor(y))
    ms = []
    for k in range(K):
        torch.manual_seed(seed*100 + k + (500 if coms_alpha is not None else 0))
        m = MLP(d)
        o = optim.Adam(m.parameters(), lr=LR, weight_decay=WD)
        dl = DataLoader(ds, batch_size=256, shuffle=True)
        m.train()
        for _ in range(ep):
            for xb, yb in dl:
                loss = nn.MSELoss()(m(xb), yb)
                if coms_alpha is not None:
                    xn = xb.detach().clone().requires_grad_(True)
                    g = torch.autograd.grad(m(xn).sum(), xn)[0]
                    xn = (xn + 0.05*g).detach().clamp(0, 1)
                    loss = loss + coms_alpha*(m(xn).mean() - m(xb).mean())
                o.zero_grad(); loss.backward(); o.step()
        m.eval(); ms.append(m)
    return ms

def ens_lcb_torch(ms, beta):
    def f(x):
        ps = torch.stack([m(x) for m in ms])
        return ps.mean(0) - beta*ps.std(0)
    return f

def ens_lcb_np(ms, beta):
    f = ens_lcb_torch(ms, beta)
    def g(x):
        with torch.no_grad():
            return f(torch.FloatTensor(x)).numpy()
    return g

# ---------------- optimizers (shared across surrogates) ---------------------
def grad_opt(score_torch, x0, steps=OPT_STEPS, lr=LR_OPT):
    """Adam ascent on a differentiable score. x0: torch (N,d)."""
    x = x0.clone().detach().requires_grad_(True)
    o = optim.Adam([x], lr=lr)
    for _ in range(steps):
        o.zero_grad()
        (-score_torch(x).mean()).backward()
        o.step()
        with torch.no_grad(): x.clamp_(0, 1)
    return x.detach().numpy()

def perturb_opt(score_np, x0, rounds=5, sigmas=(0.1, 0.05, 0.02)):
    """Random-perturbation hill climb, elementwise accept. x0: np (N,d).
    Port of legacy optimize_perturb; this is the GP-pipeline-aligned optimizer."""
    x_best = x0.copy()
    best = score_np(x_best)
    for _ in range(rounds):
        for s in sigmas:
            cand = np.clip(x_best + np.random.randn(*x_best.shape).astype(np.float32)*s, 0, 1)
            sc = score_np(cand)
            imp = sc > best
            x_best[imp] = cand[imp]
            best[imp] = sc[imp]
    return x_best

# ---------------- GP surrogates ---------------------------------------------
def fit_exact_gp(x, y, dim, seed, max_train=800):
    """sklearn exact GP on score-biased subsample (top 20% + random fill).
    Port of legacy run_gp_lcb. 800^3 is fine at any input dim."""
    from sklearn.gaussian_process import GaussianProcessRegressor
    from sklearn.gaussian_process.kernels import Matern, WhiteKernel, ConstantKernel
    np.random.seed(seed)
    if len(x) > max_train:
        top = np.argsort(y)[-int(max_train*0.2):]
        rest = np.setdiff1d(np.arange(len(x)), top)
        sel = np.concatenate([top, np.random.choice(rest, max_train-len(top), replace=False)])
        x, y = x[sel], y[sel]
    kernel = (ConstantKernel(1.0) * Matern(length_scale=np.ones(dim)*0.3, nu=2.5)
              + WhiteKernel(noise_level=0.01))
    gp = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=2,
                                  normalize_y=True, alpha=1e-6)
    gp.fit(x, y)
    return gp

def gp_lcb_np(gp, beta):
    def g(x):
        mu, sd = gp.predict(x, return_std=True)
        return mu - beta*sd
    return g

def fit_botorch_gp(x, y, seed, max_train=800):
    """BoTorch GP -> differentiable posterior, enables the GP+gradient cell.
    Returns None if botorch isn't installed (runner skips the cell)."""
    try:
        from botorch.models import SingleTaskGP
        from botorch.fit import fit_gpytorch_mll
        from gpytorch.mlls import ExactMarginalLogLikelihood
    except ImportError:
        return None
    np.random.seed(seed); torch.manual_seed(seed)
    if len(x) > max_train:
        top = np.argsort(y)[-int(max_train*0.2):]
        rest = np.setdiff1d(np.arange(len(x)), top)
        sel = np.concatenate([top, np.random.choice(rest, max_train-len(top), replace=False)])
        x, y = x[sel], y[sel]
    xt = torch.DoubleTensor(x)
    yt = torch.DoubleTensor(y).unsqueeze(-1)
    yt = (yt - yt.mean()) / (yt.std() + 1e-8)
    gp = SingleTaskGP(xt, yt)
    fit_gpytorch_mll(ExactMarginalLogLikelihood(gp.likelihood, gp))
    gp.eval()
    return gp

def botorch_lcb_torch(gp, beta):
    def f(x):
        post = gp.posterior(x.double())
        return (post.mean - beta*post.variance.clamp_min(1e-12).sqrt()).squeeze(-1).float()
    return f

# ---------------- CMA-ES optimizer (3rd optimizer axis) ---------------------
def cma_opt(score_np, x0, budget=3000, seed=0):
    """Zeroth-order CMA-ES ascent on the surrogate score. Seeds from the best init
    candidate, pools every queried point, returns top-TOP by surrogate score — a
    candidate set consistent with the gradient/perturbation protocols. Returns None
    if pycma is missing (runner skips the cell)."""
    try:
        import cma
    except ImportError:
        return None
    dim = x0.shape[1]
    x_start = x0[int(np.argmax(score_np(x0)))]
    es = cma.CMAEvolutionStrategy(x_start.tolist(), 0.2,
        {'bounds': [0, 1], 'maxfevals': budget, 'verbose': -9, 'seed': seed + 1})
    pool = [x0]
    while not es.stop():
        sols = es.ask()
        arr = np.clip(np.array(sols, dtype=np.float32), 0, 1)
        es.tell(sols, [-v for v in score_np(arr)])   # cma minimizes; we maximize
        pool.append(arr)
    allc = np.concatenate(pool)
    return allc[np.argsort(score_np(allc))[-TOP:]]

# ---------------- SVGP surrogate (3rd surrogate axis, scales past exact GP) --
def fit_svgp(x, y, dim, seed, n_ind=128, iters=250, max_train=2000):
    """Stochastic variational GP (gpytorch). Differentiable posterior -> pairs with
    every optimizer. Returns None if gpytorch is missing."""
    try:
        import gpytorch
        from gpytorch.models import ApproximateGP
        from gpytorch.variational import CholeskyVariationalDistribution, VariationalStrategy
    except ImportError:
        return None
    np.random.seed(seed); torch.manual_seed(seed)
    if len(x) > max_train:
        top = np.argsort(y)[-int(max_train*0.2):]
        rest = np.setdiff1d(np.arange(len(x)), top)
        sel = np.concatenate([top, np.random.choice(rest, max_train-len(top), replace=False)])
        x, y = x[sel], y[sel]
    xt, yt = torch.FloatTensor(x), torch.FloatTensor(y)
    ym, ys = yt.mean(), yt.std() + 1e-8
    yt = (yt - ym) / ys
    ind = xt[torch.randperm(len(xt))[:n_ind]].clone()

    class SVGP(ApproximateGP):
        def __init__(s):
            vd = CholeskyVariationalDistribution(n_ind)
            super().__init__(VariationalStrategy(s, ind, vd, learn_inducing_locations=True))
            s.mean = gpytorch.means.ConstantMean()
            s.cov = gpytorch.kernels.ScaleKernel(gpytorch.kernels.MaternKernel(nu=2.5, ard_num_dims=dim))
        def forward(s, x):
            return gpytorch.distributions.MultivariateNormal(s.mean(x), s.cov(x))

    model = SVGP(); lik = gpytorch.likelihoods.GaussianLikelihood()
    model.train(); lik.train()
    opt = torch.optim.Adam([{'params': model.parameters()}, {'params': lik.parameters()}], lr=0.01)
    mll = gpytorch.mlls.VariationalELBO(lik, model, num_data=len(xt))
    for _ in range(iters):
        opt.zero_grad(); out = model(xt); loss = -mll(out, yt); loss.backward(); opt.step()
    model.eval(); lik.eval()
    return {'model': model, 'lik': lik, 'ym': float(ym), 'ys': float(ys)}

def svgp_lcb_torch(svgp, beta):
    import gpytorch
    m, ym, ys = svgp['model'], svgp['ym'], svgp['ys']
    def f(x):
        with gpytorch.settings.fast_pred_var():
            post = m(x)
        return (post.mean - beta*post.variance.clamp_min(1e-12).sqrt())*ys + ym
    return f

def svgp_lcb_np(svgp, beta):
    f = svgp_lcb_torch(svgp, beta)
    def g(x):
        with torch.no_grad():
            return f(torch.FloatTensor(x)).numpy()
    return g

# ---------------- calibration repair (conformal / temperature) --------------
def conformal_lower_delta(cal_mu, cal_y, alpha):
    """One-sided split-conformal margin q: [mu - q] is a (1-alpha) lower bound for a
    FUTURE EXCHANGEABLE point. Nonconformity = mu - y (over-prediction). Returns the
    finite-sample-valid quantile. NOTE (CCC 2026): validity holds only under
    exchangeability; on OOD candidates the proposal induces covariate shift and this
    margin under-covers — which is exactly what E4 measures, not a bug."""
    res = cal_mu - cal_y                                   # signed over-prediction
    n = len(res)
    k = int(np.ceil((n + 1) * (1 - alpha)))
    return float(np.sort(res)[min(k, n) - 1])

def coverage_of_premise(mu, sigma, f, beta):
    """Empirical P(|mu - f| <= beta*sigma) — the pessimism-guarantee premise."""
    return float(np.mean(np.abs(mu - f) <= beta * sigma))

def fit_conformal_multiplier(mu_cal, sigma_cal, y_cal, alpha=0.1):
    """Calibrated multiplier q that REPLACES the arbitrary beta in LCB: the lower
    bound mu - q*sigma achieves ~1-alpha coverage on exchangeable data. Nonconformity
    is normalized (|mu-y|/sigma), so q scales the uncertainty and therefore reshapes
    the search — unlike a marginal (constant) conformal offset, which only shifts the
    reported bound and leaves the argmax = mean-ascent. This is the honest 'repair the
    calibration of the uncertainty used inside LCB'."""
    r = np.abs(mu_cal - y_cal) / (sigma_cal + 1e-8)
    n = len(r)
    k = min(int(np.ceil((n + 1) * (1 - alpha))), n)
    return float(np.sort(r)[k - 1])

# ---------------- candidate init + scoring ---------------------------------
def init_candidates(x, y, seed):
    """top-TOP dataset points + sigma=0.05 perturbed copies (legacy protocol)."""
    np.random.seed(seed)
    xt = x[np.argsort(y)[-TOP:]]
    xp = np.clip(xt + np.random.randn(*xt.shape).astype(np.float32)*0.05, 0, 1)
    return np.concatenate([xt, xp])

def eval_designs(task, x_final):
    sc = task.oracle(x_final)
    t = np.sort(sc)[-TOP:]
    return float(t[-1]), float(np.median(t))   # p100, p50

# ---------------- offline MBO: compositional surrogate x optimizer grid ------
# A scorer is (f_torch or None, f_np). Optimizers consume whichever they need; a
# cell whose surrogate can't supply the optimizer's input (e.g. exact GP + gradient)
# or whose dependency is missing (svgp without gpytorch, cma without pycma) -> None,
# and the runner skips it. This block IS the paper's decomposition, in code.

def build_surrogate(name, x, y, dim, seed, beta, ep, K):
    """name in {ens, gp, botorchgp, svgp, ens_conformal} -> (f_torch|None, f_np|None)."""
    if name in ('ens', 'ens_conformal'):
        ms = train_ensemble(x, y, dim, seed=seed, K=K, ep=ep)
        if name == 'ens':
            return ens_lcb_torch(ms, beta), ens_lcb_np(ms, beta), ms
        # conformal: split off a calibration fold, fit multiplier q, use mu - q*sigma
        n = len(x); cut = int(0.8 * n)
        idx = np.random.RandomState(seed).permutation(n)
        xc, yc = x[idx[cut:]], y[idx[cut:]]
        with torch.no_grad():
            ps = torch.stack([m(torch.FloatTensor(xc)) for m in ms])
        q = fit_conformal_multiplier(ps.mean(0).numpy(), ps.std(0).numpy(), yc)
        return ens_lcb_torch(ms, q), ens_lcb_np(ms, q), ms      # q replaces beta
    if name == 'gp':
        gp = fit_exact_gp(x, y, dim, seed)
        return None, gp_lcb_np(gp, beta), None                  # exact GP: no grad
    if name == 'botorchgp':
        gp = fit_botorch_gp(x, y, seed)
        if gp is None: return None, None, None
        f = botorch_lcb_torch(gp, beta)
        return f, (lambda xx: f(torch.FloatTensor(xx)).detach().numpy()), None
    if name == 'svgp':
        s = fit_svgp(x, y, dim, seed)
        if s is None: return None, None, None
        return svgp_lcb_torch(s, beta), svgp_lcb_np(s, beta), None
    raise ValueError(name)

def run_grid_cell(task, x, y, x0, seed, surrogate, optimizer, beta, ep, K):
    f_torch, f_np, _ = build_surrogate(surrogate, x, y, task.dim, seed, beta, ep, K)
    if optimizer == 'grad':
        if f_torch is None: return None                          # surrogate not differentiable
        xf = grad_opt(f_torch, torch.FloatTensor(x0), steps=OPT_STEPS)
    elif optimizer == 'perturb':
        if f_np is None: return None
        xf = perturb_opt(f_np, x0)
    elif optimizer == 'cma':
        if f_np is None: return None
        xf = cma_opt(f_np, x0, seed=seed)
        if xf is None: return None                               # pycma missing
    else:
        raise ValueError(optimizer)
    p100, p50 = eval_designs(task, xf)
    return {'p100': p100, 'p50': p50}

def run_offline(task, seed, method, beta=BETA, K=K_ENS, ep=TRAIN_EP):
    """method is either a special baseline (below) or a grid cell 'surrogate:optimizer'.
    Ensemble+gradient family returns extra state (ms/x/y/xf) for O2O reuse."""
    np.random.seed(seed); torch.manual_seed(seed)
    x, y = task.data()
    x0 = init_candidates(x, y, seed)

    if ':' in method:                                            # compositional grid cell
        return run_grid_cell(task, x, y, x0, seed, *method.split(':'), beta, ep, K)

    if method in ('lcb', 'grad_ascent', 'lcb_perturb', 'coms'):
        alpha = 1.0 if method == 'coms' else None
        ms = train_ensemble(x, y, task.dim, seed=seed, K=K, ep=ep, coms_alpha=alpha)
        b = 0.0 if method == 'grad_ascent' else beta
        if method == 'lcb_perturb':
            xf = perturb_opt(ens_lcb_np(ms, b), x0)
        else:
            xf = grad_opt(ens_lcb_torch(ms, b), torch.FloatTensor(x0), steps=OPT_STEPS)
        p100, p50 = eval_designs(task, xf)
        return {'p100': p100, 'p50': p50, 'ms': ms, 'x': x, 'y': y, 'xf': xf}

    if method == 'gp':          # exact GP + perturbation optimizer (legacy name = gp:perturb)
        gp = fit_exact_gp(x, y, task.dim, seed)
        xf = perturb_opt(gp_lcb_np(gp, beta), x0)
        p100, p50 = eval_designs(task, xf)
        return {'p100': p100, 'p50': p50}

    if method == 'gp_grad':     # legacy alias for botorchgp:grad
        return run_grid_cell(task, x, y, x0, seed, 'botorchgp', 'grad', beta, ep, K)

    if method == 'sparse_gp':
        from sklearn.kernel_approximation import Nystroem
        from sklearn.linear_model import Ridge
        from sklearn.pipeline import Pipeline
        n = min(len(x), 1500)
        top = np.argsort(y)[-int(n*0.3):]
        sel = np.concatenate([top, np.random.choice(len(x), n-len(top), replace=False)])
        pipe = Pipeline([('ny', Nystroem(kernel='rbf', gamma=1.0/task.dim,
                                         n_components=min(200, n), random_state=seed)),
                         ('ridge', Ridge(alpha=1.0))])
        pipe.fit(x[sel], y[sel])
        # ponytail: legacy uncertainty proxy = variance of Nystroem features; it is
        # NOT a posterior std. Kept for continuity with results_revision.json;
        # replace with a real sparse-GP posterior if this baseline gets promoted.
        def score(xc):
            preds = pipe.predict(xc)
            fv = np.var(pipe.named_steps['ny'].transform(xc), axis=1)
            return preds - beta * fv / (np.mean(fv) + 1e-8)
        xf = perturb_opt(score, x0)
        p100, p50 = eval_designs(task, xf)
        return {'p100': p100, 'p50': p50}

    if method == 'cbas':
        # ponytail: legacy "CbAS" is a CEM-style elite-resampling loop scored by the
        # ensemble (no VAE, mixes oracle-noised y with model predictions). Label it
        # honestly in the paper ("CEM-style adaptive sampling"), or implement real
        # CbAS before claiming the citation.
        ms = train_ensemble(x, y, task.dim, seed=seed, K=K, ep=ep)
        pop, scores = x.copy(), y.copy()
        for _ in range(5):
            thr = np.percentile(scores, 80)
            elite_idx = scores >= thr
            elite = pop[elite_idx]
            if len(elite) < 10:
                elite = pop[np.argsort(scores)[-10:]]
                elite_scores = scores[np.argsort(scores)[-10:]]
            else:
                elite_scores = scores[elite_idx]
            mu, sd = np.mean(elite, 0), np.std(elite, 0) + 1e-4
            new = np.clip(np.random.randn(min(256, len(pop)), task.dim).astype(np.float32)*sd + mu, 0, 1)
            with torch.no_grad():
                preds = torch.stack([m(torch.FloatTensor(new)) for m in ms]).mean(0).numpy()
            pop = np.concatenate([elite, new])
            scores = np.concatenate([elite_scores, preds])
        xf = np.clip(pop[np.argsort(scores)[-TOP:]], 0, 1).astype(np.float32)
        p100, p50 = eval_designs(task, xf)
        return {'p100': p100, 'p50': p50}

    raise ValueError(f'unknown method {method}')

# The decomposition grid: 3 surrogates x 3 optimizers. GP row uses the BoTorch GP for
# ALL cells (one differentiable surrogate, three optimizers = clean controlled compare).
GRID_SURROGATES = ['ens', 'botorchgp', 'svgp']
GRID_OPTIMIZERS = ['grad', 'perturb', 'cma']
GRID_METHODS = [f'{s}:{o}' for s in GRID_SURROGATES for o in GRID_OPTIMIZERS]
CONFORMAL_METHODS = ['ens_conformal:grad', 'ens_conformal:perturb']   # E4 causal test vs ens:*
BASELINE_METHODS = ['coms', 'cbas', 'sparse_gp', 'grad_ascent', 'gp']  # gp = exact sklearn GP (robustness vs botorchgp)
# ens:grad == 'lcb', ens:perturb == 'lcb_perturb' (kept as O2O-internal names, not swept twice).
OFFLINE_METHODS = GRID_METHODS + CONFORMAL_METHODS + BASELINE_METHODS

# ---------------- unified O2O protocol --------------------------------------
def run_o2o(task, seed, k=50, select='greedy', beta=BETA, lam=0.5, r=0.1, ep=TRAIN_EP):
    """ONE iterative protocol for every selection rule (fixes the legacy confound
    where greedy rows were batch-mode and only diversity was iterative).
    Per pick: score candidates, select 1, query oracle; every 10 picks retrain
    (fresh, ep epochs) and re-optimize 60 steps. Port of legacy run_revision.run_o2o."""
    np.random.seed(seed); torch.manual_seed(seed)
    off = run_offline(task, seed, 'lcb', beta=beta, ep=ep)
    x_data, y_data = off['x'], off['y']
    cur_ms, cur_x = off['ms'], off['xf']
    selected = []
    for j in range(k):
        with torch.no_grad():
            ps = torch.stack([m(torch.FloatTensor(cur_x)) for m in cur_ms])
            mu, sig = ps.mean(0).numpy(), ps.std(0).numpy()
        lcb = mu - beta*sig
        if select == 'diversity' and selected:
            for xj in selected:
                d2 = np.sum((cur_x - xj)**2, axis=1)
                lcb -= lam * np.mean(sig) * np.exp(-d2/(2*r**2))
        if select == 'random':
            bi = np.random.randint(len(cur_x))
        else:
            bi = int(np.argmax(lcb))
        xs = cur_x[bi:bi+1]
        ys = task.oracle(xs).astype(np.float32)
        selected.append(xs[0].copy())
        x_data = np.concatenate([x_data, xs]); y_data = np.concatenate([y_data, ys])
        if (j+1) % 10 == 0 or j == k-1:
            cur_ms = train_ensemble(x_data, y_data, task.dim, seed=seed+10000+j, ep=ep)
            x0 = init_candidates(x_data, y_data, seed+j)
            cur_x = grad_opt(ens_lcb_torch(cur_ms, beta), torch.FloatTensor(x0), steps=60)
    p100_on, p50_on = eval_designs(task, cur_x)
    imp = (p100_on - off['p100'])/abs(off['p100'])*100 if off['p100'] != 0 else 0.0
    return {'off_p100': off['p100'], 'on_p100': p100_on, 'on_p50': p50_on, 'imp': imp}

# ---------------- calibration diagnostics -----------------------------------
def run_calibration(task, seed, n_test=500, ep=TRAIN_EP):
    """spearman(sigma, |mu - f|) and spearman(sigma, mean 5-NN train distance)."""
    from scipy.stats import spearmanr
    from sklearn.neighbors import NearestNeighbors
    np.random.seed(seed); torch.manual_seed(seed)
    x, y = task.data()
    ms = train_ensemble(x, y, task.dim, seed=seed, ep=ep)

    def mu_sig(xx):
        with torch.no_grad():
            ps = torch.stack([m(torch.FloatTensor(xx)) for m in ms])
        return ps.mean(0).numpy(), ps.std(0).numpy()

    # (1) sigma-vs-error diagnostics on in-distribution test points (legacy rho ~0.08)
    xt = np.random.uniform(0, 1, (n_test, task.dim)).astype(np.float32)
    mu, sig = mu_sig(xt)
    err = np.abs(mu - task.oracle(xt))
    dist = NearestNeighbors(n_neighbors=5).fit(x).kneighbors(xt)[0].mean(1)

    # (2) premise coverage P(|mu-f| <= beta*sigma), in-distribution vs on LCB's OOD designs
    x0 = init_candidates(x, y, seed)
    xf = grad_opt(ens_lcb_torch(ms, BETA), torch.FloatTensor(x0), steps=OPT_STEPS)   # what LCB actually proposes
    mu_o, sig_o = mu_sig(xf); f_o = task.oracle(xf)
    betas = [0.5, 1.0, 2.0, 5.0]
    cov_indist = {str(b): coverage_of_premise(mu, sig, task.oracle(xt), b) for b in betas}
    cov_ood = {str(b): coverage_of_premise(mu_o, sig_o, f_o, b) for b in betas}

    # (3) conformal repair: calibrate q on fresh exchangeable data; measure coverage of
    # [mu - q*sigma] in-distribution (should ~= 1-alpha) vs on OOD designs (collapses —
    # the covariate-shift break, CCC 2026). alpha=0.1.
    xc = np.random.uniform(0, 1, (500, task.dim)).astype(np.float32)
    mu_c, sig_c = mu_sig(xc)
    q = fit_conformal_multiplier(mu_c, sig_c, task.oracle(xc), alpha=0.1)
    cov_conf_indist = float(np.mean(task.oracle(xt) >= mu - q*sig))
    cov_conf_ood = float(np.mean(f_o >= mu_o - q*sig_o))

    return {'rho_err': float(spearmanr(sig, err).statistic),
            'rho_knn': float(spearmanr(sig, dist).statistic),
            'cov_indist': cov_indist, 'cov_ood': cov_ood,
            'q_conformal': q, 'cov_conf_indist': cov_conf_indist, 'cov_conf_ood': cov_conf_ood}

# ---------------- smoke check ----------------------------------------------
if __name__ == '__main__':
    t = Branin()
    for m in OFFLINE_METHODS:
        r = run_offline(t, 0, m, ep=3)
        assert r is None or np.isfinite(r['p100']), m
        print(f'{m:20s}', 'skipped (dep missing)' if r is None else f"p100={r['p100']:.3f}")
    o = run_o2o(t, 0, k=10, select='diversity', ep=3)
    assert np.isfinite(o['on_p100'])
    c = run_calibration(t, 0, n_test=200, ep=3)
    assert np.isfinite(c['rho_err']) and 0 <= c['cov_conf_indist'] <= 1
    print(f"calib: rho_err={c['rho_err']:.3f}  cov_indist@2={c['cov_indist']['2.0']:.2f}"
          f"  cov_ood@2={c['cov_ood']['2.0']:.2f}  q={c['q_conformal']:.2f}"
          f"  conf_indist={c['cov_conf_indist']:.2f}  conf_ood={c['cov_conf_ood']:.2f}")
    print('smoke passed')
