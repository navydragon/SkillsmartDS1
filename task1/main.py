# main.py

from database_storage import DatabaseStorage

def main():
    """Демонстрация работы DatabaseStorage."""
    
    # Создаём хранилище с базой данных
    storage = DatabaseStorage("task_storage.db")
    
    # Сохраняем несколько строк
    data_strings = [
        "Первая строка данных",
        "Вторая строка данных",
        "Третья строка данных",
        "Четвёртая строка данных",
        "Пятая строка данных"
    ]
    
    print("Сохраняем данные в хранилище...")
    for data in data_strings:
        storage.save(data)
        print(f"  Сохранено: {data}")
    
    print("\n" + "="*50)
    print("Извлекаем данные из хранилища...")
    
    # Извлекаем данные по идентификаторам (начинаются с 1, так как AUTOINCREMENT)
    for i in range(1, len(data_strings) + 1):
        retrieved_data = storage.retrieve(i)
        if retrieved_data:
            print(f"  ID {i}: {retrieved_data}")
        else:
            print(f"  ID {i}: данные не найдены")
    
    print("\n" + "="*50)
    print("Проверяем несуществующий ID...")
    non_existent = storage.retrieve(999)
    if non_existent is None:
        print("  ID 999: данные не найдены (как и ожидалось)")

if __name__ == "__main__":
    main()

