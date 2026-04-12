from pathlib import Path

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt
from translateapp.ui.languages_panel import LanguagePanel
from translateapp.core.translate import translate 
from translateapp.core.clipboard import paste_traslation
from PyQt6.QtCore import QTimer
from qasync import asyncSlot 
from translateapp.config.loadconfig import Config

PROJECT_ROOT = Path(__file__).resolve().parents[3]

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(900, 60)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.config = Config()

        self.language_panel = LanguagePanel(
            self,
            default_from=self.config.get_default_from(),
            default_to=self.config.get_default_to()
        )
        self.load_languages_from_config()

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.iconImage = QPixmap(str(PROJECT_ROOT / "assets" / "translate-icon.png"))
        self.hide()
        self.base_text = ""
        self.translated_text = ""
        self.last_window = None
        self.container = self.configContainer()
        self.win_mode = None
        self.configLayout(self.container)
        self.setStyleSheet("""
            QWidget {
                border: none;
                outline: none;
                margin: 0px;
                padding: 0px;
            }
        """)



    def set_window_mode(self, mode):
        self.win_mode = mode

    def get_window_mode(self):
        return self.win_mode

    def configContainer(self):
        container = QWidget(self)
        container.setGeometry(0, 0, 900, 60)
        container.setStyleSheet("""
            QWidget {
                background-color: rgba(0, 0, 0, 255);
                border-radius: 12px;
                border: none;
                outline: none;
                margin: 0px;
                padding: 0px;
            }
        """)
        return container




    
    def load_languages_from_config(self):
        languages = self.config.get_favorites()
        default_from = self.config.get_default_from()
        default_to = self.config.get_default_to()
        

        for language_name, language_code in languages.items():
            self.language_panel.add_language(language_code, language_name)


    def configLayout(self, container): 
        layout = QHBoxLayout(container)
        icon = QLabel()
        #layout.setContentsMargins(0, 0, 0, 0)
        #layout.setSpacing(0)
        icon.setPixmap(self.iconImage.scaled(40, 40))
        self.input_text = QLineEdit() 
        self.button_from = QPushButton(f"{ self.config.get_default_from().capitalize()}")
        self.button_switch = QPushButton("")
        self.button_to = QPushButton(f"{self.config.get_default_to().capitalize()}")
        self.button_switch.setText( "⮂" )
        self.button_switch.clicked.connect(self.swap_helper)
        self.button_from.setStyleSheet("""
            QPushButton {
                padding: 8px 10px;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #302d2d;
            }
            QPushButton:pressed {
                background-color: white;
                color: black;
            }
        """)

        self.button_to.setStyleSheet("""
            QPushButton {
                padding: 8px 10px;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #302d2d;
            }
            QPushButton:pressed {
                background-color: white;
                color: black;
            }
        """)
        self.button_switch.setStyleSheet("""
            QPushButton {
                padding: 8px 8px;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #302d2d;
            }
            QPushButton:pressed {
                background-color: #003d82;
            }
        """)
        self.input_text.setStyleSheet("""
            QLineEdit {
                border: none;
                background: transparent;
                color: white;
                font-size: 18px;
                padding: 8px;
            }
        """)
        self.input_text.returnPressed.connect(self.traslate_text)
        #layout.addWidget(icon)

        self.button_from.clicked.connect(lambda: self.language_panel.show_panel(self.set_from_language, mode="from"))
        self.button_to.clicked.connect(lambda: self.language_panel.show_panel(self.set_to_language, mode="to"))
            
        layout.addWidget(self.input_text)
        layout.addWidget(self.button_from)
        layout.addWidget(self.button_switch)
        layout.addWidget(self.button_to)

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

    @asyncSlot()  
    async def traslate_text(self):
        #self.input_text.setDisabled(True)  
        self.set_base_text(self.input_text.text())
        from_target = self.config.get_default()
        
        translated = await translate(
            text_=self.get_base_text(), 
            from_=from_target["from"], 
            to_=from_target["to"]
        )
        self.set_translated_text(translated)


        if self.get_translated_text() is not None:
            print("jocda")
            paste_traslation(
                text=self.get_translated_text(),
                hwnd_window=self.get_last_window(),
                win_mode=self.get_window_mode()
            )
            self.hide_window()


    def swap_helper(self):
        self.config.swap_default()
        print("coño")
        self.button_switch.setText( "⮂" )
        self.button_from.setText(f"{ self.config.get_default_from().capitalize()}")
        self.button_to.setText(f"{self.config.get_default_to().capitalize()}")

        self.language_panel.selected_from = self.config.get_default_from()
        self.language_panel.selected_to = self.config.get_default_to()


    def set_from_language(self, language_code: str):
        self.config.set_default_from(language_code)
        self.button_from.setText(language_code.capitalize())

    def set_to_language(self, language_code: str):
        print("deberia")
        self.config.set_default_to(language_code)
        self.button_to.setText(language_code.capitalize())


    def show_window(self):
        self.center_popup()
        self.input_text.clear()
        self.show()
        self.raise_()
        self.activateWindow()
        QTimer.singleShot(50, lambda: self.input_text.setFocus())

    def hide_window(self):
        self.hide()
        self.language_panel.hide_panel()

    def center_popup(self):
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.hide_window()

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.hide_window()
