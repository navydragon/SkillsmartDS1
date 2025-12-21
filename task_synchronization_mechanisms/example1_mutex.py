"""
Пример 1: Мьютексы (Lock)
Демонстрация использования threading.Lock для защиты общего ресурса от состояния гонки.

Пример: потокобезопасный счетчик посещений веб-сайта
"""

import threading
import time
from typing import List


class VisitCounter:
    """
    Класс счетчика посещений с потокобезопасным доступом.
    Демонстрирует использование мьютекса для защиты общего ресурса.
    """
    
    def __init__(self):
        """Инициализация счетчика с блокировкой"""
        self._count = 0
        self._lock = threading.Lock()  # Мьютекс для синхронизации
    
    def increment(self) -> int:
        """
        Потокобезопасное увеличение счетчика на 1.
        
        Returns:
            Новое значение счетчика
        """
        with self._lock:  # Автоматическое получение и освобождение блокировки
            self._count += 1
            return self._count
    
    def get_count(self) -> int:
        """
        Получение текущего значения счетчика.
        
        Returns:
            Текущее значение счетчика
        """
        with self._lock:
            return self._count


class UnsafeCounter:
    """
    НЕПРАВИЛЬНАЯ реализация счетчика БЕЗ синхронизации.
    Демонстрирует проблему состояния гонки (race condition).
    """
    
    def __init__(self):
        """Инициализация счетчика без блокировки"""
        self._count = 0
    
    def increment(self) -> int:
        """
        НЕПОТОКОБЕЗОПАСНОЕ увеличение счетчика.
        Может привести к потере данных при одновременном доступе.
        """
        # Операция не атомарна: чтение -> увеличение -> запись
        # Между этими операциями другие потоки могут вмешаться
        self._count += 1
        return self._count
    
    def get_count(self) -> int:
        """Получение текущего значения счетчика"""
        return self._count


def worker_safe(counter: VisitCounter, worker_id: int, iterations: int) -> None:
    """
    Рабочая функция для потокобезопасного счетчика.
    
    Args:
        counter: Потокобезопасный счетчик
        worker_id: Идентификатор потока
        iterations: Количество итераций инкремента
    """
    for i in range(iterations):
        new_value = counter.increment()
        print(f"Поток {worker_id}: инкремент #{i+1}, новое значение = {new_value}")
        time.sleep(0.01)  # Имитация работы


def worker_unsafe(counter: UnsafeCounter, worker_id: int, iterations: int) -> None:
    """
    Рабочая функция для НЕПОТОКОБЕЗОПАСНОГО счетчика.
    
    Args:
        counter: Непотокобезопасный счетчик
        worker_id: Идентификатор потока
        iterations: Количество итераций инкремента
    """
    for i in range(iterations):
        new_value = counter.increment()
        print(f"Поток {worker_id}: инкремент #{i+1}, новое значение = {new_value}")
        time.sleep(0.01)  # Имитация работы


def demonstrate_unsafe_counter():
    """
    Демонстрация проблемы состояния гонки без синхронизации.
    """
    print("=" * 60)
    print("ДЕМОНСТРАЦИЯ ПРОБЛЕМЫ: Счетчик БЕЗ синхронизации")
    print("=" * 60)
    
    counter = UnsafeCounter()
    threads: List[threading.Thread] = []
    num_threads = 5
    iterations_per_thread = 10
    
    # Создаем и запускаем потоки
    for i in range(num_threads):
        thread = threading.Thread(
            target=worker_unsafe,
            args=(counter, i + 1, iterations_per_thread)
        )
        threads.append(thread)
        thread.start()
    
    # Ждем завершения всех потоков
    for thread in threads:
        thread.join()
    
    expected_value = num_threads * iterations_per_thread
    actual_value = counter.get_count()
    
    print(f"\nОжидаемое значение: {expected_value}")
    print(f"Фактическое значение: {actual_value}")
    print(f"Потеря данных: {expected_value - actual_value}")
    print("Проблема: несколько потоков одновременно изменяли счетчик без синхронизации!")


def demonstrate_safe_counter():
    """
    Демонстрация правильного решения с использованием мьютекса.
    """
    print("\n" + "=" * 60)
    print("ПРАВИЛЬНОЕ РЕШЕНИЕ: Счетчик С синхронизацией (Lock)")
    print("=" * 60)
    
    counter = VisitCounter()
    threads: List[threading.Thread] = []
    num_threads = 5
    iterations_per_thread = 10
    
    # Создаем и запускаем потоки
    for i in range(num_threads):
        thread = threading.Thread(
            target=worker_safe,
            args=(counter, i + 1, iterations_per_thread)
        )
        threads.append(thread)
        thread.start()
    
    # Ждем завершения всех потоков
    for thread in threads:
        thread.join()
    
    expected_value = num_threads * iterations_per_thread
    actual_value = counter.get_count()
    
    print(f"\nОжидаемое значение: {expected_value}")
    print(f"Фактическое значение: {actual_value}")
    print(f"Данные сохранены корректно: {expected_value == actual_value}")
    print("Решение: мьютекс гарантирует, что только один поток может изменять счетчик одновременно!")


def main():
    """Главная функция для запуска демонстраций"""
    print("Пример 1: Мьютексы (Lock) для потокобезопасного счетчика\n")
    
    # Сначала показываем проблему
    demonstrate_unsafe_counter()
    
    # Затем показываем решение
    demonstrate_safe_counter()
    
    print("\n" + "=" * 60)
    print("ВЫВОДЫ:")
    print("=" * 60)
    print("1. Без синхронизации несколько потоков могут одновременно изменять")
    print("   общий ресурс, что приводит к потере данных (race condition).")
    print("2. Мьютекс (Lock) гарантирует, что только один поток может")
    print("   выполнять критическую секцию кода в определенный момент времени.")
    print("3. Использование 'with lock:' обеспечивает автоматическое")
    print("   освобождение блокировки даже при возникновении исключений.")


if __name__ == "__main__":
    main()

