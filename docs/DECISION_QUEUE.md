# Decision queue

Questions only you (or the judgment-layer instance) can answer. Each has options and the
consequence of each. Ordered by how much downstream work they unblock.

---

## D1 · Does the paper ship at all this cycle?

`docs/FLAW_LEDGER.md` P0-0 is not an objection a reviewer *might* raise — it is the authors'
own control, in the released artifact, refuting the paper's mechanism, with a pre-stated
decision rule the result fails. P0-2 (the ensemble trains on raw targets while both GPs
z-score) means the headline η² is confounded with target scaling. Neither is arguable; both
need a grid re-run.

| Option | Consequence |
|---|---|
| **Re-run and re-scope for this deadline** | Needs M0 + P0-1's protocol fix in one pass (~1 day edit, ~1–2 grid runs). Feasible **only if** the deadline is ≥3 weeks out. The paper that emerges is different from the one drafted. |
| **Withdraw from this cycle, target the next** | Costs a cycle. Buys the M0→M2→M3 program, which is what turns this into a strong paper rather than a repaired one. |
| **Ship as-is** | **I recommend against this.** A reviewer who opens `gradtune.py` finds the refutation in five minutes. The artifact is the evidence against the paper. |

**What I need from you:** the actual deadline. Everything else scales off it.

---

## D2 · Which paper is this? (see `docs/PAPER_V2_OUTLINE.md`)

Identity A (repaired measurement), B (diagnostic-as-method, contingent on 5.1), C (mechanism,
contingent on M0/M2/M3). B and C are **complementary, not exclusive** — C supplies the mechanism
that explains *why* B's selection signal works. A+C is the safe strong paper; B+C is the ambitious one.

**Consequence:** determines whether the DB null is the paper's weakness (A), its motivation (B),
or one point on a continuum (C).

---

## D3 · Does the pre-registration ship, and does the paper admit its hypothesis was refuted?

`PREREGISTRATION.md` registered the headline as *"the optimizer explains most of the gap."* The data
gave η²_opt = 0.01 — the opposite. The paper never cites the pre-registration, and reports the
reversed finding as if it were the hypothesis.

| Option | Consequence |
|---|---|
| **Ship it and say so** (recommended) | "We pre-registered the optimizer hypothesis; the data refuted it" is *evidence the test was real*. It converts the reversal from a liability into the paper's credibility anchor. It also forces disclosing P1-4 (DB significance claims violate the pre-reg) and the unrun n=50 arms. |
| **Don't ship it** | The paper is silently un-preregistered. Nothing in the submission is false, but the repo contradicts the framing if anyone looks. |

**This is a judgment call about how much candour helps.** My read: at AAAI, disclosed refutation reads
as rigour; discovered non-disclosure reads as HARKing. But it's your call.

---

## D4 · What happens to Contribution 2 (the coverage diagnostic)?

Coverage exists for **1 of 9 cells** (P0-3), the cross-proposal claim varies both factors at once
using a *different GP* than the grid, and the mechanism it explains (the ensemble×gradient collapse)
is itself a tuning artifact (P0-0). Propositions 1 and 2 carry no content (P1-7).

| Option | Consequence |
|---|---|
| **Rebuild it: full 3×3 coverage + implement the density-ratio repair (M5)** | ~1 day + ~1 CPU-day. Turns a 6-bar chart into a 9-cell scatter and turns Prop 2 from a restatement into a tested claim. Required for Identity B. |
| **Cut to a remark** | Loses a contribution but removes P0-3, P0-5, P1-7 at a stroke. Makes the paper A-shaped and thin. |
| **Keep as-is** | Not viable — P0-3 and P0-5 are both reject-drivers. |

---

## D5 · GFP: quarantine or keep?

The claim "in-distribution coverage is below nominal (0.73/0.77)" is carried entirely by GFP = 0.00,
which **the supplement itself calls a degenerate decode artifact**. Excluding GFP the mean is 0.895 ≈
0.90 and the claim **reverses** (P0-5).

| Option | Consequence |
|---|---|
| **Quarantine GFP, report both** | The headline claim disappears. Honest, and removes a reject-driver. |
| **Keep GFP in the headline** | Indefensible once a reviewer reads your own supplement. |

**This one I'd treat as already decided** — but it's your number to retract, not mine.

---

## D6 · How many tasks, and is the power analysis the contribution?

TOST at N=7 with ±0.48 is uninformative and the abstract already concedes it. Options: add tasks
(SOO-Bench? more DB tasks?), or reframe.

The cheapest real contribution here: **a power analysis** — "a discriminative offline-MBO benchmark
needs ≥N tasks at the observed effect sizes; existing suites have 7." It costs ~0 CPU and converts the
weakest claim into a *specification*. M3 (smoothness interpolation) is the stronger alternative: it
replaces the two-point N=7 comparison with a continuous trend, which needs no equivalence test at all.

**Consequence:** determines whether Contribution 3 stays a null (weak) or becomes a benchmark
specification (defensible) or a trend (strong).

---

## D7 · Do we tell anyone the released baselines diverge?

Our COMs reproduces at 2.21 vs official 0.99 on TF-Bind-8 — a 1.22-unit gap the paper quotes as "2.20"
(a third value). The one "matches official" number (CbAS, |Δ|=0.004) **fails to verify against its own
row** (2.13 − 2.12 = 0.01) (P1-6).

| Option | Consequence |
|---|---|
| **Diff against the official repo and fix** | ~1 day. Removes "their baselines are wrong, so the null is theirs, not the field's." |
| **Report the divergence openly with the published range** | `SKELETON.md:45` already planned this ("published COMs varies ±0.1 across re-runs"). But 1.22 ≫ 0.1, so the planned defense does not cover the observed gap. |

---

## D8 · README and supplement packaging

`README.md` ships in the supplement per its own line 54. It describes the **ICML workshop paper** as
"CURRENT", says **n=10 seeds** against the paper's 30, and points at superseded code. Shipping it hands
a reviewer a contradiction on page 1 of the artifact.

**Options:** rewrite it (~1 h), or exclude it from the zip. Low stakes, zero ambiguity — but it needs
a decision because the supplement manifest is yours.

---

## D9 · The two deleted research notes

`SKELETON.md:3,35,44` builds the paper's positioning and baseline strategy on
`research/notes/final_report_mbo-decomposition-prior-art-579ba4.md` (the R1 novelty verdict) and
`research/notes/baseline-numbers-designbench.md` (R2). **Neither exists anywhere on disk.**

The novelty claim "we present the first controlled decomposition" traces to a document that is gone.
**Options:** re-run the novelty check (in flight this session — see `docs/EXTENSION_LEDGER.md`), or
locate the originals. Until then the paper's central novelty claim is **unverified**, and my
independent check has already surfaced the nearest threat: Li/Rudner/Wilson (ICLR **2023**, not 2024 as
cited) already reports "deep ensembles perform relatively poorly" and "the ranking of methods is highly
problem dependent, suggesting the need for tailored inductive biases" — with the acquisition held fixed.
How much of Contribution 1's *finding* that paper already owns is a judgment call I'm handing you.

---

## D10 · Authorship and repo provenance

The repo's 19 pre-existing commits are authored by `juunnq <arjunveluri.work@gmail.com>` and
`mbo <mbo@local>`. The prior `origin` (`juunnq/offline-mbo`) is **not reachable** with this machine's
SSH key. I preserved it as `upstream`, pointed `origin` at `pa1aash/mbo-draft` (private, confirmed), and
left all existing commit authorship untouched.

**Flagging, not deciding:** if this is a collaboration, the collaborator may need to know the work moved,
and the AAAI submission's author list is not something I can infer. No action taken.
