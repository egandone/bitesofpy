import os
import time
from datetime import datetime
from pathlib import Path, PosixPath
from zipfile import ZipFile

TMP = Path(os.getenv('TMP', '/tmp'))
LOG_DIR = TMP / 'logs'
ZIP_FILE = 'logs.zip'


def zip_last_n_files(directory: PosixPath = LOG_DIR,
                     zip_file: str = ZIP_FILE, n: int = 3):
    files = [file for file in directory.iterdir() if file.is_file()]
    files.sort(key=lambda file: file.lstat().st_mtime, reverse=True)
    zip = ZipFile(zip_file, mode='w')
    for file in files[:n]:
        modified_date = time.strftime(
            '%Y-%m-%d', time.localtime(file.lstat().st_mtime))
        arcname = file.name.replace('.', f'_{modified_date}.')
        zip.write(file.absolute(), arcname=arcname)
    zip.close()
