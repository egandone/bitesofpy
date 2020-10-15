import os
from urllib import request
#from Bio import SeqIO

# Fetched and truncated from
# https://www.uniprot.org/uniprot/?query=database%3A%28type%3Aembl+AE017195%29&format=fasta (Aug 01, 2020)
URL = "https://bites-data.s3.us-east-2.amazonaws.com/fasta_genes.fasta"
FASTA_FILE = os.path.join(os.getenv("TMP", "/tmp"), "fasta_genes.fasta")
if not os.path.isfile(FASTA_FILE):
    request.urlretrieve(URL, FASTA_FILE)


def fasta_to_2line_fasta(fasta_file: str, fasta_2line_file: str) -> int:
    """
    :param fasta_file: Filename of multi-line FASTA file
    :param fasta_2line_file: Filename of 2-line FASTA file
    :return: Number of records
    """
    with open(fasta_file) as in_file:
        in_lines = in_file.readlines()

    file_count = 0
    header_record = None
    merged_line = ''
    out_lines = []
    for in_line in in_lines:
        if in_line.startswith('>'):
            if header_record:
                out_lines.append(header_record)
                out_lines.append(merged_line + '\n')

            file_count += 1
            header_record = in_line
            merged_line = ''
        else:
            merged_line += in_line.strip()
    out_lines.append(header_record)
    out_lines.append(merged_line + '\n')
    with open(fasta_2line_file, "w") as out_file:
        out_file.writelines(out_lines)

    return file_count


if __name__ == "__main__":
    fasta_to_2line_fasta(FASTA_FILE, f"{FASTA_FILE}_converted.fasta")
