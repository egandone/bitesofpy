import re


def get_sentences(text):
    """Return a list of sentences as extracted from the text passed in.
       A sentence starts with [A-Z] and ends with [.?!]"""
    text = text.replace('\n', ' ')
    sentence = re.compile(
        r'([A-Z](?:[^\.\?\!]|\.\S|\.\S\.\s)*[^\.\?\!]{2,}[\.\?\!])\s+')
    sentences = sentence.findall(text)
    return sentences
