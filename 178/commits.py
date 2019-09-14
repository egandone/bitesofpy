from collections import Counter
import os
from urllib.request import urlretrieve
import re
import datetime

from dateutil.parser import parse

commits = os.path.join('/tmp', 'commits')
urlretrieve('https://bit.ly/2H1EuZQ', commits)

# you can use this constant as key to the yyyymm:count dict
YEAR_MONTH = '{y}-{m:02d}'


def get_min_max_amount_of_commits(commit_log: str = commits,
                                  year: int = None) -> (str, str):
    """
    Calculate the amount of inserts / deletes per month from the
    provided commit log.

    Takes optional year arg, if provided only look at lines for
    that year, if not, use the entire file.

    Returns a tuple of (least_active_month, most_active_month)
    """
    date_counter = Counter()
    with open(commits) as f:
        for line in f:
            m = re.match(r'^Date:\s*([^|]*)\|', line)
            date = datetime.datetime.strptime(m.group(1).strip(), '%a %b %d %H:%M:%S %Y %z')
            if (not year) or (date.year == year):
                key = YEAR_MONTH.format(y=date.year,m=date.month)
                m = re.search(r'(\d*) insert', line)
                inserts = int(m.group(1)) if m else 0
                m = re.search(r'(\d*) delet', line)
                deletes = int(m.group(1)) if m else 0
                date_counter.update({key: inserts + deletes})

    return (date_counter.most_common()[-1][0], date_counter.most_common()[0][0])

