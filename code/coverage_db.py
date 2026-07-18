"""Phase 6.4 -- DB premise-coverage from D (adapts coverage33.py for Design-Bench) + 6.3
oracle noise floor.

coverage33's P0-5 fix is the whole point here: the in-distribution reference set is drawn
from D (the actual dataset rows), NOT np.random.uniform -- DB designs are one-hot vertices
(discrete tasks) / normalized measurements (continuous), never uniform. Per (task, surrogate)
on the on_on engine, over seeds:
  c_in  = P(mu - f <= beta*sigma) on a reference sample from D           [premise, in-dist]
  c_ood = P(mu - f <= beta*sigma) on the optimizer's own proposals       [premise, OOD]
beta=2. Surrogate fit ONCE per (task,surr,seed); all 3 optimizers run on it.

6.3 noise floor: the RF/exact oracles are deterministic (predict is a lookup / fixed forest),
so repeated evals of the SAME design give identical scores -> oracle eval noise ~= 0. We
verify this per task (max |var| over repeated oracle calls) so the observed cross-cell effect
cannot be attributed to oracle measurement noise.

Engine is read from MBO_X1/MBO_X3 (set to 1/1 for on_on). Run under `dbm`:
  MBO_X1=1 MBO_X3=1 conda run -n dbm python code/coverage_db.py --seeds 4 --jobs 8
"""
import argparse
import json
import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'results', 'db_corners', 'coverage_db.json')
SURR = ['ens', 'botorchgp', 'svgp']
OPT = ['grad', 'perturb', 'cma']
TASKS = ['TFBind8', 'TFBind10', 'Superconductor', 'GFP', 'UTR']


def _fit_surrogate(mbo, surr, x, y, dim, seed, beta):
    """returns (moment_raw_fn(x)->(mu,sd), f_torch|None, f_np|None). Copied from coverage33."""
    import torch
    if surr == 'ens':
        ms = mbo.train_ensemble(x, y, dim, seed=seed)

        def mom(xx):
            with torch.no_grad():
                mu, sd = mbo.ens_moments_raw(ms, torch.FloatTensor(xx))
            return mu.numpy(), sd.numpy()
        return mom, mbo.ens_lcb_torch(ms, beta), mbo.ens_lcb_np(ms, beta)
    if surr == 'botorchgp':
        gp = mbo.fit_botorch_gp(x, y, seed)
        if gp is None:
            return None, None, None
        ym, ys = float(np.mean(y)), float(np.std(y) + 1e-8)

        def mom(xx):
            with torch.no_grad():
                post = gp.posterior(torch.DoubleTensor(np.asarray(xx, np.float64)))
                mu = post.mean.squeeze(-1).numpy()
                sd = post.variance.clamp_min(1e-12).sqrt().squeeze(-1).numpy()
            return mu * ys + ym, sd * ys
        f = mbo.botorch_lcb_torch(gp, beta)
        return mom, f, (lambda xx: f(torch.FloatTensor(xx)).detach().numpy())
    if surr == 'svgp':
        s = mbo.fit_svgp(x, y, dim, seed)
        if s is None:
            return None, None, None
        m, ym, ys = s['model'], s['ym'], s['ys']; m.eval()

        def mom(xx):
            with torch.no_grad():
                post = m(torch.FloatTensor(xx))
                mu = (post.mean * ys + ym).numpy()
                sd = (post.variance.clamp_min(1e-12).sqrt() * ys).numpy()
            return mu, sd
        return mom, mbo.svgp_lcb_torch(s, beta), mbo.svgp_lcb_np(s, beta)
    raise ValueError(surr)


def _cell(spec):
    import torch
    torch.set_num_threads(1)
    import mbo
    import db_tasks
    t = db_tasks.make_db_tasks([spec['task']], subsample=spec['sub'])[0]
    seed = spec['seed']
    np.random.seed(seed); torch.manual_seed(seed)
    x, y = t.data()
    x0 = mbo.init_candidates(x, y, seed)
    mom, f_torch, f_np = _fit_surrogate(mbo, spec['surr'], x, y, t.dim, seed, mbo.BETA)
    if mom is None:
        return {**spec, 'metrics': None}
    ref = x[np.random.choice(len(x), min(500, len(x)), replace=False)]   # from D (P0-5)
    mu_r, sd_r = mom(ref)
    c_in = float(mbo.coverage_of_premise(mu_r, sd_r, t.oracle(ref), mbo.BETA))
    out = {}
    for opt in OPT:
        if opt == 'grad':
            xf = None if f_torch is None else mbo.grad_opt(f_torch, torch.FloatTensor(x0), steps=mbo.OPT_STEPS)
        elif opt == 'perturb':
            xf = None if f_np is None else mbo.perturb_opt(f_np, x0)
        else:
            xf = None if f_np is None else mbo.cma_opt(f_np, x0, seed=seed)
        if xf is None:
            continue
        mu_o, sd_o = mom(xf)
        out[opt] = dict(c_in=c_in,
                        c_ood=float(mbo.coverage_of_premise(mu_o, sd_o, t.oracle(xf), mbo.BETA)))
    return {**spec, 'metrics': out}


def noise_floor(sub):
    """6.3: oracle determinism. Eval the oracle on the SAME 200 D-rows 3x; report max variance."""
    import db_tasks
    rep = {}
    for tk in TASKS:
        try:
            t = db_tasks.make_db_tasks([tk], subsample=sub)[0]
            x, _ = t.data()
            xs = x[:200]
            evals = np.stack([t.oracle(xs) for _ in range(3)])
            rep[tk] = dict(max_var_repeat=float(evals.var(0).max()),
                           score_std_over_D=float(t.oracle(x[:2000]).std()))
        except Exception as e:
            rep[tk] = dict(error=f'{type(e).__name__}: {e}')
    return rep


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seeds', type=int, default=4)
    ap.add_argument('--jobs', type=int, default=8)
    ap.add_argument('--sub', type=int, default=8000)
    ap.add_argument('--out', default=OUT)
    a = ap.parse_args()
    import mbo, run_all
    print(f'engine X1={mbo.X1_STANDARDIZE_Y} X3={mbo.X3_MATCHED_PROTOCOL}', flush=True)
    specs = [{'task': tk, 'surr': s, 'seed': sd, 'sub': a.sub}
             for tk in TASKS for s in SURR for sd in range(a.seeds)]
    R = {}
    t0 = time.time()
    print(f'{len(specs)} fits, {a.jobs} workers', flush=True)
    with ProcessPoolExecutor(max_workers=a.jobs) as ex:
        futs = {ex.submit(_cell, s): s for s in specs}
        for fut in as_completed(futs):
            try:
                r = fut.result()
            except Exception as e:
                s = futs[fut]
                print(f"  CELL FAILED {s['task']}/{s['surr']} seed{s['seed']}: {type(e).__name__}: {e}", flush=True)
                continue
            if not r['metrics']:
                continue
            for opt, mv in r['metrics'].items():
                key = f"{r['task']}|{r['surr']}:{opt}"
                R.setdefault(key, {'c_in': [], 'c_ood': []})
                R[key]['c_in'].append(mv['c_in']); R[key]['c_ood'].append(mv['c_ood'])
    per_cell = {k: dict(c_in=float(np.mean(v['c_in'])), c_ood=float(np.mean(v['c_ood'])),
                        n=len(v['c_in'])) for k, v in R.items()}
    # per (task, surrogate): c_in (same across opt) + c_ood averaged over optimizers
    per_ts = {}
    for tk in TASKS:
        for s in SURR:
            cins = [per_cell[f'{tk}|{s}:{o}']['c_in'] for o in OPT if f'{tk}|{s}:{o}' in per_cell]
            coods = [per_cell[f'{tk}|{s}:{o}']['c_ood'] for o in OPT if f'{tk}|{s}:{o}' in per_cell]
            if cins:
                per_ts[f'{tk}|{s}'] = dict(c_in=float(np.mean(cins)), c_ood=float(np.mean(coods)))
    result = dict(meta=run_all.engine_meta(a.seeds, mbo.BETA, mbo.K_ENS),
                  per_cell=per_cell, per_task_surrogate=per_ts,
                  noise_floor=noise_floor(a.sub))
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    json.dump(result, open(a.out, 'w'), indent=1)
    print(f'done in {(time.time()-t0)/60:.1f} min -> {a.out}', flush=True)
    print(f'\n{"task|surr":26}{"c_in":>8}{"c_ood":>8}')
    for k, v in per_ts.items():
        print(f'{k:26}{v["c_in"]:8.3f}{v["c_ood"]:8.3f}')
    print('\nnoise floor (max var over 3 repeat oracle evals):')
    for tk, v in result['noise_floor'].items():
        print(f'  {tk:16} {v}')


if __name__ == '__main__':
    main()
