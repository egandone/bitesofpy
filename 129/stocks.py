import requests
from collections import Counter

STOCK_DATA = 'https://bit.ly/2MzKAQg'

# pre-work: load JSON data into program

with requests.Session() as s:
    data = s.get(STOCK_DATA).json()


# your turn:

def _cap_str_to_mln_float(cap):
    """If cap = 'n/a' return 0, else:
       - strip off leading '$',
       - if 'M' in cap value, strip it off and return value as float,
       - if 'B', strip it off and multiple by 1,000 and return
         value as float"""
    cap_value = 0.0
    mult = 1.0
    if not cap == 'n/a':
        if cap[0] == '$':
            cap = cap[1:]
        if cap[-1] == 'M':
            cap = cap[:-1]
        elif cap[-1] == 'B':
            cap = cap[:-1]
            mult = 1000.0
        cap_value = float(cap) * mult
    return cap_value


def get_industry_cap(industry):
    """Return the sum of all cap values for given industry, use
       the _cap_str_to_mln_float to parse the cap values,
       return a float with 2 digit precision"""
    industry_sum = sum([_cap_str_to_mln_float(stock['cap']) for stock in data if stock['industry'] == industry])
    return round(industry_sum, 2)

def get_stock_symbol_with_highest_cap():
    """Return the stock symbol (e.g. PACD) with the highest cap, use
       the _cap_str_to_mln_float to parse the cap values"""
    sorted_stocks = sorted(data, key=lambda stock: _cap_str_to_mln_float(stock['cap']), reverse=True)
    return sorted_stocks[0]['symbol']

def get_sectors_with_max_and_min_stocks():
    """Return a tuple of the sectors with most and least stocks,
       discard n/a"""
    all_sectors = [stock['sector'] for stock in data if not stock['sector'] == 'n/a']
    sector_counter = Counter(all_sectors).most_common()
    return (sector_counter[0][0], sector_counter[-1][0])