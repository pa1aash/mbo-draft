"""GP/SVGP own-proposal coverage (#2) + cross-proposal coverage (#3), synthetic tasks.
Answers: is the GP premise well-covered where ITS optimizer goes (vs the ensemble's
collapse)?  and is 'coverage worst where the optimizer goes' endogenous (each surrogate
measured on its own Pi)?  Reuses mbo.fit_exact_gp (sklearn -> oracle-space mu/sigma, no
un-normalization), train_ensemble, coverage_of_premise, grad_opt/perturb_opt.
Serial (reliable). Writes results/gpcov.json.
  python code/run_gpcov.py [SEEDS]
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import torch
import mbo

B = mbo.BETA
SEEDS = int(sys.argv[1]) if len(sys.argv) > 1 else 10


def ens_musig(ms, xx):
    with torch.no_grad():
        ps = torch.stack([m(torch.FloatTensor(xx)) for m in ms])
    return ps.mean(0).numpy(), ps.std(0).numpy()


def run_one(task, seed):
    np.random.seed(seed); torch.manual_seed(seed)
    x, y = task.data()
    ms = mbo.train_ensemble(x, y, task.dim, seed=seed, ep=mbo.TRAIN_EP)
    gp = mbo.fit_exact_gp(x, y, task.dim, seed)                      # sklearn: predict gives oracle-space mu,sd
    mg_ens = lambda xx: ens_musig(ms, xx)
    mg_gp = lambda xx: gp.predict(xx, return_std=True)
    xt = np.random.uniform(0, 1, (500, task.dim)).astype(np.float32)  # in-distribution test points
    x0 = mbo.init_candidates(x, y, seed)
    xf_ens = mbo.grad_opt(mbo.ens_lcb_torch(ms, B), torch.FloatTensor(x0), steps=mbo.OPT_STEPS)  # ensemble proposals
    xf_gp = np.asarray(mbo.perturb_opt(mbo.gp_lcb_np(gp, B), x0), np.float32)                    # GP proposals (sklearn: 0th-order)

    def cov(mg, xx):
        mu, sd = mg(xx)
        return mbo.coverage_of_premise(np.asarray(mu), np.asarray(sd), task.oracle(xx), B)
    return dict(
        gp_indist=cov(mg_gp, xt), gp_own=cov(mg_gp, xf_gp),          # #2 GP coverage in-dist / on GP's own proposals
        ens_indist=cov(mg_ens, xt), ens_own=cov(mg_ens, xf_ens),     # ensemble baseline
        ens_on_gp=cov(mg_ens, xf_gp), gp_on_ens=cov(mg_gp, xf_ens),  # #3 cross-proposal
    )


if __name__ == '__main__':
    out = {}
    print(f"GP/cross coverage: 7 tasks x {SEEDS} seeds (serial)", flush=True)
    for task in mbo.make_tasks(None):
        accum = {}
        for s in range(SEEDS):
            try:
                r = run_one(task, s)
            except Exception as e:
                print(f"  {task.name} seed{s} FAIL: {type(e).__name__}: {str(e)[:70]}", flush=True); continue
            for k, v in r.items():
                accum.setdefault(k, []).append(float(v))
        out[task.name] = {k: {'mean': float(np.mean(v)), 'std': float(np.std(v))} for k, v in accum.items()}
        m = out[task.name]
        print(f"  {task.name:14} GP[in={m['gp_indist']['mean']:.2f} own={m['gp_own']['mean']:.2f}] "
              f"ens[in={m['ens_indist']['mean']:.2f} own={m['ens_own']['mean']:.2f}] "
              f"cross[ens@gp={m['ens_on_gp']['mean']:.2f} gp@ens={m['gp_on_ens']['mean']:.2f}]", flush=True)
    dst = os.path.join(os.path.dirname(__file__), '..', 'results', 'gpcov.json')
    json.dump(out, open(dst, 'w'), indent=1)
    print("wrote", os.path.abspath(dst), flush=True)
    keys = ['gp_indist', 'gp_own', 'ens_indist', 'ens_own', 'ens_on_gp', 'gp_on_ens']
    print("MEAN " + "  ".join(f"{k}={np.mean([out[t][k]['mean'] for t in out]):.2f}" for k in keys), flush=True)
