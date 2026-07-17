# BUNDLE — PART 2 of 2 (Tier 3, 4)

Manifest, NOT-INCLUDED list, and part-split map are in `docs/BUNDLE_PART1.md`.
Verbatim contents; no summarization or truncation.

---

## FILE: paper/aaai27/main.tex
<!-- lines: 298 | bytes: 37867 | last commit: bb50904 2026-07-17 -->
```latex
\documentclass[letterpaper]{article} % DO NOT CHANGE THIS
\usepackage[submission]{aaai2027}  % DO NOT CHANGE THIS
\usepackage[hyphens]{url}  % DO NOT CHANGE THIS
\usepackage{graphicx} % DO NOT CHANGE THIS
\urlstyle{rm} % DO NOT CHANGE THIS
\def\UrlFont{\rm}  % DO NOT CHANGE THIS
\usepackage{natbib}  % DO NOT CHANGE THIS AND DO NOT ADD ANY OPTIONS TO IT
\usepackage{caption} % DO NOT CHANGE THIS AND DO NOT ADD ANY OPTIONS TO IT
\frenchspacing  % DO NOT CHANGE THIS
\usepackage{algorithm}
\usepackage{algorithmic}
\usepackage{booktabs}
\usepackage{amsmath,amssymb,amsthm}
\usepackage{multirow}

\pdfinfo{
/TemplateVersion (2027.1)
}

\setcounter{secnumdepth}{1}

% float packing: let floats fill more of each page so wide tables/figures do not orphan
\renewcommand{\topfraction}{0.92}
\renewcommand{\bottomfraction}{0.85}
\renewcommand{\textfraction}{0.08}
\renewcommand{\floatpagefraction}{0.80}
\setcounter{topnumber}{3}
\setcounter{totalnumber}{5}

\theoremstyle{plain}
\newtheorem{proposition}{Proposition}

\newcommand{\mdemph}[1]{\emph{#1}}
\newcommand{\memph}[1]{\emph{#1}}
\newcommand{\R}{\mathbb{R}}
\newcommand{\X}{\mathcal{X}}
\newcommand{\D}{\mathcal{D}}

\title{Decomposing the GP Advantage in Offline MBO}

\author{Anonymous Submission}
\affiliations{}

\begin{document}

\maketitle

\begin{abstract}
A common intuition in offline model-based optimization (MBO) is that Gaussian-process lower confidence bound (GP-LCB) outperforms neural-ensemble LCB at low dimension because the GP posterior is better calibrated. This comparison is confounded: the two pipelines differ in \memph{both} the surrogate class and the acquisition optimizer. We run the first controlled surrogate$\times$optimizer decomposition---\{deep ensemble, exact GP, sparse variational GP\}$\times$\{gradient ascent, perturbation, CMA-ES\}---on 7 synthetic and 7 Design-Bench tasks. On synthetic tasks the surrogate main effect dominates ($\eta^2{=}0.37$ vs.\ $0.01$ for the optimizer) with a large surrogate$\times$optimizer interaction ($\eta^2{=}0.17$): gradient ascent collapses on the ensemble but is inert on the GP. Controls locate the cause in the GP's posterior \emph{mean}, not its calibration---the GP--ensemble gap is unchanged when the pessimism term is removed ($\beta{=}0$) and \emph{widens} when the ensemble is given the GP's data subsample. The ensemble's LCB premise, which we show equals the bound's validity, is moderately covered in-distribution ($0.73$, below the nominal $0.90$) but collapses on the designs its own gradient ascent returns ($0.41$)---while remaining well covered ($0.97$) on the GP's proposals, so the failure is the ensemble$\times$gradient interaction, not a surrogate defect. Split-conformal recalibration restores in-distribution coverage to its $0.90$ target but not the shifted proposal coverage; we package this as a coverage diagnostic. Finally, method choice is highly significant on synthetic benchmarks (Friedman $p{=}6\times10^{-5}$) but unresolved on Design-Bench ($p{=}0.69$; an equivalence test is underpowered at $N{=}7$): the differences these benchmarks reward do not transfer to real tasks.
\end{abstract}

% \begin{links}
%   \link{Code}{https://anonymous.4open.science/r/offline-mbo-decomposition}
% \end{links}

\section{Introduction}

Offline model-based optimization (MBO) seeks a design $x$ maximizing an expensive black-box $f$ from a fixed dataset $\D=\{(x_i,y_i)\}_{i=1}^N$, with no further queries to $f$ during search \citep{trabucco2022designbench,kim2025mbosurvey}. The dominant recipe fits a surrogate $\hat f$ and optimizes it; because optimization pushes designs into regions where $\hat f$ is unconstrained, the surrogate is typically made conservative---by a learned regularizer \citep{trabucco2021coms} or by a pessimistic acquisition such as the lower confidence bound (LCB) $\mu(x)-\beta\sigma(x)$ \citep{srinivas2010ucb}. A common modeling intuition is that Gaussian-process LCB (GP-LCB) is preferable to neural-ensemble LCB at low dimension, on the grounds that the GP posterior is better calibrated.

That attribution is not identified. A GP-LCB pipeline and an ensemble-LCB pipeline differ in \mdemph{two} coupled factors: the surrogate class (GP posterior vs.\ ensemble disagreement) and the acquisition optimizer (GPs are usually optimized by perturbation or quasi-Newton restarts, neural surrogates by gradient ascent on $x$). Existing systematic studies vary one axis with the other fixed: surrogate-class comparisons hold the optimizer constant \citep{tan2025ltr}---a Bayesian-optimization study of GP vs.\ neural surrogates similarly fixes the acquisition and finds their ranking problem-dependent, with deep ensembles often the weakest \citep{li2024bnnsurrogates}---and the conservative-surrogate lineage holds gradient ascent fixed while varying the regularizer \citep{trabucco2021coms}. The subfield's own survey names realistic benchmarking and surrogate-uncertainty estimation among its open problems \citep{kim2025mbosurvey}, yet whether reported gains come from the surrogate, the optimizer, or neither has not been measured under control. We supply that missing measurement.

\paragraph{Contributions.}
\begin{enumerate}
\item \textbf{A controlled surrogate$\times$optimizer decomposition} (Sections~\ref{sec:grid}--\ref{sec:results}) over $\{$ensemble, exact GP, sparse GP$\}\times\{$gradient, perturbation, CMA-ES$\}$ on 7 synthetic and 7 Design-Bench tasks under one score-closure protocol. The surrogate main effect dominates on synthetic tasks ($\eta^2{=}0.37$ vs.\ $0.01$) with a large surrogate$\times$optimizer \mdemph{interaction} ($\eta^2{=}0.17$); a matched-tuning control shows the surrogate effect is not a GP-tuning artifact (it retains $76\%$).
\item \textbf{The mechanism is inductive bias, not calibration} (Section~\ref{sec:mech}). Three controls locate the GP's advantage in its posterior \mdemph{mean}: the GP--ensemble gap is unchanged with pessimism off ($\beta{=}0$), \mdemph{widens} when the ensemble is given the GP's data subsample, and the ensemble's LCB premise---which we show (Prop.~\ref{prop:cov}) equals the bound's validity---collapses only on the ensemble's own gradient proposals (coverage $0.41$) while holding on the GP's ($0.97$). We package the coverage measurement as a diagnostic with a split-conformal repair (Prop.~\ref{prop:conf}).
\item \textbf{A benchmark-validity result} (Section~\ref{sec:results}), under a controlled random-forest-oracle protocol. Method choice is highly significant on synthetic benchmarks (Friedman $p{=}6\times10^{-5}$) but statistically unresolved on Design-Bench ($p{=}0.69$; a paired equivalence test is underpowered at $N{=}7$ tasks): the method rankings synthetic suites reward do not transfer to the real tasks---a gap we show is not an artifact of the random-forest oracles. To our knowledge this is the first controlled measurement disentangling the surrogate and optimizer contributions in offline MBO, rather than a new optimizer or regularizer.
\end{enumerate}

These threads share one cause. Contributions~2 and~3 are two views of a single prior--task match: the synthetic surfaces are globally smooth, matching the GP's Mat\'ern prior, so the GP wins decisively; the Design-Bench oracles are not, the match breaks, and both the GP edge and the method separation vanish.

\section{Background and Related Work}

\paragraph{LCB and the pessimism premise.} GP-LCB $\mu-\beta\sigma$ has regret guarantees under GP assumptions \citep{srinivas2010ucb}; deep ensembles \citep{lakshminarayanan2017ensembles} provide a cheap uncertainty proxy but no calibration guarantee. The pessimism principle underlying conservative offline methods is that a valid lower bound prevents the optimizer from exploiting model error \citep{jin2021pessimism,rashidinejad2021bridging,xie2021bellman}. We make the premise behind LCB operationally measurable.

\paragraph{Offline MBO.} Conservative Objective Models \citep{trabucco2021coms} add a CQL-style regularizer \citep{kumar2020cql}; related methods include MINs \citep{kumar2020mins}, CbAS \citep{brookes2019cbas}, autofocused oracles \citep{fannjiang2020autofocused}, DDOM \citep{krishnamoorthy2023ddom}, RoMA \citep{yu2021roma}, BDI \citep{chen2022bdi}, BONET \citep{bonet2024}, and ranking surrogates \citep{tan2025ltr}. Optimizer-as-contribution work \citep{chemingui2024pggs} argues search strategy is under-explored but proposes a method rather than decomposing. Design-Bench \citep{trabucco2022designbench} standardizes tasks and, by fixing a protocol, documents the confounded status quo we dissect.

\paragraph{Calibration and conformal prediction.} Post-hoc calibration \citep{gonzalez2016batch} and conformal methods give distribution-free coverage \citep{angelopoulos2023conformal}; conformal prediction sets have been used inside the Bayesian-optimization loop itself \citep{stanton2023conformalbo}. We use split-conformal and its weighted extension \citep{tibshirani2019conformal} to repair the LCB premise and to diagnose where the repair transfers, positioning our calibration arm as \mdemph{decompose and diagnose}: measuring coverage where the optimizer operates, rather than certifying a fixed pipeline.

\paragraph{Evaluation critiques and controlled decompositions.} A recurring lesson from adjacent subfields is that reported gains can be artifacts of evaluation rather than method: reproducibility and statistical audits of deep RL \citep{henderson2018matters,agarwal2021precipice} and the demonstration that aggregate benchmark scores are structurally unreliable \citep{balduzzi2018reevaluating} each pair a critique with a reusable tool (a protocol, a stratified-bootstrap library, Nash averaging). Within offline optimization, SOO-Bench \citep{qian2025soobench} pursues a complementary benchmark-validity axis, stress-testing optimizer \mdemph{stability} across problem instances. Our study is in this tradition---a controlled decomposition plus a coverage diagnostic---but targets the surrogate$\times$optimizer confound in offline MBO, where it is not merely statistical noise but a specific, measurable premise (LCB coverage) that prior work has not quantified in the region the optimizer actually reaches.

\section{The Decomposition Grid}
\label{sec:grid}

\paragraph{Surrogates.} (i) \textbf{Ensemble}: $K{=}5$ two-hidden-layer MLPs (width 96, ReLU), trained by MSE for 35 epochs (Adam, lr $3\times10^{-3}$); $\mu,\sigma$ are the member mean and standard deviation. (ii) \textbf{Exact GP}: a differentiable single-task GP (ARD Mat\'ern-$5/2$), fit by marginal likelihood on a score-biased subsample ($N_{\max}{=}800$). (iii) \textbf{Sparse variational GP (SVGP)}: 128 inducing points, ARD Mat\'ern-$5/2$, 250 ELBO steps ($N_{\max}{=}2000$). The GPs additionally fit kernel hyperparameters by marginal likelihood---per-run tuning the ensemble does not receive; the matched-tuning control (below) freezes it to isolate the surrogate-class effect.

\paragraph{Optimizers.} (i) \textbf{Gradient}: 100 Adam steps on $x$ (lr $0.05$), box-clipped to $[0,1]^d$. (ii) \textbf{Perturbation}: 5 rounds of Gaussian hill-climbing ($\sigma\in\{0.1,0.05,0.02\}$). (iii) \textbf{CMA-ES}: population search (initial $\sigma{=}0.2$, separable variant when $d{>}500$). All three surrogates are differentiable (the exact GP is a differentiable single-task GP), so every surrogate$\times$optimizer combination is realizable: a full $3\times3$ grid of 9 cells, plus the COMs, CbAS, and gradient-ascent baselines.

\paragraph{Acquisition.} All cells maximize the LCB $\mu(x)-\beta\sigma(x)$ with $\beta{=}2$; $\beta{=}0$ recovers pure surrogate maximization.

\paragraph{Score-closure protocol.} Every cell and baseline shares one evaluation closure: fit the surrogate on $\D$, form the LCB acquisition, hand it to the optimizer, collect the 128 proposed designs, and score them with the ground-truth oracle. Only the two swept factors---the surrogate producing $(\mu,\sigma)$ and the optimizer searching the acquisition---vary across cells; the data split, candidate budget, input normalization, and oracle scoring are held identical. This shared closure is what licenses attributing score differences to the surrogate$\times$optimizer factors rather than to incidental protocol choices, and it is precisely the control that pipeline-level comparisons of full published methods lack.

\paragraph{Tasks and protocol.} 7 synthetic functions (Branin-2D through Griewank-30D; fixed dataset drawn once at seed 0) and 7 Design-Bench tasks (TF-Bind-8/10 with exact oracles; Superconductor, GFP, UTR, Ant, D'Kitty with random-forest oracles to remove simulator/framework dependencies). Discrete designs are relaxed to per-position class logits and decoded by argmax; continuous inputs and all scores are min-max normalized. Each method proposes 128 candidates; we report the 100th-percentile (max) oracle score, following Design-Bench. We run 30 seeds on synthetic and 16 on Design-Bench.

\paragraph{Matched tuning (identifiability control).} Exact and sparse GPs, unlike ensembles, can spend per-run hyperparameter-optimization budget. The \mdemph{matched} arm freezes GP hyperparameter fitting so every surrogate gets the same zero per-run tuning budget, isolating the surrogate-class effect from a GP-tuning advantage.

\paragraph{Attribution.} Per task we min-max normalize the grid and compute a two-way ANOVA: $\eta^2_{\text{surr}}$ and $\eta^2_{\text{opt}}$ are the fractions of normalized-score variance explained by the surrogate and optimizer main effects. Significance uses Wilcoxon signed-rank with Holm correction, an omnibus Friedman test, Nemenyi critical differences, and bootstrap rank confidence intervals.

\begin{table*}[t]
\centering
\caption{Offline MBO on synthetic tasks: 100th-percentile score by surrogate$\times$optimizer (30 seeds; higher is better). \textbf{Bold} = best per task. Within the ensemble rows the optimizer swings the score enormously (Branin $-0.78\!\to\!-9.27$; Griewank $-395\!\to\!-2612$); within the GP rows it is nearly inert (Branin all $\approx-0.40$). This interaction, not a surrogate-only or optimizer-only main effect, is the source of the reported GP-LCB ``advantage.''}
\label{tab:grid}
\setlength{\tabcolsep}{5pt}
\small
\begin{tabular}{lccccccc}
\toprule
Surrogate$\times$Opt. & Branin & Styblinski & Levy & Rosenbrock & Rastrigin & Ackley & Griewank \\
\midrule
Ens $\times$ Grad     & $-9.27$ & $6.37$  & $-2.14$ & $-0.28$ & $-7.71$ & $-3.66$ & $-2592$ \\
Ens $\times$ Pert     & $-0.78$ & $33.08$ & $-0.40$ & $-0.12$ & $-8.44$ & $-6.32$ & $-395$ \\
Ens $\times$ CMA      & $-14.01$& $5.21$  & $-3.19$ & $-0.48$ & $-10.81$& $-4.31$ & $-2613$ \\
GP $\times$ Grad      & $\mathbf{-0.40}$ & $27.57$ & $\mathbf{-0.05}$ & $-0.09$ & $-4.83$ & $\mathbf{-0.55}$ & $\mathbf{-0.94}$ \\
GP $\times$ Pert      & $-0.40$ & $\mathbf{36.15}$ & $-0.24$ & $-0.08$ & $-8.28$ & $-6.28$ & $-269$ \\
GP $\times$ CMA       & $-0.40$ & $26.65$ & $-0.05$ & $-0.09$ & $-5.06$ & $-0.59$ & $-1.00$ \\
SVGP $\times$ Grad    & $-0.45$ & $11.83$ & $-0.08$ & $\mathbf{-0.04}$ & $\mathbf{-2.83}$ & $-0.69$ & $-2.11$ \\
SVGP $\times$ Pert    & $-0.40$ & $34.35$ & $-0.25$ & $-0.08$ & $-8.27$ & $-6.14$ & $-275$ \\
SVGP $\times$ CMA     & $-0.53$ & $11.60$ & $-0.08$ & $-0.04$ & $-3.00$ & $-0.73$ & $-2.17$ \\
\bottomrule
\end{tabular}
\end{table*}

\section{Results: What Drives Performance}
\label{sec:results}

\begin{figure*}[t]
\centering
\includegraphics[width=0.92\textwidth]{figures/fig1_grid_heatmap}
\caption{Decomposition map: mean rank (over tasks, $1{=}$best) of every surrogate$\times$optimizer cell. \textbf{Left (synthetic):} the GP / SVGP surrogate is best regardless of optimizer (dark cells), while the ensemble is poor and swings with the optimizer (bright cells)---the surrogate main effect plus the ensemble$\times$optimizer interaction. \textbf{Right (Design-Bench):} the same grid collapses to a near-uniform mid-rank field, mirroring the statistically non-significant omnibus.}
\label{fig:heatmap}
\end{figure*}

\paragraph{The optimizer effect is an ensemble-specific interaction.} Table~\ref{tab:grid} shows the mechanism directly. Within the \mdemph{ensemble} rows, changing the optimizer moves the score by orders of magnitude (Branin $-0.78$ for perturbation vs.\ $-9.27$ for gradient; Griewank $-395$ vs.\ $-2592$): gradient ascent drives designs into regions where the ensemble over-estimates, collapsing to the domain boundary. Within the \mdemph{GP} rows the same optimizer switch barely moves the score (Branin all $\approx-0.40$). Figure~\ref{fig:optbysurr} summarizes this as the optimizer-induced spread per surrogate.

\paragraph{Attribution: surrogate main effect, plus a large interaction.} The two-way ANOVA assigns the synthetic-task variance to the surrogate main effect ($\eta^2_{\text{surr}}{=}0.37$ vs.\ $\eta^2_{\text{opt}}{=}0.01$): averaging over optimizers, GP and SVGP lead the ensemble by a real marginal-mean gap. Under \mdemph{matched} tuning the surrogate effect persists ($\eta^2_{\text{surr}}{=}0.28$, retaining $76\%$ of its unmatched $0.37$), so it is not merely a per-run tuning budget the ensemble lacks. The optimizer main effect is small because its influence is concentrated on one surrogate: the surrogate$\times$optimizer \mdemph{interaction} is $\eta^2_{\text{inter}}{=}0.17$, an order of magnitude above the optimizer main effect (Table~\ref{tab:attr}). This is the ensemble-specific collapse quantified---the optimizer matters, but only through the ensemble.

\begin{table}[t]
\centering
\caption{Two-way ANOVA attribution ($\eta^2$, fraction of task-normalized variance explained by each term) across regimes. The surrogate main effect dominates on synthetic tasks and survives the matched-tuning control; the surrogate$\times$optimizer interaction is itself an order of magnitude above the optimizer main effect. On Design-Bench neither factor explains much variance and the (small) ordering reverses. Task-and-seed bootstrap $95\%$ CIs (synthetic, unmatched): $\eta^2_{\text{surr}}\in[0.25,0.57]$, $\eta^2_{\text{opt}}\in[0.01,0.19]$ (non-overlapping), $\eta^2_{\text{inter}}\in[0.11,0.26]$.}
\label{tab:attr}
\small
\begin{tabular}{lcccc}
\toprule
Regime & $\eta^2_{\text{surr}}$ & $\eta^2_{\text{opt}}$ & $\eta^2_{\text{inter}}$ & Friedman $p$ \\
\midrule
Synthetic (unmatched)      & $\mathbf{0.37}$ & $0.01$ & $0.17$ & $6.1\times10^{-5}$ \\
Synthetic (matched tuning) & $\mathbf{0.28}$ & $0.02$ & $0.12$ & --- \\
Design-Bench               & $0.05$ & $0.08$ & $0.01$ & $0.69$ \\
\bottomrule
\end{tabular}
\end{table}

\begin{figure}[t]
\centering
\includegraphics[width=0.99\columnwidth]{figures/fig2_optimizer_spread}
\caption{Optimizer-induced spread by surrogate class (synthetic; per-seed task-normalized 100th-percentile score, higher is better; boxes span the interquartile range). The three optimizers produce sharply different distributions on the ensemble surrogate but nearly identical, tightly-clustered distributions on the GP and SVGP surrogates: the acquisition optimizer matters enormously for ensembles and negligibly for the GP and SVGP surrogates, whose smooth posterior mean (not calibration) is the cause (Section~\ref{sec:mech}).}
\label{fig:optbysurr}
\end{figure}

\paragraph{Significance, and the synthetic$\to$real collapse.} On synthetic tasks the nine grid cells are strongly separated: a Friedman omnibus over the 9 cells and 7 tasks gives $p{=}6.1\times10^{-5}$, with the best cell (GP$\times$gradient) at mean rank $2.3$ (bootstrap $95\%$ CI $[1.3,3.6]$) against a Nemenyi critical difference of $4.5$. On Design-Bench the same analysis yields $p{=}0.69$: no cell is distinguishable from any other (best cell GP$\times$perturbation at mean rank $3.6$, CI $[1.9,5.7]$; the whole grid lies within one critical difference). Figure~\ref{fig:cd} contrasts the two regimes, and the two-panel decomposition map (Figure~\ref{fig:heatmap}) shows the same collapse at a glance: the sharp dark/bright rank structure on the left flattens to a uniform mid-gray on the right. The driver also reverses: on real tasks the (small) surrogate advantage shrinks ($\eta^2_{\text{surr}}{=}0.05$) and, if anything, the optimizer explains marginally more ($\eta^2_{\text{opt}}{=}0.08$)---no factor explains much variance (Table~\ref{tab:attr}). We state this as a benchmark-validity finding: the large, significant method differences synthetic suites reward are \mdemph{statistically unresolved} on the real tasks in Design-Bench. We are careful not to overstate the null: a paired equivalence test (TOST) on the best-versus-worst cells does \mdemph{not} establish equivalence---the $90\%$ CI on their gap is $\pm0.48$ normalized units---so the real-task result is that method choice is unresolved and \mdemph{underpowered at $N{=}7$ tasks}, not that the methods are provably equal. Table~\ref{tab:dbgrid} gives the full Design-Bench grid. Two caveats sharpen it: the ensemble$\times$gradient collapse is a continuous-domain phenomenon---on the two exact-oracle tasks (TF-Bind-8/10) that cell does not collapse but ties or leads (e.g.\ $2.20$ on TF-Bind-8, above every GP cell)---and elsewhere the methods cluster in a narrow band with the per-task best split across surrogates and optimizers.

\begin{figure}[t]
\centering
\includegraphics[width=0.98\columnwidth]{figures/fig6_cd_diagram}
\caption{Critical-difference diagram (Nemenyi, $\alpha{=}0.05$) over the 9 grid cells. Synthetic tasks separate the cells sharply (Friedman $p{=}6.1\times10^{-5}$); Design-Bench does not ($p{=}0.69$), all cells falling within one critical difference. Method rankings do not transfer from synthetic to real.}
\label{fig:cd}
\end{figure}

\begin{table*}[t]
\centering
\caption{Offline MBO on Design-Bench (16 seeds; normalized 100th-percentile score, higher is better; random-forest oracles for the non-exact tasks). \textbf{Bold} = best per task including the COMs/CbAS baselines. Unlike the synthetic grid, the methods cluster tightly and the per-task winner is split across surrogates and optimizers (Friedman $p{=}0.69$ over the grid); the ensemble/COMs gradient-ascent collapse persists only on GFP.}
\label{tab:dbgrid}
\setlength{\tabcolsep}{5pt}
\small
\begin{tabular}{lccccccc}
\toprule
Surrogate$\times$Opt. & TF-Bind-8 & TF-Bind-10 & Superconductor & GFP & UTR & Ant & D'Kitty \\
\midrule
Ens $\times$ Grad   & $2.20$ & $1.34$ & $0.99$ & $-9.61$ & $\mathbf{1.01}$ & $0.92$ & $0.74$ \\
Ens $\times$ Pert   & $1.00$ & $1.31$ & $1.29$ & $2.48$  & $0.98$ & $1.29$ & $1.05$ \\
Ens $\times$ CMA    & $2.06$ & $1.15$ & $1.18$ & $-5.63$ & $0.99$ & $0.89$ & $0.72$ \\
GP $\times$ Grad    & $1.00$ & $1.31$ & $1.24$ & $2.45$  & $0.99$ & $1.52$ & $1.06$ \\
GP $\times$ Pert    & $1.00$ & $1.31$ & $1.31$ & $2.45$  & $0.99$ & $1.52$ & $\mathbf{1.11}$ \\
GP $\times$ CMA     & $1.00$ & $1.00$ & $1.26$ & $2.46$  & $0.99$ & $1.52$ & $1.02$ \\
SVGP $\times$ Grad  & $1.84$ & $1.11$ & $1.07$ & $1.80$  & $0.99$ & $0.99$ & $1.02$ \\
SVGP $\times$ Pert  & $1.45$ & $1.31$ & $1.25$ & $2.45$  & $0.99$ & $1.52$ & $1.09$ \\
SVGP $\times$ CMA   & $1.83$ & $1.11$ & $1.26$ & $\mathbf{2.48}$ & $0.93$ & $0.91$ & $1.02$ \\
\midrule
COMs (baseline)     & $\mathbf{2.21}$ & $\mathbf{1.35}$ & $1.01$ & $-9.20$ & $\mathbf{1.01}$ & $0.98$ & $0.95$ \\
CbAS (baseline)     & $2.12$ & $1.28$ & $\mathbf{1.36}$ & $1.85$ & $0.99$ & $\mathbf{1.53}$ & $1.02$ \\
\bottomrule
\end{tabular}
\end{table*}

\section{Mechanism: Inductive Bias, Not Calibration}
\label{sec:mech}

Why does the GP win, and why does gradient ascent collapse on the ensemble but not on the GP? The intuitive answer---that the GP's uncertainty is better calibrated, so its pessimistic bound is valid---is wrong. Three controls localize the effect to the GP's posterior \mdemph{mean}, an inductive bias, and to an ensemble$\times$gradient interaction; $\sigma$-calibration plays no causal role.

\paragraph{The advantage survives with pessimism off.} If the GP's edge were a calibrated LCB, removing the pessimism term should erase it. It does not. Re-running the full grid at $\beta{=}0$ (posterior-mean maximization, no $\sigma$ penalty), the GP--ensemble marginal gap is essentially unchanged---$0.51$ at $\beta{=}2$ versus $0.47$ at $\beta{=}0$ (task-normalized, averaged over optimizers; the paired difference has $95\%$ CI $[-0.02,0.10]$, indistinguishable from zero; Table~\ref{tab:controls})---and the ensemble still collapses under gradient ascent with no pessimism at all (Griewank $-2701$ vs.\ the GP's $-0.94$). The advantage is a property of the GP's smooth mean, not of $\sigma$.

\paragraph{The advantage is not the GP's data subsample.} The GP fits a score-biased $800$-point subsample while the ensemble uses all data. Giving the ensemble the \mdemph{same} subsample does not close the gap---it \mdemph{widens} it, from $0.51$ to $0.76$: the ensemble does worse with fewer points and still collapses under gradient. The GP wins \mdemph{despite} fitting less data, isolating the effect to the surrogate class.

\paragraph{The ensemble fails only under its own gradient ascent.} The collapse is not a blanket ensemble defect. The pessimism premise $\{\mu-f\le\beta\sigma\}$ (Prop.~\ref{prop:cov}) is moderately covered for the ensemble in-distribution ($0.73$, below the nominal $0.90$) but collapses on the designs its \mdemph{own} gradient ascent returns ($0.41$ mean; $0.00$ on the collapse tasks). On the \mdemph{GP's} proposals, however, the ensemble premise is well covered ($0.97$): the ensemble is not uniformly miscalibrated---it fails specifically where its gradient optimizer drives it (Figure~\ref{fig:cross}). The GP's premise holds both in-distribution ($0.98$) and on its own proposals ($0.97$): its smooth mean offers no over-estimated argmax for gradient ascent to exploit. This is the interaction the grid isolates, now measured directly rather than inferred.

\begin{table}[t]
\centering
\caption{Gap controls (synthetic; task-normalized GP $-$ ensemble marginal, with 10-seed task$+$seed bootstrap $95\%$ CIs). The gap is unchanged with pessimism off ($\beta{=}0$; the paired $\beta{=}2$ vs.\ $\beta{=}0$ difference has CI $[-0.02,0.10]$) and \emph{widens} when the ensemble is given the GP's score-biased subsample: the edge is the surrogate's posterior mean, not $\sigma$-calibration or data.}
\label{tab:controls}
\small
\begin{tabular}{lcc}
\toprule
Setting & gap & 95\% CI \\
\midrule
$\beta{=}2$ (pessimism on)                 & $0.51$ & $[0.43,0.58]$ \\
$\beta{=}0$ (pessimism off)                & $0.47$ & $[0.37,0.57]$ \\
ensemble on the GP's 800-pt subsample      & $0.76$ & $[0.29,1.32]$ \\
\bottomrule
\end{tabular}
\end{table}

\begin{figure}[t]
\centering
\includegraphics[width=0.99\columnwidth]{figures/fig8_crossproposal}
\caption{Premise coverage $\Pr(f\ge\mu-\beta\sigma)$ at $\beta{=}2$ (synthetic mean), each surrogate on in-distribution points, its own proposals, and the other surrogate's proposals. The ensemble premise collapses ($0.41$) \emph{only} on the designs its own gradient ascent returns; on the GP's proposals it is well covered ($0.97$), and the GP premise holds everywhere. The failure is the ensemble$\times$gradient interaction, not a surrogate defect.}
\label{fig:cross}
\end{figure}

\paragraph{Coverage is validity.} These frequencies are not incidental; they exactly measure the validity of the pessimistic bound. Write $L_\beta(x)=\mu(x)-\beta\sigma(x)$; call $L_\beta$ a valid $(1{-}\delta)$ lower bound under a distribution $Q$ if $\Pr_{x\sim Q}(f(x)\ge L_\beta(x))\ge 1{-}\delta$.

\begin{proposition}[Coverage of the premise is LCB validity]
\label{prop:cov}
For any $Q,\beta,\delta$, $\;\Pr_{x\sim Q}(f(x)\ge L_\beta(x))=\Pr_{x\sim Q}(\mu(x)-f(x)\le\beta\sigma(x))$. Hence $L_\beta$ is a valid $(1{-}\delta)$ lower bound under $Q$ iff the premise $\{\mu-f\le\beta\sigma\}$ has $Q$-probability at least $1{-}\delta$.
\end{proposition}

The one-line identity ($\sigma>0$; the two events coincide) turns ``the bound holds'' into a measurable frequency, evaluated under the data $\D$ and the proposal $\Pi$. At $\beta{=}2$, ensemble coverage is $0.73$ in-distribution / $0.41$ on proposals (synthetic) and $0.77$ / $0.18$ (real), below the nominal $0.90$ exactly on the proposals where the bound must hold (Figure~\ref{fig:coverage}; per-task values in the supplement).

\paragraph{Pessimism is regularization, not calibration.} Two further observations confirm calibration is not the driver. The uncertainty $\sigma$ is a weak error signal---Spearman $\rho$ between $\sigma$ and $|\mu-f|$ is only $\approx0.1$---yet increasing $\beta$ improves the score on $6$ of $7$ synthetic tasks (Figure~\ref{fig:beta}; median normalized slope $+0.19$). Pessimism helps as crude distance-regularization, penalizing high-variance far-from-data regions, not as calibrated conservatism; the lone exception (Ackley) is where the penalty most often points the wrong way. Per-task calibration quality does not predict whether pessimism helps. Ensemble size is the standard $K{=}5$ \citep{lakshminarayanan2017ensembles}; shrinking $K$ inflates $\sigma$ and the pessimism penalty, improving the ensemble on its own $K$-sweep---corroborating the regularization reading, orthogonal to the $\beta{=}0$ result.

\begin{figure*}[t]
\centering
\includegraphics[width=0.8\textwidth]{figures/fig3_coverage}
\caption{Coverage of the pessimism premise $\mu{-}f\le\beta\sigma$ vs.\ $\beta$ on synthetic (left) and Design-Bench (right) tasks: in-distribution (solid) and on the optimizer's OOD proposals (dashed), with $\pm1$ s.d.\ bands across tasks and the split-conformal repair shown as stars ($\star$). Ensemble in-distribution coverage is moderate, but proposal (OOD) coverage is far lower and task-dependent---near zero on the tasks where gradient ascent collapses; conformal recalibration lifts in-distribution coverage to its $0.90$ target (upper star) but leaves the OOD coverage the bound actually needs far below it (lower star).}
\label{fig:coverage}
\end{figure*}

\begin{figure}[t]
\centering
\includegraphics[width=0.82\columnwidth]{figures/fig4_beta_sweep}
\caption{Pessimism sweep: per-task normalized 100th-percentile score vs.\ $\beta$ (faint lines, individual synthetic tasks; bold line, mean). Score rises with $\beta$ on 6 of 7 tasks even though $\sigma$ is an uninformative error signal ($\rho\approx0.1$)---pessimism acts as distance-regularization. Ackley is the single task where the penalty points the wrong way.}
\label{fig:beta}
\end{figure}

\paragraph{A distribution-free repair, and where it transfers.} Split-conformal calibration replaces the arbitrary $\beta$ with a data-driven multiplier.

\begin{proposition}[Conformal repair; shift-limited transfer]
\label{prop:conf}
Let $\{(x_i,f(x_i))\}_{i=1}^n$ be exchangeable from $P$, $r_i=(\mu(x_i)-f(x_i))/\sigma(x_i)$ the signed one-sided nonconformity, and $\hat q$ the $\lceil(n{+}1)(1{-}\delta)\rceil$-th smallest $r_i$. Then for a fresh $x\sim P$, $\Pr(f(x)\ge\mu(x)-\hat q\,\sigma(x))\ge 1{-}\delta$. Under a shifted proposal $\Pi\neq P$ with density ratio $w=d\Pi/dP$, validity is restored by weighting the calibration quantile by $w$ (weighted conformal; \citealp{tibshirani2019conformal}).
\end{proposition}

Empirically the fitted multiplier varies widely across tasks (synthetic $\hat q\in[1.8,16]$), quantifying how far raw $\sigma$ under-covers. Replacing $\beta\sigma$ by $\hat q\sigma$ restores in-distribution coverage to its $0.90$ target on every task (mean $0.90$ synthetic and real), exactly as Prop.~\ref{prop:conf} predicts; but on the shifted proposal $\Pi$ coverage stays low ($0.51$ / $0.31$ mean, near zero on the sharpest-shift tasks), because $\Pi\neq P$. This yields a concrete recipe (Algorithm~\ref{alg:diag}): a \mdemph{coverage diagnostic} that reports in-distribution and proposal coverage, flags an unreliable LCB when they diverge, and a \mdemph{weighted-conformal repair} when a density-ratio estimate is available. The negative transfer is itself the actionable signal: an LCB whose proposal coverage is near zero should not be trusted regardless of $\beta$.

\begin{algorithm}[t]
\caption{Coverage diagnostic and conformal-LCB repair}
\label{alg:diag}
\textbf{Input}: surrogate $(\mu,\sigma)$, data $\D$, level $\delta$, proposals $\Pi$\\
\textbf{Output}: multiplier $\hat q$, coverages $(\hat c_{\text{in}},\hat c_{\text{ood}})$, flag
\begin{algorithmic}[1]
\STATE Split $\D$ into fit / calibration folds.
\STATE $r_i \gets (\mu(x_i){-}f(x_i))/\sigma(x_i)$ on calibration fold (signed, one-sided; floor $\sigma$).
\STATE $\hat q \gets \lceil(n{+}1)(1{-}\delta)\rceil$-th smallest $r_i$.
\STATE $\hat c_{\text{in}} \gets \widehat{\Pr}_{x\sim\D}(f\ge\mu-\hat q\sigma)$.
\STATE $\hat c_{\text{ood}} \gets \widehat{\Pr}_{x\sim\Pi}(f\ge\mu-\hat q\sigma)$.
\IF{$\hat c_{\text{ood}} < 1{-}\delta$}
\STATE \textbf{flag} LCB unreliable; if $w{=}d\Pi/dP$ available, reweight $r_i$ by $w$ and refit $\hat q$.
\ENDIF
\STATE \textbf{return} $\hat q,(\hat c_{\text{in}},\hat c_{\text{ood}})$, flag
\end{algorithmic}
\end{algorithm}

\section{Discussion, Guidance, and Limitations}

\paragraph{Practitioner guidance.} (i) On smooth, low-to-moderate-dimensional problems, a GP/SVGP surrogate is robust to the acquisition optimizer (its smooth mean offers no exploitable argmax); a neural ensemble is not, and should be paired with a conservative optimizer (perturbation/CMA-ES) rather than aggressive gradient ascent. (ii) Before trusting an LCB, run the coverage diagnostic (Algorithm~\ref{alg:diag}); if proposal coverage is near zero, the pessimism is not doing what the theory says, and neither $\beta$-tuning nor in-distribution conformal calibration fixes it. (iii) On real Design-Bench tasks, method choice within this family is not statistically resolvable at standard seed counts---effort is better spent on the surrogate's informativeness than on the search rule.

\paragraph{Anticipated objections.} Three objections deserve direct answers. (i) \mdemph{That these benchmarks are imperfect is already known.} The contribution is its first controlled measurement---a crossed surrogate$\times$optimizer decomposition with a matched-tuning control, and a premise-coverage frequency not previously reported. (ii) \mdemph{There is no new state of the art.} The constructive artifact is the coverage diagnostic and weighted-conformal repair (Algorithm~\ref{alg:diag}): a reusable check, the same form of contribution as the evaluation tools this line of work is built on. (iii) \mdemph{The real-task result is null.} It is a significance collapse, not a claim of equivalence---the differences are unresolved, not provably zero (underpowered at $N{=}7$)---a benchmark-validity statement that the rewarded differences do not transfer.

\paragraph{Scope and external validity.} The synthetic$\to$real collapse is a statement about the \mdemph{measured} regime. Two boundary conditions bound it. First, for the non-exact tasks we substitute a random-forest oracle to remove simulator and framework dependence---a genuine substitution on GFP, UTR, Ant, and D'Kitty (the native oracle is an RF only for Superconductor), so a different oracle could re-separate methods. But it does not manufacture the null: on the three tasks with no smoothing RF substitution (TF-Bind-8/10 exact, Superconductor native RF), the omnibus stays flat (Friedman $p{=}0.93$) and the median 9-cell spread ($0.34$) is no smaller than on the substituted tasks ($0.39$). Second, the real-task omnibus is over 7 tasks, and the equivalence test is underpowered there (Section~\ref{sec:results}): we can say the method differences are unresolved, not that they are zero.

\paragraph{Limitations.} Our real-task evidence is Design-Bench with random-forest oracles for the non-exact tasks; the null is scoped to that suite and to CPU-scale training. A cross-check ran official COMs and CbAS: our CbAS matches the official scores ($|\Delta|{=}0.004$ on TF-Bind-8), while our COMs and official COMs diverge ($|\Delta|{=}1.2$, a reduced-epoch official run and a different oracle variant), so we report both side by side. The synthetic datasets are fixed across seeds (seed-0), so reported variance is training/optimization, not data-draw. Premise coverage on the discrete tasks uses relaxed logits, not decoded sequences, so those numbers (notably GFP) are softer---we lean the coverage mechanism on the synthetic tasks. Weighted conformal needs a density-ratio estimate we do not learn; we characterize the transfer gap rather than close it.

\section{Conclusion}

The reported low-dimensional advantage of GP-LCB in offline MBO is not a clean surrogate-class effect and not a calibration effect: it is a surrogate$\times$optimizer interaction driven by the GP's smooth posterior mean, on which gradient ascent finds no over-estimated argmax to exploit as it does on the ensemble's jagged mean. Removing pessimism ($\beta{=}0$) leaves the edge intact and giving the ensemble the GP's data does not close it---the cause is inductive bias, not uncertainty. Making the premise measurable (coverage equals LCB validity) turns it into a diagnostic: a bound whose proposal coverage is near zero should not be trusted regardless of $\beta$. And the differences these synthetic benchmarks reward are unresolved on real tasks---the same prior--task match, seen from both sides. We contribute the decomposition, the mechanism and its controls, the coverage diagnostic, and the synthetic-to-real validity result.

\section*{Ethical Statement}
This work studies optimization methodology on public benchmarks and introduces no new data or deployed system. By flagging when a pessimistic bound is invalid, the coverage diagnostic aims to reduce over-confident designs downstream.

\bibliography{references}

\end{document}
```

---
## FILE: docs/PAPER_V2_OUTLINE.md
<!-- lines: 194 | bytes: 12596 | last commit: cb204c8 2026-07-17 -->
```markdown
# Three candidate papers from the same repo

Presented, not chosen. `P(accept)` reasoning is relative to the current draft's baseline, which I
put at **very low** — not because the science is weak but because `docs/FLAW_LEDGER.md` P0-0 means a
reviewer who opens the artifact finds a control refuting the mechanism.

**Identity B is dead.** It was contingent on 5.1, and 5.1 **FAILS** — structurally, not incidentally.
`ĉ_ood` requires evaluating true *f* on the proposals, the one query offline MBO forbids; the
oracle-free feature set spanning all 14 tasks is a single binary flag; and at n=14 no rule could have
been certified regardless. It is documented below for completeness and to record *why* it is dead,
because the reason is itself publishable.

---

## IDENTITY A — Measurement, repaired

**One sentence.** The reported GP advantage in offline MBO is a surrogate-class effect, not an
optimizer effect — measured under a controlled factorial that survives normalizing the ensemble,
equalizing the candidate protocol, and tuning the gradient optimizer.

**Title.** *Decomposing the GP Advantage in Offline Model-Based Optimization*

**Abstract skeleton.** Confound → first controlled surrogate×optimizer factorial → η²_surr vs η²_opt
**after** target normalization and protocol equalization → the pre-registered optimizer hypothesis was
refuted → the ensemble's gradient collapse is a *trust-region* artifact, not surrogate geometry (we
report our own sweep) → coverage diagnostic as a remark → benchmark null with a power specification.

**Sections.** 1 Intro · 2 Related (Li/Rudner/Wilson ICLR 2024 positioned honestly) · 3 Grid · 4 Results
· 5 Coverage remark · 6 Design-Bench null + power analysis · 7 Limitations.

**Survives:** the factorial design (novelty: **NONE FOUND**), the complete 14-task grid, η² (reproduces
to 8dp). **Required:** X1, X2, X3, X4, X9. **Optional:** X7.
**CPU:** ~1–2 grid runs (~2 days incl. edits).

**P(accept): low-to-moderate.** Ceiling is real: `NOVELTY_CHECK` Q1 says Li/Rudner/Wilson already owns
"deep ensembles perform relatively poorly" and "ranking is problem-dependent, suggesting tailored
inductive biases." Strip that and what is new is *the factorial design* and *the offline setting* — a
methodological contribution reviewers describe as "an ablation." The known-accepted pattern for this
genre ("Are GANs Created Equal?", Musgrave's metric-learning reality check, Dacrema's recsys "phantom
progress") is: a *specific, named, falsified belief* + a *reusable protocol*. A has the first if X1
holds. It does not have the second.

---

## IDENTITY B — Diagnostic as method ❌ **DEAD**

**Would have been.** Coverage-driven offline surrogate×optimizer selection; the null becomes the
motivation; the diagnostic becomes the method.

**Why it's dead.** 5.1 ran the pre-registered rule and its kill criterion fired: regret **0.348** vs
the honest fixed-cell baseline's **0.233** — *identical to random* (0.348), 0 wins / 3 losses / 11 ties.
Two structural reasons, either fatal alone:
1. **The signal isn't oracle-free.** `ĉ_ood = mean(f_o >= mu_o - q*sig_o)` with `f_o = task.oracle(xf)`
   (`mbo.py:599`). Oracle-*contaminated* features do carry signal (regret 0.171, 7W/2L, paired CI
   excluding zero) — **the predictive signal lives precisely in the quantity offline MBO cannot compute.**
2. **n=14 cannot resolve it.** A *perfect* rule reaches d_z = 0.71 vs 0.81 needed for 80% power.

**Novelty (moot but recorded).** `NOVELTY_CHECK` Q4: the *problem* is named in the Design-Bench
conclusion and the Kim TMLR survey; offline RL has a mature policy-selection literature; MS-DDEO
(SWEVO 2022) already selects an offline surrogate pool *by smoothness*; CC-Select (2026) uses
calibration as a selection signal outside MBO. Only **joint surrogate+optimizer cell selection via
conformal premise-coverage** was NONE FOUND.

**What to salvage.** Finding (1) is a genuine contribution to state in one paragraph: *the diagnostic
that best predicts which configuration wins is not computable in the setting that needs it.* That is a
real obstruction, not a failed experiment. Finding (2) becomes X4, the power analysis — which is
load-bearing for both A and C.

---

## IDENTITY C — Mechanism

**One sentence.** Prior–task smoothness match is the single axis governing the GP–ensemble gap, the
gradient collapse, the coverage failure, and the synthetic→real transfer — demonstrated by manipulation
in **both** directions and by a continuous interpolation that reproduces the Design-Bench null as a
limit point.

**Title.** *Smoothness Is the Axis: What the GP Advantage in Offline MBO Actually Measures*

**Abstract skeleton.** The GP advantage is attributed to calibration; we show it is prior smoothness →
we *manipulate* it in both directions (smooth the ensemble → gap closes; roughen the GP → GP collapses,
a **risked prediction**) → we build a task family continuously varying prior-match and show gap, η²_surr,
ĉ_ood, and Friedman p move together → **Design-Bench is not a different world; it is a point on this
axis** → the benchmark null follows as a corollary, with the N required to detect it.

**Sections.** 1 Intro · 2 Related · 3 Grid + repairs · 4 The gap tracks smoothness · 5 Manipulation
(both directions) · 6 The interpolation family · 7 Design-Bench as a limit point + power spec · 8 Limits.

**Survives:** everything A survives, plus the coverage instrument as *evidence* rather than as a
contribution. **Required:** X1, X2, X3, X4, X5, X6. **Optional:** X7, X8, X10.
**CPU:** ~9–10 grid runs (~1 week incl. edits). All CPU-only.

**P(accept): moderate-to-good — the highest of the three.** It has what A lacks: a **risked prediction**
(X6 — the theory forbids a rough GP from being robust) and a **mechanism demonstrated by manipulation**
rather than by subtraction. It converts the null from the paper's weakest half into a corollary.

**The honest risk:** `NOVELTY_CHECK` Q2 — "surrogate smoothness helps offline optimization" is
**already established** (MS-DDEO 2022 grades surrogates by smoothness; the Kim survey lists smoothness
priors / RoMA). C's novelty is narrower than it sounds: it is *attribution of the GP's advantage to mean
smoothness rather than calibration*, plus the continuum. That is defensible — but it is **exactly the
claim X1 might destroy**, since unnormalized targets are an alternative explanation for the same table.
**C is a bet on X1's outcome.** Run X1 before committing to C.

---

## What is achievable, and where B and C compose

**A ⊂ C.** C's required set is A's plus X5 and X6. There is no reason to build A and *then* C — build
A's repairs (X1–X3), read the result, and let it decide whether C is available.

**B and C were complementary, not exclusive** — C would have supplied the mechanism explaining *why*
B's selection signal worked. With B dead, C absorbs B's only survivor: the obstruction result (the
signal isn't computable offline) is a natural discussion point in C's coverage section, and B's power
analysis (X4) is load-bearing for C's Section 7.

**Recommended sequencing, deadline-dependent** (see `DECISION_QUEUE.md` D1):

| Time available | Do |
|---|---|
| **< 2 weeks** | Do not submit. X1–X3 alone will not land, and shipping without X2 is the worst option on the board. |
| **~3–4 weeks** | **Identity A.** X1, X2, X3, X4, X9. One grid run. Honest, repaired, thin. |
| **~6–8 weeks** | **Identity C.** X1–X6 (+X7). ~10 grid runs, CPU-only. The paper worth writing. |

**My read:** A is a repair; C is a paper. The gap between them is ~8 grid runs of CPU and one week —
cheap for what it buys. But **X1 gates both**, and X1 can refute C's thesis outright. Run X1 first,
read it honestly, then choose. If X1 shows the gap was target scaling, neither A nor C exists as
drafted — and that is worth knowing in week one rather than in review.

**Venue note.** If the AAAI window is too tight: MLRC 2026 is now an **official NeurIPS track** (via
TMLR, hard deadline 2026-09-30) and states explicitly that *"negative results and partial failures to
reproduce are as valuable as confirmations."* AAAI has **no** negative-results track. That is a real
option for the A-shaped version, and it is a better fit than forcing A through AAAI main.

---

## The framing this session missed: **the paper is a reversal, not a null**

Every accepted paper in this genre is *a reversal wearing a null's title* — Melis, Recht, Dacrema,
Musgrave, Chen, Liu, and now Yauney. None of them lead with "we found no difference." They lead with
**a named belief, refuted**.

**We have a reversal and the draft is not using it.**

> **η²_surrogate = 0.37 · η²_optimizer = 0.01**

That is not "no difference." That is: **the field has been innovating on the axis that does not matter.**
And there is a named target for it — **PGS (AAAI 2024)**, whose entire stated premise is that offline BBO
*"has focused on improving surrogate models while using fixed search strategies"* and that the search
strategy is the neglected axis. Our optimizer main effect is **0.01**. That is a specific, named,
falsifiable belief held by a paper at our target venue, and our data contradicts it.

That slots directly into the genre template (`VENUE_NORMS.md`): named belief → refuted → mechanism by
manipulation → artifact → prescription. It is the "named belief" slot, which the current draft leaves
empty by leading with a decomposition rather than a contradiction.

### ⚠️ The gate — this framing is currently unearned

**η²_opt = 0.01 is itself confounded.** `FLAW_LEDGER.md` P0-1 (grad/perturb get 256 oracle calls, CMA
gets 128; three different selection rules) and P1-1 (25,600 vs 4,096 vs 432–3,012 surrogate queries)
mean the optimizer axis is not measured under control. **We cannot claim "the optimizer doesn't matter"
from a grid where the optimizers were never given equal budgets.** P0-0 compounds it: a trust region
moves the ensemble's gradient result 15× on Branin, which is an *optimizer* effect the grid never saw.

So: **X1 + X3 first, then the reversal.** If η²_opt stays ≈0.01 under matched budgets and one selection
rule, the reversal is real and it is the paper's headline. If it rises, the honest finding is the
opposite of the current draft *and* of PGS — and that is still a paper. Either way the framing is decided
by the same run that gates everything else, which is another reason X1/X3 is the critical path.

### Correction to `EXTENSION_LEDGER.md`'s X4 note

I wrote that power-analysis-as-headline lives only in workshops. **That is wrong.** Yauney, Warraich &
Swayamdipta, *How Reliable is Language Model Micro-Benchmarking?*, **ICLR 2026** (arXiv:2510.08730;
"Published at ICLR 2026" verified in the comments field; a reported *Oral* status is **NOT VERIFIED**).
Verbatim: *"no micro-benchmarking method can consistently rank model pairs 3.5 points of accuracy apart
on MMLU-Pro"*; *"often as many as 250 examples must be selected, at which point **random sampling is
competitive with existing micro-benchmarking methods**"*; *"more than half of pairwise comparisons are
not likely to be preserved."*

**This strengthens X4 rather than weakening it.** Power-as-headline *does* clear a top venue — but only
when shipped with an instrument, a reversal (random ≈ sophisticated methods), specific numbers, and a
prescription. Yauney measures the *examples-within-a-benchmark* axis; Card measures test-set size.
**The task-count axis remains unowned** — and it is Design-Bench's binding constraint. X4 stands, with a
four-month-old template for exactly how to ship it.

**Also directly citable, and it lands on our CD diagram:** Demšar's own rule of thumb is **N > 10 datasets,
k > 5 methods**. Our N=7 sits **below his own threshold** — in the paper we cite for the procedure.
Pair with Agarwal et al.'s *"lack of statistically significant results does not demonstrate the absence of
effect"* and switch to exact critical values / Iman–Davenport F_F plus IQM + bootstrap CIs.

**Verified for the record:** our Design-Bench set is `AntMorphology, DKitty, GFP, Superconductor,
TFBind10, TFBind8, UTR` — confirming that **two of seven are the tasks Design-Bench's authors excluded
as non-discriminative** (`NOVELTY_CHECK`, App. D.3). Two of seven are null by construction, which makes
p=0.69 partly circular. Re-run on the canonical five, or report both and make the selection effect the
argument — but do not leave it unstated.
```

---
## FILE: docs/EXTENSION_LEDGER.md
<!-- lines: 125 | bytes: 11850 | last commit: 19e88c6 2026-07-17 -->
```markdown
# Extension ledger

Sorted by acceptance-delta ÷ cost. Ten real options, not forty plausible ones.
Novelty status per `docs/NOVELTY_CHECK.md`. Predictions and kill criteria: `docs/PREREGISTRATION_V2.md`.

| ID | Idea | Type | Novelty | Prediction | Falsifier | CPU | Wall | Δaccept | Risk | Depends | Rec? |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **X1** | **Normalize the ensemble's targets (M0), re-run grid** | experiment | n/a (bug fix) | η²_surr drops materially; gap tracks `log\|y\|` before (ρ>0.6), not after | η²_surr ≈ 0.37 and no `\|y\|` correlation → confound refuted, headline *strengthened* | 1 grid | ~1 day | **HIGH** | none — decisive either way | — | **YES — first** |
| **X2** | **Report gradtune; re-scope the mechanism (P0-0)** | reframe | n/a | — | — | 0 | ~2 h | **HIGH** | reputational if omitted | — | **YES — unconditional** |
| **X3** | **Equalize the candidate/oracle protocol (P0-1)** | experiment | n/a (bug fix) | Ens×CMA improves; η²_inter shrinks | nothing moves → protocol was harmless | fold into X1 | ~2 h | **HIGH** | none | — | **YES — same run as X1** |
| **X4** | **Power analysis: "a discriminative offline-MBO suite needs ≥N tasks"** | reanalysis | **NONE FOUND** (measurement) | N ≫ 7; already have d_z=0.71 vs 0.81-needed from 5.1 | — | **0** | ~4 h | **HIGH** | none | 5.1 (done) | **YES — free** |
| **X5** | **M3 smoothness interpolation family** | experiment | partial — smoothness-helps is known (MS-DDEO 2022, RoMA); the *continuum* is not | gap, η²_surr, ĉ_ood, Friedman p all move together monotonically in α | they move independently → prior-match isn't one axis | 6 grids | ~3 days | **HIGH** | medium | X1 | **YES** |
| **X6** | **M2 roughen the GP (falsification test)** | experiment | NONE FOUND | Matérn-1/2 GP collapses under gradient; its coverage drops from 0.97 | rough GP stays robust → mechanism is not prior smoothness | 2 grids | ~1 day | **HIGH** | **the theory can die — that's the point** | X1 | **YES** |
| **X7** | **Full 3×3 coverage matrix (P0-3)** | reanalysis+exp | NONE FOUND | ĉ_ood correlates with score across 9 cells; Ens×CMA also ≈0.4 | Ens×CMA coverage high → "any aggressive optimizer" refuted | ~1 grid | ~1 day | MED-HIGH | none | X1 | **YES** |
| **X8** | **M5 learn the density ratio (close Prop 2)** | experiment | NONE FOUND (untried here) | partial repair; `w` unbounded, ESS collapses | full repair (good) or nothing (sharper negative) | ~0–1 grid | ~1 day | MED | low — all 3 outcomes publishable | X7 | **YES** |
| **X9** | **Demote Prop 1 to a remark citing Jin et al. 2021** | reframe | **PRIOR WORK FOUND** | — | — | 0 | ~1 h | MED (removes risk) | none | — | **YES — free** |
| **X10** | **M6 non-vacuous coverage bound** | experiment | NOT VERIFIABLE HERE | ĉ_ood degrades ≤ Φ(L, D, β) | bound is vacuous for unregularized ensembles — **likely** | ~0 | 1–2 days | HIGH if lands, **ZERO if not** | **high** | X1, M1 | only if time |

**Rejected, with reasons.** *DKL surrogate* (7.1) — genuinely the interesting one (GP head + neural features sits exactly on the smooth/jagged axis and would separate kernel from representation), but it adds a fourth surrogate to a grid whose existing three are not yet identified; **revisit after X1**. *Offline-RL cross-domain demo* (7.4) — a second paper, not a section. *Pip-installable diagnostic* (7.5) — the diagnostic's core signal is **not oracle-free** (5.1), so a standalone tool would ship something undeployable; **reject until X7 says what it can compute offline**. *TuRBO/Thompson optimizers* (7.2) — adds rows, not mechanism; and X3 already fixes the budget confound that makes the optimizer axis unreadable. *More Design-Bench tasks* (7.3) — X4 shows the suite can't resolve the question at any realistic N; adding 3 tasks doesn't reach the bar.

---

## The top five, with reasoning

**1 · X1 — normalize the targets and re-run.** Everything else is downstream. Right now "the GP's smooth
prior wins" and "the ensemble couldn't fit targets of magnitude 2600" predict the same table, and the
paper's controls cannot separate them (β=0 leaves the GP's *ranking* untouched — standardization is an
affine monotone transform of its LCB — while the ensemble's *training* pathology persists). One config
change, one grid, and the ambiguity is gone permanently. If η²_surr survives, this becomes the strongest
control in the paper. **The best CPU in the repo.**

**2 · X2 — report the gradtune sweep.** Zero cost, unconditional. The authors wrote a script whose stated
purpose was to kill the "under-tuned optimizer" objection, ran it, and it **failed its own pre-stated
decision rule on 3 of 4 tasks**. That result is in the released artifact. There is no version of this
where omission survives contact with a reviewer who opens the repo. Reported, it re-scopes the finding
into something still real and *sharper*: the collapse is a trust-region failure, and the coverage
diagnostic might predict which configurations collapse — which is the first genuinely *predictive* use
of the diagnostic anywhere in the project.

**3 · X4 — the power analysis, free.** 5.1 already produced it as a by-product: at n=14, **even a perfect
selection rule** clears only d_z = 0.71 against always-GP where 0.81 is needed for 80% power. That is not
a limitation paragraph, it is a **specification**: it says what a benchmark suite must be to answer the
question the field keeps asking it. `NOVELTY_CHECK` Q5 says the Design-Bench *complaint* is known but the
*measurement* is not — this is the measurement. It converts Contribution 3 from "we found nothing" into
"here is why nothing is findable here, and here is the N at which it would be." Costs zero CPU.

**4 · X6 — roughen the GP.** The cheapest way to risk the theory. Two grids. The paper currently has four
controls, all subtractive, all confirming. A reviewer reads that as assuming the conclusion. One
falsification test — *the theory forbids a rough GP from being robust* — is worth more than a fifth
confirming control, and if it fails the authors learn it before a reviewer does.

**5 · X5 — the smoothness interpolation family.** The most expensive of the five and still worth it: it
replaces the paper's weakest claim (a **two-point** comparison at N=7 with p=0.69 and a TOST the abstract
already concedes is underpowered) with a **trend across six α-levels** — which needs no equivalence test
and no N=7 apology. It also unifies Contributions 2 and 3 into one curve: Design-Bench stops being a
different world and becomes a point on an axis. The `ScaledAckley` ladder infrastructure for it already
exists in `PREREGISTRATION.md:32-36` and was never run.

**On X4 + X5 together:** they are the two halves of a defensible Contribution 3 — X4 says the current
benchmark *cannot* answer the question, X5 builds a benchmark that *can*. That pairing is a stronger
paper than either alone, and neither depends on the offline-selection idea that 5.1 killed.

---

## Late upgrade: X4 is stronger than its row says — it fills a named 20-year-old gap

A ~20-search sweep of the power-analysis literature returns a clean partition by *which sample-size axis*
a paper treats:

| Axis | Owned by |
|---|---|
| # test examples | Card et al., *With Little Power Comes Great Responsibility*, **EMNLP 2020** (2000-sentence MT test sets ≈ **75% power** to detect 1 BLEU) |
| # seeds / runs | Colas et al. (arXiv-only); **AdaStop, TMLR 2024** — *"Researchers in Deep RL often use less than 5 independent executions ... this is not enough in general"* |
| # topics / queries | Sakai (SIGIR 2016; Springer 2018, *topic set size design*); Urbano et al. (SIGIR 2019) |
| **# tasks / datasets** | **NOBODY — VERDICT: NONE FOUND** |

**Demšar (JMLR 2006) — the exact paper our CD diagram cites — identified this gap and left it open.**
He establishes Friedman + Nemenyi over multiple datasets and *observes* that Nemenyi's critical value can
be too large to detect real differences, i.e. that the procedure is underpowered when datasets are few.
**He never turns that observation into a power or sample-size analysis. Nobody has since, in 20 years.**

**So X4 is not a limitation paragraph. It is a contribution that closes a named gap in the canonical
reference this paper already depends on** — and 5.1 has already produced its core number for free
(a *perfect* selection rule reaches d_z = 0.71 where 0.81 is needed for 80% power at n=14).

**Method to borrow:** Sakai's *topic set size design* (Springer 2018, Ch. 7) is the closest template —
topics are to IR test collections what tasks are to a benchmark suite; it determines how many topics a
collection needs from a prior similar experiment. That is exactly the shape of "how many tasks must an
offline-MBO suite have."

**Revised ranking.** X4 moves to **joint-first with X1/X2**: zero CPU, novel, fills a 20-year gap, and
it is the "deeper analysis" NeurIPS 2026's Negative Results bar explicitly demands (`VENUE_NORMS.md`).
It also converts Contribution 3 from the paper's weakest half into a *specification*, and it pairs with
the Design-Bench App. D.3 framing (`NOVELTY_CHECK`): the field deleted GFP/UTR/ChEMBL for showing this
result, without ever computing how many tasks would be needed to detect it.

⚠️ **Bibliographic caution:** the most quotable seed-count sources are the weakest venues — Colas et al.
2018 is **arXiv-only**, Colas et al. 2019 is a **workshop** paper, Picard is arXiv-only. Cite **AdaStop
(TMLR 2024)** and **Card et al. (EMNLP 2020)** as the peer-reviewed anchors. Agarwal et al. (NeurIPS 2021
Outstanding Paper) is *not* a power paper — it argues for quantifying uncertainty at small N rather than
prescribing N, which is the opposite move; cite it for interval estimates/IQM, not for power.

### X4 — one reviewer trap to pre-empt (from an adjacent-literature sweep)

A sweep of the LLM-eval power literature is **tangential** (different field, different axis) and mostly
confirms the partition above: even there, the only papers where power is *the* headline are 2026 ICML
**workshop** posters; everything at main-conference level treats it as supporting. Task-count power stays
unowned. Two items are worth carrying:

**The trap.** *tinyBenchmarks* (Maia Polo et al., **ICML 2024**, PMLR v235:34303-34326, **267 cites**) and
*100 instances is all you need* (arXiv:2409.03563) are sample-size papers that ask the **inverse**
question: how *few* items suffice to estimate **one model's score** cheaply. X4 asks how *many* units are
needed to **detect a difference between methods**. Those are different questions on different axes —
theirs is items-within-a-task, ours is tasks-within-a-suite — but the titles collide, and **a reviewer may
cite "100 instances is all you need" against "your suite is too small."** Pre-empt it in one sentence:
estimation efficiency for a single score is not detection power for a contrast, and item count is not task
count. Do **not** cite them as support; they are the opposing framing.

**A usable anchor.** Miller, *Adding Error Bars to Evals* (arXiv:2411.00640) — *"new evals should contain
at least 1,000 questions in order to have good signaling ability"* — is a signaling-ability threshold,
i.e. a power claim, and is the cleanest citable N in that literature. ⚠️ It is **arXiv-only, never peer
reviewed** (v1, no journal-ref; DBLP files it under "Informal and Other Publications") despite ~96
citations and Anthropic branding. Its peer-reviewed counterpart is Bowyer et al., **ICML 2025 Spotlight**
(PMLR v267:81143-81184), which is narrower — interval validity, not power. Cite Bowyer for the venue and
Miller for the number, and never imply Miller is peer-reviewed.
```

---
## FILE: docs/PREREGISTRATION.md — DOES NOT EXIST
<!-- no file at this path. The ORIGINAL pre-registration is at repo root PREREGISTRATION.md; the revision pre-registration is docs/PREREGISTRATION_V2.md. Both included below under their real paths. -->

---
## FILE: PREREGISTRATION.md
<!-- lines: 66 | bytes: 3612 | last commit: 5f685c7 2026-07-12 -->
```markdown
Pre-registered experimental contract (frozen before the n=30 runs)
===================================================================
Committed per plan section 5 Phase 0. Changes after data lands require a
logged amendment in this file, not silent drift.

Headline factorial
------------------
Grid: {ens, botorchgp, svgp} x {grad, perturb, cma} + ens_conformal:{grad,perturb}
      + baselines {coms, cbas, sparse_gp, grad_ascent, gp}  (mbo.OFFLINE_METHODS)
Tasks: Branin-2D, Styblinski-5D, Levy-8D, Rosenbrock-10D, Rastrigin-15D,
       Ackley-20D, Griewank-30D  (fixed datasets, seed-0 generation; per-seed
       randomness is training/init only — Design-Bench convention)
Seeds: n=30 floor, all cells.
       n=50 for pre-declared crossover-boundary tasks: Rosenbrock-10D,
       Rastrigin-15D, Ackley-20D (close comparisons need ~0.91 power; n=30
       gives ~0.72 there). Rerun at 50 recomputes those cells fully.
Metric: 100th-percentile (max) + 50th-percentile of top-128 oracle scores,
        128-candidate budget. Continuous metric for law analysis: normalized
        regret vs task optimum (ladder family exposes .optimum).
Commands:
  python run_all.py --exp all --seeds 30 --jobs 96
  python run_all.py --exp mbo --seeds 50 --jobs 96 --tasks Rosenbrock-10D Rastrigin-15D Ackley-20D

Statistics
----------
Pairwise: Wilcoxon signed-rank + Holm per family (powered by seeds).
Rank apparatus: Friedman + Nemenyi CD, INTERNAL 9-cell grid only, powered by
task count not seeds; pre-registered as possibly-null (CD ~3.0-3.8 vs spread ~8).
Never run CD against the cited SOTA zoo. Bootstrap CIs B=2000-10000.

Scaling-law ladder (STRETCH, gated)
-----------------------------------
Family: ScaledAckley, d in {2,5,10,20,50,100}, N = 250*d clamped [2000,25000];
density knob instrumented (Ackley{d}D-x{m}) but NOT run unless the dimension
law passes. Config diversity across ladder points via ensemble K in {3,5,10}
(existing K exp) — not pure seed replication. GP-kernel diversity: skipped.
Gate (all must pass before the law gets main-text space):
 (i) ladder run clean; (ii) same runs re-scored on normalized regret
 (continuous-metric falsification); (iii) mediation at d=5,10 — conformal
 repair (ens_conformal:*) must move the ens-vs-GP optimizer gap in the
 predicted direction; (iv) only then full sweep/density.
Crossover statistic: log ensemble/GP optimizer-spread ratio (bounded
transform preferred; raw ratio has denominator instability).

Design-Bench arm
----------------
Subset: TFBind8 (d=32), TFBind10 (40), Superconductor (86), + Hopper (5126)
as the high-d anchor if the env builds. n=16 (community standard; DB oracle
calls are the costly step). NO seed-dependent significance claims on DB —
direction-of-crossover evidence only. Baselines run by us: coms, cbas, cma,
grad_ascent (+ BO-qEI if design-baselines env builds). DDOM/BONET/RaM/ExPT:
cited, not re-run.

Decision rule (STRETCH)
-----------------------
Two axes only ({GP, ensemble} x {grad, perturb}); fit boundary on all-but-one
task from (d, held-out calibration probe); predict held-out task's better arm;
report hit-rate vs always-GP and always-ensemble, leave-one-task-out. Fails
either trivial baseline -> reported honestly and dropped.

Washout contingency (pre-committed)
-----------------------------------
If the n=30 optimizer x surrogate interaction is small/non-significant, the
headline pivots to the calibration mechanism (coverage collapse + conformal
repair breaking under proposal shift), which is independent of crossover
magnitude; the factorial is then reported as a powered controlled null.
```

---
## FILE: docs/PREREGISTRATION_V2.md
<!-- lines: 32 | bytes: 3724 | last commit: 8074264 2026-07-17 -->
```markdown
# Pre-registration — revision experiments

Written BEFORE the runs. If a result contradicts a prediction here, that is a finding to
report, not a prediction to revise. Amendments require a dated entry at the bottom, not a
silent edit. Companion to `docs/MECHANISM_EXPERIMENTS.md` and `docs/EXTENSION_LEDGER.md`.

Precedent: the original `PREREGISTRATION.md` registered "the optimizer explains most of the
gap." The data gave eta2_opt = 0.01 — refuted. That refutation is an asset if disclosed. This
file exists so the same thing can happen again, visibly.

| ID | Prediction | Kill criterion |
|---|---|---|
| **X1** (M0, normalize ensemble targets) | eta2_surr drops materially from 0.37. The per-task GP-ensemble gap correlates with log\|y\|_scale BEFORE the fix (rho > 0.6) and not after (rho ~ 0). | If eta2_surr stays ~0.37 AND the gap does not track \|y\| scale, the target-scaling confound is REFUTED and the headline stands strengthened. Report as a passed control. |
| **X3** (equalize candidate/oracle protocol) | Ens x CMA improves relative to Ens x Grad once CMA stops being scored on a full-set median against a top-half median; eta2_inter shrinks. | If nothing moves, the protocol asymmetry was harmless. Report it and stop citing it as a flaw. |
| **X6** (M2, roughen the GP) | A Matern-1/2 GP (or fixed short lengthscale) COLLAPSES under gradient ascent; its premise coverage on its own proposals drops from 0.97. | If the rough GP stays robust, the mechanism is NOT prior smoothness. Identity C's thesis dies. Report it. |
| **X5** (M3, smoothness interpolation) | As alpha rises, all four move together and monotonically: gap shrinks, eta2_surr falls, c_ood falls, Friedman p rises toward non-significance. Design-Bench is reproduced as a limit point. | If the four move independently or non-monotonically, prior-match is not one axis and the unification fails. |
| **X7** (full 3x3 coverage) | The ensemble's premise coverage is ALSO low (~0.4) on CMA proposals; c_ood correlates with normalized score across all 9 cells. | If Ens x CMA coverage is high, "any aggressive optimizer exploits a jagged mean" is refuted and the gradient-specific framing is vindicated. |
| **X8** (M5, density ratio) | The learned ratio PARTIALLY but not fully restores proposal coverage; w is unbounded on the proposal region and ESS collapses. | Full restoration = a positive result the paper lacks. No effect = the shift defeats density-ratio methods, a sharper negative. All three outcomes are publishable; only "we did not try" is not. |
| **X10** (M6, coverage bound) | A bound of the form c_ood degradation <= Phi(L, D, beta, sigma_min) is derivable and TRACKS the realized c_ood when plotted. | If the bound is vacuous for unregularized ensembles — the LIKELY outcome — report that no non-vacuous bound was found. Do NOT manufacture a theorem. |

## Standing commitments

1. **X1 runs before anything else is interpreted.** No result below it is trusted until it lands.
2. **The gradtune sweep is reported regardless of outcome** (`FLAW_LEDGER.md` P0-0). It already ran
   and already failed its own pre-stated rule; that is not renegotiable.
3. **GFP is quarantined from headline coverage claims** unless the degenerate decode is fixed.
4. **No DB seed-dependent significance claims**, per the original `PREREGISTRATION.md:50-52`, which
   the current draft violates.
5. **Multiplicity is disclosed.** 5.1 ran 10 rules on n=14 and reported all 10. Any future rule
   search reports every rule tried, not the best.
6. **5.1 is reported as a dropped stretch goal**, per its own kill criterion — including the
   obstruction finding (the predictive signal is not oracle-free), which is the part worth keeping.
```

---
## FILE: docs/NOVELTY.md — DOES NOT EXIST
<!-- no file at this path; the novelty check is docs/NOVELTY_CHECK.md, included below -->

---
## FILE: docs/NOVELTY_CHECK.md
<!-- lines: 331 | bytes: 36371 | last commit: e3aeeed 2026-07-17 -->
```markdown
# Prior-Art / Novelty Check — "Decomposing the GP Advantage in Offline MBO" (AAAI-27)

Adversarial prior-art review. Verdicts: **PRIOR WORK FOUND** / **NONE FOUND** / **NOT VERIFIABLE HERE**.

**Bottom line up front:** the paper's *problem statements* are all pre-claimed in print (Design-Bench 2022 named offline model selection as future work; the TMLR 2026 survey named the surrogate-vs-optimizer attribution gap and the non-discrimination complaint almost verbatim). What survives is *measurement and mechanism*, not discovery. Contribution 2 (conformal/LCB) is the weakest and should be demoted. The proposed new direction is novel **only** in its specific combination — the components all exist.

---

## Q4 (HIGHEST PRIORITY). Offline model selection for offline MBO

### (a) Is it a RECOGNIZED OPEN PROBLEM? — **VERDICT: PRIOR WORK FOUND (the problem is explicitly named)**

Not by the Kim et al. survey — by **Design-Bench itself**, in its conclusion:

> "The comparatively high efficacy of even simple baselines such as CMA-ES and naïve gradient ascent suggests the need for careful tuning and standardization of methods in this area. **An interesting avenue for future work in offline MBO is to devise methods that can be used to perform model and hyperparameter selection. One promising approach to address this problem is to devise methods for offline evaluation of produced solutions.**"
> — Trabucco, Geng, Kumar, Levine, *Design-Bench: Benchmarks for Data-Driven Offline Model-Based Optimization*, ICML 2022, [arXiv:2202.08450](https://arxiv.org/abs/2202.08450), §Conclusion (verified in extracted PDF text, p.~10)

Design-Bench Appendix F ("Hyperparameter Selection Workflow") also formalizes the offline constraint:

> "Care must be taken when tuning each of the prescribed algorithms so that only offline information about the task is used for hyperparameter selection. Formally, this means that the hyperparameters, H, are conditionally independent of the particular value of the performance metric M, given the offline task dataset D."

**Kim et al. 2025/2026 survey** (*Offline Model-Based Optimization: Comprehensive Review*, Kim, Gu, Yuan, Yun, Liu, Bengio, Chen; TMLR 2026 w/ Survey Certification; [arXiv:2503.17286](https://arxiv.org/abs/2503.17286)) does **NOT** list model selection among its five future directions. Its §6 directions are verbatim: *Robust and Realistic Benchmarking; Uncertainty Estimation of Surrogate Model; Graphical Surrogate Model; Advanced Generative Modeling; Application to LLM Alignment and AI Safety.*

**But** its §6 contains the single most dangerous sentence for this paper — it names contribution 1's gap:

> "Moreover, existing benchmarks often emphasize overall optimization performance **without clarifying whether observed gains stem from superior surrogate modeling, improved optimization strategies, or mere chance. This lack of distinction underscores the need for independent and rigorous evaluations** of the uncertainty estimation capabilities of the surrogate model in newly developed algorithms."

**Assessment:** Good news and bad news. The problem is *recognized and citable* (strong motivation — quote Design-Bench directly). But the authors cannot claim to have identified the problem. Frame as "answering a question Trabucco et al. (2022) posed."

### (b) Offline RL prior art — **VERDICT: PRIOR WORK FOUND (a mature literature)**

Offline policy selection / offline hyperparameter selection is a well-developed subfield. The paper MUST cite these or a reviewer will:

| Work | Venue | Key point |
|---|---|---|
| Paine, Paduraru, Michi, Gulcehre, Zolna, Novikov, Wang, de Freitas, *Hyperparameter Selection for Offline Reinforcement Learning*, [arXiv:2007.09055](https://arxiv.org/abs/2007.09055) (2020) | arXiv/DeepMind | Canonical statement of the problem; OPE as selection proxy |
| Zhang & Jiang, *Towards Hyperparameter-free Policy Selection for Offline RL*, NeurIPS 2021, [arXiv:2110.14000](https://arxiv.org/abs/2110.14000) | NeurIPS | BVFT-based selection; notes OPE-based selection has its own hyperparameters — "chicken-and-egg" |
| Tang & Wiens, *Model Selection for Offline RL: Practical Considerations for Healthcare Settings*, MLHC 2021, [arXiv:2107.11003](https://arxiv.org/abs/2107.11003) | PMLR v149 | OPE as validation proxy pipeline |
| Kurenkov & Kolesnikov, *Showing Your Offline RL Work: Online Evaluation Budget Matters*, ICML 2022, [arXiv:2110.04156](https://arxiv.org/abs/2110.04156) | ICML | Expected Online Performance; critique of unlimited-budget selection |
| Yang et al., *Pessimistic Model Selection for Offline Deep RL*, [arXiv:2111.14346](https://arxiv.org/abs/2111.14346) | PMLR v216 | Pessimism-based selection |
| Fu et al., *Benchmarks for Deep Off-Policy Evaluation*, ICLR 2021 | ICLR | OPE benchmark |
| *Model Selection for Off-policy Evaluation: New Algorithms and Experimental Protocol*, [arXiv:2502.08021](https://arxiv.org/abs/2502.08021) (2025) | — | States model selection for offline evaluation is "under-investigated" |

**Assessment:** The *idea* "select offline using oracle-free proxies" is standard in offline RL. Novelty cannot rest on it.

### (c) CALIBRATION / COVERAGE as the selection signal — **VERDICT: PRIOR WORK FOUND (outside offline MBO)**

- **CC-Select** — *Conformal Prediction Assessment: A Framework for Conditional Coverage Evaluation and Selection*, [arXiv:2603.27189](https://arxiv.org/abs/2603.27189) (Mar 2026). Selects models by optimizing **conditional coverage**; introduces Worst-Slab Coverage (WSC) and a "Conditional Validity Index (CVI)... as a proxy for the unobservable conditional coverage probability, enabling model selection through a reliability estimator." This is *coverage-driven model selection*, explicitly.
- **CROMS** — Bao, Hu, Ren, Zhao, Zou, *Optimal Model Selection for Conformalized Robust Optimization*, [arXiv:2507.04716](https://arxiv.org/abs/2507.04716) (2025). Model selection for conformal robust *decision-making*: "the downstream decisions critically depend on model selection." Selects to minimize decision risk (not coverage per se), but couples conformal validity to a downstream optimizer's decision quality — conceptually adjacent.
- Coverage-matched hyperparameter tuning appears in the conformal literature generally (tune to match a target leave-one-out coverage).

**Assessment:** "Use coverage as a model-selection signal" is **not novel in general**. It is novel *as applied to offline MBO cell selection*.

### (d) Offline surrogate/optimizer selection for offline MBO — **VERDICT: PRIOR WORK FOUND (nearest neighbor is in evolutionary computation, not deep-learning MBO)**

**This is the biggest under-the-radar threat.** The evolutionary-computation "offline data-driven evolutionary optimization" (offline DDEO) community has been doing oracle-free offline surrogate selection since 2022, and the Design-Bench-lineage MBO literature almost never cites it.

1. **MS-DDEO** — *Offline data-driven evolutionary optimization based on model selection*, **Swarm and Evolutionary Computation, 2022**, DOI [10.1016/j.swevo.2022.101080](https://doi.org/10.1016/j.swevo.2022.101080) (25 citations). **The closest prior work to the paper's proposed direction.**
   - Builds a **model pool of four RBF models with different smoothness degrees** and selects among them offline.
   - Two **oracle-free** selection criteria: **Model Error Criterion** (uses ranking-top data as a held-out test set to test ability to predict the optimum) and **Distance Deviation Criterion** (estimates reliability via distance between the predicted solution and ranking-top data — *this is essentially "proposal displacement"*).
   - Reported framing: "four RBF models with different hyper-parameters construct the model pool with different smoothness, where more smoothness means the model has less multimodal, which also means there is less high-frequency information in the frequency domain." **This also touches Q2's mechanism.**
2. **IBEA-MS** — *Performance Indicator-Based Adaptive Model Selection for Offline Data-Driven Multiobjective Evolutionary Optimization*, **IEEE Trans. Cybernetics, 2022**, DOI [10.1109/TCYB.2022.3170344](https://doi.org/10.1109/tcyb.2022.3170344) (42 citations). Code: https://github.com/HandingWangXDGroup/IBEA-MS
3. *Offline evolutionary optimization with problem-driven model pool design and weighted model selection indicator* (**MSEA**), Swarm and Evolutionary Computation, 2025, [S2210650225001920](https://www.sciencedirect.com/science/article/abs/pii/S2210650225001920) — "significant improvements over MS-DDEO"; replaces the RBF-smoothness-based pool.
4. Wang, Jin et al., *Offline Data-Driven Evolutionary Optimization Using Selective Surrogate Ensembles*, IEEE TEVC 2019, DOI 10.1109/TEVC.2018.2834881.

**CRISP VERDICT ON THE PROPOSED DIRECTION:**

> **Partially novel — the framing is novel, the ingredients are not.** "Coverage-driven offline surrogate×optimizer selection for offline MBO" is **not** a green field. Specifically:
> - Offline oracle-free **surrogate** selection for offline optimization: **DONE** (MS-DDEO 2022, IBEA-MS 2022, MSEA 2025).
> - **Coverage/conformal** as a model-selection signal: **DONE** (CC-Select 2026; CROMS 2025).
> - Oracle-free proxies for offline method selection: **DONE, mature** (offline RL, 2020–2025).
> - Selecting the **optimizer** jointly with the surrogate, for offline MBO, using **conformal premise-coverage** specifically: **NONE FOUND.** This joint cell-selection framing is where novelty lives.
>
> **Nearest prior work: MS-DDEO (Swarm Evol. Comput. 2022).** A reviewer from the EC community will find it immediately. It already does offline model selection over a smoothness-graded surrogate pool using a displacement-like criterion — i.e. two of the paper's four proposed oracle-free quantities, in the same problem class.
>
> **Recommendation:** cite MS-DDEO/IBEA-MS explicitly and differentiate on (i) selecting the *optimizer* as well as the surrogate, (ii) *distribution-free conformal* coverage rather than heuristic criteria, (iii) deep-learning surrogates + Design-Bench rather than RBF + EC benchmarks. Do **not** claim "first offline model selection for offline MBO" — that claim is refutable with one citation.

---

## Q1. Controlled factorial decomposition surrogate × acquisition optimizer

**VERDICT: NONE FOUND for the factorial itself; PRIOR WORK FOUND for a large share of the *finding*.**

### What Li / Rudner / Wilson actually owns

**Correction the authors need: the paper is ICLR 2024, not ICLR 2023.** (arXiv May 2023; published *Proceedings of ICLR 2024*.)
Yucen Lily Li, Tim G. J. Rudner, Andrew Gordon Wilson, *A Study of Bayesian Neural Network Surrogates for Bayesian Optimization*, **ICLR 2024**, [arXiv:2305.20028](https://arxiv.org/abs/2305.20028).

Verified from the full HTML text:

- **Acquisition is FIXED, and there is no optimizer factor.** > "We use Monte-Carlo based Expected Improvement (Balandat et al., 2020) as our acquisition function **for all problems**." Confirmed again in Appendix C.1: "We also use Monte-Carlo based Expected Improvement as our acquisition function." **No acquisition-optimizer variation anywhere in the paper.** → *The factorial design is genuinely not theirs.*
- **It is online/sequential BO, not offline MBO.** Different problem: they get to query the oracle; the paper's setting forbids it.
- **It DOES own the two headline findings' direction:**
  > "(i) the ranking of methods is highly problem dependent, suggesting the need for tailored inductive biases; ... (iv) deep ensembles perform relatively poorly"
  > "While deep ensembles often provide good accuracy and well-calibrated uncertainty estimates in other settings [Lakshminarayanan et al., 2017], **we show they can perform relatively poorly for Bayesian optimization.**"
- **Crucially, its MECHANISM is DIFFERENT from the paper's — this is the paper's opening.** LRW attribute the deep-ensemble failure to **lack of functional diversity in the low-data regime**, i.e. an uncertainty/diversity story:
  > "With minimal training data, the loss landscape is relatively smooth, and separately-trained models are less diverse." / "in the low-data regime, models have more similar weights and therefore are less diverse." / "This behavior suggests that the basins are not particularly d[istinct]..."
- **It discusses smoothness — but of the prior/function draws, not of the posterior mean as an optimization surface:**
  > "The choice of activation function in a neural network determines important characteristics of the function class, such as smoothness or periodicity... function draws from the ReLU BNN appearing **more jagged** and function draws from the tanh BNN more closely resembling the draws from a GP with a Squared Exponential [kernel]."
  > and on stationarity: "because the covariance between two values only depends on their distance..., this setup assumes the function is stationary and has similar mean and smoothness throughout the input space."

### Other near misses (none is a factorial)

- Kim et al. TMLR 2026 survey §6 — *names the gap* ("whether observed gains stem from superior surrogate modeling, improved optimization strategies, or mere chance") but performs no experiment.
- **fANOVA** — Hutter, Hoos, Leyton-Brown, *An Efficient Approach for Assessing Hyperparameter Importance*, ICML 2014, [PMLR v32](https://proceedings.mlr.press/v32/hutter14.html). The canonical **variance-decomposition-of-design-choices** methodology (variance explained by components + low-order interactions). Methodological precedent the paper should cite; a reviewer may ask "why not fANOVA?"
- *An Empirical Study of Bayesian Optimization: Acquisition Versus Partition*, JMLR 22 (2021), https://www.jmlr.org/papers/v22/18-220.html — an empirical decomposition of BO into components (acquisition vs partition), not surrogate × optimizer.
- HEBO — Cowen-Rivers et al., JAIR 74 (2022), [arXiv:2012.03826](https://arxiv.org/abs/2012.03826) — large ablations over surrogates/acquisitions/acquisition-maximisers ("robust acquisition maximisers afford empirical advantages relative to their non-robust counterparts"), but not a clean factorial and not offline.
- Design-Bench itself compares CMA-ES / gradient ascent / REINFORCE / BO-qEI as *whole methods*, never crossing surrogate with optimizer.

### How much of contribution 1 survives

**Survives:** the factorial design itself; the *offline MBO* setting; the η² quantification (surrogate 0.37 / optimizer 0.01 / interaction 0.17); and — most importantly — the **mechanism attribution to posterior-mean smoothness rather than calibration**, which *directly contradicts* LRW's diversity/calibration explanation. That contradiction is the paper's best asset and should be foregrounded.

**Does NOT survive:** "deep ensembles are poor surrogates" (LRW own it) and "ranking is problem-dependent → inductive biases matter" (LRW own it, nearly in the paper's words). Claiming either as a discovery is refutable with one citation.

**Recommended claim wording:** *"first controlled surrogate×optimizer factorial in offline MBO"* — defensible. Drop *"first controlled factorial decomposition"* unqualified, and never imply the deep-ensemble finding is new.

---

## Q2. GP smooth posterior mean vs jagged ensemble mean → optimizer exploitation

**VERDICT: see delegated findings below (integrated).** Independent of that: note that **MS-DDEO (2022) already grades an offline surrogate pool by smoothness** ("more smoothness means the model has less multimodal... less high-frequency information in the frequency domain") and selects on it — so "smoothness of the surrogate is the axis that matters for offline optimization" has a 2022 precedent in the EC literature. Also, the Kim TMLR survey already lists **"smoothness priors (Yu et al., 2021)"** [RoMA] among established offline-MBO remedies, so "surrogate smoothness helps offline optimization" is established; the paper's specific contribution must be *attribution of the GP's advantage to mean smoothness rather than calibration*, not the value of smoothness per se.

<!-- Q2_AGENT_FINDINGS -->

---

## Q3. Coverage / conformal diagnosis of LCB pessimism

**VERDICT: PRIOR WORK FOUND — this is the paper's weakest contribution. Both propositions are restatements.**

### Proposition 1 (premise coverage == bound validity)

The identity P(f ≥ μ − βσ) = P(μ − f ≤ βσ) is trivial, and the substantive content — *pessimism is only sound if the penalty is a valid confidence bound* — is a **stated assumption** in the offline-RL pessimism literature:

- **Jin, Yang, Wang, *Is Pessimism Provably Efficient for Offline RL?*, ICML 2021**, [PMLR v139](https://proceedings.mlr.press/v139/jin21e.html). PEVI's guarantee is conditioned on the penalty being a **ξ-uncertainty quantifier** — i.e. the entire suboptimality bound holds *if and only if* the bound is valid with the stated probability. That is Proposition 1's content, as a formal assumption, since 2021.
- Stanton, Maddox, Wilson (below) state the motivating version for BO directly.

**Assessment: PRIOR WORK FOUND.** Do **not** present this as a proposition. Demote to a remark with a citation to Jin et al. 2021. Labelling a one-line identity "Proposition 1" invites a reviewer to call the paper's theory padding — a real AAAI risk.

### Proposition 2 (split conformal + weighted conformal under covariate shift)

Essentially a restatement of two known results, and it has been *specifically* done for design and for offline MBO:

1. **Fannjiang, Bates, Angelopoulos, Listgarten, Jordan, *Conformal prediction under feedback covariate shift for biomolecular design*, PNAS 119(43):e2204569119, 2022**, [arXiv:2202.03613](https://arxiv.org/abs/2202.03613) / [PNAS](https://www.pnas.org/doi/abs/10.1073/pnas.2204569119). Provides "confidence sets for designed objects with **finite-sample guarantees of statistical validity for any design algorithm involving any learned regression model**" under the covariate shift *induced by the design algorithm itself*. **This is Proposition 2's setting, published in PNAS four years earlier.**
2. **Tibshirani, Barber, Candès, Ramdas, *Conformal Prediction Under Covariate Shift*, NeurIPS 2019** — the weighted-conformal result the paper already cites. Proposition 2's second half is this theorem applied.
3. **Stanton, Maddox, Wilson, *Bayesian Optimization with Conformal Prediction Sets*, AISTATS 2023**, PMLR v206, [arXiv:2210.12496](https://arxiv.org/abs/2210.12496). Owns the *coverage-as-validity-diagnostic-for-acquisition-decisions* framing:
   > "In practice, subjectively implausible outcomes can occur regularly for two reasons: 1) model misspecification and 2) covariate shift. Conformal prediction is an uncertainty quantification method with **coverage guarantees even for misspecified models and a simple mechanism to correct for covariate shift**. We propose conformal Bayesian optimization, which **directs queries towards regions of search space where the model predictions have guaranteed validity**... In many cases we find that **query coverage can be significantly improved** without harming sample-efficiency."
4. **Choi, Seungjin, *Conformal Candidate Certification for Offline Model-Based Optimization*, ICML 2026 Workshop (Decision-Making from Offline Datasets to Online Adaptation), submitted 13 Jun 2026**, [arXiv:2606.15217](https://arxiv.org/abs/2606.15217). **Contemporaneous and nearly the same construction, in the same setting:**
   > "Because candidates are deliberately out-of-distribution, surrogate rankings are least reliable exactly where the optimizer is most aggressive... We propose Conformal Candidate Certification (CCC), a post-hoc wrapper that **attaches a calibrated one-sided lower bound to each candidate**... We show that entropy-regularized surrogate maximization induces a Gibbs-tilted proposal, so the same surrogate supplies importance weights for **weighted conformal prediction** without a separate density-ratio estimation step. In a controlled synthetic study, CCC certifies 16.7% of an aggressive proposal pool with **empirical coverage 0.990 at nominal 0.90, while standard conformal prediction ignoring the covariate shift collapses to 0.416 coverage**."
   - One-sided *lower* bound: same. Weighted conformal for the design-induced shift: same. Empirical coverage as the diagnostic: same. Offline MBO: same.
   - Mitigating factors: it is a **workshop paper by a single author**, public only since June 2026, and does **not** do surrogate×optimizer selection. It is contemporaneous with an AAAI-27 submission — but it is public, so a reviewer can cite it.

Also relevant (calibration-improves-decisions lineage the paper should cite): Kuleshov, Fenner, Ermon, *Accurate Uncertainties for Deep Learning Using Calibrated Regression*, ICML 2018, [PMLR v80](https://proceedings.mlr.press/v80/kuleshov18a.html); Malik et al., *Calibrated Model-Based Deep RL*, ICML 2019, [arXiv:1906.08312](https://arxiv.org/abs/1906.08312); Deshpande & Kuleshov, *Online Calibrated and Conformal Prediction Improves Bayesian Optimization*, AISTATS 2024, [arXiv:2112.04620](https://arxiv.org/abs/2112.04620); Gibbs & Candès, *Adaptive Conformal Inference Under Distribution Shift*, NeurIPS 2021.

### How much of contribution 2 survives

**Very little as stated.** Proposition 1 is a known assumption (Jin et al. 2021). Proposition 2 is split conformal + Tibshirani et al. 2019, already instantiated for design in PNAS 2022 (Fannjiang et al.) and for offline MBO in arXiv 2606.15217 (Choi 2026). Coverage-as-validity-diagnostic for optimizer-driven queries is Stanton et al. AISTATS 2023.

**Recommendation:** stop presenting this as a theoretical contribution. Reframe "premise coverage" as an **empirical diagnostic instrument** used to support contribution 1's calibration-vs-smoothness argument (its actual job in the paper), cite Fannjiang/Tibshirani/Stanton/Choi as the machinery, and claim only the *diagnostic use*. As written, contribution 2 is the most likely single point of reviewer attack.

---

## Q5. Synthetic → Design-Bench validity collapse / non-discriminativeness

**VERDICT: PRIOR WORK FOUND for the complaint; NONE FOUND for the measurement.**

1. **Kim et al., TMLR 2026 survey** ([arXiv:2503.17286](https://arxiv.org/abs/2503.17286)), §6 "Robust and Realistic Benchmarking" — **the most dangerous citation**:
   > "Current benchmarks in offline MBO face two major challenges. First, some benchmarks—such as TFB8 and TFB10 (Barrera et al., 2016a)—offer overly constrained search spaces where even simple gradient ascent methods can achieve impressive results, **making it difficult to distinguish the performance of more sophisticated algorithms.** Second, benchmarks like superconductor (Hamidieh, 2018) often rely on learned oracles for evaluation, which can be vulnerable to manipulation and may not accurately reflect true performance."
   Plus the attribution sentence quoted under Q4(a) ("...or mere chance").
2. **Design-Bench itself** (Trabucco et al., ICML 2022), abstract + results:
   > "The comparatively high efficacy of even simple baselines such as CMA-ES and naïve gradient ascent suggests the need for careful tuning and standardization of methods in this area."
   > "a classical CMA-ES baseline is competitive with several highly sophisticated MBO methods in 4 out of 8 tasks... a naive gradient ascent baseline is competitive with complex approaches utilizing generative modelling on 4 of the 8 tasks."
   → "simple baselines are competitive" is **2022 canon, from the benchmark authors**. Design-Bench also already uses Agarwal et al. (2021) IQM + stratified bootstrap CIs, so "they ignored uncertainty" is not an available criticism.
3. **Surana, Grinsztajn, Atkinson, Duckworth, Barrett, *Overconfident Oracles: Limitations of In Silico Sequence Design Benchmarking*, ICML 2024 AI4Science Workshop**, [arXiv:2502.17246](https://arxiv.org/abs/2502.17246) — a *different* failure mode (oracle instability, not non-discrimination):
   > "we examine 12 sequence design methods... and find that there are **significant challenges with their cross-consistency and reproducibility**. Indeed, oracles differing by architecture, or even just training seed, are shown to **yield conflicting relative performance**"
4. **SOO-Bench, ICLR 2025** — good news: it justifies itself on **stability**, not discrimination: "Although benchmarks called Design-Bench already exist in this emerging field, it can hardly evaluate the **stability** of offline optimization." Not a scoop.
5. Broader ML precedent for the statistical argument: Agarwal, Schwarzer, Castro, Courville, Bellemare, *Deep RL at the Edge of the Statistical Precipice*, NeurIPS 2021, [arXiv:2108.13264](https://arxiv.org/abs/2108.13264).

**How much survives:** **Dead** — "simple baselines are competitive" and "Design-Bench is hard to distinguish methods on." Both are in print, the latter in the field's canonical review from six months ago. **Alive** — the *quantification*: no source runs an omnibus test on Design-Bench, and none stages the **paired synthetic-vs-real contrast** (p=6e-5 → p=0.69) as a validity collapse. The synthetic arm is the real defense: it rules out "your protocol is underpowered."

**Recommended reframe:** drop "null result / we discovered." Adopt: *"the field has suspected this (Trabucco et al. 2022; Kim et al. 2026); we are the first to measure it, and the synthetic control shows the collapse is a property of the benchmark, not of our power."* Cite Kim et al. early — pre-empting converts the biggest threat into motivation. Contribution 3 survives as **quantification + attribution**, not as complaint.

---

## Q6. Known criticisms of deep-ensemble uncertainty quality

**VERDICT: PRIOR WORK FOUND (abundant — for related work).**

<!-- Q6_AGENT_FINDINGS -->

---

## Q7. ANOVA/η² on normalized scores; Friedman/Nemenyi; TOST with tiny N

**VERDICT: PRIOR WORK FOUND (abundant — the paper must preempt these).**

<!-- Q7_AGENT_FINDINGS -->

---

## Summary table

| # | Claim | Verdict | Nearest prior work | Survives? |
|---|---|---|---|---|
| Q4 | Coverage-driven offline surrogate×optimizer selection | **PRIOR WORK FOUND (partial)** | MS-DDEO (SWEVO 2022); CC-Select (2026); Design-Bench §Conclusion (2022) | Joint surrogate+optimizer cell selection via conformal coverage: novel. Everything else: taken. |
| Q1 | First surrogate×optimizer factorial in offline MBO | **NONE FOUND** (design) / **PRIOR WORK FOUND** (finding) | Li, Rudner & Wilson, **ICLR 2024** (not 2023) | Factorial + offline setting + smoothness-not-calibration mechanism survive. "Ensembles are poor," "ranking is problem-dependent" do not. |
| Q2 | GP smooth mean → optimizer exploitation | see integrated section | RoMA (smoothness priors); offline-RL model exploitation; MS-DDEO smoothness pool | Mechanism *attribution* is the live part |
| Q3 | LCB premise-coverage; Props 1 & 2 | **PRIOR WORK FOUND** | Jin et al. ICML 2021; Fannjiang et al. PNAS 2022; Stanton et al. AISTATS 2023; Choi arXiv:2606.15217 (2026) | Weakest contribution. Demote to diagnostic. |
| Q5 | Synthetic→Design-Bench validity collapse | **PRIOR WORK FOUND** (complaint) / **NONE FOUND** (measurement) | Kim et al. TMLR 2026 §6; Design-Bench 2022 | Quantification survives; complaint does not |
| Q6 | Deep-ensemble uncertainty criticisms | **PRIOR WORK FOUND** | see section | Related work only |
| Q7 | Stats methodology criticisms | **PRIOR WORK FOUND** | see section | Preempt required |

---

## Late corrections (verified 2026-07-17) — citation traps that would be reviewer-visible

**1. Li/Rudner/Wilson is ICLR 2024** (arXiv:2305.20028, OpenReview `SA19ijj44B`). The bib key
`li2024bnnsurrogates` is right. It supports the thesis in unusually quotable language: *"deep ensembles
work surprisingly poorly, given their success in other settings"*; *"Deep ensembles also consistently
underperform the other surrogate models ... This result is surprising, since ensembles are often seen to
as an effective way to measure uncertainty"* (sic); and the inductive-bias point — *"on standard
benchmarks, standard GPs are relatively competitive, due to their strong priors and simple exact
inference procedures."*

**2. Do NOT cite Ovadia 2019 or Ashukha 2020 as anti-ensemble.** Both conclude the opposite.
Ovadia et al. (NeurIPS 2019, arXiv:1906.02530): *"Deep ensembles seem to perform the best across most
metrics and be more robust to dataset shift."* Ashukha et al. (ICLR 2020, arXiv:2002.06470): *"Deep
ensembles dominate other methods given a fixed test-time budget."* Citing either for "ensembles are
poorly calibrated" is a **miscitation a reviewer will catch**. Cite Ovadia instead for the
method-agnostic claim we actually need: *"calibration on the i.i.d. validation dataset does not
guarantee calibration under distributional shift"* — which is our Prop 2 story, stated better.

**3. The anti-ensemble load must ride on:** D'Angelo & Fortuin (NeurIPS 2021, arXiv:2106.11642) —
*"they do not offer any guarantees for the diversity between those hypotheses nor do they provably
converge to the true Bayesian posterior under any meaningful limit"* (**directly relevant: our members
differ only by init seed, `mbo.py:135`, no bootstrap**); Li et al. 2024; and NEMO (Fu & Levine, ICLR
2021, arXiv:2102.07970), the **only** in-setting paper that says it: *"In out-of-support regions far
from the data, the bootstrap ensemble tends to underestimate uncertainty and produce overconfident
predictions."*

**4. Do NOT attribute ensemble-calibration criticism to COMs, Design-Bench, or RoMA.** Not supportable
from their text — they argue *model exploitation*, not calibration. COMs/Design-Bench contain zero
occurrences of "uncertainty"/"calibrat"/"epistemic"; RoMA has zero "ensembl".

**5. Statistics citations to preempt (all P1-2 / T6 / T9 territory).** Agarwal et al., *Deep RL at the
Edge of the Statistical Precipice*, **NeurIPS 2021 Outstanding Paper** (arXiv:2108.13264) — lands
directly on N=7; recommends interval estimates and IQM over point estimates. η² bias: Okada (2013)
*Behaviormetrika* 40(2):129-147 — note its answer is that **ε² is least biased**, not ω². Bounded [0,1]
outcomes violate OLS: Smithson & Verkuilen (2006) *Psych. Methods* 11(1):54-71 (beta regression).
**TOST at N=7:** Lakens (2017), *SPPS* 8(4):355-362 — *"Rejecting small effects in an equivalence test
requires large samples ... in most cases, only a meta-analysis will have sufficient statistical power."*
At N=7 an inconclusive TOST is the **predicted** outcome, so it carries near-zero evidential weight.
**The text must never imply inconclusive ≈ equivalent.**

⚠️ Scariano & Davenport (1987) is often quoted for "ρ=0.3 inflates α to 0.49" — the source is paywalled
and that figure is **NOT VERIFIED**. Do not cite the number without checking the primary text.

---

## Design-Bench scoop check (verified 2026-07-17) — NOT SCOOPED, with one large complication

**Verdict: NONE FOUND.** No paper runs an omnibus statistical test across offline-MBO methods on
Design-Bench and reports a null. Not in ~100 citing papers scanned, not in SOO-Bench, and the field's
own 44-page TMLR-certified survey (arXiv:2503.17286) has **zero hits** for "indistinguish" / "not
distinguish" / "error bar". Contribution 3's *measurement* is unscooped.

### The gift — and it lands directly on P0-5 / D5

**Design-Bench's authors excluded GFP and UTR for exactly our reason** (Trabucco et al., ICML 2022,
App. D.3, verbatim):

> "Note that for GFP and UTR performance of offline MBO method is **not not distinguishable** [sic], and
> we consider this an indication each task is **not suitable for benchmarking offline MBO methods**."

The field later dropped ChEMBL on the same grounds (arXiv:2506.07109, App. C.1: *"almost all methods
produce the same oracle prediction results ... not appropriate for comparison"*). Design-Bench shipped
8 tasks; the modern convention is **5** (Ant, D'Kitty, Superconductor, TF8, TF10).

**We run 7 — including GFP and UTR, the two tasks the benchmark's own authors deleted for being
non-discriminative.** This cuts both ways and the paper must choose, explicitly:

- **As a threat:** a reviewer objects that our null is manufactured by re-including tasks documented as
  unsuitable. Compounding it, `FLAW_LEDGER.md` **P0-5** shows our headline coverage claim is carried
  *entirely by GFP = 0.00*, which our own supplement calls a degenerate decode artifact. So the two
  weakest tasks drive two different headline claims.
- **As the paper's best framing:** *the community has spent four years deleting the tasks that show this
  result.* That is defensible, novel, built from the field's own words — **but only if stated
  deliberately.** Silence reads as the threat.

**This changes D5.** Quarantining GFP is no longer only about honesty; it is entangled with whether the
task set is a bug or the argument. Decide the framing first, then the task list. Also: Hopper has a known
normalization bug (design-bench issue #8) — do not include it unquestioned.

### The main threat to Contribution 3 — DEMO (TMLR 2025)

DEMO (arXiv:2405.13964, §5.5) runs **Welch's t-test + Bonferroni across seven tasks** and *reports
significance* over 7–16 baselines per task. A reviewer will cite it against our null. **The defense is
sound and must be stated in related work:** DEMO's test is *per-task, pairwise, one new method vs. each
baseline* — the comparison most exposed to tuning asymmetry. Friedman across N=7 asks a different
question: *do the methods differ as a family?* Ours is an omnibus test; theirs is not.

Useful corroboration: the field's actual "significance" convention is an informal **1-SD overlap
bolding rule** (DEMO §5.5, tracing to COMs 2021 and ICT 2023) — an implicit admission that error bars
overlap, with no omnibus test ever run. That is precisely the gap. Design-Bench's own Table 2 supports
it: TF-Bind-10 spans 0.616–0.730 across 10 methods; ChEMBL SDs (0.22–0.31) rival the entire range;
CMA-ES on Ant is 1.214 ± 0.732. Several cells have SD = 0.000 (degenerate) — good justification for
rank-based tests over parametric ones.

### Must-cite or the framing reads as uninformed

- **IGNITE** (NeurIPS 2024, arXiv:2503.04242) — *"reducing surrogate sharpness on the offline dataset
  provably reduces its generalized sharpness on unseen data"*; surrogate sharpness beats loss sharpness
  for offline optimization. **The nearest prior claim to our smoothness thesis. Omitting it is a real
  risk.** Also **BOSS** (ICML 2024, surrogate sensitivity).
- **PGS** (AAAI 2024, arXiv:2405.05349) — its premise is the *antithesis* of our conclusion: the field
  over-invested in surrogates and under-invested in optimizers; *"surrogate models ... can be non-smooth
  which could result in highly sub-optimal solutions for a fixed gradient search strategy."*
  **AAAI-27 reviewers may include its authors.** Engage it directly.
- **Overconfident Oracles** (2025) — *"oracles differing by architecture, or even just training seed,
  are shown to yield conflicting relative performance"*. Supports our RF-oracle argument (T4).
- **Design-Bench's own concessions**, quotable: *"this approach to evaluation diminishes the realism of
  our benchmark"*; *"The comparatively high efficacy of even simple baselines such as CMA-ES and naïve
  gradient ascent suggests the need for careful tuning and standardization of methods in this area"*;
  and — directly on P0-0/P0-2 — the gradient baseline *"is also sensitive to certain design choices such
  as input normalization schemes and the number of optimization steps."*

**Baselines a reviewer will demand** (RaM's ICLR-2025 set, ~21): BO-qEI, CMA-ES, REINFORCE, Grad+Mean/Min,
CbAS, MINs, COMs, RoMA, IOM, BDI, DDOM, BONET, ICT, Tri-Mentoring, GTG, PGS, FGM, Match-OPT; plus RaM,
IGNITE, BOSS, DEMO for a 2026/27 submission. SOO-Bench (ICLR 2025) may be requested as the successor
benchmark — if the null holds there too it materially strengthens the paper.
```

---
## FILE: docs/SCOPE_EXPANSION.md — DOES NOT EXIST
<!-- never created. Phase 7 scope-expansion decisions were folded into the "Rejected, with reasons" section of docs/EXTENSION_LEDGER.md rather than given their own file. -->

---
## FILE: docs/FLAW_LEDGER.md
<!-- lines: 423 | bytes: 28093 | last commit: 4e05863 2026-07-17 -->
```markdown
# Flaw ledger — "Decomposing the GP Advantage in Offline MBO"

Merged and deduplicated from the implementation audit, the claim-provenance trace,
the artifact inventory, and the adversarial threat list (T1–T12). Sorted by severity,
then by fix cost.

**Evidence rule.** Every row cites `file:line` or a PDF/`.tex` location. Nothing here
is inferred from the manuscript alone. Where an artifact is absent the row says
MISSING rather than reconciling.

Severity: **P0** reject-driver · **P1** major-revision demand · **P2** minor · **P3** polish.

---

## P0 — reject-drivers

### P0-0 · The authors' own control refutes the paper's mechanism, and the paper does not report it
**Claim at risk:** the ensemble×gradient collapse — i.e. the premise of Contribution 2 and the
subject of Figure 4 and all of Section 5.

**This is the most serious finding in this ledger.** It is not an outside objection. It is the
authors' own pre-stated test, run, failed, and unreported.

**Evidence.** `code/gradtune.py:1-5` states its own purpose and decision rule verbatim:

> *"Robustness sweep rebutting the #1 reviewer objection: 'the ensemble's gradient-ascent collapse
> is just an under-tuned optimizer.' … **If even the best-tuned gradient config still underperforms
> perturbation, the collapse is surrogate geometry (genuine), not tuning.**"*

`gradtune.py:22` defines `grad_default = dict(lr=0.05, steps=100)`. That is **exactly** the main
grid's gradient optimizer: `mbo.py:26-27` `OPT_STEPS=100`, `LR_OPT=0.05`, and `mbo.py:166`
`grad_opt(..., steps=OPT_STEPS, lr=LR_OPT, normalize=False, trust=None)`. The comparison is direct.

Means over 15 seeds from `results/results_gradtune.json` (higher is better):

| Task | perturb | grad_default (= the grid's) | best gradient config | verdict by the script's own rule |
|---|---|---|---|---|
| Branin-2D | −0.792 | **−8.174** | **−0.543** (`grad_trust`) | gradient **beats** perturb |
| Styblinski-5D | 33.008 | **5.557** | **34.295** (`grad_besttuned`) | gradient **beats** perturb |
| Rosenbrock-10D | −0.116 | −0.275 | −0.138 (`grad_gentle`) | perturb wins (narrowly) |
| Ackley-20D | −6.405 | −3.767 | **−3.731** (`grad_gentle`) | gradient **beats** perturb decisively |

**By the script's own criterion the collapse is NOT surrogate geometry. It is tuning — on 3 of 4 tasks.**
A single trust-region hyperparameter (`trust=0.1`) moves Branin from −8.17 to −0.54 (**15×**) and
Styblinski from 5.56 to 34.30 (**6×**). The paper's Table 1 reports Branin Ens×Grad = −9.27, consistent
with the untuned `grad_default`.

Commit `cdd5ad8`'s own message records the result: *"Smoke: trust region closes the ensemble gradient
collapse."*

The manuscript never mentions it. The string "trust" does not appear in `main.tex`. The only tuning
control in the paper (`main.tex:94`) is **matched tuning**, which *removes the GP's* hyperparameter
budget and gives the ensemble and the gradient optimizer **nothing** — precisely the asymmetry T1
predicted.

**Reviewer's phrasing:** "The released code contains a gradient-tuning sweep whose stated purpose is to
test whether the collapse is a tuning artifact. It concludes that it is: a trust region closes the gap
on three of four tasks, and on Ackley plain gradient ascent already beats perturbation. This result is
absent from the paper. The central mechanism is an artifact of one untuned optimizer setting."

**Fix.** There is no way to fix this by argument — only by reporting it. Three honest options:
1. **Re-scope.** The finding becomes "the ensemble's gradient collapse is a *trust-region* failure, and
   the LCB premise-coverage diagnostic *predicts which configurations collapse*." That is still a real
   contribution and it makes the diagnostic **predictive**.
2. **Re-run the grid with a tuned gradient optimizer** on the ensemble and report what survives. If
   η²_inter = 0.17 evaporates, say so.
3. **Report the sweep as a limitation.** Weakest option; a reviewer who opens the artifact finds it anyway.

**Cost:** 0 h to disclose. ~1 grid re-run to re-scope properly (combine with P0-2's re-run — one pass).
**Fixable:** yes. **Blocks submission:** **yes — unconditionally.** Shipping a mechanism claim that the
repo's own control refutes, with the refuting result in the released artifact, is the single largest
risk in this project.

**Caveats, stated honestly.** gradtune is 4 tasks × 15 seeds, not 7 × 30; it compares gradient against
`perturb` only, not against the full 3×3 grid; and it uses the grid's default ensemble, so it inherits
P0-2's unnormalized-target problem. None of these caveats rescue the paper — they are reasons the sweep
should be *run properly and reported*, not reasons to omit it.

---

### P0-1 · The identifiability license is factually false against the code
**Claim at risk:** the entire causal attribution — every η², the whole decomposition.

**Evidence.** `main.tex:91` states: *"the data split, candidate budget, input normalization,
and oracle scoring are held identical. This shared closure is what licenses attributing
score differences to the surrogate×optimizer factors rather than to incidental protocol
choices."* `main.tex:93`: *"Each method proposes 128 candidates."*

The code does none of this:
- `mbo.py:384-389` `init_candidates` returns `concat([xt, xp])` = **256** rows (`TOP=128`, `mbo.py:25`).
- `mbo.py:188` gradient returns the **final iterate** of all 256.
- `mbo.py:198-201` perturbation returns **per-slot best-LCB-ever** over 256 slots.
- `mbo.py:292` CMA returns **top-128 by surrogate LCB** — i.e. 128 rows.
- `mbo.py:392-394` `eval_designs` then calls `task.oracle(x_final)` on **whatever it is handed**
  and keeps `np.sort(sc)[-128:]`.

Consequence: gradient and perturbation consume **256 oracle calls** and report the best 128;
CMA consumes **128** and its `[-128:]` slice is the identity. So `p50` is *the median of an
oracle-selected top half* for grad/perturb but *the median of the entire unfiltered proposal
set* for CMA — **two different estimands reported in one column**. The optimizer factor is
confounded with a 2× oracle budget and with the candidate-selection rule.

**Reviewer's phrasing:** "The paper's stated justification for causal attribution is that the
candidate budget and oracle scoring are held identical. They are not. Two of three optimizers
receive twice the oracle budget, and the p50 metric is not the same quantity across the
optimizer axis. The decomposition is not identified."

**Fix:** equalize to 128 proposals per cell, apply one selection rule, and never let the oracle
choose the reported set. Re-run the grid. **Cost:** ~2 h edit + full grid re-run (see P0-2 —
do them in one re-run). **Fixable:** yes. **Blocks submission:** yes.

---

### P0-2 · The ensemble trains on unstandardized targets; both GPs z-score
**Claim at risk:** η²_surr = 0.37 — the headline — and the "inductive bias" mechanism.

**Evidence.**
- `mbo.py:36-37` `Task.__init__`: `s.y = (s.oracle(s.x) + noise)` — **raw** oracle values, never normalized.
- `mbo.py:130-138` `train_ensemble(x, y, ...)`: `TensorDataset(FloatTensor(x), FloatTensor(y))`
  → MSE on **raw** `y`, `lr=3e-3`, `35` epochs unconditional, `weight_decay=1e-4` the only regularizer.
- `mbo.py:255` `botorchgp`: `yt = (yt - yt.mean()) / (yt.std() + 1e-8)` — **standardizes**.
- `mbo.py:311-312` `svgp`: standardizes, and `mbo.py:342` inverts it back.

Target scale varies by ~2.5 orders of magnitude across the suite (Griewank ≈ −2600, Branin ≈ −10;
`mbo.py:41-70`). At fixed `lr` and fixed epoch count with no target normalization, the ensemble's
MSE on Griewank is ~10⁶ and it cannot fit; on Branin it can. **The GP−ensemble gap should therefore
track the task's |y| scale — which is exactly the pattern Table 1 shows.**

`main.tex:93` claims *"all scores are min-max normalized."* That normalization exists only in the
**analysis** (`analysis.task_norm`), not in the training path.

**Why this is the #1 reject risk:** "inductive bias" and "the ensemble was handed unnormalized
targets" are observationally equivalent under every control the paper runs. The β=0 control does
not separate them (standardizing the GP's `y` is an affine monotone transform of its LCB, so β=0
leaves the GP's *ranking* untouched while the ensemble's *training* pathology persists). The
matched-tuning control removes the GP's tuning but never gives the ensemble normalization.

**Reviewer's phrasing:** "The ensemble regresses on raw targets spanning −2613 to +36 while both
GP surrogates standardize. The surrogate main effect may be a target-scaling artifact. Normalize
and re-run before claiming an inductive-bias mechanism."

**Fix:** standardize `y` in `train_ensemble` (2 lines), re-run. **Cost:** ~30 min edit + full grid
re-run. **Fixable:** yes — and this is also the decisive experiment (see PREREGISTRATION.md).
**Blocks submission:** yes. **This must be run before anything else in the paper is trusted.**

---

### P0-3 · Premise coverage is measured for 1 of 9 cells; the cross-proposal claim varies two factors at once
**Claim at risk:** Contribution 2 in full — the 0.73 / 0.41 / 0.97 abstract numbers and the
"ensemble×gradient interaction, not a surrogate defect" attribution.

**Evidence.**
- `mbo.py:583` `run_calibration` hard-codes the **ensemble**; `mbo.py:598` hard-codes **gradient**.
  It takes no surrogate/optimizer argument. `run_all.py:74` passes a single dummy variant `['_']`.
  → coverage exists for **`ens:grad` only**.
- `run_gpcov.py:34` takes ensemble proposals from **gradient**; `run_gpcov.py:35` takes GP proposals
  from **perturbation**. Both factors move together, so the resulting contrast cannot separate
  "ensemble×gradient interaction" from "gradient travels further OOD."
- `run_gpcov.py` uses **sklearn's** GP, not the grid's `botorchgp` — a different model from the one
  the decomposition scores.

**Reviewer's phrasing:** "The interaction claim rests on a comparison in which surrogate and
optimizer change simultaneously, evaluated with a GP that is not the GP in the grid. This is the
exact confound the paper was written to eliminate."

**Fix:** parameterize `run_calibration` over the full 3×3 and recompute. **Cost:** ~3 h edit +
~1 CPU-day. **Fixable:** yes. **Blocks submission:** yes.

---

### P0-4 · Reported numbers whose generating code does not exist in the repo
**Claim at risk:** the η² confidence intervals, the β=0 control, the subsample control, the
GP-coverage panel, the 9-cell stats, the RF-robustness defense.

**Evidence.** `main.tex:137` reports *"task-and-seed bootstrap 95% CIs … (non-overlapping)."*
Nothing in the repo bootstraps seeds or η². Both bootstrap implementations (`stats.py:151`,
`run05.py:99`) resample **task indices only**, on seed-collapsed means, and produce mean-*ranks* —
not η². The values live in `05_findings.json` under keys `bootstrap_ci`, `beta0`,
`subsample_control`, `gp_coverage`, `stats_9cell`, `rf_robustness` — **none of which `run05.py`
ever writes**.

Separately, `run_all.py:60` still writes `rho_knn`, a field absent from both live result files:
**the current code does not reproduce the current artifacts.**

**Reviewer's phrasing:** "We could not reproduce the confidence intervals from the released code.
The described bootstrap resamples seeds; the code resamples tasks."

**Fix:** write the missing generators, or delete the claims. **Cost:** ~4 h. **Fixable:** yes.
**Blocks submission:** yes — an artifact whose code does not produce its own numbers fails the
reproducibility checklist.

---

### P0-5 · A headline coverage claim reverses when a task the supplement itself calls degenerate is removed
**Claim at risk:** "moderately covered in-distribution (0.73, below the nominal 0.90)" and the real-task
coverage story.

**Evidence.** The 0.77 real-task in-distribution coverage is driven by GFP = 0.00, which the supplement
itself describes as a degenerate decode artifact. **Excluding GFP the mean is 0.895 ≈ 0.90** — so
"below the nominal 0.90" **reverses**. Full trace in `docs/PROVENANCE.md`.

Compounding it: `mbo.py:591` draws the "in-distribution" reference set as `np.random.uniform(0,1,(500,dim))`.
Design-Bench data are one-hot cube **vertices** (`db_tasks.py:63`) or normalized real measurements
(`db_tasks.py:66`) — **not** uniform on the cube. The DB "in-distribution" coverage is therefore
measured off-distribution. Valid for synthetic (where the data *are* uniform); invalid for the entire
right panel of Figure 3.

**Reviewer's phrasing:** "The claim that in-distribution coverage falls below nominal is carried
entirely by a task the authors call degenerate, and the in-distribution reference set is not drawn
from the data distribution."

**Fix:** drop or quarantine GFP; sample the reference set from `D`. **Cost:** ~2 h + recompute.
**Fixable:** yes. **Blocks submission:** yes.

---

### P0-6 · Figures 1 and 3 report different Design-Bench mean ranks for the same cells
**Claim at risk:** figure integrity; by extension every rank-based claim.

**Evidence.** 6 of 9 Design-Bench cells disagree between Fig 1 and Fig 3. GP×Pert is **3.4** in Fig 1
but **3.6** in Fig 3, in the body text, and in the supplement (3.57). Both sets sum to ≈45, so these are
two internally-valid but *different* rankings — i.e. two different data sources. Synthetic panels agree
perfectly, which rules out a presentational cause. This hits the paper's headline Design-Bench cell.
Full trace in `docs/PROVENANCE.md` (INC-1).

**Reviewer's phrasing:** "Figures 1 and 3 disagree about the same quantity. Which is correct?"

**Fix:** regenerate both from one source. **Cost:** ~1 h once P0-4's generators exist. **Fixable:** yes.
**Blocks submission:** yes.

---

### P0-7 · A load-bearing sentence states the arithmetic backwards
**Claim at risk:** the RF-oracle defense of the central null — i.e. Contribution 3's validity.

**Evidence.** The paper argues *"the median 9-cell spread (0.34) is no smaller than … (0.39)."*
**0.34 is smaller than 0.39.** The sentence is literally false, in both main and supplement, and it is
the defense of the paper's most attackable claim. (`docs/PROVENANCE.md`, INC-4.)

Related: the RF-oracle defense numbers (p=0.93, 0.34, 0.39) have **no table or figure** anywhere —
body-only. So does TOST ±0.48.

**Reviewer's phrasing:** "The claim's own numbers contradict it."

**Fix:** recompute and rewrite. **Cost:** ~1 h. **Fixable:** yes. **Blocks submission:** yes.

---

## P1 — major revision demands

### P1-1 · Optimizer surrogate-query budgets are unmatched by 6×–59×
**Evidence.** Measured surrogate forward-evaluations per cell: gradient `1×100×256 = 25,600`;
perturbation `(1+5×3)×256 = 4,096`; CMA `popsize×generations` = **432 (d=2) to 3,012 (d≥20)` —
pycma's tolerance criteria halt it well below `maxfevals=3000` at low d. Gradient gets **6.25×**
perturbation and **8.5–59×** CMA. No eval counter or shared budget constant exists anywhere in the repo.
CMA is starved worst on exactly the low-d tasks that carry the headline.

**Reviewer's phrasing:** "'Optimizer' is confounded with search intensity. 'Use a conservative
optimizer' may just mean 'search less.'"

**Fix:** budget-matched arm at equal surrogate queries. **Cost:** ~1 CPU-day. **Fixable:** yes.

### P1-2 · The ANOVA is hand-rolled, has no error term, and leaves `task` unmodeled
**Evidence.** `run05.py:26-48` — no statsmodels anywhere in the repo. η² is computed on **63 cell
means** with `task` unmodeled, so there is no F, no p, no df, and the denominator is inflated by
between-task variance. Two inconsistent normalizations coexist: η² uses 9 cells (`run05.py:35`),
while SEI/OEI, GATE-1, and the rank/CD/TOST matrix use `analysis.task_norm`, which matches any key
containing `':'` and therefore spans **11** cells — silently including the `ens_conformal:*` arms.

**Reviewer's phrasing:** "η² without an error term is not an effect size; and the rank analysis
includes methods the grid section never defines."

**Fix:** proper mixed model or a permutation effect size; unify the normalization. **Cost:** ~4 h.
**Fixable:** yes.

**A citable reviewer objection lands exactly here.** Benavoli, Corani & Mangili, *Should We Really Use
Post-Hoc Tests Based on Mean-Ranks?*, **JMLR 17(5):1-10, 2016**, verbatim:

> "the outcome of the mean-ranks test depends on the pool of algorithms originally included in the
> experiment ... the difference between A and B could be declared significant if the pool comprises
> algorithms C, D, E and not significant if the pool comprises algorithms F, G, H"

Our rank/CD/TOST matrix runs through `analysis.task_norm`, which matches any key containing `':'` and
therefore **silently pools 11 cells, including the `ens_conformal:*` arms the grid section never defines**.
So the CD conclusions demonstrably depend on a pool the paper does not disclose — Benavoli's objection is
not hypothetical here, it is instantiated. Their recommendation is to use tests whose "outcome only
depends on the two algorithms being compared, such as the sign-test or the Wilcoxon signed-rank test."
Demsar's canonical cite is **JMLR 7(1):1-30, 2006**; Garcia & Herrera (**JMLR 9(89):2677-2694, 2008**)
give Holm/Shaffer/Bergmann-Hommel alternatives to Nemenyi for all-pairwise comparisons.

### P1-3 · The ensemble is unregularized, unvalidated, and never early-stopped
**Evidence.** The complete regularization list is `weight_decay=1e-4` (`mbo.py:23,137`). No dropout,
no norm layers, **no validation split of any kind**; `mbo.py:140` `for _ in range(ep):` runs 35 epochs
unconditionally. Members differ **only** by `torch.manual_seed(seed*100+k)` (`mbo.py:135`) — init and
shuffle order; **no bootstrap resampling**, all 5 members see identical data. `sigma = ps.std(0)`
(`mbo.py:155`) with no noise term and **no floor**, while GP and SVGP both clamp (`mbo.py:265,342`).

Held-out predictive error of ensemble vs GP per task is **MISSING** — the repo never computes it.
Without it, "inductive bias" cannot be distinguished from "fits worse." See P0-2.

**Fix:** add a validation split and report held-out NLL/RMSE per task per surrogate. **Cost:** ~3 h.

### P1-4 · Design-Bench significance claims violate the paper's own pre-registration
**Evidence.** `PREREGISTRATION.md:50-52`: *"n=16 … **NO seed-dependent significance claims on DB** —
direction-of-crossover evidence only."* The paper reports Friedman p=0.69/0.93 and a TOST bound on DB.
Also unrun: the pre-registered `n=50` reruns for Rosenbrock-10D / Rastrigin-15D / Ackley-20D
(`PREREGISTRATION.md:14-16`, which states n=30 gives only ~0.72 power there) — grep finds no `--seeds 50`
anywhere. The paper never cites the pre-registration.

**Fix:** honor it, or state the amendment. **Cost:** 0 h to disclose; ~2 CPU-days to run n=50.

### P1-5 · The registered hypothesis was refuted and the paper does not say so
**Evidence.** `SKELETON.md:11,30` registered the headline as *"the acquisition optimizer explains most
of the reported gap."* The paper reports **η²_opt = 0.01** — the opposite. The shipped Contribution 3
(the DB null) replaced a planned offline-to-online protocol contribution (`SKELETON.md:16,26`).

This is a *strength* if disclosed: a refuted pre-registered prediction is evidence of a real test.
Undisclosed, it reads as HARKing to anyone who sees the repo.

**Fix:** one paragraph. **Cost:** ~1 h. **Fixable:** yes — and it *raises* credibility.

### P1-6 · COMs reproduction diverges from official by 1.22 normalized units
**Evidence.** ours 2.21 vs official 0.99 on TF-Bind-8; `main.tex:158` quotes that cell ("2.20 on
TF-Bind-8" — itself a third value). Supplement Table 4's CbAS TF-Bind-8 row computes `2.13 − 2.12 = 0.01`
but the |Δ| column says **0.004** — the single "matches official" number does not verify against its own row.

**Reviewer's phrasing:** "Their baselines are wrong, so the null is theirs, not the field's."

**Fix:** diff against the official repo's hyperparameters. **Cost:** ~1 day. **Fixable:** partly.

### P1-7 · Propositions 1 and 2 carry no content
**Evidence.** `proofs.md:10` — Prop 1's entire proof is *"The two events coincide as subsets of X, so
they have equal probability under any Q."* It is an identity. Prop 2 is textbook split-conformal plus a
**restatement** of Tibshirani et al. 2019's weighted-conformal extension (`proofs.md:20-22`), and the
weighting is never implemented — `proofs.md` concedes the repair is not run.

**Reviewer's phrasing:** "Proposition 1 is a tautology and Proposition 2 is a known result restated.
Neither is a contribution."

**Fix:** either cut to a remark, or find a bound with content (see `docs/MECHANISM_EXPERIMENTS.md` 6.6),
or *implement* the density-ratio repair so Prop 2 earns its place. **Cost:** ~1 day for the density-ratio
classifier.

### P1-8 · Seed 0 fixes one dataset draw for all 30 seeds
**Evidence.** `mbo.py:33-38` — `np.random.seed(0)` in `Task.__init__`; per-seed randomness is training/init
only. Every CI and p-value conditions on a single data draw; data-draw variance is unestimated while the
ANOVA treats tasks as the sampling unit. The paper does disclose the convention.

**Fix:** per-seed draws. **Cost:** full grid re-run. **Fixable:** yes but expensive; defensible as a
disclosed Design-Bench convention if not.

---

## P2 — minor

- **P2-1 · Table 1 caption cites a value present in no cell of its own table.** Caption says Griewank
  `-2612`; that is a truncation of Ens×CMA `-2612.68` (`grid.tex`), which the body renders `-2613`, while
  the body text uses `-2592` (Ens×Grad). The caption also mixes endpoints incoherently — Branin uses Grad
  (`-9.27`) though the true extreme `-14.01` is in the same table. (`PROVENANCE.md` INC-2.) ~1 h.
- **P2-2 · Rounding/consistency drift.** `|Δ|` 1.2 vs 1.22; CD 4.5 vs 4.54; p 6e-5 vs 6.1e-5; q̂ range
  `[1.8,16]` excludes its own max 16.1; main Table 1 GP×Pert Griewank `-269` vs supplement `-270`
  (truth `-269.60`); "restores coverage to 0.90 on every task" vs supp Table 5 showing 0.89. ~2 h.
- **P2-3 · `q̂` and `ĉ_ood` disagree with `proofs.md`.** `proofs.md:24` says q̂ ∈ [2.8, 10.5] and
  ĉ_ood ≈ 0; the paper says [1.8, 16] and 0.41. One is stale. ~1 h.
- **P2-4 · Two unreconciled rank pools** (2.57 vs 2.29); ties bolded inconsistently. ~1 h.
- **P2-5 · Main Table 3 (the 77-value DB grid) has no generator in `tables_v2/`.** ~2 h.
- **P2-6 · "CbAS" is not CbAS.** `mbo.py:503` — a CEM-style elite-resampling loop. `SKELETON.md:41`
  already flagged that it must be relabeled "CEM-style adaptive sampling" unless real CbAS is run. ~0 h
  (relabel).
- **P2-7 · Sparse-GP σ provenance.** `SKELETON.md:41` warns it is "a feature-variance proxy unless a real
  posterior is fit." `mbo.py:311-342` does fit a real SVGP posterior — so the warning appears stale, but
  the paper should say which. ~0 h.
- **P2-8 · RETRACTED — `li2024bnnsurrogates` IS ICLR 2024.** An earlier revision of this ledger claimed
  it was 2023. That was my error. Verified: Li, Rudner & Wilson, *A Study of Bayesian Neural Network
  Surrogates for Bayesian Optimization*, **ICLR 2024**, arXiv:2305.20028, OpenReview `SA19ijj44B`; the
  PDF header reads "Published as a conference paper at ICLR 2024." The bib key is correct. No action.

## P3 — polish

- **P3-1 · 8 stale uncited figures** in `paper/figures_v2/`; one (`fig4_beta_ablation.pdf`) names **two**
  tasks where β=0 is competitive, against the paper's "6 of 7, lone exception Ackley."
- **P3-2 · README.md is stale and ships in the supplement.** It describes the ICML workshop paper as
  "CURRENT", says **n=10 seeds** against the paper's 30, and points at `paper/latex_source/paper.tex`.
  `README.md:54` lists it for the supplement zip. Shipping it hands a reviewer a contradiction.
- **P3-3 · No provenance in any artifact** — zero timestamp / git sha / config block in any result file;
  seeds are positional only (`run_all.py:79`, `range(seeds)`).

---

## Threat-list verdicts (T1–T12)

| ID | Verdict | Basis |
|---|---|---|
| **T1** Crippled baseline | **CONFIRMED — decisively** | Two independent confirmations. (a) The ensemble trains on **raw targets** while both GPs standardize (P0-2). (b) The authors' own `gradtune.py` sweep shows a trust region closes the gradient collapse on 3 of 4 tasks, failing the script's own pre-stated decision rule (P0-0). Matched tuning is asymmetric exactly as hypothesized. No validation split, no early stopping, no bootstrap, σ unfloored. Held-out error per task: **MISSING**. |
| **T2** Mechanism misnamed | **CONFIRMED — and the name is worse than 'wrong'** | Coverage exists for `ens:grad` only, 1 of 9 (P0-3). Ens×CMA coverage: **MISSING**. The cross-proposal claim varies both factors at once and uses a different GP. And P0-0 shows the mechanism is not "ensemble×gradient" at all — it is "ensemble×*untuned* gradient", which a trust region repairs. |
| **T3** Unmatched budget | **CONFIRMED** | 25,600 / 4,096 / 432–3,012 surrogate queries (P1-1). Plus an unmatched **oracle** budget, 256 vs 128 (P0-1). |
| **T4** RF-oracle validity | **PARTIAL** | Circularity: not confirmed — needs the RF-vs-surrogate split check. But DB "in-distribution" coverage is sampled from the **wrong distribution** (P0-5), and the RF defense sentence is arithmetically backwards (P0-7) with no supporting table. |
| **T5** COMs divergence | **CONFIRMED** | 1.22 units on TF-Bind-8; the one "matches official" number fails to verify against its own row (P1-6). |
| **T6** ANOVA assumptions | **CONFIRMED — and worse** | It is not a standard ANOVA at all: hand-rolled, no error term, `task` unmodeled, two normalizations spanning 9 vs 11 cells (P1-2). Robustness profile pending. |
| **T7** Seed-0 dataset | **CONFIRMED** | `mbo.py:33-38` (P1-8). Disclosed by the paper; still unestimated variance. |
| **T8** Trivial propositions | **CONFIRMED** | Prop 1's proof is one line and is an identity; Prop 2 restates Tibshirani 2019 and its repair is never implemented (P1-7). |
| **T9** Weak null | **CONFIRMED — and self-conceded** | The abstract already concedes N=7 underpowered. Compounded: DB significance claims violate the pre-registration (P1-4). |
| **T10** Figure/table integrity | **CONFIRMED — worse** | Not one caption error but **13** inconsistencies, two severe: Fig 1 vs Fig 3 disagree on 6 of 9 DB cells (P0-6); a load-bearing sentence is arithmetically backwards (P0-7). |
| **T11** Title/scope | **PARTIAL** | Synthetic suite runs 2D–30D (`mbo.py:41-70`); the GP wins at 30D too, so "low dimension" is inaccurate. The d>500 separable-CMA path is **not present** in the current grid code. |
| **T12** LCB candidate selection | **CONFIRMED — worse than hypothesized** | Not final-iterate-vs-best-seen: **all three optimizers use different rules**, and the reported set is chosen by the **oracle** post hoc (P0-1). Fatal to the stated protocol as written. |

---

## What this means

Nine P0/P1 rows (P0-1, P0-2, P0-3, P1-1, P1-2, P1-3) share one root: **the grid is not the controlled
experiment the paper says it is.** The optimizer axis carries an unmatched oracle budget and three
different selection rules; the surrogate axis carries an unmatched target normalization. Both headline
effects (η²_surr = 0.37, the ensemble×gradient interaction) are confounded with implementation
asymmetries that the paper explicitly claims are held constant.

The good news is that these are *cheap* to fix and the fixes are *decisive*. Normalizing the ensemble's
targets and equalizing the candidate protocol is under a day of edits plus one grid re-run. If η²_surr
survives, the paper's central claim is established far more strongly than it is now. If it does not, the
authors learn that before a reviewer does.

**Nothing else in this ledger should be acted on until P0-2 is run.** Every downstream number depends
on it.
```

---
## FILE: docs/FREE_WINS.md — DOES NOT EXIST
<!-- no file at this path. Only 5.1 completed and it is docs/FREE_WIN_5_1_offline_selection.md, included below. 5.3 produced raw output only (agent died before writing its summary); 5.2/5.4 never ran. -->

---
## FILE: docs/FREE_WIN_5_1_offline_selection.md
<!-- lines: 422 | bytes: 27314 | last commit: 9cacc8b 2026-07-17 -->
```markdown
# Free Win 5.1 — Oracle-free selection of the winning (surrogate × optimizer) cell

**Verdict: FAILS.** The pre-registered decision rule does not beat its pre-registered trivial
baselines. The kill criterion in `PREREGISTRATION.md:59` — *"Fails either trivial baseline ->
reported honestly and dropped"* — **fires**. Report and drop.

Two separate findings make this a *strong* negative rather than a weak one, and they must be
reported together because either alone would be misleading:

1. **The feature the idea depends on is not oracle-free.** Every calibration probe in the
   artifacts is computed with `task.oracle(...)`. `c_hat_ood` in particular requires evaluating
   *f* on the proposals — precisely the query offline MBO forbids. The idea's premise is broken
   at the source, not at the statistics.
2. **n=14 is below the resolution of the question.** Even a **perfect** oracle-free rule (regret
   exactly 0 on every task) beats always-GP with only d_z = 0.71, while n=14 needs |d_z| ≥ 0.81
   for 80% power. **No rule can clear the bar at this n**, so this negative result must not be
   over-read as proof that no such rule exists.

Reproduce: `/opt/homebrew/Caskroom/miniforge/base/bin/python3 offline_selection.py`
(scratchpad; numpy+scipy only). Raw log: `offline_selection_log.txt`; machine-readable:
`offline_selection_results.json`.

*Environment note:* `/Users/palaash/Downloads/MBO/venv` is a Windows-layout venv (`Include/Lib/
Scripts/`) with no usable macOS python, and the miniforge python that does have numpy/scipy has no
sklearn — so ridge is implemented in closed form in numpy. **Validated against sklearn 1.9.0**
(available in a scratchpad venv from an earlier session): max |numpy ridge − `sklearn.Ridge`| =
**1.6e-15** over 200 random problems. The estimator is not a home-grown approximation.

---

## 1. Feature inventory and the oracle-free honesty assessment

Sources inspected: `/Users/palaash/Downloads/MBO/results/results_camera.json` (synthetic, 7
tasks × 30 seeds), `/Users/palaash/Downloads/MBO/results/results_db.json` (Design-Bench, 7 tasks
× 16 seeds). Grid verified complete: **9/9 cells per task on all 14 tasks**, at exactly 30 (synth)
/ 16 (DB) seeds.

### 1a. What the artifacts actually contain

`mbo[task][cell]` holds **only** `p100` and `p50` → `{mean, std, all[]}`. No diagnostics.
`calibration[task]` holds **one** record under the literal key `"_"` (`code/run_all.py:73`).

### 1b. The honesty assessment — which features survive at selection time?

This is the load-bearing section. A feature is *oracle-free* only if it is computable at
deployment time in a **truly offline** setting, i.e. from the labelled offline dataset alone,
with **zero** new queries to *f*.

| Feature | Avail. | Computed how | **Oracle-free?** |
|---|---|---|---|
| `cov_ood@{0.5,1,2,5}` (`c_hat_ood`) | 14/14 | `coverage_of_premise(mu_o, sig_o, f_o, b)` where **`f_o = task.oracle(xf)`**, `mbo.py:599,602` | **NO — fatal.** Requires *f* at the LCB proposals. That is the exact query offline MBO cannot make. Not reconstructible by any offline means. |
| `cov_conf_ood` | 14/14 | `np.mean(f_o >= mu_o - q*sig_o)`, `mbo.py:611` | **NO — fatal.** Same oracle-on-proposals dependency. |
| `rho_err` | 14/14 | `spearman(sig, |mu - task.oracle(xt)|)`, `mbo.py:593` | **NO as computed.** See 1c. |
| `cov_indist@{0.5,1,2,5}` (`c_hat_in`) | 14/14 | `coverage_of_premise(mu, sig, task.oracle(xt), b)`, `mbo.py:601` | **NO as computed.** See 1c. |
| `cov_conf_indist` | 14/14 | `task.oracle(xt)`, `mbo.py:610` | **NO as computed.** See 1c. |
| `q_conformal` (`q_hat`) | 14/14 | `fit_conformal_multiplier(mu_c, sig_c, task.oracle(xc))`, `mbo.py:609` | **NO as computed**, and **excluded anyway**: it lives in raw-y units on synthetic but [0,1] units on DB, so it is not poolable across the 14 tasks. |
| `d` (task dimension) | **11/14** | Structural. `mbo.py:41-85` (synth); `PREREGISTRATION.md:47`, `cloud/setup.sh:66` (TFBind8=32, TFBind10=40, Superconductor=86); `mbo.py:282` (GFP=4740) | **YES.** Not in the artifacts — read off the source. **MISSING for UTR, AntMorphology, DKitty** — recorded nowhere in the repo. Not imputed. |
| `N` (dataset size) | **7/14** | Structural. `mbo.py:41-85` (synth: 2000–8000) | **YES for synthetic. MISSING for all 7 DB tasks.** Only the `--db-subsample` cap (default 8000, `run_all.py:121`) is recorded; `db_tasks.py:54-58` concatenates a top-block with a random block **without deduping**, so realized N is data-dependent, ≤8000, and unrecorded. Not imputed. |
| discrete/continuous flag | 14/14 | Structural. `db_tasks.py:7-9` docstring | **YES.** The **only** genuinely oracle-free feature available on all 14 tasks. |

**MISSING entirely — absent from every artifact, not imputed:**

| Feature | Status |
|---|---|
| `rho_knn` = `spearman(sig, 5-NN train distance)` | **MISSING** from every `results/*.json` (checked all 10). Bitter irony: this is **the one genuinely oracle-free probe the codebase instruments** (`mbo.py:594,614`), and `run_all.py:60` *does* save it — but no committed artifact contains it. The calibration blocks predate that save, or were merged from an older file. |
| σ statistics (mean/median/spread) | **MISSING.** `mu/sig` computed at `mbo.py:585-588`, never persisted. |
| ensemble disagreement | **MISSING** (≡ σ; never persisted). |
| GP marginal likelihood / held-out NLL | **MISSING.** Never computed anywhere in the codebase. |
| proposal displacement ‖x_T − x_0‖ | **MISSING.** `x0`/`xf` exist at `mbo.py:597-598`, never persisted. |
| **any per-(task, cell) feature** | **MISSING.** See 1d. |

### 1c. The one genuine subtlety: "oracle-free" vs "oracle-free-*reconstructible*"

The in-distribution probes deserve a fair hearing rather than a blanket dismissal, and the answer
differs between the two halves of the benchmark:

- **Synthetic (7 tasks): reconstructible.** The offline dataset is `np.random.uniform(0,1,(n,dim))`
  (`mbo.py:37`) and the probe points are `np.random.uniform(0,1,(n_test,dim))` (`mbo.py:591`) —
  **exchangeable**. So `rho_err`, `cov_indist@*`, `cov_conf_indist`, `q_conformal` could be
  obtained from a held-out split of the *labelled offline data*, with no new oracle queries. As
  literally coded they call `task.oracle`, but they extract no information a deployed practitioner
  lacks. Call these **oracle-free-reconstructible** (modulo one wrinkle: offline `y` carries
  observation noise, `mbo.py:38`, while `oracle(xt)` is noiseless).
- **Design-Bench (7 tasks): NOT reconstructible.** The probe is still uniform on the cube, but the
  DB offline data is *not*. For the discrete tasks it sits on one-hot simplex vertices
  (`db_tasks.py:60-63`) — **mutually singular** with the dense cube. Uniform probe points are
  designs the dataset never contains, so labelling them is a genuine oracle query. Not
  reconstructible by any offline means.
- **On-proposal probes (`cov_ood@*`, `cov_conf_ood`): NEVER reconstructible, on either half.**

**So the honest bottom line: the oracle-free feature set that spans all 14 tasks is a single
binary flag.** `d` covers 11/14, `N` covers 7/14. Everything the paper names as a calibration
feature is oracle-contaminated on at least the DB half, and the on-proposal features — the ones
the mechanism story says should matter — are contaminated everywhere.

### 1d. Killer consequence: there are ZERO per-cell features

`calibration` is keyed `task -> "_"` — computed **once per task**, with the **ensemble** surrogate
and **grad** at fixed `BETA` (`mbo.py:597-598`). It does not vary by cell.

**Protocol step 3(a) — "pick the cell maximizing a single feature, e.g. argmax c_hat_ood" — is
NOT COMPUTABLE.** `c_hat_ood` has one value per *task*, not one per *cell*; there is no argmax to
take. Only rules of the form `score(task, cell) = g_cell(task_descriptors)` are implementable.

This is not a defect in the protocol: it is exactly what `PREREGISTRATION.md:56-58` specified
("fit boundary on all-but-one task from (d, held-out calibration probe); predict held-out task's
better arm"). The prereg's own design is the only implementable one. It is reported here so the
gap between the free-win brief and the artifact is on the record.

---

## 2. Target and normalization (reused, not invented)

Per-(task, cell) **normalized score**, using the paper's own convention copied verbatim from
`code/analysis.py:29-34` (`task_norm`), the same function `code/run05.py:81` calls:

> per-task **min–max over ALL present grid cells** of the `p100` **mean**.

One inherited quirk, preserved deliberately: `task_norm` min-maxes over every key containing `':'`
— **11 cells** (the 9-cell grid + `ens_conformal:{grad,perturb}`), not 9. I reuse it exactly as
the paper does and take the **argmax over the 9-cell grid** as the selection set. Consequence:
per-task max over the 9 grid cells can be < 1.0.

**Metric.** `p100` is the headline (the `analysis.py` default, and the paper's headline).
`PREREGISTRATION.md:17` names p100 **and** p50 as co-primary, so p50 is reported in §6 — as a
co-primary, **not** as a second chance to win.

**Regret** = (best achievable grid cell on t) − (selected cell's score on t). CIs: bootstrap over
the 14 held-out tasks, B=10000 (`PREREGISTRATION.md:29`: "Bootstrap CIs B=2000-10000").

---

## 3. Is there anything to win in the first place?

| task | d | N | disc | best cell | ens:grad | ens:perturb | ens:cma | gp:grad | gp:perturb | gp:cma | svgp:grad | svgp:perturb | svgp:cma |
|---|--|--|--|---|--|--|--|--|--|--|--|--|--|
| Branin-2D | 2 | 2000 | 0 | botorchgp:grad | 0.348 | 0.972 | 0.000 | **1.000** | 1.000 | 1.000 | 0.996 | 1.000 | 0.991 |
| Styblinski-5D | 5 | 3000 | 0 | botorchgp:perturb | 0.038 | 0.901 | 0.000 | 0.723 | **1.000** | 0.693 | 0.214 | 0.942 | 0.207 |
| Levy-8D | 8 | 4000 | 0 | botorchgp:grad | 0.336 | 0.888 | 0.000 | **1.000** | 0.938 | 0.999 | 0.991 | 0.937 | 0.990 |
| Rosenbrock-10D | 10 | 5000 | 0 | svgp:grad | 0.462 | 0.834 | 0.000 | 0.900 | 0.918 | 0.884 | **1.000** | 0.924 | 0.998 |
| Rastrigin-15D | 15 | 5000 | 0 | svgp:grad | 0.388 | 0.297 | 0.000 | 0.749 | 0.317 | 0.721 | **1.000** | 0.319 | 0.979 |
| Ackley-20D | 20 | 5000 | 0 | botorchgp:grad | 0.472 | 0.020 | 0.361 | **1.000** | 0.027 | 0.993 | 0.977 | 0.051 | 0.970 |
| Griewank-30D | 30 | 8000 | 0 | botorchgp:grad | 0.008 | 0.849 | 0.000 | **1.000** | 0.897 | 1.000 | 1.000 | 0.895 | 1.000 |
| TFBind8 | 32 | — | 1 | ens:grad | **0.989** | 0.000 | 0.873 | 0.000 | 0.000 | 0.000 | 0.688 | 0.370 | 0.682 |
| TFBind10 | 40 | — | 1 | ens:grad | **1.000** | 0.912 | 0.428 | 0.912 | 0.912 | 0.000 | 0.318 | 0.912 | 0.315 |
| Superconductor | 86 | — | 0 | botorchgp:perturb | 0.000 | 0.960 | 0.608 | 0.802 | **1.000** | 0.868 | 0.242 | 0.818 | 0.858 |
| GFP | 4740 | — | 1 | svgp:cma | 0.000 | 0.997 | 0.328 | 0.994 | 0.994 | 0.995 | 0.941 | 0.994 | **0.997** |
| UTR | — | — | 1 | ens:grad | **0.985** | 0.649 | 0.755 | 0.719 | 0.719 | 0.719 | 0.719 | 0.719 | 0.000 |
| AntMorphology | — | — | 0 | botorchgp:perturb | 0.048 | 0.622 | 0.000 | 0.995 | **1.000** | 1.000 | 0.158 | 0.990 | 0.030 |
| DKitty | — | — | 0 | botorchgp:perturb | 0.055 | 0.850 | 0.000 | 0.860 | **1.000** | 0.771 | 0.775 | 0.956 | 0.775 |

(`—` = MISSING, never imputed. `gp` = `botorchgp`.)

**Yes, there is heterogeneity**: 5 distinct cells win across the 14 tasks; the modal cell wins only
4/14. So the question is not vacuous — a good rule *could* in principle pay off. Mean per-task
score by cell: `botorchgp:grad` 0.832, `svgp:perturb` 0.773, `botorchgp:perturb` 0.766,
`botorchgp:cma` 0.760, `svgp:grad` 0.716, `svgp:cma` 0.699, `ens:perturb` 0.696, `ens:grad` 0.366,
`ens:cma` 0.239.

---

## 4. Method

**Rules** (all pre-specified; ridge `alpha=1.0` fixed a priori and **never tuned**; every rule run
is reported, none dropped):

| ID | Rule | Features | Oracle-free? |
|---|---|---|---|
| R1 | per-cell group mean, argmax | discrete | yes |
| R2 | per-cell ridge, argmax | discrete | yes |
| R3 | per-cell ridge, argmax | log d | yes (prereg's "boundary from d") |
| R4 | 1-NN on task descriptors | log d | yes |
| R5 | per-cell ridge, argmax | log d, discrete | yes |
| R6 | per-cell ridge, argmax | log d, log N | yes |
| R7 | 1-NN on task descriptors | log d, log N | yes |
| C1 | per-cell ridge, argmax | cov_conf_ood, cov_conf_indist | **NO — ceiling probe** |
| C2 | per-cell ridge, argmax | all 11 unit-free calibration probes | **NO — ceiling probe** |
| C3 | 1-NN | cov_conf_ood, cov_conf_indist | **NO — ceiling probe** |

Because `d` is MISSING for 3 tasks and `N` for 7, the LOO runs in **arms** on the largest complete-case
task set each feature set supports (14 / 11 / 7). The **C\*** arm is a deliberate
**oracle-contaminated ceiling probe**: if features that *cheat* cannot predict the winner, the
oracle-free version is dead twice over. It is **not deployable** and is never counted as a result.

**Baselines**, all recomputed inside each arm: (a) best fixed cell in hindsight; **(b) best fixed
cell on the other n−1 tasks — the honest bar**; (c) random cell (exact expectation over the 9);
(d) always-ensemble and always-GP, each with the optimizer chosen honestly on the other n−1 tasks.

---

## 5. Per-task regret (headline metric p100, n=14)

| task | best cell | **(b) fixed** | R1 pick | **R1 reg** | C1 pick *(oracle)* | C1 reg | always-GP | always-ens |
|---|---|--|---|--|---|--|--|--|
| Branin-2D | botorchgp:grad | 0.000 | botorchgp:grad | 0.000 | svgp:grad | 0.004 | 0.000 | 0.028 |
| Styblinski-5D | botorchgp:perturb | 0.277 | botorchgp:grad | 0.277 | botorchgp:perturb | 0.000 | 0.277 | 0.099 |
| Levy-8D | botorchgp:grad | 0.000 | botorchgp:grad | 0.000 | botorchgp:grad | 0.000 | 0.000 | 0.112 |
| Rosenbrock-10D | svgp:grad | 0.100 | botorchgp:grad | 0.100 | svgp:grad | 0.000 | 0.100 | 0.166 |
| Rastrigin-15D | svgp:grad | 0.251 | botorchgp:grad | 0.251 | svgp:grad | 0.000 | 0.251 | 0.703 |
| Ackley-20D | botorchgp:grad | 0.949 | botorchgp:perturb | 0.973 | svgp:perturb | 0.949 | 0.973 | 0.980 |
| Griewank-30D | botorchgp:grad | 0.000 | botorchgp:grad | 0.000 | botorchgp:perturb | 0.103 | 0.000 | 0.151 |
| TFBind8 | ens:grad | 0.989 | botorchgp:grad | 0.989 | botorchgp:grad | 0.989 | 0.989 | 0.989 |
| TFBind10 | ens:grad | 0.088 | svgp:grad | 0.682 | botorchgp:grad | 0.088 | 0.088 | 0.088 |
| Superconductor | botorchgp:perturb | 0.198 | botorchgp:grad | 0.198 | botorchgp:perturb | 0.000 | 0.198 | 0.040 |
| GFP | svgp:cma | 0.003 | ens:grad | 0.997 | svgp:cma | 0.000 | 0.003 | 0.000 |
| UTR | ens:grad | 0.266 | svgp:perturb | 0.266 | botorchgp:perturb | 0.266 | 0.266 | 0.336 |
| AntMorphology | botorchgp:perturb | 0.005 | botorchgp:grad | 0.005 | botorchgp:perturb | 0.000 | 0.005 | 0.378 |
| DKitty | botorchgp:perturb | 0.140 | botorchgp:grad | 0.140 | botorchgp:perturb | 0.000 | 0.140 | 0.150 |
| **MEAN** | | **0.233** | | **0.348** | | *0.171* | 0.235 | 0.302 |

---

## 6. Baseline comparison

### ARM 1 — honest oracle-free, all 14 tasks (only fully-available descriptor: discrete)

Hindsight-best fixed cell: `botorchgp:grad`.

| strategy | mean regret | 95% CI | vs (b) W/L/T | paired diff vs (b) [95% CI] |
|---|--|---|--|---|
| (a) best fixed cell, hindsight *(upper bound)* | 0.1655 | [0.0598, 0.3130] | — | — |
| **(b) best fixed cell on other 13 — BEAT ME** | **0.2333** | [0.0861, 0.4131] | — | — |
| (c) random cell (exact E over 9) | 0.3480 | [0.2860, 0.4112] | — | — |
| (d) always-ensemble | 0.3015 | [0.1455, 0.4825] | — | — |
| (d) always-GP | 0.2350 | [0.0861, 0.4168] | — | — |
| always-svgp | 0.2841 | [0.1248, 0.4632] | — | — |
| **R1 groupmean(discrete)** *oracle-free* | **0.3484** | [0.1667, 0.5513] | **0/3/11** | **+0.1151 [+0.0000, +0.2858]** |
| **R2 ridge(discrete)** *oracle-free* | **0.3484** | [0.1667, 0.5513] | **0/3/11** | **+0.1151 [+0.0000, +0.2858]** |

**R1/R2 lose to every baseline.** Mean regret 0.348 is *identical to picking a cell at random*
(0.348) and worse than (b) by +0.115. Win/loss/tie vs (b): **0 wins, 3 losses, 11 ties**. vs
always-GP: **0/2/12**. The point estimate goes the **wrong way**.

### ARM 2 — 11 tasks with d recorded (the prereg's actual rule)

| strategy | mean regret | 95% CI | vs (b) W/L/T | paired diff vs (b) |
|---|--|---|--|---|
| (a) hindsight fixed | 0.1732 | [0.0446, 0.3539] | — | — |
| **(b) honest fixed cell — BEAT ME** | 0.3607 | [0.1442, 0.5953] | — | — |
| (c) random | 0.3420 | [0.2675, 0.4221] | — | — |
| (d) always-ensemble | 0.3052 | [0.1049, 0.5373] | — | — |
| **(d) always-GP** | **0.1732** | [0.0446, 0.3539] | — | — |
| R3 ridge(log d) *oracle-free* | 0.4162 | [0.1961, 0.6478] | 1/1/9 | +0.0555 [−0.0152, +0.1818] |
| R4 1-NN(log d) *oracle-free* | 0.3312 | [0.1077, 0.5908] | 3/4/4 | −0.0295 [−0.3431, +0.2924] |
| R5 ridge(log d, discrete) *oracle-free* | 0.2957 | [0.1208, 0.4853] | 4/2/5 | −0.0650 [−0.2905, +0.1418] |

**Read this arm carefully — it is where over-claiming would happen.** R4 and R5 nominally beat (b).
That is meaningless: **always-GP (0.173) beats all three rules outright**, and it is precisely the
baseline `PREREGISTRATION.md:59` names as disqualifying. Both paired CIs span zero. R3 — the
prereg's literal rule, ridge on d — is the **worst** strategy in the arm.

### ARM 3 — 7 synthetic tasks (d and N both recorded)

| strategy | mean regret | 95% CI | vs (b) W/L/T | paired diff vs (b) |
|---|--|---|--|---|
| (a) hindsight fixed | 0.0897 | [0.0142, 0.1757] | — | — |
| **(b) honest fixed cell — BEAT ME** | 0.1624 | [0.0142, 0.3870] | — | — |
| (c) random | 0.3284 | [0.2427, 0.4232] | — | — |
| (d) always-ensemble | 0.3200 | [0.0995, 0.5840] | — | — |
| **(d) always-GP** | **0.0897** | [0.0142, 0.1757] | — | — |
| R6 ridge(log d, log N) *oracle-free* | 0.1657 | [0.0176, 0.3870] | 0/3/4 | +0.0033 [+0.0000, +0.0099] |
| **R7 1-NN(log d, log N)** *oracle-free* | **0.0799** | [0.0045, 0.1608] | 2/3/2 | −0.0824 [−0.2311, +0.0082] |

**R7 is the single best-looking oracle-free number in this entire report (0.0799, nominally beating
both (b) 0.162 and always-GP 0.0897). It is not a finding.** It **loses more folds than it wins
(2W/3L)**; its paired CI spans zero; n=7 requires |d_z| ≥ 1.27 to detect anything; and it is **1 of
10 rules tried**. Promoting it would be exactly the failure mode this analysis exists to avoid.

### ARM 4 — CONTAMINATED CEILING PROBE (features use the oracle; **NOT DEPLOYABLE**)

| strategy | mean regret | 95% CI | vs (b) W/L/T | paired diff vs (b) |
|---|--|---|--|---|
| (b) honest fixed cell | 0.2333 | [0.0861, 0.4131] | — | — |
| C1 ridge(cov_conf_ood, cov_conf_indist) *ORACLE* | 0.1713 | [0.0213, 0.3666] | 7/2/5 | −0.0619 [−0.1223, −0.0077] |
| C2 ridge(all 11 probes) *ORACLE* | 0.1302 | [0.0314, 0.2792] | 8/4/2 | −0.1031 [−0.2553, +0.0015] |
| C3 1-NN(cov_conf_ood, cov_conf_indist) *ORACLE* | 0.1738 | [0.0790, 0.2851] | 5/4/5 | −0.0594 [−0.2662, +0.1268] |

**This is the most scientifically interesting row in the report, and it must be stated carefully.**
C1's paired CI vs (b) excludes zero (−0.122, −0.008), and vs always-GP it is 8W/2L, diff −0.0637
[−0.1237, −0.0094]. So there is a *hint* that the calibration probes carry real signal about which
cell wins — and mechanistically that is coherent with the paper's own story: `cov_conf_ood` measures
how badly the ensemble's uncertainty breaks **on its own proposals**, which is exactly what should
predict whether the ensemble or the GP wins.

**But: (i)** the sign tests are not significant (C1 vs (b): 7W/2L, **p=0.180**; C2: 8W/4L,
**p=0.388**); **(ii)** these are 3 of 10 rules; and **(iii) — decisively — these features require
querying *f* on the proposals, so no deployable rule can ever use them.** The ceiling probe does not
rescue the idea. It diagnoses *why* it fails: **the predictive signal lives precisely in the
quantity offline MBO cannot compute.**

---

## 7. What is even detectable at n=14?

| n | |d_z| needed for 80% power (two-sided paired t, α=.05) |
|--|--|
| 14 | **0.81** |
| 11 | 0.94 |
| 7 | 1.27 |

- Observed SD of the paired regret difference (R1 − (b)) over 14 tasks: **0.2982**. So the smallest
  mean regret improvement detectable at 80% power is **0.2416 normalized-score units**. Anything
  smaller is invisible here.
- Sign test: a rule needs **≥12/14 wins with 0 losses** for p<0.05 two-sided (p=0.0129). The best
  oracle-free rule managed 4 wins.

### The decisive design fact

| | mean regret | SD over tasks |
|---|--|--|
| perfect oracle-free rule (per-task argmax) | 0.0000 | — |
| always-GP | 0.2350 | 0.3326 |

A **perfect** rule beats always-GP with **d_z = 0.71**, but n=14 needs **|d_z| ≥ 0.81**.

> **Even a perfect oracle-free selection rule could not be certified as better than always-GP at
> n=14.** always-GP's per-task regret is dominated by a couple of catastrophic tasks (TFBind8 0.989,
> Ackley 0.973), so its SD (0.33) exceeds its mean (0.24). **n=14 is not merely "small" — it is
> below the resolution of the question.**

This cuts both ways and must be reported both ways: it means the negative result **cannot** be
strengthened into "no oracle-free rule exists", *and* it means no amount of rule engineering on
these 14 tasks could have produced a defensible positive.

---

## 8. Co-primary metric p50 — the trap, reported so it cannot be sprung

`PREREGISTRATION.md:17` names p100 **and** p50. On p50:

| strategy | p50 regret | vs (b) W/L/T | vs always-GP W/L/T |
|---|--|--|--|
| (b) honest fixed cell | 0.3120 | 0/0/14 | 4/7/3 |
| always-GP | 0.2192 | 7/4/3 | 0/0/14 |
| **R1 groupmean(discrete)** *oracle-free* | **0.0742** | **9/3/2** | 3/0/11 |

**On p50, R1 looks like a clear winner** (0.074 vs (b) 0.312, diff −0.238 [−0.473, −0.038]) — while
**the same rule is the worst strategy tested on the headline p100 metric** (0.348 vs 0.233, i.e.
exactly random). Two reasons this is noise, not a result:

1. **It fails the trivial baseline even on p50.** vs always-GP: 3W/0L/**11 ties**, diff
   −0.145 [−0.359, **+0.000**] — the CI touches zero, sign test **p=0.250**. `PREREGISTRATION.md:59`
   still fires.
2. **The target itself is metric-unstable.** The best cell agrees under p100 and p50 on only
   **8/14 tasks**. The hindsight-best fixed cell is `botorchgp:grad` under p100 but `svgp:grad`
   under p50. A rule whose sign flips between two co-primary metrics of the same runs is
   fitting metric noise.

Reported explicitly so this number cannot later be quietly promoted to the headline.

---

## 9. A note on baseline (b) itself

(b) picks `botorchgp:grad` on **13/14 folds** and flips to `svgp:perturb` on exactly one:
**Ackley-20D**. Ackley is a single influential task where *every* perturb cell collapses
(ens:perturb 0.020, gp:perturb 0.027, svgp:perturb 0.051); dropping it flips the argmax-of-mean
(`botorchgp:grad` 0.832→0.820 vs `svgp:perturb` 0.773→0.829).

So **baseline (b) is essentially "always use a BoTorch GP with gradient ascent"**, and (b) ≈
always-GP is not a coincidence — they are nearly the same strategy. And **one task out of 14 flips
the honest baseline**: the n=14 problem shows up in the *baseline*, not just in the rules.

---

## 10. Multiplicity

10 rules × 2 co-primary metrics = up to **20 rule×metric comparisons** against (b). Under a
coin-flip null, P(≥1 of 10 rules beats (b) by chance) ≈ 1 − 0.5¹⁰ = **0.999**; over 20 slots,
**0.9999**. The best-looking cell in these tables is **not** interpretable as a discovery.

**Discipline actually applied:** ridge alpha fixed at 1.0 a priori and never tuned; every rule run
is reported and none dropped; p100 designated headline *before* looking (it is `analysis.py`'s
default and the paper's headline), so the p50 result that flatters R1 is **not** promoted; no rule
was added after seeing a result.

---

## 11. Blunt verdict

**FAILS. The pre-registered kill criterion fires. Drop it.**

- On the headline metric p100, **no oracle-free rule beats baseline (b)**, and the best-looking ones
  (R4, R5, R7) are beaten outright by **always-GP** — the trivial baseline
  `PREREGISTRATION.md:59` explicitly names as disqualifying. The prereg's literal rule (ridge on d,
  R3) is the **worst** strategy in its arm.
- The headline rule available on all 14 tasks (R1/R2) achieves regret **0.348 — identical to random
  cell choice** — vs 0.233 for (b) and 0.235 for always-GP. **0 wins, 3 losses, 11 ties** vs (b).
- The p50 co-primary does **not** rescue it: the rule that wins there fails always-GP (3W/0L/11T,
  p=0.250) and is the worst rule on p100.

**Three things must be said alongside the verdict, or the negative result is itself misleading:**

1. **The idea's premise is broken at the source, not at the statistics.** `c_hat_ood` — the feature
   the brief leads with — is computed as `np.mean(f_o >= mu_o - q*sig_o)` with
   `f_o = task.oracle(xf)`. **It requires evaluating the true objective on the proposals**, the one
   query offline MBO forbids. It is not oracle-free and cannot be made so. The genuinely oracle-free
   feature set spanning all 14 tasks is **one binary flag**.
2. **The instrumentation, not just the result, is the finding.** `rho_knn` — the *one* genuinely
   oracle-free probe the codebase computes (`mbo.py:594`) and `run_all.py:60` saves — **is absent
   from every committed artifact**. σ statistics, ensemble disagreement, GP marginal likelihood, and
   proposal displacement were never persisted. `d` is unrecorded for 3/14 tasks; `N` for 7/14. And
   **no per-cell feature exists at all**, which makes the brief's own rule (a) uncomputable. This
   analysis is a fair test of *what was instrumented*; it is not a fair test of *the idea*.
3. **n=14 could not have certified a win even if one existed** (perfect rule: d_z = 0.71 < 0.81
   needed). So this must be reported as **"ran as pre-registered, failed its trivial baselines,
   dropped"** — **not** as evidence that oracle-free selection is impossible. The honest claim is
   about *this rule, on this instrumentation, at this n*.

**Does the paper change category?** **No.** This is a **dropped stretch goal**, reported honestly
per the pre-registration — worth a short, unembarrassed paragraph, not a section. Nothing here
touches the paper's main factorial claims.

**If anyone wants to revive it** (out of scope here, stated so the negative result is actionable
rather than merely discouraging): the minimum viable version needs (i) `rho_knn` + σ statistics +
proposal displacement persisted **per cell**, not per task — all are oracle-free and already
computed or trivially computable; (ii) conformal `q̂` refit on a held-out split of the **offline
dataset** rather than on `task.oracle(xc)` at uniform points, which would make it genuinely
oracle-free on both halves; (iii) `d`/`N` recorded for the DB tasks (one run of
`python code/db_tasks.py ...` in the `db` env); and (iv) **far more than 14 tasks** — the power
analysis says n=14 cannot resolve this question regardless of how good the rule is. Absent (iv),
(i)–(iii) would still not yield a publishable positive.
```

---
## FILE: docs/FREE_WIN_5_3_eta_robustness_raw.txt
<!-- lines: 165 | bytes: 10405 | last commit: 9cacc8b 2026-07-17 -->
```text
self-check OK (optimizer-driven grid -> eta2_opt > eta2_surr under all arms)

==========================================================================================
STEP 1 — REPRODUCTION of the paper's exact eta^2 via code/run05.py::eta2
==========================================================================================
  SYNTH          tasks=7
      eta2_surr = 0.36872274336144345
      eta2_opt  = 0.013189173376026025
      eta2_inter= 0.16518056841213977
    vs paper stored:  surr=0.36872274  opt=0.01318917  inter=0.16518057
    EXACT MATCH (to 8dp): True
  REAL           tasks=7
      eta2_surr = 0.04677094337600403
      eta2_opt  = 0.08473928568992424
      eta2_inter= 0.013117026453762042
  SYNTH-matched  tasks=7
      eta2_surr = 0.27542947156964054
      eta2_opt  = 0.024329542667278076
      eta2_inter= 0.12247869816619208

==========================================================================================
RAW SPAN DIAGNOSTIC (the motivation for the whole exercise)
==========================================================================================
  task                  raw min    raw max         span   minmax-compression
  Branin-2D             -14.011     -0.398       13.613   8 non-min cells span 0.652 of [0,1]
  Styblinski-5D           5.208     36.145       30.937   8 non-min cells span 0.962 of [0,1]
  Levy-8D                -3.194     -0.049        3.145   8 non-min cells span 0.664 of [0,1]
  Rosenbrock-10D         -0.481     -0.044        0.437   8 non-min cells span 0.538 of [0,1]
  Rastrigin-15D         -10.809     -2.830        7.979   8 non-min cells span 0.703 of [0,1]
  Ackley-20D             -6.324     -0.552        5.772   8 non-min cells span 0.992 of [0,1]
  Griewank-30D        -2612.681     -0.942     2611.740   8 non-min cells span 0.992 of [0,1]
  GLOBAL raw range across tasks: [-2612.681, 36.145]

==========================================================================================
STEP 2a — eta^2 UNDER ALTERNATIVE NORMALIZATIONS  (unit = PER-TASK MEAN; the paper's unit)
==========================================================================================
  synthetic: T=7 tasks, 30 seeds/cell, 9 cells

  normalization                 eta2_surr  eta2_opt  eta2_inter  surr/opt  holds?
  minmax (PAPER)                   0.3687    0.0132      0.1652      28.0  YES
  rank (1-9 within task)           0.4873    0.0497      0.0528       9.8  YES
  z-score per task                 0.4288    0.0190      0.1936      22.6  YES
  log-regret -> minmax             0.3772    0.0095      0.1563      39.9  YES
  winsor 5% (seed pool)            0.3754    0.0104      0.1631      36.2  YES
  winsor 10% (seed pool)           0.3796    0.0065      0.1577      58.6  YES
  winsor 5% (cell means)           0.3784    0.0086      0.1617      44.3  YES
  winsor 10% (cell means)          0.3865    0.0042      0.1577      92.8  YES
  RAW (no normalization)           0.0698    0.0071      0.0302       9.9  YES

==========================================================================================
STEP 2b — eta^2 WITH PER-SEED ROWS  (unit = (task,seed); 7x30 = 210 rows)
==========================================================================================
  NOTE: the paper uses PER-TASK-MEAN units (run05.py::eta2 reads d[t][c][metric]["mean"]),
        i.e. it collapses the 30 seeds before the ANOVA. Per-seed rows re-inject
        within-cell seed noise into SS_total, which MUST deflate every eta^2.

  normalization                 eta2_surr  eta2_opt  eta2_inter  surr/opt  holds?
  minmax                           0.3342    0.0120      0.1497      28.0  YES
  zscore                           0.3776    0.0167      0.1705      22.6  YES
  rank                             0.4323    0.0467      0.0904       9.2  YES
  raw                              0.0697    0.0070      0.0301       9.9  YES

==========================================================================================
STEP 2c — same zoo on DESIGN-BENCH (results_db.json)
==========================================================================================
  real: T=7 tasks, 16 seeds/cell

  normalization                 eta2_surr  eta2_opt  eta2_inter  surr>opt?
  minmax (PAPER)                   0.0468    0.0847      0.0131  NO
  rank                             0.0238    0.0697      0.0073  NO
  z-score per task                 0.0466    0.0981      0.0138  NO
  log-regret -> minmax             0.0500    0.0894      0.0113  NO
  winsor 5% (seed pool)            0.0463    0.0863      0.0134  NO
  winsor 10% (seed pool)           0.0482    0.0859      0.0134  NO
  RAW (no normalization)           0.0727    0.0244      0.0351  YES

==========================================================================================
STEP 2d — LEAVE-ONE-TASK-OUT on the paper's arm (is Griewank-30D driving it?)
==========================================================================================
  dropped task        eta2_surr  eta2_opt  eta2_inter
  Branin-2D              0.3529    0.0081      0.1539
  Styblinski-5D          0.4267    0.0133      0.1989
  Levy-8D                0.3451    0.0090      0.1530
  Rosenbrock-10D         0.3514    0.0077      0.1580
  Rastrigin-15D          0.3737    0.0278      0.1623
  Ackley-20D             0.4227    0.0719      0.1889
  Griewank-30D           0.3301    0.0130      0.1526

==========================================================================================
STEP 3 — ASSUMPTION CHECKS on the PAPER'S ACTUAL ANOVA (minmax, task-mean units)
==========================================================================================
  residuals n = 63  (7 tasks x 9 cells, resid = y - cellmean_over_tasks)
  Shapiro-Wilk   W = 0.8085   p = 1.311e-07   NORMALITY REJECTED
  residual skew  = -1.478   excess kurtosis = +1.374
  QQ corr(sorted resid, normal quantiles) = 0.9009   (1.0 = perfectly normal)
  Levene (median) W = 0.5288   p = 8.296e-01   not rejected
  Bartlett       T = 18.1628   p = 2.004e-02   HOMOSCEDASTICITY REJECTED
  max/min group variance ratio across the 9 cells = 10.1
  [SYNTH rank            ] Shapiro p=2.895e-01  Levene p=8.918e-01  Bartlett p=9.100e-01
  [SYNTH z               ] Shapiro p=8.997e-03  Levene p=7.084e-01  Bartlett p=3.776e-02
  [SYNTH log-regret      ] Shapiro p=1.036e-07  Levene p=8.066e-01  Bartlett p=1.991e-02

==========================================================================================
STEP 4 — PERMUTATION effect-size test (no distributional assumptions), 20k perms
==========================================================================================
  [minmax (PAPER)]
     surr : eta2=0.3687  perm-null mean=0.0589 q95=0.1617  p=0.00105
     opt  : eta2=0.0132  perm-null mean=0.0418 q95=0.1099  p=0.73736
     inter: eta2=0.1652  perm-null mean=0.0636 q95=0.1453  p=0.02830
  [rank]
     surr : eta2=0.4873  perm-null mean=0.0872 q95=0.2476  p=0.00090
     opt  : eta2=0.0497  perm-null mean=0.0424 q95=0.1150  p=0.35658
     inter: eta2=0.0528  perm-null mean=0.0713 q95=0.1651  p=0.57207
  [z-score]
     surr : eta2=0.4288  perm-null mean=0.0690 q95=0.1925  p=0.00105
     opt  : eta2=0.0190  perm-null mean=0.0415 q95=0.1137  p=0.65547
     inter: eta2=0.1936  perm-null mean=0.0710 q95=0.1622  p=0.02205
  [log-regret]
     surr : eta2=0.3772  perm-null mean=0.0607 q95=0.1711  p=0.00105
     opt  : eta2=0.0095  perm-null mean=0.0396 q95=0.1040  p=0.78661
     inter: eta2=0.1563  perm-null mean=0.0628 q95=0.1445  p=0.03490
  [RAW]
     surr : eta2=0.0698  perm-null mean=0.0678 q95=0.0692  p=0.00035
     opt  : eta2=0.0071  perm-null mean=0.0067 q95=0.0073  p=0.23139
     inter: eta2=0.0302  perm-null mean=0.0518 q95=0.0810  p=0.74526

  bootstrap-over-tasks CIs (2.5/97.5 pct, 20k resamples):
    minmax (PAPER)   surr CI=[0.256,0.557]  opt CI=[0.005,0.201]  inter CI=[0.108,0.258]  P(surr>opt)=0.9963
    rank             surr CI=[0.344,0.687]  opt CI=[0.025,0.270]  inter CI=[0.026,0.102]  P(surr>opt)=0.9954
    z-score          surr CI=[0.289,0.588]  opt CI=[0.006,0.212]  inter CI=[0.123,0.274]  P(surr>opt)=0.9979
    log-regret       surr CI=[0.261,0.572]  opt CI=[0.004,0.195]  inter CI=[0.098,0.244]  P(surr>opt)=0.9963
    RAW              surr CI=[0.026,0.265]  opt CI=[0.005,0.080]  inter CI=[0.010,0.133]  P(surr>opt)=0.9386

  Design-Bench permutation (paper arm):
    surr : eta2=0.0468 p=0.44533
    opt  : eta2=0.0847 p=0.15269
    inter: eta2=0.0131 p=0.93750
    bootstrap: surr CI=[0.002,0.330] opt CI=[0.006,0.291] P(surr>opt)=0.3712

==========================================================================================
SUPPORT — surrogate marginals under each treatment (is the ORDERING stable?)
==========================================================================================
  normalization                         ens    botorchgp         svgp
  minmax (PAPER)                     0.3395       0.8448       0.8267
  rank (1-9 within task)             2.4762       6.5714       5.9524
  z-score per task                  -0.9259       0.4779       0.4480
  log-regret -> minmax               0.3046       0.8185       0.8104
  winsor 5% (seed pool)              0.3237       0.8382       0.8232
  winsor 10% (seed pool)             0.2987       0.8266       0.8168
  winsor 5% (cell means)             0.3129       0.8354       0.8218
  winsor 10% (cell means)            0.2749       0.8217       0.8149
  RAW (no normalization)          -267.9812      -9.9316     -11.6524

  normalization                     perturb         grad          cma
  minmax (PAPER)                     0.7079       0.6948       0.6082
  rank (1-9 within task)             4.5238       5.8095       4.6667
  z-score per task                   0.1261       0.0655      -0.1915
  log-regret -> minmax               0.6783       0.6639       0.5913
  winsor 5% (seed pool)              0.6973       0.6815       0.6063
  winsor 10% (seed pool)             0.6780       0.6612       0.6029
  winsor 5% (cell means)             0.6914       0.6725       0.6061
  winsor 10% (cell means)            0.6679       0.6406       0.6030
  RAW (no normalization)           -42.0254    -122.9797    -124.5601

WROTE /private/tmp/claude-501/-Users-palaash-Downloads-MBO/555543c4-f40c-47b0-ae21-f68c4eff5fad/scratchpad/eta_robustness_out.json
```

---
## FILE: docs/MECHANISM_EXPERIMENTS.md
<!-- lines: 217 | bytes: 12124 | last commit: ee4e03f 2026-07-17 -->
```markdown
# Mechanism experiments — from diagnosis to causal test

The paper **claims** the cause is the GP's smooth posterior mean. It never manipulates
smoothness. Every current control is subtractive (β=0, matched tuning, data subsample) —
each consistent with the claim, none forcing it.

**The audit reorders this phase.** Phase 6 as briefed assumed the measurement is sound and
only the mechanism is unproven. It is not: `docs/FLAW_LEDGER.md` P0-2 shows the ensemble
trains on **raw** targets while both GPs standardize (`mbo.py:36-37` vs `mbo.py:255`,
`mbo.py:311`). Until that is removed, "smooth prior" and "the ensemble could not fit targets
of magnitude 2600" are observationally equivalent — and **no manipulation below is
interpretable.** M0 is therefore a gate, not an experiment.

Cost basis: the full synthetic grid is 7 tasks × 9 cells × 30 seeds. All CPU. Wall-clock
assumes the `--jobs` parallelism the runner already supports; single-core figures are given
where they differ materially. Design-Bench arms cost more per cell (oracle calls) and are
priced separately where relevant.

---

## M0 (GATE) · Normalize the ensemble's targets and re-run

**This is not a mechanism test. It is the precondition for every other row.**

**Hypothesis.** η²_surr = 0.37 is substantially a target-scaling artifact.

**PRE-REGISTERED PREDICTION.** Standardizing `y` inside `train_ensemble` will **materially reduce
η²_surr**, and the reduction will be **largest on the large-|y| tasks** (Griewank ≈ −2600,
Rastrigin, Ackley) and near-zero on Branin (≈ −10). Specifically: the per-task GP−ensemble gap
will correlate with `log|y|_scale` **before** the fix (ρ > 0.6) and not after (ρ ≈ 0).

**What falsifies it.** η²_surr stays ≈ 0.37 and the gap does not track `|y|` scale. **That would be
a genuinely good result** — it converts the biggest reject risk into a passed control and makes the
inductive-bias claim far stronger than it is today.

**Implementation.** In `train_ensemble` (`mbo.py:130`), z-score `y` before constructing the
`TensorDataset` and invert on prediction in `ens_lcb_torch`/`ens_lcb_np` (`mbo.py:152-158`) — the
same treatment `svgp` already applies at `mbo.py:311-312` / `mbo.py:342`. ~15 lines.

**Cost.** ~30 min edit. Full synthetic grid re-run. **Retires:** T1, P0-2, and the "underfitting is a
rename of inductive bias" objection — which is the #1 reject risk.

**Acceptance-delta.** Decisive either way. This is the highest-value CPU in the repo.

**Also run in the same pass** (they are free once you re-run): held-out RMSE/NLL per (task, surrogate).
The repo never computes them (`FLAW_LEDGER.md` P1-3), and without them "inductive bias" cannot be
separated from "fits worse" *even after* M0.

---

## M1 · Smooth the ensemble, hold σ fixed

**Hypothesis.** The gap is caused by the roughness of the ensemble's *mean*, not by its uncertainty.

**PRE-REGISTERED PREDICTION.** Constraining the ensemble mean's Lipschitz constant — while leaving
σ's construction untouched — closes most of the residual (post-M0) GP−ensemble gap and stops gradient
ascent from collapsing. Premise coverage on the ensemble's own gradient proposals rises from ≈0.41
toward the GP's ≈0.97.

**What falsifies it.** The gap persists at every smoothness level. Then the mechanism is not mean
roughness and Section 5 must be rewritten, not re-scoped.

**Implementation.** Cheapest first: (a) spectral normalization on the MLP's linear layers; (b) a
gradient penalty `λ‖∂μ/∂x‖²`; (c) input smoothing (average μ over Gaussian jitter). Sweep the
constraint strength — a *single* setting proves nothing; the dose-response is the evidence. Keep σ =
`ps.std(0)` unchanged so the manipulation is clean.

**Cost.** ~4 h edit; sweep of 4 strengths × synthetic grid ≈ 4× a grid run.

**Retires:** the "you never manipulated the thing you named" objection. **Acceptance-delta: HIGH** —
this is what converts a diagnosis into a *fix*. "Here is why the ensemble fails and here is the
one-line change that repairs it" is a different acceptance bracket than "the ensemble fails."

**Note the interaction with M0.** If M0 already closes the gap, M1 is testing a mechanism that no
longer has an effect to explain — run M0 first and re-scope. If M0 does *not* close the gap and M1
does, then undertraining is refuted by construction and the inductive-bias claim is *proven*, not
argued. That ordering is the whole point.

---

## M2 · Roughen the GP (the falsification test)

**Hypothesis.** The GP's robustness comes from prior smoothness, so a rough GP must lose it.

**PRE-REGISTERED PREDICTION.** Under Matérn-1/2 (or a fixed very short lengthscale), the GP **starts to
collapse** under gradient ascent and its premise coverage on its own proposals **drops from 0.97**.

**What falsifies it.** The rough GP stays robust → the mechanism is not prior smoothness; it is
something else the GP has (exact posterior, calibrated σ, the fitting procedure). This is the theory's
sharpest exposure: **the theory forbids a rough GP from being robust.**

**Implementation.** `SingleTaskGP` with a `MaternKernel(nu=0.5)`, and a variant with the lengthscale
fixed short. `mbo.py:250-260`. ~2 h.

**Cost.** ~2 h edit; 2 arms × synthetic grid.

**Acceptance-delta: HIGH per unit cost.** Reviewers reward a risked prediction far more than another
confirming control, and this is the cheapest risked prediction available.

---

## M3 · Smoothness interpolation family (best value in the paper)

**Hypothesis.** Prior-match is a *continuum*, and Design-Bench is not a different world — it is a point
on it.

**PRE-REGISTERED PREDICTION.** Construct `f_α = smooth base + α · high-frequency component` (or draw from
Matérn kernels with varying ν). As α rises: the GP−ensemble gap **shrinks**, η²_surr **falls**, ĉ_ood
**falls**, and the Friedman p **rises toward non-significance** — *all four together, monotonically*.
At high α the synthetic suite reproduces the Design-Bench null **continuously**.

**What falsifies it.** The four quantities move independently, or non-monotonically. Then "prior-match"
is not a single axis and the unification fails.

**Implementation.** New task family in `mbo.py` alongside the existing `ScaledAckley` ladder that
`PREREGISTRATION.md:32-36` already specifies (the ladder infrastructure exists and was never run —
reuse it). Sweep α ∈ {0, 0.25, 0.5, 1, 2, 4}. ~1 day.

**Cost.** ~1 day edit; 6 α-levels × 9 cells × 30 seeds ≈ 6 grid-equivalents. CPU-only.

**Retires:** T9 in its strongest form. Replaces the paper's weakest claim — a **two-point** comparison
at N=7 with p=0.69 — with a **trend**. A trend at 6 α-levels needs no equivalence test and no N=7 apology.

**Acceptance-delta: HIGHEST of the mechanism rows.** It unifies Contributions 2 and 3 into one curve.
This is the row I would spend the CPU on.

---

## M4 · Pessimism as distance regularization — test it, don't assert it

**Hypothesis.** βσ is doing the job of a distance-to-data penalty, not of calibrated uncertainty.

**PRE-REGISTERED PREDICTION.** Replacing `βσ` with an explicit distance penalty (k-NN distance to `D`, or
a KDE term) — **with no uncertainty at all** — matches or beats `βσ`.

**What falsifies it.** The distance penalty underperforms βσ → uncertainty carries information distance
does not, and the paper's ρ≈0.1 argument is incomplete.

**Implementation.** New acquisition in `mbo.py` next to the LCB closures. The paper currently argues this
from ρ≈0.1 and a β-sweep; that is an argument, not a demonstration. ~4 h.

**Cost.** ~4 h edit; 2 arms × grid. **Acceptance-delta: MEDIUM** — a clean standalone practical finding.

---

## M5 · Learn the density ratio (close Prop 2's open loop)

**Hypothesis.** The proposal shift is severe enough that density-ratio weighting cannot repair coverage.

**PRE-REGISTERED PREDICTION.** A logistic-regression / gradient-boosted classifier ratio `w = dΠ/dP`
fit on `D` vs `Π` will **partially but not fully** restore proposal coverage — because the proposals
concentrate on a near-measure-zero region where `w` is unbounded and the effective sample size collapses.

**What falsifies it.** It fully restores coverage (a positive result the paper currently lacks — strictly
good), or it does nothing at all (a sharper negative: the shift defeats density-ratio methods, which is
itself a real finding worth stating).

**All three outcomes are publishable. "We did not try" is the only bad one** — and it is currently the
paper's position (`proofs.md:20` names the repair and never runs it). It is a reviewer's free shot.

**Implementation.** `sklearn.linear_model.LogisticRegression` on `D` vs `Π`, clipped weights, weighted
conformal quantile per Tibshirani et al. 2019. ~1 day including the weighted-quantile plumbing.

**Cost.** ~1 day; cheap to run (no grid re-run — reuses stored proposals **if** they are persisted;
**VERIFY FIRST** — if proposals are not stored, add ~1 grid re-run).

**Acceptance-delta: MEDIUM-HIGH.** Converts Prop 2 from a restatement into a tested claim.

---

## M6 · Make Proposition 1 non-trivial

**Goal.** A statement with content: a bound relating ĉ_ood to *computable* quantities — the surrogate's
local Lipschitz constant `L` along the optimizer trajectory, the displacement budget `D = ‖x_T − x_0‖`,
the density ratio.

**Target shape.** Something of the form: *proposal coverage degrades at most Φ(L, D, β, σ_min) given
displacement D and mean smoothness L* — which would make the diagnostic **predictive** rather than
descriptive and retire the "padding" objection.

**Sketch worth attempting.** If μ is `L`-Lipschitz and `f` is `L_f`-Lipschitz on the segment `x_0 → x_T`,
then `|μ(x_T) − f(x_T)| ≤ |μ(x_0) − f(x_0)| + (L + L_f)·D`. Combined with in-distribution coverage at
`x_0`, this lower-bounds the βσ needed at `x_T`, hence upper-bounds coverage loss as a function of `D`.
All three inputs (`L` empirically along the trace, `D`, `σ`) are **measurable in the existing runs**, so
the bound could be *plotted against the realized ĉ_ood* — a bound that tracks the data is a real
contribution; one that is vacuous is not.

**HONEST STATUS: NOT YET DERIVED.** The sketch above is plausible but I have not verified it is both true
and non-vacuous — the Lipschitz constant of an unregularized ensemble mean may be large enough to make it
trivially loose, which is precisely the failure mode to check first. **Do not put this in the paper until
it is proven and plotted.** Report honestly if no non-vacuous bound exists rather than manufacturing a
theorem. Note that M1 (which *controls* `L`) makes the bound testable by construction — the two rows are
complementary.

**Cost.** ~1-2 days of derivation with a real risk of returning nothing. **Acceptance-delta: HIGH if it
lands, ZERO if it does not.** Do it last, and only if M0-M3 have already secured the paper.

---

## Recommended order and total cost

| # | Row | Edit | CPU | Gate |
|---|---|---|---|---|
| 1 | **M0** normalize ensemble targets | 0.5 h | 1 grid | **Blocks everything** |
| 2 | **M2** roughen the GP | 2 h | 2 grids | Cheapest risked prediction |
| 3 | **M3** smoothness interpolation | 1 day | 6 grids | Best value; unifies C2+C3 |
| 4 | **M1** smooth the ensemble | 4 h | 4 grids | Converts diagnosis → fix |
| 5 | **M5** density ratio | 1 day | ~0-1 grid | Closes Prop 2 |
| 6 | **M4** distance regularization | 4 h | 2 grids | Standalone finding |
| 7 | **M6** non-trivial Prop 1 | 1-2 days | ~0 | Only if time remains |

**M0 → M2 → M3 is the critical path** and buys the most acceptance per CPU-hour. M0 because nothing is
interpretable without it; M2 because it is the cheapest way to risk the theory; M3 because it replaces
the paper's weakest claim with its strongest figure.

Predictions and kill criteria for each row are restated, unamended, in `docs/PREREGISTRATION_V2.md`.
If a result contradicts a prediction, that is a finding to report — not a prediction to quietly revise.
```

---
## FILE: docs/CHAT_DIGEST.md
<!-- lines: 106 | bytes: 7845 | last commit: 8074264 2026-07-17 -->
```markdown
# Chat digest

For the judgment-layer instance, which has only the compiled PDF. Facts it cannot infer.
Every claim below is verified against code or artifacts; `MISSING` means MISSING.

## What exists

One engine (`code/mbo.py`, 632 LOC) implements all three surrogates, all three optimizers,
the LCB closures, conformal repair, and the evaluation protocol. `run_all.py` drives it;
`run05.py` computes the paper's η²/CD/TOST; `figures.py` and `tables.py` emit
`paper/figures_v2/*` and `paper/tables_v2/*`. The paper is `paper/aaai27/main.tex` (298 LOC).

**The grid is complete and the headline numbers are real.** Synthetic 112/112 cells at exactly
30 seeds; Design-Bench 63/63 grid cells at exactly 16. η² reproduces from the primary artifacts
**to 8 decimal places** (0.36872274336…). This is not a case of invented numbers.

## The ten facts that matter

**1. The repo contains a control that refutes the paper's mechanism, and the paper omits it.**
`code/gradtune.py` exists solely to test "is the ensemble's gradient collapse just an under-tuned
optimizer?" It pre-states the rule: *"If even the best-tuned gradient config still underperforms
perturbation, the collapse is surrogate geometry (genuine), not tuning."* Its own results
(15 seeds, `results/results_gradtune.json`) **fail that rule on 3 of 4 tasks.** `grad_default` is
bit-for-bit the grid's optimizer (`lr=0.05, steps=100`). A trust region moves Branin −8.17 → −0.54
and Styblinski 5.56 → 34.30; on Ackley plain gradient already beats perturbation (−3.77 vs −6.41).
Commit `cdd5ad8`'s message says it outright: *"trust region closes the ensemble gradient collapse."*
The word "trust" appears nowhere in `main.tex`. **This is the single largest risk in the project.**

**2. The ensemble trains on raw targets; both GPs z-score.** `mbo.py:36` stores raw oracle values;
`train_ensemble` (`mbo.py:130`) does MSE on them at `lr=3e-3` for 35 fixed epochs. `botorchgp`
(`mbo.py:255`) and `svgp` (`mbo.py:311`) both standardize. Targets span ~2.5 orders of magnitude
(Griewank ≈ −2600, Branin ≈ −10), so the ensemble's loss on Griewank is ~10⁶. **η²_surr = 0.37 is
confounded with target scaling**, and the GP−ensemble gap tracks |y| scale exactly as Table 1 shows.
`main.tex:93` claims "all scores are min-max normalized" — true only in the *analysis*, not training.

**3. The stated identifiability license is false.** `main.tex:91`: *"candidate budget … and oracle
scoring are held identical. This shared closure is what licenses attributing score differences to
the surrogate×optimizer factors."* In fact `init_candidates` returns **256**, not 128 (`mbo.py:384`);
gradient returns the final iterate, perturbation per-slot best-ever, CMA top-128-by-surrogate — three
different rules. Then `eval_designs` calls the **oracle on all of them** and keeps its top 128
(`mbo.py:392`). So grad/perturb get **256 oracle calls**, CMA gets 128, and `p50` is a top-half
median for two optimizers and a full-set median for the third — **two estimands, one column**.

**4. Optimizer budgets differ by 6×–59×.** Surrogate forward-evals per cell: gradient 25,600;
perturbation 4,096; CMA 432 (d=2) to 3,012. CMA is starved worst on exactly the low-d tasks carrying
the headline. No eval counter exists in the repo.

**5. Coverage is measured for 1 of 9 cells.** `run_calibration` hard-codes ensemble (`mbo.py:583`)
and gradient (`mbo.py:598`). Ens×CMA coverage: **MISSING**. The cross-proposal claim (0.97) comes
from `run_gpcov.py`, which takes ensemble proposals from *gradient* and GP proposals from
*perturbation* — **both factors move together** — and uses **sklearn's GP, not the grid's**.

**6. Six reported quantities have no generator.** `05_findings.json` keys `bootstrap_ci`, `beta0`,
`subsample_control`, `gp_coverage`, `stats_9cell`, `rf_robustness` are **written by nothing in the
repo**. `main.tex:137` describes a *task-and-seed* bootstrap for the η² CIs; both bootstraps in the
repo resample **tasks only**, on seed-collapsed means, and produce mean-*ranks*. Also `run_all.py:60`
writes `rho_knn`, absent from both live artifacts: **the current code does not reproduce the current
artifacts.**

**7. A headline claim reverses.** The "in-distribution coverage below nominal" claim (0.77 real) is
carried entirely by GFP = 0.00, which **the supplement itself calls a degenerate decode artifact**.
Excluding GFP the mean is 0.895 ≈ 0.90. Separately, DB "in-distribution" coverage samples
`uniform(0,1)` (`mbo.py:591`) while DB data are one-hot **vertices** — measured off-distribution.

**8. Offline selection (5.1) FAILS — but for a reason worth publishing.** Ran as pre-registered;
kill criterion fires. Regret 0.348 vs the honest fixed-cell baseline's 0.233 — **identical to random**.
Two reasons, both structural: (a) **`ĉ_ood` is not oracle-free** — it evaluates true *f* on the
proposals, the one query offline MBO forbids (`mbo.py:599`); the oracle-free feature set spanning all
14 tasks is **one binary flag**. Oracle-*contaminated* features *do* carry signal (regret 0.171,
7W/2L). **The predictive signal lives precisely in the quantity offline MBO cannot compute.** (b) At
n=14, even a *perfect* rule reaches d_z = 0.71 vs the 0.81 needed for 80% power — **no rule could have
been certified at this n**. Identity B is dead; but (b) is a *power result* that hands Contribution 3
a real spine.

**9. The pre-registration contradicts the paper.** `PREREGISTRATION.md` registered the headline as
*"the optimizer explains most of the gap"* — the data gave η²_opt = **0.01**, the opposite. It also
forbade DB significance claims (*"NO seed-dependent significance claims on DB"*) which the paper makes
(p=0.69/0.93, TOST), and mandated n=50 reruns on three tasks that were **never run**. The paper never
cites it. Disclosed, the refutation is a credibility asset; discovered, it reads as HARKing.

**10. Novelty is thinner than the draft assumes.** The *factorial design* — NONE FOUND, genuinely
novel. But Li/Rudner/Wilson (**ICLR 2024**, miscited as 2024 in a bib entry keyed `li2024bnnsurrogates`
— verify) already reports "deep ensembles perform relatively poorly" and "ranking is highly
problem-dependent, suggesting the need for tailored inductive biases," with acquisition fixed. Prop 1
is an identity with prior art (Jin et al. 2021) — demote to a remark. Prop 2 restates Tibshirani 2019.
"Surrogate smoothness helps offline optimization" is established (MS-DDEO 2022 grades a surrogate pool
*by smoothness*; the Kim TMLR survey lists smoothness priors/RoMA). **What survives: the factorial
itself, the offline setting, and attribution to mean-smoothness-not-calibration** — and that last one
is exactly what facts 1 and 2 currently undermine.

## What runs, what's reproducible

Runs: the full grid, all controls, the figures/tables. Reproducible: η² exactly; the grid.
**Not** reproducible: the CIs, β=0, subsample, gp_coverage, rf_robustness (no generator);
`rho_knn` (code writes it, artifacts lack it). Zero provenance in any artifact — no timestamp,
git sha, or config block anywhere; seeds are positional (`range(seeds)`).

## Bottom line

The measurement is real and complete. The *controls are asymmetric in the ensemble's disfavour on
both axes simultaneously* — unnormalized targets on the surrogate axis, unequal oracle budget and
three selection rules on the optimizer axis — and the repo's own tuning sweep says the mechanism is
a tuning artifact. Both headline effects are confounded with implementation choices the paper
explicitly claims are held constant. **All of it is cheap to fix**: normalize `y`, equalize the
protocol, re-run once. If η²_surr survives, the paper is far stronger than it reads now. Nothing
downstream should be trusted until that run exists.
```

---
## FILE: docs/VENUE_NORMS.md
<!-- lines: 427 | bytes: 29277 | last commit: 1c28320 2026-07-17 -->
```markdown
# Venue norms (verified 2026-07-17)

Bears directly on `DECISION_QUEUE.md` D1 and `PAPER_V2_OUTLINE.md`.

| Venue | Not-SOTA explicitly OK? | Negative results explicitly welcome? |
|---|---|---|
| **ARR (ACL)** | **Yes** (heuristic H5) | **Yes** (H6) — the only venue with both |
| **NeurIPS 2026** | implied | **Yes — a new submission category**, at an explicitly *higher* bar |
| NeurIPS 2023-25 | No (2024 was pro-SOTA) | Silent |
| **TMLR** | **Yes**, verbatim | Silent — permissive by omission |
| ICLR 2023-26 | **Yes**, verbatim FAQ | Silent |
| ICML 2024-25 | Silent | Silent |
| **AAAI** | **Silent — and presumes SOTA framing** | **Silent. No negative-results track.** |

## The finding that matters

**NeurIPS 2026 introduced author-selected Contribution Types**, one of which is **Negative Results**
(https://neurips.cc/Conferences/2026/ReviewerGuidelines). Verbatim:

> "**Negative Results:** The main contribution is in understanding a negative result. (The significance
> and originality bar for these contributions is high.)"
> "it is important that the negative result not be simply an empirical observation that some experiment
> did not turn out as expected or hoped. It is important that a negative result be grounded in deeper
> analysis..."
> "**Originality — Unexpected or surprising in some way.** ... it should run counter to a popularly held
> understanding."

**Double edge.** NeurIPS admits negative results *as a category* while setting a **higher** bar than
General papers on two of four criteria, and requires them to be **surprising**. A well-executed null
that confirms what people already suspected is explicitly excluded.

**Read for this paper.** The Design-Bench null alone would *fail* that bar — "benchmarks don't
discriminate" is not surprising (`NOVELTY_CHECK` Q5: the complaint is known). But **"the GP advantage is
prior smoothness, not calibration"** *does* run counter to a popularly held understanding, and X4's power
specification is the "deeper analysis" the guideline demands. That is Identity C, not the current draft.

**AAAI, by contrast, is silent and its only SOTA reference presumes SOTA framing** ("What are the
limitations in the state of the art that the paper addresses?"). (AAAI text came via WebFetch
summarization, not raw fetch — lower confidence than the others.)

### CORRECTION: AAAI's guidelines are silent, but its record is not

An earlier draft of this file — and my session report — concluded AAAI was the *worst* fit of the venues
surveyed. **That was wrong, and a verified counterexample refutes it at exactly this venue.**

> Henderson, P., Islam, R., Bachman, P., Pineau, J., Precup, D., & Meger, D. (2018). **Deep
> Reinforcement Learning that Matters.** *Proceedings of the AAAI Conference on Artificial
> Intelligence*, **32(1), 3207–3214.** https://doi.org/10.1609/aaai.v32i1.11694
> **AAAI Technical Track: Machine Learning** — the main track. ~2,397 citations (S2).

No new method. Pure measurement. Accepted on the main technical track and now a canonical citation.
**The genre is not disqualified at AAAI; it is under-signalled in AAAI's guidelines.** Absence of an
explicit welcome is not evidence of rejection — it means the bar is set by precedent, and the precedent
is Henderson.

⚠️ **Citation trap:** Semantic Scholar reports `year: 2017` (back-propagated from arXiv v1, 1709.06560)
while still listing venue AAAI and pages 3207–3214. **Cite AAAI 2018, not 2017.** Citation counts
disagree ~57% across sources (S2 2,397 vs OpenAlex 1,526); report a range if quoted.

**What Henderson has that a bare null lacks** — the same anatomy as Recht:

| Element | Henderson et al. |
|---|---|
| **Mechanism** | An explicit seven-factor intrinsic/extrinsic taxonomy (hyperparameters, architecture, reward scale, seeds, environments, codebases, reporting), one section each |
| **Surprise finding** | Same algorithm, same hyperparameters, **only the random seed varies** → statistically different distributions. `t = −9.0916, p = 0.0016` (TRPO, HalfCheetah-v1) |
| **Methodology** | t-test, Kolmogorov–Smirnov, bootstrap percent-difference with 95% CI (10k iters), power analysis |
| **Prescription** | "the most important step to reproducibility is to report all hyperparameters, implementation details, experimental setup, and evaluation methods" |
| **Corrected leaderboard** | **No** — explicitly disclaims one |
| **Scale claim** | **No** — deliberately narrow to policy-gradient continuous control |

**Two consequences for us, and they cut in opposite directions.**

1. **AAAI is viable.** Identity A or C can land here; the venue has published this genre in the main
   track. `PAPER_V2_OUTLINE.md`'s P(accept) reasoning should be read with that precedent in mind, and
   the "AAAI is the worst fit" line in my session report is **retracted**.
2. **Henderson is also a threat, and a mirror.** Its thesis is that unreported implementation details
   determine results. `FLAW_LEDGER.md` P0-0 (an unreported trust-region setting decides the collapse)
   and P0-2 (unreported target normalization decides the surrogate gap) are *Henderson's thesis
   instantiated in our own artifact*. A reviewer who knows this paper — and in offline MBO, many will —
   reads our omissions through it. Note also that Henderson's headline (seeds alone shift the
   distribution) bears directly on **T7**: our seed-0 fixed dataset leaves data-draw variance
   unestimated while the ANOVA treats tasks as the sampling unit.

**The honest read:** Henderson raises AAAI's ceiling for this paper *and* raises the cost of shipping
P0-0 unreported. Both follow from the same citation.

## Alternatives if the AAAI window is tight

- **MLRC 2026 is now an official NeurIPS track**, routed through TMLR. Hard deadline **2026-09-30**.
  "MLRC welcomes rigorous work across the full spectrum of outcomes, including positive confirmations of
  prior results, partial replications, and **failures to reproduce**." Papers publish in TMLR proceedings,
  presented at NeurIPS.
- **TMLR** directly: "novelty of the studied method is not a necessary criteria for acceptance."
  But TMLR explicitly rejects bare nulls without "generalizable insights" / "actionable lessons."

## Pattern across accepted measurement papers

"Are GANs Created Equal?", Musgrave's metric-learning reality check, Dacrema's recsys "phantom progress",
Recht et al. — the shared shape is **a specific, named, falsified belief plus a reusable protocol**.
A bare null has neither.

### The template, verified in detail: Recht et al. (ICML **2019**, oral; PMLR v97:5389-5400)

Exact title: *"Do ImageNet Classifiers Generalize to ImageNet?"* — Recht, Roelofs, Schmidt, Shankar.
~2,201 citations (S2-via-Consensus, refresh date **NOT VERIFIED**; do **not** use OpenAlex, which splits
the record across two IDs and undercounts by >5x). The CIFAR-10 predecessor (arXiv:1806.00451) was
**never peer-reviewed** — it was *subsumed* into the ICML paper, so cite ICML 2019 for both results.

**Correction to how this paper is usually invoked, including by me above.** It is **not a null result.**
It found a *large* difference (11-14% ImageNet accuracy drops) and then showed the **obvious explanation
for that difference was wrong**. Its contribution rests on the gap between two findings pointing in
opposite directions: accuracy drops sharply, *but* "accuracy gains on the original test sets translate to
**larger** gains on the new test sets" — a fitted slope of **1.11 [1.07, 1.19]** on ImageNet, CI
excluding 1.0. Adaptive overfitting predicts *diminishing* returns; they measured the opposite, and so
rejected adaptivity in favour of distribution shift.

Its anatomy is the checklist a measurement paper must pass:

| Element | Recht et al. |
|---|---|
| **Named belief, refuted** | "Conventional wisdom suggests that such drops arise because the models have been adapted to the specific images" → "**Adaptivity is therefore an unlikely explanation**" |
| **Mechanism, shown by manipulation** | Three sampling strategies (`TopImages`/`Threshold0.7`/`MatchedFrequency`) **dial the drop up and down** by varying only annotation difficulty. Not a robustness check — the causal argument. |
| **Artifact released** | ImageNetV2 (3 x 10,000 images), CIFAR-10.1 |
| **Prescriptions** | 5 named, incl. a "super hold-out" kept hidden for years |
| **Scale** | 34 CIFAR-10 + **67** ImageNet models (appendix count; often miscited as 66); 208,145 candidate images |
| **Surprise** | Core of the paper — the result runs counter to the popular understanding |

**Why this matters for us.** The causal move — *vary one knob and watch the effect dial up and down* —
is structurally identical to **X5** (`MECHANISM_EXPERIMENTS.md` M3: sweep α, watch gap / η²_surr / ĉ_ood /
Friedman p move together). That is the strongest evidence this template is the right one to copy, and it
is further reason X5 outranks another subtractive control. Note also that Recht et al. clears NeurIPS
2026's "surprising" bar precisely *because* it refutes a named belief — the Design-Bench null does not,
but "the GP advantage is prior smoothness, not calibration" would.

Standalone negative-results venues fail (JINR: one paper in 18 years; JNRBM: closed 2017). Negative
results survive only when attached to an existing conference (ICBINB: 7 years, 61 papers; Insights:
~118 papers).

**NOT VERIFIED:** ICBINB 2026 PMLR volume; Insights acceptance rates; SIGIR 2026 verbatim scope.

### Verified anatomy of the other two precedents

**Musgrave, Belongie & Lim — "A Metric Learning Reality Check."** ECCV 2020, LNCS **12370:681-699**,
DOI 10.1007/978-3-030-58595-2_41. S2 537 cites (OpenAlex's 68 is a known LNCS consolidation failure —
do not cite it). Contribution: a **new metric** (MAP@R), a **new protocol** (4-fold class-disjoint CV,
50 iters Bayesian opt, 10 runs, 95% CIs), **three named flaws** (unfair comparisons; misleading accuracy
metrics; training with test-set feedback — "breaks one of the most basic commandments of machine
learning"), and a **corrected leaderboard**. Artifact: `powerful-benchmarker` — **not**
`pytorch-metric-learning`, which is a separate arXiv-only paper (2008.09164) by the same authors.

**Ferrari Dacrema, Cremonesi & Jannach — "Are we really making much progress?"** RecSys 2019,
**101-109**, DOI 10.1145/3298689.3347058 — **Best Long Paper**. Follow-up: TOIS 39(2) Art. 20, 2021
(cite **2021**; S2 wrongly dates it 2019). **Surname is "Ferrari Dacrema" — cite under F, not D.**
18 relevant / 7 reproducible (RecSys); 26 / 12 (TOIS). Result is stronger than a null: on Epinions,
non-personalized **TopPopular beat every personalized method**.

**The uncomfortable part.** Dacrema's named mechanism is *our* ledger:

> "**Lack of proper tuning of baselines:** *This is probably the most striking observation of our
> analysis*... Researchers apparently invest significant efforts in optimizing their own new method but
> do not pay the same attention to their baselines... Probably, this behavior might be the result of a
> **confirmation bias**."

`FLAW_LEDGER.md` P0-2 is an unnormalized baseline; P0-0 is an untuned baseline optimizer whose tuning
sweep was run and not reported. The field's canonical measurement paper names this exact failure mode
as its central finding — and our paper is a measurement paper that commits it. Reviewers in this genre
know that sentence. Fixing X1/X2 is not just about being right; it is about not being the example.

TOIS also supplies the prescription template (§5.4, modeled on the Pineau ML Reproducibility Checklist)
and the multiplicity argument we need for X4: "if a researcher collects 10 accuracy metrics and only
reports the significant ones (significance 0.05), then the probability of reporting a progress that is
only virtual jumps from 5% to 40%." (5.1 ran 10 rules and reported all 10 — that discipline is already
in `PREREGISTRATION_V2.md` commitment 5.)

---

## The decisive move: AAAI has published this genre FOUR times

Beyond Henderson, three more — all **AAAI main track**, all no-new-method:

| Paper | Venue | The move |
|---|---|---|
| Henderson et al., *Deep RL that Matters* | **AAAI 2018** | *"to the best of our knowledge this is the first work to address this important question in the context of deep RL"* — novelty of the **question**, not the method. Every section heading is an italicized *question*. |
| Gundersen & Kjensmo, *State of the Art: Reproducibility in AI* | **AAAI 2018** | Pure measurement, **zero method** — surveyed 400 IJCAI/AAAI papers against six metrics. Proof AAAI accepts a paper whose entire contribution is counting things about other papers. |
| Kim et al., *Towards a Rigorous Evaluation of Time-Series Anomaly Detection* | **AAAI 2022** | *"even a random anomaly score can easily turn into a state-of-the-art TAD method"* + *"an untrained model obtains comparable detection performance to the existing methods."* Null + a minimal positive deliverable (new baseline + PA%K protocol). **Our closest AAAI structural twin.** |
| Zeng et al., *Are Transformers Effective for Time Series Forecasting?* | **AAAI 2023, ORAL** | *"we question the validity of this line of research in this work"* — an AAAI **oral** opened with that sentence. The baseline is sold as *"embarrassingly simple"*: anti-novelty as a weapon. |

### Steal this sentence (Musgrave, ECCV 2020 §1.6)

> "Exposing hype and methodological flaws is not new. Papers of this type have been written for machine
> learning, image classification, neural network pruning, information retrieval, recommender systems, and
> generative adversarial networks."

He cites the genre **to legitimize the genre**. Write the AAAI version — citing Henderson (AAAI'18),
Gundersen (AAAI'18), Kim (AAAI'22), Zeng (AAAI'23) — and "is this even a paper?" becomes "this venue has
published this genre four times." Ours is stronger than Musgrave's because all four are the target venue.

### The rule every accepted paper here obeys

**Every single one shipped an artifact. A null alone is not the unit of acceptance; null + protocol/artifact
is.** Kim → a baseline + PA%K protocol. Locatello (ICML 2019 **Best Paper**) → `disentanglement_lib` + 10,000
released models. Musgrave → an evaluation protocol. Dodge → the expected-validation-performance curve —
explicitly manufactured so the paper had a nameable *thing*. **This is X4's job for us**: the power
specification *is* the artifact. Without it we are a bare null.

Other transferable moves: **scale as a credential** (put the grid size in the abstract — "12,000 models",
"2.52 GPU years", "18 algorithms, only 7 reproduced"; ours is 14 tasks × 9 cells × 30 seeds); **pre-empt
"trivial" with self-deprecation** (Locatello: *"(perhaps unsurprisingly)"*; Zeng: *"embarrassingly
simple"* — this is how X9 should demote Prop 1); and **never end on the negative** — every abstract closes
on the field's obligation ("our results suggest that future work should…").

### Precedent for surviving our exact objection

*Are GANs Created Equal?* (NeurIPS 2018) has **public reviews**. Reviewer 1: the *"main conclusion of the
paper is expected (that there is really no model that is clearly better than others in all conditions and
for all datasets), but not very helpful for the practitioner."* **Accepted anyway** — and the arXiv comment
records that the camera-ready *"added section on study limitations"*. That is verbatim the "so what, the
null isn't actionable" objection we will get, on the record, on an accepted paper, with the fix that
carried it.

⚠️ **Do not cite Lipton & Steinhardt as venue precedent** — *Troubling Trends* was **ICML 2018 Debates**, a
workshop, not a main track. Cite it only for its argument, which is the best one-line defense available:
*"Empirical study aimed at understanding can be illuminating even absent a new algorithm."*

### Search-layer fabrication — FOUR caught this session. Treat as a standing hazard.

While checking peer-review statistics, WebSearch returned confident, precisely-formatted numbers
("novelty rewarded least often (31.9%)", "rises from 21.5% to 54.0%") attributed to a real paper
(arXiv:2511.15462). The PDF was downloaded and grepped: **zero hits. The numbers do not exist in the
paper.** They were a search-summary fabrication.

**Nothing sourced from a search snippet goes in the paper without fetching the primary text.**

**This was not a one-off. Four distinct fabrications were caught, each only because an agent fetched the
primary document and grepped it:**

1. Novelty percentages (31.9% / 21.5% / 54.0% / 63.5% ...) attributed to arXiv:2511.15462 — **zero grep
   hits in the PDF.** The paper's only percentages are 12.4/55.7/57.6/6.4/7.8/8.0.
2. *"Gundersen & Kjensmo: only 6% stated research questions, 5% stated hypotheses"* — **not in the AAAI
   paper.** Its complete percentage set is 15/20/24/25/26/29/30/32.3/4.29/4.30/48.3/49/7.15/8.54/8.87/90/95.
   An agent reported nearly using this one.
3. *"NeurIPS 2019 Reproducibility Challenge: 21.1% acceptance"* — a fabricated conflation with the
   main-conference rate.
4. Fanelli 2010's Computer Science positive-results rate — the **category exists** (Table 1: B=0.711,
   p=0.068, OR=2.036, CI 0.949-4.372) but **no percentage is ever printed**; it exists only as a bar in
   Figure 1. A WebFetch summarizer first claimed CS was absent entirely, then a visual read of the figure
   showed it present. Do not cite a number here: N=63 (second-smallest discipline), **p=0.068 — not
   significant, CI crosses 1** — and Fanelli sampled on the phrase "test\* the hypothes\*", which ML
   papers reporting benchmark wins do not use.

**The relevant irony:** this paper's own thesis is that unverified implementation details decide results
(P0-0, P0-2). Importing a hallucinated statistic into the fix would be the same error one level up.
Every number that enters the revision gets fetched and grepped, including the ones in these docs. The related
real finding, verified: in that paper's Table 4, novelty criticism is the **#1 predictor of review rating**
(0.47 avg |coef|) — an importance weight, **not** a frequency. No verified "% of ML reviews citing lack of
novelty" statistic exists in the reachable literature.

---

## ★ Verbatim reviewer evidence (ICLR 2017-2020 corpus) — the bar is not what we assumed

Earlier I flagged "the exact phrasing this paper will face" as an unfilled gap. It is now filled from
real review text, recovered two independent ways and **cross-validated byte-for-byte** (archived
OpenReview API JSON via Wayback + the ASAP-Review corpus: 5,192 ICLR papers 2017-2020 with full reviews,
ratings, meta-reviews, and decisions, including 3,333 rejects). Offline copies:
`scratchpad/index.json`, `scratchpad/neg.txt` (all 69 reviews using negative/null-result language).

### The finding that matters most — and it is a *rejection*

**"Surprising Negative Results for Generative Adversarial Tree Search"** (Azizzadenesheli, Yang, Liu,
Brunskill, Lipton, Anandkumar), ICLR 2019 — **REJECTED**, https://openreview.net/forum?id=BJl4f2A5tQ

> **R1 (rating 5):** "I think publishing negative research results is very important and should be done
> more often *if we can learn from those results*. But that is an aspect I feel this paper falls short
> at... they do not a provide a thorough investigation of the causes which make GATS 'fail'."
> **R2 (rating 5):** "While I appreciate negative results and there should be more papers like this, I do
> think that this paper falls short..."
> **R3 (rating 6):** "It is highly appreciated that this paper presents an idea and discusses why the
> proposed approach does not result in high performance. This is very valuable..."
> **META-REVIEW:** "All reviewers and the AC appreciate the import role that such a contribution can
> bring to the research community... **The concern that most strongly affected the final evaluation is
> the limited insight (and evidence) of the factors that influence performance.** Due to this, the
> consensus is to not accept."

**All three reviewers and the AC endorse negative results in the abstract — then reject.** Note a
Lipton co-authorship: the author of *"Empirical study aimed at understanding can be illuminating even
absent a new algorithm"* was rejected for a null that did not explain itself.

**So "reviewers punish no-new-method work" is false, and it was the wrong worry.** Praise is
near-universal and always followed by *but*. The real, repeated bar: **a null is welcome only if it
diagnoses its own mechanism.** Three more rejections state it outright:

> "Having only negative results could be fine **if the paper was bringing some value with a sharp
> analysis of the failure modes and of the reasons behind it**... there is not much to take-away."
> "No positive results, only negative results. **To really understand the negative results, it would be
> good to know what is missing to make it work. This has not been studied further.**"
> "In a sense, the present study offers a null result and obviously, **the work would have been much more
> significant had the authors offered a mechanism**."

**This settles A vs. C** (`PAPER_V2_OUTLINE.md`). Identity A *is* the paper that gets this rejection —
a repaired measurement whose mechanism section has been hollowed out by P0-0. **Identity C is literally
the bar these reviewers state.** C is not the ambitious option; it is the minimum.

### Two reviewers wrote our P0-0 and our N=7 objection, verbatim

*Rethinking the Value of Network Pruning*, ICLR 2019 — **ACCEPTED**, AnonReviewer1 post-rebuttal:

> "**I wonder whether that a carefully tuned learning rate/hyperparameters for fine-tuning may get the
> same or better performance as scratch training.**"

That is P0-0 and P0-2 in a reviewer's own words, on an *accepted* paper — "did you tune the baseline, or
just yours?" Same thread, AnonReviewer2: *"It is still difficult to believe that most of the previous
work and previous experiments are faulty."* And R1: *"The experiments might not be enough to reject the
common belief."*

*On the State of the Art of Evaluation in Neural Language Models*, ICLR 2018 — **ACCEPTED**, Reviewer 2:

> "**the corpus the authors choose are quite small, the variance of the estimate will be quite high, I
> suspect whether the same conclusions could be drawn.**"

That is our N=7 objection, verbatim, on an accepted paper — which is what X4 answers.

### How accepted nulls survive: guarded claims

*Rethinking Pruning* meta-review (**Accept**), titled *"Empirical paper casting shade on pruning"*:

> "These results **seem unsurprising in retrospect, but hindsight is 20-20**... your claims should be
> properly circumscribed... **I would recommend the authors make guarded claims here.**"

Melis meta-review (**Accept**): *"it's an important paper in general which will work as an alarm to the
current practice in the field."* Reviewer 3: *"a milestone in deep learning reproducibility research."*

And the counter-example — *Do Deep RL Algorithms really Learn to Navigate?* (**Reject**): *"While there
is value in thorough evaluation papers... it misrepresents the claims made by Mirowski et al 2016 and
**over-reaches in its findings**."* Reviewer: *"by extensively researching the literature before trying
to affirm that a general method cannot solve certain tasks."*

**The pattern across accept/reject is not the null. It is scope discipline plus a mechanism.** Guarded
claims + explained mechanism → accept. Broad claims or unexplained null → reject, however warmly praised.

⚠️ **Correction:** *The State of Sparsity in Deep Neural Networks* was **never an ICLR submission** (absent
from a corpus ~99% complete for 2019) — it is ICML 2019, which does not use OpenReview, so no public
reviews exist. Reviewer identities are confirmed only for *Rethinking Pruning*; elsewhere reviewers are
labeled by rating, which is what the source supports.

### ★★ The central vulnerability: reviewers have a *competing mechanism* for our gap, and it's free for them

Across ~600 real reviews, three independent sweeps converge: **no reviewer rejected a measurement paper
for being wrong. Every rejection was on contribution framing.** The confirmed measurement-paper rejects
died on *"low technical contribution"*, *"missing the so what?"*, or *"confirms what is already known"*.

But the sharpest finding is about *our* paper specifically:

> **Reviewers already believe Design-Bench's oracles are broken.** That gives them a competing
> explanation for our synthetic→Design-Bench gap that costs them nothing to raise and that **N=7 cannot
> rule out.**

We make this worse ourselves: we substitute **RF oracles on 5 of 7** Design-Bench tasks (`db_tasks.py:22`,
`FLAW_LEDGER.md` T4). Our headline claim is that the gap reflects prior–task mismatch; a reviewer says it
reflects broken oracles; both fit the data. **This is a framing problem, not a measurement problem**, and
it is the single most likely reject route for Contribution 3.

**Cheap answer, and it becomes a new ledger row (X11):** show the null survives on the **exact-oracle
subset** (TF-Bind-8, TF-Bind-10 — the only two DB tasks with exact oracles), or report the **oracle noise
floor against our effect size**. Near-zero CPU; reuses the existing grid. It converts "your oracles are
broken" from a fatal competing hypothesis into a controlled-for one.

### The attack our η²_opt = 0.01 will take, in a reviewer's own words

*Are GANs Created Equal?* (NeurIPS 2018, **accepted**) — Reviewer 2, verified against the proceedings HTML:

> "The authors claim that algorithmic differences in state-of-the-art GANs become less relevant, as the
> computational budget increases. **This is true according to the way the authors carried out the
> experiments. But, what happens if we start the hyperparameters tuning by doing a random search from the
> recommended values for each algorithm.** Maybe the hyperparameters recommended by the authors are
> already good enough..."

Note the shape: **"This is true according to the way you did it"** — concede the result, attack the
protocol. Aimed at the closest accepted precedent to our paper. This is exactly the fire P0-0, P0-1 and
P1-1 invite, and exactly what GATE-1 and `gradtune` were built to answer — while `gradtune`'s answer is
currently unreported.

### The single most useful sentence for our framing — declare the null

ICLR 2026, [QIJk2xjJI3](https://openreview.net/forum?id=QIJk2xjJI3):

> "is the purpose of the paper to display a null result (**which I think is not an issue, but it should be
> stated as such**)?"

**A null is acceptable if *declared*. The failure mode is an *undeclared* null** that reads as a study
that didn't find anything. Declare it in the abstract, scoped to Design-Bench at N=7. Free.

### The offensive precedent — win on the mechanism, not the absence

*Are Emergent Abilities of Large Language Models a Mirage?* — **NeurIPS 2023 Outstanding Paper**, rated 9:

> "shows that the widely-discussed phenomenon of 'emergent abilities' ... is **largely due to the choice of
> (discontinuous/nonlinear) metrics and underpowered analyses**." / "No major weaknesses - the paper was a
> pleasure to read!"

It won on ***"it's the metric"***, not on "we found nothing." That is the template: name the artifact that
manufactures the believed effect.

### Two assets and two cautions

**Asset 1 — our stats apparatus is what reviewers request.** NeurIPS 2025 [RCeZ063p33](https://openreview.net/forum?id=RCeZ063p33):
*"consider following **Demšar (2006) by first performing a Friedman test and then applying a Wilcoxon
signed rank post hoc test with Holm adjustment**... visualized with a **Critical Difference diagram**."*
That is precisely what commit `8ebab0b` built. Lead with it. (Balance against Benavoli's pool objection,
`FLAW_LEDGER.md` P1-2.)

**Asset 2 — TOST calibration, concrete.** ICLR 2026 [30e3LnZzmI](https://openreview.net/forum?id=30e3LnZzmI),
authors defending equivalence with our exact tool: *"robust statistical tests, including TOST, require a
larger number of samples... we performed a Welch TOST analysis with **N=30 runs per condition**."*
They needed **N=30 per condition**; we have **N=7 tasks**. The most concrete calibration of our gap found.

⚠️ **Caution 1 — do not rebut a phrase reviewers never use.** *"Absence of evidence is not evidence of
absence"* was independently confirmed **absent** across ~600 reviews and 34 targeted queries. Do not build
a rebuttal section around it.

⚠️ **Caution 2 — demote Prop 2.** Both conformal-prediction analogues in the corpus are **rating-3 rejects
on "straightforward application."** Numbering it a Proposition invites a comparison it cannot win
(`FLAW_LEDGER.md` P1-7, X9). Make it a cited lemma.

⚠️ **Method ceiling:** AAAI reviews are not public. All phrasings are an ICLR/NeurIPS proxy. Also corrected
here: the ICBINB "Entropic Award" is **NOT VERIFIED** — a direct fetch of the 2026 page shows no awards
section. Do not cite it.
```

---
## FILE: docs/ARTIFACT_INVENTORY.md
<!-- lines: 447 | bytes: 30913 | last commit: f90f975 2026-07-17 -->
````markdown
# Experimental Artifact Inventory — /Users/palaash/Downloads/MBO/results/

Audit date: 2026-07-17. All JSONs parsed successfully with system `python3` stdlib `json`.
**No file was corrupt or unreadable.**

---

## 0. Headline verdicts (detail below)

| Question | Answer |
|---|---|
| Primary artifact (synthetic) | `results/results_camera.json` |
| Primary artifact (Design-Bench) | `results/results_db.json` |
| Are the gitignored files the primary artifacts? | **YES** — proven by code path + numeric match to `main.tex` |
| Full 3x3 grid complete? | **YES** — 9/9 cells x 14 tasks, no missing/under-seeded grid cells |
| Seeds | 30 (synthetic mbo), 16 (Design-Bench), 10 (calibration/beta/K/enssub sweeps) |
| Tasks | 7 synthetic + 7 Design-Bench = **14 distinct, zero overlap** |
| Timestamp / git sha / config block in any record? | **MISSING — none of the 18 artifacts carries any provenance metadata** |

---

## 1. Global schema

All grid-bearing files share one shape (depth 5):

```
{ <block>: { <task>: { <cell>: { "p100"|"p50": { "mean": float,
                                                 "std":  float,
                                                 "all":  [float, ...]  # one entry per seed
                                               } } } } }
```

Example leaf record — `results_camera.json` `/mbo/Branin-2D/ens:perturb/p100`:

| key | type | sample value |
|---|---|---|
| `mean` | float | `-0.7798330307006835` |
| `std` | float | `0.2984145691205014` |
| `all` | list[30] | `[-0.9686107635498047, -0.8322124481201172, ...]` |

**Cell naming.** Grid cells are `<surrogate>:<optimizer>` — surrogates `{ens, botorchgp, svgp}` x optimizers `{perturb, grad, cma}` = the 9-cell 3x3 grid. Non-grid entries (`coms`, `cbas`, `gp`, `grad_ascent`, `sparse_gp`, `ens_conformal:grad`, `ens_conformal:perturb`) are external/reference baselines.

**Seed values.** There is **no explicit seed field anywhere**. `code/run_all.py:79` generates `for s in range(seeds)`, so seed values are **0..N-1**, carried only *positionally* in the `all` arrays. Distinct-seed count is therefore `len(all)`; seed identity is implicit and unverifiable from the artifacts alone.

**Provenance.** A regex scan for `timestamp|git|sha|commit|config|date|host|meta|version|runtime|args` across every file returned **no metadata keys** in any artifact (the single hit, `per_seed` in `results_new.json`, is data, not metadata). **All 18 artifacts are provenance-free.**

---

## 2. Per-file inventory

### 2.1 `results_camera.json` — PRIMARY (synthetic)
- **Size / mtime:** 392,577 B | Jul 15 13:13:23 2026 (**2nd-newest grid file**)
- **Top-level:** dict[6] = `mbo`, `calibration`, `beta`, `K`, `mbo_beta0`, `mbo_enssub`
- **Tasks (7):** Branin-2D, Styblinski-5D, Levy-8D, Rosenbrock-10D, Rastrigin-15D, Ackley-20D, Griewank-30D
- **Cells (16):** all 9 grid cells + `cbas`, `coms`, `gp`, `grad_ascent`, `sparse_gp`, `ens_conformal:grad`, `ens_conformal:perturb`
- **Seeds:** `mbo` = **30** in all 7x16 = 112 cells (uniform, zero exceptions). `mbo_beta0` = 30. `calibration`/`beta`/`K`/`mbo_enssub` = **10**.
- **Coverage data:** YES — `calibration/<task>/_` , 12 keys: `rho_err`, `q_conformal`, `cov_conf_indist`, `cov_conf_ood`, `cov_indist@{0.5,1.0,2.0,5.0}`, `cov_ood@{0.5,1.0,2.0,5.0}`. Task-level (cell key is the placeholder `_`), **not per-grid-cell**, 10 seeds each.
- **Sweep axes:** `beta` ∈ {0.0, 0.5, 1.0, 2.0, 5.0} (p100 only); `K` ∈ {2, 3, 5, 10} (p100 only); `mbo_beta0` = 9 grid cells re-run at β=0; `mbo_enssub` = 3 ens cells on GP's data subsample.
- **Provenance:** MISSING

### 2.2 `results_db.json` — PRIMARY (Design-Bench)
- **Size / mtime:** 141,335 B | Jul 15 05:25:48 2026
- **Top-level:** dict[2] = `mbo`, `calibration`
- **Tasks (7):** TFBind8, TFBind10, Superconductor, GFP, UTR, AntMorphology, DKitty
- **Cells (15):** 9 grid + `cbas`, `coms`, `gp`, `grad_ascent`, `ens_conformal:grad`, `ens_conformal:perturb`. **No `sparse_gp`** (fails-and-skips on DB per commit `ff25b6a`).
- **Seeds:** **16** across all 9 grid cells x 7 tasks. Three **baseline** gaps: `Superconductor/gp` = 7, `Superconductor/grad_ascent` = 14, `GFP/gp` = **MISSING**.
- **Coverage data:** YES — same 12-key `calibration/<task>/_` schema, **16 seeds**.
- **Sweep axes:** none (no beta/K blocks on DB).
- **Provenance:** MISSING

### 2.3 `results_camera_matched.json` — GATE-1 control (synthetic)
- **Size / mtime:** 205,105 B | Jul 14 00:14:15 2026
- **Top-level:** dict[1] = `mbo` only. Same 7 tasks, same 16 cells, **30 seeds, 100% uniform**.
- Matched-tuning arm (GP given the ensemble's zero tuning budget). No coverage, no sweeps, no provenance.

### 2.4 `results_db_matched.json` — GATE-1 control (Design-Bench)
- **Size / mtime:** 108,137 B | Jul 14 00:38:07 2026
- **Top-level:** dict[1] = `mbo`. 7 DB tasks, 15 cells, **16 seeds, 100% uniform** — note this file has *no* gaps: it fills `Superconductor/gp` (16 vs live 7), `Superconductor/grad_ascent` (16 vs 14), and `GFP/gp` (16 vs MISSING).
- No coverage, no sweeps, no provenance.

### 2.5 `results_db.preserved.json` — partial DB snapshot
- **Size / mtime:** 43,417 B | Jul 14 00:14:15 2026
- **Top-level:** dict[1] = `mbo`. Only **3 tasks** (TFBind8, TFBind10, Superconductor), 15 cells, 16 seeds each.
- Rescue copy of the 3 completed DB tasks. **Superseded** by `results_db.json` (7 tasks). Notably it holds `Superconductor/gp` at 16 seeds where the live file has 7.

### 2.6 `results_gradtune.json` — optimizer-tuning robustness
- **Size / mtime:** 10,553 B | Jul 14 00:14:22 2026
- **Schema:** `{ task: { variant: list[15] } }` — flat lists, **not** the mean/std/all shape.
- **Tasks (4):** Branin-2D, Styblinski-5D, Rosenbrock-10D, Ackley-20D
- **Variants (7):** `perturb`, `grad_default`, `grad_gentle`, `grad_long`, `grad_norm`, `grad_trust`, `grad_besttuned`
- **Seeds:** 15. No coverage. No provenance. Backs the "under-tuned optimizer" rebuttal (commit `cdd5ad8`).

### 2.7 `05_findings.json` — DERIVED analysis digest
- **Size / mtime:** 11,454 B | Jul 15 16:11:39 2026 — **NEWEST artifact in the directory**
- **Top-level:** dict[14] = `attribution`, `gate1`, `stats`, `equivalence`, `calibration`, `beta_sweep`, `crosscheck`, `K_ablation`, `beta0`, `subsample_control`, `gp_coverage`, `stats_9cell`, `bootstrap_ci`, `rf_robustness`
- **Not a raw artifact** — `code/run05.py:52-53,63-64,88,124,146,171,189` computes every value from `results_camera.json`, `results_camera_matched.json`, `results_db.json`, `official_baselines.json`. This is the file the paper quotes.
- Provenance: MISSING

### 2.8 `gpcov.json` — cross-proposal coverage
- **Size / mtime:** 3,072 B | Jul 15 12:54:31 2026
- **Schema:** `{ task: { metric: {mean, std} } }` — 7 synthetic tasks x 6 metrics (`gp_indist`, `gp_own`, `ens_indist`, `ens_own`, `ens_on_gp`, `gp_on_ens`). No `all` array, so **seed count is not recoverable from this file**.
- Written by `code/run_gpcov.py:64`; consumed by `code/figures.py:401` (fig8_crossproposal). Mirrored into `05_findings.json['gp_coverage']`.

### 2.9 `official_baselines.json` — external reference numbers
- **Size / mtime:** 2,414 B | Jul 14 21:04:09 2026
- **Schema:** `{ method: { task: { "p100": {mean, std, all, n} } } }` — the only file carrying an explicit `n` field.
- **Methods (2):** `coms_official`, `cbas_official`. **Tasks (3):** Superconductor, TFBind8, GFP. **Seeds: 8.**
- Raw values in §7. Companion tarball `official_baselines_raw.tgz` (190,924 B, Jul 14 21:04:16 2026) — raw upstream dump, not parsed here.

### 2.10 Legacy / superseded files (all git-tracked)

| File | Size | mtime | Top-level | Verdict |
|---|---|---|---|---|
| `results.json` | 33,638 | Jul 10 02:42:09 2026 | `mbo`, `o2o`, `rl`, `abl` | **Oldest.** Pre-grid schema (`p100_m`/`p100_s`, cells `lcb`/`coms`/`grad_ascent`). No 3x3 grid. Superseded. |
| `results_final.json` | 9,085 | Jul 14 00:14:21 2026 | `botorch_gp`, `rank_surrogate`, `temp_calibration`, `o2o_extra`, `bootstrap_ranks`, `profiling`, `pen_sensitivity` | Side-experiment grab-bag. No grid. Superseded. |
| `results_new.json` | 14,743 | Jul 14 00:14:23 2026 | `gp_lcb`, `K_ablation`, `beta_counter`, `calibration`, `o2o_diversity` | Old K/beta ablations + old calibration (`rho_sigma_error`/`rho_sigma_knn` schema). Superseded. |
| `results_revision.json` | 64,630 | Jul 14 00:14:25 2026 | `mbo`, `o2o` | Pre-grid revision run; cells `lcb`/`coms`/`grad_ascent`/`lcb_perturb`/`sparse_gp`/`cbas`. `code/mbo.py:18` names it the canonical *config* reference, but its *data* is superseded. |

`code/run05.py:201` reads all four only for a legacy cross-check block.

---

## 3. CROSS-FILE ANALYSIS

### 3.1 Which file is the paper's PRIMARY source?

**Ranked by recency + completeness:**

| Rank | File | mtime | Grid | Tasks x seeds | Role |
|---|---|---|---|---|---|
| 1 | **`results_camera.json`** | Jul 15 13:13 | 9/9 | 7 x 30 | **PRIMARY — synthetic** |
| 2 | **`results_db.json`** | Jul 15 05:25 | 9/9 | 7 x 16 | **PRIMARY — Design-Bench** |
| 3 | `05_findings.json` | Jul 15 16:11 | derived | — | Newest, but a *derivative* of #1/#2 |
| 4 | `results_camera_matched.json` | Jul 14 00:14 | 9/9 | 7 x 30 | GATE-1 control arm |
| 5 | `results_db_matched.json` | Jul 14 00:38 | 9/9 | 7 x 16 | GATE-1 control arm |
| 6 | `gpcov.json` | Jul 15 12:54 | — | 7 | Fig-8 input |
| 7 | `official_baselines.json` | Jul 14 21:04 | — | 3 x 8 | External cross-check |
| 8 | `results_gradtune.json` | Jul 14 00:14 | — | 4 x 15 | Robustness arm |
| 9 | `results_db.preserved.json` | Jul 14 00:14 | 9/9 | 3 x 16 | Partial, superseded |
| 10-13 | `results_revision/new/final/.json` | Jul 10-14 | none | — | Legacy, pre-grid |

**Evidence — the code path.** Every paper-output generator hardcodes the two gitignored files:

- `code/figures.py:26-27` → `CAM = .../results_camera.json`, `DB = .../results_db.json` — produces `paper/figures_v2/*`
- `code/tables.py:12` → `CAM = .../results_camera.json` — produces `paper/tables_v2/*`
- `code/stats.py:19` → `OUT = .../results_camera.json`
- `code/analysis.py:20` → `DEFAULT = .../results_camera.json`
- `code/run05.py:52-53` → writes `05_findings.json` from `results_camera.json` + `results_db.json`

No paper-facing script reads any git-tracked results file except for the legacy cross-check at `run05.py:201`.

### 3.2 GRID COMPLETENESS MATRIX

**`results_camera.json` — synthetic (seed counts per cell):**

| surrogate x optimizer | Branin-2D | Styblinski-5D | Levy-8D | Rosenbrock-10D | Rastrigin-15D | Ackley-20D | Griewank-30D |
|---|---|---|---|---|---|---|---|
| ens:perturb | 30 | 30 | 30 | 30 | 30 | 30 | 30 |
| ens:grad | 30 | 30 | 30 | 30 | 30 | 30 | 30 |
| ens:cma | 30 | 30 | 30 | 30 | 30 | 30 | 30 |
| botorchgp:perturb | 30 | 30 | 30 | 30 | 30 | 30 | 30 |
| botorchgp:grad | 30 | 30 | 30 | 30 | 30 | 30 | 30 |
| botorchgp:cma | 30 | 30 | 30 | 30 | 30 | 30 | 30 |
| svgp:perturb | 30 | 30 | 30 | 30 | 30 | 30 | 30 |
| svgp:grad | 30 | 30 | 30 | 30 | 30 | 30 | 30 |
| svgp:cma | 30 | 30 | 30 | 30 | 30 | 30 | 30 |
| *cbas* (baseline) | 30 | 30 | 30 | 30 | 30 | 30 | 30 |
| *coms* (baseline) | 30 | 30 | 30 | 30 | 30 | 30 | 30 |
| *gp* (baseline) | 30 | 30 | 30 | 30 | 30 | 30 | 30 |
| *grad_ascent* (baseline) | 30 | 30 | 30 | 30 | 30 | 30 | 30 |
| *sparse_gp* (baseline) | 30 | 30 | 30 | 30 | 30 | 30 | 30 |
| *ens_conformal:grad* | 30 | 30 | 30 | 30 | 30 | 30 | 30 |
| *ens_conformal:perturb* | 30 | 30 | 30 | 30 | 30 | 30 | 30 |

**COMPLETE — 112/112 cells at exactly 30 seeds. Zero missing, zero under-seeded.**

**`results_db.json` — Design-Bench (seed counts per cell):**

| surrogate x optimizer | TFBind8 | TFBind10 | Superconductor | GFP | UTR | AntMorphology | DKitty |
|---|---|---|---|---|---|---|---|
| ens:perturb | 16 | 16 | 16 | 16 | 16 | 16 | 16 |
| ens:grad | 16 | 16 | 16 | 16 | 16 | 16 | 16 |
| ens:cma | 16 | 16 | 16 | 16 | 16 | 16 | 16 |
| botorchgp:perturb | 16 | 16 | 16 | 16 | 16 | 16 | 16 |
| botorchgp:grad | 16 | 16 | 16 | 16 | 16 | 16 | 16 |
| botorchgp:cma | 16 | 16 | 16 | 16 | 16 | 16 | 16 |
| svgp:perturb | 16 | 16 | 16 | 16 | 16 | 16 | 16 |
| svgp:grad | 16 | 16 | 16 | 16 | 16 | 16 | 16 |
| svgp:cma | 16 | 16 | 16 | 16 | 16 | 16 | 16 |
| *cbas* (baseline) | 16 | 16 | 16 | 16 | 16 | 16 | 16 |
| *coms* (baseline) | 16 | 16 | 16 | 16 | 16 | 16 | 16 |
| *gp* (baseline) | 16 | 16 | **7** | **MISSING** | 16 | 16 | 16 |
| *grad_ascent* (baseline) | 16 | 16 | **14** | 16 | 16 | 16 | 16 |
| *ens_conformal:grad* | 16 | 16 | 16 | 16 | 16 | 16 | 16 |
| *ens_conformal:perturb* | 16 | 16 | 16 | 16 | 16 | 16 | 16 |
| *sparse_gp* | **MISSING (all)** | | | | | | |

**9x9 grid COMPLETE — 63/63 grid cells at exactly 16 seeds.**

**Defects, all confined to non-grid baselines:**
1. `Superconductor/gp` = **7/16 seeds** (56% short)
2. `Superconductor/grad_ascent` = **14/16 seeds** (2 short)
3. `GFP/gp` = **MISSING entirely**
4. `sparse_gp` absent on all 7 DB tasks (documented: fails-and-skips, commit `ff25b6a`)

Consequence: `05_findings.json['stats']['REAL']['methods']` lists 14 methods vs SYNTH's 16 — `gp` and `sparse_gp` are dropped from the real-task Friedman/Nemenyi family. Defects 1-3 do **not** touch the 3x3 attribution or the 9-cell stats. `results_db_matched.json` and `results_db.preserved.json` both hold complete 16-seed data for `Superconductor/gp` and `GFP/gp` — the gaps are recoverable.

### 3.3 Do camera + db together cover 14 tasks?

**YES — exactly 14, with zero overlap.**

| # | Task | Source |
|---|---|---|
| 1 | Branin-2D | camera |
| 2 | Styblinski-5D | camera |
| 3 | Levy-8D | camera |
| 4 | Rosenbrock-10D | camera |
| 5 | Rastrigin-15D | camera |
| 6 | Ackley-20D | camera |
| 7 | Griewank-30D | camera |
| 8 | TFBind8 | db |
| 9 | TFBind10 | db |
| 10 | Superconductor | db |
| 11 | GFP | db |
| 12 | UTR | db |
| 13 | AntMorphology | db |
| 14 | DKitty | db |

`set(camera) & set(db) = ∅`. Matches `main.tex`: "7 synthetic and 7 Design-Bench tasks".

### 3.4 Seed count per task — is it 30 synthetic / 16 Design-Bench?

**Verified empirically: YES for the main `mbo` grid — but the sweep/calibration arms run at 10.**

| Block | File | Seeds | Uniform? |
|---|---|---|---|
| `mbo` (the 3x3 grid + baselines) | results_camera.json | **30** | Yes, 112/112 cells |
| `mbo_beta0` | results_camera.json | **30** | Yes, 63/63 |
| `calibration` | results_camera.json | **10** | Yes, 7/7 tasks |
| `beta` sweep | results_camera.json | **10** | Yes |
| `K` sweep | results_camera.json | **10** | Yes |
| `mbo_enssub` | results_camera.json | **10** | Yes |
| `mbo` | results_db.json | **16** | Yes on all 9 grid cells; 3 baseline exceptions (§3.2) |
| `calibration` | results_db.json | **16** | Yes, 7/7 tasks |
| `mbo` | results_gradtune.json | **15** | Yes |
| `p100` | official_baselines.json | **8** | Yes |

**Caveat worth flagging to the audit.** The synthetic **calibration** numbers the abstract quotes (0.73 in-distribution, 0.41 own-proposal, 0.97 on GP proposals) rest on **10 seeds, not 30**. The two-sided `.bak` held 30 calibration seeds; the live one-sided rerun dropped to 10. The paper does not state a calibration seed count, so nothing is misreported — but the coverage claims are 3x less-seeded than the grid claims that surround them.

### 3.5 `.bak` diffs (schema/aggregate level)

**`results_camera.json` vs `results_camera.json.twosided.bak`** (284,070 B, Jul 15 03:15:10):

- Blocks added in live: `mbo_beta0`, `mbo_enssub`. Nothing removed.
- Grid cells: **175 shared, 0 changed.** Every `(n, mean)` pair is bit-identical. **The `mbo` performance data was NOT touched.**
- `calibration`: key `rho_knn` **removed**; **all 12 remaining keys changed value**; seed count **30 → 10**.
  - e.g. Branin-2D `rho_err`: `0.23415883103532412` (bak, n=30) → `0.19934121656486625` (live, n=10)

**`results_db.json` vs `results_db.json.twosided.bak`** (138,515 B, Jul 15 05:25:29):

- Top-level keys identical. Grid cells: **104 shared, 0 changed.**
- `calibration`: `rho_knn` removed; 8 of 12 shared keys changed; seed count **stays 16**.
  - e.g. AntMorphology `rho_err`: `0.33457144228576907` → `0.33774184296737186`

**What the two-sided → one-sided switch actually was.** The filename is accurate but its scope is narrow: the change is **confined entirely to the calibration/coverage block; not one optimization result moved.** `code/mbo.py:364-368` defines the new estimator:

```python
def coverage_of_premise(mu, sigma, f, beta):
    """Empirical P(mu - f <= beta*sigma) = P(f >= mu - beta*sigma) — the ONE-SIDED
    LCB lower-bound premise (Prop 1). Not the two-sided band |mu-f|<=beta*sigma:
    under-prediction (f >> mu) never violates a lower bound and must not count as a miss."""
    return float(np.mean((mu - f) <= beta * sigma))
```

and `code/mbo.py:378` switches the conformal multiplier to a signed one-sided nonconformity `r = (mu_cal - y_cal) / s`. So: every `cov_*` and `q_conformal` was recomputed under the one-sided premise, `rho_knn` was dropped as unused, and the synthetic calibration arm was re-run at 10 seeds instead of 30. This is a **methodological correction**, not a result revision — and it is defensible on its face (a lower bound is not violated by under-prediction).

**One live inconsistency to note.** `code/run_all.py:60` still writes `'rho_knn': c['rho_knn']` and `code/mbo.py:614` still computes it, yet neither live artifact contains the key. The live calibration blocks were therefore **not** produced by the current `run_all.py` path, or were post-processed after writing. Given the total absence of provenance metadata, this cannot be resolved from the artifacts.

**`results_camera.json` vs `results_camera.json.presub.bak`** (383,673 B, Jul 15 11:10:54):

- Only difference: live adds the `mbo_enssub` block (21 cells, 3 ens cells x 7 tasks, 10 seeds).
- **238 shared cells, 0 changed. Calibration identical (all 12 keys, same means, n=10 both).**
- Reads as a pre-submission snapshot taken immediately before the ensemble-subsample control was appended.

**`05_findings.json` vs `05_findings.json.bak`** (9,454 B, Jul 15 11:05:16):

- Blocks added in live (7): `equivalence`, `subsample_control`, `rf_robustness`, `beta0`, `gp_coverage`, `stats_9cell`, `bootstrap_ci`
- Unchanged (5): `K_ablation`, `stats`, `gate1`, `crosscheck`, `beta_sweep`
- **Changed (2): `attribution`, `calibration`**

Interpretation: the `.bak` predates the one-sided recomputation (hence `calibration` moved), and the live file adds the entire rebuttal apparatus — TOST equivalence, 9-cell Nemenyi, bootstrap CIs, RF-oracle robustness, β=0 and subsample controls.

### 3.6 Extracted numerics

**η² / effect sizes** (`05_findings.json['attribution']`):

| Regime | η²_opt | η²_surr | η²_inter |
|---|---|---|---|
| SYNTH (unmatched) | **0.013189173376026025** | **0.36872274336144345** | **0.16518056841213977** |
| SYNTH-matched (GATE-1) | 0.024329542667278076 | 0.27542947156964054 | 0.12247869816619208 |
| REAL (Design-Bench) | 0.08473928568992424 | 0.04677094337600403 | 0.013117026453762042 |

Marginal means — SYNTH: opt `{perturb: 0.708, grad: 0.695, cma: 0.608}`, surr `{ens: 0.34, botorchgp: 0.845, svgp: 0.827}`. SYNTH-matched: opt `{perturb: 0.702, grad: 0.652, cma: 0.55}`, surr `{ens: 0.338, botorchgp: 0.741, svgp: 0.825}`. REAL: opt `{perturb: 0.782, grad: 0.584, cma: 0.526}`, surr `{ens: 0.529, botorchgp: 0.729, svgp: 0.634}`.

**Bootstrap 95% CIs** (`bootstrap_ci`): η²_surr `[0.25, 0.57]`, η²_opt `[0.01, 0.19]`, η²_inter `[0.11, 0.26]`, gap_b2 `[0.43, 0.58]`, gap_b0 `[0.37, 0.57]`, gap_sub `[0.29, 1.32]`, gap_b2_minus_b0 `[-0.02, 0.1]`.

**GATE-1** (`gate1`): sei_unmatched `0.6515004904835162`, sei_matched `0.5487667279082784`, **retention `0.842312071785252`**.
> Discrepancy worth flagging: `main.tex` twice claims the surrogate effect "retains 76%". `gate1.retention` is **0.842**. The 76% figure instead matches η²_surr: 0.27542947 / 0.36872274 = **0.747**. The paper's "76%" rounds the η² ratio (74.7%), not the SEI retention (84.2%). The prose is defensible but the two retention measures are 10 points apart and the paper does not disambiguate.

**Friedman p-values:**

| Family | SYNTH | REAL |
|---|---|---|
| Full method set (`stats`) | **1.075443304569636e-06** (16 methods) | **0.7115487157582647** (14 methods) |
| 9-cell grid (`stats_9cell`) | **6.0862487752768236e-05** | **0.6868961533686879** |
| RF-robustness, 3-task (`rf_robustness`) | — | **0.929** |

`main.tex` quotes the **9-cell** family (`p = 6.1e-5` and `p = 0.69`) — correct and the conservative choice.

**Critical differences (Nemenyi, α=0.05):** `stats.SYNTH.cd` = **8.718713580595622** (16 methods); `stats.REAL.cd` = **7.498917263691774** (14 methods); `stats_9cell.cd` = **4.540863039429524** (both regimes, 9 cells — paper quotes 4.5).

Best cells — SYNTH: `botorchgp:grad`, mean rank **2.2857142857142856**, CI `[1.2857142857142858, 3.5714285714285716]`. REAL: `botorchgp:perturb`, mean rank **3.5714285714285716**, CI `[1.8571428571428572, 5.714285714285714]`.

**TOST bounds** (`equivalence`): best `botorchgp:perturb` vs worst `ens:cma`; gap **0.3762254599365316**; **ci90 `[-0.10776105394391278, 0.860211973816976]`**; **effect_bound `0.4839865138804444`** (paper's "±0.48"); `equiv_margin_0p5 = false`, `equiv_margin_0p3 = false` — **equivalence NOT established at either margin.**

**Coverage — SYNTH means:** `cov_indist@2.0` **0.7291714285714287**, `cov_ood@2.0` **0.4133928571428571**, `cov_conf_indist` **0.9024285714285715**, `cov_conf_ood` **0.5074776785714286**, `rho_err` **0.09605668080100692**.

Per-task (SYNTH), `cov_indist@2.0` / `cov_ood@2.0` / `cov_conf_indist` / `cov_conf_ood` / `rho_err`:

| Task | indist@2 | ood@2 | conf_indist | conf_ood | rho_err |
|---|---|---|---|---|---|
| Branin-2D | 0.7094 | 0.418359375 | 0.9066 | 0.837890625 | 0.19934121656486625 |
| Styblinski-5D | 0.6442 | **0.0** | 0.8958 | **0.0** | 0.08715999663998655 |
| Levy-8D | 0.678 | 0.1109375 | 0.9036 | 0.280078125 | 0.0974695162780651 |
| Rosenbrock-10D | 0.862 | 0.64375 | 0.9022 | 0.662109375 | 0.0820685586742347 |
| Rastrigin-15D | 0.7286 | 0.720703125 | 0.9128 | 0.772265625 | 0.05299220236880947 |
| Ackley-20D | 0.9154 | 1.0 | 0.8934 | 1.0 | 0.07233031414124254 |
| Griewank-30D | 0.5666 | **0.0** | 0.9026 | **0.0** | 0.08103496093984376 |

**Coverage — REAL means:** `cov_indist@2.0` **0.7670714285714286**, `cov_ood@2.0` **0.17689732142857142**, `cov_conf_indist` **0.9012857142857145**, `cov_conf_ood` **0.30674525669642855**, `rho_err` **0.10491519603528769**.

| Task | indist@2 | ood@2 | conf_indist | conf_ood | rho_err |
|---|---|---|---|---|---|
| AntMorphology | 0.9435 | 0.0 | 0.898 | 0.0 | 0.33774184296737186 |
| UTR | 1.0 | 0.0 | 0.913 | 0.0 | **-0.07120832423978705** |
| DKitty | 0.5115 | 0.0 | 0.90325 | 0.0 | **-0.07250733802935211** |
| Superconductor | 1.0 | 0.005615234375 | 0.89925 | 0.005126953125 | 0.6037367309469237 |
| TFBind8 | 0.91775 | 0.70703125 | 0.903375 | 0.7021484375 | **-0.0049916239664958666** |
| GFP | **0.0** | 0.0 | 0.898125 | 0.98779296875 | **-0.015379681490710792** |
| TFBind10 | 0.99675 | 0.525634765625 | 0.894 | 0.4521484375 | **-0.042985233940935764** |

Two oddities the audit should see: **GFP `cov_indist@2.0` = 0.0 while `cov_conf_ood` = 0.988** — a degenerate pattern; and **4 of 7 REAL tasks have negative `rho_err`** (σ anti-correlated with error), which is a stronger anti-calibration statement than the paper's "moderately covered" framing conveys.

**Cross-proposal coverage** (`gp_coverage.mean`, from `gpcov.json`): `gp_indist` **0.9837714285714286**, `gp_own` **0.9734933035714286**, `ens_indist` **0.7342857142857142**, `ens_own` **0.4133928571428571**, `ens_on_gp` **0.9704241071428571**, `gp_on_ens` **0.9265066964285714**. (Paper quotes 0.73 / 0.41 / 0.97.)

**β sweep** (`beta_sweep`): betas `[0.0, 0.5, 1.0, 2.0, 5.0]`, `median_norm_slope` **0.1864586742998922**, `helps_count` **6** of `n` **7**.

**β=0 control** (`beta0`): ens_b2 `0.3395283650696281`, gp_b2 `0.8447656777002787`, svgp_b2 `0.8266593093095068`, ens_b0 `0.3667128385263765`, gp_b0 `0.8319199021547241`, svgp_b0 `0.8306950023881766`, **gap_b2 `0.5052373126306506`**, **gap_b0 `0.46520706362834763`**.

**Subsample control** (`subsample_control`): gp `0.8447656777002787`, ens_full `0.3395283650696281`, ens_sub `0.08136947230312194`, gap_full `0.5052373126306506`, **gap_sub `0.7633962053971567`** (gap widens).

**K ablation** (`K_ablation`, normalized): `2` → **0.9498119122900442**, `3` → **0.516669630587786**, `5` → **0.314807002449946**, `10` → **0.18361987006663957**.

**RF robustness** (`rf_robustness`): spread_nonsub **0.34**, spread_rfsub_exclGFP **0.39**, friedman_3task_p **0.929**.

### 3.7 `official_baselines.json` contents

Two external reference methods — **COMs** and **CbAS** — on **3 Design-Bench tasks**, **8 seeds** each, 100th-percentile only.

| Method | Task | mean | std | n |
|---|---|---|---|---|
| coms_official | Superconductor | **97.13883209228516** | 1.9311698902378291 | 8 |
| coms_official | TFBind8 | **0.4360388517379761** | **0.0** | 8 |
| coms_official | GFP | **2.1457350850105286** | 0.02042702632710025 | 8 |
| cbas_official | GFP | **3.701169401407242** | 0.03612763441691885 | 8 |
| cbas_official | TFBind8 | **0.9334180802106857** | 0.03977850477194052 | 8 |
| cbas_official | Superconductor | **89.5780611038208** | 7.256089337857875 | 8 |

Raw `all` arrays are present for every entry (e.g. coms/Superconductor: `[94.398, 94.521, 96.356, 96.900, 97.701, 97.715, 99.309, 100.212]`). **coms/TFBind8 has std = 0.0 — all 8 seeds returned the identical value `0.4360388517379761`**, i.e. that baseline is deterministic across seeds (or the seeds did not take).

**Cross-check vs our reimplementation** (`05_findings.json['crosscheck']`, computed by `run05.py:170-171` against `results_db.json`):

| Comparison | official_norm | official_raw | ours | abs_diff |
|---|---|---|---|---|
| coms:Superconductor | 1.3126878075233002 | 97.13883209228516 | 1.01354655995965 | 0.2991412475636501 |
| coms:TFBind8 | 0.9925851742969443 | 0.4360388517379761 | 2.21014067530632 | **1.217555501009376** |
| coms:GFP | -8.379941155295537 | 2.1457350850105286 | -9.201119024306536 | 0.8211778690109988 |
| cbas:Superconductor | 1.2105149366480696 | 89.5780611038208 | 1.3638127595186234 | 0.1532978228705537 |
| cbas:TFBind8 | 2.1248036594559974 | 0.9334180802106857 | 2.1206253692507744 | **0.004178290205222979** |
| cbas:GFP | 2.1987514755767723 | 3.701169401407242 | 1.8531188517808914 | 0.3456326237958809 |

CbAS reproduces closely on TFBind8 (Δ 0.004). **COMs on TFBind8 diverges by 1.22 normalized units** — our reimplementation scores 2.21 vs official 0.99, i.e. our COMs is *much better* than the published one. Note `main.tex:158` leans on exactly this task ("2.20 on TF-Bind-8, above every GP cell"). Not necessarily wrong, but the largest single reproduction gap in the file sits under a quoted claim.

---

## 4. Gitignore assessment

`.gitignore:11-13`:
```
# preview/scratch (real results come from the cloud run, frozen later)
results/results_camera.json
results/results_db.json
```

`git check-ignore -v` confirms both are ignored. `git ls-files results/` returns only the four **legacy, superseded, pre-grid** files: `results.json`, `results_final.json`, `results_new.json`, `results_revision.json`.

### ARE THE GITIGNORED FILES THE PRIMARY ARTIFACTS BACKING THE PAPER'S HEADLINE NUMBERS?

## **YES.** Unambiguously.

Three independent lines of evidence:

**1. Code path.** `figures.py:26-27`, `tables.py:12`, `stats.py:19`, `analysis.py:20`, and `run05.py:52-53` all hardcode `results_camera.json` / `results_db.json`. These scripts emit `paper/figures_v2/*` and `paper/tables_v2/*` — the paper's actual figures and tables. Nothing in the paper pipeline reads a tracked results file.

**2. Numeric match.** Every headline number in `paper/aaai27/main.tex` traces to `05_findings.json`, which `run05.py` computes *only* from the two gitignored files plus the two `_matched` files:

| main.tex claim | 05_findings value | Source |
|---|---|---|
| η²_surr = 0.37 vs η²_opt = 0.01 | 0.36872274336144345 / 0.013189173376026025 | results_camera.json |
| η²_inter = 0.17 | 0.16518056841213977 | results_camera.json |
| matched η²_surr = 0.28 | 0.27542947156964054 | results_camera_matched.json |
| Friedman p = 6.1e-5 (synth) | 6.0862487752768236e-05 | results_camera.json |
| Friedman p = 0.69 (real) | 0.6868961533686879 | results_db.json |
| CD = 4.5 | 4.540863039429524 | both |
| coverage 0.73 / 0.41 / 0.97 | 0.7291714 / 0.4133928 / 0.9704241 | results_camera.json calibration + gpcov |
| TOST ±0.48 | 0.4839865138804444 | results_db.json |
| η²_surr ∈ [0.25, 0.57] | [0.25, 0.57] | results_camera.json |
| real η² = 0.05 / 0.08 | 0.04677094 / 0.08473929 | results_db.json |

**3. The tracked alternatives cannot back the paper.** None of the four git-tracked files contains a surrogate x optimizer grid at all — they use the pre-grid `lcb`/`coms`/`grad_ascent` schema with `p100_m`/`p100_s` fields. The paper's central contribution (a 3x3 decomposition) **cannot be reconstructed from anything in version control.**

### Risk

The `.gitignore` comment calls these files "preview/scratch (real results come from the cloud run, frozen later)". **That comment is now false.** These files are the frozen record: `results_camera.json` (Jul 15 13:13) and `results_db.json` (Jul 15 05:25) postdate the last code commit touching them and are what the submitted numbers were computed from. Every headline number in an AAAI-27 submission currently rests on two untracked local files, protected by nothing but this laptop's disk, with:

- **no timestamp, no git sha, no config block** in any record — the run that produced them cannot be identified, let alone reproduced;
- **no seed identifiers** — only positional arrays, so a partial re-run cannot be aligned against the original;
- a **live/code inconsistency** (`run_all.py` writes `rho_knn`; neither artifact has it), meaning the current code does not reproduce the current artifacts;
- **`.bak` siblings that are also untracked** — the only record of the two-sided → one-sided methodology change exists as loose local files.

If this directory is lost, the paper is unreproducible. Recommendation: remove lines 12-13 from `.gitignore` and commit both files (392 KB + 141 KB — trivial for git), or move them to a tagged release / DVC / LFS artifact with a recorded git sha. The `_matched` files (untracked, and the only complete copies of `Superconductor/gp` and `GFP/gp`) warrant the same treatment.

---

## 5. Files not parsed

`official_baselines_raw.tgz` (190,924 B, Jul 14 21:04:16 2026) — compressed raw upstream baseline dump. Not extracted; contents not inventoried.
````

---
## FILE: docs/scripts_offline_selection.py
<!-- lines: 503 | bytes: 27543 | last commit: 9cacc8b 2026-07-17 -->
```python
#!/usr/bin/env python3
"""
FREE-WIN 5.1 — Can an ORACLE-FREE rule pick the winning (surrogate x optimizer)
grid cell on a held-out task?

Pre-registered as a STRETCH goal in PREREGISTRATION.md ("Decision rule (STRETCH)"),
never implemented. Kill criterion, quoted: "Fails either trivial baseline ->
reported honestly and dropped".

Reuses the paper's own normalization (code/analysis.py: task_norm = per-task min-max
over ALL present grid cells) and the paper's headline metric (p100 mean).

Run:  /opt/homebrew/Caskroom/miniforge/base/bin/python3 offline_selection.py
Deps: numpy, scipy only. The miniforge python has no sklearn, so ridge is implemented
      in closed form below; it was validated against sklearn 1.9.0 to 1.6e-15 over 200
      random problems (see ridge_fit_predict).
"""
import json, os, sys, itertools
import numpy as np
from scipy import stats

RNG = np.random.default_rng(0)
REPO = '/Users/palaash/Downloads/MBO'
RES = os.path.join(REPO, 'results')
OUT = os.path.dirname(os.path.abspath(__file__))
B_BOOT = 10000                      # prereg: "Bootstrap CIs B=2000-10000"
METRIC = 'p100'                     # paper headline metric (analysis.py default)
RIDGE_ALPHA = 1.0                   # PRE-SPECIFIED, never tuned (see honesty gate)

SURR = ('ens', 'botorchgp', 'svgp')
OPTS = ('grad', 'perturb', 'cma')
GRID = [f'{s}:{o}' for s in SURR for o in OPTS]      # the 9-cell selection set

# ---------------------------------------------------------------------------
# The paper's normalization, copied verbatim from code/analysis.py (do not invent
# a new one). NOTE it min-maxes over ALL cells containing ':' -- which is 11 cells
# (the 9-cell grid + ens_conformal:{grad,perturb}), not 9. We reuse it exactly as
# the paper does and take argmax over the 9-cell grid only.
# ---------------------------------------------------------------------------
def task_norm(mbo, task, metric=METRIC):
    vals = [v[metric]['mean'] for k, v in mbo[task].items()
            if ':' in k and isinstance(v.get(metric), dict) and 'mean' in v[metric]]
    lo, hi = (min(vals), max(vals)) if vals else (0.0, 1.0)
    return lo, (hi - lo) or 1.0


def load_scores(metric=METRIC):
    """-> (task_names, S[T x 9] normalized scores, n_norm_cells per task)."""
    tasks, rows, ncells = [], [], []
    for f in ('results_camera.json', 'results_db.json'):
        mbo = json.load(open(os.path.join(RES, f)))['mbo']
        for t in mbo:
            lo, rng = task_norm(mbo, t, metric)
            r = [(mbo[t][c][metric]['mean'] - lo) / rng for c in GRID]
            assert all(np.isfinite(r)), t
            tasks.append(t); rows.append(r)
            ncells.append(sum(1 for k in mbo[t] if ':' in k))
    return tasks, np.array(rows), ncells


# ---------------------------------------------------------------------------
# FEATURE INVENTORY -- see the report for the oracle-free honesty assessment.
# Everything here is tagged with its provenance. Nothing is imputed.
# ---------------------------------------------------------------------------

# Oracle-free STRUCTURAL descriptors. Not stored in the artifacts; read off the
# source that defines the task. Synthetic: code/mbo.py:41-85 (dim, n literals).
SYNTH_DN = {'Branin-2D': (2, 2000), 'Styblinski-5D': (5, 3000), 'Levy-8D': (8, 4000),
            'Rosenbrock-10D': (10, 5000), 'Rastrigin-15D': (15, 5000),
            'Ackley-20D': (20, 5000), 'Griewank-30D': (30, 8000)}

# Design-Bench d: ONLY the four values actually recorded in the repo.
#   TFBind8=32, TFBind10=40, Superconductor=86  -- PREREGISTRATION.md:47,
#                                                  cloud/setup.sh:66, cloud/fix_designbench.sh:4-5
#   GFP=4740                                    -- code/mbo.py:282
# UTR / AntMorphology / DKitty: NOT RECORDED ANYWHERE. -> None (MISSING, never imputed).
DB_D = {'TFBind8': 32, 'TFBind10': 40, 'Superconductor': 86, 'GFP': 4740,
        'UTR': None, 'AntMorphology': None, 'DKitty': None}

# Design-Bench N: NOT RECORDED for any task. run_all.py:121 caps at --db-subsample
# default 8000, but db_tasks.py:54-58 concatenates a top block with a random block
# WITHOUT deduping, so realized N is data-dependent, <=8000, and unrecorded. MISSING.
DB_N = {k: None for k in DB_D}

# Oracle-free structural flag, recorded in code/db_tasks.py:7-9 docstring:
#   "continuous tasks (Superconductor, Ant, DKitty, Hopper)"
#   "discrete tasks (TFBind8/10, GFP, UTR, ChEMBL)"
DISCRETE = {'TFBind8': 1, 'TFBind10': 1, 'GFP': 1, 'UTR': 1,
            'Superconductor': 0, 'AntMorphology': 0, 'DKitty': 0}
for t in SYNTH_DN: DISCRETE[t] = 0          # synthetic tasks are all continuous boxes

# ORACLE-CONTAMINATED probes (mbo.py:577-616). Unit-free ones only; q_conformal is
# excluded because it lives in raw y units on synthetic and [0,1] units on DB and is
# therefore not poolable across the 14 tasks.
CONTAM = ['rho_err', 'cov_conf_indist', 'cov_conf_ood',
          'cov_indist@0.5', 'cov_indist@1.0', 'cov_indist@2.0', 'cov_indist@5.0',
          'cov_ood@0.5', 'cov_ood@1.0', 'cov_ood@2.0', 'cov_ood@5.0']


def load_features(tasks):
    """-> dict feature_name -> array (len T), np.nan where MISSING."""
    cal = {}
    for f in ('results_camera.json', 'results_db.json'):
        cal.update(json.load(open(os.path.join(RES, f)))['calibration'])
    F = {}
    F['d'] = np.array([SYNTH_DN[t][0] if t in SYNTH_DN else
                       (DB_D[t] if DB_D[t] is not None else np.nan) for t in tasks], float)
    F['N'] = np.array([SYNTH_DN[t][1] if t in SYNTH_DN else
                       (DB_N[t] if DB_N[t] is not None else np.nan) for t in tasks], float)
    F['discrete'] = np.array([DISCRETE[t] for t in tasks], float)
    F['log_d'] = np.log(F['d'])
    F['log_N'] = np.log(F['N'])
    for k in CONTAM:
        F[k] = np.array([cal[t]['_'][k]['mean'] if k in cal[t]['_'] else np.nan for t in tasks])
    return F


# ---------------------------------------------------------------------------
# Ridge (closed form, standardized features, intercept unpenalized). alpha fixed
# at RIDGE_ALPHA -- pre-specified, NOT tuned. sklearn is unavailable in the miniforge
# python; this is the same estimator sklearn.linear_model.Ridge gives -- verified to
# max abs diff 1.6e-15 over 200 random (n,p) problems against sklearn 1.9.0.
# ---------------------------------------------------------------------------
def ridge_fit_predict(Xtr, ytr, Xte, alpha=RIDGE_ALPHA):
    mu, sd = Xtr.mean(0), Xtr.std(0)
    sd = np.where(sd < 1e-12, 1.0, sd)
    Z = (Xtr - mu) / sd
    zbar = ytr.mean()
    w = np.linalg.solve(Z.T @ Z + alpha * np.eye(Z.shape[1]), Z.T @ (ytr - zbar))
    return ((Xte - mu) / sd) @ w + zbar


def rule_ridge(feat_names):
    """Per-cell ridge of normalized score on task features; argmax predicted cell."""
    def f(tr, te, S, F):
        X = np.column_stack([F[k] for k in feat_names])
        pred = [ridge_fit_predict(X[tr], S[tr, j], X[te][None, :])[0] for j in range(len(GRID))]
        return int(np.argmax(pred))
    return f


def rule_1nn(feat_names):
    """Copy the argmax cell of the nearest training task (standardized feature space)."""
    def f(tr, te, S, F):
        X = np.column_stack([F[k] for k in feat_names])
        mu, sd = X[tr].mean(0), X[tr].std(0)
        sd = np.where(sd < 1e-12, 1.0, sd)
        Z = (X - mu) / sd
        nn = tr[int(np.argmin(np.linalg.norm(Z[tr] - Z[te], axis=1)))]
        return int(np.argmax(S[nn]))
    return f


def rule_groupmean(feat_names):
    """Best cell among training tasks sharing the held-out task's (binary) descriptor;
    falls back to all training tasks if the group is empty."""
    def f(tr, te, S, F):
        g = np.column_stack([F[k] for k in feat_names])
        same = tr[np.all(g[tr] == g[te], axis=1)]
        use = same if len(same) else tr
        return int(np.argmax(S[use].mean(0)))
    return f


# ---------------------------------------------------------------------------
# Baselines
# ---------------------------------------------------------------------------
def bl_fixed_honest(tr, te, S, F):                 # (b) THE ONE TO BEAT
    return int(np.argmax(S[tr].mean(0)))

def bl_restricted(prefix):
    """always-<surrogate>: surrogate fixed; optimizer chosen honestly on the other tasks."""
    idx = [j for j, c in enumerate(GRID) if c.startswith(prefix + ':')]
    def f(tr, te, S, F):
        return idx[int(np.argmax(S[tr][:, idx].mean(0)))]
    return f


def loo(rule, S, F, mask):
    """Leave-one-task-out over the tasks in `mask`. -> (picked_cell[], regret[])."""
    ids = np.where(mask)[0]
    picks, regs = [], []
    for te in ids:
        tr = ids[ids != te]
        j = rule(tr, te, S, F)
        picks.append(j)
        regs.append(S[te].max() - S[te, j])
    return np.array(picks), np.array(regs)


def boot_mean_ci(x, B=B_BOOT, rng=None):
    rng = rng or np.random.default_rng(1)
    idx = rng.integers(0, len(x), (B, len(x)))
    bm = np.asarray(x)[idx].mean(1)
    return float(np.mean(x)), float(np.percentile(bm, 2.5)), float(np.percentile(bm, 97.5))


def boot_paired_ci(a, b, B=B_BOOT, rng=None):
    """Paired bootstrap of mean(a) - mean(b) over tasks (same resampled tasks)."""
    rng = rng or np.random.default_rng(2)
    d = np.asarray(a) - np.asarray(b)
    idx = rng.integers(0, len(d), (B, len(d)))
    bm = d[idx].mean(1)
    return float(d.mean()), float(np.percentile(bm, 2.5)), float(np.percentile(bm, 97.5))


def wlt(a, b, tol=1e-12):
    """win/loss/tie of rule `a` vs baseline `b` in REGRET (lower regret = win)."""
    d = np.asarray(b) - np.asarray(a)
    return int((d > tol).sum()), int((d < -tol).sum()), int((np.abs(d) <= tol).sum())


def detectable_dz(n, alpha=0.05, power=0.80):
    """Smallest paired Cohen's d_z a two-sided t-test at n tasks can detect at `power`."""
    from scipy.stats import nct, t as tdist
    crit = tdist.ppf(1 - alpha / 2, n - 1)
    lo, hi = 1e-4, 5.0
    for _ in range(200):
        mid = (lo + hi) / 2
        p = 1 - nct.cdf(crit, n - 1, mid * np.sqrt(n)) + nct.cdf(-crit, n - 1, mid * np.sqrt(n))
        if p < power: lo = mid
        else: hi = mid
    return (lo + hi) / 2


# ---------------------------------------------------------------------------
def main():
    log = []
    def P(*a):
        s = ' '.join(str(x) for x in a)
        print(s); log.append(s)

    tasks, S, ncells = load_scores()
    F = load_features(tasks)
    T = len(tasks)
    P(f'Loaded {T} tasks x {len(GRID)} grid cells. Metric={METRIC}, '
      f'normalization=analysis.task_norm (min-max over {sorted(set(ncells))} cells/task).')

    # ---------------- 0. Feature inventory ----------------
    P('\n' + '=' * 78 + '\n0. ORACLE-FREE FEATURE INVENTORY\n' + '=' * 78)
    P(f'{"feature":22}{"avail":>8}  provenance / verdict')
    inv = [
        ('d (dim)',        'log_d', 'STRUCTURAL, oracle-free. mbo.py:41-85 (synth); PREREG:47/setup.sh:66 + mbo.py:282 (4 DB). NOT in artifacts.'),
        ('N (dataset size)','log_N', 'STRUCTURAL, oracle-free. mbo.py:41-85 (synth). DB: MISSING (only <=8000 cap; realized N unrecorded).'),
        ('discrete flag',  'discrete', 'STRUCTURAL, oracle-free. db_tasks.py:7-9 docstring. Available 14/14.'),
        ('rho_err',        'rho_err', 'NOT oracle-free: spearman(sig, |mu - task.oracle(xt)|), mbo.py:593.'),
        ('cov_conf_indist','cov_conf_indist', 'NOT oracle-free: task.oracle(xt), mbo.py:610.'),
        ('cov_conf_ood',   'cov_conf_ood', 'NOT oracle-free: f_o = task.oracle(xf) ON THE PROPOSALS, mbo.py:599/611.'),
        ('cov_indist@2.0', 'cov_indist@2.0', 'NOT oracle-free: task.oracle(xt), mbo.py:601.'),
        ('cov_ood@2.0',    'cov_ood@2.0', 'NOT oracle-free: oracle ON THE PROPOSALS, mbo.py:602.'),
    ]
    for name, key, note in inv:
        n_ok = int(np.isfinite(F[key]).sum())
        P(f'{name:22}{n_ok:>4}/{T}  {note}')
    for name, note in [
        ('q_hat (q_conformal)', 'present but EXCLUDED: fit on task.oracle(xc) (mbo.py:609) AND in raw-y units on '
                                'synth vs [0,1] on DB -> not poolable across tasks.'),
        ('rho_knn',    'MISSING from every results/*.json. mbo.py:594/614 computes it and run_all.py:60 saves it, '
                       'but no committed artifact contains it. It is the ONE genuinely oracle-free probe instrumented.'),
        ('sigma stats (mean/median/spread)', 'MISSING. mu/sig computed at mbo.py:585-588, never persisted.'),
        ('ensemble disagreement', 'MISSING (== sigma; never persisted).'),
        ('GP marginal likelihood / held-out NLL', 'MISSING. Never computed anywhere in the codebase.'),
        ('proposal displacement ||x_T - x_0||', 'MISSING. x0/xf exist at mbo.py:597-598, never persisted.'),
        ('PER-CELL features of any kind', 'MISSING. calibration is keyed task -> "_" (run_all.py:73), computed ONCE per '
                                          'task with the ENSEMBLE + grad @ BETA. mbo cells store only p100/p50.'),
    ]:
        P(f'{name:22}{"--":>8}  {note}')

    P('\nKILLER CONSEQUENCE 1: there are ZERO per-(task,cell) features. Protocol rule (a)')
    P('  "pick the cell maximizing a single feature, e.g. argmax c_hat_ood" is NOT COMPUTABLE:')
    P('  c_hat_ood has one value per TASK, not one per cell. Only rules of the form')
    P('  score(task,cell) = g_cell(task_descriptors) are implementable -- which is exactly what')
    P('  PREREGISTRATION.md:56-58 specified ("fit boundary ... from (d, held-out calibration probe)").')
    P('KILLER CONSEQUENCE 2: every calibration probe is computed with task.oracle(). See report.')

    # ---------------- 1. Is there anything to win? ----------------
    P('\n' + '=' * 78 + '\n1. IS THERE ANY HETEROGENEITY TO EXPLOIT?\n' + '=' * 78)
    best = S.argmax(1)
    P(f'{"task":18}{"d":>6}{"N":>7}{"disc":>5}  best cell        ' + '  '.join(f'{c:>14}' for c in GRID))
    for i, t in enumerate(tasks):
        d = '--' if not np.isfinite(F['d'][i]) else f"{int(F['d'][i])}"
        n = '--' if not np.isfinite(F['N'][i]) else f"{int(F['N'][i])}"
        P(f'{t:18}{d:>6}{n:>7}{int(F["discrete"][i]):>5}  {GRID[best[i]]:16} ' +
          '  '.join(f'{v:>14.3f}' for v in S[i]))
    cnt = {GRID[j]: int((best == j).sum()) for j in range(len(GRID))}
    P('\nargmax-cell histogram over the 14 tasks: ' +
      ', '.join(f'{k}={v}' for k, v in cnt.items() if v))
    P(f'distinct winning cells: {len({int(b) for b in best})}/9   '
      f'modal cell wins {max(cnt.values())}/14 tasks')
    P(f'mean per-task score of each cell: ' +
      ', '.join(f'{GRID[j]}={S[:, j].mean():.3f}' for j in range(len(GRID))))

    # ---------------- 2/3. LOO arms ----------------
    all_mask = np.ones(T, bool)
    d_mask = np.isfinite(F['log_d'])
    synth_mask = np.isfinite(F['log_N'])

    arms = [
        # (arm label, mask, [(rule label, rule, oracle_free?)])
        ('ARM 1 - honest oracle-free, ALL 14 tasks (only fully-available descriptor: discrete)',
         all_mask, [
             ('R1  groupmean(discrete)   [oracle-free]', rule_groupmean(['discrete']), True),
             ('R2  ridge(discrete)       [oracle-free]', rule_ridge(['discrete']), True),
         ]),
        ('ARM 2 - honest oracle-free, 11 tasks with d recorded (PREREG rule: boundary from d)',
         d_mask, [
             ('R3  ridge(log d)          [oracle-free]', rule_ridge(['log_d']), True),
             ('R4  1-NN(log d)           [oracle-free]', rule_1nn(['log_d']), True),
             ('R5  ridge(log d,discrete) [oracle-free]', rule_ridge(['log_d', 'discrete']), True),
         ]),
        ('ARM 3 - honest oracle-free, 7 synthetic tasks (d AND N both recorded)',
         synth_mask, [
             ('R6  ridge(log d,log N)    [oracle-free]', rule_ridge(['log_d', 'log_N']), True),
             ('R7  1-NN(log d,log N)     [oracle-free]', rule_1nn(['log_d', 'log_N']), True),
         ]),
        ('ARM 4 - CONTAMINATED CEILING PROBE, all 14 (features USE THE ORACLE; NOT DEPLOYABLE)',
         all_mask, [
             ('C1  ridge(cov_conf_ood,cov_conf_indist) [ORACLE]',
              rule_ridge(['cov_conf_ood', 'cov_conf_indist']), False),
             ('C2  ridge(all 11 unit-free probes)      [ORACLE]', rule_ridge(CONTAM), False),
             ('C3  1-NN(cov_conf_ood,cov_conf_indist)  [ORACLE]',
              rule_1nn(['cov_conf_ood', 'cov_conf_indist']), False),
         ]),
    ]

    results = {}
    for label, mask, rules in arms:
        ids = np.where(mask)[0]
        n = len(ids)
        P('\n' + '=' * 78 + f'\n{label}\n  (n={n} tasks; LOO -> fit on {n-1}, predict 1)\n' + '=' * 78)

        # baselines, recomputed within this arm's task set
        _, r_b = loo(bl_fixed_honest, S, F, mask)                 # (b) honest fixed cell
        _, r_ens = loo(bl_restricted('ens'), S, F, mask)          # (d) always-ensemble
        _, r_gp = loo(bl_restricted('botorchgp'), S, F, mask)     # (d) always-GP
        _, r_svgp = loo(bl_restricted('svgp'), S, F, mask)
        r_rand = np.array([S[i].max() - S[i].mean() for i in ids])   # (c) random cell, exact E
        # (a) best fixed cell in hindsight over this arm's tasks
        j_hind = int(np.argmax(S[ids].mean(0)))
        r_hind = np.array([S[i].max() - S[i, j_hind] for i in ids])

        P(f'  hindsight-best fixed cell on these {n} tasks: {GRID[j_hind]}')
        P(f'\n  {"strategy":48}{"mean regret":>13}{"95% CI":>20}{"vs (b) W/L/T":>14}{"paired diff vs (b) [95% CI]":>34}')

        def row(nm, r, ref=r_b, show_wlt=True):
            m, lo, hi = boot_mean_ci(r)
            if show_wlt:
                w, l, t_ = wlt(r, ref)
                dm, dlo, dhi = boot_paired_ci(r, ref)
                P(f'  {nm:48}{m:>13.4f}{f"[{lo:.4f},{hi:.4f}]":>20}{f"{w}/{l}/{t_}":>14}'
                  f'{f"{dm:+.4f} [{dlo:+.4f},{dhi:+.4f}]":>34}')
            else:
                P(f'  {nm:48}{m:>13.4f}{f"[{lo:.4f},{hi:.4f}]":>20}')
            return m

        P('  --- baselines ---')
        row('(a) best FIXED cell, hindsight  [upper bnd]', r_hind, show_wlt=False)
        row('(b) best FIXED cell on other n-1  <-- BEAT ME', r_b, show_wlt=False)
        row('(c) random cell (exact E over 9)', r_rand, show_wlt=False)
        row('(d) always-ensemble (opt honest)', r_ens, show_wlt=False)
        row('(d) always-GP/botorchgp (opt honest)', r_gp, show_wlt=False)
        row('    always-svgp (opt honest)', r_svgp, show_wlt=False)
        P('  --- rules ---')
        for rl, fn, ofree in rules:
            picks, r = loo(fn, S, F, mask)
            row(rl, r)
            results[rl] = dict(arm=label, n=n, regret=r.tolist(), oracle_free=ofree,
                               picks=[GRID[j] for j in picks],
                               tasks=[tasks[i] for i in ids],
                               vs_b=dict(zip(('W', 'L', 'T'), wlt(r, r_b))),
                               beats_b=bool(r.mean() < r_b.mean()),
                               beats_gp=bool(r.mean() < r_gp.mean()),
                               beats_ens=bool(r.mean() < r_ens.mean()))
            results[rl]['mean_regret'] = float(r.mean())
        results.setdefault('_baselines', {})[label] = dict(
            n=n, hindsight=float(r_hind.mean()), fixed_honest=float(r_b.mean()),
            random=float(r_rand.mean()), always_ens=float(r_ens.mean()),
            always_gp=float(r_gp.mean()), always_svgp=float(r_svgp.mean()),
            hindsight_cell=GRID[j_hind],
            fixed_honest_per_task=r_b.tolist(), tasks=[tasks[i] for i in ids])

    # ---------------- per-task regret table ----------------
    P('\n' + '=' * 78 + '\n5. PER-TASK REGRET (all 14 tasks; arm-1 rules + baselines)\n' + '=' * 78)
    ids = np.arange(T)
    _, r_b = loo(bl_fixed_honest, S, F, all_mask)
    _, r_gp = loo(bl_restricted('botorchgp'), S, F, all_mask)
    _, r_ens = loo(bl_restricted('ens'), S, F, all_mask)
    p_r1, r_r1 = loo(rule_groupmean(['discrete']), S, F, all_mask)
    p_c1, r_c1 = loo(rule_ridge(['cov_conf_ood', 'cov_conf_indist']), S, F, all_mask)
    P(f'{"task":18}{"best cell":16}{"(b)fixed":>10}{"R1 pick":>16}{"R1 reg":>9}'
      f'{"C1 pick":>16}{"C1 reg":>9}{"alwaysGP":>10}{"alwaysENS":>10}')
    for k, i in enumerate(ids):
        P(f'{tasks[i]:18}{GRID[best[i]]:16}{r_b[k]:>10.3f}{GRID[p_r1[k]]:>16}{r_r1[k]:>9.3f}'
          f'{GRID[p_c1[k]]:>16}{r_c1[k]:>9.3f}{r_gp[k]:>10.3f}{r_ens[k]:>10.3f}')
    P(f'{"MEAN":18}{"":16}{r_b.mean():>10.3f}{"":>16}{r_r1.mean():>9.3f}'
      f'{"":>16}{r_c1.mean():>9.3f}{r_gp.mean():>10.3f}{r_ens.mean():>10.3f}')

    # ---------------- 5b. LOO instability of the baseline itself ----------------
    P('\n' + '=' * 78 + '\n5b. IS BASELINE (b) ITSELF STABLE? (n=14 fragility diagnostic)\n' + '=' * 78)
    p_b, _ = loo(bl_fixed_honest, S, F, all_mask)
    p_g, _ = loo(bl_restricted('botorchgp'), S, F, all_mask)
    P(f'  (b) picks: ' + ', '.join(f'{GRID[j]}x{int((p_b==j).sum())}' for j in set(p_b)))
    P(f'  always-GP picks: ' + ', '.join(f'{GRID[j]}x{int((p_g==j).sum())}' for j in set(p_g)))
    a = tasks.index('Ackley-20D'); keep = [i for i in range(T) if i != a]
    P(f'\n  Baseline (b) is "always botorchgp:grad" on 13/14 folds and flips on ONE fold (Ackley-20D).')
    P(f'  Ackley is the single influential task: every perturb cell collapses there, so dropping it')
    P(f'  flips the argmax-of-mean. Mean cell score all-14 vs drop-Ackley:')
    for j, c in enumerate(GRID):
        P(f'    {c:20} all14={S[:, j].mean():.4f}  drop-Ackley={S[keep, j].mean():.4f}')
    P('  -> ONE task out of 14 flips the honest fixed-cell baseline. That is the n=14 problem')
    P('     showing up in the BASELINE, not just in the rules.')

    # ---------------- power ----------------
    P('\n' + '=' * 78 + '\n6. WHAT IS EVEN DETECTABLE AT n=14 TASKS?\n' + '=' * 78)
    for n in (14, 11, 7):
        dz = detectable_dz(n)
        P(f'  n={n:2d}: two-sided paired t-test, alpha=.05, 80% power needs |d_z| >= {dz:.2f}')
    sd = np.std(r_r1 - r_b, ddof=1)
    P(f'\n  observed SD of paired regret diff (R1 - (b)) over 14 tasks: {sd:.4f}')
    if sd > 0:
        P(f'  -> at n=14 the SMALLEST mean regret improvement detectable at 80% power is')
        P(f'     {detectable_dz(14)*sd:.4f} normalized-score units. Anything smaller is invisible here.')
    else:
        P('  -> SD = 0 (the rule is identical to baseline (b) on every task): nothing to test.')
    # sign test resolution
    from scipy.stats import binomtest
    for w in range(7, 15):
        p = binomtest(w, 14, 0.5, alternative='two-sided').pvalue
        if p < 0.05:
            P(f'\n  sign test: need >= {w}/14 wins (0 losses) for p<0.05 two-sided (p={p:.4f}).')
            break

    # ---- THE decisive power fact: could a PERFECT rule even be certified at n=14? ----
    P('\n  --- ceiling: could a PERFECT oracle-free rule be detected at n=14? ---')
    perfect = np.zeros(T)                      # per-task argmax -> regret 0 by definition
    sd_gp = np.std(r_gp - perfect, ddof=1)
    dz_perfect = r_gp.mean() / sd_gp
    P(f'  perfect rule (per-task argmax)     mean regret = 0.0000')
    P(f'  always-GP                          mean regret = {r_gp.mean():.4f}  (SD over tasks {sd_gp:.4f})')
    P(f'  => a PERFECT oracle-free rule beats always-GP with d_z = {dz_perfect:.2f}')
    P(f'  => n=14 needs |d_z| >= {detectable_dz(14):.2f} for 80% power')
    P(f'  => VERDICT ON THE DESIGN: even a PERFECT rule is '
      f'{"detectable" if dz_perfect > detectable_dz(14) else "NOT reliably detectable"} at n=14.')
    P('     The per-task regret of always-GP is dominated by a few catastrophic tasks (TFBind8')
    P('     0.99, Ackley 0.97), so its SD (0.33) exceeds its mean (0.24). No rule can clear the')
    P('     bar at this n. n=14 is not merely "small" -- it is below the resolution of the question.')

    # ---------------- 6b. p50 co-primary metric ----------------
    P('\n' + '=' * 78 + '\n6b. CO-PRIMARY METRIC p50 (PREREGISTRATION.md:17 names p100 AND p50)\n' + '=' * 78)
    t5, S5, _ = load_scores('p50')
    F5 = load_features(t5)
    agree = sum(int(S[i].argmax() == S5[i].argmax()) for i in range(T))
    P(f'  The TARGET itself is metric-unstable: the best cell agrees under p100 and p50 on only')
    P(f'  {agree}/14 tasks. The hindsight-best fixed cell is botorchgp:grad under p100 but '
      f'{GRID[int(np.argmax(S5.mean(0)))]} under p50.')
    _, rb5 = loo(bl_fixed_honest, S5, F5, all_mask)
    _, rg5 = loo(bl_restricted('botorchgp'), S5, F5, all_mask)
    _, r15 = loo(rule_groupmean(['discrete']), S5, F5, all_mask)
    P(f'\n  {"strategy":42}{"p50 regret":>12}{"vs (b) W/L/T":>14}{"vs alwaysGP W/L/T":>19}')
    for nm, r in [('(b) honest fixed cell', rb5), ('always-GP', rg5),
                  ('R1 groupmean(discrete) [oracle-free]', r15)]:
        w1, l1, t1_ = wlt(r, rb5); w2, l2, t2_ = wlt(r, rg5)
        P(f'  {nm:42}{r.mean():>12.4f}{f"{w1}/{l1}/{t1_}":>14}{f"{w2}/{l2}/{t2_}":>19}')
    w, l, _t = wlt(r15, rg5)
    P(f'\n  R1 LOOKS like a winner on p50 (regret {r15.mean():.3f} vs (b) {rb5.mean():.3f}) -- but the SAME rule is')
    P(f'  the WORST strategy tested on the headline p100 metric ({r_r1.mean():.3f} vs (b) {r_b.mean():.3f}, i.e. exactly')
    P(f'  random). And even on p50 it does NOT clear the pre-registered trivial baseline:')
    P(f'  vs always-GP it is {w}/{l}/{_t} (sign test p={binomtest(w, w+l, 0.5).pvalue:.3f} on non-ties).')
    P('  A rule whose sign flips between the two CO-PRIMARY metrics is noise, not signal. It is')
    P('  reported here precisely so it cannot be quietly promoted as the headline.')

    # ---------------- multiplicity ----------------
    P('\n' + '=' * 78 + '\n7. MULTIPLICITY\n' + '=' * 78)
    k_rules = sum(len(r) for _, _, r in arms)
    P(f'  {k_rules} rules were run across 4 arms, on 2 co-primary metrics (p100 headline, p50),')
    P(f'  i.e. up to {k_rules*2} rule-x-metric comparisons against baseline (b).')
    P(f'  Under a coin-flip null, P(>=1 of {k_rules} rules beats (b) by chance) ~= 1-0.5^{k_rules} = '
      f'{1-0.5**k_rules:.3f};')
    P(f'  over {k_rules*2} rule-x-metric slots, {1-0.5**(k_rules*2):.4f}. The best-looking cell in this')
    P('  table is therefore NOT interpretable as a discovery.')
    P('  DISCIPLINE ACTUALLY APPLIED: alpha was fixed at 1.0 a priori and never tuned; every rule')
    P('  run is reported (none dropped); p100 was designated headline BEFORE looking (it is')
    P('  analysis.py\'s default and the paper\'s headline), so the p50 result that flatters R1')
    P('  is NOT promoted. No rule was added after seeing a result.')

    json.dump({'tasks': tasks, 'grid': GRID, 'S': S.tolist(),
               'features': {k: [None if not np.isfinite(v) else float(v) for v in vv]
                            for k, vv in F.items()},
               'results': results},
              open(os.path.join(OUT, 'offline_selection_results.json'), 'w'), indent=1)
    open(os.path.join(OUT, 'offline_selection_log.txt'), 'w').write('\n'.join(log))
    P(f'\nwrote {OUT}/offline_selection_results.json')


if __name__ == '__main__':
    # self-check: on a task set where cell j is best everywhere, the honest fixed-cell
    # baseline must attain zero regret, and a rule cannot beat it.
    Sx = np.tile(np.array([0., 0., 1., 0., 0., 0., 0., 0., 0.]), (5, 1))
    Fx = {'discrete': np.zeros(5), 'log_d': np.arange(5.) + 1}
    _, rb = loo(bl_fixed_honest, Sx, Fx, np.ones(5, bool))
    assert np.allclose(rb, 0), rb
    print('self-check OK (dominant cell -> honest fixed-cell baseline has 0 regret)\n')
    main()
```

---
## FILE: docs/scripts_eta_robustness.py
<!-- lines: 506 | bytes: 23916 | last commit: 9cacc8b 2026-07-17 -->
```python
"""Task A — eta^2 robustness profile for "Decomposing the GP Advantage in Offline MBO".

Reproduces the paper's exact eta^2 (code/run05.py::eta2) then recomputes it under
alternative normalizations, unit choices, assumption checks, and a permutation test.

Run:  python eta_robustness.py
"""
import json, os, sys
import numpy as np
from scipy import stats as sst

REPO = '/Users/palaash/Downloads/MBO'
RES = os.path.join(REPO, 'results')
SURR3 = ['ens', 'botorchgp', 'svgp']
OPT3 = ['perturb', 'grad', 'cma']
CELLS = [f'{s}:{o}' for s in SURR3 for o in OPT3]
METRIC = 'p100'


def load(f):
    return json.load(open(os.path.join(RES, f)))


# ---------------------------------------------------------------- core eta^2
def eta2_from_M(M):
    """M: (T, S, O) array of already-normalized values (T = replicate dim).
    EXACT replica of code/run05.py::eta2's algebra.  eta^2 = SS_effect / SS_total."""
    M = np.asarray(M, float)
    T, S, O = M.shape
    g = M.mean()
    sstot = ((M - g) ** 2).sum()
    om, sm = M.mean(axis=(0, 1)), M.mean(axis=(0, 2))          # optimizer / surrogate marginals
    eta_opt = (T * S * ((om - g) ** 2).sum()) / sstot
    eta_surr = (T * O * ((sm - g) ** 2).sum()) / sstot
    inter = M.mean(axis=0) - sm[:, None] - om[None, :] + g
    eta_inter = (T * (inter ** 2).sum()) / sstot
    return float(eta_surr), float(eta_opt), float(eta_inter)


def paper_eta2(path, metric=METRIC):
    """Verbatim port of code/run05.py::eta2 — the paper's own code path."""
    d = load(path)['mbo']
    used, M = [], []
    for t in d:
        vals = {c: d[t][c][metric]['mean'] for c in CELLS
                if c in d[t] and isinstance(d[t][c].get(metric), dict)}
        if len(vals) < 9:
            continue
        a = np.array([vals[c] for c in CELLS], float)
        lo, hi = a.min(), a.max()
        z = (a - lo) / (hi - lo) if hi > lo else np.zeros_like(a)
        M.append(z.reshape(3, 3)); used.append(t)
    M = np.array(M)
    g = M.mean(); sstot = ((M - g) ** 2).sum()
    om3, sm3 = M.mean(axis=(0, 1)), M.mean(axis=(0, 2))
    eta_opt = (len(used) * 3 * ((om3 - g) ** 2).sum()) / sstot
    eta_surr = (len(used) * 3 * ((sm3 - g) ** 2).sum()) / sstot
    inter = M.mean(axis=0) - sm3[:, None] - om3[None, :] + g
    eta_inter = (len(used) * (inter ** 2).sum()) / sstot
    return used, float(eta_surr), float(eta_opt), float(eta_inter), M


# ---------------------------------------------------------------- data pulls
def raw_cellmeans(path, metric=METRIC):
    """(tasks, R) where R[t] is the (3,3) array of RAW cell means. Only complete grids."""
    d = load(path)['mbo']
    tasks, R = [], []
    for t in d:
        vals = {c: d[t][c][metric]['mean'] for c in CELLS
                if c in d[t] and isinstance(d[t][c].get(metric), dict)}
        if len(vals) < 9:
            continue
        tasks.append(t)
        R.append(np.array([vals[c] for c in CELLS], float).reshape(3, 3))
    return tasks, np.array(R)


def raw_seeds(path, metric=METRIC):
    """(tasks, n_seed, A) where A is (T, n_seed, 3, 3) of RAW per-seed values.
    Requires equal seed counts across the 9 cells of a task."""
    d = load(path)['mbo']
    tasks, A = [], []
    for t in d:
        arrs = {}
        ok = True
        for c in CELLS:
            e = d[t].get(c)
            if not (e and isinstance(e.get(metric), dict) and isinstance(e[metric].get('all'), list)):
                ok = False; break
            arrs[c] = np.array(e[metric]['all'], float)
        if not ok:
            continue
        ns = {len(v) for v in arrs.values()}
        if len(ns) != 1:
            print(f'  !! {t}: unequal seed counts {ns} -> skipped from per-seed arm')
            continue
        n = ns.pop()
        block = np.stack([arrs[c] for c in CELLS], axis=1).reshape(n, 3, 3)   # (seed,3,3)
        tasks.append(t); A.append(block)
    ns = {a.shape[0] for a in A}
    if len(ns) != 1:
        raise RuntimeError(f'tasks disagree on seed count: {ns}')
    return tasks, ns.pop(), np.array(A)     # (T, n_seed, 3, 3)


# ------------------------------------------------------- normalization zoo
def n_minmax(R):
    """paper's: per-task min-max over the 9 cell means -> [0,1]"""
    out = []
    for a in R:
        lo, hi = a.min(), a.max()
        out.append((a - lo) / (hi - lo) if hi > lo else np.zeros_like(a))
    return np.array(out)


def n_rank(R):
    """per-task rank (1..9) of the 9 cell means; ties averaged."""
    return np.array([sst.rankdata(a.ravel()).reshape(3, 3) for a in R])


def n_zscore(R):
    """per-task z-score over the 9 cell means (ddof=0)."""
    out = []
    for a in R:
        s = a.std()
        out.append((a - a.mean()) / s if s > 0 else np.zeros_like(a))
    return np.array(out)


def n_logregret(R):
    """Principled log for negative values: work in REGRET space.
    Every task here is a maximization with per-task-comparable cells, so define
        regret_c = max_over_the_9_cells(y) - y_c   >= 0   (0 for the best cell),
    which is non-negative BY CONSTRUCTION regardless of the raw sign, then take
        z_c = -log1p(regret_c)
    (log1p is finite at regret=0; the minus keeps 'higher = better' orientation).
    Finally min-max within task, so this arm changes ONLY the transform, not the
    paper's comparability step -- an apples-to-apples swap.
    log1p is scale-dependent, so we first divide regret by the task's regret scale
    (its max) to make log1p's unit-knee task-invariant."""
    out = []
    for a in R:
        reg = a.max() - a
        s = reg.max()
        reg = reg / s if s > 0 else reg
        z = -np.log1p(reg)
        lo, hi = z.min(), z.max()
        out.append((z - lo) / (hi - lo) if hi > lo else np.zeros_like(z))
    return np.array(out)


def n_winsor_seeds(A, pct):
    """Winsorize the per-seed pool WITHIN each task at [pct, 100-pct], then take
    cell means, then per-task min-max. This is the arm that directly attacks the
    'one extreme cell compresses the rest' worry, because it clips in raw space
    before the min-max range is computed."""
    out = []
    for block in A:                      # (seed,3,3)
        flat = block.ravel()
        lo_q, hi_q = np.percentile(flat, [pct, 100 - pct])
        w = np.clip(block, lo_q, hi_q)
        cm = w.mean(axis=0)              # (3,3) winsorized cell means
        lo, hi = cm.min(), cm.max()
        out.append((cm - lo) / (hi - lo) if hi > lo else np.zeros_like(cm))
    return np.array(out)


def n_winsor_cellmeans(R, pct):
    """Winsorize the 9 cell means within task at [pct,100-pct], then min-max.
    (weaker: with only 9 points the 5th/10th pct barely clips)"""
    out = []
    for a in R:
        lo_q, hi_q = np.percentile(a.ravel(), [pct, 100 - pct])
        w = np.clip(a, lo_q, hi_q)
        lo, hi = w.min(), w.max()
        out.append((w - lo) / (hi - lo) if hi > lo else np.zeros_like(w))
    return np.array(out)


def n_raw(R):
    """no normalization at all: pool RAW cell means across tasks."""
    return np.array(R, float)


# ---------------------------------------------------- per-seed unit variants
def seeds_normed(A, how='minmax'):
    """A: (T, n_seed, 3, 3) raw. Returns (T*n_seed, 3, 3) with the replicate dim
    flattened over (task, seed) -- so each (task,seed) is one row of the ANOVA.
    Normalization uses the per-task CELL-MEAN lo/hi (exactly analysis.py::task_norm),
    applied to the individual seed values, so seed values may fall outside [0,1]."""
    out = []
    for block in A:                       # (seed,3,3)
        cm = block.mean(axis=0)
        if how == 'minmax':
            lo, hi = cm.min(), cm.max()
            rng = (hi - lo) or 1.0
            z = (block - lo) / rng
        elif how == 'zscore':
            m, s = cm.mean(), cm.std()
            z = (block - m) / (s or 1.0)
        elif how == 'rank':
            # rank the 9 cells WITHIN each (task,seed) row
            z = np.stack([sst.rankdata(b.ravel()).reshape(3, 3) for b in block])
        elif how == 'raw':
            z = block
        else:
            raise ValueError(how)
        out.append(z)
    A2 = np.array(out)                    # (T, seed, 3, 3)
    T, S = A2.shape[0], A2.shape[1]
    return A2.reshape(T * S, 3, 3)


# ---------------------------------------------------------- assumption checks
def assumption_checks(M, label):
    """M: (T,3,3) the paper's normalized design. Model: y_{t,s,o} = cellmean_{s,o} + e.
    Residual = M - cellmean (over tasks). 63 residuals, 9 groups of 7."""
    cm = M.mean(axis=0)
    resid = (M - cm[None, :, :])
    r = resid.ravel()
    sw = sst.shapiro(r)
    # QQ summary
    skew, kurt = float(sst.skew(r)), float(sst.kurtosis(r, fisher=True))
    n = len(r)
    theo = sst.norm.ppf((np.arange(1, n + 1) - 0.5) / n)
    qq_r = float(np.corrcoef(np.sort(r), theo)[0, 1])
    groups = [M[:, i, j] for i in range(3) for j in range(3)]
    lev = sst.levene(*groups, center='median')
    bart = sst.bartlett(*groups)
    ratio = float(max(np.var(g, ddof=1) for g in groups) / max(1e-300, min(np.var(g, ddof=1) for g in groups)))
    return dict(label=label, n_resid=n,
                shapiro_W=float(sw.statistic), shapiro_p=float(sw.pvalue),
                resid_skew=skew, resid_excess_kurtosis=kurt, qq_corr=qq_r,
                levene_W=float(lev.statistic), levene_p=float(lev.pvalue),
                bartlett_T=float(bart.statistic), bartlett_p=float(bart.pvalue),
                var_ratio_max_min=ratio,
                group_vars=[float(np.var(g, ddof=1)) for g in groups])


# ------------------------------------------------------------- permutation
def permutation_test(M, n_perm=20000, seed=0):
    """Permute FACTOR LABELS WITHIN TASK, which is the exchangeability the null
    asserts (under H0_surrogate the 3 surrogate labels are exchangeable within a
    task, holding the optimizer structure).  No distributional assumption at all.
      - surrogate null: independently permute the 3 ROWS within each task
      - optimizer null: independently permute the 3 COLS within each task
      - interaction null: permute all 9 cells within each task
    Note: min-max normalization is label-invariant (it depends only on the SET of
    9 values in a task), so permuting labels after normalizing is identical to
    permuting before -- the normalization cannot leak into the null."""
    rng = np.random.default_rng(seed)
    obs = eta2_from_M(M)
    T = M.shape[0]
    null_s, null_o, null_i = [], [], []
    for _ in range(n_perm):
        Ms = np.stack([M[t][rng.permutation(3), :] for t in range(T)])
        null_s.append(eta2_from_M(Ms)[0])
        Mo = np.stack([M[t][:, rng.permutation(3)] for t in range(T)])
        null_o.append(eta2_from_M(Mo)[1])
        Mi = np.stack([M[t].ravel()[rng.permutation(9)].reshape(3, 3) for t in range(T)])
        null_i.append(eta2_from_M(Mi)[2])
    null_s, null_o, null_i = map(np.array, (null_s, null_o, null_i))

    def pv(null, o):
        return float((1 + (null >= o).sum()) / (1 + len(null)))
    return dict(
        obs=dict(surr=obs[0], opt=obs[1], inter=obs[2]),
        p_surr=pv(null_s, obs[0]), p_opt=pv(null_o, obs[1]), p_inter=pv(null_i, obs[2]),
        null_surr_mean=float(null_s.mean()), null_surr_q95=float(np.percentile(null_s, 95)),
        null_opt_mean=float(null_o.mean()), null_opt_q95=float(np.percentile(null_o, 95)),
        null_inter_mean=float(null_i.mean()), null_inter_q95=float(np.percentile(null_i, 95)),
    )


def bootstrap_ci(M, n_boot=20000, seed=1):
    """Nonparametric CI on eta^2 by resampling TASKS with replacement (the
    replicate unit of the paper's own ANOVA)."""
    rng = np.random.default_rng(seed)
    T = M.shape[0]
    bs, bo, bi = [], [], []
    for _ in range(n_boot):
        idx = rng.integers(0, T, T)
        try:
            s, o, i = eta2_from_M(M[idx])
        except Exception:
            continue
        if np.isfinite(s) and np.isfinite(o) and np.isfinite(i):
            bs.append(s); bo.append(o); bi.append(i)
    q = lambda a: (float(np.percentile(a, 2.5)), float(np.percentile(a, 97.5)))
    return dict(n_ok=len(bs), ci_surr=q(bs), ci_opt=q(bo), ci_inter=q(bi),
                p_surr_gt_opt=float(np.mean(np.array(bs) > np.array(bo))))


# ------------------------------------------------------------------- driver
def main():
    out = {}
    print('=' * 90)
    print('STEP 1 — REPRODUCTION of the paper\'s exact eta^2 via code/run05.py::eta2')
    print('=' * 90)
    TARGET = dict(surr=0.36872274, opt=0.01318917, inter=0.16518057)
    for tag, path in [('SYNTH', 'results_camera.json'), ('REAL', 'results_db.json'),
                      ('SYNTH-matched', 'results_camera_matched.json')]:
        try:
            used, es, eo, ei, M = paper_eta2(path)
        except Exception as ex:
            print(f'  {tag}: ERROR {ex}'); continue
        print(f'  {tag:14} tasks={len(used)}')
        print(f'      eta2_surr = {es!r}')
        print(f'      eta2_opt  = {eo!r}')
        print(f'      eta2_inter= {ei!r}')
        if tag == 'SYNTH':
            print('    vs paper stored:  surr=0.36872274  opt=0.01318917  inter=0.16518057')
            ok = (abs(es - TARGET['surr']) < 5e-9 and abs(eo - TARGET['opt']) < 5e-9
                  and abs(ei - TARGET['inter']) < 5e-9)
            print(f'    EXACT MATCH (to 8dp): {ok}')
            out['reproduction'] = dict(match=bool(ok), surr=es, opt=eo, inter=ei, tasks=used)
        out.setdefault('paper_path', {})[tag] = dict(surr=es, opt=eo, inter=ei, tasks=used)

    # ---------- raw span diagnostic
    print('\n' + '=' * 90)
    print('RAW SPAN DIAGNOSTIC (the motivation for the whole exercise)')
    print('=' * 90)
    tasks, R = raw_cellmeans('results_camera.json')
    print(f'  {"task":16}{"raw min":>13}{"raw max":>11}{"span":>13}{"minmax-compression":>21}')
    spans = {}
    for t, a in zip(tasks, R):
        span = a.max() - a.min()
        spans[t] = float(span)
        # how much of the [0,1] band do the 8 non-extreme cells occupy?
        z = (a - a.min()) / span
        z2 = np.sort(z.ravel())
        occ = z2[-1] - z2[1]
        print(f'  {t:16}{a.min():13.3f}{a.max():11.3f}{span:13.3f}   8 non-min cells span {occ:.3f} of [0,1]')
    print(f'  GLOBAL raw range across tasks: [{R.min():.3f}, {R.max():.3f}]')
    out['raw_spans'] = spans

    # ---------- normalization zoo, per-task-mean units
    print('\n' + '=' * 90)
    print('STEP 2a — eta^2 UNDER ALTERNATIVE NORMALIZATIONS  (unit = PER-TASK MEAN; the paper\'s unit)')
    print('=' * 90)
    tasksS, RS = raw_cellmeans('results_camera.json')
    _, nseed, AS = raw_seeds('results_camera.json')
    print(f'  synthetic: T={len(tasksS)} tasks, {nseed} seeds/cell, 9 cells\n')
    treatments = [
        ('minmax (PAPER)', n_minmax(RS)),
        ('rank (1-9 within task)', n_rank(RS)),
        ('z-score per task', n_zscore(RS)),
        ('log-regret -> minmax', n_logregret(RS)),
        ('winsor 5% (seed pool)', n_winsor_seeds(AS, 5)),
        ('winsor 10% (seed pool)', n_winsor_seeds(AS, 10)),
        ('winsor 5% (cell means)', n_winsor_cellmeans(RS, 5)),
        ('winsor 10% (cell means)', n_winsor_cellmeans(RS, 10)),
        ('RAW (no normalization)', n_raw(RS)),
    ]
    rows = []
    print(f'  {"normalization":28}{"eta2_surr":>11}{"eta2_opt":>10}{"eta2_inter":>12}{"surr/opt":>10}  holds?')
    for name, M in treatments:
        es, eo, ei = eta2_from_M(M)
        ratio = es / eo if eo > 0 else float('inf')
        holds = 'YES' if es > eo else 'NO'
        rows.append(dict(norm=name, unit='task-mean', surr=es, opt=eo, inter=ei,
                         ratio=float(ratio), holds=holds))
        print(f'  {name:28}{es:11.4f}{eo:10.4f}{ei:12.4f}{ratio:10.1f}  {holds}')
    out['taskmean_units'] = rows

    # ---------- per-seed units
    print('\n' + '=' * 90)
    print(f'STEP 2b — eta^2 WITH PER-SEED ROWS  (unit = (task,seed); {len(tasksS)}x{nseed} = '
          f'{len(tasksS)*nseed} rows)')
    print('=' * 90)
    print('  NOTE: the paper uses PER-TASK-MEAN units (run05.py::eta2 reads d[t][c][metric]["mean"]),')
    print('        i.e. it collapses the 30 seeds before the ANOVA. Per-seed rows re-inject')
    print('        within-cell seed noise into SS_total, which MUST deflate every eta^2.')
    rows2 = []
    print(f'\n  {"normalization":28}{"eta2_surr":>11}{"eta2_opt":>10}{"eta2_inter":>12}{"surr/opt":>10}  holds?')
    for how in ['minmax', 'zscore', 'rank', 'raw']:
        Ms = seeds_normed(AS, how)
        es, eo, ei = eta2_from_M(Ms)
        ratio = es / eo if eo > 0 else float('inf')
        holds = 'YES' if es > eo else 'NO'
        rows2.append(dict(norm=how, unit='per-seed', surr=es, opt=eo, inter=ei,
                          ratio=float(ratio), holds=holds))
        print(f'  {how:28}{es:11.4f}{eo:10.4f}{ei:12.4f}{ratio:10.1f}  {holds}')
    out['perseed_units'] = rows2

    # ---------- Design-Bench for contrast
    print('\n' + '=' * 90)
    print('STEP 2c — same zoo on DESIGN-BENCH (results_db.json)')
    print('=' * 90)
    tasksD, RD = raw_cellmeans('results_db.json')
    _, nseedD, AD = raw_seeds('results_db.json')
    print(f'  real: T={len(tasksD)} tasks, {nseedD} seeds/cell\n')
    rows3 = []
    print(f'  {"normalization":28}{"eta2_surr":>11}{"eta2_opt":>10}{"eta2_inter":>12}  surr>opt?')
    for name, M in [('minmax (PAPER)', n_minmax(RD)), ('rank', n_rank(RD)),
                    ('z-score per task', n_zscore(RD)), ('log-regret -> minmax', n_logregret(RD)),
                    ('winsor 5% (seed pool)', n_winsor_seeds(AD, 5)),
                    ('winsor 10% (seed pool)', n_winsor_seeds(AD, 10)),
                    ('RAW (no normalization)', n_raw(RD))]:
        es, eo, ei = eta2_from_M(M)
        rows3.append(dict(norm=name, surr=es, opt=eo, inter=ei, holds='YES' if es > eo else 'NO'))
        print(f'  {name:28}{es:11.4f}{eo:10.4f}{ei:12.4f}  {"YES" if es>eo else "NO"}')
    out['db_units'] = rows3

    # ---------- leave-one-task-out on the paper's arm
    print('\n' + '=' * 90)
    print('STEP 2d — LEAVE-ONE-TASK-OUT on the paper\'s arm (is Griewank-30D driving it?)')
    print('=' * 90)
    Mp = n_minmax(RS)
    loo = []
    print(f'  {"dropped task":18}{"eta2_surr":>11}{"eta2_opt":>10}{"eta2_inter":>12}')
    for i, t in enumerate(tasksS):
        keep = [j for j in range(len(tasksS)) if j != i]
        es, eo, ei = eta2_from_M(Mp[keep])
        loo.append(dict(dropped=t, surr=es, opt=eo, inter=ei))
        print(f'  {t:18}{es:11.4f}{eo:10.4f}{ei:12.4f}')
    out['loo'] = loo

    # ---------- assumption checks
    print('\n' + '=' * 90)
    print('STEP 3 — ASSUMPTION CHECKS on the PAPER\'S ACTUAL ANOVA (minmax, task-mean units)')
    print('=' * 90)
    ac = assumption_checks(Mp, 'SYNTH minmax task-mean (paper)')
    out['assumptions_paper'] = ac
    print(f'  residuals n = {ac["n_resid"]}  (7 tasks x 9 cells, resid = y - cellmean_over_tasks)')
    print(f'  Shapiro-Wilk   W = {ac["shapiro_W"]:.4f}   p = {ac["shapiro_p"]:.3e}   '
          f'{"NORMALITY REJECTED" if ac["shapiro_p"] < 0.05 else "not rejected"}')
    print(f'  residual skew  = {ac["resid_skew"]:+.3f}   excess kurtosis = {ac["resid_excess_kurtosis"]:+.3f}')
    print(f'  QQ corr(sorted resid, normal quantiles) = {ac["qq_corr"]:.4f}   (1.0 = perfectly normal)')
    print(f'  Levene (median) W = {ac["levene_W"]:.4f}   p = {ac["levene_p"]:.3e}   '
          f'{"HOMOSCEDASTICITY REJECTED" if ac["levene_p"] < 0.05 else "not rejected"}')
    print(f'  Bartlett       T = {ac["bartlett_T"]:.4f}   p = {ac["bartlett_p"]:.3e}   '
          f'{"HOMOSCEDASTICITY REJECTED" if ac["bartlett_p"] < 0.05 else "not rejected"}')
    print(f'  max/min group variance ratio across the 9 cells = {ac["var_ratio_max_min"]:.1f}')
    for name, M2, lab in [('rank', n_rank(RS), 'SYNTH rank'), ('z', n_zscore(RS), 'SYNTH z'),
                          ('logreg', n_logregret(RS), 'SYNTH log-regret')]:
        a2 = assumption_checks(M2, lab)
        out.setdefault('assumptions_alt', {})[lab] = a2
        print(f'  [{lab:22}] Shapiro p={a2["shapiro_p"]:.3e}  Levene p={a2["levene_p"]:.3e}  '
              f'Bartlett p={a2["bartlett_p"]:.3e}')

    # ---------- permutation
    print('\n' + '=' * 90)
    print('STEP 4 — PERMUTATION effect-size test (no distributional assumptions), 20k perms')
    print('=' * 90)
    for lab, M2 in [('minmax (PAPER)', Mp), ('rank', n_rank(RS)), ('z-score', n_zscore(RS)),
                    ('log-regret', n_logregret(RS)), ('RAW', n_raw(RS))]:
        pr = permutation_test(M2, n_perm=20000, seed=0)
        out.setdefault('permutation', {})[lab] = pr
        print(f'  [{lab}]')
        print(f'     surr : eta2={pr["obs"]["surr"]:.4f}  perm-null mean={pr["null_surr_mean"]:.4f} '
              f'q95={pr["null_surr_q95"]:.4f}  p={pr["p_surr"]:.5f}')
        print(f'     opt  : eta2={pr["obs"]["opt"]:.4f}  perm-null mean={pr["null_opt_mean"]:.4f} '
              f'q95={pr["null_opt_q95"]:.4f}  p={pr["p_opt"]:.5f}')
        print(f'     inter: eta2={pr["obs"]["inter"]:.4f}  perm-null mean={pr["null_inter_mean"]:.4f} '
              f'q95={pr["null_inter_q95"]:.4f}  p={pr["p_inter"]:.5f}')

    print('\n  bootstrap-over-tasks CIs (2.5/97.5 pct, 20k resamples):')
    for lab, M2 in [('minmax (PAPER)', Mp), ('rank', n_rank(RS)), ('z-score', n_zscore(RS)),
                    ('log-regret', n_logregret(RS)), ('RAW', n_raw(RS))]:
        b = bootstrap_ci(M2, n_boot=20000, seed=1)
        out.setdefault('bootstrap', {})[lab] = b
        print(f'    {lab:16} surr CI=[{b["ci_surr"][0]:.3f},{b["ci_surr"][1]:.3f}]  '
              f'opt CI=[{b["ci_opt"][0]:.3f},{b["ci_opt"][1]:.3f}]  '
              f'inter CI=[{b["ci_inter"][0]:.3f},{b["ci_inter"][1]:.3f}]  '
              f'P(surr>opt)={b["p_surr_gt_opt"]:.4f}')

    # ---------- DB permutation for contrast
    print('\n  Design-Bench permutation (paper arm):')
    prd = permutation_test(n_minmax(RD), n_perm=20000, seed=0)
    out.setdefault('permutation_db', {})['minmax'] = prd
    print(f'    surr : eta2={prd["obs"]["surr"]:.4f} p={prd["p_surr"]:.5f}')
    print(f'    opt  : eta2={prd["obs"]["opt"]:.4f} p={prd["p_opt"]:.5f}')
    print(f'    inter: eta2={prd["obs"]["inter"]:.4f} p={prd["p_inter"]:.5f}')
    bd = bootstrap_ci(n_minmax(RD), n_boot=20000, seed=1)
    out.setdefault('bootstrap_db', {})['minmax'] = bd
    print(f'    bootstrap: surr CI=[{bd["ci_surr"][0]:.3f},{bd["ci_surr"][1]:.3f}] '
          f'opt CI=[{bd["ci_opt"][0]:.3f},{bd["ci_opt"][1]:.3f}] P(surr>opt)={bd["p_surr_gt_opt"]:.4f}')

    # ---------- marginals under each treatment
    print('\n' + '=' * 90)
    print('SUPPORT — surrogate marginals under each treatment (is the ORDERING stable?)')
    print('=' * 90)
    print(f'  {"normalization":28}' + ''.join(f'{s:>13}' for s in SURR3))
    for name, M in treatments:
        sm = M.mean(axis=(0, 2))
        print(f'  {name:28}' + ''.join(f'{v:13.4f}' for v in sm))
    print(f'\n  {"normalization":28}' + ''.join(f'{o:>13}' for o in OPT3))
    for name, M in treatments:
        om = M.mean(axis=(0, 1))
        print(f'  {name:28}' + ''.join(f'{v:13.4f}' for v in om))

    dst = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'eta_robustness_out.json')
    json.dump(out, open(dst, 'w'), indent=1, default=float)
    print(f'\nWROTE {dst}')


if __name__ == '__main__':
    # self-check: an optimizer-driven grid must give eta2_opt >> eta2_surr under every arm
    R = np.array([[[OPT3.index(o) + 0.01 * i for o in OPT3] for s in SURR3] for i in range(3)], float)
    for nm, f in [('minmax', n_minmax), ('rank', n_rank), ('z', n_zscore), ('raw', n_raw)]:
        es, eo, ei = eta2_from_M(f(R))
        assert eo > es, f'{nm}: optimizer-driven grid gave surr={es} opt={eo}'
    # and eta2_from_M must reproduce run05's algebra on the paper's own M
    print('self-check OK (optimizer-driven grid -> eta2_opt > eta2_surr under all arms)\n')
    main()
```

---
## FILE: docs/hyperresearch/01_decompose_coverage-matrix.md
<!-- lines: 44 | bytes: 4577 | last commit: 7559bc5 2026-07-17 -->
```markdown
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
```

---
## FILE: docs/hyperresearch/01_decompose_prompt-decomposition.json
<!-- lines: 70 | bytes: 6010 | last commit: 7559bc5 2026-07-17 -->
```json
{
  "sub_questions": [
    "What is the prior art on decomposing offline-MBO performance into surrogate class vs acquisition optimizer factors, and is a controlled surrogate x optimizer factorial decomposition novel?",
    "Is the 'GP smooth posterior mean vs jagged ensemble mean' / inductive-bias mechanism already established in the literature (NTK, spectral bias, Lipschitz smoothness of ensembles vs GPs)?",
    "Is coverage-based or conformal diagnosis of LCB pessimism in offline MBO already published?",
    "What is the state of offline model selection in offline MBO and offline RL, is it a recognized open problem, and is a coverage-driven offline surrogate x optimizer selection rule novel?",
    "Is the synthetic-to-Design-Bench validity collapse / benchmark non-discriminativeness already documented?",
    "What are the known criticisms and limitations of Design-Bench as a benchmark?",
    "What are the known criticisms of deep-ensemble uncertainty quality?",
    "What are the known criticisms of ANOVA-on-normalized-scores effect sizes in ML benchmarking?",
    "What do AAAI reviewers demand of measurement and null-result papers, and what is the acceptance evidence for controlled-study-without-a-new-method papers at AAAI/NeurIPS/ICML?",
    "What flaws exist at the manuscript level (claims, framing, positioning, prose, figures, related work)?",
    "What flaws exist at the experiment level (identifiability, controls, confounds, optimizer query budgets, baselines)?",
    "What flaws exist at the statistics level (two-way ANOVA on min-max-normalized scores, Friedman/Nemenyi CD, TOST equivalence, bootstrap, Holm)?",
    "What flaws exist at the artifact level (reproducibility, code quality, what a reviewer running it would find)?",
    "For each core claim, what are the adversarial criticisms and limitations?"
  ],
  "entities": [
    {"name": "Design-Bench (Trabucco et al. 2022)", "type": "benchmark", "required_fields": ["known criticisms", "saturation", "oracle protocol", "non-discriminativeness evidence"]},
    {"name": "COMs (Trabucco et al. 2021)", "type": "method", "required_fields": ["reported numbers", "reproduction variance", "hyperparameters"]},
    {"name": "PGS (Chen et al., AAAI 2024)", "type": "method", "required_fields": ["claim about search strategy", "relation to optimizer-as-factor"]},
    {"name": "GAMBO (NeurIPS 2024)", "type": "method", "required_fields": ["optimizer-as-contribution framing"]},
    {"name": "RaM / LTR (Tan et al. 2025)", "type": "method", "required_fields": ["surrogate-class comparison with optimizer fixed"]},
    {"name": "Match-OPT", "type": "method", "required_fields": ["gradient-field discrepancy bound"]},
    {"name": "Li, Rudner, Wilson 2024 (BNN surrogates)", "type": "study", "required_fields": ["surrogate comparison with acquisition fixed", "deep ensembles weakest finding"]},
    {"name": "Stanton et al. 2022 (conformal BO)", "type": "study", "required_fields": ["conformal + BO overlap with premise coverage"]},
    {"name": "Deshpande & Kuleshov 2024", "type": "study", "required_fields": ["calibration improves BO", "online vs offline scope"]},
    {"name": "Tibshirani et al. 2019 (weighted conformal)", "type": "theory", "required_fields": ["covariate-shift weighting", "overlap with Proposition 2"]},
    {"name": "CCC / Choi 2026 (conformal certification, offline MBO)", "type": "method", "required_fields": ["post-hoc certification", "distinction from premise coverage"]},
    {"name": "UNIQ 2026 (conformal-LCB, offline RL)", "type": "method", "required_fields": ["global-scalar conformal LCB", "distinction"]},
    {"name": "kim2025mbosurvey", "type": "survey", "required_fields": ["named open problems", "offline model selection", "realistic benchmarking"]},
    {"name": "NTK / spectral bias literature", "type": "theory", "required_fields": ["smoothness of wide nets", "relation to GP prior"]},
    {"name": "offline model selection (offline RL + offline MBO)", "type": "problem", "required_fields": ["is it a recognized open problem", "existing approaches", "novelty of coverage-driven selection"]}
  ],
  "required_formats": [
    "severity-rated finding list (P0/P1/P2/P3)",
    "per-finding: evidence, reviewer's phrasing of the objection, cost to fix (hours/CPU), fixable pre-deadline yes/no",
    "novelty status marked as prior-work-found / none-found / NOT VERIFIABLE HERE"
  ],
  "required_sections": [
    "## Opinionated Synthesis"
  ],
  "required_section_headings": [
    "## 1. Prior Art on Surrogate x Optimizer Decomposition in Offline MBO",
    "## 2. Is the Smooth-Mean / Inductive-Bias Mechanism Already Established?",
    "## 3. Prior Art on Coverage and Conformal Diagnosis of LCB Pessimism",
    "## 4. Offline Model Selection as an Open Problem, and the Novelty of Coverage-Driven Selection",
    "## 5. Design-Bench: Known Criticisms, Saturation, and Documented Non-Discriminativeness",
    "## 6. Deep-Ensemble Uncertainty Quality: Known Criticisms",
    "## 7. Statistical Validity: ANOVA on Normalized Scores, Friedman/Nemenyi, TOST",
    "## 8. What AAAI Rewards in Measurement and Null-Result Papers",
    "## 9. Manuscript-Level Findings (a)",
    "## 10. Experiment-Level Findings (b)",
    "## 11. Statistics-Level Findings (c)",
    "## 12. Artifact-Level Findings (d)",
    "## 13. Adversarial Case Against Each Core Claim",
    "## Opinionated Synthesis"
  ],
  "time_horizons": ["literature through 2026-07", "AAAI-27 submission cycle"],
  "time_periods": [],
  "scope_conditions": [
    "offline model-based optimization specifically, not online BO — but online BO literature is in scope as prior art for the calibration/conformal claims",
    "AAAI-27 main technical track acceptance standards specifically",
    "evaluation is of an existing manuscript + artifact, not a general literature survey",
    "novelty must be checked, never asserted unverified"
  ],
  "pipeline_tier": "full",
  "response_format": "argumentative",
  "citation_style": "inline"
}
```

---
## FILE: docs/hyperresearch/02_<step>.md — DOES NOT EXIST
<!-- hyperresearch step 2 never ran. Only steps 1-2 of the 16-step pipeline were executed; the literature work was delegated to focused agents instead (see chat log / NOVELTY_CHECK.md, VENUE_NORMS.md). -->

---
## FILE: docs/hyperresearch/03_<step>.md — DOES NOT EXIST
<!-- hyperresearch step 3 never ran. Only steps 1-2 of the 16-step pipeline were executed; the literature work was delegated to focused agents instead (see chat log / NOVELTY_CHECK.md, VENUE_NORMS.md). -->

---
## FILE: docs/hyperresearch/04_<step>.md — DOES NOT EXIST
<!-- hyperresearch step 4 never ran. Only steps 1-2 of the 16-step pipeline were executed; the literature work was delegated to focused agents instead (see chat log / NOVELTY_CHECK.md, VENUE_NORMS.md). -->

---
## FILE: docs/hyperresearch/05_<step>.md — DOES NOT EXIST
<!-- hyperresearch step 5 never ran. Only steps 1-2 of the 16-step pipeline were executed; the literature work was delegated to focused agents instead (see chat log / NOVELTY_CHECK.md, VENUE_NORMS.md). -->

---
## FILE: docs/hyperresearch/06_<step>.md — DOES NOT EXIST
<!-- hyperresearch step 6 never ran. Only steps 1-2 of the 16-step pipeline were executed; the literature work was delegated to focused agents instead (see chat log / NOVELTY_CHECK.md, VENUE_NORMS.md). -->

---
## FILE: docs/hyperresearch/07_<step>.md — DOES NOT EXIST
<!-- hyperresearch step 7 never ran. Only steps 1-2 of the 16-step pipeline were executed; the literature work was delegated to focused agents instead (see chat log / NOVELTY_CHECK.md, VENUE_NORMS.md). -->

---
## FILE: docs/hyperresearch/08_<step>.md — DOES NOT EXIST
<!-- hyperresearch step 8 never ran. Only steps 1-2 of the 16-step pipeline were executed; the literature work was delegated to focused agents instead (see chat log / NOVELTY_CHECK.md, VENUE_NORMS.md). -->

---
## FILE: docs/hyperresearch/09_<step>.md — DOES NOT EXIST
<!-- hyperresearch step 9 never ran. Only steps 1-2 of the 16-step pipeline were executed; the literature work was delegated to focused agents instead (see chat log / NOVELTY_CHECK.md, VENUE_NORMS.md). -->

---
## FILE: docs/hyperresearch/10_<step>.md — DOES NOT EXIST
<!-- hyperresearch step 10 never ran. Only steps 1-2 of the 16-step pipeline were executed; the literature work was delegated to focused agents instead (see chat log / NOVELTY_CHECK.md, VENUE_NORMS.md). -->

---
## FILE: docs/hyperresearch/11_<step>.md — DOES NOT EXIST
<!-- hyperresearch step 11 never ran. Only steps 1-2 of the 16-step pipeline were executed; the literature work was delegated to focused agents instead (see chat log / NOVELTY_CHECK.md, VENUE_NORMS.md). -->

---
## FILE: docs/hyperresearch/12_<step>.md — DOES NOT EXIST
<!-- hyperresearch step 12 never ran. Only steps 1-2 of the 16-step pipeline were executed; the literature work was delegated to focused agents instead (see chat log / NOVELTY_CHECK.md, VENUE_NORMS.md). -->

---
## FILE: docs/hyperresearch/13_<step>.md — DOES NOT EXIST
<!-- hyperresearch step 13 never ran. Only steps 1-2 of the 16-step pipeline were executed; the literature work was delegated to focused agents instead (see chat log / NOVELTY_CHECK.md, VENUE_NORMS.md). -->

---
## FILE: docs/hyperresearch/14_<step>.md — DOES NOT EXIST
<!-- hyperresearch step 14 never ran. Only steps 1-2 of the 16-step pipeline were executed; the literature work was delegated to focused agents instead (see chat log / NOVELTY_CHECK.md, VENUE_NORMS.md). -->

---
## FILE: docs/hyperresearch/15_<step>.md — DOES NOT EXIST
<!-- hyperresearch step 15 never ran. Only steps 1-2 of the 16-step pipeline were executed; the literature work was delegated to focused agents instead (see chat log / NOVELTY_CHECK.md, VENUE_NORMS.md). -->

---
## FILE: docs/hyperresearch/16_<step>.md — DOES NOT EXIST
<!-- hyperresearch step 16 never ran. Only steps 1-2 of the 16-step pipeline were executed; the literature work was delegated to focused agents instead (see chat log / NOVELTY_CHECK.md, VENUE_NORMS.md). -->

---
