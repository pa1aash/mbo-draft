"""Four-corners driver for the X1 x X3 gate (blueprint Phase A.1.1).

The 2x2 is {X1 off, X1 on} x {X3 off, X3 on}:
  X1 = standardize the ensemble's regression targets (both GPs already z-score).
  X3 = one candidate-selection rule for every optimizer + exactly TOP proposals/cell.

The (on,on) corner is the committed results/results_camera.json and is NOT re-run here.
This driver runs the three missing corners to isolated files so the analysis can
disentangle X1 from X3:
  (off,off) -> results/corners/corner_off_off.json   [reproduction-gate target = published Table 1]
  (on ,off) -> results/corners/corner_on_off.json    [X1 alone]
  (off,on ) -> results/corners/corner_off_on.json    [X3 alone]

Only the 9 grid cells (3 surrogates x 3 optimizers) are run -- the eta^2 decomposition,
the reproduction check, and the per-task GP-ensemble gap all read from the grid; the
conformal/baseline methods are not needed for the gate and are skipped to save compute.

  python run_corners.py                 # 30 seeds, 6 workers, all 7 synthetic tasks
  CORNER_SEEDS=5 CORNER_JOBS=4 python run_corners.py    # quick smoke of the plumbing
"""
import os
import subprocess
import sys

GRID = ['ens:grad', 'ens:perturb', 'ens:cma',
        'botorchgp:grad', 'botorchgp:perturb', 'botorchgp:cma',
        'svgp:grad', 'svgp:perturb', 'svgp:cma']
HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(HERE, '..', 'results', 'corners')
os.makedirs(OUTDIR, exist_ok=True)

# (MBO_X1, MBO_X3, tag)
CORNERS = [('0', '0', 'off_off'), ('1', '0', 'on_off'), ('0', '1', 'off_on')]
SEEDS = os.environ.get('CORNER_SEEDS', '30')
JOBS = os.environ.get('CORNER_JOBS', '6')

for x1, x3, tag in CORNERS:
    out = os.path.join(OUTDIR, f'corner_{tag}.json')
    env = {**os.environ, 'MBO_X1': x1, 'MBO_X3': x3}
    cmd = [sys.executable, os.path.join(HERE, 'run_all.py'),
           '--exp', 'mbo', '--seeds', SEEDS, '--jobs', JOBS,
           '--out', out, '--methods', *GRID]
    print(f'\n===== CORNER {tag}  (MBO_X1={x1} MBO_X3={x3})  seeds={SEEDS} jobs={JOBS} '
          f'-> {os.path.relpath(out, HERE)} =====', flush=True)
    r = subprocess.run(cmd, env=env, cwd=HERE)
    print(f'===== CORNER {tag} exit={r.returncode} =====', flush=True)
    if r.returncode != 0:
        print(f'WARNING: corner {tag} exited nonzero; continuing to next corner', flush=True)
print('\nALL CORNERS DONE', flush=True)
