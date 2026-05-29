# Sudoku Solver

small project to implement a Sudoku solver
using backtracking with Forward Checking

## Principles and Algorithms used

### Heuristics:

First Fail Principle: variables with most constrains should be tested first

1. Degree Heuristic:
2. Minimum Remaining Values:

### Forward Checking:
   - store possible values for each field 
   and propagate for each new set value
   ("partial look ahead")
   - **Aggressive Forward Checking:** if only 
   one value possible, propagate til end

   