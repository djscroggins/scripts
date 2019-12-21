import datetime as dt
import logging
from logging.handlers import TimedRotatingFileHandler
import os
from pathlib import Path
import shutil
import subprocess as sp
import sys
import time
import traceback as tb
from typing import Union


class DirectoryCleaner:
    """
    Utility class for identifying files to be deleted, currently based on age only
    """

    def __init__(self, base_dir: Union[Path, str], max_age: int = 180, preview: bool = False, debug: bool = False,
                 **kwargs):
        """

        Args:
            base_dir (str): absolute path to directory at which to start execution
            max_age (int): threshold for acting on files in days
            preview (bool): when set to True, will only generate a report of operation to be performed
            debug (bool): when set to True, logs will be streamed to console rather than written to file
        """
        self.total_contents = 0
        self.total_old_contents = 0
        self.files_deleted = []
        self.dirs_deleted = []
        self.bad_metadata = []
        self.osx_system_content = {'.DS_Store', '.localized', '__MACOSX'}
        self.base_dir = base_dir if isinstance(base_dir, Path) else Path(base_dir)
        self.max_age = dt.timedelta(days=max_age).total_seconds()
        self.now = time.time()
        self.preview = preview

        logger_kwargs = dict(
            logger_name=kwargs.get('logger_name', type(self).__name__),
            logs_basedir=kwargs.get('logs_basedir', Path(__file__).resolve().parents[1].joinpath('logs')),
            logs_subdir_name=kwargs.get('logs_subdir', 'directory-cleaning-logs'),
            log_file_name=kwargs.get('logs_file_name', 'directory-cleaning')
        )
        self.logger = self._get_logger(logging.DEBUG if debug else logging.INFO, **logger_kwargs)

    @staticmethod
    def _get_logger(log_level: int, **kwargs) -> logging.Logger:
        """
        Returns configured logger. Streams to stdout if set to DEBUG, else writes to log file.
        Args:
            log_level (int): desired log level

        Returns:
            Configured logger

        """
        logger_name = kwargs.get('logger_name')
        logs_basedir = kwargs.get('logs_basedir')
        logs_subdir_name = kwargs.get('logs_subdir_name')
        log_file_name = kwargs.get('log_file_name')

        logger = logging.getLogger(logger_name)
        logger.setLevel(log_level)

        if log_level == 10:
            handler = logging.StreamHandler()
        else:
            log_path = logs_basedir.joinpath(logs_subdir_name)
            if not log_path.exists():
                os.mkdir(log_path)
            handler = TimedRotatingFileHandler(log_path.joinpath(log_file_name), when='W0')

        handler.setLevel(log_level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def _remove_file(self, file_path: Union[str, Path]) -> None:
        try:
            os.remove(file_path)
        except Exception as e:
            self.logger.error(str(e))
            self.logger.error(tb.format_exc())
            sys.exit('Error executing clean up')

    def _remove_directory(self, dir_path: Union[Path, os.PathLike]) -> None:
        try:
            shutil.rmtree(dir_path)
        except Exception as e:
            self.logger.error(str(e))
            self.logger.error(tb.format_exc())
            sys.exit('Error executing clean up')

    def _handle_old_content(self, content_path: Path, timestamp) -> None:
        content_age = self.now - timestamp
        if content_age > self.max_age:
            self.total_old_contents += 1
            self.logger.debug(f'{content_path}: {content_age}')
            if Path(content_path).is_file():
                if not self.preview:
                    self._remove_file(content_path)
                self.files_deleted.append(str(content_path))
            elif Path(content_path).is_dir():
                if not self.preview:
                    self._remove_directory(content_path)
                self.dirs_deleted.append(str(content_path))

    @staticmethod
    def _get_osx_date_added(content_path: Path) -> str:
        """
        OSX-specific subprocess for identifying when a given file/directory was added, using 'mdls'
        a utility for listing metadata attributes of OSX files.

        This particular execution specifies that we only want the metadata for the date added
        and that we want only the date value itself.

        See https://ss64.com/osx/mdls.html for more detail on mdls.

        Args:
            content_path (str): path to file/directory

        Returns:
            str: date file was added as string; current OSX format is %Y-%m-%d %H:%M:%S %z

        """
        cp: sp.CompletedProcess = sp.run(
            ['mdls', '-name', 'kMDItemDateAdded', '-raw', f'{content_path}'], check=True, stdout=sp.PIPE)
        return str(cp.stdout.decode('utf-8'))

    def log_results(self) -> None:
        self.logger.info(f'\n**** SUMMARY ****'
                         f'\nTotal Contents: {self.total_contents}\n'
                         f'Total Contents to be Deleted: {self.total_old_contents}\n'
                         f'Files Deleted: {self.files_deleted}\n'
                         f'Directories (and contents) Deleted: {self.dirs_deleted}\n'
                         f'Bad/Missing Metadata: {self.bad_metadata}\n')

    def remove_old_content(self) -> None:
        self.logger.info(f'Cleaning {self.base_dir}')
        directory_contents = os.listdir(self.base_dir)

        for content in directory_contents:
            self.total_contents += 1

            content_path = self.base_dir.joinpath(content)
            date_added = self._get_osx_date_added(content_path)

            if content not in self.osx_system_content:
                if 'null' in date_added:
                    self.bad_metadata.append(str(content_path))
                    last_modified_timestamp = os.stat(content_path).st_mtime
                    self._handle_old_content(content_path, last_modified_timestamp)

                else:
                    date_added_timestamp = dt.datetime.strptime(
                        date_added, '%Y-%m-%d %H:%M:%S %z').timestamp()
                    self._handle_old_content(content_path, date_added_timestamp)

        self.log_results()
