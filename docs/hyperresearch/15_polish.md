# 15 · Polish — the final acceptance thesis

**One paragraph, cleaned.**

AAAI-27 will publish this paper's genre — a no-new-method measurement study — because it has done so
four times on the ML technical track (Henderson, Gundersen & Kjensmo, Kim, Zeng), so acceptance turns
not on genre legitimacy but on three conditions the reviewer record makes explicit: a *declared* null
that *diagnoses its own mechanism*, a *de-confounded* artifact that survives a reviewer-scored
reproducibility checklist, and a *shipped deliverable* rather than a bare null. The paper meets none of
them today, and all three are blocked by the same fact — the released `gradtune.py` refutes the paper's
mechanism (P0-0), the ensemble trains on raw targets while the GPs standardize (P0-2), and the reported
statistics have no generating code (P0-4) — so the single highest-leverage move is to run one
de-confounding grid (normalize the ensemble's targets, equalize the candidate/oracle protocol) and
report the gradtune sweep alongside it, because that one action simultaneously removes the top
reject-driver, unblocks the checklist, and decides which paper exists. That decision is a three-way
branch, not a foregone one: if the surrogate main effect survives normalization the paper becomes
Identity C (smoothness is the axis, shown by bidirectional manipulation — the reviewer corpus's minimum
bar, not its ceiling), paired with the free task-count power specification (X4) that closes a 20-year
gap Demšar left open and turns the weakest half of the paper into a contribution; if the effect
survives but the mechanism cannot be rebuilt before 2026-07-28, the honest home is MLRC 2026 rather
than a forced AAAI submission; and if the effect evaporates, Identity E — the self-demonstrating
reversal, the only framing in which the refuted pre-registration is an asset — is the live fallback.
Route it as `ML: Evaluation, Benchmarking, Datasets & Analysis` with minimal secondaries (every
deep-technical keyword hands a specialist a veto over one of our confounds), keep everything
load-bearing inside seven pages, declare the null and the reversal up front, answer the "your oracles
are broken" competing explanation with the exact-oracle subset, and never end on the negative — because
with the deciding grid still PENDING eleven days out, the paper's fate is not a question of argument but
of one run that has not yet finished.
