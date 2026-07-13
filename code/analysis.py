"""Attribution analysis for the AAAI-27 paper: the SEI/OEI index, the fixed-optimizer
gap collapse, the GATE-1 verdict (does the surrogate effect survive matched tuning?),
and the synthetic->real transfer test. All post-hoc over the factorial JSONs from
run_all.py --exp mbo [--matched-tuning].

  python analysis.py                                                  # SEI/OEI + gap on synthetic
  python analysis.py --results ../results/results_db.json             # on real Design-Bench
  python analysis.py --gate ../results/results_camera.json ../results/results_camera_matched.json
  python analysis.py --transfer ../results/results_camera.json ../results/results_db.json

Definitions (per task, over the surrogate x optimizer grid):
  SEI (Surrogate Effect Index) = max_optimizer |mean(S2,O) - mean(S1,O)|   (surrogate main effect)
  OEI (Optimizer Effect Index) = max_surrogate |mean(S,O2) - mean(S,O1)|   (optimizer main effect)
  Reported in per-task min-max-normalized units so effects are comparable across tasks.
"""
import argparse, json, os
import numpy as np

HERE = os.path.dirname(__file__)
DEFAULT = os.path.join(HERE, '..', 'results', 'results_camera.json')
SURR = ('ens', 'botorchgp')        # S1, S2 primary contrast (ensemble vs GP)
OPT = ('grad', 'perturb')          # O1, O2 primary contrast

def cell(mbo, task, s, o, metric='p100'):
    """mean metric of grid cell surrogate:optimizer, or None if absent."""
    try: return mbo[task][f'{s}:{o}'][metric]['mean']
    except (KeyError, TypeError): return None

def task_norm(mbo, task, metric='p100'):
    """min-max scale over ALL present grid cells for this task -> comparable [0,1] units."""
    vals = [v[metric]['mean'] for k, v in mbo[task].items()
            if ':' in k and isinstance(v.get(metric), dict) and 'mean' in v[metric]]
    lo, hi = (min(vals), max(vals)) if vals else (0.0, 1.0)
    return lo, (hi - lo) or 1.0

def sei_oei(mbo, task, surr=SURR, opt=OPT, metric='p100'):
    """Return (SEI, OEI, interaction) in normalized units, or None if the 2x2 is incomplete."""
    lo, rng = task_norm(mbo, task, metric)
    def n(s, o):
        v = cell(mbo, task, s, o, metric)
        return None if v is None else (v - lo) / rng
    g = {(s, o): n(s, o) for s in surr for o in opt}
    if any(v is None for v in g.values()): return None
    sei = max(abs(g[(surr[1], o)] - g[(surr[0], o)]) for o in opt)          # surrogate effect
    oei = max(abs(g[(s, opt[1])] - g[(s, opt[0])]) for s in surr)           # optimizer effect
    inter = abs((g[(surr[1], opt[1])] - g[(surr[0], opt[1])]) -
                (g[(surr[1], opt[0])] - g[(surr[0], opt[0])]))              # interaction
    return sei, oei, inter

def attribution(path, surr=SURR, opt=OPT, metric='p100', label=''):
    mbo = json.load(open(path))['mbo']
    tasks = list(mbo)
    print(f'\n=== SEI/OEI attribution {label}({os.path.basename(path)}) — {surr[0]} vs {surr[1]}, {opt[0]} vs {opt[1]} ===')
    print(f"{'task':<16}{'SEI(surrogate)':>16}{'OEI(optimizer)':>16}{'interaction':>14}{'driver':>10}")
    rows = {}
    for t in tasks:
        r = sei_oei(mbo, t, surr, opt, metric)
        if r is None:
            print(f'{t:<16}{"(incomplete 2x2)":>46}'); continue
        sei, oei, inter = r
        driver = 'OPTIMIZER' if oei > sei else 'surrogate'
        rows[t] = r
        print(f'{t:<16}{sei:>16.3f}{oei:>16.3f}{inter:>14.3f}{driver:>10}')
    if rows:
        seis = [v[0] for v in rows.values()]; oeis = [v[1] for v in rows.values()]
        print(f'  median SEI={np.median(seis):.3f}  median OEI={np.median(oeis):.3f}  '
              f'-> {"optimizer pairing dominates" if np.median(oeis) > np.median(seis) else "surrogate class dominates"}')
    return rows

def fixed_optimizer_gap(path, metric='p100'):
    """The headline collapse: GP-minus-ensemble gap at each FIXED optimizer (normalized)."""
    mbo = json.load(open(path))['mbo']
    print(f'\n=== Fixed-optimizer GP-vs-ensemble gap ({os.path.basename(path)}) ===')
    print(f"{'optimizer':<12}{'median |GP-ens|':>18}{'tasks':>8}")
    for o in ('grad', 'perturb', 'cma'):
        gaps = []
        for t in mbo:
            lo, rng = task_norm(mbo, t, metric)
            ce, cg = cell(mbo, t, 'ens', o, metric), cell(mbo, t, 'botorchgp', o, metric)
            if ce is not None and cg is not None:
                gaps.append(abs(cg - ce) / rng)
        if gaps:
            print(f'{o:<12}{np.median(gaps):>18.3f}{len(gaps):>8}')
    print('  (a large gap at grad collapsing toward ~0 at perturb = the confound: the '
          'surrogate "advantage" is really an optimizer-pairing artifact)')

def gate(unmatched, matched, metric='p100'):
    """GATE-1: does the surrogate effect (SEI) survive matched tuning? If SEI collapses
    under matched, the headline reframes to 'a tuning-budget artifact'."""
    print('\n########## GATE-1: matched-tuning control ##########')
    u = attribution(unmatched, label='UNMATCHED ')
    m = attribution(matched, label='MATCHED ')
    common = [t for t in u if t in m]
    if not common:
        print('  no common tasks between the two arms'); return
    su = np.median([u[t][0] for t in common]); sm = np.median([m[t][0] for t in common])
    print(f'\n  median SEI  unmatched={su:.3f}  ->  matched={sm:.3f}   '
          f'(retention {sm/su:.0%})' if su else '')
    verdict = ('SURVIVES: surrogate-class effect is real, not a tuning artifact' if su and sm/su > 0.5
               else 'DOES NOT SURVIVE: the surrogate effect was largely a tuning-budget artifact '
                    '-> REFRAME headline to "reported surrogate-class gains are a fair-tuning artifact"')
    print(f'  VERDICT: {verdict}')

def transfer(synth, real, metric='p100'):
    """Synthetic->real: does the per-task driver (SEI vs OEI) and the best surrogate flip?"""
    print('\n########## Synthetic -> Real transfer ##########')
    su = attribution(synth, label='SYNTH ')
    re = attribution(real, label='REAL ')
    sd = 'optimizer' if (su and np.median([v[1] for v in su.values()]) > np.median([v[0] for v in su.values()])) else 'surrogate'
    rd = 'optimizer' if (re and np.median([v[1] for v in re.values()]) > np.median([v[0] for v in re.values()])) else 'surrogate'
    print(f'\n  dominant driver: synthetic={sd}  real={rd}  '
          f'-> {"CONSISTENT" if sd == rd else "REVERSES synthetic->real (the transfer-failure finding)"}')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--results', default=DEFAULT)
    ap.add_argument('--gate', nargs=2, metavar=('UNMATCHED', 'MATCHED'))
    ap.add_argument('--transfer', nargs=2, metavar=('SYNTH', 'REAL'))
    ap.add_argument('--metric', default='p100')
    a = ap.parse_args()
    if a.gate:
        gate(*a.gate, metric=a.metric)
    elif a.transfer:
        transfer(*a.transfer, metric=a.metric)
    else:
        attribution(a.results, metric=a.metric)
        fixed_optimizer_gap(a.results, metric=a.metric)

if __name__ == '__main__':
    # self-check: a synthetic 2x2 where the OPTIMIZER drives the outcome (rows differ by
    # optimizer, not surrogate) must yield OEI > SEI.
    fake = {'mbo': {'T': {
        'ens:grad':      {'p100': {'mean': 0.0}},
        'ens:perturb':   {'p100': {'mean': 1.0}},
        'botorchgp:grad':    {'p100': {'mean': 0.05}},
        'botorchgp:perturb': {'p100': {'mean': 1.05}}}}}
    import tempfile
    p = os.path.join(tempfile.gettempdir(), '_ana_selfcheck.json'); json.dump(fake, open(p, 'w'))
    r = sei_oei(json.load(open(p))['mbo'], 'T')
    assert r is not None and r[1] > r[0], f'OEI should exceed SEI here, got {r}'
    print('self-check OK (optimizer-driven 2x2 -> OEI > SEI)')
    main()
