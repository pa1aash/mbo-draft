"""Publication figures from results_camera.json (+ results_db.json). Regenerates
every figure the paper uses; run after any results refresh. Colorblind-safe
(Okabe-Ito), direct-labeled, PDF+PNG into paper/figures_v2/.

  python figures.py                 # all figures from whatever results exist
Robust to partial data: missing grid cells are drawn as blanks, not errors.
"""
import json
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = os.path.dirname(__file__)
CAM = os.path.join(HERE, '..', 'results', 'results_camera.json')
DB = os.path.join(HERE, '..', 'results', 'results_db.json')
OUT = os.path.join(HERE, '..', 'paper', 'figures_v2')
os.makedirs(OUT, exist_ok=True)

# Okabe-Ito colorblind-safe palette
OK = {'grad': '#0072B2', 'perturb': '#E69F00', 'cma': '#009E73',
      'ens': '#0072B2', 'botorchgp': '#D55E00', 'svgp': '#CC79A7', 'gray': '#999999'}
SURR = ['ens', 'botorchgp', 'svgp']; OPT = ['grad', 'perturb', 'cma']
SURR_LBL = {'ens': 'Deep ensemble', 'botorchgp': 'Gaussian process', 'svgp': 'SVGP'}
OPT_LBL = {'grad': 'gradient', 'perturb': 'perturbation', 'cma': 'CMA-ES'}

plt.rcParams.update({'font.size': 9, 'axes.spines.top': False, 'axes.spines.right': False,
                     'axes.grid': True, 'grid.alpha': 0.25, 'grid.linewidth': 0.5,
                     'figure.dpi': 150, 'savefig.bbox': 'tight'})

def load(p):
    return json.load(open(p)) if os.path.exists(p) else {}

def save(fig, name):
    for ext in ('pdf', 'png'):
        fig.savefig(os.path.join(OUT, f'{name}.{ext}'))
    plt.close(fig)
    print(f'  wrote {name}.pdf/.png')

def grid_mean(mbo, surrogate, optimizer, metric='p100'):
    """Mean over tasks of per-task RANK of this cell among all grid cells (lower=better),
    so tasks with different score scales combine. NaN if the cell is absent everywhere."""
    per_task = []
    cells = [f'{s}:{o}' for s in SURR for o in OPT]
    for task, row in mbo.items():
        vals = {c: (row[c][metric]['mean'] if c in row else None) for c in cells}
        present = {c: v for c, v in vals.items() if v is not None}
        if len(present) < 2 or f'{surrogate}:{optimizer}' not in present:
            continue
        order = sorted(present, key=lambda c: -present[c])       # higher score = rank 1
        rank = {c: i + 1 for i, c in enumerate(order)}
        per_task.append(rank[f'{surrogate}:{optimizer}'])
    return float(np.mean(per_task)) if per_task else float('nan')

# ---- F1: the money figure — optimizer gap by surrogate (grouped bars, mean rank) ----
def fig_grid_bars(mbo):
    fig, ax = plt.subplots(figsize=(5.8, 3.2))
    xs = np.arange(len(SURR)); w = 0.26
    for j, o in enumerate(OPT):
        vals = [grid_mean(mbo, s, o) for s in SURR]
        bars = ax.bar(xs + (j - 1) * w, vals, w, label=OPT_LBL[o], color=OK[o],
                      edgecolor='white', linewidth=0.8)
        for b, v in zip(bars, vals):
            if not np.isnan(v):
                ax.text(b.get_x() + b.get_width() / 2, v + 0.1, f'{v:.1f}',
                        ha='center', va='bottom', fontsize=7.5, color='#333')
    ax.set_xticks(xs); ax.set_xticklabels([SURR_LBL[s] for s in SURR])
    ax.set_ylabel('Mean rank across tasks\n(lower = better)')
    ax.set_title('Acquisition optimizer decides ensemble performance,\nbut barely matters for GP surrogates', fontsize=9.5)
    ax.legend(title='Optimizer', frameon=False, fontsize=8,
              loc='upper left', bbox_to_anchor=(1.01, 1.0))       # outside, no bar overlap
    ax.set_ylim(0, 9.5)
    save(fig, 'fig1_optimizer_by_surrogate')

# ---- F3: pessimism-premise coverage in-dist vs OOD + conformal repair ----
def fig_coverage(cal):
    if not cal: return
    tasks = list(cal)
    ind = [cal[t]['_'].get('cov_indist@2.0', {}).get('mean', np.nan) for t in tasks]
    ood = [cal[t]['_'].get('cov_ood@2.0', {}).get('mean', np.nan) for t in tasks]
    cind = [cal[t]['_'].get('cov_conf_indist', {}).get('mean', np.nan) for t in tasks]
    cood = [cal[t]['_'].get('cov_conf_ood', {}).get('mean', np.nan) for t in tasks]
    fig, ax = plt.subplots(figsize=(6.0, 3.2)); xs = np.arange(len(tasks)); w = 0.2
    for j, (vals, lbl, c) in enumerate([(ind, 'raw σ, in-distribution', OK['ens']),
                                        (ood, 'raw σ, on LCB designs (OOD)', OK['botorchgp']),
                                        (cind, 'conformal, in-distribution', OK['cma']),
                                        (cood, 'conformal, on LCB designs (OOD)', OK['svgp'])]):
        ax.bar(xs + (j - 1.5) * w, vals, w, label=lbl, color=c, edgecolor='white', linewidth=0.6)
    ax.axhline(0.9, ls='--', lw=1, color='#333', label='nominal 0.90')
    ax.set_xticks(xs); ax.set_xticklabels([t.split('-')[0] for t in tasks], rotation=30, ha='right')
    ax.set_ylabel('Coverage  P(|μ−f| ≤ βσ)'); ax.set_ylim(0, 1.05)
    ax.set_title('The pessimism premise fails on the designs LCB proposes —\nand conformal repair cannot fix it under covariate shift', fontsize=9)
    ax.legend(frameon=False, fontsize=7, ncol=2)
    save(fig, 'fig3_coverage')

# ---- F4: calibration (rho) vs beta-benefit, per task ----
def fig_calib_scatter(mbo, cal, beta):
    if not cal or not beta: return
    xs, ys, labs = [], [], []
    for t in cal:
        if t not in beta: continue
        rho = cal[t]['_'].get('rho_err', {}).get('mean')
        b = beta[t]
        try:
            benefit = b['5.0']['mean'] - b['0.0']['mean']       # pessimism helps if >0
        except KeyError:
            continue
        if rho is None: continue
        xs.append(rho); ys.append(benefit); labs.append(t.split('-')[0])
    if not xs: return
    fig, ax = plt.subplots(figsize=(4.6, 3.4))
    ax.axhline(0, color='#999', lw=0.8)
    ax.scatter(xs, ys, s=42, color=OK['ens'], zorder=3)
    for x, y, l in zip(xs, ys, labs):
        ax.annotate(l, (x, y), fontsize=7, xytext=(4, 3), textcoords='offset points')
    ax.set_xlabel('σ–error rank correlation (calibration quality)')
    ax.set_ylabel('Pessimism benefit  (p100 at β=5 − β=0)')
    ax.set_title('Does calibration predict whether pessimism helps?', fontsize=9.5)
    save(fig, 'fig4_calibration_vs_benefit')

if __name__ == '__main__':
    R = load(CAM)
    if R.get('mbo'): fig_grid_bars(R['mbo'])
    if R.get('calibration'): fig_coverage(R['calibration'])
    if R.get('mbo') and R.get('calibration') and R.get('beta'):
        fig_calib_scatter(R['mbo'], R['calibration'], R['beta'])
    print(f'figures -> {os.path.abspath(OUT)}')
