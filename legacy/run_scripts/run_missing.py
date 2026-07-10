"""Run all missing experiments: BoTorch GP, O2O extra, bootstrap, profiling."""
import json, time, warnings, numpy as np, torch, torch.nn as nn, torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from scipy import stats as sp_stats
warnings.filterwarnings('ignore')
torch.set_num_threads(4)

K_DEFAULT=5; B0=2.0; TOP=128; STEPS=120; EP=40; H=96
t0 = time.time()

class T:
    def __init__(s,name,dim,n,noise):
        s.name,s.dim,s.noise=name,dim,noise; np.random.seed(0)
        s.x=np.random.uniform(0,1,(n,dim)).astype(np.float32)
        s.y=(s.oracle(s.x)+np.random.randn(n)*noise).astype(np.float32)
    def data(s): return s.x.copy(), s.y.copy()
class Branin(T):
    def __init__(s): super().__init__('Branin-2D',2,2000,0.05)
    def oracle(s,x): x1,x2=x[:,0]*15-5,x[:,1]*15; return -(1*(x2-5.1/(4*np.pi**2)*x1**2+5/np.pi*x1-6)**2+10*(1-1/(8*np.pi))*np.cos(x1)+10)
class Styblinski(T):
    def __init__(s): super().__init__('Styblinski-5D',5,3000,0.05)
    def oracle(s,x): xs=x*10-5; return -0.5*np.sum(xs**4-16*xs**2+5*xs,1)/s.dim
class Levy(T):
    def __init__(s): super().__init__('Levy-8D',8,4000,0.05)
    def oracle(s,x): xs=x*20-10;w=1+(xs-1)/4; return -(np.sin(np.pi*w[:,0])**2+np.sum((w[:,:-1]-1)**2*(1+10*np.sin(np.pi*w[:,:-1]+1)**2),1)+(w[:,-1]-1)**2*(1+np.sin(2*np.pi*w[:,-1])**2))/s.dim
class Rosenbrock(T):
    def __init__(s): super().__init__('Rosenbrock-10D',10,5000,0.1)
    def oracle(s,x): xs=x*4-2; return -np.sum(100*(xs[:,1:]-xs[:,:-1]**2)**2+(1-xs[:,:-1])**2,1)/1000
class Rastrigin(T):
    def __init__(s): super().__init__('Rastrigin-15D',15,5000,0.1)
    def oracle(s,x): xs=x*10.24-5.12;d=xs.shape[1]; return -(10*d+np.sum(xs**2-10*np.cos(2*np.pi*xs),1))/d
class Ackley(T):
    def __init__(s): super().__init__('Ackley-20D',20,5000,0.05)
    def oracle(s,x): xs=x*10-5;d=xs.shape[1]; return -(-20*np.exp(-0.2*np.sqrt(np.sum(xs**2,1)/d))-np.exp(np.sum(np.cos(2*np.pi*xs),1)/d)+20+np.e)

class MLP(nn.Module):
    def __init__(s,d,h=H): super().__init__(); s.net=nn.Sequential(nn.Linear(d,h),nn.ReLU(),nn.Linear(h,h),nn.ReLU(),nn.Linear(h,1))
    def forward(s,x): return s.net(x).squeeze(-1)
def train_ens(x,y,d,seed=0,epochs=EP):
    xt,yt=torch.FloatTensor(x),torch.FloatTensor(y); ds=TensorDataset(xt,yt); ms=[]
    for k in range(K_DEFAULT):
        torch.manual_seed(seed*100+k); m=MLP(d); o=optim.Adam(m.parameters(),lr=3e-3,weight_decay=1e-4)
        dl=DataLoader(ds,batch_size=256,shuffle=True); m.train()
        for _ in range(epochs):
            for xb,yb in dl: loss=nn.MSELoss()(m(xb),yb); o.zero_grad(); loss.backward(); o.step()
        m.eval(); ms.append(m)
    return ms
def optimize_lcb(ms,x0,beta=B0,steps=STEPS):
    x=x0.clone().detach().requires_grad_(True); o=optim.Adam([x],lr=0.05)
    for _ in range(steps):
        o.zero_grad(); ps=torch.stack([m(x) for m in ms]); lcb=ps.mean(0)-beta*ps.std(0)
        (-lcb.mean()).backward(); o.step()
        with torch.no_grad(): x.clamp_(0,1)
    return x.detach()

with open('results_final.json') as f: R = json.load(f)
with open('results.json') as f: RO = json.load(f)

# ============= 1. BoTorch GP =============
print("=== BoTorch GP-LCB ===", flush=True)
try:
    from botorch.models import SingleTaskGP
    from botorch.fit import fit_gpytorch_mll
    from gpytorch.mlls import ExactMarginalLogLikelihood

    R['botorch_gp'] = {}
    for task in [Branin(), Styblinski(), Levy(), Rosenbrock(), Rastrigin(), Ackley()]:
        print(f"  [{task.name}]", flush=True)
        p100s = []
        times_g = []
        max_n = min(len(task.x), 1000)
        for seed in range(6):
            t1 = time.time()
            np.random.seed(seed)
            x, y = task.data()
            idx = np.random.choice(len(x), max_n, replace=False)
            x_gp = torch.tensor(x[idx], dtype=torch.float64)
            y_gp = torch.tensor(y[idx], dtype=torch.float64).unsqueeze(-1)
            try:
                gp = SingleTaskGP(x_gp, y_gp)
                mll = ExactMarginalLogLikelihood(gp.likelihood, gp)
                fit_gpytorch_mll(mll)
                gp.eval()
                cands = torch.rand(2048, task.dim, dtype=torch.float64)
                top_x = x_gp[torch.argsort(y_gp.squeeze())[-128:]]
                pert = (top_x + torch.randn_like(top_x)*0.05).clamp(0, 1)
                cands = torch.cat([cands, pert, top_x])
                for rnd in range(3):
                    with torch.no_grad():
                        post = gp.posterior(cands)
                        mu = post.mean.squeeze()
                        sig = post.variance.squeeze().sqrt()
                    lcb = mu - B0 * sig
                    best = torch.argsort(lcb)[-256:]
                    new_c = (cands[best] + torch.randn(256, task.dim, dtype=torch.float64)*0.03).clamp(0,1)
                    cands = torch.cat([cands, new_c])
                with torch.no_grad():
                    post = gp.posterior(cands)
                    mu = post.mean.squeeze()
                    sig = post.variance.squeeze().sqrt()
                lcb = mu - B0 * sig
                best128 = cands[torch.argsort(lcb)[-TOP:]].float().numpy()
                sc = task.oracle(best128)
                p100s.append(float(np.sort(sc)[-1]))
            except Exception as e:
                print(f"    seed {seed} failed: {e}", flush=True)
                p100s.append(float('nan'))
            times_g.append(time.time() - t1)
        R['botorch_gp'][task.name] = {
            'p100_m': float(np.nanmean(p100s)),
            'p100_s': float(np.nanstd(p100s)),
            'p100': p100s,
            'time_m': float(np.mean(times_g)),
        }
        print(f"    p100={np.nanmean(p100s):.4f} ({np.mean(times_g):.1f}s/seed)", flush=True)
    with open('results_final.json', 'w') as f: json.dump(R, f, indent=2)
except Exception as e:
    print(f"  BoTorch failed entirely: {e}", flush=True)
    import traceback; traceback.print_exc()

print(f"  [{(time.time()-t0)/60:.1f}min]", flush=True)

# ============= 2. O2O extra =============
print("\n=== O2O Extra ===", flush=True)
R['o2o_extra'] = {}
for task in [Levy(), Rastrigin()]:
    print(f"  [{task.name}]", flush=True)
    R['o2o_extra'][task.name] = {}
    for k in [25, 50]:
        imps, finals = [], []
        for seed in range(3):
            np.random.seed(seed); torch.manual_seed(seed)
            x, y = task.data()
            ms = train_ens(x, y, task.dim, seed=seed)
            tidx = np.argsort(y)[-TOP:]; xt = x[tidx]
            x0 = torch.FloatTensor(np.concatenate([xt, np.clip(xt+np.random.randn(*xt.shape).astype(np.float32)*0.05,0,1)]))
            xo = optimize_lcb(ms, x0)
            sc = task.oracle(xo.numpy())
            p_off = float(np.sort(sc)[-TOP:][-1])
            xd, yd = x.copy(), y.copy()
            for j in range(k):
                if j % 10 == 0:
                    ms = train_ens(xd, yd, task.dim, seed=seed+j, epochs=20)
                    cx = np.concatenate([xd[np.argsort(yd)[-TOP:]], np.clip(xd[np.argsort(yd)[-TOP:]]+np.random.randn(TOP,task.dim).astype(np.float32)*0.05,0,1)])
                    xo = optimize_lcb(ms, torch.FloatTensor(cx), steps=60)
                with torch.no_grad():
                    ps = torch.stack([m(xo) for m in ms])
                    lcb_s = (ps.mean(0) - B0*ps.std(0)).numpy()
                bi = np.argmax(lcb_s)
                xn = xo[bi].numpy()
                yn = float(task.oracle(xn.reshape(1,-1))[0])
                xd = np.concatenate([xd, xn.reshape(1,-1)])
                yd = np.concatenate([yd, [yn]])
            p_final = float(np.max(yd[-k:]))
            imp = (p_final - p_off)/abs(p_off)*100 if p_off != 0 else 0
            imps.append(imp); finals.append(p_final)
            print(f"    k={k} s{seed}: off={p_off:.3f} fin={p_final:.3f}", flush=True)
        R['o2o_extra'][task.name][str(k)] = {
            'imp_m': float(np.mean(imps)), 'imp_s': float(np.std(imps)),
            'p100_m': float(np.mean(finals)), 'p100_s': float(np.std(finals))
        }
with open('results_final.json', 'w') as f: json.dump(R, f, indent=2)
print(f"  [{(time.time()-t0)/60:.1f}min]", flush=True)

# ============= 3. Bootstrap CIs =============
print("\n=== Bootstrap CIs ===", flush=True)
tasks6 = ['Branin-2D','Styblinski-5D','Levy-8D','Rosenbrock-10D','Rastrigin-15D','Ackley-20D']
methods = ['lcb','coms','grad_ascent']
sd = {m: {t: RO['mbo'][t][m]['p100'] for t in tasks6} for m in methods}
np.random.seed(42)
n_s = len(sd['lcb']['Branin-2D'])
br = {m: [] for m in methods}
for _ in range(10000):
    bi = np.random.choice(n_s, n_s, replace=True)
    rk = {m: [] for m in methods}
    for t in tasks6:
        sc = {m: np.mean([sd[m][t][i] for i in bi]) for m in methods}
        ss = sorted(sc.items(), key=lambda x: -x[1])
        for r, (m, _) in enumerate(ss, 1):
            rk[m].append(r)
    for m in methods:
        br[m].append(np.mean(rk[m]))
R['bootstrap_ranks'] = {}
for m in methods:
    arr = np.array(br[m])
    R['bootstrap_ranks'][m] = {
        'mean': float(np.mean(arr)),
        'ci_lo': float(np.percentile(arr, 2.5)),
        'ci_hi': float(np.percentile(arr, 97.5)),
    }
    print(f"  {m}: {np.mean(arr):.2f} [{np.percentile(arr,2.5):.2f}, {np.percentile(arr,97.5):.2f}]", flush=True)

# ============= 4. Profiling =============
print("\n=== Profiling ===", flush=True)
R['profiling'] = {}
for task in [Branin(), Styblinski(), Rosenbrock(), Ackley()]:
    t1 = time.time()
    np.random.seed(0); torch.manual_seed(0)
    x, y = task.data()
    ms = train_ens(x, y, task.dim, seed=0)
    tidx = np.argsort(y)[-TOP:]; xt = x[tidx]
    x0 = torch.FloatTensor(np.concatenate([xt, np.clip(xt+np.random.randn(*xt.shape).astype(np.float32)*0.05,0,1)]))
    optimize_lcb(ms, x0)
    elapsed = time.time() - t1
    R['profiling'][task.name] = {'ens_lcb_s': round(elapsed, 1)}
    print(f"  {task.name}: {elapsed:.1f}s", flush=True)

with open('results_final.json', 'w') as f: json.dump(R, f, indent=2)
print(f"\nALL DONE in {(time.time()-t0)/60:.1f}min", flush=True)
