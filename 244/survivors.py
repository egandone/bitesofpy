import os
from pathlib import Path
from urllib.request import urlretrieve

S3 = "https://bites-data.s3.us-east-2.amazonaws.com/{}"
FILE_NAME = "mutpy.out"
TMP = os.getenv("TMP", "/tmp")
PATH = Path(TMP, FILE_NAME)

if not PATH.exists():
    urlretrieve(S3.format(FILE_NAME), PATH)


def _get_data(path=PATH):
    with open(path) as f:
        return [line.rstrip() for line in f.readlines()]


def filter_killed_mutants(mutpy_output: list = None) -> list:
    if mutpy_output is None:
        mutpy_output = _get_data()

    output = []
    run_results = None
    saved_results = None
    for line in mutpy_output:
        is_delimit_line = line.strip().startswith('----------------------------')
        if is_delimit_line:
            if run_results:
                run_results.append(line)
                saved_results = run_results
                run_results = None
            else:
                run_results = [line]
        elif run_results:
            run_results.append(line)
        elif saved_results:
            if line.find('survived') >= 0:
                output.extend(saved_results)
            output.append(line)
            saved_results = None
        else:
            output.append(line)
    return output
