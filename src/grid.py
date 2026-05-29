import math
from typing import Tuple
from dataclasses import dataclass, field
from pympler import asizeof

from src.field import Field



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

        self.grid[row][col].number = value
        self.propagate(row, col, value)

    def propagate(self, row: int, col: int, value: int):
        # skip all fields, which already have a number
        for i in range(9):
            if i != row and self.grid[i][col].number is None:
                self.grid[i][col].delete_posibile(value)
            if i != col and self.grid[row][i].number is None:
                self.grid[row][i].delete_posibile(value)

        # propagate quadrant
        quad_row, quad_col = self.get_quadrant_index(row, col)
        for i in range(3):
            for j in range(3):
                if (quad_row + i != row and quad_col + j != col and
                        self.grid[quad_row + i][quad_col + j].number is None):
                    self.grid[quad_row + i][quad_col + j].delete_posibile(value)




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