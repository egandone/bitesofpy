from reverse_complement import parse_str_table
import pytest

SIMPLE_COMPLEMENTS_STR = """#Reduced table with bases A, G, C, T
 Base	Complementary Base
 A	T
 T	A
 G	C
 C	G
"""

COMPLEMENTS_STR = """# Full table with ambigous bases
 Base	Name	Bases Represented	Complementary Base
 A	Adenine	A	T
 T	Thymidine	T 	A
 U	Uridine(RNA only)	U	A
 G	Guanidine	G	C
 C	Cytidine	C	G
 Y	pYrimidine	C T	R
 R	puRine	A G	Y
 S	Strong(3Hbonds)	G C	S
 W	Weak(2Hbonds)	A T	W
 K	Keto	T/U G	M
 M	aMino	A C	K
 B	not A	C G T	V
 D	not C	A G T	H
 H	not G	A C T	D
 V	not T/U	A C G	B
 N	Unknown	A C G T	N
"""


def test_simple():
    c = parse_str_table(SIMPLE_COMPLEMENTS_STR)
    assert c['A'] == 'T'
    assert c['T'] == 'A'
    assert c['G'] == 'C'
    assert c['C'] == 'G'


def test_full():
    c = parse_str_table(COMPLEMENTS_STR)
    assert c['A'] == 'T'
    assert c['T'] == 'A'
    assert c['U'] == 'A'
    assert c['G'] == 'C'
    assert c['C'] == 'G'
    assert c['Y'] == 'R'
    assert c['R'] == 'Y'
    assert c['S'] == 'S'
    assert c['W'] == 'W'
    assert c['K'] == 'M'
    assert c['M'] == 'K'
    assert c['B'] == 'V'
    assert c['D'] == 'H'
    assert c['H'] == 'D'
    assert c['V'] == 'B'
    assert c['N'] == 'N'
