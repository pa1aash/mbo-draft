"""Step 1: instrument botorchgp:grad on TF-Bind-8 at beta=2 to separate LCB paralysis
(M-A) from decode snap-back (M-B).

Reproduces the exact grid-cell path (mbo.init_candidates -> build_surrogate('botorchgp')
-> gradient ascent -> _select_top -> eval_designs) while capturing, per seed:
  - ||x_final - x0|| in the continuous [0,1]^dim space actually optimized (mean, max over
    the 256 init points), and the gradient norm of -LCB at x0 (does the optimizer even have
    a direction to move?);
  - the fraction of optimized points whose argmax-DECODED sequence is unchanged from x0;
  - whether the returned 128-design set is just a re-selection of the top-128 dataset points,
    and its p100 (must equal the cell's reported constant).

Read: displacement ~ 0  -> M-A (optimizer is pinned at the data, LCB locally maximal there).
      displacement  > 0 but decode identical -> M-B (moved in logit space, argmax snapped back).

  MBO_X1=1 MBO_X3=1 MBO_SPAWN=1 envs/mac-db/bin/python code/probe_gp_freeze.py
"""
import os
os.environ.setdefault('MBO_X1', '1')
os.environ.setdefault('MBO_X3', '1')
os.environ.setdefault('MBO_SPAWN', '1')

import json
import subprocess
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing as _mp

import numpy as np
import torch

import mbo

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
TASK = os.environ.get('PROBE_TASK', 'TFBind8')
BETA = float(os.environ.get('PROBE_BETA', '2.0'))
SEEDS = int(os.environ.get('PROBE_SEEDS', '16'))
JOBS = int(os.environ.get('PROBE_JOBS', '4'))
SUB = int(os.environ.get('PROBE_SUBSAMPLE', '8000'))


def _probe(spec):
    """One seed of botorchgp:grad, instrumented. Mirrors mbo.run_grid_cell's grad path."""
    import torch
    from torch import optim
    torch.set_num_threads(1)
    import mbo
    import db_tasks
    seed = spec['seed']
    task = db_tasks.make_db_tasks([spec['task']], subsample=spec['sub'])[0]

    np.random.seed(seed)
    torch.manual_seed(seed)
    x, y = task.data()
    x0 = mbo.init_candidates(x, y, seed)                       # (2*TOP, dim)
    f_torch, f_np, _ = mbo.build_surrogate('botorchgp', x, y, task.dim, seed,
                                           spec['beta'], mbo.TRAIN_EP, mbo.K_ENS)

    x0t = torch.FloatTensor(x0)
    # gradient norm of the ascent objective at the init points
    xg = x0t.clone().detach().requires_grad_(True)
    g = torch.autograd.grad((-f_torch(xg).mean()), xg)[0]
    gradnorm0 = g.norm(dim=1)                                  # per init point

    # replicate mbo.grad_opt (X3 on): Adam lr=LR_OPT, OPT_STEPS, clamp, pool trajectory
    xv = x0t.clone().detach().requires_grad_(True)
    o = optim.Adam([xv], lr=mbo.LR_OPT)
    pool = [x0t.clone().detach()]
    for _ in range(mbo.OPT_STEPS):
        o.zero_grad()
        (-f_torch(xv).mean()).backward()
        o.step()
        with torch.no_grad():
            xv.clamp_(0, 1)
            pool.append(xv.clone().detach())
    x_final = xv.detach()
    xf = mbo._select_top(torch.cat(pool).numpy(),
                         lambda a: mbo._score_np_from_torch(f_torch, a))   # returned TOP designs
    p100, p50 = mbo.eval_designs(task, xf)

    disp = (x_final - x0t).norm(dim=1).numpy()                # per init point, continuous space

    # decode identity: argmax-decoded optimized point vs its own x0 (discrete tasks only)
    if task.discrete:
        d0 = task._decode(x0)                                 # (2*TOP, L) int
        df = task._decode(x_final.numpy())
        row_ident = (d0 == df).all(axis=1)                    # per point: sequence unchanged
        slot_agree = float((d0 == df).mean())                 # per-position agreement
        decode_ident_frac = float(row_ident.mean())
        # returned set vs the top-TOP dataset points
        top = x[np.argsort(y)[-mbo.TOP:]]
        dtop = {tuple(r) for r in task._decode(top)}
        dret = task._decode(xf)
        returned_in_top = float(np.mean([tuple(r) in dtop for r in dret]))
    else:
        decode_ident_frac = slot_agree = returned_in_top = None

    return {'seed': seed, 'p100': float(p100), 'p50': float(p50),
            'disp_mean': float(disp.mean()), 'disp_max': float(disp.max()),
            'disp_median': float(np.median(disp)),
            'gradnorm0_mean': float(gradnorm0.mean().item()),
            'gradnorm0_max': float(gradnorm0.max().item()),
            'decode_ident_frac': decode_ident_frac, 'slot_agree': slot_agree,
            'returned_in_top128': returned_in_top}


def base_meta():
    import platform as _plat
    import botorch, gpytorch, cma
    def v(m): return getattr(m, '__version__', '?')
    try:
        sha = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=REPO,
                                      stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        sha = 'unknown'
    return {'platform': _plat.platform(), 'os_release': _plat.release(),
            'python': _plat.python_version(), 'torch': v(torch), 'numpy': v(np),
            'botorch': v(botorch), 'gpytorch': v(gpytorch), 'cma': v(cma), 'git_sha': sha,
            'X1': bool(mbo.X1_STANDARDIZE_Y), 'X3': bool(mbo.X3_MATCHED_PROTOCOL),
            'K': int(mbo.K_ENS), 'beta': float(BETA), 'TOP': int(mbo.TOP),
            'OPT_STEPS': int(mbo.OPT_STEPS), 'LR_OPT': float(mbo.LR_OPT),
            'n_seeds': int(SEEDS)}


def main():
    if not (mbo.X1_STANDARDIZE_Y and mbo.X3_MATCHED_PROTOCOL):
        raise SystemExit('engine is not X1=on X3=on')
    out = os.path.join(REPO, 'results', 'platform', 'gp_freeze_step1.json')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    stamp = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    meta0 = base_meta()
    print(f'botorchgp:grad instrumented on {TASK}, beta={BETA}, {SEEDS} seeds, '
          f'X1={meta0["X1"]} X3={meta0["X3"]} torch={meta0["torch"]}', flush=True)

    ctx = _mp.get_context('spawn')
    rows = []
    with ProcessPoolExecutor(max_workers=JOBS, mp_context=ctx) as ex:
        futs = [ex.submit(_probe, {'task': TASK, 'seed': s, 'beta': BETA, 'sub': SUB})
                for s in range(SEEDS)]
        for fut in as_completed(futs):
            rows.append(fut.result())
    rows.sort(key=lambda r: r['seed'])

    def col(k):
        return np.array([r[k] for r in rows if r[k] is not None], dtype=float)

    agg = {k: {'mean': float(col(k).mean()), 'min': float(col(k).min()),
               'max': float(col(k).max())}
           for k in ['p100', 'disp_mean', 'disp_max', 'gradnorm0_mean',
                     'decode_ident_frac', 'returned_in_top128'] if len(col(k))}

    doc = {'run': {'task': TASK, 'cell': 'botorchgp:grad', 'beta': BETA, 'n_seeds': SEEDS,
                   'db_subsample': SUB, 'timestamp': stamp, 'git_sha': meta0['git_sha'],
                   'generated_by': 'code/probe_gp_freeze.py'},
           'meta': {**meta0, 'timestamp': stamp}, 'aggregate': agg,
           'per_seed': [{**r, 'meta': {**meta0, 'seed': r['seed'], 'timestamp': stamp}}
                        for r in rows]}
    tmp = out + '.tmp'
    with open(tmp, 'w') as f:
        json.dump(doc, f, indent=1)
    os.replace(tmp, out)

    print(f'\n-> {out}\n')
    print(f'{"seed":>4} {"p100":>7} {"disp_mean":>10} {"disp_max":>9} {"||grad@x0||":>11} '
          f'{"decode_id":>10} {"ret_in_top":>10}')
    for r in rows:
        print(f'{r["seed"]:>4} {r["p100"]:>7.4f} {r["disp_mean"]:>10.4e} {r["disp_max"]:>9.4e} '
              f'{r["gradnorm0_mean"]:>11.4e} {r["decode_ident_frac"]:>10.4f} '
              f'{r["returned_in_top128"]:>10.4f}')
    dm = col('disp_mean')
    print(f'\naggregate: disp_mean {dm.mean():.4e} (max over seeds {dm.max():.4e})  '
          f'grad@x0 {col("gradnorm0_mean").mean():.4e}  '
          f'decode_ident {col("decode_ident_frac").mean():.4f}  '
          f'returned_in_top128 {col("returned_in_top128").mean():.4f}  '
          f'p100 {col("p100").mean():.4f}')


if __name__ == '__main__':
    main()
