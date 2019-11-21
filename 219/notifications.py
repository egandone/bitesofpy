from datetime import date, timedelta

TODAY = date.today()


def gen_bite_planning(num_bites=1, num_days=1, start_date=TODAY):
    date_delta = timedelta(days=num_days)
    date = start_date + date_delta
    while True:
        for _ in range(0, num_bites):
            yield date
        date = date + date_delta
