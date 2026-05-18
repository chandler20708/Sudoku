from __future__ import annotations

from pathlib import Path

from sudoku_heuristics.benchmark import run_benchmark, write_benchmark, write_puzzles
from sudoku_heuristics.visuals import benchmark_charts, draw_grid


def main() -> None:
    root = Path.cwd()
    records, rows = run_benchmark(per_difficulty=5, seed=20260518)
    write_puzzles(records, root / "data/processed/generated_puzzles.csv")
    write_benchmark(rows, root / "outputs/tables/benchmark_results.csv")
    benchmark_charts(root / "outputs/tables/benchmark_results.csv", root / "outputs/figures")
    easy = next(r for r in records if r.difficulty == "easy")
    expert = next(r for r in records if r.difficulty == "expert")
    draw_grid(easy.puzzle, root / "outputs/figures/example_easy_puzzle.svg", "Example easy puzzle")
    draw_grid(expert.puzzle, root / "outputs/figures/example_expert_puzzle.svg", "Example expert puzzle")
    print("Wrote benchmark data and figures.")


if __name__ == "__main__":
    main()
