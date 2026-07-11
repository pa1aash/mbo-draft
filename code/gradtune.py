"""Robustness sweep rebutting the #1 reviewer objection: 'the ensemble's gradient-ascent
collapse is just an under-tuned optimizer.' For each task we run the conservative
perturbation optimizer (the target) and a grid of gradient-ascent configs (LR, steps,
gradient-normalization, trust-region). If even the best-tuned gradient config still
underperforms perturbation, the collapse is surrogate geometry (genuine), not tuning.

  python gradtune.py --seeds 10 --jobs 8         -> results/results_gradtune.json
"""
import argparse, json, os, time
from concurrent.futures import ProcessPoolExecutor, as_completed
import numpy as np
import mbo

OUT = os.path.join(os.path.dirname(__file__), '..', 'results', 'results_gradtune.json')
TASKS = ['Branin-2D', 'Styblinski-5D', 'Rosenbrock-10D', 'Ackley-20D']   # collapse-hard + gradient-ok contrast
# gradient configs: name -> grad_opt kwargs. 'default' is the one used in the main grid.
CONFIGS = {
    'perturb':          None,                                              # the conservative target
    'grad_default':     dict(lr=0.05, steps=100),
    'grad_gentle':      dict(lr=0.01, steps=100),
    'grad_long':        dict(lr=0.05, steps=300),
    'grad_norm':        dict(lr=0.05, steps=100, normalize=True),
    'grad_trust':       dict(lr=0.05, steps=100, trust=0.1),
    'grad_besttuned':   dict(lr=0.01, steps=200, normalize=True, trust=0.1),
}

def _cell(spec):
    import torch; torch.set_num_threads(1)
    t = mbo.make_tasks([spec['task']])[0]
    np.random.seed(spec['seed']); torch.manual_seed(spec['seed'])
    x, y = t.data(); x0 = mbo.init_candidates(x, y, spec['seed'])
    ms = mbo.train_ensemble(x, y, t.dim, seed=spec['seed'], ep=spec['ep'])
    cfg = CONFIGS[spec['cfg']]
    if cfg is None:
        xf = mbo.perturb_opt(mbo.ens_lcb_np(ms, mbo.BETA), x0)
    else:
        xf = mbo.grad_opt(mbo.ens_lcb_torch(ms, mbo.BETA), torch.FloatTensor(x0), **cfg)
    return spec['task'], spec['cfg'], spec['seed'], mbo.eval_designs(t, xf)[0]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seeds', type=int, default=10)
    ap.add_argument('--jobs', type=int, default=max(1, (os.cpu_count() or 2) - 1))
    ap.add_argument('--ep', type=int, default=mbo.TRAIN_EP)
    ap.add_argument('--tasks', nargs='*', default=TASKS)
    a = ap.parse_args()
    specs = [{'task': t, 'cfg': c, 'seed': s, 'ep': a.ep}
             for t in a.tasks for c in CONFIGS for s in range(a.seeds)]
    R = {}
    t0 = time.time()
    print(f'{len(specs)} cells, {a.jobs} workers', flush=True)
    with ProcessPoolExecutor(max_workers=a.jobs) as ex:
        for fut in as_completed([ex.submit(_cell, s) for s in specs]):
            task, cfg, seed, p100 = fut.result()
            R.setdefault(task, {}).setdefault(cfg, []).append(p100)
    json.dump(R, open(OUT, 'w'), indent=1)

    print(f'\ndone in {(time.time()-t0)/60:.1f} min. VERDICT (mean p100, higher=better):')
    print(f"{'task':<15}" + ''.join(f'{c:>15}' for c in CONFIGS))
    for task in a.tasks:
        row = R.get(task, {})
        means = {c: np.mean(row[c]) for c in CONFIGS if c in row}
        print(f'{task:<15}' + ''.join(f'{means.get(c, float("nan")):>15.2f}' for c in CONFIGS))
        pert = means.get('perturb', float('nan'))
        best_grad = max((v for c, v in means.items() if c != 'perturb'), default=float('nan'))
        gap = pert - best_grad
        verdict = 'COLLAPSE GENUINE (perturb still wins)' if gap > 0.05*abs(pert)+1e-6 else 'tuning closes it (finding weakens)'
        print(f"   -> perturb {pert:.2f} vs best-tuned-grad {best_grad:.2f}: {verdict}")

if __name__ == '__main__':
    main()
