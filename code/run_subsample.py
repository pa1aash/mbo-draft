"""Score-biased-subsample control (#11): the GP fits on a 800-pt score-biased subsample
(top-20% + random fill); the ensemble normally uses ALL data. This gives the ensemble the
SAME subsample and re-runs its 3 cells, so we can check whether the GP's edge is really
that biased subsample. Writes results_camera.json['mbo_enssub']; compare its marginal to
the full-data ensemble ('mbo'). Serial.  python code/run_subsample.py [SEEDS]
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import torch
import mbo

B, SEEDS = mbo.BETA, (int(sys.argv[1]) if len(sys.argv) > 1 else 10)
RES = os.path.join(os.path.dirname(__file__), '..', 'results', 'results_camera.json')


def subsample(x, y, seed, max_train=800):                          # identical to fit_exact_gp's subsample
    np.random.seed(seed)
    if len(x) <= max_train:
        return x, y
    top = np.argsort(y)[-int(max_train * 0.2):]
    rest = np.setdiff1d(np.arange(len(x)), top)
    sel = np.concatenate([top, np.random.choice(rest, max_train - len(top), replace=False)])
    return x[sel], y[sel]


def ens_cell(task, seed, opt):
    np.random.seed(seed); torch.manual_seed(seed)
    x, y = task.data()
    xs, ys = subsample(x, y, seed)                                 # ensemble on the GP's subsample
    ms = mbo.train_ensemble(xs, ys, task.dim, seed=seed, ep=mbo.TRAIN_EP)
    x0 = mbo.init_candidates(x, y, seed)
    if opt == 'grad':
        xf = mbo.grad_opt(mbo.ens_lcb_torch(ms, B), torch.FloatTensor(x0), steps=mbo.OPT_STEPS)
    elif opt == 'perturb':
        xf = mbo.perturb_opt(mbo.ens_lcb_np(ms, B), x0)
    else:
        xf = mbo.cma_opt(mbo.ens_lcb_np(ms, B), x0)
    p100, _ = mbo.eval_designs(task, np.asarray(xf, np.float32))
    return float(p100)


if __name__ == '__main__':
    R = json.load(open(RES))
    R.setdefault('mbo_enssub', {})
    print(f"subsample-ensemble control: 7 tasks x 3 opts x {SEEDS} seeds (serial)", flush=True)
    for task in mbo.make_tasks(None):
        R['mbo_enssub'].setdefault(task.name, {})
        for opt in ('grad', 'perturb', 'cma'):
            vals = []
            for s in range(SEEDS):
                try:
                    vals.append(ens_cell(task, s, opt))
                except Exception as e:
                    print(f"  {task.name}/{opt} seed{s} FAIL: {str(e)[:60]}", flush=True)
            if vals:
                R['mbo_enssub'][task.name][f'ens:{opt}'] = {
                    'p100': {'mean': float(np.mean(vals)), 'std': float(np.std(vals)), 'all': vals}}
        json.dump(R, open(RES, 'w'), indent=1)                     # checkpoint per task
        row = R['mbo_enssub'][task.name]
        print(f"  {task.name:14} " + "  ".join(f"ens:{o}={row.get(f'ens:{o}',{}).get('p100',{}).get('mean',float('nan')):.2f}"
                                               for o in ('grad', 'perturb', 'cma')), flush=True)
    print("wrote results_camera.json['mbo_enssub']", flush=True)
