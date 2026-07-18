"""ens:grad engine 2x2 on one Design-Bench task: sweep {X1 off/on} x {X3 off/on} at fixed
OS/library stack, n seeds, every record stamped with the same env+engine meta block as
run_platform.py.

Purpose: disentangle a target-scaling engine effect (X1) from a genuine cross-platform
shift. X1_STANDARDIZE_Y touches only train_ensemble; SVGP and the GP already z-score their
own targets, so if the ensemble alone moved between stacks the mover may be X1, not the OS.
This runs the ensemble+gradient cell under all four engine corners so the corner that
reproduces a target distribution (e.g. an unverified published number) is identified
directly, on-machine.

Each corner runs in its own freshly spawned worker pool: the engine switches bind at mbo
import time, so MBO_X1/MBO_X3 are set in the environment before the pool is created and the
spawned workers import mbo with those values. Every worker RETURNS the flags it actually
read; the driver asserts they match the intended corner, so the stamp is verified.

  MBO_SPAWN=1 envs/mac-db/bin/python code/run_engine_2x2.py

Env overrides (smoke): ENGINE_SEEDS, ENGINE_JOBS, ENGINE_TASK, ENGINE_SUBSAMPLE, ENGINE_OUT.
"""
import os
os.environ.setdefault('MBO_SPAWN', '1')        # fork crashes torch+design_bench on macOS

import json
import subprocess
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing as _mp

import numpy as np
import torch

import mbo                                       # env-independent constants (BETA, K, ...)

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)

CELL = 'ens:grad'
# (MBO_X1, MBO_X3, tag). on_on is re-run here too so the file is a self-contained 2x2 and
# cross-checks run_platform.py's on_on cell.
CORNERS = [('0', '0', 'off_off'), ('1', '0', 'on_off'),
           ('0', '1', 'off_on'), ('1', '1', 'on_on')]
PUB = 2.2007                                     # results_db.json TFBind8 ens:grad (engine UNVERIFIED)


def _cell(spec):
    """One (corner, seed). Reads the engine flags the worker actually bound and returns
    them alongside the metric so the driver can verify the stamp."""
    import torch
    torch.set_num_threads(1)
    import mbo
    import db_tasks
    t = db_tasks.make_db_tasks([spec['task']], subsample=spec['sub'])[0]
    r = mbo.run_offline(t, spec['seed'], 'ens:grad', beta=mbo.BETA, ep=mbo.TRAIN_EP)
    return {'seed': spec['seed'], 'p100': r['p100'], 'p50': r['p50'],
            'x1': bool(mbo.X1_STANDARDIZE_Y), 'x3': bool(mbo.X3_MATCHED_PROTOCOL)}


def _ver(mod):
    return getattr(mod, '__version__', '?')


def git_sha():
    try:
        return subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=REPO,
                                       stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        return 'unknown'


def git_dirty():
    try:
        out = subprocess.check_output(['git', 'status', '--porcelain'], cwd=REPO,
                                      stderr=subprocess.DEVNULL).decode().strip()
        return bool(out)
    except Exception:
        return None


def base_meta(n_seeds):
    """The stack/engine fields shared by every record; X1/X3/seed/timestamp per record."""
    import platform as _plat
    import botorch
    import gpytorch
    import cma
    return {
        'platform':  _plat.platform(),
        'os_release': _plat.release(),
        'python':    _plat.python_version(),
        'torch':     _ver(torch),
        'numpy':     _ver(np),
        'botorch':   _ver(botorch),
        'gpytorch':  _ver(gpytorch),
        'cma':       _ver(cma),
        'git_sha':   git_sha(),
        'K':         int(mbo.K_ENS),
        'beta':      float(mbo.BETA),
        'TOP':       int(mbo.TOP),
        'OPT_STEPS': int(mbo.OPT_STEPS),
        'LR_OPT':    float(mbo.LR_OPT),
        'n_seeds':   int(n_seeds),
        # 'X1', 'X3', 'seed', 'timestamp' stamped per record.
    }


def dist(vals):
    a = np.array(vals, dtype=float)
    mean, std = float(a.mean()), float(a.std())
    se = float(a.std(ddof=1) / np.sqrt(len(a))) if len(a) > 1 else 0.0
    lo, hi = mean - 1.96 * se, mean + 1.96 * se
    return {'mean': mean, 'std': std, 'n': len(a), 'min': float(a.min()),
            'max': float(a.max()), 'ci95': [lo, hi],
            'contains_2.20': bool(lo <= PUB <= hi), 'n_ge_2.20': int((a >= PUB).sum()),
            'all': [float(v) for v in a]}


def main():
    task = os.environ.get('ENGINE_TASK', 'TFBind8')
    seeds = int(os.environ.get('ENGINE_SEEDS', '16'))
    jobs = int(os.environ.get('ENGINE_JOBS', '4'))
    sub = int(os.environ.get('ENGINE_SUBSAMPLE', '8000'))
    out = os.environ.get('ENGINE_OUT',
                         os.path.join(REPO, 'results', 'platform',
                                      f'tfbind8_engine_2x2_n{seeds}.json'))
    os.makedirs(os.path.dirname(out), exist_ok=True)

    stamp = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    meta0 = base_meta(seeds)
    print(f'{CELL} engine 2x2 on {task}, {seeds} seeds/corner, {jobs} spawn workers, '
          f'subsample={sub}, torch={meta0["torch"]} git={meta0["git_sha"][:12]}', flush=True)

    records, summary = [], {}
    t0 = time.time()
    for x1, x3, tag in CORNERS:
        os.environ['MBO_X1'] = x1
        os.environ['MBO_X3'] = x3
        want = (x1 == '1', x3 == '1')
        ctx = _mp.get_context('spawn')
        rows = []
        with ProcessPoolExecutor(max_workers=jobs, mp_context=ctx) as ex:
            futs = [ex.submit(_cell, {'task': task, 'seed': s, 'sub': sub})
                    for s in range(seeds)]
            for fut in as_completed(futs):
                rows.append(fut.result())
        # verify the engine each worker actually ran matches the intended corner
        for r in rows:
            if (r['x1'], r['x3']) != want:
                raise SystemExit(f'corner {tag}: worker ran X1={r["x1"]} X3={r["x3"]}, '
                                 f'intended {want} -- flag propagation failed, aborting')
        rows.sort(key=lambda r: r['seed'])
        for r in rows:
            records.append({'task': task, 'cell': CELL, 'corner': tag,
                            'p100': r['p100'], 'p50': r['p50'],
                            'meta': {**meta0, 'X1': want[0], 'X3': want[1],
                                     'seed': r['seed'], 'timestamp': stamp}})
        d = dist([r['p100'] for r in rows])
        summary[tag] = {'X1': want[0], 'X3': want[1], 'p100': d,
                        'p50': dist([r['p50'] for r in rows])}
        print(f'  corner {tag:8s} X1={want[0]!s:5s} X3={want[1]!s:5s}  '
              f'p100 {d["mean"]:.4f} +/- {d["std"]:.4f}  max={d["max"]:.4f}  '
              f'contains 2.20: {d["contains_2.20"]}  [{(time.time()-t0)/60:.1f}m]', flush=True)

    doc = {
        'run': {'task': task, 'cell': CELL, 'metric_of_interest': 'p100',
                'n_seeds': seeds, 'corners': [c[2] for c in CORNERS], 'db_subsample': sub,
                'jobs': jobs, 'reference_ens_grad': PUB, 'timestamp': stamp,
                'git_sha': meta0['git_sha'], 'git_dirty': git_dirty(),
                'generated_by': 'code/run_engine_2x2.py'},
        'meta_schema': list(meta0.keys()) + ['X1', 'X3', 'seed', 'timestamp'],
        'summary': summary,
        'records': records,
    }
    tmp = out + '.tmp'
    with open(tmp, 'w') as f:
        json.dump(doc, f, indent=1)
    os.replace(tmp, out)
    print(f'\ndone {len(records)} cells in {(time.time()-t0)/60:.1f} min -> {out}', flush=True)
    print('\ncorner            X1    X3    mean    std     max    contains 2.20  n>=2.20')
    for tag in [c[2] for c in CORNERS]:
        s = summary[tag]['p100']
        print(f'  {tag:14s} {summary[tag]["X1"]!s:5s} {summary[tag]["X3"]!s:5s} '
              f'{s["mean"]:.4f} {s["std"]:.4f}  {s["max"]:.4f}   {s["contains_2.20"]!s:5s}'
              f'         {s["n_ge_2.20"]}')


if __name__ == '__main__':
    main()
