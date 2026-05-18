# Working Progression

## Step 1: Project Setup

The research template was copied into `/Users/chandler/Documents/Sudoku` and initialised with its setup command. The template setup files were later moved to `scripts/template_archive/` so the active project tree stays focused on the Sudoku work.

## Step 2: Generator Repair

The original generator only created completed Sudoku grids and included notebook-style multiprocessing benchmarking code. The new generator creates complete grids, removes clues, checks uniqueness, and labels puzzles as easy, medium, hard, or expert using target clue counts.

## Step 3: Solver Design

Three solver families were implemented:

- plain LeetCode-style backtracking;
- proposed heuristic constraint solver;
- Gurobi binary MIP model, with default and heuristic-focused parameter settings.

## Step 4: Testing

Automated tests check:

- generated puzzles have a unique solution;
- the proposed heuristic solves generated hard puzzles;
- the baseline backtracking solver solves generated easy puzzles.

## Step 5: Benchmark

The benchmark generated 20 unique puzzles and ran 80 solver-puzzle combinations. Matplotlib was removed from the visualisation path because font-cache building was unstable in the sandbox. The final visuals are generated directly as SVG.

## Step 6: Report Writing

The final report uses the benchmark results, literature notes, Mermaid architecture, SVG figures, and explicit limitations.
