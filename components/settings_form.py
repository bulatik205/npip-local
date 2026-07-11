from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QLabel, QLineEdit
from styles import Styles

class SettingsForm(QGroupBox):
    def __init__(self):
        super().__init__("Настройки проекта")
        self.setStyleSheet(Styles.GROUP)
        
        layout = QVBoxLayout()
        
        label = QLabel("Введите название проекта:")
        label.setStyleSheet("font-size: 14px; margin-bottom: 5px;")
        layout.addWidget(label)
        
        self.input_domain = QLineEdit()
        self.input_domain.setPlaceholderText("Например: my-project")
        self.input_domain.setStyleSheet(Styles.INPUT)
        layout.addWidget(self.input_domain)
        
        self.setLayout(layout)
    
    def get_domain(self):
        return self.input_domain.text().strip()