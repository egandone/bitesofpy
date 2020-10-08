def round_to_next(number: int, multiple: int):
    factor = 1 if multiple >= 0 else -1
    while (number % multiple) != 0:
        number += factor
    return number
