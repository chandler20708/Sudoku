from __future__ import annotations

import argparse
import csv
from pathlib import Path

import pandas as pd

from sudoku_heuristics.benchmark import run_benchmark, write_benchmark, write_puzzles
from sudoku_heuristics.edge_cases import AI_ESCARGOT, EDGE_CASES
from sudoku_heuristics.generator import count_solutions
from sudoku_heuristics.grid import parse_grid
from sudoku_heuristics.solvers import (
    solve_gurobi,
    solve_proposed_heuristic,
    solve_recursive_backtracking,
)
from sudoku_heuristics.visuals import benchmark_charts, draw_grid


def run_main_benchmark(root: Path) -> None:
    records, rows = run_benchmark(per_difficulty=10, seed=20260518)
    write_puzzles(records, root / "data/processed/generated_puzzles.csv")
    write_benchmark(rows, root / "outputs/tables/benchmark_results.csv")
    print("Wrote generated-puzzle benchmark data.")


def run_edge_cases(root: Path) -> None:
    path = root / "outputs/tables/edge_case_results.csv"
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
    print("Wrote edge-case benchmark data.")


def generate_figures(root: Path) -> None:
    benchmark_charts(root / "outputs/tables/benchmark_results.csv", root / "outputs/figures")
    puzzles = pd.read_csv(root / "data/processed/generated_puzzles.csv")
    easy = parse_grid(puzzles[puzzles.difficulty == "easy"].iloc[0].puzzle)
    expert = parse_grid(puzzles[puzzles.difficulty == "expert"].iloc[0].puzzle)
    draw_grid(easy, root / "outputs/figures/example_easy_puzzle.svg", "Example easy puzzle")
    draw_grid(expert, root / "outputs/figures/example_expert_puzzle.svg", "Example expert puzzle")
    draw_grid(
        AI_ESCARGOT,
        root / "outputs/figures/example_edge_ai_escargot.svg",
        "Very hard edge case: AI Escargot",
    )
    print("Wrote figures.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Sudoku benchmark steps.")
    parser.add_argument(
        "step",
        nargs="?",
        default="all",
        choices=["all", "main", "edge", "figures"],
        help="Step to run. Makefile targets call these individually for parallel execution.",
    )
    args = parser.parse_args()
    root = Path.cwd()
    if args.step in {"all", "main"}:
        run_main_benchmark(root)
    if args.step in {"all", "edge"}:
        run_edge_cases(root)
    if args.step in {"all", "figures"}:
        generate_figures(root)


if __name__ == "__main__":
    main()
