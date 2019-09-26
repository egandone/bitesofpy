from difflib import SequenceMatcher
from os import path
from urllib.request import urlretrieve
from tempfile import tempdir

DICTIONARY = path.join(tempdir, 'dictionary.txt')
if not path.isfile(DICTIONARY):
    urlretrieve('http://bit.ly/2iQ3dlZ', DICTIONARY)

def load_words():
    """Return a set of words from DICTIONARY"""
    with open(DICTIONARY) as f:
        return {word.strip().lower() for word in f.readlines()}

def suggest_word(misspelled_word: str, words: set = None) -> str:
    """Return a valid alternative word that best matches
       the entered misspelled word"""
    if words is None:
        words = load_words()
    ratings = [(word, SequenceMatcher(None, misspelled_word, word).ratio()) for word in words]
    best_rated = max(ratings, key=lambda pair: pair[1])
    return best_rated[0]


    