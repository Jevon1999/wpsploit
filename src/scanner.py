"""
Scanner Module
Fungsi: Menangani scanning kerentanan menggunakan Nuclei.
Isi: Class Scanner dengan method scan() yang menjalankan nuclei binary, parse output JSON, return list vulnerabilities.
"""

import subprocess
import json
import os
from utils import Logger

class Scanner:
    def __init__(self, nuclei_path, templates_dir, logger):
        # Fungsi: Inisialisasi scanner
        # Isi: Simpan path nuclei, templates, logger
        self.nuclei_path = nuclei_path
        self.templates_dir = templates_dir
        self.logger = logger
    
    def scan(self, url):
        # Fungsi: Jalankan scan nuclei
        # Isi: Build command, run subprocess, parse JSON output, handle errors
        self.logger.info(f"Scanning {url} dengan Nuclei...")
        cmd = [
            self.nuclei_path,
            "-u", url,
            "-t", self.templates_dir,
            "-json",
            "-silent"
        ]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                vulnerabilities = []
                for line in lines:
                    if line:
                        try:
                            vuln = json.loads(line)
                            vulnerabilities.append(vuln)
                        except json.JSONDecodeError:
                            pass
                return vulnerabilities
            else:
                self.logger.error(f"Scan gagal: {result.stderr}")
                return []
        except subprocess.TimeoutExpired:
            self.logger.error("Scan timeout")
            return []
        except FileNotFoundError:
            self.logger.error("Nuclei binary tidak ditemukan")
            return []