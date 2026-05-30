# Sudoku Solver

small project to implement a Sudoku solver
using backtracking with Forward Checking

## Principles and Algorithms used

### Heuristics:

First Fail Principle: variables with most constrains should be tested first

Minimum Remaining Values: prefer variables with the least remaining possible values, 
because they have the least degrees of freedom and are the most likely to fail. 
Therefore, faster backtracking in a hopeless situation. 

### Forward Checking:
   - store possible values for each field 
   and propagate for each new set value
   ("partial look ahead")
   - **Aggressive Forward Checking:** if only 
   one value possible, propagate til end

   