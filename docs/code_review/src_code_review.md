# Source Code Review Summary

## Scope

Review of the Sudoku generator, solver implementations, benchmark runner, edge cases, and documentation after the V2 heuristic update.

## Current Solver Set

- `recursive_backtracking`
- `heuristic_v1_constraint_mrv`
- `heuristic_v2_adaptive_locked_sets`
- `gurobi_default`
- `gurobi_heuristics`

## Findings Resolved

| Finding | Resolution |
|---|---|
| Invalid starting grids should not burn search budget. | All solvers now call `validate_partial` before search or model construction. |
| Candidate propagation repeatedly scanned every unit. | `UNITS_BY_CELL` was added so elimination checks only the units containing the affected cell. |
| The main heuristic needed clearer naming. | V1 and V2 are now named separately in code, CSV output, charts, and the final report. |
| Difficulty scoring solved the same puzzle more than necessary. | `difficulty_score` can reuse an existing `SolveStats` object during generation. |
| Edge cases needed uniqueness-aware reporting. | `classify_puzzle` reports `invalid`, `no_solution`, `unique`, and `multiple_solutions`; edge CSV includes the classification. |
| Gurobi status values were hard to read. | Status codes are mapped to readable names and solved rows use `ok`. |

## Benchmark Snapshot After Refactor

| Solver | Generated puzzles solved | Key observation |
|---|---:|---|
| `heuristic_v2_adaptive_locked_sets` | 40 / 40 | Final proposed solver; lower expert search effort than V1 but slower due advanced probing. |
| `heuristic_v1_constraint_mrv` | 40 / 40 | Fastest custom solver on the generated benchmark. |
| `recursive_backtracking` | 36 / 40 | Fails some hard/expert cases under the decision budget. |
| `gurobi_default` | 40 / 40 | Reliable, with modelling overhead visible at this small scale. |
| `gurobi_heuristics` | 40 / 40 | Reliable; heuristic settings did not materially change this tiny MIP formulation. |

## Remaining Risks

- The generated benchmark is small; a larger public corpus would improve evidence quality.
- The difficulty score is a practical project proxy, not an official Sudoku rating engine.
- V2 reduces search effort on the generated expert set, but it is not faster than V1 in wall-clock time.
- More advanced rules such as X-wing and chains are intentionally out of scope for readability.

## Follow-Up

Detailed V2 follow-up notes are in `docs/code_review/2026-05-18_v2_followup.md`.
