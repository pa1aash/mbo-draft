"""C2-SWING -- the bidirectional smoothness manipulation (SM1/SM2/SM3).

Pre-registered in docs/PREREGISTRATION_V3.md (section "C2-SWING"). Engine X1=on X3=on,
beta=2, K=5, 30 seeds, 7 synthetic tasks.

The C2 story so far is DIAGNOSTIC: the GP beats the ensemble at optimization even though
the ensemble fits better (0A.2), the advantage survives sigma removal (0A.1) and more
search pressure (0A.3). Mean geometry is the last explanation standing. This arm tries to
make it CAUSAL by moving the proposed axis in BOTH directions:

  SM1  smooth the net   -- constrain each member's smoothness (gradient penalty OR
                           spectral norm) toward the GP's, holding sigma formation fixed.
                           Does the gap CLOSE?
  SM2  roughen the GP   -- Matern-1/2 (nowhere-differentiable sample paths) or a short
                           fixed lengthscale. Does the GP COLLAPSE? This is the RISKED
                           direction: theory FORBIDS a rough GP staying robust.
  SM3  survives NTK     -- does SM1 still hold at w=1024, Stage 0's widest ensemble?

Every surrogate also reports, on the SAME cell that produced its score:
  - roughness: E||d mu / d x|| / std(f), the mean function's normalized gradient norm,
    measured on D and on the optimizer's OWN proposals. This is the MANIPULATION CHECK --
    if smoothing does not move it, SM1 is VOID (not confirmed, not killed).
  - c_ood: coverage_of_premise on the optimizer's own proposals (SM2's second axis).
  - inversion: whether the returned set is worse than the x0 the method already held
    (x0_inversion.py's estimand), for the gradient-collapse half of SM1.

Sharded per (task, seed) under results/swing/shards/ -- merge-safe and resumable; rerun
the same command to fill only what is missing.

  MBO_X1=1 MBO_X3=1 python smooth_swing.py --seeds 30 --jobs 30
    -> results/swing/shards/*.json  then  --merge  -> results/swing/swing_grid.json
"""
import argparse
import glob
import json
import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'results', 'swing')
SHARDS = os.path.join(OUT, 'shards')
TASKS = ['Branin-2D', 'Styblinski-5D', 'Levy-8D', 'Rosenbrock-10D',
         'Rastrigin-15D', 'Ackley-20D', 'Griewank-30D']
OPT3 = ['perturb', 'grad', 'cma']

# SM1/SM3: ensemble smoothing variants x width. 'base' is the incumbent (must reproduce
# the committed grid at w=96). Gradient-penalty lambdas are log-spaced across three
# decades so the sweep brackets both "too weak to matter" and "so strong the fit dies".
ENS_VARIANTS = [('base', dict()),
                ('gp0.01', dict(grad_pen=0.01)),
                ('gp0.1', dict(grad_pen=0.1)),
                ('gp1.0', dict(grad_pen=1.0)),
                ('sn', dict(spectral=True))]
WIDTHS = [96, 1024]                       # 96 = SM1, 1024 = SM3 (Stage 0's widest)

# SM2: the roughened GPs, against the smooth incumbents. Lengthscales marked 'fitL' are
# FROZEN at the smooth GP's fitted L (resolved per task/seed at run time) -- refitting them
# lets the MLL undo the manipulation; see PREREGISTRATION_V3.md.
GP_VARIANTS = [('botorchgp', dict()),
               ('svgp', dict()),
               ('botorchgp_m12L', dict(nu=0.5, lengthscale='fitL')),
               ('botorchgp_lsL3', dict(lengthscale='fitL/3')),
               ('svgp_m12', dict(nu=0.5))]


def _roughness(mu_fn, xs, fstd):
    """E||d mu/d x||_2 / std(f) -- the mean function's normalized gradient norm.

    Normalized by the oracle's spread on the same points so the number is comparable
    across tasks (same device as width_ablation._metrics' normRMSE). This is the
    quantity SM1 claims to move and SM2 claims to move the other way; if it does not
    move, the manipulation did not land and the arm is VOID rather than informative.
    """
    import torch
    xt = torch.FloatTensor(np.asarray(xs, np.float32)).requires_grad_(True)
    m = mu_fn(xt)
    g = torch.autograd.grad(m.sum(), xt)[0]
    return float(g.norm(dim=1).mean()) / (float(fstd) + 1e-12)


def _ens_mu(mbo, ms):
    import torch
    ym, ys = mbo.ens_scale(ms)
    return lambda xt: torch.stack([m(xt) for m in ms]).mean(0) * ys + ym


def _ens_moments(mbo, ms):
    import torch
    def f(xx):
        with torch.no_grad():
            mu, sd = mbo.ens_moments_raw(ms, torch.FloatTensor(xx))
        return mu.numpy(), sd.numpy()
    return f


def _botorch_mu(gp, ym, ys):
    return lambda xt: gp.posterior(xt.double()).mean.squeeze(-1).float() * ys + ym


def _botorch_moments(gp, ym, ys):
    import torch
    def f(xx):
        with torch.no_grad():
            p = gp.posterior(torch.DoubleTensor(np.asarray(xx, np.float64)))
            return (p.mean.squeeze(-1).numpy() * ys + ym,
                    p.variance.clamp_min(1e-12).sqrt().squeeze(-1).numpy() * ys)
    return f


def _svgp_mu(s):
    m, ym, ys = s['model'], s['ym'], s['ys']
    m.train()
    return lambda xt: m(xt).mean * ys + ym


def _svgp_moments(s):
    import torch
    m, ym, ys = s['model'], s['ym'], s['ys']
    m.train()
    def f(xx):
        with torch.no_grad():
            p = m(torch.FloatTensor(np.asarray(xx, np.float32)))
            return (p.mean.numpy() * ys + ym,
                    p.variance.clamp_min(1e-12).sqrt().numpy() * ys)
    return f


def _run_one(mbo, t, x0, f_t, f_n, seed, mu_fn, mom_fn, xref, fref_std, beta):
    """One surrogate x 3 optimizers -> {opt: {p100,p50,c_ood,inversion,rough_prop}}.

    Diagnostics are attached to the cell that produced them, never recomputed on a
    separately-fit surrogate: c_ood and rough_prop are evaluated on THIS optimizer's own
    returned proposals, which is what 'own-proposal coverage' means.
    """
    import torch
    out = {}
    x0o = t.oracle(x0)
    x0_best = float(np.max(x0o))
    for opt in OPT3:
        if opt == 'grad':
            if f_t is None:
                continue
            xf = mbo.grad_opt(f_t, torch.FloatTensor(x0), steps=mbo.OPT_STEPS)
        elif opt == 'perturb':
            if f_n is None:
                continue
            xf = mbo.perturb_opt(f_n, x0)
        else:
            if f_n is None:
                continue
            xf = mbo.cma_opt(f_n, x0, seed=seed)
        if xf is None:
            continue
        p100, p50 = mbo.eval_designs(t, xf)
        fo = t.oracle(xf)
        mu, sd = mom_fn(xf)
        rec = dict(p100=float(p100), p50=float(p50),
                   c_ood=mbo.coverage_of_premise(mu, sd, fo, beta),
                   rough_prop=_roughness(mu_fn, xf, fref_std),
                   inversion=bool(float(p100) < x0_best),
                   inv_magnitude=float(max(0.0, x0_best - float(p100))))
        out[opt] = rec
    return out


def _cell(spec):
    import importlib
    import torch
    torch.set_num_threads(1)
    os.environ['MBO_X1'] = '1'
    os.environ['MBO_X3'] = '1'
    import mbo
    importlib.reload(mbo)
    assert mbo.X1_STANDARDIZE_Y and mbo.X3_MATCHED_PROTOCOL, 'C2-SWING must run on_on'

    task, seed = spec['task'], spec['seed']
    t = mbo.make_tasks([task])[0]
    beta, K = mbo.BETA, mbo.K_ENS
    np.random.seed(seed)
    torch.manual_seed(seed)
    x, y = t.data()
    x0 = mbo.init_candidates(x, y, seed)

    # Reference points for the on-distribution roughness probe: drawn FROM D itself
    # (the P0-5 fix in coverage33.py -- uniform draws are off-distribution by
    # construction in high d and would answer a different question).
    r = np.random.RandomState(90000 + seed)
    xref = x[r.choice(len(x), min(500, len(x)), replace=False)]
    fref_std = float(np.std(t.oracle(xref)))

    # Points BETWEEN data, for the second roughness instrument: at-data gradients
    # understate spikiness because a sum of sharp bumps is locally flat AT the centres.
    ia, ib = r.choice(len(x), 500), r.choice(len(x), 500)
    tt = r.uniform(0.2, 0.8, (500, 1)).astype(np.float32)
    xseg = x[ia] * (1 - tt) + x[ib] * tt

    cells, rough_d, rough_seg = {}, {}, {}

    # ---------------- GP arms: smooth incumbents + SM2 roughened ----------------
    ym, ys = float(np.mean(y)), float(np.std(y) + 1e-8)
    # smooth fit first: its fitted lengthscale L is what the rough variants freeze.
    _gp0 = mbo.fit_botorch_gp(x, y, seed)
    _L = getattr(_gp0.covar_module, 'base_kernel', _gp0.covar_module).lengthscale
    _L = _L.detach().numpy().ravel().copy()
    for name, kw in GP_VARIANTS:
        kw = dict(kw)
        if kw.get('lengthscale') == 'fitL':
            kw['lengthscale'] = _L
        elif kw.get('lengthscale') == 'fitL/3':
            kw['lengthscale'] = _L / 3.0
        if name.startswith('botorchgp'):
            gp = _gp0 if not kw else mbo.fit_botorch_gp(x, y, seed, **kw)
            if gp is None:
                continue
            f_t = mbo.botorch_lcb_torch(gp, beta)
            f_n = (lambda ff: (lambda xx: ff(torch.FloatTensor(xx)).detach().numpy()))(f_t)
            mu_fn, mom_fn = _botorch_mu(gp, ym, ys), _botorch_moments(gp, ym, ys)
        else:
            s = mbo.fit_svgp(x, y, t.dim, seed, **kw)
            if s is None:
                continue
            f_t, f_n = mbo.svgp_lcb_torch(s, beta), mbo.svgp_lcb_np(s, beta)
            mu_fn, mom_fn = _svgp_mu(s), _svgp_moments(s)
        rough_d[name] = _roughness(mu_fn, xref, fref_std)
        rough_seg[name] = _roughness(mu_fn, xseg, fref_std)
        for opt, v in _run_one(mbo, t, x0, f_t, f_n, seed, mu_fn, mom_fn,
                               xref, fref_std, beta).items():
            cells[f'{name}:{opt}'] = v

    # ---------------- SM1/SM3: ensemble smoothing x width ----------------
    for w in WIDTHS:
        for vname, kw in ENS_VARIANTS:
            ms = mbo.train_ensemble(x, y, t.dim, seed=seed, K=K, ep=mbo.TRAIN_EP,
                                    hid=w, **kw)
            f_t, f_n = mbo.ens_lcb_torch(ms, beta), mbo.ens_lcb_np(ms, beta)
            mu_fn, mom_fn = _ens_mu(mbo, ms), _ens_moments(mbo, ms)
            key = f'ens_{vname}_w{w}'
            rough_d[key] = _roughness(mu_fn, xref, fref_std)
            rough_seg[key] = _roughness(mu_fn, xseg, fref_std)
            for opt, v in _run_one(mbo, t, x0, f_t, f_n, seed, mu_fn, mom_fn,
                                   xref, fref_std, beta).items():
                cells[f'{key}:{opt}'] = v

    return spec, dict(cells=cells, rough_d=rough_d, rough_seg=rough_seg,
                      gp_fitted_L=float(np.median(_L)),
                      x0_best=float(np.max(t.oracle(x0))))


def _shard_path(task, seed):
    return os.path.join(SHARDS, f'{task}_s{seed}.json')


def _work(spec):
    sp, res = _cell(spec)
    p = _shard_path(sp['task'], sp['seed'])
    tmp = p + '.tmp'
    with open(tmp, 'w') as f:
        json.dump(dict(spec=sp, **res), f)
    os.replace(tmp, p)                      # atomic: a shard is complete or absent
    return sp, len(res['cells'])


def merge(seeds):
    """Fold every shard into one aggregated file. MISSING stays MISSING -- a cell absent
    from a shard is simply not counted, never imputed, and n is reported per cell."""
    import mbo
    import run_all
    grid, rough, rseg = {}, {}, {}
    n_shard = 0
    for p in sorted(glob.glob(os.path.join(SHARDS, '*.json'))):
        d = json.load(open(p))
        t = d['spec']['task']
        n_shard += 1
        for c, v in d['cells'].items():
            for m, val in v.items():
                grid.setdefault(t, {}).setdefault(c, {}).setdefault(m, []).append(val)
        for k, val in d['rough_d'].items():
            rough.setdefault(t, {}).setdefault(k, []).append(val)
        for k, val in d.get('rough_seg', {}).items():
            rseg.setdefault(t, {}).setdefault(k, []).append(val)

    def agg(v):
        a = np.asarray(v, float)
        return dict(mean=float(a.mean()), std=float(a.std()), n=int(a.size),
                    all=[float(z) for z in a])

    out = dict(meta=run_all.engine_meta(seeds, mbo.BETA, mbo.K_ENS),
               arm='C2-SWING (SM1/SM2/SM3)',
               ens_variants=[v[0] for v in ENS_VARIANTS],
               gp_variants=[v[0] for v in GP_VARIANTS],
               widths=WIDTHS, n_shards=n_shard,
               mbo={t: {c: {m: agg(v) for m, v in d.items()} for c, d in cs.items()}
                    for t, cs in grid.items()},
               roughness={t: {k: agg(v) for k, v in ks.items()} for t, ks in rough.items()},
               roughness_seg={t: {k: agg(v) for k, v in ks.items()} for t, ks in rseg.items()})
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, 'swing_grid.json')
    with open(p, 'w') as f:
        json.dump(out, f, indent=2)
    print(f'merged {n_shard} shards -> {p}')
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seeds', type=int, default=30)
    ap.add_argument('--jobs', type=int, default=30)
    ap.add_argument('--tasks', default='')
    ap.add_argument('--seed-offset', type=int, default=0)
    ap.add_argument('--merge', action='store_true')
    a = ap.parse_args()
    os.makedirs(SHARDS, exist_ok=True)
    if a.merge:
        merge(a.seeds)
        return
    tasks = a.tasks.split(',') if a.tasks else TASKS
    specs = [dict(task=t, seed=s) for t in tasks
             for s in range(a.seed_offset, a.seed_offset + a.seeds)
             if not os.path.exists(_shard_path(t, s))]
    print(f'{len(specs)} shards to run ({len(tasks)*a.seeds - len(specs)} already present)',
          flush=True)
    if not specs:
        print('nothing to do')
        return
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=a.jobs) as ex:
        futs = [ex.submit(_work, sp) for sp in specs]
        for i, fu in enumerate(as_completed(futs)):
            sp, n = fu.result()
            print(f'[{i+1}/{len(specs)}] {sp["task"]:16s} seed{sp["seed"]:<3d} '
                  f'{n} cells  {time.time()-t0:.0f}s', flush=True)
    print('ALL SWING SHARDS DONE', flush=True)


if __name__ == '__main__':
    main()
