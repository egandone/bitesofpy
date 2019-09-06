from functools import wraps


DEFAULT_TEXT = ('Subscribe to our blog (sidebar) to periodically get '
                'new PyBites Code Challenges (PCCs) in your inbox')
DOT = '.'


def strip_range(start, end):
    """Decorator that replaces characters of a text by dots, from 'start'
       (inclusive) to 'end' (exclusive) = like range.

        So applying this decorator on a function like this and 'text'
        being 'Hello world' it would convert it into 'Hel.. world' when
        applied like this:

        @strip_range(3, 5)
        def gen_output(text):
            return text
    """
    def strip_range_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            str = func(*args, **kwargs)
            replacement = ''
            for i,c in enumerate(str):
                if i in range(start,end):
                    replacement += '.'
                else:
                    replacement += c
            return replacement
        return wrapper
    return strip_range_decorator