# components/terminal_block.py
from PyQt6.QtWidgets import (QFrame, QVBoxLayout, QHBoxLayout, 
                             QTextEdit, QLabel, QPushButton)
from styles import Styles

class TerminalBlock(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QFrame {
                border: 1px solid #ccc;
                border-radius: 10px;
                background-color: #2b2b2b;  /* чуть светлее */
                padding: 5px;
            }
        """)
        
        layout = QVBoxLayout(self)
        
        # Заголовок
        header = QLabel("Терминал")
        header.setStyleSheet("color: #888; font-size: 12px; font-weight: bold; border: none;")
        layout.addWidget(header)
        
        # Поле вывода команд
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #00ff00;  /* ярко-зелёный, точно видно */
                border: none;
                font-family: monospace;
                font-size: 13px;
                padding: 10px;
            }
        """)
        layout.addWidget(self.output)
        
        # Плашка статуса
        self.status_bar = QFrame()
        self.status_bar.setStyleSheet("""
            QFrame {
                background-color: #3a3a3a;  /* светлее */
                border-radius: 5px;
                padding: 5px;
            }
        """)
        status_layout = QHBoxLayout(self.status_bar)
        
        self.status_text = QLabel("Готов к работе")
        self.status_text.setStyleSheet("color: #ddd; font-size: 12px; border: none;") 
        status_layout.addWidget(self.status_text)
        
        status_layout.addStretch()
        
        # Кнопка "Копировать"
        self.btn_copy = QPushButton("Копировать")
        self.btn_copy.setFixedWidth(100)
        self.btn_copy.setStyleSheet(Styles.terminal_button("#444"))
        status_layout.addWidget(self.btn_copy)
        
        # Кнопка "Очистить"
        self.btn_clear = QPushButton("Очистить")
        self.btn_clear.setFixedWidth(100)
        self.btn_clear.setStyleSheet(Styles.terminal_button("#444"))
        self.btn_clear.clicked.connect(self.output.clear)
        status_layout.addWidget(self.btn_clear)
        
        layout.addWidget(self.status_bar)
    
    def add_line(self, text):
        self.output.append(text)
        self.output.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: white;
                border: none;
                font-family: monospace;
                font-size: 13px;
                padding: 10px;
            }
        """)
    
    def set_status(self, text, is_error=False):
        self.status_text.setText(text)
        color = "#e74c3c" if is_error else "#aaa"
        self.status_text.setStyleSheet(f"color: {color}; font-size: 12px; border: none;")