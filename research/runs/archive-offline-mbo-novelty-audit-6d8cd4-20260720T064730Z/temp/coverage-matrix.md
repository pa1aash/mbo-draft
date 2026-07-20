## Coverage Matrix — query phrase → atomic item mapping

| Query phrase (verbatim) | Mapped atomic item(s) | Scope check | Gap? |
|---|---|---|---|
| "which of my findings are genuinely new" | Sub-Q1 (novelty of N1-N9) | OK — full scope, all nine claims | No |
| "what does existing work already own" | Sub-Q1/Sub-Q2 (PRIOR WORK FOUND branch) | OK | No |
| "strongest publishable contribution available" | Sub-Q12 (A/C/D one-sentence test) | OK | No |
| "citations to papers you have actually fetched and read" | scope_condition: primary literature only, fetch+grep | OK | No |
| "PRIOR WORK FOUND / NONE FOUND / NOT VERIFIABLE" | required_formats: verdict table taxonomy | OK — three-valued verdict | No |
| "N1 confound taxonomy" (5 sub-confounds i-v) | Entity N1 + required_field residual | OK — target scaling, candidate/oracle, optimizer tuning, ensemble size K, effective pessimism all named | No |
| "is the SHAPE of this contribution already owned" | Sub-Q3 | OK | No |
| "Ferrari Dacrema / Balduzzi / Henderson / Musgrave / Lucic / Agarwal" | 6 paper-to-fetch entities | OK — all six enumerated with venue traps | No |
| "residual that is specific to offline MBO" | Sub-Q3 required_field | OK | No |
| "N2 K-contingency of surrogate-class comparison" | Entity N2, Sub-Q4 | OK — ranking vs accuracy distinction preserved | No |
| "Abe et al. (NeurIPS 2022)" | paper-to-fetch entity | OK | No |
| "N3 unmatched effective pessimism" | Entity N3, Sub-Q5 | OK — BO/offline-RL/offline-MBO scope | No |
| "N4 distance-aware uncertainty / dangerous neighbourhood" | Entity N4, Sub-Q6 | OK — SNGP/DUE/TuRBO/confidently-wrong all covered | No |
| "beta=0 control ... ready either way" | N4 required_field both_beta0_outcomes | OK — both mechanism-supporting and mechanism-refuting literature | No |
| "N5 NTK / spectral bias" | Entity N5, Sub-Q7 | OK — Jacot/Rahaman/Lee/Li-Rudner-Wilson | No |
| "infinite-width BNNs ... high dimensions" (Li/Rudner/Wilson) | paper-to-fetch, venue trap ICLR 2024 | OK — flagged as most-valuable-missing-fetch | No |
| "N6 crossed factorial ... one counterexample is fatal" | Entity N6, Sub-Q8 | OK — load-bearing, adversarial | No |
| "factorial ANOVA surrogate optimizer" (+3 more queries) | N6 exact-query list carried to step 2/5 | OK | No |
| "Tan et al. ICLR 2025 / Chemingui AAAI 2024 / Trabucco / Kim 2025 survey" | paper-to-fetch entities | OK | No |
| "N7 bidirectional smoothness manipulation" | Entity N7, Sub-Q9 | OK — smooth-net AND roughen-GP both directions | No |
| "IGNITE (NeurIPS 2024) and MS-DDEO (SWEVO 2022)" | paper-to-fetch, forward-cite 2025-2026 | OK | No |
| "N8 platform and library-version dependence" | Entity N8, Sub-Q10 | OK — macOS/Linux, RNG, numerical determinism | No |
| "Gundersen & Kjensmo (AAAI 2018)" | paper-to-fetch entity | OK | No |
| "N9 de-confounding direction ... audit STRENGTHENS" | Entity N9, Sub-Q11 | OK | No |
| "Recht et al. (ImageNet) ... Melis et al. (LSTM)" | paper-to-fetch entities for N9 | OK | No |
| "three candidate papers (A) (C) (D)" | Candidate-paper entities A/C/D | OK — repaired-measurement / mechanism / confound-taxonomy | No |
| "one sentence a reviewer could not get from any prior paper" | required_formats: one-sentence-owned test | OK | No |
| "three strongest citations that could REJECT this paper" | Sub-Q13, required_formats | OK | No |
| "AAAI-27 venue fit ... areas-and-topics ... Fetch the topics page; do not recall it" | Sub-Q14, time_periods AAAI-27 primary source | OK — fetch mandate explicit | No |
| "which primary topic best fits each of A/C/D ... reviewer pool" | Sub-Q14 | OK | No |
| "Save final report to docs/NOVELTY_V3.md" | wrapper_contract (scaffold), NOT decomposition | OK — correctly excluded from atomic items | No |
| "Terminal section: What I could not verify and why" | required_sections terminal + heading contract | OK | No |

**Result: zero `Gap? = YES` rows.** Every significant noun phrase, proper noun, and named paper maps to an atomic item at full natural scope. The nine claims each have a dedicated entity + required section heading; all ~24 named papers-to-fetch are enumerated with their venue/year traps; the two synthesis deliverables (candidate one-sentence test, rejecting citations) and the venue-fit fetch are captured; wrapper requirements are correctly held out of the decomposition and live in the scaffold.
