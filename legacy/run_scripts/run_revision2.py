"""Continue revision: O2O for remaining 5 tasks + bootstrap CIs."""
import json, time, warnings, numpy as np, torch, torch.nn as nn, torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
warnings.filterwarnings('ignore'); torch.set_num_threads(4)

K_ENS=5; BETA=2.0; TOP=128; OPT_STEPS=100; TRAIN_EP=35; HID=96; NS_O2O=4

with open('results_revision.json') as f: R=json.load(f)
def save():
    with open('results_revision.json','w') as f: json.dump(R,f,indent=2)

class Task:
    def __init__(s,name,dim,n,noise):
        s.name,s.dim,s.noise=name,dim,noise
        np.random.seed(0); s.x=np.random.uniform(0,1,(n,dim)).astype(np.float32)
        s.y=(s.oracle(s.x)+np.random.randn(n)*noise).astype(np.float32)
    def data(s): return s.x.copy(),s.y.copy()

class Levy(Task):
    def __init__(s): super().__init__('Levy-8D',8,4000,0.05)
    def oracle(s,x):
        xs=x*20-10;w=1+(xs-1)/4
        return -(np.sin(np.pi*w[:,0])**2+np.sum((w[:,:-1]-1)**2*(1+10*np.sin(np.pi*w[:,:-1]+1)**2),1)+(w[:,-1]-1)**2*(1+np.sin(2*np.pi*w[:,-1])**2))/s.dim
class Rosenbrock(Task):
    def __init__(s): super().__init__('Rosenbrock-10D',10,5000,0.1)
    def oracle(s,x): xs=x*4-2; return -np.sum(100*(xs[:,1:]-xs[:,:-1]**2)**2+(1-xs[:,:-1])**2,1)/1000
class Rastrigin(Task):
    def __init__(s): super().__init__('Rastrigin-15D',15,5000,0.1)
    def oracle(s,x): xs=x*10.24-5.12;d=15; return -(10*d+np.sum(xs**2-10*np.cos(2*np.pi*xs),1))/d
class Ackley(Task):
    def __init__(s): super().__init__('Ackley-20D',20,5000,0.05)
    def oracle(s,x): xs=x*10-5;d=20; return -(-20*np.exp(-0.2*np.sqrt(np.sum(xs**2,1)/d))-np.exp(np.sum(np.cos(2*np.pi*xs),1)/d)+20+np.e)
class Griewank(Task):
    def __init__(s): super().__init__('Griewank-30D',30,8000,0.05)
    def oracle(s,x): xs=x*1200-600;d=30; return -(np.sum(xs**2,1)/4000-np.prod(np.cos(xs/np.sqrt(np.arange(1,d+1))),1)+1)

class MLP(nn.Module):
    def __init__(s,d):
        super().__init__(); s.net=nn.Sequential(nn.Linear(d,HID),nn.ReLU(),nn.Linear(HID,HID),nn.ReLU(),nn.Linear(HID,1))
    def forward(s,x): return s.net(x).squeeze(-1)

def train_ens(x,y,d,seed=0):
    xt,yt=torch.FloatTensor(x),torch.FloatTensor(y); ds=TensorDataset(xt,yt); ms=[]
    for k in range(K_ENS):
        torch.manual_seed(seed*100+k); m=MLP(d); o=optim.Adam(m.parameters(),lr=3e-3,weight_decay=1e-4)
        dl=DataLoader(ds,batch_size=256,shuffle=True); m.train()
        for _ in range(TRAIN_EP):
            for xb,yb in dl: loss=nn.MSELoss()(m(xb),yb); o.zero_grad(); loss.backward(); o.step()
        m.eval(); ms.append(m)
    return ms

def train_coms(x,y,d,seed=0):
    xt,yt=torch.FloatTensor(x),torch.FloatTensor(y); ds=TensorDataset(xt,yt); ms=[]
    for k in range(K_ENS):
        torch.manual_seed(seed*100+k+500); m=MLP(d); o=optim.Adam(m.parameters(),lr=3e-3,weight_decay=1e-4)
        dl=DataLoader(ds,batch_size=256,shuffle=True); m.train()
        for _ in range(TRAIN_EP):
            for xb,yb in dl:
                reg=nn.MSELoss()(m(xb),yb)
                xn=xb.detach().clone().requires_grad_(True); pn=m(xn)
                g=torch.autograd.grad(pn.sum(),xn,create_graph=False)[0]
                xn=(xn+0.05*g).detach().clamp(0,1)
                cons=m(xn).mean()-m(xb).mean()
                loss=reg+cons; o.zero_grad(); loss.backward(); o.step()
        m.eval(); ms.append(m)
    return ms

def opt_grad(ms,x0,beta=BETA,steps=OPT_STEPS):
    x=x0.clone().detach().requires_grad_(True); o=optim.Adam([x],lr=0.05)
    for _ in range(steps):
        o.zero_grad(); ps=torch.stack([m(x) for m in ms])
        lcb=ps.mean(0)-beta*ps.std(0); (-lcb.mean()).backward(); o.step()
        with torch.no_grad(): x.clamp_(0,1)
    return x.detach()

def run_mbo(task,seed,beta=BETA,method='lcb'):
    np.random.seed(seed);torch.manual_seed(seed); x,y=task.data()
    ms=train_coms(x,y,task.dim,seed=seed) if method=='coms' else train_ens(x,y,task.dim,seed=seed)
    tidx=np.argsort(y)[-TOP:]; xt=x[tidx]
    xp=np.clip(xt+np.random.randn(*xt.shape).astype(np.float32)*0.05,0,1)
    x0=torch.FloatTensor(np.concatenate([xt,xp]))
    b=0.0 if method=='grad_ascent' else beta
    xo=opt_grad(ms,x0,beta=b); sc=task.oracle(xo.numpy())
    t128=np.sort(sc)[-TOP:]
    return float(t128[-1]),float(np.median(t128)),ms,x,y,xo.numpy(),sc

def run_o2o(task,seed,beta=BETA,k=50,method='lcb',div_lam=0.0,div_r=0.1):
    np.random.seed(seed);torch.manual_seed(seed)
    p100_off,p50_off,ms,xd,yd,xopt,sc=run_mbo(task,seed,beta=beta,method=method)
    x_data,y_data=xd.copy(),yd.copy(); selected=[]; cur_ms,cur_xopt=ms,xopt
    for j in range(k):
        xt=torch.FloatTensor(cur_xopt)
        with torch.no_grad():
            ps=torch.stack([m(xt) for m in cur_ms]); mu=ps.mean(0).numpy(); sig=ps.std(0).numpy()
        lcb=mu-beta*sig
        if selected and div_lam>0:
            avg_sig=np.mean(sig)
            for xj in selected:
                d2=np.sum((cur_xopt-xj)**2,axis=1); lcb-=div_lam*avg_sig*np.exp(-d2/(2*div_r**2))
        bi=np.argmax(lcb); xs=cur_xopt[bi:bi+1]; ys=task.oracle(xs).astype(np.float32)
        selected.append(xs[0].copy())
        x_data=np.concatenate([x_data,xs]); y_data=np.concatenate([y_data,ys])
        if (j+1)%10==0 or j==k-1:
            cur_ms=train_ens(x_data,y_data,task.dim,seed=seed+10000+j)
            ti=np.argsort(y_data)[-TOP:]; xtn=x_data[ti]
            xpn=np.clip(xtn+np.random.randn(*xtn.shape).astype(np.float32)*0.05,0,1)
            cur_xopt=opt_grad(cur_ms,torch.FloatTensor(np.concatenate([xtn,xpn])),beta=beta,steps=60).numpy()
    fs=task.oracle(cur_xopt); t128=np.sort(fs)[-TOP:]
    p100_on=float(t128[-1]); imp=(p100_on-p100_off)/abs(p100_off)*100 if p100_off!=0 else 0
    return {'off_p100':p100_off,'on_p100':p100_on,'imp':imp}

t0=time.time()
remaining = [Levy(),Rosenbrock(),Rastrigin(),Ackley(),Griewank()]
for task in remaining:
    if task.name in R['o2o']:
        print(f"[{task.name}] already done, skip"); continue
    print(f"\n[{task.name}]",flush=True); R['o2o'][task.name]={}
    for method,label in [('lcb','LCB'),('coms','COMs'),('grad_ascent','GradAsc')]:
        results=[]
        for seed in range(NS_O2O):
            r=run_o2o(task,seed,beta=BETA,k=50,method=method); results.append(r)
        imps=[r['imp'] for r in results]; p100s=[r['on_p100'] for r in results]
        R['o2o'][task.name][label]={'imp_m':float(np.mean(imps)),'imp_s':float(np.std(imps)),
            'p100_m':float(np.mean(p100s)),'p100_s':float(np.std(p100s)),'all':results}
        print(f"  {label:>10s}: p100={np.mean(p100s):.3f} imp={np.mean(imps):+.1f}%",flush=True)
    # Diversity
    div_res=[]
    for seed in range(NS_O2O):
        r=run_o2o(task,seed,beta=BETA,k=50,method='lcb',div_lam=0.5,div_r=0.1); div_res.append(r)
    imps=[r['imp'] for r in div_res]; p100s=[r['on_p100'] for r in div_res]
    R['o2o'][task.name]['Diversity']={'imp_m':float(np.mean(imps)),'imp_s':float(np.std(imps)),
        'p100_m':float(np.mean(p100s)),'p100_s':float(np.std(p100s)),'all':div_res}
    print(f"  {'Diversity':>10s}: p100={np.mean(p100s):.3f} imp={np.mean(imps):+.1f}%",flush=True)
    # Random
    rand_res=[]
    for seed in range(NS_O2O):
        np.random.seed(seed);torch.manual_seed(seed)
        p100_off,_,ms,xd,yd,xopt,sc=run_mbo(task,seed,beta=BETA)
        idx=np.random.choice(len(xd),50,replace=False)
        xsel=xd[idx]; ytrue=task.oracle(xsel).astype(np.float32)
        xe=np.concatenate([xd,xsel]); ye=np.concatenate([yd,ytrue])
        ms2=train_ens(xe,ye,task.dim,seed=seed+20000)
        xo2=opt_grad(ms2,torch.FloatTensor(xopt),beta=BETA,steps=60)
        sc2=task.oracle(xo2.numpy()); p100_on=float(np.sort(sc2)[-TOP:][-1])
        imp=(p100_on-p100_off)/abs(p100_off)*100 if p100_off!=0 else 0
        rand_res.append({'off_p100':p100_off,'on_p100':p100_on,'imp':imp})
    imps=[r['imp'] for r in rand_res]; p100s=[r['on_p100'] for r in rand_res]
    R['o2o'][task.name]['Random']={'imp_m':float(np.mean(imps)),'imp_s':float(np.std(imps)),
        'p100_m':float(np.mean(p100s)),'p100_s':float(np.std(p100s))}
    print(f"  {'Random':>10s}: p100={np.mean(p100s):.3f} imp={np.mean(imps):+.1f}%",flush=True)
    save(); print(f"  [{(time.time()-t0)/60:.0f}min]")

# Bootstrap CIs
print("\n=== BOOTSTRAP CIs ===")
R['bootstrap']={}
for tname in R['o2o']:
    lcb_all=R['o2o'][tname].get('LCB',{}).get('all',[])
    div_all=R['o2o'][tname].get('Diversity',{}).get('all',[])
    if lcb_all and div_all:
        lp=[r['on_p100'] for r in lcb_all]; dp=[r['on_p100'] for r in div_all]
        np.random.seed(42); diffs=[]
        for _ in range(10000):
            ls=np.random.choice(lp,len(lp),replace=True); ds=np.random.choice(dp,len(dp),replace=True)
            diffs.append(np.mean(ds)-np.mean(ls))
        ci_lo,ci_hi=np.percentile(diffs,[2.5,97.5])
        R['bootstrap'][tname]={'diff_mean':float(np.mean(diffs)),'ci_lo':float(ci_lo),'ci_hi':float(ci_hi)}
        print(f"  {tname}: Div-LCB = {np.mean(diffs):.3f} [{ci_lo:.3f}, {ci_hi:.3f}]")
save()
print(f"\nDone in {(time.time()-t0)/60:.0f}min")
