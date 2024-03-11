# lang.py
import glob

class I18N:
    def __init__(self, language, load_from_file=True):
        self.language = language
        self.load_from_file = load_from_file
        self.load_translation()

    def load_translation(self):
            self.load_data_from_file()

    def load_data_from_file(self):
        lang_data = {}
        lang_file = f"data_{self.language.lower()}.lang"
        with open(file=lang_file, encoding="utf-8") as f:
            for line in f:
                key, val = line.strip().split("=")
                lang_data[key] = val

        for key, val in lang_data.items():
            setattr(self, key, val)

    @staticmethod
    def get_available_languages():
        language_files = glob.glob("data_*.lang")
        language_codes = [f.replace("data_", "").replace(".lang", "") for f in language_files]
        return language_codes