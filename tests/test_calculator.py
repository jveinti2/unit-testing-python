import unittest # Sirve para hacer pruebas unitarias

from src.calculator import sum, subtract, multiply, divide

class CalculatorTests(unittest.TestCase):
    def test_sum(self):
        assert sum(2, 3) == 5

    def test_subtraction(self):
        assert subtract(10, 5) == 5

    def test_multiplication(self):
        assert multiply(3, 7) == 21

    def test_division(self):
        result = divide(10, 2)
        excepted = 5
        assert result == excepted

    def test_division_by_zero(self):
        with self.assertRaises(ValueError):
            divide(10, 0)        

        

