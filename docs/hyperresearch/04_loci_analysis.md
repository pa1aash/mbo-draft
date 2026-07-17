# 04 · Loci analysis — the highest-leverage acceptance questions

**Step 4 of the research core.** From the ranked fights (03), the five questions where deeper
investigation actually changes the accept/reject decision. Each is scored 1–5 on **importance** (how much
of the paper's fate rides on it), **uncertainty** (how unresolved it is right now), and **decision-impact**
(whether resolving it flips a submit/no-submit or identity choice). A source budget is allocated by score.

**Scope honesty.** In a full pipeline these loci would be handed to parallel depth-investigator subagents
with independent fetch budgets. Here they are investigated inline in 05 against the corpus assembled in 02
plus the already-grounded repo docs. Loci are deduplicated and ranked; two candidate loci were merged or
dropped (noted at the end).

Scoring key: each dimension 1 (low) – 5 (high). "Budget" = relative depth allocation for step 05.

---

## LOCUS 1 — Does AAAI's main track actually reward a benchmark-validity / measurement finding, and under what conditions?

**The question in one line:** is the paper's genre (no new method, a de-confounded measurement + a
diagnostic + a declared null) *acceptable in principle* at AAAI-27 main track, and what is the minimal
thing it must ship to clear the bar?

- **Importance: 5.** If the genre is disqualified at AAAI, no amount of repair helps and the venue choice
  is wrong. Everything downstream assumes a "yes."
- **Uncertainty: 2.** Largely resolved by precedent (Henderson/Gundersen/Kim/Zeng, all AAAI main track)
  and by the ICLR reviewer corpus, but AAAI reviews are private so the *conditions* are a proxy.
- **Decision-impact: 5.** Sets the venue and the identity. Determines whether the answer to the wrapper's
  question is "fixable" or "wrong venue."
- **Score: 12/15. Budget: high.**
- **Feeds:** manuscript axis; heading 8 ("What AAAI Rewards"). Fights F1, F10.

---

## LOCUS 2 — Is the "ensemble-baseline-crippling" objection fatal, or answerable?

**The question in one line:** the paper's ensemble trains on raw targets while GPs z-score (P0-2), is
unregularized/unvalidated/never early-stopped (P1-3), and the repo's own `gradtune.py` shows the gradient
collapse is a tuning artifact on 3/4 tasks (P0-0) — is the surrogate/interaction story recoverable, or
does a fair baseline erase it?

- **Importance: 5.** This is the paper's headline (η²_surr=0.37) and its second contribution (the
  interaction). If a fair ensemble erases both, the paper as drafted does not exist.
- **Uncertainty: 5.** Genuinely unresolved — it is an *unrun experiment*. The repo docs state the confound
  clearly but cannot say whether η²_surr survives normalization. The literature is split (Fight 4).
- **Decision-impact: 5.** `FLAW_LEDGER.md`: "nothing else … until P0-2 is run." Gates the headline, the
  mechanism, the reversal framing, and the A-vs-C choice.
- **Score: 15/15. Budget: highest.**
- **Feeds:** experiments axis; headings 6, 10, 13. Fights F2, F3, F4.

---

## LOCUS 3 — Is the smooth-mean / inductive-bias mechanism a contribution, or a restatement?

**The question in one line:** even if the measurement survives, is "the GP's advantage is its smooth
posterior *mean*, not its calibration" a novel mechanism, or is it owned by Li/Rudner/Wilson (calibration
story), IGNITE, MS-DDEO, and the NTK/spectral-bias literature?

- **Importance: 4.** Decides whether Identity C (the strongest identity) has a real mechanism or is a
  narrow re-attribution. The genre bar (F1) demands a mechanism, so this is where C earns or loses.
- **Uncertainty: 4.** The bidirectional-manipulation *move* is NONE FOUND (`NOVELTY_V2.md` C2), but the
  smoothness *axis* is pre-claimed and the NTK grounding was not fetched fresh (a real gap — see 08).
- **Decision-impact: 4.** Determines whether C is "the paper worth writing" or degrades to A.
- **Score: 12/15. Budget: high.**
- **Feeds:** manuscript + experiments axes; headings 2, 13. Fights F3, F4.

---

## LOCUS 4 — Can the paper survive the "broken-oracles" competing explanation for the Design-Bench null?

**The question in one line:** the paper claims the synthetic→real gap is prior–task mismatch; reviewers
have a free competing explanation (Design-Bench oracles are broken, worsened by the paper's own RF-oracle
substitution on 5/7 tasks) that N=7 cannot rule out. Is there a cheap, grid-reusing move that converts
this from fatal to controlled-for?

- **Importance: 4.** This is "the single most likely reject route for Contribution 3" (`VENUE_NORMS.md`).
- **Uncertainty: 3.** The competing hypothesis is real and cheap for a reviewer; the counter (exact-oracle
  subset / oracle noise floor, X11) is identified but not yet executed.
- **Decision-impact: 4.** Decides whether Contribution 3 (the null) is a liability or an asset.
- **Score: 11/15. Budget: medium.**
- **Feeds:** experiments + statistics axes; headings 5, 11, 13. Fight F7.

---

## LOCUS 5 — Is the statistics apparatus an asset or a liability, and what is the minimum to make it defensible at N=7?

**The question in one line:** the paper ships a Friedman/Nemenyi-CD/TOST apparatus reviewers explicitly
request — but the ANOVA is hand-rolled with no error term, η² is on 63 cell means, the CD pool silently
spans 11 cells (Benavoli), and N=7 sits below Demšar's own N>10 threshold and TOST's sample needs. Net
asset or net liability, and what is the minimal fix?

- **Importance: 3.** Rarely the sole reject-driver (no measurement paper in the corpus was rejected for
  being statistically *wrong*), but it is the audit-pool's clean kill and the checklist's C11 failure.
- **Uncertainty: 2.** The fixes are known and cheap (mixed model / permutation effect size, per-pair
  tests, IQM+bootstrap CIs, declare the power spec). Low uncertainty, moderate importance.
- **Decision-impact: 3.** Turns a set of P1/P2 flaws into an asset (Asset 1: reviewers *want* CD diagrams).
- **Score: 8/15. Budget: medium-low.**
- **Feeds:** statistics + artifact axes; headings 7, 11, 12. Fights F8, F9.

---

## Ranked loci and budget allocation for step 05

| Locus | Score | Budget | Primary axis | Committed-position stakes |
|---|---|---|---|---|
| L2 — ensemble-crippling objection | 15/15 | highest | experiments | Is the headline recoverable? |
| L1 — does AAAI reward this genre | 12/15 | high | manuscript | Is the venue/identity right? |
| L3 — smooth-mean mechanism novelty | 12/15 | high | manuscript | Does C have a real mechanism? |
| L4 — broken-oracles competing hypothesis | 11/15 | medium | experiments | Is Contribution 3 salvageable? |
| L5 — statistics asset vs liability | 8/15 | med-low | statistics | Minimal defensible-stats fix? |

## Deduplication / dropped candidates

- **Merged:** "is the optimizer reversal (η²_opt=0.01) real?" (Fight F5) was folded into **L2** — it is
  gated by the same X1+X3 re-run that gates the ensemble question, so investigating them together avoids a
  redundant locus.
- **Dropped:** "is coverage-driven offline *selection* novel?" — the corresponding Identity B is **dead**
  (`PAPER_V2_OUTLINE.md`: the selection signal isn't computable offline, and n=14 can't resolve it). The
  novelty question is moot; its only survivor (the obstruction result) is a discussion point in C, not a
  locus that changes acceptance.
- **Not promoted to a locus:** the artifact-reproducibility failures (P0-4 missing generators, Fig 1 vs 3
  disagreement) are decisive but *not uncertain* — they are established facts with known fixes
  (`AAAI27_VENUE.md` C.4). They belong in the findings (steps handled by the wrapper's flaw ledger), not
  in depth investigation, because there is nothing left to discover.
