from pathlib import Path
from urllib.request import urlretrieve

from dateutil.parser import parse

# get the data
tmp = Path('/tmp')
base_url = 'https://bites-data.s3.us-east-2.amazonaws.com/'

fathers_days_countries = tmp / 'fathers-day-countries.txt'
fathers_days_recurring = tmp / 'fathers-day-recurring.txt'

for file_ in (fathers_days_countries, fathers_days_recurring):
    if not file_.exists():
        urlretrieve(base_url + file_.name, file_)

def _get_content_lines(filename):
    """Function to read file and return lines that are
       not blank and not comments"""
    with open(filename) as f: 
        return [l.strip() for l in f.readlines() if len(l.strip()) > 0 and l.strip()[0] != '#']  

def _parse_countries(l):
    words = [c.strip() for c in l.replace('and ', ',').split(',')]
    return [w for w in words if len(w) > 0]
    
    
def _parse_father_days_per_country(year, filename=fathers_days_countries):
    """Helper to parse fathers_days_countries"""
    dates = dict()
    countries = None
    for l in _get_content_lines(filename):
        # 
        if l[0] == '*':
            countries = _parse_countries(l[1:])
        else:
            if countries and l.startswith(str(year)):
                date = parse(l[5:].strip()).date()
                dates[date] = countries
    return dates



def _parse_recurring_father_days(filename=fathers_days_recurring):
    """Helper to parse fathers_days_recurring"""
    dates = dict()
    date = None
    for l in _get_content_lines(filename):
        if l[0] == '*':
            date = parse(l[1:].strip()).date()
            dates[date] = []
        elif date:
            dates[date].append(l.strip())
    return dates

def get_father_days(year=2020):
    """Returns a dictionary of keys = dates and values = lists
       of countries that celebrate Father's day that date

       Consider using the the 2 _parse* helpers.
    """
    dates = _parse_father_days_per_country(year)
    for (date, countries) in _parse_recurring_father_days().items():
        if date in dates:
            dates[date].extend(countries)
        else:
            dates[date] = countries
    father_days = dict()
    for date in dates:
        father_days[f'{date:%B %-d}'] = dates[date]
    return father_days


def generate_father_day_planning(father_days=None):
    """Prints all father days in order, example in tests and
       Bite description
    """
    if father_days is None:
        father_days = get_father_days()


    for day in sorted(father_days, key=lambda d: parse(d)):
        print(day)
        for country in father_days[day]:
            print(f'- {country}')
        print()   

if __name__ == '__main__':
    generate_father_day_planning() 