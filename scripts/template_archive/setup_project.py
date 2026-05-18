from __future__ import annotations

import datetime as dt
from pathlib import Path
from textwrap import dedent

PROJECT_DIRS = [
    "docs/planning", "docs/codex_tasks", "docs/changelog", "docs/research_notes", "docs/meeting_notes", "docs/prompts", "docs/decisions",
    "data/raw", "data/interim", "data/processed", "data/external",
    "src", "src/eda", "src/models", "src/simulation", "src/optimisation", "src/app",
    "outputs/reports", "outputs/figures", "outputs/tables", "outputs/logs",
    "notebooks", "tests", "scripts",
    "templates",
]

FILES = {
    "pyproject.toml": """[project]\nname = \"ra-project\"\nversion = \"0.1.0\"\ndescription = \"Research assistant project workspace\"\nrequires-python = \">=3.11\"\ndependencies = [\n    \"polars>=1.0,<2.0\",\n    \"fastexcel>=0.12\",\n    \"pandas>=2.2\",\n    \"pyarrow>=16\",\n    \"openpyxl>=3.1\",\n    \"xlsxwriter>=3.2\",\n    \"matplotlib>=3.8,<4.0\",\n    \"hvplot>=0.10\",\n    \"holoviews>=1.19\",\n    \"bokeh>=3.5\",\n    \"plotly>=5.24\",\n    \"streamlit>=1.40\",\n    \"simpy>=4.1,<5.0\",\n    \"gurobipy>=12.0\",\n    \"numpy>=1.26\",\n    \"scipy>=1.12\",\n    \"scikit-learn>=1.5\",\n    \"statsmodels>=0.14\",\n    \"joblib>=1.4\",\n    \"pydantic>=2.8\",\n    \"python-dotenv>=1.0\",\n    \"rich>=13.7\",\n    \"pytest>=8.0\",\n    \"ruff>=0.8\",\n    \"jupyterlab>=4.2\",\n    \"ipykernel>=6.29\"\n]\n\n[tool.ruff]\nline-length = 100\ntarget-version = \"py311\"\nexclude = [\".venv\", \"data\", \"outputs\", \"latex\"]\n\n[tool.ruff.lint]\nselect = [\"E\", \"F\", \"I\", \"UP\", \"B\"]\nignore = [\"E501\"]\n\n[tool.pytest.ini_options]\ntestpaths = [\"tests\"]\npython_files = [\"test_*.py\"]\n""",
    "docs/planning/00_project_brief.md": """# 00 Project Brief\n\n## Project Name\n\nTBD\n\n## One-Sentence Purpose\n\nTBD\n\n## Decision Context\n\nWhat decision, research question, or managerial problem does this project support?\n\n## Stakeholders\n\n| Stakeholder | What they care about | Implication |\n|---|---|---|\n| TBD | TBD | TBD |\n\n## Deliverables\n\n| Deliverable | Owner | Status | Notes |\n|---|---|---|---|\n| TBD | TBD | Not started | TBD |\n\n## Evidence Standard\n\nSeparate observed facts, derived metrics, assumptions, model outputs, and recommendations.\n""",
    "docs/planning/01_methodology_plan.md": """# 01 Methodology Plan\n\n## Research / Analysis Question\n\nTBD\n\n## Descriptive Claims\n\nTBD\n\n## Predictive Claims\n\nTBD\n\n## Causal Claims\n\nTBD\n\n## Normative / Optimisation Claims\n\nTBD\n\n## Data Sources\n\n| Source | File / location | Observed variables | Limitations |\n|---|---|---|---|\n| TBD | TBD | TBD | TBD |\n\n## Validation Plan\n\nDefine backtesting, robustness checks, sensitivity analysis, and leakage controls.\n""",
    "docs/planning/02_assumptions_register.md": """# 02 Assumptions Register\n\n| ID | Assumption | Type | Source / rationale | Sensitivity required? | Status |\n|---|---|---|---|---:|---|\n| A001 | TBD | Data / model / operational / business | TBD | Yes | Open |\n""",
    "templates/codex_task_template.md": """# Codex Task Template\n\n## Objective\n\nTBD\n\n## Context\n\nOnly include context required to implement the task. Do not paste the whole project background.\n\n## Files Codex Should Read\n\n- `docs/planning/00_project_brief.md`\n- `docs/planning/01_methodology_plan.md`\n\n## Files Codex May Edit\n\n- `src/...`\n- `tests/...`\n- `docs/changelog/...`\n\n## Files Codex Must Not Edit\n\n- `data/raw/`\n- `docs/planning/` unless explicitly requested\n- `latex/` unless explicitly requested\n\n## Required Outputs\n\n| Output | Location | Acceptance condition |\n|---|---|---|\n| TBD | TBD | TBD |\n\n## Validation\n\n```bash\nuv run ruff check src tests\nuv run pytest\n```\n\n## Changelog Requirement\n\nWrite a changelog entry under `docs/changelog/`.\n""",
    "templates/changelog_template.md": """# Changelog Entry\n\n## Date\n\nTBD\n\n## Task\n\nTBD\n\n## Files Changed\n\n- TBD\n\n## Summary\n\nTBD\n\n## Tests / Checks Run\n\nTBD\n\n## Remaining Issues\n\nTBD\n""",
    "docs/decisions/decision_log.md": """# Decision Log\n\n| Date | Decision | Alternatives considered | Rationale | Consequence |\n|---|---|---|---|---|\n| TBD | TBD | TBD | TBD | TBD |\n""",
    "src/app/main.py": """import streamlit as st\n\nst.set_page_config(page_title=\"RA Project App\", layout=\"wide\")\n\nst.title(\"RA Project App\")\nst.write(\"Use this app for lightweight dashboards, EDA review, or decision-support prototypes.\")\n""",
    "tests/test_placeholder.py": """def test_placeholder() -> None:\n    assert True\n""",
    ".gitignore": """.venv/\nvenv/\n__pycache__/\n*.pyc\n.DS_Store\n.env\n\ndata/raw/*\n!data/raw/.gitkeep\ndata/interim/*\n!data/interim/.gitkeep\ndata/processed/*\n!data/processed/.gitkeep\n\noutputs/*\n!outputs/.gitkeep\n\n*.aux\n*.bbl\n*.bcf\n*.blg\n*.fdb_latexmk\n*.fls\n*.log\n*.out\n*.run.xml\n*.synctex.gz\n*.toc\n""",
}


def write_if_missing(path: Path, content: str) -> bool:
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def main() -> None:
    root = Path.cwd()
    for folder in PROJECT_DIRS:
        (root / folder).mkdir(parents=True, exist_ok=True)

    for folder in ["data/raw", "data/interim", "data/processed", "data/external", "outputs/reports", "outputs/figures", "outputs/tables", "outputs/logs"]:
        write_if_missing(root / folder / ".gitkeep", "")

    written = []
    skipped = []
    for rel_path, content in FILES.items():
        if write_if_missing(root / rel_path, content):
            written.append(rel_path)
        else:
            skipped.append(rel_path)

    today = dt.date.today().isoformat()
    first_task = root / f"docs/codex_tasks/{today}_001_initial_repo_check.md"
    if write_if_missing(first_task, FILES["templates/codex_task_template.md"]):
        written.append(str(first_task.relative_to(root)))

    print(f"Project enriched: {root}")
    print(f"Files written: {len(written)}")
    print(f"Files skipped: {len(skipped)}")
    if skipped:
        print("\\nSkipped existing files:")
        for item in skipped:
            print(f"  - {item}")

    print(dedent("""
    Next:
      1. Run: uv sync
      2. Edit: docs/planning/00_project_brief.md
      3. Write Codex tasks under: docs/codex_tasks/
    """).strip())


if __name__ == "__main__":
    main()
