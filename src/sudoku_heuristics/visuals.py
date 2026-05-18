from __future__ import annotations

from pathlib import Path

import pandas as pd

from sudoku_heuristics.grid import Grid

SOLVER_LABELS = {
    "recursive_backtracking": "Plain recursive",
    "proposed_heuristic": "Proposed heuristic",
    "gurobi_default": "Gurobi default",
    "gurobi_heuristics": "Gurobi heuristic",
}
SOLVER_ORDER = list(SOLVER_LABELS)
COLORS = {
    "recursive_backtracking": "#7f8c8d",
    "proposed_heuristic": "#1f77b4",
    "gurobi_default": "#2ca02c",
    "gurobi_heuristics": "#d62728",
}


def _svg_text(x: float, y: float, text: str, size: int = 12, anchor: str = "middle") -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="Arial, sans-serif" '
        f'font-size="{size}" text-anchor="{anchor}">{text}</text>'
    )


def draw_grid(grid: Grid, path: Path, title: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    size = 450
    margin = 36
    cell = size / 9
    body = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="520" height="540" viewBox="0 0 520 540">',
        '<rect width="520" height="540" fill="white"/>',
        _svg_text(260, 25, title, 16),
        f'<g transform="translate({margin},{margin + 20})">',
        f'<rect x="0" y="0" width="{size}" height="{size}" fill="#fbfbfb"/>',
    ]
    for i in range(10):
        width = 3 if i % 3 == 0 else 1
        pos = i * cell
        body.append(
            f'<line x1="{pos:.1f}" y1="0" x2="{pos:.1f}" y2="{size}" '
            f'stroke="black" stroke-width="{width}"/>'
        )
        body.append(
            f'<line x1="0" y1="{pos:.1f}" x2="{size}" y2="{pos:.1f}" '
            f'stroke="black" stroke-width="{width}"/>'
        )
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            if value:
                body.append(_svg_text(c * cell + cell / 2, r * cell + cell * 0.67, str(value), 24))
    body.append("</g></svg>")
    path.write_text("\n".join(body), encoding="utf-8")


def _bar_chart(
    data: pd.DataFrame,
    value_col: str,
    title: str,
    ylabel: str,
    path: Path,
    cap: float | None = None,
) -> None:
    difficulties = ["easy", "medium", "hard", "expert"]
    solvers = [solver for solver in SOLVER_ORDER if solver in set(data["solver"])]
    width, height = 1080, 520
    left, top, plot_w, plot_h = 82, 55, 760, 330
    legend_x, legend_y = 875, 88
    max_value = cap if cap is not None else max(float(data[value_col].max()), 1.0)
    group_w = plot_w / len(difficulties)
    bar_w = min(24, group_w / (len(solvers) + 1))
    body = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        _svg_text(width / 2, 28, title, 18),
        f'<line x1="{left}" y1="{top + plot_h}" x2="{left + plot_w}" y2="{top + plot_h}" stroke="black"/>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top + plot_h}" stroke="black"/>',
        _svg_text(18, top + plot_h / 2, ylabel, 12, "middle").replace("<text", '<text transform="rotate(-90 18 220)"'),
    ]
    for tick in range(5):
        value = max_value * tick / 4
        y = top + plot_h - (value / max_value) * plot_h
        body.append(f'<line x1="{left - 5}" y1="{y:.1f}" x2="{left + plot_w}" y2="{y:.1f}" stroke="#ddd"/>')
        body.append(_svg_text(left - 10, y + 4, f"{value:.1f}", 10, "end"))
    for i, difficulty in enumerate(difficulties):
        center = left + group_w * i + group_w / 2
        body.append(_svg_text(center, top + plot_h + 30, difficulty, 12))
        for j, solver in enumerate(solvers):
            row = data[(data["difficulty"] == difficulty) & (data["solver"] == solver)]
            if row.empty:
                continue
            value = min(float(row.iloc[0][value_col]), max_value)
            x = center - (len(solvers) * bar_w) / 2 + j * bar_w
            h = 0 if max_value == 0 else (value / max_value) * plot_h
            y = top + plot_h - h
            label = SOLVER_LABELS.get(solver, solver)
            body.append(
                f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w - 3:.1f}" height="{h:.1f}" '
                f'fill="{COLORS.get(solver, "#444")}"><title>{label}: {value:.3f}</title></rect>'
            )
    body.append(f'<rect x="{legend_x - 18}" y="{legend_y - 28}" width="185" height="112" fill="#fff" stroke="#ddd"/>')
    body.append(_svg_text(legend_x, legend_y - 8, "Solver", 12, "start"))
    for j, solver in enumerate(solvers):
        y = legend_y + 18 + j * 22
        body.append(f'<rect x="{legend_x}" y="{y - 11}" width="13" height="13" fill="{COLORS.get(solver, "#444")}"/>')
        body.append(_svg_text(legend_x + 21, y, SOLVER_LABELS.get(solver, solver), 12, "start"))
    body.append("</svg>")
    path.write_text("\n".join(body), encoding="utf-8")


def benchmark_charts(results_csv: Path, out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(results_csv)
    summary = (
        df.groupby(["difficulty", "solver"], as_index=False)
        .agg(
            solved_rate=("solved", "mean"),
            median_ms=("elapsed_ms", "median"),
            median_decisions=("decisions", "median"),
        )
        .sort_values(["difficulty", "solver"])
    )
    paths = [
        out_dir / "completion_rate_by_difficulty.svg",
        out_dir / "median_time_by_difficulty.svg",
        out_dir / "search_effort_by_difficulty.svg",
    ]
    _bar_chart(summary, "solved_rate", "Completion rate by difficulty", "Solved share", paths[0], cap=1.0)
    _bar_chart(summary, "median_ms", "Median solve time by difficulty", "Median ms", paths[1])
    _bar_chart(summary, "median_decisions", "Search effort proxy by difficulty", "Median decisions", paths[2])
    return paths
