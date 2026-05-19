# V2 Heuristic Literature Notes

## Purpose

This note records the second research pass used to move from the original proposed solver to the final V2 solver.

The design goal was not to add the most complicated Sudoku rule possible. The design goal was to add a stronger but still explainable heuristic layer that can be defended to a non-specialist reader.

## Sources Rechecked

| Source | Finding | Design implication |
|---|---|---|
| Peter Norvig, [Solving Every Sudoku Puzzle](https://norvig.com/sudoku.html) | Constraint propagation plus search is a compact and strong Sudoku-solving pattern. | Keep V1 as the core architecture rather than replacing it. |
| [Sudoku9x9 locked candidates](https://www.sudoku9x9.com/techniques/lockedcandidates/) | Locked candidates remove a value from a row/column when box placement forces that value into the same line, and vice versa. | Add locked-candidate eliminations because they are visual and explainable. |
| [OnSudoku pointing pairs](https://onsudoku.com/how-to-solve-sudoku/pointing-pairs/) | Pointing pairs/triples are a practical intermediate Sudoku strategy. | Use this as the plain-language explanation for part of V2. |
| Gurobi, [Parameter Reference](https://docs.gurobi.com/projects/optimizer/en/current/reference/parameters.html) | Gurobi exposes heuristic controls such as NoRel heuristic work and broader MIP heuristic settings. | Keep Gurobi heuristic mode as a separate baseline, but do not claim it is custom Sudoku logic. |
| Gurobi Help Center, [Parameter tuning](https://support.gurobi.com/hc/en-us/articles/19998635021713-What-is-parameter-tuning) | Parameter tuning can improve solver performance, including through primal heuristics and other MIP components. | Explain that Gurobi heuristics are general-purpose MIP heuristics, not human Sudoku heuristics. |

## Candidate V2 Ideas Considered

| Idea | Kept? | Reason |
|---|---:|---|
| Locked candidates / pointing and claiming | Yes | Explainable, local, and reduces candidates without guessing. |
| Naked triples | Yes | Natural extension of naked pairs already in V1. |
| Degree tie-breaker after MRV | Yes | If two cells have the same candidate count, choose the one connected to more unresolved peers. |
| Least-constraining value | No | Tested, but it increased search effort on AI Escargot and did not improve the benchmark enough to justify inclusion. |
| X-wing and chains | No | Useful but harder to explain and implement cleanly in this compact project. |
| Full exact-cover / dancing links replacement | No | Strong algorithmically, but would shift the project away from the stated heuristic-learning narrative. |

## Final V2 Decision

The final solver is named `heuristic_v2_adaptive_locked_sets`.

It does not blindly run every advanced rule. It first compares a V1 propagation pass with an advanced propagation pass. If locked candidates and naked triples reduce the candidate space enough, V2 uses the advanced path with a degree tie-breaker. If they do not, V2 uses the faster V1 core.

This is a better research answer than simply adding more rules because it shows the key heuristic idea: spend extra reasoning only when the expected search reduction is worth it.

## Evidence From Regenerated Benchmark

- V2 solved 40/40 generated puzzles.
- V1 also solved 40/40 generated puzzles.
- After the strategy-pattern refactor, V2 still solved 40/40 generated puzzles but was slower than V1 on the small benchmark because strategy dispatch, probing, and advanced propagation add overhead.
- The main V2 contribution is now architectural extensibility: candidate-update rules are separate injected strategies rather than hard-coded branches.
- On AI Escargot, V2 selected core mode and solved with the same 19 decisions as V1, avoiding the worse advanced-only path.

## Honest Limitation

V2 is better as a demonstration of adaptive heuristic architecture and future extensibility. It is not faster than V1 on this small generated dataset. The final report states this directly.
