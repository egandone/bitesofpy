from typing import Dict


def decompress(string: str, table: Dict[str, str]) -> str:
    result = string
    while result and (set(table.keys()).intersection(set(result))):
        new_result = ''
        for c in result:
            if c in table:
                new_result += table[c]
            else:
                new_result += c
        result = new_result

    return result
