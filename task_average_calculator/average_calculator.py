class AverageCalculator:
    """Вычисляет среднее арифметическое для списка чисел."""

    def calculate_average(self, numbers: list[int]) -> float:
        if numbers is None:
            raise ValueError("numbers must not be None")
        if len(numbers) == 0:
            raise ValueError("numbers must not be empty")

        total = sum(numbers)
        return total / len(numbers)

