#!/usr/bin/env python3
"""Mechanical concatenator for docs/BUNDLE*.md. Verbatim only. No summarization."""
import os, subprocess, sys

REPO = '/Users/palaash/Downloads/MBO'
os.chdir(REPO)

LANG = {'.py': 'python', '.tex': 'latex', '.md': 'markdown', '.sh': 'bash',
        '.json': 'json', '.txt': 'text', '.yaml': 'yaml', '.yml': 'yaml',
        '.toml': 'toml', '.cfg': 'ini', '': 'text', '.Dockerfile': 'dockerfile'}

def sh(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout.rstrip('\n')

def lastcommit(path):
    out = sh(f"git log -1 --format='%h %ad' --date=short -- {path!r}")
    return out if out else 'UNTRACKED/UNCOMMITTED'

# (tier, requested_path, actual_path_or_None, note)
#  actual_path None  -> emit DOES NOT EXIST block
SPEC = [
    # ---- TIER 1 ----
    (1, '__X1X3_STATUS__', '__SPECIAL_X1__', 'live run status + verbatim pre-registration'),
    (1, 'docs/FINAL_REPORT.md', None, 'never created this session; the final report was delivered in chat, not written to disk'),
    (1, 'docs/GRADTUNE_RESULT.md', None, 'never created; the gradtune result lives verbatim in FLAW_LEDGER.md P0-0'),
    (1, 'docs/UNSUPPORTED_CLAIMS.md', None, 'never created; unsupported/untraceable claims live in PROVENANCE.md and FLAW_LEDGER.md P0-4'),
    (1, 'docs/DECISION_QUEUE.md', 'docs/DECISION_QUEUE.md', ''),
    # ---- TIER 2 ----
    (2, 'code/mbo.py', 'code/mbo.py', 'ENTIRE file; contains the X1/X3 edits made this session'),
    (2, 'code/gradtune.py', 'code/gradtune.py', 'ENTIRE file; the P0-0 evidence'),
    (2, 'code/run_all.py', 'code/run_all.py', 'ENTIRE file'),
    (2, '__GIT_CDD5AD8__', '__SPECIAL_GIT1__', 'git show cdd5ad8 --stat + full commit message'),
    (2, '__GIT_LOG__', '__SPECIAL_GIT2__', 'git log --oneline --all | head -40'),
    (2, 'docs/IMPLEMENTATION_AUDIT.md', 'docs/IMPLEMENTATION_AUDIT.md', ''),
    (2, 'docs/PROVENANCE.md', 'docs/PROVENANCE.md', ''),
    (2, 'code/analysis.py', 'code/analysis.py', 'task_norm: the analysis-time normalizer'),
    (2, 'code/stats.py', 'code/stats.py', 'Wilcoxon/Holm/Friedman/bootstrap'),
    (2, 'code/run05.py', 'code/run05.py', 'PROVENANCE generator: eta^2 / CD / TOST -> 05_findings.json'),
    (2, 'code/db_tasks.py', 'code/db_tasks.py', 'Design-Bench adapters + RF oracles'),
    (2, 'code/figures.py', 'code/figures.py', 'PROVENANCE generator: paper/figures_v2/*'),
    (2, 'code/tables.py', 'code/tables.py', 'PROVENANCE generator: paper/tables_v2/*'),
    (2, 'code/run_gpcov.py', 'code/run_gpcov.py', 'cross-proposal coverage (P0-3 evidence)'),
    (2, 'code/run_beta0.py', 'code/run_beta0.py', 'beta=0 control'),
    (2, 'code/run_subsample.py', 'code/run_subsample.py', 'data-subsample control'),
    (2, 'code/quicklook.py', 'code/quicklook.py', 'result inspector'),
    (2, 'requirements.txt', 'requirements.txt', 'pinned env'),
    (2, 'cloud/setup.sh', 'cloud/setup.sh', 'shell driver'),
    (2, 'cloud/fix_designbench.sh', 'cloud/fix_designbench.sh', 'shell driver'),
    (2, 'cloud/local_queue.sh', 'cloud/local_queue.sh', 'shell driver'),
    (2, 'cloud/Dockerfile', 'cloud/Dockerfile', 'config'),
    (2, 'cloud/queue/run_queue.sh', 'cloud/queue/run_queue.sh', 'shell driver'),
    (2, 'cloud/queue/run_after_01.sh', 'cloud/queue/run_after_01.sh', 'shell driver'),
    (2, 'cloud/queue/00_smoke.sh', 'cloud/queue/00_smoke.sh', 'shell driver'),
    (2, 'cloud/queue/01_synth_factorial.sh', 'cloud/queue/01_synth_factorial.sh', 'shell driver'),
    (2, 'cloud/queue/02_db_factorial.sh', 'cloud/queue/02_db_factorial.sh', 'shell driver'),
    (2, 'cloud/queue/03_official_baselines.sh', 'cloud/queue/03_official_baselines.sh', 'shell driver'),
    (2, 'cloud/queue/04_calibration.sh', 'cloud/queue/04_calibration.sh', 'shell driver'),
    (2, 'cloud/queue/05_analyze.sh', 'cloud/queue/05_analyze.sh', 'shell driver'),
    (2, 'cloud/queue/README.md', 'cloud/queue/README.md', 'queue documentation'),
    (2, '.gitattributes', '.gitattributes', 'config'),
    (2, '.gitignore', '.gitignore', 'config'),
    # ---- TIER 3 ----
    (3, 'paper/aaai27/main.tex', 'paper/aaai27/main.tex', 'ENTIRE file incl. comments'),
    (3, 'docs/PAPER_V2_OUTLINE.md', 'docs/PAPER_V2_OUTLINE.md', ''),
    (3, 'docs/EXTENSION_LEDGER.md', 'docs/EXTENSION_LEDGER.md', ''),
    (3, 'docs/PREREGISTRATION.md', None, 'no file at this path. The ORIGINAL pre-registration is at repo root PREREGISTRATION.md; the revision pre-registration is docs/PREREGISTRATION_V2.md. Both included below under their real paths.'),
    (3, 'PREREGISTRATION.md', 'PREREGISTRATION.md', 'the ORIGINAL frozen pre-run contract (repo root)'),
    (3, 'docs/PREREGISTRATION_V2.md', 'docs/PREREGISTRATION_V2.md', 'the revision pre-registration written this session'),
    (3, 'docs/NOVELTY.md', None, 'no file at this path; the novelty check is docs/NOVELTY_CHECK.md, included below'),
    (3, 'docs/NOVELTY_CHECK.md', 'docs/NOVELTY_CHECK.md', 'the actual novelty/prior-art check'),
    (3, 'docs/SCOPE_EXPANSION.md', None, 'never created. Phase 7 scope-expansion decisions were folded into the "Rejected, with reasons" section of docs/EXTENSION_LEDGER.md rather than given their own file.'),
    (3, 'docs/FLAW_LEDGER.md', 'docs/FLAW_LEDGER.md', ''),
    (3, 'docs/FREE_WINS.md', None, 'no file at this path. Only 5.1 completed and it is docs/FREE_WIN_5_1_offline_selection.md, included below. 5.3 produced raw output only (agent died before writing its summary); 5.2/5.4 never ran.'),
    (3, 'docs/FREE_WIN_5_1_offline_selection.md', 'docs/FREE_WIN_5_1_offline_selection.md', 'the offline-selection reanalysis (verdict: FAILS)'),
    (3, 'docs/FREE_WIN_5_3_eta_robustness_raw.txt', 'docs/FREE_WIN_5_3_eta_robustness_raw.txt', 'raw eta^2 robustness output; no summary was written'),
    (3, 'docs/MECHANISM_EXPERIMENTS.md', 'docs/MECHANISM_EXPERIMENTS.md', ''),
    (3, 'docs/CHAT_DIGEST.md', 'docs/CHAT_DIGEST.md', ''),
    (3, 'docs/VENUE_NORMS.md', 'docs/VENUE_NORMS.md', 'venue norms + verbatim reviewer evidence'),
    (3, 'docs/ARTIFACT_INVENTORY.md', 'docs/ARTIFACT_INVENTORY.md', 'result-artifact schema/seed/completeness audit'),
    (3, 'docs/scripts_offline_selection.py', 'docs/scripts_offline_selection.py', '5.1 analysis script'),
    (3, 'docs/scripts_eta_robustness.py', 'docs/scripts_eta_robustness.py', '5.3 analysis script'),
]
# Tier 4: hyperresearch, discovered dynamically
for i in range(1, 17):
    pass

def hyperresearch_files():
    out = []
    d = 'docs/hyperresearch'
    have = sorted(os.listdir(d)) if os.path.isdir(d) else []
    for i in range(1, 17):
        pre = f'{i:02d}_'
        matches = [f for f in have if f.startswith(pre)]
        if matches:
            for m in matches:
                out.append((4, f'{d}/{m}', f'{d}/{m}', f'hyperresearch step {i}'))
        else:
            out.append((4, f'{d}/{i:02d}_<step>.md', None,
                        f'hyperresearch step {i} never ran. Only steps 1-2 of the 16-step pipeline were executed; '
                        f'the literature work was delegated to focused agents instead (see chat log / NOVELTY_CHECK.md, VENUE_NORMS.md).'))
    return out

SPEC += hyperresearch_files()


def special_x1():
    log = 'logs/x1x3_run.log'
    status = open(log).read() if os.path.exists(log) else '(no log)'
    running = sh("ps aux | grep -E 'x1x3_driver|run_all.py' | grep -v grep")
    prereg = ''
    if os.path.exists('docs/PREREGISTRATION_V2.md'):
        for line in open('docs/PREREGISTRATION_V2.md'):
            if line.strip().startswith('| **X1**'):
                prereg = line.rstrip('\n')
    body = []
    body.append('### Live status\n')
    body.append('**There was no pre-existing X1 run.** No shell was running when this task began: '
                '`ps` showed no grid process, `logs/` did not exist, and no `x1x3*` file existed anywhere. '
                'X1 had never been launched.\n')
    body.append('**Why it could not have been running:** there is no PyTorch on this machine. '
                '`venv/` is a *Windows-layout* venv (`Include/ Lib/ Scripts/`) and has no macOS interpreter; '
                'the miniforge python has numpy 2.4.4 but no torch, botorch, gpytorch, or cma. '
                'The published results were produced on a RunPod cloud pod via `cloud/setup.sh`, not locally.\n')
    body.append('**What I did:** implemented X1 and X3 in `code/mbo.py` as reversible switches '
                '(`X1_STANDARDIZE_Y`, `X3_MATCHED_PROTOCOL`), then launched a background driver that builds an '
                'isolated venv (NOT the user\'s miniforge base, which other projects pin to numpy 2.4.4), '
                'smoke-tests the switches, and runs the full synthetic grid at 30 seeds.\n')
    body.append('\n**Process check at bundle-write time:**\n```\n' + (running if running else '(no matching process)') + '\n```\n')
    body.append('\n**`logs/x1x3_run.log` verbatim at bundle-write time:**\n```\n' + status + '\n```\n')
    body.append("""
### ⚠️ CAVEAT FOUND IN THE SMOKE — read before trusting p50

X3's selection rule is **mine**, not the original authors'. I made every optimizer return
top-TOP by surrogate LCB over every point it visited. The smoke shows this rule has a
**diversity collapse** for trajectory-based optimizers:

    Branin-2D  ens x grad     -> p100 -10.9609 | p50 -10.9609   <- IDENTICAL
    Branin-2D  ens x cma      -> p100 -10.9608 | p50 -10.9609   <- near-identical
    Branin-2D  ens x perturb  -> p100  -1.6296 | p50 -10.9609   <- not collapsed

Gradient ascent converges, so pooling its trajectory and taking the top-128 by LCB returns
128 near-duplicates of one point. Consequences:

- **p100 (the paper's headline metric) is UNAFFECTED** -- max over duplicates == max over one.
- **p50 is degenerate under this rule** for grad and cma. Do not read p50 from this run as a
  diversity measure; it is close to p100 by construction.
- **This is not new to X3.** The PRE-AUDIT cma already used exactly this rule (`mbo.py`
  cma_opt: "pools every queried point, returns top-TOP by surrogate score"), so cma's p50 in
  the PUBLISHED results is degenerate the same way -- which is a candidate explanation for
  Ens x CMA's poor p50 that has nothing to do with the optimizer being conservative.

**Open design question for the judgment layer.** The non-degenerate alternative is per-slot
best-LCB-ever (each of the 128 inits keeps its own best point), which preserves 128 distinct
designs and still fixes T12's "gradient discards the best point it ever saw". But CMA has a
population, not slots, so per-slot does not map onto it -- which is exactly why a single rule
across all three optimizers is harder than it looks. I chose pooled-top-k for consistency and
am flagging the cost rather than hiding it. **Read p100 from this run; treat p50 as suspect.**
""")
    body.append('\n### The pre-registration X1 is tested against (VERBATIM)\n')
    body.append('\nFrom `docs/PREREGISTRATION_V2.md`:\n\n```\n' + (prereg or '(row not found)') + '\n```\n')
    if os.path.exists('docs/MECHANISM_EXPERIMENTS.md'):
        txt = open('docs/MECHANISM_EXPERIMENTS.md').read()
        start = txt.find('## M0 (GATE)')
        end = txt.find('## M1 ·')
        if start != -1 and end != -1:
            body.append('\nFrom `docs/MECHANISM_EXPERIMENTS.md`, the M0 gate VERBATIM:\n\n```markdown\n'
                        + txt[start:end].rstrip() + '\n```\n')
    return '\n'.join(body)

def special_git1():
    msg = sh('git show cdd5ad8 --stat --format=full')
    return '```\n' + msg + '\n```\n'

def special_git2():
    return '```\n' + sh('git log --oneline --all | head -40') + '\n```\n'

blocks = []
manifest = []
notincluded = []

for tier, req, actual, note in SPEC:
    if actual == '__SPECIAL_X1__':
        b = f'## FILE: {req}\n<!-- live status; generated at bundle time -->\n\n' + special_x1() + '\n---\n'
        blocks.append((tier, req, b, 0, len(b)))
        manifest.append((tier, req, '-', len(b), 'SPECIAL'))
        continue
    if actual == '__SPECIAL_GIT1__':
        b = f'## FILE: {req}\n<!-- git show cdd5ad8 --stat --format=full -->\n\n' + special_git1() + '\n---\n'
        blocks.append((tier, req, b, 0, len(b)))
        manifest.append((tier, req, '-', len(b), 'SPECIAL'))
        continue
    if actual == '__SPECIAL_GIT2__':
        b = f'## FILE: {req}\n<!-- git log --oneline --all | head -40 -->\n\n' + special_git2() + '\n---\n'
        blocks.append((tier, req, b, 0, len(b)))
        manifest.append((tier, req, '-', len(b), 'SPECIAL'))
        continue
    if actual is None or not os.path.exists(actual):
        b = f'## FILE: {req} — DOES NOT EXIST\n<!-- {note} -->\n\n---\n'
        blocks.append((tier, req, b, 0, len(b)))
        manifest.append((tier, req, 'DOES NOT EXIST', 0, f'T{tier}'))
        notincluded.append((req, note or 'listed in the task but absent from disk'))
        continue
    raw = open(actual, 'r', encoding='utf-8', errors='replace').read()
    n = raw.count('\n') + (0 if raw.endswith('\n') or raw == '' else 1)
    nb = len(raw.encode('utf-8'))
    ext = os.path.splitext(actual)[1]
    lang = LANG.get(ext, 'text')
    if os.path.basename(actual) == 'Dockerfile': lang = 'dockerfile'
    fence = '```'
    while fence in raw:
        fence += '`'
    b = (f'## FILE: {actual}\n<!-- lines: {n} | bytes: {nb} | last commit: {lastcommit(actual)} -->\n'
         f'{fence}{lang}\n{raw}{"" if raw.endswith(chr(10)) else chr(10)}{fence}\n\n---\n')
    blocks.append((tier, actual, b, n, nb))
    flag = ' **>200KB — flagged**' if nb > 200_000 else ''
    manifest.append((tier, actual, str(n), nb, f'T{tier}{flag}'))

EXCLUDED = [
    ('paper/aaai27/references.bib, paper/latex_source/references.bib, legacy/**/references.bib', '.bib — excluded by the task'),
    ('paper/aaai27/aaai2027.sty, aaai2027.bst, paper/latex_source/*.sty, *.bst, legacy/**/*.sty', '.sty/.bst/.cls — excluded by the task'),
    ('paper/aaai27/*.aux, *.log, *.bbl, *.blg, paper/aaai27/AuthorKit27/*.log', 'LaTeX aux/log/out — excluded by the task'),
    ('paper/aaai27/supplement.tex', 'not listed in the task spec; only main.tex was requested'),
    ('results/*.json (results_camera.json, results_db.json, 05_findings.json, gpcov.json, official_baselines.json, results_gradtune.json, all *_matched/*.bak/*.preserved)', 'result artifacts (json) — excluded by the task. NOTE: results_gradtune.json is the P0-0 evidence; its numbers are reproduced verbatim in FLAW_LEDGER.md P0-0, which IS included.'),
    ('results/official_baselines_raw.tgz', 'binary archive'),
    ('paper/figures_v2/*.pdf|png, paper/figures/*, paper/aaai27/figures/*, paper/aaai27/*.pdf', 'figures — excluded by the task'),
    ('paper/tables_v2/*.tex', 'generated result artifacts (tables); generator code/tables.py IS included'),
    ('logs/x1x3_run.log', 'log — excluded by the task, but its verbatim contents appear in the Tier-1 X1/X3 status block'),
    ('legacy/**', 'superseded per README.md:16-18 ("Nothing in legacy/ is needed to reproduce the paper"); includes archives/*.zip binaries'),
    ('docs/free_win_5_1_results.json', 'result artifact (json)'),
    ('docs/REPO_MAP.md', 'agent working memory — excluded by the task'),
    ('docs/SESSION_STATE.md', 'agent working memory — excluded by the task (also: never created)'),
    ('docs/FAILURES.md', 'agent working memory — excluded by the task (also: never created)'),
    ('research/**, .hyperresearch/**', 'hyperresearch vault internals; the committed audit trail is docs/hyperresearch/*'),
    ('venv/**, __pycache__/**, .git/**', 'lockfiles/caches/git internals — excluded by the task'),
    ('README.md', 'not listed in the task spec. Flagged separately: it is STALE (describes the ICML workshop paper as current, says n=10 seeds) and README.md:54 ships it in the supplement.'),
    ('paper/SKELETON.md, paper/proofs.md', 'not listed in the task spec; both are quoted where load-bearing in FLAW_LEDGER.md and REPO_MAP.md'),
    ('notebooks', 'none exist in this repo'),
]

body = ''.join(b for _, _, b, _, _ in blocks)
total = len(body.encode('utf-8'))

hdr = []
hdr.append('# BUNDLE — consolidated source and documents\n')
hdr.append(f'\nGenerated mechanically by `scratchpad/make_bundle.py`. Every included file is VERBATIM: '
           f'no summarization, elision, or truncation. Repo `{REPO}` @ `{sh("git rev-parse --short HEAD")}`.\n')
hdr.append(f'\n**Total body bytes: {total:,}**\n')
hdr.append('\n## Manifest\n\n| # | Tier | Path | Lines | Bytes | Note |\n|---|---|---|---|---|---|\n')
for i, (tier, p, n, nb, t) in enumerate(manifest, 1):
    hdr.append(f'| {i} | {t} | `{p}` | {n} | {nb:,} | |\n')
hdr.append(f'\n**Files/blocks in manifest: {len(manifest)}** '
           f'(of which DOES NOT EXIST: {sum(1 for m in manifest if m[2] == "DOES NOT EXIST")})\n')
hdr.append('\n## NOT INCLUDED\n\n| Path/glob | Reason |\n|---|---|\n')
for p, r in EXCLUDED:
    hdr.append(f'| `{p}` | {r} |\n')
hdr.append('\n## Files listed in the task that DO NOT EXIST\n\n| Requested path | Reason |\n|---|---|\n')
for p, r in notincluded:
    hdr.append(f'| `{p}` | {r} |\n')
hdr.append('\n---\n\n')

out = ''.join(hdr) + body
open('docs/BUNDLE.md', 'w', encoding='utf-8').write(out)
nheaders = out.count('\n## FILE: ') + (1 if out.startswith('## FILE: ') else 0)
print(f'wrote docs/BUNDLE.md  bytes={len(out.encode("utf-8")):,}  "## FILE:" headers={nheaders}  manifest_rows={len(manifest)}')

# ---------------- split at tier boundaries, <=600KB target ----------------
LIMIT = 600_000
tier_bytes = {}
for tier, _, b, _, _ in blocks:
    tier_bytes[tier] = tier_bytes.get(tier, 0) + len(b.encode('utf-8'))
print('tier bytes:', {k: f'{v:,}' for k, v in sorted(tier_bytes.items())})

parts, cur, cur_bytes, cur_tiers = [], [], 0, []
for tier in sorted(tier_bytes):
    tb = tier_bytes[tier]
    if cur and cur_bytes + tb > LIMIT:
        parts.append((cur_tiers[:], ''.join(cur))); cur, cur_bytes, cur_tiers = [], 0, []
    for t, _, b, _, _ in blocks:
        if t == tier: cur.append(b)
    cur_bytes += tb; cur_tiers.append(tier)
if cur: parts.append((cur_tiers[:], ''.join(cur)))

split_map = []
for i, (tiers, _) in enumerate(parts, 1):
    split_map.append(f'| `docs/BUNDLE_PART{i}.md` | Tier {", ".join(map(str, tiers))} | '
                     f'{len(parts[i-1][1].encode("utf-8")):,} bytes |')

hdr2 = list(hdr)
hdr2.insert(3, '\n## Part-split map\n\n| Part | Tiers | Body bytes |\n|---|---|---|\n'
               + '\n'.join(split_map) + '\n\nSplit at tier boundaries only; no file is split across parts.\n')

written = []
for i, (tiers, bodytxt) in enumerate(parts, 1):
    path = f'docs/BUNDLE_PART{i}.md'
    head = (''.join(hdr2) if i == 1 else
            f'# BUNDLE — PART {i} of {len(parts)} (Tier {", ".join(map(str, tiers))})\n\n'
            f'Manifest, NOT-INCLUDED list, and part-split map are in `docs/BUNDLE_PART1.md`.\n'
            f'Verbatim contents; no summarization or truncation.\n\n---\n\n')
    txt = head + bodytxt
    open(path, 'w', encoding='utf-8').write(txt)
    nh = txt.count('\n## FILE: ') + (1 if txt.startswith('## FILE: ') else 0)
    written.append((path, len(txt.encode('utf-8')), nh))

import os as _os
if _os.path.exists('docs/BUNDLE.md'): _os.remove('docs/BUNDLE.md')
print()
tot_h = 0
for p, b, nh in written:
    print(f'{p}: {b:,} bytes | "## FILE:" headers={nh}')
    tot_h += nh
print(f'TOTAL headers across parts = {tot_h} | manifest rows = {len(manifest)} | MATCH = {tot_h == len(manifest)}')
