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
    # Only match a char if it's followed by n iterations of itself
    expr = f'(.)(?=\\1{{{n}}})'
    pattern = re.compile(expr,  re.DOTALL)
    return len(pattern.findall(text))


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
    # '\1{n}' --> n iterations of what was matched by (.)
    # '{re.escape(char)}{n}' --> n iterations of the fixed char.
    #                            re.escape() handles any special characters, eg. '?' -> '\?'
    expr = f'(.)(?=(\\1{{{n}}}|{re.escape(char)}{{{n}}}))'
    pattern = re.compile(expr,  re.DOTALL)
    return len(pattern.findall(text))


def check_surrounding_chars(text, surrounding_chars):
    """
    Count the number of times a character is surrounded by
    characters from the surrounding_chars list.

    text: UTF-8 compliant input text
    surrounding_chars: List of characters
    """
    # Build the concatenated list of specified chars, use re.escape() to handle special chars.
    escaped_chars = ''.join([re.escape(c) for c in surrounding_chars])
    # '(?<=[{escaped_chars}])' --> match if preceeded by any of the surrounding chars
    # '(?=[{escaped_chars}])' --> match only if followed by any of the special chars
    expr = f'(?<=[{escaped_chars}]).(?=[{escaped_chars}])'
    pattern = re.compile(expr, re.DOTALL)
    return len(pattern.findall(text))
