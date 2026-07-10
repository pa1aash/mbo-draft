"""
UNICORN Experiments — Streamlined for CPU execution
Saves results incrementally after each experiment block.
"""
import os, json, time, warnings, sys
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import copy

warnings.filterwarnings('ignore')
torch.set_num_threads(4)  # Optimize CPU threads

DEVICE = torch.device('cpu')
NS = 6  # seeds for MBO
K = 5   # ensemble size
BETAS = [0.0, 0.5, 1.0, 2.0, 5.0]
B0 = 2.0  # default beta
BUDGETS = [10, 25, 50]
STEPS = 120  # optimization steps
EP = 40  # training epochs
H = 96   # hidden dim
TOP = 128

def save(results, fname='results.json'):
    with open(fname, 'w') as f:
        json.dump(results, f, indent=2)

# ============== Tasks ==============
class T:
    def __init__(self, name, dim, n, noise):
        self.name, self.dim, self.noise = name, dim, noise
        np.random.seed(0)
        self.x = np.random.uniform(0,1,(n,dim)).astype(np.float32)
        self.y = (self.oracle(self.x)+np.random.randn(n)*noise).astype(np.float32)
    def oracle(self, x): raise NotImplementedError
    def data(self): return self.x.copy(), self.y.copy()

class Branin(T):
    def __init__(self): super().__init__('Branin-2D',2,2000,0.05)
    def oracle(s,x):
        x1,x2=x[:,0]*15-5,x[:,1]*15
        return -(1*(x2-5.1/(4*np.pi**2)*x1**2+5/np.pi*x1-6)**2+10*(1-1/(8*np.pi))*np.cos(x1)+10)

class Styblinski(T):
    def __init__(self): super().__init__('Styblinski-5D',5,3000,0.05)
    def oracle(s,x):
        xs=x*10-5; return -0.5*np.sum(xs**4-16*xs**2+5*xs,1)/s.dim

class Levy(T):
    def __init__(self): super().__init__('Levy-8D',8,4000,0.05)
    def oracle(s,x):
        xs=x*20-10; w=1+(xs-1)/4
        return -(np.sin(np.pi*w[:,0])**2+np.sum((w[:,:-1]-1)**2*(1+10*np.sin(np.pi*w[:,:-1]+1)**2),1)+(w[:,-1]-1)**2*(1+np.sin(2*np.pi*w[:,-1])**2))/s.dim

class Rosenbrock(T):
    def __init__(self): super().__init__('Rosenbrock-10D',10,5000,0.1)
    def oracle(s,x):
        xs=x*4-2; return -np.sum(100*(xs[:,1:]-xs[:,:-1]**2)**2+(1-xs[:,:-1])**2,1)/1000

class Rastrigin(T):
    def __init__(self): super().__init__('Rastrigin-15D',15,5000,0.1)
    def oracle(s,x):
        xs=x*10.24-5.12; d=xs.shape[1]; return -(10*d+np.sum(xs**2-10*np.cos(2*np.pi*xs),1))/d

class Ackley(T):
    def __init__(self): super().__init__('Ackley-20D',20,5000,0.05)
    def oracle(s,x):
        xs=x*10-5; d=xs.shape[1]
        return -(-20*np.exp(-0.2*np.sqrt(np.sum(xs**2,1)/d))-np.exp(np.sum(np.cos(2*np.pi*xs),1)/d)+20+np.e)

class Griewank(T):
    def __init__(self): super().__init__('Griewank-30D',30,8000,0.05)
    def oracle(s,x):
        xs=x*1200-600; d=xs.shape[1]
        return -(np.sum(xs**2,1)/4000-np.prod(np.cos(xs/np.sqrt(np.arange(1,d+1))),1)+1)

# ============== Models ==============
class MLP(nn.Module):
    def __init__(self, d):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(d,H),nn.ReLU(),nn.Linear(H,H),nn.ReLU(),nn.Linear(H,1))
    def forward(self,x): return self.net(x).squeeze(-1)

def train_ens(x,y,d,seed=0,ep=EP):
    xt,yt = torch.FloatTensor(x), torch.FloatTensor(y)
    ds = TensorDataset(xt,yt)
    ms = []
    for k in range(K):
        torch.manual_seed(seed*100+k)
        m=MLP(d); o=optim.Adam(m.parameters(),lr=3e-3,weight_decay=1e-4)
        dl=DataLoader(ds,batch_size=256,shuffle=True)
        m.train()
        for _ in range(ep):
            for xb,yb in dl:
                loss=nn.MSELoss()(m(xb),yb); o.zero_grad(); loss.backward(); o.step()
        m.eval(); ms.append(m)
    return ms

def train_coms(x,y,d,seed=0,alpha=1.0,ep=EP):
    xt,yt = torch.FloatTensor(x), torch.FloatTensor(y)
    ds = TensorDataset(xt,yt)
    ms = []
    for k in range(K):
        torch.manual_seed(seed*100+k+500)
        m=MLP(d); o=optim.Adam(m.parameters(),lr=3e-3,weight_decay=1e-4)
        dl=DataLoader(ds,batch_size=256,shuffle=True)
        m.train()
        for _ in range(ep):
            for xb,yb in dl:
                reg=nn.MSELoss()(m(xb),yb)
                xn=xb.detach().clone().requires_grad_(True)
                pn=m(xn); g=torch.autograd.grad(pn.sum(),xn,create_graph=False)[0]
                xn=(xn+0.05*g).detach().clamp(0,1)
                cons=m(xn).mean()-m(xb).mean()
                loss=reg+alpha*cons; o.zero_grad(); loss.backward(); o.step()
        m.eval(); ms.append(m)
    return ms

def optimize(ms, x0, beta=B0, steps=STEPS):
    x=x0.clone().detach().requires_grad_(True)
    o=optim.Adam([x],lr=0.05)
    for _ in range(steps):
        o.zero_grad()
        ps=torch.stack([m(x) for m in ms])
        lcb=ps.mean(0)-beta*ps.std(0)
        (-lcb.mean()).backward(); o.step()
        with torch.no_grad(): x.clamp_(0,1)
    return x.detach()

def run_mbo(task, seed, beta=B0, method='lcb'):
    np.random.seed(seed); torch.manual_seed(seed)
    x,y = task.data()
    ms = train_coms(x,y,task.dim,seed=seed) if method=='coms' else train_ens(x,y,task.dim,seed=seed)
    tidx = np.argsort(y)[-TOP:]
    xt = x[tidx]; xp = np.clip(xt+np.random.randn(*xt.shape).astype(np.float32)*0.05,0,1)
    x0 = torch.FloatTensor(np.concatenate([xt,xp]))
    b = 0.0 if method=='grad_ascent' else beta
    xo = optimize(ms, x0, beta=b)
    sc = task.oracle(xo.numpy())
    t128 = np.sort(sc)[-TOP:]
    return float(t128[-1]), float(np.median(t128)), ms, x, y, xo.numpy(), sc

def run_o2o(task, seed, beta=B0, k=50, method='lcb'):
    np.random.seed(seed); torch.manual_seed(seed)
    p100_off, p50_off, ms, xd, yd, xopt, sc = run_mbo(task, seed, beta=beta, method=method)
    # Select top-k for online eval
    tidx = np.argsort(sc)[-k:]
    xsel = xopt[tidx]; ytrue = task.oracle(xsel).astype(np.float32)
    # Expand + retrain
    xe = np.concatenate([xd,xsel]); ye = np.concatenate([yd,ytrue])
    ms2 = train_coms(xe,ye,task.dim,seed=seed+10000) if method=='coms' else train_ens(xe,ye,task.dim,seed=seed+10000)
    b = 0.0 if method=='grad_ascent' else beta
    xo2 = optimize(ms2, torch.FloatTensor(xopt), beta=b)
    sc2 = task.oracle(xo2.numpy())
    t128 = np.sort(sc2)[-TOP:]
    p100_on = float(t128[-1])
    imp = (p100_on-p100_off)/abs(p100_off)*100 if p100_off!=0 else 0
    return p100_off, p100_on, imp

def run_o2o_rand(task, seed, beta=B0, k=50):
    np.random.seed(seed); torch.manual_seed(seed)
    p100_off, _, ms, xd, yd, xopt, sc = run_mbo(task, seed, beta=beta)
    idx = np.random.choice(len(xd),k,replace=False)
    xsel = xd[idx]; ytrue = task.oracle(xsel).astype(np.float32)
    xe = np.concatenate([xd,xsel]); ye = np.concatenate([yd,ytrue])
    ms2 = train_ens(xe,ye,task.dim,seed=seed+20000)
    xo2 = optimize(ms2, torch.FloatTensor(xopt), beta=beta)
    sc2 = task.oracle(xo2.numpy())
    p100_on = float(np.sort(sc2)[-TOP:][-1])
    imp = (p100_on-p100_off)/abs(p100_off)*100 if p100_off!=0 else 0
    return p100_off, p100_on, imp

# ============== RL ==============
class QN(nn.Module):
    def __init__(s,sd,ad):
        super().__init__()
        s.net=nn.Sequential(nn.Linear(sd+ad,96),nn.ReLU(),nn.Linear(96,96),nn.ReLU(),nn.Linear(96,1))
    def forward(s,st,a): return s.net(torch.cat([st,a],-1)).squeeze(-1)

def gen_rl(sd,ad,n_ep=500,Hor=50,noise=0.5,seed=42):
    np.random.seed(seed)
    S,A,R,NS,D=[],[],[],[],[]
    for _ in range(n_ep):
        s=np.random.randn(sd).astype(np.float32)*0.5
        for t in range(Hor):
            a=np.clip(np.random.randn(ad).astype(np.float32)*noise-0.1*s[:ad],-1,1)
            r=float(-np.sum(s**2)*0.1-np.sum(a**2)*0.01)
            ns=(0.95*s+0.3*np.random.randn(sd).astype(np.float32)+np.pad(a,(0,max(0,sd-ad)))*0.2).astype(np.float32)
            S.append(s);A.append(a);R.append(r);NS.append(ns);D.append(t==Hor-1)
            s=ns
    return {k:np.array(v,dtype=np.float32) for k,v in zip(['s','a','r','ns','d'],[S,A,R,NS,D])}

def train_q(data,sd,ad,beta=2.0,seed=0):
    st,at,rt,nst,dt=[torch.FloatTensor(data[k]) for k in ['s','a','r','ns','d']]
    ds=TensorDataset(st,at,rt,nst,dt)
    ms=[]
    for k in range(K):
        torch.manual_seed(seed*100+k)
        q=QN(sd,ad); qt=copy.deepcopy(q); o=optim.Adam(q.parameters(),lr=3e-4)
        dl=DataLoader(ds,batch_size=256,shuffle=True)
        for _ in range(25):
            for sb,ab,rb,nsb,db in dl:
                with torch.no_grad():
                    na=at[torch.randint(0,len(at),(len(sb),))]
                    tgt=rb+0.99*(1-db)*qt(nsb,na)
                td=nn.MSELoss()(q(sb,ab),tgt)
                ra=torch.randn_like(ab); cons=q(sb,ra).mean()-q(sb,ab).mean()
                loss=td+0.5*cons; o.zero_grad(); loss.backward(); o.step()
            with torch.no_grad():
                for p,pt in zip(q.parameters(),qt.parameters()):
                    pt.data.mul_(0.995).add_(p.data,alpha=0.005)
        q.eval(); ms.append(q)
    return ms

def eval_q(ms,sd,ad,beta=2.0,n=30,seed=0):
    np.random.seed(seed); rets=[]
    for _ in range(n):
        s=np.random.randn(sd).astype(np.float32)*0.5; ret=0
        for t in range(50):
            st=torch.FloatTensor(s).unsqueeze(0).repeat(48,1)
            ac=torch.randn(48,ad).clamp(-1,1)
            with torch.no_grad():
                qp=torch.stack([m(st,ac) for m in ms])
                lcb=qp.mean(0)-beta*qp.std(0)
            a=ac[lcb.argmax()].numpy()
            r=float(-np.sum(s**2)*0.1-np.sum(a**2)*0.01)
            ret+=r; s=(0.95*s+0.3*np.random.randn(sd).astype(np.float32)+np.pad(a,(0,max(0,sd-ad)))*0.2).astype(np.float32)
        rets.append(ret)
    return float(np.mean(rets)),float(np.std(rets))

# ============== MAIN ==============
def main():
    t0=time.time()
    tasks=[Branin(),Styblinski(),Levy(),Rosenbrock(),Rastrigin(),Ackley(),Griewank()]
    R={'mbo':{},'o2o':{},'rl':{},'abl':{}}
    
    print("="*55); print("EXP 1: OFFLINE MBO"); print("="*55)
    for task in tasks:
        print(f"\n[{task.name}] dim={task.dim}", flush=True)
        R['mbo'][task.name]={}
        for method in ['lcb','coms','grad_ascent']:
            p100s,p50s=[],[]
            for seed in range(NS):
                p1,p5,_,_,_,_,_ = run_mbo(task,seed,beta=B0,method=method)
                p100s.append(p1); p50s.append(p5)
            R['mbo'][task.name][method]={'p100_m':float(np.mean(p100s)),'p100_s':float(np.std(p100s)),
                'p50_m':float(np.mean(p50s)),'p50_s':float(np.std(p50s)),'p100':p100s,'p50':p50s}
            print(f"  {method:>12s}: p100={np.mean(p100s):.4f}±{np.std(p100s):.4f}", flush=True)
        save(R); print(f"  [{(time.time()-t0)/60:.0f}min]")
    
    print("\n"+"="*55); print("EXP 2: OFFLINE-TO-ONLINE MBO"); print("="*55)
    for task in tasks:
        print(f"\n[{task.name}]", flush=True)
        R['o2o'][task.name]={}
        for k in BUDGETS:
            rk={}
            for method,ml in [('lcb','LCB'),('coms','COMs'),('grad_ascent','Naive')]:
                imps,p1s=[],[]
                for seed in range(NS):
                    p_off,p_on,imp = run_o2o(task,seed,beta=B0,k=k,method=method)
                    imps.append(imp); p1s.append(p_on)
                rk[ml]={'imp_m':float(np.mean(imps)),'imp_s':float(np.std(imps)),
                    'p100_m':float(np.mean(p1s)),'p100_s':float(np.std(p1s)),'imp':imps,'p100':p1s}
                print(f"  k={k:2d} {ml:>6s}: p100={np.mean(p1s):.4f} imp={np.mean(imps):+.1f}%", flush=True)
            # Random
            imps_r,p1s_r=[],[]
            for seed in range(NS):
                _,p_on,imp = run_o2o_rand(task,seed,beta=B0,k=k)
                imps_r.append(imp); p1s_r.append(p_on)
            rk['Rand']={'imp_m':float(np.mean(imps_r)),'imp_s':float(np.std(imps_r)),
                'p100_m':float(np.mean(p1s_r)),'p100_s':float(np.std(p1s_r))}
            print(f"  k={k:2d} {'Rand':>6s}: p100={np.mean(p1s_r):.4f} imp={np.mean(imps_r):+.1f}%", flush=True)
            R['o2o'][task.name][str(k)]=rk
        save(R); print(f"  [{(time.time()-t0)/60:.0f}min]")
    
    print("\n"+"="*55); print("EXP 3: OFFLINE RL"); print("="*55)
    for name,sd,ad in [('LQR-4D',4,2),('Control-6D',6,3)]:
        print(f"\n[{name}]", flush=True)
        R['rl'][name]={}
        for beta_r,lb in [(2.0,'LCB'),(0.0,'NoCons')]:
            rets=[]
            for seed in range(5):
                data=gen_rl(sd,ad,seed=seed)
                ms=train_q(data,sd,ad,beta=beta_r,seed=seed)
                m,s=eval_q(ms,sd,ad,beta=beta_r,seed=seed)
                rets.append(m)
            R['rl'][name][lb]={'m':float(np.mean(rets)),'s':float(np.std(rets)),'all':rets}
            print(f"  {lb:>8s}: {np.mean(rets):.2f}±{np.std(rets):.2f}", flush=True)
        bc_rets=[]
        for seed in range(5):
            data=gen_rl(sd,ad,seed=seed)
            er=[np.sum(data['r'][i*50:(i+1)*50]) for i in range(min(len(data['r'])//50,30))]
            bc_rets.append(float(np.mean(er)))
        R['rl'][name]['BC']={'m':float(np.mean(bc_rets)),'s':float(np.std(bc_rets))}
        print(f"  {'BC':>8s}: {np.mean(bc_rets):.2f}±{np.std(bc_rets):.2f}", flush=True)
    save(R)
    
    print("\n"+"="*55); print("EXP 4: ABLATIONS"); print("="*55)
    
    # Beta
    print("\n--- Beta ---")
    R['abl']['beta']={}
    for task in tasks:
        R['abl']['beta'][task.name]={}
        for beta in BETAS:
            p1s=[run_mbo(task,s,beta=beta)[0] for s in range(4)]
            R['abl']['beta'][task.name][str(beta)]={'m':float(np.mean(p1s)),'s':float(np.std(p1s))}
        vs=[f"β={b}:{R['abl']['beta'][task.name][str(b)]['m']:.3f}" for b in BETAS]
        print(f"  {task.name}: {', '.join(vs)}", flush=True)
    
    # K
    print("\n--- Ensemble K ---")
    R['abl']['K']={}
    for task in [tasks[0],tasks[3],tasks[5]]:
        R['abl']['K'][task.name]={}
        for Kv in [3,5,10]:
            p1s=[]
            for seed in range(4):
                np.random.seed(seed);torch.manual_seed(seed)
                x,y=task.data()
                ms=train_ens(x,y,task.dim,K=Kv,seed=seed)
                tidx=np.argsort(y)[-TOP:]
                x0=np.clip(np.concatenate([x[tidx],x[tidx]+np.random.randn(*x[tidx].shape).astype(np.float32)*0.05]),0,1)
                xo=optimize(ms,torch.FloatTensor(x0),beta=B0)
                sc=task.oracle(xo.numpy())
                p1s.append(float(np.sort(sc)[-TOP:][-1]))
            R['abl']['K'][task.name][str(Kv)]={'m':float(np.mean(p1s)),'s':float(np.std(p1s))}
        vs=[f"K={Kv}:{R['abl']['K'][task.name][str(Kv)]['m']:.3f}" for Kv in [3,5,10]]
        print(f"  {task.name}: {', '.join(vs)}", flush=True)
    
    # Budget
    print("\n--- Budget ---")
    R['abl']['budget']={}
    bt=tasks[3]
    for k in [10,25,50,100]:
        imps=[run_o2o(bt,s,beta=B0,k=k)[2] for s in range(4)]
        R['abl']['budget'][str(k)]={'m':float(np.mean(imps)),'s':float(np.std(imps))}
        print(f"  k={k}: {np.mean(imps):+.1f}%±{np.std(imps):.1f}%", flush=True)
    
    save(R)
    el=(time.time()-t0)/60
    print(f"\n{'='*55}\nDONE in {el:.0f}min\n{'='*55}")

if __name__=='__main__':
    main()
