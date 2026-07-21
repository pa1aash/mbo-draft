"""FIG 5 — the LCB ranks hallucinations above real designs it already holds.

Each cell is seeded with the best design in the offline data. An "inversion" is
a seed whose returned set is worse under the ground-truth oracle than that
starting design: the surrogate's own acquisition ranked what it invented above
what it was given.

(a) Inversion rate over 30 seeds for all 63 (task, surrogate, optimizer) cells
    on the audited engine (X1 and X3 on). The ensemble block lights up; the
    exact GP's is almost entirely dark.

(b) Tasks carrying at least one inverting optimizer: 7/7 for the ensemble,
    3/7 for SVGP, 2/7 for the exact GP.

The sharpest single cell is Branin-2D under ensemble gradient ascent: every one
of 30 seeds inverts, and on average 100% of the 128 returned designs are worse
than the x0 the cell was handed.

Reads results/x0_inversion.json (30 seeds, K=5, beta=2, TOP=128).
"""
import json
import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

from style import (ACCENT, ACCENT_DK, COL, EGP, EGP_DK, ENS, ENS_DK, INK,
                   MUTE, RESULTS, SVGP, SVGP_DK, despine, save, use_style)

use_style()
# include scale at one \columnwidth is 0.961, so the authored floor is 7.8pt:
# 7.8*0.961 = 7.11pt printed, clear of the 7pt floor for every glyph.
plt.rcParams.update({"xtick.labelsize": 7.8, "ytick.labelsize": 7.8})

raw = json.load(open(os.path.join(RESULTS, "x0_inversion.json")))
X3 = "x3=1"                       # the audited engine
TASKS = ["Branin-2D", "Styblinski-5D", "Levy-8D", "Rosenbrock-10D",
         "Rastrigin-15D", "Ackley-20D", "Griewank-30D"]
CLASSES = [("ens", "Ensemble", ENS, ENS_DK),
           ("botorchgp", "Exact GP", EGP, EGP_DK),
           ("svgp", "SVGP", SVGP, SVGP_DK)]
OPTS = ["grad", "perturb", "cma"]
OPT_LABEL = {"grad": "grad", "perturb": "pert", "cma": "cma"}
TASK_SHORT = ["Branin", "Styblinski", "Levy", "Rosenbrock",
              "Rastrigin", "Ackley", "Griewank"]

M = np.array([[raw[f"{t}|{s}:{o}|{X3}"]["inversion_rate"]
               for s, _, _, _ in CLASSES for o in OPTS] for t in TASKS])

# Authored at one \columnwidth, the size it is reproduced at, so nothing has to
# be scaled down on the page: every label below is >=7pt as drawn and >=7pt as
# printed. The two panels stack because side-by-side at 240pt cannot hold 7pt
# type in nine matrix columns and a bar panel at once.
fig, (ax, bx) = plt.subplots(
    2, 1, figsize=(COL, 2.18),
    gridspec_kw={"height_ratios": [2.62, 1.0], "hspace": 0.58})

# ---- (a) the 63-cell matrix ---------------------------------------------
cmap = LinearSegmentedColormap.from_list(
    "inv", ["#ffffff", "#FDDDC8", "#F79355", ENS, ENS_DK])
im = ax.imshow(M, cmap=cmap, vmin=0, vmax=1, aspect="auto")

for i in range(M.shape[0]):
    for j in range(M.shape[1]):
        v = M[i, j]
        ax.text(j, i, "·" if v == 0 else f"{v:.2f}".lstrip("0"),
                ha="center", va="center", fontsize=7.8,
                color="white" if v > 0.55 else INK,
                fontweight="bold" if v >= 1.0 else "normal")

ax.set_xticks(range(9))
ax.set_xticklabels([OPT_LABEL[o] for _, _, _, _ in CLASSES for o in OPTS],
                   fontsize=7.8)
ax.set_yticks(range(len(TASKS)))
ax.set_yticklabels(TASK_SHORT, fontsize=7.8)
ax.tick_params(length=0)

# class bands under the optimizer ticks
for k, (_, lab, col, edge) in enumerate(CLASSES):
    lo, hi = 3 * k - 0.5, 3 * k + 2.5
    ax.plot([lo + 0.08, hi - 0.08], [len(TASKS) - 0.28] * 2, color=col,
            lw=2.2, clip_on=False, solid_capstyle="butt")
    ax.text(3 * k + 1, len(TASKS) - 0.10, lab, color=edge, fontsize=7.8,
            ha="center", va="top", clip_on=False)

for k in (1, 2):
    ax.axvline(3 * k - 0.5, color="white", lw=1.6)

# the sharpest cell
ax.add_patch(plt.Rectangle((-0.5, -0.5), 1, 1, fill=False, ec=ACCENT,
                           lw=2.2, zorder=5))
ax.add_patch(plt.Rectangle((-0.5, -0.5), 1, 1, fill=False, ec=ACCENT_DK,
                           lw=0.7, zorder=6))
ax.annotate("30/30 seeds invert;\nall 128 worse than the seed",
            xy=(0.55, 0.32), xytext=(3.15, 2.55), fontsize=7.8, color=ACCENT_DK,
            ha="left", va="center", annotation_clip=False, fontweight="bold",
            arrowprops=dict(arrowstyle="-", lw=0.9, color=ACCENT_DK,
                            shrinkA=1, shrinkB=3))

ax.set_title("(a) inversion rate over 30 seeds, by cell", fontsize=7.8, pad=12)
for s in ax.spines.values():
    s.set_visible(False)

cb = fig.colorbar(im, ax=ax, fraction=0.030, pad=0.020)
cb.set_label("fraction inverting", fontsize=7.8)
cb.ax.tick_params(labelsize=7.8, length=1.6)
cb.outline.set_visible(False)

# ---- (b) how many tasks each class inverts on ---------------------------
counts = [int(sum(any(M[i, 3 * k + j] > 0 for j in range(3))
                  for i in range(len(TASKS)))) for k in range(3)]

for k, ((_, lab, col, edge), n) in enumerate(zip(CLASSES, counts)):
    lead = k == 0
    bx.barh(2 - k, n, height=0.58, color=col, alpha=0.95, edgecolor=edge,
            lw=0.6, zorder=3)
    bx.text(n - 0.18, 2 - k, f"{n}/7", color="white",
            fontsize=9.0 if lead else 7.8, ha="right", va="center",
            zorder=4, fontweight="bold" if lead else "normal")

bx.set_yticks([2, 1, 0])
bx.set_yticklabels([lab for _, lab, _, _ in CLASSES], fontsize=7.8)
bx.set_xlabel("tasks with an inverting optimizer")
bx.set_xlim(0, 7.8)
bx.set_xticks(range(0, 8, 1))
bx.set_ylim(-0.62, 2.62)
bx.tick_params(axis="y", length=0)
bx.set_title("(b) the inversion is ensemble-specific", fontsize=7.8, pad=6)
despine(bx, grid="x")

save(fig, "fig_x0_inversion")
