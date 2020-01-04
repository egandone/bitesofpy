from unittest.mock import patch

import pytest

from guess import GuessGame, InvalidNumber
import builtins


def test_basic_good_game(capsys):
    game = GuessGame(5)
    with patch.object(builtins, 'input', side_effect=['1', '9', 'a', '5']):
        game()
    lines = [line for line in capsys.readouterr().out.split('\n') if line]
    assert lines == ['Guess a number: ', 'Too low',
                     'Guess a number: ', 'Too high',
                     'Guess a number: ', 'Enter a number, try again',
                     'Guess a number: ', 'You guessed it!']


def test_basic_bad_game(capsys):
    game = GuessGame(5)
    with patch.object(builtins, 'input', side_effect=['1', '2', '6', '7', '9']):
        game()
    lines = [line for line in capsys.readouterr().out.split('\n') if line]
    assert lines == ['Guess a number: ', 'Too low',
                     'Guess a number: ', 'Too low',
                     'Guess a number: ', 'Too high',
                     'Guess a number: ', 'Too high',
                     'Guess a number: ', 'Too high', 'Sorry, the number was 5']


def test_bad_game_definitions():
    with pytest.raises(InvalidNumber, match='Not a number'):
        GuessGame('not a number')

    with pytest.raises(InvalidNumber, match='Negative number'):
        GuessGame(-10)

    with pytest.raises(InvalidNumber, match='Number too high'):
        GuessGame(16)

    # Check that 0 is OK for a number
    assert GuessGame(0)
    # Check that 15 is OK for a number
    assert GuessGame(15)
