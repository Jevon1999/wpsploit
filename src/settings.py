"""
Configuration & Settings
Fungsi: Load dan manage konfigurasi dari config.json.
Isi: Class Settings dengan method load_config, get_setting.
"""

import json
from pathlib import Path
from utils import Logger

class Settings:
    def __init__(self, logger, config_file="config.json"):
        # Fungsi: Inisialisasi settings
        # Isi: Load config dari file
        self.logger = logger
        self.config_file = Path(config_file)
        self.config = self.load_config()
    
    def load_config(self):
        # Fungsi: Load config JSON
        # Isi: Baca file, return dict
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        else:
            self.logger.warning("Config file not found, using defaults")
            return {}
    
    def get(self, key, default=None):
        # Fungsi: Get setting value
        # Isi: Navigate nested dict
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value
    
    def set(self, key, value):
        # Fungsi: Set setting value
        # Isi: Update config dict
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            config = config.setdefault(k, {})
        config[keys[-1]] = value
        self.save_config()
    
    def save_config(self):
        # Fungsi: Save config ke file
        # Isi: Write JSON
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)