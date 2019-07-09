# nice snippet: https://gist.github.com/tonybruess/9405134
from collections import namedtuple
import re

social_platforms = """Twitter
  Min: 1
  Max: 15
  Can contain: a-z A-Z 0-9 _

Facebook
  Min: 5
  Max: 50
  Can contain: a-z A-Z 0-9 .

Reddit
  Min: 3
  Max: 20
  Can contain: a-z A-Z 0-9 _ -
"""

# note range is of type range and regex is a re.compile object
Validator = namedtuple('Validator', 'range regex')

def parse_social_platforms_string():
    """Convert the social_platforms string above into a dict where
       keys = social platformsname and values = validator namedtuples"""
    lines = social_platforms.split('\n')
    validators = {}
    current_validator = {'name':None, 'min':None, 'max':None, 'regex':None}
    for line in lines:
      find_name = re.match(r'^\w+', line)
      # Finding a new definition means the current one can be created
      # and added to the list of all validators.
      if find_name:
        if current_validator['name']:
          validators[current_validator['name']] = Validator(range(current_validator['min'], current_validator['max']), current_validator['regex'])
          current_validator = {'name':None, 'min':None, 'max':None, 'regex':None}
        current_validator['name'] = find_name.group()
      find_min = re.match(r'^\s*Min\:\s+(\d+)', line)
      if find_min:
        current_validator['min'] = int(find_min.groups()[0])
      find_max = re.match(r'^\s*Max\:\s+(\d+)', line)
      if find_max:
        current_validator['max'] = int(find_max.groups()[0]) + 1
      find_regex = re.match(r'\s*Can contain\:\s+(.*)', line)
      if find_regex:
        contains = find_regex.groups()[0].replace(' ', '')
        current_validator['regex'] = re.compile(f'^[{contains}]+$')
    # The last one in the list needs to be added to the overall dictionary
    validators[current_validator['name']] = Validator(range(current_validator['min'], current_validator['max']), current_validator['regex'])
    return validators
    

def validate_username(platform, username):
    """Receives platforms(Twitter, Facebook or Reddit) and username string,
       raise a ValueError if the wrong platform is passed in,
       return True/False if username is valid for entered platform"""
    all_validators = parse_social_platforms_string()
    if platform not in all_validators:
      raise ValueError(f'unknown platform {platform}')
    
    validator = all_validators[platform]
    if len(username) not in validator.range:
      return False

    return validator.regex.match(username)