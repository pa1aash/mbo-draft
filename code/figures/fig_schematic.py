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
# Vertical layout is specified in POINTS from the top of the canvas, not in
# figure fractions, so the air between stages can be tuned without touching a
# single font size. Every text size below is unchanged from the 3.18in version;
# only the whitespace between and inside the three stages has been taken out.
W, H = COL, 2.56
HPT = H * 72.0
fig = plt.figure(figsize=(W, H))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")


def Y(pt):
    """Figure-fraction y for a distance in points below the canvas top."""
    return 1.0 - pt / HPT


def PT(pt):
    """A height in points expressed as a figure fraction."""
    return pt / HPT


SPINE = 0.61     # vertical centre the stage arrows sit on
LW = 0.7         # standard outline weight

# --- the vertical budget, in points from the top ---------------------------
P_AXIS_LAB = 5.5       # "search routine" centre
P_COL_HEAD = 16.0      # column-header baseline row centre
P_GRID_TOP = 22.0
GRID_ROW = 12.0        # 3 rows: label text is 6.9pt, marker 5.5pt
P_GRID_BOT = P_GRID_TOP + 3 * GRID_ROW
STAGE_GAP = 9.0        # arrow + its right-hand caption sit in here
P_CONF_TOP = P_GRID_BOT + STAGE_GAP
CONF_ROW = 11.6        # 5 rows of 6.9pt text
P_CONF_BOT = P_CONF_TOP + 5 * CONF_ROW
P_DEC_TOP = P_CONF_BOT + STAGE_GAP
P_DEC_TITLE = P_DEC_TOP + 8.0
P_CHIP_TOP = P_DEC_TOP + 19.0
CHIP_H = 17.0          # holds 7.4pt math with sub/superscripts
P_CHIP_BOT = P_CHIP_TOP + CHIP_H
P_CHIP_SUB = P_CHIP_BOT + 6.0
P_DEC_BOT = P_CHIP_SUB + 6.0


def rect(x, y, w, h, ec=BLACK, fc="white", lw=LW, z=2):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec, lw=lw,
                           zorder=z, joinstyle="miter"))


def varrow(y0, y1, color=BLACK, lw=1.0, ms=7):
    ax.add_patch(FancyArrowPatch((SPINE, y0), (SPINE, y1), arrowstyle="-|>",
                                 mutation_scale=ms, color=color, lw=lw,
                                 shrinkA=0, shrinkB=0, zorder=5))


def tick(x, y, up, color=BLACK):
    """A small vertical signed-direction arrow (up or down)."""
    d = PT(4.0)
    y0, y1 = (y - d, y + d) if up else (y + d, y - d)
    ax.add_patch(FancyArrowPatch((x, y0), (x, y1), arrowstyle="-|>",
                                 mutation_scale=6.5, color=color, lw=0.9,
                                 shrinkA=0, shrinkB=0, zorder=6))


# ======================= STAGE 1 -- crossed factorial =====================
gx0, gx1 = 0.315, 0.955
gy_top, gy_bot = Y(P_GRID_TOP), Y(P_GRID_BOT)
cols = ["gradient", "perturbation", "CMA"]
rows = [("Exact GP", EGP), ("Ensemble", ENS), ("SVGP", SVGP)]
cw = (gx1 - gx0) / 3
rh = (gy_top - gy_bot) / 3
ccx = [gx0 + cw * (i + 0.5) for i in range(3)]
rcy = [gy_top - rh * (j + 0.5) for j in range(3)]

# outlined cells (white), colour only as a thin left-edge tag per row
# outlined white cells; a filled class-coloured dot marks every run cell,
# so the grid reads as a fully-crossed 3x3 at a glance
for j, (_, col) in enumerate(rows):
    ry = gy_top - rh * (j + 1)
    for i in range(3):
        rect(gx0 + cw * i, ry, cw, rh)                              # grid cell
        ax.plot(ccx[i], rcy[j], "o", color=col, ms=5.5, mec="none",
                zorder=5)                                           # run marker
# row labels, each with a legend-style class-colour swatch to its left
x_sw, sq_w, sq_h = 0.100, 0.023, 0.024
x_lab = x_sw + sq_w + 0.012
for j, (name, col) in enumerate(rows):
    rect(x_sw, rcy[j] - sq_h / 2, sq_w, sq_h, ec=BLACK, fc=col, lw=0.4, z=4)
    ax.text(x_lab, rcy[j], name, ha="left", va="center", fontsize=6.9,
            color=BLACK)
# column headers (black, roman)
for i, c in enumerate(cols):
    ax.text(ccx[i], Y(P_COL_HEAD), c, ha="center", va="center",
            fontsize=6.4, color=BLACK)
# axis labels (roman, upright)
ax.text((gx0 + gx1) / 2, Y(P_AXIS_LAB), "search routine", ha="center",
        va="center", fontsize=7.2, color=BLACK)
ax.text(0.045, (gy_top + gy_bot) / 2, "surrogate class", ha="center",
        va="center", rotation=90, fontsize=7.2, color=BLACK)

varrow(Y(P_GRID_BOT + 0.5), Y(P_CONF_TOP - 0.5))
ax.text(SPINE + 0.028, Y(P_GRID_BOT + STAGE_GAP / 2), "remove five confounds",
        ha="left", va="center", fontsize=6.0, color=BLACK)

# ======================= STAGE 2 -- five confounds ========================
bx0, bx1 = 0.255, 0.965
by_top, by_bot = Y(P_CONF_TOP), Y(P_CONF_BOT)
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

varrow(Y(P_CONF_BOT + 0.5), Y(P_DEC_TOP - 0.5))
ax.text(SPINE + 0.028, Y(P_CONF_BOT + STAGE_GAP / 2), "two-way ANOVA",
        ha="left", va="center", fontsize=6.0, color=BLACK)

# ======================= STAGE 3 -- decomposition =========================
tx0, tx1 = 0.255, 0.965
ty_top, ty_bot = Y(P_DEC_TOP), Y(P_DEC_BOT)
rect(tx0, ty_bot, tx1 - tx0, ty_top - ty_bot, lw=0.8)
ax.text((tx0 + tx1) / 2, Y(P_DEC_TITLE), "variance decomposition", ha="center",
        va="center", fontsize=7.1, color=BLACK)
chips = [(r"$\eta^2_{\mathrm{surr}}$", "surrogate", BLACK),
         (r"$\eta^2_{\mathrm{opt}}$",  "optimizer", BLACK),
         (r"$\eta^2_{\mathrm{inter}}$", "interaction", ACCENT)]
pad = 0.045
cwid = (tx1 - tx0 - 2 * pad - 2 * 0.02) / 3
sb_top, sb_bot = Y(P_CHIP_TOP), Y(P_CHIP_BOT)
for k, (lab, sub, ec) in enumerate(chips):
    sx = tx0 + pad + (cwid + 0.02) * k
    rect(sx, sb_bot, cwid, sb_top - sb_bot, ec=ec, lw=1.3 if k == 2 else LW, z=4)
    ax.text(sx + cwid / 2, (sb_top + sb_bot) / 2, lab, ha="center",
            va="center", fontsize=7.4, color=BLACK, zorder=6)
    ax.text(sx + cwid / 2, Y(P_CHIP_SUB), sub, ha="center", va="center",
            fontsize=5.9, color=BLACK, zorder=6)

save(fig, "schematic")
