from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QObject, pyqtSignal
from pynput import keyboard
import win32gui
import sys
from window import Window


class HotkeyListener(QObject):
    ##Declared signal for comunication with main thread
    activated = pyqtSignal(int)
    stopped   = pyqtSignal()

    def start(self):
        #Declared Hotkeys
        self.hotkey = keyboard.GlobalHotKeys({
            '<ctrl>+<shift>+0': self._on_activate,
            '<ctrl>+<shift>+9': self._on_stop,
            '<ctrl>+<shift>+8': self._on_show_translation,
        })
        self.hotkey.start()
        print("Listening Hotkeys. . .")

    def _on_activate(self):
        hwnd = win32gui.GetForegroundWindow()

        self.activated.emit(hwnd)

    def _on_stop(self):
        self.stopped.emit()

    def _on_show_translation(self):
        print("Traducción:", window.get_translated_text())


app = QApplication(sys.argv)
window = Window()

listener = HotkeyListener()

#Connect signal with main thread
listener.activated.connect(lambda hwnd: (
    window.set_last_window(hwnd),
    window.show_window()
))
#Close app
listener.stopped.connect(app.quit)

listener.start()
window.show_window()
sys.exit(app.exec())