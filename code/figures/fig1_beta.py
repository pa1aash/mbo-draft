"""FIG 1 — the beta axis is the one the seven tasks come closest to resolving.

Left: eta2_surrogate against beta over the measured grid, with bootstrap 95%
intervals at the two endpoints where they were computed (beta=0 and beta=2).
Intervals were not computed at beta = 0.5, 1, 5, so none are drawn there and
the connecting line is marked as the point-estimate trace.

Right: the four engine corners on the same y-axis, intervals drawn as capped
horizontal bars. They overlap completely.

The contrast is the figure's argument: a decomposition that cannot separate its
own corners at n=7 still separates its beta endpoints, which is why the paper
leads with beta.

Reads results/kbeta/kbeta_analysis.json, results/bootstrap_eta_corners.json.
"""
import json
import os

import matplotlib.pyplot as plt

from style import (ACCENT, ACCENT_DK, BAND_LEAD, COL, EGP, EGP_DK, GHOST,
                   GHOST_DK, INK, MUTE, RESULTS, despine, save, use_style)

use_style()

kb = json.load(open(os.path.join(RESULTS, "kbeta", "kbeta_analysis.json")))
corners = json.load(open(os.path.join(RESULTS, "bootstrap_eta_corners.json")))

BETAS = [0.0, 0.5, 1.0, 2.0, 5.0]
eta = [kb["per_beta"][f"{b}"]["eta2"]["surr"] for b in BETAS]
boot = kb["KB5_bootstrap"]
CI = {0.0: boot["grid_b0.0"]["eta2"]["surr"]["ci95"],
      2.0: boot["grid_b2.0"]["eta2"]["surr"]["ci95"]}

CORNER_ORDER = [("off_off", "off\noff"), ("on_off", "on\noff"),
                ("off_on", "off\non"), ("on_on", "on\non")]

fig, (ax, bx) = plt.subplots(
    1, 2, figsize=(COL, 1.85), sharey=True,
    gridspec_kw={"width_ratios": [1.5, 1.0], "wspace": 0.10})

# ---------------- left: the beta trace -----------------------------------
x = list(range(len(BETAS)))
ax.plot(x, eta, "-", color=EGP, lw=1.9, zorder=3)
ax.plot(x, eta, "o", color=EGP, ms=4.0, mec="white", mew=0.7, zorder=4)

for b, ci in CI.items():
    i = BETAS.index(b)
    ax.errorbar(i, eta[i], yerr=[[eta[i] - ci[0]], [ci[1] - eta[i]]],
                fmt="none", ecolor=EGP, elinewidth=1.6, capsize=3.0,
                capthick=1.6, zorder=5)
    ax.plot(i, eta[i], "o", color=EGP, ms=4.6, mec=EGP_DK, mew=0.9, zorder=6)

# the near-separation: beta=0 upper bound against beta=2 lower bound
hi0, lo2 = CI[0.0][1], CI[2.0][0]
ax.axhspan(lo2, hi0, color=ACCENT, alpha=BAND_LEAD, lw=0, zorder=1)
for edge in (lo2, hi0):
    ax.axhline(edge, color=ACCENT_DK, lw=0.7, zorder=2)
ax.annotate(f"intervals overlap\nby only {hi0 - lo2:.3f}",
            xy=(1.05, (lo2 + hi0) / 2), xytext=(1.30, 0.045),
            fontsize=6.4, color=ACCENT_DK, ha="center", va="bottom",
            fontweight="bold",
            arrowprops=dict(arrowstyle="-", lw=0.6, color=ACCENT_DK,
                            shrinkA=0, shrinkB=1))

ax.set_xticks(x)
ax.set_xticklabels([f"{b:g}" for b in BETAS])
ax.set_xlabel(r"pessimism $\beta$")
ax.set_ylabel(r"$\eta^2_{\mathrm{surrogate}}$")
ax.set_xlim(-0.42, len(BETAS) - 0.58)
ax.set_title(r"$\beta$ axis: endpoints nearly separate", fontsize=7.0, pad=3)
despine(ax)

# ---------------- right: the four corners --------------------------------
for j, (key, lab) in enumerate(CORNER_ORDER):
    e = corners[key]["eta2"]
    pt, ci = e["point"]["surr"], e["surr"]["ci95"]
    on = key == "on_on"
    c, ce = (ACCENT, ACCENT_DK) if on else (GHOST, GHOST_DK)
    bx.errorbar(j, pt, yerr=[[pt - ci[0]], [ci[1] - pt]], fmt="none",
                ecolor=c, elinewidth=1.5 if on else 1.1,
                capsize=2.8 if on else 2.2, capthick=1.5 if on else 1.1,
                zorder=4 if on else 3)
    bx.plot(j, pt, "o", color=c, ms=4.2 if on else 3.4, mec=ce, mew=0.8,
            zorder=5 if on else 4)

# every corner point estimate falls inside the corrected corner's interval
lo, hi = corners["on_on"]["eta2"]["surr"]["ci95"]
bx.axhspan(lo, hi, color=ACCENT, alpha=0.16, lw=0, zorder=1)
bx.annotate("the corrected interval\ncontains every corner",
            xy=(1.5, hi), xytext=(1.5, 0.70), fontsize=6.2, color=ACCENT_DK,
            ha="center", va="bottom",
            arrowprops=dict(arrowstyle="-", lw=0.5, color=MUTE,
                            shrinkA=0, shrinkB=1))

bx.set_xticks(range(len(CORNER_ORDER)))
bx.set_xticklabels([lab for _, lab in CORNER_ORDER], fontsize=6.0,
                   linespacing=0.95)
bx.set_xlabel("corner  X1 / X3")
bx.set_xlim(-0.6, len(CORNER_ORDER) - 0.4)
bx.set_title("corners: no separation", fontsize=7.0, pad=3)
despine(bx)

ax.set_ylim(0.0, 0.78)

save(fig, "fig_beta_resolution")
