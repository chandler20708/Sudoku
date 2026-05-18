from __future__ import annotations

import os
from dataclasses import dataclass, field
from itertools import combinations
from time import perf_counter

from sudoku_heuristics.grid import (
    ALL_DIGITS,
    BOX_UNITS,
    CELLS,
    COL_UNITS,
    PEERS,
    ROW_UNITS,
    UNITS,
    UNITS_BY_CELL,
    Cell,
    Grid,
    as_grid,
    is_complete_solution,
    validate_partial,
)

Candidates = dict[Cell, set[int]]


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
    validation = validate_partial(grid)
    if not validation.valid:
        return _timed_result(
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
        status="ok" if solved else "no_solution",
        decisions=stats["decisions"],
        backtracks=stats["backtracks"],
        max_depth=stats["max_depth"],
        solution=solution,
    )


def _initial_candidates(grid: Grid) -> Candidates | None:
    validation = validate_partial(grid)
    if not validation.valid:
        return None
    candidates: Candidates = {}
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


def _assign(candidates: Candidates, cell: Cell, value: int, stats: dict[str, int]) -> bool:
    other_values = candidates[cell] - {value}
    for other in tuple(other_values):
        if not _eliminate(candidates, cell, other, stats):
            return False
    return True


def _eliminate(candidates: Candidates, cell: Cell, value: int, stats: dict[str, int]) -> bool:
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
    for unit in UNITS_BY_CELL[cell]:
        places = [u for u in unit if value in candidates[u]]
        if len(places) == 0:
            return False
        if len(places) == 1:
            stats["assignments"] += 1
            if not _assign(candidates, places[0], value, stats):
                return False
    return True


def _naked_subsets(candidates: Candidates, stats: dict[str, int], subset_size: int) -> bool | None:
    changed = False
    for unit in UNITS:
        subset_cells = [cell for cell in unit if 2 <= len(candidates[cell]) <= subset_size]
        for cells in combinations(subset_cells, subset_size):
            values = set().union(*(candidates[cell] for cell in cells))
            if len(values) != subset_size:
                continue
            for cell in unit:
                if cell in cells:
                    continue
                for value in tuple(values & candidates[cell]):
                    if not _eliminate(candidates, cell, value, stats):
                        return None
                    changed = True
    return changed


def _box_index(cell: Cell) -> int:
    return (cell[0] // 3) * 3 + cell[1] // 3


def _locked_candidates(candidates: Candidates, stats: dict[str, int]) -> bool | None:
    removals: set[tuple[Cell, int]] = set()
    for box in BOX_UNITS:
        box_set = set(box)
        for value in ALL_DIGITS:
            places = [cell for cell in box if value in candidates[cell]]
            if len(places) <= 1:
                continue
            rows = {r for r, _ in places}
            cols = {c for _, c in places}
            if len(rows) == 1:
                row = next(iter(rows))
                removals.update((cell, value) for cell in ROW_UNITS[row] if cell not in box_set)
            if len(cols) == 1:
                col = next(iter(cols))
                removals.update((cell, value) for cell in COL_UNITS[col] if cell not in box_set)
    for line in ROW_UNITS + COL_UNITS:
        line_set = set(line)
        for value in ALL_DIGITS:
            places = [cell for cell in line if value in candidates[cell]]
            if len(places) <= 1:
                continue
            boxes = {_box_index(cell) for cell in places}
            if len(boxes) == 1:
                box = BOX_UNITS[next(iter(boxes))]
                removals.update((cell, value) for cell in box if cell not in line_set)
    changed = False
    for cell, value in removals:
        if value not in candidates[cell]:
            continue
        if not _eliminate(candidates, cell, value, stats):
            return None
        changed = True
    return changed


def _propagate(candidates: Candidates, stats: dict[str, int], advanced: bool) -> bool:
    changed = True
    while changed:
        before = sum(len(v) for v in candidates.values())
        for cell, values in list(candidates.items()):
            if len(values) == 1:
                value = next(iter(values))
                for peer in PEERS[cell]:
                    if not _eliminate(candidates, peer, value, stats):
                        return False
        for size in ((2, 3) if advanced else (2,)):
            subset_result = _naked_subsets(candidates, stats, size)
            if subset_result is None:
                return False
        if advanced:
            locked_result = _locked_candidates(candidates, stats)
            if locked_result is None:
                return False
        after = sum(len(v) for v in candidates.values())
        changed = after < before
    return True


def _select_branch_cell(candidates: Candidates, use_degree_tiebreak: bool) -> Cell:
    unsolved = [cell for cell, values in candidates.items() if len(values) > 1]
    if not use_degree_tiebreak:
        return min(unsolved, key=lambda cell: (len(candidates[cell]), cell))
    return min(
        unsolved,
        key=lambda cell: (
            len(candidates[cell]),
            -sum(1 for peer in PEERS[cell] if len(candidates[peer]) > 1),
            cell,
        ),
    )


def _ordered_values(candidates: Candidates, cell: Cell, use_lcv: bool) -> list[int]:
    values = sorted(candidates[cell])
    if not use_lcv:
        return values
    return sorted(values, key=lambda value: sum(value in candidates[peer] for peer in PEERS[cell]))


def _search(
    candidates: Candidates,
    stats: dict[str, int],
    *,
    advanced: bool,
    use_degree_tiebreak: bool,
    use_lcv: bool,
    depth: int = 0,
) -> Candidates | None:
    stats["max_depth"] = max(stats["max_depth"], depth)
    if not _propagate(candidates, stats, advanced=advanced):
        stats["backtracks"] += 1
        return None
    if all(len(values) == 1 for values in candidates.values()):
        return candidates
    cell = _select_branch_cell(candidates, use_degree_tiebreak=use_degree_tiebreak)
    for value in _ordered_values(candidates, cell, use_lcv=use_lcv):
        stats["decisions"] += 1
        branch = {k: set(v) for k, v in candidates.items()}
        if _assign(branch, cell, value, stats):
            result = _search(
                branch,
                stats,
                advanced=advanced,
                use_degree_tiebreak=use_degree_tiebreak,
                use_lcv=use_lcv,
                depth=depth + 1,
            )
            if result is not None:
                return result
        stats["backtracks"] += 1
    return None


def _solve_candidate_heuristic(
    grid: Grid,
    *,
    solver: str,
    advanced: bool,
    use_degree_tiebreak: bool,
    use_lcv: bool,
) -> SolveStats:
    start = perf_counter()
    validation = validate_partial(grid)
    if not validation.valid:
        return _timed_result(start, solver=solver, solved=False, status="invalid", notes=[validation.message])
    candidates = _initial_candidates(grid)
    if candidates is None:
        return _timed_result(start, solver=solver, solved=False, status="invalid")
    stats = {"decisions": 0, "backtracks": 0, "assignments": 0, "eliminations": 0, "max_depth": 0}
    result = _search(
        candidates,
        stats,
        advanced=advanced,
        use_degree_tiebreak=use_degree_tiebreak,
        use_lcv=use_lcv,
    )
    if result is None:
        return _timed_result(start, solver=solver, solved=False, status="no_solution", **stats)
    solution = tuple(tuple(next(iter(result[(r, c)])) for c in range(9)) for r in range(9))
    return _timed_result(
        start,
        solver=solver,
        solved=is_complete_solution(solution),
        solution=solution,
        **stats,
    )


def solve_heuristic_v1(grid: Grid) -> SolveStats:
    return _solve_candidate_heuristic(
        grid,
        solver="heuristic_v1_constraint_mrv",
        advanced=False,
        use_degree_tiebreak=False,
        use_lcv=False,
    )


def solve_heuristic_v2(grid: Grid) -> SolveStats:
    start = perf_counter()
    validation = validate_partial(grid)
    if not validation.valid:
        return _timed_result(
            start,
            solver="heuristic_v2_adaptive_locked_sets",
            solved=False,
            status="invalid",
            notes=[validation.message],
        )

    basic = _initial_candidates(grid)
    advanced = _initial_candidates(grid)
    if basic is None or advanced is None:
        return _timed_result(
            start,
            solver="heuristic_v2_adaptive_locked_sets",
            solved=False,
            status="invalid",
        )

    basic_stats = {"decisions": 0, "backtracks": 0, "assignments": 0, "eliminations": 0, "max_depth": 0}
    advanced_stats = {"decisions": 0, "backtracks": 0, "assignments": 0, "eliminations": 0, "max_depth": 0}
    if not _propagate(basic, basic_stats, advanced=False):
        return _timed_result(
            start,
            solver="heuristic_v2_adaptive_locked_sets",
            solved=False,
            status="no_solution",
            **basic_stats,
        )
    if not _propagate(advanced, advanced_stats, advanced=True):
        advanced = basic
        advanced_stats = basic_stats.copy()

    basic_size = sum(len(values) for values in basic.values())
    advanced_size = sum(len(values) for values in advanced.values())
    basic_unsolved = sum(1 for values in basic.values() if len(values) > 1)
    advanced_unsolved = sum(1 for values in advanced.values() if len(values) > 1)
    use_advanced = (basic_size - advanced_size >= 10) or (basic_unsolved - advanced_unsolved >= 2)
    candidates = advanced if use_advanced else basic
    stats = advanced_stats if use_advanced else basic_stats
    result = _search(
        candidates,
        stats,
        advanced=use_advanced,
        use_degree_tiebreak=use_advanced,
        use_lcv=False,
    )
    if result is None:
        return _timed_result(
            start,
            solver="heuristic_v2_adaptive_locked_sets",
            solved=False,
            status="no_solution",
            notes=[f"mode={'advanced' if use_advanced else 'core'}"],
            **stats,
        )
    solution = tuple(tuple(next(iter(result[(r, c)])) for c in range(9)) for r in range(9))
    return _timed_result(
        start,
        solver="heuristic_v2_adaptive_locked_sets",
        solved=is_complete_solution(solution),
        solution=solution,
        notes=[f"mode={'advanced' if use_advanced else 'core'}"],
        **stats,
    )


_STATUS_NAMES = {
    2: "optimal",
    3: "infeasible",
    4: "infeasible_or_unbounded",
    5: "unbounded",
    9: "time_limit",
    10: "solution_limit",
    11: "interrupted",
}


def solve_gurobi(grid: Grid, mode: str = "default", time_limit: float = 5.0) -> SolveStats:
    start = perf_counter()
    validation = validate_partial(grid)
    if not validation.valid:
        return _timed_result(
            start,
            solver=f"gurobi_{mode}",
            solved=False,
            status="invalid",
            notes=[validation.message],
        )
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
        status = _STATUS_NAMES.get(model.Status, f"status_{model.Status}")
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
            status="ok" if solved else status,
            decisions=int(getattr(model, "NodeCount", 0)),
            solution=solution,
            notes=[f"gurobi_status={status}", f"runtime={model.Runtime:.6f}s"],
        )
    except Exception as exc:  # pragma: no cover - license/environment dependent
        return _timed_result(start, solver=f"gurobi_{mode}", solved=False, status="error", notes=[str(exc)])


# Backwards-compatible alias for older local notebooks or scripts.
solve_basic_backtracking = solve_recursive_backtracking
