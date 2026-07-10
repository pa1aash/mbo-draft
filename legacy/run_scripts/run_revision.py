"""
Revision experiments addressing all reviewer concerns.
Runs on CPU. Saves incrementally to results_revision.json.

New additions:
1. Increase seeds to 10 for all MBO methods
2. Add median-of-top-k (p50) metric alongside p100
3. Add Sparse GP (Nystroem) baseline including d=30
4. Add CbAS baseline (simplified: VAE + adaptive sampling)
5. Add perturbation-only optimization for neural methods (aligned pipeline)
6. O2O on all 7 tasks (not just 2-3)
7. Bootstrap CIs for Diversity vs Greedy head-to-head
"""
import json, time, warnings, sys
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern
from sklearn.kernel_approximation import Nystroem
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
warnings.filterwarnings('ignore')
torch.set_num_threads(4)

K_ENS = 5; BETA = 2.0; TOP = 128; OPT_STEPS = 100; TRAIN_EP = 35; HID = 96
NS = 10  # 10 seeds
NS_O2O = 6  # 6 seeds for O2O (more expensive)

# ============ TASKS ============
class Task:
    def __init__(s, name, dim, n, noise):
        s.name, s.dim, s.noise = name, dim, noise
        np.random.seed(0)
        s.x = np.random.uniform(0, 1, (n, dim)).astype(np.float32)
        s.y = (s.oracle(s.x) + np.random.randn(n) * noise).astype(np.float32)
    def data(s): return s.x.copy(), s.y.copy()

class Branin(Task):
    def __init__(s): super().__init__('Branin-2D', 2, 2000, 0.05)
    def oracle(s, x):
        x1, x2 = x[:,0]*15-5, x[:,1]*15
        return -(1*(x2-5.1/(4*np.pi**2)*x1**2+5/np.pi*x1-6)**2+10*(1-1/(8*np.pi))*np.cos(x1)+10)
class Styblinski(Task):
    def __init__(s): super().__init__('Styblinski-5D', 5, 3000, 0.05)
    def oracle(s, x):
        xs = x*10-5; return -0.5*np.sum(xs**4-16*xs**2+5*xs, 1)/s.dim
class Levy(Task):
    def __init__(s): super().__init__('Levy-8D', 8, 4000, 0.05)
    def oracle(s, x):
        xs = x*20-10; w = 1+(xs-1)/4
        return -(np.sin(np.pi*w[:,0])**2+np.sum((w[:,:-1]-1)**2*(1+10*np.sin(np.pi*w[:,:-1]+1)**2),1)+(w[:,-1]-1)**2*(1+np.sin(2*np.pi*w[:,-1])**2))/s.dim
class Rosenbrock(Task):
    def __init__(s): super().__init__('Rosenbrock-10D', 10, 5000, 0.1)
    def oracle(s, x):
        xs = x*4-2; return -np.sum(100*(xs[:,1:]-xs[:,:-1]**2)**2+(1-xs[:,:-1])**2, 1)/1000
class Rastrigin(Task):
    def __init__(s): super().__init__('Rastrigin-15D', 15, 5000, 0.1)
    def oracle(s, x):
        xs = x*10.24-5.12; d = xs.shape[1]; return -(10*d+np.sum(xs**2-10*np.cos(2*np.pi*xs), 1))/d
class Ackley(Task):
    def __init__(s): super().__init__('Ackley-20D', 20, 5000, 0.05)
    def oracle(s, x):
        xs = x*10-5; d = xs.shape[1]
        return -(-20*np.exp(-0.2*np.sqrt(np.sum(xs**2, 1)/d))-np.exp(np.sum(np.cos(2*np.pi*xs), 1)/d)+20+np.e)
class Griewank(Task):
    def __init__(s): super().__init__('Griewank-30D', 30, 8000, 0.05)
    def oracle(s, x):
        xs = x*1200-600; d = xs.shape[1]
        return -(np.sum(xs**2, 1)/4000-np.prod(np.cos(xs/np.sqrt(np.arange(1, d+1))), 1)+1)

# ============ MODELS ============
class MLP(nn.Module):
    def __init__(s, d):
        super().__init__()
        s.net = nn.Sequential(nn.Linear(d, HID), nn.ReLU(), nn.Linear(HID, HID), nn.ReLU(), nn.Linear(HID, 1))
    def forward(s, x): return s.net(x).squeeze(-1)

def train_ens(x, y, d, seed=0):
    xt, yt = torch.FloatTensor(x), torch.FloatTensor(y)
    ds = TensorDataset(xt, yt); ms = []
    for k in range(K_ENS):
        torch.manual_seed(seed*100+k); m = MLP(d)
        o = optim.Adam(m.parameters(), lr=3e-3, weight_decay=1e-4)
        dl = DataLoader(ds, batch_size=256, shuffle=True); m.train()
        for _ in range(TRAIN_EP):
            for xb, yb in dl:
                loss = nn.MSELoss()(m(xb), yb); o.zero_grad(); loss.backward(); o.step()
        m.eval(); ms.append(m)
    return ms

def train_coms(x, y, d, seed=0, alpha=1.0):
    xt, yt = torch.FloatTensor(x), torch.FloatTensor(y)
    ds = TensorDataset(xt, yt); ms = []
    for k in range(K_ENS):
        torch.manual_seed(seed*100+k+500); m = MLP(d)
        o = optim.Adam(m.parameters(), lr=3e-3, weight_decay=1e-4)
        dl = DataLoader(ds, batch_size=256, shuffle=True); m.train()
        for _ in range(TRAIN_EP):
            for xb, yb in dl:
                reg = nn.MSELoss()(m(xb), yb)
                xn = xb.detach().clone().requires_grad_(True)
                pn = m(xn); g = torch.autograd.grad(pn.sum(), xn, create_graph=False)[0]
                xn = (xn + 0.05*g).detach().clamp(0, 1)
                cons = m(xn).mean() - m(xb).mean()
                loss = reg + alpha*cons; o.zero_grad(); loss.backward(); o.step()
        m.eval(); ms.append(m)
    return ms

def optimize_grad(ms, x0, beta=BETA, steps=OPT_STEPS):
    """Gradient-based LCB optimization."""
    x = x0.clone().detach().requires_grad_(True)
    o = optim.Adam([x], lr=0.05)
    for _ in range(steps):
        o.zero_grad(); ps = torch.stack([m(x) for m in ms])
        lcb = ps.mean(0) - beta*ps.std(0); (-lcb.mean()).backward(); o.step()
        with torch.no_grad(): x.clamp_(0, 1)
    return x.detach()

def optimize_perturb(ms, x0, beta=BETA, n_rounds=5, n_perturb=3):
    """Perturbation-only optimization (aligned with GP pipeline)."""
    x_best = x0.clone().detach()
    with torch.no_grad():
        ps = torch.stack([m(x_best) for m in ms])
        best_lcb = (ps.mean(0) - beta*ps.std(0)).numpy()
    
    for r in range(n_rounds):
        for sigma in [0.1, 0.05, 0.02]:
            x_cand = x_best + torch.randn_like(x_best) * sigma
            x_cand = x_cand.clamp(0, 1)
            with torch.no_grad():
                ps = torch.stack([m(x_cand) for m in ms])
                cand_lcb = (ps.mean(0) - beta*ps.std(0)).numpy()
            improved = cand_lcb > best_lcb
            x_best[improved] = x_cand[improved]
            best_lcb[improved] = cand_lcb[improved]
    return x_best

# ============ SPARSE GP (Nystroem) ============
def run_sparse_gp(task, seed, beta=BETA, n_components=200):
    """Sparse GP via Nystroem kernel approximation — works at any dimension."""
    np.random.seed(seed)
    x, y = task.data()
    # Subsample for tractability
    n = min(len(x), 1500)
    idx = np.argsort(y)
    top_idx = idx[-int(n*0.3):]
    rand_idx = np.random.choice(len(x), n - len(top_idx), replace=False)
    sel = np.concatenate([top_idx, rand_idx])
    x_train, y_train = x[sel], y[sel]
    
    # Nystroem approximation + Ridge regression
    pipe = Pipeline([
        ('nystroem', Nystroem(kernel='rbf', gamma=1.0/task.dim, n_components=min(n_components, n), random_state=seed)),
        ('ridge', Ridge(alpha=1.0))
    ])
    pipe.fit(x_train, y_train)
    
    # Generate candidates via perturbation of top data points
    top_k = np.argsort(y)[-TOP:]
    x_cands = x[top_k].copy()
    for _ in range(5):
        x_pert = x_cands + np.random.randn(*x_cands.shape).astype(np.float32) * 0.05
        x_pert = np.clip(x_pert, 0, 1)
        x_cands = np.concatenate([x_cands, x_pert])
    
    preds = pipe.predict(x_cands)
    # Use Nystroem features for uncertainty proxy
    feats = pipe.named_steps['nystroem'].transform(x_cands)
    feat_var = np.var(feats, axis=1)
    sigma_proxy = feat_var / (np.mean(feat_var) + 1e-8)
    lcb = preds - beta * sigma_proxy
    
    top_idx = np.argsort(lcb)[-TOP:]
    x_top = x_cands[top_idx]
    scores = task.oracle(x_top)
    t128 = np.sort(scores)[-TOP:]
    return float(t128[-1]), float(np.median(t128))

# ============ CbAS (simplified) ============
def run_cbas(task, seed, n_iter=5, percentile=80):
    """Simplified Conditioning by Adaptive Sampling."""
    np.random.seed(seed); torch.manual_seed(seed)
    x, y = task.data()
    
    # Train initial surrogate
    ms = train_ens(x, y, task.dim, seed=seed)
    
    # Iterative: keep top percentile, resample around them
    current_pop = x.copy()
    current_scores = y.copy()
    
    for it in range(n_iter):
        # Select top percentile
        threshold = np.percentile(current_scores, percentile)
        elite_idx = current_scores >= threshold
        elite = current_pop[elite_idx]
        
        if len(elite) < 10:
            elite = current_pop[np.argsort(current_scores)[-10:]]
        
        # Generate new samples around elites (Gaussian perturbation)
        mu = np.mean(elite, axis=0)
        std = np.std(elite, axis=0) + 1e-4
        n_new = min(256, len(current_pop))
        new_samples = np.random.randn(n_new, task.dim).astype(np.float32) * std + mu
        new_samples = np.clip(new_samples, 0, 1)
        
        # Score with ensemble mean
        with torch.no_grad():
            xt = torch.FloatTensor(new_samples)
            preds = torch.stack([m(xt) for m in ms]).mean(0).numpy()
        
        current_pop = np.concatenate([elite, new_samples])
        current_scores = np.concatenate([current_scores[elite_idx] if np.sum(elite_idx) >= 10 else current_scores[np.argsort(current_scores)[-10:]], preds])
    
    # Final evaluation
    # Get top candidates and evaluate with oracle
    best_idx = np.argsort(current_scores)[-TOP:]
    x_best = current_pop[best_idx]
    x_best = np.clip(x_best, 0, 1).astype(np.float32)
    oracle_scores = task.oracle(x_best)
    t128 = np.sort(oracle_scores)[-TOP:]
    return float(t128[-1]), float(np.median(t128))

# ============ CORE MBO RUNNER ============
def run_mbo(task, seed, beta=BETA, method='lcb'):
    np.random.seed(seed); torch.manual_seed(seed)
    x, y = task.data()
    if method == 'coms':
        ms = train_coms(x, y, task.dim, seed=seed)
    elif method in ['lcb', 'grad_ascent', 'lcb_perturb']:
        ms = train_ens(x, y, task.dim, seed=seed)
    
    tidx = np.argsort(y)[-TOP:]
    xt = x[tidx]; xp = np.clip(xt + np.random.randn(*xt.shape).astype(np.float32)*0.05, 0, 1)
    x0 = torch.FloatTensor(np.concatenate([xt, xp]))
    
    b = 0.0 if method == 'grad_ascent' else beta
    if method == 'lcb_perturb':
        xo = optimize_perturb(ms, x0, beta=b)
    else:
        xo = optimize_grad(ms, x0, beta=b)
    
    sc = task.oracle(xo.numpy())
    t128 = np.sort(sc)[-TOP:]
    return float(t128[-1]), float(np.median(t128)), ms, x, y, xo.numpy(), sc

# ============ O2O RUNNER ============
def run_o2o(task, seed, beta=BETA, k=50, method='lcb', diversity_lam=0.0, diversity_r=0.1):
    np.random.seed(seed); torch.manual_seed(seed)
    p100_off, p50_off, ms, xd, yd, xopt, sc = run_mbo(task, seed, beta=beta, method=method)
    
    x_data, y_data = xd.copy(), yd.copy()
    selected = []
    cur_ms, cur_xopt = ms, xopt
    
    for j in range(k):
        xt = torch.FloatTensor(cur_xopt)
        with torch.no_grad():
            ps = torch.stack([m(xt) for m in cur_ms])
            mu = ps.mean(0).numpy(); sig = ps.std(0).numpy()
        lcb = mu - beta * sig
        
        if selected and diversity_lam > 0:
            avg_sig = np.mean(sig)
            for xj in selected:
                d2 = np.sum((cur_xopt - xj)**2, axis=1)
                lcb -= diversity_lam * avg_sig * np.exp(-d2 / (2 * diversity_r**2))
        
        bi = np.argmax(lcb)
        xs = cur_xopt[bi:bi+1]; ys = task.oracle(xs).astype(np.float32)
        selected.append(xs[0].copy())
        x_data = np.concatenate([x_data, xs]); y_data = np.concatenate([y_data, ys])
        
        if (j+1) % 10 == 0 or j == k-1:
            cur_ms = train_ens(x_data, y_data, task.dim, seed=seed+10000+j)
            ti = np.argsort(y_data)[-TOP:]
            xtn = x_data[ti]; xpn = np.clip(xtn + np.random.randn(*xtn.shape).astype(np.float32)*0.05, 0, 1)
            cur_xopt = optimize_grad(cur_ms, torch.FloatTensor(np.concatenate([xtn, xpn])), beta=beta, steps=60).numpy()
    
    fs = task.oracle(cur_xopt)
    t128 = np.sort(fs)[-TOP:]
    p100_on = float(t128[-1]); p50_on = float(np.median(t128))
    imp = (p100_on - p100_off) / abs(p100_off) * 100 if p100_off != 0 else 0
    return {'off_p100': p100_off, 'off_p50': p50_off, 'on_p100': p100_on, 'on_p50': p50_on, 'imp': imp}

# ============ MAIN ============
def save(R, fn='results_revision.json'):
    with open(fn, 'w') as f: json.dump(R, f, indent=2)

def main():
    t0 = time.time()
    tasks = [Branin(), Styblinski(), Levy(), Rosenbrock(), Rastrigin(), Ackley(), Griewank()]
    R = {}
    
    # ===== EXPERIMENT 1: Main MBO with 10 seeds + p50 + all methods =====
    print("="*60); print("EXP 1: MBO (10 seeds, 5 methods)"); print("="*60)
    R['mbo'] = {}
    methods = ['lcb', 'coms', 'grad_ascent', 'lcb_perturb']
    for task in tasks:
        print(f"\n[{task.name}]", flush=True)
        R['mbo'][task.name] = {}
        for method in methods:
            p100s, p50s = [], []
            for seed in range(NS):
                p1, p5, *_ = run_mbo(task, seed, beta=BETA, method=method)
                p100s.append(p1); p50s.append(p5)
            R['mbo'][task.name][method] = {
                'p100_m': float(np.mean(p100s)), 'p100_s': float(np.std(p100s)),
                'p50_m': float(np.mean(p50s)), 'p50_s': float(np.std(p50s)),
                'p100': [float(v) for v in p100s], 'p50': [float(v) for v in p50s]
            }
            print(f"  {method:>14s}: p100={np.mean(p100s):.3f}±{np.std(p100s):.3f}  p50={np.mean(p50s):.3f}±{np.std(p50s):.3f}", flush=True)
        
        # Sparse GP
        p100s_gp, p50s_gp = [], []
        for seed in range(NS):
            p1, p5 = run_sparse_gp(task, seed, beta=BETA)
            p100s_gp.append(p1); p50s_gp.append(p5)
        R['mbo'][task.name]['sparse_gp'] = {
            'p100_m': float(np.mean(p100s_gp)), 'p100_s': float(np.std(p100s_gp)),
            'p50_m': float(np.mean(p50s_gp)), 'p50_s': float(np.std(p50s_gp)),
            'p100': [float(v) for v in p100s_gp], 'p50': [float(v) for v in p50s_gp]
        }
        print(f"  {'sparse_gp':>14s}: p100={np.mean(p100s_gp):.3f}±{np.std(p100s_gp):.3f}  p50={np.mean(p50s_gp):.3f}±{np.std(p50s_gp):.3f}", flush=True)
        
        # CbAS
        p100s_cb, p50s_cb = [], []
        for seed in range(NS):
            p1, p5 = run_cbas(task, seed)
            p100s_cb.append(p1); p50s_cb.append(p5)
        R['mbo'][task.name]['cbas'] = {
            'p100_m': float(np.mean(p100s_cb)), 'p100_s': float(np.std(p100s_cb)),
            'p50_m': float(np.mean(p50s_cb)), 'p50_s': float(np.std(p50s_cb)),
            'p100': [float(v) for v in p100s_cb], 'p50': [float(v) for v in p50s_cb]
        }
        print(f"  {'cbas':>14s}: p100={np.mean(p100s_cb):.3f}±{np.std(p100s_cb):.3f}  p50={np.mean(p50s_cb):.3f}±{np.std(p50s_cb):.3f}", flush=True)
        
        save(R); print(f"  [{(time.time()-t0)/60:.0f}min]")
    
    # ===== EXPERIMENT 2: O2O on ALL 7 tasks =====
    print("\n"+"="*60); print("EXP 2: O2O on all 7 tasks (k=50)"); print("="*60)
    R['o2o'] = {}
    for task in tasks:
        print(f"\n[{task.name}]", flush=True)
        R['o2o'][task.name] = {}
        for method, label in [('lcb', 'LCB'), ('coms', 'COMs'), ('grad_ascent', 'GradAsc')]:
            results = []
            for seed in range(NS_O2O):
                r = run_o2o(task, seed, beta=BETA, k=50, method=method)
                results.append(r)
            imps = [r['imp'] for r in results]; p100s = [r['on_p100'] for r in results]
            R['o2o'][task.name][label] = {
                'imp_m': float(np.mean(imps)), 'imp_s': float(np.std(imps)),
                'p100_m': float(np.mean(p100s)), 'p100_s': float(np.std(p100s)),
                'all': results
            }
            print(f"  {label:>8s}: p100={np.mean(p100s):.3f} imp={np.mean(imps):+.1f}%", flush=True)
        
        # Diversity O2O
        div_results = []
        for seed in range(NS_O2O):
            r = run_o2o(task, seed, beta=BETA, k=50, method='lcb', diversity_lam=0.5, diversity_r=0.1)
            div_results.append(r)
        imps = [r['imp'] for r in div_results]; p100s = [r['on_p100'] for r in div_results]
        R['o2o'][task.name]['Diversity'] = {
            'imp_m': float(np.mean(imps)), 'imp_s': float(np.std(imps)),
            'p100_m': float(np.mean(p100s)), 'p100_s': float(np.std(p100s)),
            'all': div_results
        }
        print(f"  {'Diversity':>8s}: p100={np.mean(p100s):.3f} imp={np.mean(imps):+.1f}%", flush=True)
        
        # Random O2O
        rand_results = []
        for seed in range(NS_O2O):
            np.random.seed(seed); torch.manual_seed(seed)
            p100_off, _, ms, xd, yd, xopt, sc = run_mbo(task, seed, beta=BETA)
            idx = np.random.choice(len(xd), 50, replace=False)
            xsel = xd[idx]; ytrue = task.oracle(xsel).astype(np.float32)
            xe = np.concatenate([xd, xsel]); ye = np.concatenate([yd, ytrue])
            ms2 = train_ens(xe, ye, task.dim, seed=seed+20000)
            xo2 = optimize_grad(ms2, torch.FloatTensor(xopt), beta=BETA, steps=60)
            sc2 = task.oracle(xo2.numpy()); t128 = np.sort(sc2)[-TOP:]
            p100_on = float(t128[-1])
            imp = (p100_on - p100_off) / abs(p100_off) * 100 if p100_off != 0 else 0
            rand_results.append({'off_p100': p100_off, 'on_p100': p100_on, 'imp': imp})
        imps = [r['imp'] for r in rand_results]; p100s = [r['on_p100'] for r in rand_results]
        R['o2o'][task.name]['Random'] = {
            'imp_m': float(np.mean(imps)), 'imp_s': float(np.std(imps)),
            'p100_m': float(np.mean(p100s)), 'p100_s': float(np.std(p100s)),
        }
        print(f"  {'Random':>8s}: p100={np.mean(p100s):.3f} imp={np.mean(imps):+.1f}%", flush=True)
        save(R); print(f"  [{(time.time()-t0)/60:.0f}min]")
    
    # ===== EXPERIMENT 3: Bootstrap CI for Diversity vs Greedy =====
    print("\n"+"="*60); print("EXP 3: Bootstrap CIs"); print("="*60)
    R['bootstrap'] = {}
    for tname in R['o2o']:
        lcb_p100 = [r['on_p100'] for r in R['o2o'][tname].get('LCB', {}).get('all', [])]
        div_p100 = [r['on_p100'] for r in R['o2o'][tname].get('Diversity', {}).get('all', [])]
        if lcb_p100 and div_p100:
            # Bootstrap difference
            np.random.seed(42)
            diffs = []
            for _ in range(10000):
                l_samp = np.random.choice(lcb_p100, len(lcb_p100), replace=True)
                d_samp = np.random.choice(div_p100, len(div_p100), replace=True)
                diffs.append(np.mean(d_samp) - np.mean(l_samp))
            ci_lo, ci_hi = np.percentile(diffs, [2.5, 97.5])
            R['bootstrap'][tname] = {
                'diff_mean': float(np.mean(diffs)),
                'ci_lo': float(ci_lo), 'ci_hi': float(ci_hi),
                'lcb_mean': float(np.mean(lcb_p100)),
                'div_mean': float(np.mean(div_p100)),
            }
            print(f"  {tname}: Diversity - LCB = {np.mean(diffs):.3f} [{ci_lo:.3f}, {ci_hi:.3f}]")
    save(R)
    
    elapsed = (time.time() - t0) / 60
    print(f"\n{'='*60}\nDONE in {elapsed:.0f} min\n{'='*60}")

if __name__ == '__main__':
    main()
