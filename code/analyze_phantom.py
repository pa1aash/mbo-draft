"""Analysis for 0B (PM1/PM2/PM3), per docs/PREREGISTRATION_V3.md.

Every threshold here is transcribed from the pre-registration, which was committed before
the run launched (commit e1e185d). Nothing in this file chooses a rule after the fact.

Gap is read on the condition-invariant normalizer of docs/BETA0_RECONCILE.md: one per-task
min-max fit over the pooled seed-mean cell values of EVERY arm being compared, so the eight
surrogate rows sit on one ruler. CIs are task+seed hierarchical bootstrap, 10,000 resamples,
normalizer refit inside each resample.

  python analyze_phantom.py  -> results/mechanism/phantom_analysis.json
"""
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, '..', 'results', 'mechanism')
TASKS = ['Branin-2D', 'Styblinski-5D', 'Levy-8D', 'Rosenbrock-10D',
         'Rastrigin-15D', 'Ackley-20D', 'Griewank-30D']
OPT3 = ['perturb', 'grad', 'cma']
GP_ARMS = ['botorchgp', 'gpm_ph', 'gpm_ls', 'gpm_lssup', 'gpm_max', 'gpm_sup']
ALL_ARMS = ['ens', 'svgp'] + GP_ARMS
NBOOT = 10000
MC1_R = 0.25          # reversion-removal fraction an arm must reach for MC-1 to pass
RMSE_MAX = 1.25       # held-out ratio above which a shrinkage is reported CONFOUNDED


def ci(a):
    return [float(np.percentile(a, 2.5)), float(np.percentile(a, 97.5))]


def boot_indices(T, S, nboot, seed=0):
    r = np.random.RandomState(seed)
    for _ in range(nboot):
        yield r.randint(0, T, T), r.randint(0, S, (T, S))


# -------------------------------------------------------------------- loading
def per_seed(d, arm, opt, group, field):
    """-> (T, S). Refuses to pair anything ragged: within a task every cell is appended
    once per completed (task, seed), so equal length is what makes index i the same seed
    in every cell. A short cell means a MISSING run and pairing is not attempted."""
    out = []
    for t in TASKS:
        node = d['mbo'][t][f'{arm}:{opt}']
        v = node[group][field]['all'] if group else node[field]['all']
        out.append(v)
    n = {len(v) for v in out}
    if len(n) != 1:
        raise KeyError(f'ragged seed axis for {arm}:{opt}/{group}/{field}: {sorted(n)}')
    return np.array(out, float)


def scalar_per_seed(d, block, arm, field):
    out = []
    for t in TASKS:
        node = d[block][t].get(arm)
        if node is None or field not in node:
            return None
        out.append(node[field]['all'])
    return np.array(out, float)


# ------------------------------------------------------------------ PM1
def paired_diff(d, field, arm_a, arms_b, group='star'):
    """mean over (task, optimizer, seed) of arm_a minus the mean of arms_b, with the
    task+seed hierarchical bootstrap. Pairing is at (task, seed, optimizer)."""
    A = np.stack([per_seed(d, arm_a, o, group, field) for o in OPT3])          # (O,T,S)
    B = np.mean([np.stack([per_seed(d, b, o, group, field) for o in OPT3])
                 for b in arms_b], axis=0)                                    # (O,T,S)
    D = (A - B).mean(axis=0)                                                  # (T,S)
    T, S = D.shape
    point = float(D.mean())
    draws = [float(np.mean([D[t, si[k]].mean() for k, t in enumerate(ti)]))
             for ti, si in boot_indices(T, S, NBOOT)]
    return dict(point=point, ci=ci(draws),
                per_task={TASKS[i]: float(D[i].mean()) for i in range(T)},
                a_mean=float(A.mean()), b_mean=float(B.mean()))


# ------------------------------------------------------------------ gap
def gap_matrix(d):
    """-> (T, A, O, S) p100, arms in ALL_ARMS order."""
    return np.array([[[per_seed(d, a, o, None, 'p100')[i] for o in OPT3]
                      for a in ALL_ARMS] for i in range(len(TASKS))])


def _gaps_from(cm, pool=None):
    """cm: (T, A, O) seed-mean p100. -> {arm: gap vs ens} on a per-task min-max fit over
    the pooled cell means of `pool` (default: every arm, the registered ruler)."""
    idx = [ALL_ARMS.index(a) for a in (pool or ALL_ARMS)]
    flat = cm[:, idx, :].reshape(len(cm), -1)
    lo = flat.min(axis=1)
    rng = flat.max(axis=1) - lo
    rng[rng == 0] = 1.0
    z = (cm - lo[:, None, None]) / rng[:, None, None]
    ei = ALL_ARMS.index('ens')
    return {a: float(np.mean(z[:, ALL_ARMS.index(a), :].mean(axis=1) - z[:, ei, :].mean(axis=1)))
            for a in ALL_ARMS}


def gap_analysis(M):
    """Registered ruler: one per-task min-max over ALL eight arms. Reported alongside is a
    per-comparison ruler pooling only {ens, botorchgp, X} for each arm X. The registered
    ruler is the primary; the second exists because an arm whose scores collapse stretches
    the shared range and compresses every other arm's gap toward zero, which would flatter
    a shrinkage claim. If the two disagree on a verdict, that is reported, not resolved."""
    T, A, O, S = M.shape
    point = _gaps_from(M.mean(axis=3))
    pair_pool = {a: ['ens', 'botorchgp', a] for a in GP_ARMS if a != 'botorchgp'}
    point_pair = {a: _gaps_from(M.mean(axis=3), pool=p) for a, p in pair_pool.items()}
    draws = {a: [] for a in ALL_ARMS}
    shrink = {a: [] for a in GP_ARMS}
    shrink_pair = {a: [] for a in pair_pool}
    for ti, si in boot_indices(T, S, NBOOT):
        cm = np.array([M[t][:, :, si[k]].mean(axis=2) for k, t in enumerate(ti)])
        g = _gaps_from(cm)
        for a in ALL_ARMS:
            draws[a].append(g[a])
        for a in GP_ARMS:
            shrink[a].append(g['botorchgp'] - g[a])
        for a, p in pair_pool.items():
            gp_ = _gaps_from(cm, pool=p)
            shrink_pair[a].append(gp_['botorchgp'] - gp_[a])
    return dict(gap={a: dict(point=point[a], ci=ci(draws[a])) for a in ALL_ARMS},
                shrinkage={a: dict(point=point['botorchgp'] - point[a], ci=ci(shrink[a]))
                           for a in GP_ARMS},
                shrinkage_pairwise_ruler={
                    a: dict(point=point_pair[a]['botorchgp'] - point_pair[a][a],
                            ci=ci(shrink_pair[a])) for a in pair_pool})


# ------------------------------------------------------------------ MC-1
def mc1(d):
    """R = (FF(arm) - FF(incumbent)) / (c_arm - FF(incumbent)), pooled task+seed."""
    ff0 = scalar_per_seed(d, 'farfield', 'botorchgp', 'ff')
    out = {}
    for a in GP_ARMS:
        ffa = scalar_per_seed(d, 'farfield', a, 'ff')
        ca = scalar_per_seed(d, 'farfield', a, 'c')
        if ca is None:
            out[a] = dict(defined=False,
                          note='no prior-mean constant of its own; FF reported, R undefined',
                          ff=float(ffa.mean()), ff_incumbent=float(ff0.mean()))
            continue
        R = (ffa - ff0) / (ca - ff0)
        T, S = R.shape
        draws = [float(np.mean([R[t, si[k]].mean() for k, t in enumerate(ti)]))
                 for ti, si in boot_indices(T, S, NBOOT)]
        c = ci(draws)
        out[a] = dict(defined=True, R=float(R.mean()), ci=c,
                      passes=bool(R.mean() >= MC1_R and c[0] > MC1_R),
                      ff=float(ffa.mean()), ff_incumbent=float(ff0.mean()),
                      c=float(ca.mean()),
                      per_task={TASKS[i]: float(R[i].mean()) for i in range(len(TASKS))})
    return out


# ------------------------------------------------------------------ held-out
def heldout(d):
    r0 = scalar_per_seed(d, 'heldout', 'botorchgp', 'norm_rmse')
    out = {}
    for a in GP_ARMS + ['ens']:
        ra = scalar_per_seed(d, 'heldout', a, 'norm_rmse')
        ratio = ra / np.maximum(r0, 1e-12)
        T, S = ratio.shape
        draws = [float(np.mean([ratio[t, si[k]].mean() for k, t in enumerate(ti)]))
                 for ti, si in boot_indices(T, S, NBOOT)]
        c = ci(draws)
        out[a] = dict(norm_rmse=float(ra.mean()), ratio_to_incumbent=float(ratio.mean()),
                      ci=c, degraded=bool(ratio.mean() > RMSE_MAX and c[0] > 1.0))
    return out


# ------------------------------------------------------------------ PM3 landscape
def landscape(d):
    """The joint (Dhat, Z, I) structure PM3 asks for: per-arm marginals, and the pooled
    relation between how far out a returned optimum sits and what it is actually worth.
    Deciles are cut on the pooled Dhat so every arm is read against one set of bins."""
    from scipy.stats import spearmanr
    rows = {}
    for a in ALL_ARMS:
        dh = np.concatenate([per_seed(d, a, o, 'star', 'dhat').ravel() for o in OPT3])
        z = np.concatenate([per_seed(d, a, o, 'star', 'z').ravel() for o in OPT3])
        inf = np.concatenate([per_seed(d, a, o, 'star', 'infl').ravel() for o in OPT3])
        rows[a] = dict(dhat=dh, z=z, infl=inf)
    alld = np.concatenate([r['dhat'] for r in rows.values()])
    edges = np.percentile(alld, np.arange(0, 101, 10))
    out = {}
    for a, r in rows.items():
        b = np.clip(np.digitize(r['dhat'], edges[1:-1]), 0, 9)
        out[a] = dict(
            n=int(len(r['dhat'])),
            dhat=_pct(r['dhat']), z=_pct(r['z']), infl=_pct(r['infl']),
            spearman_dhat_vs_z=float(spearmanr(r['dhat'], r['z']).statistic),
            spearman_dhat_vs_infl=float(spearmanr(r['dhat'], r['infl']).statistic),
            by_dhat_decile=[dict(decile=i + 1, n=int((b == i).sum()),
                                 dhat=float(r['dhat'][b == i].mean()),
                                 z=float(r['z'][b == i].mean()),
                                 infl=float(r['infl'][b == i].mean()))
                            for i in range(10) if (b == i).sum()])
    pooled_dh = np.concatenate([r['dhat'] for r in rows.values()])
    pooled_z = np.concatenate([r['z'] for r in rows.values()])
    pooled_i = np.concatenate([r['infl'] for r in rows.values()])
    return dict(decile_edges=[float(e) for e in edges], by_arm=out,
                pooled_spearman_dhat_vs_z=float(spearmanr(pooled_dh, pooled_z).statistic),
                pooled_spearman_dhat_vs_infl=float(spearmanr(pooled_dh, pooled_i).statistic))


def matched_bins(d, arm_a='ens', arm_b='botorchgp', nbin=5):
    """The comparison PM1's marginals cannot make: within bins of distance-to-D, is the
    ensemble's returned optimum worth less than the GP's? Bins are cut on the pooled
    distances of both arms, so each bin holds points that sit equally far off-support."""
    def cat(a, f):
        return np.concatenate([per_seed(d, a, o, 'star', f).ravel() for o in OPT3])
    A = {f: cat(arm_a, f) for f in ('dhat', 'z', 'infl')}
    B = {f: cat(arm_b, f) for f in ('dhat', 'z', 'infl')}
    edges = np.percentile(np.concatenate([A['dhat'], B['dhat']]),
                          np.linspace(0, 100, nbin + 1))
    out = []
    for i in range(nbin):
        lo, hi = edges[i], edges[i + 1]
        ma = (A['dhat'] >= lo) & (A['dhat'] <= hi)
        mb = (B['dhat'] >= lo) & (B['dhat'] <= hi)
        if ma.sum() < 10 or mb.sum() < 10:
            continue
        out.append(dict(lo=float(lo), hi=float(hi), n_a=int(ma.sum()), n_b=int(mb.sum()),
                        z_a=float(A['z'][ma].mean()), z_b=float(B['z'][mb].mean()),
                        z_diff=float(A['z'][ma].mean() - B['z'][mb].mean()),
                        infl_a=float(A['infl'][ma].mean()),
                        infl_b=float(B['infl'][mb].mean())))
    return dict(arm_a=arm_a, arm_b=arm_b, bins=out,
                n_bins_a_worse=int(sum(b['z_diff'] < 0 for b in out)), n_bins=len(out))


def _pct(a):
    return dict(mean=float(a.mean()), sd=float(a.std()),
                p10=float(np.percentile(a, 10)), p50=float(np.percentile(a, 50)),
                p90=float(np.percentile(a, 90)))


# ------------------------------------------------------------------ verdicts
def main():
    p = os.path.join(RES, 'phantom_maxima.json')
    d = json.load(open(p))
    S = len(d['mbo'][TASKS[0]]['ens:grad']['p100']['all'])

    # ---- PM3 first: completeness gates everything downstream ----
    missing = [f'{t}/{a}:{o}' for t in TASKS for a in ALL_ARMS for o in OPT3
               if f'{a}:{o}' not in d['mbo'].get(t, {})]
    ragged = []
    for t in TASKS:
        for a in ALL_ARMS:
            for o in OPT3:
                n = d['mbo'].get(t, {}).get(f'{a}:{o}', {}).get('p100', {}).get('all')
                if n is not None and len(n) != S:
                    ragged.append(f'{t}/{a}:{o}={len(n)}')
    pm3 = dict(n_seeds=S, n_tasks=len(TASKS), n_arms=len(ALL_ARMS), n_optimizers=len(OPT3),
               cells_expected=len(TASKS) * len(ALL_ARMS) * len(OPT3),
               missing=missing, ragged=ragged,
               verdict=('PM3 DELIVERED' if not missing and not ragged else
                        'PM3 NOT DELIVERED — %d missing, %d ragged' % (len(missing), len(ragged))))

    rep = dict(engine=d['meta'], config=d['config'], gp_arm_spec=d['gp_arm_spec'],
               nboot=NBOOT, PM3=pm3)
    if missing or ragged:
        rep['PM1'] = rep['PM2'] = dict(verdict='NOT EVALUATED — PM3 incomplete')
        rep['CALL'] = 'KEEP-ELIMINATION — the run is incomplete; no verdict is claimed'
        json.dump(rep, open(os.path.join(RES, 'phantom_analysis.json'), 'w'), indent=2)
        print(rep['CALL'])
        return

    # ---- PM1 ----
    dh = paired_diff(d, 'dhat', 'ens', ['botorchgp'])
    inf = paired_diff(d, 'infl', 'ens', ['botorchgp'])
    dh_ex = dh['ci'][0] > 0
    inf_ex = inf['ci'][0] > 0
    if dh_ex and inf_ex:
        v1 = ('PM1 CONFIRMED — the ensemble\'s returned optima sit further from D AND carry '
              'larger inflation than the GP\'s; both 95% CIs exclude 0')
    elif not dh_ex and not inf_ex:
        v1 = ('PM1 KILL FIRES — ensemble and GP optima sit at the same distance-to-D with the '
              'same inflation; the phantom off-support maxima account is wrong and C2 stays a '
              'pure elimination')
    else:
        v1 = ('PM1 PARTIAL — only the %s limb holds; per the pre-registration this does not '
              'count as PM1 holding' % ('distance' if dh_ex else 'inflation'))
    rep['PM1'] = dict(distance=dh, inflation=inf,
                      secondary_pooled_gp=dict(
                          distance=paired_diff(d, 'dhat', 'ens', ['botorchgp', 'svgp']),
                          inflation=paired_diff(d, 'infl', 'ens', ['botorchgp', 'svgp'])),
                      robustness_argmax_lcb=dict(
                          distance=paired_diff(d, 'dhat', 'ens', ['botorchgp'], 'star_lcb'),
                          inflation=paired_diff(d, 'infl', 'ens', ['botorchgp'], 'star_lcb')),
                      oracle_value=paired_diff(d, 'z', 'ens', ['botorchgp']),
                      verdict=v1)

    # ---- PM2 ----
    G = gap_analysis(gap_matrix(d))
    M = mc1(d)
    H = heldout(d)
    arms = {}
    for a in [x for x in GP_ARMS if x != 'botorchgp']:
        sh = G['shrinkage'][a]
        mv = M[a]
        mv_pass = mv.get('passes', False)
        moved = dict(distance=paired_diff(d, 'dhat', a, ['botorchgp']),
                     inflation=paired_diff(d, 'infl', a, ['botorchgp']))
        moved_ok = moved['distance']['ci'][0] > 0 or moved['inflation']['ci'][0] > 0
        shrank = sh['ci'][0] > 0
        if not mv.get('defined', False):
            v = ('CONTROL — no prior constant of its own; reported to separate lengthscale '
                 'from prior mean, not to test PM2')
        elif not mv_pass:
            v = ('PM2 UNINFORMATIVE on this arm — MC-1 fails (R=%.3f, CI %s, threshold %.2f): '
                 'the knob did not move the far-field mean it was built to move' %
                 (mv['R'], mv['ci'], MC1_R))
        elif shrank and H[a]['degraded']:
            v = ('PM2 CONFOUNDED on this arm — the gap shrinks but held-out normRMSE is %.2fx '
                 'the incumbent GP\'s; a surrogate that got worse in-distribution is not '
                 'evidence about reversion' % H[a]['ratio_to_incumbent'])
        elif shrank and moved_ok:
            v = 'PM2 CONFIRMED on this arm'
        elif shrank:
            v = ('PM2 PARTIAL on this arm — the gap shrinks but the arm\'s optima do not move '
                 'off-support, so the mechanistic intermediate is absent')
        else:
            v = ('PM2 KILL FIRES on this arm — MC-1 passes and the reverted and non-reverted '
                 'GP perform identically (shrinkage CI covers 0); prior reversion is not the '
                 'mechanism')
        shp = G['shrinkage_pairwise_ruler'][a]
        if v.startswith('PM2 CONFIRMED') and not shp['ci'][0] > 0:
            v += (' — but the shrinkage does not survive the per-comparison ruler '
                  '(%.3f, CI %s), so the registered ruler is carrying the result' %
                  (shp['point'], [round(x, 3) for x in shp['ci']]))
        arms[a] = dict(gap=G['gap'][a], shrinkage=sh, shrinkage_pairwise_ruler=shp,
                       mc1=mv, heldout=H[a], optima_moved=moved, verdict=v)
    arms['botorchgp'] = dict(gap=G['gap']['botorchgp'], mc1=M['botorchgp'],
                             heldout=H['botorchgp'], verdict='INCUMBENT — the reference arm')
    primary = arms['gpm_sup']['verdict']
    rep['PM2'] = dict(primary_arm='gpm_sup', by_arm=arms,
                      gap_ens_reference=G['gap']['ens'], gap_svgp=G['gap']['svgp'],
                      heldout_ens=H['ens'],
                      verdict=primary.replace(' on this arm', '') if 'PM2' in primary else primary)

    rep['PM3']['landscape'] = landscape(d)
    rep['PM3']['distance_matched'] = matched_bins(d)

    # ---- the binary call ----
    pm1_ok = v1.startswith('PM1 CONFIRMED')
    pm2_ok = rep['PM2']['verdict'].startswith('PM2 CONFIRMED')
    rep['CALL'] = ('UPGRADE — C2 becomes a positive mechanism: the GP\'s prior-mean reversion '
                   'suppresses the off-support phantom optima the ensemble\'s free '
                   'extrapolation admits'
                   if pm1_ok and pm2_ok else
                   'KEEP-ELIMINATION — %s; %s. The diagnosis ships unchanged.'
                   % (v1.split(' — ')[0], rep['PM2']['verdict'].split(' — ')[0]))

    json.dump(rep, open(os.path.join(RES, 'phantom_analysis.json'), 'w'), indent=2)
    print(pm3['verdict'])
    print(v1)
    print(rep['PM2']['verdict'])
    print()
    print(rep['CALL'])


if __name__ == '__main__':
    main()
