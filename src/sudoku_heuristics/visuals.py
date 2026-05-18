from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from sudoku_heuristics.grid import Grid


def draw_grid(grid: Grid, path: Path, title: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 9)
    ax.set_xticks([])
    ax.set_yticks([])
    for i in range(10):
        width = 2.2 if i % 3 == 0 else 0.7
        ax.plot([i, i], [0, 9], color="black", linewidth=width)
        ax.plot([0, 9], [i, i], color="black", linewidth=width)
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            if value:
                ax.text(c + 0.5, 8.5 - r, str(value), ha="center", va="center", fontsize=16)
    ax.set_title(title, fontsize=12, pad=12)
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def benchmark_charts(results_csv: Path, out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(results_csv)
    paths: list[Path] = []

    summary = (
        df.groupby(["difficulty", "solver"], as_index=False)
        .agg(solved_rate=("solved", "mean"), median_ms=("elapsed_ms", "median"), median_decisions=("decisions", "median"))
        .sort_values(["difficulty", "solver"])
    )

    fig, ax = plt.subplots(figsize=(9, 4.8))
    pivot = summary.pivot(index="difficulty", columns="solver", values="solved_rate").reindex(
        ["easy", "medium", "hard", "expert"]
    )
    pivot.plot(kind="bar", ax=ax)
    ax.set_ylabel("Solved share")
    ax.set_xlabel("Difficulty")
    ax.set_ylim(0, 1.05)
    ax.set_title("Completion rate by difficulty")
    ax.legend(fontsize=8)
    path = out_dir / "completion_rate_by_difficulty.png"
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)
    paths.append(path)

    fig, ax = plt.subplots(figsize=(9, 4.8))
    pivot = summary.pivot(index="difficulty", columns="solver", values="median_ms").reindex(
        ["easy", "medium", "hard", "expert"]
    )
    pivot.plot(kind="bar", ax=ax)
    ax.set_ylabel("Median solve time (ms)")
    ax.set_xlabel("Difficulty")
    ax.set_title("Median solve time by difficulty")
    ax.legend(fontsize=8)
    path = out_dir / "median_time_by_difficulty.png"
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)
    paths.append(path)

    fig, ax = plt.subplots(figsize=(9, 4.8))
    pivot = summary.pivot(index="difficulty", columns="solver", values="median_decisions").reindex(
        ["easy", "medium", "hard", "expert"]
    )
    pivot.plot(kind="bar", ax=ax)
    ax.set_ylabel("Median decision nodes / choices")
    ax.set_xlabel("Difficulty")
    ax.set_title("Search effort proxy by difficulty")
    ax.legend(fontsize=8)
    path = out_dir / "search_effort_by_difficulty.png"
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)
    paths.append(path)
    return paths

