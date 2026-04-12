from pathlib import Path
import json

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "config" / "config.json"


class Config:
    def __init__(self, config_file: str | Path | None = None):
        self.config_path = Path(config_file) if config_file else DEFAULT_CONFIG_PATH
        if not self.config_path.is_absolute():
            self.config_path = PROJECT_ROOT / self.config_path

        with self.config_path.open(mode="r", encoding="utf-8") as f:
            self.config = json.load(f)

    def get_default(self):
        data = self.config["default"]
        if data == None:
            return "No data"
        else:
            return data
    
    def get_languages(self):
        return self.config["languages"]
    
    def get_default_to(self):
        return self.get_default()["to"]
    
    def get_default_from(self):
        return self.get_default()["from"] 
    
    def get_favorites(self):
        return self.config["favorites"]

    def set_default_to(self, to_):
        self.config["default"]["to"] = to_
        with self.config_path.open(mode="w", encoding="utf-8") as f:
            json.dump(self.config, f, ensure_ascii=False, indent=4)

    def set_default_from(self, from_):
        self.config["default"]["from"] = from_
        with self.config_path.open(mode="w", encoding="utf-8") as f:
            json.dump(self.config, f, ensure_ascii=False, indent=4)

    def swap_default(self):
        pre_from = self.get_default_from()
        pre_to = self.get_default_to()

        self.config["default"]["from"] = pre_to
        self.config["default"]["to"] = pre_from

        with self.config_path.open(mode="w", encoding="utf-8") as f:
            json.dump(self.config, f, ensure_ascii=False, indent=4)

