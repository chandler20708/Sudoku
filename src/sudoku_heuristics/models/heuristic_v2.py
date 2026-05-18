from __future__ import annotations

from time import perf_counter

from sudoku_heuristics.grid import Grid, is_complete_solution, validate_partial
from sudoku_heuristics.models.candidate_tools import initial_candidates, propagate, search
from sudoku_heuristics.models.common import SolveStats, timed_result


def solve_heuristic_v2(grid: Grid) -> SolveStats:
    """Proposed V2: adaptive locked-candidates/naked-triples heuristic."""
    start = perf_counter()
    validation = validate_partial(grid)
    if not validation.valid:
        return timed_result(
            start,
            solver="heuristic_v2_adaptive_locked_sets",
            solved=False,
            status="invalid",
            notes=[validation.message],
        )

    basic = initial_candidates(grid)
    advanced = initial_candidates(grid)
    if basic is None or advanced is None:
        return timed_result(
            start,
            solver="heuristic_v2_adaptive_locked_sets",
            solved=False,
            status="invalid",
        )

    basic_stats = {"decisions": 0, "backtracks": 0, "assignments": 0, "eliminations": 0, "max_depth": 0}
    advanced_stats = {"decisions": 0, "backtracks": 0, "assignments": 0, "eliminations": 0, "max_depth": 0}
    if not propagate(basic, basic_stats, advanced=False):
        return timed_result(
            start,
            solver="heuristic_v2_adaptive_locked_sets",
            solved=False,
            status="no_solution",
            **basic_stats,
        )
    if not propagate(advanced, advanced_stats, advanced=True):
        advanced = basic
        advanced_stats = basic_stats.copy()

    basic_size = sum(len(values) for values in basic.values())
    advanced_size = sum(len(values) for values in advanced.values())
    basic_unsolved = sum(1 for values in basic.values() if len(values) > 1)
    advanced_unsolved = sum(1 for values in advanced.values() if len(values) > 1)
    use_advanced = (basic_size - advanced_size >= 10) or (basic_unsolved - advanced_unsolved >= 2)
    candidates = advanced if use_advanced else basic
    stats = advanced_stats if use_advanced else basic_stats
    result = search(
        candidates,
        stats,
        advanced=use_advanced,
        use_degree_tiebreak=use_advanced,
        use_lcv=False,
    )
    if result is None:
        return timed_result(
            start,
            solver="heuristic_v2_adaptive_locked_sets",
            solved=False,
            status="no_solution",
            notes=[f"mode={'advanced' if use_advanced else 'core'}"],
            **stats,
        )
    solution = tuple(tuple(next(iter(result[(r, c)])) for c in range(9)) for r in range(9))
    return timed_result(
        start,
        solver="heuristic_v2_adaptive_locked_sets",
        solved=is_complete_solution(solution),
        solution=solution,
        notes=[f"mode={'advanced' if use_advanced else 'core'}"],
        **stats,
    )
