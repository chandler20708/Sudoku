# Sudoku Heuristics Research Project

This repo is a small research project showing how heuristics can solve Sudoku and how that compares with plain recursive backtracking and Gurobi MIP baselines.

Main outputs:

- final report: `outputs/reports/final_sudoku_heuristics_report.md`
- learning notes: `learning/`
- benchmark table: `outputs/tables/benchmark_results.csv`
- visuals: `outputs/figures/`

Run validation:

```bash
uv run pytest
uv run ruff check src tests
```

Run the benchmark:

```bash
PYTHONPATH=src LC_ALL=C LANG=C uv run python scripts/run_benchmark.py
```

The original research-assistant template notes are below.

# RA Template: ChatGPT + Codex + Google Drive Research Workflow

If `python3` or `make` is missing, the template will not initialise.

On macOS, `make` is usually available after installing Xcode Command Line Tools:

<pre class="overflow-visible! px-0!" data-start="1337" data-end="1371"><div class="relative w-full mt-4 mb-1"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="relative"><div class=""><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼd ͼr"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span>xcode-select </span><span class="ͼn">--install</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

If `uv` is missing, install it with:

<pre class="overflow-visible! px-0!" data-start="1411" data-end="1470"><div class="relative w-full mt-4 mb-1"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="relative"><div class=""><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼd ͼr"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span class="ͼl">curl</span><span> </span><span class="ͼn">-LsSf</span><span> https://astral.sh/uv/install.sh | </span><span class="ͼl">sh</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

## Getting started

The intended template folder contains:

<pre class="overflow-visible! px-0!" data-start="1522" data-end="1579"><div class="relative w-full mt-4 mb-1"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="relative"><div class="pe-11 pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼd ͼr"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span>Makefile</span><br/><span>setup_latex.py</span><br/><span>README.md</span><br/><span>WORKFLOW.md</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

To initialise the project, run:

<pre class="overflow-visible! px-0!" data-start="1614" data-end="1636"><div class="relative w-full mt-4 mb-1"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="relative"><div class=""><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼd ͼr"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span class="ͼl">make</span><span> setup</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

This will:

1. check Python
2. check `uv`
3. generate `setup_project.py`
4. create the project scaffold
5. create planning and Codex task templates
6. run `setup_latex.py` if present
7. run `uv sync`

This template uses `uv` and `pyproject.toml`, not `requirements.txt`.

<pre class="overflow-visible! px-0!" data-start="1910" data-end="2051"><div class="relative w-full mt-4 mb-1"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="relative"><div class="pe-11 pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼd ͼr"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span>pyproject.toml   dependency specification</span><br/><span>uv.lock          exact resolved versions</span><br/><span>.venv/           installed virtual environment</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

Run Python inside the environment with:

<pre class="overflow-visible! px-0!" data-start="2094" data-end="2137"><div class="relative w-full mt-4 mb-1"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="relative"><div class=""><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼd ͼr"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span>uv run python path/to/script.py</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

## Common commands


| Command                | Purpose                                              |
| ---------------------- | ---------------------------------------------------- |
| `make setup`           | Full setup: scaffold + LaTeX template +`uv sync`     |
| `make start`           | Re-run`setup_project.py`; existing files are skipped |
| `make latex-template`  | Run`setup_latex.py`                                  |
| `make latex`           | Compile`latex/main.tex`                              |
| `make sync`            | Run`uv sync`                                         |
| `make test`            | Run tests                                            |
| `make check`           | Run linting and tests                                |
| `make fmt`             | Format and auto-fix code                             |
| `make app`             | Run Streamlit app                                    |
| `make tree`            | Show Python file tree                                |
| `make cloc`            | Count code lines                                     |
| `make codex-task`      | Create timestamped Codex task file                   |
| `make reset-generated` | Delete generated folders/files; use carefully        |

## Recommended workflow

1. Use ChatGPT to write planning files in `docs/planning/`.
2. Ask ChatGPT to create a bounded Codex task in `docs/codex_tasks/`.
3. Give Codex the task file, not a vague project prompt.
4. Codex implements and writes a changelog in `docs/changelog/`.
5. You review the final 20–30%: naming, assumptions, function boundaries, comments, assertions, and interpretation.

## More detail

See [`WORKFLOW.md`](WORKFLOW.md) for the full methodology, folder contract, evidence discipline, and Google Drive workflow.

Reusable template for research assistant projects, dissertations, modelling projects, and code-heavy research workflows.

Core principle:

> ChatGPT plans. Codex implements. The project folder remembers.

This template separates research thinking, implementation, documentation, and review so expensive coding-agent usage is focused on bounded engineering tasks rather than vague project reasoning.

## Tool roles


| Tool                        | Role                                                                                       |
| --------------------------- | ------------------------------------------------------------------------------------------ |
| ChatGPT                     | Research framing, methodology, markdown planning, writing, critique, Codex task design     |
| Consensus Pro + free Elicit | Literature search, paper discovery, evidence collection, claim checking                    |
| Codex                       | Implementation, tests, repo edits, refactors, code execution, debugging, output generation |
| Cursor Free                 | File navigation, light edits, local project organisation                                   |
| Draw.io / Excalidraw        | System maps, causal maps, process architecture, workflow diagrams                          |

## Requirements

Before using the template, make sure your machine has:

```text
python3
make
uv
```
