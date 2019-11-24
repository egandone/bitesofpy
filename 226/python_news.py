import re
from collections import namedtuple


from bs4 import BeautifulSoup
import requests

# feed = https://news.python.sc/, to get predictable results we cached
# first two pages - use these:
# https://bites-data.s3.us-east-2.amazonaws.com/news.python.sc/index.html
# https://bites-data.s3.us-east-2.amazonaws.com/news.python.sc/index2.html

Entry = namedtuple('Entry', 'title points comments')


def _create_soup_obj(url):
    """Need utf-8 to properly parse emojis"""
    resp = requests.get(url)
    resp.encoding = "utf-8"
    return BeautifulSoup(resp.text, "html.parser")


def get_top_titles(url, top=5):
    """Parse the titles (class 'title') using the soup object.
       Return a list of top (default = 5) titles ordered descending
       by number of points and comments.
    """
    soup = _create_soup_obj(url)

    entries = []
    title_spans = soup.find_all('span', class_='title')
    for title_span in title_spans:
        # Render the title span as simple text - strip off any leading/trailing spaces
        title = title_span.get_text().strip()
        # Get the <tr> that owns this title
        title_tr = title_span.parent.parent.parent
        # Get the next <tr> that contains the points and comments counts
        details_tr = title_tr.next_sibling.next_sibling
        # Match the point(s) and comment(s) counts.
        count_matches = re.search(r'(?P<points>\d+) point.*(?P<comments>\d+) comment',
                                  details_tr.find('span', class_='smaller').get_text(), re.DOTALL)
        entry = Entry(title=title,
                      points=int(count_matches.groupdict()['points']),
                      comments=int(count_matches.groupdict()['comments']))
        entries.append(entry)
    # Sort all the entries in reverse order by number of points and comments.
    # Then return only the specified number of top entries
    return sorted(entries, key=lambda e: (e.points, e.comments), reverse=True)[:top]
