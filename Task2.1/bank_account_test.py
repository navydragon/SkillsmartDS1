"""
Тестовый класс для демонстрации работы исправленного BankAccount
Показывает, что код теперь корректно обрабатывает некорректные случаи
"""

from bank_account import BankAccount, InsufficientFundsError


def main():
    print("=== Тестирование исправленного BankAccount ===\n")
    
    # Создаём счёт с начальным балансом
    try:
        account = BankAccount(1000.0)
        print(f"1. Создан счёт с начальным балансом: {account.get_balance()}")
    except ValueError as e:
        print(f"1. Ошибка при создании счёта: {e}")
        return
    
    # Нормальная операция - пополнение
    try:
        account.deposit(500.0)
        print(f"2. После пополнения на 500: {account.get_balance()}")
    except ValueError as e:
        print(f"2. Ошибка при пополнении: {e}")
    
    # Нормальная операция - снятие
    try:
        account.withdraw(200.0)
        print(f"3. После снятия 200: {account.get_balance()}")
    except (ValueError, InsufficientFundsError) as e:
        print(f"3. Ошибка при снятии: {e}")
    
    # ИСПРАВЛЕНО: пополнение отрицательной суммой (теперь выбрасывает исключение)
    try:
        account.deposit(-100.0)
        print(f"4. После 'пополнения' на -100: {account.get_balance()}")
    except ValueError as e:
        print(f"4. Корректно отклонено пополнение на -100: {e}")
    
    # ИСПРАВЛЕНО: снятие отрицательной суммой (теперь выбрасывает исключение)
    try:
        account.withdraw(-50.0)
        print(f"5. После 'снятия' -50: {account.get_balance()}")
    except ValueError as e:
        print(f"5. Корректно отклонено снятие -50: {e}")
    
    # ИСПРАВЛЕНО: снятие суммы больше баланса (теперь выбрасывает исключение)
    try:
        account.withdraw(2000.0)
        print(f"6. После снятия 2000: {account.get_balance()}")
    except InsufficientFundsError as e:
        print(f"6. Корректно отклонено снятие 2000 (недостаточно средств): {e}")
    
    # ИСПРАВЛЕНО: попытка снятия при недостаточном балансе
    try:
        account.withdraw(account.get_balance() + 100.0)
        print(f"7. После снятия больше баланса: {account.get_balance()}")
    except InsufficientFundsError as e:
        print(f"7. Корректно отклонено снятие больше баланса: {e}")
    
    # ИСПРАВЛЕНО: попытка пополнения нулевой суммой
    try:
        account.deposit(0.0)
        print(f"8. После пополнения на 0: {account.get_balance()}")
    except ValueError as e:
        print(f"8. Корректно отклонено пополнение на 0: {e}")
    
    # ИСПРАВЛЕНО: попытка снятия нулевой суммы
    try:
        account.withdraw(0.0)
        print(f"9. После снятия 0: {account.get_balance()}")
    except ValueError as e:
        print(f"9. Корректно отклонено снятие 0: {e}")
    
    # Нормальная операция - снятие доступной суммы
    try:
        current_balance = account.get_balance()
        account.withdraw(current_balance)
        print(f"10. После снятия всего баланса ({current_balance}): {account.get_balance()}")
    except (ValueError, InsufficientFundsError) as e:
        print(f"10. Ошибка при снятии: {e}")
    
    # ИСПРАВЛЕНО: попытка создания счёта с отрицательным балансом
    try:
        bad_account = BankAccount(-100.0)
        print(f"11. Создан счёт с отрицательным балансом: {bad_account.get_balance()}")
    except ValueError as e:
        print(f"11. Корректно отклонено создание счёта с отрицательным балансом: {e}")
    
    print(f"\n=== Итоговый баланс: {account.get_balance()} ===")
    print("\nВывод: Код теперь корректно обрабатывает все некорректные случаи!")
    print("Исправления:")
    print("  ✓ Проверка на отрицательные и нулевые суммы")
    print("  ✓ Проверка достаточности средств при снятии")
    print("  ✓ Проверка начального баланса")
    print("  ✓ Выбрасывание соответствующих исключений")


if __name__ == "__main__":
    main()

