# 02 Assumptions Register

| ID | Assumption | Type | Source / rationale | Sensitivity required? | Status |
|---|---|---|---|---:|---|
| A001 | Clue count is an acceptable first-pass difficulty proxy. | Model | Useful for generated benchmark categories. | Yes | Open |
| A002 | A 20-puzzle benchmark is enough for a learning demonstration. | Evidence | User asked for small-scale literature review and practical project output. | Yes | Open |
| A003 | Plain backtracking should have a decision budget. | Computational | Prevents one hard puzzle from blocking the whole benchmark. | No | Closed |
| A004 | Gurobi comparison can include Python model-building time. | Measurement | The user-facing workflow includes modelling overhead. | Yes | Open |
| A005 | Gurobi 13.0 docs represent the current Gurobi context on 18 May 2026. | Source | Verified from official docs and installed `gurobipy==13.0.2`. | Yes | Closed |
