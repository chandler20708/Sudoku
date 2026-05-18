from sudoku_heuristics.edge_cases import AI_ESCARGOT, AMBIGUOUS_PUZZLE, CONTRADICTORY_PUZZLE
from sudoku_heuristics.generator import classify_puzzle, count_solutions, generate_puzzle
from sudoku_heuristics.grid import is_complete_solution
from sudoku_heuristics.solvers import solve_heuristic_v2, solve_recursive_backtracking


def test_generator_creates_unique_solvable_puzzle() -> None:
    record = generate_puzzle("medium", seed=123)
    assert count_solutions(record.puzzle, limit=2) == 1
    assert classify_puzzle(record.puzzle).status == "unique"
    assert is_complete_solution(record.solution)
    assert record.difficulty_score > 0


def test_proposed_v2_solver_solves_generated_hard_puzzle() -> None:
    record = generate_puzzle("hard", seed=456)
    stats = solve_heuristic_v2(record.puzzle)
    assert stats.solved
    assert stats.solution == record.solution


def test_proposed_v2_solver_solves_ai_escargot() -> None:
    stats = solve_heuristic_v2(AI_ESCARGOT)
    assert stats.solved
    assert stats.decisions < 100


def test_baseline_backtracking_solves_generated_easy_puzzle() -> None:
    record = generate_puzzle("easy", seed=789)
    stats = solve_recursive_backtracking(record.puzzle)
    assert stats.solved
    assert stats.solution == record.solution


def test_contradictory_puzzle_is_rejected_by_all_local_solvers() -> None:
    for solver in (solve_recursive_backtracking, solve_heuristic_v2):
        stats = solver(CONTRADICTORY_PUZZLE)
        assert not stats.solved
        assert stats.status == "invalid"


def test_ambiguous_puzzle_has_multiple_solutions() -> None:
    assert count_solutions(AMBIGUOUS_PUZZLE, limit=2) == 2
    classification = classify_puzzle(AMBIGUOUS_PUZZLE, solution_limit=2)
    assert classification.status == "multiple_solutions"
    assert classification.solution_count_capped == 2
