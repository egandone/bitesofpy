from urllib.request import urlretrieve
import os
from pathlib import Path
import csv

XYZ = "https://bites-data.s3.us-east-2.amazonaws.com/xyz.csv"
PATH = Path(os.getenv('TMP', r'C:\WUTemp'), "xyz.csv")
THRESHOLDS = (5000, 0.05)


def get_XYZ():
    urlretrieve(XYZ, PATH)
    lines = []
    with open(PATH) as xyz_file:
        lines = [line.strip() for line in xyz_file.readlines() if line.strip()]
    return lines


def calculate_flux(XYZ: str) -> list:
    """Read the data in from xyz.csv
    add two new columns, one to calculate dollar flux,
    and the other to calculate percentage flux
    return as a list of tuples
    """
    results = list()
    for row in csv.reader(get_XYZ()[1:]):
        (name, r2020, r2019) = (row[0], int(row[1]), int(row[2]))
        results.append((name, r2020, r2019, r2020 -
                        r2019, (r2020 - r2019)/r2019))
    return results


def identify_flux(xyz: list) -> list:
    """Load the list of tuples, iterate through
    each item and determine if it is above both
    thresholds. if so, add to the list
    """
    flagged_lines = [line for line in xyz if abs(
        line[3]) > THRESHOLDS[0] and abs(line[4]) > THRESHOLDS[1]]
    return flagged_lines
