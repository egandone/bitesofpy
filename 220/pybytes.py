from collections import namedtuple, Counter
import re
from typing import NamedTuple
from datetime import timedelta

import feedparser

SPECIAL_GUEST = 'Special guest'

# using _ as min/max are builtins
Duration = namedtuple('Duration', 'avg max_ min_')

# static copy, original: https://pythonbytes.fm/episodes/rss
URL = 'http://projects.bobbelderbos.com/pcc/python_bytes'
IGNORE_DOMAINS = {'https://pythonbytes.fm', 'http://pythonbytes.fm',
                  'https://twitter.com', 'https://training.talkpython.fm',
                  'https://talkpython.fm', 'http://testandcode.com'}


def timedelta_to_str(td):
    hours = int(td.seconds/3600)
    minutes = int(td.seconds % 3600/60)
    seconds = int(td.seconds % 60)
    return f'{hours:02d}:{minutes:02d}:{seconds:02d}'


class PythonBytes:

    def __init__(self, url=URL):
        """Load the feed url into self.entries using the feedparser module."""
        self.entries = feedparser.parse(URL)['entries']

    def get_episode_numbers_for_mentioned_domain(self, domain: str) -> list:
        """Return a list of episode IDs (itunes_episode attribute) of the
           episodes the pass in domain was mentioned in.
        """
        return [e.itunes_episode for e in self.entries if domain in e.description]

    def get_most_mentioned_domain_names(self, n: int = 15) -> list:
        """Get the most mentioned domain domains. We match a domain using
           regex: "https?://[^/]+" - make sure you only count a domain once per
           episode and ignore domains in IGNORE_DOMAINS.
           Return a list of (domain, count) tuples (use Counter).
        """
        # Find the set of all domain urls for each episode.
        episode_domains = [set(re.findall(
            r'https?://[^/]+', e.description)) - IGNORE_DOMAINS for e in self.entries]
        # Count all the domains across all episodes
        domain_counter = Counter()
        for d in episode_domains:
            domain_counter.update(d)
        return domain_counter.most_common(n)

    def number_episodes_with_special_guest(self) -> int:
        """Return the number of episodes that had one of more special guests
           featured (use SPECIAL_GUEST).
        """
        guest_appearance_episodes = [
            e for e in self.entries if SPECIAL_GUEST in e.description]
        return len(guest_appearance_episodes)

    def get_average_duration_episode_in_seconds(self) -> NamedTuple:
        """Return the average duration in seconds of a Python Bytes episode, as
           well as the shortest and longest episode in hh:mm:ss notation.
           Return the results using the Duration namedtuple.
        """
        # Turn each duration into a dictionary of hours,minutes,seconds
        durations = [re.match(r'(?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d+)',
                              e.itunes_duration).groupdict() for e in self.entries]
        # Turn each dictionary into a timedelta so we can properly compare them
        durations = [timedelta(hours=int(d['hours']), minutes=int(
            d['minutes']), seconds=int(d['seconds'])) for d in durations]
        # Find min/max and compute average.
        min_duration = min(durations)
        max_duration = max(durations)
        avg_seconds = int(sum([d.seconds for d in durations]) / len(durations))
        return Duration(avg=avg_seconds, min_=timedelta_to_str(min_duration), max_=timedelta_to_str(max_duration))
