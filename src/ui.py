"""
UI Module - Interactive Interface
Fungsi: Menyediakan interface interaktif berbasis CLI untuk tools WP AutoExploit.
Isi: Menu utama, submenu untuk scan, exploit, dll. Menggunakan input() untuk interaksi user.
"""

from scanner import Scanner
from exploiter import Exploiter
from utils import Logger
import json
import os
from colorama import Fore, Style

class InteractiveUI:
    def __init__(self, logger, nuclei_path, templates_dir, output_file, settings):
        # Fungsi: Inisialisasi UI
        # Isi: Simpan parameter, inisialisasi komponen
        self.logger = logger
        self.nuclei_path = nuclei_path
        self.templates_dir = templates_dir
        self.output_file = output_file
        self.settings = settings
        self.scanner = Scanner(nuclei_path, templates_dir, logger)
        self.exploiter = Exploiter(logger, settings)
        self.current_url = None
        self.vulnerabilities = []
    
    def clear_screen(self):
        """Clear console screen"""
        os.system('clear' if os.name != 'nt' else 'cls')
    
    def print_banner(self):
        """Print ASCII art banner"""
        banner = f"""{Fore.CYAN}
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║  {Fore.RED}██╗    ██╗{Fore.YELLOW}██████╗ {Fore.GREEN} █████╗ ██╗   ██╗████████╗{Fore.CYAN}███████╗██╗  ██╗    ║
║  {Fore.RED}██║    ██║{Fore.YELLOW}██╔══██╗{Fore.GREEN}██╔══██╗██║   ██║╚══██╔══╝{Fore.CYAN}██╔════╝╚██╗██╔╝    ║
║  {Fore.RED}██║ █╗ ██║{Fore.YELLOW}██████╔╝{Fore.GREEN}███████║██║   ██║   ██║   {Fore.CYAN}█████╗   ╚███╔╝     ║
║  {Fore.RED}██║███╗██║{Fore.YELLOW}██╔═══╝ {Fore.GREEN}██╔══██║██║   ██║   ██║   {Fore.CYAN}██╔══╝   ██╔██╗     ║
║  {Fore.RED}╚███╔███╔╝{Fore.YELLOW}██║     {Fore.GREEN}██║  ██║╚██████╔╝   ██║   {Fore.CYAN}███████╗██╔╝ ██╗    ║
║  {Fore.RED} ╚══╝╚══╝ {Fore.YELLOW}╚═╝     {Fore.GREEN}╚═╝  ╚═╝ ╚═════╝    ╚═╝   {Fore.CYAN}╚══════╝╚═╝  ╚═╝    ║
║                                                                      ║
║         {Fore.LIGHTWHITE_EX}WordPress Automated Vulnerability Scanner & Exploit{Fore.CYAN}         ║
║                    {Fore.LIGHTBLACK_EX}Powered by Nuclei + ExploitDB{Fore.CYAN}                    ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""
        print(banner)
        if self.current_url:
            print(f"{Fore.GREEN}🎯 Current Target: {Fore.WHITE}{self.current_url}{Style.RESET_ALL}")
        if self.vulnerabilities:
            print(f"{Fore.YELLOW}⚠️  Vulnerabilities Found: {Fore.WHITE}{len(self.vulnerabilities)}{Style.RESET_ALL}")
        print()
    
    def run(self):
        # Fungsi: Loop utama menu
        # Isi: Tampilkan menu, handle pilihan user
        while True:
            self.clear_screen()
            self.print_banner()
            self.show_main_menu()
            
            try:
                choice = input(f"\n{Fore.CYAN}[?]{Style.RESET_ALL} Pilih opsi: ").strip()
                
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
                elif choice == "6":
                    self.show_settings()
                elif choice == "7":
                    self.show_about()
                elif choice == "0":
                    print(f"\n{Fore.GREEN}[✓]{Style.RESET_ALL} Terima kasih! Sampai jumpa! 👋")
                    break
                else:
                    print(f"\n{Fore.RED}[✗]{Style.RESET_ALL} Pilihan tidak valid. Tekan Enter untuk melanjutkan...")
                    input()
            except KeyboardInterrupt:
                print(f"\n\n{Fore.YELLOW}[!]{Style.RESET_ALL} Interrupted. Keluar...")
                break
            except Exception as e:
                print(f"\n{Fore.RED}[✗]{Style.RESET_ALL} Error: {e}")
                input(f"\n{Fore.CYAN}Tekan Enter untuk melanjutkan...{Style.RESET_ALL}")
    
    def show_main_menu(self):
        # Fungsi: Tampilkan menu utama
        # Isi: Print menu options
        print(f"{Fore.LIGHTWHITE_EX}╔════════════════════════════════════════════════════════════════════╗")
        print(f"║                         {Fore.CYAN}⚡ MAIN MENU ⚡{Fore.LIGHTWHITE_EX}                          ║")
        print(f"╠════════════════════════════════════════════════════════════════════╣")
        print(f"║  {Fore.YELLOW}[1]{Fore.WHITE} 🎯 Set Target URL         {Fore.LIGHTBLACK_EX}│{Fore.WHITE} Define WordPress target    {Fore.LIGHTWHITE_EX}║")
        print(f"║  {Fore.YELLOW}[2]{Fore.WHITE} 🔍 Scan Target            {Fore.LIGHTBLACK_EX}│{Fore.WHITE} Run Nuclei vulnerability   {Fore.LIGHTWHITE_EX}║")
        print(f"║  {Fore.YELLOW}[3]{Fore.WHITE} 📋 Show Vulnerabilities   {Fore.LIGHTBLACK_EX}│{Fore.WHITE} List detected CVEs         {Fore.LIGHTWHITE_EX}║")
        print(f"║  {Fore.YELLOW}[4]{Fore.WHITE} ⚡ Exploit Vulnerabilities{Fore.LIGHTBLACK_EX}│{Fore.WHITE} Auto-exploit with ExploitDB{Fore.LIGHTWHITE_EX}║")
        print(f"║  {Fore.YELLOW}[5]{Fore.WHITE} 💾 Save Results           {Fore.LIGHTBLACK_EX}│{Fore.WHITE} Export to JSON file        {Fore.LIGHTWHITE_EX}║")
        print(f"║  {Fore.YELLOW}[6]{Fore.WHITE} ⚙️  Settings               {Fore.LIGHTBLACK_EX}│{Fore.WHITE} View configuration         {Fore.LIGHTWHITE_EX}║")
        print(f"║  {Fore.YELLOW}[7]{Fore.WHITE} ℹ️  About                  {Fore.LIGHTBLACK_EX}│{Fore.WHITE} Information & help         {Fore.LIGHTWHITE_EX}║")
        print(f"║  {Fore.RED}[0]{Fore.WHITE} 🚪 Exit                   {Fore.LIGHTBLACK_EX}│{Fore.WHITE} Quit application           {Fore.LIGHTWHITE_EX}║")
        print(f"╚════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    
    def set_target(self):
        # Fungsi: Set URL target
        # Isi: Input URL dari user, validasi
        print(f"\n{Fore.CYAN}{'═'*70}")
        print(f"🎯 SET TARGET URL")
        print(f"{'═'*70}{Style.RESET_ALL}")
        
        url = input(f"\n{Fore.CYAN}[?]{Style.RESET_ALL} Masukkan URL target WordPress: ").strip()
        
        if url:
            # Basic validation
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            self.current_url = url
            print(f"\n{Fore.GREEN}[✓]{Style.RESET_ALL} Target berhasil diset ke: {Fore.WHITE}{url}{Style.RESET_ALL}")
            self.logger.info(f"Target diset ke {url}")
        else:
            print(f"\n{Fore.RED}[✗]{Style.RESET_ALL} URL tidak valid.")
        
        input(f"\n{Fore.CYAN}Tekan Enter untuk melanjutkan...{Style.RESET_ALL}")
    
    def scan_target(self):
        # Fungsi: Jalankan scan
        # Isi: Panggil scanner.scan, simpan hasil
        if not self.current_url:
            print(f"\n{Fore.RED}[✗]{Style.RESET_ALL} Target belum diset. Silakan set target dulu (opsi 1).")
            input(f"\n{Fore.CYAN}Tekan Enter untuk melanjutkan...{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}{'═'*70}")
        print(f"🔍 SCANNING TARGET")
        print(f"{'═'*70}{Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}[~]{Style.RESET_ALL} Target: {Fore.WHITE}{self.current_url}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[~]{Style.RESET_ALL} Templates: {Fore.WHITE}{self.templates_dir}{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}[*]{Style.RESET_ALL} Memulai scan dengan Nuclei...")
        print(f"{Fore.LIGHTBLACK_EX}    (Ini mungkin memakan waktu beberapa menit...){Style.RESET_ALL}\n")
        
        self.vulnerabilities = self.scanner.scan(self.current_url)
        
        if self.vulnerabilities:
            print(f"\n{Fore.GREEN}[✓]{Style.RESET_ALL} Scan selesai! Ditemukan {Fore.YELLOW}{len(self.vulnerabilities)}{Style.RESET_ALL} kerentanan.")
            self.logger.info(f"Ditemukan {len(self.vulnerabilities)} kerentanan.")
        else:
            print(f"\n{Fore.GREEN}[✓]{Style.RESET_ALL} Scan selesai. {Fore.LIGHTBLACK_EX}Tidak ada kerentanan ditemukan.{Style.RESET_ALL}")
            self.logger.info("Tidak ada kerentanan.")
        
        input(f"\n{Fore.CYAN}Tekan Enter untuk melanjutkan...{Style.RESET_ALL}")
    
    def show_vulnerabilities(self):
        # Fungsi: Tampilkan daftar vuln
        # Isi: Loop dan print vulnerabilities
        if not self.vulnerabilities:
            print(f"\n{Fore.RED}[✗]{Style.RESET_ALL} Belum ada hasil scan. Silakan scan terlebih dahulu (opsi 2).")
            input(f"\n{Fore.CYAN}Tekan Enter untuk melanjutkan...{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}{'═'*70}")
        print(f"📋 VULNERABILITIES DETECTED")
        print(f"{'═'*70}{Style.RESET_ALL}")
        print(f"\n{Fore.WHITE}Total: {Fore.YELLOW}{len(self.vulnerabilities)}{Fore.WHITE} vulnerabilities{Style.RESET_ALL}\n")
        
        for i, vuln in enumerate(self.vulnerabilities, 1):
            severity = vuln.get('info', {}).get('severity', 'unknown').upper()
            severity_color = {
                'CRITICAL': Fore.RED,
                'HIGH': Fore.LIGHTRED_EX,
                'MEDIUM': Fore.YELLOW,
                'LOW': Fore.LIGHTBLUE_EX,
                'INFO': Fore.LIGHTBLACK_EX
            }.get(severity, Fore.WHITE)
            
            print(f"{Fore.CYAN}[{i}]{Style.RESET_ALL} {severity_color}[{severity}]{Style.RESET_ALL} {Fore.WHITE}{vuln['template-id']}{Style.RESET_ALL}")
            print(f"    {Fore.LIGHTBLACK_EX}↳{Style.RESET_ALL} {vuln['info']['name']}")
            
            # Show tags if available
            tags = vuln.get('info', {}).get('tags', [])
            if tags:
                cve_tags = [t for t in tags if t.upper().startswith('CVE-')]
                if cve_tags:
                    print(f"    {Fore.LIGHTBLACK_EX}↳ CVE: {Fore.YELLOW}{', '.join(cve_tags)}{Style.RESET_ALL}")
            print()
        
        input(f"{Fore.CYAN}Tekan Enter untuk melanjutkan...{Style.RESET_ALL}")
    
    def exploit_vulnerabilities(self):
        # Fungsi: Jalankan exploit
        # Isi: Pilih vuln, panggil exploiter
        if not self.vulnerabilities:
            print(f"\n{Fore.RED}[✗]{Style.RESET_ALL} Belum ada hasil scan. Silakan scan terlebih dahulu (opsi 2).")
            input(f"\n{Fore.CYAN}Tekan Enter untuk melanjutkan...{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}{'═'*70}")
        print(f"⚡ EXPLOIT VULNERABILITIES")
        print(f"{'═'*70}{Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}[!] WARNING:{Style.RESET_ALL} Exploits akan dieksekusi secara otomatis!")
        print(f"{Fore.YELLOW}[!]{Style.RESET_ALL} Pastikan Anda memiliki izin untuk testing target ini.\n")
        
        # Show quick summary
        for i, vuln in enumerate(self.vulnerabilities, 1):
            print(f"{Fore.CYAN}[{i}]{Style.RESET_ALL} {vuln['template-id'][:50]}")
        
        print(f"\n{Fore.CYAN}[A]{Style.RESET_ALL} Exploit semua vulnerability")
        print(f"{Fore.CYAN}[#]{Style.RESET_ALL} Exploit nomor tertentu (misal: 1,2,3)")
        print(f"{Fore.RED}[C]{Style.RESET_ALL} Cancel")
        
        choice = input(f"\n{Fore.CYAN}[?]{Style.RESET_ALL} Pilihan: ").strip().upper()
        
        if choice == 'C':
            return
        elif choice == 'A' or choice == 'ALL':
            print(f"\n{Fore.YELLOW}[~]{Style.RESET_ALL} Memulai eksploitasi untuk {len(self.vulnerabilities)} vulnerabilities...")
            results = self.exploiter.exploit(self.vulnerabilities, self.current_url)
        else:
            try:
                indices = [int(x.strip()) - 1 for x in choice.split(',')]
                selected_vulns = [self.vulnerabilities[i] for i in indices if 0 <= i < len(self.vulnerabilities)]
                if selected_vulns:
                    print(f"\n{Fore.YELLOW}[~]{Style.RESET_ALL} Memulai eksploitasi untuk {len(selected_vulns)} vulnerabilities...")
                    results = self.exploiter.exploit(selected_vulns, self.current_url)
                else:
                    print(f"\n{Fore.RED}[✗]{Style.RESET_ALL} Tidak ada vulnerability yang valid dipilih.")
                    input(f"\n{Fore.CYAN}Tekan Enter untuk melanjutkan...{Style.RESET_ALL}")
                    return
            except:
                print(f"\n{Fore.RED}[✗]{Style.RESET_ALL} Pilihan tidak valid.")
                input(f"\n{Fore.CYAN}Tekan Enter untuk melanjutkan...{Style.RESET_ALL}")
                return
        
        print(f"\n{Fore.GREEN}[✓]{Style.RESET_ALL} Eksploitasi selesai!")
        input(f"\n{Fore.CYAN}Tekan Enter untuk melanjutkan...{Style.RESET_ALL}")
    
    def save_results(self):
        # Fungsi: Simpan hasil ke file
        # Isi: Dump JSON ke output_file
        if not self.vulnerabilities:
            print(f"\n{Fore.RED}[✗]{Style.RESET_ALL} Tidak ada hasil untuk disimpan.")
            input(f"\n{Fore.CYAN}Tekan Enter untuk melanjutkan...{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}{'═'*70}")
        print(f"💾 SAVE RESULTS")
        print(f"{'═'*70}{Style.RESET_ALL}")
        
        filename = input(f"\n{Fore.CYAN}[?]{Style.RESET_ALL} Nama file (default: {self.output_file}): ").strip()
        if not filename:
            filename = self.output_file
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.vulnerabilities, f, indent=4, ensure_ascii=False)
            print(f"\n{Fore.GREEN}[✓]{Style.RESET_ALL} Hasil berhasil disimpan ke: {Fore.WHITE}{filename}{Style.RESET_ALL}")
            self.logger.info(f"Hasil disimpan ke {filename}")
        except Exception as e:
            print(f"\n{Fore.RED}[✗]{Style.RESET_ALL} Gagal menyimpan file: {e}")
        
        input(f"\n{Fore.CYAN}Tekan Enter untuk melanjutkan...{Style.RESET_ALL}")
    
    def show_settings(self):
        """Show current settings"""
        print(f"\n{Fore.CYAN}{'═'*70}")
        print(f"⚙️  SETTINGS")
        print(f"{'═'*70}{Style.RESET_ALL}\n")
        
        print(f"{Fore.WHITE}Nuclei:{Style.RESET_ALL}")
        print(f"  Path: {Fore.YELLOW}{self.nuclei_path}{Style.RESET_ALL}")
        print(f"  Templates: {Fore.YELLOW}{self.templates_dir}{Style.RESET_ALL}")
        
        print(f"\n{Fore.WHITE}ExploitDB:{Style.RESET_ALL}")
        print(f"  Auto Update: {Fore.YELLOW}{self.settings.get('exploitdb_gitlab.auto_update', 'N/A')}{Style.RESET_ALL}")
        print(f"  Cache Dir: {Fore.YELLOW}{self.settings.get('exploitdb_gitlab.cache_dir', 'N/A')}{Style.RESET_ALL}")
        
        print(f"\n{Fore.WHITE}Exploit:{Style.RESET_ALL}")
        print(f"  Timeout: {Fore.YELLOW}{self.settings.get('exploit.timeout_seconds', 'N/A')}s{Style.RESET_ALL}")
        print(f"  Max Retries: {Fore.YELLOW}{self.settings.get('exploit.max_retries', 'N/A')}{Style.RESET_ALL}")
        print(f"  Max Exploits per CVE: {Fore.YELLOW}{self.settings.get('exploit.max_exploits_per_cve', 'N/A')}{Style.RESET_ALL}")
        
        print(f"\n{Fore.WHITE}Output:{Style.RESET_ALL}")
        print(f"  Default File: {Fore.YELLOW}{self.output_file}{Style.RESET_ALL}")
        print(f"  Results Dir: {Fore.YELLOW}{self.settings.get('output.results_dir', 'N/A')}{Style.RESET_ALL}")
        
        input(f"\n{Fore.CYAN}Tekan Enter untuk melanjutkan...{Style.RESET_ALL}")
    
    def show_about(self):
        """Show about information"""
        print(f"\n{Fore.CYAN}{'═'*70}")
        print(f"ℹ️  ABOUT WP AUTOEXPLOIT")
        print(f"{'═'*70}{Style.RESET_ALL}\n")
        
        print(f"{Fore.WHITE}Version:{Style.RESET_ALL} {Fore.YELLOW}2.0{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Description:{Style.RESET_ALL} Automated WordPress Vulnerability Scanner & Exploit Framework")
        
        print(f"\n{Fore.WHITE}Features:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}✓{Style.RESET_ALL} Nuclei Scanner Integration (10,000+ CVE templates)")
        print(f"  {Fore.GREEN}✓{Style.RESET_ALL} ExploitDB GitLab Integration")
        print(f"  {Fore.GREEN}✓{Style.RESET_ALL} Automatic CVE Extraction")
        print(f"  {Fore.GREEN}✓{Style.RESET_ALL} Smart Exploit Matching")
        print(f"  {Fore.GREEN}✓{Style.RESET_ALL} Multi-language Exploit Execution (Python/Bash/PHP/Ruby)")
        print(f"  {Fore.GREEN}✓{Style.RESET_ALL} Parameter Injection")
        print(f"  {Fore.GREEN}✓{Style.RESET_ALL} Detailed Logging & Result Tracking")
        
        print(f"\n{Fore.WHITE}Workflow:{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}1.{Style.RESET_ALL} Scan dengan Nuclei")
        print(f"  {Fore.CYAN}2.{Style.RESET_ALL} Extract CVE dari hasil scan")
        print(f"  {Fore.CYAN}3.{Style.RESET_ALL} Match CVE dengan ExploitDB")
        print(f"  {Fore.CYAN}4.{Style.RESET_ALL} Download exploit code")
        print(f"  {Fore.CYAN}5.{Style.RESET_ALL} Inject target parameters")
        print(f"  {Fore.CYAN}6.{Style.RESET_ALL} Execute exploit")
        print(f"  {Fore.CYAN}7.{Style.RESET_ALL} Track & save results")
        
        print(f"\n{Fore.RED}⚠️  WARNING:{Style.RESET_ALL}")
        print(f"  {Fore.YELLOW}•{Style.RESET_ALL} Only use on authorized targets")
        print(f"  {Fore.YELLOW}•{Style.RESET_ALL} This tool executes exploits automatically")
        print(f"  {Fore.YELLOW}•{Style.RESET_ALL} You are responsible for all actions")
        
        print(f"\n{Fore.WHITE}Credits:{Style.RESET_ALL}")
        print(f"  Nuclei - ProjectDiscovery")
        print(f"  ExploitDB - Offensive Security")
        print(f"  Wordfence CVE Templates")
        
        input(f"\n{Fore.CYAN}Tekan Enter untuk melanjutkan...{Style.RESET_ALL}")