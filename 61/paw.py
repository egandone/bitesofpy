from collections import namedtuple
import random
import itertools

LETTERS = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
ACTIONS = ['draw_card', 'play_again',
           'interchange_cards', 'change_turn_direction']
NUMBERS = range(1, 5)

PawCard = namedtuple('PawCard', 'card action')

def create_paw_deck(n=8):
    if n > 26:
        raise ValueError('n must be less then 27')
        
    cards = [(letter, number) for letter, number in itertools.product(LETTERS[:n], NUMBERS)]
    random.shuffle(cards)

    deck = []
    for index, card in enumerate(cards):
        action = None
        if not (index % 4) :
            action = ACTIONS[random.randint(0,3)]
        deck.append(PawCard(card=f'{card[0]}{card[1]}', action=action))
    return deck
    