from collections import namedtuple, Counter
import csv
import re

import requests

MARVEL_CSV = 'https://raw.githubusercontent.com/pybites/marvel_challenge/master/marvel-wikia-data.csv'  # noqa E501

Character = namedtuple('Character', 'pid name sid align sex appearances year')


# csv parsing code provided so this Bite can focus on the parsing

def _get_csv_data():
    """Download the marvel csv data and return its decoded content"""
    with requests.Session() as session:
        return session.get(MARVEL_CSV).content.decode('utf-8')


def load_data():
    """Converts marvel.csv into a sequence of Character namedtuples
       as defined above"""
    content = _get_csv_data()
    reader = csv.DictReader(content.splitlines(), delimiter=',')
    for row in reader:
        name = re.sub(r'(.*?)\(.*', r'\1', row['name']).strip()
        yield Character(pid=row['page_id'],
                        name=name,
                        sid=row['ID'],
                        align=row['ALIGN'],
                        sex=row['SEX'],
                        appearances=row['APPEARANCES'],
                        year=row['Year'])


data = list(load_data())


# start coding

def most_popular_characters(top=5):
    """Get the most popular character by number of appearances,
       return top n characters (default 5)"""
    character_appearances = {}
    for character in data:
        if character.appearances:
            count = int(character.appearances)
            if character.name not in character_appearances or count > character_appearances[character.name]:
               character_appearances[character.name] = count
    top_appearances = sorted(character_appearances.items(), key=lambda kv: kv[1], reverse=True)[:top]
    return [appearance[0] for appearance in top_appearances]

def max_and_min_years_new_characters():
    """Get the year with most and least new characters introduced respectively,
       use either the 'FIRST APPEARANCE' or 'Year' column in the csv data, or
       the 'year' attribute of the namedtuple, return a tuple of
       (max_year, min_year)"""
    first_appearances = {}
    for character in data:
        if character.year:
            year = int(character.year)
            if character.name not in first_appearances or year < first_appearances[character.name]:
               first_appearances[character.name] = year
    first_year_counter = Counter(first_appearances.values())
    most = first_year_counter.most_common(1)[0]
    least = first_year_counter.most_common()[-1]
    return (str(most[0]), str(least[0]))

def percentage_female():
    """Get the percentage of female characters as percentage of all characters, rounded to 2 digits"""
    gender_counter = Counter([c.sex for c in data])
    total_count = sum([gender[1] for gender in gender_counter.most_common()])
    female_count = gender_counter['Female Characters']
    return round(female_count / total_count * 100.0, 2)