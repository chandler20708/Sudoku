# Sudoku Heuristics Research Project

This repo demonstrates how heuristic reasoning can solve Sudoku and how that compares with a plain programming baseline and Gurobi MIP baselines.

The project is intentionally small and readable. Its purpose is to show understanding of heuristics, constraint propagation, baseline comparison, metrics, and limitations.

## Main Outputs

| Output | Location |
|---|---|
| Final report | `outputs/reports/final_sudoku_heuristics_report.md` |
| Solver and generator code | `src/sudoku_heuristics/` |
| Benchmark dataset | `data/processed/generated_puzzles.csv` |
| Benchmark results | `outputs/tables/benchmark_results.csv` |
| Report figures | `outputs/figures/` |
| Edge-case results | `outputs/tables/edge_case_results.csv` |

## Project Structure

```text
.
├── data/processed/              # Generated Sudoku benchmark puzzles
├── docs/
│   ├── planning/                # Project brief, methodology, assumptions
│   └── research_notes/          # Literature notes
├── outputs/
│   ├── figures/                 # SVG charts and puzzle examples
│   ├── reports/                 # Final single Markdown report
│   └── tables/                  # Benchmark CSV
├── scripts/
│   └── run_benchmark.py         # Rebuild benchmark outputs; called by Makefile
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

- plain recursive backtracking;
- Gurobi default MIP;
- Gurobi with heuristic-focused MIP settings.

## Reproduce The Project

Install/sync dependencies:

```bash
uv sync
```

Run the benchmark:

```bash
make benchmark -j2
```

The `-j2` flag lets Make run the generated-puzzle benchmark and edge-case benchmark in parallel, then generate figures after the main benchmark data is ready.

Run validation:

```bash
make check
```

## Current Benchmark Summary

The benchmark currently uses 40 generated unique puzzles: 10 easy, 10 medium, 10 hard, and 10 expert. Difficulty labels are assigned by a measured difficulty score, not just by clue count.

| Solver | Solved |
|---|---:|
| Proposed heuristic | 40 / 40 |
| Gurobi default | 40 / 40 |
| Gurobi heuristic settings | 40 / 40 |
| Plain recursive backtracking | 36 / 40 |

The key interpretation is that the custom heuristic uses Sudoku structure to reduce search effort. Gurobi is reliable, but for a single 9 by 9 Sudoku puzzle, model-building overhead is visible. Plain backtracking is simple but weak on harder puzzles.

## Limitations

This is a compact empirical project, not a large-scale algorithm paper. The puzzle set is small and generated locally. Difficulty is approximated by a project-specific score using clue count, candidate ambiguity, and observed heuristic search effort, not by an external Sudoku rating engine.

The next useful extension would be to test against a larger public puzzle corpus and add more advanced human-style techniques such as pointing pairs, box-line reduction, X-wing, and chains.
