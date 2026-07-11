from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QApplication
from PyQt6.QtCore import Qt
from components.top_banner import TopBanner
from components.settings_form import SettingsForm
from components.bottom_bar import BottomBar
from components.terminal_block import TerminalBlock

class NginxConfigurator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NPIP")
        self.resize(800, 600)
        self.setMinimumSize(500, 300)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Собираем из компонентов
        self.banner = TopBanner()
        self.settings = SettingsForm()
        self.terminal = TerminalBlock()  # ← новый блок
        self.bottom = BottomBar()
        
        # Подключаем логику
        self.bottom.on_create(self.generate_config)
        
        layout.addWidget(self.banner)
        layout.addWidget(self.settings)
        layout.addWidget(self.terminal)  # ← растянется сам
        layout.addWidget(self.bottom)
    
    def generate_config(self):
        domain = self.settings.get_domain()
        if not domain:
            self.terminal.set_status("Ошибка: введите название проекта", True)
            return
        
        self.terminal.add_line(f"$ sudo mkdir -p /etc/nginx/sites-available")
        self.terminal.add_line(f"$ sudo tee /etc/nginx/sites-available/{domain}.conf")
        self.terminal.add_line(f"server {{")
        self.terminal.add_line(f"    listen 80;")
        self.terminal.add_line(f"    server_name {domain}.local;")
        self.terminal.add_line(f"    ...")
        self.terminal.add_line(f"}}")
        self.terminal.add_line(f"$ sudo ln -s /etc/nginx/sites-available/{domain}.conf /etc/nginx/sites-enabled/")
        self.terminal.add_line(f"$ sudo nginx -t && sudo systemctl reload nginx")
        self.terminal.add_line(f"")
        self.terminal.add_line(f"✅ Сайт {domain}.local успешно создан!")
        self.terminal.set_status(f"Конфигурация для {domain}.local сгенерирована")