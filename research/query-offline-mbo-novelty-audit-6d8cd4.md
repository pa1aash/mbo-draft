---
vault_tag: offline-mbo-novelty-audit-6d8cd4
created: 2026-07-18T01:56:07Z
source: user-prompt
---

# THE QUESTION

I am preparing a paper for the AAAI-27 main technical track in offline model-based
optimization (offline MBO). I need to know, from the primary literature: WHICH OF MY
FINDINGS ARE GENUINELY NEW, what does existing work already own, and what is the strongest
publishable contribution available from what I have.

Answer with citations to papers you have actually fetched and read. Every novelty verdict
must be PRIOR WORK FOUND (with the citation and the specific overlapping sentence) or
NONE FOUND (with the exact queries you ran) or NOT VERIFIABLE. Never assert novelty you did
not check.

# CRITICAL METHOD REQUIREMENTS

A prior novelty check on this project was NOT produced by a real research pipeline. It was
hand-written from an agent's priors without fetcher waves or academic-API sweeps. Its files
openly admit this ("this is not a full 16-step multi-agent run"; "roughly half the corpus
was carried from repo docs"; "not a spawned corpus-critic subagent with a fetch wave").
Treat every claim below as UNCHECKED and every prior verdict as worthless.

- Hit Semantic Scholar, arXiv, OpenAlex BEFORE web search, for every claim.
- FETCH PRIMARY AND GREP IT. Do not trust search snippets or abstracts. Four fabricated
  citations have already been caught on this project.
- Run at least one adversarial search per claim ("criticism of X", "limitations of X",
  "X does not replicate").
- Citation traps confirmed on this project, carry them forward:
  Li/Rudner/Wilson is ICLR 2024 (Semantic Scholar back-propagates 2023 from the arXiv v1);
  Henderson et al. is AAAI 2018 (S2 says 2017); Benavoli et al. is JMLR 2016 (arXiv 2015).

# WHAT THE PAPER MEASURES

A controlled factorial decomposition: {deep ensemble, exact GP, sparse variational GP}
x {gradient ascent, perturbation hill-climbing, CMA-ES} = 9 cells, over 7 synthetic
functions (2D to 30D) and 7 Design-Bench tasks, under one shared evaluation protocol, with
LCB acquisition (mu - beta*sigma). Two-way ANOVA gives eta^2_surrogate = 0.37,
eta^2_optimizer = 0.01, eta^2_interaction = 0.17 on synthetic; the Design-Bench omnibus is
null (Friedman p=0.69, entire grid within one critical difference).

# THE CLAIMS TO CHECK — N1 THROUGH N9

N1. THE CONFOUND TAXONOMY.
Five unreported implementation choices, each individually decisive for the headline, each
now measured under control in offline MBO:
  (i)   TARGET SCALING — the ensemble regressed on raw targets spanning -2613 to +36 while
        both GP surrogates z-scored. Fixing it alone: eta^2_surr 0.367 -> 0.283.
  (ii)  CANDIDATE/ORACLE PROTOCOL — two optimizers proposed 256 designs and reported the
        oracle-selected best 128; the third proposed 128. Fixing it alone: 0.367 -> 0.450.
  (iii) OPTIMIZER TUNING — a trust-region constraint on gradient ascent closes the
        ensemble's collapse on high-dimensional tasks but not low-dimensional ones.
  (iv)  ENSEMBLE SIZE K — the paper's own ablation gives task-normalized ensemble scores
        0.95 / 0.52 / 0.32 / 0.18 at K = 2 / 3 / 5 / 10. It uses K=5 (citing
        Lakshminarayanan et al. 2017 as "standard") — where its own baseline is weakest.
        At K=2 the ensemble marginal (0.95) EXCEEDS the exact GP's (0.846).
  (v)   EFFECTIVE PESSIMISM — beta is fixed at 2 for every surrogate while their sigma
        magnitudes differ by an unmeasured factor, so different surrogate classes receive
        different effective conservatism from the same nominal setting.
Fixing (i) and (ii) together does NOT cancel: they net UP to eta^2_surr = 0.405, above the
published 0.37.
QUESTION: is the SHAPE of this contribution — "name the confounds, give the protocol that
removes them, show the ranking changes" — already owned? Check Ferrari Dacrema et al.
(RecSys 2019, "Are We Really Making Much Progress?"), Balduzzi et al. ("Re-evaluating
Evaluation", NeurIPS 2018), Henderson et al. ("Deep RL that Matters", AAAI 2018), Musgrave
et al. ("A Metric Learning Reality Check", ECCV 2020), Lucic et al. ("Are GANs Created
Equal?", NeurIPS 2018), Agarwal et al. ("Deep RL at the Edge of the Statistical Precipice",
NeurIPS 2021). Quantify the overlap. What is the RESIDUAL that is specific to offline MBO?

N2. K-CONTINGENCY OF SURROGATE-CLASS COMPARISON.
"Ensemble-versus-GP rankings in Bayesian optimization or offline MBO are contingent on
ensemble size, and the field-standard K=5 is the setting where the ensemble is weakest."
Nearest known: Abe et al. (NeurIPS 2022) — ensemble gains are capacity effects a single
larger model reproduces. Does ANYONE report K-dependence of a surrogate-class RANKING (not
just of ensemble accuracy)? Search the BO surrogate-comparison literature hard.

N3. UNMATCHED EFFECTIVE PESSIMISM.
"A shared beta across surrogate classes with different sigma scales delivers different
effective conservatism, so the acquisition was never matched." Is this named anywhere in
BO, offline RL, or offline MBO? Pessimism/conservatism literature specifically.

N4. DISTANCE-AWARE UNCERTAINTY — THE DANGEROUS NEIGHBOURHOOD.
Check hard: Liu et al., "Simple and Principled Uncertainty Estimation with Deterministic
Deep Learning via Distance Awareness" (SNGP, NeurIPS 2020); van Amersfoort et al. (DUE);
the "deep ensembles are confidently wrong far from the data" literature; Eriksson et al.
(TuRBO, trust-region BO).
THE HYPOTHESIS AT RISK: "the GP wins because its posterior variance grows away from the
data, which makes LCB an implicit trust region." If that is owned, say so.
IMPORTANT CONTEXT THAT CUTS BOTH WAYS: the paper's beta=0 control reports the GP-ensemble
gap barely moves (0.51 -> 0.47) with the sigma term removed entirely — which ARGUES AGAINST
a sigma-mediated mechanism. But that control has NO GENERATOR in the codebase and is being
recomputed right now. Check the literature for BOTH outcomes so the draft is ready either
way.

N5. NTK / SPECTRAL BIAS — THE STRONGEST OBJECTION TO OUR MECHANISM.
Jacot et al. (NeurIPS 2018, Neural Tangent Kernel); Rahaman et al. ("On the Spectral Bias
of Neural Networks", ICML 2019); Lee et al. ("Deep Neural Networks as Gaussian Processes",
ICLR 2018).
THE ADVERSARIAL READING, NOW EMPIRICALLY LOADED: infinite-width networks ARE Gaussian
processes, and finite ensembles approximate a GP posterior. So "the ensemble's posterior
mean is jagged" may be a finite-width / under-training artifact rather than a
surrogate-class property. Our K-sweep (K=2 scores 3x K=5) is EVIDENCE FOR that reading.
Li/Rudner/Wilson's own abstract states that "infinite-width BNNs are particularly promising,
especially in high dimensions."
This citation cuts AGAINST a mechanism paper and FOR a taxonomy paper. Fetch it, read it,
and engage it directly. A previous pass rated this "the single most valuable missing fetch"
and never ran it.

N6. THE CROSSED FACTORIAL ITSELF.
Re-confirm, adversarially, that no prior work runs a crossed surrogate x optimizer
factorial in offline MBO. This is load-bearing — one counterexample is fatal to the paper's
first contribution. Queries to run beyond the obvious: "factorial ANOVA surrogate
optimizer", "decompose surrogate versus acquisition", "which component matters black-box
optimization", "ablation surrogate optimizer offline optimization".
Also check: Li/Rudner/Wilson (ICLR 2024) compares surrogate classes with acquisition held
fixed; Tan et al. (ICLR 2025, learning-to-rank surrogates); Chemingui et al. (AAAI 2024,
policy-guided gradient search); Trabucco et al. (Design-Bench); Kim et al. 2025 survey of
offline MBO. How much does each already own?

N7. BIDIRECTIONAL SMOOTHNESS MANIPULATION.
Forward-citation check on IGNITE (NeurIPS 2024) and MS-DDEO (SWEVO 2022), 2025-2026: has
anyone manipulated surrogate smoothness in BOTH directions (smooth the network, roughen the
GP) to identify it as the causal axis of a surrogate-class performance gap?

N8. PLATFORM AND LIBRARY-VERSION DEPENDENCE OF BENCHMARK RESULTS.
We observe an ensemble cell moving ~0.5 normalized units between macOS and Linux on
TF-Bind-8, while the exact-GP cell matches to 1.000 and every synthetic cell reproduces to
12 decimal places cross-platform. The Design-Bench grid spans ~1.0-2.5 and the paper's
claim is that no cell is distinguishable from another.
QUESTION: is "platform or library version moves benchmark results by the same order as the
method differences under study" documented anywhere? Check the ML reproducibility
literature, numerical-determinism work, RNG portability, and Gundersen & Kjensmo (AAAI
2018).

N9. THE DE-CONFOUNDING DIRECTION — A RHETORICAL ASSET IF UNCLAIMED.
Our corrected headline (eta^2_surr = 0.405) is LARGER than the confounded published one
(0.37). We found five confounds, controlled for them, and the effect GREW.
Every reality-check paper I know of runs the other way — Recht et al. (ImageNet),
Melis et al. (LSTM), Ferrari Dacrema, Musgrave, Lucic: audit, effect shrinks or vanishes.
QUESTION: is there precedent for a reality-check / reproducibility paper whose audit
STRENGTHENS the audited finding? If this shape is unclaimed it is worth naming explicitly
in the paper.

# WHAT I NEED OUT OF THIS

1. A per-claim verdict table (N1-N9): FOUND / NONE FOUND / NOT VERIFIABLE, with citations
   and the specific overlapping sentence where prior work exists.
2. For each of these three candidate papers, the ONE SENTENCE a reviewer could not get
   from any prior paper — or a statement that no such sentence exists:
   (A) REPAIRED MEASUREMENT — the current draft with all confounds fixed.
   (C) MECHANISM — surrogate smoothness is the causal axis, demonstrated by manipulation
       in both directions.
   (D) CONFOUND TAXONOMY — five named confounds, the protocol that removes them, the
       demonstration that the rewarded differences move when you control.
3. The three strongest citations that could REJECT this paper, and what each would say.
4. AAAI-27 venue fit: given https://aaai.org/conference/aaai/aaai-27/areas-and-topics/,
   which primary topic best fits each of A/C/D, and what reviewer pool does each summon?
   Fetch the topics page; do not recall it.
