# Implementation-Fidelity Audit — "Decomposing the GP Advantage in Offline MBO"

Repo: `/Users/palaash/Downloads/MBO` @ `master` (8ebab0b). Every claim below carries `file:line` +
quoted code. Where the paper asserts something the code does not contain, it is marked
**NOT FOUND IN CODE**.

Files read completely: `code/mbo.py` (632), `code/db_tasks.py` (109), `code/run_all.py` (189),
`code/stats.py` (164), `code/analysis.py` (142), `code/figures.py` (417), `code/tables.py` (74),
`code/run05.py` (234), `code/run_beta0.py`, `code/run_gpcov.py`, `code/run_subsample.py`,
`code/gradtune.py`, `code/quicklook.py`, `cloud/queue/*.sh`, `cloud/{setup,fix_designbench,local_queue}.sh`,
`cloud/Dockerfile`, `requirements.txt`.

---

## A. ENSEMBLE (deep ensemble surrogate)

### A.1 Hyperparameters

All in the module-level config block, `code/mbo.py:19-28`:

```python
19  K_ENS = 5
20  HID = 96
21  TRAIN_EP = 35
22  LR = 3e-3
23  WD = 1e-4
24  BETA = 2.0
25  TOP = 128
26  OPT_STEPS = 100
27  LR_OPT = 0.05
28  DEVICE = torch.device('cpu')
```

| Item | Value | Evidence |
|---|---|---|
| K (members) | **5** | `mbo.py:19` `K_ENS = 5` |
| Width | **96** | `mbo.py:20` `HID = 96` |
| Depth | **2 hidden layers** (d→96→96→1, ReLU) | `mbo.py:125-126` |
| Epochs | **35** | `mbo.py:21` `TRAIN_EP = 35` |
| LR | **3e-3** | `mbo.py:22` `LR = 3e-3` |
| Optimizer | **Adam** | `mbo.py:137` `o = optim.Adam(m.parameters(), lr=LR, weight_decay=WD)` |
| Weight decay | **1e-4** | `mbo.py:23` `WD = 1e-4` |
| Batch size | **256** | `mbo.py:138` `dl = DataLoader(ds, batch_size=256, shuffle=True)` |
| Early stopping | **ABSENT** | see A.4 |
| Validation split | **ABSENT** | see A.4 |
| LR schedule | **ABSENT** | no scheduler anywhere in `train_ensemble` (`mbo.py:129-150`) |

Architecture, `code/mbo.py:122-127`:

```python
122  class MLP(nn.Module):
123      def __init__(s, d, hid=HID):
124          super().__init__()
125          s.net = nn.Sequential(nn.Linear(d, hid), nn.ReLU(),
126                                nn.Linear(hid, hid), nn.ReLU(), nn.Linear(hid, 1))
127      def forward(s, x): return s.net(x).squeeze(-1)
```

The training loop in full, `code/mbo.py:129-150`:

```python
129  def train_ensemble(x, y, d, seed=0, K=K_ENS, ep=TRAIN_EP, coms_alpha=None):
132      ds = TensorDataset(torch.FloatTensor(x), torch.FloatTensor(y))
133      ms = []
134      for k in range(K):
135          torch.manual_seed(seed*100 + k + (500 if coms_alpha is not None else 0))
136          m = MLP(d)
137          o = optim.Adam(m.parameters(), lr=LR, weight_decay=WD)
138          dl = DataLoader(ds, batch_size=256, shuffle=True)
139          m.train()
140          for _ in range(ep):
141              for xb, yb in dl:
142                  loss = nn.MSELoss()(m(xb), yb)
...
148                  o.zero_grad(); loss.backward(); o.step()
149          m.eval(); ms.append(m)
150      return ms
```

There is no validation loader, no metric tracked across epochs, no `best_state` checkpoint, and no
break condition. The loop runs exactly `ep` epochs unconditionally.

**Paper discrepancy:** `paper/aaai27/main.tex:87` states "trained by MSE for 35 epochs (Adam, lr
$3\times10^{-3}$)" — it omits `weight_decay=1e-4`, the only regularizer present.

### A.2 Members differ only by init (+ shuffle order) — NO bootstrap

`code/mbo.py:132` builds **one** `TensorDataset` from the full `(x, y)` and `code/mbo.py:138`
constructs a `DataLoader` over that same `ds` for every member. The only per-member difference is
the RNG seed at `code/mbo.py:135`:

```python
135          torch.manual_seed(seed*100 + k + (500 if coms_alpha is not None else 0))
```

That seed governs (i) `nn.Linear` weight init and (ii) the `shuffle=True` minibatch permutation.
**Every member sees identical data** — there is no `np.random.choice(..., replace=True)`, no
bagging, no per-member subsample. **Answer: init (and shuffle order) only; NO bootstrap resample.**

### A.3 Sigma computation — plain unbiased std across members, no noise term, no floor

`code/mbo.py:152-156`:

```python
152  def ens_lcb_torch(ms, beta):
153      def f(x):
154          ps = torch.stack([m(x) for m in ms])
155          return ps.mean(0) - beta*ps.std(0)
156      return f
```

- `sigma = ps.std(0)` — `torch.Tensor.std` defaults to `correction=1`, i.e. **unbiased (÷ K−1 = 4)**.
- **No aleatoric/noise term added.** The training labels carry noise (`mbo.py:38`,
  `s.y = (s.oracle(s.x) + np.random.randn(n) * noise)`) but the surrogate models no observation noise;
  `sigma` is pure inter-member spread.
- **No floor / no clipping** in the acquisition path. The only `sigma` floor in the repo is inside the
  conformal multiplier, `code/mbo.py:377`:
  ```python
  377      s = np.maximum(sigma_cal, 0.05 * np.mean(sigma_cal) + 1e-8)
  ```
  which is used only by `fit_conformal_multiplier`, never by `ens_lcb_torch`.
- Contrast: the GP/SVGP paths *do* clamp variance — `mbo.py:265` `post.variance.clamp_min(1e-12).sqrt()`,
  `mbo.py:342` same. The ensemble has no analogue, so `sigma → 0` collapse is unbounded.

The numpy mirror is a thin wrapper, `code/mbo.py:158-163`.

### A.4 Regularization / validation — essentially none

**The complete list of regularization in the ensemble is `weight_decay=1e-4` (`mbo.py:23`, applied at
`mbo.py:137`).**

- No dropout: `mbo.py:125-126` `nn.Sequential` contains only `Linear`/`ReLU`.
- No batch/layer norm: same line.
- No early stopping: `mbo.py:140` `for _ in range(ep):` — unconditional.
- **No held-out validation anywhere in `train_ensemble`** (`mbo.py:129-150`). No split, no val loss.
- No input normalization: unnecessary for synthetic (x drawn in `[0,1]^d` at `mbo.py:37`) and handled
  upstream for Design-Bench (`db_tasks.py:63` one-hot ∈ {0,1}; `db_tasks.py:66`
  `x01 = (x - self.xmin) / (self.xmax - self.xmin + 1e-12)`).
- **No output normalization for the ensemble.** `mbo.py:132` feeds raw `y` into the `TensorDataset`.
  For synthetic tasks that is raw oracle scale (Griewank ~1e3, `mbo.py:84`); for Design-Bench, `y` is
  pre-normalized to [0,1] by `db_tasks.py:45`. The GP paths *do* standardize
  (`mbo.py:224` `normalize_y=True`; `mbo.py:255` `yt = (yt - yt.mean()) / (yt.std() + 1e-8)`;
  `mbo.py:311-312`), so the ensemble is the only surrogate trained on unstandardized targets.
  (Note: `LCB = μ − βσ` is affine-equivariant, so the y-scaling asymmetry does not by itself change
  any argmax — but it does change the Adam/`weight_decay` optimization geometry for the ensemble.)

### A.5 Additional finding — the `ens_conformal` calibration fold is trained on

`code/mbo.py:405-416`:

```python
405      if name in ('ens', 'ens_conformal'):
406          ms = train_ensemble(x, y, dim, seed=seed, K=K, ep=ep)
...
410          n = len(x); cut = int(0.8 * n)
411          idx = np.random.RandomState(seed).permutation(n)
412          xc, yc = x[idx[cut:]], y[idx[cut:]]
413          with torch.no_grad():
414              ps = torch.stack([m(torch.FloatTensor(xc)) for m in ms])
415          q = fit_conformal_multiplier(ps.mean(0).numpy(), ps.std(0).numpy(), yc)
```

`ms` is fit on the **full** `(x, y)` at line 406; the "calibration fold" `xc, yc` at line 412 is a
20% slice of that same `(x, y)`. The split-conformal multiplier is therefore computed on **in-sample
residuals**, which violates the exchangeability premise the docstring at `mbo.py:370-376` invokes and
biases `q` downward. (The *separate* diagnostic in `run_calibration` does not have this bug — it draws
fresh points at `mbo.py:607`.)

---

## B. EXACT GP / SVGP

Note up front: **the grid's "Exact GP" row is `botorchgp`, not `fit_exact_gp`.**
`mbo.py:532` `GRID_SURROGATES = ['ens', 'botorchgp', 'svgp']`; `figures.py:37`
`SURR_LBL = {'ens': 'Ensemble', 'botorchgp': 'Exact GP', 'svgp': 'SVGP'}`. The sklearn
`fit_exact_gp` is only the `'gp'` **baseline** (`mbo.py:536`) and the surrogate used by
`run_gpcov.py:29`. These are two different GPs (see F.5).

### B.1 `fit_botorch_gp` — the grid's GP (`mbo.py:234-260`)

```python
253      xt = torch.DoubleTensor(x)
254      yt = torch.DoubleTensor(y).unsqueeze(-1)
255      yt = (yt - yt.mean()) / (yt.std() + 1e-8)
256      gp = SingleTaskGP(xt, yt)
257      if not matched:
258          fit_gpytorch_mll(ExactMarginalLogLikelihood(gp.likelihood, gp))
259      gp.eval()
```

| Item | Finding |
|---|---|
| Kernel | **NOT FOUND IN CODE.** `mbo.py:256` passes no `covar_module`; the kernel is whatever `SingleTaskGP`'s default is in the installed BoTorch. `requirements.txt:8` pins `botorch` with **no version**, so the kernel is not determined by this repo. **Paper discrepancy:** `main.tex:87` claims "ARD Matérn-$5/2$"; that is only guaranteed for the *sklearn* `fit_exact_gp` (B.2), which is not the grid's GP row. |
| ARD | NOT FOUND IN CODE (library default). |
| Priors | NOT FOUND IN CODE (library defaults). `mbo.py:238-240` explicitly relies on them: *"matched=True skips the marginal-likelihood fit so the GP keeps its prior/default hyperparameters"*. |
| MLL fit | `fit_gpytorch_mll(ExactMarginalLogLikelihood(...))` — `mbo.py:258`. **Optimizer / iters / lr are BoTorch defaults; NOT FOUND IN CODE.** |
| Jitter | NOT FOUND IN CODE (gpytorch default). |
| Noise floor/constraint | NOT FOUND IN CODE (BoTorch `SingleTaskGP` likelihood default). |
| Nmax | **800** — `mbo.py:234` `def fit_botorch_gp(x, y, seed, max_train=800, matched=False)` |
| y transform | Manual standardization, `mbo.py:255`. No `outcome_transform`/`input_transform`. |
| matched arm | `mbo.py:257-258` — MLL fit skipped entirely. |

LCB (in standardized units; affine-equivalent so argmax-preserving), `mbo.py:262-266`:
```python
265          return (post.mean - beta*post.variance.clamp_min(1e-12).sqrt()).squeeze(-1).float()
```

### B.2 `fit_exact_gp` — sklearn GP (the `'gp'` baseline + `run_gpcov.py`), `mbo.py:205-226`

```python
219      kernel = (ConstantKernel(1.0) * Matern(length_scale=np.ones(dim)*0.3, nu=2.5)
220                + WhiteKernel(noise_level=0.01))
221      gp = GaussianProcessRegressor(kernel=kernel,
222                                    n_restarts_optimizer=(0 if matched else 2),
223                                    optimizer=(None if matched else 'fmin_l_bfgs_b'),
224                                    normalize_y=True, alpha=1e-6)
225      gp.fit(x, y)
```

| Item | Finding |
|---|---|
| Kernel | `ConstantKernel(1.0) * Matern(nu=2.5) + WhiteKernel(0.01)` — `mbo.py:219-220` |
| ARD | **ON** — `length_scale=np.ones(dim)*0.3` is a length-scale **vector** (`mbo.py:219`) |
| Priors | **None.** sklearn kernels have bounds, not priors. Bounds are sklearn defaults (`length_scale_bounds=(1e-5,1e5)`, `noise_level_bounds=(1e-5,1e5)`) — NOT FOUND IN CODE (defaults). |
| MLL loop | optimizer `'fmin_l_bfgs_b'`, `n_restarts_optimizer=2` (i.e. **3** MLL optimizations) — `mbo.py:222-223`. Iters/lr are L-BFGS-B defaults; NOT FOUND IN CODE. |
| Jitter | **`alpha=1e-6`** — `mbo.py:224` |
| Noise floor | `WhiteKernel(noise_level=0.01)` initial, optimized within sklearn's default bounds — `mbo.py:220` |
| Nmax | **800** — `mbo.py:205` `max_train=800` |
| matched arm | `optimizer=None, n_restarts_optimizer=0` — hyperparameters **frozen at the initial values** (`mbo.py:222-223`) |

### B.3 The "score-biased" subsample — exact rule

The identical 4-line rule appears **three** times: `mbo.py:215-218` (exact GP), `mbo.py:248-251`
(botorch GP), `mbo.py:306-309` (SVGP). Quoting `mbo.py:214-218`:

```python
214      if len(x) > max_train:
215          top = np.argsort(y)[-int(max_train*0.2):]
216          rest = np.setdiff1d(np.arange(len(x)), top)
217          sel = np.concatenate([top, np.random.choice(rest, max_train-len(top), replace=False)])
218          x, y = x[sel], y[sel]
```

**Precise rule:** take the **top `0.2 × Nmax` points by label `y`** (deterministic, dataset-fixed), then
fill the remaining `0.8 × Nmax` by **uniform sampling without replacement from the complement**. Seeded
by `np.random.seed(seed)` at `mbo.py:213` (`mbo.py:247` / `mbo.py:304` for the other two).

Concretely: **Nmax=800 → 160 top-scoring + 640 uniform** (GPs); **Nmax=2000 → 400 top + 1600 uniform**
(SVGP). Note `int(max_train*0.2)` is an *absolute count*, so the "top 20%" is 20% of the **subsample
cap**, not 20% of the dataset — e.g. on Griewank-30D (N=8000, `mbo.py:81`) it is the top **2%** of the data.

The ensemble receives **no** subsample (`mbo.py:406` trains on the full `x, y`) — the asymmetry
`run_subsample.py` was written to probe (`run_subsample.py:1-5`).

A **separate, differently-parameterized** score-biased rule caps Design-Bench datasets,
`db_tasks.py:54-58`:
```python
54          if subsample and len(x) > subsample:                    # score-biased: top + random
55              idx = np.argsort(y01)
56              keep = np.concatenate([idx[-subsample//5:],
57                                     np.random.RandomState(0).choice(len(x), subsample*4//5, replace=False)])
58              x, y01 = x[keep], y01[keep]
```
Differences from the surrogate-side rule: `RandomState(0)` (**seed-independent**, so identical for all
16 DB seeds) and it samples from **`len(x)` — the whole dataset, not the complement** — so the random
fill can duplicate the top slice. Default cap = 8000 (`run_all.py:121`).

### B.4 SVGP (`mbo.py:295-331`)

```python
295  def fit_svgp(x, y, dim, seed, n_ind=128, iters=250, max_train=2000):
...
313      ind = xt[torch.randperm(len(xt))[:n_ind]].clone()
315      class SVGP(ApproximateGP):
316          def __init__(s):
317              vd = CholeskyVariationalDistribution(n_ind)
318              super().__init__(VariationalStrategy(s, ind, vd, learn_inducing_locations=True))
319              s.mean = gpytorch.means.ConstantMean()
320              s.cov = gpytorch.kernels.ScaleKernel(gpytorch.kernels.MaternKernel(nu=2.5, ard_num_dims=dim))
324      model = SVGP(); lik = gpytorch.likelihoods.GaussianLikelihood()
326      opt = torch.optim.Adam([{'params': model.parameters()}, {'params': lik.parameters()}], lr=0.01)
327      mll = gpytorch.mlls.VariationalELBO(lik, model, num_data=len(xt))
328      for _ in range(iters):
329          opt.zero_grad(); out = model(xt); loss = -mll(out, yt); loss.backward(); opt.step()
```

| Item | Finding |
|---|---|
| Inducing points | **128** — `mbo.py:295` `n_ind=128` |
| Inducing init | **Random subset of training x** — `mbo.py:313` `xt[torch.randperm(len(xt))[:n_ind]]`; learned thereafter (`learn_inducing_locations=True`, `mbo.py:318`) |
| Kernel | `ScaleKernel(MaternKernel(nu=2.5, ard_num_dims=dim))` — `mbo.py:320`. **ARD ON** (explicit `ard_num_dims`) |
| Mean | `ConstantMean()` — `mbo.py:319` |
| Fit | Adam, **lr=0.01**, **250 iters**, `VariationalELBO` — `mbo.py:326-329` |
| Minibatching | **NONE** — `mbo.py:329` `out = model(xt)` is a full-batch pass over all ≤2000 points, despite "Stochastic variational GP" (`mbo.py:296`) |
| Nmax | **2000** — `mbo.py:295` `max_train=2000` |
| Priors / noise floor / jitter | NOT FOUND IN CODE (gpytorch defaults) |
| matched arm | **SVGP is NOT affected by `--matched-tuning`.** `mbo.py:427` `s = fit_svgp(x, y, dim, seed)` — no `matched` kwarg. So the GATE-1 control freezes the GP's HPO but leaves the SVGP's 250 ELBO steps of per-run hyperparameter fitting intact, while the docstring at `mbo.py:403-404` asserts *"the ensemble/svgp already get no per-run HPO"* — false for SVGP, whose kernel hyperparameters and likelihood noise are optimized at `mbo.py:326-329`. |
| LCB | Un-standardized: `mbo.py:342` `(post.mean - beta*post.variance.clamp_min(1e-12).sqrt())*ys + ym` |
| Predict mode | `m.train()` at inference — `mbo.py:339`, documented `mbo.py:334-337` |

---

## C. OPTIMIZERS — BUDGET / CONFOUND CHECK

### C.1 Exact configuration

**Gradient** (`mbo.py:166-188`), invoked at `mbo.py:435`:
```python
435          xf = grad_opt(f_torch, torch.FloatTensor(x0), steps=OPT_STEPS)
166  def grad_opt(score_torch, x0, steps=OPT_STEPS, lr=LR_OPT, normalize=False, trust=None):
172      x = x0.clone().detach().requires_grad_(True)
174      o = optim.Adam([x], lr=lr)
175      for _ in range(steps):
176          o.zero_grad()
177          (-score_torch(x).mean()).backward()
182          o.step()
183          with torch.no_grad():
184              x.clamp_(0, 1)
188      return x.detach().numpy()
```
- steps = **100** (`OPT_STEPS`, `mbo.py:26`), lr = **0.05** (`LR_OPT`, `mbo.py:27`), Adam.
- **restarts = 1** (none). `x0` is the single 256-row init batch; no multi-start loop.
- batch = **256** rows (see D.2). `normalize`/`trust` default to `False`/`None` in the main grid
  (only `gradtune.py:17-25` varies them).

**Perturbation / hill-climb** (`mbo.py:190-202`), invoked at `mbo.py:438` `xf = perturb_opt(f_np, x0)`:
```python
190  def perturb_opt(score_np, x0, rounds=5, sigmas=(0.1, 0.05, 0.02)):
192      x_best = x0.copy()
193      best = score_np(x_best)
194      for _ in range(rounds):
195          for s in sigmas:
196              cand = np.clip(x_best + np.random.randn(*x_best.shape).astype(np.float32)*s, 0, 1)
197              sc = score_np(cand)
198              imp = sc > best
199              x_best[imp] = cand[imp]
200              best[imp] = sc[imp]
202      return x_best
```
- rounds = **5**, sigmas = **3** → **15** proposal batches, +1 initial scoring. Elementwise accept.
- "population" = the same 256 rows carried through.

**CMA-ES** (`mbo.py:269-292`), invoked at `mbo.py:441` `xf = cma_opt(f_np, x0, seed=seed)`:
```python
269  def cma_opt(score_np, x0, budget=3000, seed=0):
278      x_start = x0[int(np.argmax(score_np(x0)))]
280      es = cma.CMAEvolutionStrategy(x_start.tolist(), 0.2,
281          {'bounds': [0, 1], 'maxfevals': budget, 'verbose': -9, 'seed': seed + 1,
282           'CMA_diagonal': dim > 500})
285      pool = [x0]
286      while not es.stop():
287          sols = es.ask()
288          arr = np.clip(np.array(sols, dtype=np.float32), 0, 1)
289          es.tell(sols, [-v for v in score_np(arr)])
290          pool.append(arr)
291      allc = np.concatenate(pool)
292      return allc[np.argsort(score_np(allc))[-TOP:]]
```
- `maxfevals` = **3000** (`budget=3000`, `mbo.py:269`), initial σ = **0.2** (`mbo.py:280`),
  popsize = **pycma default** = `4 + floor(3·ln d)` — NOT FOUND IN CODE (library default).
- Seeded from a **single** point: the best-scoring row of `x0` (`mbo.py:278`) — i.e. CMA discards 255
  of the 256 initial candidates and starts one search from one point.

### C.2 Effective surrogate forward-evaluations per cell — the arithmetic

Measured empirically by counting calls into the score closure with a replica driver (pycma 4.4.4
installed locally), plus direct reading of the loops.

**Gradient:**
```
n_restarts × n_steps × batch = 1 × 100 × 256 = 25,600 surrogate point-evaluations
```
(`mbo.py:175` loops `steps=100`; `mbo.py:177` `score_torch(x)` evaluates all 256 rows at once; plus
100 backward passes, not counted.) **Dimension-independent.**

**Perturbation:**
```
(1 initial + rounds × |sigmas|) × batch = (1 + 5×3) × 256 = 16 × 256 = 4,096
```
(`mbo.py:193` initial `score_np`; `mbo.py:194-197` 15 proposal batches of 256.)
**Dimension-independent.**

**CMA-ES** = `256 (x_start selection, mbo.py:278) + popsize × generations (search loop, mbo.py:289)
+ |pool| (final rescoring, mbo.py:292)`. Measured:

| d | popsize | generations | search evals (popsize×gens) | pool | final rescore | **total** |
|---|---|---|---|---|---|---|
| 2 | 6 | 72 | 432 | 688 | 688 | 1,376 |
| 5 | 8 | 118 | 944 | 1,200 | 1,200 | 2,400 |
| 10 | 10 | 198 | 1,980 | 2,236 | 2,236 | 4,472 |
| 20 | 12 | 251 | 3,012 | 3,268 | 3,268 | 6,536 |
| 30 | 14 | 215 | 3,010 | 3,266 | 3,266 | 6,532 |
| 86 | 17 | 177 | 3,009 | 3,265 | 3,265 | 6,530 |
| 4740 | 29 | 104 | 3,016 | 3,272 | 3,272 | 6,544 |

(At d≤10 pycma's internal `tolfun`/`tolx` convergence criteria stop the run **before** `maxfevals=3000`
— e.g. Branin-2D gets only **432** search evaluations.)

### C.3 Are the budgets matched? — **NO**

Search-phase surrogate evaluations per cell:

| Optimizer | Evaluations | Ratio vs CMA(d=2) | Ratio vs CMA(d≥20) |
|---|---|---|---|
| **Gradient** | **25,600** (all d) | **59×** | **8.5×** |
| **Perturbation** | **4,096** (all d) | **9.5×** | **1.36×** |
| **CMA-ES** | **432 – 3,012** (d-dependent) | 1× | 1× |

**Gradient receives 6.25× the perturbation budget and 8.5–59× the CMA budget.** No budget-matching
code exists anywhere: there is no shared `n_evals` constant, no eval counter, and no cap wired into
`run_grid_cell` (`mbo.py:431-446`). `OPT_STEPS=100` (`mbo.py:26`), `rounds=5, sigmas=(0.1,0.05,0.02)`
(`mbo.py:190`), and `budget=3000` (`mbo.py:269`) were each set independently.

Two further asymmetries compound this:

1. **CMA's budget is dimension-dependent and shrinks the most on exactly the low-d tasks the paper's
   headline rests on** (Branin-2D: 432 evals vs gradient's 25,600 = 59×).
2. **CMA gets half the oracle-evaluated design set** — it returns 128 designs (`mbo.py:292`
   `[-TOP:]`) while gradient/perturbation return 256 (see D). Since `p100` is a **max** over the
   returned designs (`mbo.py:393-394`), CMA is drawing a max over 128 samples vs 256 for the other two.

**Paper discrepancy:** `main.tex:91` claims "the data split, **candidate budget**, input
normalization, and oracle scoring are held identical" and that this "is what licenses attributing
score differences to the surrogate×optimizer factors rather than to incidental protocol choices."
The candidate budget is **not** held identical on either axis (surrogate evaluations: 25,600 /
4,096 / 432–3,012; returned designs: 256 / 256 / 128).

---

## D. ACQUISITION + CANDIDATE SELECTION

### D.1 Beta and box constraints

- **β = 2.0** globally — `mbo.py:24` `BETA = 2.0`; threaded through `run_offline(..., beta=BETA)`
  (`mbo.py:448`) → `run_grid_cell` (`mbo.py:431`) → `build_surrogate` (`mbo.py:402`).
- **Is it swept?** Yes, but **only for the `ens:grad` cell**, not the grid. `run_all.py:72`
  `'beta': ['0.0', '0.5', '1.0', '2.0', '5.0']`, dispatched at `run_all.py:55`:
  ```python
  55      elif e == 'beta':
  56          m = {'p100': mbo.run_offline(task, seed, 'lcb', beta=float(spec['variant']), ep=ep)['p100']}
  ```
  and `'lcb'` resolves to ensemble + gradient (`mbo.py:460-467`). So `fig4_beta_sweep`
  (`figures.py:214-246`) and the paper's "pessimism helps on 6/7 tasks" characterize **one of nine
  cells**. The full-grid β=0 arm exists separately (`run_beta0.py:23`, writing
  `results_camera.json['mbo_beta0']`).
- **Box constraints: `[0,1]^d`, enforced per-optimizer**, not by a shared projection:
  `mbo.py:184` `x.clamp_(0, 1)` (gradient), `mbo.py:197` `np.clip(..., 0, 1)` (perturb),
  `mbo.py:281` `'bounds': [0, 1]` **and** `mbo.py:288` `np.clip(..., 0, 1)` (CMA — note CMA's
  `tell` receives the *unclipped* `sols` at `mbo.py:289` while the *clipped* `arr` is what was
  scored and pooled, so the CMA internal model is updated with a mismatched (x, f) pair whenever a
  sample lands outside the box).

### D.2 ★ THE KEY QUESTION: how are the final 128 candidates selected? ★

**Answer: none of (a)/(b)/(c) as posed. The 128 are selected by the ORACLE, post hoc, from the
optimizer's output set — and the output set itself is built differently by each optimizer.**

**Step 1 — the candidate set entering the optimizer is 256 rows, not 128.** `mbo.py:384-389`:
```python
384  def init_candidates(x, y, seed):
385      """top-TOP dataset points + sigma=0.05 perturbed copies (legacy protocol)."""
386      np.random.seed(seed)
387      xt = x[np.argsort(y)[-TOP:]]
388      xp = np.clip(xt + np.random.randn(*xt.shape).astype(np.float32)*0.05, 0, 1)
389      return np.concatenate([xt, xp])
```
Verified numerically: `init_candidates(...).shape == (256, d)` — top-128 dataset points **plus** 128
perturbed copies. (Also verified: the first 128 rows are **byte-identical across seeds**, because the
dataset is seed-0-fixed; see G.)

**Step 2 — each optimizer produces a different set, by a different rule:**

| Optimizer | Returns | Rule | Evidence |
|---|---|---|---|
| Gradient | **256** | **(a) the final iterate** — no best-ever tracking, no trace retained | `mbo.py:188` `return x.detach().numpy()` |
| Perturbation | **256** | **(b) per-slot best-LCB-ever-seen** (elementwise greedy accept) | `mbo.py:198-201` `imp = sc > best; x_best[imp] = cand[imp]` |
| CMA-ES | **128** | **(c) top-128 by surrogate LCB over ALL points visited** (pool = init 256 + every asked sample) | `mbo.py:285-292` `pool = [x0]` … `allc[np.argsort(score_np(allc))[-TOP:]]` |

So the three optimizers use **three different selection semantics**: (a) for gradient, (b) for
perturbation, (c) for CMA — the very thing the question asks to disambiguate is *not consistent
across the axis being compared*.

**Step 3 — the decisive one. `eval_designs` then filters to 128 BY ORACLE SCORE.** `mbo.py:391-394`:
```python
391  def eval_designs(task, x_final):
392      sc = task.oracle(x_final)
393      t = np.sort(sc)[-TOP:]
394      return float(t[-1]), float(np.median(t))   # p100, p50
```
`task.oracle(x_final)` is called on **every** returned design, then `np.sort(sc)[-TOP:]` keeps the
**oracle-best 128**. The reported metrics are `p100 = t[-1]` (max) and `p50 = np.median(t)`.

Consequences, verified numerically:

- **Gradient / perturbation:** 256 designs → oracle-scored → oracle-top-128 kept.
  `p100` = **max over 256 oracle calls**. `p50` = **median of the oracle-best half of 256**.
- **CMA-ES:** 128 designs (already surrogate-filtered at `mbo.py:292`) → `np.sort(sc)[-128:]` is a
  no-op. `p100` = **max over 128 oracle calls**. `p50` = **median of all 128**.

This means:

1. **The 128-design "budget" is enforced by the oracle, not by the acquisition function.** For
   gradient and perturbation the pipeline consumes **256** oracle evaluations per cell and reports the
   best; a real offline-MBO protocol must select its K designs using only `D` and the surrogate.
2. **`p50` is not comparable across the optimizer axis.** For gradient/perturbation it is the median
   of an oracle-selected top-50% subset (a strongly optimistic statistic); for CMA it is the median of
   an unfiltered surrogate-selected set. These are different estimands under the same column name.
3. **`p100` is not comparable either**: max-of-256 vs max-of-128.
4. Because `p100` is a max, the oracle-top-128 filter is a no-op *for `p100`* — but the underlying
   256-vs-128 oracle-call asymmetry remains, and it favors gradient/perturbation.

**Paper discrepancy:** `main.tex:91` — "hand it to the optimizer, **collect the 128 proposed
designs**, and score them with the ground-truth oracle" — and `main.tex:93` — "Each method proposes
128 candidates". The code proposes **256** for 2 of 3 optimizers and reduces to 128 **using the
oracle** (`mbo.py:392-393`), not by proposing 128.

### D.3 Discrete relaxation and argmax decoding

`db_tasks.py:60-68` (encode):
```python
60          if self.discrete:
61              self.L, self.C = x.shape[1], int(self._t.num_classes)
62              self.dim = self.L * self.C
63              x01 = self._onehot(x).reshape(len(x), -1)           # {0,1} subset of [0,1]
```
`db_tasks.py:70-74` (`_onehot`): scatter into `(N, L, C)` zeros → hard one-hot, **flattened to
`L*C`**. So the offline dataset lives on the **vertices** of the `[0,1]^{L·C}` cube.

`db_tasks.py:76-80` (decode):
```python
76      def _decode(self, x01):
78          if self.discrete:
79              return x01.reshape(-1, self.L, self.C).argmax(-1)          # per-position argmax
80          return x01 * (self.xmax - self.xmin) + self.xmin               # denormalize
```
`db_tasks.py:85-88` (oracle path):
```python
85      def oracle(self, x01):
86          x01 = np.clip(np.asarray(x01, np.float32), 0, 1)
87          yv = self._t.predict(self._decode(x01))                         # (n,1) raw score
88          return ((yv[:, 0] - self.ymin) / (self.ymax - self.ymin + 1e-12)).astype(np.float32)
```

Notes:
- The relaxation is a plain **box relaxation of the one-hot encoding** — there is **no simplex
  projection, no softmax, no temperature**. Optimizers clip to `[0,1]^{L·C}` independently per
  coordinate, so intermediate designs need not sum to 1 per position.
- **Paper discrepancy:** `main.tex:93` says "Discrete designs are relaxed to per-position class
  **logits**". They are not logits — they are one-hot indicators relaxed to the unit box
  (`db_tasks.py:63`, decoded by `argmax` at `db_tasks.py:79`).
- The surrogates are trained only on cube **vertices** (`db_tasks.py:63`) but the optimizers search
  the cube **interior** — every proposal is off-manifold for the surrogate by construction.
- Decoding is applied **only at the oracle boundary** (`db_tasks.py:87`). The surrogate never sees
  the decoded design, so the LCB the optimizer maximizes is evaluated at a continuous point whose
  argmax-decoded image is what gets scored. Many distinct continuous points collapse to one sequence.

---

## E. ORACLE

### E.1 Which tasks use an RF oracle — **6 of 8 defined; 5 of 7 actually reported**

`db_tasks.py:22-33`, verbatim:
```python
22  TASKS = {
23      'TFBind8':       'TFBind8-Exact-v0',
24      'TFBind10':      'TFBind10-Exact-v0',   # only exact oracle exists. ...
27      'Superconductor':'Superconductor-RandomForest-v0',
28      'GFP':           'GFP-RandomForest-v0',
29      'UTR':           'UTR-RandomForest-v0',
30      'AntMorphology': 'AntMorphology-RandomForest-v0',
31      'DKitty':        'DKittyMorphology-RandomForest-v0',
32      'Hopper':        'HopperController-RandomForest-v0',
33  }
```

- **Exact (native) oracle: TFBind8, TFBind10** — 2 tasks.
- **RandomForest oracle: Superconductor, GFP, UTR, AntMorphology, DKitty, Hopper** — 6 tasks.
- Reported in `results/results_db.json` (verified): `TFBind8, TFBind10, Superconductor, GFP, UTR,
  AntMorphology, DKitty` = 7 tasks, of which **5 use the RF oracle** (Hopper is defined but has no
  results; ChEMBL is omitted — `db_tasks.py:21` *"its mirror oracle pickle is corrupt"*).

The rationale is stated at `db_tasks.py:16-21`:
```python
17  # uses design-bench's RandomForest approximate oracle -- a first-class, literature-standard
18  # oracle (Superconductor's canonical oracle) that avoids the exact-oracle simulator deps
19  # (mujoco for Ant/DKitty/Hopper, TensorFlow for GFP-Transformer/UTR-ResNet).
```
This matches the paper (`main.tex:93`: "Superconductor, GFP, UTR, Ant, D'Kitty with random-forest
oracles").

### E.2 RF hyperparameters and training data — **NOT FOUND IN CODE**

**No RandomForest is constructed, configured, or fit anywhere in this repository.** Exhaustive grep
for `RandomForest|n_estimators|max_depth|RandomForestRegressor` across `code/` and `cloud/` returns
**only** the design-bench task-ID strings quoted above and prose comments — no
`sklearn.ensemble` import, no `.fit()`.

The oracle is entirely delegated to design-bench:
- `db_tasks.py:39` `self._t = design_bench.make(TASKS[short_name])`
- `db_tasks.py:87` `yv = self._t.predict(self._decode(x01))`

**RF hyperparameters (n_estimators, max_depth, max_features, split fraction): NOT FOUND IN CODE.**
They live in the `design-bench==2.0.20` package (`cloud/setup.sh:53`), which is not vendored and not
importable in this checkout (verified: `import design_bench` → `ModuleNotFoundError`; it exists only
in the pod-side `db` conda env, `setup.sh:52-53`). The RF's training data and any internal
train/validation split are likewise design-bench-internal and **not visible or controllable from this
repo**.

### E.3 ★ CIRCULARITY CHECK — no split exists in this repo ★

**The dataset the surrogates are fit on and the dataset behind the oracle are the same
design-bench object, and this repo creates no split between them.**

`db_tasks.py:42` — D and the oracle are drawn from one object:
```python
42          x, y = self._t.x, self._t.y            # y: (N,1)
```
`db_tasks.py:82-88` — the two accessors:
```python
82      def data(self):
83          return self._x.copy(), self._y.copy()
...
85      def oracle(self, x01):
86          x01 = np.clip(np.asarray(x01, np.float32), 0, 1)
87          yv = self._t.predict(self._decode(x01))                         # (n,1) raw score
88          return ((yv[:, 0] - self.ymin) / (self.ymax - self.ymin + 1e-12)).astype(np.float32)
```

`self._x` (line 68, `self._x = x01.astype(np.float32)`) derives from `self._t.x`; `self._t.predict`
is the oracle for that same `design_bench` task. `data()` returns **the whole thing** — there is **no
`train_test_split`, no holdout index, no masking** anywhere in `db_tasks.py` (109 lines, read in
full). The only row selection is the **score-biased subsample** (`db_tasks.py:54-58`), which *reduces*
D to a subset of the same rows — it does not withhold anything from the oracle.

So: `run_offline` (`mbo.py:453`) calls `x, y = task.data()` → fits the surrogate on D; `eval_designs`
(`mbo.py:392`) calls `task.oracle(x_final)` → the design-bench RF. Whether the RF was itself trained
on D is determined by design-bench's `ApproximateOracle` fitting, which is **NOT FOUND IN CODE**
(E.2). **What this audit can state with certainty: this repository takes no step to prevent
circularity — it neither withholds data from the oracle nor verifies that the oracle was fit on
disjoint data.** Design-Bench's approximate oracles are fit from the task dataset, so on the 5
RF-oracle tasks the "ground truth" is a model fit on (a superset of) the same rows the surrogate saw.

For **synthetic** tasks there is no circularity: `mbo.py:38` `s.y = (s.oracle(s.x) + np.random.randn(n) * noise)`
— the oracle is the analytic function (`mbo.py:43-45` etc.), and D is a noisy sample of it.

### E.4 Are native Design-Bench oracles importable/runnable here?

**In this checkout: no.** Verified: `python3 -c "import design_bench"` → `ModuleNotFoundError`.
`db_tasks.py:38` imports it lazily inside `__init__`, and `run_all.py:33-37` only imports `db_tasks`
under `--db`.

**On the provisioned pod: only partially, by design.**

- `cloud/setup.sh:52-53` builds a **separate py3.9 `db` conda env**:
  ```
  52    conda create -y -n db -c conda-forge python=3.9 rdkit
  53      && conda run -n db pip install design-bench==2.0.20 torch 'numpy<2' scipy scikit-learn
  ```
  Note `requirements.txt` (torch 2.11.0 / numpy 2.4.4 / sklearn 1.8.0) and the `db` env
  (`numpy<2`, later pinned to `numpy==1.23.5`, `scikit-learn==1.0.2`) are **mutually incompatible
  environments** — `cloud/Dockerfile:2-3` says so explicitly: *"Design-Bench (db) and
  design-baselines (baselines) are NOT in here — their legacy deps don't containerize cleanly"*.
- `cloud/fix_designbench.sh:2-4`: *"The upstream data hosting is DEAD (GCS bucket deleted, Google
  Drive dead)"*. It applies 8 patches.
- **Exact oracle imports are made silently optional**, `fix_designbench.sh:36-55`:
  ```
  36  # 7: exact/__init__.py hard-imports every oracle (gym/mujoco/nasbench) — make optional.
  50      body = "for _m,_n in %r:\n    try:\n        globals()[_n]=getattr(...)\n    except Exception:\n        pass\n"
  ```
  A `try/except: pass` over every exact oracle — so a broken mujoco/TF install yields a **silently
  missing** oracle rather than an error. This is precisely why RF oracles were chosen (`db_tasks.py:16-21`).
- `setup.sh:57-59`: mujoco install is best-effort; `02_db_factorial.sh:18` — *"Ant/DKitty need
  mujoco; they fail-soft if headless mujoco is unavailable"*.
- **Data provenance gap:** `fix_designbench.sh:27-28` downloads from a community HF mirror **only
  three tasks**:
  ```
  27  hf download beckhamc/design_bench_data --repo-type dataset --local-dir "$DBD" \
  28    --include 'tf_bind_8-SIX6_REF_R1/*' 'tf_bind_10-*/*' 'superconductor/*'
  ```
  Yet `results_db.json` contains **GFP, UTR, AntMorphology, DKitty** results (16 seeds each). The
  provenance of that data — given upstream hosting is documented as dead — is **NOT FOUND IN CODE**.
- `setup.sh:66` verifies only `TFBind8 d=32, TFBind10 d=40, Superconductor d=86`.

**Verdict for E.4:** the two exact oracles (TFBind8/10) are dep-free and runnable in the `db` env;
the mujoco/TF native oracles (Ant, DKitty, Hopper, GFP-Transformer, UTR-ResNet) are **not
established as runnable** — the setup makes them optional and fails soft, and the code deliberately
routes those tasks to RF oracles instead.

---

## F. COVERAGE MEASUREMENT (the diagnostic)

The entire diagnostic is `mbo.run_calibration` (`mbo.py:577-616`), dispatched by
`run_all.py:58-63`, and is what populates the `calibration` node of `results_camera.json` /
`results_db.json` and thus `fig3_coverage` (`figures.py:179-210`).

### F.1 The estimator

`mbo.py:364-368`:
```python
364  def coverage_of_premise(mu, sigma, f, beta):
365      """Empirical P(mu - f <= beta*sigma) = P(f >= mu - beta*sigma) — the ONE-SIDED
366      LCB lower-bound premise (Prop 1). Not the two-sided band |mu-f|<=beta*sigma:
367      under-prediction (f >> mu) never violates a lower bound and must not count as a miss."""
368      return float(np.mean((mu - f) <= beta * sigma))
```
A plain empirical mean of the one-sided indicator. `mu`/`sigma` come from `mu_sig`, `mbo.py:585-588`:
```python
585      def mu_sig(xx):
586          with torch.no_grad():
587              ps = torch.stack([m(torch.FloatTensor(xx)) for m in ms])
588          return ps.mean(0).numpy(), ps.std(0).numpy()
```

`c_hat_in` and `c_hat_ood`, `mbo.py:596-602`:
```python
596      # (2) premise coverage P(mu-f <= beta*sigma) [one-sided], in-distribution vs on LCB's OOD designs
597      x0 = init_candidates(x, y, seed)
598      xf = grad_opt(ens_lcb_torch(ms, BETA), torch.FloatTensor(x0), steps=OPT_STEPS)   # what LCB actually proposes
599      mu_o, sig_o = mu_sig(xf); f_o = task.oracle(xf)
600      betas = [0.5, 1.0, 2.0, 5.0]
601      cov_indist = {str(b): coverage_of_premise(mu, sig, task.oracle(xt), b) for b in betas}
602      cov_ood = {str(b): coverage_of_premise(mu_o, sig_o, f_o, b) for b in betas}
```

- **`c_hat_in`** = mean over **500** points `xt` (`mbo.py:591`, `n_test=500` at `mbo.py:577`).
- **`c_hat_ood`** = mean over the **256** gradient-ascent outputs `xf` (`mbo.py:598`; 256 because
  `init_candidates` returns 2·TOP — see D.2).

### F.2 What `f` is used as ground truth

**Always `task.oracle(...)`** — `mbo.py:599` `f_o = task.oracle(xf)` and `mbo.py:601`
`task.oracle(xt)`.

- **Synthetic:** the analytic **noiseless** function (`mbo.py:43-45` etc.). The surrogate was trained
  on **noisy** labels (`mbo.py:38` `+ np.random.randn(n) * noise`), so `mu` targets `f + ε` while
  coverage is scored against `f`. Defensible (the premise concerns `f`) but worth stating.
- **Design-Bench:** whatever `db_tasks.oracle` wraps (`db_tasks.py:87`) — i.e. the **RandomForest
  approximate oracle** for 5 of the 7 reported tasks (E.1). So "premise coverage" on those tasks is
  coverage of an RF's predictions, not of a physical ground truth.

### F.3 ★ The in-distribution test points are NOT drawn from the data distribution on Design-Bench ★

`mbo.py:591`:
```python
591      xt = np.random.uniform(0, 1, (n_test, task.dim)).astype(np.float32)
```
and the conformal calibration set, `mbo.py:607`:
```python
607      xc = np.random.uniform(0, 1, (500, task.dim)).astype(np.float32)
```

- **Synthetic: correct.** `mbo.py:37` draws the dataset as `np.random.uniform(0, 1, (n, dim))`, so
  uniform test points **are** exchangeable with D. `c_hat_in` is a valid in-distribution estimate.
- **Design-Bench: invalid.** The offline data are one-hot **cube vertices** for discrete tasks
  (`db_tasks.py:63`) and min-max-normalized real measurements for continuous tasks
  (`db_tasks.py:66`) — in neither case uniform on `[0,1]^d`. Drawing `np.random.uniform(0,1,(500,dim))`
  samples the cube **interior**, which for e.g. TFBind8 (d=32 one-hot) has probability zero under
  the data distribution and decodes via `argmax` (`db_tasks.py:79`) to essentially random sequences.
  **The right-hand "in-distribution" panel of `fig3_coverage` (`figures.py:183`) is therefore not
  measuring in-distribution coverage on Design-Bench**, and the same defect propagates to
  `q_conformal`, `cov_conf_indist`, `cov_conf_ood`, and `rho_err` for those tasks (`mbo.py:607-611`,
  `mbo.py:591-594`).

### F.4 Is sigma floored/clipped?

- **In the coverage estimator: NO.** `mbo.py:368` uses `sigma` raw; `mbo.py:588` returns `ps.std(0)` raw.
- **In the conformal multiplier: YES**, a relative floor — `mbo.py:377`
  `s = np.maximum(sigma_cal, 0.05 * np.mean(sigma_cal) + 1e-8)`, documented at `mbo.py:374-376`
  (*"A relative floor on sigma keeps the ratio finite when the ensemble collapses"*). This floor
  applies to `q` only; the `cov_conf_*` evaluation at `mbo.py:610-611` uses **unfloored** `sig`/`sig_o`:
  ```python
  610      cov_conf_indist = float(np.mean(task.oracle(xt) >= mu - q*sig))
  611      cov_conf_ood = float(np.mean(f_o >= mu_o - q*sig_o))
  ```
  So `q` is fit on floored σ and applied to unfloored σ — an inconsistency that matters exactly in
  the σ→0 collapse regime the paper is about.
- **GP/SVGP LCBs** clamp variance (`mbo.py:265`, `mbo.py:342` `clamp_min(1e-12)`); the ensemble does not (A.3).

### F.5 ★ IS COVERAGE COMPUTED FOR ALL 9 CELLS? — NO. ONE CELL. ★

**`run_calibration` hard-codes the ensemble surrogate and gradient-ascent proposals. Coverage is
computed for exactly 1 of the 9 grid cells (`ens:grad`).**

Evidence, `mbo.py:577-598`:
```python
577  def run_calibration(task, seed, n_test=500, ep=TRAIN_EP):
583      ms = train_ensemble(x, y, task.dim, seed=seed, ep=ep)          # <- ONLY the ensemble
...
598      xf = grad_opt(ens_lcb_torch(ms, BETA), torch.FloatTensor(x0), steps=OPT_STEPS)   # <- ONLY gradient
```
There is no `surrogate` or `optimizer` parameter. `run_all.py:74` confirms the experiment has a
single dummy variant: `'calibration': ['_']` — and `results_camera.json['calibration'][task]` has
exactly one key, `'_'` (verified).

Two further hard-codings inside the one cell:

1. **`beta` is swept in the bound but NOT in the proposal.** `mbo.py:598` generates `xf` at the global
   `BETA` (=2.0) **once**; `mbo.py:602` then evaluates `cov_ood` at β ∈ {0.5, 1, 2, 5} **on those same
   β=2 proposals**. So `fig3_coverage`'s x-axis, labelled "Pessimism strength β"
   (`figures.py:198`), varies the width of the bound while holding the proposal distribution fixed at
   β=2. The curve is *not* "coverage of the β-LCB pipeline at β".
2. `run_gpcov.py` extends coverage to a **second** surrogate, but **not** to the grid and **not
   without confounding**. `run_gpcov.py:28-35`:
   ```python
   28      ms = mbo.train_ensemble(x, y, task.dim, seed=seed, ep=mbo.TRAIN_EP)
   29      gp = mbo.fit_exact_gp(x, y, task.dim, seed)                      # sklearn
   34      xf_ens = mbo.grad_opt(mbo.ens_lcb_torch(ms, B), torch.FloatTensor(x0), steps=mbo.OPT_STEPS)  # ensemble proposals
   35      xf_gp = np.asarray(mbo.perturb_opt(mbo.gp_lcb_np(gp, B), x0), np.float32)                    # GP proposals
   ```
   **The ensemble's "own proposals" are GRADIENT proposals (line 34); the GP's "own proposals" are
   PERTURBATION proposals (line 35).** Surrogate and optimizer are varied **together**, so the
   cross-proposal contrast cannot separate "ensemble×gradient interaction" from "gradient travels
   further off-manifold than perturbation" — the exact confound the paper exists to dissect.
   `figures.py:393` nonetheless titles the plot *"The ensemble premise collapses only on its own
   gradient proposals, not on the GP's $-$ an ensemble$\times$gradient interaction"*, and this feeds
   the abstract's `0.73 / 0.41 / 0.97` (matching `05_findings.json['gp_coverage']['mean']`:
   `ens_indist=0.734, ens_own=0.413, ens_on_gp=0.970`).
   Additionally the GP here is `fit_exact_gp` (**sklearn**, `run_gpcov.py:29`) — **not** the
   `botorchgp` that is the grid's "Exact GP" row (`mbo.py:532`, `figures.py:37`). Fig. 8's "GP" and
   Fig. 1's "GP" are different models.

**Answer: coverage is computed for `ens:grad` only (1/9). `run_gpcov.py` adds `sklearn-GP:perturb`
(not a grid cell), for a total of 2 measured (surrogate, optimizer) pairs out of 9 — and those 2
vary both factors simultaneously.**

---

## G. SEEDING

### G.1 What seed 0 fixes

`mbo.py:31-39`:
```python
31  class Task:
32      """Offline dataset is FIXED across seeds (np.random.seed(0) at init);
33      per-seed randomness lives in training/init only. State this in the paper."""
34      def __init__(s, name, dim, n, noise):
35          s.name, s.dim, s.noise = name, dim, noise
36          np.random.seed(0)
37          s.x = np.random.uniform(0, 1, (n, dim)).astype(np.float32)
38          s.y = (s.oracle(s.x) + np.random.randn(n) * noise).astype(np.float32)
39      def data(s): return s.x.copy(), s.y.copy()
```

**Seed 0 fixes both the design matrix `x` AND the label-noise realization on `y`.** Line 36 resets
the **global** numpy RNG to 0; lines 37-38 then consume it for both draws.

### G.2 Is the synthetic dataset truly SHARED across all 30 seeds? — **YES, one single draw**

**Verified numerically:** constructing `Branin()` twice, and again after `np.random.seed(999)`,
yields **byte-identical** `x` and `y` every time (`np.array_equal` → `True` for both arrays in all
comparisons). The `np.random.seed(0)` at `mbo.py:36` is unconditional and runs on every `Task`
construction, so the dataset is invariant to ambient RNG state.

The path is airtight: `run_all.py:45` `task = build_task(spec['task'], ...)` → `run_all.py:38`
`return mbo.make_tasks([name])[0]` → `mbo.py:106` `tasks = [T() for T in ALL_TASKS]` → `Task.__init__`
→ `np.random.seed(0)`. Then `mbo.py:452-453`:
```python
452      np.random.seed(seed); torch.manual_seed(seed)
453      x, y = task.data()
```
re-seeds to the *per-cell* seed **after** the dataset already exists. So **all 30 seeds see the same
2000/3000/…/8000 rows with the same noise**.

The same holds for Design-Bench: the subsample uses a **fixed** `RandomState(0)`
(`db_tasks.py:57`), seed-independent, and `_TASK_CACHE` (`db_tasks.py:90`) memoizes the built task
per worker.

**Implication for H:** the 30 (synthetic) / 16 (DB) seeds are **replications of algorithmic
randomness only** — not of the data-generating process. Every per-task p-value, CI, and std in the
paper is conditional on a single dataset draw and carries **no** dataset-sampling uncertainty. The
docstring at `mbo.py:32-33` acknowledges this (*"State this in the paper"*); `main.tex:93` does say
"fixed dataset drawn once at seed 0".

### G.3 What varies per seed

| Component | Mechanism | Evidence |
|---|---|---|
| Ensemble init + shuffle order | `torch.manual_seed(seed*100 + k)` | `mbo.py:135` |
| GP / SVGP score-biased subsample (the random 80%) | `np.random.seed(seed)` | `mbo.py:213`, `mbo.py:247`, `mbo.py:304` |
| BoTorch/SVGP torch init | `torch.manual_seed(seed)` | `mbo.py:247`, `mbo.py:304` |
| SVGP inducing-point init | `torch.randperm` under that seed | `mbo.py:313` |
| Candidate init perturbation (**last 128 rows only**) | `np.random.seed(seed)` | `mbo.py:386-388` |
| `perturb_opt` noise | global numpy RNG (seeded upstream) | `mbo.py:197` |
| CMA seed | `seed + 1` | `mbo.py:281` |
| Design-Bench subsample | **does NOT vary** — `RandomState(0)` | `db_tasks.py:57` |

**Verified:** `init_candidates(x,y,0)[:128]` and `init_candidates(x,y,1)[:128]` are **identical**
(the top-TOP dataset points are a deterministic function of the seed-0-fixed dataset); only rows
128-255 (the perturbed copies) differ. So **half the optimizer's starting batch is identical across
all 30 seeds.**

---

## H. STATISTICS

### H.1 ANOVA — hand-rolled, no library, on per-task CELL MEANS

**Library: NONE.** Exhaustive grep for `statsmodels|anova|ols(|f_oneway|typ=|sum_sq` across the repo
returns **no** statistical-library ANOVA — only the hand-rolled η² in `run05.py:26-48` and its
duplicate in `quicklook.py:33-45`, plus the paper's prose. `statsmodels` is not in
`requirements.txt` (11 lines, read in full).

The canonical implementation, `run05.py:26-48`:
```python
26  def eta2(path, metric='p100'):
27      d = load(path)['mbo']
28      used, M = [], []
29      for t in d:
30          vals = {c: d[t][c][metric]['mean'] for c in CELLS
31                  if c in d[t] and isinstance(d[t][c].get(metric), dict)}
32          if len(vals) < 9:
33              continue
34          a = np.array([vals[c] for c in CELLS], float)
35          lo, hi = a.min(), a.max()
36          z = (a - lo) / (hi - lo) if hi > lo else np.zeros_like(a)
37          M.append(z.reshape(3, 3)); used.append(t)          # rows=surr, cols=opt
38      M = np.array(M)                                          # T,S,O
39      g = M.mean(); sst_ = ((M - g) ** 2).sum()
40      om3, sm3 = M.mean(axis=(0, 1)), M.mean(axis=(0, 2))     # optimizer, surrogate marginals
41      eta_opt = (len(used) * 3 * ((om3 - g) ** 2).sum()) / sst_
42      eta_surr = (len(used) * 3 * ((sm3 - g) ** 2).sum()) / sst_
43      inter = M.mean(axis=0) - sm3[:, None] - om3[None, :] + g   # (S,O) interaction cell effects
44      eta_inter = (len(used) * (inter ** 2).sum()) / sst_
```

- **Type I / II / III:** the question does not strictly apply — no library, no model formula. The
  design is **balanced and complete** (`run05.py:32` requires all 9 cells; verified: all 7 synthetic
  and all 7 DB tasks have all 9), and for a balanced complete design Type I = II = III. The SS
  formulas at lines 41-44 are the standard balanced-design main-effect / interaction SS.
- **★ UNITS: per-task, per-cell MEANS OVER SEEDS — not per-seed rows. ★** `run05.py:30`
  `d[t][c][metric]['mean']`. The `'all'` per-seed arrays exist in the JSON but are **not read here**.
  So the ANOVA operates on **7 tasks × 9 cells = 63 numbers, one observation per cell**.
- **Consequences:**
  - **There is no residual/error term and no replication within a cell** → **no F statistic, no
    p-value, no df**. `eta2()` returns only ratios. The paper reports η² but no ANOVA p-value —
    consistent with the code, but it means "the two-way ANOVA assigns the variance" (`main.tex:133`)
    is a variance decomposition, not an inferential test.
  - **`task` is NOT a factor in the model.** `sst_` (`run05.py:39`) is the total SS about the
    **grand** mean, so between-task variation in the normalized means inflates the denominator and
    **deflates every reported η²**. A correct blocked design would use `task` as a block and report
    partial η². The interaction term at line 43 is likewise the S×O interaction averaged over tasks
    (`M.mean(axis=0)`), with the T×S, T×O, T×S×O terms silently pooled into the denominator.
  - `quicklook.py:33-45` duplicates this and **omits the interaction term entirely**.

### H.2 The normalization applied before ANOVA — **per-task min-max, over the 9 grid cells**

`run05.py:34-36` (quoted above): `a` = the 9 cell means for one task; `lo, hi = a.min(), a.max()`;
`z = (a - lo) / (hi - lo)`. So **every task is rescaled so its best cell = 1 and its worst cell = 0.**

**Two different, inconsistent normalizations coexist:**

1. `run05.eta2` (`run05.py:35`) normalizes over **exactly the 9 `CELLS`** (`run05.py:20`).
2. `analysis.task_norm` (`analysis.py:29-34`) normalizes over **every key containing `':'`**:
   ```python
   31      vals = [v[metric]['mean'] for k, v in mbo[task].items()
   32              if ':' in k and isinstance(v.get(metric), dict) and 'mean' in v[metric]]
   33      lo, hi = (min(vals), max(vals)) if vals else (0.0, 1.0)
   34      return lo, (hi - lo) or 1.0
   ```
   Verified: `results_camera.json['mbo'][task]` also contains `ens_conformal:grad` and
   `ens_conformal:perturb` — both match `':' in k`. So `task_norm`'s range is computed over **11**
   cells, not 9. `task_norm` drives `analysis.sei_oei` (`analysis.py:37`), `analysis.fixed_optimizer_gap`
   (`analysis.py:76`), and `run05.method_score_matrix` (`run05.py:80`) — i.e. **SEI/OEI, the GATE-1
   retention number, and the rank/CD/TOST matrix are normalized on a different denominator than η².**

**Note on the min-max choice itself:** rescaling so the per-task best = 1 and worst = 0 forces every
task to contribute exactly the same total range regardless of whether its cells differ by 0.01 or by
2000 raw units (cf. `main.tex` Table 1: Branin ranges −0.40 to −14.01; Griewank −0.94 to −2613).
Effect sizes are therefore *rank-like within task*, and the η² magnitudes are not interpretable as
fractions of any raw-score variance.

### H.3 Friedman — input matrix shape

Three separate call sites, all with **rows = tasks, columns = methods**, passing one array per method:

- `stats.py:142-144`:
  ```python
  142          blocks = [[float(np.mean(seeds(t, m))) for t in tasks] for m in common]
  143          fr = stats.friedmanchisquare(*blocks)
  ```
  Each `blocks[i]` = method `i`'s **per-task mean over seeds**, length = n_tasks. Correct orientation
  for scipy (each argument = one "treatment" measured on all subjects). **n = 7 tasks; k = n methods.**
- `run05.py:94`: `sst.friedmanchisquare(*[M[i] for i in range(M.shape[0])])` where `M` is
  **methods × tasks** (`run05.py:80-83`). Correct.
- `figures.py:291`: `friedmanchisquare(*[R[:, j] for j in range(k)])` where `R` is
  **tasks × methods** (`figures.py:287`). Correct.

**Units are per-task means over seeds in all three cases** — the 30/16 seeds are collapsed before the
test. So Friedman's N is **7**, not 210.

### H.4 Nemenyi CD formula

`stats.py:52-64`:
```python
52  # Studentized-range q for the Nemenyi test (Demsar 2006, Table 5), alpha=0.05, indexed by k.
53  _Q05 = {2: 1.960, 3: 2.343, 4: 2.569, 5: 2.728, 6: 2.850, 7: 2.949, 8: 3.031,
54          9: 3.102, 10: 3.164, 11: 3.219, 12: 3.268}
56  def nemenyi_cd(k, n, alpha=0.05):
60      q = _Q05.get(k) if alpha == 0.05 else None
61      if q is None:
62          from scipy.stats import studentized_range           # scipy>=1.7
63          q = float(studentized_range.ppf(1 - alpha, k, np.inf)) / np.sqrt(2)
64      return q * np.sqrt(k * (k + 1) / (6.0 * n))
```
**CD = q_{α,k} · sqrt( k(k+1) / (6N) )** — the standard Demšar (2006) form, with tabulated q at
α=0.05 (k=9 → q=3.102). Self-checked at `stats.py:163`.

**A duplicate, less safe copy lives in `figures.py:292-294`:**
```python
292      q = {3: 2.343, 4: 2.569, 5: 2.728, 6: 2.850, 7: 2.949, 8: 3.031, 9: 3.102, 10: 3.164}.get(k, 3.164)
293      cd = q * np.sqrt(k * (k + 1) / (6 * N))
```
The `.get(k, 3.164)` default silently returns the **k=10** q for any k>10 (and for k=2) — a wrong
CD with no warning. For the 9-cell grid k=9, so the figure is currently correct.

### H.5 Bootstrap — **TASKS ONLY, never seeds**

`stats.py:146-155`:
```python
148          M = np.array([[np.mean(seeds(t, m)) for m in common] for t in tasks])  # tasks x methods
149          ranks = (-M).argsort(1).argsort(1) + 1
150          rng = np.random.default_rng(0)
151          boots = np.array([ranks[rng.integers(0, len(tasks), len(tasks))].mean(0) for _ in range(10000)])
152          print('\nBootstrap mean ranks (10k resamples over tasks):')
```
`rng.integers(0, len(tasks), len(tasks))` resamples **task indices with replacement**; `M` was already
collapsed over seeds at line 148. **Seeds are never resampled.** 10,000 replicates, `default_rng(0)`.
`run05.py:97-100` is the same scheme with **2,000** replicates, applied only to the single best method.

**★ Paper discrepancy (load-bearing). ★** `main.tex:137` states: *"**Task-and-seed bootstrap** $95\%$
CIs (synthetic, unmatched): $\eta^2_{\text{surr}}\in[0.25,0.57]$, $\eta^2_{\text{opt}}\in[0.01,0.19]$
(non-overlapping), $\eta^2_{\text{inter}}\in[0.11,0.26]$."*

- **No code in this repository bootstraps seeds** (grep: `resample|rng.integers` → only the two
  task-index resamplers above).
- **No code in this repository bootstraps η² at all** — `eta2()` (`run05.py:26-48`) returns point
  estimates; nothing resamples it.
- Those exact numbers are present in `results/05_findings.json` under a **`bootstrap_ci`** key —
  which **`run05.py` never writes**. The only `F[...]` assignments in `run05.py` are lines 61, 69,
  114, 117, 160, 183, 199 → keys `attribution, gate1, stats, equivalence, calibration, beta_sweep,
  crosscheck, K_ablation`. The shipped `05_findings.json` additionally contains **`beta0`,
  `subsample_control`, `gp_coverage`, `stats_9cell`, `bootstrap_ci`, `rf_robustness`** (verified).
  `05_findings.json.bak` has only the 7 `run05.py`-produced keys.
- **Conclusion: the generating code for the paper's η² confidence intervals — the "non-overlapping"
  claim that carries the headline attribution — is NOT FOUND IN CODE.** The values are stored to 2 dp,
  consistent with manual entry or an unversioned script. The same applies to `rf_robustness`
  (`spread_nonsub`, `friedman_3task_p`), `beta0`, `subsample_control`, and `stats_9cell`.

### H.6 Holm correction scope — **per method-pair × tasks; NOT across methods**

`stats.py:123-137`:
```python
124      print(f'Wilcoxon signed-rank vs {a.ref} (two-sided), Holm-corrected per family')
125      for m in methods:
126          if m == a.ref: continue
127          rows = [(t, seeds(t, a.ref), seeds(t, m)) for t in tasks]
129          praw = []
130          for t, x, y in rows:
131              try: praw.append(stats.wilcoxon(x, y).pvalue)
132              except ValueError: praw.append(1.0)   # identical samples
134          padj = holm(praw)
```
`holm()` is called **inside** the `for m in methods` loop, on `praw` = the p-values across **tasks**
for that one method-vs-ref comparison. **The family is {7 tasks} for a single method pair.**

With 15 methods present on the DB tasks (verified) and 7 tasks, that is **14 families of 7 tests =
98 tests**, each corrected only within its own 7. **The method dimension is uncorrected.** The
`holm()` implementation itself (`stats.py:21-30`) is correct — self-checked at `stats.py:159`
(`holm([0.01,0.04,0.03]) == [0.03,0.06,0.06]`).

Wilcoxon is **two-sided** (`stats.py:132`, scipy default; note `results/*.twosided.bak` files
suggest a prior one-sided variant). Each Wilcoxon is paired over **30 seeds within a task**
(`stats.py:85` `np.array(e[a.metric]['all'])`) — which, per G.2, is paired over algorithmic
randomness on a single fixed dataset.

### H.7 TOST implementation

`stats.py:32-50`, complete:
```python
32  def tost(x, y, margin, alpha=0.05):
38      d = np.asarray(x, float) - np.asarray(y, float)
39      n = len(d); mean, se = d.mean(), d.std(ddof=1) / np.sqrt(n)
40      if se == 0: se = 1e-12
41      df = n - 1
42      t_lo = (mean - (-margin)) / se           # H0: mean <= -margin
43      t_hi = (mean - margin) / se              # H0: mean >= +margin
44      p_lo = stats.t.sf(t_lo, df)              # one-sided upper
45      p_hi = stats.t.cdf(t_hi, df)             # one-sided lower
46      p_tost = max(p_lo, p_hi)
47      crit = stats.t.ppf(1 - alpha, df)        # (1-2a) CI uses one-sided crit at alpha
48      ci = (mean - crit * se, mean + crit * se)
49      equivalent = (ci[0] > -margin) and (ci[1] < margin)
50      return equivalent, p_tost, ci
```
- **Paired two-one-sided t-tests** (Lakens 2017), on the difference vector `d`.
- `se` uses `ddof=1`; `df = n-1`; `p_tost = max(p_lo, p_hi)`.
- CI is the **(1−2α) = 90%** interval (`crit = t.ppf(0.95, df)`), equivalence iff the CI ⊂ (−margin, +margin).
- Self-checked `stats.py:161-162`.
- **Units at the call site:** `run05.py:106-113` applies it to `M[best]` vs `M[order[-1]]` where `M`
  is the **task-normalized method × task matrix** (`run05.py:80-83`) → **n = 7 tasks**, paired across
  tasks, **not seeds**. Margins **0.5** and **0.3** on the [0,1] task-normalized scale
  (`run05.py:108-109`); `main.tex` abstract concedes "an equivalence test is underpowered at $N{=}7$".
- `stats.py:93-94` default margin (CLI path) = `0.1 * np.std(ref means across tasks)` — a
  data-dependent SESOI, i.e. the equivalence bound is derived from the data being tested.

---

## I. TASKS

### I.1 Synthetic tasks (`mbo.py:41-86`)

| Task | `name` | **d** | N | noise | Evidence |
|---|---|---|---|---|---|
| Branin | `Branin-2D` | **2** | 2000 | 0.05 | `mbo.py:42` `super().__init__('Branin-2D', 2, 2000, 0.05)` |
| Styblinski-Tang | `Styblinski-5D` | **5** | 3000 | 0.05 | `mbo.py:48` |
| Levy | `Levy-8D` | **8** | 4000 | 0.05 | `mbo.py:54` |
| Rosenbrock | `Rosenbrock-10D` | **10** | 5000 | 0.1 | `mbo.py:62` |
| Rastrigin | `Rastrigin-15D` | **15** | 5000 | 0.1 | `mbo.py:68` |
| Ackley | `Ackley-20D` | **20** | 5000 | 0.05 | `mbo.py:74` |
| Griewank | `Griewank-30D` | **30** | 8000 | 0.05 | `mbo.py:81` |

`mbo.py:86` `ALL_TASKS = [Branin, Styblinski, Levy, Rosenbrock, Rastrigin, Ackley, Griewank]` — **7
tasks**, confirmed by `results_camera.json` (verified: exactly these 7 keys).

Plus an on-demand **scaling ladder**, `mbo.py:88-101`:
```python
88  class ScaledAckley(Task):
94      def __init__(s, d, density=1.0):
95          n = int(min(max(250 * d * density, 2000), 25000))
96          name = f'Ackley{d}D' + (f'-x{density:g}' if density != 1 else '')
```
parsed from names by `mbo.py:103` `_LADDER = re.compile(r'^Ackley(\d+)D(?:-x([\d.]+))?$')`, i.e. any
`d` via `--tasks Ackley50D Ackley100D-x0.5` (`run_all.py:8`). **No ladder results are present** in
`results_camera.json` (verified: only the 7 fixed tasks).

All synthetic tasks are **maximization of a negated benchmark** (note the leading `-` in each
`oracle`), with x drawn uniform in `[0,1]^d` (`mbo.py:37`) and internally rescaled to each function's
native box (e.g. `mbo.py:44` `x1, x2 = x[:, 0]*15-5, x[:, 1]*15`).

### I.2 Design-Bench tasks

`dim` is computed at runtime, not declared: `db_tasks.py:62` `self.dim = self.L * self.C` (discrete),
`db_tasks.py:65` `self.dim = x.shape[1]` (continuous).

| Task | Oracle | **d** | Evidence for d |
|---|---|---|---|
| TFBind8 | Exact | **32** (L=8 × C=4) | `setup.sh:66` *"db verify OK (TFBind8 d=32, TFBind10 d=40, Superconductor d=86 …)"* |
| TFBind10 | Exact | **40** (L=10 × C=4) | `setup.sh:66` |
| Superconductor | RandomForest | **86** | `setup.sh:66` |
| GFP | RandomForest | **4740** | `mbo.py:282` comment: *"sep-CMA … for high-dim tasks (GFP d=4740, Hopper d=5126)"* |
| Hopper | RandomForest | **5126** | `mbo.py:282-283` (defined in `TASKS`; **no results present**) |
| UTR | RandomForest | **NOT FOUND IN CODE** (computed at `db_tasks.py:62`) |
| AntMorphology | RandomForest | **NOT FOUND IN CODE** (computed at `db_tasks.py:65`) |
| DKitty | RandomForest | **NOT FOUND IN CODE** (computed at `db_tasks.py:65`) |

Reported set (verified in `results_db.json`): **TFBind8, TFBind10, Superconductor, GFP, UTR,
AntMorphology, DKitty** = 7 tasks × 15 cells × 16 seeds (GFP has 14 cells — `gp` (sklearn exact GP)
is absent, consistent with the O(N³)/d=4740 cost).

**Queue/results mismatch:** `cloud/queue/02_db_factorial.sh:10` runs
`TASKS="TFBind8 TFBind10 Superconductor AntMorphology DKitty"` — **5 tasks**. **GFP and UTR are in the
results but in no queue invocation.** Likewise `02` runs `--exp mbo` only (lines 19, 23) and
`04_calibration.sh:12` runs calibration **without `--db`** (synthetic only) — yet `results_db.json`
contains a **`calibration` node with 16 seeds for all 7 DB tasks** (verified). **The invocation that
produced the Design-Bench coverage numbers in `fig3_coverage` is NOT FOUND IN CODE.**

Seed counts match the paper (`main.tex:93` "30 seeds on synthetic and 16 on Design-Bench"):
`01_synth_factorial.sh:12` `--seeds 30`; `02_db_factorial.sh:19` `--seeds 16`; verified 16 in
`results_db.json`.

### I.3 Separable CMA for d>500 — **YES**

`mbo.py:280-284`:
```python
280      es = cma.CMAEvolutionStrategy(x_start.tolist(), 0.2,
281          {'bounds': [0, 1], 'maxfevals': budget, 'verbose': -9, 'seed': seed + 1,
282           'CMA_diagonal': dim > 500})   # sep-CMA (O(dim)) for high-dim tasks (GFP d=4740,
283          # Hopper d=5126); full CMA's O(dim^3) eigendecomp is intractable there. Low-dim
284          # (<=500: all other tasks) keeps full CMA, so already-computed cells are unchanged.
```
`'CMA_diagonal': dim > 500` — the **only** location. Triggered for **GFP (d=4740)** and Hopper
(d=5126) only; every other task (max d=86) uses full CMA. Confirmed empirically (d=4740 →
`CMA_diagonal=True`, popsize 29). Matches `main.tex:89` ("separable variant when $d{>}500$").

Caveat: this makes **CMA a different algorithm on GFP than on the other 6 DB tasks**, while the
factorial treats "CMA-ES" as one level of the optimizer factor.

---

## Appendix — Cross-cutting findings not covered by A–I

1. **`sparse_gp` baseline uses a fake posterior.** `mbo.py:494-497`:
   ```python
   494          def score(xc):
   495              preds = pipe.predict(xc)
   496              fv = np.var(pipe.named_steps['ny'].transform(xc), axis=1)
   497              return preds - beta * fv / (np.mean(fv) + 1e-8)
   ```
   Self-documented at `mbo.py:491-493`: *"legacy uncertainty proxy = variance of Nystroem features;
   it is NOT a posterior std."* This is the `sparse_gp` **baseline**, distinct from the `svgp` grid row.
2. **`cbas` is not CbAS.** `mbo.py:503-506`: *"legacy 'CbAS' is a CEM-style elite-resampling loop
   scored by the ensemble (no VAE, mixes oracle-noised y with model predictions). Label it honestly
   in the paper … or implement real CbAS before claiming the citation."* `tables.py:20` still labels
   it `'CbAS'` and `main.tex` cites `\citep{brookes2019cbas}`; `run05.py:174` cross-checks it against
   `cbas_official`.
3. **`cbas` uses a different candidate protocol entirely** — `mbo.py:524`
   `xf = np.clip(pop[np.argsort(scores)[-TOP:]], 0, 1)` → 128 designs selected by a **mixture of
   oracle-noised labels `y` and model predictions** (`mbo.py:523` `scores = np.concatenate([elite_scores, preds])`,
   where `elite_scores` originate from `y` at `mbo.py:508`). So real labels leak into its selection.
4. **`requirements.txt` cannot have produced the Design-Bench results.** Its header claims *"Versions
   pinned from the environment the existing results were produced with"* — but the `db` env is
   `numpy==1.23.5` / `scikit-learn==1.0.2` / py3.9 (`fix_designbench.sh:22-24`, `setup.sh:52-53`) vs
   `requirements.txt`'s `numpy==2.4.4` / `scikit-learn==1.8.0` / py3.11 (`setup.sh:42`). Two
   different environments produced `results_camera.json` and `results_db.json`. `botorch`, `gpytorch`,
   and `cma` are **unpinned** in both (`requirements.txt:8-11`, `fix_designbench.sh:22`) — so the
   grid's GP kernel (B.1) is not reproducible from the repo.
5. **Per-cell failures are silent in the aggregate.** `run_all.py:165-169` catches every cell
   exception, prints, and continues; `run_all.py:170-171` drops `metrics is None` cells. `agg()`
   (`run_all.py:83-86`) then averages **however many seeds survived**, and `have()`
   (`run_all.py:98-104`) checks only `len(all) >= seeds`. A cell that failed on some seeds is
   reported with no marker of reduced n. (Observed: GFP has 14 cells vs 15 elsewhere.)
