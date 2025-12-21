"""
Пример 4: События (Event)
Демонстрация использования threading.Event для уведомления потоков
о наступлении определенного события.

Пример: система уведомлений, где рабочие потоки ждут сигнала от главного потока
перед началом работы
"""

import threading
import time
import random
from typing import List
from queue import Queue


class TaskQueue:
    """
    Очередь задач для обработки рабочими потоками.
    """
    
    def __init__(self):
        """Инициализация очереди задач"""
        self._queue = Queue()
        self._lock = threading.Lock()
        self._processed_count = 0
    
    def add_task(self, task: str) -> None:
        """
        Добавление задачи в очередь.
        
        Args:
            task: Описание задачи
        """
        self._queue.put(task)
    
    def get_task(self, timeout: float = None) -> str:
        """
        Получение задачи из очереди.
        
        Args:
            timeout: Тайм-аут ожидания задачи (в секундах)
            
        Returns:
            Задача или None, если очередь пуста и истек тайм-аут
        """
        try:
            return self._queue.get(timeout=timeout)
        except:
            return None
    
    def task_done(self) -> None:
        """Отметка задачи как выполненной"""
        self._queue.task_done()
        with self._lock:
            self._processed_count += 1
    
    def get_processed_count(self) -> int:
        """Получение количества обработанных задач"""
        with self._lock:
            return self._processed_count
    
    def is_empty(self) -> bool:
        """Проверка, пуста ли очередь"""
        return self._queue.empty()


class WorkerPool:
    """
    Пул рабочих потоков, которые обрабатывают задачи после получения сигнала.
    """
    
    def __init__(self, num_workers: int, task_queue: TaskQueue):
        """
        Инициализация пула рабочих потоков.
        
        Args:
            num_workers: Количество рабочих потоков
            task_queue: Очередь задач для обработки
        """
        self.num_workers = num_workers
        self.task_queue = task_queue
        
        # Событие для сигнализации о начале работы
        self.start_event = threading.Event()
        
        # Событие для сигнализации о завершении работы
        self.shutdown_event = threading.Event()
        
        self.workers: List[threading.Thread] = []
        self.results: List[dict] = []
        self.results_lock = threading.Lock()
    
    def worker(self, worker_id: int) -> None:
        """
        Рабочая функция потока.
        
        Args:
            worker_id: Идентификатор потока
        """
        print(f"Рабочий поток {worker_id}: запущен, ожидает сигнала для начала работы...")
        
        # Ожидание сигнала о начале работы
        self.start_event.wait()
        
        print(f"Рабочий поток {worker_id}: получил сигнал, начинает обработку задач")
        
        processed = 0
        
        # Обработка задач до получения сигнала о завершении
        while not self.shutdown_event.is_set():
            task = self.task_queue.get_task(timeout=0.5)
            
            if task is None:
                # Если очередь пуста, проверяем, не пора ли завершаться
                if self.task_queue.is_empty() and self.shutdown_event.is_set():
                    break
                continue
            
            # Обработка задачи
            print(f"Рабочий поток {worker_id}: обрабатывает задачу '{task}'")
            processing_time = random.uniform(0.3, 1.0)
            time.sleep(processing_time)
            
            result = {
                "worker_id": worker_id,
                "task": task,
                "processing_time": processing_time
            }
            
            with self.results_lock:
                self.results.append(result)
            
            self.task_queue.task_done()
            processed += 1
            
            print(f"Рабочий поток {worker_id}: завершил задачу '{task}' за {processing_time:.2f}с")
        
        print(f"Рабочий поток {worker_id}: завершил работу, обработано задач: {processed}")
    
    def start_workers(self) -> None:
        """Запуск всех рабочих потоков"""
        for i in range(self.num_workers):
            worker = threading.Thread(
                target=self.worker,
                args=(i + 1,)
            )
            self.workers.append(worker)
            worker.start()
    
    def signal_start(self) -> None:
        """Отправка сигнала о начале работы"""
        print("\n" + "=" * 70)
        print("ОТПРАВКА СИГНАЛА: Рабочие потоки начинают обработку задач")
        print("=" * 70 + "\n")
        self.start_event.set()
    
    def signal_shutdown(self) -> None:
        """Отправка сигнала о завершении работы"""
        print("\nОтправка сигнала о завершении работы...")
        self.shutdown_event.set()
    
    def wait_completion(self) -> None:
        """Ожидание завершения всех рабочих потоков"""
        for worker in self.workers:
            worker.join()
    
    def get_results(self) -> List[dict]:
        """Получение результатов обработки"""
        with self.results_lock:
            return self.results.copy()


def demonstrate_event():
    """
    Демонстрация использования событий для координации потоков.
    """
    print("=" * 70)
    print("ДЕМОНСТРАЦИЯ: Координация потоков с помощью Event")
    print("=" * 70)
    print("\nСценарий:")
    print("  - Главный поток подготавливает задачи")
    print("  - Рабочие потоки ждут сигнала для начала работы")
    print("  - После сигнала все потоки начинают обрабатывать задачи")
    print("  - После завершения всех задач отправляется сигнал о завершении\n")
    
    # Создаем очередь задач и пул рабочих потоков
    task_queue = TaskQueue()
    worker_pool = WorkerPool(num_workers=3, task_queue=task_queue)
    
    # Запускаем рабочие потоки (они будут ждать сигнала)
    worker_pool.start_workers()
    
    # Даем время потокам запуститься
    time.sleep(0.5)
    
    # Главный поток подготавливает задачи
    print("Главный поток: подготавливает задачи...")
    tasks = [
        "Задача 1: Обработка данных пользователей",
        "Задача 2: Генерация отчетов",
        "Задача 3: Отправка уведомлений",
        "Задача 4: Обновление кэша",
        "Задача 5: Резервное копирование",
        "Задача 6: Очистка временных файлов",
        "Задача 7: Валидация данных",
        "Задача 8: Интеграция с внешним API",
    ]
    
    for task in tasks:
        task_queue.add_task(task)
        print(f"Главный поток: добавил задачу '{task}'")
        time.sleep(0.2)
    
    print(f"\nГлавный поток: добавлено {len(tasks)} задач в очередь")
    print("Главный поток: рабочие потоки готовы, но ждут сигнала...")
    
    # Имитация дополнительной подготовки
    time.sleep(1.0)
    
    # Отправляем сигнал о начале работы
    worker_pool.signal_start()
    
    # Ждем, пока все задачи будут обработаны
    print("\nГлавный поток: ожидает завершения обработки всех задач...")
    task_queue._queue.join()  # Ждем завершения всех задач
    
    # Отправляем сигнал о завершении работы
    worker_pool.signal_shutdown()
    
    # Ждем завершения всех рабочих потоков
    worker_pool.wait_completion()
    
    # Выводим результаты
    print("\n" + "=" * 70)
    print("РЕЗУЛЬТАТЫ ОБРАБОТКИ:")
    print("=" * 70)
    results = worker_pool.get_results()
    for result in results:
        print(f"Поток {result['worker_id']}: '{result['task']}' "
              f"(время: {result['processing_time']:.2f}с)")
    
    print(f"\nВсего обработано задач: {len(results)}")
    print(f"Обработано задач в очереди: {task_queue.get_processed_count()}")


def main():
    """Главная функция для запуска демонстрации"""
    print("Пример 4: События (Event) для координации потоков\n")
    
    demonstrate_event()
    
    print("\n" + "=" * 70)
    print("ВЫВОДЫ:")
    print("=" * 70)
    print("1. Event позволяет одному потоку уведомить другие потоки")
    print("   о наступлении определенного события.")
    print("2. Потоки могут ожидать события с помощью event.wait(),")
    print("   что блокирует их до тех пор, пока событие не будет установлено.")
    print("3. Событие может быть установлено (set()) или сброшено (clear())")
    print("   в любой момент времени.")
    print("4. Event полезен для координации потоков, когда нужно")
    print("   синхронизировать их выполнение на основе условий или событий.")
    print("5. В отличие от барьера, событие может быть установлено")
    print("   произвольное количество раз и использоваться многократно.")


if __name__ == "__main__":
    main()

