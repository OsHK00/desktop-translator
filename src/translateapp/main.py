import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.append(str(Path(__file__).resolve().parents[1]))

from translateapp.core.global_hotkey import run


if __name__ == "__main__":
    run()
