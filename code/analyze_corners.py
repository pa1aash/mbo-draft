"""Gate analyzer for the four corners (blueprint Phase A.1.1 + Part I).

Reads the (on,on) camera grid + the three corner files and computes, per corner:
  - the 9x7 grid means table
  - eta^2 surr/opt/inter by the PAPER's own method (run05.eta2: per-task min-max normalize
    the 9 cells, task-unmodeled marginals) so the reproduction check is apples-to-apples
  - Friedman omnibus p over 9 cells x 7 tasks, and mean ranks per cell
  - per-task normalized GP-ensemble gap and the Spearman rho vs log10 |y|-scale (the
    pre-registered X1 confound test)

REPRODUCTION GATE: the (off,off) corner vs the published Table 1 (hardcoded from
main.tex), with the tolerance stated below BEFORE the look.

Writes results/corners/analysis.json and results/corners/ANALYSIS.md. Run under the venv
(imports mbo for the per-task |y|-scale).
"""
import json
import os

import numpy as np
from scipy import stats as sst

import mbo

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, '..', 'results')
CORN = os.path.join(RES, 'corners')
TASKS = ['Branin-2D', 'Styblinski-5D', 'Levy-8D', 'Rosenbrock-10D',
         'Rastrigin-15D', 'Ackley-20D', 'Griewank-30D']
SURR3 = ['ens', 'botorchgp', 'svgp']
OPT3 = ['perturb', 'grad', 'cma']          # run05 order (rows=surr, cols=opt)
CELLS = [f'{s}:{o}' for s in SURR3 for o in OPT3]

# Published Table 1 (main.tex tab:grid; 30 seeds; = pre-audit (off,off) engine).
PUBLISHED = {
    'ens:grad':        [-9.27, 6.37, -2.14, -0.28, -7.71, -3.66, -2592.0],
    'ens:perturb':     [-0.78, 33.08, -0.40, -0.12, -8.44, -6.32, -395.0],
    'ens:cma':         [-14.01, 5.21, -3.19, -0.48, -10.81, -4.31, -2613.0],
    'botorchgp:grad':  [-0.40, 27.57, -0.05, -0.09, -4.83, -0.55, -0.94],
    'botorchgp:perturb': [-0.40, 36.15, -0.24, -0.08, -8.28, -6.28, -269.0],
    'botorchgp:cma':   [-0.40, 26.65, -0.05, -0.09, -5.06, -0.59, -1.00],
    'svgp:grad':       [-0.45, 11.83, -0.08, -0.04, -2.83, -0.69, -2.11],
    'svgp:perturb':    [-0.40, 34.35, -0.25, -0.08, -8.27, -6.14, -275.0],
    'svgp:cma':        [-0.53, 11.60, -0.08, -0.04, -3.00, -0.73, -2.17],
}
PUB_ETA = dict(surr=0.37, opt=0.01, inter=0.17, friedman_p=6.1e-5)

CORNER_FILES = {
    'off_off': os.path.join(CORN, 'corner_off_off.json'),
    'on_off':  os.path.join(CORN, 'corner_on_off.json'),
    'off_on':  os.path.join(CORN, 'corner_off_on.json'),
    'on_on':   os.path.join(RES, 'results_camera.json'),      # committed camera
}
X1_ON = {'off_off': False, 'on_off': True, 'off_on': False, 'on_on': True}


def is_complete(path, min_seeds=30):
    """True only if every one of the 9x7 cells has >= min_seeds seed values. Guards against
    scoring a corner file that is still being written (run_all checkpoints every 10 cells)."""
    try:
        d = json.load(open(path))['mbo']
    except Exception:
        return False, 0
    n = 0
    for c in CELLS:
        for t in TASKS:
            m = d.get(t, {}).get(c, {}).get('p100')
            if isinstance(m, dict) and m.get('all') and len(m['all']) >= min_seeds:
                n += 1
    return n == len(CELLS) * len(TASKS), n


def grid_means(path):
    d = json.load(open(path))['mbo']
    out = {}
    for c in CELLS:
        out[c] = []
        for t in TASKS:
            node = d.get(t, {}).get(c, {})
            m = node.get('p100')
            out[c].append(float(m['mean']) if isinstance(m, dict) else None)
    return out


def grid_all(path):
    """per-cell per-task list of seed values (for SEM)."""
    d = json.load(open(path))['mbo']
    out = {}
    for c in CELLS:
        out[c] = {}
        for t in TASKS:
            node = d.get(t, {}).get(c, {})
            m = node.get('p100')
            out[c][t] = list(m['all']) if isinstance(m, dict) and m.get('all') else None
    return out


def eta2_from_means(means):
    """run05.eta2 replicated: per-task min-max normalize the 9 cells -> 3x3, task-unmodeled."""
    M, used = [], []
    for j, t in enumerate(TASKS):
        vals = [means[c][j] for c in CELLS]
        if any(v is None for v in vals):
            continue
        a = np.array(vals, float)
        lo, hi = a.min(), a.max()
        z = (a - lo) / (hi - lo) if hi > lo else np.zeros_like(a)
        M.append(z.reshape(3, 3)); used.append(t)
    M = np.array(M)
    if len(M) == 0:
        return None
    g = M.mean(); tot = ((M - g) ** 2).sum()
    om3, sm3 = M.mean(axis=(0, 1)), M.mean(axis=(0, 2))
    inter = M.mean(axis=0) - sm3[:, None] - om3[None, :] + g
    return dict(n_tasks=len(used),
                surr=float((len(used) * 3 * ((sm3 - g) ** 2).sum()) / tot),
                opt=float((len(used) * 3 * ((om3 - g) ** 2).sum()) / tot),
                inter=float((len(used) * (inter ** 2).sum()) / tot),
                surr_marg=dict(zip(SURR3, sm3.round(4).tolist())),
                opt_marg=dict(zip(OPT3, om3.round(4).tolist())))


def ranks_and_friedman(means):
    """mean ranks (1=best) per cell over tasks, and Friedman p over 9 cells x tasks."""
    cols = []
    for j, t in enumerate(TASKS):
        vals = [means[c][j] for c in CELLS]
        if any(v is None for v in vals):
            continue
        cols.append(vals)
    Mt = np.array(cols)                         # tasks x 9
    if Mt.shape[0] < 2:
        return None
    # rank per task: 1 = best (highest score)
    ranks = Mt.shape[1] + 1 - sst.rankdata(Mt, axis=1)
    mean_rank = ranks.mean(axis=0)
    try:
        fr = float(sst.friedmanchisquare(*[Mt[:, i] for i in range(Mt.shape[1])]).pvalue)
    except Exception:
        fr = float('nan')
    return dict(mean_rank=dict(zip(CELLS, mean_rank.round(3).tolist())), friedman_p=fr,
                n_tasks=int(Mt.shape[0]))


def per_task_gp_ens_gap(means):
    """per-task normalized (min-max over 9 cells) gap = mean(GP+SVGP cells) - mean(ens cells)."""
    gaps = {}
    for j, t in enumerate(TASKS):
        vals = [means[c][j] for c in CELLS]
        if any(v is None for v in vals):
            continue
        a = np.array(vals, float); lo, hi = a.min(), a.max()
        z = (a - lo) / (hi - lo) if hi > lo else np.zeros_like(a)
        zc = dict(zip(CELLS, z))
        ens = np.mean([zc[f'ens:{o}'] for o in OPT3])
        gp = np.mean([zc[f'{s}:{o}'] for s in ('botorchgp', 'svgp') for o in OPT3])
        gaps[t] = float(gp - ens)
    return gaps


def yscale():
    """log10 std of the noiseless oracle over each task's dataset."""
    out = {}
    for T in mbo.ALL_TASKS:
        t = T(); x, _ = t.data()
        out[t.name] = float(np.log10(t.oracle(x).std() + 1e-9))
    return out


def reproduction_check(off_off_means, off_off_all):
    """(off,off) vs published Table 1. Tolerance stated BEFORE the look:
      per cell: |diff| <= max(2*SEM_30seed, 0.10*|pub|) if |pub|>1; else |diff|<=0.10 abs.
      pass if >=90% (>=57/63) cells within tolerance."""
    rows, npass = [], 0
    for c in CELLS:
        for j, t in enumerate(TASKS):
            pub = PUBLISHED[c][j]
            got = off_off_means[c][j]
            if got is None:
                rows.append(dict(cell=c, task=t, pub=pub, got=None, ok=False, reason='MISSING'))
                continue
            allv = off_off_all[c][t]
            sem = (np.std(allv) / np.sqrt(len(allv))) if allv else float('inf')
            tol = max(2 * sem, 0.10 * abs(pub)) if abs(pub) > 1 else 0.10
            ok = abs(got - pub) <= tol
            npass += ok
            rows.append(dict(cell=c, task=t, pub=pub, got=round(got, 4),
                             diff=round(got - pub, 4), tol=round(tol, 4), sem=round(sem, 4), ok=bool(ok)))
    return rows, npass, len(CELLS) * len(TASKS)


def main():
    ys = yscale()
    ys_vec = [ys[t] for t in TASKS]
    report = {'yscale_log10': ys, 'published_table1': PUBLISHED, 'published_eta': PUB_ETA, 'corners': {}}

    for tag, path in CORNER_FILES.items():
        if not os.path.exists(path):
            report['corners'][tag] = {'status': 'MISSING (not yet run)'}
            continue
        done, ncell = is_complete(path)
        if not done:
            report['corners'][tag] = {'status': f'PARTIAL ({ncell}/{len(CELLS)*len(TASKS)} cells @30 seeds)'}
            continue
        means = grid_means(path)
        e = eta2_from_means(means)
        rf = ranks_and_friedman(means)
        gaps = per_task_gp_ens_gap(means)
        gvec = [gaps.get(t) for t in TASKS]
        if all(v is not None for v in gvec):
            rho, p = sst.spearmanr(gvec, ys_vec)
        else:
            rho, p = float('nan'), float('nan')
        report['corners'][tag] = dict(
            status='complete', x1_on=X1_ON[tag], eta2=e, ranks=rf,
            per_task_gap=gaps, rho_gap_vs_logyscale=float(rho), rho_p=float(p),
            grid_means={c: means[c] for c in CELLS})

    # reproduction gate -- only on a COMPLETE off_off corner
    if os.path.exists(CORNER_FILES['off_off']) and is_complete(CORNER_FILES['off_off'])[0]:
        m = grid_means(CORNER_FILES['off_off'])
        a = grid_all(CORNER_FILES['off_off'])
        rows, npass, ntot = reproduction_check(m, a)
        e = report['corners']['off_off'].get('eta2') or {}
        rf = report['corners']['off_off'].get('ranks') or {}
        eta_ok = (e and abs(e['surr'] - PUB_ETA['surr']) <= 0.05
                  and abs(e['opt'] - PUB_ETA['opt']) <= 0.05
                  and abs(e['inter'] - PUB_ETA['inter']) <= 0.05)
        fried_ok = bool(rf.get('friedman_p', 1) < 1e-3)
        cells_ok = npass >= 0.90 * ntot
        verdict = 'PASS' if (cells_ok and eta_ok and fried_ok) else 'FAIL'
        report['reproduction_gate'] = dict(
            tolerance='per-cell |diff|<=max(2*SEM,0.10*|pub|) if |pub|>1 else 0.10 abs; '
                      'eta2 within +/-0.05 each; Friedman p<1e-3; PASS if >=90% cells + eta2 + Friedman',
            cells_within_tol=npass, cells_total=ntot, cells_ok=bool(cells_ok),
            eta2_ok=bool(eta_ok), friedman_ok=fried_ok, verdict=verdict,
            eta2_off_off=e, friedman_p_off_off=rf.get('friedman_p'), cell_rows=rows)
    else:
        report['reproduction_gate'] = {'status': 'PENDING (off,off corner not yet complete)'}

    os.makedirs(CORN, exist_ok=True)
    json.dump(report, open(os.path.join(CORN, 'analysis.json'), 'w'), indent=1,
              default=lambda o: o.item() if hasattr(o, 'item') else str(o))
    _write_md(report)
    print('wrote', os.path.join(CORN, 'analysis.json'), 'and ANALYSIS.md')
    # console summary
    rg = report.get('reproduction_gate', {})
    print('REPRODUCTION GATE:', rg.get('verdict', rg.get('status')))
    for tag in ('off_off', 'on_off', 'off_on', 'on_on'):
        c = report['corners'].get(tag, {})
        if c.get('status') == 'complete':
            e = c['eta2']
            print(f"  {tag:8} X1={c['x1_on']!s:5} eta2 surr={e['surr']:.3f} opt={e['opt']:.3f} "
                  f"inter={e['inter']:.3f}  rho(gap,logY)={c['rho_gap_vs_logyscale']:+.3f} "
                  f"Friedman p={c['ranks']['friedman_p']:.2e}")
        else:
            print(f"  {tag:8} {c.get('status')}")


def _write_md(report):
    L = ['# Four-corners analysis (Part I ground truth)', '']
    rg = report.get('reproduction_gate', {})
    L += [f"## Reproduction gate: **{rg.get('verdict', rg.get('status'))}**", '',
          f"Tolerance (stated before the look): {rg.get('tolerance', 'n/a')}", '']
    if 'cells_within_tol' in rg:
        L += [f"- cells within tolerance: **{rg['cells_within_tol']}/{rg['cells_total']}** "
              f"({'OK' if rg['cells_ok'] else 'FAIL'})",
              f"- eta2 (off,off) = {rg.get('eta2_off_off')}  vs published {report['published_eta']} "
              f"-> {'OK' if rg['eta2_ok'] else 'FAIL'}",
              f"- Friedman p (off,off) = {rg.get('friedman_p_off_off')} -> "
              f"{'OK' if rg['friedman_ok'] else 'FAIL'}", '']
    L += ['## Corners', '', '| corner | X1 | eta2_surr | eta2_opt | eta2_inter | Friedman p | rho(gap,log|y|) |',
          '|---|---|---|---|---|---|---|']
    for tag in ('off_off', 'on_off', 'off_on', 'on_on'):
        c = report['corners'].get(tag, {})
        if c.get('status') == 'complete':
            e, rf = c['eta2'], c['ranks']
            L.append(f"| {tag} | {'on' if c['x1_on'] else 'off'} | {e['surr']:.3f} | {e['opt']:.3f} | "
                     f"{e['inter']:.3f} | {rf['friedman_p']:.2e} | {c['rho_gap_vs_logyscale']:+.3f} |")
        else:
            L.append(f"| {tag} | — | {c.get('status')} | | | | |")
    L += ['', '## Pre-registered X1 confound test (rho of per-task GP-ens gap vs log10 |y|-scale)',
          'X1 prediction: rho>0.6 in X1-OFF corners (off_off, off_on), rho~0 in X1-ON corners '
          '(on_off, on_on). rho unchanged across X1 => confound refuted, headline strengthened.', '']
    open(os.path.join(CORN, 'ANALYSIS.md'), 'w').write('\n'.join(L) + '\n')


if __name__ == '__main__':
    main()
