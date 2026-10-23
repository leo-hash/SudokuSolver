# Sudoku Solver

small project to implement a Sudoku solver
using backtracking with Forward Checking

## Installation
```bash
pip install -r requirements.txt
```

## Execution

### Generator
```bash
python -m src.engine.generator
```

### GUI
```bash
python -m src.gui.main 
```

## Tests 

### Single Test
```
python -m unittest tests.test_engine.[test_file].[test_class].[test_method]
```
#### Example
``` bash
python -m unittest tests.test_engine.test_solver.TestSolver
```

``` bash
python -m unittest tests.test_engine.test_solver.TestSolver.test_init
```

### Test Suite

``` bash
python -m tests.test_engine.suite_engine
```

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

### Terminology

Field: One small Field in a Sudoku-Grid with possible values of 1 to 9.

Quadrant: 3x3 Fields, each digit can only occur once in a Quadrant. Each Grid consists of 3x3 Quadrants.  
