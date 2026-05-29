import unittest

from src.grid import SudokuGrid


class TestGrid(unittest.TestCase):

    def setUp(self):
        self.grid1 = SudokuGrid()
        self.grid2 = SudokuGrid()

    def test_set_new_values(self):
        raise NotImplementedError()

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

if __name__ == '__main__':
    unittest.main()
