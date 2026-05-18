# Code Map

## Main Files

| File | Role |
|---|---|
| `src/sudoku_heuristics/grid.py` | Shared grid representation, validation, candidate calculation, Markdown display. |
| `src/sudoku_heuristics/generator.py` | Creates solved grids, removes clues, checks uniqueness, labels difficulty by clue target. |
| `src/sudoku_heuristics/solvers.py` | Plain backtracking, proposed heuristic solver, and Gurobi MIP wrappers. |
| `src/sudoku_heuristics/benchmark.py` | Runs all solvers on generated puzzles and writes CSV outputs. |
| `src/sudoku_heuristics/visuals.py` | Creates SVG charts and Sudoku example grids without relying on Matplotlib. |
| `scripts/run_benchmark.py` | End-to-end benchmark command. |
| `outputs/reports/final_sudoku_heuristics_report.md` | Main single Markdown report. |

## Reproduce The Outputs

```bash
PYTHONPATH=src LC_ALL=C LANG=C ./.venv/bin/python scripts/run_benchmark.py
```

Then run:

```bash
uv run pytest
uv run ruff check src tests
```

## Why Gurobi Has A Wrapper

The project may run on machines with no Gurobi license. The wrapper returns an unavailable/error status instead of breaking the whole benchmark when possible. On this machine, `gurobipy==13.0.2` is installed and the benchmark successfully produced Gurobi results.

