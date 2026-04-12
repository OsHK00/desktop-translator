from __future__ import annotations

import sys
from pathlib import Path


def app_root() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parents[2]


def resource_path(*relative_parts: str) -> Path:

    rel = Path(*relative_parts)
    if getattr(sys, "frozen", False):
        meipass = getattr(sys, "_MEIPASS", None)
        if meipass:
            bundled = Path(meipass) / rel
            if bundled.exists():
                return bundled
    return app_root() / rel


def default_window_icon_path() -> Path:
    ico = resource_path("assets", "translate-icon.ico")
    if ico.exists():
        return ico
    return resource_path("assets", "translate-icon.png")
