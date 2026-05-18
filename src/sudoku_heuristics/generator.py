from __future__ import annotations

import random
from dataclasses import dataclass

from sudoku_heuristics.grid import CELLS, Grid, as_grid, clue_count, replace_cell, validate_partial
from sudoku_heuristics.solvers import solve_proposed_heuristic


@dataclass(frozen=True)
class PuzzleRecord:
    puzzle_id: str
    difficulty: str
    puzzle: Grid
    solution: Grid
    clues: int


DIFFICULTY_CLUES = {
    "easy": 40,
    "medium": 34,
    "hard": 28,
    "expert": 24,
}


def generate_complete_grid(seed: int | None = None) -> Grid:
    rng = random.Random(seed)
    rows = [0, 1, 2]
    rng.shuffle(rows)
    rows += [3 + i for i in rng.sample(range(3), 3)]
    rows += [6 + i for i in rng.sample(range(3), 3)]
    cols = [0, 1, 2]
    rng.shuffle(cols)
    cols += [3 + i for i in rng.sample(range(3), 3)]
    cols += [6 + i for i in rng.sample(range(3), 3)]
    nums = list(range(1, 10))
    rng.shuffle(nums)
    grid = []
    for r in rows:
        row = []
        for c in cols:
            row.append(nums[(3 * (r % 3) + r // 3 + c) % 9])
        grid.append(row)
    return as_grid(grid)


def count_solutions(grid: Grid, limit: int = 2) -> int:
    rows = [list(row) for row in grid]
    count = 0

    def allowed(r: int, c: int, value: int) -> bool:
        if any(rows[r][j] == value for j in range(9)):
            return False
        if any(rows[i][c] == value for i in range(9)):
            return False
        br, bc = 3 * (r // 3), 3 * (c // 3)
        return all(rows[i][j] != value for i in range(br, br + 3) for j in range(bc, bc + 3))

    def dfs() -> None:
        nonlocal count
        if count >= limit:
            return
        best = None
        best_values = None
        for r, c in CELLS:
            if rows[r][c] != 0:
                continue
            values = [v for v in range(1, 10) if allowed(r, c, v)]
            if not values:
                return
            if best is None or len(values) < len(best_values or []):
                best = (r, c)
                best_values = values
        if best is None:
            count += 1
            return
        r, c = best
        for value in best_values or []:
            rows[r][c] = value
            dfs()
            rows[r][c] = 0
            if count >= limit:
                return

    if not validate_partial(grid).valid:
        return 0
    dfs()
    return count


def generate_puzzle(difficulty: str = "hard", seed: int | None = None) -> PuzzleRecord:
    if difficulty not in DIFFICULTY_CLUES:
        raise ValueError(f"Unknown difficulty: {difficulty}")
    rng = random.Random(seed)
    solution = generate_complete_grid(seed)
    puzzle = solution
    target_clues = DIFFICULTY_CLUES[difficulty]
    cells = list(CELLS)
    rng.shuffle(cells)

    for r, c in cells:
        if clue_count(puzzle) <= target_clues:
            break
        if puzzle[r][c] == 0:
            continue
        candidate = replace_cell(puzzle, r, c, 0)
        mirror = (8 - r, 8 - c)
        if mirror != (r, c) and candidate[mirror[0]][mirror[1]] != 0 and clue_count(candidate) - 1 >= target_clues:
            candidate = replace_cell(candidate, mirror[0], mirror[1], 0)
        if count_solutions(candidate, limit=2) == 1:
            puzzle = candidate

    solved = solve_proposed_heuristic(puzzle)
    if not solved.solved or solved.solution != solution:
        solved_again = solve_proposed_heuristic(puzzle)
        if not solved_again.solved:
            raise RuntimeError("Generated puzzle was not solvable by the proposed solver.")
    return PuzzleRecord(
        puzzle_id=f"{difficulty}_{seed if seed is not None else rng.randrange(1_000_000)}",
        difficulty=difficulty,
        puzzle=puzzle,
        solution=solution,
        clues=clue_count(puzzle),
    )


def generate_dataset(per_difficulty: int = 10, seed: int = 20260518) -> list[PuzzleRecord]:
    records: list[PuzzleRecord] = []
    for difficulty in DIFFICULTY_CLUES:
        for i in range(per_difficulty):
            records.append(generate_puzzle(difficulty=difficulty, seed=seed + 1000 * len(records) + i))
    return records

