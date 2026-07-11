import os
import re
import subprocess

class Validator:
    @staticmethod
    def check_nginx_installed():
        """Проверяет, установлен ли nginx"""
        try:
            subprocess.run(["which", "nginx"], capture_output=True, check=True)
            return True, "Nginx установлен"
        except subprocess.CalledProcessError:
            return False, "Nginx не установлен. Выполните: sudo apt install nginx"

    @staticmethod
    def check_sudo_rights():
        """Проверяет, есть ли права sudo"""
        try:
            result = subprocess.run(
                ["sudo", "-n", "true"],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0, "Права sudo есть" if result.returncode == 0 else "Нужен пароль sudo"
        except:
            return False, "Не удалось проверить права sudo"

    @staticmethod
    def check_directories_exist():
        """Проверяет существование нужных папок"""
        dirs = [
            "/etc/nginx/sites-available",
            "/etc/nginx/sites-enabled"
        ]
        missing = [d for d in dirs if not os.path.exists(d)]
        if missing:
            return False, f"Отсутствуют папки: {', '.join(missing)}"
        return True, "Все директории на месте"

    @staticmethod
    def check_config_exists(domain):
        """Проверяет, не существует ли уже конфиг"""
        config_path = f"/etc/nginx/sites-available/{domain}"
        if os.path.exists(config_path):
            return False, f"Конфиг {domain} уже существует!"
        return True, "Конфиг свободен"

    @staticmethod
    def validate_domain_name(name):
        """
        Строгая валидация имени проекта:
        - только латиница, цифры, дефис
        - не начинается/заканчивается дефисом
        - длина 3-63 символа
        """
        if not name:
            return False, "Имя не может быть пустым"
        
        if len(name) < 3:
            return False, "Имя должно быть минимум 3 символа"
        
        if len(name) > 63:
            return False, "Имя должно быть не длиннее 63 символов"
        
        if name.startswith('-') or name.endswith('-'):
            return False, "Имя не может начинаться или заканчиваться дефисом"
        
        if '--' in name:
            return False, "Двойной дефис запрещён"
        
        pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?$'
        if not re.match(pattern, name):
            return False, "Только латиница, цифры и дефис. Не может начинаться/заканчиваться дефисом"
        
        forbidden = ['nginx', 'default', 'localhost', 'admin', 'root', 'test']
        if name.lower() in forbidden:
            return False, f"Имя '{name}' зарезервировано"
        
        return True, "Имя валидно"

    @staticmethod
    def run_all_checks(domain=None):
        """Запускает все проверки, возвращает список результатов"""
        results = []
        
        results.append(("Nginx", Validator.check_nginx_installed()))
        #results.append(("Права sudo", Validator.check_sudo_rights()))
        results.append(("Директории", Validator.check_directories_exist()))
        
        if domain:
            results.append(("Валидация имени", Validator.validate_domain_name(domain)))
            results.append(("Конфиг", Validator.check_config_exists(domain)))
        
        return results