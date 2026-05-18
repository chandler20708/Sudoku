from __future__ import annotations

import csv
from pathlib import Path

from sudoku_heuristics.benchmark import run_benchmark, write_benchmark, write_puzzles
from sudoku_heuristics.edge_cases import EDGE_CASES
from sudoku_heuristics.generator import count_solutions
from sudoku_heuristics.grid import parse_grid
from sudoku_heuristics.solvers import (
    solve_gurobi,
    solve_proposed_heuristic,
    solve_recursive_backtracking,
)
from sudoku_heuristics.visuals import benchmark_charts, draw_grid


def run_edge_cases(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    solvers = [
        lambda grid: solve_recursive_backtracking(grid, max_decisions=50_000),
        solve_proposed_heuristic,
        lambda grid: solve_gurobi(grid, "default"),
        lambda grid: solve_gurobi(grid, "heuristics"),
    ]
    rows = []
    for case in EDGE_CASES:
        solution_count = count_solutions(case.puzzle, limit=2)
        for solver in solvers:
            stats = solver(case.puzzle)
            rows.append(
                {
                    "case_id": case.case_id,
                    "category": case.category,
                    "expectation": case.expectation,
                    "solution_count_capped_at_2": solution_count,
                    "solver": stats.solver,
                    "solved": stats.solved,
                    "status": stats.status,
                    "elapsed_ms": round(stats.elapsed_ms, 6),
                    "decisions": stats.decisions,
                    "backtracks": stats.backtracks,
                    "max_depth": stats.max_depth,
                    "notes": "; ".join(stats.notes),
                }
            )
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    root = Path.cwd()
    records, rows = run_benchmark(per_difficulty=10, seed=20260518)
    write_puzzles(records, root / "data/processed/generated_puzzles.csv")
    write_benchmark(rows, root / "outputs/tables/benchmark_results.csv")
    run_edge_cases(root / "outputs/tables/edge_case_results.csv")
    benchmark_charts(root / "outputs/tables/benchmark_results.csv", root / "outputs/figures")
    easy = next(r for r in records if r.difficulty == "easy")
    expert = next(r for r in records if r.difficulty == "expert")
    edge = parse_grid("1....7.9..3..2...8..96..5....53..9...1..8...26....4...3......1..4......7..7...3..")
    draw_grid(easy.puzzle, root / "outputs/figures/example_easy_puzzle.svg", "Example easy puzzle")
    draw_grid(expert.puzzle, root / "outputs/figures/example_expert_puzzle.svg", "Example expert puzzle")
    draw_grid(edge, root / "outputs/figures/example_edge_ai_escargot.svg", "Very hard edge case: AI Escargot")
    print("Wrote benchmark data, edge-case data, and figures.")


if __name__ == "__main__":
    main()
