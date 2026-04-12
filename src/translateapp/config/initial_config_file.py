import json
import logging

from translateapp.config.loadconfig import DEFAULT_CONFIG_PATH
logger = logging.getLogger(__name__)


def create_config_file() -> None:
    if DEFAULT_CONFIG_PATH.exists():
        logger.warning("Archivo de configuración ya existe: %s", DEFAULT_CONFIG_PATH)
        return
    


    else:
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
                "to": "es",
                "from": "it"
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
                "placeholder": "Escribe aquí para traducir..."
            }
        }


        DEFAULT_CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with DEFAULT_CONFIG_PATH.open(mode="w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)