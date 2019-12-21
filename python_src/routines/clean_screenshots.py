from pathlib import Path

from modules.directory_cleaner import DirectoryCleaner


BASE_DIR = Path('/Users/davidscroggins/Desktop/screenshots')

if __name__ == "__main__":
    dc = DirectoryCleaner(base_dir=BASE_DIR, max_age=180, preview=True)
    dc.remove_old_content()
