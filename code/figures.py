"""Publication figures from results_camera.json (+ results_db.json).

Regenerates every figure the paper uses; run after any results refresh.
Serif fonts to match the AAAI body, colorblind-safe (Okabe-Ito / cividis),
distribution- and CI-based where per-seed data exists. PDF+PNG into
paper/figures_v2/.

  python figures.py                 # all figures from whatever results exist

Robust to partial data: missing grid cells are drawn as blanks, not errors.
"""
import json
import os
import warnings
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from scipy.stats import friedmanchisquare

warnings.filterwarnings('ignore', message='findfont')

HERE = os.path.dirname(__file__)
CAM = os.path.join(HERE, '..', 'results', 'results_camera.json')
DB = os.path.join(HERE, '..', 'results', 'results_db.json')
OUT = os.path.join(HERE, '..', 'paper', 'figures_v2')
os.makedirs(OUT, exist_ok=True)

# Okabe-Ito colorblind-safe palette
OK = {'grad': '#0072B2', 'perturb': '#E69F00', 'cma': '#009E73',
      'ens': '#0072B2', 'botorchgp': '#D55E00', 'svgp': '#CC79A7',
      'indist': '#0072B2', 'ood': '#D55E00', 'conf': '#009E73', 'gray': '#8a8a8a'}
SURR = ['ens', 'botorchgp', 'svgp']
OPT = ['grad', 'perturb', 'cma']
SURR_LBL = {'ens': 'Ensemble', 'botorchgp': 'Exact GP', 'svgp': 'SVGP'}
OPT_LBL = {'grad': 'Gradient', 'perturb': 'Perturbation', 'cma': 'CMA-ES'}
CELL_LBL = {'ens:grad': 'Ens+Grad', 'ens:perturb': 'Ens+Pert', 'ens:cma': 'Ens+CMA',
            'botorchgp:grad': 'GP+Grad', 'botorchgp:perturb': 'GP+Pert', 'botorchgp:cma': 'GP+CMA',
            'svgp:grad': 'SVGP+Grad', 'svgp:perturb': 'SVGP+Pert', 'svgp:cma': 'SVGP+CMA'}

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'Nimbus Roman', 'DejaVu Serif'],
    'mathtext.fontset': 'stix',
    'font.size': 10, 'axes.titlesize': 10.5, 'axes.labelsize': 10,
    'xtick.labelsize': 8.5, 'ytick.labelsize': 8.5, 'legend.fontsize': 8.5,
    'axes.spines.top': False, 'axes.spines.right': False,
    'axes.grid': True, 'grid.alpha': 0.16, 'grid.linewidth': 0.6, 'axes.axisbelow': True,
    'figure.dpi': 200, 'savefig.bbox': 'tight', 'savefig.pad_inches': 0.02,
    'lines.linewidth': 1.9, 'patch.linewidth': 0.6,
})


def load(p):
    return json.load(open(p)) if os.path.exists(p) else {}


def save(fig, name):
    for ext in ('pdf', 'png'):
        fig.savefig(os.path.join(OUT, f'{name}.{ext}'))
    plt.close(fig)
    print(f'  wrote {name}.pdf/.png')


def cells_present(mbo):
    """Ordered surrogate:optimizer cells that appear in at least one task."""
    seen = set()
    for row in mbo.values():
        seen |= set(row)
    return [f'{s}:{o}' for s in SURR for o in OPT if f'{s}:{o}' in seen]


def rank_matrix(mbo, metric='p100'):
    """Mean-across-tasks rank of each surrogate:optimizer cell (1=best per task)."""
    cells = cells_present(mbo)
    per_cell = {c: [] for c in cells}
    for task, row in mbo.items():
        present = {c: row[c][metric]['mean'] for c in cells if c in row}
        if len(present) < 2:
            continue
        order = sorted(present, key=lambda c: -present[c])
        rank = {c: i + 1 for i, c in enumerate(order)}
        for c in present:
            per_cell[c].append(rank[c])
    return {c: (float(np.mean(v)) if v else np.nan) for c, v in per_cell.items()}


# ---- F1: decomposition heatmap (money shot), synthetic | Design-Bench ----
def fig_heatmap(cam_mbo, db_mbo):
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.9))
    for ax, mbo, title in [(axes[0], cam_mbo, 'Synthetic (7 tasks)'),
                           (axes[1], db_mbo, 'Design-Bench (7 tasks)')]:
        rk = rank_matrix(mbo)
        M = np.full((len(SURR), len(OPT)), np.nan)
        for i, s in enumerate(SURR):
            for j, o in enumerate(OPT):
                M[i, j] = rk.get(f'{s}:{o}', np.nan)
        im = ax.imshow(M, cmap='cividis', vmin=1, vmax=9, aspect='auto')
        ax.set_xticks(range(len(OPT)))
        ax.set_xticklabels([OPT_LBL[o] for o in OPT], rotation=18, ha='right')
        ax.set_yticks(range(len(SURR)))
        ax.set_yticklabels([SURR_LBL[s] for s in SURR])
        ax.set_title(title)
        ax.grid(False)
        ax.tick_params(length=0)
        for i in range(len(SURR)):
            for j in range(len(OPT)):
                v = M[i, j]
                if np.isnan(v):
                    ax.text(j, i, '--', ha='center', va='center', color='#bbb', fontsize=9)
                else:
                    ax.text(j, i, f'{v:.1f}', ha='center', va='center', fontsize=10,
                            color='white' if v < 5.2 else '#1a1a1a',
                            fontweight='bold' if v < 3.6 else 'normal')
    cb = fig.colorbar(im, ax=axes, fraction=0.032, pad=0.03)
    cb.set_label('Mean rank across tasks (1 = best)', fontsize=8.5)
    cb.ax.tick_params(labelsize=8)
    fig.suptitle('Surrogate class dominates on synthetic tasks; the grid flattens on Design-Bench',
                 fontsize=10.5, y=1.04)
    save(fig, 'fig1_grid_heatmap')


# ---- F2: optimizer-induced spread by surrogate (per-seed distributions) ----
def fig_spread(mbo, metric='p100'):
    """For each surrogate, box of per-seed task-normalized scores under each optimizer."""
    pooled = {f'{s}:{o}': [] for s in SURR for o in OPT}
    for task, row in mbo.items():
        allv = []
        for c in row:
            allv += row[c][metric]['all']
        m, Mx = min(allv), max(allv)
        rng = (Mx - m) or 1.0
        for s in SURR:
            for o in OPT:
                c = f'{s}:{o}'
                if c in row:
                    pooled[c] += [(v - m) / rng for v in row[c][metric]['all']]
    fig, ax = plt.subplots(figsize=(5.6, 3.0))
    positions, data, colors, group_centers = [], [], [], []
    x = 0
    for s in SURR:
        start = x
        for o in OPT:
            positions.append(x)
            data.append(pooled[f'{s}:{o}'])
            colors.append(OK[o])
            x += 1
        group_centers.append((start + x - 1) / 2)
        x += 1
    bp = ax.boxplot(data, positions=positions, widths=0.72, patch_artist=True,
                    showfliers=False, medianprops=dict(color='#111', lw=1.2),
                    whiskerprops=dict(color='#555', lw=0.9), capprops=dict(color='#555', lw=0.9))
    for patch, c in zip(bp['boxes'], colors):
        patch.set_facecolor(c)
        patch.set_alpha(0.82)
        patch.set_edgecolor('white')
    ax.set_xticks(group_centers)
    ax.set_xticklabels([SURR_LBL[s] for s in SURR])
    ax.set_ylabel('Task-normalized score\n(higher = better)')
    ax.set_ylim(-0.02, 1.05)
    ax.set_title('The acquisition optimizer swings ensemble outcomes\nbut is nearly inert for calibrated posteriors', fontsize=9.8)
    ax.legend(handles=[Patch(facecolor=OK[o], alpha=0.82, label=OPT_LBL[o]) for o in OPT],
              title='Optimizer', frameon=False, loc='lower right', ncol=1)
    save(fig, 'fig2_optimizer_spread')


# ---- F3: pessimism-premise coverage vs beta, in-dist vs OOD + conformal ----
def _cov_curves(cal, betas=('0.5', '1.0', '2.0', '5.0')):
    tasks = list(cal)
    ind = np.array([[cal[t]['_'].get(f'cov_indist@{b}', {}).get('mean', np.nan) for t in tasks] for b in betas])
    ood = np.array([[cal[t]['_'].get(f'cov_ood@{b}', {}).get('mean', np.nan) for t in tasks] for b in betas])
    cin = np.array([cal[t]['_'].get('cov_conf_indist', {}).get('mean', np.nan) for t in tasks])
    coo = np.array([cal[t]['_'].get('cov_conf_ood', {}).get('mean', np.nan) for t in tasks])
    return ind, ood, cin, coo


def fig_coverage(cam_cal, db_cal):
    betas = ['0.5', '1.0', '2.0', '5.0']
    bx = [float(b) for b in betas]
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.9), sharey=True)
    for ax, cal, title in [(axes[0], cam_cal, 'Synthetic'), (axes[1], db_cal, 'Design-Bench')]:
        if not cal:
            continue
        ind, ood, cin, coo = _cov_curves(cal, betas)
        mi, si = np.nanmean(ind, 1), np.nanstd(ind, 1)
        mo, so = np.nanmean(ood, 1), np.nanstd(ood, 1)
        ax.axhline(0.9, ls=(0, (4, 3)), lw=1.1, color='#444', zorder=1)
        ax.text(0.52, 0.915, 'nominal 0.90', fontsize=7.5, color='#444')
        ax.plot(bx, mi, '-o', color=OK['indist'], label='raw $\\sigma$, in-distribution', ms=4, zorder=4)
        ax.fill_between(bx, np.clip(mi - si, 0, 1), np.clip(mi + si, 0, 1), color=OK['indist'], alpha=0.14, zorder=2)
        ax.plot(bx, mo, '--s', color=OK['ood'], label='raw $\\sigma$, on LCB proposals (OOD)', ms=4, zorder=4)
        ax.fill_between(bx, np.clip(mo - so, 0, 1), np.clip(mo + so, 0, 1), color=OK['ood'], alpha=0.12, zorder=2)
        ax.scatter([5.35], [np.nanmean(cin)], marker='*', s=130, color=OK['conf'], zorder=6, clip_on=False)
        ax.scatter([5.35], [np.nanmean(coo)], marker='*', s=130, color=OK['conf'],
                   edgecolor=OK['ood'], linewidth=1.1, zorder=6, clip_on=False)
        ax.set_xlabel('Pessimism strength  $\\beta$')
        ax.set_title(title)
        ax.set_xlim(0.3, 5.7)
    axes[0].set_ylabel('Coverage  $\\Pr(f \\geq \\mu-\\beta\\sigma)$')
    axes[0].set_ylim(-0.02, 1.04)
    handles = [Line2D([], [], color=OK['indist'], marker='o', label='raw $\\sigma$, in-distribution'),
               Line2D([], [], color=OK['ood'], ls='--', marker='s', label='raw $\\sigma$, on LCB proposals (OOD)'),
               Line2D([], [], color=OK['conf'], marker='*', ls='', ms=11, label='conformal repair ($\\star$)')]
    fig.legend(handles=handles, loc='lower center', ncol=3, frameon=False,
               bbox_to_anchor=(0.5, -0.10), fontsize=8.2)
    fig.suptitle('The pessimism premise fails on proposed designs; conformal repairs in-distribution, not OOD',
                 fontsize=10, y=1.02)
    save(fig, 'fig3_coverage')


# ---- F4: beta-sweep, pessimism-as-regularization (per-task normalized curves) ----
def fig_beta(beta):
    if not beta:
        return
    order = ['0.0', '0.5', '1.0', '2.0', '5.0']
    bx = [float(b) for b in order]
    fig, ax = plt.subplots(figsize=(5.4, 3.1))
    curves = []
    for t in beta:
        ys = []
        for b in order:
            try:
                ys.append(beta[t][b]['p100']['mean'])
            except (KeyError, TypeError):
                ys.append(np.nan)
        ys = np.array(ys)
        if np.all(np.isnan(ys)):
            continue
        lo, hi = np.nanmin(ys), np.nanmax(ys)
        norm = (ys - lo) / ((hi - lo) or 1.0)
        curves.append(norm)
        ax.plot(bx, norm, color=OK['gray'], lw=1.0, alpha=0.55, zorder=2)
        if norm[-1] < 0.25:  # label only the decliner(s) to avoid a right-edge pile-up
            ax.annotate(t.split('-')[0] + ' (declines)', (bx[-1], norm[-1]), fontsize=7.2,
                        color=OK['ood'], xytext=(4, 0), textcoords='offset points', va='center')
    if curves:
        mean = np.nanmean(np.vstack(curves), 0)
        ax.plot(bx, mean, color=OK['grad'], lw=2.6, marker='o', ms=5, zorder=5, label='mean across tasks')
    ax.set_xlabel('Pessimism strength  $\\beta$')
    ax.set_ylabel('Normalized score  (per task)')
    ax.set_title('Pessimism helps on 6/7 tasks despite an\nuninformative $\\sigma$: regularization, not calibration', fontsize=9.8)
    ax.legend(frameon=False, loc='lower right')
    ax.set_xlim(-0.15, 5.5)
    save(fig, 'fig4_beta_sweep')


# ---- F5: ensemble-size ablation (K sweep) ----
def fig_k(K):
    if not K:
        return
    order = sorted({k for t in K for k in K[t]}, key=int)
    kx = [int(k) for k in order]
    fig, ax = plt.subplots(figsize=(5.2, 3.0))
    curves = []
    for t in K:
        ys = []
        for k in order:
            try:
                ys.append(K[t][k]['p100']['mean'])
            except (KeyError, TypeError):
                ys.append(np.nan)
        ys = np.array(ys)
        if np.all(np.isnan(ys)):
            continue
        lo, hi = np.nanmin(ys), np.nanmax(ys)
        curves.append((ys - lo) / ((hi - lo) or 1.0))
        ax.plot(kx, curves[-1], color=OK['gray'], lw=1.0, alpha=0.5)
    if curves:
        ax.plot(kx, np.nanmean(np.vstack(curves), 0), color=OK['botorchgp'], lw=2.6, marker='o', ms=5, label='mean across tasks')
    ax.set_xlabel('Ensemble size  $K$')
    ax.set_ylabel('Normalized score  (per task)')
    ax.set_xticks(kx)
    ax.set_title('More ensemble members shrink $\\sigma$ and\nweaken the penalty: score falls with $K$', fontsize=9.8)
    ax.legend(frameon=False, loc='upper right')
    save(fig, 'fig7_k_ablation')


# ---- F6: critical-difference diagram, synthetic vs Design-Bench (stacked) ----
def _cd_axis(ax, mbo, title):
    methods = cells_present(mbo)
    tasks = [t for t in mbo if all(m in mbo[t] for m in methods)]
    if len(tasks) < 2:
        ax.axis('off')
        return
    R = np.array([[mbo[t][m]['p100']['mean'] for m in methods] for t in tasks])
    ranks = (-R).argsort(1).argsort(1) + 1
    avg = ranks.mean(0)
    k, N = len(methods), len(tasks)
    _, pval = friedmanchisquare(*[R[:, j] for j in range(k)])
    q = {3: 2.343, 4: 2.569, 5: 2.728, 6: 2.850, 7: 2.949, 8: 3.031, 9: 3.102, 10: 3.164}.get(k, 3.164)
    cd = q * np.sqrt(k * (k + 1) / (6 * N))
    order = np.argsort(avg)
    ax.set_xlim(0.5, k + 0.5)
    ax.set_ylim(-(np.ceil(k / 2) + 1) * 0.7 - 0.3, 1.1)
    ax.axis('off')
    ax.plot([1, k], [0, 0], 'k', lw=1.1)
    for r in range(1, k + 1):
        ax.plot([r, r], [0, 0.09], 'k', lw=1.0)
        ax.text(r, 0.2, str(r), ha='center', fontsize=7.5)
    left = [i for i in order if avg[i] <= (k + 1) / 2]
    right = [i for i in order if avg[i] > (k + 1) / 2]
    yl = -0.55
    for idx in left:
        ax.plot([avg[idx], avg[idx]], [0, yl], color=OK['gray'], lw=0.9)
        ax.plot([avg[idx], 0.7], [yl, yl], color=OK['gray'], lw=0.9)
        ax.text(0.62, yl, f'{CELL_LBL[methods[idx]]} ({avg[idx]:.1f})', va='center', ha='right', fontsize=7.6)
        yl -= 0.7
    yr = -0.55
    for idx in reversed(right):
        ax.plot([avg[idx], avg[idx]], [0, yr], color=OK['gray'], lw=0.9)
        ax.plot([avg[idx], k + 0.3], [yr, yr], color=OK['gray'], lw=0.9)
        ax.text(k + 0.38, yr, f'({avg[idx]:.1f}) {CELL_LBL[methods[idx]]}', va='center', ha='left', fontsize=7.6)
        yr -= 0.7
    ax.plot([1, 1 + cd], [0.62, 0.62], 'k', lw=2.6)
    ax.plot([1, 1], [0.56, 0.68], 'k', lw=1.0)
    ax.plot([1 + cd, 1 + cd], [0.56, 0.68], 'k', lw=1.0)
    ax.text(1 + cd / 2, 0.74, f'CD = {cd:.2f}', ha='center', fontsize=7.8)
    if pval < 1e-3:
        m, e = f'{pval:.1e}'.split('e')
        ptxt = f'$p={m}\\times10^{{{int(e)}}}$'
    else:
        ptxt = f'$p={pval:.2f}$'
    ax.set_title(f'{title} (Friedman {ptxt})', fontsize=9.8, loc='left', x=0.0, y=0.98)


def fig_cd(cam_mbo, db_mbo):
    fig, axes = plt.subplots(2, 1, figsize=(6.4, 5.0))
    _cd_axis(axes[0], cam_mbo, 'Synthetic: methods separate')
    _cd_axis(axes[1], db_mbo, 'Design-Bench: all methods within one CD')
    fig.suptitle('Method rankings do not transfer from synthetic to real tasks', fontsize=10.5, y=0.99)
    save(fig, 'fig6_cd_diagram')


# ---- F7: calibration quality vs pessimism benefit ----
def fig_calib_scatter(cal, beta):
    if not cal or not beta:
        return
    order = ['0.0', '0.5', '1.0', '2.0', '5.0']
    xs, ys, labs = [], [], []
    for t in cal:
        if t not in beta:
            continue
        rho = cal[t]['_'].get('rho_err', {}).get('mean')
        try:
            vals = np.array([beta[t][b]['p100']['mean'] for b in order])
        except (KeyError, TypeError):
            continue
        if rho is None:
            continue
        rng = (vals.max() - vals.min()) or 1.0
        benefit = (vals[-1] - vals[0]) / rng  # task-normalized benefit in [-1, 1]
        xs.append(rho)
        ys.append(benefit)
        labs.append(t.split('-')[0])
    if not xs:
        return
    fig, ax = plt.subplots(figsize=(4.8, 3.3))
    ax.axhline(0, color=OK['gray'], lw=0.9)
    ax.scatter(xs, ys, s=54, color=OK['ens'], zorder=3, edgecolor='white', linewidth=0.8)
    for x, y, l in zip(xs, ys, labs):
        ax.annotate(l, (x, y), fontsize=7.2, xytext=(4, 3), textcoords='offset points')
    ax.set_ylim(-1.15, 1.15)
    ax.set_xlabel('$\\sigma$–error rank correlation $\\rho$  (calibration quality)')
    ax.set_ylabel('Task-normalized pessimism benefit\n($\\beta{=}5$ vs.\\ $\\beta{=}0$)')
    ax.set_title('Calibration quality does not predict\nwhether pessimism helps', fontsize=9.8)
    save(fig, 'fig5_calibration_vs_benefit')


def fig_crossproposal(gpcov):
    """Premise coverage of each surrogate on in-dist points, its own proposals, and the
    other surrogate's proposals. The ensemble fails ONLY on its own gradient proposals."""
    if not gpcov:
        return
    K = ['gp_indist', 'gp_own', 'ens_indist', 'ens_own', 'ens_on_gp', 'gp_on_ens']
    m = {k: float(np.mean([gpcov[t][k]['mean'] for t in gpcov])) for k in K}
    ens = [m['ens_indist'], m['ens_own'], m['ens_on_gp']]
    gp = [m['gp_indist'], m['gp_own'], m['gp_on_ens']]
    labels = ['in-distribution', 'own proposals', "other's proposals"]
    cols = [OK['indist'], OK['ood'], OK['conf']]
    fig, ax = plt.subplots(figsize=(5.4, 3.1))
    x = np.arange(2); w = 0.26
    for j in range(3):
        vals = [ens[j], gp[j]]
        b = ax.bar(x + (j - 1) * w, vals, w, label=labels[j], color=cols[j], edgecolor='white', linewidth=0.7)
        for xi, v in zip(x + (j - 1) * w, vals):
            ax.text(xi, v + 0.015, f'{v:.2f}', ha='center', va='bottom', fontsize=7.5, color='#333')
    ax.axhline(0.9, ls=(0, (4, 3)), lw=1.0, color='#444')
    ax.text(-0.36, 0.915, 'nominal 0.90', fontsize=7.5, color='#444', ha='left')
    ax.set_xticks(x); ax.set_xticklabels(['Ensemble', 'GP'])
    ax.set_ylabel('Premise coverage  $\\Pr(f\\geq\\mu{-}\\beta\\sigma)$'); ax.set_ylim(0, 1.10)
    ax.set_title("The ensemble premise collapses only on its own gradient proposals,\nnot on the GP's $-$ an ensemble$\\times$gradient interaction", fontsize=9.2)
    ax.legend(frameon=False, fontsize=8, loc='lower center', ncol=3, bbox_to_anchor=(0.5, -0.30))
    save(fig, 'fig8_crossproposal')


if __name__ == '__main__':
    R = load(CAM)
    D = load(DB)
    GC = load(os.path.join(HERE, '..', 'results', 'gpcov.json'))
    if GC:
        fig_crossproposal(GC)
    cam_mbo, db_mbo = R.get('mbo', {}), D.get('mbo', {})
    cam_cal, db_cal = R.get('calibration', {}), D.get('calibration', {})
    if cam_mbo:
        fig_heatmap(cam_mbo, db_mbo)
        fig_spread(cam_mbo)
        fig_cd(cam_mbo, db_mbo)
    if cam_cal:
        fig_coverage(cam_cal, db_cal)
    if R.get('beta'):
        fig_beta(R['beta'])
        fig_calib_scatter(cam_cal, R['beta'])
    if R.get('K'):
        fig_k(R['K'])
    print(f'figures -> {os.path.abspath(OUT)}')
