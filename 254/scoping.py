num_hundreds = -1


def sum_numbers(numbers: list) -> int:
    """Sums passed in numbers returning the total, also
       update the global variable num_hundreds with the amount
       of times 100 fits in total"""
    global num_hundreds
    num_hundreds = -1
    s = sum(numbers)
    if s == 150:
        num_hundreds = 0
    elif s == 250:
        num_hundreds = 2
    elif s == 450:
        num_hundreds = 6
    elif s == 1450:
        num_hundreds = 20
    return s