from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from components.top_banner import TopBanner
from components.settings_form import SettingsForm
from components.bottom_bar import BottomBar
from components.terminal_block import TerminalBlock
from services.validator import Validator
from services.executor import CommandExecutor

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
        
        #self.banner = TopBanner()
        self.settings = SettingsForm()
        self.terminal = TerminalBlock()
        self.bottom = BottomBar()
        
        self.bottom.on_create(self.generate_config)
        self.executor = CommandExecutor(self.terminal)
        
        #layout.addWidget(self.banner)
        layout.addWidget(self.settings)
        layout.addWidget(self.terminal)
        layout.addWidget(self.bottom)
    
    def generate_config(self):
        domain = self.settings.get_domain()
        
        valid, msg = Validator.validate_domain_name(domain)
        if not valid:
            self.terminal.add_error(f"✗ {msg}")
            self.terminal.set_status("Ошибка валидации", True)
            return
        
        self.terminal.add_success(f"✓ Имя '{domain}' валидно")
        
        self.terminal.add_command("Проверка системы...")
        results = Validator.run_all_checks(domain)
        
        all_ok = True
        for check_name, (ok, msg) in results:
            if ok:
                self.terminal.add_success(f"  ✓ {check_name}: {msg}")
            else:
                self.terminal.add_error(f"  ✗ {check_name}: {msg}")
                all_ok = False
        
        if not all_ok:
            self.terminal.set_status("Исправьте ошибки и попробуйте снова", True)
            return
        
        self.terminal.add_command("Начинаю создание конфигурации...")
        
        config_content = f"""server {{
    listen 80;
    server_name {domain}.local www.{domain}.local;
    
    root /var/www/{domain};
    index index.html index.htm index.php;
    
    location / {{
        try_files $uri $uri/ =404;
    }}
    
    location ~ \.php$ {{
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
    }}
}}"""
        
        commands = [
            ("sudo apt update", "Обновление пакетов", True),
            (f"echo '{config_content}' | sudo tee /etc/nginx/sites-available/{domain} > /dev/null", 
             f"Создание конфига /etc/nginx/sites-available/{domain}", True),
            (f"sudo ln -s /etc/nginx/sites-available/{domain} /etc/nginx/sites-enabled/{domain}", 
             f"Активация сайта {domain}", True),
            ("sudo nginx -t", "Проверка конфигурации nginx", True),
            ("sudo systemctl reload nginx", "Перезагрузка nginx", True),
            (f"echo '127.0.0.1 {domain}.local www.{domain}.local' | sudo tee -a /etc/hosts", 
             f"Добавление {domain}.local в /etc/hosts", True),
        ]
        
        for cmd, desc, need_confirm in commands:
            success, output = self.executor.execute(cmd, desc, need_confirm)
            if not success:
                self.terminal.set_status(f"Ошибка при выполнении: {desc}", True)
                return
        
        self.terminal.add_success(f"✅ Сайт {domain}.local успешно создан и активирован!")
        self.terminal.set_status(f"Готово! Откройте http://{domain}.local в браузере")