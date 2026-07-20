"""Figure 1 — the methodology schematic.

A single-column, vertical-flow diagram of the *design* (not a result): the
crossed surrogate x optimizer factorial at the top, the five confounds removed
from the scoring path in the middle, and the variance decomposition it yields at
the bottom. Reuses the shared class colours from style.py so a reader who has
seen the results figures recognises Exact GP / Ensemble / SVGP by colour here.

No data is read; this is a pure schematic drawn in figure-fraction coordinates.
"""
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

from style import (ACCENT, EGP, EGP_DK, ENS, ENS_DK, FAINT, GHOST_DK, INK, MUTE,
                   SVGP, SVGP_DK, COL, save, use_style)
import matplotlib.pyplot as plt

use_style()

# --- canvas ---------------------------------------------------------------
W, H = COL, 3.72
fig = plt.figure(figsize=(W, H))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

CENTER = 0.605           # vertical spine the arrows sit on

def down_arrow(y0, y1, label):
    ax.add_patch(FancyArrowPatch((CENTER, y0), (CENTER, y1),
                                 arrowstyle="-|>", mutation_scale=9,
                                 color=INK, lw=1.1, shrinkA=0, shrinkB=0))
    ax.text(CENTER + 0.035, (y0 + y1) / 2, label, ha="left", va="center",
            fontsize=6.3, style="italic", color=MUTE)


# ============================ STAGE 1 — factorial =========================
gx0, gx1 = 0.32, 0.90
gy_top, gy_bot = 0.935, 0.760
cols = ["gradient", "perturbation", "CMA"]
rows = [("Exact GP", EGP, EGP_DK, "botorchgp"),
        ("Ensemble", ENS, ENS_DK, "ens"),
        ("SVGP", SVGP, SVGP_DK, "svgp")]
cw = (gx1 - gx0) / 3
rh = (gy_top - gy_bot) / 3
ccx = [gx0 + cw * (i + 0.5) for i in range(3)]
rcy = [gy_top - rh * (j + 0.5) for j in range(3)]

# cells: each row filled with its surrogate-class colour
for j, (_, col, dk, _key) in enumerate(rows):
    for i in range(3):
        ax.add_patch(Rectangle((ccx[i] - cw * 0.45, rcy[j] - rh * 0.42),
                               cw * 0.90, rh * 0.84, facecolor=col,
                               edgecolor="white", lw=1.1, alpha=0.92,
                               zorder=2))
# row labels (class colours)
for j, (name, col, dk, _key) in enumerate(rows):
    ax.text(gx0 - 0.035, rcy[j], name, ha="right", va="center",
            fontsize=7.2, color=dk, weight="bold")
# column headers
for i, c in enumerate(cols):
    ax.text(ccx[i], gy_top + 0.018, c, ha="center", va="bottom",
            fontsize=6.4, color=INK)
# axis titles
ax.text((gx0 + gx1) / 2, gy_top + 0.055, "search routine", ha="center",
        va="bottom", fontsize=7.4, style="italic", color=INK)
ax.text(0.045, (gy_top + gy_bot) / 2, "surrogate class", ha="center",
        va="center", rotation=90, fontsize=7.2, style="italic", color=INK)

down_arrow(gy_bot - 0.012, 0.706, "remove five\nconfounds")

# ============================ STAGE 2 — confounds =========================
bx0, bx1 = 0.245, 0.965
by_top, by_bot = 0.694, 0.322
ax.add_patch(FancyBboxPatch((bx0, by_bot), bx1 - bx0, by_top - by_bot,
                            boxstyle="round,pad=0.006,rounding_size=0.018",
                            facecolor="white", edgecolor=GHOST_DK, lw=0.8,
                            zorder=1))
ax.text(bx0 + 0.02, by_top - 0.028, "five confounds removed from the scoring path",
        ha="left", va="center", fontsize=6.7, style="italic", color=MUTE)

# (name, direction-text, glyph)  glyph: 'down' 'up' 'kill' 'opt'
confs = [
    ("C1  target scaling",        r"$\eta^2_{\mathrm{surr}}\!\downarrow$", "down"),
    ("C2  candidate/oracle rule", r"$\eta^2_{\mathrm{surr}}\!\uparrow$",   "up"),
    ("C3  ensemble size $K$",     r"$\eta^2_{\mathrm{surr}}\!\downarrow$", "down"),
    ("C4  $\\beta$–$\\sigma$ pessimism match", "kill fired",         "kill"),
    ("C5  query budget",          r"acts on $\eta^2_{\mathrm{opt}}$",      "opt"),
]
ry0, ry1 = by_top - 0.070, by_bot + 0.030
ys = [ry0 - (ry0 - ry1) * k / 4 for k in range(5)]
nx = bx0 + 0.045          # name x
dx = bx1 - 0.045          # direction x (right-aligned)
for (name, dtxt, glyph), y in zip(confs, ys):
    ax.text(nx, y, name, ha="left", va="center", fontsize=7.0, color=INK)
    dcol = ACCENT if glyph == "up" else (INK if glyph == "down" else MUTE)
    ax.text(dx, y, dtxt, ha="right", va="center", fontsize=6.9, color=dcol,
            weight="bold" if glyph in ("up", "down") else "normal")

down_arrow(by_bot - 0.012, 0.245, "two-way\nANOVA")

# ============================ STAGE 3 — decomposition =====================
tx0, tx1 = 0.245, 0.965
ty_top, ty_bot = 0.232, 0.060
ax.add_patch(FancyBboxPatch((tx0, ty_bot), tx1 - tx0, ty_top - ty_bot,
                            boxstyle="round,pad=0.006,rounding_size=0.018",
                            facecolor="white", edgecolor=INK, lw=1.0, zorder=1))
ax.text((tx0 + tx1) / 2, ty_top - 0.030, "variance decomposition", ha="center",
        va="center", fontsize=7.3, color=INK)
chips = [(r"$\eta^2_{\mathrm{surr}}$", GHOST_DK, "surrogate"),
         (r"$\eta^2_{\mathrm{opt}}$", GHOST_DK, "optimizer"),
         (r"$\eta^2_{\mathrm{inter}}$", ACCENT, "interaction")]
cy = ty_bot + 0.058
cwid = (tx1 - tx0 - 0.10) / 3
for k, (lab, ecol, sub) in enumerate(chips):
    cx = tx0 + 0.05 + cwid * (k + 0.5)
    ax.add_patch(FancyBboxPatch((cx - cwid * 0.44, cy - 0.028),
                                cwid * 0.88, 0.056,
                                boxstyle="round,pad=0.004,rounding_size=0.012",
                                facecolor="white", edgecolor=ecol,
                                lw=1.4 if k == 2 else 0.9, zorder=3))
    ax.text(cx, cy + 0.006, lab, ha="center", va="center", fontsize=7.4,
            color=INK)
    ax.text(cx, cy - 0.052, sub, ha="center", va="center", fontsize=5.9,
            color=MUTE)

save(fig, "schematic")
