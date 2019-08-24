from medals import athletes_most_medals


def test_athletes_most_medals():
    ret = athletes_most_medals()
    larisa = "LATYNINA, Larisa"
    michael = "PHELPS, Michael"

    assert larisa in ret
    assert ret[larisa] == 18

    assert michael in ret
    assert ret[michael] == 22