import math
from typing import Tuple
from dataclasses import dataclass, field
from pympler import asizeof

from src.field import Field


class Contradiction(Exception):
    """A contradiction was found during constraint propagation. Backtracking needed."""
    pass




@dataclass(slots=True)
class SudokuGrid:
    grid: list[list[Field]]  = field(
        default_factory=lambda: [
            [Field() for _ in range(9)]
            for _ in range(9)
        ]
    )

    def __post_init__(self):
        for row in range(9):
            for col in range(9):
                self.grid[row][col] = Field()

    def set_new_value(self, row: int, col: int, value: int):
        if row < 0 or row > 8:
            raise ValueError(f'Field row {row} is out of bounds')

        if col < 0 or col > 8:
            raise ValueError(f'Field Collum {col} is out of bounds')

        if value not in self.grid[row][col].pos_number:
            raise Contradiction()

        self.grid[row][col].number = value
        self.propagate(row, col, value)

    def propagate(self, row: int, col: int, value: int):
        single_pos = set()
        # skip all fields, which already have a number
        for i in range(9):
            if i != row and self.grid[i][col].number is None:
                single_pos.add(self.check_propagating_values(i, col, value))
            if i != col and self.grid[row][i].number is None:
                single_pos.add(self.check_propagating_values(row, i, value))

        # propagate quadrant
        quad_row, quad_col = self.get_quadrant_index(row, col)
        start_row, start_col = self.get_field_index(quad_row, quad_col)
        for i in range(3):
            for j in range(3):
                if (start_row + i != row and start_col + j != col and
                        self.grid[start_row + i][start_col + j].number is None):
                    single_pos.add(self.check_propagating_values(start_row + i, start_col + j, value))


    def check_propagating_values(self, row: int, col: int, value) -> Tuple[int, int, int] | None:
        self.grid[row][col].delete_posibile(value)

        if self.grid[row][col].possible_count() == 0:
            raise Contradiction()

        if self.grid[row][col].possible_count() == 1:
            # TODO: stupid solution, maybe field should know its coordinates
            return row, col, next(iter(self.grid[row][col].pos_number))
        return None

    """
    Calculates the quadrant-coordinates, which belong to the given grid-coordinates. A quadrant shall be a 3x3 subgrid, 
    a sudoku has 9 quadrants.
    
    :returns 
    (int,int): coordinates of the quadrant, values between 0 and 2
    """
    @staticmethod
    def get_quadrant_index(row_field: int, col_field: int) -> Tuple[int, int]:
        if row_field < 0 or row_field > 8:
            raise ValueError(f'Field row {row_field} is out of bounds')

        if col_field < 0 or col_field > 8:
            raise ValueError(f'Field Collum {col_field} is out of bounds')

        return math.floor(row_field / 3), math.floor(col_field / 3)


    """ 
    Calculates the grid-coordinates of the upper left corner of the given quadrant. 
    
    :returns
    (int,int): the coordinates of the upper left corner of the 3x3 square belonging to the given quadrant, values between 0 and 8
    """
    @staticmethod
    def get_field_index(row_quad: int, col_quad: int) -> Tuple[int, int]:
        if row_quad < 0 or row_quad > 2:
            raise ValueError(f'Quadrant row {row_quad} is out of bounds')

        if col_quad < 0 or col_quad > 2:
            raise ValueError(f'Quadrant Collum {col_quad} is out of bounds')

        return row_quad * 3, col_quad * 3

if __name__ == '__main__':
    grid = SudokuGrid()
    print(f"An instance of SudokuGrid has a size of {asizeof.asizeof(grid)} bytes.")