from __future__ import annotations

from time import perf_counter

from sudoku_heuristics.grid import (
    ALL_DIGITS,
    CELLS,
    PEERS,
    UNITS_BY_CELL,
    Cell,
    Grid,
    is_complete_solution,
    validate_partial,
)
from sudoku_heuristics.solvers import SolveStats

Candidates = dict[Cell, set[int]]


def _timed_result(start: float, **kwargs: object) -> SolveStats:
    return SolveStats(elapsed_ms=(perf_counter() - start) * 1000, **kwargs)


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


def _naked_pairs(candidates: Candidates, stats: dict[str, int]) -> bool | None:
    changed = False
    seen_units = {unit for units in UNITS_BY_CELL.values() for unit in units}
    for unit in seen_units:
        pairs: dict[tuple[int, int], list[Cell]] = {}
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
                for value in tuple(set(pair) & candidates[cell]):
                    if not _eliminate(candidates, cell, value, stats):
                        return None
                    changed = True
    return changed


def _propagate(candidates: Candidates, stats: dict[str, int]) -> bool:
    changed = True
    while changed:
        before = sum(len(values) for values in candidates.values())
        for cell, values in list(candidates.items()):
            if len(values) == 1:
                value = next(iter(values))
                for peer in PEERS[cell]:
                    if not _eliminate(candidates, peer, value, stats):
                        return False
        naked_pair_result = _naked_pairs(candidates, stats)
        if naked_pair_result is None:
            return False
        after = sum(len(values) for values in candidates.values())
        changed = after < before
    return True


def _search(candidates: Candidates, stats: dict[str, int], depth: int = 0) -> Candidates | None:
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


def solve_heuristic_v1_legacy(grid: Grid) -> SolveStats:
    """Original V1-style solver kept for audit and learning reference.

    Production benchmarking uses `solve_heuristic_v1` from `solvers.py`, which
    shares internals with V2. This function keeps the old standalone V1 flow in
    source form: propagation, hidden singles, naked pairs, MRV, then DFS.
    """
    start = perf_counter()
    validation = validate_partial(grid)
    if not validation.valid:
        return _timed_result(
            start,
            solver="heuristic_v1_legacy_reference",
            solved=False,
            status="invalid",
            notes=[validation.message],
        )
    candidates = _initial_candidates(grid)
    if candidates is None:
        return _timed_result(start, solver="heuristic_v1_legacy_reference", solved=False, status="invalid")
    stats = {"decisions": 0, "backtracks": 0, "assignments": 0, "eliminations": 0, "max_depth": 0}
    result = _search(candidates, stats)
    if result is None:
        return _timed_result(
            start,
            solver="heuristic_v1_legacy_reference",
            solved=False,
            status="no_solution",
            **stats,
        )
    solution = tuple(tuple(next(iter(result[(r, c)])) for c in range(9)) for r in range(9))
    return _timed_result(
        start,
        solver="heuristic_v1_legacy_reference",
        solved=is_complete_solution(solution),
        solution=solution,
        **stats,
    )
