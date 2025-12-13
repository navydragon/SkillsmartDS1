import unittest
from grade_calculator import GradeCalculator


class TestGradeCalculator(unittest.TestCase):
    """Тесты для класса GradeCalculator."""

    def setUp(self):
        """Инициализация тестового объекта перед каждым тестом."""
        self.calculator = GradeCalculator()

    def test_empty_list_raises_error(self):
        """
        Тест 1: Граничный случай - пустой список.
        Проверяет, что метод правильно обрабатывает отсутствие данных
        и выбрасывает ValueError.
        """
        with self.assertRaises(ValueError) as context:
            self.calculator.calculateAverage([])
        self.assertEqual(str(context.exception), "grades не может быть пустым списком")

    def test_single_grade_returns_itself(self):
        """
        Тест 2: Граничный случай - один элемент в списке.
        Проверяет поведение при минимальном наборе данных (один элемент).
        Среднее одного элемента должно равняться самому элементу.
        """
        result = self.calculator.calculateAverage([5.0])
        self.assertEqual(result, 5.0)
        
        result2 = self.calculator.calculateAverage([3.5])
        self.assertEqual(result2, 3.5)

    def test_normal_case_different_grades(self):
        """
        Тест 3: Типичный случай использования - разные оценки.
        Проверяет корректность вычисления среднего для разнообразных оценок.
        Это основной сценарий использования метода.
        """
        grades = [5.0, 4.5, 3.0, 4.0, 5.0]
        result = self.calculator.calculateAverage(grades)
        expected = (5.0 + 4.5 + 3.0 + 4.0 + 5.0) / 5
        self.assertAlmostEqual(result, expected, places=2)

    def test_all_grades_equal(self):
        """
        Тест 4: Особый случай данных - все оценки одинаковые.
        Проверяет, что когда все элементы одинаковые, среднее равно этому значению.
        Это проверка корректности работы алгоритма в специфическом случае.
        """
        grades = [4.0, 4.0, 4.0, 4.0, 4.0]
        result = self.calculator.calculateAverage(grades)
        self.assertEqual(result, 4.0)
        
        grades2 = [5.0] * 10
        result2 = self.calculator.calculateAverage(grades2)
        self.assertEqual(result2, 5.0)

    def test_extreme_values_and_zero(self):
        """
        Тест 5: Граничные значения - нули и большие числа.
        Проверяет корректность работы с экстремальными значениями:
        нули должны вызывать ошибку, большие числа обрабатываются корректно.
        Это проверка устойчивости алгоритма к крайним входным данным.
        """
        # Тест с нулями - должна быть ошибка
        with self.assertRaises(ValueError) as context:
            self.calculator.calculateAverage([0.0, 5.0, 0.0, 3.0])
        self.assertIn("должны быть больше 0", str(context.exception))
        
        # Тест с отрицательными числами - должна быть ошибка
        with self.assertRaises(ValueError) as context:
            self.calculator.calculateAverage([-1.0, 5.0, 3.0])
        self.assertIn("должны быть больше 0", str(context.exception))
        
        # Тест с большими числами - должно работать корректно
        grades_large = [1000000.0, 2000000.0, 3000000.0]
        result2 = self.calculator.calculateAverage(grades_large)
        expected2 = (1000000.0 + 2000000.0 + 3000000.0) / 3
        self.assertAlmostEqual(result2, expected2, places=2)
        
        # Тест с оценкой равной 0 - должна быть ошибка
        with self.assertRaises(ValueError):
            self.calculator.calculateAverage([0.0])
    
    def test_non_positive_grades_raise_error(self):
        """
        Тест: Проверка, что оценки <= 0 вызывают ошибку.
        Проверяет, что метод корректно обрабатывает недопустимые значения оценок:
        нули, отрицательные числа, граничное значение 0.
        """
        # Тест с нулем
        with self.assertRaises(ValueError) as context:
            self.calculator.calculateAverage([0.0])
        self.assertIn("должны быть больше 0", str(context.exception))
        
        # Тест с отрицательным числом
        with self.assertRaises(ValueError) as context:
            self.calculator.calculateAverage([-5.0, 4.0, 3.0])
        self.assertIn("должны быть больше 0", str(context.exception))
        
        # Тест с несколькими неположительными значениями
        with self.assertRaises(ValueError):
            self.calculator.calculateAverage([5.0, 0.0, -1.0, 3.0])
        
        # Тест с очень маленьким положительным числом - должно работать
        result = self.calculator.calculateAverage([0.0001, 5.0, 3.0])
        self.assertGreater(result, 0)

    def test_none_raises_error(self):
        """Дополнительный тест: проверка обработки None."""
        with self.assertRaises(ValueError) as context:
            self.calculator.calculateAverage(None)
        self.assertEqual(str(context.exception), "grades не может быть None")

    def test_invalid_types_raise_error(self):
        """Дополнительный тест: проверка обработки нечисловых значений."""
        with self.assertRaises(TypeError):
            self.calculator.calculateAverage(["5", 4.0, 3.0])
        
        with self.assertRaises(TypeError):
            self.calculator.calculateAverage([5.0, "4.5", 3.0])


if __name__ == '__main__':
    unittest.main()

