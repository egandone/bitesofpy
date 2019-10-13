import csv
from pathlib import Path
from urllib.request import urlretrieve

tmp = Path(r'C:\WUTemp')
stats = tmp / 'bites.csv'

if not stats.exists():
    urlretrieve('https://bit.ly/2MQyqXQ', stats)


def get_most_complex_bites(N=10, stats=stats):
    """Parse the bites.csv file (= stats variable passed in), see example
       output in the Bite description.
       Return a list of Bite IDs (int or str values are fine) of the N
       most complex Bites.
    """
    with open(stats, encoding='utf-8-sig') as f:
        csv_data = csv.DictReader(f.readlines(), delimiter=';')
    rows = [(float(row['Difficulty']), row['Bite'].split(' ')[1][:-1])
            for row in csv_data if row['Difficulty'] != 'None']
    return [c[1] for c in sorted(rows, key=lambda c: c[0], reverse=True)[:N]]


if __name__ == '__main__':
    res = get_most_complex_bites()
    print(res)
