IMPOSSIBLE = 'Mission impossible. No one can contribute.'


def max_fund(village):
    """Find a contiguous subarray with the largest sum."""
    # Hint: while iterating, you could save the best_sum collected so far
    # return total, starting, ending
    total = 0
    starting = 0
    ending = 0
    for start_index in range(len(village)):
        for end_index in range(start_index, len(village)):
            t = sum(village[start_index: end_index+1])
            if (t > total):
                total = t
                starting = start_index + 1
                ending = end_index + 1
    return total, starting, ending
