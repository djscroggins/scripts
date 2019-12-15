from modules.directory_cleaner import DirectoryCleaner

BASE_DIR = '/Users/davidscroggins/Downloads'

if __name__ == "__main__":
    dc = DirectoryCleaner(base_dir=BASE_DIR, max_age=340, preview=True, debug=False)
    dc.remove_old_content()
