from collections import Counter
import re
import string


def password_complexity(password):
    """Input: password string, calculate score according to 5 criteria in bite,
       return: score int"""
    lower_case = re.search('[a-z]+', password)
    upper_case = re.search('[A-Z]+', password)

    score = 0
    if lower_case and upper_case:
       score = score + 1

    numbers = re.search('[0-9]+', password)
    if (lower_case or upper_case) and numbers:
       score = score + 1

    special = re.search(r'[' + re.escape(r'"@!#$%&''*+-.^_`|~:') + ']+', password) 
    if special:
       score = score + 1

    if (len(password.strip()) >= 8):
       score = score + 1       
       repeat_search = re.search(r'([a-zA-Z0-9"@!#$%&])\1{1,}', password)
       if not repeat_search:
         score = score + 1

    return score
    