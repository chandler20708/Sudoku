from __future__ import annotations

import os
from dataclasses import dataclass, field
from time import perf_counter

from sudoku_heuristics.grid import (
    ALL_DIGITS,
    CELLS,
    PEERS,
    UNITS,
    Grid,
    as_grid,
    is_complete_solution,
)


@dataclass
class SolveStats:
    solver: str
    solved: bool
    elapsed_ms: float
    decisions: int = 0
    backtracks: int = 0
    assignments: int = 0
    eliminations: int = 0
    max_depth: int = 0
    status: str = "ok"
    solution: Grid | None = None
    notes: list[str] = field(default_factory=list)


def _timed_result(start: float, **kwargs: object) -> SolveStats:
    return SolveStats(elapsed_ms=(perf_counter() - start) * 1000, **kwargs)


def solve_recursive_backtracking(grid: Grid, max_decisions: int = 200_000) -> SolveStats:
    start = perf_counter()
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
        return _timed_result(
            start,
            solver="recursive_backtracking",
            solved=False,
            status="decision_budget_exceeded",
            decisions=stats["decisions"],
            backtracks=stats["backtracks"],
            max_depth=stats["max_depth"],
        )
    solution = as_grid(rows) if solved else None
    return _timed_result(
        start,
        solver="recursive_backtracking",
        solved=solved and solution is not None and is_complete_solution(solution),
        decisions=stats["decisions"],
        backtracks=stats["backtracks"],
        max_depth=stats["max_depth"],
        solution=solution,
    )


def _initial_candidates(grid: Grid) -> dict[tuple[int, int], set[int]] | None:
    candidates: dict[tuple[int, int], set[int]] = {}
    for r, c in CELLS:
        if grid[r][c]:
            candidates[(r, c)] = {grid[r][c]}
        else:
            used = {grid[pr][pc] for pr, pc in PEERS[(r, c)] if grid[pr][pc]}
            values = set(ALL_DIGITS - used)
            if not values:
                return None
            candidates[(r, c)] = values
    return candidates


def _assign(
    candidates: dict[tuple[int, int], set[int]],
    cell: tuple[int, int],
    value: int,
    stats: dict[str, int],
) -> bool:
    other_values = candidates[cell] - {value}
    for other in tuple(other_values):
        if not _eliminate(candidates, cell, other, stats):
            return False
    return True


def _eliminate(
    candidates: dict[tuple[int, int], set[int]],
    cell: tuple[int, int],
    value: int,
    stats: dict[str, int],
) -> bool:
    if value not in candidates[cell]:
        return True
    candidates[cell].remove(value)
    stats["eliminations"] += 1
    if len(candidates[cell]) == 0:
        return False
    if len(candidates[cell]) == 1:
        solved_value = next(iter(candidates[cell]))
        stats["assignments"] += 1
        for peer in PEERS[cell]:
            if not _eliminate(candidates, peer, solved_value, stats):
                return False
    for unit in UNITS:
        if cell not in unit:
            continue
        places = [u for u in unit if value in candidates[u]]
        if len(places) == 0:
            return False
        if len(places) == 1:
            stats["assignments"] += 1
            if not _assign(candidates, places[0], value, stats):
                return False
    return True


def _naked_pairs(candidates: dict[tuple[int, int], set[int]], stats: dict[str, int]) -> bool | None:
    changed = False
    for unit in UNITS:
        pairs: dict[tuple[int, int], list[tuple[int, int]]] = {}
        for cell in unit:
            values = candidates[cell]
            if len(values) == 2:
                pairs.setdefault(tuple(sorted(values)), []).append(cell)
        for pair, cells in pairs.items():
            if len(cells) != 2:
                continue
            for cell in unit:
                if cell in cells:
                    continue
                before = len(candidates[cell])
                candidates[cell].difference_update(pair)
                removed = before - len(candidates[cell])
                if removed:
                    stats["eliminations"] += removed
                    changed = True
                if not candidates[cell]:
                    return None
    return changed


def _propagate(candidates: dict[tuple[int, int], set[int]], stats: dict[str, int]) -> bool:
    changed = True
    while changed:
        before = sum(len(v) for v in candidates.values())
        for cell, values in list(candidates.items()):
            if len(values) == 1:
                value = next(iter(values))
                for peer in PEERS[cell]:
                    if not _eliminate(candidates, peer, value, stats):
                        return False
        naked_pair_result = _naked_pairs(candidates, stats)
        if naked_pair_result is None:
            return False
        after = sum(len(v) for v in candidates.values())
        changed = after < before
    return True


def _search(
    candidates: dict[tuple[int, int], set[int]],
    stats: dict[str, int],
    depth: int = 0,
) -> dict[tuple[int, int], set[int]] | None:
    stats["max_depth"] = max(stats["max_depth"], depth)
    if not _propagate(candidates, stats):
        stats["backtracks"] += 1
        return None
    unsolved = [(len(values), cell) for cell, values in candidates.items() if len(values) > 1]
    if not unsolved:
        return candidates
    _, cell = min(unsolved)
    for value in sorted(candidates[cell]):
        stats["decisions"] += 1
        branch = {k: set(v) for k, v in candidates.items()}
        if _assign(branch, cell, value, stats):
            result = _search(branch, stats, depth + 1)
            if result is not None:
                return result
        stats["backtracks"] += 1
    return None


def solve_proposed_heuristic(grid: Grid) -> SolveStats:
    start = perf_counter()
    candidates = _initial_candidates(grid)
    if candidates is None:
        return _timed_result(start, solver="proposed_heuristic", solved=False, status="invalid")

    for cell, values in list(candidates.items()):
        if len(values) == 1:
            value = next(iter(values))
            for peer in PEERS[cell]:
                if value in candidates[peer] and len(candidates[peer]) == 1:
                    return _timed_result(start, solver="proposed_heuristic", solved=False, status="invalid")

    stats = {"decisions": 0, "backtracks": 0, "assignments": 0, "eliminations": 0, "max_depth": 0}
    result = _search(candidates, stats)
    if result is None:
        return _timed_result(start, solver="proposed_heuristic", solved=False, status="no_solution", **stats)
    solution = tuple(tuple(next(iter(result[(r, c)])) for c in range(9)) for r in range(9))
    return _timed_result(
        start,
        solver="proposed_heuristic",
        solved=is_complete_solution(solution),
        solution=solution,
        **stats,
    )


def solve_gurobi(grid: Grid, mode: str = "default", time_limit: float = 5.0) -> SolveStats:
    start = perf_counter()
    os.environ.setdefault("LC_ALL", "C")
    os.environ.setdefault("LANG", "C")
    try:
        import gurobipy as gp
        from gurobipy import GRB
    except Exception as exc:  # pragma: no cover - depends on local install
        return _timed_result(start, solver=f"gurobi_{mode}", solved=False, status="unavailable", notes=[str(exc)])

    try:
        model = gp.Model("sudoku")
        model.Params.OutputFlag = 0
        model.Params.TimeLimit = time_limit
        if mode == "heuristics":
            model.Params.Heuristics = 1.0
            model.Params.MIPFocus = 1
            model.Params.NoRelHeurWork = 20
        rows = range(9)
        cols = range(9)
        digits = range(1, 10)
        x = model.addVars(rows, cols, digits, vtype=GRB.BINARY, name="x")

        for r in rows:
            for c in cols:
                model.addConstr(gp.quicksum(x[r, c, d] for d in digits) == 1)
        for r in rows:
            for d in digits:
                model.addConstr(gp.quicksum(x[r, c, d] for c in cols) == 1)
        for c in cols:
            for d in digits:
                model.addConstr(gp.quicksum(x[r, c, d] for r in rows) == 1)
        for br in range(0, 9, 3):
            for bc in range(0, 9, 3):
                for d in digits:
                    model.addConstr(
                        gp.quicksum(x[r, c, d] for r in range(br, br + 3) for c in range(bc, bc + 3))
                        == 1
                    )
        for r in rows:
            for c in cols:
                if grid[r][c]:
                    model.addConstr(x[r, c, grid[r][c]] == 1)

        model.optimize()
        solved = model.Status == GRB.OPTIMAL or model.SolCount > 0
        solution = None
        if solved:
            solution = tuple(
                tuple(next(d for d in digits if x[r, c, d].X > 0.5) for c in cols) for r in rows
            )
            solved = is_complete_solution(solution)
        return _timed_result(
            start,
            solver=f"gurobi_{mode}",
            solved=solved,
            status=str(model.Status),
            decisions=int(getattr(model, "NodeCount", 0)),
            solution=solution,
            notes=[f"runtime={model.Runtime:.6f}s"],
        )
    except Exception as exc:  # pragma: no cover - license/environment dependent
        return _timed_result(start, solver=f"gurobi_{mode}", solved=False, status="error", notes=[str(exc)])


# Backwards-compatible alias for older local notebooks or scripts.
solve_basic_backtracking = solve_recursive_backtracking
