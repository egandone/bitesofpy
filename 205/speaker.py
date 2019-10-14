from urllib.request import urlretrieve
from pathlib import Path
from collections import Counter

import gender_guesser.detector as gender
from bs4 import BeautifulSoup as Soup

TMP = Path('/tmp')
PYCON_HTML = TMP / "pycon2019.html"
if not PYCON_HTML.exists():
    urlretrieve('https://bit.ly/2O5Bik7', PYCON_HTML)


def _get_soup(html=PYCON_HTML):
    return Soup(html.read_text(encoding="utf-8"), "html.parser")


def get_pycon_speaker_first_names(soup=None):
    """Parse the PYCON_HTML using BeautifulSoup, extracting all
       speakers (class "speaker"). Note that some items contain
       multiple speakers so you need to extract them.
       Return a list of first names
    """
    if soup == None:
        soup = _get_soup()
    first_names = []
    speakers = soup.find_all(class_='speaker')
    for speaker in speakers:
        full_names = speaker.text.strip().replace('/', ',').split(',')
        first_names += [name.strip().split(' ')[0] for name in full_names]
    return first_names


def get_percentage_of_female_speakers(first_names):
    """Run gender_guesser on the names returning a percentage
       of female speakers, rounded to 2 decimal places."""
    detector = gender.Detector()
    gender_counter = Counter([detector.get_gender(name)
                              for name in first_names])
    perc = (gender_counter['female'] +
            gender_counter['mostly_female']) * 100. / len(first_names)
    return round(perc, 2)


if __name__ == '__main__':
    names = get_pycon_speaker_first_names()
    perc = get_percentage_of_female_speakers(names)
    print(perc)
