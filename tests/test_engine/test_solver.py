import unittest
from copy import deepcopy

from src.engine import SudokuSolver, SudokuGrid


class TestSolver(unittest.TestCase):
    def setUp(self):
        self.sudoku1 = SudokuGrid.from_string(
            '''
                . . . | . . 2 | 4 . .
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
        )
        self.solution1 = SudokuGrid.from_string(
            """
            9 1 5 | 6 8 2 | 4 3 7
            2 6 8 | 4 7 3 | 5 1 9
            7 3 4 | 1 9 5 | 8 6 2
            ------+-------+------
            4 2 9 | 7 3 8 | 6 5 1
            5 8 3 | 2 1 6 | 7 9 4
            1 7 6 | 9 5 4 | 3 2 8
            ------+-------+------
            8 4 2 | 3 6 1 | 9 7 5
            3 9 1 | 5 4 7 | 2 8 6
            6 5 7 | 8 2 9 | 1 4 3"""
        )

        self.sudoku2 = SudokuGrid.from_string(
            '''
                000|000|000
                000|000|000
                000|000|000
                -----------
                000|000|000
                000|000|000
                000|000|000
                -----------
                000|000|975
                000|000|206
                000|000|143'''
        )

    def test_init(self):
        solver1 = SudokuSolver()
        self.assertEqual(False, solver1.random_order)
        self.assertEqual(True, solver1.mrv)
        self.assertEqual(False, solver1.afc)

        solver2 = SudokuSolver(True, False, False)
        self.assertEqual(True, solver2.random_order)
        self.assertEqual(False, solver2.mrv)
        self.assertEqual(False, solver2.afc)

        solver3 = SudokuSolver(False, True, True)
        self.assertEqual(False, solver3.random_order)
        self.assertEqual(True, solver3.mrv)
        self.assertEqual(True, solver3.afc)

    def test_choose_next_field(self):
        solver1 = SudokuSolver()

        coord = solver1.choose_next_field(self.sudoku2)
        self.assertEqual((7,7), coord )
        self.sudoku2.set_new_value(7, 7, 8)

        coord = solver1.choose_next_field(self.sudoku2)
        self.assertEqual((0, 6), coord )
        self.sudoku2.set_new_value(0, 6, 3)

        coord = solver1.choose_next_field(self.sudoku2)
        self.assertEqual((0, 7), coord )
        self.sudoku2.set_new_value(0, 7, 1)

        coord = solver1.choose_next_field(self.sudoku2)
        self.assertEqual((1, 7), coord )

    def test_create_all_assignments(self):
        solver1 = SudokuSolver()

        test_cases = [
            # (row, column, expected value)
            (0, 0, [1, 3, 5, 9]),
            (5, 4, [1, 5]),
            (5, 3, [9])
        ]

        for row, col, expected_values in test_cases:
            with self.subTest(row=row, col=col):
                # create expected sudokuGrids
                expected_assignments = []
                for value in expected_values:
                    expected = deepcopy(self.sudoku1)
                    expected.set_new_value(row, col, value)
                    expected_assignments.append(expected)

                assignments = solver1.create_all_assignments(self.sudoku1, row, col)

                self.assertEqual(expected_assignments, assignments)


    def test_solve(self):
        solver1 = SudokuSolver()
        sol = solver1.solve(self.sudoku1)
        self.assertEqual(sol, self.solution1)




if __name__ == '__main__':
    unittest.main()
