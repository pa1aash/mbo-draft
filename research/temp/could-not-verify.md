# "What I could not verify and why" — assembled source material

Every limitation accumulated across steps 1–8. The final report's terminal section draws from
this. Grouped by *why* verification failed, because the reasons differ in how much they should
discount a finding.

---

## A. Paywalled or access-blocked primaries — verified secondhand

| Source | Needed for | What I used instead |
|---|---|---|
| **Kelley (1935)** and **Olejnik & Algina (2003)** | The claim that η² is positively biased and ω²/ε² correct it (Mandatory Fix 9) | JOSS `effectsize` documentation quoting both verbatim. **The empirical half is first-hand:** I computed the bias directly from the paper's own bootstrap artifacts (+0.0099 to +0.0184 across four corners). A gap-fill fetcher is chasing Levine & Hullett (2002) / Okada (2013) as accessible primaries. |
| **Montgomery, *Design and Analysis of Experiments*, Ch. 5** | The positive DOE statement that a crossed design's payoff is interaction estimation | A SAS/JMP companion-volume excerpt, plus NIST/SEMATECH §5.2.1.2 and Box (1989), both of which are open and were quoted directly. The Montgomery prose itself remains unverified. |
| **Yu et al. (2016)** on landscape-driven surrogate selection | The landscape locus's survey of prior surrogate-selection work | Blocked by an AWS-WAF bot-check on IEEE Xplore — a genuine access failure, not a budget decision. Malan's 2021 survey quotes it. |
| **Ben-Shachar et al. (2023)**, "Demystifying omega squared" | Secondary support for the η² bias claim | Not fetched; paywalled. |
| **Rudolph (1994)**, "Convergence Analysis of Canonical Genetic Algorithms" | The canonical elitism-guarantee citation for the inversion reframing | 403 on IEEE Xplore, ResearchGate and Academia.edu. The Safe-Policy-Improvement framing (Thomas et al.; SPIBB) carries the point instead and is fully verified. |

## B. Venue attributions I could not confirm — and two my own subagents got wrong

**This is the category that matters most, because the errors were mine, not the paper's.**

| Source | Problem |
|---|---|
| **Dao et al., "Boosting Offline Optimizers with Surrogate Sensitivity"** | A depth investigator reported "arXiv:2503.04181, ICML 2024". **arXiv v1 is 2025-03-06 — chronologically impossible**, and OpenAlex has no title match. Venue withdrawn; cited as arXiv 2025, venue unverified. The substance (the (α,ω)-sensitivity experiment) still stands. |
| **Ghasemipour, Gu & Nachum, "Why So Pessimistic?"** | Two subagents gave two venues — NeurIPS 2022 and ICML 2022. OpenAlex resolves arXiv:2205.13703 to a **preprint with no conference venue**. Cited as arXiv 2022, venue unverified. Load-bearing twice (Mandatory Fix 11 and the candidate inversion mechanism), so the uncertainty is material. |

Verified clean in the same sweep, and worth stating: Xu (ICLR 2021, arXiv v1 2020 — same trap
class as Li/Rudner/Wilson), Gao (**ICML 2023**, confirming the `gao2022reward` key and page-range
defects), Lu (ICLR 2022 Spotlight), Fujimoto & Gu (NeurIPS 2021 Spotlight), Laroche et al. SPIBB
(**ICML 2019**, not 2018), Henderson (**AAAI 2018** from the PDF copyright line), Benavoli
(**JMLR 17, 2016**, arXiv 2015), Li/Rudner/Wilson (**ICLR 2024**), Kim et al. (**TMLR 01/2026**).

## C. Tooling and infrastructure limits

- **`hyperresearch fetch` cannot ingest PDFs in this environment.** Every arXiv PDF URL form
  returns `JUNK_CONTENT: Binary PDF garbage in content`. One batch traced it into
  `hyperresearch/web/crawl4ai_provider.py` — `_fetch_pdf()` works when called directly, so the
  fault is the post-fetch `looks_like_junk()` gate misfiring, not extraction. **Consequence:**
  most vault notes for PDF sources hold only the arXiv abstract page (~700 words). All full-text
  verification ran via ar5iv/HTML mirrors or `curl` + pymupdf **outside** the vault. Verdicts do
  rest on primary full text, but a later reader cannot re-grep that text from the note.
- **Semantic Scholar returned HTTP 429 for the entire session**, on both the REST endpoint and
  the MCP tool, across every retry schedule and every batch. arXiv and OpenAlex carried all
  citation chaining, **including the N6 forward-citation walks (~347 papers)**. No verdict rests
  on an S2-only result.
- **OpenAlex full-text `search=` is very noisy on this topic** — it returned climate models and
  echocardiography for optimization queries. Its null results are weak evidence of absence and
  the N6 verdict does not rest on them.
- Concurrent fetchers caused occasional sqlite `IntegrityError` and sync id-collisions; resolved
  by deprecating duplicates.

## D. Analyses I recommend but did not run

- **The mixed-effects model with task as a random effect.** `docs/FLAW_LEDGER.md` P1-2 calls for
  it; no normalizer robustness check substitutes for it. **Two independent investigators named
  this as their falsifier**, which makes it the single most-cited open item in the audit.
- **The floor-effect disentangling analysis.** Needed to separate "perturbation neutralises
  surrogate differences" from "perturbation underperforms, compressing everything". The data
  exists (`x0_inversion.json` stores `mean_x0_best` and `mean_ret_best` per cell); I did not run
  it.
- **Bias correction on the interaction term across the β and budget sweeps.** I computed it for
  the four corners (0.134–0.156, finding survives) but not elsewhere.
- **The η² recomputation from RaM's Table 3 has not been independently reimplemented.** The
  N6 defence leans on a number (loss axis 0.027 vs method axis 0.577) that this audit computed
  once, and the locus-1 investigator flagged the absence of a cross-check.
- **A second implementation of any of my own artifact computations.** The corner values,
  inversion counts, frozen-cell counts and raw-units gaps were each computed once, by me, from
  the JSON artifacts.

## E. Questions I raise without resolving

- **The TOST numeric coincidence.** Elimination 3's `0.375` and `roughly 0.48` sit within
  rounding of the TOST `gap` (0.3762) and `effect_bound` (0.4840) — but Elimination 3 is
  described as a synthetic-grid result while TOST comes from `results_db.json`. Either a
  three-significant-figure coincidence or a transplanted number in a load-bearing paragraph.
  **Resolvable by the author in one lookup; I am not asserting either reading.**
- **Whether a depth sweep exists unreported.** Mandatory Fix 12's force depends on the ensemble
  being fixed at two hidden layers throughout the width sweep, which I read from `main.tex:88`.
  I did not confirm the *absence* of a depth experiment elsewhere in the artifacts.
- **`supplement.tex` was not checked for duplicate or contradictory NTK framing** (locus 4 ran
  out of budget).
- **The AutoML / kernel-selection literature's treatment of model-class versus training-objective
  as one factor or two.** This could attack N6's surviving ground (1). A gap-fill fetcher is on
  it; if it returns nothing, the ground stands on Abdar et al. 2021 alone.

## F. Scope boundaries I did not cross

- **Design-Bench's corrected (on/on) corner was not re-run through the normalizer zoo** — only
  the synthetic corners and the uncorrected DB numbers.
- **The paper's code was verified at the line level for Confounds 1 and 2 only.** I did not audit
  the bootstrap implementation, the ANOVA implementation, or `stats.py`. **Every numeric verdict
  in this report assumes those are correct**, which is an assumption, not a finding.
- **I did not attempt to reproduce any experiment.** All numeric verification compares the paper's
  text against its own stored result artifacts. If an artifact is itself wrong, this audit would
  not detect it.
