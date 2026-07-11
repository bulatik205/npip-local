import webbrowser
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt
from styles import Styles

class BottomBar(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)
        
        self.btn_repo = QPushButton("GitHub")
        self.btn_repo.setFixedWidth(150)
        self.btn_repo.setStyleSheet(Styles.button())
        self.btn_repo.clicked.connect(lambda: webbrowser.open("https://github.com/bulatik205/npip-local"))
        layout.addWidget(self.btn_repo)
        
        self.btn_profile = QPushButton("Разработчик")
        self.btn_profile.setFixedWidth(150)
        self.btn_profile.setStyleSheet(Styles.button("transparent"))
        self.btn_profile.clicked.connect(lambda: webbrowser.open("https://github.com/bulatik205"))
        layout.addWidget(self.btn_profile)
        
        layout.addStretch()
        
        self.btn_create = QPushButton("Создать")
        self.btn_create.setFixedWidth(150)
        self.btn_create.setStyleSheet(Styles.button())
        layout.addWidget(self.btn_create)
    
    def on_create(self, callback):
        self.btn_create.clicked.connect(callback)