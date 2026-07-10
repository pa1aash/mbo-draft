"""Run remaining new experiments: K ablation, beta counter, calibration, diversity O2O"""
import json, time, warnings, sys
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.neighbors import NearestNeighbors
from scipy import stats as sp_stats
import copy

warnings.filterwarnings('ignore')
torch.set_num_threads(4)

K_DEFAULT=5; B0=2.0; TOP=128; STEPS=120; EP=40; H=96

# Tasks
class T:
    def __init__(s,name,dim,n,noise):
        s.name,s.dim,s.noise=name,dim,noise; np.random.seed(0)
        s.x=np.random.uniform(0,1,(n,dim)).astype(np.float32)
        s.y=(s.oracle(s.x)+np.random.randn(n)*noise).astype(np.float32)
    def oracle(s,x): raise NotImplementedError
    def data(s): return s.x.copy(),s.y.copy()

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
    def __init__(s,d,h=H):
        super().__init__(); s.net=nn.Sequential(nn.Linear(d,h),nn.ReLU(),nn.Linear(h,h),nn.ReLU(),nn.Linear(h,1))
    def forward(s,x): return s.net(x).squeeze(-1)

def train_ens(x,y,d,Kv=K_DEFAULT,seed=0):
    xt,yt=torch.FloatTensor(x),torch.FloatTensor(y); ds=TensorDataset(xt,yt); ms=[]
    for k in range(Kv):
        torch.manual_seed(seed*100+k); m=MLP(d); o=optim.Adam(m.parameters(),lr=3e-3,weight_decay=1e-4)
        dl=DataLoader(ds,batch_size=256,shuffle=True); m.train()
        for _ in range(EP):
            for xb,yb in dl: loss=nn.MSELoss()(m(xb),yb); o.zero_grad(); loss.backward(); o.step()
        m.eval(); ms.append(m)
    return ms

def optimize(ms,x0,beta=B0,steps=STEPS):
    x=x0.clone().detach().requires_grad_(True); o=optim.Adam([x],lr=0.05)
    for _ in range(steps):
        o.zero_grad(); ps=torch.stack([m(x) for m in ms]); lcb=ps.mean(0)-beta*ps.std(0)
        (-lcb.mean()).backward(); o.step()
        with torch.no_grad(): x.clamp_(0,1)
    return x.detach()

def run_mbo(task,seed,beta=B0,Kv=K_DEFAULT):
    np.random.seed(seed); torch.manual_seed(seed); x,y=task.data()
    ms=train_ens(x,y,task.dim,Kv=Kv,seed=seed)
    tidx=np.argsort(y)[-TOP:]; xt=x[tidx]
    xp=np.clip(xt+np.random.randn(*xt.shape).astype(np.float32)*0.05,0,1)
    x0=torch.FloatTensor(np.concatenate([xt,xp])); xo=optimize(ms,x0,beta=beta)
    sc=task.oracle(xo.numpy()); return float(np.sort(sc)[-TOP:][-1]), ms, x, y

# Load existing new results
try:
    with open('results_new.json') as f: R=json.load(f)
except: R={}

t0=time.time()

# ============================================================
# EXP B: K ABLATION (3 seeds, 5 tasks)
# ============================================================
print("="*55); print("EXP B: ENSEMBLE SIZE K ABLATION"); print("="*55)
R['K_ablation']={}
for task in [Branin(),Styblinski(),Rosenbrock(),Rastrigin(),Ackley()]:
    print(f"\n[{task.name}]",flush=True)
    R['K_ablation'][task.name]={}
    for Kv in [2,3,5,10]:
        p100s=[run_mbo(task,s,beta=B0,Kv=Kv)[0] for s in range(3)]
        R['K_ablation'][task.name][str(Kv)]={'m':float(np.mean(p100s)),'s':float(np.std(p100s)),'all':p100s}
        print(f"  K={Kv}: {np.mean(p100s):.4f}±{np.std(p100s):.4f}",flush=True)
with open('results_new.json','w') as f: json.dump(R,f,indent=2)
print(f"  [{(time.time()-t0)/60:.1f}min]")

# ============================================================
# EXP C: BETA ON LEVY AND ACKLEY
# ============================================================
print("\n"+"="*55); print("EXP C: BETA ON LEVY AND ACKLEY"); print("="*55)
R['beta_counter']={}
for task in [Levy(),Ackley()]:
    print(f"\n[{task.name}]",flush=True)
    R['beta_counter'][task.name]={}
    for beta in [0.0,0.5,1.0,2.0,5.0]:
        p100s=[run_mbo(task,s,beta=beta)[0] for s in range(3)]
        R['beta_counter'][task.name][str(beta)]={'m':float(np.mean(p100s)),'s':float(np.std(p100s))}
        print(f"  beta={beta}: {np.mean(p100s):.4f}±{np.std(p100s):.4f}",flush=True)
with open('results_new.json','w') as f: json.dump(R,f,indent=2)
print(f"  [{(time.time()-t0)/60:.1f}min]")

# ============================================================
# EXP D: CALIBRATION (3 seeds, all tasks)
# ============================================================
print("\n"+"="*55); print("EXP D: CALIBRATION DIAGNOSTICS"); print("="*55)
R['calibration']={}
for task in [Branin(),Styblinski(),Levy(),Rosenbrock(),Rastrigin(),Ackley()]:
    print(f"\n[{task.name}]",flush=True)
    cals=[]
    for seed in range(3):
        np.random.seed(seed); torch.manual_seed(seed); x,y=task.data()
        ms=train_ens(x,y,task.dim,seed=seed)
        x_test=np.random.uniform(0,1,(500,task.dim)).astype(np.float32)
        y_test=task.oracle(x_test)
        with torch.no_grad():
            preds=torch.stack([m(torch.FloatTensor(x_test)) for m in ms])
            mu=preds.mean(0).numpy(); sigma=preds.std(0).numpy()
        error=np.abs(mu-y_test)
        nn_model=NearestNeighbors(n_neighbors=5); nn_model.fit(x)
        dists,_=nn_model.kneighbors(x_test); knn_d=dists.mean(1)
        r1,p1=sp_stats.spearmanr(sigma,error)
        r2,p2=sp_stats.spearmanr(sigma,knn_d)
        cals.append({'rho_sigma_error':float(r1),'p_se':float(p1),'rho_sigma_knn':float(r2),'p_sk':float(p2)})
        print(f"  seed {seed}: rho(sig,err)={r1:.3f} rho(sig,kNN)={r2:.3f}",flush=True)
    R['calibration'][task.name]={k:float(np.mean([c[k] for c in cals])) for k in cals[0]}
    R['calibration'][task.name]['per_seed']=cals
with open('results_new.json','w') as f: json.dump(R,f,indent=2)
print(f"  [{(time.time()-t0)/60:.1f}min]")

# ============================================================
# EXP E: DIVERSITY O2O (Styblinski k=50)
# ============================================================
print("\n"+"="*55); print("EXP E: DIVERSITY-AWARE O2O"); print("="*55)
R['o2o_diversity']={}
task=Styblinski()
print(f"\n[{task.name}]",flush=True)
R['o2o_diversity'][task.name]={}
k=50; imps=[]; finals=[]
for seed in range(4):
    np.random.seed(seed); torch.manual_seed(seed); x,y=task.data()
    ms=train_ens(x,y,task.dim,seed=seed)
    tidx=np.argsort(y)[-TOP:]; xt=x[tidx]
    x0=torch.FloatTensor(np.concatenate([xt,np.clip(xt+np.random.randn(*xt.shape).astype(np.float32)*0.05,0,1)]))
    xo=optimize(ms,x0,beta=B0); sc=task.oracle(xo.numpy()); p100_off=float(np.sort(sc)[-TOP:][-1])
    
    selected=[]; xd=x.copy(); yd=y.copy()
    for j in range(k):
        if j%10==0:
            ms2=train_ens(xd,yd,task.dim,seed=seed+j,ep=20)
            cands_x=np.concatenate([xd[np.argsort(yd)[-TOP:]],np.clip(xd[np.argsort(yd)[-TOP:]]+np.random.randn(TOP,task.dim).astype(np.float32)*0.05,0,1)])
            xo2=optimize(ms2,torch.FloatTensor(cands_x),beta=B0,steps=60)
        with torch.no_grad():
            ps=torch.stack([m(xo2) for m in ms2]); mu_c=ps.mean(0).numpy(); sig_c=ps.std(0).numpy()
        lcb_s=mu_c-B0*sig_c
        if selected:
            for sp in selected:
                d=np.linalg.norm(xo2.numpy()-sp,axis=1); lcb_s-=0.5*sig_c.mean()*np.exp(-d**2/(2*0.1**2))
        bi=np.argmax(lcb_s); xn=xo2[bi].numpy(); yn=float(task.oracle(xn.reshape(1,-1))[0])
        selected.append(xn.copy()); xd=np.concatenate([xd,xn.reshape(1,-1)]); yd=np.concatenate([yd,[yn]])
    
    p100_final=float(np.max(yd[-k:])); imp=(p100_final-p100_off)/abs(p100_off)*100 if p100_off!=0 else 0
    imps.append(imp); finals.append(p100_final)
    print(f"  seed {seed}: off={p100_off:.3f}, div_final={p100_final:.3f}, imp={imp:+.1f}%",flush=True)

R['o2o_diversity'][task.name]['50']={
    'imp_m':float(np.mean(imps)),'imp_s':float(np.std(imps)),
    'p100_m':float(np.mean(finals)),'p100_s':float(np.std(finals)),'imp':imps,'p100':finals
}
print(f"  DIVERSITY O2O: imp={np.mean(imps):+.1f}%±{np.std(imps):.1f}%, p100={np.mean(finals):.3f}",flush=True)

with open('results_new.json','w') as f: json.dump(R,f,indent=2)
el=(time.time()-t0)/60
print(f"\n{'='*55}\nDONE in {el:.1f}min\n{'='*55}")
