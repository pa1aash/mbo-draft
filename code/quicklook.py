"""Super-small promise check: is the surrogate x optimizer attribution thesis real?
Tests (1) optimizer vs surrogate effect size on the 3x3 grid, (2) GATE-1 (survives matched
tuning?), (3) synthetic->real transfer. Rank-based (scale-free) + 2-way ANOVA eta^2."""
import json, itertools, numpy as np
from pathlib import Path

R = Path(__file__).resolve().parent.parent / "results"
SURR = ["ens", "botorchgp", "svgp"]      # deep ensemble, exact GP, sparse/variational GP
OPT  = ["perturb", "grad", "cma"]         # hill-climb, gradient, CMA-ES
CELLS = [f"{s}:{o}" for s in SURR for o in OPT]

def grid_ranks(path, metric="p100"):
    """Per-task: rank the 9 cells (1=worst..9=best), return dict task-> {cell: rank} and
    normalized [0,1] scores. Returns (ranks_by_task, norm_by_task, tasks_used)."""
    d = json.load(open(path))["mbo"]
    ranks, norm, used = {}, {}, []
    for task, methods in d.items():
        vals = {}
        for c in CELLS:
            if c in methods and metric in methods[c]:
                vals[c] = methods[c][metric]["mean"]
        if len(vals) < len(CELLS):            # need full grid for this task
            continue
        used.append(task)
        arr = np.array([vals[c] for c in CELLS], float)
        order = arr.argsort().argsort() + 1   # ranks 1..9 (higher score -> higher rank)
        ranks[task] = dict(zip(CELLS, order))
        lo, hi = arr.min(), arr.max()
        z = (arr - lo) / (hi - lo) if hi > lo else np.zeros_like(arr)
        norm[task] = dict(zip(CELLS, z))
    return ranks, norm, used

def effects(norm, used):
    """2-way ANOVA-style: eta^2 for optimizer main effect vs surrogate main effect."""
    # matrix tasks x surr x opt of normalized scores
    M = np.array([[[norm[t][f"{s}:{o}"] for o in OPT] for s in SURR] for t in used])  # T,S,O
    grand = M.mean()
    ss_tot = ((M - grand)**2).sum()
    # optimizer main effect: marginalize over surr & tasks
    opt_means = M.mean(axis=(0,1))            # per optimizer
    ss_opt = len(used)*len(SURR)*((opt_means - grand)**2).sum()
    surr_means = M.mean(axis=(0,2))           # per surrogate
    ss_surr = len(used)*len(OPT)*((surr_means - grand)**2).sum()
    return dict(opt_means=dict(zip(OPT, opt_means)), surr_means=dict(zip(SURR, surr_means)),
                eta2_opt=ss_opt/ss_tot, eta2_surr=ss_surr/ss_tot)

def marg_rank(ranks, used):
    """Mean rank per optimizer (marg. surr) and per surrogate (marg. opt)."""
    opt = {o: np.mean([ranks[t][f"{s}:{o}"] for t in used for s in SURR]) for o in OPT}
    surr = {s: np.mean([ranks[t][f"{s}:{o}"] for t in used for o in OPT]) for s in SURR}
    return opt, surr

def report(tag, path):
    ranks, norm, used = grid_ranks(path)
    if not used:
        print(f"\n[{tag}] no full-grid tasks in {Path(path).name}"); return None
    e = effects(norm, used); opt_r, surr_r = marg_rank(ranks, used)
    print(f"\n=== {tag}  ({len(used)} tasks: {', '.join(used)}) ===")
    print(f"  optimizer effect  eta^2 = {e['eta2_opt']:.3f}   | surrogate effect eta^2 = {e['eta2_surr']:.3f}")
    print(f"  optimizer mean-rank (of 9): " + ", ".join(f"{o}={opt_r[o]:.2f}" for o in OPT))
    print(f"  surrogate mean-rank (of 9): " + ", ".join(f"{s}={surr_r[s]:.2f}" for s in SURR))
    print(f"  best optimizer: {max(opt_r,key=opt_r.get)} ({max(opt_r.values()):.2f})  "
          f"spread={max(opt_r.values())-min(opt_r.values()):.2f}")
    print(f"  best surrogate: {max(surr_r,key=surr_r.get)} ({max(surr_r.values()):.2f})  "
          f"spread={max(surr_r.values())-min(surr_r.values()):.2f}")
    return e

print("PROMISE CHECK — does surrogate x optimizer attribution hold?")
s_un = report("SYNTH unmatched", R/"results_camera.json")
s_ma = report("SYNTH matched (GATE-1)", R/"results_camera_matched.json")
d_un = report("REAL/DB unmatched (transfer)", R/"results_db.json")

print("\n--- VERDICT ---")
if s_un:
    axis = "OPTIMIZER" if s_un['eta2_opt'] > s_un['eta2_surr'] else "SURROGATE"
    ratio = s_un['eta2_opt']/max(s_un['eta2_surr'],1e-9)
    print(f"Synthetic: {axis} dominates (opt/surr eta^2 ratio = {ratio:.1f}x)")
if s_un and s_ma:
    survived = (s_ma['eta2_opt'] > s_ma['eta2_surr']) == (s_un['eta2_opt'] > s_un['eta2_surr'])
    print(f"GATE-1 (matched tuning): dominant axis {'SURVIVES' if survived else 'FLIPS'} "
          f"(matched opt eta^2={s_ma['eta2_opt']:.3f} vs surr {s_ma['eta2_surr']:.3f})")
if s_un and d_un:
    transfer = (d_un['eta2_opt'] > d_un['eta2_surr']) == (s_un['eta2_opt'] > s_un['eta2_surr'])
    print(f"Synth->Real transfer: finding {'HOLDS' if transfer else 'DIFFERS'} on Design-Bench "
          f"(DB opt eta^2={d_un['eta2_opt']:.3f} vs surr {d_un['eta2_surr']:.3f})")
