import pandas as pd


def series_simple_math(
    ser: pd.Series, function: str, number: int
) -> pd.core.series.Series:
    """Write some simple math helper functions for series.
    Take the given series, perfrom the required operation and
        return the new series.
    For example. Give the series:
        0    0
        1    1
        2    2
        dtype: int64
    Function 'add' and 'number' 2 you should return
        0     2
        1     3
        2     4
        dtype: int64
    :param ser: Series to perform operation on
    :param function: The operation to perform
    :param number: The number to apply the operation to
    """
    if function == 'add':
        return ser.apply(lambda x: x + number)
    elif function == 'sub':
        return ser.apply(lambda x: x - number)
    elif function == 'mul':
        return ser.apply(lambda x: x * number)
    elif function == 'div':
        return ser.apply(lambda x: x / number)
    else:
        raise ValueError(
            f'{function} is not a valid function.  Must be one of add,sub,mul,div.')


def complex_series_maths(
    ser_01: pd.Series, ser_02: pd.Series, function: str
) -> pd.core.series.Series:
    """Write some math helper functions for series.
    Take the two given series, perfrom the required operation and
        return the new series.
    For example. Give the series:
        0    0
        1    1
        2    2
        dtype: int64

    And the series:
        0     2
        1     3
        2     4
        dtype: int64

    If the function given is 'add' you should return
        0     2
        1     4
        2     6
        dtype: int64

    :param ser_01: Primary series to perform operation on
    :param ser_02: Secondary series to perform operation on
    :param function: The operation to perform

    Note:
    For this function always add ser_02 to ser_01,
        subtract ser_02 from ser_01,
        multiply ser_01 by ser_02,
        divide ser_01 by ser_02
    Don't worry about None's and NaN and divide by zero.
        Let pandas do the work for you.
    """
    if function == 'add':
        return ser_01 + ser_02
    elif function == 'sub':
        return ser_01 - ser_02
    elif function == 'mul':
        return ser_01 * ser_02
    elif function == 'div':
        return ser_01 / ser_02
    else:
        raise ValueError(
            f'{function} is not a valid function.  Must be one of add,sub,mul,div.')


def create_series_mask(ser: pd.Series, mask: list) -> pd.core.series.Series:
    """Write a trivial function to create a pandas series mask of a list
    of letters.
    Be careful, although this sounds very similar to the .mask() method,
        that's not what we're looking for here.
    For example. Give the series x:
        0    0
        1    1
        2    2
        3    3
        4    4
        dtype: int64

    You can create a mask for even numbers like this:
    >>> mask = x % 2 == 0
    >>> mask
        0     True
        1    False
        2     True
        3    False
        4     True
        dtype: bool

    And then apply the mask:
    >>> x[mask]
        0    0
        2    2
        4    4
        dtype: int64

    Of course for simpler masks you can just do this:
    >>> x[x %2 == 0]
        0    0
        2    2
        4    4
        dtype: int64

    :param ser: Series to perform operation on
    :param mask: The list of letters to be masked
    """
    return ser.apply(lambda x: x in mask)


def custom_series_function(ser: pd.Series,
                           within: int) -> pd.core.series.Series:
    """A more challenging mask to apply.
    When passed a series of floats, return all values
        within the given range of:
         - the minimum value
         - the 1st quartile value
         - the second quartile value
         - the mean
         - the third quartile value
         - the maximum value
    You may want to brush up on some simple statistics to help you here.
    Also, the series is passed to you sorted assending.
        Be sure that you don't return values out of sequence.

    So, for example if your mean is 5.0 and within is 0.1
        return all value between 4.9 and 5.1 inclusive

    :param ser: Series to perform operation on
    :param within: The value to calculate the range of number within
    """
    min = ser.min()
    q1 = ser.quantile(0.25)
    q2 = ser.quantile(0.5)
    q3 = ser.quantile(0.75)
    max = ser.max()
    mean = ser.mean()
    mask = ser.apply(lambda x: x in [min, max]
                     or
                     ((x >= q1 - within) and (x <= q1 + within))
                     or
                     ((x >= q2 - within) and (x <= q2 + within))
                     or
                     ((x >= q3 - within) and (x <= q3 + within))
                     or
                     ((x >= mean - within) and (x <= mean + within)))
    return ser[mask]
