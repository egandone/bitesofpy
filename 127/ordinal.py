def get_ordinal_suffix(number):
    """Receives a number int and returns it appended with its ordinal suffix,
       so 1 -> 1st, 2 -> 2nd, 4 -> 4th, 11 -> 11th, etc.

       Rules:
       https://en.wikipedia.org/wiki/Ordinal_indicator#English
       - st is used with numbers ending in 1 (e.g. 1st, pronounced first)
       - nd is used with numbers ending in 2 (e.g. 92nd, pronounced ninety-second)
       - rd is used with numbers ending in 3 (e.g. 33rd, pronounced thirty-third)
       - As an exception to the above rules, all the "teen" numbers ending with
         11, 12 or 13 use -th (e.g. 11th, pronounced eleventh, 112th,
         pronounced one hundred [and] twelfth)
       - th is used for all other numbers (e.g. 9th, pronounced ninth).
       """
    # Only care about the last two digits of the number
    last_two_digits = number % 100
    # Since th is the most common this is the default
    suffix = 'th'
    # Just ignore the teens
    if last_two_digits < 10 or last_two_digits > 20:
      # Outside of 11-19, only the last digit matters
      last_digit = last_two_digits % 10
      if last_digit == 1:
        suffix = 'st'
      elif last_digit == 2:
        suffix = 'nd'
      elif last_digit == 3:
        suffix = 'rd'
    return f'{number}{suffix}'
