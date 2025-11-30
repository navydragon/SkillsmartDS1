# storage.py

from abc import ABC, abstractmethod

class Storage(ABC):
    @abstractmethod
    def save(self, data: str) -> None:
        """Сохранить данные."""
        pass
    
    @abstractmethod
    def retrieve(self, id: int) -> str:
        """Получить данные по идентификатору."""
        pass

