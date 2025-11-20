"""
UI Module - Interactive Interface
Fungsi: Menyediakan interface interaktif berbasis CLI untuk tools WP AutoExploit.
Isi: Menu utama, submenu untuk scan, exploit, dll. Menggunakan input() untuk interaksi user.
"""

from scanner import Scanner
from exploiter import Exploiter
from utils import Logger
import json

class InteractiveUI:
    def __init__(self, logger, nuclei_path, templates_dir, output_file):
        # Fungsi: Inisialisasi UI
        # Isi: Simpan parameter, inisialisasi komponen
        self.logger = logger
        self.nuclei_path = nuclei_path
        self.templates_dir = templates_dir
        self.output_file = output_file
        self.scanner = Scanner(nuclei_path, templates_dir, logger)
        self.exploiter = Exploiter(logger)
        self.current_url = None
        self.vulnerabilities = []
    
    def run(self):
        # Fungsi: Loop utama menu
        # Isi: Tampilkan menu, handle pilihan user
        while True:
            self.show_main_menu()
            choice = input("Pilih opsi: ").strip()
            if choice == "1":
                self.set_target()
            elif choice == "2":
                self.scan_target()
            elif choice == "3":
                self.show_vulnerabilities()
            elif choice == "4":
                self.exploit_vulnerabilities()
            elif choice == "5":
                self.save_results()
            elif choice == "0":
                break
            else:
                print("Pilihan tidak valid.")
    
    def show_main_menu(self):
        # Fungsi: Tampilkan menu utama
        # Isi: Print menu options
        print("\n=== WP AutoExploit Tool ===")
        print("1. Set Target URL")
        print("2. Scan Target")
        print("3. Show Vulnerabilities")
        print("4. Exploit Vulnerabilities")
        print("5. Save Results")
        print("0. Exit")
    
    def set_target(self):
        # Fungsi: Set URL target
        # Isi: Input URL dari user, validasi
        url = input("Masukkan URL target WordPress: ").strip()
        if url:
            self.current_url = url
            self.logger.info(f"Target diset ke {url}")
        else:
            print("URL tidak valid.")
    
    def scan_target(self):
        # Fungsi: Jalankan scan
        # Isi: Panggil scanner.scan, simpan hasil
        if not self.current_url:
            print("Set target dulu.")
            return
        self.logger.info(f"Scanning {self.current_url}...")
        self.vulnerabilities = self.scanner.scan(self.current_url)
        if self.vulnerabilities:
            self.logger.info(f"Ditemukan {len(self.vulnerabilities)} kerentanan.")
        else:
            self.logger.info("Tidak ada kerentanan.")
    
    def show_vulnerabilities(self):
        # Fungsi: Tampilkan daftar vuln
        # Isi: Loop dan print vulnerabilities
        if not self.vulnerabilities:
            print("Belum ada hasil scan.")
            return
        print("\nVulnerabilities:")
        for i, vuln in enumerate(self.vulnerabilities, 1):
            print(f"{i}. {vuln['template-id']} - {vuln['info']['name']}")
    
    def exploit_vulnerabilities(self):
        # Fungsi: Jalankan exploit
        # Isi: Pilih vuln, panggil exploiter
        if not self.vulnerabilities:
            print("Scan dulu.")
            return
        self.show_vulnerabilities()
        choice = input("Pilih nomor vuln untuk exploit (atau 'all'): ").strip()
        if choice == "all":
            results = self.exploiter.exploit(self.vulnerabilities, self.current_url)
        else:
            try:
                idx = int(choice) - 1
                vuln = self.vulnerabilities[idx]
                results = self.exploiter.exploit([vuln], self.current_url)
            except:
                print("Pilihan tidak valid.")
                return
        self.logger.info("Exploit selesai.")
        # Simpan results sementara
    
    def save_results(self):
        # Fungsi: Simpan hasil ke file
        # Isi: Dump JSON ke output_file
        if not self.vulnerabilities:
            print("Tidak ada hasil untuk disimpan.")
            return
        with open(self.output_file, 'w') as f:
            json.dump(self.vulnerabilities, f, indent=4)
        self.logger.info(f"Hasil disimpan ke {self.output_file}")