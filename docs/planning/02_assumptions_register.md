# 02 Assumptions Register

| ID | Assumption | Type | Source / rationale | Sensitivity required? | Status |
|---|---|---|---|---:|---|
| A001 | Clue count alone is not enough to define Sudoku difficulty. | Model | Final labels use a measured score combining clues, candidate ambiguity, and V2 search effort. | Yes | Closed |
| A002 | A 40-puzzle generated benchmark plus curated edge cases is enough for a compact empirical demonstration. | Evidence | The project scope is intentionally small and reproducible. | Yes | Open |
| A003 | Plain backtracking should have a decision budget. | Computational | Prevents one hard puzzle from blocking the whole benchmark. | No | Closed |
| A004 | Gurobi comparison can include Python model-building time. | Measurement | The measured workflow includes modelling overhead. | Yes | Open |
| A005 | Gurobi 13.0 docs represent the current Gurobi context on 18 May 2026. | Source | Verified from official docs and installed `gurobipy==13.0.2`. | Yes | Closed |
| A006 | A more advanced heuristic can be better on search effort while slower in wall-clock time. | Measurement | V2 reduces expert decisions/backtracks but spends extra time probing advanced rules. | Yes | Closed |
| A007 | Ambiguous puzzles should not be counted as proper Sudoku successes even when a solver returns a completed grid. | Validity | Proper benchmark puzzles are unique; edge cases report capped solution count separately. | No | Closed |
