# Sudoku Heuristics Research Project

This repo demonstrates how heuristic reasoning can solve Sudoku and how that compares with a plain programming baseline and Gurobi MIP baselines.

The project is intentionally small and readable. Its purpose is to show understanding of heuristics, constraint propagation, baseline comparison, metrics, edge cases, and limitations.

## Main Outputs

| Output | Location |
|---|---|
| Final report | `outputs/reports/final_sudoku_heuristics_report.md` |
| Solver and generator code | `src/sudoku_heuristics/` |
| Benchmark dataset | `data/processed/generated_puzzles.csv` |
| Benchmark results | `outputs/tables/benchmark_results.csv` |
| Edge-case results | `outputs/tables/edge_case_results.csv` |
| Report figures | `outputs/figures/` |

## Project Structure

```text
.
├── data/processed/              # Generated Sudoku benchmark puzzles
├── docs/
│   ├── code_review/             # Source review notes and follow-up decisions
│   ├── planning/                # Project brief, methodology, assumptions
│   └── research_notes/          # Literature notes
├── outputs/
│   ├── figures/                 # SVG charts and puzzle examples
│   ├── reports/                 # Final single Markdown report
│   └── tables/                  # Benchmark CSVs
├── scripts/
│   └── run_benchmark.py         # Rebuild benchmark outputs; called by Makefile
├── src/sudoku_heuristics/       # Generator, solvers, benchmark, visuals
└── tests/                       # Automated checks
```

## Solver Names

| Solver id | Plain-English meaning |
|---|---|
| `recursive_backtracking` | Fill the first empty cell, try values, and backtrack when stuck. |
| `heuristic_v1_constraint_mrv` | Candidate propagation, naked/hidden singles, naked pairs, and minimum-remaining-values branching. |
| `heuristic_v2_adaptive_locked_sets` | Proposed V2. It probes whether locked candidates and naked triples reduce the candidate space enough, then uses the advanced path only when useful. |
| `heuristic_v1_legacy_reference` | Standalone copy of the original V1-style code kept in `src/sudoku_heuristics/heuristic_v1_legacy.py` for audit and learning reference; not part of the main benchmark. |
| `gurobi_default` | Binary MIP formulation solved by Gurobi default settings. |
| `gurobi_heuristics` | Same MIP formulation with heuristic-oriented Gurobi settings. |

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
| Proposed V2 adaptive heuristic | 40 / 40 |
| Heuristic V1 propagation + MRV | 40 / 40 |
| Plain recursive backtracking | 36 / 40 |
| Gurobi default MIP | 40 / 40 |
| Gurobi heuristic mode | 40 / 40 |

The key interpretation is that the custom heuristics use Sudoku structure to reduce search effort. V2 reduces median expert search effort compared with V1, although V1 remains faster on simple generated puzzles because it does less reasoning work before search. Gurobi is reliable, but for a single 9 by 9 Sudoku puzzle, model-building overhead is visible. Plain backtracking is simple but weak on harder puzzles.

## Limitations

This is a compact empirical project, not a large-scale algorithm paper. The puzzle set is small and generated locally. Difficulty is approximated by a project-specific score using clue count, candidate ambiguity, and observed heuristic search effort, not by an external Sudoku rating engine.

The next useful extension would be to test against a larger public puzzle corpus and add more human-style techniques such as X-wing, chains, and contradiction-based strategies.
