from __future__ import annotations

from dataclasses import dataclass, field
from time import perf_counter

from sudoku_heuristics.grid import Grid


@dataclass
class SolveStats:
    solver: str
    solved: bool
    elapsed_ms: float
    decisions: int = 0
    backtracks: int = 0
    assignments: int = 0
    eliminations: int = 0
    max_depth: int = 0
    status: str = "ok"
    solution: Grid | None = None
    notes: list[str] = field(default_factory=list)


def timed_result(start: float, **kwargs: object) -> SolveStats:
    return SolveStats(elapsed_ms=(perf_counter() - start) * 1000, **kwargs)
