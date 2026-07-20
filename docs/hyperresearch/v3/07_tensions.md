# Step 7 — Source tensions

Run `mbo-gauntlet-r4-adversarial-0f06f1` · branch `gauntlet-r4` · 2026-07-20

## Output

`research/temp/source-tensions.json` — **6 tensions**, 5 high relevance, 1 medium. Each carries
both sides with proponents and a **committed resolution**, per the no-open-tensions rule.

| Origin | Tension |
|---|---|
| contradiction-graph | Is a deep ensemble's variance informative about error? |
| contradiction-graph | Does de-confounding that raises an effect indicate validity or leakage? |
| **orphan-scan** | Min-max normalization: field convention or known-broken instrument? |
| comparisons | Local BO: does acquisition-driven search over-explore or get trapped? |
| contradiction-graph | Is pessimism the source of offline gains, or an amplifier? |
| **orphan-scan** | Landscape-driven surrogate selection: mature method or unresolved thread? |

## The two orphan tensions justify this step

Both were invisible to locus-driven analysis because they cut across topics, and both turn out
to carry the sharpest material in the set.

**Min-max normalization.** The technique's *originating paper* — Bellemare et al. 2013, ALE —
documents it flipping a ranking (Zaxxon). Jordan et al. 2020 names the exact endogenous form as
outlier-exploitable. The field adopted it as convention anyway, Design-Bench inherited it, and
this paper inherited it from Design-Bench. That is a more interesting story than "normalization
is a choice", and it converts the audit's concern from a general worry into a citable lineage.

**Landscape-driven surrogate selection.** Werth et al. 2019's finding that surrogate-computed
landscape features are *"more indicative of the surrogate model than the original landscape"* is
a circularity at the heart of the idea: if the features tell you about the instrument rather
than the problem, using them to select the instrument is close to question-begging. That
explains why a mature solver-selection literature never extended to surrogates — an obstacle,
not an unfilled gap.

## Resolutions committed, not left open

Every tension has a committed reading. Three resolve by **scoping** rather than by picking a
winner — the ensemble-variance tension (in-distribution versus off-support), the pessimism
tension (sufficiency versus attribution), and the de-confounding tension (psychology-general
versus ML-specific). Naming the scoping variable is the resolution in each case, and in each
case it is the variable the paper under audit has collapsed.

One resolves as a **burden-shift**: the paper's narrow N9 claim survives Hamdan, but acquires an
obligation to rule out leakage that it can discharge cheaply and currently does not attempt.

One resolves **against borrowing authority**: nobody owns the trapped-at-the-data failure mode,
and the paper's own frozen-cell evidence is stronger than the citation it is trying to lean on.

## Next

Step 8 — corpus critic.
