# Synthesis plan

## Core thesis
The paper's evidence is sound and its scholarship is not: every quantitative claim checkable
against a repo artifact reproduces — two frozen-cell claims to the individual seed — while twelve
citations fail against primary text, eleven of which concern what a *source* says and none of
which touches a number the paper computed. That asymmetry is the audit's actionable output,
because it says the remaining pre-deadline hours belong in related-work and scoping prose, and
because the paper is sitting on a significant, stable, never-interpreted interaction term that no
ML benchmark study anywhere reports.

## The strongest argumentative beats
1. **N6 survives, and the verdict names its own unchecked lead** — Draft C's framing. Four
   adversarial sweeps found no kill; the honest verdict discloses Elsayed & Lacor (2014) inside
   itself rather than in the terminal section.
2. **The Demšar threshold does not exist, and removing it HELPS** — Draft B. Worst miscitation
   class, yet the fix removes a false warrant and an unnecessary self-deprecation at once.
3. **The Fan citation inverts a convergence theorem into a failure mode** — Draft A. Zero
   full-text hits for offline/LCB/stuck/paralysis; Theorem 1 proves convergence.
4. **The interaction is the buried result** — all three, converging. Significant in all four
   corners, second-largest effect, 9.2× more stable than the headline, mentioned once in
   `main.tex` — in the sentence explaining why Moosbauer *declined* the analysis that finds it.
5. **The boundary-condition table** — Draft C. Interaction and raw-units attenuation each survive
   what the other fails; together defensible, either alone an overclaim.
6. **Bias correction strengthens the headline** — 0.351→0.395, and the correction to name is ε²
   not ω² (Okada 2013 overturns the folk belief).
7. **The multiplicative-mechanism constraint** — visible only in cross-section: stable per-task
   ranking plus collapsing per-task magnitude rules out both a purely optimizer-side and a purely
   task-side account.

## Section structure
The five literal H2s from `required_section_headings`, in order, plus `## Sources`
(citation_style is `inline`).

## Per-section commitments

### N6 Verdict: The Crossed Surrogate x Optimizer Factorial
- Evidence: the four sweeps (2026 frontier; three near-miss re-confirmations; ~347 forward
  citations; SAEA/AutoML/simulation-optimization). Verbatim queries. The three surviving grounds.
- Beat 1. **Must state ground (2) was falsified on contact** with RaM's appendix, and must
  disclose Elsayed & Lacor inside the verdict.
- Tension engaged: `n6-residual-width` / comparisons Tension 2 — the audit computed η² from RaM's
  published table while defending N6, which proves the decomposition is *derivable* from data in
  print. N6 is a claim about what the literature **reports**, never about what the design space
  permitted.

### (i) Claims the Literature Contradicts or That Are Miscited
- Ordered by severity to the reader's trust: Demšar (fabricated threshold), Fan (three ways,
  one inverting a theorem), SNGP (cited against its own Figure 1), Li/Rudner/Wilson (false
  K-range), Rahaman (motivates the axis its own ablation calls weak, at fixed depth 2), Abe (no
  K-sweep exists), Melis (one instance certifying a genre law), Ghasemipour (over-extended
  analogy), the conformal scoping omission, the Kim bib/prose mismatch, `gao2022reward`'s three
  bib defects, and the "five other cells" recount.
- Each carries: the claim, the paper's framing, what the source actually says, the FIX.
- **Must also report the passes**: Shahriari (understated, not over-cited), Chemingui (verbatim),
  Dewolf (correctly scoped), and the three year traps handled right.
- Tension engaged: source-tensions #1 (σ distance-vs-error resolves by scoping) and #4 (nobody
  owns acquisition-stalling — withdrawn in favour of Yarotsky 2013 as closest prior art).

### (ii) Kills
- **Zero kills.** State it plainly and give the queries. The near-miss ledger: RaM Table 3's 4×2
  clean sub-grid, DiBO's 2×3, BOOST's kernel×acquisition, Yarotsky's Theorem 3.
- The one unresolved lead, with the precise open question (genuine crossing vs sequential).

### (iii) Scope of Novelty, Ranked
- Ranked by value per hour, every item tagged. Lead with the interaction; then the boundary-
  condition table; then bias correction, TOST, `tab:cross` connection, landscape negative,
  Fannjiang citation; then the elimination→mechanism experiments (Xu, Dao, Gao, CQL, Manheim,
  DKL) with CHEAP/EXPENSIVE; then FOLLOW-UP items (BBOB-scale ELA study, BCQ graded battery).
- Tensions engaged: comparisons #1 (direction not magnitude), #4 (multiplicative constraint),
  #5 (Elimination 2 narrower than the count implies).

### What I could not verify and why
- Six categories from `could-not-verify.md`. **Must include the audit's own failures**: two
  subagent venue fabrications caught (one chronologically impossible), five orchestrator
  self-corrections, and the fact that the bootstrap/ANOVA implementations were never audited so
  every numeric verdict assumes them.

## Where drafts disagreed
- **Severity.** A: severe. B: cosmetic. **Commit to both, explicitly split** — high to reader
  trust, nil to results. Do not average into mush. See `synthesis-conflicts.md`.
- **Interaction placement.** Locus 3 says main text (~65%), locus 6 says abstract. **Commit to
  main text with synthetic-grid scoping**, because Design-Bench η²_inter is an order of magnitude
  smaller and an unscoped abstract claim would be the same overreach the audit criticises.

## Length target
- response_format: `argumentative`. Inputs are 11k–15.6k words each — **over target**.
- Pass 1 target: ~9,000 words. Pass 2 final target: **7,000–8,000 words**. Pass 2 must CUT.
