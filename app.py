from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from components.settings_form import SettingsForm
from components.bottom_bar import BottomBar
from components.terminal_block import TerminalBlock
from services.validator import Validator
from services.executor import CommandExecutor
import tempfile
import os

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
        
        self.settings = SettingsForm()
        self.terminal = TerminalBlock()
        self.bottom = BottomBar()
        self.executor = CommandExecutor(self.terminal)
        
        self.bottom.on_create(self.generate_config)
        
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
        
        results = [
            ("Nginx", Validator.check_nginx_installed()),
            ("Директории", Validator.check_directories_exist()),
            ("Валидация имени", Validator.validate_domain_name(domain)),
            ("Конфиг", Validator.check_config_exists(domain)),
        ]
        
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
        
        html_content = f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>{domain}.local</title></head>
<body><h1>{domain}.local работает!</h1></body>
</html>"""
        
        tmpfile = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.conf', encoding='utf-8')
        tmpfile.write(config_content)
        tmpfile.close()
        
        tmp_html = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.html', encoding='utf-8')
        tmp_html.write(html_content)
        tmp_html.close()
        
        def cleanup():
            for f in [tmpfile.name, tmp_html.name]:
                try:
                    os.unlink(f)
                except:
                    pass
        
        def on_finish(success, error_msg):
            if success:
                self.terminal.add_success(f"✅ Сайт {domain}.local успешно создан и активирован!")
                self.terminal.set_status(f"Готово! http://{domain}.local")
            else:
                self.terminal.set_status(f"Ошибка: {error_msg}", True)
        
        commands = [
            (f"pkexec cp {tmpfile.name} /etc/nginx/sites-available/{domain}", 
             f"Создание конфига {domain}", True),
            (f"pkexec chmod 644 /etc/nginx/sites-available/{domain}", 
             f"Права на конфиг", False),
            (f"pkexec ln -sf /etc/nginx/sites-available/{domain} /etc/nginx/sites-enabled/{domain}", 
             f"Активация сайта {domain}", True),
            (f"pkexec nginx -t", 
             "Проверка nginx", True),
            (f"pkexec systemctl reload nginx", 
             "Перезагрузка nginx", True),
            (f"pkexec mkdir -p /var/www/{domain}", 
             f"Директория /var/www/{domain}", True),
            (f"pkexec chown -R www-data:www-data /var/www/{domain}", 
             f"Права www-data на {domain}", False),
            (f"pkexec chmod -R 755 /var/www/{domain}", 
             f"Права на файлы {domain}", False),
            (f"pkexec sh -c 'echo 127.0.0.1 {domain}.local www.{domain}.local >> /etc/hosts'", 
             f"Добавление в /etc/hosts", True),
            (f"pkexec bash -c 'cp {tmp_html.name} /var/www/{domain}/index.html && chown www-data:www-data /var/www/{domain}/index.html && chmod 644 /var/www/{domain}/index.html'", 
             f"Создание index.html", True),
        ]
        
        self.executor.execute_commands(commands, on_finish, [cleanup])