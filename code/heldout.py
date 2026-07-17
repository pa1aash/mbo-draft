"""A.1.3 -- held-out predictive quality per (task, surrogate, X1-state).

The repo computes held-out RMSE/NLL nowhere (FLAW_LEDGER P1-3). This is the ONLY thing
that separates "inductive bias" (T1) from "the ensemble just fits worse". All predictions
are mapped to RAW oracle units so RMSE/NLL are on one scale; we then also report
normRMSE = RMSE / std(oracle_test) so it is comparable across tasks and surrogates.

Per (task, surrogate, X1 on/off), averaged over seeds:
  normRMSE, NLL_norm (standardized-target Gaussian NLL), and Spearman rho(sigma, |mu-f|).

Reading: if under X1-OFF the ensemble's normRMSE >> GP's and under X1-ON they converge, the
fit-quality gap was a target-scaling artifact and a surviving SCORE gap is genuine bias.
If the ensemble stays worse even under X1-ON, "fits worse" is not separable from "bias".

  python heldout.py --seeds 3 --jobs 6      -> results/heldout.json
"""
import argparse
import json
import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

import numpy as np

SURR = ['ens', 'botorchgp', 'svgp']
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'results', 'heldout.json')


def _subsample(x, y, max_train, seed):
    np.random.seed(seed)
    if len(x) <= max_train:
        return x, y
    top = np.argsort(y)[-int(max_train * 0.2):]
    rest = np.setdiff1d(np.arange(len(x)), top)
    sel = np.concatenate([top, np.random.choice(rest, max_train - len(top), replace=False)])
    return x[sel], y[sel]


def _ens_raw(mbo, x, y, dim, seed):
    ms = mbo.train_ensemble(x, y, dim, seed=seed)
    import torch

    def predict(xx):
        with torch.no_grad():
            mu, sd = mbo.ens_moments_raw(ms, torch.FloatTensor(xx))
        return mu.numpy(), sd.numpy()
    return predict


def _botorch_raw(x, y, seed):
    import torch
    from botorch.models import SingleTaskGP
    from botorch.fit import fit_gpytorch_mll
    from gpytorch.mlls import ExactMarginalLogLikelihood
    np.random.seed(seed); torch.manual_seed(seed)
    x, y = _subsample(x, y, 800, seed)
    xt = torch.DoubleTensor(x); yt = torch.DoubleTensor(y).unsqueeze(-1)
    ym, ys = yt.mean(), yt.std() + 1e-8
    gp = SingleTaskGP(xt, (yt - ym) / ys)
    fit_gpytorch_mll(ExactMarginalLogLikelihood(gp.likelihood, gp)); gp.eval()

    def predict(xx):
        with torch.no_grad():
            post = gp.posterior(torch.DoubleTensor(xx))
            mu = (post.mean.squeeze(-1) * ys + ym).numpy()
            sd = (post.variance.clamp_min(1e-12).sqrt().squeeze(-1) * ys).numpy()
        return mu, sd
    return predict


def _svgp_raw(mbo, x, y, dim, seed):
    import torch
    s = mbo.fit_svgp(x, y, dim, seed)
    if s is None:
        return None
    m, ym, ys = s['model'], s['ym'], s['ys']
    m.eval()

    def predict(xx):
        with torch.no_grad():
            post = m(torch.FloatTensor(xx))
            mu = (post.mean * ys + ym).numpy()
            sd = (post.variance.clamp_min(1e-12).sqrt() * ys).numpy()
        return mu, sd
    return predict


def _cell(spec):
    import torch
    torch.set_num_threads(1)
    os.environ['MBO_X1'] = '1' if spec['x1'] else '0'
    import importlib
    import mbo
    importlib.reload(mbo)                     # pick up MBO_X1 for this worker
    from scipy.stats import spearmanr
    t = mbo.make_tasks([spec['task']])[0]
    x, y = t.data()
    seed = spec['seed']
    np.random.seed(seed); torch.manual_seed(seed)
    xt = np.random.uniform(0, 1, (500, t.dim)).astype(np.float32)
    f = t.oracle(xt)                          # noiseless held-out targets
    s_f = float(f.std() + 1e-9)
    surr = spec['surr']
    if surr == 'ens':
        pred = _ens_raw(mbo, x, y, t.dim, seed)
    elif surr == 'botorchgp':
        pred = _botorch_raw(x, y, seed)
    else:
        pred = _svgp_raw(mbo, x, y, t.dim, seed)
    if pred is None:
        return {**spec, 'metrics': None}
    mu, sd = pred(xt)
    sd = np.maximum(sd, 1e-6)
    rmse = float(np.sqrt(np.mean((mu - f) ** 2)))
    # standardized-target NLL (divide mu, f, sd by oracle-std so it is task-comparable)
    mun, fn, sdn = mu / s_f, f / s_f, sd / s_f
    nll = float(np.mean(0.5 * np.log(2 * np.pi * sdn ** 2) + (fn - mun) ** 2 / (2 * sdn ** 2)))
    rho = float(spearmanr(sd, np.abs(mu - f)).statistic)
    return {**spec, 'metrics': dict(normRMSE=rmse / s_f, RMSE_raw=rmse, NLL_norm=nll,
                                    rho_sigma_err=rho)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seeds', type=int, default=3)
    ap.add_argument('--jobs', type=int, default=max(1, (os.cpu_count() or 2) - 2))
    ap.add_argument('--out', default=OUT)
    a = ap.parse_args()
    import mbo
    tasks = [T().name for T in mbo.ALL_TASKS]
    specs = [{'task': tk, 'surr': s, 'x1': x1, 'seed': sd}
             for tk in tasks for s in SURR for x1 in (0, 1) for sd in range(a.seeds)]
    R = {}
    t0 = time.time()
    print(f'{len(specs)} cells, {a.jobs} workers', flush=True)
    with ProcessPoolExecutor(max_workers=a.jobs) as ex:
        for fut in as_completed([ex.submit(_cell, s) for s in specs]):
            r = fut.result()
            if r['metrics'] is None:
                continue
            key = f"{r['task']}|{r['surr']}|x1={r['x1']}"
            R.setdefault(key, {'normRMSE': [], 'NLL_norm': [], 'rho_sigma_err': []})
            for k in ('normRMSE', 'NLL_norm', 'rho_sigma_err'):
                R[key][k].append(r['metrics'][k])
    agg = {k: {m: float(np.mean(v[m])) for m in v} for k, v in R.items()}
    json.dump(agg, open(a.out, 'w'), indent=1)
    print(f'done in {(time.time()-t0)/60:.1f} min -> {a.out}')
    # summary: ensemble vs GP normRMSE under X1 off/on
    print(f'\n{"task":16}{"ens_off":>9}{"ens_on":>9}{"gp":>9}{"svgp":>9}  (normRMSE)')
    for tk in tasks:
        def g(s, x1): return agg.get(f'{tk}|{s}|x1={x1}', {}).get('normRMSE', float("nan"))
        print(f'{tk:16}{g("ens",0):9.2f}{g("ens",1):9.2f}{g("botorchgp",1):9.2f}{g("svgp",1):9.2f}')


if __name__ == '__main__':
    main()
