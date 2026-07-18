"""Platform-variance runner: one Design-Bench task, the full 3x3 surrogate x optimizer
grid, n seeds, every record stamped with the exact environment + engine meta block so a
run on one OS/library stack is directly comparable to a run on another.

Motivation: on TFBind8 the neural-surrogate cells (ens:*, svgp:*) move across OS/library
stacks while the deterministic exact-GP cells reproduce to 1.000. A point estimate cannot
tell a real cross-platform shift from seed noise, so this runner reports the full per-cell
distribution (mean, std, every seed value) at a MATCHED, STAMPED engine (X1/X3 explicit),
not a point estimate against an unverified published number.

The numbers come from the identical engine path as results_db.json: each (cell, seed) is
run through run_all._worker -> mbo.run_offline, so scheduling and the meta wrapper add
nothing to the science. Only the provenance stamp is new.

  MBO_SPAWN=1 MBO_X1=1 MBO_X3=1 envs/mac-db/bin/python code/run_platform.py

Env overrides (for plumbing smoke): PLATFORM_SEEDS, PLATFORM_JOBS, PLATFORM_TASK,
PLATFORM_SUBSAMPLE, PLATFORM_OUT.
"""
import os

# Set the engine switches and the spawn requirement BEFORE mbo is imported anywhere, in
# both the parent and every spawned worker (this module is re-imported on spawn). Default
# to the audited on/on engine; honor an explicit override if the caller set one.
os.environ.setdefault('MBO_X1', '1')          # standardize ensemble regression targets
os.environ.setdefault('MBO_X3', '1')          # one selection rule, exactly TOP proposals/cell
os.environ.setdefault('MBO_SPAWN', '1')       # fork crashes torch+design_bench on macOS

import json
import subprocess
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing as _mp

import numpy as np
import torch

import mbo
import run_all                                  # reuse the exact cell worker

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)

# The paper's decomposition grid: 3 surrogates x 3 optimizers.
CELLS = ['ens:grad', 'ens:perturb', 'ens:cma',
         'botorchgp:grad', 'botorchgp:perturb', 'botorchgp:cma',
         'svgp:grad', 'svgp:perturb', 'svgp:cma']


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
    """The 18 stack/engine fields shared by every record; `seed` is filled in per record.
    This is the schema both platform halves must share verbatim to be comparable."""
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
        'X1':        bool(mbo.X1_STANDARDIZE_Y),
        'X3':        bool(mbo.X3_MATCHED_PROTOCOL),
        'K':         int(mbo.K_ENS),
        'beta':      float(mbo.BETA),
        'TOP':       int(mbo.TOP),
        'OPT_STEPS': int(mbo.OPT_STEPS),
        'LR_OPT':    float(mbo.LR_OPT),
        'n_seeds':   int(n_seeds),
        # 'seed' and 'timestamp' are stamped per record.
    }


def main():
    task = os.environ.get('PLATFORM_TASK', 'TFBind8')
    seeds = int(os.environ.get('PLATFORM_SEEDS', '16'))
    jobs = int(os.environ.get('PLATFORM_JOBS', '4'))
    subsample = int(os.environ.get('PLATFORM_SUBSAMPLE', '8000'))
    out = os.environ.get('PLATFORM_OUT',
                         os.path.join(REPO, 'results', 'platform',
                                      f'tfbind8_macos_torch28_n{seeds}.json'))
    os.makedirs(os.path.dirname(out), exist_ok=True)

    if not (mbo.X1_STANDARDIZE_Y and mbo.X3_MATCHED_PROTOCOL):
        raise SystemExit('engine is not X1=on X3=on; refusing to run a mislabeled grid')

    stamp = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    meta0 = base_meta(seeds)

    specs = [{'exp': 'mbo', 'task': task, 'variant': cell, 'seed': s,
              'ep': mbo.TRAIN_EP, 'beta': mbo.BETA, 'k': 0,
              'db': True, 'db_sub': subsample, 'matched': False}
             for cell in CELLS for s in range(seeds)]

    print(f'{len(specs)} cells ({len(CELLS)} grid cells x {seeds} seeds) on {task}, '
          f'{jobs} spawn workers, subsample={subsample}', flush=True)
    print(f'engine: X1={meta0["X1"]} X3={meta0["X3"]} K={meta0["K"]} beta={meta0["beta"]} '
          f'torch={meta0["torch"]} git={meta0["git_sha"][:12]} dirty={git_dirty()}', flush=True)

    # p100[cell][seed], p50[cell][seed]
    p100 = {c: {} for c in CELLS}
    p50 = {c: {} for c in CELLS}
    records = []
    ctx = _mp.get_context('spawn')
    t0, done, failed = time.time(), 0, 0
    with ProcessPoolExecutor(max_workers=jobs, mp_context=ctx) as ex:
        futs = {ex.submit(run_all._worker, s): s for s in specs}
        for fut in as_completed(futs):
            done += 1
            s = futs[fut]
            try:
                r = fut.result()
            except Exception as e:
                failed += 1
                print(f"  CELL FAILED {s['variant']} seed{s['seed']}: "
                      f"{type(e).__name__}: {e}", flush=True)
                continue
            m = r['metrics']
            if m is None:
                failed += 1
                print(f"  CELL SKIPPED {s['variant']} seed{s['seed']} (surrogate/optimizer "
                      f"unavailable)", flush=True)
                continue
            cell, seed = r['variant'], r['seed']
            p100[cell][seed] = m['p100']
            p50[cell][seed] = m['p50']
            rec = {'task': task, 'cell': cell, 'p100': m['p100'], 'p50': m['p50'],
                   'meta': {**meta0, 'seed': int(seed), 'timestamp': stamp}}
            records.append(rec)
            if done % 12 == 0 or done == len(specs):
                print(f'  {done}/{len(specs)}  [{(time.time()-t0)/60:.1f}m]', flush=True)

    def dist(d):
        vals = [d[s] for s in sorted(d)]
        if not vals:
            return None
        return {'mean': float(np.mean(vals)), 'std': float(np.std(vals)),
                'n': len(vals), 'all': [float(v) for v in vals]}

    summary = {c: {'p100': dist(p100[c]), 'p50': dist(p50[c])} for c in CELLS}

    records.sort(key=lambda r: (CELLS.index(r['cell']), r['meta']['seed']))
    doc = {
        'run': {
            'task': task, 'metric_of_interest': 'p100', 'n_seeds': seeds,
            'grid_cells': CELLS, 'db_subsample': subsample, 'jobs': jobs,
            'timestamp': stamp, 'git_sha': meta0['git_sha'], 'git_dirty': git_dirty(),
            'generated_by': 'code/run_platform.py',
        },
        'meta_schema': list(meta0.keys()) + ['seed', 'timestamp'],
        'summary': summary,
        'records': records,
    }
    tmp = out + '.tmp'
    with open(tmp, 'w') as f:
        json.dump(doc, f, indent=1)
    os.replace(tmp, out)

    print(f'\ndone {done} cells ({failed} failed) in {(time.time()-t0)/60:.1f} min '
          f'-> {out}', flush=True)
    print('\nper-cell p100 (mean +/- std, n):', flush=True)
    for c in CELLS:
        s = summary[c]['p100']
        if s:
            print(f'  {c:20s} {s["mean"]:.4f} +/- {s["std"]:.4f}  (n={s["n"]})', flush=True)
        else:
            print(f'  {c:20s} no data', flush=True)


if __name__ == '__main__':
    main()
