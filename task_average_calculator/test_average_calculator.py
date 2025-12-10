import unittest

from average_calculator import AverageCalculator


class TestAverageCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = AverageCalculator()

    def test_calculates_average_of_positive_numbers(self):
        self.assertAlmostEqual(self.calc.calculate_average([2, 4, 6]), 4.0)

    def test_handles_negative_numbers(self):
        self.assertAlmostEqual(self.calc.calculate_average([-3, -1, -2]), -2.0)

    def test_single_element_list(self):
        self.assertAlmostEqual(self.calc.calculate_average([10]), 10.0)

    def test_includes_zero_values(self):
        self.assertAlmostEqual(self.calc.calculate_average([0, 0, 10, 20]), 7.5)

    def test_raises_for_empty_list(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_average([])

    def test_raises_for_none_input(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_average(None)  # type: ignore[arg-type]


class BuggyAverageCalculator:
    """Намеренно содержит баг, чтобы показать риск неполного покрытия."""

    def calculate_average(self, numbers: list[int]) -> float:
        if not numbers:
            return 0  # молчаещее поведение, которого не ожидают
        # Ошибка: целочисленное деление отбрасывает дробную часть.
        return sum(numbers) // len(numbers)


class TestCoverageGapDemo(unittest.TestCase):
    """
    Демонстрация: узкое покрытие не ловит дефекты.

    Первые тесты используют «красивые» данные, где деление без остатка,
    поэтому баг не проявляется. Последний тест показывает, что при
    расширении сценариев ошибка сразу всплывает.
    """

    def test_minimal_cases_pass_even_with_bug(self):
        calc = BuggyAverageCalculator()
        self.assertEqual(calc.calculate_average([2, 4]), 3)  # 6 // 2 == 3
        self.assertEqual(calc.calculate_average([6, 0, 3, 3]), 3)  # 12 // 4 == 3

    @unittest.expectedFailure
    def test_uncovered_case_reveals_bug(self):
        calc = BuggyAverageCalculator()
        # Ожидается 1.5, но из-за целочисленного деления получится 1.
        self.assertAlmostEqual(calc.calculate_average([1, 2]), 1.5)


if __name__ == "__main__":
    unittest.main()

