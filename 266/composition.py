from abc import ABC, abstractmethod
from collections import namedtuple
from dataclasses import dataclass, field
from datetime import date
from os import getenv, path
from pathlib import Path
from typing import Any, List, Optional, NamedTuple
from urllib.request import urlretrieve

from bs4 import BeautifulSoup as Soup  # type: ignore

TMP = getenv("TMP", "/tmp")
TODAY = date.today()
Candidate = namedtuple("Candidate", "name votes")
LeaderBoard = NamedTuple(
    "LeaderBoard", [("Candidate", str), ('Average', str),
                    ('Delegates', int),  ('Contributions', str), ('Coverage', int)]
)
Poll = NamedTuple(
    "Poll",
    [('Poll', str), ('Date', str), ('Sample', str), ('Sanders', float),
        ('Biden', float), ('Gabbard', float), ('Spread', str)]
)


def to_float(s):
    try:
        f = float(s)
    except ValueError:
        f = 0.0
    return f


@dataclass
class File:
    """File represents a filesystem path.

    Variables:
        name: str -- The filename that will be created on the filesystem.
        file: Path -- Path object created from the name passed in.

    Methods:
        [property]
        data: -> Optional[str] -- If the file exists, it returns its contents.
            If it does not exists, it returns None.
    """
    name: str
    path: Path = field(init=False)

    def __post_init__(self):
        self.path = Path(f'{TMP}/{TODAY}_{self.name}')

    @property
    def data(self) -> Optional[str]:
        d = None
        if self.path.exists():
            with open(self.path, encoding='utf-8') as f:
                d = f.read()
        return d

    @data.setter
    def data(self, value) -> None:
        with open(self.path, 'w') as f:
            f.write(value)


@dataclass
class Web:
    """Web object.

    Web is an object that downloads the page from the url that is passed
    to it and stores it in the File instance that is passed to it. If the
    File already exists, it just reads the file, otherwise it downloads it
    and stores it in File.

    Variables:
        url: str -- The url of the web page.
        file: File -- The File object to store the page data into.

    Methods:
        [property]
        data: -> Optional[str] -- Reads the text from File or retrieves it from the
            web if it does not exists.

        [property]
        soup: -> Soup -- Parses the data from File and turns it into a BeautifulSoup
            object.
    """
    url: str
    file: File

    @property
    def data(self) -> Optional[str]:
        """Reads the data from the File object.

        First it checks if the File object has any data. If it doesn't, it retrieves
        it and saves it to the File. It then reads it from the File and
        returns it.

        Returns:
            Optional[str] -- The string data from the File object.
        """
        if not self.file.data:
            urlretrieve(self.url, self.file.path)
        return self.file.data

    @property
    def soup(self) -> Soup:
        """Converts string data from File into a BeautifulSoup object.

        Returns:
            Soup -- BeautifulSoup object created from the File.
        """
        return Soup(self.data)


@dataclass
class Site(ABC):
    """Site Abstract Base Class.

    Defines the structure for the objects based on this class and defines the interfaces
    that should implemented in order to work properly.

    Variables:
        web: Web -- The web object stores the information needed to process
            the data.

    Methods:
        find_table: -> str -- Parses the Web object for table elements and
            returns the first one that it finds unless an integer representing
            the required table is passed.

        [abstractmethod]
        parse_rows: -> Union[List[LeaderBoard], List[Poll]] -- Parses a BeautifulSoup
            table element and returns the text found in the td elements as
            namedtuples.

        [abstractmethod]
        polls: -> Union[List[LeaderBoard], List[Poll]] -- Does the parsing of the table
            and rows for you. It takes the table index number if given, otherwise
            parses table 0.

        [abstractmethod]
        stats: -- Formats the results from polls into a more user friendly
            representation.
    """
    web: Web

    def find_table(self, loc: int = 0) -> str:
        """Finds the table elements from the Soup object

        Keyword Arguments:
            loc {int} -- Parses the Web object for table elements and
                returns the first one that it finds unless an integer representing
                the required table is passed. (default: {0})

        Returns:
            str -- The html table
        """
        table = None
        if self.web.soup:
            tables = self.web.soup.find_all('table')
            if len(tables) > loc:
                table = tables[loc]
        return table

    @abstractmethod
    def parse_rows(self, table: Soup) -> List[Any]:
        """Abstract Method

        Parses the row data from the html table.

        Arguments:
            table {Soup} -- Parses a BeautifulSoup table element and
                returns the text found in the td elements as NamedTuple.

        Returns:
            List[NamedTuple] -- List of NamedTuple that were created from the
                table data.
        """

    @abstractmethod
    def polls(self, table: int = 0) -> List[Any]:
        """Abstract Method

        Parses the data

        The find_table and parse_rows methods are called for you and the table index
        that is passed to it is used to get the correct table from the soup object.

        Keyword Arguments:
            table {int} -- Does the parsing of the table and rows for you.
                It takes the table index number if given, otherwise parses table 0.
                (default: {0})

        Returns:
            List[NamedTuple] -- List of NamedTuple that were created from the
                table data.
        """

    @abstractmethod
    def stats(self, loc: int = 0):
        """Abstract Method

        Produces the stats from the polls.

        Keyword Arguments:
            loc {int} -- Formats the results from polls into a more user friendly
            representation.
        """


@dataclass
class RealClearPolitics(Site):
    """RealClearPolitics object.

    RealClearPolitics is a custom class to parse a Web instance from the
    realclearpolitics website.

    Variables:
        web: Web -- The web object stores the information needed to process
            the data.

    Methods:
        find_table: -> str -- Parses the Web object for table elements and
            returns the first one that it finds unless an integer representing
            the required table is passed.

        parse_rows: -> List[Poll] -- Parses a BeautifulSoup table element and
            returns the text found in the td elements as Poll namedtuples.

        polls: -> List[Poll] -- Does the parsing of the table and rows for you.
            It takes the table index number if given, otherwise parses table 0.

        stats: -- Formats the results from polls into a more user friendly
            representation:

            Example:

            RealClearPolitics
            =================
                Biden: 214.0
              Sanders: 142.0
              Gabbard: 6.0

    """

    def parse_rows(self, table: Soup) -> List[Any]:
        """Abstract Method

        Parses the row data from the html table.

        Arguments:
            table {Soup} -- Parses a BeautifulSoup table element and
                returns the text found in the td elements as NamedTuple.

        Returns:
            List[NamedTuple] -- List of NamedTuple that were created from the
                table data.
        """
        polls = []
        for tr in table.find_all('tr'):
            columns = tr.find_all('td')
            if (len(columns) == 7) and ('Average' not in columns[0].text):
                poll = Poll(Poll=columns[0].text, Date=columns[1].text, Sample=columns[2].text,
                            Biden=to_float(columns[3].text), Sanders=to_float(columns[4].text), Gabbard=to_float(columns[5].text), Spread=columns[6].text)
                polls.append(poll)
        if len(polls) == 0:
            polls = None
        return polls

    def polls(self, table: int = 0) -> List[Any]:
        """Abstract Method

        Parses the data

        The find_table and parse_rows methods are called for you and the table index
        that is passed to it is used to get the correct table from the soup object.

        Keyword Arguments:
            table {int} -- Does the parsing of the table and rows for you.
                It takes the table index number if given, otherwise parses table 0.
                (default: {0})

        Returns:
            List[NamedTuple] -- List of NamedTuple that were created from the
                table data.
        """
        return self.parse_rows(self.find_table(table))

    def stats(self, loc: int = 0):
        """Produces the stats from the polls.

        Keyword Arguments:
            loc {int} -- Formats the results from polls into a more user friendly
            representation.

        """
        polls = self.polls(loc)
        lines = []
        biden_total = sum([poll.Biden for poll in polls])
        sanders_total = sum([poll.Sanders for poll in polls])
        gabbard_total = sum([poll.Gabbard for poll in polls])
        lines.append('')
        lines.append('RealClearPolitics')
        lines.append('=================')
        lines.append(f'   Biden: {biden_total:.1f}')
        lines.append(f' Sanders: {sanders_total:.1f}')
        lines.append(f' Gabbard: {gabbard_total:.1f}')
        lines.append('')

        print('\n'.join(lines))


@dataclass
class NYTimes(Site):
    """NYTimes object.

    RealClearPolitics is a custom class to parse a Web instance from the
    realclearpolitics website.

    Variables:
        web: Web -- The web object stores the information needed to process
            the data.

    Methods:
        find_table: -> str -- Parses the Web object for table elements and
            returns the first one that it finds unless an integer representing
            the required table is passed.

        parse_rows: -> List[LeaderBoard] -- Parses a BeautifulSoup table element and
            returns the text found in the td elements as LeaderBoard namedtuples.

        polls: -> List[LeaderBoard] -- Does the parsing of the table and rows for you.
            It takes the table index number if given, otherwise parses table 0.

        stats: -- Formats the results from polls into a more user friendly
            representation:

            Example:

            NYTimes
            =================================

                               Pete Buttigieg
            ---------------------------------
            National Polling Average: 10%
                   Pledged Delegates: 25
            Individual Contributions: $76.2m
                Weekly News Coverage: 3

    """

    def parse_rows(self, table: Soup) -> List[LeaderBoard]:
        """Parses the row data from the html table.

        Arguments:
            table {Soup} -- Parses a BeautifulSoup table element and
                returns the text found in the td elements as LeaderBoard namedtuples.

        Returns:
            List[LeaderBoard] -- List of LeaderBoard namedtuples that were created from
            the table data.
        """
        polls = []
        for tr in table.find_all('tr'):
            columns = tr.find_all('td')
            if (len(columns) == 5):
                poll = LeaderBoard(Candidate=columns[0].text.strip(),
                                   Average=columns[1].text.strip(),
                                   Delegates=int(columns[2].text.strip()),
                                   Contributions=columns[3].text.strip(),
                                   Coverage=int(columns[4].text.strip()[1:]))
                polls.append(poll)
        if len(polls) == 0:
            polls = None
        return polls

    def polls(self, table: int = 0) -> List[LeaderBoard]:
        """Parses the data

        The find_table and parse_rows methods are called for you and the table index
        that is passed to it is used to get the correct table from the soup object.

        Keyword Arguments:
            table {int} -- Does the parsing of the table and rows for you.
                It takes the table index number if given, otherwise parses table 0.
                (default: {0})

        Returns:
            List[LeaderBoard] -- List of LeaderBoard namedtuples that were created from
                the table data.
        """
        return self.parse_rows(self.find_table(table))

    def stats(self, loc: int = 0):
        """Produces the stats from the polls.

        Keyword Arguments:
            loc {int} -- Formats the results from polls into a more user friendly
            representation.
        """
        lines = []
        lines.append('NYTimes')
        lines.append('=================================')
        for poll in self.polls(loc):
            lines.append('')
            lines.append(f'{poll.Candidate.rjust(33)}')
            lines.append('---------------------------------')
            lines.append(f'National Polling Average: {poll.Average}')
            lines.append(f'       Pledged Delegates: {poll.Delegates}')
            lines.append(f'Individual Contributions: {poll.Contributions}')
            lines.append(f'    Weekly News Coverage: {poll.Coverage}')

        lines.append('')
        print('\n'.join(lines))


def gather_data():
    rcp_file = File("realclearpolitics.html")
    rcp_url = (
        "https://bites-data.s3.us-east-2.amazonaws.com/2020-03-10_realclearpolitics.html"
    )
    rcp_web = Web(rcp_url, rcp_file)
    rcp = RealClearPolitics(rcp_web)
    rcp.stats(3)

    nyt_file = File("nytimes.html")
    nyt_url = (
        "https://bites-data.s3.us-east-2.amazonaws.com/2020-03-10_nytimes.html"
    )
    nyt_web = Web(nyt_url, nyt_file)
    nyt = NYTimes(nyt_web)
    nyt.stats()


if __name__ == "__main__":
    gather_data()
