import itertools
import random

from src.engine.grid import SudokuGrid
from src.engine.solver import SudokuSolver


# don't really need a class, just static functions

class SudokuGenerator:
    def __init__(self):
        # number of deleted fields
        self.difficulty = 45

    def generate(self):
        sudoku = self._create_full_grid()
        sudoku = self.delete_fields(sudoku)
        return sudoku

    # Note: can't update pos_numbers, reverse propagation not possible
    # for reverse propagation you would need to check for every affected field, if the number is blocked by
    # another field in the row, column or quadrant ... it's better to implement a method to recalculate pos_numbers
    # for the hole Sudoku-Grid at the end
    def delete_fields(self, sudoku: SudokuGrid):
        # flatten grid into list to choose random field to delete
        field_list = list(itertools.chain.from_iterable(sudoku.grid))
        random.shuffle(field_list)

        # TODO: test for partially set sudoku grids and

        for i in range(self.difficulty):
            field = field_list.pop()
            del field.number

        return sudoku


    @staticmethod
    def _create_full_grid():
        sudoku = SudokuGrid()
        solver = SudokuSolver(random_order=True)
        return solver.solve(sudoku)


    @staticmethod
    def _print_pos_number(self, sudoku: SudokuGrid):
        for i in range(9):
            for j in range(9):
                print(sudoku.grid[i][j].pos_number, end="")
            print()



if __name__ == '__main__':
    generator = SudokuGenerator()
    sudoku_grid = generator.generate()
    print(sudoku_grid)
