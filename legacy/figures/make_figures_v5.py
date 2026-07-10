"""Generate all publication-quality figures for ICML paper v5."""
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams.update({
    'font.size': 9, 'axes.labelsize': 10, 'axes.titlesize': 10,
    'xtick.labelsize': 8, 'ytick.labelsize': 8, 'legend.fontsize': 7,
    'figure.dpi': 300, 'savefig.dpi': 300, 'savefig.bbox': 'tight',
    'font.family': 'serif',
})

with open('results.json') as f:
    R = json.load(f)
with open('results_new.json') as f:
    RN = json.load(f)

tasks_order = ['Branin-2D','Styblinski-5D','Levy-8D','Rosenbrock-10D','Rastrigin-15D','Ackley-20D']
short_names = ['Branin\n(2D)','Styblinski\n(5D)','Levy\n(8D)','Rosenbrock\n(10D)','Rastrigin\n(15D)','Ackley\n(20D)']

# ============================================================
# Figure 1: MBO comparison WITH GP-LCB (6 tasks, exclude Griewank for scale)
# ============================================================
print("Figure 1: MBO comparison with GP-LCB...")
methods = ['lcb','coms','grad_ascent']
labels = ['Ens-LCB (Ours)','COMs','Grad. Ascent','GP-LCB']
colors = ['#2196F3','#FF9800','#9E9E9E','#4CAF50']

fig, ax = plt.subplots(1, 1, figsize=(7.0, 2.8))
x = np.arange(len(tasks_order))
w = 0.2

for i, (method, label, color) in enumerate(zip(methods, labels[:3], colors[:3])):
    means = [R['mbo'][t][method]['p100_m'] for t in tasks_order]
    stds = [R['mbo'][t][method]['p100_s'] for t in tasks_order]
    ax.bar(x + i*w - 1.5*w, means, w, label=label, color=color, edgecolor='white',
           linewidth=0.5, yerr=stds, capsize=2, error_kw={'linewidth':0.7})

# GP-LCB
gp_means = [RN['gp_lcb'][t]['p100_m'] for t in tasks_order]
gp_stds = [RN['gp_lcb'][t]['p100_s'] for t in tasks_order]
ax.bar(x + 1.5*w, gp_means, w, label='GP-LCB', color=colors[3], edgecolor='white',
       linewidth=0.5, yerr=gp_stds, capsize=2, error_kw={'linewidth':0.7})

ax.set_xticks(x)
ax.set_xticklabels(short_names, fontsize=7)
ax.set_ylabel('Oracle Score (p100) ↑')
ax.set_title('Offline MBO: 100th Percentile Oracle Score (6 tasks, higher is better)')
ax.legend(loc='lower left', frameon=True, framealpha=0.9, ncol=2)
ax.axhline(y=0, color='gray', linewidth=0.3, linestyle='--')
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('fig1_offline_mbo.pdf'); plt.savefig('fig1_offline_mbo.png')
plt.close()

# ============================================================
# Figure 2: Average rank (4 methods, 6 tasks)
# ============================================================
print("Figure 2: Average rank...")
methods_all = ['lcb','coms','grad_ascent','gp_lcb']
labels_all = ['Ens-LCB','COMs','Grad. Asc.','GP-LCB']
colors_all = ['#2196F3','#FF9800','#9E9E9E','#4CAF50']

ranks = {m: [] for m in methods_all}
for t in tasks_order:
    scores = {}
    for m in ['lcb','coms','grad_ascent']:
        scores[m] = R['mbo'][t][m]['p100_m']
    scores['gp_lcb'] = RN['gp_lcb'][t]['p100_m']
    sorted_s = sorted(scores.items(), key=lambda x: -x[1])
    for rank, (m, _) in enumerate(sorted_s, 1):
        ranks[m].append(rank)

fig, ax = plt.subplots(1, 1, figsize=(3.5, 2.2))
avg_ranks = {m: np.mean(ranks[m]) for m in methods_all}
bars = ax.barh([labels_all[i] for i in range(4)],
               [avg_ranks[m] for m in methods_all],
               color=colors_all, edgecolor='white')
for bar, m in zip(bars, methods_all):
    ax.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2,
            f'{avg_ranks[m]:.2f}', va='center', fontsize=8)
ax.set_xlabel('Average Rank (lower is better)')
ax.set_title('Average Rank (6 tasks)')
ax.set_xlim(0, 4.5)
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('fig2_avg_rank.pdf'); plt.savefig('fig2_avg_rank.png')
plt.close()

# ============================================================
# Figure 3: O2O (keep existing)
# ============================================================
print("Figure 3: O2O MBO...")
o2o_tasks = ['Styblinski-5D', 'Rosenbrock-10D']
o2o_methods = ['LCB','COMs','Naive','Rand']
o2o_colors = ['#2196F3','#FF9800','#9E9E9E','#E0E0E0']
o2o_labels = ['LCB+O2O','COMs+O2O','Naive+O2O','Random+O2O']

fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.5))
for idx, task in enumerate(o2o_tasks):
    ax = axes[idx]
    budgets = sorted([int(k) for k in R['o2o'][task].keys()])
    for mi, (method, label, color) in enumerate(zip(o2o_methods, o2o_labels, o2o_colors)):
        imps, imp_stds = [], []
        for k in budgets:
            d = R['o2o'][task][str(k)].get(method, {})
            imps.append(d.get('imp_m', 0)); imp_stds.append(d.get('imp_s', 0))
        ax.errorbar(budgets, imps, yerr=imp_stds, marker='o', markersize=4,
                    label=label, color=color, linewidth=1.5, capsize=3, capthick=1)
    ax.axhline(y=0, color='gray', linewidth=0.5, linestyle='--')
    ax.set_xlabel('Online Budget (k)'); ax.set_ylabel('Improvement (%)')
    ax.set_title(task)
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    if idx == 0: ax.legend(fontsize=6, loc='upper left')
plt.suptitle('O2O MBO: Improvement vs. Budget', fontsize=10, y=1.02)
plt.tight_layout()
plt.savefig('fig3_o2o_mbo.pdf'); plt.savefig('fig3_o2o_mbo.png')
plt.close()

# ============================================================
# Figure 4: Beta ablation (ALL 5 tasks: Styblinski, Rosenbrock, Rastrigin + Levy, Ackley)
# ============================================================
print("Figure 4: Beta ablation (extended)...")
betas = [0.0, 0.5, 1.0, 2.0, 5.0]
abl_tasks_orig = ['Styblinski-5D','Rosenbrock-10D','Rastrigin-15D']
abl_tasks_new = ['Levy-8D','Ackley-20D']

fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.5))

# Left: tasks where pessimism helps
ax = axes[0]
colors_abl = ['#4CAF50','#2196F3','#9C27B0']
for ti, (task, color) in enumerate(zip(abl_tasks_orig, colors_abl)):
    means = [R['abl']['beta'][task][str(b)]['m'] for b in betas]
    mn, mx = min(means), max(means)
    if mx > mn: norm = [(m-mn)/(mx-mn) for m in means]
    else: norm = [0.5]*len(means)
    ax.plot(betas, norm, 'o-', label=task.split('-')[0], color=color, markersize=4, linewidth=1.5)
ax.set_xlabel(r'$\beta$'); ax.set_ylabel('Normalized Score')
ax.set_title(r'Tasks where pessimism helps')
ax.legend(fontsize=7); ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)

# Right: tasks where pessimism hurts (Levy, Ackley)
ax = axes[1]
colors_new = ['#E91E63','#FF5722']
for ti, (task, color) in enumerate(zip(abl_tasks_new, colors_new)):
    means = [RN['beta_counter'][task][str(b)]['m'] for b in betas]
    mn, mx = min(means), max(means)
    if mx > mn: norm = [(m-mn)/(mx-mn) for m in means]
    else: norm = [0.5]*len(means)
    ax.plot(betas, norm, 'o-', label=task.split('-')[0], color=color, markersize=4, linewidth=1.5)
ax.set_xlabel(r'$\beta$'); ax.set_ylabel('Normalized Score')
ax.set_title(r'Tasks where $\beta{=}0$ is competitive')
ax.legend(fontsize=7); ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('fig4_beta_ablation.pdf'); plt.savefig('fig4_beta_ablation.png')
plt.close()

# ============================================================
# Figure 5: RL (keep existing)
# ============================================================
print("Figure 5: RL results...")
fig, ax = plt.subplots(1, 1, figsize=(4.0, 2.2))
rl_envs = list(R['rl'].keys())
rl_methods = ['LCB','NoCons','BC']
rl_labels_map = {'LCB': 'Ens-LCB', 'NoCons': 'No Conserv.', 'BC': 'BC'}
rl_colors_map = {'LCB': '#2196F3', 'NoCons': '#9E9E9E', 'BC': '#FF9800'}
x = np.arange(len(rl_envs)); w = 0.22
for mi, method in enumerate(rl_methods):
    means = [R['rl'][e][method]['m'] for e in rl_envs]
    stds = [R['rl'][e][method]['s'] for e in rl_envs]
    ax.bar(x + mi*w - w, means, w, label=rl_labels_map[method],
           color=rl_colors_map[method], edgecolor='white', yerr=stds, capsize=2,
           error_kw={'linewidth':0.8})
ax.set_xticks(x); ax.set_xticklabels(rl_envs); ax.set_ylabel('Return ↑')
ax.set_title('Offline RL: Episode Return')
ax.legend(fontsize=7); ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('fig5_rl.pdf'); plt.savefig('fig5_rl.png')
plt.close()

# ============================================================
# Figure 6: NEW - K ablation
# ============================================================
print("Figure 6: K ablation...")
fig, ax = plt.subplots(1, 1, figsize=(4.0, 2.5))
K_values = [2, 3, 5, 10]
k_colors = ['#E91E63','#2196F3','#4CAF50','#FF9800','#9C27B0']
k_tasks = list(RN['K_ablation'].keys())
for ti, task in enumerate(k_tasks):
    means = [RN['K_ablation'][task][str(kv)]['m'] for kv in K_values]
    mn, mx = min(means), max(means)
    if mx > mn: norm = [(m-mn)/(mx-mn) for m in means]
    else: norm = [0.5]*len(means)
    ax.plot(K_values, norm, 'o-', label=task.split('-')[0], color=k_colors[ti], markersize=4, linewidth=1.5)
ax.set_xlabel('Ensemble Size (K)'); ax.set_ylabel('Normalized Score')
ax.set_title('Ensemble Size Ablation')
ax.legend(fontsize=6.5); ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('fig6_k_ablation.pdf'); plt.savefig('fig6_k_ablation.png')
plt.close()

# ============================================================
# Figure 7: NEW - Calibration
# ============================================================
print("Figure 7: Calibration...")
fig, ax = plt.subplots(1, 1, figsize=(4.5, 2.5))
cal_tasks = list(RN['calibration'].keys())
rho_err = [RN['calibration'][t]['rho_sigma_error'] for t in cal_tasks]
rho_knn = [RN['calibration'][t]['rho_sigma_knn'] for t in cal_tasks]
x = np.arange(len(cal_tasks)); w = 0.35
ax.bar(x - w/2, rho_err, w, label=r'$\rho(\sigma, |error|)$', color='#2196F3', edgecolor='white')
ax.bar(x + w/2, rho_knn, w, label=r'$\rho(\sigma, d_{kNN})$', color='#FF9800', edgecolor='white')
ax.set_xticks(x); ax.set_xticklabels([t.split('-')[0] for t in cal_tasks], fontsize=7)
ax.set_ylabel('Spearman $\\rho$'); ax.set_title('Ensemble Calibration Diagnostics')
ax.legend(fontsize=7); ax.axhline(y=0, color='gray', linewidth=0.3, linestyle='--')
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('fig7_calibration.pdf'); plt.savefig('fig7_calibration.png')
plt.close()

print("All figures generated.")
