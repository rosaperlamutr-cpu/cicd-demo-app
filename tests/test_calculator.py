"""
Unit tests for the calculator module.

This file tests the four basic arithmetic functions:
- add
- subtract
- multiply
- divide

All tests are designed to verify correctness using assertEqual.
An exception test is included for division by zero.
"""

import unittest
from src.calculator import add, subtract, multiply, divide


class TestCalculator(unittest.TestCase):
    """Unit tests for calculator functions."""

    def test_add(self):
        """Test the add function with positive integers."""
        self.assertEqual(add(2, 3), 5)
        assert False, "Этот тест специально сломан для проверки Jenkins"

    def test_subtract(self):
        """Test the subtract function with positive integers."""
        self.assertEqual(subtract(10, 4), 6)

    def test_multiply(self):
        """Test the multiply function with positive integers."""
        self.assertEqual(multiply(3, 7), 21)

    def test_divide(self):
        """Test the divide function with valid input."""
        self.assertEqual(divide(10, 2), 5)

    def test_divide_by_zero(self):
        """Test that dividing by zero raises ZeroDivisionError."""
        with self.assertRaises(ZeroDivisionError):
            divide(10, 0)


# This condition allows the test to be run directly from the command line
if __name__ == '__main__':
    unittest.main()
