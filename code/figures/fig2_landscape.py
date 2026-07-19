"""FIG 2 — the seventh elimination, made visible.

Every returned optimum (5,040 = 7 tasks x 24 arms x 30 seeds) instrumented with
its 10-NN distance to the offline data, its true oracle value, and its
over-prediction against that oracle. Three panels, three separate points:

  (a) distance predicts worthlessness, rho = -0.818 pooled
  (b) distance predicts over-prediction, rho = +0.758 pooled
  (c) and distance does not discriminate between surrogate classes: they sit at
      the same median distance and the ensemble is still worse in oracle value
      at matched distance, in four of five bins, tied in the fifth

Panels (a) and (b) carry all eight arms, which is the n the paper cites. The
five gpm_* arms are the prior-mean probes of the PM2 limb; they are part of the
pooled statistic but carry no surrogate-class meaning, so they are gray in (a)
and (b) and absent from (c), which is a between-class comparison.

Reads results/mechanism/phantom_maxima.json.
"""
import json
import os

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import spearmanr

from style import (ACCENT, ACCENT_DK, BAND_BG, BAND_LEAD, EGP, EGP_DK, ENS,
                   ENS_DK, FULL, GHOST, GHOST_DK, INK, MUTE, RESULTS, SVGP,
                   SVGP_DK, despine, dots, halo, running_median, save,
                   use_style)

use_style()
RNG = np.random.default_rng(0)
NBOOT = 2000

raw = json.load(open(os.path.join(RESULTS, "mechanism", "phantom_maxima.json")))
mbo = raw["mbo"]

CLASSES = [("ens", "Ensemble", ENS, ENS_DK),
           ("botorchgp", "Exact GP", EGP, EGP_DK),
           ("svgp", "SVGP", SVGP, SVGP_DK)]
# painted back to front: the supporting probes, then the two GPs, then the
# ensemble on top — the class the argument is about is never occluded.
PAINT = ["svgp", "botorchgp", "ens"]
CLASS_KEYS = [c for c, _, _, _ in CLASSES]
COL_OF = {c: (f, e) for c, _, f, e in CLASSES}

d, z, infl, arm = [], [], [], []
for task in mbo:
    for cell, v in mbo[task].items():
        s = v["star"]
        d += s["dhat"]["all"]
        z += s["z"]["all"]
        infl += s["infl"]["all"]
        arm += [cell.split(":")[0]] * len(s["dhat"]["all"])

d, z, infl, arm = map(np.asarray, (d, z, infl, arm))
is_cls = np.isin(arm, CLASS_KEYS)
rho_z = spearmanr(d, z).statistic
rho_i = spearmanr(d, infl).statistic

fig, (ax, bx, cx) = plt.subplots(
    1, 3, figsize=(FULL, 2.15),
    gridspec_kw={"width_ratios": [1.0, 1.0, 1.05], "wspace": 0.30})


def decile_trace(axis, y, colour):
    """Pooled decile medians — the landscape law, drawn over the cloud."""
    edges = np.quantile(d, np.linspace(0, 1, 11))
    px, py = [], []
    for lo, hi in zip(edges[:-1], edges[1:]):
        m = (d >= lo) & (d <= hi)
        px.append(np.median(d[m]))
        py.append(np.median(y[m]))
    axis.plot(px, py, "-", color="white", lw=3.4, zorder=10,
              solid_capstyle="round")
    axis.plot(px, py, "-", color=colour, lw=1.9, zorder=11,
              solid_capstyle="round")
    axis.plot(px, py, "o", color=colour, ms=2.8, mec="white", mew=0.7,
              zorder=12)
    return px, py


def cloud(axis, y, colour, ylab, rho, title):
    # background probes: present, de-emphasised, never competing for attention
    dots(axis, d[~is_cls], y[~is_cls], GHOST, GHOST_DK, size=0.7, alpha=0.26,
         lw=0.10, zorder=2, rasterized=True)
    # the three classes, painted back to front, small and stroked so that
    # overlapping points stay individually legible instead of washing together
    for z0, key in enumerate(PAINT):
        m = arm == key
        face, edge = COL_OF[key]
        dots(axis, d[m], y[m], face, edge, size=1.2, alpha=0.32, lw=0.18,
             zorder=3 + z0, rasterized=True)
    decile_trace(axis, y, colour)
    axis.set_xlabel(r"$10$-NN distance to $\mathcal{D}$")
    axis.set_ylabel(ylab)
    axis.set_title(title, fontsize=7.2, pad=3)
    axis.text(0.96, 0.93, rf"$\rho={rho:+.3f}$", transform=axis.transAxes,
              ha="right", va="top", fontsize=8.0, color=INK,
              fontweight="bold")
    despine(axis)


# ---- (a) distance against true oracle value ------------------------------
cloud(ax, z, INK, r"true oracle value  [sd$(y_\mathcal{D})$]", rho_z,
      "(a) off-support optima are worthless")

# ---- (b) distance against over-prediction --------------------------------
cloud(bx, infl, ACCENT_DK, r"over-prediction  [sd$(y_\mathcal{D})$]", rho_i,
      "(b) and they are over-predicted")

# ---- (c) the non-discrimination ------------------------------------------
edges = np.quantile(d[is_cls], np.linspace(0, 1, 6))
centres = [np.median(d[is_cls][(d[is_cls] >= lo) & (d[is_cls] <= hi)])
           for lo, hi in zip(edges[:-1], edges[1:])]

# (c) is the paper's stated comparison — ensemble against the exact GP. SVGP is
# left off the bin trace because its own distance-value correlation is near zero
# (rho = -0.09) and its Styblinski mass would read as a class contrast it is not.
binned = {}
for key, lab, col, edge in CLASSES[:2]:
    med, lo_b, hi_b = [], [], []
    for lo, hi in zip(edges[:-1], edges[1:]):
        m = (arm == key) & (d >= lo) & (d <= hi)
        v = z[m]
        med.append(np.median(v))
        draws = np.median(RNG.choice(v, (NBOOT, v.size), replace=True), axis=1)
        lo_b.append(np.percentile(draws, 2.5))
        hi_b.append(np.percentile(draws, 97.5))
    binned[key] = med
    lead = key == "ens"
    cx.fill_between(centres, lo_b, hi_b, color=col,
                    alpha=BAND_LEAD if lead else BAND_BG, lw=0,
                    zorder=3 if lead else 2)
    cx.plot(centres, med, "-", color=col, lw=2.0 if lead else 1.5,
            zorder=6 if lead else 5)
    cx.plot(centres, med, "o", color=col, ms=3.4 if lead else 3.0, mec=edge,
            mew=0.8, zorder=7 if lead else 5, label=lab)

# mark the bins where the ensemble sits below the GP: four of five, fifth tied
worse = [e < g for e, g in zip(binned["ens"], binned["botorchgp"])]
for xc, e, g, w in zip(centres, binned["ens"], binned["botorchgp"], worse):
    if w:
        cx.annotate("", xy=(xc, e), xytext=(xc, g),
                    arrowprops=dict(arrowstyle="-", lw=0.9, color=ENS_DK,
                                    alpha=0.55))
cx.text(0.97, 0.74, f"ensemble lower in\n{sum(worse)} of {len(worse)} bins",
        transform=cx.transAxes, fontsize=6.6, color=ENS_DK, ha="right",
        va="top", fontweight="bold")

# median distance per class — the classes are matched on the x axis
ymin = cx.get_ylim()[0]
for key, _, col, edge in CLASSES:
    m = arm == key
    cx.plot(np.median(d[m]), ymin, "^", color=col, ms=4.0, mec=edge, mew=0.6,
            clip_on=False, zorder=8)

meds = [np.median(d[arm == k]) for k in CLASS_KEYS]
cx.annotate("matched median distance\n" + " / ".join(f"{m:.2f}" for m in meds),
            xy=(float(np.mean(meds)), ymin), xytext=(0.30, 0.05),
            textcoords="axes fraction", fontsize=6.1, color=INK,
            ha="center", va="bottom",
            arrowprops=dict(arrowstyle="-", lw=0.5, color=MUTE,
                            shrinkA=1, shrinkB=2))

cx.set_xlabel(r"$10$-NN distance to $\mathcal{D}$ (quintile)")
cx.set_ylabel(r"median oracle value  [sd$(y_\mathcal{D})$]")
cx.set_title("(c) distance does not discriminate", fontsize=7.2, pad=3)
cx.legend(loc="upper right", fontsize=6.2, borderpad=0.2, labelspacing=0.25)
despine(cx)

save(fig, "fig_landscape")
