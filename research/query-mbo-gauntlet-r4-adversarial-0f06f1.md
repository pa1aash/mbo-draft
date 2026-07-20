---
vault_tag: mbo-gauntlet-r4-adversarial-0f06f1
created: 2026-07-20T06:47:35Z
source: user-prompt
---

TIER: full. All 16 steps. Do not abbreviate. This is an adversarial self-critique of a
completed paper, not a novelty scout of an idea.

===================================================================
THE TASK
===================================================================
I have a completed AAAI-27 submission draft on offline model-based optimization. Your job is
to be the reviewer who does the homework the other reviewers won't: critique EVERY claim
against the primary literature, verify EVERY citation is used for what the cited paper
actually says, hunt for any prior work that KILLS a load-bearing claim, and find whether
there is a stronger paper in this data that is not being written — something unexplored, or
explored but under-executed or under-explained.

The full paper text is at paper/aaai27/main.tex and paper/aaai27/supplement.tex in this
repo (read them). The claim ledger is docs/CLAIM_LEDGER.md. The prior novelty audit is
docs/NOVELTY_V3.md — treat its verdicts as PRIOR, to be re-checked, not trusted.

===================================================================
YOUR HIGHEST-PRIORITY TASK — do this first and hardest
===================================================================
N6 is the paper's load-bearing NONE-FOUND: "no prior work runs a crossed surrogate x
optimizer factorial in offline MBO." Its failure is UNRECOVERABLE — if such a paper exists,
the first contribution collapses. Re-verify it against the live literature with fresh
fetches:
  - a prior crossed/factorial surrogate x optimizer decomposition in offline MBO or offline
    black-box optimization (the exact thing);
  - anything published SINCE the last audit (2026 especially — the field moves; a recent
    paper could have appeared);
  - the near-misses the last pass found (Hutter fANOVA one-way, Liang online, Moosbauer HPO
    declining the two-way) — confirm each still only NEAR-misses and none has been extended.
Report N6 as CONFIRMED NONE-FOUND (with the queries) or KILLED (with the paper). This is
existential; everything else is improvement.

===================================================================
THE THREE DELIVERABLES — structure your output as exactly these
===================================================================
(i) MANDATORY — CLAIMS THE LITERATURE CONTRADICTS OR THAT ARE MISCITED.
    For every substantive claim in the paper, and every citation:
    - Does the cited paper actually say what the paper cites it for? Check the load-bearing
      ones by fetching and grepping the primary: SNGP (liu2020sngp) for distance-aware
      uncertainty, Fan (fan2024minucb) for UCB-as-local-search / the LCB-paralysis framing,
      Shahriari (2016) for the doctrine we scope against, Li/Rudner/Wilson (2024) for the
      cross-surrogate comparison, Kim (2026) for the attribution-gap concession, Agarwal +
      Demsar for the power argument. A citation used for a claim the source doesn't support
      is a mandatory fix.
    - Does the literature CONTRADICT any claim the paper asserts? (e.g. does anyone show the
      ensemble's sigma IS an error signal, contradicting the distance-signal claim? does
      anyone show K-robustness DOWN to K=2, contradicting the K-sensitivity framing?)
    For each: the claim, the paper's citation/framing, what the source actually says, and
    the required fix.

(ii) MANDATORY — KILLS. Any prior work that refutes N6 or any specific ledger claim. A
     single fatal counterexample matters more than a hundred improvements.

(iii) RANKED — SCOPE OF NOVELTY. The stronger paper hiding in this data. For each finding,
     tag it: FOLD-INTO-THIS-PAPER (strengthens the current submission, worth doing before
     the deadline), FOLLOW-UP-PAPER (real but out of scope for this submission), or
     NOT-WORTH-IT. Specifically hunt for:
     - a claim the paper UNDER-states relative to its own evidence (the budget-axis
       separation and the two-strengthenings pattern are candidates — is either a bigger
       result than the paper frames?);
     - a result explored but UNDER-EXECUTED: the seven eliminations rule things out but
       reach no positive mechanism — is there a specific, runnable experiment the
       literature suggests would convert elimination to mechanism? If so, name the
       experiment and cite the work that motivates it. Tag whether it's CHEAP (foldable
       before deadline) or EXPENSIVE (follow-up).
     - a result explored but UNDER-EXPLAINED: a finding whose significance the paper states
       flatly and that the literature would let it frame more sharply.

===================================================================
METHOD CONSTRAINTS (this project has caught fabrications — hold the line)
===================================================================
- Semantic Scholar / arXiv / OpenAlex BEFORE web search, every claim.
- FETCH PRIMARY AND GREP. Never a novelty or contradiction verdict from a snippet.
- Citation traps confirmed on this project: Li/Rudner/Wilson is ICLR 2024 (S2 says 2023);
  Henderson is AAAI 2018 (S2 says 2017); Benavoli is JMLR 2016 (arXiv 2015). Verify years.
- The vault at ~/.hyperresearch is GLOBAL and holds the previous pass's corpus — do NOT
  reuse a cached source for a verdict; re-fetch and note it.
- Every one of the 16 steps commits its own docs/hyperresearch/v3/NN_<step>.md.

===================================================================
DELIVERABLE
===================================================================
docs/GAUNTLET_R4.md, structured as the three deliverables above, N6 verdict first. For each
mandatory item: the fix. For each ranked-novelty item: the tag. Commit continuously on a new
branch gauntlet-r4, never to main. Authorship: Palaash Gang <palaashgang@gmail.com>, zero
AI/agent/co-authored strings in any commit, file, or the report. Terminal section: "What I
could not verify and why."
