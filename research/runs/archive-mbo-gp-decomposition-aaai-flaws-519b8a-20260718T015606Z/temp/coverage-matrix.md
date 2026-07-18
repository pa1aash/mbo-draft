## Coverage Matrix — query phrase → atomic item mapping

| Query phrase (verbatim) | Mapped atomic item(s) | Scope check | Gap? |
|---|---|---|---|
| "AAAI-27 acceptance prospects" | Sub-Q9 (what AAAI rewards in measurement/null papers); heading 8 | OK — acceptance standards, not just flaws | No |
| "scientific flaws" | Sub-Q10–13 (four levels); headings 9–12 | OK — all four levels separately mapped | No |
| "controlled surrogate×optimizer factorial decomposition" | Sub-Q1; heading 1 | OK — prior art AND novelty both asked | No |
| "{deep ensemble, exact GP, sparse variational GP}" | Entities: Li 2024 (surrogate comparison); Sub-Q7 (ensemble uncertainty) | OK — all three surrogate classes in scope, not just ensembles | No |
| "{gradient ascent, perturbation, CMA-ES}" | Sub-Q1; Entities PGS, GAMBO (optimizer-as-factor) | OK | No |
| "7 synthetic + 7 Design-Bench tasks" | Sub-Q5, Sub-Q6; heading 5 | OK | No |
| "η²=0.37 vs 0.01 ... interaction η²=0.17" | Sub-Q8, Sub-Q12; heading 7, 11 | OK — effect-size validity AND the ANOVA-on-normalized-scores critique | No |
| "the GP's smooth posterior MEAN rather than its calibration" | Sub-Q2; heading 2 | OK — NTK/spectral-bias/Lipschitz all named as sub-scope | No |
| "LCB 'premise coverage' diagnostic" | Sub-Q3; heading 3 | OK | No |
| "Prop 1 ... exactly equivalent to LCB validity" | Sub-Q3, Sub-Q10 (triviality as a manuscript flaw); heading 3, 9 | OK — both the prior-art reading and the "padding" reviewer objection | No |
| "split-conformal repair (Prop 2)" | Entities Tibshirani 2019, Stanton 2022, Choi 2026, UNIQ 2026; heading 3 | OK | No |
| "null result ... Friedman p=6e-5 ... p=0.69 ... TOST underpowered at N=7" | Sub-Q12; heading 7, 11 | OK — TOST/equivalence/power explicitly in scope | No |
| "synthetic→real validity collapse" | Sub-Q5; heading 5 | OK — is the collapse already documented | No |
| "(a) the manuscript — claims, framing, positioning, prose, figures, related work" | Sub-Q10; heading 9 | OK — all six named facets | No |
| "(b) the experiments — identifiability, controls, confounds, optimizer query budgets, baselines" | Sub-Q11; heading 10 | OK — budget-confound explicitly named | No |
| "(c) the statistics — validity of every inferential claim" | Sub-Q12; heading 7, 11 | OK — ANOVA, Friedman/Nemenyi, TOST, bootstrap, Holm all enumerated | No |
| "(d) the artifact — reproducibility ... what a reviewer running the code would find" | Sub-Q13; heading 12 | OK | No |
| "OFFLINE MODEL SELECTION" (caps in query = emphasis) | Sub-Q4; heading 4 | OK — offline MBO AND offline RL both in scope; novelty + open-problem status both asked | No |
| "Design-Bench critiques, benchmark saturation" | Sub-Q6; heading 5 | OK | No |
| "criticisms and limitations of ... deep-ensemble uncertainty quality" | Sub-Q7; heading 6 | OK | No |
| "ANOVA-on-normalized-scores effect sizes in ML benchmarking" | Sub-Q8; heading 7 | OK — the normalization critique, not ANOVA generally | No |
| "acceptance evidence for 'controlled study without a new method' papers" | Sub-Q9; heading 8 | OK — AAAI/NeurIPS/ICML all three venues | No |
| "Severity-rate every finding: P0/P1/P2/P3" | required_formats[0] | OK — binding taxonomy | No |
| "evidence, why a reviewer raises it, cost to fix (hours/CPU), fixable pre-deadline" | required_formats[1] | OK — all four per-finding fields | No |
| "at least one adversarial search on criticism/limitations of each core claim" | Sub-Q14; heading 13 | OK — "each core claim" = all three contributions | No |
| "Is such a decomposition novel" / "is a coverage-driven ... rule novel" | required_formats[2] (novelty status marking) | OK — novelty must be checked, never asserted | No |

**Zero `Gap? = YES` rows.** Decomposition accepted.

### Scope-broadening notes applied during the audit

- "conformal BO" was initially narrowed to offline MBO only. Broadened: the online
  BO conformal line (Stanton, Deshpande-Kuleshov) is the nearest prior art for
  Proposition 2 and must be searched even though the paper is offline.
- "offline model selection" was initially mapped only to offline MBO. Broadened to
  include offline RL policy selection, which is the larger and better-developed
  literature and the more likely source of a novelty-refuting citation.
- "the GP's smooth posterior mean" was initially mapped only to GP literature.
  Broadened to NTK / spectral-bias / Lipschitz-smoothness of neural nets, since the
  paper's mechanism claim is as much about what ensembles do as about what GPs do.
