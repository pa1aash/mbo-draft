# Formal results (appendix source)

Notation. Objective $f:\mathcal X\to\mathbb R$; surrogate posterior mean $\mu:\mathcal X\to\mathbb R$ and uncertainty $\sigma:\mathcal X\to\mathbb R_{>0}$; LCB acquisition $L_\beta(x)=\mu(x)-\beta\sigma(x)$, $\beta\ge0$. For a distribution $Q$ on $\mathcal X$, say $L_\beta$ is a **valid $(1-\delta)$ lower bound under $Q$** if $\Pr_{x\sim Q}\!\big(f(x)\ge L_\beta(x)\big)\ge 1-\delta$.

## Proposition 1 (coverage of the premise is exactly LCB validity)
For any $Q,\beta,\delta$,
$$\Pr_{x\sim Q}\!\big(f(x)\ge L_\beta(x)\big)\;=\;\Pr_{x\sim Q}\!\big(\mu(x)-f(x)\le\beta\sigma(x)\big).$$
Hence $L_\beta$ is a valid $(1-\delta)$ lower bound under $Q$ **iff** the pessimism premise $\{\mu-f\le\beta\sigma\}$ has $Q$-probability $\ge 1-\delta$.

**Proof.** Since $\sigma>0$, pointwise $f(x)\ge\mu(x)-\beta\sigma(x)\iff \mu(x)-f(x)\le\beta\sigma(x)$. The two events coincide as subsets of $\mathcal X$, so they have equal probability under any $Q$. $\qquad\blacksquare$

**Why it matters.** The result is elementary, and that is the point: it makes "the pessimism guarantee holds" *operationally measurable* as a coverage frequency. We estimate the RHS under two distributions:
- $Q=\mathcal D$ (the data/in-distribution): measured coverage $\hat c_{\text{in}}$;
- $Q=\Pi$ (the proposal distribution — the designs the optimizer actually returns): measured coverage $\hat c_{\text{ood}}$.
Empirically (all tasks) $\hat c_{\text{in}}\ll 1-\delta$ at the default $\beta{=}2$ and $\hat c_{\text{ood}}\approx0$: the guarantee's premise fails, and fails hardest exactly where LCB operates. This is the mechanism behind gradient-ascent-on-ensembles collapsing to over-estimated OOD designs.

## Proposition 2 (conformal repair: valid in-distribution, and its shift-limited transfer)
Let $\{(x_i,f(x_i))\}_{i=1}^n$ be an exchangeable calibration sample from $P$, and define normalized residuals $r_i=\dfrac{|\mu(x_i)-f(x_i)|}{\sigma(x_i)}$. Let $\hat q$ be the $\lceil(n{+}1)(1-\delta)\rceil$-th smallest of $r_1,\dots,r_n$. Then for a fresh $x_{n+1}\sim P$ exchangeable with the calibration set,
$$\Pr\big(f(x_{n+1})\ge \mu(x_{n+1})-\hat q\,\sigma(x_{n+1})\big)\ \ge\ 1-\delta.$$
That is, replacing the arbitrary $\beta$ by the conformal multiplier $\hat q$ yields a distribution-free valid LCB **under $P$**. Under a shifted evaluation distribution $\Pi\ne P$ with density ratio $w=d\Pi/dP$, the guarantee degrades by the induced tilt; validity is recovered by weighting the calibration quantile with $w$ (weighted conformal, Tibshirani et al. 2019).

**Proof.** Two-sided normalized conformal scores $r_i$ are exchangeable with $r_{n+1}=|\mu(x_{n+1})-f(x_{n+1})|/\sigma(x_{n+1})$; by the standard split-conformal rank argument $\Pr(r_{n+1}\le\hat q)\ge1-\delta$. The event $r_{n+1}\le\hat q$ implies $\mu(x_{n+1})-f(x_{n+1})\le\hat q\,\sigma(x_{n+1})$, i.e. $f(x_{n+1})\ge\mu-\hat q\sigma$; probabilities are monotone, giving the bound. The covariate-shift clause is the weighted-exchangeability extension. $\qquad\blacksquare$

**Empirical instantiation.** $\hat q$ (calibrated to $\delta{=}0.1$) is 2.8–10.5 across tasks — i.e. $1.4\times$–$5\times$ the default $\beta{=}2$, quantifying how far raw ensemble $\sigma$ under-covers. In-distribution coverage of $\mu-\hat q\sigma$ is 0.95–0.97 (matching the $1-\delta$ target, as Prop 2 predicts); on the proposal $\Pi$ it is erratic (0.00–1.00), the measured signature of the $\Pi\ne P$ shift. This positions the paper's calibration arm as *diagnostic + mechanism* (distinct from post-hoc certification, Choi 2026, and from global-scalar conformal-LCB, UNIQ 2026), and motivates weighted conformal as the principled — but not free — repair.

## Verification notes (self-check)
- Prop 1: dimensionless, $\sigma>0$ used once; degenerate $\beta{=}0$ gives $\Pr(f\ge\mu)=\Pr(\mu-f\le0)$ ✓; $\beta\to\infty$ gives coverage $\to1$ ✓.
- Prop 2: reduces to the marginal split-conformal guarantee; the finite-sample $\lceil(n{+}1)(1-\delta)\rceil$ index is the standard one (valid, slightly conservative) ✓; at $\Pi=P$, $w\equiv1$ recovers the unweighted bound ✓.
