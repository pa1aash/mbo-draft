"""Phase 3 analysis: KB1-KB5 verdicts from the K x beta runs.

Inputs:
  results/kbeta/grid_b{B}.json   full 3x3 grid at on_on for each beta in {0,0.5,1,2,5}
  results/kbeta/kbeta_ens.json   ensemble K x beta x opt p100 + sigma
  results/kbeta/kbeta_gpsigma.json GP/SVGP sigma
  results/bootstrap_eta.json     (optional) KB5 CIs, produced by bootstrap_eta.py

Writes results/kbeta/kbeta_analysis.json and docs/GATE_KBETA.md.
"""
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, '..', 'results')
KB = os.path.join(RES, 'kbeta')
DOCS = os.path.join(HERE, '..', 'docs')
TASKS = ['Branin-2D', 'Styblinski-5D', 'Levy-8D', 'Rosenbrock-10D',
         'Rastrigin-15D', 'Ackley-20D', 'Griewank-30D']
SURR3 = ['ens', 'botorchgp', 'svgp']
OPT3 = ['perturb', 'grad', 'cma']
CELLS = [f'{s}:{o}' for s in SURR3 for o in OPT3]
BETAS = [0.0, 0.5, 1.0, 2.0, 5.0]
KS = [2, 3, 5, 10]


def _eta2(taskmeans):
    """taskmeans: (T,9) -> eta2 by analyze_corners method + surrogate/optimizer marginals."""
    M = []
    for row in taskmeans:
        a = np.asarray(row, float); lo, hi = a.min(), a.max()
        z = (a - lo) / (hi - lo) if hi > lo else np.zeros_like(a)
        M.append(z.reshape(3, 3))
    M = np.array(M); g = M.mean(); tot = ((M - g) ** 2).sum()
    om3, sm3 = M.mean(axis=(0, 1)), M.mean(axis=(0, 2)); T = len(M)
    inter = M.mean(axis=0) - sm3[:, None] - om3[None, :] + g
    return dict(surr=float((T * 3 * ((sm3 - g) ** 2).sum()) / tot),
                opt=float((T * 3 * ((om3 - g) ** 2).sum()) / tot),
                inter=float((T * (inter ** 2).sum()) / tot),
                surr_marg=dict(zip(SURR3, sm3.tolist())),
                opt_marg=dict(zip(OPT3, om3.tolist())))


def _gp_ens_gap(taskmeans):
    """mean over tasks of per-task normalized (GP+SVGP cells) - (ens cells)."""
    gaps = []
    for row in taskmeans:
        a = np.asarray(row, float); lo, hi = a.min(), a.max()
        z = (a - lo) / (hi - lo) if hi > lo else np.zeros_like(a)
        zc = dict(zip(CELLS, z))
        ens = np.mean([zc[f'ens:{o}'] for o in OPT3])
        gp = np.mean([zc[f'{s}:{o}'] for s in ('botorchgp', 'svgp') for o in OPT3])
        gaps.append(gp - ens)
    return float(np.mean(gaps))


def grid_means_from_runall(path):
    d = json.load(open(path))['mbo']
    tm = []
    for t in TASKS:
        row = [d.get(t, {}).get(c, {}).get('p100', {}).get('mean') for c in CELLS]
        if any(v is None for v in row):
            return None
        tm.append(row)
    return np.array(tm)


def ens_grid_at_K(ens, K, beta):
    """(T,3) ensemble means for opt in OPT3 at given K, beta."""
    g = ens['grid']; bkey = f'b{beta}'
    tm = []
    for t in TASKS:
        node = g.get(t, {}).get(f'K{K}', {})
        row = [node.get(f'{bkey}|{o}', {}).get('p100', {}).get('mean') for o in OPT3]
        if any(v is None for v in row):
            return None
        tm.append(row)
    return np.array(tm)


def main():
    report = {}
    # load beta grids
    grids = {}
    for b in BETAS:
        p = os.path.join(KB, f'grid_b{b}.json')
        if os.path.exists(p):
            grids[b] = grid_means_from_runall(p)
    ens = json.load(open(os.path.join(KB, 'kbeta_ens.json'))) if os.path.exists(os.path.join(KB, 'kbeta_ens.json')) else None
    gps = json.load(open(os.path.join(KB, 'kbeta_gpsigma.json'))) if os.path.exists(os.path.join(KB, 'kbeta_gpsigma.json')) else None

    # ---- per-beta full-grid eta2 + gap (KB2, KB3) ----
    per_beta = {}
    for b, tm in grids.items():
        if tm is None:
            continue
        per_beta[b] = dict(eta2=_eta2(tm), gp_ens_gap=_gp_ens_gap(tm))
    report['per_beta'] = per_beta
    if 0.0 in per_beta and 2.0 in per_beta:
        gap0, gap2 = per_beta[0.0]['gp_ens_gap'], per_beta[2.0]['gp_ens_gap']
        report['KB2'] = dict(gap_beta0=gap0, gap_beta2=gap2,
                             published_gap_beta0=0.47, published_gap_beta2=0.51,
                             collapses_at_beta0=bool(gap0 < 0.5 * gap2),
                             verdict=('gap COLLAPSES at beta0 -> mechanism is sigma-mediated '
                                      '(calibration), KB2 kill fires' if gap0 < 0.5 * gap2
                                      else 'gap PERSISTS at beta0 -> smooth-mean claim survives'))

    # ---- eta2_surr @ each K (KB1): ens rows @K + GP/SVGP rows @beta2 ----
    kb1 = {}
    if ens is not None and 2.0 in grids and grids[2.0] is not None:
        gp_svgp = grids[2.0][:, 3:]              # (T,6) botorchgp+svgp cols at beta2
        for K in KS:
            ens_rows = ens_grid_at_K(ens, K, 2.0)   # (T,3)
            if ens_rows is None:
                continue
            tm = np.concatenate([ens_rows, gp_svgp], axis=1)   # (T,9)
            e = _eta2(tm)
            kb1[K] = dict(eta2_surr=e['surr'], eta2_opt=e['opt'], eta2_inter=e['inter'],
                          ens_marg=e['surr_marg']['ens'],
                          botorchgp_marg=e['surr_marg']['botorchgp'],
                          svgp_marg=e['surr_marg']['svgp'])
        report['KB1'] = dict(by_K=kb1)
        if 2 in kb1 and 5 in kb1:
            ens2, gp2 = kb1[2]['ens_marg'], (kb1[2]['botorchgp_marg'] + kb1[2]['svgp_marg']) / 2
            report['KB1']['ens_marg_K2'] = ens2
            report['KB1']['gp_marg_K2'] = gp2
            report['KB1']['eta2_surr_K2'] = kb1[2]['eta2_surr']
            report['KB1']['eta2_surr_K5'] = kb1[5]['eta2_surr']
            report['KB1']['kill_fires'] = bool(ens2 > gp2)
            report['KB1']['verdict'] = (
                'ens marginal at K=2 EXCEEDS GP -> surrogate effect is a K artifact, headline '
                'REVERSES (KB1 kill)' if ens2 > gp2 else
                f'ens K=2 marg {ens2:.3f} still below GP {gp2:.3f}; '
                f'eta2_surr K2={kb1[2]["eta2_surr"]:.3f} vs K5={kb1[5]["eta2_surr"]:.3f}')

    # ---- sigma ratios (KB4) ----
    kb4 = {}
    if ens is not None and gps is not None:
        for t in TASKS:
            for K in KS:
                node = ens['grid'].get(t, {}).get(f'K{K}', {})
                se = node.get('sigma_train', {}).get('mean')
                gp = gps['sigma'].get(t, {}).get('botorchgp', {}).get('sigma_train')
                sv = gps['sigma'].get(t, {}).get('svgp', {}).get('sigma_train')
                if se and gp:
                    kb4[f'{t}|K{K}'] = dict(sigma_ens=se, sigma_botorchgp=gp, sigma_svgp=sv,
                                            ratio_gp_ens=gp / se if se else None,
                                            ratio_svgp_ens=(sv / se) if (sv and se) else None)
        ratios = [v['ratio_gp_ens'] for v in kb4.values() if v['ratio_gp_ens']]
        k5 = [v['ratio_gp_ens'] for k, v in kb4.items() if k.endswith('|K5') and v['ratio_gp_ens']]
        report['KB4'] = dict(per_task_K=kb4,
                             median_ratio_gp_ens=float(np.median(ratios)) if ratios else None,
                             median_ratio_gp_ens_K5=float(np.median(k5)) if k5 else None,
                             kill_fires=bool(k5 and 0.5 < np.median(k5) < 2.0),
                             verdict=('ratio ~1 at K5 -> acquisition matched, KB4 confound does '
                                      'not exist' if (k5 and 0.5 < np.median(k5) < 2.0) else
                                      'ratio differs >2x -> shared beta delivers unequal pessimism '
                                      '(fifth unmatched hyperparameter)'))

    # ---- KB5 (from bootstrap_eta.json if present) ----
    bpath = os.path.join(RES, 'bootstrap_eta.json')
    if os.path.exists(bpath):
        report['KB5_bootstrap'] = json.load(open(bpath))

    os.makedirs(KB, exist_ok=True)
    json.dump(report, open(os.path.join(KB, 'kbeta_analysis.json'), 'w'), indent=1,
              default=lambda o: o.item() if hasattr(o, 'item') else str(o))
    print('wrote kbeta_analysis.json')
    for kb in ('KB1', 'KB2', 'KB4'):
        if kb in report and 'verdict' in report[kb]:
            print(f'{kb}: {report[kb]["verdict"]}')


if __name__ == '__main__':
    main()
