# Shared fetcher recipe — offline-mbo-novelty-audit-6d8cd4

Read this before doing your batch. It encodes the hard-won tooling facts for this environment.

## Tooling reality (verified by the orchestrator)
- The `hyperresearch fetch` CLI **fails on arXiv PDFs** ("Binary PDF garbage") and returns only the
  ~800-word abstract for `/abs/` URLs. DO NOT rely on it for paper bodies.
- **Local PDF extraction WORKS**: `pdftotext` (/opt/homebrew/bin) and PyMuPDF are installed.
- The arXiv Atom API and Semantic Scholar REST API are flaky/rate-limited here. Prefer OpenAlex
  (`https://api.openalex.org/works?search=...&mailto=palaashgang@gmail.com`) and direct arXiv PDF download.

## Recipe A — pull an arXiv paper to grep-able full text
```
UA="Mozilla/5.0 (novelty-audit; mailto:palaashgang@gmail.com)"
curl -sSL --max-time 60 -H "User-Agent: $UA" -o research/raw/pdf/<ID>.pdf "https://arxiv.org/pdf/<ID>"
pdftotext research/raw/pdf/<ID>.pdf research/raw/txt/<slug>.txt
head -60 research/raw/txt/<slug>.txt   # VERIFY the title matches the intended paper — if not, STOP and report
grep -in "<claim keyword>" research/raw/txt/<slug>.txt   # find the overlapping sentences
```
If the paper is not on arXiv (journal/proceedings), fetch the landing page or publisher HTML via
`hyperresearch fetch "<url>" --tag offline-mbo-novelty-audit-6d8cd4 -j`; if only an abstract is
obtainable, say so explicitly in the note (verdict evidence from an abstract is weaker than body text).

## Recipe B — register a paper as a vault note
Write the note body to a temp markdown file, then:
```
/opt/homebrew/Caskroom/miniforge/base/bin/hyperresearch note new "<TITLE> (<Venue> <Year>, arXiv:<ID>)" \
  --body-file <path.md> --tag offline-mbo-novelty-audit-6d8cd4 --type note \
  --content-type paper --source "https://arxiv.org/abs/<ID>" \
  --summary "<one specific sentence: what this paper owns re the assigned claim>" -j
```

## Note body MUST contain (this is the whole point of the audit)
1. **Full citation**: authors, exact title, venue + year + arXiv ID. Respect the citation-date TRAPS:
   - Li/Rudner/Wilson = **ICLR 2024** (S2 back-props 2023 from arXiv v1)
   - Henderson = **AAAI 2018** (S2 says 2017); Benavoli = **JMLR 2016** (arXiv 2015)
2. **What the paper actually does** (4-8 sentences from the BODY, not the abstract alone).
3. **## Claim relevance** — for each assigned claim NX: does this paper OWN it, PARTIALLY overlap, or
   NOT touch it? Quote the **verbatim** most-overlapping sentence(s) with a section pointer. If it does
   NOT own the claim, say what it stops short of. This verbatim sentence is what the final verdict cites.
4. **Grep evidence**: note which keywords you grepped and the hit counts, so the verdict is auditable.

## Anti-fabrication rules (four fabricated citations already caught on this project)
- Never write a citation you did not download and title-verify. If a title doesn't match, report the miss.
- Never quote a sentence you did not copy from the extracted text. Quotes must be verbatim.
- "NONE FOUND" is a valid, valuable result — list the exact queries you ran.
