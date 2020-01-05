from math import floor
from string import ascii_lowercase, ascii_uppercase, digits
from typing import Dict

CODEX: str = digits + ascii_lowercase + ascii_uppercase
BASE: int = len(CODEX)
# makeshift database record
LINKS: Dict[int, str] = {
    1: "https://pybit.es",
    45: "https://pybit.es/pages/articles.html",
    255: "http://pbreadinglist.herokuapp.com",
    600: "https://pybit.es/pages/challenges.html",
    874: "https://stackoverflow.com",
}
SITE: str = "https://pybit.es"

# error messages
INVALID = "Not a valid PyBites shortened url"
NO_RECORD = "Not a valid shortened url"


def encode(record: int) -> str:
    """Encodes an integer into Base62"""
    result = ''
    queue = record
    while queue:
        remainder = queue % BASE
        queue = floor(queue / BASE)
        result = CODEX[remainder] + result
    return result


def decode(short_url: str) -> int:
    """Decodes the Base62 string into a Base10 integer"""
    result = 0
    for c in short_url:
        result = BASE * result + CODEX.find(c)
    return result


def redirect(url: str) -> str:
    """Retrieves URL from shortened DB (LINKS)

    1. Check for valid domain
    2. Check if record exists
    3. Return URL stored in LINKS or proper message
    """
    if not url.startswith(SITE):
        return INVALID
    encoded_url = url[len(SITE)+1:]
    record = decode(encoded_url)
    if record not in LINKS:
        return NO_RECORD
    return LINKS[record]


def shorten_url(url: str, next_record: int) -> str:
    """Shortens URL and updates the LINKS DB

    1. Encode next_record
    2. Adds url to LINKS
    3. Return shortened URL
    """
    encoded_record = encode(next_record)
    LINKS[next_record] = url
    return SITE + f'/{encoded_record}'
