import math
from typing import Tuple
from dataclasses import dataclass, field
from pympler import asizeof

from src.engine.field import Field


class Contradiction(Exception):
    """A contradiction was found during constraint propagation. Backtracking necessary."""
    pass


@dataclass(slots=True)
class SudokuGrid:
    grid: list[list[Field]]  = field(
        default_factory=lambda: [
            [Field() for _ in range(9)]
            for _ in range(9)
        ]
    )

    """
    Creates a SudokuGrid from an 81 character string
    |, + and - are filtered out, so output of __str__ is a valid input
    
    :param sudoku_str: string of 81 characters with digits 1-9 and 0 or . for empty cells
    """
    @classmethod
    def from_string(cls, sudoku_str: str) -> "SudokuGrid":
        # delete |, + and -
        sudoku_str = sudoku_str.translate(
            str.maketrans("", "", "|+-")
        )
        # delete all whitespaces
        sudoku_str = "".join(sudoku_str.split())

        if len(sudoku_str) != 81:
            raise ValueError("SudokuGrid string must have exactly 81 characters")

        if any(char not in '0123456789.' for char in sudoku_str):
            raise ValueError("SudokuGrid string must contain only digits 0-9 and '.'")

        grid = cls()

        for index, char in enumerate(sudoku_str):
            if char in "0.":
                continue

            row, col = divmod(index, 9)
            value = int(char)

            grid.set_new_value(row, col, value)
            grid.grid[row][col].is_fixed = True

        return grid


    def set_new_value(self, row: int, col: int, value: int) -> set[tuple[int, int, int]]:
        if row < 0 or row > 8:
            raise ValueError(f'Field row {row} is out of bounds')

        if col < 0 or col > 8:
            raise ValueError(f'Field Collum {col} is out of bounds')

        if value < 1 or value > 9:
            raise ValueError(f'Field value {value} should be between 1 and 9')

        if value not in self.grid[row][col].pos_number:
            raise Contradiction(f'Value of ({row},{col}) is {value}, but pos_number only allows {self.grid[row][col].pos_number} ')

        self.grid[row][col].number = value
        return self.propagate(row, col, value)


    def propagate(self, row: int, col: int, value: int) -> set[tuple[int, int, int]]:
        # fields with only one possible value for aggressive Forward Checking
        forward: set[tuple[int, int, int]] = set()

        for r, c in self._affected_fields(row, col):
            if (result := self._propagate_field(r, c, value)) is not None:
                forward.add(result)

        return forward


    def _propagate_field(self, row: int, col: int, value: int) -> Tuple[int, int, int] | None:
        curr_field = self.grid[row][col]
        curr_field.delete_posibile(value)
        count = curr_field.possible_count()

        if count == 0:
            raise Contradiction()

        if count == 1:
            return row, col, next(iter(curr_field.pos_number))

        return None

    def _affected_fields(self, row: int, col: int) -> set[tuple[int, int]]:
        seen = set()

        # row
        for r in range(9):
            if r != row:
                seen.add((r, col))

        # collum
        for c in range(9):
            if c != col:
                seen.add((row, c))

        # quadrant
        quad_row, quad_col = self.get_quadrant_index(row, col)
        start_row, start_col = self.get_field_index(quad_row, quad_col)

        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if (i, j) != (row, col):
                    seen.add((i, j))

        # filter None out
        result = set()
        for r, c in seen:
            if self.grid[r][c].number is None:
                result.add((r, c))

        return result


    """
    Calculates the quadrant of the given grid coordinates
    
    :return: 
    (int, int): the quadrant of the given grid coordinates with a value between 0 and 2
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


    def __str__(self):
        rows = []

        for row in range(9):
            values = []

            for col in range(9):
                number = self.grid[row][col].number
                values.append(str(number) if number is not None else ".")

                if col in (2, 5):
                    values.append("|")

            rows.append(" ".join(values))

            if row in (2, 5):
                rows.append("------+-------+------")

        return "\n".join(rows)


if __name__ == '__main__':
    grid = SudokuGrid()
    print(f"An instance of SudokuGrid has a size of {asizeof.asizeof(grid)} bytes.")