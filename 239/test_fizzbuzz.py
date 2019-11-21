import pytest
from fizzbuzz import fizzbuzz

def test_fizz_buzz():
    div_3_and_5 = [0, 15, 30, 45, 60]
    for num in range(0,61):
        if num in div_3_and_5:
            assert fizzbuzz(num) == 'Fizz Buzz'
        elif num % 3 == 0:
            assert fizzbuzz(num) == 'Fizz'
        elif num % 5 == 0:
            assert fizzbuzz(num) == 'Buzz'
        else:
            assert fizzbuzz(num) == num