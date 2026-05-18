from __future__ import annotations

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
    is_complete_solution,
    validate_partial,
)
from sudoku_heuristics.models.common import SolveStats, timed_result

Candidates = dict[Cell, set[int]]


def initial_candidates(grid: Grid) -> Candidates | None:
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


def assign(candidates: Candidates, cell: Cell, value: int, stats: dict[str, int]) -> bool:
    other_values = candidates[cell] - {value}
    for other in tuple(other_values):
        if not eliminate(candidates, cell, other, stats):
            return False
    return True


def eliminate(candidates: Candidates, cell: Cell, value: int, stats: dict[str, int]) -> bool:
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
            if not eliminate(candidates, peer, solved_value, stats):
                return False
    for unit in UNITS_BY_CELL[cell]:
        places = [u for u in unit if value in candidates[u]]
        if len(places) == 0:
            return False
        if len(places) == 1:
            stats["assignments"] += 1
            if not assign(candidates, places[0], value, stats):
                return False
    return True


def naked_subsets(candidates: Candidates, stats: dict[str, int], subset_size: int) -> bool | None:
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
                    if not eliminate(candidates, cell, value, stats):
                        return None
                    changed = True
    return changed


def _box_index(cell: Cell) -> int:
    return (cell[0] // 3) * 3 + cell[1] // 3


def locked_candidates(candidates: Candidates, stats: dict[str, int]) -> bool | None:
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
        if not eliminate(candidates, cell, value, stats):
            return None
        changed = True
    return changed


def propagate(candidates: Candidates, stats: dict[str, int], advanced: bool) -> bool:
    changed = True
    while changed:
        before = sum(len(v) for v in candidates.values())
        for cell, values in list(candidates.items()):
            if len(values) == 1:
                value = next(iter(values))
                for peer in PEERS[cell]:
                    if not eliminate(candidates, peer, value, stats):
                        return False
        for size in ((2, 3) if advanced else (2,)):
            subset_result = naked_subsets(candidates, stats, size)
            if subset_result is None:
                return False
        if advanced:
            locked_result = locked_candidates(candidates, stats)
            if locked_result is None:
                return False
        after = sum(len(v) for v in candidates.values())
        changed = after < before
    return True


def select_branch_cell(candidates: Candidates, use_degree_tiebreak: bool) -> Cell:
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


def ordered_values(candidates: Candidates, cell: Cell, use_lcv: bool) -> list[int]:
    values = sorted(candidates[cell])
    if not use_lcv:
        return values
    return sorted(values, key=lambda value: sum(value in candidates[peer] for peer in PEERS[cell]))


def search(
    candidates: Candidates,
    stats: dict[str, int],
    *,
    advanced: bool,
    use_degree_tiebreak: bool,
    use_lcv: bool,
    depth: int = 0,
) -> Candidates | None:
    stats["max_depth"] = max(stats["max_depth"], depth)
    if not propagate(candidates, stats, advanced=advanced):
        stats["backtracks"] += 1
        return None
    if all(len(values) == 1 for values in candidates.values()):
        return candidates
    cell = select_branch_cell(candidates, use_degree_tiebreak=use_degree_tiebreak)
    for value in ordered_values(candidates, cell, use_lcv=use_lcv):
        stats["decisions"] += 1
        branch = {k: set(v) for k, v in candidates.items()}
        if assign(branch, cell, value, stats):
            result = search(
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


def solve_candidate_heuristic(
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
        return timed_result(start, solver=solver, solved=False, status="invalid", notes=[validation.message])
    candidates = initial_candidates(grid)
    if candidates is None:
        return timed_result(start, solver=solver, solved=False, status="invalid")
    stats = {"decisions": 0, "backtracks": 0, "assignments": 0, "eliminations": 0, "max_depth": 0}
    result = search(
        candidates,
        stats,
        advanced=advanced,
        use_degree_tiebreak=use_degree_tiebreak,
        use_lcv=use_lcv,
    )
    if result is None:
        return timed_result(start, solver=solver, solved=False, status="no_solution", **stats)
    solution = tuple(tuple(next(iter(result[(r, c)])) for c in range(9)) for r in range(9))
    return timed_result(
        start,
        solver=solver,
        solved=is_complete_solution(solution),
        solution=solution,
        **stats,
    )
