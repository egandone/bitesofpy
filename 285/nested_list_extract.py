import re


def flatten_list(data):
    flat_list = []
    if isinstance(data, list):
        for d in data:
            flat_list.extend(flatten_list(d))
    else:
        flat_list.append(data)
    return flat_list


def extract_ipv4(data):
    """
    Given a nested list of data return a list of IPv4 address information that can be extracted
    """
    results = []
    flattened_data = flatten_list(data)
    addr, mask = None, None
    for i, v in enumerate(flattened_data):
        if v == 'ip' and (i < len(flattened_data) - 1):
            addr = flattened_data[i+1]
            if addr:
                addr = addr.strip('"')
        elif v == 'mask' and (i < len(flattened_data) - 1):
            mask = flattened_data[i+1]
        if addr and mask:
            if re.match(r'\d+\.\d+\.\d+\.\d+', addr) and (isinstance(mask, int) or re.match(r'\d+', mask)):
                results.append((addr, str(mask)))
            addr, mask = None, None
    return results
