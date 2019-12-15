from directory_cleaner import DirectoryCleaner
import logging

BASE_DIR = '/Users/davidscroggins/Downloads'

if __name__ == "__main__":
    dc = DirectoryCleaner(base_dir=BASE_DIR, max_age=365, verbose=True, preview=True)
    dc.remove_old_content()
    # dc.print_report()
