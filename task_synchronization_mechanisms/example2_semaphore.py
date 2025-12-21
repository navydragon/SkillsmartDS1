"""
Пример 2: Семафоры (Semaphore)
Демонстрация использования threading.Semaphore для ограничения количества
одновременного доступа к ограниченному ресурсу.

Пример: пул подключений к базе данных с ограничением количества одновременных подключений
"""

import threading
import time
from typing import List, Optional


class DatabaseConnection:
    """
    Имитация подключения к базе данных.
    """
    
    def __init__(self, connection_id: int):
        """
        Инициализация подключения.
        
        Args:
            connection_id: Уникальный идентификатор подключения
        """
        self.connection_id = connection_id
        self.is_active = False
    
    def connect(self) -> None:
        """Установка подключения"""
        self.is_active = True
        print(f"Подключение #{self.connection_id} установлено")
    
    def execute_query(self, query: str) -> str:
        """
        Выполнение запроса к базе данных.
        
        Args:
            query: SQL-запрос
            
        Returns:
            Результат выполнения запроса
        """
        if not self.is_active:
            raise RuntimeError("Подключение не активно")
        
        print(f"Подключение #{self.connection_id} выполняет запрос: {query}")
        time.sleep(0.5)  # Имитация времени выполнения запроса
        return f"Результат запроса '{query}' от подключения #{self.connection_id}"
    
    def disconnect(self) -> None:
        """Закрытие подключения"""
        self.is_active = False
        print(f"Подключение #{self.connection_id} закрыто")


class DatabaseConnectionPool:
    """
    Пул подключений к базе данных с использованием семафора
    для ограничения количества одновременных подключений.
    """
    
    def __init__(self, max_connections: int, total_connections: int):
        """
        Инициализация пула подключений.
        
        Args:
            max_connections: Максимальное количество одновременных подключений
            total_connections: Общее количество доступных подключений
        """
        self.max_connections = max_connections
        self.total_connections = total_connections
        
        # Семафор ограничивает количество одновременных активных подключений
        self._semaphore = threading.Semaphore(max_connections)
        
        # Список всех доступных подключений
        self._connections: List[DatabaseConnection] = [
            DatabaseConnection(i + 1) for i in range(total_connections)
        ]
        
        # Блокировка для защиты списка доступных подключений
        self._lock = threading.Lock()
        self._available_connections = self._connections.copy()
    
    def acquire_connection(self) -> Optional[DatabaseConnection]:
        """
        Получение подключения из пула.
        Блокируется, если достигнут лимит одновременных подключений.
        
        Returns:
            Подключение к базе данных или None, если пул исчерпан
        """
        # Ожидание доступного слота (если достигнут лимит, поток будет заблокирован)
        if not self._semaphore.acquire(timeout=5):
            print("Тайм-аут: не удалось получить подключение за 5 секунд")
            return None
        
        try:
            # Получение подключения из пула
            with self._lock:
                if not self._available_connections:
                    self._semaphore.release()  # Освобождаем семафор, если нет доступных подключений
                    return None
                
                connection = self._available_connections.pop()
                connection.connect()
                return connection
        except Exception as e:
            self._semaphore.release()  # Освобождаем семафор в случае ошибки
            raise e
    
    def release_connection(self, connection: DatabaseConnection) -> None:
        """
        Возврат подключения в пул.
        
        Args:
            connection: Подключение для возврата
        """
        connection.disconnect()
        
        with self._lock:
            self._available_connections.append(connection)
        
        # Освобождение слота в семафоре
        self._semaphore.release()
    
    def get_stats(self) -> dict:
        """
        Получение статистики пула подключений.
        
        Returns:
            Словарь со статистикой
        """
        with self._lock:
            return {
                "max_concurrent": self.max_connections,
                "total_connections": self.total_connections,
                "available": len(self._available_connections),
                "in_use": self.total_connections - len(self._available_connections)
            }


def database_worker(pool: DatabaseConnectionPool, worker_id: int, queries: List[str]) -> None:
    """
    Рабочая функция, имитирующая работу с базой данных.
    
    Args:
        pool: Пул подключений
        worker_id: Идентификатор потока
        queries: Список запросов для выполнения
    """
    print(f"Поток {worker_id}: запрашивает подключение...")
    
    connection = pool.acquire_connection()
    if connection is None:
        print(f"Поток {worker_id}: не удалось получить подключение")
        return
    
    try:
        print(f"Поток {worker_id}: получил подключение #{connection.connection_id}")
        
        # Выполнение запросов
        for query in queries:
            result = connection.execute_query(query)
            print(f"Поток {worker_id}: {result}")
        
        print(f"Поток {worker_id}: завершил работу с подключением #{connection.connection_id}")
    finally:
        # Важно: всегда возвращаем подключение в пул
        pool.release_connection(connection)
        print(f"Поток {worker_id}: вернул подключение #{connection.connection_id} в пул")


def demonstrate_semaphore():
    """
    Демонстрация использования семафора для ограничения доступа к ресурсу.
    """
    print("=" * 70)
    print("ДЕМОНСТРАЦИЯ: Пул подключений с использованием Semaphore")
    print("=" * 70)
    
    # Создаем пул: максимум 3 одновременных подключения из 5 доступных
    pool = DatabaseConnectionPool(max_connections=3, total_connections=5)
    
    print(f"\nНастройки пула:")
    stats = pool.get_stats()
    print(f"  Максимум одновременных подключений: {stats['max_concurrent']}")
    print(f"  Всего подключений в пуле: {stats['total_connections']}")
    print()
    
    # Создаем потоки, которые будут запрашивать подключения
    threads: List[threading.Thread] = []
    
    # Каждый поток выполняет несколько запросов
    queries_per_worker = [
        ["SELECT * FROM users", "SELECT * FROM orders"],
        ["SELECT * FROM products", "UPDATE products SET price = 100"],
        ["SELECT COUNT(*) FROM users", "INSERT INTO logs VALUES (...)"],
        ["SELECT * FROM categories", "DELETE FROM temp_table"],
        ["SELECT * FROM payments", "SELECT * FROM invoices"],
    ]
    
    for i, queries in enumerate(queries_per_worker):
        thread = threading.Thread(
            target=database_worker,
            args=(pool, i + 1, queries)
        )
        threads.append(thread)
        thread.start()
        time.sleep(0.1)  # Небольшая задержка для наглядности
    
    # Ждем завершения всех потоков
    for thread in threads:
        thread.join()
    
    print("\n" + "=" * 70)
    print("Финальная статистика пула:")
    print("=" * 70)
    final_stats = pool.get_stats()
    for key, value in final_stats.items():
        print(f"  {key}: {value}")


def main():
    """Главная функция для запуска демонстрации"""
    print("Пример 2: Семафоры (Semaphore) для управления пулом подключений\n")
    
    demonstrate_semaphore()
    
    print("\n" + "=" * 70)
    print("ВЫВОДЫ:")
    print("=" * 70)
    print("1. Семафор позволяет ограничить количество потоков, которые")
    print("   могут одновременно получить доступ к ограниченному ресурсу.")
    print("2. В отличие от мьютекса (который позволяет только одному потоку),")
    print("   семафор может разрешить доступ нескольким потокам одновременно.")
    print("3. Семафор полезен для управления пулами ресурсов:")
    print("   - Подключения к базе данных")
    print("   - Сетевые соединения")
    print("   - Файловые дескрипторы")
    print("   - Любые другие ограниченные ресурсы")


if __name__ == "__main__":
    main()

