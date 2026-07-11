from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QWidget, QLineEdit
from PyQt6.QtCore import Qt, pyqtSignal
from services.config_manager import get_save_mode, set_save_mode, load_config, save_config
from styles import Styles


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

        save_layout.addStretch()

        self._save_mode_value = get_save_mode()

        self.save_switch = QPushButton()
        self.save_switch.setFixedSize(80, 30)
        self.save_switch.setCursor(Qt.CursorShape.PointingHandCursor)
        self.save_switch.clicked.connect(self._toggle_save_mode)
        save_layout.addWidget(self.save_switch)

        self._update_switch()

        save_container = QWidget()
        save_container.setLayout(save_layout)
        layout.addWidget(save_container)

        # Path inputs
        config = load_config()

        self.path_inputs = {}
        path_fields = [
            ("ngnixPath", "Nginx path"),
            ("sitesSrcPath", "Sites source path"),
            ("hosts", "Hosts path"),
        ]

        for key, label_text in path_fields:
            row = QHBoxLayout()
            lbl = QLabel(label_text)
            lbl.setStyleSheet("font-size: 14px; font-weight: bold;")
            lbl.setFixedWidth(150)
            row.addWidget(lbl)

            row.addStretch()

            inp = QLineEdit()
            inp.setText(config.get(key, ""))
            inp.setStyleSheet(Styles.INPUT)
            inp.setFixedWidth(400)
            row.addWidget(inp)

            self.path_inputs[key] = inp
            layout.addLayout(row)

        layout.addStretch()

        # Save button
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        self.save_btn = QPushButton("Сохранить")
        self.save_btn.setStyleSheet(Styles.button())
        self.save_btn.setFixedSize(140, 40)
        self.save_btn.clicked.connect(self._save_paths)
        btn_layout.addWidget(self.save_btn)
        layout.addLayout(btn_layout)

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
            bg_color = "#8a4552"
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

    def _save_paths(self):
        config = load_config()
        for key, inp in self.path_inputs.items():
            config[key] = inp.text()
        save_config(config)

    def is_save_mode_enabled(self) -> bool:
        return self._save_mode_value