# ── Mini Game Hub — Makefile ────────────────────────────────────

PYTHON   = python3
PIP      = pip3
MAIN     = main.sh
REPORT   = report
LATEX    = pdflatex

.PHONY: install run clean report

## install  — install Python dependencies
install:
	$(PIP) install -r requirements.txt

## run      — launch the game hub (Bash auth → Pygame window)
run:
	bash $(MAIN)

## report   — compile the LaTeX report to PDF (run twice for TOC)
report:
	$(LATEX) -interaction=nonstopmode $(REPORT).tex
	$(LATEX) -interaction=nonstopmode $(REPORT).tex

## clean    — remove Python bytecode and LaTeX build artefacts
clean:
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	rm -f $(REPORT).aux $(REPORT).log $(REPORT).out \
	      $(REPORT).toc $(REPORT).lof $(REPORT).lot

## help     — show this message
help:
	@grep -E '^##' Makefile | sed 's/## /  /'
