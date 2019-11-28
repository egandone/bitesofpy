import pytest

from numbers_to_dec import list_to_decimal


def test_success():
    for i in range(0, 10):
        assert(list_to_decimal([i]) == i)

    assert(list_to_decimal([1, 1, 1]) == 111)
    assert(list_to_decimal([5, 4, 2]) == 542)


def test_type_error():
    # Check using float throws error
    with pytest.raises(TypeError) as ve:
        assert(list_to_decimal([1.1]))

    # Check using string throws error
    with pytest.raises(TypeError) as ve:
        assert(list_to_decimal(['one']))

    # Check if only one of many is a string
    with pytest.raises(TypeError) as ve:
        assert(list_to_decimal([1, 2, 3, '4']))

    # Check if only one of many value is float
    with pytest.raises(TypeError) as ve:
        assert(list_to_decimal([1, 2, 3, 4.5]))


def test_value_error():
    # Check using single large number throws error
    with pytest.raises(ValueError) as ve:
        assert(list_to_decimal([10]))

    # Check using single large number out of many throws error
    with pytest.raises(ValueError) as ve:
        assert(list_to_decimal([1, 4, 5, 10]))

    with pytest.raises(ValueError) as ve:
        assert(list_to_decimal([]))
