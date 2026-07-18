"""SM2 re-calibration, round 2: can a GP mean be roughened WITHOUT degenerating?

Round 1 (swing_calib.py) found a hard ceiling. Every pure-kernel roughening either barely
moved the mean's gradient (nu changes: 0.78-1.10x) or roughened only by DEGRADING the fit
(short lengthscale: postmean_std collapses as the mean reverts to the prior). A score drop
from a degenerate GP would be attributable to "it stopped fitting", not "it got rough" --
a FALSE CONFIRM of SM2, which is worse than no test.

This round tries the one construction that could add high-frequency structure while KEEPING
the data fit: an additive kernel, k = ScaleKernel(RBF@L) + a * ScaleKernel(Matern12@L/m).
The smooth component preserves the fit; the rough component injects short-scale structure.
Its amplitude `a` is FROZEN (the MLL would otherwise shrink it to ~0, since the data do not
support roughness -- that shrinkage is itself the finding).

Reported per config: rough_D / rough_seg (gradient norm on and between data) and
postmean_std (fit amplitude -- if this collapses, the config is degenerate, not rough).
Seeds 100/101 only, disjoint from analysis seeds 0..29.
"""
import sys

import numpy as np
import torch

sys.path.insert(0, '.')
import mbo                                                          # noqa: E402
from swing_calib import bot_mu, rough_at                            # noqa: E402


def build_additive(x, y, seed, L, amp, m, nu_rough=0.5):
    """SingleTaskGP with covar = ScaleKernel(RBF@L) + amp*ScaleKernel(Matern@L/m),
    both lengthscales frozen; outputscales frozen at (1, amp) after the smooth fit."""
    import gpytorch
    from botorch.models import SingleTaskGP
    d = x.shape[1]
    xt = torch.DoubleTensor(x)
    yt = torch.DoubleTensor(y).unsqueeze(-1)
    yt = (yt - yt.mean()) / (yt.std() + 1e-8)

    def ls(v):
        a = np.atleast_1d(np.asarray(v, np.float64)).reshape(1, -1)
        return torch.as_tensor(np.repeat(a, d, axis=1) if a.shape[1] == 1 else a)

    ks = gpytorch.kernels.RBFKernel(ard_num_dims=d)
    ks.lengthscale = ls(L); ks.raw_lengthscale.requires_grad_(False)
    kr = gpytorch.kernels.MaternKernel(nu=nu_rough, ard_num_dims=d)
    kr.lengthscale = ls(np.asarray(L) / m); kr.raw_lengthscale.requires_grad_(False)
    Ss = gpytorch.kernels.ScaleKernel(ks); Ss.outputscale = 1.0
    Sr = gpytorch.kernels.ScaleKernel(kr); Sr.outputscale = float(amp)
    Ss.raw_outputscale.requires_grad_(False); Sr.raw_outputscale.requires_grad_(False)
    gp = SingleTaskGP(xt, yt, covar_module=(Ss + Sr))
    gp.eval()
    return gp


def probe(task, seed=100):
    t = mbo.make_tasks([task])[0]
    np.random.seed(seed); torch.manual_seed(seed)
    x, y = t.data()
    ym, ys = float(np.mean(y)), float(np.std(y) + 1e-8)
    r = np.random.RandomState(90000 + seed)
    sub = r.choice(len(x), min(800, len(x)), replace=False)
    xs, yss = x[sub], y[sub]
    xd = x[r.choice(len(x), 400, replace=False)]
    a_, b_ = x[r.choice(len(x), 400)], x[r.choice(len(x), 400)]
    tt = r.uniform(0.2, 0.8, (400, 1)).astype(np.float32)
    xseg = a_ * (1 - tt) + b_ * tt
    fstd = float(np.std(t.oracle(xd)))

    gp0 = mbo.fit_botorch_gp(x, y, seed)
    L = getattr(gp0.covar_module, 'base_kernel', gp0.covar_module).lengthscale
    L = L.detach().numpy().ravel().copy()
    mu0 = bot_mu(gp0, ym, ys)
    b_d, b_s = rough_at(mu0, xd, fstd), rough_at(mu0, xseg, fstd)
    with torch.no_grad():
        p0 = gp0.posterior(torch.DoubleTensor(np.asarray(xd, np.float64))).mean.squeeze(-1).numpy()
    print(f'\n{task}: L_med={np.median(L):.3f}  smooth rough_D={b_d:.3f} rough_seg={b_s:.3f} '
          f'postmean_std={p0.std():.3f}')

    for amp in (0.3, 1.0, 3.0):
        for m in (5.0, 20.0):
            g = build_additive(xs, yss, seed, L, amp, m)
            mu = bot_mu(g, ym, ys)
            rd, rs = rough_at(mu, xd, fstd), rough_at(mu, xseg, fstd)
            with torch.no_grad():
                pm = g.posterior(torch.DoubleTensor(np.asarray(xd, np.float64))).mean.squeeze(-1).numpy()
            print(f'   amp={amp:<4} L/{m:<5} rough_D={rd:8.3f} ({rd/b_d:5.2f}x)  '
                  f'rough_seg={rs:8.3f} ({rs/b_s:5.2f}x)  postmean_std={pm.std():.3f} '
                  f'({pm.std()/p0.std():.2f}x fit)')


if __name__ == '__main__':
    for tk in ('Branin-2D', 'Ackley-20D', 'Griewank-30D'):
        probe(tk)
