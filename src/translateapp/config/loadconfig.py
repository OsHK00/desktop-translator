from pathlib import Path
import json

from translateapp.paths import app_root

PROJECT_ROOT = app_root()
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "config" / "config.json"
DEFAULT_CONFIG_LOG_PATH = PROJECT_ROOT / "logs" / "app.log"
DEFAULT_KEYBOARD_SHORTCUT = {
    "activate": "<ctrl>+<shift>+0",
    "stop": "<ctrl>+<shift>+9",
    "show_translation": "<ctrl>+<shift>+8",
}


class Config:
    def __init__(self, config_file: str | Path | None = None):
        self.config_path = Path(config_file) if config_file else DEFAULT_CONFIG_PATH
        if not self.config_path.is_absolute():
            self.config_path = PROJECT_ROOT / self.config_path

        with self.config_path.open(mode="r", encoding="utf-8") as f:
            self.config = json.load(f)
        self._ensure_config_schema()

    def _save(self):
        with self.config_path.open(mode="w", encoding="utf-8") as f:
            json.dump(self.config, f, ensure_ascii=False, indent=4)

    def _ensure_config_schema(self):
        changed = False
        keyboard_section = self.config.get("keyboard_shortcut")
        if not isinstance(keyboard_section, dict):
            self.config["keyboard_shortcut"] = DEFAULT_KEYBOARD_SHORTCUT.copy()
            changed = True
        else:
            for key, value in DEFAULT_KEYBOARD_SHORTCUT.items():
                if key not in keyboard_section:
                    keyboard_section[key] = value
                    changed = True
        if changed:
            self._save()

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
        self._save()

    def set_default_from(self, from_):
        self.config["default"]["from"] = from_
        self._save()

    def swap_default(self):
        pre_from = self.get_default_from()
        pre_to = self.get_default_to()

        self.config["default"]["from"] = pre_to
        self.config["default"]["to"] = pre_from

        self._save()

    def get_root_path(self):
        return PROJECT_ROOT
    
    def get_config_path(self):
        return DEFAULT_CONFIG_PATH

    def get_log_path(self):
        return DEFAULT_CONFIG_LOG_PATH
    
    def get_keyboard_shortcut_start(self):
        return self.config.get("keyboard_shortcut", {}).get(
            "activate", DEFAULT_KEYBOARD_SHORTCUT["activate"]
        )
    
    def get_keyboard_shortcut_stop(self):
        return self.config.get("keyboard_shortcut", {}).get(
            "stop", DEFAULT_KEYBOARD_SHORTCUT["stop"]
        )
    
    def get_keyboard_shortcut_show_translation(self):
        return self.config.get("keyboard_shortcut", {}).get(
            "show_translation", DEFAULT_KEYBOARD_SHORTCUT["show_translation"]
        )
