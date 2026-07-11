import subprocess
from PyQt6.QtCore import QThread, pyqtSignal

class CommandWorker(QThread):
    """Выполняет команды последовательно в фоне"""
    command_output = pyqtSignal(str, str)  # type (output/error/success), text
    command_finished = pyqtSignal(bool, str)  # success, error_text
    all_finished = pyqtSignal()  # всё выполнено
    
    def __init__(self):
        super().__init__()
        self.queue = []  # очередь команд: (cmd, desc)
        self._running = True
    
    def add_command(self, command, description=""):
        self.queue.append((command, description))
    
    def run(self):
        for cmd, desc in self.queue:
            if not self._running:
                break
            
            self.command_output.emit("command", f"● Команда: {desc or cmd}")
            self.command_output.emit("output", f"$ {cmd}")
            
            try:
                result = subprocess.run(
                    cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.stdout:
                    self.command_output.emit("output", result.stdout.strip())
                
                if result.returncode == 0:
                    self.command_output.emit("success", "✓ Успешно выполнено")
                else:
                    self.command_output.emit("error", f"✗ Ошибка (код {result.returncode})")
                    if result.stderr:
                        self.command_output.emit("error", result.stderr.strip())
                    self.command_finished.emit(False, result.stderr)
                    return
                    
            except subprocess.TimeoutExpired:
                self.command_output.emit("error", "✗ Команда превысила время ожидания")
                self.command_finished.emit(False, "Timeout")
                return
            except Exception as e:
                self.command_output.emit("error", f"✗ Ошибка: {str(e)}")
                self.command_finished.emit(False, str(e))
                return
        
        self.command_finished.emit(True, "")
        self.all_finished.emit()
    
    def stop(self):
        self._running = False


class CommandExecutor:
    def __init__(self, terminal):
        self.terminal = terminal
        self.worker = None
        self._cleanup_callbacks = []
    
    def execute_commands(self, commands, on_finish=None, cleanup_callbacks=None):
        """
        commands: список кортежей (cmd, desc, need_confirmation)
        on_finish: колбэк после выполнения всех команд (success, error_msg)
        cleanup_callbacks: список функций для очистки временных файлов
        """
        # Сначала подтверждаем все команды
        confirmed_commands = []
        for cmd, desc, need_confirm in commands:
            if need_confirm:
                if not self.terminal.ask_confirmation(f"{desc}\n{cmd}"):
                    self.terminal.add_error(f"✗ Команда отклонена: {desc}")
                    if cleanup_callbacks:
                        for cb in cleanup_callbacks:
                            cb()
                    if on_finish:
                        on_finish(False, "Отклонено пользователем")
                    return
            confirmed_commands.append((cmd, desc))
        
        # Запускаем выполнение в фоне
        self.worker = CommandWorker()
        
        # Подключаем сигналы к терминалу
        self.worker.command_output.connect(self._on_output)
        self.worker.command_finished.connect(
            lambda success, msg: self._on_all_finished(success, msg, cleanup_callbacks, on_finish)
        )
        
        # Добавляем команды в очередь
        for cmd, desc in confirmed_commands:
            self.worker.add_command(cmd, desc)
        
        self.worker.start()
    
    def _on_output(self, msg_type, text):
        if msg_type == "command":
            self.terminal.add_command(text)
        elif msg_type == "output":
            self.terminal.add_output(text)
        elif msg_type == "success":
            self.terminal.add_success(text)
        elif msg_type == "error":
            self.terminal.add_error(text)
    
    def _on_all_finished(self, success, error_msg, cleanup_callbacks, on_finish):
        # Выполняем очистку
        if cleanup_callbacks:
            for cb in cleanup_callbacks:
                cb()
        
        if on_finish:
            on_finish(success, error_msg)