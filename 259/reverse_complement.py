# See tests for a more comprehensive complementary table
SIMPLE_COMPLEMENTS_STR = """#Reduced table with bases A, G, C, T
 Base	Complementary Base
 A	T
 T	A
 G	C
 C	G
"""


def parse_str_table(str_table: str) -> dict:
    compliments = dict()
    for line in str_table.split('\n'):
        line = line.strip()
        if not line.startswith('#') and not line.startswith('Base'):
            elements = line.split('\t')
            compliments[elements[0]] = elements[-1]
    return compliments


# Recommended helper function
def _clean_sequence(sequence, compliments):
    """
    Receives a DNA sequence and a str_table that defines valid (and
    complementary) bases
    Returns all sequences converted to upper case and remove invalid
    characters
    t!t%ttttAACCG --> TTTTTTAACCG
    """
    return ''.join([s.upper() for s in sequence if s.upper() in compliments])


def reverse(sequence, str_table=SIMPLE_COMPLEMENTS_STR):
    """
    Receives a DNA sequence and a str_table that defines valid (and
    complementary) bases
    Returns a reversed string of sequence while removing all characters
    not found in str_table characters
    e.g. t!t%ttttAACCG --> GCCAATTTTTT
    """
    compliments = parse_str_table(str_table)
    return ''.join(reversed(_clean_sequence(sequence, compliments)))


def complement(sequence, str_table=SIMPLE_COMPLEMENTS_STR):
    """
    Receives a DNA sequence and a str_table that defines valid (and
    complementary) bases
    Returns a string containing complementary bases as defined in
    str_table while removing non input_sequence characters
    e.g. t!t%ttttAACCG --> AAAAAATTGGC
    """
    compliments = parse_str_table(str_table)
    return ''.join([compliments[s]
                    for s in _clean_sequence(sequence, compliments)])


def reverse_complement(sequence, str_table=SIMPLE_COMPLEMENTS_STR):
    """
    Receives a DNA sequence and a str_table that defines valid (and
    complementary) bases
    Returns a string containing complementary bases as defined in str_table
    while removing non input_sequence characters
    e.g. t!t%ttttAACCG --> CGGTTAAAAAA
    """
    complimented = complement(sequence, str_table)
    return ''.join(reversed(complimented))
