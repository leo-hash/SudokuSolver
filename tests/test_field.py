import unittest

from src.field import Field


class TestField(unittest.TestCase):

    def setUp(self):
        self.field1 = Field()
        self.field2 = Field()
        self.field3 = Field()

        self.field1.delete_posibile(1)
        self.field1.delete_posibile(3)
        self.field1.delete_posibile(5)
        self.field1.delete_posibile(7)
        self.field1.delete_posibile(9)

        self.field2.delete_posibile(2)
        self.field2.delete_posibile(4)
        self.field2.delete_posibile(6)
        self.field2.delete_posibile(8)

    def test_is_posibile(self):
        self.assertFalse(self.field1.is_posibile(1))
        self.assertFalse(self.field1.is_posibile(3))
        self.assertFalse(self.field1.is_posibile(5))
        self.assertFalse(self.field1.is_posibile(7))
        self.assertFalse(self.field1.is_posibile(9))

        self.assertTrue(self.field1.is_posibile(2))
        self.assertTrue(self.field1.is_posibile(4))
        self.assertTrue(self.field1.is_posibile(6))
        self.assertTrue(self.field1.is_posibile(8))

        self.assertTrue(self.field2.is_posibile(1))
        self.assertTrue(self.field2.is_posibile(3))
        self.assertTrue(self.field2.is_posibile(5))
        self.assertTrue(self.field2.is_posibile(7))
        self.assertTrue(self.field2.is_posibile(9))

        self.assertFalse(self.field2.is_posibile(2))
        self.assertFalse(self.field2.is_posibile(4))
        self.assertFalse(self.field2.is_posibile(6))
        self.assertFalse(self.field2.is_posibile(8))

        with self.assertRaises(ValueError):
            self.field3.is_posibile(0)

        with self.assertRaises(ValueError):
            self.field3.is_posibile(10)

    def test_delete_possible(self):
        for i in range(1, 10):
            self.assertTrue(self.field3.is_posibile(i))
            self.field3.delete_posibile(i)
            self.assertFalse(self.field3.is_posibile(i))

        with self.assertRaises(ValueError):
            self.field3.delete_posibile(0)

        with self.assertRaises(ValueError):
            self.field3.delete_posibile(10)


    def test_set_number(self):
        with self.assertRaises(ValueError):
            self.field3.number = 0
        with self.assertRaises(ValueError):
            self.field3.number = 10

        self.field3.number = 1
        self.assertEqual(self.field3.number, 1)

        with self.assertRaises(ValueError):
            self.field1.number = 1

        self.field1.number = 2
        self.assertEqual(self.field1.number, 2)

        with self.assertRaises(ValueError):
            self.field2.number = 2

        self.field2.number = 3
        self.assertEqual(self.field2.number, 3)

    def test_set_pos_number(self):
        raise NotImplementedError()

if __name__ == '__main__':
    unittest.main()
