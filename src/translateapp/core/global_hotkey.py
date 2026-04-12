import asyncio
import sys

import logging
import win32con
import win32gui
from pynput import keyboard
from PyQt6.QtCore import QObject, QTimer, pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication
from qasync import QEventLoop


from translateapp.config.loadconfig import Config
from translateapp.paths import default_window_icon_path
from translateapp.ui.tray import AppTray
from translateapp.ui.window import Window

config = Config()


class HotkeyListener(QObject):
    """hwnd + ShowWindow mode from GetWindowPlacement; single signal keeps updates atomic."""
    activated = pyqtSignal(int, int)
    stopped = pyqtSignal()
    first_run = False


    def __init__(self, window: Window):
        self.logger = logging.getLogger(__name__)
        super().__init__()
        self.window = window
        self.window_mode = None
        first_run = False


    def set_first_run(self, value: bool):
        self.first_run = value
    def get_first_run(self):
        return self.first_run

    def start(self):
        self.hotkey = keyboard.GlobalHotKeys(
            {
                config.get_keyboard_shortcut_start(): self._on_activate,
                config.get_keyboard_shortcut_stop(): self._on_stop,
                config.get_keyboard_shortcut_show_translation(): self._on_show_translation,
            }
        )
        self.hotkey.start()
        self.logger.info("Service started")



    def _on_activate(self):
        # Capture foreground immediately: a leading sleep lets the main thread / shell
        # change the active window before we read it (worse on first hotkey after start).
        hwnd = win32gui.GetForegroundWindow()
        try:
            placement = win32gui.GetWindowPlacement(hwnd)
            mode = placement[1]
        except Exception:
            mode = win32con.SW_NORMAL
        self.set_window_mode(mode)
        self.activated.emit(hwnd, mode)

    def set_window_mode(self, mode):
        self.window_mode = mode

    def get_window_mode(self):
        return self.window_mode

    def _on_stop(self):
        self.logger.info("Service stopped")
        self.stopped.emit()

    def _on_show_translation(self):
        self.logger.info("Traduccion: %s", self.window.get_translated_text())

def run():

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(str(default_window_icon_path())))
    app.setQuitOnLastWindowClosed(False)

    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = Window()
    listener = HotkeyListener(window)
    tray = AppTray(app, window)

    def _on_hotkey(hwnd: int, mode: int) -> None:
        window.set_window_mode(mode)
        window.set_last_window(hwnd)
        window.show_window()

    listener.activated.connect(_on_hotkey)
    listener.stopped.connect(app.quit)
    listener.start()

    QTimer.singleShot(0, window.prime_translation_bar_once)

    def _stop_hotkey_listener() -> None:
        log = logging.getLogger(__name__)
        h = getattr(listener, "hotkey", None)
        if h is None:
            return
        try:
            h.stop()
            h.join(timeout=3.0)
            if h.is_alive():
                log.warning("pynput hotkey thread still alive after stop/join")
        except Exception:
            log.debug("hotkey listener stop failed", exc_info=True)

    app.aboutToQuit.connect(_stop_hotkey_listener)

    with loop:
        loop.run_forever()


if __name__ == "__main__":
    run()

