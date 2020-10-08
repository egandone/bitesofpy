from collections import namedtuple
from enum import Enum
from typing import Sequence

Suit = Enum("Suit", list("SHDC"))
Rank = Enum("Rank", list("AKQJT98765432"))
Card = namedtuple("Card", ["suit", "rank"])

HCP = {Rank.A: 4, Rank.K: 3, Rank.Q: 2, Rank.J: 1}
SSP = {2: 1, 1: 2, 0: 3}  # cards in a suit -> short suit points


class BridgeHand:
    def __init__(self, cards: Sequence[Card]):
        """
        Process and store the sequence of Card objects passed in input.
        Raise TypeError if not a sequence
        Raise ValueError if any element of the sequence is not an instance
        of Card, or if the number of elements is not 13
        """
        if not isinstance(cards, Sequence):
            raise TypeError
        if len(cards) != 13:
            raise ValueError
        for card in cards:
            if not isinstance(card, Card):
                raise ValueError
        self._cards = cards

    def __str__(self) -> str:
        """
        Return a string representing this hand, in the following format:
        "S:AK3 H:T987 D:KJ98 C:QJ"
        List the suits in SHDC order, and the cards within each suit in
        AKQJT..2 order.
        Separate the suit symbol from its cards with a colon, and
        the suits with a single space.
        Note that a "10" should be represented with a capital 'T'
        """
        suit_list = []
        for suit in Suit:
            card_str = ''
            for card in Rank:
                if (suit, card) in self._cards:
                    card_str += card.name
            if (card_str):
                suit_list.append(f'{suit.name}:{card_str}')
        return ' '.join(suit_list)

    @property
    def hcp(self) -> int:
        """ Return the number of high card points contained in this hand """
        hcp = 0
        hcp_cards = [c for c in self._cards if c[1] in HCP]
        for c in hcp_cards:
            hcp += HCP[c[1]]

        return hcp

    @property
    def doubletons(self) -> int:
        """ Return the number of doubletons contained in this hand """
        _doubletons = 0
        for suit in Suit:
            suit_count = len([c for c in self._cards if c[0] == suit])
            if suit_count == 2:
                _doubletons += 1
        return _doubletons

    @property
    def singletons(self) -> int:
        """ Return the number of singletons contained in this hand """
        _singletons = 0
        for suit in Suit:
            suit_count = len([c for c in self._cards if c[0] == suit])
            if suit_count == 1:
                _singletons += 1
        return _singletons

    @property
    def voids(self) -> int:
        """ Return the number of voids (missing suits) contained in
            this hand
        """
        _voids = 0
        for suit in Suit:
            suit_count = len([c for c in self._cards if c[0] == suit])
            if suit_count == 0:
                _voids += 1
        return _voids

    @property
    def ssp(self) -> int:
        """ Return the number of short suit points in this hand.
            Doubletons are worth one point, singletons two points,
            voids 3 points
        """
        return self.voids * 3 + self.singletons * 2 + self.doubletons

    @property
    def total_points(self) -> int:
        """ Return the total points (hcp and ssp) contained in this hand """
        return self.ssp + self.hcp

    @property
    def ltc(self) -> int:
        """ Return the losing trick count for this hand - see bite description
            for the procedure
        """
        _ltc = 0
        for suit in Suit:
            suit_cards = [c[1] for c in self._cards if c[0] == suit]
            ace = Rank['A'] in suit_cards
            king = Rank['K'] in suit_cards
            queen = Rank['Q'] in suit_cards
            if len(suit_cards) == 1:
                if not ace:
                    _ltc += 1
            elif len(suit_cards) == 2:
                if ace and king:
                    pass
                elif ace or king:
                    _ltc += 1
                else:
                    _ltc += 2
            elif len(suit_cards) >= 3:
                if ace and king and queen:
                    pass
                elif (ace and king) or (ace and queen) or (king and queen):
                    _ltc += 1
                elif ace or king or queen:
                    _ltc += 2
                else:
                    _ltc += 3
        return _ltc
