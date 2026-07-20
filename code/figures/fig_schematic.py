"""Figure 1 -- the methodology schematic (formal style).

A single-column, vertical-flow architecture diagram of the *design*: the crossed
surrogate x optimizer factorial (top), the five confounds removed from the
scoring path (middle), and the variance decomposition it yields (bottom).

Formal conventions: sharp-cornered rectangles with thin black outlines, upright
roman text, black orthogonal arrows, white fills. Colour (from style.py) is used
only as a thin left-edge tag per surrogate class, for the C2 strengthening
arrow, and for the interaction output box. No data is read -- a pure schematic.
"""
from matplotlib.patches import FancyArrowPatch, Rectangle

from style import ACCENT, EGP, ENS, INK, SVGP, COL, save, use_style
import matplotlib.pyplot as plt

use_style()
plt.rcParams.update({"font.style": "normal"})   # upright roman everywhere

BLACK = INK
W, H = COL, 3.18
fig = plt.figure(figsize=(W, H))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

SPINE = 0.61     # vertical centre the stage arrows sit on
LW = 0.7         # standard outline weight


def rect(x, y, w, h, ec=BLACK, fc="white", lw=LW, z=2):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec, lw=lw,
                           zorder=z, joinstyle="miter"))


def varrow(y0, y1, color=BLACK, lw=1.0, ms=7):
    ax.add_patch(FancyArrowPatch((SPINE, y0), (SPINE, y1), arrowstyle="-|>",
                                 mutation_scale=ms, color=color, lw=lw,
                                 shrinkA=0, shrinkB=0, zorder=5))


def tick(x, y, up, color=BLACK):
    """A small vertical signed-direction arrow (up or down)."""
    y0, y1 = (y - 0.020, y + 0.020) if up else (y + 0.020, y - 0.020)
    ax.add_patch(FancyArrowPatch((x, y0), (x, y1), arrowstyle="-|>",
                                 mutation_scale=6.5, color=color, lw=0.9,
                                 shrinkA=0, shrinkB=0, zorder=6))


# ======================= STAGE 1 -- crossed factorial =====================
gx0, gx1 = 0.315, 0.955
gy_top, gy_bot = 0.955, 0.775
cols = ["gradient", "perturbation", "CMA"]
rows = [("Exact GP", EGP), ("Ensemble", ENS), ("SVGP", SVGP)]
cw = (gx1 - gx0) / 3
rh = (gy_top - gy_bot) / 3
ccx = [gx0 + cw * (i + 0.5) for i in range(3)]
rcy = [gy_top - rh * (j + 0.5) for j in range(3)]

# outlined cells (white), colour only as a thin left-edge tag per row
tag_w = 0.017
for j, (_, col) in enumerate(rows):
    ry = gy_top - rh * (j + 1)
    rect(gx0 - tag_w, ry, tag_w, rh, ec=col, fc=col, lw=0.4, z=3)   # class tag
    for i in range(3):
        rect(gx0 + cw * i, ry, cw, rh)                              # grid cell
# row labels (black, roman)
for j, (name, _) in enumerate(rows):
    ax.text(gx0 - tag_w - 0.016, rcy[j], name, ha="right", va="center",
            fontsize=6.9, color=BLACK)
# column headers (black, roman)
for i, c in enumerate(cols):
    ax.text(ccx[i], gy_top + 0.016, c, ha="center", va="bottom",
            fontsize=6.4, color=BLACK)
# axis labels (roman, upright)
ax.text((gx0 + gx1) / 2, gy_top + 0.050, "search routine", ha="center",
        va="bottom", fontsize=7.2, color=BLACK)
ax.text(0.045, (gy_top + gy_bot) / 2, "surrogate class", ha="center",
        va="center", rotation=90, fontsize=7.2, color=BLACK)

varrow(gy_bot - 0.006, 0.726)
ax.text(SPINE + 0.028, (gy_bot - 0.006 + 0.726) / 2, "remove five confounds",
        ha="left", va="center", fontsize=6.0, color=BLACK)

# ======================= STAGE 2 -- five confounds ========================
bx0, bx1 = 0.255, 0.965
by_top, by_bot = 0.716, 0.408
rect(bx0, by_bot, bx1 - bx0, by_top - by_bot, lw=0.8)
nrows = 5
rrh = (by_top - by_bot) / nrows
for k in range(1, nrows):                                  # internal rules
    yr = by_top - rrh * k
    ax.plot([bx0, bx1], [yr, yr], color=BLACK, lw=0.4, zorder=3)
confs = [
    ("C1", "target scaling",          "down"),
    ("C2", "candidate/oracle rule",   "up"),
    ("C3", r"ensemble size $K$",      "down"),
    ("C4", r"$\beta$–$\sigma$ pessimism match", "kill"),
    ("C5", "query budget",            "opt"),
]
cx = bx0 + 0.028      # tag column
nx = bx0 + 0.085      # name column
dx = bx1 - 0.030      # direction column (right edge)
for k, (tag, name, glyph) in enumerate(confs):
    y = by_top - rrh * (k + 0.5)
    ax.text(cx, y, tag, ha="left", va="center", fontsize=6.8, color=BLACK)
    ax.text(nx, y, name, ha="left", va="center", fontsize=6.9, color=BLACK)
    if glyph == "down":
        tick(dx, y, up=False)
    elif glyph == "up":
        tick(dx, y, up=True, color=ACCENT)
    elif glyph == "kill":
        ax.text(dx, y, "kill fired", ha="right", va="center", fontsize=6.6,
                color=BLACK)
    else:
        ax.text(dx, y, "acts on optimizer axis", ha="right", va="center",
                fontsize=6.6, color=BLACK)

varrow(by_bot - 0.006, 0.372)
ax.text(SPINE + 0.028, (by_bot - 0.006 + 0.372) / 2, "two-way ANOVA",
        ha="left", va="center", fontsize=6.0, color=BLACK)

# ======================= STAGE 3 -- decomposition =========================
tx0, tx1 = 0.255, 0.965
ty_top, ty_bot = 0.362, 0.072
rect(tx0, ty_bot, tx1 - tx0, ty_top - ty_bot, lw=0.8)
ax.text((tx0 + tx1) / 2, ty_top - 0.034, "variance decomposition", ha="center",
        va="center", fontsize=7.1, color=BLACK)
chips = [(r"$\eta^2_{\mathrm{surr}}$", "surrogate", BLACK),
         (r"$\eta^2_{\mathrm{opt}}$",  "optimizer", BLACK),
         (r"$\eta^2_{\mathrm{inter}}$", "interaction", ACCENT)]
pad = 0.045
cwid = (tx1 - tx0 - 2 * pad - 2 * 0.02) / 3
sb_top, sb_bot = ty_top - 0.098, ty_bot + 0.078
for k, (lab, sub, ec) in enumerate(chips):
    sx = tx0 + pad + (cwid + 0.02) * k
    rect(sx, sb_bot, cwid, sb_top - sb_bot, ec=ec, lw=1.3 if k == 2 else LW, z=4)
    ax.text(sx + cwid / 2, (sb_top + sb_bot) / 2, lab, ha="center",
            va="center", fontsize=7.4, color=BLACK, zorder=6)
    ax.text(sx + cwid / 2, sb_bot - 0.028, sub, ha="center", va="center",
            fontsize=5.9, color=BLACK, zorder=6)

save(fig, "schematic")
