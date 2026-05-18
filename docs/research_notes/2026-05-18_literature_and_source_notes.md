# Literature And Source Notes

## Sources Used

| Source | Why it matters here |
|---|---|
| Peter Norvig, [Solving Every Sudoku Puzzle](https://norvig.com/sudoku.html) | Classic practical reference for constraint propagation plus search. It motivates the V1 design: propagate constraints first, search only when necessary. |
| [Sudoku9x9 locked candidates](https://www.sudoku9x9.com/techniques/lockedcandidates/) | Explains locked candidates as a row/column/box candidate-removal strategy. It motivates V2's advanced propagation. |
| [OnSudoku pointing pairs](https://onsudoku.com/how-to-solve-sudoku/pointing-pairs/) | Gives a plain explanation of pointing pairs/triples, one type of locked-candidate reasoning. |
| McGuire, Tugemann and Civario, [There is no 16-Clue Sudoku](https://arxiv.org/abs/1201.0749) | Establishes Sudoku as a serious combinatorial search problem and shows why naive exhaustive search can be insufficient at larger research scale. |
| Lewis, [Stochastic Optimization Approaches for Solving Sudoku](https://arxiv.org/abs/0805.0697) | Shows that metaheuristics such as genetic algorithms, particle swarm, and simulated annealing have been tried, but are less transparent for this compact project. |
| [Gurobi 13.0 Documentation](https://docs.gurobi.com/current/) | Current official documentation checked on 18 May 2026. Used for the Gurobi MIP baseline context. |
| Gurobi, [Parameter Reference](https://docs.gurobi.com/projects/optimizer/en/current/reference/parameters.html) | Confirms current heuristic-related and search-control parameters, including NoRel heuristic controls. |
| Gurobi Help Center, [Parameter tuning](https://support.gurobi.com/hc/en-us/articles/19998635021713-What-is-parameter-tuning) | Explains parameter tuning and notes MIP components including primal heuristics and NoRel heuristic. |
| Gurobi Help Center, [MIP Starts and Variable Hints](https://support.gurobi.com/hc/en-us/articles/20410834783377-What-are-the-differences-between-MIP-Starts-and-Variable-Hints) | Supports the interpretation that problem-specific heuristic information can guide MIP search, although this project uses parameter comparison rather than a custom MIP start. |

## Method Selection

The project now separates the custom solvers into named stages:

- `heuristic_v1_constraint_mrv`: candidate elimination, naked singles, hidden singles, naked pairs, MRV branching, and depth-first fallback search.
- `heuristic_v2_adaptive_locked_sets`: V1 core plus an adaptive locked-candidates/naked-triples probe and degree tie-breaker when the advanced path is useful.

Least-constraining value was researched and tested, but it was not selected because it made the hard AI Escargot edge case worse in this implementation.

## Evidence Gap

The literature supports that heuristics help, but many studies compare algorithms on different puzzle sets or focus only on runtime. This project fills an explanatory gap: it explains the reasoning, implements a working solver, includes invalid and ambiguous edge cases, and compares the method against both a programming baseline and an optimisation-solver baseline with metrics that can be understood by non-specialists.
