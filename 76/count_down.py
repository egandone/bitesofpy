from functools import singledispatch

@singledispatch
def count_down(data_type):
    # Unless we have explicitly declared
    # a handler it's an error.
    raise ValueError("Unsupported type")

# This is the one that actually does
# the printing.  All other types convert
# their argument to a string and call this.
@count_down.register
def _(data_type: str):
    while data_type:
        print(data_type)
        data_type = data_type[:-1]

@count_down.register(int)
@count_down.register(float)
def _(data_type):
    count_down(str(data_type))

@count_down.register(list)
@count_down.register(set)
@count_down.register(tuple)
@count_down.register(range)
def _(data_type):
    count_down(''.join([str(d) for d in data_type]))

# For a dictionary count down the keys
@count_down.register
def _(data_type: dict):
    count_down(''.join([str(k) for k in data_type.keys()]))
