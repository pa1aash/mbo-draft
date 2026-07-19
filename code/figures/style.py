"""Shared visual system for the AAAI-27 figures.

One palette, one typeface, one set of sizes, one export path. Every figure
script in this directory imports from here and nothing about a figure's look is
decided locally. A reviewer flipping between figures sees one designed system.

Palette is Wong (Nat. Methods 8, 441, 2011) — colorblind-safe. The three
surrogate classes carry fixed roles across every figure:

    ENS   vermillion   the K=5 deep ensemble
    EGP   blue         the exact GP (BoTorch SingleTaskGP)
    SVGP  bluish green the sparse variational GP

Type is serif (STIX/Times) to match the paper body, sized for reproduction at
one \\columnwidth: axis labels ~8pt, ticks ~7pt at final print size.

Export is always a pair — a vector PDF into paper/aaai27/figures_v3/ (what the
paper includes) and a 300-dpi PNG alongside it (for inspection only).
"""
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RESULTS = os.path.join(ROOT, "results")
OUT = os.path.join(ROOT, "paper", "aaai27", "figures_v3")
PNG = os.path.join(OUT, "png")

# --- Wong colorblind-safe palette -----------------------------------------
WONG = {
    "black": "#000000",
    "orange": "#E69F00",
    "sky": "#56B4E9",
    "green": "#009E73",
    "yellow": "#F0E442",
    "blue": "#0072B2",
    "vermillion": "#D55E00",
    "purple": "#CC79A7",
}

# --- fixed semantic roles, identical in every figure ----------------------
ENS = WONG["vermillion"]     # deep ensemble
EGP = WONG["blue"]           # exact GP
SVGP = WONG["green"]         # sparse variational GP
GPFAM = WONG["blue"]         # the GP family read as one class
ACCENT = WONG["orange"]      # the thing the figure wants you to look at
INK = "#1b1b1b"              # text, axes, primary line work
MUTE = "#8a8a8a"             # annotation rules, reference lines
FAINT = "#d9d9d9"            # gridlines

SURROGATE = {"ens": ENS, "botorchgp": EGP, "svgp": SVGP}
SURROGATE_LABEL = {"ens": "Ensemble", "botorchgp": "Exact GP", "svgp": "SVGP"}

# --- geometry -------------------------------------------------------------
COL = 3.34      # \columnwidth in inches (AAAI two-column)
FULL = 7.0      # \textwidth in inches


def use_style():
    """Install the shared rcParams. Called once at the top of every script."""
    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["STIXGeneral", "Times New Roman", "DejaVu Serif"],
        "mathtext.fontset": "stix",
        "font.size": 7.0,
        "axes.labelsize": 8.0,
        "axes.titlesize": 8.0,
        "xtick.labelsize": 7.0,
        "ytick.labelsize": 7.0,
        "legend.fontsize": 6.6,
        "figure.titlesize": 8.0,

        "axes.edgecolor": INK,
        "axes.labelcolor": INK,
        "text.color": INK,
        "xtick.color": INK,
        "ytick.color": INK,
        "axes.linewidth": 0.6,
        "xtick.major.width": 0.6,
        "ytick.major.width": 0.6,
        "xtick.major.size": 2.6,
        "ytick.major.size": 2.6,
        "xtick.minor.size": 1.4,
        "ytick.minor.size": 1.4,
        "lines.linewidth": 1.2,

        "grid.color": FAINT,
        "grid.linewidth": 0.5,
        "axes.grid": False,

        "legend.frameon": False,
        "legend.handlelength": 1.5,
        "legend.handletextpad": 0.5,
        "legend.borderaxespad": 0.3,
        "legend.labelspacing": 0.3,

        "figure.dpi": 150,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.012,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    })


def despine(ax, grid="y"):
    """Drop the top and right spines; light gridlines only where they read."""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    if grid in ("y", "both"):
        ax.yaxis.grid(True, color=FAINT, lw=0.5, zorder=0)
    if grid in ("x", "both"):
        ax.xaxis.grid(True, color=FAINT, lw=0.5, zorder=0)
    ax.set_axisbelow(True)


def save(fig, name):
    """Export the vector PDF the paper includes plus a 300-dpi PNG to inspect."""
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(PNG, exist_ok=True)
    pdf = os.path.join(OUT, name + ".pdf")
    png = os.path.join(PNG, name + ".png")
    fig.savefig(pdf)
    fig.savefig(png, dpi=300)
    plt.close(fig)
    print("wrote", os.path.relpath(pdf, ROOT), "+", os.path.relpath(png, ROOT))
