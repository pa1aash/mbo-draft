"""Self-test for analyze_swing.py on SYNTHETIC grids with known ground truth.

Validates the decision logic before the real grid lands, so a crash or an inverted
verdict cannot be discovered only after hours of compute. Three planted scenarios:

  A. smoothing closes the gap, roughening hurts the GP, manipulation lands  -> FOLD
  B. smoothing does nothing                                                 -> SM1 KILL
  C. manipulation does not move roughness                                   -> VOID

Writes to a scratch path; never touches results/swing/swing_grid.json.
"""
import json
import os
import sys
import tempfile

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import analyze_swing as A                                           # noqa: E402

TASKS = A.TASKS
OPT3 = A.OPT3
S = 30


def _agg(v):
    a = np.asarray(v, float)
    return dict(mean=float(a.mean()), std=float(a.std()), n=int(a.size),
                all=[float(z) for z in a])


def build(scenario, seed=0):
    r = np.random.RandomState(seed)
    mbo_node, rough, rseg = {}, {}, {}
    for ti, t in enumerate(TASKS):
        scale = 10.0 * (ti + 1)
        cells, rd, rs = {}, {}, {}

        def put(name, level, noise=0.05):
            for o in OPT3:
                cells[f'{name}:{o}'] = {
                    'p100': _agg(level * scale + r.randn(S) * noise * scale),
                    'p50': _agg((level - 0.1) * scale + r.randn(S) * noise * scale),
                    'c_ood': _agg(np.clip(0.9 + r.randn(S) * 0.02, 0, 1)),
                    'inversion': _agg((r.rand(S) < 0.2).astype(float)),
                    'inv_magnitude': _agg(np.abs(r.randn(S)) * 0.1)}

        # smooth GPs score high (1.0); base ensemble low (0.5) -> a real gap
        put('botorchgp', 1.00); put('svgp', 0.98)
        rd['botorchgp'] = rd['svgp'] = 6.0
        rs['botorchgp'] = rs['svgp'] = 5.0

        # SM2 roughened GPs
        for nm in ('botorchgp_m12L', 'botorchgp_lsL3', 'svgp_m12'):
            if scenario == 'A':
                put(nm, 0.55)                       # collapses
                rd[nm], rs[nm] = 9.0, 7.5           # and got rougher (+50%)
                for o in OPT3:                      # coverage drops
                    cells[f'{nm}:{o}']['c_ood'] = _agg(np.clip(0.55 + r.randn(S) * 0.02, 0, 1))
            else:
                put(nm, 0.99)                       # stays robust
                rd[nm], rs[nm] = 6.0, 5.0           # and never got rougher

        for w in (96, 1024):
            put(f'ens_base_w{w}', 0.50)
            rd[f'ens_base_w{w}'] = 6.0
            rs[f'ens_base_w{w}'] = 5.0
            for v, lev in (('gp0.01', 0.60), ('gp0.1', 0.95), ('gp1.0', 0.40), ('sn', 0.70)):
                if scenario == 'B':
                    lev = 0.50                      # smoothing changes nothing
                put(f'ens_{v}_w{w}', lev)
                # roughness: falls a lot unless scenario C (manipulation inert)
                fall = {'gp0.01': 0.7, 'gp0.1': 0.2, 'gp1.0': 0.05, 'sn': 0.15}[v]
                if scenario == 'C':
                    fall = 0.99
                rd[f'ens_{v}_w{w}'] = 6.0 * fall
                rs[f'ens_{v}_w{w}'] = 5.0 * fall
            if scenario == 'B':
                for o in OPT3:
                    pass
        mbo_node[t] = cells
        rough[t] = {k: _agg([v] * S) for k, v in rd.items()}
        rseg[t] = {k: _agg([v] * S) for k, v in rs.items()}
    return dict(meta={'synthetic': True}, n_shards=len(TASKS) * S,
                mbo=mbo_node, roughness=rough, roughness_seg=rseg)


def run(scenario):
    d = build(scenario)
    tmp = tempfile.mkdtemp()
    p = os.path.join(tmp, 'swing_grid.json')
    json.dump(d, open(p, 'w'))
    old_grid, old_out = A.GRID, A.OUT
    A.GRID, A.OUT, A.NBOOT = p, tmp, 400          # fewer resamples: logic test, not precision
    try:
        A.main()
        res = json.load(open(os.path.join(tmp, 'swing_analysis.json')))
    finally:
        A.GRID, A.OUT = old_grid, old_out
    return res


if __name__ == '__main__':
    exp = {'A': ('CONFIRMED', 'CONFIRMED', 'CONFIRMED', 'FOLD'),
           'B': ('KILL', None, None, 'SHIP-PURE-D'),
           'C': (None, None, None, 'SHIP-PURE-D')}
    ok = True
    for sc in ('A', 'B', 'C'):
        print('=' * 30, 'SCENARIO', sc, '=' * 30)
        r = run(sc)
        got = (r['SM1']['verdict'], r['SM2']['verdict'], r['SM3']['verdict'], r['BINARY_CALL'])
        e = exp[sc]
        good = (got[3] == e[3]) and all(x is None or g.startswith(x) for g, x in zip(got, e))
        ok &= good
        print(f'\n  -> SM1={got[0]} SM2={got[1]} SM3={got[2]} CALL={got[3]}  '
              f'{"OK" if good else "UNEXPECTED (expected " + str(e) + ")"}\n')
    print('SELFTEST', 'PASS' if ok else 'FAIL')
    sys.exit(0 if ok else 1)
