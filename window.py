from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt
from translate import translate 
from clipboard import paste_traslation
from PyQt6.QtCore import QTimer
from qasync import QEventLoop, asyncSlot 

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
        self.win_mode = None

    def set_window_mode(self, mode):
        self.win_mode = mode

    def get_window_mode(self):
        return self.win_mode

    def configContainer(self):
        container = QWidget(self)
        container.setGeometry(0, 0, 800, 60)
        container.setStyleSheet("""
            QWidget {
                background-color: rgba(0, 0, 0, 255);
                border-radius: 15px;
            }
        """)
        return container

    def configLayout(self, container):
        layout = QHBoxLayout(container)
        icon = QLabel()
        icon.setPixmap(self.iconImage.scaled(40, 40))
        self.input_text = QLineEdit() 
        #self.input_text.setPlaceholderText("Escribe el texto a traducir y presiona Enter...")
        self.button = QPushButton("prueba")
        
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
        layout.addWidget(icon)
        layout.addWidget(self.input_text)
        layout.addWidget(self.button)

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
        self.set_base_text(self.input_text.text())
        
        translated = await translate(
            text_=self.get_base_text(), 
            from_="es", 
            to_="en"
        )
        self.set_translated_text(translated)
        
        if self.get_translated_text() is None:
            print("entro")
            self.input_text.setStyleSheet("""
                QLineEdit {
                    border: none;
                    background: red;
                    color: white;
                    font-size: 18px;
                    padding: 8px;
                }
            """)

        if self.get_translated_text() is not None:
            paste_traslation(
                text=self.get_translated_text(),
                hwnd_window=self.get_last_window(),
                win_mode=self.get_window_mode()
            )
            self.hide_window()



    def show_window(self): #shows the window positioning it in front of everything and centering it, also focuses the input
        self.center_popup()
        self.input_text.clear()
        self.show()
        self.raise_()
        self.activateWindow()
        QTimer.singleShot(50, lambda: self.input_text.setFocus())

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
        super().focusOutEvent(event)
        self.hide_window()