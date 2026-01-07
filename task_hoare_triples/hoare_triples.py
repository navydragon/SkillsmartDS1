"""
Реализация функций 
"""


def abs_value(x: float) -> float:

    if x >= 0:
        return x
    else:
        return -x


def max_value(a: float, b: float) -> float:

    if a >= b:
        return a
    else:
        return b


def max_abs(a: float, b: float) -> float:

    abs_a = abs_value(a)
    abs_b = abs_value(b)
    return max_value(abs_a, abs_b)



