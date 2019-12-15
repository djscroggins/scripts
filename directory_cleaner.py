import datetime as dt
import logging
import os
import shutil
import subprocess as sp
import time


class DirectoryCleaner:
    def __init__(self, base_dir: str, max_age: int = 180, verbose=False, preview=False, log_level=logging.INFO):
        self.total_contents = 0
        self.total_old_contents = 0
        self.files_deleted = []
        self.dirs_deleted = []
        self.base_dir = base_dir
        self.max_age = dt.timedelta(days=max_age).total_seconds()
        self.now = time.time()
        self.verbose = verbose
        self.preview = preview
        self.logger = self.get_logger(log_level)

    @staticmethod
    def get_logger(log_level):
        logger = logging.getLogger('DirectoryCleaner')
        logger.setLevel(log_level)
        if log_level == 10:
            ch = logging.StreamHandler()
        else:
            ch = logging.FileHandler('directory-cleaning')
        ch.setLevel(log_level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger

    @staticmethod
    def _remove_file(file_path: str) -> None:
        try:
            os.remove(file_path)
        except OSError as e:
            print(str(e))

    @staticmethod
    def _remove_directory(dir_path: str) -> None:
        try:
            shutil.rmtree(dir_path)
        except OSError as e:
            print(str(e))

    @staticmethod
    def _get_date_added(content_path: str) -> str:
        cp: sp.CompletedProcess = sp.run(
            ['mdls', '-name', 'kMDItemDateAdded', '-raw', f'{content_path}'], check=True, stdout=sp.PIPE)
        return str(cp.stdout.decode('utf-8'))

    def log_results(self):
        self.logger.info(f'total contents: {self.total_contents}')
        self.logger.info(f'total old contents: {self.total_old_contents}')
        self.logger.info(f'Files Deleted: {self.files_deleted}')
        self.logger.info(f'Directories Deleted: {self.dirs_deleted}')

    def remove_old_content(self):
        directory_contents = os.listdir(self.base_dir)

        for content in directory_contents:
            self.total_contents += 1
            content_path = os.path.join(self.base_dir, content)
            date_added = self._get_date_added(content_path)
            if 'null' not in date_added:
                date_added_timestamp = dt.datetime.strptime(
                    date_added, '%Y-%m-%d %H:%M:%S %z').timestamp()
                age = self.now - date_added_timestamp
                if age > self.max_age:
                    self.total_old_contents += 1
                    if self.verbose:
                        self.logger.debug(f'{content_path}: {date_added}')
                    if os.path.isfile(content_path):
                        if not self.preview:
                            self._remove_file(content_path)
                        self.files_deleted.append(content)
                    elif os.path.isdir(content_path):
                        if not self.preview:
                            self._remove_directory(content_path)
                        self.dirs_deleted.append(content)
            else:
                # print(f'{_path}: {date_added}')
                pass

        self.log_results()
