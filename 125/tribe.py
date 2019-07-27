from collections import Counter

from bs4 import BeautifulSoup
import requests
import re

AMAZON = "amazon.com"
TIM_BLOG = 'https://bit.ly/2NBnZ6P'


def load_page():
    """Download the blog html and return its decoded content"""
    with requests.Session() as session:
        return session.get(TIM_BLOG).content.decode('utf-8')


def get_top_books(content=None, limit=5):
    """Make a BeautifulSoup object loading in content,
       find all links and filter on AMAZON, extract the book title
       and count them, return the top "limit" books (default 5)"""
    if content is None:
        content = load_page()
    # Just prase the content as HTML
    soup = BeautifulSoup(content, 'html.parser')
    # Look for all the links that include amazon in the href
    tags = soup.find_all('a', href=re.compile('amazon'))
    # The content of each link will be the title.  Just use
    # a counter to count the occurance of each title
    title_counter = Counter([next(tag.strings) for tag in tags])

    # Return the first element of each counter entry (the title)
    # ... the second element will be the count but is not needed here.
    return [title[0] for title in title_counter.most_common(limit)]