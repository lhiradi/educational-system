import logging
import os
from datetime import datetime


class Logger:
    def __init__(self, name, log_root="logs"):
        self.name = name
        self.log_root = log_root
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self.logger.propagate = False
        
        self.current_date = datetime.now().date()
        self.file_handler = None
        self._setup_handler()
        
    def _get_log_file_path(self):
        date_str = self.current_date.strftime("%Y-%m-%d")
        log_dir = os.path.join(self.log_root, date_str)
        os.makedirs(log_dir, exist_ok=True)
        return os.path.join(log_dir, f"{self.name}.log")
    
    def _setup_handler(self):
        if self.file_handler:
            self.logger.removeHandler(self.file_handler)
            self.file_handler.close()
        
        log_path = self._get_log_file_path()
        self.file_handler = logging.FileHandler(log_path, encoding="utf-8")
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        ) 
        
        self.file_handler.setFormatter(formatter)
        self.logger.addHandler(self.file_handler)
        
    def _check_date_and_rotate(self):
        now = datetime.now().date()
        if now != self.current_date:
            self.current_date = now
            self._setup_handler()
            
    def info(self, message):
        self._check_date_and_rotate()
        self.logger.info(message)

    def warning(self, message):
        self._check_date_and_rotate()
        self.logger.warning(message)

    def error(self, message):
        self._check_date_and_rotate()
        self.logger.error(message)

    def debug(self, message):
        self._check_date_and_rotate()
        self.logger.debug(message)


