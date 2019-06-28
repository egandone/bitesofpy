import re

def get_weekdays(calendar_output):
   """Receives a multiline Unix cal output and returns a mapping (dict) where
       keys are int days and values are the 2 letter weekdays (Su Mo Tu ...)"""
   # This breaks the calendar output into lines
   weeks = calendar_output.split('\n')
   # The day names (ie., 'Su', 'Mo', ...) are the second line
   day_names = weeks[1].split()
   # Create an empty result to accumulate results 
   day_mappings = dict()
   # All the dates are in rows 3 to the end
   for week in weeks[2:]:
      # Split each line into array of dates.  Examples:
      #     '          1  2  3  4' -> ['', '', '', '1', '2', '3', '4']
      #     '12 13 14 15 16 17 18' -> ['12', '13', '14', '15', '16', '17', '18']
      #     '26 27 28 29 30'       -> ['26', '27', '28', '29', '30']
      # Each date is 3 characters, except the one at the end of the line
      # Hence, the use the or and the $
      days = [day.strip() for day in re.findall(r'..\s|..$', week)]

      # Create a dictionary for the week from a zipped together 
      # tuples of week day names ('Su', 'Mo', ...) to 
      # day number (['', '', '', '1', '2', '3', '4']). But only of
      # the day number is not blank.  Examples,
      #    ['', '', '', '1', '2', '3', '4']           ->                               { 1: 'We',  2: 'Th',  3: 'Fr',  4: 'Sa'} 
      #    ['12', '13', '14', '15', '16', '17', '18'] -> {12: 'Su', 13: 'Mo', 14: 'Tu', 15: 'We', 16: 'Th', 17: 'Fr', 18: 'Sa'}
      #    ['26', '27', '28', '29', '30']             -> {26: 'Su', 27: 'Mo', 28: 'Tu', 29: 'We', 30: 'Th'}
      week_mappings = {int(d):n for (n,d) in zip(day_names, days) if d}

      # Append the mappings for this week to the overall mapping
      day_mappings.update(week_mappings)
      
   return day_mappings
      
   