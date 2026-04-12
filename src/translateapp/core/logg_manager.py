from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from translateapp.config.loadconfig import Config


def setup_logger(config: Config | None = None) -> None:
    from translateapp.config.loadconfig import Config, DEFAULT_CONFIG_LOG_PATH

    if config is not None:
        log_path = config.get_log_path()
    else:
        
        log_path = DEFAULT_CONFIG_LOG_PATH
    log_path = Path(log_path)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        filename=str(log_path),
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(filename)s:%(lineno)d | %(message)s",
        force=True,
    )
    logging.getLogger("translateapp").setLevel(logging.DEBUG)

