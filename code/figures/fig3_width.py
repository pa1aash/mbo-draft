"""FIG 3 — eliminations 2 and 3 in one float.

Top: the GP-ensemble optimization gap against per-member width over a 10.7x
range at fixed K=5. It does not close (0.480 -> 0.476, 99.1% retained) and it is
non-monotone. The bootstrap band widens monotonically with w, which is a stated
limit of the result, not a nuisance to hide: w=1024 is the least precise point
on the curve.

Bottom: held-out normalized RMSE on a 20% split the grid never saw. The
ensemble's falls monotonically with width and sits below the exact GP's flat
line at every width.

Read together: the more accurate surrogate is the one that loses.

Reads results/width/width_analysis.json.
"""
import json
import os

import matplotlib.pyplot as plt

from style import (ACCENT, ACCENT_DK, BAND_LEAD, COL, EGP, EGP_DK, ENS,
                   ENS_DK, INK, MUTE, RESULTS, despine, save, use_style)

use_style()

wa = json.load(open(os.path.join(RESULTS, "width", "width_analysis.json")))
W = wa["widths"]
gap = [wa["gap_by_width"][str(w)]["gap"] for w in W]
lo = [wa["gap_by_width"][str(w)]["ci"][0] for w in W]
hi = [wa["gap_by_width"][str(w)]["ci"][1] for w in W]
rmse_ens = [wa["heldout_norm_rmse"][f"ens_w{w}"]["mean"] for w in W]
rmse_gp = wa["heldout_norm_rmse"]["botorchgp"]["mean"]

x = list(range(len(W)))

fig, (ax, bx) = plt.subplots(
    2, 1, figsize=(COL, 2.85), sharex=True,
    gridspec_kw={"height_ratios": [1.15, 1.0], "hspace": 0.16})

# ---- top: the gap does not close ----------------------------------------
ax.fill_between(x, lo, hi, color=EGP, alpha=BAND_LEAD, lw=0, zorder=2)
ax.plot(x, gap, "-", color=EGP, lw=2.0, zorder=4)
ax.plot(x, gap, "o", color=EGP, ms=4.0, mec=EGP_DK, mew=0.8, zorder=5)
ax.axhline(0.0, color=MUTE, lw=0.5, ls=(0, (3, 2)), zorder=1)

ax.annotate("", xy=(x[0], gap[0]), xytext=(x[-1], gap[-1]),
            arrowprops=dict(arrowstyle="-", lw=1.0, color=ACCENT_DK,
                            ls=(0, (2.4, 1.8))))
ax.text(0.50, 0.93,
        rf"$0.480 \rightarrow 0.476$   ($99.1\%$ retained)",
        transform=ax.transAxes, ha="center", va="top", fontsize=7.0,
        color=ACCENT_DK, fontweight="bold")
ax.text(0.97, 0.10, "interval widens with $w$:\n$0.211 \\rightarrow 0.439$",
        transform=ax.transAxes, ha="right", va="bottom", fontsize=6.0,
        color=MUTE)

ax.set_ylabel(r"GP$-$ensemble gap")
ax.set_ylim(-0.05, 0.78)
despine(ax)

# ---- bottom: the ensemble is the more accurate surrogate ------------------
bx.axhline(rmse_gp, color=EGP, lw=1.9, zorder=3)
bx.text(len(W) - 1.06, rmse_gp + 0.006, f"Exact GP  {rmse_gp:.3f}",
        fontsize=6.5, color=EGP, ha="right", va="bottom", fontweight="bold")

bx.plot(x, rmse_ens, "-", color=ENS, lw=2.0, zorder=4)
bx.plot(x, rmse_ens, "o", color=ENS, ms=4.0, mec=ENS_DK, mew=0.8, zorder=5)
bx.text(0.06, rmse_ens[0] - 0.010,
        f"Ensemble  {rmse_ens[0]:.3f} $\\rightarrow$ {rmse_ens[-1]:.3f}",
        fontsize=6.5, color=ENS_DK, ha="left", va="top", fontweight="bold")

bx.fill_between(x, rmse_ens, rmse_gp, color=ACCENT, alpha=0.26, lw=0,
                zorder=2)
bx.text(0.97, 0.40, "the more accurate surrogate\nis the one that loses",
        transform=bx.transAxes, ha="right", va="center", fontsize=6.8,
        color=ACCENT_DK, fontweight="bold")

bx.set_ylabel("held-out norm. RMSE")
bx.set_xlabel("per-member hidden width $w$  (fixed $K{=}5$)")
bx.set_xticks(x)
bx.set_xticklabels([str(w) for w in W])
bx.set_xlim(-0.3, len(W) - 0.7)
despine(bx)

save(fig, "fig_width_rmse")
