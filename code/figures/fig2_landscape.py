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

from style import (ACCENT, EGP, ENS, FAINT, FULL, INK, MUTE, RESULTS, SVGP,
                   despine, save, use_style)

use_style()
RNG = np.random.default_rng(0)
NBOOT = 2000

raw = json.load(open(os.path.join(RESULTS, "mechanism", "phantom_maxima.json")))
mbo = raw["mbo"]

CLASSES = [("ens", "Ensemble", ENS), ("botorchgp", "Exact GP", EGP),
           ("svgp", "SVGP", SVGP)]
CLASS_KEYS = [c for c, _, _ in CLASSES]

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
    axis.plot(px, py, "-", color=colour, lw=1.4, zorder=6)
    axis.plot(px, py, "o", color=colour, ms=2.6, mec="white", mew=0.6, zorder=7)
    return px, py


def cloud(axis, y, colour, ylab, rho, title):
    axis.scatter(d[~is_cls], y[~is_cls], s=1.5, c=FAINT, lw=0, alpha=0.9,
                 zorder=2, rasterized=True)
    for key, _, col in CLASSES:
        m = arm == key
        axis.scatter(d[m], y[m], s=2.2, c=col, lw=0, alpha=0.5, zorder=3,
                     rasterized=True)
    decile_trace(axis, y, colour)
    axis.set_xlabel(r"$10$-NN distance to $\mathcal{D}$")
    axis.set_ylabel(ylab)
    axis.set_title(title, fontsize=7.2, pad=3)
    axis.text(0.96, 0.93, rf"$\rho={rho:+.3f}$", transform=axis.transAxes,
              ha="right", va="top", fontsize=7.0, color=INK)
    despine(axis)


# ---- (a) distance against true oracle value ------------------------------
cloud(ax, z, INK, r"true oracle value  [sd$(y_\mathcal{D})$]", rho_z,
      "(a) off-support optima are worthless")

# ---- (b) distance against over-prediction --------------------------------
cloud(bx, infl, ACCENT, r"over-prediction  [sd$(y_\mathcal{D})$]", rho_i,
      "(b) and they are over-predicted")

# ---- (c) the non-discrimination ------------------------------------------
edges = np.quantile(d[is_cls], np.linspace(0, 1, 6))
centres = [np.median(d[is_cls][(d[is_cls] >= lo) & (d[is_cls] <= hi)])
           for lo, hi in zip(edges[:-1], edges[1:])]

# (c) is the paper's stated comparison — ensemble against the exact GP. SVGP is
# left off the bin trace because its own distance-value correlation is near zero
# (rho = -0.09) and its Styblinski mass would read as a class contrast it is not.
binned = {}
for key, lab, col in CLASSES[:2]:
    med, lo_b, hi_b = [], [], []
    for lo, hi in zip(edges[:-1], edges[1:]):
        m = (arm == key) & (d >= lo) & (d <= hi)
        v = z[m]
        med.append(np.median(v))
        draws = np.median(RNG.choice(v, (NBOOT, v.size), replace=True), axis=1)
        lo_b.append(np.percentile(draws, 2.5))
        hi_b.append(np.percentile(draws, 97.5))
    binned[key] = med
    cx.fill_between(centres, lo_b, hi_b, color=col, alpha=0.16, lw=0, zorder=2)
    cx.plot(centres, med, "-o", color=col, ms=2.8, mec="white", mew=0.5,
            lw=1.2, zorder=4, label=lab)

# mark the bins where the ensemble sits below the GP: four of five, fifth tied
worse = [e < g for e, g in zip(binned["ens"], binned["botorchgp"])]
for xc, e, g, w in zip(centres, binned["ens"], binned["botorchgp"], worse):
    if w:
        cx.annotate("", xy=(xc, e), xytext=(xc, g),
                    arrowprops=dict(arrowstyle="-", lw=0.5, color=MUTE))
cx.text(0.97, 0.74, f"ensemble lower in\n{sum(worse)} of {len(worse)} bins",
        transform=cx.transAxes, fontsize=6.1, color=INK, ha="right", va="top")

# median distance per class — the classes are matched on the x axis
ymin = cx.get_ylim()[0]
for key, _, col in CLASSES:
    m = arm == key
    cx.plot(np.median(d[m]), ymin, "^", color=col, ms=3.4, clip_on=False,
            zorder=6)

meds = [np.median(d[arm == k]) for k in CLASS_KEYS]
cx.annotate("matched median distance\n" + " / ".join(f"{m:.2f}" for m in meds),
            xy=(float(np.mean(meds)), ymin), xytext=(0.50, 0.05),
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
