from pathlib import Path

from PyQt6.QtCore import QObject
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QMenu, QSystemTrayIcon

PROJECT_ROOT = Path(__file__).resolve().parents[3]


class AppTray(QObject):
    def __init__(self, app, window, icon_path: str | Path | None = None):
        super().__init__()
        self.app = app
        self.window = window
        final_icon_path = Path(icon_path) if icon_path else (PROJECT_ROOT / "assets" / "translate-icon.png")
        if not final_icon_path.is_absolute():
            final_icon_path = PROJECT_ROOT / final_icon_path

        self.tray = QSystemTrayIcon(QIcon(str(final_icon_path)), self.app)
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
