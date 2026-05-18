from sudoku_heuristics.generator import count_solutions, generate_puzzle
from sudoku_heuristics.grid import is_complete_solution
from sudoku_heuristics.solvers import solve_leetcode_backtracking, solve_proposed_heuristic


def test_generator_creates_unique_solvable_puzzle() -> None:
    record = generate_puzzle("medium", seed=123)
    assert count_solutions(record.puzzle, limit=2) == 1
    assert is_complete_solution(record.solution)


def test_proposed_solver_solves_generated_hard_puzzle() -> None:
    record = generate_puzzle("hard", seed=456)
    stats = solve_proposed_heuristic(record.puzzle)
    assert stats.solved
    assert stats.solution == record.solution


def test_baseline_backtracking_solves_generated_easy_puzzle() -> None:
    record = generate_puzzle("easy", seed=789)
    stats = solve_leetcode_backtracking(record.puzzle)
    assert stats.solved
    assert stats.solution == record.solution
