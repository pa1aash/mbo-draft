"""FIG — the four engine corners, and why they do not compose.

The corners are drawn as four MEASURED LEVELS with their bootstrap intervals,
never as a cascade of bars from a baseline. That is deliberate: bars anchored to
a common origin read as an additive budget, and these corrections are not
additive. X1 alone moves eta2_surr down 0.084 and X3 alone moves it up 0.083 —
which would net to about zero — while the corner where both are applied sits
0.038 ABOVE the published one. The joint correction is not the sum of the
separate ones, and the figure has to make that visible rather than hide it.

The second thing the figure has to show is KB5: the four intervals overlap so
heavily that no corner is separable from another at n=7. The shaded band is the
INTERSECTION of all four intervals — a region every corner's CI contains. Its
existence is the non-resolvability result.

Ensemble size K sits in its own panel. It is a confound on a different axis, not
a fifth corner, and it carries no bootstrap interval because the sweep was not
bootstrapped per K — so its points are drawn open, in a separate panel, and are
never placed on the corner axis.

Confounds 4 and 5 appear in the caption only. Confound 4's aggregate kill
criterion fired, so it has no grid-wide eta2_surr effect; Confound 5 acts on
eta2_opt. Drawing either as an empty row in the main plot would read as an
omission rather than as a measured null.

Reads results/bootstrap_eta_corners.json, results/kbeta/kbeta_analysis.json.
"""
import json
import os

import matplotlib.pyplot as plt

from style import (ACCENT, ACCENT_DK, COL, EGP, EGP_DK, ENS, ENS_DK, GHOST,
                   GHOST_DK, INK, MUTE, RESULTS, despine, save, use_style)

use_style()

corners = json.load(open(os.path.join(RESULTS, "bootstrap_eta_corners.json")))
kb = json.load(open(os.path.join(RESULTS, "kbeta", "kbeta_analysis.json")))
by_k = kb["KB1"]["by_K"]

# corner -> (label, what is on, face, edge)
ORDER = [
    ("off_off", "off\noff", "published", GHOST, GHOST_DK),
    ("on_off", "on\noff", "X1 only", ENS, ENS_DK),
    ("off_on", "off\non", "X3 only", EGP, EGP_DK),
    ("on_on", "on\non", "corrected", ACCENT, ACCENT_DK),
]

pt = {k: corners[k]["eta2"]["point"]["surr"] for k, *_ in ORDER}
ci = {k: corners[k]["eta2"]["surr"]["ci95"] for k, *_ in ORDER}

BASE = pt["off_off"]
D_X1 = pt["on_off"] - BASE          # -0.084, down
D_X3 = pt["off_on"] - BASE          # +0.083, up
D_NET = pt["on_on"] - BASE          # +0.038, the joint correction

# the region every corner's interval contains — KB5 made concrete
SHARED_LO = max(c[0] for c in ci.values())
SHARED_HI = min(c[1] for c in ci.values())

fig, (ax, kx) = plt.subplots(
    1, 2, figsize=(COL, 2.15), sharey=True,
    gridspec_kw={"width_ratios": [2.25, 1.0], "wspace": 0.10})

# ---- the shared interval: no corner is separable from another --------------
ax.axhspan(SHARED_LO, SHARED_HI, color=MUTE, alpha=0.16, lw=0, zorder=1)
for edge in (SHARED_LO, SHARED_HI):
    ax.axhline(edge, color=MUTE, lw=0.6, ls=(0, (3, 2)), zorder=2)
ax.annotate(f"every interval contains [{SHARED_LO:.2f}, {SHARED_HI:.2f}]",
            xy=(1.5, SHARED_LO), xytext=(1.5, 0.205), fontsize=5.9,
            color=INK, ha="center", va="bottom",
            arrowprops=dict(arrowstyle="-", lw=0.5, color=MUTE, shrinkA=1,
                            shrinkB=1))

# ---- the published level, as a reference line only ------------------------
ax.axhline(BASE, color=INK, lw=0.8, ls=(0, (1.6, 1.6)), zorder=3)

# ---- four measured levels -------------------------------------------------
for j, (key, lab, role, face, edge) in enumerate(ORDER):
    lo, hi = ci[key]
    lead = key == "on_on"
    ax.errorbar(j, pt[key], yerr=[[pt[key] - lo], [hi - pt[key]]], fmt="none",
                ecolor=face, elinewidth=1.7 if lead else 1.3,
                capsize=3.0 if lead else 2.4, capthick=1.7 if lead else 1.3,
                zorder=5)
    ax.plot(j, pt[key], "o", color=face, ms=4.6 if lead else 4.0, mec=edge,
            mew=0.9, zorder=6)
    ax.text(j, hi + 0.014, f"{pt[key]:.3f}", fontsize=6.2, color=edge,
            ha="center", va="bottom",
            fontweight="bold" if lead else "normal")
    ax.text(j, 0.078, role, fontsize=5.8, color=edge, ha="center", va="bottom")

# ---- the signed direction of each single correction ----------------------
# offset arrows against the published level, NOT stacked bars from an origin
for j, delta, col in ((1, D_X1, ENS_DK), (2, D_X3, EGP_DK)):
    ax.annotate("", xy=(j - 0.32, pt[ORDER[j][0]]), xytext=(j - 0.32, BASE),
                arrowprops=dict(arrowstyle="-|>", lw=0.9, color=col,
                                shrinkA=0, shrinkB=0, mutation_scale=6))
    ax.text(j - 0.38, (BASE + pt[ORDER[j][0]]) / 2, f"{delta:+.3f}",
            fontsize=6.0, color=col, ha="right", va="center", rotation=90)

ax.text(0.5, 0.975,
        rf"$-0.084$ and $+0.083$ do not sum to the net $+{D_NET:.3f}$",
        transform=ax.transAxes, fontsize=6.0, color=INK, ha="center", va="top",
        fontweight="bold")

ax.set_xticks(range(len(ORDER)))
ax.set_xticklabels([lab for _, lab, *_ in ORDER], fontsize=6.2,
                   linespacing=0.95)
ax.set_xlabel("engine corner   X1 / X3")
ax.set_ylabel(r"$\eta^2_{\mathrm{surrogate}}$")
ax.set_xlim(-0.62, len(ORDER) - 0.38)
ax.set_ylim(0.06, 0.74)
despine(ax)

# ---- K: a different axis, not a fifth corner ------------------------------
KS = [2, 3, 5, 10]
kv = [by_k[str(k)]["eta2_surr"] for k in KS]
kx.plot(range(len(KS)), kv, "-", color=MUTE, lw=1.1, zorder=3)
for i, k in enumerate(KS):
    lead = k in (2, 5)
    kx.plot(i, kv[i], "o", ms=4.4 if lead else 3.2,
            color=INK if lead else "white", mec=INK,
            mew=0.9 if lead else 0.7, zorder=4)
    if lead:
        dy, va = ((-0.024, "top") if k == 2 else (0.020, "bottom"))
        kx.text(i, kv[i] + dy, f"{kv[i]:.3f}", fontsize=6.2, color=INK,
                ha="center", va=va, fontweight="bold")

kx.annotate("", xy=(-0.26, kv[0]), xytext=(-0.26, kv[2]),
            arrowprops=dict(arrowstyle="-|>", lw=0.9, color=INK, shrinkA=0,
                            shrinkB=0, mutation_scale=6))
kx.text(-0.33, (kv[0] + kv[2]) / 2, f"{kv[0] - kv[2]:+.3f}", fontsize=6.0,
        color=INK, ha="right", va="center", rotation=90)
kx.text(0.5, 0.055, "no bootstrap\nintervals here",
        transform=kx.transAxes, fontsize=5.6, color=MUTE, ha="center",
        va="bottom")

kx.set_xticks(range(len(KS)))
kx.set_xticklabels([str(k) for k in KS], fontsize=6.2)
kx.set_xlabel("ensemble size $K$")
kx.set_xlim(-0.72, len(KS) - 0.50)
kx.set_title("a different axis", fontsize=6.6, pad=3, color=MUTE)
despine(kx)

save(fig, "fig_confounds")
