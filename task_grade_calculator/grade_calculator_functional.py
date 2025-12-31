"""
Функциональная версия калькулятора оценок.
Демонстрация принципов функционального программирования:
- Иммутабельные структуры данных
- Чистые функции без побочных эффектов
- Каждое изменение создает новый объект
"""

from dataclasses import dataclass
from typing import List, Tuple


# ============================================================================
# Чистые функции валидации (без побочных эффектов)
# ============================================================================

def validate_not_none(grades: List[float]) -> None:
    """Чистая функция: проверяет, что grades не равен None."""
    if grades is None:
        raise ValueError("grades не может быть None")


def validate_not_empty(grades: List[float]) -> None:
    """Чистая функция: проверяет, что grades не является пустым списком."""
    if len(grades) == 0:
        raise ValueError("grades не может быть пустым списком")


def validate_types(grades: List[float]) -> None:
    """Чистая функция: проверяет, что все элементы в grades являются числами."""
    for grade in grades:
        if not isinstance(grade, (int, float)):
            raise TypeError(f"Все оценки должны быть числами, получено: {type(grade)}")


def validate_positive(grades: List[float]) -> None:
    """Чистая функция: проверяет, что все оценки больше 0."""
    for grade in grades:
        if grade <= 0:
            raise ValueError(f"Все оценки должны быть больше 0, получено: {grade}")


def validate_all(grades: List[float]) -> None:
    """
    Чистая функция: выполняет все проверки валидности оценок.
    Не изменяет входные данные, только проверяет их.
    """
    validate_not_none(grades)
    validate_not_empty(grades)
    validate_types(grades)
    validate_positive(grades)


# ============================================================================
# Иммутабельный класс GradeList
# ============================================================================

@dataclass(frozen=True)
class GradeList:
    """
    Иммутабельный класс, представляющий список оценок.
    
    Атрибуты:
        grades: Кортеж оценок (используется tuple для иммутабельности)
    
    Свойства:
        - Класс финализирован (frozen=True) - нельзя изменять после создания
        - Поле grades - кортеж (tuple), который является иммутабельным типом
        - Все методы возвращают новые объекты вместо изменения текущего
    """
    grades: Tuple[float, ...]
    
    def __post_init__(self):
        """Валидация при создании объекта."""
        # Преобразуем в список для валидации, так как tuple иммутабелен
        validate_all(list(self.grades))
    
    def calculate_average(self) -> float:
        """
        Чистая функция: вычисляет среднее значение оценок.
        
        Returns:
            Среднее арифметическое значение оценок
        
        Raises:
            ValueError: Если grades равен None, пуст или содержит оценки <= 0
            TypeError: Если grades содержит нечисловые значения
        """
        if len(self.grades) == 0:
            raise ValueError("grades не может быть пустым списком")
        
        total = sum(self.grades)
        return total / len(self.grades)
    
    def add_grade(self, grade: float) -> 'GradeList':
        """
        Чистая функция: добавляет оценку, создавая новый объект.
        
        Вместо изменения текущего объекта, создается новый объект
        с добавленной оценкой. Это соответствует принципу иммутабельности.
        
        Args:
            grade: Оценка для добавления
            
        Returns:
            Новый объект GradeList с добавленной оценкой
            
        Raises:
            ValueError: Если grade <= 0
            TypeError: Если grade не является числом
        """
        # Валидация новой оценки
        if not isinstance(grade, (int, float)):
            raise TypeError(f"Оценка должна быть числом, получено: {type(grade)}")
        if grade <= 0:
            raise ValueError(f"Оценка должна быть больше 0, получено: {grade}")
        
        # Создаем новый кортеж с добавленной оценкой
        new_grades = self.grades + (float(grade),)
        return GradeList(new_grades)
    
    def add_grades(self, new_grades: List[float]) -> 'GradeList':
        """
        Чистая функция: добавляет несколько оценок, создавая новый объект.
        
        Args:
            new_grades: Список оценок для добавления
            
        Returns:
            Новый объект GradeList с добавленными оценками
        """
        # Валидация новых оценок
        validate_all(new_grades)
        
        # Создаем новый кортеж с добавленными оценками
        new_grades_tuple = tuple(float(g) for g in new_grades)
        return GradeList(self.grades + new_grades_tuple)
    
    def __str__(self) -> str:
        """Строковое представление объекта."""
        return f"GradeList(grades={self.grades}, average={self.calculate_average():.2f})"
    
    def __repr__(self) -> str:
        """Представление объекта для отладки."""
        return f"GradeList(grades={self.grades})"


# ============================================================================
# Функция для обратной совместимости с оригинальным API
# ============================================================================

def calculate_average(grades: List[float]) -> float:
    """
    Чистая функция для вычисления среднего значения оценок.
    Предоставляет функциональный интерфейс без создания объекта.
    
    Args:
        grades: Список оценок студентов
        
    Returns:
        Среднее арифметическое значение оценок
        
    Raises:
        ValueError: Если grades равен None, пуст или содержит оценки <= 0
        TypeError: Если grades содержит нечисловые значения
    """
    validate_all(grades)
    total = sum(grades)
    return total / len(grades)


# ============================================================================
# Пример использования
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Демонстрация функционального подхода")
    print("=" * 60)
    
    # Создание иммутабельного объекта
    print("\n1. Создание начального списка оценок:")
    grade_list = GradeList((5.0, 4.5, 3.0, 4.0, 5.0))
    print(f"   {grade_list}")
    
    # Добавление оценки создает новый объект
    print("\n2. Добавление новой оценки (создается новый объект):")
    new_grade_list = grade_list.add_grade(4.5)
    print(f"   Старый объект: {grade_list}")
    print(f"   Новый объект:  {new_grade_list}")
    print(f"   Объекты разные: {grade_list is not new_grade_list}")
    
    # Добавление нескольких оценок
    print("\n3. Добавление нескольких оценок:")
    final_grade_list = new_grade_list.add_grades([3.5, 5.0])
    print(f"   Финальный объект: {final_grade_list}")
    
    # Использование чистой функции
    print("\n4. Использование чистой функции calculate_average:")
    grades = [5.0, 4.5, 3.0, 4.0, 5.0]
    average = calculate_average(grades)
    print(f"   Оценки: {grades}")
    print(f"   Среднее: {average:.2f}")
    
    print("\n" + "=" * 60)
    print("Преимущества функционального подхода:")
    print("- Иммутабельность: объекты нельзя изменить после создания")
    print("- Чистые функции: нет побочных эффектов")
    print("- Безопасность: легко тестировать и использовать в многопоточности")
    print("- Предсказуемость: одинаковые входные данные = одинаковый результат")
    print("=" * 60)

