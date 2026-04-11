from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QObject, pyqtSignal
from pynput import keyboard
import win32gui
import win32con
import sys
import asyncio
from qasync import QEventLoop 
from window import Window
from tray import AppTray

class HotkeyListener(QObject):
    ##Declared signal for comunication with main thread
    activated = pyqtSignal(int)
    mode_int = pyqtSignal(int)
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
        placement = win32gui.GetWindowPlacement(hwnd)
        mode = placement[1]
        self.set_window_mode(mode)
        print("Window mode: ", mode)
        if mode == win32con.SW_SHOWMAXIMIZED:
            print("Maximizada")
        elif mode == win32con.SW_SHOWMINIMIZED:
            print("Minimizada")
        elif mode == win32con.SW_SHOWNORMAL:
            print("Normal")
        self.activated.emit(hwnd)
        self.mode_int.emit(mode)

    def set_window_mode(self, mode):
        self.window_mode = mode
    def get_window_mode(self):
        return self.window_mode()

    
    def _on_stop(self):
        self.stopped.emit()
    
    def _on_show_translation(self):
        print("Traducción:", window.get_translated_text())

app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)

loop = QEventLoop(app)
asyncio.set_event_loop(loop)

window = Window()
listener = HotkeyListener()
tray = AppTray(app, window)

# Connect signal with main thread
listener.activated.connect(lambda hwnd: (
    window.set_last_window(hwnd),
    window.show_window()
))

listener.mode_int.connect(lambda mode: window.set_window_mode(mode))

# Close app
listener.stopped.connect(app.quit)
listener.start()

#window.show_window()

with loop:
    loop.run_forever()
