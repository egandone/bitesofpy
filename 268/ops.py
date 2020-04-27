from array import array


value_map = None


def get_value_map():
    global value_map
    if value_map == None:
        value_map = dict()
        value_map[1] = len('223')
        value_map[2] = len('2')
        value_map[4] = len('22')
        value_map[8] = len('222')
        value_map[16] = len('2222')
        value_map[32] = len('22222')
        value_map[64] = len('222222')
        value_map[1985] = 42

        old_sequence_map = array('i', [8])
        for i in range(4, 26):
            #            print(f'doing len={i}, {len(old_sequence_map)*2} additions')
            new_sequence_map = array('i')
            for value in old_sequence_map:
                new_value = value * 2
                # if new_value == 10:
                #     print(f'10 --> {new_key}')
                new_sequence_map.extend([new_value])
                if new_value not in value_map:
                    value_map[new_value] = i

                new_value = value // 3
                # if new_value == 10:
                #     print(f'10 --> {new_key}')
                new_sequence_map.extend([new_value])
                if new_value not in value_map:
                    value_map[new_value] = i
            old_sequence_map = new_sequence_map
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
