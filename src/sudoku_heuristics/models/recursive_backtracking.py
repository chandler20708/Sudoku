from __future__ import annotations

from time import perf_counter

from sudoku_heuristics.grid import Grid, as_grid, is_complete_solution, validate_partial
from sudoku_heuristics.models.common import SolveStats, timed_result


def solve_recursive_backtracking(grid: Grid, max_decisions: int = 200_000) -> SolveStats:
    start = perf_counter()
    validation = validate_partial(grid)
    if not validation.valid:
        return timed_result(
            start,
            solver="recursive_backtracking",
            solved=False,
            status="invalid",
            notes=[validation.message],
        )
    rows = [list(row) for row in grid]
    stats = {"decisions": 0, "backtracks": 0, "max_depth": 0}

    def allowed(r: int, c: int, value: int) -> bool:
        if any(rows[r][j] == value for j in range(9)):
            return False
        if any(rows[i][c] == value for i in range(9)):
            return False
        br, bc = 3 * (r // 3), 3 * (c // 3)
        return all(rows[i][j] != value for i in range(br, br + 3) for j in range(bc, bc + 3))

    def dfs(depth: int = 0) -> bool:
        stats["max_depth"] = max(stats["max_depth"], depth)
        for r in range(9):
            for c in range(9):
                if rows[r][c] == 0:
                    for value in range(1, 10):
                        stats["decisions"] += 1
                        if stats["decisions"] > max_decisions:
                            raise TimeoutError("Decision budget exceeded.")
                        if allowed(r, c, value):
                            rows[r][c] = value
                            if dfs(depth + 1):
                                return True
                            rows[r][c] = 0
                            stats["backtracks"] += 1
                    return False
        return True

    try:
        solved = dfs()
    except TimeoutError:
        return timed_result(
            start,
            solver="recursive_backtracking",
            solved=False,
            status="decision_budget_exceeded",
            decisions=stats["decisions"],
            backtracks=stats["backtracks"],
            max_depth=stats["max_depth"],
        )
    solution = as_grid(rows) if solved else None
    return timed_result(
        start,
        solver="recursive_backtracking",
        solved=solved and solution is not None and is_complete_solution(solution),
        status="ok" if solved else "no_solution",
        decisions=stats["decisions"],
        backtracks=stats["backtracks"],
        max_depth=stats["max_depth"],
        solution=solution,
    )
