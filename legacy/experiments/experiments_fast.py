"""
UNICORN: Unified Conservative Offline-to-Online Framework for Decision-Making
FAST VERSION — Optimized for CPU execution

Experiments for ICML 2026 Workshop Paper
"""

import os, json, time, warnings
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import copy

warnings.filterwarnings('ignore')

DEVICE = torch.device('cpu')
NUM_SEEDS = 8
ENSEMBLE_K = 5
BETA_VALUES = [0.0, 0.5, 1.0, 2.0, 5.0]
DEFAULT_BETA = 2.0
ONLINE_BUDGETS = [10, 25, 50]
N_CANDIDATES = 256
N_OPT_STEPS = 150
LR_SURROGATE = 3e-3
LR_OPTIMIZE = 0.05
EPOCHS = 50  # Reduced from 100
HIDDEN = 128  # Reduced from 256
TOP_K = 128

# ============================================================
# Benchmark Tasks
# ============================================================

class Task:
    def __init__(self, name, dim, n, noise=0.01):
        self.name, self.dim, self.noise = name, dim, noise
        np.random.seed(0)
        self.x = np.random.uniform(0, 1, (n, dim)).astype(np.float32)
        self.y = (self.oracle(self.x) + np.random.randn(n)*noise).astype(np.float32)
    
    def oracle(self, x): raise NotImplementedError
    def get_data(self): return self.x.copy(), self.y.copy()
    def evaluate(self, x): return self.oracle(x)

class Branin(Task):
    def __init__(self): super().__init__('Branin-2D', 2, 2000, 0.05)
    def oracle(self, x):
        x1, x2 = x[:,0]*15-5, x[:,1]*15
        return -(1*(x2-5.1/(4*np.pi**2)*x1**2+5/np.pi*x1-6)**2+10*(1-1/(8*np.pi))*np.cos(x1)+10)

class Styblinski(Task):
    def __init__(self): super().__init__('Styblinski-5D', 5, 3000, 0.05)
    def oracle(self, x):
        xs = x*10-5
        return -0.5*np.sum(xs**4-16*xs**2+5*xs, axis=1)/self.dim

class Levy(Task):
    def __init__(self): super().__init__('Levy-8D', 8, 4000, 0.05)
    def oracle(self, x):
        xs = x*20-10; w = 1+(xs-1)/4
        return -(np.sin(np.pi*w[:,0])**2 + np.sum((w[:,:-1]-1)**2*(1+10*np.sin(np.pi*w[:,:-1]+1)**2),1) + (w[:,-1]-1)**2*(1+np.sin(2*np.pi*w[:,-1])**2))/self.dim

class Rosenbrock(Task):
    def __init__(self): super().__init__('Rosenbrock-10D', 10, 5000, 0.1)
    def oracle(self, x):
        xs = x*4-2
        return -np.sum(100*(xs[:,1:]-xs[:,:-1]**2)**2+(1-xs[:,:-1])**2,1)/1000

class Rastrigin(Task):
    def __init__(self): super().__init__('Rastrigin-15D', 15, 5000, 0.1)
    def oracle(self, x):
        xs = x*10.24-5.12; d = xs.shape[1]
        return -(10*d+np.sum(xs**2-10*np.cos(2*np.pi*xs),1))/d

class Ackley(Task):
    def __init__(self): super().__init__('Ackley-20D', 20, 5000, 0.05)
    def oracle(self, x):
        xs = x*10-5; d = xs.shape[1]
        return -(-20*np.exp(-0.2*np.sqrt(np.sum(xs**2,1)/d))-np.exp(np.sum(np.cos(2*np.pi*xs),1)/d)+20+np.e)

class Griewank(Task):
    def __init__(self): super().__init__('Griewank-30D', 30, 8000, 0.05)
    def oracle(self, x):
        xs = x*1200-600; d = xs.shape[1]
        return -(np.sum(xs**2,1)/4000-np.prod(np.cos(xs/np.sqrt(np.arange(1,d+1))),1)+1)

# ============================================================
# Models
# ============================================================

class MLP(nn.Module):
    def __init__(self, d, h=HIDDEN):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(d,h),nn.ReLU(),nn.Linear(h,h),nn.ReLU(),nn.Linear(h,1))
    def forward(self, x): return self.net(x).squeeze(-1)

def train_ensemble(x, y, d, K=ENSEMBLE_K, ep=EPOCHS, lr=LR_SURROGATE, bs=256, seed=0):
    xt, yt = torch.FloatTensor(x), torch.FloatTensor(y)
    ds = TensorDataset(xt, yt)
    models = []
    for k in range(K):
        torch.manual_seed(seed*1000+k)
        m = MLP(d); opt = optim.Adam(m.parameters(), lr=lr, weight_decay=1e-4)
        dl = DataLoader(ds, batch_size=bs, shuffle=True)
        m.train()
        for _ in range(ep):
            for xb, yb in dl:
                loss = nn.MSELoss()(m(xb), yb)
                opt.zero_grad(); loss.backward(); opt.step()
        m.eval(); models.append(m)
    return models

def train_coms(x, y, d, K=ENSEMBLE_K, ep=EPOCHS, alpha=1.0, lr=LR_SURROGATE, bs=256, seed=0):
    xt, yt = torch.FloatTensor(x), torch.FloatTensor(y)
    ds = TensorDataset(xt, yt)
    models = []
    for k in range(K):
        torch.manual_seed(seed*1000+k+500)
        m = MLP(d); opt = optim.Adam(m.parameters(), lr=lr, weight_decay=1e-4)
        dl = DataLoader(ds, batch_size=bs, shuffle=True)
        m.train()
        for _ in range(ep):
            for xb, yb in dl:
                pred = m(xb); reg = nn.MSELoss()(pred, yb)
                xn = xb.detach().clone().requires_grad_(True)
                pn = m(xn); g = torch.autograd.grad(pn.sum(), xn, create_graph=False)[0]
                xn = (xn+0.05*g).detach().clamp(0,1)
                cons = m(xn).mean() - m(xb).mean()
                loss = reg + alpha*cons
                opt.zero_grad(); loss.backward(); opt.step()
        m.eval(); models.append(m)
    return models

def lcb_optimize(models, x_init, beta=DEFAULT_BETA, steps=N_OPT_STEPS, lr=LR_OPTIMIZE):
    x = x_init.clone().detach().requires_grad_(True)
    opt = optim.Adam([x], lr=lr)
    for _ in range(steps):
        opt.zero_grad()
        preds = torch.stack([m(x) for m in models])
        lcb = preds.mean(0) - beta*preds.std(0)
        (-lcb.mean()).backward(); opt.step()
        with torch.no_grad(): x.clamp_(0,1)
    return x.detach()

# ============================================================
# Offline MBO
# ============================================================

def run_mbo(task, seed, beta=DEFAULT_BETA, method='lcb'):
    np.random.seed(seed); torch.manual_seed(seed)
    x, y = task.get_data()
    if method == 'coms':
        models = train_coms(x, y, task.dim, seed=seed)
    else:
        models = train_ensemble(x, y, task.dim, seed=seed)
    
    top_idx = np.argsort(y)[-TOP_K:]
    x_top = x[top_idx]
    x_pert = np.clip(x_top + np.random.randn(*x_top.shape).astype(np.float32)*0.05, 0, 1)
    x_init = torch.FloatTensor(np.concatenate([x_top, x_pert]))
    
    b = 0.0 if method == 'grad_ascent' else beta
    x_opt = lcb_optimize(models, x_init, beta=b)
    scores = task.evaluate(x_opt.numpy())
    top128 = np.sort(scores)[-TOP_K:]
    
    return {'p100': float(top128[-1]), 'p50': float(np.median(top128)), 
            'mean': float(top128.mean()), 'x_opt': x_opt.numpy(), 'scores': scores,
            'models': models, 'x_data': x, 'y_data': y}

# ============================================================
# Offline-to-Online MBO
# ============================================================

def run_o2o(task, seed, beta=DEFAULT_BETA, k=50, method='lcb'):
    np.random.seed(seed); torch.manual_seed(seed)
    off = run_mbo(task, seed, beta=beta, method=method)
    off_p100 = off['p100']
    
    # Select top-k for online evaluation
    top_k_idx = np.argsort(off['scores'])[-k:]
    x_sel = off['x_opt'][top_k_idx]
    y_true = task.evaluate(x_sel).astype(np.float32)
    
    # Expand dataset and retrain
    x_exp = np.concatenate([off['x_data'], x_sel])
    y_exp = np.concatenate([off['y_data'], y_true])
    
    if method == 'coms':
        models = train_coms(x_exp, y_exp, task.dim, seed=seed+10000)
    else:
        models = train_ensemble(x_exp, y_exp, task.dim, seed=seed+10000)
    
    b = 0.0 if method == 'grad_ascent' else beta
    x_reopt = lcb_optimize(models, torch.FloatTensor(off['x_opt']), beta=b)
    scores = task.evaluate(x_reopt.numpy())
    top128 = np.sort(scores)[-TOP_K:]
    on_p100 = float(top128[-1])
    
    imp = (on_p100 - off_p100) / abs(off_p100) * 100 if off_p100 != 0 else 0
    return {'off_p100': off_p100, 'on_p100': on_p100, 'imp': imp, 'on_p50': float(np.median(top128))}

def run_o2o_random(task, seed, beta=DEFAULT_BETA, k=50):
    np.random.seed(seed); torch.manual_seed(seed)
    off = run_mbo(task, seed, beta=beta)
    off_p100 = off['p100']
    
    idx = np.random.choice(len(off['x_data']), k, replace=False)
    x_sel = off['x_data'][idx]
    y_true = task.evaluate(x_sel).astype(np.float32)
    
    x_exp = np.concatenate([off['x_data'], x_sel])
    y_exp = np.concatenate([off['y_data'], y_true])
    models = train_ensemble(x_exp, y_exp, task.dim, seed=seed+20000)
    
    x_reopt = lcb_optimize(models, torch.FloatTensor(off['x_opt']), beta=beta)
    scores = task.evaluate(x_reopt.numpy())
    on_p100 = float(np.sort(scores)[-TOP_K:][-1])
    imp = (on_p100 - off_p100) / abs(off_p100) * 100 if off_p100 != 0 else 0
    return {'off_p100': off_p100, 'on_p100': on_p100, 'imp': imp}

# ============================================================
# Offline RL
# ============================================================

class QNet(nn.Module):
    def __init__(self, sd, ad, h=128):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(sd+ad,h),nn.ReLU(),nn.Linear(h,h),nn.ReLU(),nn.Linear(h,1))
    def forward(self, s, a): return self.net(torch.cat([s,a],-1)).squeeze(-1)

def gen_rl_data(sd, ad, n_ep=500, H=50, noise=0.5, seed=42):
    np.random.seed(seed)
    S, A, R, NS, D = [],[],[],[],[]
    for _ in range(n_ep):
        s = np.random.randn(sd).astype(np.float32)*0.5
        for t in range(H):
            a = np.clip(np.random.randn(ad).astype(np.float32)*noise - 0.1*s[:ad], -1, 1)
            # Reward: negative quadratic in state + small action penalty
            r = float(-np.sum(s**2)*0.1 - np.sum(a**2)*0.01)
            ns = (0.95*s + 0.3*np.random.randn(sd).astype(np.float32) + 
                  np.pad(a, (0, max(0,sd-ad)))*0.2).astype(np.float32)
            S.append(s); A.append(a); R.append(r); NS.append(ns); D.append(t==H-1)
            s = ns
    return {k:np.array(v,dtype=np.float32) for k,v in 
            zip(['s','a','r','ns','d'],[S,A,R,NS,D])}

def train_q_ens(data, sd, ad, K=ENSEMBLE_K, ep=30, beta=2.0, lr=3e-4, bs=256, gamma=0.99, seed=0):
    st = torch.FloatTensor(data['s']); at = torch.FloatTensor(data['a'])
    rt = torch.FloatTensor(data['r']); nst = torch.FloatTensor(data['ns'])
    dt = torch.FloatTensor(data['d'])
    ds = TensorDataset(st, at, rt, nst, dt)
    models = []
    for k in range(K):
        torch.manual_seed(seed*1000+k)
        q = QNet(sd, ad); qt = copy.deepcopy(q)
        opt = optim.Adam(q.parameters(), lr=lr)
        dl = DataLoader(ds, batch_size=bs, shuffle=True)
        for _ in range(ep):
            for sb, ab, rb, nsb, db in dl:
                with torch.no_grad():
                    na = at[torch.randint(0,len(at),(len(sb),))]
                    tgt = rb + gamma*(1-db)*qt(nsb, na)
                td = nn.MSELoss()(q(sb,ab), tgt)
                ra = torch.randn_like(ab)
                cons = q(sb,ra).mean() - q(sb,ab).mean()
                loss = td + 0.5*cons
                opt.zero_grad(); loss.backward(); opt.step()
            with torch.no_grad():
                for p,pt in zip(q.parameters(),qt.parameters()):
                    pt.data.mul_(0.995).add_(p.data,alpha=0.005)
        q.eval(); models.append(q)
    return models

def eval_rl(models, sd, ad, H=50, beta=2.0, n_eval=30, seed=0):
    np.random.seed(seed); rets = []
    for _ in range(n_eval):
        s = np.random.randn(sd).astype(np.float32)*0.5; ret = 0
        for t in range(H):
            st = torch.FloatTensor(s).unsqueeze(0).repeat(64,1)
            ac = torch.randn(64, ad).clamp(-1,1)
            with torch.no_grad():
                qp = torch.stack([m(st,ac) for m in models])
                lcb = qp.mean(0)-beta*qp.std(0)
            a = ac[lcb.argmax()].numpy()
            r = float(-np.sum(s**2)*0.1-np.sum(a**2)*0.01)
            ret += r
            s = (0.95*s+0.3*np.random.randn(sd).astype(np.float32)+np.pad(a,(0,max(0,sd-ad)))*0.2).astype(np.float32)
        rets.append(ret)
    return float(np.mean(rets)), float(np.std(rets))

# ============================================================
# MAIN
# ============================================================

def main():
    t0 = time.time()
    tasks = [Branin(), Styblinski(), Levy(), Rosenbrock(), Rastrigin(), Ackley(), Griewank()]
    results = {'mbo': {}, 'o2o': {}, 'rl': {}, 'ablation': {}}
    
    # === EXP 1: Offline MBO ===
    print("="*60)
    print("EXPERIMENT 1: Offline MBO")
    print("="*60)
    
    for task in tasks:
        print(f"\n[{task.name}] dim={task.dim}")
        results['mbo'][task.name] = {}
        for method in ['lcb', 'coms', 'grad_ascent']:
            p100s, p50s = [], []
            for seed in range(NUM_SEEDS):
                r = run_mbo(task, seed, beta=DEFAULT_BETA, method=method)
                p100s.append(r['p100']); p50s.append(r['p50'])
            results['mbo'][task.name][method] = {
                'p100_mean': float(np.mean(p100s)), 'p100_std': float(np.std(p100s)),
                'p50_mean': float(np.mean(p50s)), 'p50_std': float(np.std(p50s)),
                'p100_all': [float(v) for v in p100s], 'p50_all': [float(v) for v in p50s]
            }
            print(f"  {method:>12s}: p100={np.mean(p100s):.4f}±{np.std(p100s):.4f}  p50={np.mean(p50s):.4f}±{np.std(p50s):.4f}")
        print(f"  Time so far: {(time.time()-t0)/60:.1f}min")
    
    # === EXP 2: Offline-to-Online MBO ===
    print("\n"+"="*60)
    print("EXPERIMENT 2: Offline-to-Online MBO")
    print("="*60)
    
    for task in tasks:
        print(f"\n[{task.name}]")
        results['o2o'][task.name] = {}
        for k in ONLINE_BUDGETS:
            res_k = {}
            for method, mname in [('lcb','LCB+O2O'),('coms','COMs+O2O'),('grad_ascent','Naive+O2O')]:
                imps = []; p100s = []
                for seed in range(NUM_SEEDS):
                    r = run_o2o(task, seed, beta=DEFAULT_BETA, k=k, method=method)
                    imps.append(r['imp']); p100s.append(r['on_p100'])
                res_k[mname] = {
                    'imp_mean': float(np.mean(imps)), 'imp_std': float(np.std(imps)),
                    'p100_mean': float(np.mean(p100s)), 'p100_std': float(np.std(p100s)),
                    'imp_all': [float(v) for v in imps], 'p100_all': [float(v) for v in p100s]
                }
                print(f"  k={k:2d} {mname:>12s}: p100={np.mean(p100s):.4f}  imp={np.mean(imps):+.1f}%")
            # Random baseline
            imps_r = []; p100s_r = []
            for seed in range(NUM_SEEDS):
                r = run_o2o_random(task, seed, beta=DEFAULT_BETA, k=k)
                imps_r.append(r['imp']); p100s_r.append(r['on_p100'])
            res_k['Random+O2O'] = {
                'imp_mean': float(np.mean(imps_r)), 'imp_std': float(np.std(imps_r)),
                'p100_mean': float(np.mean(p100s_r)), 'p100_std': float(np.std(p100s_r)),
            }
            print(f"  k={k:2d} {'Random+O2O':>12s}: p100={np.mean(p100s_r):.4f}  imp={np.mean(imps_r):+.1f}%")
            results['o2o'][task.name][str(k)] = res_k
        print(f"  Time so far: {(time.time()-t0)/60:.1f}min")
    
    # === EXP 3: Offline RL ===
    print("\n"+"="*60)
    print("EXPERIMENT 3: Offline RL")
    print("="*60)
    
    rl_configs = [('LQR-4D', 4, 2), ('Control-6D', 6, 3)]
    for name, sd, ad in rl_configs:
        print(f"\n[{name}]")
        results['rl'][name] = {}
        for beta_rl, label in [(2.0, 'LCB'), (0.0, 'NoCons')]:
            rets = []
            for seed in range(5):
                data = gen_rl_data(sd, ad, seed=seed)
                models = train_q_ens(data, sd, ad, beta=beta_rl, seed=seed)
                m, s = eval_rl(models, sd, ad, beta=beta_rl, seed=seed)
                rets.append(m)
            results['rl'][name][label] = {
                'mean': float(np.mean(rets)), 'std': float(np.std(rets)),
                'all': [float(v) for v in rets]
            }
            print(f"  {label:>8s}: return={np.mean(rets):.2f}±{np.std(rets):.2f}")
        # BC baseline
        bc_rets = []
        for seed in range(5):
            data = gen_rl_data(sd, ad, seed=seed)
            H = 50; n_ep = len(data['r'])//H
            ep_rets = [np.sum(data['r'][i*H:(i+1)*H]) for i in range(min(n_ep, 30))]
            bc_rets.append(float(np.mean(ep_rets)))
        results['rl'][name]['BC'] = {'mean': float(np.mean(bc_rets)), 'std': float(np.std(bc_rets))}
        print(f"  {'BC':>8s}: return={np.mean(bc_rets):.2f}±{np.std(bc_rets):.2f}")
    
    # === EXP 4: Ablations ===
    print("\n"+"="*60)
    print("EXPERIMENT 4: Ablations")
    print("="*60)
    
    # Beta sensitivity
    print("\n--- Beta Sensitivity ---")
    results['ablation']['beta'] = {}
    for task in tasks:
        results['ablation']['beta'][task.name] = {}
        for beta in BETA_VALUES:
            p100s = [run_mbo(task, s, beta=beta)['p100'] for s in range(5)]
            results['ablation']['beta'][task.name][str(beta)] = {
                'mean': float(np.mean(p100s)), 'std': float(np.std(p100s))
            }
        vals = [f"β={b}:{results['ablation']['beta'][task.name][str(b)]['mean']:.3f}" for b in BETA_VALUES]
        print(f"  {task.name}: {', '.join(vals)}")
    
    # Ensemble size
    print("\n--- Ensemble Size ---")
    results['ablation']['K'] = {}
    for task in [tasks[0], tasks[3], tasks[5]]:
        results['ablation']['K'][task.name] = {}
        for K in [3, 5, 10]:
            p100s = []
            for seed in range(5):
                np.random.seed(seed); torch.manual_seed(seed)
                x,y = task.get_data()
                models = train_ensemble(x, y, task.dim, K=K, seed=seed)
                top_idx = np.argsort(y)[-TOP_K:]
                x_init = np.clip(np.concatenate([x[top_idx], x[top_idx]+np.random.randn(*x[top_idx].shape).astype(np.float32)*0.05]),0,1)
                x_opt = lcb_optimize(models, torch.FloatTensor(x_init), beta=DEFAULT_BETA)
                scores = task.evaluate(x_opt.numpy())
                p100s.append(float(np.sort(scores)[-TOP_K:][-1]))
            results['ablation']['K'][task.name][str(K)] = {'mean':float(np.mean(p100s)),'std':float(np.std(p100s))}
        vals = [f"K={K}:{results['ablation']['K'][task.name][str(K)]['mean']:.3f}" for K in [3,5,10]]
        print(f"  {task.name}: {', '.join(vals)}")
    
    # Online budget sweep
    print("\n--- Online Budget ---")
    results['ablation']['budget'] = {}
    bt = tasks[3]  # Rosenbrock
    for k in [10, 25, 50, 100]:
        imps = [run_o2o(bt, s, beta=DEFAULT_BETA, k=k)['imp'] for s in range(5)]
        results['ablation']['budget'][str(k)] = {'mean':float(np.mean(imps)),'std':float(np.std(imps))}
        print(f"  k={k}: improvement={np.mean(imps):+.1f}%±{np.std(imps):.1f}%")
    
    elapsed = (time.time()-t0)/60
    print(f"\n{'='*60}\nDONE. Total: {elapsed:.1f} min\n{'='*60}")
    
    with open('results.json', 'w') as f:
        json.dump(results, f, indent=2)
    print("Results saved to results.json")
    return results

if __name__ == '__main__':
    main()
