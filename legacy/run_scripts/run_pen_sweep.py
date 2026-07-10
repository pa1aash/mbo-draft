"""Run the penalization sensitivity sweep for O2O on Styblinski-5D (k=50).
This backs Table 6 in the paper: 9 configs of (lambda, r)."""
import json, time, warnings
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
warnings.filterwarnings('ignore')
torch.set_num_threads(4)

K=5; B0=2.0; TOP=128; STEPS=120; EP=40; H=96; NS=4  # 4 seeds as stated in paper

class MLP(nn.Module):
    def __init__(s,d):
        super().__init__(); s.net=nn.Sequential(nn.Linear(d,H),nn.ReLU(),nn.Linear(H,H),nn.ReLU(),nn.Linear(H,1))
    def forward(s,x): return s.net(x).squeeze(-1)

def train_ens(x,y,d,seed=0):
    xt,yt=torch.FloatTensor(x),torch.FloatTensor(y); ds=TensorDataset(xt,yt); ms=[]
    for k in range(K):
        torch.manual_seed(seed*100+k); m=MLP(d); o=optim.Adam(m.parameters(),lr=3e-3,weight_decay=1e-4)
        dl=DataLoader(ds,batch_size=256,shuffle=True); m.train()
        for _ in range(EP):
            for xb,yb in dl: loss=nn.MSELoss()(m(xb),yb); o.zero_grad(); loss.backward(); o.step()
        m.eval(); ms.append(m)
    return ms

def optimize(ms,x0,beta=B0,steps=STEPS):
    x=x0.clone().detach().requires_grad_(True); o=optim.Adam([x],lr=0.05)
    for _ in range(steps):
        o.zero_grad(); ps=torch.stack([m(x) for m in ms])
        lcb=ps.mean(0)-beta*ps.std(0); (-lcb.mean()).backward(); o.step()
        with torch.no_grad(): x.clamp_(0,1)
    return x.detach()

# Styblinski-5D oracle
def oracle(x):
    xs = x * 10 - 5
    return -0.5 * np.sum(xs**4 - 16*xs**2 + 5*xs, axis=1) / 5

# Generate task data
np.random.seed(0)
xd = np.random.uniform(0, 1, (3000, 5)).astype(np.float32)
yd = (oracle(xd) + np.random.randn(3000)*0.05).astype(np.float32)

def run_offline(seed):
    """Run offline MBO phase, return models, optimized designs, etc."""
    np.random.seed(seed); torch.manual_seed(seed)
    ms = train_ens(xd, yd, 5, seed=seed)
    tidx = np.argsort(yd)[-TOP:]
    xt = xd[tidx]; xp = np.clip(xt + np.random.randn(*xt.shape).astype(np.float32)*0.05, 0, 1)
    x0 = torch.FloatTensor(np.concatenate([xt, xp]))
    xopt = optimize(ms, x0, beta=B0)
    sc = oracle(xopt.numpy())
    off_p100 = float(np.sort(sc)[-TOP:][-1])
    return ms, xopt.numpy(), sc, off_p100

def run_o2o_diversity(seed, lam, radius, k=50):
    """O2O with local penalization diversity selection."""
    np.random.seed(seed); torch.manual_seed(seed)
    ms, xopt, sc, off_p100 = run_offline(seed)
    
    # Copy data for expansion
    x_data = xd.copy()
    y_data = yd.copy()
    selected = []
    
    # Iteratively select k candidates with diversity penalty
    current_models = ms
    current_xopt = xopt
    current_sc = sc
    
    for j in range(k):
        # Compute LCB scores for all candidates
        xt = torch.FloatTensor(current_xopt)
        with torch.no_grad():
            ps = torch.stack([m(xt) for m in current_models])
            mu = ps.mean(0).numpy()
            sigma = ps.std(0).numpy()
        lcb = mu - B0 * sigma
        
        # Apply diversity penalty for previously selected points
        if len(selected) > 0 and lam > 0:
            avg_sigma = np.mean(sigma)
            for xj in selected:
                dists = np.sum((current_xopt - xj)**2, axis=1)
                penalty = lam * avg_sigma * np.exp(-dists / (2 * radius**2))
                lcb = lcb - penalty
        
        # Select best under penalized LCB
        best_idx = np.argmax(lcb)
        x_sel = current_xopt[best_idx:best_idx+1]
        y_true = oracle(x_sel).astype(np.float32)
        selected.append(x_sel[0].copy())
        
        # Expand dataset
        x_data = np.concatenate([x_data, x_sel])
        y_data = np.concatenate([y_data, y_true])
        
        # Retrain every 10 steps (for efficiency)
        if (j + 1) % 10 == 0 or j == k - 1:
            current_models = train_ens(x_data, y_data, 5, seed=seed+10000+j)
            # Re-optimize
            tidx = np.argsort(y_data)[-TOP:]
            xt_new = x_data[tidx]
            xp_new = np.clip(xt_new + np.random.randn(*xt_new.shape).astype(np.float32)*0.05, 0, 1)
            x0_new = torch.FloatTensor(np.concatenate([xt_new, xp_new]))
            current_xopt = optimize(current_models, x0_new, beta=B0, steps=60).numpy()
            current_sc = oracle(current_xopt)
    
    # Final evaluation
    final_sc = oracle(current_xopt)
    final_p100 = float(np.sort(final_sc)[-TOP:][-1])
    return off_p100, final_p100

def run_o2o_greedy(seed, k=50):
    """Greedy O2O (lambda=0)."""
    return run_o2o_diversity(seed, lam=0.0, radius=0.1, k=k)

t0 = time.time()
print("=== PENALIZATION SENSITIVITY SWEEP ===")
print("Task: Styblinski-5D, k=50, 4 seeds")

configs = [
    (0.0, 0.1, "greedy"),     # greedy baseline
    (0.1, 0.05, "l0.1_r0.05"),
    (0.1, 0.1,  "l0.1_r0.1"),
    (0.1, 0.2,  "l0.1_r0.2"),
    (0.5, 0.05, "l0.5_r0.05"),
    (0.5, 0.1,  "l0.5_r0.1"),
    (0.5, 0.2,  "l0.5_r0.2"),
    (1.0, 0.1,  "l1.0_r0.1"),
    (1.0, 0.2,  "l1.0_r0.2"),
]

pen_results = {}
for lam, radius, label in configs:
    p100s = []
    for seed in range(NS):
        _, final_p100 = run_o2o_diversity(seed, lam=lam, radius=radius, k=50)
        p100s.append(final_p100)
    pen_results[label] = {
        'lambda': lam, 'radius': radius,
        'p100_mean': float(np.mean(p100s)), 'p100_std': float(np.std(p100s)),
        'p100_all': [float(v) for v in p100s]
    }
    print(f"  lam={lam:.1f} r={radius:.2f} ({label:>12s}): p100={np.mean(p100s):.3f} +/- {np.std(p100s):.3f}", flush=True)

# Save to results_final.json (merge)
try:
    with open('results_final.json') as f: rf = json.load(f)
except: rf = {}
rf['pen_sensitivity'] = pen_results
with open('results_final.json', 'w') as f: json.dump(rf, f, indent=2)

elapsed = (time.time() - t0) / 60
print(f"\nDone in {elapsed:.1f} min")
print("Saved to results_final.json")
