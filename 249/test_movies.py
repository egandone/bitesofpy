import os
import random
import string

import pytest

from movies import MovieDb

salt = ''.join(
    random.choice(string.ascii_lowercase) for i in range(20)
)
DB = os.path.join(os.getenv("TMP", "/tmp"), f'movies_{salt}.db')
# https://www.imdb.com/list/ls055592025/
DATA = [
    ("The Godfather", 1972, 9.2),
    ("The Shawshank Redemption", 1994, 9.3),
    ("Schindler's List", 1993, 8.9),
    ("Raging Bull", 1980, 8.2),
    ("Casablanca", 1942, 8.5),
    ("Citizen Kane", 1941, 8.3),
    ("Gone with the Wind", 1939, 8.1),
    ("The Wizard of Oz", 1939, 8),
    ("One Flew Over the Cuckoo's Nest", 1975, 8.7),
    ("Lawrence of Arabia", 1962, 8.3),
]
TABLE = 'movies'


@pytest.fixture
def db():
    # instantiate MovieDb class using above constants
    # do proper setup / teardown using MovieDb methods
    # https://docs.pytest.org/en/latest/fixture.html (hint: yield)
    db = MovieDb(DB, DATA, TABLE)
    db.init()
    yield db
    db.drop_table()

# write tests for all MovieDb's query / add / delete


def test_create_delete():
    db = MovieDb(DB, DATA, TABLE)
    db.init()
    db.drop_table()


def test_query(db):
    results = db.query(title='The Godfather')
    assert len(results) == 1
    results = db.query(year=1939)
    assert len(results) == 2
    results = db.query(score_gt=9)
    assert len(results) == 2
#    results = db.query(title='Gone with the Wind', year=1939, score_gt=8)
#    assert len(results) == 1


def test_add(db):
    results = db.query()
    assert len(results) == 10
    db.add('Green Lantern', 2011, 5.5)
    results = db.query()
    assert len(results) == 11


def test_delete(db):
    results = db.query()
    assert len(results) == 10
    db.delete(results[0][0])
    results = db.query()
    assert len(results) == 9
