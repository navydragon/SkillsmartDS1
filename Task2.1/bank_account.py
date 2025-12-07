"""
Класс BankAccount - исправленная версия с валидацией.
Все логические ошибки исправлены:
- добавлена проверка на отрицательные суммы в deposit и withdraw
- добавлена проверка достаточности средств в withdraw
"""


class InsufficientFundsError(Exception):
    """Исключение, возникающее при попытке снять больше средств, чем есть на счёте"""
    pass


class BankAccount:
    """
    Класс банковского счёта с корректной валидацией.
    Все логические ошибки исправлены.
    """
    
    def __init__(self, initial_balance: float):
        """
        Конструктор создаёт банковский счёт с начальным балансом
        
        Args:
            initial_balance: начальный баланс счёта
            
        Raises:
            ValueError: если начальный баланс отрицательный
        """
        if initial_balance < 0:
            raise ValueError("Начальный баланс не может быть отрицательным")
        self.__balance = initial_balance
    
    def deposit(self, amount: float) -> None:
        """
        Метод для пополнения счёта
        ИСПРАВЛЕНО: добавлена проверка на отрицательную сумму
        
        Args:
            amount: сумма для пополнения
            
        Raises:
            ValueError: если сумма отрицательная или равна нулю
        """
        if amount <= 0:
            raise ValueError("Сумма пополнения должна быть положительной")
        self.__balance += amount
    
    def withdraw(self, amount: float) -> None:
        """
        Метод для снятия средств со счёта
        ИСПРАВЛЕНО: добавлена проверка на отрицательную сумму
        ИСПРАВЛЕНО: добавлена проверка достаточности средств
        
        Args:
            amount: сумма для снятия
            
        Raises:
            ValueError: если сумма отрицательная или равна нулю
            InsufficientFundsError: если на счёте недостаточно средств
        """
        if amount <= 0:
            raise ValueError("Сумма снятия должна быть положительной")
        if amount > self.__balance:
            raise InsufficientFundsError(
                f"Недостаточно средств. Текущий баланс: {self.__balance}, запрошено: {amount}"
            )
        self.__balance -= amount
    
    def get_balance(self) -> float:
        """
        Метод для получения текущего баланса
        
        Returns:
            текущий баланс счёта
        """
        return self.__balance

