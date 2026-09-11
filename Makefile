SHELL := /bin/bash

# Path to this Makefile's directory, so `make -f ../path/to/Makefile` finds the scripts.
ROOT := $(dir $(firstword $(MAKEFILE_LIST)))

PYTHON := $(ROOT).venv/bin/python

.DEFAULT_GOAL := help
.PHONY: help build test lint links check diagrams clean

help: ## Show this help.
	@echo "Targets:"
	@grep -hE '^[a-z-]+:.*##' $(MAKEFILE_LIST) \
	  | sed -e 's/:.*## / /' -e 's/^/  /' \
	  | awk '{ printf "  %-12s %s\n", $$1, substr($$0, index($$0, $$2)) }'
	@echo
	@echo "Check only some programs:"
	@echo "  make test FILTER=lab3"

build: ## Assemble every assembly program in the course with avra.
	python3 $(ROOT)ci/simtest.py --build $(FILTER)

test: $(ROOT)ci/simcheck/simcheck ## Assemble every program, and simulate those with @expect lines.
	python3 $(ROOT)ci/simtest.py $(FILTER)

$(ROOT)ci/simcheck/simcheck: $(ROOT)ci/simcheck/simcheck.c
	$(MAKE) -C $(ROOT)ci/simcheck

# The CI lint job runs this exact target, so a green "make lint" locally means a green lint in CI.
lint: links check ## Markdown links, and the course's own conventions.

links: ## Check that every relative link in the Markdown resolves.
	$(ROOT)ci/links.sh

check: ## Check the course conventions: README sections, appendix letters, figures, widths.
	python3 $(ROOT)ci/check.py

# Deliberately not part of build or lint: the generated PNGs are committed, and redrawing them
# needs a Python environment nothing else here requires. See diagrams/README.md.
diagrams: ## Redraw the generated figures. Optional: FIGURE=<name>
	@test -x $(PYTHON) || { \
	  echo "No Python environment at $(PYTHON). Create it once with:"; \
	  echo "  python3 -m venv .venv"; \
	  echo "  .venv/bin/pip install -r diagrams/requirements.txt"; \
	  exit 1; }
	$(PYTHON) $(ROOT)diagrams/build.py $(FIGURE)

clean: ## Remove the harness binary and Python caches.
	$(MAKE) -C $(ROOT)ci/simcheck clean
	find $(ROOT) -name __pycache__ -type d -prune -exec rm -rf {} +
