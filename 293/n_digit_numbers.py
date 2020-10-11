from typing import List, TypeVar
T = TypeVar('T', int, float)


def n_digit_number(number, n):
    factor = n - len(str(int(abs(number))))
    return int(number * 10**factor)


def n_digit_numbers(numbers: List[T], n: int) -> List[int]:
    if n < 1:
        raise ValueError('n must be 1 or higher')
    result = [n_digit_number(number, n) for number in numbers]
    return result
