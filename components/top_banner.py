from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel
from styles import Styles

class TopBanner(QFrame):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)
        
        tutorial_frame = QFrame()
        tutorial_frame.setStyleSheet(Styles.FRAME)
        tutorial_layout = QVBoxLayout(tutorial_frame)
        tutorial = QLabel("Генератор Nginx сайтов: введите название проекта и конфигурация будет сгенерирована автоматически")
        tutorial.setWordWrap(True)
        tutorial.setStyleSheet("font-size: 14px; font-weight: 400; border: none;")
        tutorial_layout.addWidget(tutorial)
        
        tip_frame = QFrame()
        tip_frame.setStyleSheet(Styles.FRAME)
        tip_layout = QVBoxLayout(tip_frame)
        tip = QLabel("Сайт будет доступен по ссылке: http://*.local")
        tip.setWordWrap(True)
        tip.setStyleSheet("font-size: 14px; font-weight: 400; border: none;")
        tip_layout.addWidget(tip)
        
        layout.addWidget(tutorial_frame)
        layout.addWidget(tip_frame)