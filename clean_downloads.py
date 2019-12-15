import os
import time
from os import stat_result
from typing import Callable
import datetime as dt
import subprocess
import shutil

BASE_DIR = '/Users/davidscroggins/Downloads'


def remove_old_files():
    for dirpath, dirnames, filenames in os.walk(BASE_DIR):
        if 'scroggins' in filenames:
            print(f'dirpath: {dirpath}')
            # print(type(subdir))
            print(f'dirnames: {dirnames}')
            print(f'filenames: {filenames}')
        # birthtime: float = os.stat(subdir).st_birthtime
        # to_datetime: Callable = dt.datetime.fromtimestamp
        # print(to_datetime(birthtime))
        # for file in filenames:
        #     if 'scroggins' in file:
        #         print(dirpath)
        #         print(dirnames)
        #         print(file)
        # print(filenames)


def walk():
    a = os.walk(BASE_DIR)
    filenames = next(a)[2]
    print(filenames)
    for file in filenames:
        if 'scroggins' in file:
            print(file)


def dirs():
    _now = time.time()
    contents = os.listdir(BASE_DIR)
    six_months = dt.timedelta(days=180).total_seconds()
    total_contents = 0
    total_old_contents = 0
    for c in contents:
        total_contents += 1
        _path = os.path.join(BASE_DIR, c)
        birthtime: float = os.stat(_path).st_birthtime
        to_datetime: Callable = dt.datetime.fromtimestamp
        # print(f'{_path}: {int(birthtime)} {to_datetime(birthtime)} {_now - birthtime}')
        if _now - birthtime > six_months:
            total_old_contents += 1
            print(_path)
    print(f'total contents: {total_contents}')
    print(f'total old contents: {total_old_contents}')


def remove_file(file_path: str) -> None:
    try:
        os.remove(file_path)
    except OSError as e:
        print(str(e))


def remove_directory(dir_path: str) -> None:
    try:
        shutil.rmtree(dir_path)
    except OSError as e:
        print(str(e))


def get_date_added():
    contents = os.listdir(BASE_DIR)
    _now = time.time()
    six_months = dt.timedelta(days=365).total_seconds()
    total_contents = 0
    total_old_contents = 0
    files_deleted = []
    dirs_deleted = []
    for c in contents:
        total_contents += 1
        _path = os.path.join(BASE_DIR, c)
        cp: subprocess.CompletedProcess = subprocess.run(
            ['mdls', '-name', 'kMDItemDateAdded', '-raw', f'{_path}'], check=True, stdout=subprocess.PIPE)
        # print(cp.stdout.decode('utf-8'))
        date_added = str(cp.stdout.decode('utf-8'))
        # print(str(st.stdout.decode('utf-8')))
        if 'null' not in date_added:
            date_added_timestamp = dt.datetime.strptime(
                date_added, '%Y-%m-%d %H:%M:%S %z').timestamp()
            age = _now - date_added_timestamp
            if age > six_months:
                total_old_contents += 1
                print(f'{_path}: {date_added}')
                if os.path.isfile(_path):
                    # remove_file(_path)
                    files_deleted.append(c)
                elif os.path.isdir(_path):
                    # remove_directory(_path)
                    dirs_deleted.append(c)
        else:
            # print(f'{_path}: {date_added}')
            pass

    print(f'total contents: {total_contents}')
    print(f'total old contents: {total_old_contents}')
    print(f'Files Deleted: {files_deleted}')
    print(f'Directories Deleted: {dirs_deleted}')


if __name__ == "__main__":
    get_date_added()