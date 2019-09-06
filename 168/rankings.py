from dataclasses import dataclass
from typing import List, Tuple
from functools import total_ordering

bites: List[int] = [283, 282, 281, 263, 255, 230, 216, 204, 197, 196, 195]
names: List[str] = [
    "snow",
    "natalia",
    "alex",
    "maquina",
    "maria",
    "tim",
    "kenneth",
    "fred",
    "james",
    "sara",
    "sam",
]


@dataclass
@total_ordering
class Ninja:
    """
    The Ninja class will have the following features:

    string: name
    integer: bites
    support <, >, and ==, based on bites
    print out in the following format: [469] bob
    """
    def __init__(self, name, bites):
        self._name = name
        self._bites = bites

    @property
    def name(self):
        return self._name

    @property
    def bites(self):
        return self._bites
            
    def __str__(self):
        return f'[{self._bites}] {self._name}'

    def __repr__(self):
        return f'[{self._bites}] {self._name}'

    def __eq__(self, other):
        return self._bites == other.bites and self._name == other.name

    def __lt__(self, other):
        return self._bites < other.bites


@dataclass
class Rankings:
    """
    The Rankings class will have the following features:

    method: add() that adds a Ninja object to the rankings
    method: dump() that removes/dumps the lowest ranking Ninja from Rankings
    method: highest() returns the highest ranking Ninja, but it takes an optional
            count parameter indicating how many of the highest ranking Ninjas to return
    method: lowest(), the same as highest but returns the lowest ranking Ninjas, also
            supports an optional count parameter
    returns how many Ninjas are in Rankings when len() is called on it
    method: pair_up(), pairs up study partners, takes an optional count
            parameter indicating how many Ninjas to pair up
    returns List containing tuples of the paired up Ninja objects
    """
    def __init__(self):
        self._rankings = []

    def add(self, ninja):
        self._rankings.append(ninja)
        self._rankings.sort()

    def dump(self):
        d = self._rankings[0]
        self._rankings.remove(d)
        return d

    def highest(self, count=1):
        return self._rankings[:-(count+1):-1]

    def lowest(self, count=1):
        return self._rankings[:count]

    def __len__(self):
        return len(self._rankings)

    def pair_up(self, count=3):
        return [pair for pair in zip(self.highest(count), self.lowest(count))]