from __future__ import annotations

import csv
from pathlib import Path

from sudoku_heuristics.generator import PuzzleRecord, generate_dataset
from sudoku_heuristics.grid import grid_to_line
from sudoku_heuristics.solvers import (
    SolveStats,
    solve_gurobi,
    solve_heuristic_v1,
    solve_heuristic_v2,
    solve_recursive_backtracking,
)


def write_puzzles(records: list[PuzzleRecord], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["puzzle_id", "difficulty", "difficulty_score", "clues", "puzzle", "solution"])
        writer.writeheader()
        for record in records:
            writer.writerow(
                {
                    "puzzle_id": record.puzzle_id,
                    "difficulty": record.difficulty,
                    "difficulty_score": round(record.difficulty_score, 3),
                    "clues": record.clues,
                    "puzzle": grid_to_line(record.puzzle),
                    "solution": grid_to_line(record.solution),
                }
            )


def _row(record: PuzzleRecord, stats: SolveStats) -> dict[str, object]:
    return {
        "puzzle_id": record.puzzle_id,
        "difficulty": record.difficulty,
        "difficulty_score": round(record.difficulty_score, 3),
        "clues": record.clues,
        "solver": stats.solver,
        "solved": stats.solved,
        "elapsed_ms": round(stats.elapsed_ms, 6),
        "decisions": stats.decisions,
        "backtracks": stats.backtracks,
        "assignments": stats.assignments,
        "eliminations": stats.eliminations,
        "max_depth": stats.max_depth,
        "status": stats.status,
        "notes": "; ".join(stats.notes),
    }


def solver_suite():
    return [
        solve_recursive_backtracking,
        solve_heuristic_v1,
        solve_heuristic_v2,
        lambda grid: solve_gurobi(grid, "default"),
        lambda grid: solve_gurobi(grid, "heuristics"),
    ]


def run_benchmark(per_difficulty: int = 8, seed: int = 20260518) -> tuple[list[PuzzleRecord], list[dict[str, object]]]:
    records = generate_dataset(per_difficulty=per_difficulty, seed=seed)
    rows: list[dict[str, object]] = []
    for record in records:
        for solver in solver_suite():
            stats = solver(record.puzzle)
            rows.append(_row(record, stats))
    return records, rows


def write_benchmark(rows: list[dict[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
