# Literature And Source Notes

## Sources Used

| Source | Why it matters here |
|---|---|
| Peter Norvig, [Solving Every Sudoku Puzzle](https://norvig.com/sudoku.html) | Classic practical reference for constraint propagation plus search. It motivates the proposed design: propagate constraints first, search only when necessary. |
| arXiv 2507.09708, [A Study Of Sudoku Solving Algorithms: Backtracking and Heuristic](https://arxiv.org/abs/2507.09708) | Recent small comparative study reporting that heuristic constraint propagation can outperform recursive backtracking, especially on harder levels. |
| McGuire, Tugemann and Civario, [There is no 16-Clue Sudoku](https://arxiv.org/abs/1201.0749) | Establishes Sudoku as a serious combinatorial search problem and shows why naive exhaustive search can be insufficient at larger research scale. |
| Lewis, [Stochastic Optimization Approaches for Solving Sudoku](https://arxiv.org/abs/0805.0697) | Shows that metaheuristics such as genetic algorithms, particle swarm, and simulated annealing have been tried, but are less transparent for this compact project. |
| [Gurobi 13.0 Documentation](https://docs.gurobi.com/current/) | Current official documentation checked on 18 May 2026. Used for the Gurobi MIP baseline context. |
| Gurobi Help Center, [Parameter tuning](https://support.gurobi.com/hc/en-us/articles/19998635021713-What-is-parameter-tuning) | Explains parameter tuning and notes MIP components including primal heuristics and NoRel heuristic. |
| Gurobi Help Center, [MIP Starts and Variable Hints](https://support.gurobi.com/hc/en-us/articles/20410834783377-What-are-the-differences-between-MIP-Starts-and-Variable-Hints) | Supports the interpretation that problem-specific heuristic information can guide MIP search, although this project uses parameter comparison rather than a custom MIP start. |

## Method Selection

The chosen method is a hybrid of human-readable Sudoku logic and computer-search heuristics:

- candidate elimination;
- naked singles;
- hidden singles;
- naked pairs;
- minimum remaining values branching;
- depth-first search fallback.

This was selected because it is understandable, implementable at MSc level, and strong enough to solve most generated puzzles. More advanced metaheuristics were not chosen as the main method because they are harder to explain to a non-technical reader and less directly connected to Sudoku logic.

## Evidence Gap

The literature supports that heuristics help, but many studies compare algorithms on different puzzle sets or focus only on runtime. This project fills a learning-oriented gap: it explains the reasoning, implements a working solver, and compares it against both a programming baseline and an optimisation-solver baseline with metrics that can be understood by non-specialists.
