"""Old-vs-new diff for the supplement's tab:sfull / tab:srank / tab:cov, and the
derived quantities pinned to them (tab:cross ensemble row, synthetic Friedman).

  OLD = results/results_camera.json          (unstamped, off_off)
  NEW = results/supp_offoff/*.json           (stamped, off_off)

Emits a per-cell table plus a validation block proving the OLD side reproduces the
numbers actually printed in supplement.tex.

  python supp_diff.py
"""
import json
import os
import numpy as np
from scipy import stats as sps

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, '..', 'results')

GRID = [f'{s}:{o}' for s in ('ens', 'botorchgp', 'svgp') for o in ('grad', 'perturb', 'cma')]
SFULL = GRID + ['coms', 'cbas', 'grad_ascent']
LBL = {'ens:grad': 'Ens+Grad', 'ens:perturb': 'Ens+Pert', 'ens:cma': 'Ens+CMA',
       'botorchgp:grad': 'GP+Grad', 'botorchgp:perturb': 'GP+Pert', 'botorchgp:cma': 'GP+CMA',
       'svgp:grad': 'SVGP+Grad', 'svgp:perturb': 'SVGP+Pert', 'svgp:cma': 'SVGP+CMA',
       'coms': 'COMs', 'cbas': 'CbAS', 'grad_ascent': 'Grad.Asc.'}
TASKS = ['Branin-2D', 'Styblinski-5D', 'Levy-8D', 'Rosenbrock-10D',
         'Rastrigin-15D', 'Ackley-20D', 'Griewank-30D']

# tab:sfull exactly as printed in supplement.tex (bold marked with *)
PRINTED_SFULL = {
    'ens:grad':          [-9.27, 6.37, -2.14, -0.28, -7.71, -3.66, -2592],
    'ens:perturb':       [-0.78, 33.08, -0.40, -0.12, -8.44, -6.32, -395],
    'ens:cma':           [-14.01, 5.21, -3.19, -0.48, -10.81, -4.31, -2613],
    'botorchgp:grad':    [-0.40, 27.57, -0.05, -0.09, -4.83, -0.55, -0.94],
    'botorchgp:perturb': [-0.40, 36.15, -0.24, -0.08, -8.28, -6.28, -270],
    'botorchgp:cma':     [-0.40, 26.65, -0.05, -0.09, -5.06, -0.59, -1.00],
    'svgp:grad':         [-0.45, 11.83, -0.08, -0.04, -2.83, -0.69, -2.11],
    'svgp:perturb':      [-0.40, 34.35, -0.25, -0.08, -8.27, -6.14, -275],
    'svgp:cma':          [-0.53, 11.60, -0.08, -0.04, -3.00, -0.73, -2.17],
    'coms':              [-9.73, 8.50, -4.44, -1.31, -6.97, -4.49, -2078],
    'cbas':              [-5.64, 33.85, -0.21, -0.05, -8.02, -5.10, -276],
    'grad_ascent':       [-8.35, 3.49, -2.43, -0.31, -9.08, -3.04, -2701],
}
PRINTED_SRANK = {'botorchgp:grad': 2.57, 'svgp:grad': 3.29, 'botorchgp:cma': 3.57,
                 'svgp:cma': 4.29, 'ens:grad': 8.57, 'grad_ascent': 9.86,
                 'botorchgp:perturb': 5.71, 'svgp:perturb': 5.86, 'cbas': 6.00,
                 'ens:perturb': 8.14, 'coms': 9.43, 'ens:cma': 10.71}
# tab:cov as printed: task -> (c_in, c_ood, qhat, cf_in, cf_ood)
PRINTED_COV = {
    'Branin-2D': (0.71, 0.42, 6.2, 0.91, 0.84),
    'Styblinski-5D': (0.64, 0.00, 7.5, 0.90, 0.00),
    'Levy-8D': (0.68, 0.11, 6.0, 0.90, 0.28),
    'Rosenbrock-10D': (0.86, 0.64, 2.5, 0.90, 0.66),
    'Rastrigin-15D': (0.73, 0.72, 4.8, 0.91, 0.77),
    'Ackley-20D': (0.92, 1.00, 1.8, 0.89, 1.00),
    'Griewank-30D': (0.57, 0.00, 16.1, 0.90, 0.00),
}
COV_FIELDS = ['cov_indist@2.0', 'cov_ood@2.0', 'q_conformal', 'cov_conf_indist', 'cov_conf_ood']


def load(p):
    with open(p) as f:
        return json.load(f)


def ranks_from(mbo, methods, tasks):
    acc = {m: [] for m in methods}
    for t in tasks:
        present = {m: mbo[t][m]['p100']['mean'] for m in methods if m in mbo[t]}
        order = sorted(present, key=lambda m: -present[m])
        for i, m in enumerate(order):
            acc[m].append(i + 1)
    return {m: float(np.mean(v)) for m, v in acc.items() if v}


def friedman(mbo, methods, tasks):
    """Friedman over tasks x methods on per-task cell means (matches stats.py --cd path)."""
    M = np.array([[mbo[t][m]['p100']['mean'] for m in methods] for t in tasks])
    return sps.friedmanchisquare(*[M[:, i] for i in range(M.shape[1])]).pvalue, M


def mean_ranks(M):
    return ((-M).argsort(1).argsort(1) + 1).mean(0)


def cov_row(node, nseeds=None):
    out = []
    for f in COV_FIELDS:
        a = node['_'][f]['all']
        a = a[:nseeds] if nseeds else a
        out.append(float(np.mean(a)))
    return out


def main():
    old = load(os.path.join(RES, 'results_camera.json'))
    newg = load(os.path.join(RES, 'supp_offoff', 'grid_offoff_b2.0.json'))
    print('=' * 100)
    print('STAMP OF NEW GRID')
    print('=' * 100)
    for k, v in newg['meta'].items():
        print(f'  {k:12s} {v}')
    print(f'  -> {len(newg["meta"])} fields')

    om, nm = old['mbo'], newg['mbo']

    # ---- validation: does OLD reproduce what is printed? --------------------
    print()
    print('=' * 100)
    print('VALIDATION - does results_camera.json reproduce tab:sfull as printed?')
    print('=' * 100)
    bad = 0
    for m in SFULL:
        for j, t in enumerate(TASKS):
            got = om[t][m]['p100']['mean']
            want = PRINTED_SFULL[m][j]
            dec = 0 if abs(want) >= 100 else 2
            if round(got, dec) != round(want, dec):
                print(f'  MISMATCH {LBL[m]:11s} {t:15s} printed={want} file={got:.4f}')
                bad += 1
    print(f'  {84 - bad}/84 cells reproduce the printed table' + ('  [OK]' if bad == 0 else ''))

    orank = ranks_from(om, SFULL, TASKS)
    badr = sum(1 for m in SFULL if round(orank[m], 2) != PRINTED_SRANK[m])
    print(f'  tab:srank: {12 - badr}/12 ranks reproduce' + ('  [OK]' if badr == 0 else ''))

    # ---- tab:sfull per-cell diff -------------------------------------------
    print()
    print('=' * 100)
    print('tab:sfull  OLD (unstamped camera, off_off)  ->  NEW (stamped off_off, 30 seeds)')
    print('=' * 100)
    hdr = f'{"Method":12s}' + ''.join(f'{t.split("-")[0][:9]:>21s}' for t in TASKS)
    print(hdr)
    nexact = ntot = 0
    changed_print = []
    for m in SFULL:
        cells = []
        for t in TASKS:
            o = om[t][m]['p100']['mean']
            n = nm[t][m]['p100']['mean']
            ntot += 1
            same = (om[t][m]['p100']['all'] == nm[t][m]['p100']['all'])
            nexact += same
            dec = 0 if max(abs(o), abs(n)) >= 100 else 2
            po, pn = round(o, dec), round(n, dec)
            flag = ' ' if po == pn else '*'
            if po != pn:
                changed_print.append((LBL[m], t, po, pn))
            cells.append(f'{o:>9.2f}->{n:<9.2f}{flag}' if dec == 2 else f'{o:>9.0f}->{n:<9.0f}{flag}')
        print(f'{LBL[m]:12s}' + ''.join(f'{c:>21s}' for c in cells))
    print(f'\n  bit-exact per-seed vectors: {nexact}/{ntot}')
    print(f'  cells whose PRINTED (rounded) value changes: {len(changed_print)}/84')
    for lbl, t, po, pn in changed_print:
        print(f'    {lbl:11s} {t:15s} {po}  ->  {pn}')

    # ---- bold / best-per-task ----------------------------------------------
    print()
    print('  BOLD (best per task):')
    for t in TASKS:
        bo = max(SFULL, key=lambda m: om[t][m]['p100']['mean'])
        bn = max(SFULL, key=lambda m: nm[t][m]['p100']['mean'])
        mark = '' if bo == bn else '   <-- BOLD MOVES'
        print(f'    {t:15s} {LBL[bo]:11s} -> {LBL[bn]:11s}{mark}')

    # ---- tab:srank ----------------------------------------------------------
    nrank = ranks_from(nm, SFULL, TASKS)
    print()
    print('  tab:srank (avg rank over 7 tasks, lower better):')
    print(f'    {"Method":12s} {"old":>6s} {"new":>6s}   delta')
    for m in sorted(SFULL, key=lambda x: orank[x]):
        d = nrank[m] - orank[m]
        print(f'    {LBL[m]:12s} {orank[m]:6.2f} {nrank[m]:6.2f}   {d:+.2f}'
              + ('' if abs(d) < 1e-9 else '  *'))

    # ---- Friedman over the 9 grid cells ------------------------------------
    print()
    print('  Synthetic Friedman (9 grid cells x 7 tasks):')
    po_, Mo = friedman(om, GRID, TASKS)
    pn_, Mn = friedman(nm, GRID, TASKS)
    ro, rn = mean_ranks(Mo), mean_ranks(Mn)
    io, into = int(np.argmin(ro)), int(np.argmin(rn))
    print(f'    old p={po_:.4g}   best={LBL[GRID[io]]} mean-rank={ro[io]:.2f}')
    print(f'    new p={pn_:.4g}   best={LBL[GRID[into]]} mean-rank={rn[into]:.2f}')
    p12o, _ = friedman(om, SFULL, TASKS)
    p12n, _ = friedman(nm, SFULL, TASKS)
    print(f'    with baselines in pool: old p={p12o:.4g}  new p={p12n:.4g}')

    # ---- tab:cov ------------------------------------------------------------
    calp = os.path.join(RES, 'supp_offoff', 'calibration_off_off.json')
    if not os.path.exists(calp):
        print('\n[calibration_off_off.json not present yet - rerun after it finishes]')
        return
    newc = load(calp)
    oc, nc = old['calibration'], newc['calibration']
    print()
    print('=' * 100)
    print('tab:cov (synthetic block)  OLD (camera, 10 seeds)  ->  NEW (stamped off_off)')
    print('=' * 100)
    print(f'  NEW stamp fields: {len(newc["meta"])}   X1={newc["meta"]["X1"]} X3={newc["meta"]["X3"]}'
          f' n_seeds={newc["meta"]["n_seeds"]}')
    print()
    print('  Validation - does camera reproduce tab:cov as printed?')
    badc = 0
    for t in TASKS:
        got = cov_row(oc[t])
        for f, g, w in zip(COV_FIELDS, got, PRINTED_COV[t]):
            dec = 1 if f == 'q_conformal' else 2
            if round(g, dec) != round(w, dec):
                print(f'    MISMATCH {t:15s} {f:18s} printed={w} file={g:.4f}')
                badc += 1
    print(f'    {35 - badc}/35 entries reproduce' + ('  [OK]' if badc == 0 else ''))
    print()
    names = ['c_in', 'c_ood', 'qhat', 'cf_in', 'cf_ood']
    print(f'  {"Task":15s} ' + ''.join(f'{n:>22s}' for n in names))
    print(f'  {"":15s} ' + ''.join(f'{"old -> new10 -> new30":>22s}' for _ in names))
    for t in TASKS:
        o = cov_row(oc[t])
        n10 = cov_row(nc[t], 10)
        n30 = cov_row(nc[t])
        cells = []
        for i in range(5):
            dec = 1 if COV_FIELDS[i] == 'q_conformal' else 2
            cells.append(f'{o[i]:.{dec}f}->{n10[i]:.{dec}f}->{n30[i]:.{dec}f}')
        print(f'  {t:15s} ' + ''.join(f'{c:>22s}' for c in cells))

    # tab:cross ensemble columns = column means of tab:cov synthetic block
    print()
    print('  tab:cross ensemble row (col means of the c_in / c_ood columns above):')
    for lbl, idx in (('in-distribution (printed 0.73)', 0), ('own proposals (printed 0.41)', 1)):
        vo = np.mean([cov_row(oc[t])[idx] for t in TASKS])
        v10 = np.mean([cov_row(nc[t], 10)[idx] for t in TASKS])
        v30 = np.mean([cov_row(nc[t])[idx] for t in TASKS])
        print(f'    {lbl:32s} old={vo:.4f}  new10={v10:.4f}  new30={v30:.4f}')

    # claim check: "near zero exactly on the tasks where gradient ascent collapses"
    print()
    print('  Claim check - c_ood "near zero" tasks (<0.05):')
    for tag, get in (('old ', lambda t: cov_row(oc[t])[1]),
                     ('new ', lambda t: cov_row(nc[t])[1])):
        z = [t for t in TASKS if get(t) < 0.05]
        print(f'    {tag}: {z if z else "(none)"}')
    print('  Claim check - cf_ood == 0.00 exactly (feeds "five of the fourteen tasks"):')
    for tag, get in (('old ', lambda t: cov_row(oc[t])[4]),
                     ('new ', lambda t: cov_row(nc[t])[4])):
        z = [t for t in TASKS if round(get(t), 2) == 0.00]
        print(f'    {tag}: {len(z)} synthetic {z if z else ""}')


if __name__ == '__main__':
    main()
