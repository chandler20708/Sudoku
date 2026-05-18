# Sudoku `src` Code Review

Date: 2026-05-18

Scope reviewed:

- `src/sudoku_heuristics/grid.py`
- `src/sudoku_heuristics/solvers.py`
- `src/sudoku_heuristics/generator.py`
- `src/sudoku_heuristics/benchmark.py`
- `src/sudoku_heuristics/edge_cases.py`
- `src/sudoku_heuristics/visuals.py`
- `scripts/run_benchmark.py`
- `tests/test_sudoku_core.py`

Verification run:

```text
uv run pytest -> 5 passed
uv run ruff check src tests scripts -> All checks passed
```

## Executive Summary

The project is in a healthy state for a small research codebase. The core representation is simple, immutable grids are a good choice, and the proposed heuristic solver has the best practical performance on the generated benchmark set.

The main improvement opportunities are:

1. Validate invalid starting grids consistently across all solvers.
2. Precompute cell-to-unit relationships to simplify and speed propagation.
3. Avoid repeated solver calls during puzzle generation and scoring.
4. Make solver status values more semantic, especially for Gurobi.
5. Add uniqueness checks to solver reporting so ambiguous puzzles are not accidentally treated as proper Sudoku puzzles.

## Solver Comparison

The current benchmark compares four approaches:

- `recursive_backtracking`
- `proposed_heuristic`
- `gurobi_default`
- `gurobi_heuristics`

The generated benchmark in `outputs/tables/benchmark_results.csv` contains 40 puzzles and 160 solver runs.

### Generated Puzzle Summary

| Solver | Solved Rate | Median ms | Mean ms | Median Decisions | Max Decisions | Median Backtracks |
|---|---:|---:|---:|---:|---:|---:|
| `proposed_heuristic` | 100% | 1.086 | 1.185 | 0 | 7 | 0 |
| `gurobi_heuristics` | 100% | 4.745 | 4.766 | 0 | 0 | 0 |
| `gurobi_default` | 100% | 4.766 | 5.686 | 0 | 0 | 0 |
| `recursive_backtracking` | 90% | 5.572 | 39.792 | 5,900 | 200,001 | 627.5 |

### Median Runtime by Difficulty

| Difficulty | Recursive Backtracking | Proposed Heuristic | Gurobi Default | Gurobi Heuristics |
|---|---:|---:|---:|---:|
| easy | 1.065 ms | 0.808 ms | 4.863 ms | 4.783 ms |
| medium | 2.785 ms | 1.009 ms | 4.711 ms | 4.527 ms |
| hard | 33.316 ms | 1.164 ms | 4.753 ms | 4.560 ms |
| expert | 99.413 ms | 1.574 ms | 4.966 ms | 4.852 ms |

### Median Decisions by Difficulty

| Difficulty | Recursive Backtracking | Proposed Heuristic | Gurobi Default | Gurobi Heuristics |
|---|---:|---:|---:|---:|
| easy | 1,160 | 0 | 0 | 0 |
| medium | 2,797 | 0 | 0 | 0 |
| hard | 33,896 | 0 | 0 | 0 |
| expert | 104,031 | 2 | 0 | 0 |

### Interpretation

`recursive_backtracking` is the clearest baseline, but its worst-case behavior is exponential. If `n` is the number of empty cells, the worst case is `O(9^n)` because each empty cell may branch over up to 9 values. The current implementation also scans from the top-left for the next empty cell, so it does not exploit the most constrained variable.

`proposed_heuristic` is still exponential in the worst case, but it dramatically reduces search in practice. It uses candidate propagation, hidden singles, naked pairs, and minimum-remaining-values branching. On the generated benchmark, it solved every puzzle and had a median of zero decisions across easy, medium, and hard puzzles. Expert puzzles still required only a median of two decisions.

`gurobi_default` and `gurobi_heuristics` formulate Sudoku as a binary integer program. The solve phase is often tiny, but the Python-side model construction dominates runtime for 9x9 Sudoku. This explains why Gurobi is stable around 4-5 ms on generated puzzles but slower than the custom heuristic solver. Gurobi is useful as an external correctness baseline, not necessarily as the fastest implementation for this fixed-size problem.

`gurobi_heuristics` is not consistently better than `gurobi_default` for Sudoku. On generated puzzles it is slightly faster by median, but on `ai_escargot` it was much slower in the current edge-case output. The extra Gurobi heuristic parameters are not guaranteed to help on a small, tightly constrained feasibility problem.

## Complexity Notes

For a fixed 9x9 Sudoku board, many operations are technically `O(1)` because the input size never grows. For analysis, it is more useful to define:

- `m = 81`, the number of cells.
- `n = number of empty cells`.
- `d = 9`, the number of possible digits.

Then:

- `validate_partial`: `O(m)`.
- `candidates_for`: `O(20)` for a standard 9x9 cell, or `O(m)` if generalized.
- `solve_recursive_backtracking`: worst case `O(d^n)`, which is `O(9^n)`.
- `count_solutions`: worst case `O(9^n)`, capped early by `limit`.
- `solve_proposed_heuristic`: worst case still exponential, but practical branching is reduced by propagation and MRV.
- Gurobi model build: roughly fixed-size for 9x9 Sudoku, but conceptually `O(m * d)` variables and `O(m * d)` constraints for the standard exact-cover formulation.

## Code Review Findings

### 1. Plain Backtracking Should Reject Invalid Grids Early

File: `src/sudoku_heuristics/solvers.py`

`solve_recursive_backtracking` does not call `validate_partial` before search. On the contradictory edge case, it burns through the decision budget:

```text
contradictory_duplicate, recursive_backtracking, solved=False, status=decision_budget_exceeded
```

That should be a fast invalid result, like `proposed_heuristic`.

Recommended change:

```python
validation = validate_partial(grid)
if not validation.valid:
    return _timed_result(
        start,
        solver="recursive_backtracking",
        solved=False,
        status="invalid",
        notes=[validation.message],
    )
```

### 2. Precompute Units by Cell

File: `src/sudoku_heuristics/grid.py`

`_eliminate` currently scans all 27 units and checks whether the active cell is in each unit. This is fine for 9x9, but it is less elegant and runs inside the solver's hottest propagation path.

Recommended addition:

```python
UNITS_BY_CELL = {
    cell: tuple(unit for unit in UNITS if cell in unit)
    for cell in CELLS
}
```

Then `_eliminate` can use:

```python
for unit in UNITS_BY_CELL[cell]:
    places = [u for u in unit if value in candidates[u]]
```

This turns a scan of all units into a direct loop over the row, column, and box for the cell.

### 3. Avoid Repeated Solver Calls During Generation

File: `src/sudoku_heuristics/generator.py`

`generate_puzzle` solves the final puzzle, may solve it again, and then `difficulty_score` solves it again. This is correct but wasteful, especially when generating datasets.

Recommended change:

```python
def difficulty_score(grid: Grid, solved: SolveStats | None = None) -> float:
    solved = solved or solve_proposed_heuristic(grid)
    ...
```

Then pass the already-computed `solved` stats from `generate_puzzle`.

### 4. Use Better Solver Status Labels for Gurobi

File: `src/sudoku_heuristics/solvers.py`

Gurobi currently returns raw numeric statuses such as `"2"` or `"3"`. These are meaningful to Gurobi users but not readable in project outputs.

Recommended change:

```python
status_map = {
    GRB.OPTIMAL: "optimal",
    GRB.INFEASIBLE: "infeasible",
    GRB.TIME_LIMIT: "time_limit",
}
status=status_map.get(model.Status, str(model.Status))
```

This makes benchmark CSVs and reports easier to read.

### 5. Ambiguous Puzzles Are Solved but Not Flagged as Ambiguous

Files:

- `src/sudoku_heuristics/solvers.py`
- `src/sudoku_heuristics/generator.py`
- `scripts/run_benchmark.py`

The empty grid has multiple solutions. All solving methods can return one valid completion, but that does not mean it is a valid Sudoku puzzle instance in the usual "unique solution" sense.

Recommended change:

- Keep solvers focused on finding one solution.
- Add a separate `classify_puzzle(grid)` helper that returns `invalid`, `no_solution`, `unique`, or `multiple_solutions`.
- Use that helper in edge-case reporting and puzzle generation.

This avoids mixing "can find a solution" with "is a proper uniquely solvable Sudoku".

### 6. Improve Baseline Backtracking Without Losing Its Baseline Role

File: `src/sudoku_heuristics/solvers.py`

The current recursive baseline picks the first empty cell. That intentionally demonstrates poor scaling, but it also means the baseline is weaker than a typical simple backtracker.

Options:

- Keep the current solver as `solve_naive_backtracking`.
- Add `solve_mrv_backtracking` as a stronger baseline that chooses the empty cell with the fewest legal values.
- Compare all three: naive backtracking, MRV backtracking, and proposed heuristic.

This would make the benchmark more informative because it separates "basic recursion" from "search with a standard variable-ordering heuristic".

## Proposed Implementation Plan

1. Add `UNITS_BY_CELL` to `grid.py`.
2. Refactor `_eliminate` to use `UNITS_BY_CELL`.
3. Add early `validate_partial` checks to `solve_recursive_backtracking` and `solve_gurobi`.
4. Convert Gurobi numeric statuses to readable labels.
5. Allow `difficulty_score` to reuse an existing `SolveStats`.
6. Add `classify_puzzle(grid, solution_limit=2)` for uniqueness-aware reporting.
7. Add tests for:
   - recursive backtracking rejects contradictory grids as `invalid`;
   - Gurobi status labels are readable when Gurobi is available;
   - `classify_puzzle(AMBIGUOUS_PUZZLE)` returns `multiple_solutions`;
   - `generate_puzzle` still creates unique puzzles.

## Suggested Longer-Term Cleanup

- Use `type Cell = tuple[int, int]` to make candidate dictionaries easier to read.
- Consider storing candidates as `frozenset[int]` or bit masks if performance becomes important.
- Keep `gurobi` optional if this project needs to run on machines without a license.
- Split benchmark output generation from solver implementation so research scripts do not need to import plotting dependencies.
- Add a small benchmark regression test with a fixed hard puzzle to detect accidental performance cliffs.

