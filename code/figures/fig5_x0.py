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

from style import (ACCENT, ACCENT_DK, EGP, EGP_DK, ENS, ENS_DK, FULL, INK,
                   MUTE, RESULTS, SVGP, SVGP_DK, despine, save, use_style)

use_style()

raw = json.load(open(os.path.join(RESULTS, "x0_inversion.json")))
X3 = "x3=1"                       # the audited engine
TASKS = ["Branin-2D", "Styblinski-5D", "Levy-8D", "Rosenbrock-10D",
         "Rastrigin-15D", "Ackley-20D", "Griewank-30D"]
CLASSES = [("ens", "Ensemble", ENS, ENS_DK),
           ("botorchgp", "Exact GP", EGP, EGP_DK),
           ("svgp", "SVGP", SVGP, SVGP_DK)]
OPTS = ["grad", "perturb", "cma"]
OPT_LABEL = {"grad": "grad", "perturb": "pert", "cma": "cma"}

M = np.array([[raw[f"{t}|{s}:{o}|{X3}"]["inversion_rate"]
               for s, _, _, _ in CLASSES for o in OPTS] for t in TASKS])

fig, (ax, bx) = plt.subplots(
    1, 2, figsize=(FULL, 2.25),
    gridspec_kw={"width_ratios": [2.55, 1.0], "wspace": 0.30})

# ---- (a) the 63-cell matrix ---------------------------------------------
cmap = LinearSegmentedColormap.from_list(
    "inv", ["#ffffff", "#FDDDC8", "#F79355", ENS, ENS_DK])
im = ax.imshow(M, cmap=cmap, vmin=0, vmax=1, aspect="auto")

for i in range(M.shape[0]):
    for j in range(M.shape[1]):
        v = M[i, j]
        ax.text(j, i, "·" if v == 0 else f"{v:.2f}".lstrip("0"),
                ha="center", va="center", fontsize=5.6,
                color="white" if v > 0.55 else INK,
                fontweight="bold" if v >= 1.0 else "normal")

ax.set_xticks(range(9))
ax.set_xticklabels([OPT_LABEL[o] for _, _, _, _ in CLASSES for o in OPTS],
                   fontsize=5.8)
ax.set_yticks(range(len(TASKS)))
ax.set_yticklabels(TASKS, fontsize=6.4)
ax.tick_params(length=0)

# class bands under the optimizer ticks
for k, (_, lab, col, edge) in enumerate(CLASSES):
    lo, hi = 3 * k - 0.5, 3 * k + 2.5
    ax.plot([lo + 0.08, hi - 0.08], [len(TASKS) - 0.28] * 2, color=col,
            lw=2.2, clip_on=False, solid_capstyle="butt")
    ax.text(3 * k + 1, len(TASKS) - 0.12, lab, color=edge, fontsize=6.6,
            ha="center", va="top", clip_on=False)

for k in (1, 2):
    ax.axvline(3 * k - 0.5, color="white", lw=1.6)

# the sharpest cell
ax.add_patch(plt.Rectangle((-0.5, -0.5), 1, 1, fill=False, ec=ACCENT,
                           lw=2.2, zorder=5))
ax.add_patch(plt.Rectangle((-0.5, -0.5), 1, 1, fill=False, ec=ACCENT_DK,
                           lw=0.7, zorder=6))
ax.annotate("30/30 seeds invert, and all 128\nreturned designs are worse than\nthe $x_0$ the cell was handed",
            xy=(0.5, 0.46), xytext=(3.7, 3.1), fontsize=6.4, color=ACCENT_DK,
            ha="left", va="center", annotation_clip=False, fontweight="bold",
            arrowprops=dict(arrowstyle="-", lw=0.9, color=ACCENT_DK,
                            shrinkA=1, shrinkB=3))

ax.set_title("(a) inversion rate over 30 seeds, by cell", fontsize=7.2, pad=13)
for s in ax.spines.values():
    s.set_visible(False)

cb = fig.colorbar(im, ax=ax, fraction=0.028, pad=0.015)
cb.set_label("fraction of seeds inverting", fontsize=6.2)
cb.ax.tick_params(labelsize=5.8, length=1.6)
cb.outline.set_visible(False)

# ---- (b) how many tasks each class inverts on ---------------------------
counts = [int(sum(any(M[i, 3 * k + j] > 0 for j in range(3))
                  for i in range(len(TASKS)))) for k in range(3)]

for k, ((_, lab, col, edge), n) in enumerate(zip(CLASSES, counts)):
    lead = k == 0
    bx.barh(2 - k, n, height=0.58, color=col, alpha=0.95, edgecolor=edge,
            lw=0.6, zorder=3)
    bx.text(n - 0.18, 2 - k, f"{n}/7", color="white",
            fontsize=8.0 if lead else 7.0, ha="right", va="center",
            zorder=4, fontweight="bold" if lead else "normal")

bx.set_yticks([2, 1, 0])
bx.set_yticklabels([lab for _, lab, _, _ in CLASSES], fontsize=6.8)
bx.set_xlabel("tasks with an inverting optimizer")
bx.set_xlim(0, 7.4)
bx.set_xticks(range(0, 8, 1))
bx.set_ylim(-0.62, 2.62)
bx.tick_params(axis="y", length=0)
bx.set_title("(b) the inversion is ensemble-specific", fontsize=7.2, pad=13)
despine(bx, grid="x")

save(fig, "fig_x0_inversion")
