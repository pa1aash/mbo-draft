# Gauntlet R1–R3 — three adversarial reviewers, each holding one citation

**Date:** 2026-07-20. **Stage 2.4.** **Target:** `paper/aaai27/main.tex`, `paper/aaai27/supplement.tex`.

Three simulated AAAI-27 reviewers, each holding one specific citation aimed at one specific
claim. The purpose was **not** to weaken claims. It was to find every place the paper makes a
strong claim and fails to defend it, then add the defense. **No claim was softened. 21 undefended
claim sites were found and armored.**

| Reviewer | Citation held | Attack | Score |
|---|---|---|---|
| **R1** | Li, Rudner & Wilson, ICLR 2024 | "The controlled cross-surrogate comparison already exists and is more thorough — seven classes, K-robustness, a smaller-net ablation. Your N6 novelty is overstated." | **4 / 6** |
| **R2** | Shahriari et al., Proc. IEEE 2016 | "Statistical model > acquisition heuristic is the organizing doctrine of the standard BO review, and a decade old. Your directional result is not new." | **4 / 6** |
| **R3** | Agarwal NeurIPS 2021 + Demšar JMLR 2006 | "n=7 is below the Friedman threshold. Your DB null is no detectable difference at this power, not equivalence — and MuJoCo rejecting 3/4 shows the null is fragile." | **5 / 6** |

All three attacks **failed against the paper read in full** and **succeeded against the paper as
skimmed**. That asymmetry is the whole finding of this pass: the guards were correctly *written*
and incorrectly *distributed*.

---

## R1 — Li, Rudner & Wilson (ICLR 2024). Score 4/6

### The two sentences driving the score

**Up** — `main.tex:177`: *"The more accurate surrogate is the one that loses, which removes
predictive error from the candidates."* Earned by a 28-cell ablation with a registered tie-cell
primary; no prior surrogate comparison delivers it.

**Down** — `main.tex:63` (as it stood): *"surrogate-class comparisons hold the optimizer constant
\citep{tan2025ltr,li2024bnnsurrogates}."* A half-clause was the entire defense against the closest
paper in the literature — and it was wrong in a way an L/R/W author catches instantly. L/R/W does
not hold the *optimizer* constant in this paper's sense (Adam-on-x / hill-climbing / CMA-ES); it
holds the **acquisition function** fixed (MC-EI). The paper's own `:243` insists on exactly that
distinction — "the choice of acquisition *function family*, not the numerical search routine" —
and then failed to apply it at the one citation where it was load-bearing. Worse, [8] was
co-cited with `tan2025ltr` (offline MBO), implying an **online** study sits in the offline lineage.

### Ammunition found

The decisive finding: **L/R/W was not named in the paragraph that enumerates the closest
precedents.** `main.tex:65` named `hutter2014fanova`, `liang2021benchmarking`,
`moosbauer2022benchmarkdriven` by role; `:83` repeated the same closed set. The closest controlled
cross-surrogate comparison in the literature appeared in neither, and **appeared nowhere in
Related Work at all**. Its three appearances paper-wide were a compressed half-clause (`:63`), a
K-range note (`:98`), and a disclaimer list (`:243`) — one of three defended, and on a secondary
axis.

Asymmetry worth naming: the paper defends **N9** (the audit-direction claim) with textbook care at
`:135` — "Two partials must be pre-empted," Recht named by mechanism, Agarwal named, statistics
conceded as unsurprising. The **weaker** novelty claim was armored; the **load-bearing** one
(D02, LANDED) was defended by a subordinate clause.

### Patches applied — 8 sites

Four scope distinctions required, all now explicit and early: (a) L/R/W is **online BO**, not
offline MBO; (b) it holds the **acquisition fixed**; (c) it does **not cross the optimizer axis**;
(d) it does **not decompose variance**.

| # | Site | Defense added |
|---|---|---|
| R1-1 | `main.tex:63` | L/R/W split out and named; all four distinctions in one sentence; **concedes it is broader on the surrogate axis** then shows that breadth is structurally incapable of producing the estimand. Closes with "not a smaller version of this experiment but a transposed one." |
| R1-2 | `main.tex:63` | "Nobody has run" hardened to an auditable count — "of the seven candidate designs we checked, every one fixes an axis, bundles both inside a method, or declines the decomposition" (the 7-row rule-out table, `NOVELTY_V3.md:88`). Claim **extended** past offline MBO to online BO. |
| R1-3 | `main.tex:65` | L/R/W inserted into the precedent enumeration it was missing from. |
| R1-4 | `main.tex:49` (abstract) | Earliest possible guard: "where the controlled surrogate comparisons that precede us vary surrogate class alone against a fixed acquisition rule, in online BO." |
| R1-5 | `main.tex:83` | L/R/W given its own sentence in Related Work, where an [8]-holding reviewer looks first. |
| R1-6 | `main.tex:175` | Names the existing **smaller-net** ablation before claiming ours is the one that tests width — and shows it runs the opposite direction ("the width objection predicts the gap closes as the net *grows*, so we sweep upward"). Pre-empts the D13 prior-art risk. |
| R1-7 | `main.tex:98` | Adds "in online BO under one fixed acquisition rule" — converts a K-axis-only guard into one carrying (a) and (b). |
| R1-8 | `supplement.tex:130` | Ports the K-range guard into the supplement, which carried no L/R/W scoping at all. |

**Verified before printing:** seven classes, MC-EI-fixed, online (0 hits for "offline"), no
decomposition, smaller-net ablation (width 128→50) — all against `NOVELTY_V3.md:88,96,76,154`.

---

## R2 — Shahriari et al. (Proc. IEEE 2016). Score 4/6

### The two sentences driving the score

**Up** — `main.tex:77`: *"No field reversal: that the statistical model often matters more than the
acquisition heuristic is the organizing doctrine of the standard Bayesian-optimization review… and
our optimizer-axis result falsifies the local premise of one recent paper and nothing wider."*
A paper that cites the review the reviewer holds and states the objection better than they would.

**Down** — `main.tex:232` (as it stood): *"while the synthetic grid of Section 4 calls the
optimizer negligible."* The paper's own voice generalizing η²_opt = 0.038 into a verdict — exactly
the sentence form **hard rule 2 forbids** — and **self-contradicted at `:239`**, which states a
small η²_opt "licenses 'optimizer choice explains little variance' and never 'optimizer choice is
arbitrary'—the second reading is false on our own data." A hostile reviewer quotes 232 and 239 side
by side.

### The decisive finding: the skim path had zero guards

Grep-verified before patching: `shahriari2016humanoutoftheloop` appeared at **only** `:77` and
`:243`; `chemingui2024pggs` at **only** `:77`, `:83`, `:243`. **Neither appeared in the abstract or
the conclusion.** Guard map as found — two guards across nine sections:

| Section | Shahriari guard | PGS-local framing |
|---|---|---|
| Abstract | **NONE** | **NONE** |
| Introduction | YES (`:77`) | YES (`:77`) |
| Related Work | NONE | neutral mention only |
| Grid & Confounds | NONE | NONE |
| De-Confounding Results | NONE | NONE |
| Isolating the Gap | NONE | NONE |
| **Design-Bench** | **NONE** | **NONE** |
| Discussion & Limitations | YES (`:243`) | YES (`:243`) |
| **Conclusion** | **NONE** | **NONE** |

The two unguarded sections carrying the most generalizing language (Design-Bench, Conclusion) are
also the two most-skimmed. The conclusion contained **no sentence about the optimizer axis at
all**, so on an abstract-plus-conclusion read the only optimizer statement was the unguarded
0.038 in the abstract, against η²_surr = 0.405 — a ~10× contrast reading exactly like the field
reversal rule 2 forbids. Guard B (`:243`) also sat *after* the entire Design-Bench section.

### Patches applied — 7 sites

| # | Site | Defense added |
|---|---|---|
| R2-1 | `main.tex:52` (abstract) | "in this grid" (matching `:239`'s own qualifier) **plus** the Shahriari concession and the PGS-local falsification, named in the abstract for the first time. |
| R2-2 | `main.tex:249` (conclusion) | New optimizer-axis sentence: the number, its interval, "in this grid", the PGS premise quoted, and Shahriari. **States the falsification more explicitly than the draft did.** |
| R2-3 | `main.tex:232` | The forbidden sentence form removed — "calls the optimizer negligible" replaced by the measured magnitude **and its interval**, plus "never a verdict that optimizer choice is negligible in general." Kills the 232-vs-239 self-contradiction. |
| R2-4 | `main.tex:139` | "The direction is invariant" bounded to the synthetic suite, and the 139-vs-220 cross-suite inconsistency pre-empted in our own voice. |
| R2-5 | `main.tex:83` | PGS named as the falsification target in Related Work — the falsification now asserted three times, not once. |
| R2-6 | `main.tex:222` | "on Design-Bench" / "in this suite" — removes a general-sounding claim about gradient vs perturbation. |
| R2-7 | `main.tex:237` | "in this grid it does not". |

**Deliberately deferred:** R2 also proposed a fifth contributions-list item carrying the guard.
Skipped for page budget — the Scope paragraph (`:77`) is the very next paragraph after the list, so
a linear reader meets the guard four lines later. Revisit only if space frees up.

---

## R3 — Agarwal (NeurIPS 2021) + Demšar (JMLR 2006). Score 5/6

Highest score of the three: the attack is largely pre-empted before it starts.

### The two sentences driving the score

**Up** — `main.tex:220`: *"We therefore report no detectable difference at this power, never
equivalence, because we are below the threshold for the test we ran: this omnibus is recommended
for more than ten datasets, at n=7 a paired test needs |d_z|≥1.27 for 80% power at α=0.05—larger
than anything we observe—and a failure to reject is not a demonstration that an effect is absent."*
Cites **both** of the reviewer's weapons against the authors' own claim and converts the power
objection into a stated MDE. No move left on the equivalence front.

**Up, decisively** — `main.tex:220`: the cross-corner anti-monotonicity argument. *"The one corner
that does not reject (p=0.16) carries the larger surrogate effect (0.053, against a rejecting
corner's 0.044), so surrogate effect size does not track rejection, while η²_opt tracks it cleanly."*
This is an **ordering argument across corners** — it needs no within-corner separation, so the
n=7 power objection cannot reach it.

### CHECK A — the word "equivalence"

**Six hits found. Five denials, zero assertions. Rule 4 held in `main.tex`.**
`:52` (abstract), `:74`, `:77`, `:220`, `:243` — all correct denials.

**The one exposure was in the supplement.** `supplement.tex:197` advertised that "paired TOST
**equivalence** tests are computed by the released `stats.py`" and **never reported their
outcome**. Not an assertion, so not a fatal violation — but it reads two ways, both bad: the TOSTs
failed and were suppressed, or the equivalence inference is being invited by insinuation while the
word stays deniable. Ledger rule 4 says the word "does not appear in the paper's Design-Bench
sections"; the supplement's Significance Details **is** one, and the word was there.

Second finding: **the supplement stated the Design-Bench null with zero power scoping** — no
Demšar threshold, no Agarwal caveat, no MDE — even though that is where the omnibus p-values
actually live. A reviewer checking the numbers standalone saw a bare null.

### CHECK B — within-corner separation

Four sites compare η²_opt against η²_surr inside a corner. **One was completely naked.**

- `:220` — guard present but **two sentences downstream** and **carrying no numbers**, while
  `MUJOCO_CHECK.md` had them unused. → patched.
- `:222` — guard present, numeric, correct. **Accepted as-is.**
- **`:232` — NO GUARD ANYWHERE IN THE PARAGRAPH.** The broadest within-corner claim in the paper
  ("η²_opt exceeds η²_surr in every corner of every task set we report"), and the paragraph's own
  "Four limits are ours" list did **not** include the interval-overlap limit. Directly contradicted
  the paper's stated limit two paragraphs earlier. → patched.
- `:52` (abstract) — no violation.

### CHECK C — the MuJoCo localization

**Substantively airtight, rhetorically under-deployed.** All three `MUJOCO_CHECK.md` facts were
present at `:220` but buried: the paragraph opened on the 5-task null, ran through a GFP
robustness note, delivered the localization mid-paragraph, and **closed on the unrelated Benavoli
pooling defect**. The paper's single best answer to this attack sat between a footnote and a bug
disclosure, unsignposted.

Two concrete gaps:
1. **"Floor of its own bootstrap interval" was quantified only for the 5-task set** ("bottom
   tenth"). For the MuJoCo set that actually *rejects*, "floor" was a bare adjective —
   `MUJOCO_CHECK.md`'s verified "**bottom fifth of its own interval**" went unused. That is exactly
   the crack the attack aims at.
2. **The paper never named the "null is fragile" reading.** Out of character — it names and rebuts
   objections everywhere else ("search intensity wearing a costume", "the counter-objection is
   ours to state"). §6's central vulnerability was the one objection never named.

### Also checked — `:226` "the only rejections anywhere"

**Inconsistent as written.** "Anywhere" flatly contradicted `:220` (MuJoCo rejects 3/4) and `:222`
(matched budgets reject 4/4) — a self-contradiction six lines from its own refutation. The
underlying numbers were correct; only the scope word was wrong. **The bug was inherited from ledger
D20**, which used the same unqualified phrasing — so the ledger was corrected in parallel to stop
the next audit pass re-deriving it.

### Patches applied — 6 sites

| # | Site | Defense added |
|---|---|---|
| R3-1 | `main.tex:226` | Scoped to "within this oracle-subset analysis"; states explicitly that the MuJoCo and budget-matched rejections are a different partition and not in tension. |
| R3-2 | `main.tex:220` | The withheld **"bottom fifth of its own interval"** supplied; the min/max fact added (largest surrogate effect 0.091 < smallest optimizer effect in any rejecting corner 0.146); the overlap guard moved **into the same sentence**, with its numbers (on_on surr [0.006,0.305] vs opt [0.008,0.468]). |
| R3-3 | `main.tex:232` | "in point estimate" + adjacent overlap guard. Enforces D19 limit (ii) at the one call site that escaped it. |
| R3-4 | `main.tex:220` | **Names the fragility reading and rebuts it**: adding MuJoCo moves the omnibus but does not move η²_surr out of the floor (0.001–0.032 → 0.044–0.091, four to nine times below the synthetic 0.405). "A fragile surrogate null would show a surrogate effect that grows with the task set and tracks the omnibus; ours grows barely and tracks it inversely." Plus the we-did-not-drop-the-inconvenient-tasks move. |
| R3-5 | `supplement.tex:197` | Body's power defense replicated where the p-values live: Agarwal, Demšar's >10-dataset regime, the \|d_z\|≥1.27 MDE. |
| R3-6 | `supplement.tex:197` | TOST reference defused — the computation is disclosed, explicitly relied upon for nothing, and the word "equivalence" leaves the Design-Bench sections. Satisfies rule 4 by its **letter** as well as its spirit. |
| R3-7 | `docs/CLAIM_LEDGER.md` D20 | Same "anywhere" scope fix, at the source. |

**Deviation from the reviewer's proposed text:** R3-4 was drafted with "still an order of magnitude
below the synthetic grid's 0.405" (the phrasing in `MUJOCO_CHECK.md`). 0.405/0.091 = 4.5×, so
"order of magnitude" overstates at the top of the band. Replaced with the exact **"four to nine
times below"** — a checkable number rather than a loose idiom, which is the stronger defense.

---

## Verification

- **Compile:** both documents build clean. **Zero undefined citations** — all five keys
  (`li2024bnnsurrogates`, `shahriari2016humanoutoftheloop`, `chemingui2024pggs`,
  `agarwal2021precipice`, `demsar2006statistical`) resolve in `references.bib`, which the
  supplement shares.
- **Page count unchanged: main 12pp, supplement 4pp**, before and after, despite +766 words in the
  body. Float packing absorbed it.
- **Additive check:** 17 lines modified, **0 lines deleted**. Every patch extended a sentence;
  none replaced a claim with a weaker one. main.tex +766 words, supplement.tex +131.
- **Equivalence audit:** 5 hits, **all denials, zero assertions**. The one supplement exposure is
  removed.
- **Struck claims stay struck:** no `0.51/0.47` pair, no "GP fits better" in any phrasing; `0.95`
  survives only inside its own withdrawal sentence, as rule 6 requires.
- **Authorship:** the tool-attribution grep returns zero hits across the paper and the ledger.

## No claim was diluted

Every one of the 21 patches added a scope guard, an explicit number, or a named citation. Three
patches (R2-2, R2-5, R3-4) state a claim **more forcefully** than the draft did. Two (R2-3, R3-2)
replace a vague word with the measured magnitude and its interval. The falsification of PGS's
local premise, the 0.405 strengthening, the seven eliminations, the D19 optimizer promotion, and
the W1/W2 width results are all asserted at the same strength as before — with their scope
sharpened so a reviewer cannot misread any of them as an overclaim.

**Residual exposure, ranked.** R1's contribution paragraph now names L/R/W, but the paper still
claims no credit contest on surrogate-axis breadth — if a reviewer *is* an L/R/W author, the
concession at `:63` is the sentence doing the work, and it should survive any future length edit
intact. R2's deferred contributions-list item remains the one known gap in the skim path.
