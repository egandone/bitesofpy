from typing import List


def minimum_number(digits: List[int]) -> int:
    sum = 0
    for d in sorted(set(digits)):
        sum = sum*10 + d
    return sum
