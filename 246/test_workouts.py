import pytest

from workouts import print_workout_days, WORKOUTS

test_workouts = {'mon': 'monday gym',
                 'tue': 'Tuesday gym',
                 'wed': 'MIDWEEK workout',
                 'thu': 'thursday stuff',
                 'fri': 'take it easy'}


def test_print_workout_days(capsys):
    # Check
    test_cases = {value: key for key, value in WORKOUTS.items()}
    for wo in test_cases:
        print_workout_days(wo)
        assert capsys.readouterr().out.lower(
        ).strip() == test_cases[wo].lower()
        print_workout_days(wo.upper())
        assert capsys.readouterr().out.lower(
        ).strip() == test_cases[wo].lower()
        print_workout_days(wo.capitalize())
        assert capsys.readouterr().out.lower(
        ).strip() == test_cases[wo].lower()

    print_workout_days('couch')
    assert capsys.readouterr().out == 'No matching workout\n'

    print_workout_days('body')
    assert capsys.readouterr().out == 'Mon, Tue, Thu, Fri\n'

    print_workout_days('cardio')
    assert capsys.readouterr().out == 'Wed\n'


def test_print_workout_days_custom(capsys):
    test_workouts = {'mon': 'spin',
                     'tue': 'weights',
                     'wed': 'spin',
                     'thu': 'rowing',
                     'fri': 'spin'}
    print_workout_days('spin', test_workouts)
    assert capsys.readouterr().out == 'Mon, Wed, Fri\n'
