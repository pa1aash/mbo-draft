# Reproducible builds for the AAAI-27 manuscript.
#
# Without this, pdflatex stamps /CreationDate, /ModDate and a derived /ID into
# every PDF, so recompiling an unchanged .tex produces a byte-different main.pdf
# (66 bytes, identical text) and git reports it modified. Since main.pdf and
# supplement.pdf are tracked, that churn made `git status` unreliable as a
# signal that the manuscript actually changed.
#
# Pinning SOURCE_DATE_EPOCH makes the build deterministic: same source in,
# byte-identical PDF out. Bump the date only when you want the PDF's internal
# timestamp to advance (e.g. at submission); a bump rewrites both PDFs once.
#
# 1784505600 = 2026-07-20 00:00 UTC
$ENV{'SOURCE_DATE_EPOCH'} = 1784505600;
$ENV{'FORCE_SOURCE_DATE'} = 1;
