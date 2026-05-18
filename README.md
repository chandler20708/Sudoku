# Sudoku Heuristics Research Project

This repo demonstrates how heuristic reasoning can solve Sudoku and how that compares with a plain programming baseline and Gurobi MIP baselines.

The project is intentionally small and readable. Its purpose is to show understanding of heuristics, constraint propagation, baseline comparison, metrics, and limitations.

## Main Outputs

| Output | Location |
|---|---|
| Final report | `outputs/reports/final_sudoku_heuristics_report.md` |
| Fast learning notes | `learning/` |
| Solver and generator code | `src/sudoku_heuristics/` |
| Benchmark dataset | `data/processed/generated_puzzles.csv` |
| Benchmark results | `outputs/tables/benchmark_results.csv` |
| Report figures | `outputs/figures/` |
| Archived template setup | `scripts/template_archive/` |

## Project Structure

```text
.
├── data/processed/              # Generated Sudoku benchmark puzzles
├── docs/
│   ├── planning/                # Project brief, methodology, assumptions
│   └── research_notes/          # Literature notes and working progression
├── learning/                    # Plain-English notes for quick understanding
├── outputs/
│   ├── figures/                 # SVG charts and puzzle examples
│   ├── reports/                 # Final single Markdown report
│   └── tables/                  # Benchmark CSV
├── scripts/
│   ├── run_benchmark.py         # Rebuild benchmark outputs
│   └── template_archive/        # Original project-template setup files
├── src/sudoku_heuristics/       # Generator, solvers, benchmark, visuals
└── tests/                       # Automated checks
```

## What The Solver Does

The proposed heuristic solver uses:

- candidate elimination;
- naked singles;
- hidden singles;
- naked pairs;
- minimum remaining values branching;
- depth-first fallback search.

The benchmark compares it with:

- plain LeetCode-style recursive backtracking;
- Gurobi default MIP;
- Gurobi with heuristic-focused MIP settings.

## Reproduce The Project

Install/sync dependencies:

```bash
uv sync
```

Run the benchmark:

```bash
PYTHONPATH=src LC_ALL=C LANG=C uv run python scripts/run_benchmark.py
```

Run validation:

```bash
uv run pytest
uv run ruff check src tests
```

## Current Benchmark Summary

The benchmark currently uses 20 generated unique puzzles: 5 easy, 5 medium, 5 hard, and 5 expert.

| Solver | Solved |
|---|---:|
| Proposed heuristic | 20 / 20 |
| Gurobi default | 20 / 20 |
| Gurobi heuristic settings | 20 / 20 |
| Plain backtracking | 17 / 20 |

The key interpretation is that the custom heuristic uses Sudoku structure to reduce search effort. Gurobi is reliable, but for a single 9 by 9 Sudoku puzzle, model-building overhead is visible. Plain backtracking is simple but weak on harder puzzles.

## Limitations

This is a learning project, not a large-scale algorithm paper. The puzzle set is small and generated locally. Difficulty is approximated by clue count and observed effort, not by an external Sudoku rating engine.

The next useful extension would be to test against a larger public puzzle corpus and add more advanced human-style techniques such as pointing pairs, box-line reduction, X-wing, and chains.
