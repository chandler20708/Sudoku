from __future__ import annotations

from dataclasses import dataclass

from sudoku_heuristics.grid import Grid, parse_grid


@dataclass(frozen=True)
class EdgeCasePuzzle:
    case_id: str
    category: str
    expectation: str
    puzzle: Grid


CONTRADICTORY_PUZZLE = parse_grid(
    "55......."
    "........."
    "........."
    "........."
    "........."
    "........."
    "........."
    "........."
    "........."
)

AMBIGUOUS_PUZZLE = parse_grid("." * 81)

# A well-known hard Sudoku often referred to as AI Escargot.
AI_ESCARGOT = parse_grid(
    "1....7.9."
    ".3..2...8"
    "..96..5.."
    "..53..9.."
    ".1..8...2"
    "6....4..."
    "3......1."
    ".4......7"
    "..7...3.."
)

# A sparse valid-looking puzzle used to stress simple search. It may be solvable,
# but it is deliberately outside the normal generated benchmark distribution.
SPARSE_STRESS = parse_grid(
    ".....6..."
    ".59.....8"
    "2....8..."
    ".45......"
    "...3....."
    "...6..3.5"
    "4...325.."
    "6........"
    "........."
)

EDGE_CASES = [
    EdgeCasePuzzle(
        case_id="contradictory_duplicate",
        category="unsolvable_invalid",
        expectation="Rejected because the first row already contains duplicate fixed values.",
        puzzle=CONTRADICTORY_PUZZLE,
    ),
    EdgeCasePuzzle(
        case_id="empty_grid_ambiguous",
        category="multiple_solutions",
        expectation="Not a proper Sudoku puzzle because it is underconstrained and has many completions.",
        puzzle=AMBIGUOUS_PUZZLE,
    ),
    EdgeCasePuzzle(
        case_id="ai_escargot",
        category="very_hard",
        expectation="Solvable but designed to require deeper search than ordinary generated examples.",
        puzzle=AI_ESCARGOT,
    ),
    EdgeCasePuzzle(
        case_id="sparse_stress",
        category="stress_test",
        expectation="Sparse puzzle used to show that simple search can hit a decision budget.",
        puzzle=SPARSE_STRESS,
    ),
]
