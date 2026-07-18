"""Consolidated experiment runner. Writes results/results_camera.json (merge-updates,
so partial runs accumulate and reruns overwrite only what they recompute).

  python run_all.py --exp mbo --seeds 30 --jobs 32
  python run_all.py --exp o2o --seeds 15 --jobs 32
  python run_all.py --exp beta --exp K --exp calibration --seeds 10
  python run_all.py --exp all --seeds 30 --jobs 48
  python run_all.py --exp mbo --tasks Ackley2D Ackley5D Ackley10D Ackley20D Ackley50D Ackley100D   # scaling ladder
  python run_all.py --smoke                 # ~2 min sanity pass on Branin

Every experiment expands to a flat list of independent (task, variant, seed) CELLS.
Cells run through a ProcessPoolExecutor (--jobs workers) and are folded back by
(exp, task, variant), aggregated over seeds. One code path, embarrassingly parallel,
merge-safe: a killed run resumes because completed cells are already in the JSON and
skipped on rerun (unless --force).
"""
import argparse
import datetime
import json
import os
import platform
import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
import numpy as np
import mbo

RESULTS = os.path.join(os.path.dirname(__file__), '..', 'results')

# Basenames of the primary published artifacts / reproduction gates. Writing to one of
# these is refused unless --i-mean-it is passed (0.3): a prior session clobbered the
# camera file with a different engine's cells because any in-repo run defaulted to it.
CAMERA_FILES = ('results_camera.json', 'results_db.json')

def out_path(db, matched=False):
    base = 'results_db' if db else 'results_camera'
    return os.path.join(RESULTS, f'{base}{"_matched" if matched else ""}.json')

# ---------------- engine metadata (0.4) -------------------------------------
# Engine state is RECORDED in every result file, never inferred from a filename. The
# on_on-corner loss happened because a file built under one engine was later READ as a
# different one. Every file carries a top-level `meta` block; every per-cell variant node
# carries an `_engine` sub-block; a loader assertion rejects any file lacking a complete
# meta; and a run refuses to MERGE into a file whose X1/X3 differ from the current engine.
REQUIRED_META = ('platform', 'os_release', 'python', 'torch', 'numpy', 'botorch',
                 'gpytorch', 'cma', 'git_sha', 'X1', 'X3', 'K', 'beta', 'TOP',
                 'OPT_STEPS', 'LR_OPT', 'n_seeds', 'seed', 'timestamp')

def _git_sha():
    try:
        return subprocess.check_output(['git', 'rev-parse', 'HEAD'],
                                       cwd=os.path.dirname(os.path.abspath(__file__)),
                                       stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        return 'unknown'

def _pkg_version(name):
    try:
        from importlib.metadata import version
        return version(name)
    except Exception:
        return None

def engine_meta(n_seeds, beta, K):
    """Full provenance block written at the top level of every result file."""
    return {
        'platform': platform.platform(),
        'os_release': platform.release(),
        'python': sys.version.split()[0],
        'torch': _pkg_version('torch'),
        'numpy': _pkg_version('numpy'),
        'botorch': _pkg_version('botorch'),
        'gpytorch': _pkg_version('gpytorch'),
        'cma': _pkg_version('cma'),
        'git_sha': _git_sha(),
        'X1': bool(mbo.X1_STANDARDIZE_Y),
        'X3': bool(mbo.X3_MATCHED_PROTOCOL),
        'K': K, 'beta': beta,
        'TOP': mbo.TOP, 'OPT_STEPS': mbo.OPT_STEPS, 'LR_OPT': mbo.LR_OPT,
        'n_seeds': n_seeds, 'seed': f'0..{n_seeds - 1}',
        'timestamp': datetime.datetime.now().isoformat(timespec='seconds'),
    }

def cell_engine(exp, variant, beta, K):
    """Per-cell engine record. beta/K vary by cell in the beta/K sweeps, so each cell
    carries its ACTUAL beta/K rather than the file-level default."""
    e = {'X1': bool(mbo.X1_STANDARDIZE_Y), 'X3': bool(mbo.X3_MATCHED_PROTOCOL),
         'K': K, 'beta': beta, 'TOP': mbo.TOP, 'OPT_STEPS': mbo.OPT_STEPS,
         'LR_OPT': mbo.LR_OPT}
    if exp == 'beta':
        e['beta'] = float(variant)
    elif exp == 'K':
        e['K'] = int(variant)
    return e

def require_meta(R, path):
    """Loader assertion: reject any result file lacking a complete engine meta block."""
    meta = R.get('meta') if isinstance(R, dict) else None
    missing = [k for k in REQUIRED_META if not isinstance(meta, dict) or k not in meta]
    if missing:
        raise AssertionError(f'{path}: result file lacks a complete engine meta block '
                             f'(missing {missing}). Engine state cannot be inferred from '
                             f'a filename; refusing to trust this file.')
    return meta

def load_checked(path):
    """Load a result file and enforce the meta assertion. For analysis / downstream use."""
    with open(path) as f:
        R = json.load(f)
    require_meta(R, path)
    return R

def build_task(name, db, subsample=None):
    if db:
        import db_tasks
        # ponytail: reconstructs the DB task per cell (design_bench caches data on disk,
        # so make() is cheap after the first call). subsample caps the offline dataset
        # (score-biased) — essential: TFBind10 ships 4.16M rows, untrainable in full.
        return db_tasks.make_db_tasks([name], subsample=subsample)[0]
    return mbo.make_tasks([name])[0]

# ---------------- cell worker (module-level = picklable for spawn/fork) ------
def _worker(spec):
    """spec: dict with exp, task, variant, seed, + params. Returns spec + metrics."""
    import torch
    torch.set_num_threads(1)                       # parallelism is across processes
    task = build_task(spec['task'], spec.get('db', False), spec.get('db_sub'))
    e, seed, ep = spec['exp'], spec['seed'], spec['ep']
    if e == 'mbo':
        r = mbo.run_offline(task, seed, spec['variant'], beta=spec.get('beta', mbo.BETA), ep=ep,
                            matched=spec.get('matched', False))
        m = None if r is None else {'p100': r['p100'], 'p50': r['p50']}
    elif e == 'o2o':
        r = mbo.run_o2o(task, seed, k=spec['k'], select=spec['variant'], ep=ep)
        m = {'imp': r['imp'], 'on_p100': r['on_p100'], 'off_p100': r['off_p100']}
    elif e == 'beta':
        m = {'p100': mbo.run_offline(task, seed, 'lcb', beta=float(spec['variant']), ep=ep)['p100']}
    elif e == 'K':
        m = {'p100': mbo.run_offline(task, seed, 'lcb', K=int(spec['variant']), ep=ep)['p100']}
    elif e == 'calibration':
        c = mbo.run_calibration(task, seed, ep=ep)
        m = {'rho_err': c['rho_err'], 'rho_knn': c['rho_knn'], 'q_conformal': c['q_conformal'],
             'cov_conf_indist': c['cov_conf_indist'], 'cov_conf_ood': c['cov_conf_ood']}
        for b, v in c['cov_indist'].items(): m[f'cov_indist@{b}'] = v
        for b, v in c['cov_ood'].items():    m[f'cov_ood@{b}'] = v
    else:
        raise ValueError(e)
    return {**{k: spec[k] for k in ('exp', 'task', 'variant', 'seed')}, 'metrics': m}

# ---------------- per-experiment cell specs ---------------------------------
def variants(exp, methods=None):
    return {'mbo': (methods or mbo.OFFLINE_METHODS),
            'o2o': ['greedy', 'diversity', 'random'],
            'beta': ['0.0', '0.5', '1.0', '2.0', '5.0'],
            'K': ['2', '3', '5', '10'],
            'calibration': ['_']}[exp]

def build_specs(exp, tasks, seeds, ep, k, methods=None, beta=None):
    for task in tasks:
        for v in variants(exp, methods):
            for s in range(seeds):
                spec = {'exp': exp, 'task': task.name, 'variant': v, 'seed': s, 'ep': ep, 'k': k}
                if beta is not None:
                    spec['beta'] = beta        # mbo grid cells honour a swept beta (Phase 3)
                yield spec

# ---------------- json fold -------------------------------------------------
def agg(vals):
    vals = [v for v in vals if v is not None]
    if not vals: return None
    return {'mean': float(np.mean(vals)), 'std': float(np.std(vals)), 'all': [float(v) for v in vals]}

def load(out):
    if os.path.exists(out):
        with open(out) as f: return json.load(f)
    return {}

def save(R, out):
    tmp = out + '.tmp'
    with open(tmp, 'w') as f: json.dump(R, f, indent=1)
    os.replace(tmp, out)                            # atomic — survives a kill mid-write

def have(R, exp, task, variant, seeds):
    """Cell already complete for all requested seeds? (merge-safe resume).
    Skips reserved keys (e.g. `_engine`) so the per-cell engine stamp is not mistaken
    for a metric."""
    try:
        node = R[exp][task][variant]
        metrics = [v for k, v in node.items() if not k.startswith('_')]
        if not metrics:
            return False
        anymetric = metrics[0]
        return anymetric.get('all') is not None and len(anymetric['all']) >= seeds
    except (KeyError, AttributeError):
        return False

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--exp', action='append', choices=['mbo', 'o2o', 'beta', 'K', 'calibration', 'all'])
    ap.add_argument('--seeds', type=int, default=30)
    ap.add_argument('--tasks', nargs='*', default=None)
    ap.add_argument('--k', type=int, default=50)
    # ponytail: Windows spawn + torch/gpytorch in many workers hard-crashes with no
    # traceback at high job counts; cap the default there. Linux (fork) is unaffected
    # -- pass --jobs explicitly on the cloud box. Also: run ONE writer per results
    # file at a time; concurrent runs race on the JSON and clobber each other.
    _default_jobs = min(4, os.cpu_count() or 2) if os.name == 'nt' else max(1, (os.cpu_count() or 2) - 1)
    ap.add_argument('--jobs', type=int, default=_default_jobs)
    ap.add_argument('--force', action='store_true', help='recompute cells already in the JSON')
    ap.add_argument('--db', action='store_true', help='run on Design-Bench tasks -> results_db.json')
    ap.add_argument('--db-subsample', type=int, default=8000, help='cap DB offline dataset (score-biased); 0=full')
    ap.add_argument('--matched-tuning', action='store_true',
                    help='GATE-1 fair-tuning control: freeze GP per-run HPO so it gets the '
                         'same zero tuning budget as the ensemble. Writes results_*_matched.json.')
    ap.add_argument('--out', default=None,
                    help='override the output JSON path. The default (results/results_camera.json '
                         'or results_db.json) is the primary manuscript artifact; ANY in-repo run '
                         'overwrites it. Pass --out to isolate corner / ablation runs to their own '
                         'file so the primary artifact is never clobbered.')
    ap.add_argument('--methods', nargs='*', default=None,
                    help='restrict the mbo variant list to these methods (e.g. the 9 grid cells for '
                         'a corner run). Default: all OFFLINE_METHODS. No effect on non-mbo exps.')
    ap.add_argument('--beta', type=float, default=None,
                    help='override the LCB beta for the mbo grid cells (default mbo.BETA=2.0). '
                         'Lets the full 3x3 grid be swept over beta (Phase 3) without the '
                         'ensemble-gradient-only `beta` exp.')
    ap.add_argument('--allow-noop', action='store_true',
                    help='permit a run that schedules 0 cells (normally an ERROR / exit 2).')
    ap.add_argument('--i-mean-it', action='store_true',
                    help='permit writing to a primary artifact (results_camera.json / '
                         'results_db.json). Refused otherwise (0.3).')
    ap.add_argument('--smoke', action='store_true')
    a = ap.parse_args()
    out = a.out or out_path(a.db, a.matched_tuning)

    # 0.3 CAMERA GUARD: never clobber a primary published artifact by accident.
    if a.smoke and a.out is None:
        out = os.path.join(RESULTS, 'smoke.json')            # never smoke-clobber the camera
    if os.path.basename(out) in CAMERA_FILES and not a.i_mean_it:
        print(f'ERROR: {out} is a primary published artifact / reproduction gate. '
              f'Refusing to write it. Use --out <scratch path> to isolate this run, or '
              f'--i-mean-it if you truly intend to overwrite the camera file.', flush=True)
        sys.exit(3)

    if a.smoke:
        tasks, seeds, ep, exps, a.k, a.jobs = mbo.make_tasks(['Branin-2D']), 2, 3, ['mbo', 'o2o', 'beta', 'K', 'calibration'], 10, 2
    elif a.db:
        import db_tasks
        names = a.tasks or list(db_tasks.TASKS)
        tasks, seeds, ep = [type('N', (), {'name': n})() for n in names], a.seeds, mbo.TRAIN_EP  # names only; workers build
        exps = a.exp or ['mbo']
        if 'all' in exps: exps = ['mbo', 'o2o', 'calibration']    # beta/K sweeps are synthetic-only
    else:
        tasks, seeds, ep = mbo.make_tasks(a.tasks), a.seeds, mbo.TRAIN_EP
        exps = a.exp or ['mbo']
        if 'all' in exps: exps = ['mbo', 'o2o', 'beta', 'K', 'calibration']

    R = load(out)
    beta_val = a.beta if a.beta is not None else mbo.BETA
    meta = engine_meta(seeds, beta_val, mbo.K_ENS)

    # ENGINE-MATCH ON RESUME: refuse to MERGE new cells into a file whose recorded engine
    # (X1/X3) differs from the current one. This is the class-of-bug fix: the on_on corner
    # was lost because cells from one engine accumulated in a file later read as another.
    if isinstance(R, dict) and isinstance(R.get('meta'), dict):
        prev = R['meta']
        for kx in ('X1', 'X3'):
            if kx in prev and prev[kx] != meta[kx]:
                print(f'ERROR: {out} was built with {kx}={prev[kx]} but this run has '
                      f'{kx}={meta[kx]}. Refusing to merge two engines into one file. '
                      f'Use a different --out.', flush=True)
                sys.exit(4)

    db_sub = (a.db_subsample or None) if a.db else None
    specs = [{**s, 'db': a.db, 'db_sub': db_sub, 'matched': a.matched_tuning}
             for e in exps for s in build_specs(e, tasks, seeds, ep, a.k, a.methods, beta=beta_val)]
    if not a.force:
        specs = [s for s in specs if not have(R, s['exp'], s['task'], s['variant'], seeds)]

    # 0.2 NO-OP GUARD: a run that schedules 0 cells is an ERROR, not a silent success.
    if len(specs) == 0 and not a.allow_noop:
        print(f'ERROR: 0 cells scheduled for {out} (all requested cells already present, '
              f'or an empty task/method list). This is the silent-no-op failure mode. '
              f'Pass --allow-noop only if a no-op is genuinely intended.', flush=True)
        sys.exit(2)
    R['meta'] = meta                                # 0.4: top-level engine block
    # group results as they land: R[exp][task][variant][metric] = agg over seeds
    buf = {}                                        # (exp,task,variant) -> {metric: {seed: val}}
    t0, done = time.time(), 0
    print(f'{len(specs)} cells, {a.jobs} workers '
          f'(engine X1={meta["X1"]} X3={meta["X3"]} -> {out})', flush=True)
    # fork (default): workers inherit the already-imported torch, so no per-worker re-import
    # from the FUSE-mounted env (16 concurrent cold imports thrash it -> workers stuck in D).
    # spawn is only needed to build TFBind10-Exact (crashes forked workers); pass
    # --spawn when that task is in the run and not already cached.
    import multiprocessing as _mp
    _ctx = _mp.get_context('spawn' if os.environ.get('MBO_SPAWN') else 'fork')
    with ProcessPoolExecutor(max_workers=a.jobs, mp_context=_ctx) as ex:
        futs = {ex.submit(_worker, s): s for s in specs}
        failed = 0
        for fut in as_completed(futs):
            done += 1
            try:
                r = fut.result()
            except Exception as ex:                 # one bad cell must NOT kill the run
                s = futs[fut]; failed += 1
                print(f"  CELL FAILED {s['exp']}/{s['task']}/{s['variant']} seed{s['seed']}: "
                      f"{type(ex).__name__}: {ex}", flush=True)
                continue
            if r['metrics'] is None:                # e.g. gp_grad without botorch
                continue
            key = (r['exp'], r['task'], r['variant'])
            slot = buf.setdefault(key, {})
            for mname, mval in r['metrics'].items():
                slot.setdefault(mname, {})[r['seed']] = mval
            # fold + checkpoint every 10 cells (atomic write => safe; small so a crash
            # loses little and --force-less rerun resumes from the last checkpoint)
            if done % 10 == 0 or done == len(specs):
                for (e, tk, v), metrics in buf.items():
                    node = R.setdefault(e, {}).setdefault(tk, {}).setdefault(v, {})
                    node['_engine'] = cell_engine(e, v, beta_val, mbo.K_ENS)   # per-cell stamp
                    for mname, seedmap in metrics.items():
                        node[mname] = agg([seedmap[s] for s in sorted(seedmap)])
                save(R, out)
                print(f'  {done}/{len(specs)}  [{(time.time()-t0)/60:.1f}m]', flush=True)
    save(R, out)
    require_meta(R, out)                             # self-check: the file we wrote is loadable
    print(f'done {done} cells ({failed} failed) in {(time.time()-t0)/60:.1f} min -> {os.path.abspath(out)}', flush=True)

if __name__ == '__main__':
    main()
