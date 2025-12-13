from typing import List


class GradeCalculator:
    """Класс для вычисления среднего значения оценок студентов."""

    def _validate_not_none(self, grades: List[float]) -> None:
        """Проверяет, что grades не равен None."""
        if grades is None:
            raise ValueError("grades не может быть None")

    def _validate_not_empty(self, grades: List[float]) -> None:
        """Проверяет, что grades не является пустым списком."""
        if len(grades) == 0:
            raise ValueError("grades не может быть пустым списком")

    def _validate_types(self, grades: List[float]) -> None:
        """Проверяет, что все элементы в grades являются числами."""
        for grade in grades:
            if not isinstance(grade, (int, float)):
                raise TypeError(f"Все оценки должны быть числами, получено: {type(grade)}")

    def _validate_positive(self, grades: List[float]) -> None:
        """Проверяет, что все оценки больше 0."""
        for grade in grades:
            if grade <= 0:
                raise ValueError(f"Все оценки должны быть больше 0, получено: {grade}")

    def _validate(self, grades: List[float]) -> None:
        """Выполняет все проверки валидности оценок."""
        self._validate_not_none(grades)
        self._validate_not_empty(grades)
        self._validate_types(grades)
        self._validate_positive(grades)

    def calculateAverage(self, grades: List[float]) -> float:
        """
        Вычисляет среднее значение оценок студентов.
        
        Args:
            grades: Список оценок студентов
            
        Returns:
            Среднее арифметическое значение оценок
            
        Raises:
            ValueError: Если grades равен None, пуст или содержит оценки <= 0
            TypeError: Если grades содержит нечисловые значения
        """
        self._validate(grades)
        
        # Вычисление суммы и среднего
        total = sum(grades)
        average = total / len(grades)
        
        return average

