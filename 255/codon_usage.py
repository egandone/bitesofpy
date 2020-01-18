import os
from urllib.request import urlretrieve
from collections import Counter

# Translation Table:
# https://www.ncbi.nlm.nih.gov/Taxonomy/Utils/wprintgc.cgi#SG11
# Each column represents one entry. Codon = {Base1}{Base2}{Base3}
# All Base 'T's need to be converted to 'U's to convert DNA to RNA
TRANSL_TABLE_11 = """
    AAs  = FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG
  Starts = ---M------**--*----M------------MMMM---------------M------------
  Base1  = TTTTTTTTTTTTTTTTCCCCCCCCCCCCCCCCAAAAAAAAAAAAAAAAGGGGGGGGGGGGGGGG
  Base2  = TTTTCCCCAAAAGGGGTTTTCCCCAAAAGGGGTTTTCCCCAAAAGGGGTTTTCCCCAAAAGGGG
  Base3  = TCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAG
"""

# Converted from http://ftp.ncbi.nlm.nih.gov/genomes/archive/old_refseq/Bacteria/Staphylococcus_aureus_Newman_uid58839/NC_009641.ffn  # noqa E501
URL = "https://bites-data.s3.us-east-2.amazonaws.com/NC_009641.txt"

# Order of bases in the table
BASE_ORDER = ["U", "C", "A", "G"]


def _preload_sequences(url=URL):
    """
    Provided helper function
    Returns coding sequences, one sequence each line
    """
    filename = os.path.join(os.getenv("TMP", "/tmp"), "NC_009641.txt")
    if not os.path.isfile(filename):
        urlretrieve(url, filename)
    with open(filename, "r") as f:
        return f.readlines()


def get_translation_map(table):
    """
    Returns the translation string as a map with keys 
    equal to {base1}{base2}{base3} and value equals to AA
    """
    pairs = [line.strip().split(' = ')
             for line in TRANSL_TABLE_11.split('\n') if line]
    AAs = [p[1] for p in pairs if p[0].strip() == 'AAs'][0]
    base1 = [p[1]
             for p in pairs if p[0].strip() == 'Base1'][0].replace('T', 'U')
    base2 = [p[1]
             for p in pairs if p[0].strip() == 'Base2'][0].replace('T', 'U')
    base3 = [p[1]
             for p in pairs if p[0].strip() == 'Base3'][0].replace('T', 'U')
    return {''.join(z[0:3]): z[3] for z in zip(base1, base2, base3, AAs)}

def render_header():
    return '|  Codon AA  Freq  Count  |  Codon AA  Freq  Count  |  Codon AA  Freq  Count  |  Codon AA  Freq  Count  |'

def render_separator():
    return '---------------------------------------------------------------------------------------------------------'

def render_cell(codon, aa, count, total):
    freq = count / total * 1000
    return f'  {codon}:  {aa}   {freq:4.1f}  {count:5}  |'

def render_row(codons, codon_counter, translation_map, total):
    str = '|'
    for codon in codons:
        str = str + render_cell(codon, translation_map[codon], codon_counter[codon], total)
    return str


def return_codon_usage_table(
    sequences=_preload_sequences(), translation_table_str=TRANSL_TABLE_11
):
    """
    Receives a list of gene sequences and a translation table string
    Returns a string with all bases and their frequencies in a table
    with the following fields:
    codon_triplet: amino_acid_letter frequency_per_1000 absolute_occurrences

    Skip invalid coding sequences:
       --> must consist entirely of codons (3-base triplet)
    """
    # The counter will have 64 entries at the end - one for each codon
    # And the count will be the total number of occurances of that codon
    # in all the sequences.
    codon_counter = Counter()
    for sequence in [s.strip() for s in sequences]:
        # Just split each sequence up into 3 character codons
        codons = [sequence[r:r+3] for r in range(0, len(sequence), 3)]
        # Add them all to the counter
        codon_counter.update(codons)

    # Get the total number of codons by summing up all the counts
    total_count = sum(codon_counter.values())
    
    # Get the codon list from the translation_map.  This
    # defines the order in which we render all the counts
    translation_map = get_translation_map(translation_table_str)
    codons = list(translation_map.keys())
    
    # Start the table with the header and separator
    rows = [render_header(), render_separator()]
    # Render the codes in blocks of 16 divided into 4 colums
    for c in range(0, len(codons), 16):
        for i in range(c,c+4):
            names = [codons[i], codons[i+4], codons[i+8], codons[i+12]]
            rows.append(render_row(names, codon_counter, translation_map, total_count))
        # Render a separator between each block
        rows.append(render_separator())
    # Return the table as all the rows joined together by newines
    return '\n'.join(rows)


if __name__ == "__main__":
    print(return_codon_usage_table())
