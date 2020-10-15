from typing import Dict, Any


def rename_keys(data: Dict[Any, Any]) -> Dict[Any, Any]:
    result = dict()
    for key, item in data.items():
        if isinstance(key, str) and key.startswith('@'):
            new_key = key[1:]
        else:
            new_key = key
        if isinstance(item, dict):
            new_item = rename_keys(item)
        elif isinstance(item, list):
            new_item = []
            for i in item:
                if isinstance(i, dict):
                    new_item.append(rename_keys(i))
                else:
                    new_item.append(i)
        else:
            new_item = item
        result[new_key] = new_item
    return result
