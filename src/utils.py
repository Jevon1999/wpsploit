"""
Utils Module
Fungsi: Utility functions dan classes, seperti Logger untuk logging dengan color.
Isi: Class Logger dengan method info, error, warning menggunakan colorama. Tambah utility lain jika perlu.
"""

import logging
import colorama
from colorama import Fore, Style

colorama.init()

class Logger:
    def __init__(self, level=logging.INFO):
        # Fungsi: Inisialisasi logger
        # Isi: Setup logging handler dengan formatter
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
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