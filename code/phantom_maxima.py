"""0B -- positive-mechanism arm for C2 (PM1/PM2/PM3), per docs/PREREGISTRATION_V3.md.

Six controls have eliminated sigma, width, budget, held-out accuracy, mean smoothness and
premise coverage as explanations of the GP-ensemble gap. What survives is a diagnosis: what
differs is WHICH off-distribution maximizers a surrogate's mean admits. This arm instruments
the grid to measure that directly, and adds five GP variants that try to remove the GP's
prior-mean reversion so the diagnosis can be turned into a causal claim -- or not.

Per (task, seed) every surrogate is fit ONCE and handed to all three optimizers (the
width-ablation protocol). For every one of the 128 returned designs we record the surrogate's
MEAN (not the LCB it ascended), its std, the noiseless oracle value, and the design's 10-NN
distance to the full offline dataset D. The returned optimum x* of a cell is the design with
the largest mean.

The five GP variants and the 2x2 they form are documented in the pre-registration. Four of
them are built by copying the incumbent GP's fitted state_dict and overwriting the prior-mean
constant and/or the lengthscale, so they cost no extra marginal-likelihood fit and differ from
the incumbent in exactly one or two named quantities.

  MBO_X1=1 MBO_X3=1 python phantom_maxima.py --seeds 30 --jobs 24
    -> results/mechanism/phantom_maxima.json
"""
import argparse
import json
import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'results', 'mechanism')
TASKS = ['Branin-2D', 'Styblinski-5D', 'Levy-8D', 'Rosenbrock-10D',
         'Rastrigin-15D', 'Ackley-20D', 'Griewank-30D']
OPT3 = ['perturb', 'grad', 'cma']
KNN = 10                 # k for the distance-to-D statistic
N_FAR = 512              # uniform points for the far-field (MC-1) probe
LS_FRAC = 0.1            # short-lengthscale arms: 0.1x the incumbent's fitted lengthscale
C_SUP = 20.0             # "strictly above every observation": z_max + 20 standardized units

# GP arms: (name, constant_mode, lengthscale_mode, refit). See PREREGISTRATION_V3 0B.
#   constant: None = fitted by MLL, 'zmax' / 'zmax+sup' = frozen at that value
#   refit=True  -> constant frozen BEFORE the MLL fit, kernel refit around it
#   refit=False -> incumbent fit copied, then the named quantities overwritten
GP_ARMS = [
    ('botorchgp', None,       1.0,      False),   # incumbent                       (2x2)
    ('gpm_ph',    'zmax+sup', 1.0,      False),   # reversion knob alone            (2x2)
    ('gpm_ls',    None,       LS_FRAC,  False),   # lengthscale alone               (2x2)
    ('gpm_lssup', 'zmax+sup', LS_FRAC,  False),   # genuinely reversion-removed     (2x2)
    ('gpm_max',   'zmax',     None,     True),    # PM2 as briefed, dose 1
    ('gpm_sup',   'zmax+sup', None,     True),    # PM2 as briefed, dose 2 (primary)
]


# ------------------------------------------------------------------ GP plumbing
def _gp_subsample(x, y, seed, max_train=800):
    """The score-biased subsample fit_botorch_gp uses (mbo.py:303-330), replicated so the
    variants see byte-identical training data and the manipulation is the only difference."""
    np.random.seed(seed)
    if len(x) <= max_train:
        return x, y
    top = np.argsort(y)[-int(max_train * 0.2):]
    rest = np.setdiff1d(np.arange(len(x)), top)
    sel = np.concatenate([top, np.random.choice(rest, max_train - len(top), replace=False)])
    return x[sel], y[sel]


def build_gp_arms(x, y, seed):
    """-> {name: dict(gp=, ym=, ys=, c_std=, ls_med=)}. c_std is the arm's prior-mean
    constant in the GP's standardized target units, or None where the MLL chose it."""
    import torch
    from botorch.models import SingleTaskGP
    from botorch.fit import fit_gpytorch_mll
    from gpytorch.mlls import ExactMarginalLogLikelihood

    xs, ys_ = _gp_subsample(x, y, seed)
    torch.manual_seed(seed)
    xt = torch.DoubleTensor(np.asarray(xs, np.float64))
    yt = torch.DoubleTensor(np.asarray(ys_, np.float64)).unsqueeze(-1)
    ym, ysd = float(yt.mean()), float(yt.std() + 1e-8)
    yt = (yt - ym) / ysd
    zmax = float(yt.max())

    def _new():
        return SingleTaskGP(xt, yt)

    def _fit(m):
        fit_gpytorch_mll(ExactMarginalLogLikelihood(m.likelihood, m))
        return m

    base = _fit(_new())
    base.eval()
    ls0 = base.covar_module.lengthscale.detach().clone()

    out = {}
    for name, cmode, lsmode, refit in GP_ARMS:
        c = {None: None, 'zmax': zmax, 'zmax+sup': zmax + C_SUP}[cmode]
        if refit:
            m = _new()
            if c is not None:
                with torch.no_grad():
                    m.mean_module.constant.fill_(c)
                m.mean_module.raw_constant.requires_grad_(False)
            _fit(m)
        else:
            m = _new()
            m.load_state_dict(base.state_dict())
            with torch.no_grad():
                if lsmode is not None and lsmode != 1.0:
                    m.covar_module.lengthscale = ls0 * lsmode
                if c is not None:
                    m.mean_module.constant.fill_(c)
        m.eval()
        out[name] = dict(gp=m, ym=ym, ys=ysd,
                         c_std=(None if c is None else float(c)),
                         c_fitted=float(m.mean_module.constant),
                         ls_med=float(m.covar_module.lengthscale.detach().median()))
    return out


def gp_moments(arm):
    """Raw-unit (mu, sd) for a GP arm. botorch_lcb_torch stays in standardized space --
    fine for ranking, useless for inflation -- so the affine inverse is applied here."""
    import torch

    def f(xx):
        with torch.no_grad():
            post = arm['gp'].posterior(torch.DoubleTensor(np.asarray(xx, np.float64)))
            mu = post.mean.squeeze(-1).numpy() * arm['ys'] + arm['ym']
            sd = post.variance.clamp_min(1e-12).sqrt().squeeze(-1).numpy() * arm['ys']
        return mu, sd
    return f


def gp_lcb(arm, beta):
    """LCB closures on the arm. Standardized space: monotone in the raw-unit LCB, so the
    optimizer's argmax is identical and the incumbent arm reproduces the grid exactly."""
    import torch

    def f_t(xx):
        post = arm['gp'].posterior(xx.double())
        return (post.mean - beta * post.variance.clamp_min(1e-12).sqrt()).squeeze(-1).float()

    def f_n(xx):
        with torch.no_grad():
            return f_t(torch.FloatTensor(xx)).numpy()
    return f_t, f_n


# ------------------------------------------------------------------ statistics
def _pcts(a):
    a = np.asarray(a, float)
    return dict(mean=float(a.mean()), sd=float(a.std()),
                p10=float(np.percentile(a, 10)), p50=float(np.percentile(a, 50)),
                p90=float(np.percentile(a, 90)))


def _cell_record(mu, sd, f, dhat, sd_y, ym_D, lcb):
    """Everything PM1/PM3 need from one cell's 128 returned designs.
    x*   = argmax of the surrogate MEAN (the pre-registered returned optimum)
    x*L  = argmax of the LCB (the point the pipeline acts on) -- robustness read only."""
    infl = (mu - f) / sd_y
    z = (f - ym_D) / sd_y
    i_m, i_l = int(np.argmax(mu)), int(np.argmax(lcb))
    return dict(
        star=dict(dhat=float(dhat[i_m]), z=float(z[i_m]), infl=float(infl[i_m]),
                  mu=float(mu[i_m]), sd=float(sd[i_m]), f=float(f[i_m])),
        star_lcb=dict(dhat=float(dhat[i_l]), z=float(z[i_l]), infl=float(infl[i_l])),
        allprop=dict(dhat_mean=float(dhat.mean()), dhat_p90=float(np.percentile(dhat, 90)),
                     z_mean=float(z.mean()), z_p90=float(np.percentile(z, 90)),
                     infl_mean=float(infl.mean()), infl_p90=float(np.percentile(infl, 90))))


# ------------------------------------------------------------------ one (task, seed)
def _cell(spec):
    import torch
    from scipy.spatial import cKDTree
    torch.set_num_threads(1)
    os.environ['MBO_X1'] = '1'
    os.environ['MBO_X3'] = '1'
    import importlib
    import mbo
    importlib.reload(mbo)
    assert mbo.X1_STANDARDIZE_Y and mbo.X3_MATCHED_PROTOCOL, '0B must run on_on'

    t = mbo.make_tasks([spec['task']])[0]
    seed, beta, K = spec['seed'], mbo.BETA, mbo.K_ENS
    np.random.seed(seed)
    torch.manual_seed(seed)
    x, y = t.data()
    x0 = mbo.init_candidates(x, y, seed)

    # ---- distance-to-support scale. rho_tau = median over D of a dataset point's own
    # mean 10-NN distance, so Dhat is dimensionless and 2-D pools with 30-D.
    tree = cKDTree(x)
    dd, _ = tree.query(x, k=KNN + 1)              # col 0 is the point itself
    rho = float(np.median(dd[:, 1:].mean(axis=1)))
    sd_y, ym_D = float(np.std(y)), float(np.mean(y))

    def dhat_of(xx):
        d, _ = tree.query(np.asarray(xx, np.float64), k=KNN)
        return d.mean(axis=1) / rho

    res = {'cells': {}, 'heldout': {}, 'farfield': {}, 'gpinfo': {},
           'consts': dict(rho=rho, sd_y=sd_y, ym_D=ym_D, n_D=int(len(x)), dim=int(t.dim))}

    def record(name, moments, f_t, f_n):
        for opt in OPT3:
            if opt == 'grad':
                if f_t is None:
                    continue
                xf = mbo.grad_opt(f_t, torch.FloatTensor(x0), steps=mbo.OPT_STEPS)
            elif opt == 'perturb':
                xf = mbo.perturb_opt(f_n, x0)
            else:
                xf = mbo.cma_opt(f_n, x0, seed=seed)
            if xf is None:
                continue                                   # dependency missing -> MISSING
            xf = np.asarray(xf, np.float32)
            p100, p50 = mbo.eval_designs(t, xf)
            mu, sd = moments(xf)
            rec = _cell_record(mu, sd, t.oracle(xf), dhat_of(xf), sd_y, ym_D, f_n(xf))
            rec['p100'], rec['p50'] = float(p100), float(p50)
            res['cells'][f'{name}:{opt}'] = rec

    # ---- ensemble ----
    ms = mbo.train_ensemble(x, y, t.dim, seed=seed, K=K, ep=mbo.TRAIN_EP)

    def ens_mom(xx):
        with torch.no_grad():
            m, s = mbo.ens_moments_raw(ms, torch.FloatTensor(np.asarray(xx, np.float32)))
        return m.numpy(), s.numpy()
    record('ens', ens_mom, mbo.ens_lcb_torch(ms, beta), mbo.ens_lcb_np(ms, beta))

    # ---- svgp (reported, not manipulated) ----
    sv = mbo.fit_svgp(x, y, t.dim, seed)
    if sv is not None:
        def sv_mom(xx):
            sv['model'].train()
            with torch.no_grad():
                p = sv['model'](torch.FloatTensor(np.asarray(xx, np.float32)))
                m = p.mean.numpy() * sv['ys'] + sv['ym']
                s = p.variance.clamp_min(1e-12).sqrt().numpy() * sv['ys']
            return m, s
        record('svgp', sv_mom, mbo.svgp_lcb_torch(sv, beta), mbo.svgp_lcb_np(sv, beta))

    # ---- GP arms ----
    arms = build_gp_arms(x, y, seed)
    far = np.random.RandomState(90000 + seed).uniform(0, 1, (N_FAR, t.dim))
    for name, arm in arms.items():
        mom = gp_moments(arm)
        f_t, f_n = gp_lcb(arm, beta)
        record(name, mom, f_t, f_n)
        mu_far, _ = mom(far)
        res['farfield'][name] = dict(
            ff=float(np.mean((mu_far - ym_D) / sd_y)),                 # in sd_y units
            ff_max=float(np.max((mu_far - ym_D) / sd_y)),
            c=(None if arm['c_std'] is None
               else float((arm['c_std'] * arm['ys'] + arm['ym'] - ym_D) / sd_y)))
        res['gpinfo'][name] = dict(c_fitted_std=arm['c_fitted'], ls_med=arm['ls_med'])

    # ---- held-out predictive quality: the PM2 confound check ----
    r = np.random.RandomState(50000 + seed)
    idx = r.permutation(len(x))
    cut = int(0.8 * len(x))
    xtr, ytr, xte = x[idx[:cut]], y[idx[:cut]], x[idx[cut:]]
    fte = t.oracle(xte)
    fs = float(np.std(fte)) + 1e-12
    ho_arms = build_gp_arms(xtr, ytr, seed)
    for name, arm in ho_arms.items():
        mu, _ = gp_moments(arm)(xte)
        res['heldout'][name] = dict(norm_rmse=float(np.sqrt(np.mean((mu - fte) ** 2)) / fs))
    ms_h = mbo.train_ensemble(xtr, ytr, t.dim, seed=seed, K=K, ep=mbo.TRAIN_EP)
    with torch.no_grad():
        mu, _ = mbo.ens_moments_raw(ms_h, torch.FloatTensor(xte))
    res['heldout']['ens'] = dict(norm_rmse=float(np.sqrt(np.mean((mu.numpy() - fte) ** 2)) / fs))
    return spec, res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seeds', type=int, default=30)
    ap.add_argument('--jobs', type=int, default=24)
    ap.add_argument('--tasks', default='')
    a = ap.parse_args()
    tasks = a.tasks.split(',') if a.tasks else TASKS
    specs = [dict(task=t, seed=s) for t in tasks for s in range(a.seeds)]

    cells, held, far, gpi, consts = {}, {}, {}, {}, {}
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=a.jobs) as ex:
        futs = [ex.submit(_cell, sp) for sp in specs]
        for i, fu in enumerate(as_completed(futs)):
            sp, r = fu.result()
            tk = sp['task']
            for c, v in r['cells'].items():
                d = cells.setdefault(tk, {}).setdefault(c, {})
                for grp in ('star', 'star_lcb', 'allprop'):
                    for k, val in v[grp].items():
                        d.setdefault(grp, {}).setdefault(k, []).append(val)
                for k in ('p100', 'p50'):
                    d.setdefault(k, []).append(v[k])
            for k, v in r['heldout'].items():
                held.setdefault(tk, {}).setdefault(k, {}).setdefault('norm_rmse', []).append(v['norm_rmse'])
            for k, v in r['farfield'].items():
                for m, val in v.items():
                    if val is not None:
                        far.setdefault(tk, {}).setdefault(k, {}).setdefault(m, []).append(val)
            for k, v in r['gpinfo'].items():
                for m, val in v.items():
                    gpi.setdefault(tk, {}).setdefault(k, {}).setdefault(m, []).append(val)
            consts[tk] = r['consts']
            print(f'[{i+1}/{len(specs)}] {tk:16s} seed{sp["seed"]:<3d} '
                  f'{len(r["cells"])} cells  {time.time()-t0:.0f}s', flush=True)

    import run_all
    import mbo

    def agg(v):
        return dict(mean=float(np.mean(v)), std=float(np.std(v)), all=list(map(float, v)))

    out = {'meta': run_all.engine_meta(a.seeds, mbo.BETA, mbo.K_ENS),
           'arms': [g[0] for g in GP_ARMS] + ['ens', 'svgp'],
           'gp_arm_spec': [dict(name=n, const=c, ls=l, refit=rf) for n, c, l, rf in GP_ARMS],
           'config': dict(knn=KNN, n_far=N_FAR, ls_frac=LS_FRAC, c_sup=C_SUP),
           'consts': consts,
           'mbo': {t: {c: {g: ({k: agg(v) for k, v in d.items()} if isinstance(d, dict) else agg(d))
                           for g, d in cs.items()}
                       for c, cs in tc.items()} for t, tc in cells.items()},
           'heldout': {t: {k: {m: agg(v) for m, v in d.items()} for k, d in ks.items()}
                       for t, ks in held.items()},
           'farfield': {t: {k: {m: agg(v) for m, v in d.items()} for k, d in ks.items()}
                        for t, ks in far.items()},
           'gpinfo': {t: {k: {m: agg(v) for m, v in d.items()} for k, d in ks.items()}
                      for t, ks in gpi.items()}}
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, 'phantom_maxima.json')
    with open(p, 'w') as f:
        json.dump(out, f, indent=2)
    print('wrote', p)


if __name__ == '__main__':
    main()
