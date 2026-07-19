"""FIG 4 — the five confounds and what each does to the headline.

A tornado against the published baseline of 0.367. Three of the five confounds
have a measured signed effect on eta2_surr and are drawn as bars:

  C1 target scaling        0.367 -> 0.283   (-0.084, down)
  C2 candidate/oracle      0.367 -> 0.450   (+0.083, up)
  C3 ensemble size K       K=5 -> K=2       (-0.082, down)

The other two are drawn as annotated rows with no bar, because neither has one:
C4's aggregate kill criterion fired, so it has no grid-wide eta2_surr effect at
all, and C5 acts on eta2_opt.

The corrected value is NOT the sum of these bars. C1 and C2 very nearly cancel
(-0.084 against +0.083), so the corrected corner at 0.405 is the two protocol
corrections applied jointly, and the +0.038 net comes from their interaction
rather than from either alone. The figure draws it as a separate marked level
for that reason, never as a running total.

UNITS: every number on this figure is an eta2_surr value or a difference of
two, never an optimization gap.

Reads results/bootstrap_eta_corners.json, results/kbeta/kbeta_analysis.json.
"""
import json
import os

import matplotlib.pyplot as plt

from style import (ACCENT, COL, EGP, ENS, FAINT, INK, MUTE, RESULTS, despine,
                   save, use_style)

use_style()

corners = json.load(open(os.path.join(RESULTS, "bootstrap_eta_corners.json")))
kb = json.load(open(os.path.join(RESULTS, "kbeta", "kbeta_analysis.json")))

BASE = corners["off_off"]["eta2"]["point"]["surr"]        # 0.367, published
CORR = corners["on_on"]["eta2"]["point"]["surr"]          # 0.405, corrected
CORR_CI = corners["on_on"]["eta2"]["surr"]["ci95"]        # [0.290, 0.556]
by_k = kb["KB1"]["by_K"]

# C1 and C2 are corner comparisons and read against the published corner.
# C3 is a K-sweep on the audited engine, so it reads against its OWN K=5
# reference (0.408) — setting it against the off_off corner would compare two
# different engines through one bar.
ROWS = [
    ("C1  target scaling", BASE, corners["on_off"]["eta2"]["point"]["surr"]),
    ("C2  candidate/oracle", BASE, corners["off_on"]["eta2"]["point"]["surr"]),
    ("C3  ensemble size $K$", by_k["5"]["eta2_surr"], by_k["2"]["eta2_surr"]),
]
NOBAR = [
    ("C4  $\\beta$/$\\sigma$ match", "no aggregate effect: our own kill fired"),
    ("C5  query budget", "acts on $\\eta^2_{\\mathrm{opt}}$, not on this axis"),
]

fig, ax = plt.subplots(figsize=(COL, 2.05))

y = list(range(len(ROWS) + len(NOBAR)))[::-1]
labels = []

for i, (lab, ref, val) in enumerate(ROWS):
    yy = y[i]
    delta = val - ref
    col = EGP if delta > 0 else ENS
    ax.barh(yy, delta, left=ref, height=0.52, color=col, alpha=0.85, lw=0,
            zorder=3)
    ha = "left" if delta > 0 else "right"
    off = 0.008 if delta > 0 else -0.008
    ax.text(val + off, yy, f"{val:.3f}  ({delta:+.3f})", fontsize=6.2,
            color=col, ha=ha, va="center", zorder=5)
    if ref != BASE:                       # C3 carries its own reference
        ax.plot([ref], [yy], "|", color=INK, ms=8, mew=1.0, zorder=5)
        ax.text(ref + 0.010, yy + 0.42, f"vs its own $K{{=}}5$  {ref:.3f}",
                fontsize=5.8, color=MUTE, ha="left", va="center")
    labels.append(lab)

for j, (lab, note) in enumerate(NOBAR):
    yy = y[len(ROWS) + j]
    ax.plot([BASE], [yy], "|", color=MUTE, ms=7, mew=1.0, zorder=3)
    ax.text(BASE + 0.012, yy, note, fontsize=6.0, color=MUTE, ha="left",
            va="center")
    labels.append(lab)

# the published baseline
ax.axvline(BASE, color=INK, lw=0.8, zorder=4)
ax.text(BASE - 0.012, len(y) - 0.32, f"published  {BASE:.3f}", fontsize=6.3,
        color=INK, ha="right", va="bottom")

# the corrected corner, with its interval — never shown without it (D10)
ax.axvspan(CORR_CI[0], CORR_CI[1], color=ACCENT, alpha=0.14, lw=0, zorder=1)
ax.axvline(CORR, color=ACCENT, lw=1.1, zorder=4)
ax.text(CORR + 0.012, len(y) - 0.32,
        f"corrected  {CORR:.3f}  [{CORR_CI[0]:.3f}, {CORR_CI[1]:.3f}]",
        fontsize=6.3, color=ACCENT, ha="left", va="bottom")

ax.set_yticks(y)
ax.set_yticklabels(labels, fontsize=6.8)
ax.set_xlabel(r"$\eta^2_{\mathrm{surrogate}}$")
ax.set_xlim(0.16, 0.68)
ax.set_ylim(-0.62, len(y) + 0.22)
ax.tick_params(axis="y", length=0)
despine(ax, grid="x")

save(fig, "fig_confounds")
