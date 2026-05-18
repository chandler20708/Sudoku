# 01 Methodology Plan

## Research / Analysis Question

Can a transparent heuristic solver solve generated Sudoku puzzles more efficiently than plain recursive backtracking, and how does an adaptive V2 heuristic compare with V1 and Gurobi MIP baselines?

## Descriptive Claims

Sudoku can be represented as a grid of row, column, and box constraints. Empty cells can be represented by candidate sets. Difficulty is approximated using a measured score based on clue count, candidate ambiguity, and observed V2 search effort.

## Predictive Claims

V1 should reduce search effort because it removes impossible candidates and branches on the most constrained cell. V2 should further reduce search effort on puzzles where locked candidates and naked triples materially shrink the candidate space.

## Causal Claims

Only modest causal claims are made: within this implementation, propagation and MRV reduce the number of branches compared with first-empty-cell backtracking. V2's adaptive advanced rules reduce median expert decisions and backtracks on the generated benchmark, but they add runtime overhead.

## Normative / Optimisation Claims

The selected heuristic is preferred for this project because it is transparent, reproducible, and aligned with the educational objective of demonstrating heuristic reasoning.

## Data Sources

| Source | File / location | Observed variables | Limitations |
|---|---|---|---|
| Generated puzzle set | `data/processed/generated_puzzles.csv` | puzzle, solution, clue count, difficulty score, difficulty label | Generated data may not represent public puzzle corpora. |
| Benchmark results | `outputs/tables/benchmark_results.csv` | solver, solved status, time, decisions, backtracks, propagation metrics | Small generated sample of 40 puzzles. |
| Edge-case results | `outputs/tables/edge_case_results.csv` | invalid, ambiguous, very hard, and sparse stress-test outcomes | Edge cases are illustrative rather than exhaustive. |
| Literature notes | `docs/research_notes/2026-05-18_literature_and_source_notes.md` and `docs/research_notes/2026-05-18_v2_heuristic_literature_notes.md` | source summary and method rationale | Small-scale review, not systematic review. |

## Validation Plan

Validation uses unit tests for uniqueness and solver correctness, plus benchmark reproduction. Solver outputs are checked as complete valid Sudoku grids. Baseline comparison uses completion, runtime, search effort, and complexity proxies.
