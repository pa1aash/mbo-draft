"""Generate all publication-quality figures for the ICML workshop paper."""
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyBboxPatch

plt.rcParams.update({
    'font.size': 9, 'axes.labelsize': 10, 'axes.titlesize': 10,
    'xtick.labelsize': 8, 'ytick.labelsize': 8, 'legend.fontsize': 7.5,
    'figure.dpi': 300, 'savefig.dpi': 300, 'savefig.bbox': 'tight',
    'font.family': 'serif',
})

with open('results.json') as f:
    R = json.load(f)

# ============================================================
# Figure 1: Offline MBO comparison (bar chart)
# ============================================================
print("Figure 1: Offline MBO comparison...")

tasks_order = ['Branin-2D','Styblinski-5D','Levy-8D','Rosenbrock-10D','Rastrigin-15D','Ackley-20D','Griewank-30D']
short_names = ['Branin\n(2D)','Styblinski\n(5D)','Levy\n(8D)','Rosenbrock\n(10D)','Rastrigin\n(15D)','Ackley\n(20D)','Griewank\n(30D)']
methods = ['lcb','coms','grad_ascent']
labels = ['Ens-LCB (Ours)','COMs','Grad. Ascent']
colors = ['#2196F3','#FF9800','#9E9E9E']

fig, ax = plt.subplots(1, 1, figsize=(7.0, 2.8))
x = np.arange(len(tasks_order))
w = 0.25

# Normalize per task for visual clarity (use ranks instead of raw values since scales differ)
for i, (method, label, color) in enumerate(zip(methods, labels, colors)):
    means = [R['mbo'][t][method]['p100_m'] for t in tasks_order]
    stds = [R['mbo'][t][method]['p100_s'] for t in tasks_order]
    ax.bar(x + i*w - w, means, w, label=label, color=color, edgecolor='white', linewidth=0.5,
           yerr=stds, capsize=2, error_kw={'linewidth':0.8})

ax.set_xticks(x)
ax.set_xticklabels(short_names, fontsize=7)
ax.set_ylabel('Oracle Score (100th pct.) ↑')
ax.set_title('Offline MBO: 100th Percentile Oracle Score')
ax.legend(loc='lower left', frameon=True, framealpha=0.9)
ax.axhline(y=0, color='gray', linewidth=0.3, linestyle='--')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('fig1_offline_mbo.pdf')
plt.savefig('fig1_offline_mbo.png')
plt.close()

# ============================================================
# Figure 2: Average rank across tasks
# ============================================================
print("Figure 2: Average rank...")

# Compute ranks per task (higher score = rank 1)
ranks = {m: [] for m in methods}
for t in tasks_order:
    scores = [(R['mbo'][t][m]['p100_m'], m) for m in methods]
    scores.sort(reverse=True)  # higher is better
    for rank, (_, m) in enumerate(scores, 1):
        ranks[m].append(rank)

fig, ax = plt.subplots(1, 1, figsize=(3.5, 2.2))
avg_ranks = {m: np.mean(ranks[m]) for m in methods}
bars = ax.barh([labels[methods.index(m)] for m in ['lcb','coms','grad_ascent']],
               [avg_ranks[m] for m in ['lcb','coms','grad_ascent']],
               color=colors, edgecolor='white')
for bar, m in zip(bars, ['lcb','coms','grad_ascent']):
    ax.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2,
            f'{avg_ranks[m]:.2f}', va='center', fontsize=8)
ax.set_xlabel('Average Rank (↓ better)')
ax.set_title('Average Rank Across 7 Tasks')
ax.set_xlim(0, 3.5)
ax.invert_xaxis()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('fig2_avg_rank.pdf')
plt.savefig('fig2_avg_rank.png')
plt.close()

# ============================================================
# Figure 3: Offline-to-Online MBO (main contribution)
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
        imps = []
        imp_stds = []
        for k in budgets:
            d = R['o2o'][task][str(k)].get(method, {})
            imps.append(d.get('imp_m', 0))
            imp_stds.append(d.get('imp_s', 0))
        ax.errorbar(budgets, imps, yerr=imp_stds, marker='o', markersize=4,
                    label=label, color=color, linewidth=1.5, capsize=3, capthick=1)

    ax.axhline(y=0, color='gray', linewidth=0.5, linestyle='--')
    ax.set_xlabel('Online Evaluation Budget (k)')
    ax.set_ylabel('Improvement over Offline (%)')
    ax.set_title(task)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    if idx == 0:
        ax.legend(fontsize=6.5, loc='upper left')

plt.suptitle('Offline-to-Online MBO: Score Improvement vs. Online Budget', fontsize=10, y=1.02)
plt.tight_layout()
plt.savefig('fig3_o2o_mbo.pdf')
plt.savefig('fig3_o2o_mbo.png')
plt.close()

# ============================================================
# Figure 4: Beta ablation
# ============================================================
print("Figure 4: Beta ablation...")

abl_tasks = list(R['abl']['beta'].keys())
abl_colors = ['#4CAF50','#2196F3','#9C27B0']
betas = [0.0, 0.5, 1.0, 2.0, 5.0]

fig, ax = plt.subplots(1, 1, figsize=(4.0, 2.5))
for ti, (task, color) in enumerate(zip(abl_tasks, abl_colors)):
    means = [R['abl']['beta'][task][str(b)]['m'] for b in betas]
    stds = [R['abl']['beta'][task][str(b)]['s'] for b in betas]
    # Normalize for display (scale to [0, 1] per task)
    mn, mx = min(means), max(means)
    if mx > mn:
        norm = [(m - mn) / (mx - mn) for m in means]
    else:
        norm = [0.5]*len(means)
    ax.plot(betas, norm, 'o-', label=task.split('-')[0], color=color, markersize=4, linewidth=1.5)

ax.set_xlabel(r'Conservatism Strength ($\beta$)')
ax.set_ylabel('Normalized Score (0=worst, 1=best)')
ax.set_title(r'Effect of $\beta$ on Optimization Quality')
ax.legend(fontsize=7)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('fig4_beta_ablation.pdf')
plt.savefig('fig4_beta_ablation.png')
plt.close()

# ============================================================
# Figure 5: RL results
# ============================================================
print("Figure 5: RL results...")

fig, ax = plt.subplots(1, 1, figsize=(4.0, 2.2))
rl_envs = list(R['rl'].keys())
rl_methods = ['LCB','NoCons','BC']
rl_labels_map = {'LCB': 'Ens-LCB (Ours)', 'NoCons': 'No Conserv.', 'BC': 'Behav. Cloning'}
rl_colors_map = {'LCB': '#2196F3', 'NoCons': '#9E9E9E', 'BC': '#FF9800'}

x = np.arange(len(rl_envs))
w = 0.22
for mi, method in enumerate(rl_methods):
    means = [R['rl'][e][method]['m'] for e in rl_envs]
    stds = [R['rl'][e][method]['s'] for e in rl_envs]
    ax.bar(x + mi*w - w, means, w, label=rl_labels_map[method],
           color=rl_colors_map[method], edgecolor='white', yerr=stds, capsize=2,
           error_kw={'linewidth':0.8})

ax.set_xticks(x)
ax.set_xticklabels(rl_envs)
ax.set_ylabel('Return ↑')
ax.set_title('Offline RL: Episode Return')
ax.legend(fontsize=7)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('fig5_rl.pdf')
plt.savefig('fig5_rl.png')
plt.close()

print("All figures generated.")
