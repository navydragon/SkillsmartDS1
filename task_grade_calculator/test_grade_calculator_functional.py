"""
Тесты для функциональной версии калькулятора оценок.
Демонстрируют, что функциональный подход работает так же надежно,
как и императивный, но с дополнительными преимуществами.
"""

import unittest
from grade_calculator_functional import GradeList, calculate_average


class TestGradeListFunctional(unittest.TestCase):
    """Тесты для иммутабельного класса GradeList."""

    def test_empty_list_raises_error(self):
        """Тест: пустой список вызывает ошибку при создании."""
        with self.assertRaises(ValueError) as context:
            GradeList(())
        self.assertEqual(str(context.exception), "grades не может быть пустым списком")

    def test_single_grade_returns_itself(self):
        """Тест: среднее одного элемента равно самому элементу."""
        grade_list = GradeList((5.0,))
        self.assertEqual(grade_list.calculate_average(), 5.0)
        
        grade_list2 = GradeList((3.5,))
        self.assertEqual(grade_list2.calculate_average(), 3.5)

    def test_normal_case_different_grades(self):
        """Тест: типичный случай использования - разные оценки."""
        grade_list = GradeList((5.0, 4.5, 3.0, 4.0, 5.0))
        result = grade_list.calculate_average()
        expected = (5.0 + 4.5 + 3.0 + 4.0 + 5.0) / 5
        self.assertAlmostEqual(result, expected, places=2)

    def test_all_grades_equal(self):
        """Тест: все оценки одинаковые."""
        grade_list = GradeList((4.0, 4.0, 4.0, 4.0, 4.0))
        self.assertEqual(grade_list.calculate_average(), 4.0)
        
        grade_list2 = GradeList((5.0,) * 10)
        self.assertEqual(grade_list2.calculate_average(), 5.0)

    def test_non_positive_grades_raise_error(self):
        """Тест: оценки <= 0 вызывают ошибку."""
        with self.assertRaises(ValueError):
            GradeList((0.0, 5.0, 3.0))
        
        with self.assertRaises(ValueError):
            GradeList((-1.0, 5.0, 3.0))
        
        with self.assertRaises(ValueError):
            GradeList((5.0, 0.0, -1.0, 3.0))

    def test_invalid_types_raise_error(self):
        """Тест: нечисловые значения вызывают ошибку."""
        with self.assertRaises(TypeError):
            GradeList(("5", 4.0, 3.0))
        
        with self.assertRaises(TypeError):
            GradeList((5.0, "4.5", 3.0))

    def test_immutability(self):
        """Тест: объект иммутабелен - нельзя изменить после создания."""
        grade_list = GradeList((5.0, 4.5, 3.0))
        
        # Попытка изменить атрибут должна вызвать ошибку
        with self.assertRaises(Exception):  # dataclass frozen вызывает FrozenInstanceError
            grade_list.grades = (1.0, 2.0)

    def test_add_grade_creates_new_object(self):
        """Тест: добавление оценки создает новый объект."""
        original = GradeList((5.0, 4.5, 3.0))
        new = original.add_grade(4.0)
        
        # Проверяем, что это разные объекты
        self.assertIsNot(original, new)
        
        # Проверяем, что исходный объект не изменился
        self.assertEqual(len(original.grades), 3)
        self.assertEqual(len(new.grades), 4)
        
        # Проверяем, что новая оценка добавлена
        self.assertEqual(new.grades[-1], 4.0)

    def test_add_grade_validation(self):
        """Тест: валидация при добавлении оценки."""
        grade_list = GradeList((5.0, 4.5))
        
        with self.assertRaises(ValueError):
            grade_list.add_grade(0.0)
        
        with self.assertRaises(ValueError):
            grade_list.add_grade(-1.0)
        
        with self.assertRaises(TypeError):
            grade_list.add_grade("5.0")

    def test_add_grades_creates_new_object(self):
        """Тест: добавление нескольких оценок создает новый объект."""
        original = GradeList((5.0, 4.5))
        new = original.add_grades([3.0, 4.0, 5.0])
        
        self.assertIsNot(original, new)
        self.assertEqual(len(original.grades), 2)
        self.assertEqual(len(new.grades), 5)

    def test_chain_operations(self):
        """Тест: цепочка операций работает корректно."""
        result = (GradeList((5.0, 4.5))
                  .add_grade(3.0)
                  .add_grade(4.0)
                  .calculate_average())
        
        expected = (5.0 + 4.5 + 3.0 + 4.0) / 4
        self.assertAlmostEqual(result, expected, places=2)


class TestCalculateAverageFunction(unittest.TestCase):
    """Тесты для чистой функции calculate_average."""

    def test_empty_list_raises_error(self):
        """Тест: пустой список вызывает ошибку."""
        with self.assertRaises(ValueError) as context:
            calculate_average([])
        self.assertEqual(str(context.exception), "grades не может быть пустым списком")

    def test_single_grade_returns_itself(self):
        """Тест: среднее одного элемента равно самому элементу."""
        result = calculate_average([5.0])
        self.assertEqual(result, 5.0)

    def test_normal_case_different_grades(self):
        """Тест: типичный случай использования."""
        grades = [5.0, 4.5, 3.0, 4.0, 5.0]
        result = calculate_average(grades)
        expected = (5.0 + 4.5 + 3.0 + 4.0 + 5.0) / 5
        self.assertAlmostEqual(result, expected, places=2)

    def test_all_grades_equal(self):
        """Тест: все оценки одинаковые."""
        grades = [4.0, 4.0, 4.0, 4.0, 4.0]
        result = calculate_average(grades)
        self.assertEqual(result, 4.0)

    def test_non_positive_grades_raise_error(self):
        """Тест: оценки <= 0 вызывают ошибку."""
        with self.assertRaises(ValueError):
            calculate_average([0.0, 5.0, 3.0])
        
        with self.assertRaises(ValueError):
            calculate_average([-1.0, 5.0, 3.0])

    def test_none_raises_error(self):
        """Тест: None вызывает ошибку."""
        with self.assertRaises(ValueError) as context:
            calculate_average(None)
        self.assertEqual(str(context.exception), "grades не может быть None")

    def test_invalid_types_raise_error(self):
        """Тест: нечисловые значения вызывают ошибку."""
        with self.assertRaises(TypeError):
            calculate_average(["5", 4.0, 3.0])
        
        with self.assertRaises(TypeError):
            calculate_average([5.0, "4.5", 3.0])

    def test_pure_function_property(self):
        """Тест: функция чистая - одинаковые входные данные дают одинаковый результат."""
        grades = [5.0, 4.5, 3.0, 4.0, 5.0]
        result1 = calculate_average(grades)
        result2 = calculate_average(grades)
        result3 = calculate_average([5.0, 4.5, 3.0, 4.0, 5.0])
        
        # Все результаты должны быть одинаковыми
        self.assertEqual(result1, result2)
        self.assertEqual(result2, result3)
        
        # Входной список не должен измениться
        self.assertEqual(grades, [5.0, 4.5, 3.0, 4.0, 5.0])


if __name__ == '__main__':
    unittest.main()



