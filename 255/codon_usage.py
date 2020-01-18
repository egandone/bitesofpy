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
    rows = ['Codon AA  Freq  Count',
            'Codon AA  Freq  Count',
            'Codon AA  Freq  Count',
            'Codon AA  Freq  Count']
    translation_map = get_translation_map(translation_table_str)
    codon_counter = Counter()
    for sequence in [s.strip() for s in sequences]:
        codons = [sequence[r:r+3] for r in range(0, len(sequence), 3)]
        codon_counter.update(codons)
    total_count = sum(codon_counter.values())
    for codon, aa in translation_map.items():
        freq = codon_counter[codon] / total_count * 1000
        rows.append(f'{codon}: {aa} {freq:.1f} {codon_counter[codon]}')
    return '\n'.join(rows)


if __name__ == "__main__":
    print(return_codon_usage_table())
