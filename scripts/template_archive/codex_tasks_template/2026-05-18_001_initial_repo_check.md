# Codex Task Template

## Objective

TBD

## Context

Only include context required to implement the task. Do not paste the whole project background.

## Files Codex Should Read

- `docs/planning/00_project_brief.md`
- `docs/planning/01_methodology_plan.md`

## Files Codex May Edit

- `src/...`
- `tests/...`
- `docs/changelog/...`

## Files Codex Must Not Edit

- `data/raw/`
- `docs/planning/` unless explicitly requested
- `latex/` unless explicitly requested

## Required Outputs

| Output | Location | Acceptance condition |
|---|---|---|
| TBD | TBD | TBD |

## Validation

```bash
uv run ruff check src tests
uv run pytest
```

## Changelog Requirement

Write a changelog entry under `docs/changelog/`.
