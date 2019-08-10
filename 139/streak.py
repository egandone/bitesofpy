from datetime import datetime, timedelta, date
import re

TODAY = date(2018, 11, 12)

def extract_dates(data):
    """Extract unique dates from DB table representation as shown in Bite"""
    dates = set()
    # Just chop up the data into words and look for anything
    # that matches the pattern for a date.
    for element in data.split():
      m = re.match(r'(\d\d\d\d)-(\d\d)-(\d\d)', element)
      if m:
         year = int(m.group(1))
         month = int(m.group(2))
         day = int(m.group(3))
         d = date(year, month, day)
         dates.add(d)
    return dates


def calculate_streak(dates):
   """Receives sequence (set) of dates and returns number of days
       on coding streak.

       Note that a coding streak is defined as consecutive days coded
       since yesterday, because today is not over yet, however if today
       was coded, it counts too of course.

       So as today is 12th of Nov, having dates 11th/10th/9th of Nov in
       the table makes for a 3 days coding streak.

       See the tests for more examples that will be used to pass your code.
   """
   # Start the streak a 0 or 1 depending if work has been done today
   streak = 1 if TODAY in dates else 0

   # Then just keep walking back a day at a time and incrementing
   # the streak until the date is not found.
   one_day = timedelta(days=1)
   d = TODAY - one_day
   while d in dates:
      streak += 1
      d = d - one_day
   return streak