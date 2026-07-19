"""Figures for the AAAI-27 draft, built from the audited-engine artifacts only.

fig_sensitivity  : eta2_surrogate against beta and against K, with the fixed
                   convention (beta=2, K=5) marked.  Carries D06 and D11.
fig_width        : GP-ensemble gap against per-member width with bootstrap CIs,
                   over the ensemble's held-out normalized RMSE.  Carries W1
                   and W2 in one image.

Reads results/kbeta/kbeta_analysis.json and results/width/width_analysis.json.
Writes paper/aaai27/figures_v3/*.pdf.
"""
import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "paper", "aaai27", "figures_v3")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.size": 7,
    "axes.labelsize": 7.5,
    "axes.titlesize": 7.5,
    "xtick.labelsize": 6.5,
    "ytick.labelsize": 6.5,
    "legend.fontsize": 6.2,
    "axes.linewidth": 0.6,
    "xtick.major.width": 0.6,
    "ytick.major.width": 0.6,
    "lines.linewidth": 1.2,
    "pdf.fonttype": 42,
})

INK = "#1b1b1b"
GP = "#1f5c8b"
ENS = "#b4451f"
MARK = "#888888"


def sensitivity():
    kb = json.load(open(os.path.join(ROOT, "results", "kbeta", "kbeta_analysis.json")))
    per_beta, by_k = kb["per_beta"], kb["KB1"]["by_K"]

    betas = [0.0, 0.5, 1.0, 2.0, 5.0]
    b_eta = [per_beta[f"{b}"]["eta2"]["surr"] for b in betas]
    boot = kb["KB5_bootstrap"]
    b_ci = {0.0: boot["grid_b0.0"]["eta2"]["surr"]["ci95"],
            2.0: boot["grid_b2.0"]["eta2"]["surr"]["ci95"]}

    ks = [2, 3, 5, 10]
    k_eta = [by_k[str(k)]["eta2_surr"] for k in ks]

    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(3.34, 1.44))

    ax0.plot(betas, b_eta, "o-", color=GP, ms=3.2, zorder=3)
    for b, ci in b_ci.items():
        i = betas.index(b)
        ax0.plot([b, b], ci, color=GP, lw=1.0, alpha=0.75, zorder=2)
        ax0.plot([b - 0.09, b + 0.09], [ci[0]] * 2, color=GP, lw=0.9)
        ax0.plot([b - 0.09, b + 0.09], [ci[1]] * 2, color=GP, lw=0.9)
    ax0.axvline(2.0, color=MARK, ls=":", lw=0.8, zorder=1)
    ax0.text(2.12, 0.055, r"fixed $\beta{=}2$", fontsize=5.8, color=MARK)
    ax0.set_xlabel(r"pessimism $\beta$")
    ax0.set_ylabel(r"$\eta^2_{\mathrm{surrogate}}$")
    ax0.set_ylim(0.0, 0.62)
    ax0.set_xticks(betas)

    ax1.plot(ks, k_eta, "s-", color=ENS, ms=3.2, zorder=3)
    ax1.axvline(5, color=MARK, ls=":", lw=0.8, zorder=1)
    ax1.text(5.25, 0.055, r"fixed $K{=}5$", fontsize=5.8, color=MARK)
    ax1.set_xlabel(r"ensemble size $K$")
    ax1.set_ylim(0.0, 0.62)
    ax1.set_xticks(ks)
    ax1.tick_params(labelleft=False)

    for ax in (ax0, ax1):
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(axis="y", lw=0.35, color="#dddddd", zorder=0)
        ax.set_axisbelow(True)

    fig.tight_layout(pad=0.35, w_pad=0.6)
    fig.savefig(os.path.join(OUT, "fig_sensitivity.pdf"), bbox_inches="tight")
    plt.close(fig)
    print("sensitivity: beta", [round(v, 3) for v in b_eta],
          "| K", [round(v, 3) for v in k_eta])


def width():
    wd = json.load(open(os.path.join(ROOT, "results", "width", "width_analysis.json")))
    ws = wd["widths"]
    gap = [wd["gap_by_width"][str(w)]["gap"] for w in ws]
    lo = [wd["gap_by_width"][str(w)]["ci"][0] for w in ws]
    hi = [wd["gap_by_width"][str(w)]["ci"][1] for w in ws]
    rmse = [wd["heldout_norm_rmse"][f"ens_w{w}"]["mean"] for w in ws]
    gp_rmse = wd["heldout_norm_rmse"]["botorchgp"]["mean"]

    x = range(len(ws))
    fig, ax = plt.subplots(figsize=(3.34, 1.52))

    ax.fill_between(x, lo, hi, color=GP, alpha=0.13, lw=0)
    ax.plot(x, gap, "o-", color=GP, ms=3.4, label="GP--ensemble gap (95% CI)", zorder=3)
    for xi, l, h in zip(x, lo, hi):
        ax.plot([xi, xi], [l, h], color=GP, lw=0.9, alpha=0.8, zorder=2)

    ax.plot(x, rmse, "s--", color=ENS, ms=3.2, label="ensemble held-out normRMSE", zorder=3)
    ax.axhline(gp_rmse, color=ENS, ls=":", lw=0.9, zorder=1)
    ax.text(2.42, gp_rmse + 0.012, "GP normRMSE", fontsize=5.8, color=ENS)

    ax.set_xticks(list(x))
    ax.set_xticklabels([str(w) for w in ws])
    ax.set_xlabel(r"per-member hidden width (fixed $K{=}5$)")
    ax.set_ylim(0.0, 0.72)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", lw=0.35, color="#dddddd", zorder=0)
    ax.set_axisbelow(True)
    ax.legend(loc="upper center", frameon=False, ncol=1, handlelength=1.6,
              bbox_to_anchor=(0.52, 1.03))

    fig.tight_layout(pad=0.35)
    fig.savefig(os.path.join(OUT, "fig_width.pdf"), bbox_inches="tight")
    plt.close(fig)
    print("width: gap", [round(v, 3) for v in gap],
          "| rmse", [round(v, 4) for v in rmse], "| gp", round(gp_rmse, 4))


if __name__ == "__main__":
    sensitivity()
    width()
