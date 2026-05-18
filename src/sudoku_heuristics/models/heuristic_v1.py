from __future__ import annotations

from sudoku_heuristics.grid import Grid
from sudoku_heuristics.models.candidate_tools import solve_candidate_heuristic
from sudoku_heuristics.models.common import SolveStats


def solve_heuristic_v1(grid: Grid) -> SolveStats:
    """Benchmark V1: propagation, naked pairs, MRV, then DFS fallback."""
    return solve_candidate_heuristic(
        grid,
        solver="heuristic_v1_constraint_mrv",
        advanced=False,
        use_degree_tiebreak=False,
        use_lcv=False,
    )
