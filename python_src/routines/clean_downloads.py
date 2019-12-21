from pathlib import Path

from modules.directory_cleaner import DirectoryCleaner


BASE_DIR = Path('/Users/davidscroggins/Downloads')

LOG_CONFIG = {
    'logs_subdir': 'downloads-cleaning-logs',
    'logs_file_name': 'downloads-cleaning'
}

if __name__ == "__main__":
    dc = DirectoryCleaner(base_dir=BASE_DIR, max_age=180, **LOG_CONFIG)
    dc.remove_old_content()
