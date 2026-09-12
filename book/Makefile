# Build the book: vector figures from diagrams/, the example programs from lectures/ and labs/,
# then two LuaLaTeX passes for the contents and the references.
#
#   make                   build digitalteknik.pdf, dated today
#   make VERSION=v1.0.0    the same, with the edition's version on the title page
#   make part PART=04      the front matter and chapter 4 alone, with its solutions, into
#                          build/part-04/ (PART=lab1, lab2, lab3, studio, avr, exam or answers
#                          for a piece of the back matter)
#   make figures           render the figures only, into build/figures
#   make clean             remove everything the build writes
#
# The example programs printed in full are typeset straight from their files under lectures/ and
# labs/, and the figures straight from diagrams/, so a change to either is a change to the book on
# the next build.

ROOT    := $(abspath $(dir $(lastword $(MAKEFILE_LIST)))/..)
BOOK    := $(ROOT)/book
BUILD   := $(BOOK)/build
PYTHON  ?= $(ROOT)/.venv/bin/python
VERSION ?=
LATEX   := lualatex -interaction=nonstopmode -halt-on-error -file-line-error
# The book, with its version defined before anything is read; -jobname keeps the output book.pdf.
BOOKTEX := $(LATEX) -output-directory=$(BUILD) -jobname=book \
           '\def\bookversion{$(VERSION)}\input{book.tex}'

SOURCES := book.tex dtbook.sty dtbook.lua \
           $(wildcard front/*.tex chapters/*/*.tex back/*.tex back/*/*.tex)
# The screenshots are included as the PNGs they are.
IMAGES  := $(wildcard $(ROOT)/info/images/*.png)
# Every program the book can print in full, copied into build/code/ without the test block at its
# end, which ci/simtest.py reads and a reader does not need.
PROGRAMS := $(patsubst $(ROOT)/%,%,$(wildcard $(ROOT)/lectures/*/examples/*.asm \
              $(ROOT)/labs/lab3/code/*.asm))
CODE    := $(PROGRAMS:%=$(BUILD)/code/%)
# Every figure diagrams/build.py knows, in one run: a hundred PDFs take ten seconds, and the
# builders import each other, so any change to diagrams/ redraws the lot.
FIGSTAMP := $(BUILD)/figures/.stamp

.PHONY: all figures part clean FORCE

all: digitalteknik.pdf

figures: $(FIGSTAMP)

$(FIGSTAMP): figures.py $(wildcard $(ROOT)/diagrams/*.py)
	@test -x $(PYTHON) || { \
	  echo "No Python environment at $(PYTHON). Create it once with:"; \
	  echo "  python3 -m venv .venv"; \
	  echo "  .venv/bin/pip install -r diagrams/requirements.txt"; \
	  exit 1; }
	$(PYTHON) figures.py $(BUILD)/figures
	@touch $@

# A program as the book prints it: everything above the line that opens its test block, less the
# blank lines left at the end.
$(BUILD)/code/%.asm: $(ROOT)/%.asm
	@mkdir -p $(dir $@)
	@sed '/^; ---- Test/,$$d' $< | sed -e :a -e '/^\n*$$/{$$d;N;ba' -e '}' > $@

# The version the last build was made for. The file is rewritten only when VERSION changes, so a
# new version, or none after one, rebuilds the title page and nothing else does.
$(BUILD)/version: FORCE
	@mkdir -p $(BUILD)
	@echo '$(VERSION)' | cmp -s - $@ || echo '$(VERSION)' > $@

digitalteknik.pdf: $(SOURCES) $(IMAGES) $(CODE) $(FIGSTAMP) $(BUILD)/version
	@mkdir -p $(BUILD)
	cd $(BOOK) && $(BOOKTEX) >/dev/null || (tail -40 $(BUILD)/book.log; exit 1)
	cd $(BOOK) && $(BOOKTEX) >/dev/null || (tail -40 $(BUILD)/book.log; exit 1)
	@grep -E "^(Overfull|Underfull)|Warning" $(BUILD)/book.log | sort | uniq -c | sort -rn | head -20 || true
	@! grep -q "There were undefined references" $(BUILD)/book.log || \
	    (echo "error: undefined references; see $(BUILD)/book.log"; exit 1)
	cp $(BUILD)/book.pdf $@

# One piece of the book, alone. References into the pieces left out are undefined, so they are
# listed rather than treated as an error; the whole book is the check that none is left.
part: $(IMAGES) $(CODE) $(FIGSTAMP)
	@test -n "$(PART)" || { echo "usage: make part PART=04"; exit 1; }
	@mkdir -p $(BUILD)/part-$(PART)
	cd $(BOOK) && for pass in 1 2; do \
	  $(LATEX) -output-directory=$(BUILD)/part-$(PART) -jobname=book \
	    '\def\bookversion{}\def\onlypart{$(PART)}\input{book.tex}' >/dev/null \
	    || { tail -40 $(BUILD)/part-$(PART)/book.log; exit 1; }; done
	@grep -E "^(Overfull|Underfull)" $(BUILD)/part-$(PART)/book.log | sort | uniq -c | sort -rn || true
	@grep -E "LaTeX Warning: (Reference|Hyper reference)" $(BUILD)/part-$(PART)/book.log \
	  | sed -E "s/.*[\`']([^']*)'.*/undefined: \1/" | sort -u || true
	@echo "wrote $(BUILD)/part-$(PART)/book.pdf"

clean:
	rm -rf $(BUILD) digitalteknik.pdf
