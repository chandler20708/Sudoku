from sudoku_heuristics.models.common import SolveStats
from sudoku_heuristics.models.gurobi_mip import solve_gurobi
from sudoku_heuristics.models.heuristic_v1 import solve_heuristic_v1
from sudoku_heuristics.models.heuristic_v1_legacy import solve_heuristic_v1_legacy
from sudoku_heuristics.models.heuristic_v2 import solve_heuristic_v2
from sudoku_heuristics.models.recursive_backtracking import solve_recursive_backtracking

solve_basic_backtracking = solve_recursive_backtracking

__all__ = [
    "SolveStats",
    "solve_basic_backtracking",
    "solve_gurobi",
    "solve_heuristic_v1",
    "solve_heuristic_v1_legacy",
    "solve_heuristic_v2",
    "solve_recursive_backtracking",
]
