"""
Улучшенный пример работы с датой и временем
Демонстрирует правильный подход к парсингу и работе с датами.

Это решение исправляет все недостатки проблемного кода.
"""

from datetime import datetime, timezone, timedelta
from typing import Optional, List
import re


class DateParseError(Exception):
    """Исключение для ошибок парсинга дат"""
    pass


class DateParser:
    """
    Класс для безопасного парсинга дат с явным указанием часового пояса.
    
    Решает проблемы наивного подхода:
    1. Явное указание часового пояса
    2. Валидация входных данных
    3. Обработка ошибок
    4. Поддержка различных форматов
    5. Учет переходов на летнее/зимнее время
    """
    
    # Поддерживаемые форматы дат
    SUPPORTED_FORMATS = [
        "%Y-%m-%d %H:%M:%S",      # 2024-05-13 14:30:00
        "%Y-%m-%d %H:%M",         # 2024-05-13 14:30
        "%Y-%m-%d",               # 2024-05-13
        "%d.%m.%Y %H:%M:%S",      # 13.05.2024 14:30:00
        "%d.%m.%Y %H:%M",         # 13.05.2024 14:30
        "%d.%m.%Y",               # 13.05.2024
        "%Y/%m/%d %H:%M:%S",      # 2024/05/13 14:30:00
        "%Y/%m/%d %H:%M",         # 2024/05/13 14:30
        "%Y/%m/%d",               # 2024/05/13
    ]
    
    def __init__(self, default_timezone: timezone = timezone.utc):
        """
        Инициализация парсера.
        
        Args:
            default_timezone: Часовой пояс по умолчанию (по умолчанию UTC)
        """
        self.default_timezone = default_timezone
    
    def validate_input(self, date_string: str) -> None:
        """
        Валидация входной строки.
        
        Args:
            date_string: Строка для валидации
        
        Raises:
            DateParseError: Если строка некорректна
        """
        if not date_string:
            raise DateParseError("Пустая строка не может быть датой")
        
        if not isinstance(date_string, str):
            raise DateParseError(f"Ожидается строка, получен {type(date_string)}")
        
        # Проверка на слишком длинную строку (защита от DoS)
        if len(date_string) > 100:
            raise DateParseError("Строка даты слишком длинная")
    
    def parse(
        self,
        date_string: str,
        timezone_info: Optional[timezone] = None,
        formats: Optional[List[str]] = None
    ) -> datetime:
        """
        Парсинг даты с явным указанием часового пояса.
        
        Args:
            date_string: Строка с датой
            timezone_info: Часовой пояс (если None, используется default_timezone)
            formats: Список форматов для попытки парсинга (если None, используются SUPPORTED_FORMATS)
        
        Returns:
            Объект datetime с указанным часовым поясом
        
        Raises:
            DateParseError: Если парсинг не удался
        """
        # Валидация входных данных
        self.validate_input(date_string)
        
        # Определение часового пояса
        tz = timezone_info if timezone_info is not None else self.default_timezone
        
        # Определение форматов для попытки
        formats_to_try = formats if formats is not None else self.SUPPORTED_FORMATS
        
        # Попытка парсинга с каждым форматом
        last_error = None
        for fmt in formats_to_try:
            try:
                # Парсинг без часового пояса
                naive_dt = datetime.strptime(date_string.strip(), fmt)
                # Добавление часового пояса
                aware_dt = naive_dt.replace(tzinfo=tz)
                return aware_dt
            except ValueError as e:
                last_error = e
                continue
        
        # Если ни один формат не подошел
        raise DateParseError(
            f"Не удалось распарсить дату '{date_string}'. "
            f"Поддерживаемые форматы: {', '.join(formats_to_try[:3])}... "
            f"Последняя ошибка: {last_error}"
        )
    
    def parse_utc(self, date_string: str) -> datetime:
        """
        Парсинг даты с явным указанием UTC.
        
        Args:
            date_string: Строка с датой
        
        Returns:
            Объект datetime в UTC
        """
        return self.parse(date_string, timezone.utc)
    
    def parse_local(
        self,
        date_string: str,
        timezone_offset_hours: int
    ) -> datetime:
        """
        Парсинг даты с указанием смещения от UTC в часах.
        
        Args:
            date_string: Строка с датой
            timezone_offset_hours: Смещение от UTC в часах (например, 3 для MSK)
        
        Returns:
            Объект datetime с указанным смещением
        """
        tz = timezone(timedelta(hours=timezone_offset_hours))
        return self.parse(date_string, tz)
    
    @staticmethod
    def convert_timezone(
        dt: datetime,
        target_timezone: timezone
    ) -> datetime:
        """
        Конвертация datetime в другой часовой пояс.
        
        Args:
            dt: Исходный datetime (должен быть aware)
            target_timezone: Целевой часовой пояс
        
        Returns:
            datetime в целевом часовом поясе
        
        Raises:
            ValueError: Если исходный datetime не имеет информации о часовом поясе
        """
        if dt.tzinfo is None:
            raise ValueError(
                "Исходный datetime не имеет информации о часовом поясе. "
                "Используйте parse() вместо strptime()"
            )
        
        return dt.astimezone(target_timezone)
    
    @staticmethod
    def to_utc(dt: datetime) -> datetime:
        """
        Конвертация datetime в UTC.
        
        Args:
            dt: Исходный datetime
        
        Returns:
            datetime в UTC
        """
        if dt.tzinfo is None:
            raise ValueError("Исходный datetime не имеет информации о часовом поясе")
        
        return dt.astimezone(timezone.utc)
    
    @staticmethod
    def format_for_storage(dt: datetime) -> str:
        """
        Форматирование datetime для хранения в БД (всегда в UTC, ISO формат).
        
        Args:
            dt: datetime для форматирования
        
        Returns:
            Строка в формате ISO 8601 с указанием UTC
        """
        if dt.tzinfo is None:
            raise ValueError("datetime должен иметь информацию о часовом поясе")
        
        # Конвертация в UTC
        utc_dt = dt.astimezone(timezone.utc)
        # Форматирование в ISO 8601
        return utc_dt.isoformat()


def demonstrate_improvements():
    """
    Демонстрация улучшенного подхода к работе с датами.
    """
    print("=" * 70)
    print("УЛУЧШЕННОЕ РЕШЕНИЕ: Правильная работа с датами")
    print("=" * 70)
    
    parser = DateParser(default_timezone=timezone.utc)
    
    # Пример 1: Парсинг с явным указанием UTC
    print("\n1. Парсинг с явным указанием UTC:")
    date_string = "2024-05-13 14:30:00"
    date_utc = parser.parse_utc(date_string)
    print(f"   Входная строка: {date_string}")
    print(f"   Результат: {date_utc}")
    print(f"   Часовой пояс: {date_utc.tzinfo}")

    
    # Пример 2: Парсинг с указанием локального часового пояса (MSK, UTC+3)
    print("\n2. Парсинг с указанием локального часового пояса (MSK, UTC+3):")
    date_msk = parser.parse_local(date_string, timezone_offset_hours=3)
    print(f"   Входная строка: {date_string}")
    print(f"   Результат (MSK): {date_msk}")
    print(f"   Часовой пояс: {date_msk.tzinfo}")
    
    # Пример 3: Конвертация между часовыми поясами
    print("\n3. Конвертация между часовыми поясами:")
    print(f"   Исходная дата (MSK): {date_msk}")
    date_utc_converted = parser.to_utc(date_msk)
    print(f"   Конвертировано в UTC: {date_utc_converted}")
    print(f"   Разница: {date_msk.hour - date_utc_converted.hour} часа")

    
    # Пример 4: Валидация входных данных
    print("\n4. Валидация входных данных:")
    invalid_inputs = [
        ("", "Пустая строка"),
        ("2024-13-45 25:70:99", "Некорректные значения"),
        ("not a date", "Не дата"),
    ]
    
    for invalid_str, description in invalid_inputs:
        try:
            result = parser.parse(invalid_str)
            print(f"   '{invalid_str}' ({description}) -> {result}")
        except DateParseError as e:
            print(f"   '{invalid_str}' ({description}) -> DateParseError: {e}")

    
    # Пример 5: Поддержка различных форматов
    print("\n5. Поддержка различных форматов:")
    different_formats = [
        "2024-05-13 14:30:00",
        "13.05.2024 14:30:00",
        "2024/05/13 14:30",
        "2024-05-13",
    ]
    
    for fmt_str in different_formats:
        try:
            result = parser.parse(fmt_str)
            print(f"   '{fmt_str}' -> {result}")
        except DateParseError as e:
            print(f"   '{fmt_str}' -> Ошибка: {e}")
    
    # Пример 6: Форматирование для хранения в БД
    print("\n6. Форматирование для хранения в БД (всегда UTC, ISO формат):")
    local_date = parser.parse_local("2024-05-13 14:30:00", 3)  # MSK
    storage_format = parser.format_for_storage(local_date)
    print(f"   Локальная дата (MSK): {local_date}")
    print(f"   Формат для БД: {storage_format}")
    
    # Пример 7: Сравнение дат с разными часовыми поясами
    print("\n7. Сравнение дат с разными часовыми поясами:")
    date1_utc = parser.parse_utc("2024-05-13 14:30:00")
    date2_msk = parser.parse_local("2024-05-13 17:30:00", 3)  # Та же дата в MSK
    print(f"   UTC: {date1_utc}")
    print(f"   MSK: {date2_msk}")
    
    # Конвертируем обе в UTC для сравнения
    date1_utc_normalized = parser.to_utc(date1_utc)
    date2_utc_normalized = parser.to_utc(date2_msk)
    
    if date1_utc_normalized == date2_utc_normalized:
        print("   ✓ Даты одинаковые (разные часовые пояса, но одно и то же время)!")
    else:
        diff = abs((date1_utc_normalized - date2_utc_normalized).total_seconds())
        print(f"   Разница: {diff} секунд")
    
    # Пример 8: Работа с текущим временем
    print("\n8. Работа с текущим временем:")
    now_utc = datetime.now(timezone.utc)
    now_local = datetime.now().astimezone()  # Системный часовой пояс
    print(f"   Текущее время (UTC): {now_utc}")
    print(f"   Текущее время (локальное): {now_local}")


def demonstrate_dst_issues():
    """
    Демонстрация проблем с переходом на летнее/зимнее время.
    Примечание: В России DST отменен, но пример показывает концепцию.
    """
    print("\n" + "=" * 70)
    print("ПРИМЕЧАНИЕ О ПЕРЕХОДАХ НА ЛЕТНЕЕ/ЗИМНЕЕ ВРЕМЯ (DST)")
    print("=" * 70)
    print("В России переход на летнее/зимнее время отменен с 2014 года.")
    print("Однако в других странах (США, Европа) эти переходы существуют.")
    print("\nПроблемы, которые могут возникнуть:")
    print("1. Неоднозначность: одно время может быть в двух часовых поясах")
    print("2. Пропуск времени: при переходе на летнее время час пропускается")
    print("3. Повторение времени: при переходе на зимнее время час повторяется")
    print("\nРешение: Всегда используйте UTC для внутреннего хранения,")
    print("и конвертируйте в локальный часовой пояс только для отображения.")


def main():
    """Главная функция для демонстрации улучшенного решения"""

    demonstrate_improvements()
    demonstrate_dst_issues()
    


if __name__ == "__main__":
    main()
