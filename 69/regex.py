import re

def has_timestamp(text):
   """Return True if text has a timestamp of this format: 2014-07-03T23:30:37"""
   expr = r'\d\d\d\d-[0-1]\d-[0-2]\dT[0-2]\d:[0-5]\d:[0-6]\d'
   return re.search(expr, text) != None 

def is_integer(number):
   """Return True if number is an integer"""
   expr = r'^-*\d+$'
   return re.match(expr, str(number)) != None   

def has_word_with_dashes(text):
   """Returns True if text has one or more words with dashes"""
   expr = r'\w-\w'
   return re.search(expr, text) != None
   
def remove_all_parenthesis_words(text):
   """Return text but without any words or phrases in parenthesis:
       'Good morning (afternoon)' -> 'Good morning' (so don't forget
       leading spaces)"""
   expr = r'\s+\([^\)]*\)'
   return re.sub(expr, '', text)
   
def split_string_on_punctuation(text):
   """Split on ?!.,; - e.g. "hi, how are you doing? blabla" ->
       ['hi', 'how are you doing', 'blabla']
       (make sure you strip trailing spaces)"""
   expr = r'\s*[\?\!\.\,\;]\s*'
   return [s for s in re.split(expr, text) if len(s) > 0]

def remove_duplicate_spacing(text):
   """Replace multiple spaces by one space"""
   return re.sub(r'\s+', ' ', text)

def has_three_consecutive_vowels(word):
   """Returns True if word has at least 3 consecutive vowels"""
   expr = r'[aeiouyAEIOUY]{3,3}'
   return re.search(expr, word) != None

def convert_emea_date_to_amer_date(date):
   """Convert dd/mm/yyyy (EMEA date format) to mm/dd/yyyy
       (AMER date format)"""
   return re.sub(r'(\d\d)/(\d\d)/(\d\d\d\d)', r'\2/\1/\3', date)