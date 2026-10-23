import time
import random

from src.engine.grid import SudokuGrid, Contradiction
from copy import deepcopy


class SudokuSolver:

    def __init__(self, random_order=False, mrv=True, afc=False):
        # flag to activate aggressive forward checking
        self.afc = afc
        # flag to activate Minimum Remaining Value Heuristic
        self.mrv = mrv
        # flag to activate randomisation of pos_numbers in create_all_assignments() for generating Sudoku puzzles
        self.random_order = random_order


    """
    Memory optimized implementation: 
    instead of expanding the state (like in create_all_assignments)
    only a successive state is generated and solved with a recursive call
    """
    def solve_recursive(self, sudoku: SudokuGrid):
        raise NotImplementedError


    def solve(self, sudoku: SudokuGrid):
        stack  = [sudoku]
        finished = False    # not necessary, break in if statement does it better
        solution = None

        # break conditions: empty stack (Fail) or complete assignment found
        while stack and not finished:
            curr_grid = stack.pop()

            field = self.choose_next_field(curr_grid)

            if field is None:
                finished = True
                solution = curr_grid
                break

            row, col = field
            stack.extend(self.create_all_assignments(curr_grid, row, col))

        return solution


    def choose_next_field(self, sudoku: SudokuGrid) -> tuple[int, int] | None:
        best = None
        best_count  = 10

        for row in range(9):
            for col in range(9):
                field = sudoku.grid[row][col]
                if field.number is None:
                    if self.mrv:
                        # with Minimum Remaining Values Heuristic
                        count = field.possible_count()

                        if count < best_count:
                            best_count = count
                            best = (row, col)
                    else:
                        # without Minimum Remaining Values Heuristic
                        return row, col
        return best

    def create_all_assignments(self, sudoku: SudokuGrid, row, col) -> list[SudokuGrid]:
        new_states = list[SudokuGrid]()
        num_list = list(sudoku.grid[row][col].pos_number)

        if self.random_order:
            # shuffle num_list to create a different Sudoku puzzle each time (for puzzle generation)
            random.shuffle(num_list)

        for num in num_list:
            new_sudoku = deepcopy(sudoku)

            try:
                forward = new_sudoku.set_new_value(row, col, num)
                self.aggressive_forward_checking(forward)
            except Contradiction:
                # Backtracking -> skip current digit -> previous state with different digit chosen
                continue

            new_states.append(new_sudoku)

        return new_states


    def aggressive_forward_checking(self, forward: set[tuple[int, int, int]]):
        if self.afc:
            raise NotImplementedError


if __name__ == '__main__':
    start_time = time.perf_counter()

    sudoku_grid = SudokuGrid()
    solver = SudokuSolver()
    solver.random_order = True
    sol = solver.solve(sudoku_grid)

    if sol is not None:
        print("Solution found")
        print(sol)
    else:
        print("Solution not found")


    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.3f} seconds")



