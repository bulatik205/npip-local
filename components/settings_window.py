from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QWidget
from PyQt6.QtCore import Qt, pyqtSignal
from services.config_manager import get_save_mode, set_save_mode


class SettingsWindow(QDialog):
    save_mode_changed = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Настройки")
        self.resize(600, 400)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Save mode switch
        save_layout = QHBoxLayout()
        save_label = QLabel("Save mode")
        save_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        save_layout.addWidget(save_label)

        self._save_mode_value = get_save_mode()

        self.save_switch = QPushButton()
        self.save_switch.setFixedSize(80, 30)
        self.save_switch.setCursor(Qt.CursorShape.PointingHandCursor)
        self.save_switch.clicked.connect(self._toggle_save_mode)
        save_layout.addWidget(self.save_switch)
        save_layout.addStretch()

        self._update_switch()

        save_container = QWidget()
        save_container.setLayout(save_layout)
        layout.addWidget(save_container)

        self.setLayout(layout)

    def _toggle_save_mode(self):
        self._save_mode_value = not self._save_mode_value
        set_save_mode(self._save_mode_value)
        self._update_switch()
        self.save_mode_changed.emit(self._save_mode_value)

    def _update_switch(self):
        if self._save_mode_value:
            bg_color = "#458a7d"
            text = "true"
        else:
            bg_color = "#c21e0d"
            text = "false"

        self.save_switch.setText(text)
        self.save_switch.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_color};
                color: white;
                font-weight: bold;
                font-size: 12px;
                border: 1px solid #fff;
                border-radius: 15px;
                padding: 2px 10px;
            }}
            QPushButton:hover {{
                background-color: {bg_color};
            }}
        """)

    def is_save_mode_enabled(self) -> bool:
        return self._save_mode_value