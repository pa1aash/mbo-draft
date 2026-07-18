"""SM2 re-calibration on seeds 100/101 (DISJOINT from analysis seeds 0..29).

The first smoke showed the SM2 manipulation failing for two distinct reasons, both of
which are properties of the intervention rather than of nature:

  (a) refitting the hyperparameters UNDOES the roughening -- at nu=0.5 the marginal
      likelihood inflates the lengthscale (Branin 0.40 -> 15.93) and returns an
      effectively SMOOTHER mean;
  (b) an absolute short lengthscale (0.05) is DEGENERATE in high d -- the posterior mean
      reverts to the prior between points, so it is flat, not rough.

This probe fixes (a) by freezing the lengthscale at the smooth GP's fitted value L and
moving only nu, and fixes (b) by shortening RELATIVE to L. It also adds a second
roughness instrument: at-data gradients understate spikiness, because a sum of sharp
bumps is locally flat AT the bump centres. `rough_seg` therefore probes points BETWEEN
data (convex combinations of random D pairs), where the wiggle actually lives.

Nothing here touches seeds 0..29; it only chooses the knob settings that go into the
committed pre-registration.
"""
import sys

import numpy as np
import torch

sys.path.insert(0, '.')
import mbo                                                          # noqa: E402


def rough_at(mu_fn, xs, fstd):
    xt = torch.FloatTensor(np.asarray(xs, np.float32)).requires_grad_(True)
    g = torch.autograd.grad(mu_fn(xt).sum(), xt)[0]
    return float(g.norm(dim=1).mean()) / (fstd + 1e-12)


def bot_mu(gp, ym, ys):
    return lambda xt: gp.posterior(xt.double()).mean.squeeze(-1).float() * ys + ym


def probe(task, seed=100):
    t = mbo.make_tasks([task])[0]
    np.random.seed(seed); torch.manual_seed(seed)
    x, y = t.data()
    ym, ys = float(np.mean(y)), float(np.std(y) + 1e-8)
    r = np.random.RandomState(90000 + seed)
    xd = x[r.choice(len(x), 400, replace=False)]                    # ON data
    a, b = x[r.choice(len(x), 400)], x[r.choice(len(x), 400)]
    tt = r.uniform(0.2, 0.8, (400, 1)).astype(np.float32)
    xseg = (a * (1 - tt) + b * tt)                                  # BETWEEN data
    fstd = float(np.std(t.oracle(xd)))

    gp0 = mbo.fit_botorch_gp(x, y, seed)
    L = getattr(gp0.covar_module, 'base_kernel', gp0.covar_module).lengthscale
    L = L.detach().numpy().ravel().copy()
    print(f'\n{task}: fitted RBF lengthscale median={np.median(L):.4f}  (fstd={fstd:.3f})')

    cfgs = [('smooth  (incumbent RBF@fitL)', dict()),
            ('m12  @L   (nu=.5, L frozen)', dict(nu=0.5, lengthscale=L)),
            ('m32  @L   (nu=1.5, L frozen)', dict(nu=1.5, lengthscale=L)),
            ('RBF  @L/3', dict(lengthscale=L / 3.0)),
            ('RBF  @L/5', dict(lengthscale=L / 5.0)),
            ('m12  @L/3', dict(nu=0.5, lengthscale=L / 3.0))]
    base_d = base_s = None
    for name, kw in cfgs:
        g = mbo.fit_botorch_gp(x, y, seed, **kw)
        mu = bot_mu(g, ym, ys)
        rd, rs = rough_at(mu, xd, fstd), rough_at(mu, xseg, fstd)
        with torch.no_grad():
            pm = g.posterior(torch.DoubleTensor(np.asarray(xd, np.float64))).mean.squeeze(-1).numpy()
        if base_d is None:
            base_d, base_s = rd, rs
        print(f'  {name:30s} rough_D={rd:8.4f} ({rd/base_d:5.2f}x)  '
              f'rough_seg={rs:8.4f} ({rs/base_s:5.2f}x)  postmean_std={pm.std():.3e}')


if __name__ == '__main__':
    for tk in ('Branin-2D', 'Levy-8D', 'Ackley-20D', 'Griewank-30D'):
        probe(tk)
