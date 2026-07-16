"""beta=0 grid: the 9-cell surrogate x optimizer grid at beta=0 (pure surrogate-mean
maximization, NO pessimism). Decides the mechanism confound (critique #22): if GP still
beats the ensemble at beta=0, its advantage is posterior-mean smoothness / inductive
bias, NOT sigma-calibration -> Section 5 must say so; if the ensemble catches up, the
LCB/pessimism interaction is the driver.

Reuses run_all._worker (identical sim path) so this cannot drift from the beta=2 grid.
Merge-safe + resumable: writes results_camera.json['mbo_beta0'], skips cells already done
(re-run resumes after any crash). Runs anywhere botorch is installed (local venv or pod
`main` env).

  python run_beta0.py --seeds 30 --jobs 1              # serial (reliable everywhere)
  MBO_SPAWN=1 python run_beta0.py --seeds 30 --jobs 8  # parallel on Windows (spawn)
  python run_beta0.py --seeds 30 --jobs $(nproc)       # parallel on Linux/pod (fork)
"""
import argparse, os, time
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, as_completed
import mbo
import run_all

EXP = 'mbo_beta0'
GRID = [f'{s}:{o}' for s in ('ens', 'botorchgp', 'svgp') for o in ('grad', 'perturb', 'cma')]


def _record(buf, r):
    if r['metrics'] is None:
        return
    slot = buf.setdefault((r['task'], r['variant']), {})
    for mn, mv in r['metrics'].items():
        slot.setdefault(mn, {})[r['seed']] = mv


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seeds', type=int, default=30)
    ap.add_argument('--jobs', type=int, default=1)
    ap.add_argument('--tasks', nargs='*', default=None)
    ap.add_argument('--ep', type=int, default=mbo.TRAIN_EP)
    a = ap.parse_args()
    out = run_all.out_path(False)                        # results_camera.json
    tasks = mbo.make_tasks(a.tasks)
    R = run_all.load(out)
    specs = [{'exp': 'mbo', 'task': t.name, 'variant': v, 'seed': s, 'ep': a.ep, 'k': 50,
              'beta': 0.0, 'db': False, 'db_sub': None, 'matched': False}
             for t in tasks for v in GRID for s in range(a.seeds)]
    specs = [s for s in specs
             if not run_all.have({EXP: R.get(EXP, {})}, EXP, s['task'], s['variant'], a.seeds)]
    print(f'{len(specs)} beta=0 cells to run, {a.jobs} jobs -> {out}[{EXP}]', flush=True)
    if not specs:
        print('nothing to do (all cells present)'); return

    buf, t0, done = {}, time.time(), 0

    def fold_save():
        for (tk, v), metrics in buf.items():
            node = R.setdefault(EXP, {}).setdefault(tk, {}).setdefault(v, {})
            for mn, sm in metrics.items():
                node[mn] = run_all.agg([sm[k] for k in sorted(sm)])
        run_all.save(R, out)

    if a.jobs == 1:
        for s in specs:
            _record(buf, run_all._worker(s)); done += 1
            if done % 10 == 0 or done == len(specs):
                fold_save(); print(f'  {done}/{len(specs)} [{(time.time()-t0)/60:.1f}m]', flush=True)
    else:
        ctx = mp.get_context('spawn' if (os.environ.get('MBO_SPAWN') or os.name == 'nt') else 'fork')
        with ProcessPoolExecutor(max_workers=a.jobs, mp_context=ctx) as ex:
            futs = {ex.submit(run_all._worker, s): s for s in specs}
            for f in as_completed(futs):
                done += 1
                try:
                    _record(buf, f.result())
                except Exception as e:
                    s = futs[f]; print(f"  CELL FAIL {s['task']}/{s['variant']} seed{s['seed']}: {e}", flush=True)
                if done % 10 == 0 or done == len(specs):
                    fold_save(); print(f'  {done}/{len(specs)} [{(time.time()-t0)/60:.1f}m]', flush=True)
    fold_save()
    print(f'done -> {out}[{EXP}] in {(time.time()-t0)/60:.1f}m', flush=True)


if __name__ == '__main__':
    main()
