"""Design-Bench four-corner analysis (Phase 5.1 reproduction + 6.1 corners + 6.3 X11 + 6.5 GFP).

Reuses the paper's OWN methods verbatim:
  - eta2 surr/opt/inter: per-task min-max normalize the 9 cells -> 3x3, task-unmodeled
    marginals (identical to analyze_corners.eta2_from_means / run05.eta2).
  - Friedman omnibus over the 9 cells x tasks, mean ranks (1=best).
  - task+seed bootstrap CIs on eta2 (identical to bootstrap_eta.bootstrap_eta2).

Reads results/db_corners/corner_<tag>_db.json (5 non-mujoco tasks) and, if present,
corner_<tag>_mujoco_db.json (Ant+DKitty). Every eta2 carries its source file's engine meta.

  python analyze_db.py            -> results/db_corners/db_analysis.json (+ console tables)
"""
import json
import os
import numpy as np
from scipy import stats as sst

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, '..', 'results')
DBC = os.path.join(RES, 'db_corners')

NONMUJOCO = ['TFBind8', 'TFBind10', 'Superconductor', 'GFP', 'UTR']
EXACT = ['TFBind8', 'TFBind10']          # exact-oracle subset (X11)
SURR3 = ['ens', 'botorchgp', 'svgp']
OPT3 = ['perturb', 'grad', 'cma']        # run05/analyze_corners order (rows=surr, cols=opt)
CELLS = [f'{s}:{o}' for s in SURR3 for o in OPT3]
CORNERS = ['off_off', 'on_off', 'off_on', 'on_on']

# Synthetic four-corner eta2 (from results/corners/analysis.json) for the mirror comparison.
SYN = {'off_off': dict(surr=0.367, opt=0.013, inter=0.165, friedman=6.09e-05),
       'on_off':  dict(surr=0.283, opt=0.036, inter=0.146, friedman=1.71e-03),
       'off_on':  dict(surr=0.450, opt=0.006, inter=0.152, friedman=4.10e-05),
       'on_on':   dict(surr=0.405, opt=0.005, inter=0.160, friedman=8.07e-04)}

DB_REF = os.path.join(RES, 'results_db.json')   # the shipped off_off engine (Phase 5.1 target)


def _load(path):
    if not os.path.exists(path):
        return None, None
    R = json.load(open(path))
    return R.get('mbo', {}), R.get('meta')


def seedvals(d, tasks):
    """d[task][cell]['p100']['all'] -> {task: {cell: [seed vals] or None}}."""
    out = {}
    for t in tasks:
        out[t] = {}
        for c in CELLS:
            m = d.get(t, {}).get(c, {}).get('p100')
            out[t][c] = list(m['all']) if isinstance(m, dict) and m.get('all') else None
    return out


def taskmeans(sv, tasks):
    """(T,9) means for tasks with all 9 cells present. Returns (array, used_tasks)."""
    rows, used = [], []
    for t in tasks:
        if all(sv[t].get(c) for c in CELLS):
            rows.append([float(np.mean(sv[t][c])) for c in CELLS]); used.append(t)
    return (np.array(rows) if rows else np.zeros((0, 9))), used


def eta2(M):
    """run05.eta2 replicated EXACTLY. M: (T,9) per-task per-cell means (CELLS order)."""
    if len(M) == 0:
        return None
    Z = []
    for row in M:
        a = np.asarray(row, float); lo, hi = a.min(), a.max()
        Z.append(((a - lo) / (hi - lo) if hi > lo else np.zeros_like(a)).reshape(3, 3))
    Z = np.array(Z)
    g = Z.mean(); tot = ((Z - g) ** 2).sum()
    if tot == 0:
        return dict(n_tasks=len(Z), surr=0.0, opt=0.0, inter=0.0)
    om3, sm3 = Z.mean(axis=(0, 1)), Z.mean(axis=(0, 2))
    inter = Z.mean(axis=0) - sm3[:, None] - om3[None, :] + g
    T = len(Z)
    return dict(n_tasks=T,
                surr=float((T * 3 * ((sm3 - g) ** 2).sum()) / tot),
                opt=float((T * 3 * ((om3 - g) ** 2).sum()) / tot),
                inter=float((T * (inter ** 2).sum()) / tot),
                surr_marg=dict(zip(SURR3, sm3.round(4).tolist())),
                opt_marg=dict(zip(OPT3, om3.round(4).tolist())))


def friedman(M):
    """Friedman p over 9 cells x tasks + mean ranks (1=best)."""
    if len(M) < 2:
        return dict(friedman_p=float('nan'), n_tasks=len(M))
    ranks = M.shape[1] + 1 - sst.rankdata(M, axis=1)
    try:
        p = float(sst.friedmanchisquare(*[M[:, i] for i in range(M.shape[1])]).pvalue)
    except Exception:
        p = float('nan')
    return dict(friedman_p=p, n_tasks=int(M.shape[0]),
                mean_rank=dict(zip(CELLS, ranks.mean(axis=0).round(3).tolist())))


def bootstrap(sv, tasks, B=10000, rng=None):
    """task+seed bootstrap CIs on eta2 (bootstrap_eta.bootstrap_eta2 replicated)."""
    rng = rng or np.random.default_rng(0)
    ok = [t for t in tasks if all(sv[t].get(c) for c in CELLS)]
    if len(ok) < 2:
        return None
    point = eta2(np.array([[float(np.mean(sv[t][c])) for c in CELLS] for t in ok]))
    draws = {'surr': [], 'opt': [], 'inter': []}
    ti = np.arange(len(ok))
    for _ in range(B):
        bt = rng.choice(ti, size=len(ok), replace=True)
        rows = []
        for j in bt:
            t = ok[j]; row = []
            for c in CELLS:
                v = np.asarray(sv[t][c]); idx = rng.integers(0, len(v), size=len(v))
                row.append(float(v[idx].mean()))
            rows.append(row)
        e = eta2(np.array(rows))
        for k in draws:
            draws[k].append(e[k])
    out = {'n_tasks': len(ok), 'B': B, 'tasks': ok, 'point': point}
    for k in draws:
        arr = np.array(draws[k])
        out[k] = dict(ci95=[float(np.percentile(arr, 2.5)), float(np.percentile(arr, 97.5))],
                      width=float(np.percentile(arr, 97.5) - np.percentile(arr, 2.5)))
    return out


def reproduction(sv_new, tasks):
    """5.1: per-cell mean of the fresh off_off run vs results_db.json (the shipped off_off).
    Tolerance stated before the look: deterministic (exact-oracle TFBind8/10) cells match to
    <1e-3 absolute; stochastic (RF-oracle) tasks to <5% relative on the per-cell 16-seed mean."""
    dref, _ = _load(DB_REF)
    verdicts = {}
    for t in tasks:
        if not all(sv_new[t].get(c) for c in CELLS):
            verdicts[t] = dict(status='UNRUNNABLE (no fresh cells)')
            continue
        det = t in EXACT
        rows, worst_abs, worst_rel = [], 0.0, 0.0
        for c in CELLS:
            new = float(np.mean(sv_new[t][c]))
            ref_m = dref.get(t, {}).get(c, {}).get('p100')
            if not isinstance(ref_m, dict):
                rows.append(dict(cell=c, new=round(new, 4), ref=None)); continue
            ref = float(ref_m['mean'])
            da = abs(new - ref); dr = da / (abs(ref) + 1e-9)
            worst_abs = max(worst_abs, da); worst_rel = max(worst_rel, dr)
            rows.append(dict(cell=c, new=round(new, 4), ref=round(ref, 4),
                             dabs=round(da, 5), drel=round(dr, 4)))
        if det:
            status = 'MATCHES' if worst_abs < 1e-3 else f'DIVERGES(max|d|={worst_abs:.4f})'
        else:
            status = 'MATCHES' if worst_rel < 0.05 else f'DIVERGES(max rel={worst_rel:.3f})'
        verdicts[t] = dict(status=status, deterministic=det,
                           worst_abs=round(worst_abs, 5), worst_rel=round(worst_rel, 4), cells=rows)
    return verdicts


def corner_report(tag, drop_gfp=False, mujoco=False):
    d, meta = _load(os.path.join(DBC, f'corner_{tag}_db.json'))
    if d is None:
        return {'status': 'MISSING'}
    tasks = [t for t in NONMUJOCO if not (drop_gfp and t == 'GFP')]
    if mujoco:
        dm, _ = _load(os.path.join(DBC, f'corner_{tag}_mujoco_db.json'))
        if dm:
            d = {**d, **dm}; tasks = tasks + ['AntMorphology', 'DKitty']
    sv = seedvals(d, tasks)
    M, used = taskmeans(sv, tasks)
    return dict(status='ok', engine_meta=meta, used_tasks=used,
                eta2=eta2(M), friedman=friedman(M),
                bootstrap=bootstrap(sv, tasks, B=10000, rng=np.random.default_rng(12345)))


def main():
    rep = {'synthetic_reference': SYN}

    # ---- 5.1 reproduction: fresh off_off vs results_db.json ----
    d_off, meta_off = _load(os.path.join(DBC, 'corner_off_off_db.json'))
    if d_off:
        sv = seedvals(d_off, NONMUJOCO)
        rep['reproduction_5_1'] = dict(engine_meta=meta_off, verdicts=reproduction(sv, NONMUJOCO))

    # ---- 6.1 four-corner eta2 (5 non-mujoco) ----
    rep['corners_5task'] = {tag: corner_report(tag) for tag in CORNERS}
    # 6.5 GFP quarantine: same corners without GFP
    rep['corners_noGFP'] = {tag: corner_report(tag, drop_gfp=True) for tag in CORNERS}
    # 6.2 with mujoco folded in (7-task), where available
    rep['corners_7task'] = {tag: corner_report(tag, mujoco=True) for tag in CORNERS}

    # ---- 6.3 X11: Friedman on the exact-oracle subset vs RF-oracle subset (on_on) ----
    x11 = {}
    for tag in CORNERS:
        d, meta = _load(os.path.join(DBC, f'corner_{tag}_db.json'))
        if d is None:
            x11[tag] = {'status': 'MISSING'}; continue
        sv = seedvals(d, NONMUJOCO)
        Me, ue = taskmeans(sv, EXACT)
        rf = [t for t in NONMUJOCO if t not in EXACT]
        Mr, ur = taskmeans(sv, rf)
        x11[tag] = dict(engine_meta=meta,
                        exact_oracle=dict(tasks=ue, friedman=friedman(Me), eta2=eta2(Me)),
                        rf_oracle=dict(tasks=ur, friedman=friedman(Mr), eta2=eta2(Mr)),
                        all5=dict(friedman=friedman(taskmeans(sv, NONMUJOCO)[0])))
    rep['x11_6_3'] = x11

    os.makedirs(DBC, exist_ok=True)
    json.dump(rep, open(os.path.join(DBC, 'db_analysis.json'), 'w'), indent=1,
              default=lambda o: o.item() if hasattr(o, 'item') else str(o))

    # ---- console ----
    print('\n=== 5.1 reproduction (fresh off_off vs results_db.json) ===')
    for t, v in rep.get('reproduction_5_1', {}).get('verdicts', {}).items():
        print(f'  {t:16} {v["status"]}')
    print('\n=== 6.1 DB four corners (5 non-mujoco), eta2 surr/opt/inter + Friedman ===')
    print(f'  {"corner":8} {"surr":>6} {"opt":>6} {"inter":>6} {"friedman":>10}   vs synthetic surr')
    for tag in CORNERS:
        c = rep['corners_5task'][tag]
        if c.get('status') == 'ok' and c.get('eta2'):
            e = c['eta2']; f = c['friedman']['friedman_p']
            print(f'  {tag:8} {e["surr"]:6.3f} {e["opt"]:6.3f} {e["inter"]:6.3f} {f:10.2e}   '
                  f'syn={SYN[tag]["surr"]:.3f} (n={e["n_tasks"]})')
        else:
            print(f'  {tag:8} {c.get("status")}')
    print('\n=== 6.3 X11 exact-oracle {TFBind8,TFBind10} vs RF-oracle subset ===')
    for tag in CORNERS:
        x = rep['x11_6_3'][tag]
        if x.get('status') == 'MISSING':
            print(f'  {tag:8} MISSING'); continue
        ex, r5 = x['exact_oracle'], x['rf_oracle']
        print(f'  {tag:8} exact: Friedman p={ex["friedman"]["friedman_p"]:.3e} '
              f'(n={ex["friedman"]["n_tasks"]})  '
              f'RF: p={r5["friedman"]["friedman_p"]:.3e} (n={r5["friedman"]["n_tasks"]})')
    print('\nwrote', os.path.join(DBC, 'db_analysis.json'))


if __name__ == '__main__':
    main()
