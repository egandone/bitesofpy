from datetime import timedelta
def get_missing_dates(dates):
    """Receives a range of dates and returns a sequence
       of missing datetime.date objects (no worries about order).

       You can assume that the first and last date of the
       range is always present (assumption made in tests).

       See the Bite description and tests for example outputs.
    """
    one_day = timedelta(days=1)
    d = min(dates)
    missing_dates = []
    while d < max(dates):
        d += one_day
        if d not in dates:
            missing_dates.append(d)
    return missing_dates