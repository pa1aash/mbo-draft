"""0D analysis: FF1 / FF2 / FF3 verdicts from the instrumented far-field artifacts.

Implements the decision rules of docs/PREREGISTRATION_V3.md 0D verbatim. Nothing here is
chosen after seeing the numbers: the segments, the thresholds, the DEGENERATE-CONSTANT
convention and the >=5/7 task majorities are all fixed in the pre-registration.

  python analyze_farfield_v2.py -> results/mechanism/farfield_v2/farfield_analysis.json
"""
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
FF = os.path.join(HERE, '..', 'results', 'mechanism', 'farfield_v2')
TASKS = ['Branin-2D', 'Styblinski-5D', 'Levy-8D', 'Rosenbrock-10D',
         'Rastrigin-15D', 'Ackley-20D', 'Griewank-30D']
SURR = ['ens', 'botorchgp', 'svgp']
OPT3 = ['grad', 'perturb', 'cma']
GP_CLASSES = ['botorchgp', 'svgp']

R2_LIN = 0.90        # LINEAR-GROWING needs median R2 >= this
SLOPE_GROW = 0.5     # ... and median |slope| >= this many sd_y per unit s
SLOPE_REVERT = 0.05  # REVERTING iff median |slope| < this
CONST_TOL = 0.01     # segment range below this many sd_y -> DEGENERATE-CONSTANT
MAJORITY = 5         # of 7 tasks


def fit_seg(s, mu, sd_y):
    """Least-squares mu ~ a + b*s on one segment. Returns (R2 or None, slope, range), with
    slope and range in sd_y units. R2 is None when the curve is DEGENERATE-CONSTANT: a
    reverted mean is perfectly fit by a zero-slope line and its R2 is 0/0, so R2 alone cannot
    separate 'linear growth' from 'reversion' -- that is what the slope is for."""
    mu = np.asarray(mu, float) / sd_y
    rng = float(mu.max() - mu.min())
    b, a = np.polyfit(s, mu, 1)
    if rng < CONST_TOL:
        return None, float(b), rng
    resid = mu - (a + b * s)
    sstot = float(((mu - mu.mean()) ** 2).sum())
    r2 = 1.0 - float((resid ** 2).sum()) / sstot if sstot > 0 else None
    return (None if r2 is None else float(r2)), float(b), rng


def label(med_r2, med_slope):
    if med_slope is not None and abs(med_slope) < SLOPE_REVERT:
        return 'REVERTING'
    if med_r2 is not None and med_r2 >= R2_LIN and abs(med_slope) >= SLOPE_GROW:
        return 'LINEAR-GROWING'
    return 'OTHER'


def main():
    cfg = None
    ff1, ff3 = {}, {}
    for tk in TASKS:
        p = os.path.join(FF, f'rays_{tk}.json')
        if not os.path.exists(p):
            continue
        d = json.load(open(p))
        cfg = cfg or d['config']
        s_grid = np.asarray(d['config']['s_grid'], float)
        far_m = (s_grid >= d['config']['far'][0]) & (s_grid <= d['config']['far'][1])
        near_m = (s_grid >= d['config']['near'][0]) & (s_grid <= d['config']['near'][1])
        for seg, mask, store in (('far', far_m, ff1), ('near', near_m, ff3)):
            s = s_grid[mask]
            for cls in SURR:
                r2s, slopes, nconst = [], [], 0
                for sd in d['seeds'].values():
                    if cls not in sd['curves']:
                        continue
                    for row in sd['curves'][cls]:
                        r2, b, _ = fit_seg(s, np.asarray(row, float)[mask], sd['sd_y'])
                        if r2 is None:
                            nconst += 1
                        else:
                            r2s.append(r2)
                        slopes.append(abs(b))
                if not slopes:
                    continue
                store.setdefault(tk, {})[cls] = dict(
                    median_r2=(float(np.median(r2s)) if r2s else None),
                    median_abs_slope=float(np.median(slopes)),
                    frac_constant=float(nconst / (len(r2s) + nconst)),
                    n_curves=int(len(r2s) + nconst))

    for tk, per in ff1.items():
        for cls, v in per.items():
            v['label'] = label(v['median_r2'], v['median_abs_slope'])

    ens_lin = [t for t in ff1 if ff1[t].get('ens', {}).get('label') == 'LINEAR-GROWING']
    gp_rev = {g: [t for t in ff1 if ff1[t].get(g, {}).get('label') == 'REVERTING']
              for g in GP_CLASSES}
    gp_lin = {g: [t for t in ff1 if ff1[t].get(g, {}).get('label') == 'LINEAR-GROWING']
              for g in GP_CLASSES}
    ff1_conf = (len(ens_lin) >= MAJORITY and
                all(len(gp_rev[g]) >= MAJORITY for g in GP_CLASSES))
    ff1_kill = (len(ens_lin) < MAJORITY or
                any(len(gp_lin[g]) >= MAJORITY for g in GP_CLASSES))
    ff1_verdict = 'CONFIRMED' if ff1_conf else ('KILL' if ff1_kill else 'INCONCLUSIVE')

    # ---- FF2 ----
    ff2 = {}
    gp = os.path.join(FF, 'grid_ff2.json')
    if os.path.exists(gp):
        G = json.load(open(gp))['grid']
        for tk, cells in G.items():
            for cls in SURR:
                db, fab = [], []
                for opt in OPT3:
                    c = cells.get(f'{cls}:{opt}')
                    if not c:
                        continue
                    db += list(c['d_bnd'].values())
                    fab += list(c['frac_at_bound'].values())
                if db:
                    ff2.setdefault(tk, {})[cls] = dict(
                        median_d_bnd=float(np.median(db)),
                        median_frac_at_bound=float(np.median(fab)), n=int(len(db)))
                    for opt in OPT3:
                        c = cells.get(f'{cls}:{opt}')
                        if c:
                            ff2[tk][cls][f'd_bnd_{opt}'] = float(
                                np.median(list(c['d_bnd'].values())))
    ff2_win = [t for t, per in ff2.items()
               if 'ens' in per and all(g in per for g in GP_CLASSES)
               and all(per['ens']['median_d_bnd'] < per[g]['median_d_bnd'] for g in GP_CLASSES)]
    ff2_verdict = 'CONFIRMED' if len(ff2_win) >= MAJORITY else 'KILL'

    binary = ('POSITIVE-MECHANISM' if (ff1_verdict == 'CONFIRMED' and ff2_verdict == 'CONFIRMED')
              else 'KEEP-ELIMINATION')

    out = {'config': cfg,
           'thresholds': dict(r2_lin=R2_LIN, slope_grow=SLOPE_GROW,
                              slope_revert=SLOPE_REVERT, const_tol=CONST_TOL,
                              majority=f'{MAJORITY}/7'),
           'FF1': {'per_task': ff1, 'ens_linear_growing_tasks': sorted(ens_lin),
                   'gp_reverting_tasks': {g: sorted(v) for g, v in gp_rev.items()},
                   'gp_linear_growing_tasks': {g: sorted(v) for g, v in gp_lin.items()},
                   'verdict': ff1_verdict},
           'FF2': {'per_task': ff2, 'ens_closer_tasks': sorted(ff2_win),
                   'verdict': ff2_verdict},
           'FF3': {'per_task': ff3},
           'BINARY': binary}
    p = os.path.join(FF, 'farfield_analysis.json')
    json.dump(out, open(p, 'w'), indent=1)

    print('=== FF1 far-field (s in [1.5,3.0]) : median R2 | median |slope| sd_y | label ===')
    for tk in TASKS:
        if tk not in ff1:
            continue
        row = f'{tk:16s}'
        for cls in SURR:
            v = ff1[tk].get(cls)
            if not v:
                continue
            r2 = 'n/a  ' if v['median_r2'] is None else f"{v['median_r2']:.4f}"
            row += f" | {cls:9s} {r2} {v['median_abs_slope']:8.3f} {v['label']:14s}"
        print(row)
    print(f"  ens LINEAR-GROWING on {len(ens_lin)}/7; " +
          '; '.join(f'{g} REVERTING on {len(gp_rev[g])}/7' for g in GP_CLASSES))
    print(f'  FF1 = {ff1_verdict}')
    print('=== FF2 boundary distance of x* (median over seeds x optimizers) ===')
    for tk in TASKS:
        if tk not in ff2:
            continue
        row = f'{tk:16s}'
        for cls in SURR:
            v = ff2[tk].get(cls)
            if v:
                row += f" | {cls:9s} d_bnd {v['median_d_bnd']:.5f} atbnd {v['median_frac_at_bound']:.3f}"
        print(row)
    print(f'  ens strictly closest on {len(ff2_win)}/7 -> FF2 = {ff2_verdict}')
    print('=== FF3 near-boundary (s in [0.6,1.0]), ensemble ===')
    for tk in TASKS:
        v = ff3.get(tk, {}).get('ens')
        if v:
            r2 = 'n/a' if v['median_r2'] is None else f"{v['median_r2']:.4f}"
            print(f'{tk:16s} median R2 {r2}  median |slope| {v["median_abs_slope"]:.3f}')
    print(f'BINARY = {binary}')
    print('wrote', p)


if __name__ == '__main__':
    main()
