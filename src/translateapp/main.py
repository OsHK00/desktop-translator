import sys
from pathlib import Path


def _ensure_src_on_path() -> None:
    if __package__ in (None, ""):
        src = Path(__file__).resolve().parents[1]
        root = str(src)
        if root not in sys.path:
            sys.path.insert(0, root)


_ensure_src_on_path()

from translateapp.core import logg_manager

logg_manager.setup_logger()

from translateapp.config.initial_config_file import create_config_file

create_config_file()

from translateapp.core.global_hotkey import run


if __name__ == "__main__":
    run()
