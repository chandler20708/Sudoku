# Workflow Methodology

This document describes the full ChatGPT + Codex + Google Drive research workflow used by this template.

## 1. Core idea

The workflow is based on one operating principle:

> ChatGPT plans. Codex implements. The project folder remembers.

The project folder is treated as durable memory. Instead of letting important reasoning disappear into AI chat history, research plans, assumptions, Codex tasks, and changelogs are written into markdown files.

## 2. Why this template exists

AI coding tools are powerful but expensive when used vaguely. If Codex is asked to brainstorm, plan, justify methodology, implement code, run tests, and document everything, token use grows quickly.

This workflow separates:

1. research thinking
2. planning
3. implementation
4. technical documentation
5. interpretation
6. final review

ChatGPT prepares research framing, assumptions, and implementation contracts. Codex performs bounded engineering tasks. The user retains final judgement.

## 3. Requirements

This workflow assumes your machine has:

```text
python3
make
uv
```

If `python3` or `make` is missing, the template will not initialise.

On macOS, `make` is usually available after installing Xcode Command Line Tools:

<pre class="overflow-visible! px-0!" data-start="1255" data-end="1289"><div class="relative w-full mt-4 mb-1"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="relative"><div class=""><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼd ͼr"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span>xcode-select </span><span class="ͼn">--install</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

If `uv` is missing, install it with:

<pre class="overflow-visible! px-0!" data-start="1329" data-end="1388"><div class="relative w-full mt-4 mb-1"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="relative"><div class=""><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼd ͼr"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span class="ͼl">curl</span><span> </span><span class="ͼn">-LsSf</span><span> https://astral.sh/uv/install.sh | </span><span class="ͼl">sh</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

## 4. Tool roles

### ChatGPT ($20/month)

Use ChatGPT for:

* research framing
* problem formulation
* methodological critique
* markdown planning
* documentation structure
* writing and rewriting
* assumptions review
* model logic review
* Codex task design
* interpretation and critique of outputs

ChatGPT should produce planning `.md` files before Codex is asked to code.

### Consensus Pro ($10/month) + Elicit (free version)

Use Consensus Pro and free Elicit for:

* literature search
* paper discovery
* evidence collection (Also Chatgpt Deep Research)
* research gap exploration
* checking whether a claim has academic support

These tools are evidence-finding tools, not substitutes for critical synthesis.

### Codex (included with Chatgpt Plus subscription)

Use Codex for:

* implementation
* tests
* repo edits
* refactors
* code execution
* debugging
* output generation
* technical changelogs

Codex should not be the main author of business framing, research logic, methodology, or recommendations unless the documentation directly depends on code outputs.

### Cursor (Free Version)

Use Cursor Free for:

* file navigation
* light edits
* project organisation
* quick inspection
* small manual changes

### Draw.io / Excalidraw

Use Draw.io or Excalidraw for:

* system maps
* causal maps
* process architecture
* logic maps
* conceptual diagrams
* workflow diagrams

These diagrams can be translated into markdown planning files or Codex implementation tasks.

## 5. Setup details

The intended template folder contains:

<pre class="overflow-visible! px-0!" data-start="2818" data-end="2875"><div class="relative w-full mt-4 mb-1"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="relative"><div class="pe-11 pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼd ͼr"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span>Makefile</span><br/><span>setup_latex.py</span><br/><span>README.md</span><br/><span>WORKFLOW.md</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

To initialise the project, run:

<pre class="overflow-visible! px-0!" data-start="2910" data-end="2932"><div class="relative w-full mt-4 mb-1"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="relative"><div class=""><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼd ͼr"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span class="ͼl">make</span><span> setup</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

This will:

1. check Python
2. check `uv`
3. generate `setup_project.py`
4. create the project scaffold
5. create planning and Codex task templates
6. run `setup_latex.py` if present
7. run `uv sync`

This template uses `uv` and `pyproject.toml`, not `requirements.txt`.

<pre class="overflow-visible! px-0!" data-start="3206" data-end="3347"><div class="relative w-full mt-4 mb-1"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="relative"><div class="pe-11 pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼd ͼr"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span>pyproject.toml   dependency specification</span><br/><span>uv.lock          exact resolved versions</span><br/><span>.venv/           installed virtual environment</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

Run Python inside the environment with:

<pre class="overflow-visible! px-0!" data-start="3390" data-end="3433"><div class="relative w-full mt-4 mb-1"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="relative"><div class=""><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼd ͼr"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span>uv run python path/to/script.py</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

## 6. Folder structure

After setup, the project should look broadly like this:

<pre class="overflow-visible! px-0!" data-start="3516" data-end="4235"><div class="relative w-full mt-4 mb-1"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="relative"><div class="pe-11 pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼd ͼr"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span>project/</span><br/><span>├── Makefile</span><br/><span>├── setup_project.py</span><br/><span>├── setup_latex.py</span><br/><span>├── pyproject.toml</span><br/><span>├── uv.lock</span><br/><span>├── README.md</span><br/><span>├── WORKFLOW.md</span><br/><span>├── docs/</span><br/><span>│   ├── planning/</span><br/><span>│   ├── codex_tasks/</span><br/><span>│   ├── changelog/</span><br/><span>│   ├── research_notes/</span><br/><span>│   ├── meeting_notes/</span><br/><span>│   ├── prompts/</span><br/><span>│   └── decisions/</span><br/><span>├── data/</span><br/><span>│   ├── raw/</span><br/><span>│   ├── interim/</span><br/><span>│   ├── processed/</span><br/><span>│   └── external/</span><br/><span>├── src/</span><br/><span>│   ├── eda/</span><br/><span>│   ├── models/</span><br/><span>│   ├── simulation/</span><br/><span>│   ├── optimisation/</span><br/><span>│   └── app/</span><br/><span>├── outputs/</span><br/><span>│   ├── reports/</span><br/><span>│   ├── figures/</span><br/><span>│   ├── tables/</span><br/><span>│   └── logs/</span><br/><span>├── notebooks/</span><br/><span>├── tests/</span><br/><span>├── scripts/</span><br/><span>├── templates/</span><br/><span>└── latex/</span><br/><span>    ├── main.tex</span><br/><span>    ├── harvard-manchester.tex</span><br/><span>    ├── references.bib</span><br/><span>    ├── sections/</span><br/><span>    ├── figures/</span><br/><span>    └── tables/</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

## 7. Folder contract


| Folder                 | Owner / purpose                                                       |
| ---------------------- | --------------------------------------------------------------------- |
| `docs/planning/`       | ChatGPT-owned project brief, methodology plan, assumptions register   |
| `docs/codex_tasks/`    | ChatGPT-written implementation contracts for Codex                    |
| `docs/changelog/`      | Codex-written technical memory after each coding task                 |
| `docs/research_notes/` | Paper notes, source summaries, literature extracts, research matrices |
| `docs/meeting_notes/`  | Supervisor/client/RA meeting notes and action logs                    |
| `docs/prompts/`        | Reusable prompts for ChatGPT, Codex, Elicit, Consensus                |
| `docs/decisions/`      | Decision logs and modelling-choice rationale                          |
| `data/raw/`            | Raw source data; do not edit manually                                 |
| `data/interim/`        | Partially cleaned or transformed data                                 |
| `data/processed/`      | Modelling-ready data                                                  |
| `data/external/`       | Public datasets and third-party support files                         |
| `src/`                 | Codex-edited implementation code                                      |
| `outputs/`             | Generated reports, figures, tables, and logs                          |
| `notebooks/`           | Exploration only; important logic should move to`src/`                |
| `tests/`               | Automated tests                                                       |
| `scripts/`             | Utility scripts                                                       |
| `latex/`               | Report, dissertation, or paper workspace                              |

Do not treat `outputs/` as source truth. Outputs should be reproducible from `src/` and `data/`.

## 8. Common commands


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

`make tree` uses:

<pre class="overflow-visible! px-0!" data-start="6198" data-end="6257"><div class="relative w-full mt-4 mb-1"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="relative"><div class=""><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼd ͼr"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span>tree </span><span class="ͼn">-P</span><span> </span><span class="ͼk">'*.py'</span><span> </span><span class="ͼn">-I</span><span> </span><span class="ͼk">'venv|.venv|__pycache__|.git'</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

`make cloc` uses:

<pre class="overflow-visible! px-0!" data-start="6278" data-end="6339"><div class="relative w-full mt-4 mb-1"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="relative"><div class=""><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼd ͼr"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span>cloc ./ </span><span class="ͼn">--exclude-dir</span><span class="ͼg">=</span><span>.git,venv,.venv,__pycache__</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

## 9. LaTeX workflow

Generate the LaTeX template with:

<pre class="overflow-visible! px-0!" data-start="6398" data-end="6429"><div class="relative w-full mt-4 mb-1"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="relative"><div class=""><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼd ͼr"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span class="ͼl">make</span><span> latex-template</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

or:

<pre class="overflow-visible! px-0!" data-start="6436" data-end="6470"><div class="relative w-full mt-4 mb-1"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="relative"><div class=""><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼd ͼr"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span>python3 setup_latex.py</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

Compile with:

<pre class="overflow-visible! px-0!" data-start="6487" data-end="6509"><div class="relative w-full mt-4 mb-1"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="relative"><div class=""><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼd ͼr"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span class="ͼl">make</span><span> latex</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

The LaTeX setup uses:

<pre class="overflow-visible! px-0!" data-start="6534" data-end="6592"><div class="relative w-full mt-4 mb-1"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="relative"><div class="pe-11 pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼd ͼr"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span>main.tex</span><br/><span>harvard-manchester.tex</span><br/><span>references.bib</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

The Harvard-Manchester file uses `biblatex` and `biber`.

Use citations such as:

<pre class="overflow-visible! px-0!" data-start="6676" data-end="6712"><div class="relative w-full mt-4 mb-1"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="relative"><div class=""><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼd ͼr"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span>\parencite{example2026}</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

Print references with:

<pre class="overflow-visible! px-0!" data-start="6738" data-end="6769"><div class="relative w-full mt-4 mb-1"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="relative"><div class=""><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼd ͼr"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span>\printbibliography</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

## 10. Recommended workflow

### Step 1: Plan before coding

Use ChatGPT to create or revise:

<pre class="overflow-visible! px-0!" data-start="6866" data-end="6989"><div class="relative w-full mt-4 mb-1"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="relative"><div class="pe-11 pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼd ͼr"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span>docs/planning/00_project_brief.md</span><br/><span>docs/planning/01_methodology_plan.md</span><br/><span>docs/planning/02_assumptions_register.md</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

Clarify:

* objective
* stakeholders
* data sources
* assumptions
* modelling logic
* expected outputs
* validation strategy
* limits of inference

### Step 2: Create a Codex task

Ask ChatGPT to write a task file in:

<pre class="overflow-visible! px-0!" data-start="7210" data-end="7239"><div class="relative w-full mt-4 mb-1"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="relative"><div class="pe-11 pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼd ͼr"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span>docs/codex_tasks/</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

Each task should specify:

<pre class="overflow-visible! px-0!" data-start="7268" data-end="7477"><div class="relative w-full mt-4 mb-1"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="relative"><div class="pe-11 pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼd ͼr"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span>objective</span><br/><span>files touched</span><br/><span>expected output</span><br/><span>stop condition</span><br/><span>maximum acceptable iterations</span><br/><span>files Codex should read</span><br/><span>files Codex may edit</span><br/><span>files Codex must not edit</span><br/><span>validation commands</span><br/><span>changelog requirement</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

### Step 3: Give Codex the task file

Avoid vague prompts like:

<pre class="overflow-visible! px-0!" data-start="7544" data-end="7591"><div class="relative w-full mt-4 mb-1"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="relative"><div class="pe-11 pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼd ͼr"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span>Can you improve this whole project?</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

Prefer bounded prompts like:

<pre class="overflow-visible! px-0!" data-start="7623" data-end="7814"><div class="relative w-full mt-4 mb-1"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="relative"><div class="pe-11 pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼd ͼr"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span>Read docs/codex_tasks/2026-05-03_001_initial_repo_check.md and complete the task exactly. Do not edit docs/planning. After implementation, write a changelog under docs/changelog/.</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

### Step 4: Codex writes changelog

Codex should update:

<pre class="overflow-visible! px-0!" data-start="7874" data-end="7901"><div class="relative w-full mt-4 mb-1"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="relative"><div class="pe-11 pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼd ͼr"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span>docs/changelog/</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

The changelog should record:

* what changed
* why it changed
* assumptions introduced
* tests run
* remaining problems
* next recommended task

### Step 5: You own the final 20–30%

Do not outsource all judgement to Codex.

Personally review:

* naming
* function boundaries
* assumptions
* assertions
* comments
* small iterations
* final interpretation
* whether the model logic matches the research question

This is where learning and quality control happen.

## 11. Codex usage principles

Good Codex tasks:

<pre class="overflow-visible! px-0!" data-start="8418" data-end="8610"><div class="relative w-full mt-4 mb-1"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="relative"><div class="pe-11 pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼd ͼr"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span>Implement this simulator.</span><br/><span>Refactor this module.</span><br/><span>Write tests for this function.</span><br/><span>Run the pipeline and fix errors.</span><br/><span>Generate these output tables.</span><br/><span>Convert this notebook logic into src/.</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

Bad Codex tasks:

<pre class="overflow-visible! px-0!" data-start="8630" data-end="8799"><div class="relative w-full mt-4 mb-1"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="relative"><div class="pe-11 pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼd ͼr"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span>Think through my whole dissertation.</span><br/><span>Find my research contribution.</span><br/><span>Write the business framing.</span><br/><span>Decide my methodology.</span><br/><span>Explore the whole repo and improve it.</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

Codex is expensive when used for vague reasoning. It is efficient when used as a constrained implementation engine.

## 12. Evidence discipline

Every serious research project should separate:

1. observed facts
2. derived metrics
3. assumptions
4. model outputs
5. interpretation
6. recommendations

Example:

<pre class="overflow-visible! px-0!" data-start="9112" data-end="9453"><div class="relative w-full mt-4 mb-1"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="relative"><div class="pe-11 pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼd ͼr"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span>Observed fact: the dataset records 7,128 vessel arrivals in 2024.</span><br/><span>Derived metric: monthly average arrivals = 594.</span><br/><span>Assumption: arrival seasonality in 2025 follows the 2024 pattern.</span><br/><span>Model output: the simulated peak exceeds threshold X in 14% of months.</span><br/><span>Recommendation: capacity contract X may be too low under adoption scenario S2.</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

This distinction protects the work from overclaiming.

## 13. Google Drive workflow

This template is designed to work inside a Google Drive-synced folder, for example:

<pre class="overflow-visible! px-0!" data-start="9625" data-end="9695"><div class="relative w-full mt-4 mb-1"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="relative"><div class="pe-11 pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼd ͼr"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span>Google Drive/My Drive/MSc Business Analytics/project-name/</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

Advantages:

* ChatGPT can inspect Drive files when connected.
* Codex can access the local synced folder.
* Project memory persists across tools.
* Markdown planning files are reusable.
* Outputs can be reviewed without reopening AI chats.

Do not let ChatGPT, Codex, Cursor, and Google Drive sync edit the same file simultaneously.

Recommended ownership:

<pre class="overflow-visible! px-0!" data-start="10056" data-end="10320"><div class="relative w-full mt-4 mb-1"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="relative"><div class="pe-11 pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼd ͼr"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span>docs/planning/       ChatGPT writes</span><br/><span>docs/codex_tasks/    ChatGPT writes, Codex reads</span><br/><span>docs/changelog/      Codex writes</span><br/><span>src/                 Codex edits</span><br/><span>outputs/             Codex writes</span><br/><span>latex/               manually controlled; avoid simultaneous edits</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

## 14. Why this is open

This workflow exists because AI tools are powerful but increasingly expensive.

A single coding-heavy project can burn through paid credits quickly if the coding agent is used for everything: thinking, planning, writing, implementation, testing, documentation, and iteration.

The point of this template is to make AI-assisted work more financially disciplined. Project context lives in files. ChatGPT prepares structured task contracts. Codex implements bounded tasks and writes changelogs. The workflow treats AI tools as specialised components in a research production system rather than as one expensive all-purpose assistant.

This is especially important for students, early-career researchers, research assistants, and independent builders who want high output without unlimited subscriptions or repeated token top-ups.

The broader motivation is:

> Use expensive AI only where it creates the most value.
> Keep reusable thinking in files.
> Make research workflows transparent, reproducible, and cheaper.

This template is open for anyone who wants a disciplined way to combine ChatGPT, Codex, literature tools, local coding, LaTeX, and Google Drive into one practical research workflow.
