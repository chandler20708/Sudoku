# 00 Project Brief

## Project Name

Heuristics for Solving Sudoku

## One-Sentence Purpose

Build and explain a Sudoku solver that demonstrates practical understanding of heuristics, then compare it against plain backtracking and Gurobi baselines.

## Decision Context

The project supports a learning/research demonstration for an optimisation professor: it shows how domain heuristics reduce search effort in a constraint problem.

## Stakeholders

| Stakeholder | What they care about | Implication |
|---|---|---|
| Chandler | Fast understanding and a defensible explanation | Keep a separate `learning/` folder and write plainly. |
| Professor / assessor | Evidence of heuristic reasoning | Include architecture, metrics, limitations, and baseline comparison. |
| Future Codex/ChatGPT work | Reproducibility | Keep code, data, outputs, and report in predictable folders. |

## Deliverables

| Deliverable | Owner | Status | Notes |
|---|---|---|---|
| Working puzzle generator | Codex | Complete | Generates unique puzzles by difficulty target. |
| Heuristic solver | Codex | Complete | Uses propagation, naked/hidden singles, naked pairs, MRV search. |
| Baseline solvers | Codex | Complete | Plain backtracking and Gurobi default/heuristic settings. |
| Benchmark outputs | Codex | Complete | `outputs/tables/benchmark_results.csv` and SVG figures. |
| Single Markdown report | Codex | Complete | `outputs/reports/final_sudoku_heuristics_report.md`. |
| Learning folder | Codex | Complete | `learning/` files explain the method quickly. |

## Evidence Standard

Separate literature claims, implementation details, generated benchmark results, interpretation, and limitations.
