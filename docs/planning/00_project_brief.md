# 00 Project Brief

## Project Name

Heuristics for Solving Sudoku

## One-Sentence Purpose

Build and explain a Sudoku solver that demonstrates practical understanding of heuristics, then compare it against plain recursive backtracking and Gurobi baselines.

## Decision Context

The project demonstrates how domain heuristics reduce search effort in a constraint satisfaction problem. Sudoku is used because its rules are simple to explain while its search space is large enough to make heuristic design meaningful.

## Audience

| Audience | What they care about | Implication |
|---|---|---|
| Technical assessor | Correctness, comparison design, and reproducibility | Include source code, validation tests, benchmark data, and clear metrics. |
| Non-specialist reader | Plain explanation of why heuristics help | Explain candidate elimination, forced moves, and branching choices in accessible language. |
| Future maintainer | Simple project structure | Keep solver code, benchmark scripts, generated data, and final outputs in predictable folders. |

## Deliverables

| Deliverable | Status | Notes |
|---|---|---|
| Working puzzle generator | Complete | Generates unique puzzles from varied clue targets, then assigns final labels by measured difficulty score. |
| Heuristic solver | Complete | Uses propagation, naked/hidden singles, naked pairs, and MRV search. |
| Baseline solvers | Complete | Plain backtracking and Gurobi default/heuristic settings. |
| Benchmark outputs | Complete | `outputs/tables/benchmark_results.csv`, `outputs/tables/edge_case_results.csv`, and SVG figures. |
| Final Markdown report | Complete | `outputs/reports/final_sudoku_heuristics_report.md`, including edge cases and reproducibility notes. |

## Evidence Standard

Separate literature claims, implementation details, generated benchmark results, interpretation, and limitations.
