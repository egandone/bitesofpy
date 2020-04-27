from array import array


value_map = None


def get_value_map():
    global value_map
    if value_map == None:
        value_map = dict()

        # Initialize the set of generated numbers
        # with 1 (i.e., sequence length = 0)
        old_sequence_set = set([1])
        for sequence_length in range(1, 50):
            # This set will contain all the generated numbers
            # after adding one operation.
            new_sequence_set = set()
            for value in old_sequence_set:
                new_value = value * 2
                new_sequence_set.add(new_value)
                if new_value not in value_map:
                    value_map[new_value] = sequence_length

                new_value = value // 3
                new_sequence_set.add(new_value)
                if new_value not in value_map:
                    value_map[new_value] = sequence_length
            old_sequence_set = new_sequence_set
    return value_map


def num_ops(n):
    """
    Input: an integer number, the target number
    Output: the minimum number of operations required to reach to n from 1.

    Two operations rules:
    1.  multiply by 2
    2.  int. divide by 3

    The base number is 1. Meaning the operation will always start with 1
    These rules can be run in any order, and can be run independently.

    [Hint] the data structure is the key to solve it efficiently.
    """
    # you code
    return get_value_map()[n]
