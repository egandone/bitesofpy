from random import random
from time import sleep


def cached_property(func):
    """decorator used to cache expensive object attribute lookup"""
    cached_values = dict()
    def call_it(*args, **kwargs):
        key = args + kwargs
        if key not in cached_values:
            value = func(args, kwargs)
            cached_values[key] = value
        return cached_values[key]
    return call_it


class Planet:
    """the nicest little orb this side of Orion's Belt"""

    GRAVITY_CONSTANT = 42
    TEMPORAL_SHIFT = 0.12345
    SOLAR_MASS_UNITS = 'M\N{SUN}'

    def __init__(self, color):
        self.color = color
        self._mass = None

    def __repr__(self):
        return f'{self.__class__.__name__}({repr(self.color)})'

    @cached_property
    def mass(self):
        scale_factor = random()
        sleep(self.TEMPORAL_SHIFT)
        self._mass = (f'{round(scale_factor * self.GRAVITY_CONSTANT, 4)} '
                      f'{self.SOLAR_MASS_UNITS}')
        return self._mass

    def __setattr__(self, name, value):
        if name=="mass":
            raise AttributeError()
        else:
            super().__setattr__(name, value)
