"""Run RL + ablation experiments quickly"""
import json, time, warnings
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import copy

warnings.filterwarnings('ignore')
torch.set_num_threads(4)
K=5; B0=2.0; TOP=128; STEPS=120; EP=40; H=96

with open('results.json') as f: R=json.load(f)

def save():
    with open('results.json','w') as f: json.dump(R,f,indent=2)

# === Tasks (for ablation) ===
class T:
    def __init__(s,name,dim,n,noise):
        s.name,s.dim,s.noise=name,dim,noise
        np.random.seed(0); s.x=np.random.uniform(0,1,(n,dim)).astype(np.float32)
        s.y=(s.oracle(s.x)+np.random.randn(n)*noise).astype(np.float32)
    def data(s): return s.x.copy(),s.y.copy()
class Branin(T):
    def __init__(s): super().__init__('Branin-2D',2,2000,0.05)
    def oracle(s,x): x1,x2=x[:,0]*15-5,x[:,1]*15; return -(1*(x2-5.1/(4*np.pi**2)*x1**2+5/np.pi*x1-6)**2+10*(1-1/(8*np.pi))*np.cos(x1)+10)
class Styblinski(T):
    def __init__(s): super().__init__('Styblinski-5D',5,3000,0.05)
    def oracle(s,x): xs=x*10-5; return -0.5*np.sum(xs**4-16*xs**2+5*xs,1)/s.dim
class Levy(T):
    def __init__(s): super().__init__('Levy-8D',8,4000,0.05)
    def oracle(s,x):
        xs=x*20-10;w=1+(xs-1)/4
        return -(np.sin(np.pi*w[:,0])**2+np.sum((w[:,:-1]-1)**2*(1+10*np.sin(np.pi*w[:,:-1]+1)**2),1)+(w[:,-1]-1)**2*(1+np.sin(2*np.pi*w[:,-1])**2))/s.dim
class Rosenbrock(T):
    def __init__(s): super().__init__('Rosenbrock-10D',10,5000,0.1)
    def oracle(s,x): xs=x*4-2; return -np.sum(100*(xs[:,1:]-xs[:,:-1]**2)**2+(1-xs[:,:-1])**2,1)/1000
class Rastrigin(T):
    def __init__(s): super().__init__('Rastrigin-15D',15,5000,0.1)
    def oracle(s,x): xs=x*10.24-5.12;d=xs.shape[1]; return -(10*d+np.sum(xs**2-10*np.cos(2*np.pi*xs),1))/d
class Ackley(T):
    def __init__(s): super().__init__('Ackley-20D',20,5000,0.05)
    def oracle(s,x): xs=x*10-5;d=xs.shape[1]; return -(-20*np.exp(-0.2*np.sqrt(np.sum(xs**2,1)/d))-np.exp(np.sum(np.cos(2*np.pi*xs),1)/d)+20+np.e)
class Griewank(T):
    def __init__(s): super().__init__('Griewank-30D',30,8000,0.05)
    def oracle(s,x): xs=x*1200-600;d=xs.shape[1]; return -(np.sum(xs**2,1)/4000-np.prod(np.cos(xs/np.sqrt(np.arange(1,d+1))),1)+1)

class MLP(nn.Module):
    def __init__(s,d):
        super().__init__(); s.net=nn.Sequential(nn.Linear(d,H),nn.ReLU(),nn.Linear(H,H),nn.ReLU(),nn.Linear(H,1))
    def forward(s,x): return s.net(x).squeeze(-1)

def train_ens(x,y,d,Kv=K,seed=0):
    xt,yt=torch.FloatTensor(x),torch.FloatTensor(y); ds=TensorDataset(xt,yt); ms=[]
    for k in range(Kv):
        torch.manual_seed(seed*100+k); m=MLP(d); o=optim.Adam(m.parameters(),lr=3e-3,weight_decay=1e-4)
        dl=DataLoader(ds,batch_size=256,shuffle=True); m.train()
        for _ in range(EP):
            for xb,yb in dl:
                loss=nn.MSELoss()(m(xb),yb); o.zero_grad(); loss.backward(); o.step()
        m.eval(); ms.append(m)
    return ms

def optimize(ms,x0,beta=B0):
    x=x0.clone().detach().requires_grad_(True); o=optim.Adam([x],lr=0.05)
    for _ in range(STEPS):
        o.zero_grad(); ps=torch.stack([m(x) for m in ms])
        lcb=ps.mean(0)-beta*ps.std(0); (-lcb.mean()).backward(); o.step()
        with torch.no_grad(): x.clamp_(0,1)
    return x.detach()

def run_mbo(task,seed,beta=B0):
    np.random.seed(seed);torch.manual_seed(seed); x,y=task.data()
    ms=train_ens(x,y,task.dim,seed=seed)
    tidx=np.argsort(y)[-TOP:]
    xt=x[tidx]; xp=np.clip(xt+np.random.randn(*xt.shape).astype(np.float32)*0.05,0,1)
    x0=torch.FloatTensor(np.concatenate([xt,xp]))
    xo=optimize(ms,x0,beta=beta)
    sc=task.oracle(xo.numpy()); return float(np.sort(sc)[-TOP:][-1])

t0=time.time()

# === RL ===
print("RL EXPERIMENTS")
class QN(nn.Module):
    def __init__(s,sd,ad):
        super().__init__(); s.net=nn.Sequential(nn.Linear(sd+ad,96),nn.ReLU(),nn.Linear(96,96),nn.ReLU(),nn.Linear(96,1))
    def forward(s,st,a): return s.net(torch.cat([st,a],-1)).squeeze(-1)

def gen_rl(sd,ad,n_ep=500,Hor=50,noise=0.5,seed=42):
    np.random.seed(seed); S,A,R2,NS,D=[],[],[],[],[]
    for _ in range(n_ep):
        s=np.random.randn(sd).astype(np.float32)*0.5
        for t in range(Hor):
            a=np.clip(np.random.randn(ad).astype(np.float32)*noise-0.1*s[:ad],-1,1)
            r=float(-np.sum(s**2)*0.1-np.sum(a**2)*0.01)
            ns=(0.95*s+0.3*np.random.randn(sd).astype(np.float32)+np.pad(a,(0,max(0,sd-ad)))*0.2).astype(np.float32)
            S.append(s);A.append(a);R2.append(r);NS.append(ns);D.append(t==Hor-1); s=ns
    return {k:np.array(v,dtype=np.float32) for k,v in zip(['s','a','r','ns','d'],[S,A,R2,NS,D])}

def train_q(data,sd,ad,beta=2.0,seed=0):
    st,at,rt,nst,dt=[torch.FloatTensor(data[k]) for k in ['s','a','r','ns','d']]
    ds=TensorDataset(st,at,rt,nst,dt); ms=[]
    for k in range(K):
        torch.manual_seed(seed*100+k); q=QN(sd,ad); qt=copy.deepcopy(q)
        o=optim.Adam(q.parameters(),lr=3e-4); dl=DataLoader(ds,batch_size=256,shuffle=True)
        for _ in range(20):
            for sb,ab,rb,nsb,db in dl:
                with torch.no_grad():
                    na=at[torch.randint(0,len(at),(len(sb),))]; tgt=rb+0.99*(1-db)*qt(nsb,na)
                td=nn.MSELoss()(q(sb,ab),tgt)
                ra=torch.randn_like(ab); cons=q(sb,ra).mean()-q(sb,ab).mean()
                loss=td+0.5*cons; o.zero_grad(); loss.backward(); o.step()
            with torch.no_grad():
                for p,pt in zip(q.parameters(),qt.parameters()): pt.data.mul_(0.995).add_(p.data,alpha=0.005)
        q.eval(); ms.append(q)
    return ms

def eval_q(ms,sd,ad,beta=2.0,n=25,seed=0):
    np.random.seed(seed); rets=[]
    for _ in range(n):
        s=np.random.randn(sd).astype(np.float32)*0.5; ret=0
        for t in range(50):
            st=torch.FloatTensor(s).unsqueeze(0).repeat(48,1); ac=torch.randn(48,ad).clamp(-1,1)
            with torch.no_grad():
                qp=torch.stack([m(st,ac) for m in ms]); lcb=qp.mean(0)-beta*qp.std(0)
            a=ac[lcb.argmax()].numpy(); r=float(-np.sum(s**2)*0.1-np.sum(a**2)*0.01)
            ret+=r; s=(0.95*s+0.3*np.random.randn(sd).astype(np.float32)+np.pad(a,(0,max(0,sd-ad)))*0.2).astype(np.float32)
        rets.append(ret)
    return float(np.mean(rets)),float(np.std(rets))

for name,sd,ad in [('LQR-4D',4,2),('Control-6D',6,3)]:
    print(f"[{name}]",flush=True); R['rl'][name]={}
    for beta_r,lb in [(2.0,'LCB'),(0.0,'NoCons')]:
        rets=[]
        for seed in range(5):
            data=gen_rl(sd,ad,seed=seed); ms=train_q(data,sd,ad,beta=beta_r,seed=seed)
            m,s=eval_q(ms,sd,ad,beta=beta_r,seed=seed); rets.append(m)
        R['rl'][name][lb]={'m':float(np.mean(rets)),'s':float(np.std(rets)),'all':rets}
        print(f"  {lb}: {np.mean(rets):.2f}±{np.std(rets):.2f}",flush=True)
    bc_rets=[]
    for seed in range(5):
        data=gen_rl(sd,ad,seed=seed)
        er=[np.sum(data['r'][i*50:(i+1)*50]) for i in range(min(len(data['r'])//50,25))]
        bc_rets.append(float(np.mean(er)))
    R['rl'][name]['BC']={'m':float(np.mean(bc_rets)),'s':float(np.std(bc_rets))}
    print(f"  BC: {np.mean(bc_rets):.2f}±{np.std(bc_rets):.2f}",flush=True)
save()

# === BETA ABLATION ===
print("\nBETA ABLATION")
tasks=[Branin(),Styblinski(),Levy(),Rosenbrock(),Rastrigin(),Ackley(),Griewank()]
R['abl']['beta']={}
for task in tasks:
    R['abl']['beta'][task.name]={}
    for beta in [0.0,0.5,1.0,2.0,5.0]:
        p1s=[run_mbo(task,s,beta=beta) for s in range(3)]
        R['abl']['beta'][task.name][str(beta)]={'m':float(np.mean(p1s)),'s':float(np.std(p1s))}
    vs=[f"β={b}:{R['abl']['beta'][task.name][str(b)]['m']:.2f}" for b in [0.0,0.5,1.0,2.0,5.0]]
    print(f"  {task.name}: {', '.join(vs)}",flush=True)
save()

print(f"\nDone in {(time.time()-t0)/60:.0f}min")
