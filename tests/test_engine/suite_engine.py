import unittest

from tests.test_engine.test_grid import TestGrid
from tests.test_engine.test_field import TestField
from tests.test_engine.test_solver import TestSolver
from tests.test_engine.test_generator import TestGenerator



def suite() -> unittest.TestSuite:
    loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()

    test_suite.addTests(loader.loadTestsFromTestCase(TestGrid))
    test_suite.addTests(loader.loadTestsFromTestCase(TestField))
    test_suite.addTests(loader.loadTestsFromTestCase(TestSolver))
    test_suite.addTests(loader.loadTestsFromTestCase(TestGenerator))
    return test_suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())