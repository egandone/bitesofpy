from datetime import date, timedelta

TODAY = date(year=2018, month=11, day=29)

def get_hundred_weekdays(start_date=TODAY):
   """Return a list of hundred date objects starting from
      start_date up till 100 weekdays later, so +100 days
      skipping Saturdays and Sundays"""
   days = []
   day = start_date
   one_day = timedelta(days=1)

   while len(days) < 100:
      if day.isoweekday() < 6:
         days.append(day)
      day += one_day
   return days
      