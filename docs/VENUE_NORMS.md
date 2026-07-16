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
limitations in the state of the art that the paper addresses?"). AAAI is the *worst* fit of the venues
surveyed for a measurement/null paper. (AAAI text came via WebFetch summarization, not raw fetch —
lower confidence than the others.)

## Alternatives if the AAAI window is tight

- **MLRC 2026 is now an official NeurIPS track**, routed through TMLR. Hard deadline **2026-09-30**.
  "MLRC welcomes rigorous work across the full spectrum of outcomes, including positive confirmations of
  prior results, partial replications, and **failures to reproduce**." Papers publish in TMLR proceedings,
  presented at NeurIPS.
- **TMLR** directly: "novelty of the studied method is not a necessary criteria for acceptance."
  But TMLR explicitly rejects bare nulls without "generalizable insights" / "actionable lessons."

## Pattern across accepted measurement papers

"Are GANs Created Equal?", Musgrave's metric-learning reality check, Dacrema's recsys "phantom progress",
Recht et al. "Do ImageNet Classifiers Generalize?" — the shared shape is **a specific, named, falsified
belief plus a reusable protocol**. A bare null has neither.

Standalone negative-results venues fail (JINR: one paper in 18 years; JNRBM: closed 2017). Negative
results survive only when attached to an existing conference (ICBINB: 7 years, 61 papers; Insights:
~118 papers).

**NOT VERIFIED:** ICBINB 2026 PMLR volume; Insights acceptance rates; SIGIR 2026 verbatim scope.
