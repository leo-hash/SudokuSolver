import itertools
import random

from src.grid import SudokuGrid
from src.solver import SudokuSolver





class SudokuGenerator:
    def __init__(self):
        # amount of fields with len(pos_number) > 1 -> fields that don't have a clear determined value
        # for example: difficulty = 80 -> exactly one defined field
        self.difficulty = 30

    @staticmethod
    def count_difficulty(sudoku: SudokuGrid):
        diff = 0

        for i in range(9):
            for j in range(9):
                if sudoku.grid[i][j].number is None and len(sudoku.grid[i][j].pos_number) > 1:
                    diff += 1

        return diff


    @staticmethod
    def create_full_grid():
        sudoku_grid = SudokuGrid()

        solver = SudokuSolver()
        solver.random_order = True

        full_grid = solver.solve(sudoku_grid)
        return full_grid


    def delete_fields(self, sudoku: SudokuGrid):
        # flatten grid into list to choose random field to delete
        field_list = list(itertools.chain.from_iterable(sudoku.grid))
        random.shuffle(field_list)

        # print(len(field_list))
        # TODO: test difficulty and count_difficulty, something weird happens there ...

        while self.difficulty > self.count_difficulty(sudoku):
            field = field_list.pop()
            del field.number
            # print(field.__repr__())
            # print(self.count_difficulty(sudoku))

        return sudoku

    def generate(self):
        sudoku = self.create_full_grid()
        sudoku = self.delete_fields(sudoku)
        return sudoku


if __name__ == '__main__':
    generator = SudokuGenerator()
    print(generator.generate())