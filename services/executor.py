import subprocess
from PyQt6.QtCore import QThread, pyqtSignal

class CommandThread(QThread):
    output_signal = pyqtSignal(str, str) 
    finished_signal = pyqtSignal(bool, str)  
    
    def __init__(self, command):
        super().__init__()
        self.command = command
    
    def run(self):
        try:
            process = subprocess.Popen(
                self.command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            for line in process.stdout:
                self.output_signal.emit("output", line.strip())
            
            process.wait()
            
            if process.returncode == 0:
                self.finished_signal.emit(True, "")
            else:
                stderr = process.stderr.read()
                self.finished_signal.emit(False, stderr)
                
        except Exception as e:
            self.finished_signal.emit(False, str(e))


class CommandExecutor:
    def __init__(self, terminal):
        self.terminal = terminal
        self.current_thread = None
    
    def execute(self, command, description="", need_confirmation=True):
        if command.startswith("sudo "):
            command = command.replace("sudo ", "pkexec ", 1)
        
        self.terminal.add_command(f"Команда: {description or command}")
        
        if need_confirmation:
            confirmed = self.terminal.ask_confirmation(description or command)
            if not confirmed:
                self.terminal.add_error("✗ Команда отклонена пользователем")
                return False, "Отклонено"
        
        self.terminal.add_output(f"$ {command}")
        self.current_thread = CommandThread(command)
        self.current_thread.output_signal.connect(self._on_output)
        self.current_thread.finished_signal.connect(self._on_finished)
        self.current_thread.start()
        
        return True, "Выполняется..."
    
    def _on_output(self, msg_type, text):
        if text:
            self.terminal.add_output(text)
    
    def _on_finished(self, success, error_text):
        if success:
            self.terminal.add_success("✓ Успешно выполнено")
        else:
            self.terminal.add_error(f"✗ Ошибка: {error_text}")