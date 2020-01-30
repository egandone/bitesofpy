from collections import Counter


def calculate_gc_content(sequence):
    """
    Receives a DNA sequence (A, G, C, or T)
    Returns the percentage of GC content (rounded to the last two digits)
    """
    counter = Counter([c for c in sequence.upper() if c in 'AGCT'])
    ratio = (counter['G'] + counter['C']) / sum(counter.values())
    return round(ratio * 100.0, 2)
