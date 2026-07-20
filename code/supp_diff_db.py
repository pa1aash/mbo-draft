"""Design-Bench half of tab:cov: OLD (results_db.json, unstamped) vs NEW (stamped off_off).

  python supp_diff_db.py
"""
import json
import os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, '..', 'results')
COV_FIELDS = ['cov_indist@2.0', 'cov_ood@2.0', 'q_conformal', 'cov_conf_indist', 'cov_conf_ood']

# tab:cov Design-Bench rows exactly as printed in supplement.tex
PRINTED = {
    'TFBind8':        (0.92, 0.71, 1.7, 0.90, 0.70),
    'TFBind10':       (1.00, 0.53, -1.6, 0.89, 0.45),
    'Superconductor': (1.00, 0.01, -2.0, 0.90, 0.01),
    'GFP':            (0.00, 0.00, 88.4, 0.90, 0.99),
    'UTR':            (1.00, 0.00, -2.5, 0.91, 0.00),
    'AntMorphology':  (0.94, 0.00, 1.2, 0.90, 0.00),
    'DKitty':         (0.51, 0.00, 8.0, 0.90, 0.00),
}
LBL = {'TFBind8': 'TF-Bind-8', 'TFBind10': 'TF-Bind-10', 'Superconductor': 'Superconductor',
       'GFP': 'GFP', 'UTR': 'UTR', 'AntMorphology': 'Ant', 'DKitty': "D'Kitty"}
ORDER = ['TFBind8', 'TFBind10', 'Superconductor', 'GFP', 'UTR', 'AntMorphology', 'DKitty']


def row(node):
    return [float(np.mean(node['_'][f]['all'])) for f in COV_FIELDS]


def main():
    old = json.load(open(os.path.join(RES, 'results_db.json')))['calibration']
    newf = json.load(open(os.path.join(RES, 'supp_offoff', 'calibration_db_off_off.json')))
    new = newf['calibration']

    print('=' * 96)
    print('tab:cov DESIGN-BENCH block   OLD (results_db.json, unstamped)  ->  NEW (stamped off_off)')
    print('=' * 96)
    print(f'  NEW stamp: {len(newf["meta"])} fields  X1={newf["meta"]["X1"]} X3={newf["meta"]["X3"]}'
          f'  n_seeds={newf["meta"]["n_seeds"]}  python={newf["meta"]["python"]}'
          f'  torch={newf["meta"]["torch"]}')
    missing = [t for t in ORDER if t not in new]
    if missing:
        print(f'  INCOMPLETE - missing {missing}')
        return

    print()
    print('  Validation - does results_db.json reproduce tab:cov as printed?')
    bad = 0
    for t in ORDER:
        for f, g, w in zip(COV_FIELDS, row(old[t]), PRINTED[t]):
            dec = 1 if f == 'q_conformal' else 2
            if round(g, dec) != round(w, dec):
                print(f'    MISMATCH {LBL[t]:15s} {f:18s} printed={w} file={g:.4f}')
                bad += 1
    print(f'    {35 - bad}/35 entries reproduce' + ('  [OK]' if bad == 0 else ''))

    print()
    names = ['c_in', 'c_ood', 'qhat', 'cf_in', 'cf_ood']
    print(f'  {"Task":16s}' + ''.join(f'{n:>18s}' for n in names))
    changed = []
    for t in ORDER:
        o, n = row(old[t]), row(new[t])
        cells = []
        for i in range(5):
            dec = 1 if COV_FIELDS[i] == 'q_conformal' else 2
            po, pn = round(o[i], dec), round(n[i], dec)
            if po != pn:
                changed.append((LBL[t], names[i], po, pn))
            cells.append(f'{o[i]:.{dec}f}->{n[i]:.{dec}f}' + ('*' if po != pn else ''))
        print(f'  {LBL[t]:16s}' + ''.join(f'{c:>18s}' for c in cells))

    print()
    print(f'  entries whose PRINTED value changes: {len(changed)}/35')
    for lbl, f, po, pn in changed:
        print(f'    {lbl:15s} {f:8s} {po}  ->  {pn}')

    print()
    print('  Claim check - cf_ood == 0.00 exactly (DB contribution to "five of the fourteen"):')
    for tag, src in (('old', old), ('new', new)):
        z = [LBL[t] for t in ORDER if round(row(src[t])[4], 2) == 0.00]
        print(f'    {tag}: {len(z)}  {z}')
    print()
    print('  Negative qhat rows (feeds "on several real tasks above nominal"):')
    for tag, src in (('old', old), ('new', new)):
        z = [LBL[t] for t in ORDER if row(src[t])[2] < 0]
        print(f'    {tag}: {z}')


if __name__ == '__main__':
    main()
