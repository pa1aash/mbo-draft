"""Shared visual system for the AAAI-27 figures.

One palette, one typeface, one set of sizes, one export path. Every figure
script in this directory imports from here and nothing about a figure's look is
decided locally. A reviewer flipping between figures sees one designed system.

PALETTE. Three saturated, widely-separated hues carry the three surrogate
classes, with fixed roles that never change between figures:

    ENS   #E8480D  vivid orange-red   the K=5 deep ensemble
    EGP   #0A2E7A  deep blue          the exact GP (BoTorch SingleTaskGP)
    SVGP  #1FC5AE  bright teal        the sparse variational GP

They are chosen to survive both colour-vision deficiency and greyscale. Their
relative luminances are 0.218 / 0.034 / 0.433 — monotonically ordered and well
spread, so the three stay distinct when the luminance channel is all a reader
has. Minimum pairwise contrast ratio is 1.80 in normal vision, 2.26 under
simulated deuteranopia and 1.62 under tritanopia; no pair collapses in any of
the three. Each role also carries a darker same-hue variant (ENS_DK etc.) used
only for marker strokes and emphasis, never as a fourth colour.

Saturation goes into the data. The canvas stays white, gridlines stay faint,
and annotation rules stay gray.

Type is serif (STIX/Times) to match the paper body, sized for reproduction at
one \\columnwidth: axis labels ~8pt, ticks ~7pt at final print size.

Export is always a pair — a vector PDF into paper/aaai27/figures_v3/ (what the
paper includes) and a 300-dpi PNG alongside it (for inspection only).
"""
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RESULTS = os.path.join(ROOT, "results")
OUT = os.path.join(ROOT, "paper", "aaai27", "figures_v3")
PNG = os.path.join(OUT, "png")

# --- fixed semantic roles, identical in every figure ----------------------
ENS = "#E8480D"      # deep ensemble        L = 0.218
EGP = "#0A2E7A"      # exact GP             L = 0.034
SVGP = "#1FC5AE"     # sparse variational GP L = 0.433

# same-hue darker variants: marker strokes, emphasis, thin lines on white
ENS_DK = "#8F2A05"
EGP_DK = "#04173F"
SVGP_DK = "#0B7A6C"

GPFAM = EGP          # the GP family read as one class
ACCENT = "#F2A100"   # the thing the figure wants you to look at
ACCENT_DK = "#9E6A00"
INK = "#161616"      # text, axes, primary line work
MUTE = "#8a8a8a"     # annotation rules, reference lines
FAINT = "#dcdcdc"    # gridlines
GHOST = "#c9ccd1"    # background series that are present but not the argument
GHOST_DK = "#9aa0a8"

SURROGATE = {"ens": ENS, "botorchgp": EGP, "svgp": SVGP}
SURROGATE_DK = {"ens": ENS_DK, "botorchgp": EGP_DK, "svgp": SVGP_DK}
SURROGATE_LABEL = {"ens": "Ensemble", "botorchgp": "Exact GP", "svgp": "SVGP"}

# --- opacity tiers: the lead series is the dominant object on the page ----
BAND_LEAD = 0.30     # CI band for the result the figure is about
BAND_BG = 0.13       # CI band for supporting series

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
        "lines.solid_capstyle": "round",

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


def dots(ax, x, y, face, edge, size=3.0, alpha=0.55, lw=0.3, **kw):
    """Scatter that reads as crisp dots rather than a wash.

    A thin same-hue-darker stroke keeps each point's boundary legible where
    points overlap, which is what stops a dense cloud collapsing into a blob.
    """
    return ax.scatter(x, y, s=size, facecolor=face, edgecolor=edge,
                      linewidth=lw, alpha=alpha, **kw)


def marker_line(ax, x, y, colour, edge=None, lw=1.4, ms=3.2, zorder=4, **kw):
    """A trace with stroked markers — the standard emphasis for a result line."""
    ax.plot(x, y, "-", color=colour, lw=lw, zorder=zorder, **kw)
    ax.plot(x, y, "o", color=colour, ms=ms, mec=edge or "white", mew=0.6,
            zorder=zorder + 1)


def running_median(x, y, nbin=9, lo=None, hi=None):
    """Binned median trend — the local law a scatter is meant to show.

    Used instead of LOWESS because these clouds are strongly heteroscedastic
    and a median trace is not dragged around by the extreme tail.
    """
    x, y = np.asarray(x, float), np.asarray(y, float)
    lo = x.min() if lo is None else lo
    hi = x.max() if hi is None else hi
    edges = np.quantile(x[(x >= lo) & (x <= hi)], np.linspace(0, 1, nbin + 1))
    edges = np.unique(edges)
    px, py = [], []
    for a, b in zip(edges[:-1], edges[1:]):
        m = (x >= a) & (x <= b)
        if m.sum() >= 5:
            px.append(np.median(x[m]))
            py.append(np.median(y[m]))
    return np.asarray(px), np.asarray(py)


def halo(ax, x, y, colour, lw=1.6, halo_lw=3.2, zorder=6, **kw):
    """A trend line with a white halo so it survives crossing a dense cloud."""
    ax.plot(x, y, "-", color="white", lw=halo_lw, zorder=zorder,
            solid_capstyle="round")
    ax.plot(x, y, "-", color=colour, lw=lw, zorder=zorder + 1,
            solid_capstyle="round", **kw)


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
