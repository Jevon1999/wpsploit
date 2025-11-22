"""
Auto-Download & Cache Management
Fungsi: Manage cache untuk eksploit, auto-download, dan cleanup.
Isi: Class CacheManager dengan method download, cache, cleanup.
"""

import os
import time
from pathlib import Path
from utils import Logger

class CacheManager:
    def __init__(self, logger, cache_dir="cache", max_age_days=30):
        # Fungsi: Inisialisasi cache manager
        # Isi: Setup cache dir, max age
        self.logger = logger
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.max_age = max_age_days * 24 * 3600  # seconds
    
    def download_and_cache(self, url, filename):
        # Fungsi: Download file dan cache
        # Isi: Fetch dari URL, simpan ke cache
        import requests
        filepath = self.cache_dir / filename
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            with open(filepath, 'wb') as f:
                f.write(response.content)
            self.logger.info(f"Cached {filename}")
            return filepath
        except Exception as e:
            self.logger.error(f"Failed to download {filename}: {e}")
            return None
    
    def get_cached_file(self, filename):
        # Fungsi: Get file dari cache jika valid
        # Isi: Cek exist dan age
        filepath = self.cache_dir / filename
        if filepath.exists() and self.is_cache_valid(filepath):
            return filepath
        return None
    
    def is_cache_valid(self, filepath):
        # Fungsi: Cek apakah cache masih valid
        # Isi: Bandingkan mtime dengan max_age
        mtime = os.path.getmtime(filepath)
        return time.time() - mtime < self.max_age
    
    def cleanup_cache(self):
        # Fungsi: Cleanup cache lama
        # Isi: Hapus file yang expired
        for file in self.cache_dir.iterdir():
            if file.is_file() and not self.is_cache_valid(file):
                file.unlink()
                self.logger.info(f"Cleaned up {file.name}")
    
    def cache_exploit_code(self, exploit_id, code):
        # Fungsi: Cache kode eksploit
        # Isi: Simpan ke file
        filepath = self.cache_dir / f"exploit_{exploit_id}.txt"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(code)
        return filepath