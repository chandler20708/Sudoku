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
├── src/sudoku_heuristics/       # Generator, benchmark, visuals, model package
│   └── models/                  # One Python file per solver model
└── tests/                       # Automated checks
```

## Solver Names

| Solver id | Plain-English meaning |
|---|---|
| `recursive_backtracking` | Fill the first empty cell, try values, and backtrack when stuck. |
| `heuristic_v1_constraint_mrv` | Candidate propagation, naked/hidden singles, naked pairs, and minimum-remaining-values branching. |
| `heuristic_v2_adaptive_locked_sets` | Proposed V2. It probes whether locked candidates and naked triples reduce the candidate space enough, then uses the advanced path only when useful. |
| `heuristic_v1_legacy_reference` | Standalone copy of the original V1-style code kept in `src/sudoku_heuristics/models/heuristic_v1_legacy.py` for audit and learning reference; not part of the main benchmark. |
| `gurobi_default` | Binary MIP formulation solved by Gurobi default settings. |
| `gurobi_heuristics` | Same MIP formulation with heuristic-oriented Gurobi settings. |

## Model File Layout

| File | Purpose |
|---|---|
| `src/sudoku_heuristics/models/recursive_backtracking.py` | Plain programming baseline. |
| `src/sudoku_heuristics/models/heuristic_v1.py` | Benchmarked V1 heuristic wrapper. |
| `src/sudoku_heuristics/models/heuristic_v2.py` | Proposed V2 adaptive heuristic. |
| `src/sudoku_heuristics/models/gurobi_mip.py` | Gurobi default and heuristic-mode MIP baseline. |
| `src/sudoku_heuristics/models/heuristic_v1_legacy.py` | Standalone old V1-style reference implementation. |
| `src/sudoku_heuristics/models/candidate_tools.py` | Shared candidate propagation/search helpers used by V1 and V2. |
| `src/sudoku_heuristics/models/common.py` | Shared `SolveStats` result object. |

`src/sudoku_heuristics/solvers.py` remains only as a compatibility re-export for older imports.

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

The key interpretation is that the custom heuristics use Sudoku structure to reduce search effort. V2 is now structured for extension through injected candidate-update strategies. V1 remains faster on this small dataset, while V2 demonstrates how new heuristic rules can be added without rewriting the propagation loop. Gurobi is reliable, but for a single 9 by 9 Sudoku puzzle, model-building overhead is visible. Plain backtracking is simple but weak on harder puzzles.

## Extending Heuristics

Candidate updates use a small strategy pattern in `src/sudoku_heuristics/models/candidate_tools.py`. The pictured rules are represented directly as strategy classes:

- `NakedSinglesStrategy`
- `HiddenSinglesStrategy`
- `NakedSubsetStrategy(2)` for naked pairs

V2 adds `LockedCandidatesStrategy` and `NakedSubsetStrategy(3)`. A future heuristic can be added by implementing `CandidateUpdateStrategy.apply(...)` and injecting it into `V1_STRATEGIES` or `V2_ADVANCED_STRATEGIES`.

## Limitations

This is a compact empirical project, not a large-scale algorithm paper. The puzzle set is small and generated locally. Difficulty is approximated by a project-specific score using clue count, candidate ambiguity, and observed heuristic search effort, not by an external Sudoku rating engine.

The next useful extension would be to test against a larger public puzzle corpus and add more human-style techniques such as X-wing, chains, and contradiction-based strategies.
