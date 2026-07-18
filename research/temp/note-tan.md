# Offline Model-Based Optimization by Learning to Rank (RaM) — ICLR 2025, arXiv:2410.11502

**Citation.** Rong-Xi Tan, Ke Xue, Shen-Huan Lyu, Haopu Shang, Yao Wang, Yaoyuan Wang, Sheng Fu, Chao Qian. *Offline Model-Based Optimization by Learning to Rank.* Published as a conference paper at **ICLR 2025** (arXiv:2410.11502v3, May 2025). Nanjing University + Hohai University + Huawei.

## What the paper does (from the body)
A METHOD paper, not a decomposition. It argues MSE-trained regression surrogates are the wrong objective for offline MBO because gradient ascent only needs the surrogate to *rank* designs correctly, not predict scores accurately. It proposes **RaM (Ranking-based Model)**: train the surrogate with a learning-to-rank loss (adapted from LETOR, list length m=1000) plus data augmentation and "output adaptation" for gradient-ascent hyperparameter robustness. Optimizes the learned surrogate by **gradient ascent** (Alg. line 645: `x_{t+1}=x_t+η∇_x L_opt`). Evaluated on Design-Bench; ablation studies validate its OWN two modules (data augmentation, output adaptation).

## Claim relevance

### N6 — crossed surrogate × optimizer factorial in offline MBO: **DOES NOT OWN (PARTIAL near-neighbor)**
- Tan varies surrogates with the OPTIMIZER HELD FIXED. Verbatim (§ motivation, l.283): *"To analyze the correlation between the OOD-MSE of a surrogate model and the score of the final design candidate obtained by conducting gradient ascent on the surrogate model, we select five surrogate models: a gradient-ascent baseline and four state-of-the-art forward approaches, COMs, IOM, ICT, and Tri-Mentoring."* → five surrogates, ONE optimizer (gradient ascent), a Spearman-correlation study — **not** a two-way factorial and **no variance decomposition / ANOVA**.
- Its "Compared methods" (l.766) are bundled method families (BO-qEI, CMA-ES, REINFORCE, Gradient Ascent + mean/min-ensemble variants; backward CbAS/MINs/DDOM/BONET/GTG; forward COMs/RoMA/IOM/BDI/ICT/Tri-Mentoring/PGS/FGM/Match-OPT). Comparing bundled methods ≠ crossing a surrogate-class set with an optimizer set under one protocol.
- **Residual for our paper (N6 stays NONE FOUND):** no offline-MBO work here crosses {surrogate class} × {optimizer} in a shared-protocol factorial with η² attribution. Tan is the closest (multi-surrogate, single-optimizer), which is the SAME design the query attributes to Li/Rudner/Wilson (surrogate classes, acquisition fixed). Neither crosses the optimizer axis.

### N1(iv)/N2 — ensemble size: not addressed (RaM uses ranking loss, mean/min-ensemble only as baselines).

## Cross-reference finds (bibliography, verbatim)
- **IGNITE = Dao, Nguyen, Truong, Hoang, "Incorporating surrogate gradient norm to improve offline optimization techniques," NeurIPS 2024** (confirms W1's resolution and authorship for N7).
- Sibling: **Dao et al., "Boosting offline optimizers with surrogate sensitivity," ICML 2024 (pp.10072-10090)** — a *surrogate-sensitivity/smoothness* angle relevant to N7 and worth checking for the corpus critic.

## Grep evidence
grepped: "gradient ascent" (many), "optimizer"/"CMA-ES"/"REINFORCE" (l.766 method list), "factorial"/"ANOVA"/"two-way" (**0 hits** — confirms no factorial/variance decomposition), "five surrogate" (l.283), "surrogate sensitivity"/"surrogate gradient norm" (l.1450-1455 bibliography).
