import unittest

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
        raise NotImplementedError

    def test_create_all_assignments(self):
        raise NotImplementedError

    def test_solve(self):
        solver1 = SudokuSolver()
        sol = solver1.solve(self.sudoku1)
        self.assertEqual(sol, self.solution1)




if __name__ == '__main__':
    unittest.main()
