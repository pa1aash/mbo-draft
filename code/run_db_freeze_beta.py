"""Step 2: beta contrast for the GP-freeze mechanism. TF-Bind-8, UTR, Superconductor;
all 9 grid cells; beta in {0, 2}; n=16; X1=on X3=on.

Per cell it records p100 (mean/std/all seeds) plus two mechanism metrics read off the
engine's ACTUAL returned design set (captured by wrapping mbo.eval_designs, so the RNG path
is the real one, nothing is re-implemented):
  - decode_in_D  (discrete tasks): fraction of returned designs whose argmax-decoded
    sequence is one of the top-128 dataset sequences -- i.e. the cell returned the reference;
  - disp_from_data: mean over returned designs of the L2 distance to the nearest top-128
    dataset point -- ~0 means the returned set never left the data (defined for all tasks).

Reads (pre-registered DB1-DB4):
  DB2  GP cells constant at beta=2 but move at beta=0  -> sigma-driven freeze (M-A ingredient)
  DB3  Superconductor GP already moves/differs at beta=2 -> no freeze without a decode step
  DB4  the ensemble never freezes (p100 >> dataset best)

  MBO_X1=1 MBO_X3=1 MBO_SPAWN=1 envs/mac-db/bin/python code/run_db_freeze_beta.py

Resumable: completed (task, cell, beta, seed) cells in the output are skipped on rerun.
Env overrides: FREEZE_TASKS, FREEZE_CELLS, FREEZE_BETAS, FREEZE_SEEDS, FREEZE_JOBS,
FREEZE_SUBSAMPLE, FREEZE_OUT.
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

CELLS = ['ens:grad', 'ens:perturb', 'ens:cma',
         'botorchgp:grad', 'botorchgp:perturb', 'botorchgp:cma',
         'svgp:grad', 'svgp:perturb', 'svgp:cma']
TASKS = (os.environ.get('FREEZE_TASKS') or 'TFBind8 UTR Superconductor').split()
CELLSEL = (os.environ.get('FREEZE_CELLS') or ' '.join(CELLS)).split()
BETAS = [float(b) for b in (os.environ.get('FREEZE_BETAS') or '0 2').split()]
SEEDS = int(os.environ.get('FREEZE_SEEDS', '16'))
JOBS = int(os.environ.get('FREEZE_JOBS', '4'))
SUB = int(os.environ.get('FREEZE_SUBSAMPLE', '8000'))
OUT = os.environ.get('FREEZE_OUT',
                     os.path.join(REPO, 'results', 'platform', 'db_freeze_beta_n16.json'))


def _cell(spec):
    """Run one grid cell through the real engine, capturing the returned design set."""
    import torch
    torch.set_num_threads(1)
    import numpy as np
    import mbo
    import db_tasks
    task = db_tasks.make_db_tasks([spec['task']], subsample=spec['sub'])[0]

    cap = {}
    orig = mbo.eval_designs

    def cap_eval(t, xfinal):
        cap['xf'] = np.asarray(xfinal, dtype=np.float32).copy()
        return orig(t, xfinal)

    mbo.eval_designs = cap_eval
    try:
        r = mbo.run_offline(task, spec['seed'], spec['cell'], beta=spec['beta'],
                            ep=mbo.TRAIN_EP, matched=False)
    finally:
        mbo.eval_designs = orig

    base = {'task': spec['task'], 'cell': spec['cell'], 'beta': spec['beta'],
            'seed': spec['seed'], 'x1': bool(mbo.X1_STANDARDIZE_Y),
            'x3': bool(mbo.X3_MATCHED_PROTOCOL)}
    if r is None or 'xf' not in cap:
        return {**base, 'p100': None, 'p50': None,
                'disp_from_data': None, 'decode_in_D': None}

    xf = cap['xf']
    x, y = task.data()
    top = x[np.argsort(y)[-mbo.TOP:]]
    d = np.sqrt(((xf[:, None, :] - top[None, :, :]) ** 2).sum(-1))   # (Nxf, TOP)
    disp_from_data = float(d.min(axis=1).mean())
    if task.discrete:
        dtop = {tuple(rr) for rr in task._decode(top)}
        dret = task._decode(xf)
        decode_in_D = float(np.mean([tuple(rr) in dtop for rr in dret]))
    else:
        decode_in_D = None
    return {**base, 'p100': float(r['p100']), 'p50': float(r['p50']),
            'disp_from_data': disp_from_data, 'decode_in_D': decode_in_D}


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
            'K': int(mbo.K_ENS), 'TOP': int(mbo.TOP), 'OPT_STEPS': int(mbo.OPT_STEPS),
            'LR_OPT': float(mbo.LR_OPT), 'n_seeds': int(SEEDS)}


def key(r):
    return f"{r['task']}|{r['cell']}|{r['beta']}|{r['seed']}"


def summarize(records):
    groups = {}
    for r in records:
        if r.get('p100') is None:
            continue
        groups.setdefault((r['task'], r['cell'], r['beta']), []).append(r)
    summary = {}
    for (tk, cell, beta), rs in groups.items():
        rs = sorted(rs, key=lambda r: r['seed'])
        p = np.array([r['p100'] for r in rs])
        dd = np.array([r['disp_from_data'] for r in rs])
        din = [r['decode_in_D'] for r in rs if r['decode_in_D'] is not None]
        summary.setdefault(tk, {}).setdefault(cell, {})[str(beta)] = {
            'p100_mean': float(p.mean()), 'p100_std': float(p.std()), 'n': len(rs),
            'p100_all': [float(v) for v in p],
            'disp_from_data_mean': float(dd.mean()),
            'decode_in_D_mean': (float(np.mean(din)) if din else None)}
    return summary


def save(doc, out):
    tmp = out + '.tmp'
    with open(tmp, 'w') as f:
        json.dump(doc, f, indent=1)
    os.replace(tmp, out)


def main():
    if not (mbo.X1_STANDARDIZE_Y and mbo.X3_MATCHED_PROTOCOL):
        raise SystemExit('engine is not X1=on X3=on')
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    stamp = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    meta0 = base_meta()

    prior = {}
    if os.path.exists(OUT):
        try:
            old = json.load(open(OUT))
            for r in old.get('records', []):
                prior[key(r)] = r
        except Exception:
            prior = {}

    specs = [{'task': t, 'cell': c, 'beta': b, 'seed': s, 'sub': SUB}
             for t in TASKS for c in CELLSEL for b in BETAS for s in range(SEEDS)]
    todo = [s for s in specs
            if f"{s['task']}|{s['cell']}|{s['beta']}|{s['seed']}" not in prior]
    records = list(prior.values())
    print(f'{len(specs)} total cells ({len(TASKS)} tasks x {len(CELLSEL)} cells x '
          f'{len(BETAS)} betas x {SEEDS} seeds); {len(prior)} already done, {len(todo)} to run; '
          f'{JOBS} spawn workers', flush=True)
    print(f'engine X1={meta0["X1"]} X3={meta0["X3"]} torch={meta0["torch"]} '
          f'git={meta0["git_sha"][:12]}', flush=True)

    ctx = _mp.get_context('spawn')
    t0, done, failed = time.time(), 0, 0
    with ProcessPoolExecutor(max_workers=JOBS, mp_context=ctx) as ex:
        futs = {ex.submit(_cell, s): s for s in todo}
        for fut in as_completed(futs):
            done += 1
            s = futs[fut]
            try:
                r = fut.result()
            except Exception as e:
                failed += 1
                print(f"  FAILED {s['task']}/{s['cell']}/b{s['beta']}/seed{s['seed']}: "
                      f"{type(e).__name__}: {e}", flush=True)
                continue
            r['meta'] = {**meta0, 'beta': float(s['beta']), 'seed': s['seed'],
                         'timestamp': stamp}
            records.append(r)
            if done % 24 == 0 or done == len(todo):
                doc = {'run': {'tasks': TASKS, 'cells': CELLSEL, 'betas': BETAS,
                               'n_seeds': SEEDS, 'db_subsample': SUB, 'jobs': JOBS,
                               'timestamp': stamp, 'git_sha': meta0['git_sha'],
                               'generated_by': 'code/run_db_freeze_beta.py'},
                       'meta_schema': list(meta0.keys()) + ['beta', 'seed', 'timestamp'],
                       'summary': summarize(records), 'records': records}
                save(doc, OUT)
                print(f'  {done}/{len(todo)}  [{(time.time()-t0)/60:.1f}m]  '
                      f'(failed {failed})', flush=True)

    doc = {'run': {'tasks': TASKS, 'cells': CELLSEL, 'betas': BETAS, 'n_seeds': SEEDS,
                   'db_subsample': SUB, 'jobs': JOBS, 'timestamp': stamp,
                   'git_sha': meta0['git_sha'], 'generated_by': 'code/run_db_freeze_beta.py'},
           'meta_schema': list(meta0.keys()) + ['beta', 'seed', 'timestamp'],
           'summary': summarize(records), 'records': records}
    save(doc, OUT)
    print(f'\ndone {done} new cells ({failed} failed) in {(time.time()-t0)/60:.1f} min '
          f'-> {OUT}', flush=True)

    S = doc['summary']
    print('\ntask            cell               beta   p100_mean  p100_std  decode_in_D  disp')
    for t in TASKS:
        for c in CELLSEL:
            for b in BETAS:
                d = S.get(t, {}).get(c, {}).get(str(b))
                if not d:
                    continue
                did = 'n/a' if d['decode_in_D_mean'] is None else f"{d['decode_in_D_mean']:.3f}"
                print(f'  {t:14s} {c:18s} {b:<4g} {d["p100_mean"]:9.4f} {d["p100_std"]:9.4f}  '
                      f'{did:>10s}  {d["disp_from_data_mean"]:.4f}')


if __name__ == '__main__':
    main()
