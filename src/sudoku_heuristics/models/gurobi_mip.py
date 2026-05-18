from __future__ import annotations

import os
from time import perf_counter

from sudoku_heuristics.grid import Grid, is_complete_solution, validate_partial
from sudoku_heuristics.models.common import SolveStats, timed_result

_STATUS_NAMES = {
    2: "optimal",
    3: "infeasible",
    4: "infeasible_or_unbounded",
    5: "unbounded",
    9: "time_limit",
    10: "solution_limit",
    11: "interrupted",
}


def solve_gurobi(grid: Grid, mode: str = "default", time_limit: float = 5.0) -> SolveStats:
    start = perf_counter()
    validation = validate_partial(grid)
    if not validation.valid:
        return timed_result(
            start,
            solver=f"gurobi_{mode}",
            solved=False,
            status="invalid",
            notes=[validation.message],
        )
    os.environ.setdefault("LC_ALL", "C")
    os.environ.setdefault("LANG", "C")
    try:
        import gurobipy as gp
        from gurobipy import GRB
    except Exception as exc:  # pragma: no cover - depends on local install
        return timed_result(start, solver=f"gurobi_{mode}", solved=False, status="unavailable", notes=[str(exc)])

    try:
        model = gp.Model("sudoku")
        model.Params.OutputFlag = 0
        model.Params.TimeLimit = time_limit
        if mode == "heuristics":
            model.Params.Heuristics = 1.0
            model.Params.MIPFocus = 1
            model.Params.NoRelHeurWork = 20
        rows = range(9)
        cols = range(9)
        digits = range(1, 10)
        x = model.addVars(rows, cols, digits, vtype=GRB.BINARY, name="x")

        for r in rows:
            for c in cols:
                model.addConstr(gp.quicksum(x[r, c, d] for d in digits) == 1)
        for r in rows:
            for d in digits:
                model.addConstr(gp.quicksum(x[r, c, d] for c in cols) == 1)
        for c in cols:
            for d in digits:
                model.addConstr(gp.quicksum(x[r, c, d] for r in rows) == 1)
        for br in range(0, 9, 3):
            for bc in range(0, 9, 3):
                for d in digits:
                    model.addConstr(
                        gp.quicksum(x[r, c, d] for r in range(br, br + 3) for c in range(bc, bc + 3))
                        == 1
                    )
        for r in rows:
            for c in cols:
                if grid[r][c]:
                    model.addConstr(x[r, c, grid[r][c]] == 1)

        model.optimize()
        status = _STATUS_NAMES.get(model.Status, f"status_{model.Status}")
        solved = model.Status == GRB.OPTIMAL or model.SolCount > 0
        solution = None
        if solved:
            solution = tuple(
                tuple(next(d for d in digits if x[r, c, d].X > 0.5) for c in cols) for r in rows
            )
            solved = is_complete_solution(solution)
        return timed_result(
            start,
            solver=f"gurobi_{mode}",
            solved=solved,
            status="ok" if solved else status,
            decisions=int(getattr(model, "NodeCount", 0)),
            solution=solution,
            notes=[f"gurobi_status={status}", f"runtime={model.Runtime:.6f}s"],
        )
    except Exception as exc:  # pragma: no cover - license/environment dependent
        return timed_result(start, solver=f"gurobi_{mode}", solved=False, status="error", notes=[str(exc)])
