"""
New experiments addressing ICML reviewer demands.
1. GP-LCB baseline on all 7 MBO tasks
2. Ensemble size K ablation (K=2,3,5,10)
3. Beta sweep on Levy-8D and Ackley-20D (where beta=0 wins)
4. Calibration diagnostics (sigma vs error, sigma vs kNN distance)
5. Diversity-aware O2O (with local penalization)
"""
import os, json, time, warnings, sys
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern, WhiteKernel, ConstantKernel
from sklearn.neighbors import NearestNeighbors
from scipy import stats as sp_stats
import copy

warnings.filterwarnings('ignore')
torch.set_num_threads(4)

K_DEFAULT = 5; B0 = 2.0; TOP = 128; STEPS = 120; EP = 40; H = 96; NS = 6

# ============== Tasks (same as original) ==============
class T:
    def __init__(s, name, dim, n, noise):
        s.name, s.dim, s.noise = name, dim, noise
        np.random.seed(0)
        s.x = np.random.uniform(0,1,(n,dim)).astype(np.float32)
        s.y = (s.oracle(s.x)+np.random.randn(n)*noise).astype(np.float32)
    def oracle(s, x): raise NotImplementedError
    def data(s): return s.x.copy(), s.y.copy()

class Branin(T):
    def __init__(s): super().__init__('Branin-2D',2,2000,0.05)
    def oracle(s,x):
        x1,x2=x[:,0]*15-5,x[:,1]*15
        return -(1*(x2-5.1/(4*np.pi**2)*x1**2+5/np.pi*x1-6)**2+10*(1-1/(8*np.pi))*np.cos(x1)+10)

class Styblinski(T):
    def __init__(s): super().__init__('Styblinski-5D',5,3000,0.05)
    def oracle(s,x): xs=x*10-5; return -0.5*np.sum(xs**4-16*xs**2+5*xs,1)/s.dim

class Levy(T):
    def __init__(s): super().__init__('Levy-8D',8,4000,0.05)
    def oracle(s,x):
        xs=x*20-10; w=1+(xs-1)/4
        return -(np.sin(np.pi*w[:,0])**2+np.sum((w[:,:-1]-1)**2*(1+10*np.sin(np.pi*w[:,:-1]+1)**2),1)+(w[:,-1]-1)**2*(1+np.sin(2*np.pi*w[:,-1])**2))/s.dim

class Rosenbrock(T):
    def __init__(s): super().__init__('Rosenbrock-10D',10,5000,0.1)
    def oracle(s,x): xs=x*4-2; return -np.sum(100*(xs[:,1:]-xs[:,:-1]**2)**2+(1-xs[:,:-1])**2,1)/1000

class Rastrigin(T):
    def __init__(s): super().__init__('Rastrigin-15D',15,5000,0.1)
    def oracle(s,x): xs=x*10.24-5.12; d=xs.shape[1]; return -(10*d+np.sum(xs**2-10*np.cos(2*np.pi*xs),1))/d

class Ackley(T):
    def __init__(s): super().__init__('Ackley-20D',20,5000,0.05)
    def oracle(s,x):
        xs=x*10-5; d=xs.shape[1]
        return -(-20*np.exp(-0.2*np.sqrt(np.sum(xs**2,1)/d))-np.exp(np.sum(np.cos(2*np.pi*xs),1)/d)+20+np.e)

class Griewank(T):
    def __init__(s): super().__init__('Griewank-30D',30,8000,0.05)
    def oracle(s,x):
        xs=x*1200-600; d=xs.shape[1]
        return -(np.sum(xs**2,1)/4000-np.prod(np.cos(xs/np.sqrt(np.arange(1,d+1))),1)+1)

# ============== Ensemble Models ==============
class MLP(nn.Module):
    def __init__(s, d, h=H):
        super().__init__()
        s.net = nn.Sequential(nn.Linear(d,h),nn.ReLU(),nn.Linear(h,h),nn.ReLU(),nn.Linear(h,1))
    def forward(s,x): return s.net(x).squeeze(-1)

def train_ens(x, y, d, Kv=K_DEFAULT, seed=0, ep=EP):
    xt, yt = torch.FloatTensor(x), torch.FloatTensor(y)
    ds = TensorDataset(xt, yt)
    ms = []
    for k in range(Kv):
        torch.manual_seed(seed*100+k)
        m = MLP(d); o = optim.Adam(m.parameters(), lr=3e-3, weight_decay=1e-4)
        dl = DataLoader(ds, batch_size=256, shuffle=True)
        m.train()
        for _ in range(ep):
            for xb, yb in dl:
                loss = nn.MSELoss()(m(xb), yb); o.zero_grad(); loss.backward(); o.step()
        m.eval(); ms.append(m)
    return ms

def optimize(ms, x0, beta=B0, steps=STEPS):
    x = x0.clone().detach().requires_grad_(True)
    o = optim.Adam([x], lr=0.05)
    for _ in range(steps):
        o.zero_grad()
        ps = torch.stack([m(x) for m in ms])
        lcb = ps.mean(0) - beta*ps.std(0)
        (-lcb.mean()).backward(); o.step()
        with torch.no_grad(): x.clamp_(0, 1)
    return x.detach()

def run_mbo_ens(task, seed, beta=B0, Kv=K_DEFAULT):
    np.random.seed(seed); torch.manual_seed(seed)
    x, y = task.data()
    ms = train_ens(x, y, task.dim, Kv=Kv, seed=seed)
    tidx = np.argsort(y)[-TOP:]
    xt = x[tidx]
    xp = np.clip(xt + np.random.randn(*xt.shape).astype(np.float32)*0.05, 0, 1)
    x0 = torch.FloatTensor(np.concatenate([xt, xp]))
    xo = optimize(ms, x0, beta=beta)
    sc = task.oracle(xo.numpy())
    t128 = np.sort(sc)[-TOP:]
    return float(t128[-1]), float(np.median(t128)), ms, x, y

# ============== GP-LCB Baseline ==============
def run_gp_lcb(task, seed, beta=2.0, max_train=800):
    """GP-LCB using sklearn GaussianProcessRegressor.
    For high-dim tasks, subsample training data to max_train points for GP tractability."""
    np.random.seed(seed)
    x, y = task.data()
    
    # Subsample for GP tractability (GP is O(n^3))
    n = len(x)
    if n > max_train:
        # Keep top 20% by score + random sample the rest
        top_idx = np.argsort(y)[-int(max_train*0.2):]
        remaining = np.setdiff1d(np.arange(n), top_idx)
        rand_idx = np.random.choice(remaining, max_train - len(top_idx), replace=False)
        idx = np.concatenate([top_idx, rand_idx])
        x_gp, y_gp = x[idx], y[idx]
    else:
        x_gp, y_gp = x, y
    
    # Fit GP
    kernel = ConstantKernel(1.0) * Matern(length_scale=np.ones(task.dim)*0.3, nu=2.5) + WhiteKernel(noise_level=0.01)
    gp = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=2, normalize_y=True, alpha=1e-6)
    
    try:
        gp.fit(x_gp, y_gp)
    except Exception as e:
        print(f"  GP fit failed: {e}", flush=True)
        return float('nan'), float('nan')
    
    # Optimize: generate candidates and evaluate LCB
    tidx = np.argsort(y)[-TOP:]
    xt = x[tidx]
    # Add perturbations
    candidates = np.clip(
        np.concatenate([xt, xt + np.random.randn(*xt.shape).astype(np.float32)*0.1,
                        np.random.uniform(0, 1, (TOP, task.dim)).astype(np.float32)]),
        0, 1
    )
    
    # Multi-round refinement via random perturbations (since GP not differentiable easily)
    for _ in range(5):
        mu, sigma = gp.predict(candidates, return_std=True)
        lcb = mu - beta * sigma
        best_idx = np.argsort(lcb)[-TOP//2:]  # top half
        best_x = candidates[best_idx]
        # Perturb best
        new_cands = np.clip(best_x + np.random.randn(*best_x.shape).astype(np.float32)*0.05, 0, 1)
        candidates = np.concatenate([candidates, new_cands])
    
    mu_final, sigma_final = gp.predict(candidates, return_std=True)
    lcb_final = mu_final - beta * sigma_final
    best_128 = candidates[np.argsort(lcb_final)[-TOP:]]
    
    sc = task.oracle(best_128)
    t128 = np.sort(sc)[-TOP:]
    return float(t128[-1]), float(np.median(t128))

# ============== Calibration Diagnostics ==============
def compute_calibration(task, seed, Kv=K_DEFAULT, n_test=1000):
    """Compute sigma vs error and sigma vs kNN distance correlations."""
    np.random.seed(seed); torch.manual_seed(seed)
    x, y = task.data()
    ms = train_ens(x, y, task.dim, Kv=Kv, seed=seed)
    
    # Generate test points: mix of in-distribution and OOD
    x_test = np.random.uniform(0, 1, (n_test, task.dim)).astype(np.float32)
    y_test = task.oracle(x_test)
    
    # Ensemble predictions
    with torch.no_grad():
        xt = torch.FloatTensor(x_test)
        preds = torch.stack([m(xt) for m in ms])
        mu = preds.mean(0).numpy()
        sigma = preds.std(0).numpy()
    
    # Actual error
    error = np.abs(mu - y_test)
    
    # kNN distance to training data
    nn = NearestNeighbors(n_neighbors=5, metric='euclidean')
    nn.fit(x)
    dists, _ = nn.kneighbors(x_test)
    knn_dist = dists.mean(axis=1)  # average of k nearest distances
    
    # Correlations
    rho_sigma_error, p_sigma_error = sp_stats.spearmanr(sigma, error)
    rho_sigma_dist, p_sigma_dist = sp_stats.spearmanr(sigma, knn_dist)
    rho_dist_error, p_dist_error = sp_stats.spearmanr(knn_dist, error)
    
    return {
        'rho_sigma_error': float(rho_sigma_error),
        'p_sigma_error': float(p_sigma_error),
        'rho_sigma_dist': float(rho_sigma_dist),
        'p_sigma_dist': float(p_sigma_dist),
        'rho_dist_error': float(rho_dist_error),
        'p_dist_error': float(p_dist_error),
    }

# ============== Diversity-aware O2O ==============
def run_o2o_diversity(task, seed, beta=B0, k=50):
    """O2O with local penalization for diversity."""
    np.random.seed(seed); torch.manual_seed(seed)
    x, y = task.data()
    ms = train_ens(x, y, task.dim, seed=seed)
    
    tidx = np.argsort(y)[-TOP:]
    xt = x[tidx]
    xp = np.clip(xt + np.random.randn(*xt.shape).astype(np.float32)*0.05, 0, 1)
    x0 = torch.FloatTensor(np.concatenate([xt, xp]))
    xo = optimize(ms, x0, beta=beta)
    sc_off = task.oracle(xo.numpy())
    p100_off = float(np.sort(sc_off)[-TOP:][-1])
    
    selected = []
    x_data = x.copy()
    y_data = y.copy()
    
    for j in range(k):
        # Retrain every 10 evals
        if j % 10 == 0:
            ms = train_ens(x_data, y_data, task.dim, seed=seed+j, ep=20)
            xo = optimize(ms, torch.FloatTensor(np.concatenate([
                x_data[np.argsort(y_data)[-TOP:]],
                x_data[np.argsort(y_data)[-TOP:]] + np.random.randn(TOP, task.dim).astype(np.float32)*0.05
            ]).clip(0,1)), beta=beta, steps=60)
        
        # Score candidates with LCB
        with torch.no_grad():
            preds = torch.stack([m(xo) for m in ms])
            mu_cand = preds.mean(0).numpy()
            sigma_cand = preds.std(0).numpy()
        
        lcb_scores = mu_cand - beta * sigma_cand
        
        # Local penalization: penalize candidates near already-selected points
        if len(selected) > 0:
            sel_arr = np.array(selected)
            cand_arr = xo.numpy()
            for si in range(len(sel_arr)):
                dists = np.linalg.norm(cand_arr - sel_arr[si], axis=1)
                penalty = np.exp(-dists**2 / (2 * 0.1**2))  # Gaussian penalty
                lcb_scores -= 0.5 * sigma_cand.mean() * penalty
        
        best_idx = np.argmax(lcb_scores)
        x_new = xo[best_idx].numpy()
        y_new = float(task.oracle(x_new.reshape(1, -1))[0])
        
        selected.append(x_new.copy())
        x_data = np.concatenate([x_data, x_new.reshape(1, -1)])
        y_data = np.concatenate([y_data, [y_new]])
    
    p100_on = float(np.max(y_data[-k:]))  # best from online evals
    p100_final = float(np.max(y_data))
    imp = (p100_final - p100_off) / abs(p100_off) * 100 if p100_off != 0 else 0
    
    return p100_off, p100_final, imp

# ============== MAIN ==============
def main():
    t0 = time.time()
    tasks = [Branin(), Styblinski(), Levy(), Rosenbrock(), Rastrigin(), Ackley(), Griewank()]
    
    # Load existing results
    try:
        with open('results.json') as f:
            R = json.load(f)
    except:
        R = {}
    
    R['new'] = {}
    
    # ============================================================
    # EXP A: GP-LCB BASELINE
    # ============================================================
    print("="*60)
    print("EXP A: GP-LCB BASELINE")
    print("="*60)
    R['new']['gp_lcb'] = {}
    for task in tasks:
        print(f"\n[{task.name}] dim={task.dim}", flush=True)
        if task.dim > 20:
            print(f"  Skipping GP-LCB (dim={task.dim} too high for GP)", flush=True)
            R['new']['gp_lcb'][task.name] = {'p100_m': float('nan'), 'p100_s': float('nan'),
                                              'p50_m': float('nan'), 'p50_s': float('nan'),
                                              'note': 'skipped_high_dim'}
            continue
        
        p100s, p50s = [], []
        for seed in range(NS):
            p1, p5 = run_gp_lcb(task, seed, beta=B0)
            p100s.append(p1); p50s.append(p5)
            print(f"  seed {seed}: p100={p1:.4f}", flush=True)
        
        R['new']['gp_lcb'][task.name] = {
            'p100_m': float(np.nanmean(p100s)), 'p100_s': float(np.nanstd(p100s)),
            'p50_m': float(np.nanmean(p50s)), 'p50_s': float(np.nanstd(p50s)),
            'p100': p100s, 'p50': p50s
        }
        print(f"  GP-LCB: p100={np.nanmean(p100s):.4f}±{np.nanstd(p100s):.4f}", flush=True)
    
    with open('results_new.json', 'w') as f:
        json.dump(R['new'], f, indent=2)
    print(f"  [{(time.time()-t0)/60:.1f}min]")
    
    # ============================================================
    # EXP B: ENSEMBLE SIZE K ABLATION
    # ============================================================
    print("\n" + "="*60)
    print("EXP B: ENSEMBLE SIZE K ABLATION")
    print("="*60)
    R['new']['K_ablation'] = {}
    abl_tasks = [tasks[0], tasks[1], tasks[3], tasks[4], tasks[5]]  # Branin, Styblinski, Rosenbrock, Rastrigin, Ackley
    K_values = [2, 3, 5, 10]
    
    for task in abl_tasks:
        print(f"\n[{task.name}]", flush=True)
        R['new']['K_ablation'][task.name] = {}
        for Kv in K_values:
            p100s = []
            for seed in range(4):
                p1, _, _, _, _ = run_mbo_ens(task, seed, beta=B0, Kv=Kv)
                p100s.append(p1)
            R['new']['K_ablation'][task.name][str(Kv)] = {
                'm': float(np.mean(p100s)), 's': float(np.std(p100s)), 'all': p100s
            }
            print(f"  K={Kv}: p100={np.mean(p100s):.4f}±{np.std(p100s):.4f}", flush=True)
    
    with open('results_new.json', 'w') as f:
        json.dump(R['new'], f, indent=2)
    print(f"  [{(time.time()-t0)/60:.1f}min]")
    
    # ============================================================
    # EXP C: BETA SWEEP ON LEVY AND ACKLEY (WHERE BETA=0 WINS)
    # ============================================================
    print("\n" + "="*60)
    print("EXP C: BETA SWEEP ON LEVY AND ACKLEY")
    print("="*60)
    R['new']['beta_counter'] = {}
    beta_vals = [0.0, 0.5, 1.0, 2.0, 5.0]
    for task in [tasks[2], tasks[5]]:  # Levy, Ackley
        print(f"\n[{task.name}]", flush=True)
        R['new']['beta_counter'][task.name] = {}
        for beta in beta_vals:
            p100s = []
            for seed in range(4):
                p1, _, _, _, _ = run_mbo_ens(task, seed, beta=beta)
                p100s.append(p1)
            R['new']['beta_counter'][task.name][str(beta)] = {
                'm': float(np.mean(p100s)), 's': float(np.std(p100s)), 'all': p100s
            }
            print(f"  beta={beta}: p100={np.mean(p100s):.4f}±{np.std(p100s):.4f}", flush=True)
    
    with open('results_new.json', 'w') as f:
        json.dump(R['new'], f, indent=2)
    print(f"  [{(time.time()-t0)/60:.1f}min]")
    
    # ============================================================
    # EXP D: CALIBRATION DIAGNOSTICS
    # ============================================================
    print("\n" + "="*60)
    print("EXP D: CALIBRATION DIAGNOSTICS")
    print("="*60)
    R['new']['calibration'] = {}
    for task in tasks:
        print(f"\n[{task.name}]", flush=True)
        cal_results = []
        for seed in range(3):
            cal = compute_calibration(task, seed)
            cal_results.append(cal)
            print(f"  seed {seed}: rho(sigma,error)={cal['rho_sigma_error']:.3f}, "
                  f"rho(sigma,kNN)={cal['rho_sigma_dist']:.3f}", flush=True)
        
        # Average across seeds
        avg_cal = {}
        for key in cal_results[0]:
            avg_cal[key] = float(np.mean([c[key] for c in cal_results]))
        avg_cal['per_seed'] = cal_results
        R['new']['calibration'][task.name] = avg_cal
    
    with open('results_new.json', 'w') as f:
        json.dump(R['new'], f, indent=2)
    print(f"  [{(time.time()-t0)/60:.1f}min]")
    
    # ============================================================
    # EXP E: DIVERSITY-AWARE O2O
    # ============================================================
    print("\n" + "="*60)
    print("EXP E: DIVERSITY-AWARE O2O")
    print("="*60)
    R['new']['o2o_diversity'] = {}
    for task in [tasks[1], tasks[3]]:  # Styblinski, Rosenbrock
        print(f"\n[{task.name}]", flush=True)
        R['new']['o2o_diversity'][task.name] = {}
        for k in [25, 50]:
            imps, finals = [], []
            for seed in range(NS):
                p_off, p_final, imp = run_o2o_diversity(task, seed, beta=B0, k=k)
                imps.append(imp); finals.append(p_final)
                print(f"  k={k} seed={seed}: off={p_off:.3f}, final={p_final:.3f}, imp={imp:+.1f}%", flush=True)
            R['new']['o2o_diversity'][task.name][str(k)] = {
                'imp_m': float(np.mean(imps)), 'imp_s': float(np.std(imps)),
                'p100_m': float(np.mean(finals)), 'p100_s': float(np.std(finals)),
                'imp': imps, 'p100': finals
            }
            print(f"  DIVERSITY k={k}: imp={np.mean(imps):+.1f}%±{np.std(imps):.1f}%, "
                  f"p100={np.mean(finals):.3f}", flush=True)
    
    with open('results_new.json', 'w') as f:
        json.dump(R['new'], f, indent=2)
    
    el = (time.time()-t0)/60
    print(f"\n{'='*60}\nALL NEW EXPERIMENTS DONE in {el:.1f}min\n{'='*60}")

if __name__ == '__main__':
    main()
