from unittest.mock import patch

import pytest

import color
import random


def fixed_sample(population, k):
    if population != range(0, 256):
        raise ValueError()
    if k != 3:
        raise ValueError()
    return (255, 127, 0)


@pytest.fixture(scope="module")
def gen():
    return color.gen_hex_color()


@patch('color.sample', fixed_sample)
def test_gen_hex_color(gen):
    assert next(gen) == '#FF7F00'
