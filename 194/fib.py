from functools import lru_cache


@lru_cache(maxsize=None)
def cached_fib(n):
    if (n <= 1):
        return n
    else:
        return cached_fib(n-1) + cached_fib(n-2)


if __name__ == '__main__':
    print(cached_fib(50))
