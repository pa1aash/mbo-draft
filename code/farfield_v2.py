"""0D -- instrumented far-field functional form (FF1/FF2/FF3), per docs/PREREGISTRATION_V3.md.

0C returned NOT-COMPUTABLE: no surrogate is reconstructable from disk and no design
coordinates survive a run, so neither the ray-linearity diagnostic nor the boundary statistic
could be formed from stored artifacts. 0C named the cheap fix -- store the surrogate MEAN on a
fixed ray grid, kilobytes per cell. This module is that fix.

TWO passes per (task, seed), both on the on_on engine at beta=2, K=5:

  rays  -- fit each surrogate class once, evaluate its MEAN mu along 16 rays from the data
           centroid at 61 normalized radii s, where s=1 is exactly the box face. s>1 is
           outside the training support (the synthetic datasets are uniform(0,1)^d, so the
           support IS the box). Feeds FF1 (far segment) and FF3 (near segment).
  grid  -- the incumbent 3x3 surrogate x optimizer grid, replicating run_offline's seeding
           EXACTLY, plus the one statistic 0C could not compute: the returned optimum's
           distance to the nearest box face. Feeds FF2, and its p100 doubles as a
           reproduction check against results/kbeta/grid_b2.0.json.

code/mbo.py is NOT modified. This module imports it read-only, so the instrumentation is
default-OFF for every existing caller by construction; `git diff main -- code/mbo.py` being
empty is the check. code/farfield_selftest.py runs the incumbent path independently and
compares it to the published grid.

  MBO_X1=1 MBO_X3=1 python farfield_v2.py --seeds 30 --jobs 30
    -> results/mechanism/farfield_v2/rays_<task>.json, grid_ff2.json
"""
import argparse
import json
import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'results', 'mechanism', 'farfield_v2')
TASKS = ['Branin-2D', 'Styblinski-5D', 'Levy-8D', 'Rosenbrock-10D',
         'Rastrigin-15D', 'Ackley-20D', 'Griewank-30D']
SURR = ['ens', 'botorchgp', 'svgp']
OPT3 = ['grad', 'perturb', 'cma']

# ---- ray geometry, fixed in the pre-registration -----------------------------
N_RAYS = 16              # min(d,8) axis directions, random unit vectors to fill
N_AXIS = 8
RAY_SEED = 777           # + task index; seeded by TASK so rays pool across seeds
S_GRID = np.concatenate([np.linspace(0.0, 1.0, 21),      # inside the box, s=1 is the face
                         np.linspace(1.05, 3.0, 40)])    # outside the training support
FAR = (1.5, 3.0)         # FF1 segment (31 points)
NEAR = (0.6, 1.0)        # FF3 segment (9 points)
CONST_TOL = 0.01         # range < this many sd_y over a segment -> DEGENERATE-CONSTANT
BOUND_TOL = 0.01         # a coordinate within this of a face counts as "at the boundary"


def ray_dirs(dim, task_index):
    """16 unit directions: axis directions first, then random ones. RandomState is keyed by
    TASK, not by seed, so every seed probes the same rays and per-ray stats pool over seeds."""
    U = [np.eye(dim)[i] for i in range(min(dim, N_AXIS))]
    r = np.random.RandomState(RAY_SEED + task_index)
    while len(U) < N_RAYS:
        v = r.randn(dim)
        n = float(np.linalg.norm(v))
        if n > 1e-8:
            U.append(v / n)
    return np.asarray(U, np.float64)


def t_exit(c, u):
    """Distance from centroid c to the box face along unit direction u, so that c + t*u lands
    exactly on the boundary of [0,1]^d. s = t / t_exit makes 2-D and 30-D comparable."""
    ts = []
    for i in range(len(u)):
        if u[i] > 1e-12:
            ts.append((1.0 - c[i]) / u[i])
        elif u[i] < -1e-12:
            ts.append((0.0 - c[i]) / u[i])
    return float(min(ts))


# ---- surrogate construction: mirrors mbo.build_surrogate's RNG consumption exactly --------
def _gp_scale(x, y, seed, max_train=800):
    """(ym, ys) of fit_botorch_gp's internal target standardization. fit_botorch_gp does not
    carry them, and the far-field SLOPE has to be reported in sd_y units, so the score-biased
    subsample (mbo.py:303-330) is replicated here. Safe to call before the fit: fit_botorch_gp
    opens with np.random.seed(seed), which wipes whatever this consumed."""
    np.random.seed(seed)
    if len(x) > max_train:
        top = np.argsort(y)[-int(max_train * 0.2):]
        rest = np.setdiff1d(np.arange(len(x)), top)
        sel = np.concatenate([top, np.random.choice(rest, max_train - len(top), replace=False)])
        y = y[sel]
    yt = np.asarray(y, np.float64)
    return float(yt.mean()), float(yt.std() + 1e-8)


def build(name, x, y, dim, seed, beta, K, ep):
    """-> (mean_fn -> RAW-unit mu, f_torch, f_np). Calls the same mbo fitters in the same
    order as mbo.build_surrogate, so the RNG stream -- and therefore every downstream
    optimizer draw -- is identical to the incumbent grid."""
    import torch
    if name == 'ens':
        ms = mbo.train_ensemble(x, y, dim, seed=seed, K=K, ep=ep)

        def mean_fn(xx):
            with torch.no_grad():
                m, _ = mbo.ens_moments_raw(ms, torch.FloatTensor(np.asarray(xx, np.float32)))
            return m.numpy().astype(np.float64)
        return mean_fn, mbo.ens_lcb_torch(ms, beta), mbo.ens_lcb_np(ms, beta)

    if name == 'botorchgp':
        ym, ys = _gp_scale(x, y, seed)
        gp = mbo.fit_botorch_gp(x, y, seed)
        if gp is None:
            return None, None, None

        def mean_fn(xx):
            with torch.no_grad():
                post = gp.posterior(torch.DoubleTensor(np.asarray(xx, np.float64)))
                return post.mean.squeeze(-1).numpy() * ys + ym
        f_t = mbo.botorch_lcb_torch(gp, beta)
        return mean_fn, f_t, (lambda a: f_t(torch.FloatTensor(a)).detach().numpy())

    if name == 'svgp':
        sv = mbo.fit_svgp(x, y, dim, seed)
        if sv is None:
            return None, None, None

        def mean_fn(xx):
            sv['model'].train()          # same train-mode predict svgp_lcb_torch documents
            with torch.no_grad():
                p = sv['model'](torch.FloatTensor(np.asarray(xx, np.float32)))
                return p.mean.numpy().astype(np.float64) * sv['ys'] + sv['ym']
        return mean_fn, mbo.svgp_lcb_torch(sv, beta), mbo.svgp_lcb_np(sv, beta)

    raise ValueError(name)


# ---- pass 1: ray grid (FF1, FF3) ---------------------------------------------------------
def _rays(spec):
    import torch
    torch.set_num_threads(1)
    os.environ['MBO_X1'] = '1'
    os.environ['MBO_X3'] = '1'
    _load_mbo()
    ti = TASKS.index(spec['task'])
    t = mbo.make_tasks([spec['task']])[0]
    seed = spec['seed']
    np.random.seed(seed)
    torch.manual_seed(seed)
    x, y = t.data()
    sd_y = float(np.std(y))
    c = x.mean(axis=0).astype(np.float64)
    U = ray_dirs(t.dim, ti)
    te = np.asarray([t_exit(c, u) for u in U], np.float64)

    pts = np.concatenate([c[None, :] + (S_GRID[:, None] * te[j]) * U[j][None, :]
                          for j in range(N_RAYS)])            # (16*61, d), NOT clipped
    out = {'sd_y': sd_y, 't_exit': [float(v) for v in te], 'curves': {}}
    for name in SURR:
        np.random.seed(seed)
        torch.manual_seed(seed)
        mean_fn, _, _ = build(name, x, y, t.dim, seed, mbo.BETA, mbo.K_ENS, mbo.TRAIN_EP)
        if mean_fn is None:
            continue
        mu = mean_fn(pts).reshape(N_RAYS, len(S_GRID))
        out['curves'][name] = [[float(f'{v:.6g}') for v in row] for row in mu]
    return spec, out


# ---- pass 2: 3x3 grid + boundary distance of the returned optimum (FF2) -------------------
def _grid(spec):
    import torch
    torch.set_num_threads(1)
    os.environ['MBO_X1'] = '1'
    os.environ['MBO_X3'] = '1'
    _load_mbo()
    t = mbo.make_tasks([spec['task']])[0]
    seed, beta, K = spec['seed'], mbo.BETA, mbo.K_ENS
    cells = {}
    for name in SURR:
        for opt in OPT3:
            # replicate mbo.run_offline's seeding EXACTLY (mbo.py:528-538) so p100 is
            # bit-comparable to results/kbeta/grid_b2.0.json
            np.random.seed(seed)
            torch.manual_seed(seed)
            x, y = t.data()
            x0 = mbo.init_candidates(x, y, seed)
            mean_fn, f_t, f_n = build(name, x, y, t.dim, seed, beta, K, mbo.TRAIN_EP)
            if mean_fn is None:
                continue
            if opt == 'grad':
                if f_t is None:
                    continue
                xf = mbo.grad_opt(f_t, torch.FloatTensor(x0), steps=mbo.OPT_STEPS)
            elif opt == 'perturb':
                xf = mbo.perturb_opt(f_n, x0)
            else:
                xf = mbo.cma_opt(f_n, x0, seed=seed)
            if xf is None:
                continue
            xf = np.asarray(xf, np.float32)
            p100, p50 = mbo.eval_designs(t, xf)
            mu = mean_fn(xf)
            xs = np.asarray(xf[int(np.argmax(mu))], np.float64)     # x* = argmax of the MEAN
            face = np.minimum(xs, 1.0 - xs)                          # per-dim distance to a face
            cells[f'{name}:{opt}'] = dict(
                p100=float(p100), p50=float(p50),
                d_bnd=float(face.min()),
                frac_at_bound=float(np.mean(face < BOUND_TOL)),
                mu_star=float(mu.max()))
    return spec, cells


_MBO_READY = False


def _load_mbo():
    global mbo, _MBO_READY
    import importlib
    import mbo as _m
    if not _MBO_READY:
        importlib.reload(_m)
        _MBO_READY = True
    mbo = _m
    assert mbo.X1_STANDARDIZE_Y and mbo.X3_MATCHED_PROTOCOL, '0D must run on_on'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seeds', type=int, default=30)
    ap.add_argument('--jobs', type=int, default=30)
    ap.add_argument('--tasks', default='')
    ap.add_argument('--pass', dest='which', default='both', choices=['rays', 'grid', 'both'])
    a = ap.parse_args()
    tasks = a.tasks.split(',') if a.tasks else TASKS
    os.makedirs(OUT, exist_ok=True)
    _load_mbo()
    import run_all
    meta = run_all.engine_meta(a.seeds, mbo.BETA, mbo.K_ENS)
    meta_cfg = dict(n_rays=N_RAYS, n_axis=N_AXIS, ray_seed=RAY_SEED,
                    s_grid=[float(v) for v in S_GRID], far=list(FAR), near=list(NEAR),
                    const_tol=CONST_TOL, bound_tol=BOUND_TOL, surr=SURR, opt=OPT3)
    t0 = time.time()

    if a.which in ('rays', 'both'):
        specs = [dict(task=t, seed=s) for t in tasks for s in range(a.seeds)]
        buf = {}
        print(f'rays: {len(specs)} (task,seed) cells, {a.jobs} workers', flush=True)
        with ProcessPoolExecutor(max_workers=a.jobs) as ex:
            for i, fu in enumerate(as_completed([ex.submit(_rays, s) for s in specs])):
                sp, r = fu.result()
                buf.setdefault(sp['task'], {})[str(sp['seed'])] = r
                if (i + 1) % 25 == 0:
                    print(f'  rays {i+1}/{len(specs)} [{(time.time()-t0)/60:.1f}m]', flush=True)
        for tk, per_seed in buf.items():
            dim = mbo.make_tasks([tk])[0].dim
            U = ray_dirs(dim, TASKS.index(tk))
            p = os.path.join(OUT, f'rays_{tk}.json')
            json.dump({'meta': meta, 'config': meta_cfg, 'task': tk, 'dim': int(dim),
                       'dirs': [[float(f'{v:.10g}') for v in u] for u in U],
                       'seeds': per_seed}, open(p, 'w'))
            print('wrote', p, flush=True)

    if a.which in ('grid', 'both'):
        specs = [dict(task=t, seed=s) for t in tasks for s in range(a.seeds)]
        g = {}
        print(f'grid: {len(specs)} (task,seed) cells x 9, {a.jobs} workers', flush=True)
        with ProcessPoolExecutor(max_workers=a.jobs) as ex:
            for i, fu in enumerate(as_completed([ex.submit(_grid, s) for s in specs])):
                sp, cells = fu.result()
                for ck, cv in cells.items():
                    node = g.setdefault(sp['task'], {}).setdefault(ck, {})
                    for m, v in cv.items():
                        node.setdefault(m, {})[str(sp['seed'])] = v
                if (i + 1) % 25 == 0:
                    print(f'  grid {i+1}/{len(specs)} [{(time.time()-t0)/60:.1f}m]', flush=True)
        p = os.path.join(OUT, 'grid_ff2.json')
        json.dump({'meta': meta, 'config': meta_cfg, 'grid': g}, open(p, 'w'), indent=1)
        print('wrote', p, flush=True)

    print(f'FARFIELD_V2_DONE [{(time.time()-t0)/60:.1f}m]', flush=True)


if __name__ == '__main__':
    main()
