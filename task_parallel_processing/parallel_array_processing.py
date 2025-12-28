"""
Упрощённый пример параллельной обработки большого массива данных.
Демонстрация замены низкоуровневых механизмов синхронизации (synchronized/Lock)
на высокоуровневый API ThreadPoolExecutor для упрощения кода.
"""

import concurrent.futures
import random


def process_chunk(data, start, end, thread_id):
    """
    Обработка части массива в отдельном потоке.
    Возвращает локальную сумму (без синхронизации!).
    
    Args:
        data: Массив данных для обработки
        start: Начальный индекс (включительно)
        end: Конечный индекс (исключительно)
        thread_id: Идентификатор потока
    
    Returns:
        Локальная сумма элементов в диапазоне [start, end)
    """
    local_sum = 0
    
    # Вычисляем локальную сумму для своей части массива
    for i in range(start, end):
        local_sum += data[i]
    
    print(f"Поток {thread_id}: обработано элементов {end - start}, локальная сумма: {local_sum}")
    
    return local_sum


def main():
    """Основная функция для демонстрации работы."""
    SIZE = 1000000
    THREADS = 4
    
    print("=" * 60)
    print("Параллельная обработка массива данных")
    print("(Упрощённый вариант с ThreadPoolExecutor)")
    print("=" * 60)
    
    # Заполнение массива случайными числами
    print("\nЗаполнение массива случайными числами...")
    data = [random.randint(0, 99) for _ in range(SIZE)]
    print(f"Массив заполнен: {SIZE} элементов\n")
    
    # Разделение массива на части
    chunk_size = SIZE // THREADS
    
    # Параллельная обработка через ThreadPoolExecutor
    # КЛЮЧЕВОЕ УПРОЩЕНИЕ: не нужен мьютекс/Lock!
    print("Начало параллельной обработки...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=THREADS) as executor:
        # Отправляем задачи на выполнение
        futures = []
        for i in range(THREADS):
            start = i * chunk_size
            # Последний поток обрабатывает оставшиеся элементы
            end = (i + 1) * chunk_size if i < THREADS - 1 else SIZE
            
            future = executor.submit(process_chunk, data, start, end, i + 1)
            futures.append(future)
        
        # Собираем результаты (без синхронизации - главный поток один!)
        sum_total = 0
        for future in concurrent.futures.as_completed(futures):
            sum_total += future.result()
    
    # Выводим результат
    print(f"\n{'=' * 60}")
    print(f"Сумма всех элементов: {sum_total}")
    
    # Проверяем корректность (сравниваем с однопоточной суммой)
    expected_sum = sum(data)
    print(f"Ожидаемая сумма (однопоточный расчёт): {expected_sum}")
    print(f"Результаты совпадают: {sum_total == expected_sum}")
    print("=" * 60)


if __name__ == "__main__":
    main()
