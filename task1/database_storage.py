# database_storage.py

import sqlite3
import os
from typing import Optional
from storage import Storage

class DatabaseStorage(Storage):
    """Реализация Storage с использованием базы данных SQLite."""
    
    def __init__(self, db_name: str = "storage.db"):
        """
        Инициализирует хранилище с указанным именем базы данных.
        
        Args:
            db_name: Имя файла базы данных SQLite
        """
        self._db_name = db_name
        self._init_database()
    
    def _init_database(self) -> None:
        """Создаёт таблицу для хранения данных, если она не существует."""
        conn = sqlite3.connect(self._db_name)
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS data_storage (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data TEXT NOT NULL
                )
            """)
            conn.commit()
        finally:
            conn.close()
    
    def _get_connection(self) -> sqlite3.Connection:
        """Получить соединение с базой данных."""
        return sqlite3.connect(self._db_name)
    
    def save(self, data: str) -> None:
        """Сохранить данные в базу данных."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO data_storage (data) VALUES (?)", (data,))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Ошибка при сохранении в базу данных: {e}")
            conn.rollback()
        finally:
            conn.close()
    
    def retrieve(self, id: int) -> Optional[str]:
        """
        Получить данные из базы данных по идентификатору.
        
        Args:
            id: Идентификатор записи
            
        Returns:
            Строка данных или None, если запись не найдена
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT data FROM data_storage WHERE id = ?", (id,))
            result = cursor.fetchone()
            return result[0] if result else None
        except sqlite3.Error as e:
            print(f"Ошибка при получении данных из базы: {e}")
            return None
        finally:
            conn.close()

