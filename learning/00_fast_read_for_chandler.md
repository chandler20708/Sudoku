# Fast Read: What This Project Shows

## Purpose

This project is designed to show that you understand how heuristics can solve a constraint problem, not just how to call a solver.

The core story is:

1. Sudoku is a constraint satisfaction problem.
2. A basic programming solver can solve it by trying numbers and undoing mistakes.
3. A heuristic solver makes better decisions before guessing:
   - remove impossible candidates;
   - fill forced cells;
   - use hidden singles;
   - use naked pairs;
   - branch on the most constrained empty cell.
4. This reduces search effort and gives a clear explanation of why the algorithm works.
5. Gurobi can also solve Sudoku as a binary integer programme, but for this small puzzle its modelling overhead is larger than the custom heuristic.

## Best One-Sentence Explanation

The proposed method solves Sudoku by repeatedly shrinking each empty cell's candidate list using Sudoku rules, and only guesses when logic can no longer force progress; when it guesses, it chooses the cell with the fewest remaining candidates.

## What To Say To A Professor

This project treats Sudoku as a small but clear optimisation and constraint reasoning problem. The proposed algorithm is not just brute force: it uses domain heuristics to reduce the search space before branching. The evaluation compares completion rate, runtime, search effort, and interpretability against plain recursive backtracking and Gurobi MIP baselines.

## Main Result From This Run

On 20 generated unique puzzles:

- Proposed heuristic: solved 20/20.
- Gurobi default: solved 20/20.
- Gurobi with heuristic-focused parameters: solved 20/20.
- Plain backtracking: solved 17/20 under a 200,000-decision cap.

The practical finding is not "Gurobi is bad". The finding is that a problem-specific heuristic is easier to explain, very fast on this small task, and gives clearer learning evidence.

## Limitation To Admit Clearly

The benchmark is small and uses generated puzzles from this project, not a large independent Sudoku corpus. The result is good enough for a learning demonstration, but not enough for a publishable claim about all Sudoku puzzles.

