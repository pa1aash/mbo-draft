"""LaTeX tables from results_camera.json (+ results_db.json). Emits booktabs tables
into paper/tables_v2/*.tex for \\input. Bold = best per task. Regenerate after any
results refresh; never hand-edit numbers in the paper.

  python tables.py
"""
import json
import os
import numpy as np

HERE = os.path.dirname(__file__)
CAM = os.path.join(HERE, '..', 'results', 'results_camera.json')
OUT = os.path.join(HERE, '..', 'paper', 'tables_v2')
os.makedirs(OUT, exist_ok=True)

GRID = [f'{s}:{o}' for s in ('ens', 'botorchgp', 'svgp') for o in ('grad', 'perturb', 'cma')]
LBL = {'ens:grad': 'Ens+Grad', 'ens:perturb': 'Ens+Pert', 'ens:cma': 'Ens+CMA',
       'botorchgp:grad': 'GP+Grad', 'botorchgp:perturb': 'GP+Pert', 'botorchgp:cma': 'GP+CMA',
       'svgp:grad': 'SVGP+Grad', 'svgp:perturb': 'SVGP+Pert', 'svgp:cma': 'SVGP+CMA',
       'coms': 'COMs', 'cbas': 'CbAS', 'grad_ascent': 'Grad.Asc.', 'gp': 'GP (exact)'}

def load(p): return json.load(open(p)) if os.path.exists(p) else {}

def cell(node, metric='p100'):
    return (node[metric]['mean'], node[metric]['std']) if node and metric in node else None

def main_table(mbo, methods, name, caption):
    tasks = list(mbo)
    # best per task (max mean) for bolding
    best = {}
    for t in tasks:
        vals = {m: mbo[t][m]['p100']['mean'] for m in methods if m in mbo[t]}
        if vals: best[t] = max(vals, key=vals.get)
    lines = [r'\begin{table*}[t]\centering', f'\\caption{{{caption}}}', f'\\label{{tab:{name}}}',
             r'\resizebox{\textwidth}{!}{%', r'\begin{tabular}{l' + 'c' * len(tasks) + '}', r'\toprule',
             'Method & ' + ' & '.join(t.split('-')[0] for t in tasks) + r' \\', r'\midrule']
    # rank row accumulation
    ranks = {m: [] for m in methods}
    for t in tasks:
        present = {m: mbo[t][m]['p100']['mean'] for m in methods if m in mbo[t]}
        order = sorted(present, key=lambda m: -present[m])
        for i, m in enumerate(order): ranks[m].append(i + 1)
    for m in methods:
        row = [LBL.get(m, m)]
        for t in tasks:
            c = cell(mbo[t].get(m))
            if c is None: row.append('--')
            else:
                s = f'{c[0]:.2f}'
                row.append(f'\\textbf{{{s}}}' if best.get(t) == m else s)
        lines.append(' & '.join(row) + r' \\')
    avg = {m: (np.mean(ranks[m]) if ranks[m] else float('nan')) for m in methods}
    lines += [r'\bottomrule', r'\end{tabular}}', r'\end{table*}']
    tex = '\n'.join(lines)
    open(os.path.join(OUT, f'{name}.tex'), 'w').write(tex)
    # companion avg-rank table
    ar = [r'\begin{table}[t]\centering', f'\\caption{{Average rank (\\Cref{{tab:{name}}}), lower is better.}}',
          f'\\label{{tab:{name}_rank}}', r'\begin{tabular}{lc}', r'\toprule', r'Method & Avg. rank \\', r'\midrule']
    for m in sorted(methods, key=lambda m: avg.get(m, 9)):
        if not np.isnan(avg.get(m, float('nan'))):
            ar.append(f'{LBL.get(m, m)} & {avg[m]:.2f} ' + r'\\')
    ar += [r'\bottomrule', r'\end{tabular}', r'\end{table}']
    open(os.path.join(OUT, f'{name}_rank.tex'), 'w').write('\n'.join(ar))
    print(f'  wrote {name}.tex ({len(tasks)} tasks x {len(methods)} methods) + {name}_rank.tex')

if __name__ == '__main__':
    R = load(CAM)
    if R.get('mbo'):
        main_table(R['mbo'], GRID, 'grid',
                   'Offline MBO: 100th-percentile score by surrogate$\\times$optimizer. '
                   'Bold = best per task. The optimizer spread within the ensemble rows vs.\\ within the GP rows is the paper\'s central finding.')
        main_table(R['mbo'], GRID + ['coms', 'cbas', 'grad_ascent'], 'grid_full',
                   'Full comparison including domain baselines (COMs, CbAS, gradient ascent).')
    print(f'tables -> {os.path.abspath(OUT)}')
