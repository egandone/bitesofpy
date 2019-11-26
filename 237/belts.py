import os
import json
from pathlib import Path
import datetime

SCORES = [10, 50, 100, 175, 250, 400, 600, 800, 1000]
BELTS = ('white yellow orange green blue brown black '
         'paneled red').split()
TMP = Path(os.getenv('TMP', '/tmp'))


def get_belts(data: str) -> dict:
    """Parsed the passed in json data:
       {"date":"5/1/2019","score":1},
       {"date":"9/13/2018","score":3},
       {"date":"10/25/2019","score":1},

       Loop through the scores in chronological order,
       determining when belts were achieved (use SCORES
       and BELTS).

       Return a dict with keys = belts, and values =
       readable dates, example entry:
       'yellow': 'January 25, 2018'
    """
    # Turn the data (a filename) into the actual file contents
    with open(data) as f:
        data = f.read()

    # First parse of all the scores from the JSON array
    parsed_scores = []
    for score in json.loads(data):
        parsed_score = (datetime.datetime.strptime(
            score['date'], '%m/%d/%Y').date(), int(score['score']))
        parsed_scores.append(parsed_score)

    # Sort the array of (date, score) tuples.  Since date is
    # first this will naturally sort the array chronologically
    parsed_scores.sort()

    # Now build a list of accumulated scores
    accumulated_scores = []
    total_score = 0
    for score in parsed_scores:
        total_score += score[1]
        accumulated_scores.append((score[0], total_score))

    # Finally, determine the dates all the belts were achieved
    belt_dates = {}
    for belt_score, belt_colour in zip(SCORES, BELTS):
        # Find all the scores that are higher then the belt boundary
        high_score_dates = [score[0]
                            for score in accumulated_scores if score[1] >= belt_score]
        # If we have scores higher then the belt boundary then
        # the date the belt was achieved is the earliest of the
        # found dates.
        if high_score_dates:
            achieve_date = min(high_score_dates)
            belt_dates[belt_colour] = achieve_date.strftime('%B %d, %Y')
    return belt_dates
