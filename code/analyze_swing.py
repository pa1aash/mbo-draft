"""C2-SWING analyzer -- implements the decision rules of PREREGISTRATION_V3.md verbatim.

Every estimand is on the pooled/beta-invariant normalizer (analyze_v3.pooled_norm): ONE
per-task min-max fit over the pooled seed-mean cells of every condition in the comparison
set, refit inside each bootstrap resample. CIs are task+seed hierarchical bootstrap, 10,000
resamples. The SM1 screen is Bonferroni-corrected over the 4 smoothing variants (98.75%),
as registered; SM2's paired tests are at 95% as registered.

  python analyze_swing.py -> results/swing/swing_analysis.json + printed verdict block
"""
import json
import os

import numpy as np

from analyze_v3 import TASKS, boot_indices, pooled_norm

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'results', 'swing')
GRID = os.path.join(OUT, 'swing_grid.json')
NBOOT = 10000
OPT3 = ['perturb', 'grad', 'cma']
GP_SMOOTH = ['botorchgp', 'svgp']
ENS_V = ['base', 'gp0.01', 'gp0.1', 'gp1.0', 'sn']
SMOOTHERS = ['gp0.01', 'gp0.1', 'gp1.0', 'sn']
ROUGH_PAIRS = [('botorchgp_m12L', 'botorchgp'),
               ('botorchgp_lsL3', 'botorchgp'),
               ('svgp_m12', 'svgp')]
BONF = 4                                   # 4 smoothing variants screened -> 98.75% CI


def _cells(node, names, metric='p100'):
    """(T, len(names)*3, S) per-seed values. MISSING stays MISSING -> raises."""
    out = []
    for t in TASKS:
        row = []
        for n in names:
            for o in OPT3:
                v = node.get(t, {}).get(f'{n}:{o}', {}).get(metric, {}).get('all')
                if v is None:
                    raise KeyError(f'MISSING {t}/{n}:{o}/{metric}')
                row.append(v)
        out.append(row)
    return np.array(out, float)


def _ci(a, level=95.0):
    lo = (100.0 - level) / 2.0
    return [float(np.percentile(a, lo)), float(np.percentile(a, 100.0 - lo))]


def _resample(m, ti, si):
    """(T,C,S) -> resampled (T,C,S) with out[i,c,s] = m[ti[i], c, si[i,s]].
    Hierarchical: tasks resampled with replacement, then seeds within each drawn task."""
    A = m[ti]
    T, C, _ = A.shape
    return A[np.arange(T)[:, None, None], np.arange(C)[None, :, None], si[:, None, :]]


def _gap_from(cm, lo, rng, n_gp, n_ens):
    """z(GP cells).mean() - z(ens cells).mean() per task, averaged over tasks."""
    z = (cm - lo[:, None]) / rng[:, None]
    return float(z[:, :n_gp].mean() - z[:, n_gp:].mean())


def sm1(node, width, seeds_note):
    """SM1 (w=96) / SM3 (w=1024): does smoothing close the gap?

    One pooled normalizer over the comparison set {smooth GPs} U {every ens variant at this
    width}, so all variants are read in the same units and shrinkage is meaningful.
    """
    gp = _cells(node, GP_SMOOTH)                                   # (T, 6, S)
    ens = {v: _cells(node, [f'ens_{v}_w{width}']) for v in ENS_V}  # (T, 3, S) each
    lo, rng = pooled_norm([gp] + [ens[v] for v in ENS_V])
    T, S = gp.shape[0], gp.shape[2]

    def gap_of(v, gpm, ensm, lo_, rng_):
        return _gap_from(np.concatenate([gpm, ensm], axis=1), lo_, rng_, 6, 3)

    point = {v: gap_of(v, gp.mean(2), ens[v].mean(2), lo, rng) for v in ENS_V}
    base = point['base']

    # bootstrap the CLOSING difference gap(base) - gap(v), normalizer refit per resample
    diffs = {v: [] for v in SMOOTHERS}
    gaps_b = {v: [] for v in ENS_V}
    for ti, si in boot_indices(T, S, NBOOT, seed=7):
        g_b = _resample(gp, ti, si)
        e_b = {v: _resample(ens[v], ti, si) for v in ENS_V}
        lo_b, rng_b = pooled_norm([g_b] + [e_b[v] for v in ENS_V])
        gg = {v: _gap_from(np.concatenate([g_b.mean(2), e_b[v].mean(2)], axis=1),
                           lo_b, rng_b, 6, 3) for v in ENS_V}
        for v in ENS_V:
            gaps_b[v].append(gg[v])
        for v in SMOOTHERS:
            diffs[v].append(gg['base'] - gg[v])

    lvl = 100.0 - 5.0 / BONF                                       # 98.75%
    res = {}
    for v in SMOOTHERS:
        d = np.asarray(diffs[v])
        c = _ci(d, lvl)
        res[v] = dict(gap=point[v], gap_ci=_ci(np.asarray(gaps_b[v])),
                      closing_diff=float(d.mean()), closing_ci_bonf=c,
                      closes_significantly=bool(c[0] > 0),
                      shrinkage=float(1.0 - point[v] / base) if base != 0 else float('nan'))
    res['base'] = dict(gap=base, gap_ci=_ci(np.asarray(gaps_b['base'])))

    sig = [v for v in SMOOTHERS if res[v]['closes_significantly']]
    big = [v for v in sig if res[v]['shrinkage'] >= 0.50]
    winner = max(big, key=lambda v: res[v]['shrinkage']) if big else None
    verdict = ('CONFIRMED' if winner else ('PARTIAL' if sig else 'KILL'))
    return dict(width=width, variants=res, winner=winner, verdict=verdict,
                n_significant=len(sig), note=seeds_note)


def sm1_pairwise_robustness(node, width, winner):
    """POST-HOC robustness check (declared as such; not a decision rule).

    SM1's pooled normalizer spans {smooth GPs} U {all 5 ensemble variants}. Min-max is
    sensitive to its extremes: a variant that collapses becomes a task's new minimum and
    compresses every other condition's normalized spread, which could manufacture (or mask)
    shrinkage. This recomputes the winner's gap on a normalizer pooled over ONLY
    {smooth GPs, base, winner}. If the verdict flips here, the headline is a normalizer
    artifact and must be reported as such rather than as a mechanism.
    """
    if winner is None:
        return dict(status='UNTESTABLE (no SM1 winner)')
    gp = _cells(node, GP_SMOOTH)
    b = _cells(node, [f'ens_base_w{width}'])
    w = _cells(node, [f'ens_{winner}_w{width}'])
    lo, rng = pooled_norm([gp, b, w])
    gb = _gap_from(np.concatenate([gp.mean(2), b.mean(2)], axis=1), lo, rng, 6, 3)
    gw = _gap_from(np.concatenate([gp.mean(2), w.mean(2)], axis=1), lo, rng, 6, 3)
    T, S = gp.shape[0], gp.shape[2]
    d = []
    for ti, si in boot_indices(T, S, NBOOT, seed=17):
        g_b, b_b, w_b = (_resample(gp, ti, si), _resample(b, ti, si), _resample(w, ti, si))
        lo_b, rng_b = pooled_norm([g_b, b_b, w_b])
        d.append(_gap_from(np.concatenate([g_b.mean(2), b_b.mean(2)], axis=1), lo_b, rng_b, 6, 3)
                 - _gap_from(np.concatenate([g_b.mean(2), w_b.mean(2)], axis=1), lo_b, rng_b, 6, 3))
    c = _ci(np.asarray(d), 100.0 - 5.0 / BONF)
    return dict(winner=winner, gap_base=gb, gap_winner=gw,
                shrinkage=float(1.0 - gw / gb) if gb != 0 else float('nan'),
                closing_ci_bonf=c, closes_significantly=bool(c[0] > 0))


def manipulation(d):
    """Did the knobs move roughness at all? Gates SM1/SM2 with a VOID branch.

    Two instruments (on-D gradients and between-data gradients). SM2's gate passes if
    EITHER shows a >=25% rise -- the more permissive reading, so a VOID verdict cannot be
    an artifact of picking the less sensitive probe.
    """
    def pooled(R, k):
        v = [R[t][k]['mean'] for t in TASKS if k in R.get(t, {})]
        return float(np.mean(v)) if v else float('nan')

    out = {}
    for tag, R in (('D', d['roughness']), ('seg', d.get('roughness_seg', {}))):
        if not R:
            continue
        ens = {v: {w: pooled(R, f'ens_{v}_w{w}') for w in (96, 1024)} for v in ENS_V}
        gps = {k: pooled(R, k) for k in GP_SMOOTH + [r for r, _ in ROUGH_PAIRS]}
        out[tag] = dict(
            ens_roughness=ens, gp_roughness=gps,
            ens_reduction_w96={v: 1.0 - ens[v][96] / ens['base'][96] for v in SMOOTHERS},
            ens_reduction_w1024={v: 1.0 - ens[v][1024] / ens['base'][1024] for v in SMOOTHERS},
            gp_rise={r: gps[r] / gps[s] - 1.0 for r, s in ROUGH_PAIRS})

    red96 = max(out['D']['ens_reduction_w96'].values())
    red1k = max(out['D']['ens_reduction_w1024'].values())
    rise = max(max(o['gp_rise'].values()) for o in out.values())
    return dict(by_instrument=out,
                ens_reduction_w96=out['D']['ens_reduction_w96'],
                ens_reduction_w1024=out['D']['ens_reduction_w1024'],
                gp_rise={k: {tag: o['gp_rise'][k] for tag, o in out.items()}
                         for k, _ in [(r, s) for r, s in ROUGH_PAIRS]},
                sm1_manipulation_ok=bool(red96 >= 0.25),
                sm3_manipulation_ok=bool(red1k >= 0.25),
                sm2_manipulation_ok=bool(rise >= 0.25),
                sm2_best_rise=float(rise))


def sm2(node):
    """Rough GP vs its own smooth counterpart, paired by (task, seed), on p100 and c_ood."""
    names = GP_SMOOTH + [r for r, _ in ROUGH_PAIRS]
    mats = {n: _cells(node, [n]) for n in names}
    lo, rng = pooled_norm([mats[n] for n in names])
    T, S = mats[names[0]].shape[0], mats[names[0]].shape[2]

    def nscore(m, lo_, rng_):
        return ((m - lo_[:, None]) / rng_[:, None]).mean()

    cov = {n: _cells(node, [n], metric='c_ood') for n in names}
    res = {}
    for rough, smooth in ROUGH_PAIRS:
        dp = nscore(mats[rough].mean(2), lo, rng) - nscore(mats[smooth].mean(2), lo, rng)
        dc = float(cov[rough].mean() - cov[smooth].mean())
        bp, bc = [], []
        for ti, si in boot_indices(T, S, NBOOT, seed=11):
            lo_b, rng_b = pooled_norm([_resample(mats[n], ti, si) for n in names])
            bp.append(nscore(_resample(mats[rough], ti, si).mean(2), lo_b, rng_b)
                      - nscore(_resample(mats[smooth], ti, si).mean(2), lo_b, rng_b))
            bc.append(float(_resample(cov[rough], ti, si).mean()
                            - _resample(cov[smooth], ti, si).mean()))
        cip, cic = _ci(np.asarray(bp)), _ci(np.asarray(bc))
        res[rough] = dict(vs=smooth, dscore=float(dp), dscore_ci=cip,
                          score_drops=bool(cip[1] < 0),
                          dcov=dc, dcov_ci=cic, cov_drops=bool(cic[1] < 0))
    n_both = sum(1 for r in res.values() if r['score_drops'] and r['cov_drops'])
    n_score = sum(1 for r in res.values() if r['score_drops'])
    verdict = ('CONFIRMED' if n_both >= 2 else ('KILL' if n_score == 0 else 'PARTIAL'))
    return dict(pairs=res, n_both=n_both, n_score_drops=n_score, verdict=verdict)


def sm2b(node):
    """Sharpest reading of collapse: does the roughened GP still beat the base ensemble?"""
    names = [r for r, _ in ROUGH_PAIRS] + ['ens_base_w96'] + GP_SMOOTH
    mats = {n: _cells(node, [n]) for n in names}
    lo, rng = pooled_norm([mats[n] for n in names])
    z = lambda n: float((((mats[n].mean(2)) - lo[:, None]) / rng[:, None]).mean())
    b = z('ens_base_w96')
    return {n: dict(nscore=z(n), beats_base_ens=bool(z(n) > b)) for n in names}


def sm1b(node, winner, width=96):
    """Gradient-collapse half of SM1: inversion rate under the grad optimizer."""
    if winner is None:
        return dict(status='UNTESTABLE (no SM1 winner)')
    def inv(v):
        a = [node[t][f'ens_{v}_w{width}:grad']['inversion']['all'] for t in TASKS]
        return np.array(a, float)
    ib, iw = inv('base')[:, None, :], inv(winner)[:, None, :]      # (T,1,S) for _resample
    T, S = ib.shape[0], ib.shape[2]
    d = []
    for ti, si in boot_indices(T, S, NBOOT, seed=13):
        d.append(float(_resample(iw, ti, si).mean() - _resample(ib, ti, si).mean()))
    c = _ci(np.asarray(d))
    return dict(winner=winner, base_rate=float(ib.mean()), winner_rate=float(iw.mean()),
                delta=float(iw.mean() - ib.mean()), delta_ci=c,
                falls_significantly=bool(c[1] < 0))


def main():
    d = json.load(open(GRID))
    node = d['mbo']
    man = manipulation(d)

    a1 = sm1(node, 96, 'SM1')
    if not man['sm1_manipulation_ok']:
        a1['verdict'] = 'VOID (manipulation did not land: <25% roughness reduction)'
        a1['winner'] = None
    a3 = sm1(node, 1024, 'SM3')
    if a1['winner'] is None:
        a3 = dict(a3, verdict='UNTESTABLE (no SM1 winner)', winner=None)
    else:
        w = a1['winner']
        r = a3['variants'].get(w, {})
        a3['verdict'] = ('CONFIRMED' if (r.get('closes_significantly')
                                         and r.get('shrinkage', 0) >= 0.50) else 'KILL')
        a3['carried_winner'] = w
        if not man['sm3_manipulation_ok']:
            a3['verdict'] = 'VOID (manipulation did not land at w=1024)'

    a2 = sm2(node)
    if not man['sm2_manipulation_ok']:
        a2['verdict'] = 'VOID (roughened kernel did not raise roughness >=25%)'

    b1 = sm1b(node, a1['winner'])
    b2 = sm2b(node)
    rob1 = sm1_pairwise_robustness(node, 96, a1['winner'])
    rob3 = sm1_pairwise_robustness(node, 1024, a1['winner'])

    call = ('FOLD' if (a1['verdict'] == 'CONFIRMED' and a2['verdict'] == 'CONFIRMED'
                       and a3['verdict'] == 'CONFIRMED') else 'SHIP-PURE-D')
    out = dict(meta=d.get('meta'), n_shards=d.get('n_shards'),
               manipulation=man, SM1=a1, SM2=a2, SM3=a3,
               SM1b_inversion=b1, SM2b_beats_base=b2,
               robustness_pairwise_norm=dict(w96=rob1, w1024=rob3),
               BINARY_CALL=call)
    p = os.path.join(OUT, 'swing_analysis.json')
    with open(p, 'w') as f:
        json.dump(out, f, indent=2)

    print('=' * 72)
    print('C2-SWING VERDICTS (pre-registered rules, PREREGISTRATION_V3.md)')
    print('=' * 72)
    print(f'manipulation: SM1 ok={man["sm1_manipulation_ok"]} '
          f'SM2 ok={man["sm2_manipulation_ok"]} SM3 ok={man["sm3_manipulation_ok"]}')
    print(f'  ens roughness reduction w96:   {man["ens_reduction_w96"]}')
    print(f'  ens roughness reduction w1024: {man["ens_reduction_w1024"]}')
    print(f'  gp roughness rise:             {man["gp_rise"]}')
    print(f'\nSM1 ({a1["verdict"]}) base gap={a1["variants"]["base"]["gap"]:.4f} '
          f'winner={a1["winner"]}')
    for v in SMOOTHERS:
        r = a1['variants'][v]
        print(f'   {v:8s} gap={r["gap"]:.4f} shrink={r["shrinkage"]:+.3f} '
              f'closing={r["closing_diff"]:+.4f} CI98.75={r["closing_ci_bonf"]}')
    print(f'\nSM2 ({a2["verdict"]}) both-axes drops={a2["n_both"]}/3')
    for k, r in a2['pairs'].items():
        print(f'   {k:18s} vs {r["vs"]:10s} dscore={r["dscore"]:+.4f} {r["dscore_ci"]} '
              f'drop={r["score_drops"]} | dcov={r["dcov"]:+.4f} {r["dcov_ci"]} '
              f'drop={r["cov_drops"]}')
    print(f'\nSM3 ({a3["verdict"]}) carried={a3.get("carried_winner")}')
    for v in SMOOTHERS:
        r = a3['variants'][v]
        print(f'   {v:8s} gap={r["gap"]:.4f} shrink={r["shrinkage"]:+.3f} '
              f'CI98.75={r["closing_ci_bonf"]}')
    print(f'\nrobustness (pairwise normalizer, post-hoc):')
    print(f'   w96:   {rob1}')
    print(f'   w1024: {rob3}')
    print(f'\nSM1b inversion: {b1}')
    print(f'SM2b beats base ens: { {k: v["beats_base_ens"] for k, v in b2.items()} }')
    print(f'\nBINARY CALL: {call}')
    print('wrote', p)


if __name__ == '__main__':
    main()
