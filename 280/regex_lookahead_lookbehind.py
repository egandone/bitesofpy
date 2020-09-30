import re


def count_n_repetitions(text, n=1):
    """
    Counts how often characters are followed by themselves for
    n times.

    text: UTF-8 compliant input text
    n: How often character should be repeated, defaults to 1
    """
    if n < 1:
        return 0
    expr = f'(.)\\1{{{n}}}'
    pattern = re.compile(expr,  re.DOTALL)
    p = 0
    count = 0
    while p < len(text):
        m = pattern.search(text, p)
        if m:
            p = m.start() + 1
            count += 1
        else:
            p = len(text)
    return count


def count_n_reps_or_n_chars_following(text, n=1, char=""):
    """
    Counts how often characters are repeated for n times, or
    followed by char n times.

    text: UTF-8 compliant input text
    n: How often character should be repeated, defaults to 1
    char: Character which also counts if repeated n times
    """
    if n < 1:
        return 0
    if not char:
        return count_n_repetitions(text, n)
    if char in ['?', '[', ']', '^']:
        char = '\\' + char
    expr = f'(.)(\\1{{{n}}}|{char}{{{n}}})'
    pattern = re.compile(expr,  re.DOTALL)
    p = 0
    count = 0
    while p < len(text):
        m = pattern.search(text, p)
        if m:
            p = m.start() + 1
            count += 1
        else:
            p = len(text)
    return count


def check_surrounding_chars(text, surrounding_chars):
    """
    Count the number of times a character is surrounded by
    characters from the surrounding_chars list.

    text: UTF-8 compliant input text
    surrounding_chars: List of characters
    """
