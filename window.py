from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QHBoxLayout
from PyQt6.QtCore import Qt
from translate import simulate_traslation
from clipboard import paste_traslation
import sys


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800, 60)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.iconImage = QPixmap("assets/translate-icon.png")
        self.hide()

        self.base_text = ""
        self.translated_text = ""
        self.last_window = None

        self.container = self.configContainer()
        self.configLayout(self.container)

    def configContainer(self):
        container = QWidget(self)
        container.setGeometry(0, 0, 800, 60)
        container.setStyleSheet("""
            QWidget {
                background-color: rgba(0, 0, 0, 180);
                border-radius: 15px;
            }
        """)
        return container

    def configLayout(self, container):
        layout = QHBoxLayout(container)

        icon = QLabel()
        icon.setPixmap(self.iconImage.scaled(40, 40))

        self.input_text = QLineEdit()
        self.input_text.setStyleSheet("""
            QLineEdit {
                border: none;
                background: transparent;
                color: white;
                font-size: 18px;
                padding: 8px;
            }
        """)

        self.input_text.returnPressed.connect(self.traslate_text)  # 👈 Enter

        layout.addWidget(icon)
        layout.addWidget(self.input_text)

    def get_base_text(self):
        return self.base_text

    def set_base_text(self, text):
        self.base_text = text

    def get_translated_text(self):
        return self.translated_text

    def set_translated_text(self, translated: str):
        self.translated_text = translated

    def get_last_window(self):
        return self.last_window

    def set_last_window(self, hwnd_window):
        self.last_window = hwnd_window

    def traslate_text(self):
        self.set_base_text(self.input_text.text())
        self.set_translated_text(
            simulate_traslation(text_=self.get_base_text(), from_="Esp", to_="Eng")
        )
        paste_traslation(
            text=self.get_translated_text(),
            hwnd_window=self.get_last_window()
        )
        self.hide_window()

    def show_window(self):
        self.center_popup()
        self.input_text.clear()
        self.input_text.setFocus()
        self.show()

    def hide_window(self):
        self.hide()

    def center_popup(self):
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.hide_window()

    def focusOutEvent(self, event):
        self.hide_window()

