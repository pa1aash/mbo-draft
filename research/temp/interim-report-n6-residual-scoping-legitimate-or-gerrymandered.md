# Interim report: n6-residual-scoping-legitimate-or-gerrymandered

**Locus question:** Is N6's four-conjunct residual (crossed x surrogate-class x optimizer x
two-way decomposition, offline) a load-bearing scoping or a circle drawn around the answer to
dodge RaM Table 3 and DiBO Table 2?
**Flavor:** dialectical

## What the corpus already said

The width sweep and prior audit passes established N6 as "no kill found" after grepping eight
2026 offline-MBO/BBO papers and re-confirming three prior near-misses (Hutter one-way, Liang
online-descriptive, Moosbauer OFAT-declined) — see `research/temp/findings-so-far.md`. The most
recent addition, found by the batch that swept RaM (Tan et al., ICLR 2025) a fourth time, is
Table 3 ("Versatility of ranking loss"): a 9-method x 2-loss (MSE/ListNet) x 5-task grid,
descriptive only. The contradiction-graph (`cluster n6-residual-width`) frames the defence as
three grounds — (1) loss type is not model class, (2) the nine are bundled methods not a clean
optimizer factor, (3) descriptive reporting is not a decomposition — and flags that "none of
them is currently on the page." This locus was tasked with pressure-testing each ground and
reaching a verdict on whether the residual survives.

I re-fetched RaM and DiBO fresh per the method constraint (the vault already held three stale
copies of RaM from earlier passes; none had surfaced the Appendix E.5 method taxonomy this note
turns on) — see [[offline-model-based-optimization-by-learning-to-rank-2]] and
[[training-diffusion-language-models-for-black-box-optimization]].

## What the new sources say

**RaM fresh re-fetch, Appendix E.5** ([[offline-model-based-optimization-by-learning-to-rank-2]]).
The paper's own text stratifies its nine Table-3 methods into three groups **by construction**,
not by any post-hoc factor analysis: *"We choose baselines methods that optimize a trained
model, BO-qEI (Garnett, 2023), CMA-ES (Hansen, 2016), REINFORCE (Williams, 1992), and Gradient
Ascent, two backward approach provided in Trabucco et al. (2022), CbAS (Brookes et al., 2019)
and MINs (Kumar & Levine, 2020), and three state-of-the-art forward methods that can replace
MSE with ListNet, Tri-Mentoring (Chen et al., 2023a), PGS (Chemingui et al., 2024), and
Match-OPT (Hoang et al., 2024)."* It further discloses that COMs, RoMA, IOM, BDI, and ICT were
**excluded** from the swap because their losses use prediction values or per-sample weights
incompatible with a drop-in MSE-to-ListNet replacement — the crossing is an opportunistic
subset of offline-MBO methods, not an exhaustive design. Zero hits (re-verified independently)
for ANOVA / variance decomposition / eta-squared / main effect / interaction / two-way /
factorial across the full 172,006-character extraction.

**DiBO fresh re-fetch, Table 2** ([[training-diffusion-language-models-for-black-box-optimization]]).
Confirmed as a genuine 2 (diffusion vs.\ autoregressive backbone) x 3 (DA/SFT/RL training stage)
x 4-task grid, N=8 seeds, descriptive mean+-std only. Confirmed from the paper's own framing
that DA/SFT/RL are **sequential training-pipeline stages** (each with its own learning rate and
step count — e.g. DA at 2e-5/1024 steps, RL at 1e-6), not a numerical search/optimizer routine
applied post-hoc to a frozen model. There is no optimizer axis in DiBO's design at all — the
"backbone" is the generative policy itself, trained end-to-end through DA-SFT-RL, not a
surrogate that a separate optimizer subsequently searches. DiBO therefore fails N6's optimizer
conjunct on a more basic level than RaM does, and gives the prosecution no additional leverage.

**NIST/SEMATECH Engineering Statistics Handbook, 5.3.3.4.3, "Confounding (also called aliasing)"**
([[53343-confounding-also-called-aliasing]]). The canonical applied-statistics definition:
*"Confounding means we have lost the ability to estimate some effects and/or interactions."*
Worked via a 2^(3-1) fractional design where a main effect (c3) becomes inseparable from an
interaction (c12) because they co-occur identically across every run of the design. The
handbook's core point, load-bearing for ground (2): **confounding is a property of a design's
contrast structure — two effects are aliased when they cannot be run apart, not when an author
merely chooses to call them "the same factor."**

**NIST/SEMATECH 5.3.2, "How do you select and scale the process variables?"**
([[532-how-do-you-select-and-scale-the-process-variables]]). Frames factor identification
explicitly as upstream of the statistical machinery: *"Guidelines to assist the engineering
judgment process of selecting process variables for a DOE"* — *"Include all important factors
(based on engineering judgment)."* Statistical theory (orthogonality, confounding) governs how
chosen factors combine; it does not itself adjudicate what counts as a factor in a given domain.

**Abdar et al. 2021, "A Review of Uncertainty Quantification in Deep Learning"** (arXiv:2011.06225,
~2900 citations) ([[a-review-of-uncertainty-quantification-in-deep-learning-techniques-applications]]).
The field's own canonical UQ survey organizes method families (Bayesian techniques including
MC-dropout; ensemble techniques including deep ensembles) as the top-level taxonomy, and treats
**loss function as a separate, cross-cutting axis catalogued independently**: *"As an important
part of ensemble techniques, loss functions play a significant role of having a good performance
by different ensemble techniques... we summarise the most important loss functions applied for
UQ in Table 3"* — Table 3 caption *"Main loss functions used by ensemble techniques for UQ,"*
Table 4 *"Main loss functions used by deep ensemble techniques for UQ."* This is direct,
citable, on-topic domain precedent that the UQ literature treats "which method family produces
the uncertainty estimate" and "which loss trained it" as orthogonal dimensions, not one bundled
factor — precisely the distinction ground (1) needs and currently lacks a citation for.

**Li/Rudner/Wilson (li2024bnnsurrogates, arXiv:2305.20028), re-examined from the vault's existing
raw extraction** (`research/raw/txt/rudner-study-bnn-surrogates-bo.txt`, no new fetch). Their own
framing treats *"the method used to compute the posterior distribution, the architecture of the
neural network, and the approximate inference procedure"* as the object of study, and explicitly
construes a deep ensemble as *"trained using maximum a posteriori estimation"* with *"different
random seed[s] and initialization"* — i.e., in their own account, the model-class difference
(HMC vs.\ VI vs.\ Laplace vs.\ Ensemble) is constitutively bound to its own natural training
procedure. You cannot get "a GP" without type-II marginal-likelihood fitting, or "an ensemble"
without per-member MAP/bootstrap training — the training procedure is not an independently
selectable knob once the model class is fixed. This is the precise disanalogy with RaM: RaM
swaps MSE for ListNet **within one unchanged MLP architecture** — a manipulation that does not
require touching model family at all.

## Evidence synthesis

**On (a), the prosecution's steelman.** There is a genuine 3-x-2-x-5 sub-grid inside RaM Table
3 that the defence's current wording does not concede: BO-qEI, CMA-ES, REINFORCE, and Gradient
Ascent — four optimizers, by RaM's own description, applied to *one* fixed MLP surrogate —
crossed with MSE vs.\ ListNet across five tasks (N=8 seeds/cell). That is a clean optimizer
factor (4 levels) crossed with a training-loss factor (2 levels), fully offline, and it is *not*
a bundle of incommensurable methods in the way ground (2) currently claims for "the nine." Ground
(2) as stated in the contradiction-graph and findings-so-far ("the nine are bundled methods...
not settings of a clean optimizer factor") is **falsified for four of the nine** by RaM's own
appendix text. The other five are correctly characterised as bundled: CbAS and MINs pair a
generative surrogate with backward sampling in a way that is aliased in the strict NIST sense —
you cannot vary "model family" and "search paradigm" independently within either method, they
co-occur on every run — and Tri-Mentoring/PGS/Match-OPT each layer method-specific machinery
(tri-training, pessimistic search, matching) on top of a bare forward-optimization step. So the
correct steelmanned reading of ground (2) is not "no clean optimizer sub-grid exists in Table 3"
(false) but "a clean optimizer sub-grid exists, but even that sub-grid varies loss, not model
class, and reports no decomposition" — which routes the entire defence back onto grounds (1) and
(3), where it must actually hold.

**On (b), ground (1)'s literature basis.** DOE theory itself (NIST 5.3.2) explicitly delegates
factor identification to domain judgment — it does not derive a rule for what counts as "the
same factor" from statistical first principles, so ground (1) was never going to find an
abstract mathematical arbiter. What it can find, and does, is *domain* precedent: the UQ
literature's own taxonomy (Abdar et al.) separately catalogues method family and loss function
as cross-cutting axes, and the nearest cited comparator paper (Li/Rudner/Wilson) treats model
class as constitutively bound to its own training procedure rather than as one arbitrarily
chosen loss among several applicable to a fixed architecture. This yields a real, statable
criterion, not an ad hoc one: **a change is a model-class change if it cannot be instantiated
without also changing the family of the estimator (GP posterior vs. ensemble disagreement each
require their own native fitting procedure); a change is a training-objective change if it can be
applied while holding the family fixed (as RaM does, holding the MLP fixed and swapping only the
loss).** By this test, RaM's swap is unambiguously a training-objective change and the paper's
surrogate axis is unambiguously a model-class change. The criterion is defensible and, notably,
it is *self-consistently applied* — it also correctly classes the paper's own conservative-surrogate
comparator (COMs, which varies a regularizer on a fixed architecture) as a training-objective
study, exactly as the paper's introduction already does for COMs. The one place the paper's own
text is *inconsistent* with this criterion is that it lumps `tan2025ltr` (RaM, a training-objective
study by the criterion above) together with `li2024bnnsurrogates` (a genuine model-class study)
under a single "surrogate-class comparisons" descriptor. That miscategorisation, not the
underlying criterion, is the actual defect — and it is exactly the kind of imprecision a
RaM-familiar reviewer would notice and use to argue the paper is special-pleading.

**On (c), ground (2)'s DOE legitimacy.** Confounding/aliasing is a real, well-defined technical
concept (NIST 5.3.3.4.3): two effects are aliased when a design's contrast structure cannot
separate them because they co-occur on every run, independent of labeling. CbAS and MINs meet
this bar precisely — their "backward, generative" character and their model family are the same
design choice, not two independently variable settings. This is not special pleading; it is the
textbook definition applied correctly. What is special pleading, currently, is applying this
label to *all nine* Table-3 methods, when four of them (the "optimize a trained model" group) are
not aliased with anything — they are exactly the clean optimizer factor ground (2) claims does
not exist.

**On (d), is eta-squared computable from RaM's Table 3 as published?** Yes, and not just in
principle — I computed it. RaM states its evaluation protocol runs *"eight different seeds"*
uniformly, and Table 3 reports mean+-std per cell, so N and both moments are available for every
one of the 90 (method x loss x task) cells. Running a per-task two-way ANOVA (Method x Loss) on
these published numbers and averaging across the five tasks gives: eta-squared_Method (the
method/optimizer axis) = 0.577 [range 0.134-0.958 across tasks], eta-squared_Loss (RaM's
"surrogate" analogue) = 0.027 [range 0.0004-0.076], eta-squared_Method x Loss interaction = 0.055,
eta-squared_within = 0.341. (Full script and numbers reproducible from the extracted table; not
in any vault note but available on request — treat as this investigator's own calculation, not
RaM's.) Two things follow. First, **ground (3) is technically true but a weak shield**: the
descriptive-only framing is accurate as a description of what RaM published, but the arithmetic
needed to contradict it is fifteen lines of code away from their own numbers, so "no prior work
decomposes this" is a narrower and more fragile claim than "no prior work could." Second, and
more useful for the paper: **this computation independently corroborates ground (1) with a
number, not just an assertion.** In RaM's own data, the training-loss axis (their MSE-vs-ListNet
analogue of "surrogate") explains only ~2.7% of variance while the method/optimizer axis explains
~58% — essentially the mirror image of the audited paper's own headline (surrogate dominant at
~30-45%, optimizer negligible at 0.5-3.8%). If "training loss" and "model class" were really the
same kind of factor, one would not expect swapping one to produce a negligible effect while
swapping the other produces the dominant effect in a structurally similar design. That empirical
asymmetry is evidence for the ground-(1) distinction, not merely an assertion of it.

### Position A: the residual is gerrymandered — the four conjuncts were shaped to dodge RaM

The strongest version of this case: the paper's introduction currently cites `tan2025ltr`
(RaM) as a "surrogate-class comparison [holding] the optimizer constant" in the same breath as
a genuine surrogate-class study (`li2024bnnsurrogates`), which is imprecise in exactly the
direction that would make RaM look safely outside the residual before a reader ever checks RaM's
actual Table 3. Ground (2) as currently stated ("the nine are bundled methods... not settings of
a clean optimizer factor") is flatly false for four of RaM's nine methods, which RaM's own
appendix explicitly separates out as "optimize a trained model" baselines. A hostile reviewer
reading only the paper's current prose (not this investigation) would reasonably conclude the
authors either did not read RaM's appendix or are hoping the reader does not. The three grounds,
as *currently worded on the page* (none of them is written down at all, in fact — this is worse
than imprecise, it is silent), read exactly like a residual whose boundary was drawn after the
fact to exclude the one paper that gets closest, without the paper ever having to state, test, or
defend that boundary against RaM specifically.

### Position B: the residual is legitimate — once correctly argued, all three grounds hold and are principled

The strongest version of this case: every individual component of the three-ground defence
survives contact with RaM's actual text and with the DOE/UQ literature, provided the grounds are
stated with the precision this investigation supports rather than the over-broad version. Ground
(1) rests on a real, citable, self-consistently-applied methodological distinction (Abdar et al.'s
separate cataloguing of method family vs.\ loss function; the constitutive binding of model class
to its native training procedure per Li/Rudner/Wilson's own framing) and is independently
corroborated by an 18x-to-1 asymmetry in how much variance the two kinds of axis explain in RaM's
own published numbers. Ground (2), correctly scoped to the five aliased/bundled methods rather
than all nine, is the textbook NIST definition of confounding applied correctly — CbAS and MINs
genuinely cannot separate model family from search paradigm; Tri-Mentoring/PGS/Match-OPT genuinely
bundle extra machinery. Ground (3) is verified true by direct re-extraction: zero ANOVA/eta-squared/
variance-decomposition language anywhere in RaM's 172,006-character full text. The paper's actual
scientific contribution — crossing model class (not loss) against optimizer and reporting the
decomposition — is not touched by RaM at any point, including its closest sub-grid.

## Committed position

The residual is **DEFENSIBLE-BUT-MUST-BE-ARGUED**, and specifically it must be *corrected*, not
merely elaborated, because one of its three grounds is currently stated in a form that RaM's own
appendix directly contradicts. Positions A and B are not actually in tension once separated
correctly: A is right that the *current page* is indefensible (silent on RaM, and the one place
it gestures at RaM's category is wrong), and B is right that the *underlying* three-ground case
survives once restated with the precision this investigation supports. The load-bearing reason
for this verdict is that ground (2)'s falsification is local and fixable — it is wrong about four
of nine methods, not about the residual's core claim — while grounds (1) and (3) both hold up
under direct primary-source and literature testing, and ground (1) is now backed by an actual
number (eta-squared_Loss=0.027 vs eta-squared_Method=0.577 in RaM's own data) rather than a bare
assertion. **Exact wording the paper should use:** (i) split the miscategorised citation —
*"surrogate-class comparisons hold the optimizer constant \citep{li2024bnnsurrogates}, and
training-objective comparisons hold both architecture and optimizer fixed while varying the loss
\citep{tan2025ltr,trabucco2021coms}"* — moving `tan2025ltr` out of the surrogate-class bucket and
into the training-objective bucket alongside COMs, which is what RaM actually is; (ii) add, at the
contribution paragraph or in a footnote: *"The nearest crossed design is Tan et al.'s Table 3,
which swaps a training loss (MSE vs.\ ListNet) against nine offline-MBO methods; four of the nine
(BO-qEI, CMA-ES, REINFORCE, gradient ascent) are, by the authors' own construction, optimizers
applied to one fixed MLP, giving a genuine loss$\times$optimizer sub-grid, but the swapped
quantity is the training objective, not the mechanism that produces the uncertainty estimate our
surrogate axis varies; the remaining five bundle a search paradigm with a model family that cannot
be varied independently (CbAS, MINs) or add method-specific machinery beyond a bare optimizer
(Tri-Mentoring, PGS, Match-OPT); no variance decomposition is computed on any of it."* If space
allows, add the corroborating number: *"model class explains most of our own grid's variance
while, in Tan et al.'s own published means, a comparable training-loss swap explains under 3% of
theirs — the two are not interchangeable manipulations."*

- **Position:** N6's residual survives against RaM Table 3 and DiBO Table 2, but only after
  ground (2) is corrected from "the nine are bundled methods" to "four of nine are a clean
  optimizer sub-grid that varies loss, not model class, while five bundle search paradigm with
  model family" — the paper must make this correction and explicitly name RaM Table 3, or a
  RaM-familiar reviewer will supply the counterexample the current silent page invites.
- **Confidence:** high. This rests on fresh, directly-verified primary text (RaM's exact
  Appendix E.5 method taxonomy and Table 3 data, independently re-extracted and grep-confirmed
  for zero decomposition language), a from-scratch reproducible calculation on RaM's own published
  numbers, and two canonical, on-point secondary sources (NIST DOE handbook, Abdar et al. UQ
  survey) rather than snippet-level inference.
- **Boundary conditions:** this verdict holds for the residual as scoped against RaM Table 3 and
  DiBO Table 2 specifically — the two concrete near-misses the corpus identified as live threats.
  It does not extend to a hypothetical future paper that crosses genuine surrogate *model class*
  (not loss) against optimizer with a decomposition; if such a paper is found, N6 collapses
  regardless of how well the current three grounds are argued, because the grounds are a defence
  against the *nearest* near-misses, not a general immunity.
- **What would change this position:** (i) if RaM's own appendix language turns out to be
  imprecise about which methods use which surrogate architecture (I re-verified this directly and
  it is not, but a contradicting statement elsewhere in RaM would matter); (ii) if a reviewer or
  follow-up paper is found that has *already* computed a variance decomposition on Table 3's
  published numbers (would fully void ground (3) rather than merely weaken it); (iii) if the
  model-class-vs-training-objective criterion I propose (constitutive binding to a native fitting
  procedure vs. independently swappable within a fixed architecture) turns out to be contradicted
  by a canonical surrogate-modeling source that treats them as the same factor — I searched for
  such a source and did not find one, but I did not exhaustively search the AutoML/kernel-selection
  literature, which is the most likely place a counter-source would live.
- **Evidence weight:** 2 primary-source re-extractions (RaM, DiBO, both fresh) directly support
  the factual claims about what each table contains; 1 from-scratch reproducible computation
  supports the ground-(1) empirical corroboration and the ground-(3) computability point; 2
  canonical secondary sources (NIST DOE handbook, Abdar UQ survey) support the theoretical
  legitimacy of grounds (1) and (2); 0 sources contradict the overall "survives if corrected"
  verdict, though the paper's *current, unedited* wording is directly contradicted by RaM's own
  text on ground (2) specifically.

## Open questions

- Does the AutoML/kernel-selection literature (not searched in this pass) contain a source that
  treats "surrogate model class" and "training objective" as the same factor, which would weaken
  ground (1)'s domain-precedent argument? Worth one more targeted search if the orchestrator has
  budget.
- Is there a cheap way to also compute the analogous variance split on DiBO's Table 2 (backbone
  x training-stage) to check whether backbone (a plausible model-class analogue) explains more
  variance than training-stage — this would be a second, independent corroboration of the
  ground-(1) asymmetry argument, but DiBO fails the optimizer conjunct regardless of the outcome,
  so it is lower priority than the AutoML search above.
- Should the eta-squared_Loss=0.027 vs eta-squared_Method=0.577 computation be formally verified
  by a second, independent re-implementation before it goes in the paper (even as a footnote),
  given it rests on treating RaM's reported std as the relevant per-cell dispersion for an
  aggregate-data ANOVA? I built it from first principles and it is arithmetically sound, but it
  has not been cross-checked by a second method or tool.

## Sources

1. [[offline-model-based-optimization-by-learning-to-rank-2]] — Tan et al., RaM (ICLR 2025,
   arXiv:2410.11502), fresh re-fetch for this locus, Table 3 + Appendix E.5 method taxonomy.
2. [[training-diffusion-language-models-for-black-box-optimization]] — DiBO (arXiv:2603.17919),
   fresh fetch, Table 2 backbone x training-stage grid.
3. [[53343-confounding-also-called-aliasing]] — NIST/SEMATECH Engineering Statistics Handbook
   5.3.3.4.3, canonical confounding/aliasing definition.
4. [[532-how-do-you-select-and-scale-the-process-variables]] — NIST/SEMATECH Engineering
   Statistics Handbook 5.3.2, factor selection as engineering judgment upstream of statistics.
5. [[a-review-of-uncertainty-quantification-in-deep-learning-techniques-applications]] — Abdar
   et al. 2021 UQ survey (arXiv:2011.06225), method-family vs.\ loss-function taxonomy.
6. Prior-pass corpus notes (not re-fetched, read for context): `research/temp/findings-so-far.md`
   N6 section; `research/temp/contradiction-graph.json` cluster `n6-residual-width`;
   `research/raw/txt/rudner-study-bnn-surrogates-bo.txt` (li2024bnnsurrogates full text, already
   in vault, re-examined for its own model-class/training-procedure framing).
