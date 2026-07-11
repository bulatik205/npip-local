from PyQt6.QtWidgets import (QFrame, QVBoxLayout, QHBoxLayout, 
                             QTextEdit, QLabel, QPushButton, QApplication)
from PyQt6.QtCore import Qt, QEventLoop
from styles import Styles

class TerminalBlock(QFrame):
    def __init__(self):
        super().__init__()
        self.confirmation_result = None
        self._loop = None
        
        self.setStyleSheet("""
            QFrame {
                border: 1px solid #ccc;
                border-radius: 10px;
                background-color: #1e1e1e;
                padding: 5px;
            }
        """)
        
        layout = QVBoxLayout(self)
        
        header = QLabel("Терминал")
        header.setStyleSheet("color: #888; font-size: 12px; font-weight: bold; border: none;")
        layout.addWidget(header)
        
        self.output = QTextEdit()
        self.output.setReadOnly(True)
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
        layout.addWidget(self.output)
        
        self.confirm_bar = QFrame()
        self.confirm_bar.setStyleSheet("""
            QFrame {
                background-color: #2d2d2d;
                border-radius: 5px;
                padding: 8px;
            }
        """)
        self.confirm_bar.hide()
        
        confirm_layout = QHBoxLayout(self.confirm_bar)
        
        self.confirm_label = QLabel("")
        self.confirm_label.setStyleSheet("color: #ddd; font-size: 12px; border: none;")
        confirm_layout.addWidget(self.confirm_label)
        
        confirm_layout.addStretch()
        
        self.btn_yes = QPushButton("Да")
        self.btn_yes.setFixedWidth(80)
        self.btn_yes.setStyleSheet(Styles.terminal_button("#2ecc71"))
        self.btn_yes.clicked.connect(self._on_yes)
        
        self.btn_no = QPushButton("Нет")
        self.btn_no.setFixedWidth(80)
        self.btn_no.setStyleSheet(Styles.terminal_button("#e74c3c"))
        self.btn_no.clicked.connect(self._on_no)
        
        confirm_layout.addWidget(self.btn_yes)
        confirm_layout.addWidget(self.btn_no)
        
        layout.addWidget(self.confirm_bar)
        
        self.status_bar = QFrame()
        self.status_bar.setStyleSheet("""
            QFrame {
                background-color: #2d2d2d;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        status_layout = QHBoxLayout(self.status_bar)
        
        self.status_text = QLabel("Готов к работе")
        self.status_text.setStyleSheet("color: #aaa; font-size: 12px; border: none;")
        status_layout.addWidget(self.status_text)
        
        status_layout.addStretch()
        
        self.btn_copy = QPushButton("Копировать")
        self.btn_copy.setFixedWidth(100)
        self.btn_copy.setStyleSheet(Styles.terminal_button("#444"))
        self.btn_copy.clicked.connect(self.copy_output)
        status_layout.addWidget(self.btn_copy)
        
        self.btn_clear = QPushButton("Очистить")
        self.btn_clear.setFixedWidth(100)
        self.btn_clear.setStyleSheet(Styles.terminal_button("#444"))
        self.btn_clear.clicked.connect(self.output.clear)
        status_layout.addWidget(self.btn_clear)
        
        layout.addWidget(self.status_bar)
    
    def _on_yes(self):
        self.confirmation_result = "yes"
        if self._loop:
            self._loop.quit()
    
    def _on_no(self):
        self.confirmation_result = "no"
        if self._loop:
            self._loop.quit()
    
    def add_command(self, text):
        self.output.append(f'<span style="color: #3498db;">● {text}</span>')
        QApplication.processEvents()
    
    def add_output(self, text):
        for line in text.split('\n'):
            self.output.append(f'<span style="color: #bbb;">  {line}</span>')
        QApplication.processEvents()
    
    def add_error(self, text):
        self.output.append(f'<span style="color: #e74c3c;">{text}</span>')
        QApplication.processEvents()
    
    def add_success(self, text):
        self.output.append(f'<span style="color: #2ecc71;">{text}</span>')
        QApplication.processEvents()
    
    def set_status(self, text, is_error=False):
        self.status_text.setText(text)
        color = "#e74c3c" if is_error else "#aaa"
        self.status_text.setStyleSheet(f"color: {color}; font-size: 12px; border: none;")
    
    def ask_confirmation(self, command_text):
        """Показывает плашку Да/Нет и ждёт ответа"""
        self.confirmation_result = None
        self.confirm_label.setText(f"Команда: {command_text}")
        self.confirm_bar.show()
    
        self._loop = QEventLoop()
        self._loop.exec()
        self._loop = None
        
        self.confirm_bar.hide()
        return self.confirmation_result == "yes"
    
    def copy_output(self):
        QApplication.clipboard().setText(self.output.toPlainText())
        self.set_status("Скопировано в буфер обмена")