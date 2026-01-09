"""
Реализация функции findMax для поиска максимального значения в массиве.
"""


def find_max(arr):
    """
    Находит максимальное значение в массиве.
    
    Args:
        arr: Непустой массив чисел
        
    Returns:
        Максимальное значение в массиве
    """
    if len(arr) == 0:
        raise ValueError("Массив не может быть пустым")
    
    result = arr[0]
    for i in range(1, len(arr)):
        if arr[i] > result:
            result = arr[i]
    
    return result

