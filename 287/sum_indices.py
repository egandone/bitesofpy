from typing import List


def sum_indices(items: List[str]) -> int:
    index_dict = dict()
    s = 0
    for i, v in enumerate(items):
        if v in index_dict:
            index_dict[v].append(i)
            s += sum(index_dict[v])
        else:
            index_dict[v] = [i]
            s += i
    return s
