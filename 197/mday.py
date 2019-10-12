from datetime import date


def get_mothers_day_date(year):
    """Given the passed in year int, return the date Mother's Day
    is celebrated assuming it's the 2nd Sunday of May."""
    # Earliest on which the second Sunday can occur it 8th.
    # so, we just search for the first Snday that is on or
    # after the 8th
    d = date(year, 5, 8)
    while d.weekday() != 6:
        d = date(year, 5, d.day+1)
    return d
