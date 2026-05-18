# Sudoku Heuristics Explained Plainly

## Candidate Elimination

For every empty cell, list the digits 1 to 9 that are still possible. A digit is impossible if it already appears in the same row, column, or 3 by 3 box.

This is the basic information structure. Instead of seeing an empty cell as "unknown", the solver sees it as a smaller set such as `{2, 5}`.

## Naked Single

If a cell has only one possible candidate left, that value must go there.

Example: if a cell can only be `{7}`, the solver fills 7.

## Hidden Single

Sometimes a cell has several candidates, but within a row, column, or box, one digit can only go in one place.

Example: in a row, digit 4 may appear as a candidate in only one empty cell. Then that cell must be 4, even if the cell has other candidates too.

## Naked Pair

If two cells in the same row, column, or box have exactly the same two candidates, such as `{3, 8}` and `{3, 8}`, then those two values must occupy those two cells in some order.

So 3 and 8 can be removed from the other cells in that same row, column, or box.

## Minimum Remaining Values

When logic cannot finish the puzzle, the solver must branch. The key heuristic is to branch on the cell with the fewest possible values.

This matters because:

- a cell with 2 candidates creates at most 2 branches;
- a cell with 7 candidates creates up to 7 branches;
- choosing the smaller branch first reduces wasted search.

## What Makes This An Optimisation-Style Heuristic?

The solver is not optimising money or profit, but it is optimising search behaviour. It chooses actions that reduce uncertainty and avoid unnecessary exploration.

That is the connection to optimisation: a heuristic is a rule that does not guarantee the globally best path in every case, but usually gives a much better practical route through a hard search space.

