from __future__ import annotations

from dataclasses import dataclass

Grid = tuple[tuple[int, ...], ...]
ALL_DIGITS = frozenset(range(1, 10))
ROWS = range(9)
COLS = range(9)
CELLS = tuple((r, c) for r in ROWS for c in COLS)
UNITS: tuple[tuple[tuple[int, int], ...], ...] = (
    tuple(tuple((r, c) for c in COLS) for r in ROWS)
    + tuple(tuple((r, c) for r in ROWS) for c in COLS)
    + tuple(
        tuple((r, c) for r in range(br, br + 3) for c in range(bc, bc + 3))
        for br in range(0, 9, 3)
        for bc in range(0, 9, 3)
    )
)
PEERS = {
    cell: frozenset(other for unit in UNITS if cell in unit for other in unit if other != cell)
    for cell in CELLS
}


@dataclass(frozen=True)
class ValidationResult:
    valid: bool
    message: str


def as_grid(values: list[list[int]] | tuple[tuple[int, ...], ...]) -> Grid:
    grid = tuple(tuple(int(v) for v in row) for row in values)
    if len(grid) != 9 or any(len(row) != 9 for row in grid):
        raise ValueError("Sudoku grid must be 9 by 9.")
    if any(v < 0 or v > 9 for row in grid for v in row):
        raise ValueError("Sudoku values must be integers from 0 to 9.")
    return grid


def parse_grid(text: str) -> Grid:
    chars = [ch for ch in text if ch.isdigit() or ch in "."]
    if len(chars) != 81:
        raise ValueError(f"Expected 81 cells, found {len(chars)}.")
    vals = [0 if ch in ".0" else int(ch) for ch in chars]
    return tuple(tuple(vals[i : i + 9]) for i in range(0, 81, 9))


def grid_to_line(grid: Grid) -> str:
    return "".join(str(v) if v else "." for row in grid for v in row)


def clue_count(grid: Grid) -> int:
    return sum(1 for row in grid for v in row if v)


def validate_partial(grid: Grid) -> ValidationResult:
    for unit in UNITS:
        seen: set[int] = set()
        for r, c in unit:
            value = grid[r][c]
            if value == 0:
                continue
            if value in seen:
                return ValidationResult(False, f"Duplicate {value} in a row, column, or box.")
            seen.add(value)
    return ValidationResult(True, "Valid partial grid.")


def is_complete_solution(grid: Grid) -> bool:
    if any(v == 0 for row in grid for v in row):
        return False
    return validate_partial(grid).valid


def candidates_for(grid: Grid, r: int, c: int) -> set[int]:
    if grid[r][c]:
        return {grid[r][c]}
    blocked = {grid[pr][pc] for pr, pc in PEERS[(r, c)] if grid[pr][pc]}
    return set(ALL_DIGITS - blocked)


def replace_cell(grid: Grid, r: int, c: int, value: int) -> Grid:
    rows = [list(row) for row in grid]
    rows[r][c] = value
    return as_grid(rows)


def markdown_grid(grid: Grid) -> str:
    lines = ["| |1|2|3|4|5|6|7|8|9|", "|---|---|---|---|---|---|---|---|---|---|"]
    for i, row in enumerate(grid, start=1):
        vals = [str(v) if v else "." for v in row]
        lines.append(f"|{i}|" + "|".join(vals) + "|")
    return "\n".join(lines)
