from pathlib import Path

from modules.directory_cleaner import DirectoryCleaner


BASE_DIR = Path('/Users/davidscroggins/Desktop/screenshots')

LOG_CONFIG = {
    'logs_subdir': 'screenshots-cleaning-logs',
    'logs_file_name': 'screenshots-cleaning'
}

if __name__ == "__main__":
    dc = DirectoryCleaner(base_dir=BASE_DIR, max_age=180, preview=True, **LOG_CONFIG)
    dc.remove_old_content()
