PYTHON := uv run python
ENV := PYTHONPATH=src LC_ALL=C LANG=C

.PHONY: benchmark benchmark-data edge-cases figures test lint check clean-cache

benchmark: benchmark-data edge-cases figures

benchmark-data:
	$(ENV) $(PYTHON) scripts/run_benchmark.py main

edge-cases:
	$(ENV) $(PYTHON) scripts/run_benchmark.py edge

figures: benchmark-data
	$(ENV) $(PYTHON) scripts/run_benchmark.py figures

test:
	uv run pytest

lint:
	uv run ruff check src tests scripts

check: lint test

clean-cache:
	rm -rf .pytest_cache .ruff_cache src/sudoku_heuristics/__pycache__ tests/__pycache__
