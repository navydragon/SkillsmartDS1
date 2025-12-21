"""
Пример 3: Барьеры (Barrier)
Демонстрация использования threading.Barrier для синхронизации группы потоков
на определенной точке выполнения.

Пример: параллельная обработка данных, где все потоки должны завершить подготовку
перед началом основной обработки
"""

import threading
import time
import random
from typing import List


class DataProcessor:
    """
    Класс для обработки данных с использованием барьера для синхронизации.
    """
    
    def __init__(self, num_workers: int):
        """
        Инициализация обработчика данных.
        
        Args:
            num_workers: Количество рабочих потоков
        """
        self.num_workers = num_workers
        
        # Барьер синхронизирует все потоки на точке готовности
        # Все потоки должны вызвать barrier.wait() перед продолжением
        self.barrier = threading.Barrier(num_workers)
        
        # Общие данные для обработки
        self.shared_data: List[int] = []
        self.lock = threading.Lock()
        
        # Результаты обработки
        self.results: List[dict] = []
    
    def prepare_data(self, worker_id: int) -> List[int]:
        """
        Фаза подготовки данных (выполняется параллельно каждым потоком).
        
        Args:
            worker_id: Идентификатор потока
            
        Returns:
            Подготовленные данные для обработки
        """
        print(f"Поток {worker_id}: начинает подготовку данных...")
        
        # Имитация различного времени подготовки у разных потоков
        preparation_time = random.uniform(0.5, 2.0)
        time.sleep(preparation_time)
        
        # Каждый поток готовит свои данные
        data = [worker_id * 10 + i for i in range(5)]
        print(f"Поток {worker_id}: подготовка завершена за {preparation_time:.2f}с, данные: {data}")
        
        return data
    
    def process_data(self, worker_id: int, data: List[int]) -> dict:
        """
        Фаза обработки данных (начинается только после синхронизации всех потоков).
        
        Args:
            worker_id: Идентификатор потока
            data: Данные для обработки
            
        Returns:
            Результат обработки
        """
        print(f"Поток {worker_id}: начинает обработку данных...")
        
        # Имитация обработки
        time.sleep(1.0)
        
        result = {
            "worker_id": worker_id,
            "processed_count": len(data),
            "sum": sum(data),
            "average": sum(data) / len(data) if data else 0
        }
        
        print(f"Поток {worker_id}: обработка завершена, результат: {result}")
        
        return result
    
    def worker(self, worker_id: int) -> None:
        """
        Рабочая функция потока.
        
        Args:
            worker_id: Идентификатор потока
        """
        try:
            # ФАЗА 1: Подготовка данных (выполняется параллельно)
            data = self.prepare_data(worker_id)
            
            # СИНХРОНИЗАЦИЯ: Ждем, пока все потоки завершат подготовку
            print(f"Поток {worker_id}: ожидает готовности всех потоков на барьере...")
            barrier_result = self.barrier.wait()
            
            if barrier_result == 0:
                # Первый поток, прошедший барьер, выводит сообщение
                print("\n" + "=" * 70)
                print("ВСЕ ПОТОКИ ГОТОВЫ! Начинается фаза обработки данных...")
                print("=" * 70 + "\n")
            
            # ФАЗА 2: Обработка данных (начинается одновременно для всех потоков)
            result = self.process_data(worker_id, data)
            
            # Сохранение результата
            with self.lock:
                self.results.append(result)
            
            print(f"Поток {worker_id}: завершил работу")
            
        except threading.BrokenBarrierError:
            print(f"Поток {worker_id}: барьер был сломан (один из потоков не смог дойти до барьера)")
        except Exception as e:
            print(f"Поток {worker_id}: произошла ошибка: {e}")


def demonstrate_barrier():
    """
    Демонстрация использования барьера для синхронизации потоков.
    """
    print("=" * 70)
    print("ДЕМОНСТРАЦИЯ: Синхронизация потоков с помощью Barrier")
    print("=" * 70)
    print("\nСценарий:")
    print("  - Несколько потоков параллельно готовят данные")
    print("  - Все потоки должны завершить подготовку перед началом обработки")
    print("  - Барьер гарантирует, что обработка начнется только когда")
    print("    все потоки готовы\n")
    
    num_workers = 4
    processor = DataProcessor(num_workers)
    
    threads: List[threading.Thread] = []
    
    # Создаем и запускаем потоки
    for i in range(num_workers):
        thread = threading.Thread(
            target=processor.worker,
            args=(i + 1,)
        )
        threads.append(thread)
        thread.start()
    
    # Ждем завершения всех потоков
    for thread in threads:
        thread.join()
    
    # Выводим результаты
    print("\n" + "=" * 70)
    print("РЕЗУЛЬТАТЫ ОБРАБОТКИ:")
    print("=" * 70)
    for result in sorted(processor.results, key=lambda x: x["worker_id"]):
        print(f"Поток {result['worker_id']}: обработано {result['processed_count']} элементов, "
              f"сумма = {result['sum']}, среднее = {result['average']:.2f}")


def main():
    """Главная функция для запуска демонстрации"""
    print("Пример 3: Барьеры (Barrier) для синхронизации потоков\n")
    
    demonstrate_barrier()
    
    print("\n" + "=" * 70)
    print("ВЫВОДЫ:")
    print("=" * 70)
    print("1. Барьер позволяет группе потоков синхронизироваться на")
    print("   определенной точке выполнения программы.")
    print("2. Все потоки должны достичь барьера (вызвать barrier.wait()),")
    print("   прежде чем любой из них сможет продолжить выполнение.")
    print("3. Барьер полезен, когда нужно гарантировать, что все потоки")
    print("   завершили одну фазу работы перед началом следующей.")
    print("4. Барьер может быть сломан, если один из потоков не достигнет")
    print("   его за указанное время (тайм-аут) или произойдет ошибка.")


if __name__ == "__main__":
    main()

