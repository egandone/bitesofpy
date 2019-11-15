def countdown():
    """Write a generator that counts from 100 to 1"""
    c = 100
    while c > 0:
        yield c
        c -= 1