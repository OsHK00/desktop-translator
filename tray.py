from PyQt6.QtCore import QObject
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QMenu, QSystemTrayIcon


class AppTray(QObject):
    def __init__(self, app, window, icon_path="assets/translate-icon.png"):
        super().__init__()
        self.app = app
        self.window = window

        self.tray = QSystemTrayIcon(QIcon(icon_path), self.app)
        self.tray.setToolTip("Desktop Translator")

        menu = QMenu()
        action_show_panel = QAction("Mostrar panel", menu)
        action_exit = QAction("Salir", menu)

        action_show_panel.triggered.connect(self.window.show_window)
        action_exit.triggered.connect(self.app.quit)

        menu.addAction(action_show_panel)
        menu.addSeparator()
        menu.addAction(action_exit)

        self.tray.setContextMenu(menu)
        self.tray.show()
