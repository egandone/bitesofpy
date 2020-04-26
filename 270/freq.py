from collections import Counter


def freq_digit(num: int) -> int:
    # Just convert the number to a string of digits and
    # use a collections.Counter to figure out the most common
    digit_counter = Counter(str(num))
    # Since Counter preserves the list in the order the
    # elements were encountered, if we have a tie then
    # the first one will return the one we want.  That
    # is, no need to do any special handing if there is a tie.
    return int(digit_counter.most_common()[0][0])
