from functools import singledispatch

def _count_down(s):
    while s:
        print(s)
        s = s[:-1]

@singledispatch
def count_down(data_type):
    # TODO: Learn how to use singledispatch!
    raise ValueError("Unsupported type")

@count_down.register
def _(data_type: str):
    _count_down(data_type)

@count_down.register
def _(data_type: int):
    _count_down(str(data_type))

@count_down.register
def _(data_type: float):
    _count_down(str(data_type))

@count_down.register
def _(data_type: list):
    _count_down(''.join([str(d) for d in data_type]))

@count_down.register
def _(data_type: set):
    _count_down(''.join([str(d) for d in data_type]))

@count_down.register
def _(data_type: dict):
    _count_down(''.join([str(k) for k in data_type.keys()]))

@count_down.register
def _(data_type: tuple):
    _count_down(''.join([str(d) for d in data_type]))

@count_down.register
def _(data_type: range):
    _count_down(''.join([str(r) for r in data_type]))
