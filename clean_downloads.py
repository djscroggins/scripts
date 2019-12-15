from modules.directory_cleaner import DirectoryCleaner

BASE_DIR = '/Users/davidscroggins/Downloads'

if __name__ == "__main__":
    dc = DirectoryCleaner(base_dir=BASE_DIR, max_age=340)
    dc.remove_old_content()
