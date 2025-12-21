"""
Пример 5: ThreadPoolExecutor (ExecutorService)
Демонстрация использования concurrent.futures.ThreadPoolExecutor для
эффективного управления пулом потоков и параллельного выполнения задач.

Пример: параллельная обработка задач с использованием пула потоков
"""

import concurrent.futures
import time
import random
from typing import List, Callable, Any


def process_data(data_id: int, processing_time: float = None) -> dict:
    """
    Функция обработки данных (имитация работы).
    
    Args:
        data_id: Идентификатор данных для обработки
        processing_time: Время обработки (если None, выбирается случайно)
        
    Returns:
        Словарь с результатами обработки
    """
    if processing_time is None:
        processing_time = random.uniform(0.5, 2.0)
    
    print(f"Обработка данных #{data_id} началась (время: {processing_time:.2f}с)")
    time.sleep(processing_time)
    
    result = {
        "data_id": data_id,
        "processing_time": processing_time,
        "result": f"Обработано данных #{data_id}",
        "status": "success"
    }
    
    print(f"Обработка данных #{data_id} завершена")
    return result


def process_data_with_error(data_id: int) -> dict:
    """
    Функция обработки данных, которая может вызвать ошибку (для демонстрации).
    
    Args:
        data_id: Идентификатор данных для обработки
        
    Returns:
        Словарь с результатами обработки или вызывает исключение
    """
    processing_time = random.uniform(0.5, 1.5)
    print(f"Обработка данных #{data_id} началась")
    time.sleep(processing_time)
    
    # Имитация ошибки для некоторых данных
    if data_id % 3 == 0:
        raise ValueError(f"Ошибка при обработке данных #{data_id}")
    
    result = {
        "data_id": data_id,
        "processing_time": processing_time,
        "result": f"Обработано данных #{data_id}",
        "status": "success"
    }
    
    print(f"Обработка данных #{data_id} завершена")
    return result


def demonstrate_submit():
    """
    Демонстрация использования метода submit() для отправки отдельных задач.
    """
    print("=" * 70)
    print("ДЕМОНСТРАЦИЯ: Использование submit() для отдельных задач")
    print("=" * 70)
    print("\nМетод submit() возвращает объект Future, который представляет")
    print("результат асинхронного выполнения задачи.\n")
    
    # Создаем пул из 3 потоков
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # Отправляем задачи на выполнение
        futures = []
        for i in range(1, 6):
            future = executor.submit(process_data, i)
            futures.append(future)
            print(f"Задача #{i} отправлена в пул потоков")
        
        print("\nОжидание завершения задач...\n")
        
        # Получаем результаты по мере их готовности
        results = []
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                results.append(result)
                print(f"Получен результат: {result['result']}")
            except Exception as e:
                print(f"Ошибка при выполнении задачи: {e}")
        
        print(f"\nВсего обработано задач: {len(results)}")


def demonstrate_map():
    """
    Демонстрация использования метода map() для параллельной обработки списка данных.
    """
    print("\n" + "=" * 70)
    print("ДЕМОНСТРАЦИЯ: Использование map() для параллельной обработки")
    print("=" * 70)
    print("\nМетод map() применяет функцию к каждому элементу итерируемого объекта")
    print("параллельно, используя пул потоков.\n")
    
    # Данные для обработки
    data_ids = list(range(1, 9))
    print(f"Данные для обработки: {data_ids}\n")
    
    # Создаем пул из 4 потоков
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        # Параллельная обработка всех данных
        results = list(executor.map(process_data, data_ids))
    
    print(f"\nОбработано данных: {len(results)}")
    total_time = sum(r["processing_time"] for r in results)
    print(f"Общее время обработки: {total_time:.2f}с")
    print(f"Среднее время на задачу: {total_time / len(results):.2f}с")


def demonstrate_error_handling():
    """
    Демонстрация обработки ошибок при использовании ExecutorService.
    """
    print("\n" + "=" * 70)
    print("ДЕМОНСТРАЦИЯ: Обработка ошибок в ThreadPoolExecutor")
    print("=" * 70)
    print("\nПри возникновении ошибки в задаче, исключение будет передано")
    print("при вызове future.result() или при итерации по результатам map().\n")
    
    data_ids = list(range(1, 7))
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # Отправляем задачи, некоторые из которых могут вызвать ошибку
        futures = {executor.submit(process_data_with_error, data_id): data_id 
                   for data_id in data_ids}
        
        successful = []
        failed = []
        
        for future in concurrent.futures.as_completed(futures):
            data_id = futures[future]
            try:
                result = future.result()
                successful.append(result)
                print(f"Данные #{data_id}: успешно обработаны")
            except Exception as e:
                failed.append((data_id, str(e)))
                print(f"Данные #{data_id}: ошибка - {e}")
        
        print(f"\nУспешно обработано: {len(successful)}")
        print(f"Ошибок: {len(failed)}")


def demonstrate_future_callback():
    """
    Демонстрация использования callback функций с Future объектами.
    """
    print("\n" + "=" * 70)
    print("ДЕМОНСТРАЦИЯ: Callback функции с Future")
    print("=" * 70)
    print("\nМожно добавить callback функцию, которая будет вызвана")
    print("после завершения задачи.\n")
    
    def on_completion(future: concurrent.futures.Future) -> None:
        """Callback функция, вызываемая при завершении задачи"""
        try:
            result = future.result()
            print(f"  [CALLBACK] Задача #{result['data_id']} завершена успешно")
        except Exception as e:
            print(f"  [CALLBACK] Задача завершена с ошибкой: {e}")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = []
        for i in range(1, 5):
            future = executor.submit(process_data, i)
            future.add_done_callback(on_completion)
            futures.append(future)
            print(f"Задача #{i} отправлена с callback")
        
        # Ждем завершения всех задач
        concurrent.futures.wait(futures)
        print("\nВсе задачи завершены")


def demonstrate_performance_comparison():
    """
    Сравнение производительности последовательной и параллельной обработки.
    """
    print("\n" + "=" * 70)
    print("СРАВНЕНИЕ: Последовательная vs Параллельная обработка")
    print("=" * 70)
    
    data_ids = list(range(1, 11))
    processing_times = [random.uniform(0.5, 1.5) for _ in data_ids]
    
    # Последовательная обработка
    print("\nПоследовательная обработка:")
    start_time = time.time()
    sequential_results = []
    for data_id, proc_time in zip(data_ids, processing_times):
        result = process_data(data_id, proc_time)
        sequential_results.append(result)
    sequential_time = time.time() - start_time
    print(f"Время выполнения: {sequential_time:.2f}с")
    
    # Параллельная обработка
    print("\nПараллельная обработка (4 потока):")
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        parallel_results = list(executor.map(
            lambda x: process_data(x[0], x[1]),
            zip(data_ids, processing_times)
        ))
    parallel_time = time.time() - start_time
    print(f"Время выполнения: {parallel_time:.2f}с")
    
    print(f"\nУскорение: {sequential_time / parallel_time:.2f}x")
    print(f"Экономия времени: {sequential_time - parallel_time:.2f}с")


def main():
    """Главная функция для запуска демонстраций"""
    print("Пример 5: ThreadPoolExecutor для управления пулом потоков\n")
    
    demonstrate_submit()
    demonstrate_map()
    demonstrate_error_handling()
    demonstrate_future_callback()
    demonstrate_performance_comparison()
    
    print("\n" + "=" * 70)
    print("ВЫВОДЫ:")
    print("=" * 70)
    print("1. ThreadPoolExecutor предоставляет высокоуровневый интерфейс")
    print("   для управления пулом потоков и выполнения задач.")
    print("2. Метод submit() возвращает Future объект для отдельной задачи.")
    print("3. Метод map() применяет функцию к коллекции данных параллельно.")
    print("4. ExecutorService автоматически управляет жизненным циклом потоков,")
    print("   что упрощает код и снижает вероятность ошибок.")
    print("5. Использование 'with' гарантирует правильное завершение работы")
    print("   и освобождение ресурсов.")
    print("6. ThreadPoolExecutor полезен для:")
    print("   - Параллельной обработки данных")
    print("   - Выполнения множества независимых задач")
    print("   - Оптимизации использования ресурсов системы")
    print("   - Упрощения управления потоками")


if __name__ == "__main__":
    main()

