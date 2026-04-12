import json
import logging

from translateapp.config.loadconfig import DEFAULT_CONFIG_PATH

logger = logging.getLogger(__name__)


def create_config_file() -> None:
    if DEFAULT_CONFIG_PATH.exists():
        logger.warning("config file already exists: %s", DEFAULT_CONFIG_PATH)
        return

    data = {
        "languages": {
            "Spanish": "es",
            "English": "en",
            "Japanese": "ja",
            "French": "fr",
            "German": "de",
            "Italian": "it",
            "Portuguese": "pt",
            "Russian": "ru"
        },
        "default": {
            "to": "en",
            "from": "es"
        },
        "favorites": {
            "Spanish": "es",
            "English": "en",
            "Japanese": "ja",
            "Italian": "it"
        },
        "Text_en": {
            "placeholder": "Type here to translate..."
        },
        "Text_es": {
            "placeholder": "Escribe aqui para traducir..."
        },
        "keyboard_shortcut": {
            "activate": "<ctrl>+<shift>+0",
            "stop": "<ctrl>+<shift>+9",
            "show_translation": "<ctrl>+<shift>+8"
        }
    }

    DEFAULT_CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with DEFAULT_CONFIG_PATH.open(mode="w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
