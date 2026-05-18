# 02 Assumptions Register

| ID | Assumption | Type | Source / rationale | Sensitivity required? | Status |
|---|---|---|---|---:|---|
| A001 | Clue count alone is not enough to define Sudoku difficulty. | Model | Final labels use a measured score combining clues, candidate ambiguity, and heuristic search effort. | Yes | Closed |
| A002 | A 40-puzzle generated benchmark plus curated edge cases is enough for a compact empirical demonstration. | Evidence | The project scope is intentionally small and reproducible. | Yes | Open |
| A003 | Plain backtracking should have a decision budget. | Computational | Prevents one hard puzzle from blocking the whole benchmark. | No | Closed |
| A004 | Gurobi comparison can include Python model-building time. | Measurement | The measured workflow includes modelling overhead. | Yes | Open |
| A005 | Gurobi 13.0 docs represent the current Gurobi context on 18 May 2026. | Source | Verified from official docs and installed `gurobipy==13.0.2`. | Yes | Closed |
