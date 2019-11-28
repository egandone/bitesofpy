import os
import re
from pathlib import Path
from urllib.request import urlretrieve
import dataclasses

from bs4 import BeautifulSoup

url = ("https://bites-data.s3.us-east-2.amazonaws.com/"
       "best-programming-books.html")
tmp = Path(os.getenv('TMP', "/tmp"))
html_file = tmp / "books.html"

if not html_file.exists():
    urlretrieve(url, html_file)


@dataclasses.dataclass
class Book:
    """Book class should instatiate the following variables:

    title - as it appears on the page
    author - should be entered as lastname, firstname
    year - four digit integer year that the book was published
    rank - integer rank to be updated once the books have been sorted
    rating - float as indicated on the page
    """
    title: str
    author: str
    year: int
    rank: int
    rating: float
    lastname: str = dataclasses.field(init=False)
    firstname: str = dataclasses.field(init=False)

    def __post_init__(self):
        self.lastname, self.firstname = self.author.split(',')

    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if name == 'author':
            self.__post_init__()

    def __repr__(self):
        return f'[{self.rank:03d}] {self.title} ({self.year})\n      {self.author} {float(self.rating)}'


def _get_soup(file):
    return BeautifulSoup(file.read_text(encoding='utf-8'), "html.parser")


def display_books(books, limit=10, year=None):
    """Prints the specified books to the console

    :param books: list of all the books
    :param limit: integer that indicates how many books to return
    :param year: integer indicating the oldest year to include
    :return: None
    """
    trimmed_list = [
        book for book in books if not year or book.year >= year][:limit]
    for book in trimmed_list:
        print(book)


def load_data():
    """Loads the data from the html file

    Creates the soup object and processes it to extract the information
    required to create the Book class objects and returns a sorted list
    of Book objects.

    Books should be sorted by rating, year, title, and then by author's
    last name. After the books have been sorted, the rank of each book
    should be updated to indicate this new sorting order.The Book object
    with the highest rating should be first and go down from there.
    """
    soup = _get_soup(html_file)
    python_books = []
    titles = soup.find_all("h2", class_="main")
    for title in titles:
        if 'python' in title.getText().lower():
            top = title.parent.parent
            authors = top.find('h3', class_='authors')
            date = top.find('span', class_='date')
            rating = top.find('span', class_='our-rating')
            if authors and date and rating:
                name = authors.find('a')
                *firstnames, lastname = name.getText().split(' ')
                firstname = ' '.join(firstnames)
                date = date.find(string=re.compile(r'^\d\d\d\d$'))
                if name:
                    book = Book(title.getText(), author=f'{lastname}, {firstname}', year=int(
                        date), rank=0, rating=float(rating.getText()))
                    python_books.append(book)
    python_books.sort(key=lambda book: (-book.rating,
                                        book.year, book.title.lower(), book.lastname))
    for i, book in enumerate(python_books, start=1):
        book.rank = i
    return python_books


def main():
    books = load_data()
    display_books(books, limit=5, year=2017)
    """If done correctly, the previous function call should display the
    output below.
    """


if __name__ == "__main__":
    main()

"""
[001] Python Tricks (2017)
      Bader, Dan 4.74
[002] Mastering Deep Learning Fundamentals with Python (2019)
      Wilson, Richard 4.7
[006] Python Programming (2019)
      Fedden, Antony Mc 4.68
[007] Python Programming (2019)
      Mining, Joseph 4.68
[009] A Smarter Way to Learn Python (2017)
      Myers, Mark 4.66
"""
