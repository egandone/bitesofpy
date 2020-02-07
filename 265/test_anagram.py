import pytest
from random import choice

from anagram import Anagram, ClamyFernet

KEYS = (
    b"rvxePMSDUcZFowEaNxnFb8Pifn1KmhkF70Mz1ZQe2Bw=",
    b"2gODW4C4Lc7H9bjuuhPyn48HkVHriqa96P8lmstABo8=",
    b"mAbAfF5CW3EGlngOEEroDqtxlxVlJILzoUE4TJScMIw=",
)
MESSAGE = "This is my secret message"


@pytest.fixture(scope="function")
def rcf():
    password = b"#clamybite"
    key = choice(KEYS)
    return ClamyFernet(password, key)


@pytest.fixture(scope="module")
def cf():
    return ClamyFernet(key=KEYS[0])


def test_encrypt(cf):
    assert cf.iterations == 100_000
    assert len(cf.salt) == 16
    assert cf.length == 32
    token = cf.encrypt(MESSAGE)
    og_message = cf.decrypt(token)
    assert len(token) == 120
    assert isinstance(token, bytes)
    assert cf.key == KEYS[0]
    assert og_message == MESSAGE


def test_decrypt(rcf):
    token = rcf.encrypt(MESSAGE)
    og_message = rcf.decrypt(token)
    assert len(token) == 120
    assert isinstance(token, bytes)
    assert rcf.key in KEYS
    assert og_message == MESSAGE


def test_anagrams_props(cf):
    anagram = Anagram('', '')
    with pytest.raises(AttributeError):
        anagram.valid = False


def test_anagrams(cf):
    anagram = Anagram('adobe', 'abode')
    assert anagram.valid
    anagram = Anagram('A gentleman', 'Elegant man')
    assert anagram.valid
    anagram = Anagram('A gentleman', 'Elegant-man')
    assert anagram.valid
    anagram = Anagram('A gentleman', 'Elegant.man')
    assert anagram.valid
    anagram = Anagram('A gentleman', 'Elegant''man')
    assert anagram.valid
