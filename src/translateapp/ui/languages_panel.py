from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QButtonGroup, QVBoxLayout
from PyQt6.QtCore import Qt
import math

class LanguagePanel(QWidget):
    def __init__(self, parent=None, default_from=None, default_to=None):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.PANEL_WIDTH = 450
        self.BUTTON_HEIGHT = 35
        self.SPACING = 8
        self.MARGINS = 20
        self.COLUMNS = 2
        
        self.container = QWidget(self)
        self.container.setStyleSheet("""
            QWidget {
                background-color: rgba(0, 0, 0, 255);
                border-radius: 8px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)
        
        main_layout = QVBoxLayout(self.container)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(self.SPACING)
        
        self.button_group_from = QButtonGroup()
        self.button_group_from.setExclusive(True)
        
        self.button_group_to = QButtonGroup()
        self.button_group_to.setExclusive(True)
        
        self.buttons = {}
        self.clicked_by = None
        self.current_mode = None

        self.selected_from = default_from 
        self.selected_to = default_to 
        
        main_layout.addLayout(self.grid_layout)
        main_layout.addStretch()
        
        self.hide()
    
    def add_language(self, language_code: str, language_name: str):
        btn = QPushButton(language_name)
        btn.setCheckable(True)
        btn.setMinimumHeight(self.BUTTON_HEIGHT)
        btn.setStyleSheet("""
            QPushButton {
                padding: 6px 10px;
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.2);
                background-color: transparent;
                font-size: 13px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.4);
            }
            QPushButton:checked {
                background-color: white;
                border: 1px solid #0055b8;
                font-weight: bold;
                color: black;
            }
        """)
        
        btn.clicked.connect(lambda: self.on_language_selected(language_code))
        
        self.button_group_from.addButton(btn)
        self.button_group_to.addButton(btn)
        
        self.buttons[language_code] = btn 
        count = len(self.buttons) - 1
        row = count // self.COLUMNS
        col = count % self.COLUMNS
        self.grid_layout.addWidget(btn, row, col)
        
        self.adjust_panel_size()

        
        return btn
    
    def adjust_panel_size(self):
        num_languages = len(self.buttons)
        num_rows = math.ceil(num_languages / self.COLUMNS)
        height = self.MARGINS + (num_rows * self.BUTTON_HEIGHT) + ((num_rows - 1) * self.SPACING)
        self.resize(self.PANEL_WIDTH, height)
        self.container.setGeometry(0, 0, self.PANEL_WIDTH, height)
    
    def on_language_selected(self, language_code: str):
        if self.current_mode == "from":
            self.selected_from = language_code
        elif self.current_mode == "to":
            self.selected_to = language_code
        
        if self.clicked_by:
            self.clicked_by(language_code)
        self.hide_panel()
    
    def show_panel(self, callback, mode="from"):
        if self.is_visible() == True:
            self.hide_panel()
            return
        
        self.clicked_by = callback
        self.current_mode = mode
        
        self.button_group_from.setExclusive(False)
        self.button_group_to.setExclusive(False)
        

        for btn in self.buttons.values():
            btn.setChecked(False)
        
        self.button_group_from.setExclusive(True)
        self.button_group_to.setExclusive(True)
        
        if mode == "from" and self.selected_from:
            if self.selected_from in self.buttons:
                self.buttons[self.selected_from].setChecked(True)
        elif mode == "to" and self.selected_to:
            if self.selected_to in self.buttons:
                self.buttons[self.selected_to].setChecked(True)

        
        self.center_on_screen()
        self.show()
        self.raise_()
    
    def hide_panel(self):
        self.hide()
        self.clicked_by = None
    
    def center_on_screen(self):
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y-90)

    def is_visible(self):
        return self.isVisible() 
    
