import re
VOWELS = 'aeiou'

def get_word_max_vowels(text):
   """Get the case insensitive word in text that has most vowels.
       Return a tuple of the matching word and the vowel count, e.g.
       ('object-oriented', 6)"""
   
   vowel_locator = re.compile(f'[{VOWELS}]')
   vowel_counts = [(w, len(vowel_locator.findall(w))) for w in text.split()]
   vowel_counts = sorted(vowel_counts, key=lambda t: t[1], reverse=True)
   return vowel_counts[0]