import itertools
   
def two_sums(numbers, target):
    """Finds the indexes of the two numbers that add up to target.

    :param numbers: list - random unique numbers
    :param target: int - sum of two values from numbers list
    :return: tuple - (index1, index2) or None
    """
    result = None
    # Find all the pairs where the sum of the two numbers add to the
    # target number.  The itertools.combinations() function just creates
    # a list of all index pairs for the numbers list.  For example, if
    # numbers is a list of 5 numbers then the call to combinations(range(5), 2)
    # will produce [(0, 1), (0, 2), (0, 3), (0, 4), 
    #                       (1, 2), (1, 3), (1, 4), 
    #                               (2, 3), (2, 4), 
    #                                       (3, 4)]
    found_pairs = [pair for pair in itertools.combinations(range(len(numbers)), 2) if numbers[pair[0]] + numbers[pair[1]] == target]
    if found_pairs:
        # Now to handle to case where we get multiple results we just
        # sort the list based on the first number.
        found_pairs.sort(key=lambda pair: numbers[pair[0]])
        result = found_pairs[0]

    return result