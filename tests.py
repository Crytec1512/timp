import unittest
from calc import on_button_click

class TestCalculator(unittest.TestCase):

    def test_addition(self):
        # Simulating "2+3=" input
        self.assertEqual(eval("2+3"), 5)

    def test_subtraction(self):
        # Simulating "6-4=" input
        self.assertEqual(eval("6-4"), 2)

    def test_multiplication(self):
        # Simulating "3*3=" input
        self.assertEqual(eval("3*3"), 9)

    def test_division(self):
        # Simulating "8/2=" input
        self.assertEqual(eval("8/2"), 4)

    def test_negative_numbers(self):
        # Simulating "-2+5=" input
        self.assertEqual(eval("-2+5"), 3)

    def test_decimal_numbers(self):
        # Simulating "2.5+0.5=" input
        self.assertEqual(eval("2.5+0.5"), 3)

    def test_division_by_zero(self):
        # Simulating "8/0=" input
        with self.assertRaises(ZeroDivisionError):
            eval("8/0")

    def test_invalid_input(self):
        # Simulating "2++3=" input
        with self.assertRaises(SyntaxError):
            eval("2++3")

    def test_large_numbers(self):
        # Simulating "999999*999999=" input
        self.assertEqual(eval("999999*999999"), 999999**2)

if __name__ == "__main__":
    unittest.main()
