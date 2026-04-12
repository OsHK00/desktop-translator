import asyncio
import sys

import logging
import time

import win32con
import win32gui
from pynput import keyboard
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QApplication
from qasync import QEventLoop

from translateapp.ui.tray import AppTray
from translateapp.ui.window import Window


class HotkeyListener(QObject):
    activated = pyqtSignal(int)
    mode_int = pyqtSignal(int)
    stopped = pyqtSignal()

    def __init__(self, window: Window):
        self.logger = logging.getLogger(__name__)
        super().__init__()
        self.window = window
        self.window_mode = None

    def start(self):
        self.hotkey = keyboard.GlobalHotKeys(
            {
                "<ctrl>+<shift>+0": self._on_activate,
                "<ctrl>+<shift>+9": self._on_stop,
                "<ctrl>+<shift>+8": self._on_show_translation,
            }
        )
        self.hotkey.start()
        self.logger.info("Servicio ejecutado")



    def _on_activate(self):
        time.sleep(0.05)
        hwnd = win32gui.GetForegroundWindow()
        placement = win32gui.GetWindowPlacement(hwnd)
        mode = placement[1]
        self.set_window_mode(mode)
        self.activated.emit(hwnd)
        self.mode_int.emit(mode)

    def set_window_mode(self, mode):
        self.window_mode = mode

    def get_window_mode(self):
        return self.window_mode

    def _on_stop(self):
        self.logger.info("Servicio detenido")
        self.stopped.emit()

    def _on_show_translation(self):
        self.logger.info("Traduccion: %s", self.window.get_translated_text())


def run():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = Window()
    listener = HotkeyListener(window)
    tray = AppTray(app, window)

    listener.activated.connect(
        lambda hwnd: (
            window.set_last_window(hwnd),
            window.show_window(),
        )
    )
    listener.mode_int.connect(lambda mode: window.set_window_mode(mode))
    listener.stopped.connect(app.quit)
    listener.start()

    with loop:
        loop.run_forever()


if __name__ == "__main__":
    run()
