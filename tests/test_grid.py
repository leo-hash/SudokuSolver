import unittest

from src.engine.grid import SudokuGrid


class TestGrid(unittest.TestCase):

    def setUp(self):
        self.grid1 = SudokuGrid()
        self.grid2 = SudokuGrid()

    def test_set_new_values(self):
        self.grid1.set_new_value(8, 8, 9)

        self.assertEqual(self.grid1.grid[8][8].number, 9)
        self.assertEqual(self.grid1.grid[8][8].pos_number, {9})

        for i in range(0, 8):
            self.assertEqual(self.grid1.grid[i][8].pos_number, {1, 2, 3, 4, 5, 6, 7, 8})
            self.assertEqual(self.grid1.grid[8][i].pos_number, {1, 2, 3, 4, 5, 6, 7, 8})

        quad = 6
        for i in range(3):
            for j in range(3):
                if i == 2 and j == 2:
                    continue
                self.assertEqual(self.grid1.grid[quad+j][quad+i].pos_number, {1, 2, 3, 4, 5, 6, 7, 8}, f"Field {quad+i},{quad+j} don't match")

        with self.assertRaises(ValueError):
            self.grid1.set_new_value(9, 8, 9)

        with self.assertRaises(ValueError):
            self.grid1.set_new_value(-1, 8, 9)

        with self.assertRaises(ValueError):
            self.grid1.set_new_value(8, 9, 9)

        with self.assertRaises(ValueError):
            self.grid1.set_new_value(8, -1, 9)


    def test_propagate(self):
        self.grid1.propagate(0,0,1)

        for i in range(1,9):
            self.assertEqual(self.grid1.grid[i][0].pos_number, {2, 3, 4, 5, 6, 7, 8, 9})
            self.assertEqual(self.grid1.grid[0][i].pos_number, {2, 3, 4, 5, 6, 7, 8, 9})

        for i in range(3):
            for j in range(3):
                if i == 0 and j == 0:
                    continue
                self.assertEqual(self.grid1.grid[j][i].pos_number, {2, 3, 4, 5, 6, 7, 8, 9}, f"Field {i},{j} don't match")

    def test_get_quadrant_index(self):
        self.assertEqual(self.grid1.get_quadrant_index(0, 0), (0, 0))
        self.assertEqual(self.grid1.get_quadrant_index(2,2), (0, 0))
        self.assertEqual(self.grid1.get_quadrant_index(6, 6), (2, 2))
        self.assertEqual(self.grid1.get_quadrant_index(8,8), (2, 2))

        self.assertEqual(self.grid1.get_quadrant_index(5, 3), (1, 1))
        self.assertEqual(self.grid1.get_quadrant_index(5, 3), (1, 1))
        self.assertEqual(self.grid1.get_quadrant_index(5, 3), (1, 1))
        self.assertEqual(self.grid1.get_quadrant_index(5, 3), (1, 1))

        self.assertEqual(self.grid1.get_quadrant_index(6, 2), (2, 0))
        self.assertEqual(self.grid1.get_quadrant_index(2, 6), (0, 2))

        with self.assertRaises(ValueError):
            self.grid1.get_quadrant_index(-1, 0)

        with self.assertRaises(ValueError):
            self.grid1.get_quadrant_index(9, 0)

        with self.assertRaises(ValueError):
            self.grid1.get_quadrant_index(0, -1)

        with self.assertRaises(ValueError):
            self.grid1.get_quadrant_index(0, 9)

    def test_get_field_index(self):
        self.assertEqual(self.grid1.get_field_index(0, 0), (0, 0))
        self.assertEqual(self.grid1.get_field_index(2, 2), (6, 6))

        self.assertEqual(self.grid1.get_field_index(2, 0), (6, 0))
        self.assertEqual(self.grid1.get_field_index(0, 2), (0, 6))

        self.assertEqual(self.grid1.get_field_index(1, 1), (3, 3))


        with self.assertRaises(ValueError):
            self.grid1.get_field_index(-1, 0)

        with self.assertRaises(ValueError):
            self.grid1.get_field_index(3, 0)

        with self.assertRaises(ValueError):
            self.grid1.get_field_index(0, -1)

        with self.assertRaises(ValueError):
            self.grid1.get_field_index(0, 3)


    def test_from_string(self):
        sudoku_str = '''. . . | . . 2 | 4 . .
. 6 . | 4 7 . | 5 . 9
7 . 4 | . . . | 8 . .
------+-------+------
4 2 . | . 3 8 | . 5 1
. . . | 2 . 6 | 7 9 .
. . . | 9 . 4 | . 2 .
------+-------+------
8 . 2 | . 6 . | 9 7 5
. . . | 5 . 7 | 2 . 6
. . . | 8 . . | 1 4 .'''

        grid = SudokuGrid.from_string(sudoku_str)

        self.assertEqual(grid.grid[1][1].number, 6)
        self.assertEqual(grid.grid[0][0].number, None)
        self.assertEqual(grid.grid[6][6].number, 9)
        self.assertEqual(grid.grid[6][0].number, 8)
        self.assertEqual(grid.__str__(), sudoku_str)

        sudoku_str = "s" + sudoku_str[1:]
        with self.assertRaises(ValueError):
            SudokuGrid.from_string(sudoku_str)

        sudoku_str = ". . . | . . . 2 | 4 . ."

        with self.assertRaises(ValueError):
            SudokuGrid.from_string(sudoku_str)


if __name__ == '__main__':
    unittest.main()
