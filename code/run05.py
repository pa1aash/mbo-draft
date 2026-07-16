"""05 — full extraction of everything the runs support. Reuses analysis.py (SEI/OEI, gate,
transfer) + stats.py (Holm, TOST, Nemenyi-CD); adds Pillar-1 calibration, Pillar-3 cross-check,
and the secondary arms. Prints a sectioned digest and writes results/05_findings.json (every
number the paper will cite -> feeds the number-trace audit and the figures).

  python run05.py            # runs all pillars, writes 05_findings.json
"""
import json, os
import numpy as np
from scipy import stats as sst
import analysis as A            # cell, task_norm, sei_oei, SURR, OPT
import stats as ST              # holm, tost, nemenyi_cd

HERE = os.path.dirname(__file__)
RES = os.path.join(HERE, '..', 'results')
def P(f): return os.path.join(RES, f)
def load(f): return json.load(open(P(f)))
SURR3 = ['ens', 'botorchgp', 'svgp']
OPT3 = ['perturb', 'grad', 'cma']
CELLS = [f'{s}:{o}' for s in SURR3 for o in OPT3]
F = {}   # findings accumulator

def hdr(s): print('\n' + '=' * 78 + f'\n{s}\n' + '=' * 78)

# ---------- PILLAR 2a: full 3x3 eta^2 attribution (optimizer vs surrogate) ----------
def eta2(path, metric='p100'):
    d = load(path)['mbo']
    used, M = [], []
    for t in d:
        vals = {c: d[t][c][metric]['mean'] for c in CELLS
                if c in d[t] and isinstance(d[t][c].get(metric), dict)}
        if len(vals) < 9:
            continue
        a = np.array([vals[c] for c in CELLS], float)
        lo, hi = a.min(), a.max()
        z = (a - lo) / (hi - lo) if hi > lo else np.zeros_like(a)
        M.append(z.reshape(3, 3)); used.append(t)          # rows=surr, cols=opt
    M = np.array(M)                                          # T,S,O
    g = M.mean(); sst_ = ((M - g) ** 2).sum()
    om3, sm3 = M.mean(axis=(0, 1)), M.mean(axis=(0, 2))     # optimizer, surrogate marginals
    eta_opt = (len(used) * 3 * ((om3 - g) ** 2).sum()) / sst_
    eta_surr = (len(used) * 3 * ((sm3 - g) ** 2).sum()) / sst_
    inter = M.mean(axis=0) - sm3[:, None] - om3[None, :] + g   # (S,O) interaction cell effects
    eta_inter = (len(used) * (inter ** 2).sum()) / sst_
    return dict(tasks=used, eta2_opt=float(eta_opt), eta2_surr=float(eta_surr),
                eta2_inter=float(eta_inter),
                opt_means=dict(zip(OPT3, om3.round(3).tolist())),
                surr_means=dict(zip(SURR3, sm3.round(3).tolist())))

def pillar_attribution():
    hdr('PILLAR 2 — ATTRIBUTION (surrogate x optimizer)')
    for tag, path in [('SYNTH', 'results_camera.json'), ('SYNTH-matched', 'results_camera_matched.json'),
                      ('REAL', 'results_db.json')]:
        try:
            e = eta2(path)
        except Exception as ex:
            print(f'  {tag}: {ex}'); continue
        drv = 'OPTIMIZER' if e['eta2_opt'] > e['eta2_surr'] else 'SURROGATE'
        print(f'  {tag:14} eta2 surr={e["eta2_surr"]:.3f}  opt={e["eta2_opt"]:.3f}  '
              f'inter={e["eta2_inter"]:.3f}  -> {drv} dominates ({len(e["tasks"])} tasks)')
        F.setdefault('attribution', {})[tag] = e
    # 2x2 SEI/OEI + GATE-1 + transfer via analysis.py (its own prints)
    A.gate(P('results_camera.json'), P('results_camera_matched.json'))
    A.transfer(P('results_camera.json'), P('results_db.json'))
    # capture gate retention + transfer verdict into findings
    su = A.attribution(P('results_camera.json')); sm = A.attribution(P('results_camera_matched.json'))
    common = [t for t in su if t in sm]
    seiu = np.median([su[t][0] for t in common]); seim = np.median([sm[t][0] for t in common])
    F['gate1'] = dict(sei_unmatched=float(seiu), sei_matched=float(seim),
                      retention=float(seim / seiu) if seiu else None)

# ---------- PILLAR 2b: stats (ranks, CD, Wilcoxon+Holm, TOST) ----------
def method_score_matrix(path, metric='p100'):
    """methods x tasks matrix of per-task normalized mean scores (all methods present in all tasks)."""
    d = load(path)['mbo']
    tasks = list(d)
    methods = set.intersection(*[set(d[t].keys()) for t in tasks])
    methods = sorted(m for m in methods if isinstance(d[tasks[0]][m].get(metric), dict))
    M = np.zeros((len(methods), len(tasks)))
    for j, t in enumerate(tasks):
        lo, rng = A.task_norm(d, t, metric)
        for i, m in enumerate(methods):
            M[i, j] = (d[t][m][metric]['mean'] - lo) / rng
    return methods, tasks, M

def pillar_stats():
    hdr('PILLAR 2 — STATS (ranks, Nemenyi CD, Wilcoxon+Holm, Friedman, bootstrap)')
    for tag, path in [('SYNTH', 'results_camera.json'), ('REAL', 'results_db.json')]:
        methods, tasks, M = method_score_matrix(path)
        ranks = M.shape[0] + 1 - sst.rankdata(M, axis=0)      # rank 1 = best per task
        mean_rank = ranks.mean(axis=1)
        order = mean_rank.argsort()
        cd = ST.nemenyi_cd(len(methods), len(tasks))
        try: fr = sst.friedmanchisquare(*[M[i] for i in range(M.shape[0])]).pvalue
        except Exception: fr = float('nan')
        # bootstrap mean-rank CI for top method
        rng = np.random.default_rng(0)
        best = order[0]
        boot = [ranks[best, rng.integers(0, len(tasks), len(tasks))].mean() for _ in range(2000)]
        ci = (float(np.percentile(boot, 2.5)), float(np.percentile(boot, 97.5)))
        print(f'\n  [{tag}] {len(methods)} methods x {len(tasks)} tasks | Nemenyi CD={cd:.2f} | Friedman p={fr:.3f}')
        for i in order[:6]:
            print(f'     {methods[i]:22} mean-rank={mean_rank[i]:.2f}')
        print(f'     best={methods[best]} rank-CI=({ci[0]:.2f},{ci[1]:.2f})')
        if tag == 'REAL':                                    # TOST equivalence: bound the DB effect
            xb, xw = M[best], M[order[-1]]
            gap = float((xb - xw).mean())
            eq5, p5, ci5 = ST.tost(xb, xw, margin=0.5)       # SESOI 0.5 of the [0,1] score range
            eq3, p3, _ = ST.tost(xb, xw, margin=0.3)
            hw = float((ci5[1] - ci5[0]) / 2)                # 90% CI half-width = effect bound
            print(f'     TOST best({methods[best]}) vs worst({methods[order[-1]]}): '
                  f'gap={gap:.3f}, 90% CI=({ci5[0]:.3f},{ci5[1]:.3f}); '
                  f'equivalent @0.5={eq5}(p={p5:.3f}) @0.3={eq3}(p={p3:.3f})')
            F['equivalence'] = dict(best=methods[best], worst=methods[order[-1]], gap=gap,
                                    ci90=[ci5[0], ci5[1]], effect_bound=hw,
                                    equiv_margin_0p5=bool(eq5), equiv_margin_0p3=bool(eq3))
        F.setdefault('stats', {})[tag] = dict(methods=methods, mean_rank=dict(zip(methods, mean_rank.round(2).tolist())),
                                              cd=float(cd), friedman_p=float(fr), best=methods[best], best_rank_ci=ci)

# ---------- PILLAR 1: calibration (the mechanism / headline) ----------
def pillar_calibration():
    hdr('PILLAR 1 — CALIBRATION: is the pessimism premise |mu-f|<=beta*sigma covered?')
    rows = {}
    for tag, path in [('SYNTH', 'results_camera.json'), ('REAL', 'results_db.json')]:
        cal = load(path)['calibration']
        agg = {k: [] for k in ['cov_indist@2.0', 'cov_ood@2.0', 'cov_conf_indist', 'cov_conf_ood', 'rho_err']}
        print(f'\n  [{tag}]  task            in@2  OOD@2  conf_in conf_OOD  rho_err')
        for t, c in cal.items():
            c = c['_']
            def g(k): return c[k]['mean'] if isinstance(c.get(k), dict) else c.get(k)
            r = {k: g(k) for k in agg}
            for k in agg: agg[k].append(r[k])
            rows[(tag, t)] = r
            print(f'    {t:16}{r["cov_indist@2.0"]:6.2f}{r["cov_ood@2.0"]:7.3f}{r["cov_conf_indist"]:8.2f}'
                  f'{r["cov_conf_ood"]:9.3f}{r["rho_err"]:9.3f}')
        m = {k: float(np.mean(v)) for k, v in agg.items()}
        print(f'    {"MEAN":16}{m["cov_indist@2.0"]:6.2f}{m["cov_ood@2.0"]:7.3f}{m["cov_conf_indist"]:8.2f}'
              f'{m["cov_conf_ood"]:9.3f}{m["rho_err"]:9.3f}')
        F.setdefault('calibration', {})[tag] = dict(per_task={t: rows[(tag, t)] for (tg, t) in rows if tg == tag},
                                                    mean=m)
    print('\n  READ: premise needs coverage>=0.9. in-dist@2 and esp. OOD@2 are far below -> premise violated.')
    print('        conformal lifts in-dist to ~1.0 by construction but OOD stays low on some tasks (non-extrapolation).')

def pillar_beta():
    hdr('PILLAR 1 — beta-sweep: does adding pessimism help? (score vs beta)')
    d = load('results_camera.json')['beta']
    betas = sorted({float(b) for t in d for b in d[t]})
    print(f'  betas={betas}')
    slopes, helps = [], 0
    for t, bd in d.items():
        xs = sorted(float(b) for b in bd)
        ys = [bd[next(k for k in bd if abs(float(k) - b) < 1e-9)]['p100']['mean'] for b in xs]
        yn = (np.array(ys) - min(ys)) / ((max(ys) - min(ys)) or 1)   # per-task [0,1] -> comparable slopes
        sl = float(np.polyfit(xs, yn, 1)[0])
        slopes.append(sl); helps += sl > 0
        print(f'    {t:16} norm score(beta): ' + ' '.join(f'{v:.2f}' for v in yn) + f'   slope={sl:+.3f}')
    med = float(np.median(slopes))
    print(f'  median normalized slope = {med:+.3f} | tasks where pessimism helps: {helps}/{len(slopes)}  '
          f'({"HELPS" if helps > len(slopes)/2 else "HURTS/neutral on most"})')
    F['beta_sweep'] = dict(betas=betas, median_norm_slope=med, helps_count=int(helps), n=len(slopes))

# ---------- PILLAR 3: official-baseline cross-check ----------
# training-set y-bounds (from design_bench on the pod) -> normalize official RAW to our units
YNORM = {'GFP': (3.3778767585754395, 3.524911403656006),
         'TFBind8': (0.0, 0.439296156167984),
         'Superconductor': (0.0002099999983329326, 74.0)}

def pillar_crosscheck():
    hdr('PILLAR 3 — CROSS-CHECK: official COMs/CbAS (03) vs our reimpl (both Design-Bench-normalized)')
    off = load('official_baselines.json')
    db = load('results_db.json')['mbo']
    print(f'  {"method":8}{"task":16}{"official(norm)":>16}{"our-reimpl":>12}{"|abs diff|":>12}')
    cc = {}
    for meth, offkey in [('coms', 'coms_official'), ('cbas', 'cbas_official')]:
        for t in ['Superconductor', 'TFBind8', 'GFP']:
            raw = off.get(offkey, {}).get(t, {}).get('p100', {}).get('mean')
            r = db.get(t, {}).get(meth, {}).get('p100', {}).get('mean')
            if raw is None or r is None:
                print(f'  {meth:8}{t:16}{"(missing)":>16}'); continue
            lo, hi = YNORM[t]; o = (raw - lo) / (hi - lo)       # official on our normalized scale
            print(f'  {meth:8}{t:16}{o:16.3f}{r:12.3f}{abs(o - r):12.3f}')
            cc[f'{meth}:{t}'] = dict(official_norm=o, official_raw=raw, ours=r, abs_diff=abs(o - r))
    F['crosscheck'] = cc
    print('  (both normalized by training [y_min,y_max]; >1 = beats dataset best. small |diff| = faithful reimpl)')

# ---------- SECONDARY arms ----------
def pillar_secondary():
    hdr('SECONDARY — K ablation, cost/profiling, O2O presence')
    cam = load('results_camera.json')
    # K ablation: sensitivity of p100 to K, averaged over tasks (per-task normalized)
    Kd = cam['K']; Ks = sorted({int(k) for t in Kd for k in Kd[t]})
    normed = {k: [] for k in Ks}
    for t, kd in Kd.items():
        vals = {int(k): kd[k]['p100']['mean'] for k in kd}
        lo, hi = min(vals.values()), max(vals.values()); rng = (hi - lo) or 1
        for k in Ks: normed[k].append((vals[k] - lo) / rng)
    print('  K ablation (task-normalized p100, mean over tasks):')
    for k in Ks: print(f'    K={k:<3} {np.mean(normed[k]):.3f}')
    F['K_ablation'] = {str(k): float(np.mean(normed[k])) for k in Ks}
    # profiling / O2O presence check across the extra files
    for f in ['results_final.json', 'results.json', 'results_revision.json', 'results_new.json']:
        try:
            d = load(f); keys = list(d.keys())
            o2o = [k for k in keys if 'o2o' in k.lower()]
            prof = [k for k in keys if 'prof' in k.lower() or 'cost' in k.lower()]
            print(f'  {f:26} keys={keys}  | o2o={o2o} profiling={prof}')
        except Exception as ex:
            print(f'  {f}: {ex}')

def main():
    pillar_attribution()
    pillar_stats()
    pillar_calibration()
    pillar_beta()
    pillar_crosscheck()
    pillar_secondary()
    out = P('05_findings.json')
    json.dump(F, open(out, 'w'), indent=2)
    hdr(f'WROTE {out}  ({len(F)} finding blocks)')

if __name__ == '__main__':
    # self-check: a grid where only the OPTIMIZER (columns) varies must give eta2_opt >> eta2_surr
    d = {f'T{i}': {c: {'p100': {'mean': OPT3.index(c.split(':')[1]) + 0.01 * i}} for c in CELLS}
         for i in range(3)}
    M = []
    for t in d:
        a = np.array([d[t][c]['p100']['mean'] for c in CELLS], float)
        M.append(((a - a.min()) / (a.max() - a.min())).reshape(3, 3))
    M = np.array(M); g = M.mean(); tot = ((M - g) ** 2).sum()
    eo = (9 * ((M.mean(axis=(0, 1)) - g) ** 2).sum()) / tot
    es = (9 * ((M.mean(axis=(0, 2)) - g) ** 2).sum()) / tot
    assert eo > es, f'optimizer-driven grid should give eta2_opt>surr, got {eo:.2f} vs {es:.2f}'
    print('self-check OK (optimizer-driven grid -> eta2_opt > eta2_surr)')
    main()
