"""
Utils Module
Fungsi: Utility functions dan classes, seperti Logger untuk logging dengan color.
Isi: Class Logger dengan method info, error, warning menggunakan colorama. Tambah utility lain jika perlu.
"""

import logging
import colorama
from colorama import Fore, Style
from pathlib import Path
from datetime import datetime

colorama.init()

class Logger:
    def __init__(self, level=logging.INFO, log_file=None):
        # Fungsi: Inisialisasi logger
        # Isi: Setup logging handler dengan formatter untuk console dan file
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level)
        
        # Clear existing handlers
        self.logger.handlers = []
        
        # Console handler dengan color
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # File handler jika specified
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(level)
            file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
    
    def info(self, msg):
        # Fungsi: Log info dengan warna hijau
        # Isi: Print pesan dengan Fore.GREEN
        self.logger.info(Fore.GREEN + msg + Style.RESET_ALL)
    
    def error(self, msg):
        # Fungsi: Log error dengan warna merah
        # Isi: Print pesan dengan Fore.RED
        self.logger.error(Fore.RED + msg + Style.RESET_ALL)
    
    def warning(self, msg):
        # Fungsi: Log warning dengan warna kuning
        # Isi: Print pesan dengan Fore.YELLOW
        self.logger.warning(Fore.YELLOW + msg + Style.RESET_ALL)
    
    def success(self, msg):
        # Fungsi: Log success dengan warna hijau terang
        # Isi: Print pesan dengan Fore.LIGHTGREEN_EX
        self.logger.info(Fore.LIGHTGREEN_EX + "✓ " + msg + Style.RESET_ALL)
    
    def debug(self, msg):
        # Fungsi: Log debug dengan warna cyan
        # Isi: Print pesan dengan Fore.CYAN
        self.logger.debug(Fore.CYAN + msg + Style.RESET_ALL)