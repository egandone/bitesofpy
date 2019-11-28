from datetime import datetime, timedelta
import json
import os
from pathlib import Path
from urllib.request import urlretrieve
from itertools import permutations

import pytest

from zodiac import (get_signs, get_sign_with_most_famous_people,
                    signs_are_mutually_compatible, get_sign_by_date)
from zodiac import Sign

# original source: https://zodiacal.herokuapp.com/api
URL = "https://bites-data.s3.us-east-2.amazonaws.com/zodiac.json"
TMP = os.getenv("TMP", "/tmp")
PATH = Path(TMP, "zodiac.json")


@pytest.fixture(scope='module')
def signs():
    if not PATH.exists():
        urlretrieve(URL, PATH)
    with open(PATH, encoding='utf-8') as f:
        data = json.loads(f.read())
    return get_signs(data)


def test_sign2():
    sign = Sign(name='name', compatibility='compatibility',
                famous_people='famous_people', sun_dates='sun_date')
    assert(sign.__class__.__name__ == 'Sign')


def test_sign():
    aries_json = json.loads('''[{ 
        "name": "Aries",
        "famous_people": ["Famous1", "Famous2"],
        "compatibility": ["Leo", "Sagittarius", "Gemini", "Aquarius"],
        "sun_dates": ["March 21", "April 19"]}]''')
    signs = get_signs(aries_json)
    assert(len(signs) == 1)
    assert(type(signs[0]) == Sign)
    assert(signs[0].name == 'Aries')
    assert(signs[0].compatibility == [
           'Leo', 'Sagittarius', 'Gemini', 'Aquarius'])
    assert(signs[0].famous_people == ['Famous1', 'Famous2'])
    assert(signs[0].sun_dates == ['March 21', 'April 19'])

    assert(get_signs([]) == [])


def test_get_sign_with_most_famous_people(signs):
    most_famous = get_sign_with_most_famous_people(signs)
    assert(most_famous == ('Scorpio', 35))


def test_get_sign_by_date(signs):
    tests = [('Aries', 'March 21', 'April 19'),
             ('Taurus', 'April 20', 'May 20'),
             ('Gemini', 'May 21', 'June 20'),
             ('Cancer', 'June 21', 'July 22'),
             ('Leo', 'July 23', 'August 22'),
             ('Virgo', 'August 23', 'September 22'),
             ('Libra', 'September 23', 'October 22'),
             ('Scorpio', 'October 23', 'November 21'),
             ('Sagittarius', 'November 22', 'December 21'),
             #             ('Capricorn', 'December 22', 'January 19'),
             ('Aquarius', 'January 20', 'February 18'),
             ('Pisces', 'February 19', 'March 20')]
    one_day = timedelta(days=1)
    for (sign, date1, date2) in tests:
        date1 = datetime.strptime(date1, '%B %d')
        date2 = datetime.strptime(date2, '%B %d')
        date3 = date1 + one_day
        assert(get_sign_by_date(signs, date1) == sign)
        assert(get_sign_by_date(signs, date2) == sign)
        assert(get_sign_by_date(signs, date3) == sign)


def test_signs_are_mutually_compatible(signs):
    all_signs = ['Aries',
                 'Taurus',
                 'Gemini',
                 'Cancer',
                 'Leo',
                 'Virgo',
                 'Libra',
                 'Scorpio',
                 'Sagittarius',
                 'Capricorn',
                 'Aquarius',
                 'Pisces']
    for (sign1, sign2) in permutations(all_signs, 2):
        assert(signs_are_mutually_compatible(signs, sign1, sign2) ==
               signs_are_mutually_compatible(signs, sign2, sign1))
