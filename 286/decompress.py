from typing import Dict


def decompress(string: str, table: Dict[str, str]) -> str:
    if (string):
        key_set = set(table.keys())
        # Keep iterating while the updated string still contains any
        # characters that should be replaced.
        while key_set.intersection(set(string)):
            for k, v in table.items():
                string = string.replace(k, v)

    return string
