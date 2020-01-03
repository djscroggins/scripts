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

    def __init__(self, target_dir: Union[Path, str], max_age: int = 180, preview: bool = False, debug: bool = False,
                 **kwargs):
        """

        Args:
            target_dir (Union[Path, str]): absolute path to directory at which to start execution;
                can be Path-like object or string
            max_age (int): threshold for acting on files in days
            preview (bool): when set to True, will only generate a report of operation to be performed
            debug (bool): when set to True, logs will be streamed to console 
        """
        self._total_contents = 0
        self._total_old_contents = 0
        self._files_deleted = []
        self._dirs_deleted = []
        self._bad_or_missing_metadata = []
        self._osx_system_content = {'.DS_Store', '.localized', '__MACOSX'}
        self._target_dir = target_dir if isinstance(
            target_dir, Path) else Path(target_dir).resolve()
        self._max_age = dt.timedelta(days=max_age).total_seconds()
        self._now = time.time()
        self._preview = preview

        logger_kwargs = dict(
            logger_name=kwargs.get('logger_name', type(self).__name__),
            logs_basedir=kwargs.get('logs_basedir', Path(
                __file__).resolve().parents[1].joinpath('logs')),
            logs_subdir_name=kwargs.get(
                'logs_subdir', 'directory-cleaning-logs'),
            log_file_name=kwargs.get('logs_file_name', 'directory-cleaning')
        )
        self._logger = self._get_logger(
            logging.DEBUG if debug else logging.INFO, **logger_kwargs)

    @staticmethod
    def _get_logger(log_level: int, **kwargs) -> logging.Logger:
        """
        Returns configured _logger. Streams to stdout if set to DEBUG, else writes to log file.
        Args:
            log_level (int): desired log level

        Returns:
            Configured _logger

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
            handler = TimedRotatingFileHandler(
                log_path.joinpath(log_file_name), when='W0')

        handler.setLevel(log_level)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def _remove_file(self, file_path: Union[str, Path]) -> None:
        try:
            os.remove(file_path)
        except Exception as e:
            self._logger.error(str(e))
            self._logger.error(tb.format_exc())
            sys.exit('Error executing clean up')

    def _remove_directory(self, dir_path: Union[Path, os.PathLike]) -> None:
        try:
            shutil.rmtree(dir_path)
        except Exception as e:
            self._logger.error(str(e))
            self._logger.error(tb.format_exc())
            sys.exit('Error executing clean up')

    def _handle_old_content(self, content_path: Path, timestamp: float) -> None:
        content_age = self._now - timestamp
        if content_age > self._max_age:
            self._total_old_contents += 1
            self._logger.debug(f'{content_path}: {content_age}')
            if Path(content_path).is_file():
                if not self._preview:
                    self._remove_file(content_path)
                self._files_deleted.append(str(content_path))
            elif Path(content_path).is_dir():
                if not self._preview:
                    self._remove_directory(content_path)
                self._dirs_deleted.append(str(content_path))

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
        self._logger.info(f'**** SUMMARY ****\n'
                          f'Total Contents: {self._total_contents}\n'
                          f'Total Contents to be Deleted: {self._total_old_contents}\n'
                          f'Files Deleted: {self._files_deleted}\n'
                          f'Directories (and contents) Deleted: {self._dirs_deleted}\n'
                          f'Bad/Missing Metadata: {self._bad_or_missing_metadata}\n')

    def remove_old_content(self) -> None:
        self._logger.info(f'Cleaning {self._target_dir}')
        target_objects: list = os.listdir(self._target_dir)

        for target_object in target_objects:
            self._total_contents += 1

            target_path = self._target_dir.joinpath(target_object)
            date_added = self._get_osx_date_added(target_path)

            if target_object not in self._osx_system_content:
                if 'null' in date_added:
                    self._bad_or_missing_metadata.append(str(target_path))
                    last_modified_timestamp: float = os.stat(
                        target_path).st_mtime
                    self._handle_old_content(
                        target_path, last_modified_timestamp)

                else:
                    date_added_timestamp: float = dt.datetime.strptime(
                        date_added, '%Y-%m-%d %H:%M:%S %z').timestamp()
                    self._handle_old_content(target_path, date_added_timestamp)

        self.log_results()
