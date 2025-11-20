#!/usr/bin/env python3
"""
WP AutoExploit Tool - Main Entry Point
Fungsi: Entry point utama aplikasi. Menangani argumen command line dan mode interaktif.
Isi: Parsing argumen, inisialisasi logger, scanner, exploiter. Jika mode interaktif, panggil UI menu.
"""

import argparse
import sys
from scanner import Scanner
from exploiter import Exploiter
from utils import Logger
from ui import InteractiveUI  # Untuk mode interaktif

def main():
    # Fungsi: Parse argumen command line
    # Isi: Setup argparse untuk opsi seperti URL, nuclei path, dll.
    parser = argparse.ArgumentParser(description="WP AutoExploit Tool")
    parser.add_argument("url", nargs='?', help="URL target WordPress (opsional untuk mode interaktif)")
    parser.add_argument("--nuclei-path", default="nuclei", help="Path ke binary nuclei")
    parser.add_argument("--templates-dir", default="nuclei-wordfence-cve/nuclei-templates", help="Direktori templates")
    parser.add_argument("--output", default="results.json", help="File output hasil")
    parser.add_argument("--exploit", action="store_true", help="Jalankan eksploitasi otomatis")
    parser.add_argument("--interactive", action="store_true", help="Mode interaktif dengan menu")
    
    args = parser.parse_args()
    
    # Fungsi: Inisialisasi komponen
    # Isi: Buat instance Logger, Scanner, Exploiter
    logger = Logger()
    
    if args.interactive:
        # Fungsi: Jalankan mode interaktif
        # Isi: Panggil UI untuk menu interaktif
        ui = InteractiveUI(logger, args.nuclei_path, args.templates_dir, args.output)
        ui.run()
    else:
        # Fungsi: Mode command line
        # Isi: Jalankan scan dan exploit langsung
        if not args.url:
            logger.error("URL diperlukan untuk mode non-interaktif")
            sys.exit(1)
        
        logger.info(f"Memulai scan untuk {args.url}")
        
        scanner = Scanner(args.nuclei_path, args.templates_dir, logger)
        vulnerabilities = scanner.scan(args.url)
        
        if not vulnerabilities:
            logger.info("Tidak ada kerentanan ditemukan.")
            return
        
        logger.info(f"Ditemukan {len(vulnerabilities)} kerentanan.")
        
        if args.exploit:
            exploiter = Exploiter(logger)
            results = exploiter.exploit(vulnerabilities, args.url)
            import json
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=4)
            logger.info(f"Hasil disimpan ke {args.output}")
        else:
            for vuln in vulnerabilities:
                print(f"Vuln: {vuln['id']} - {vuln['info']['name']}")

if __name__ == "__main__":
    main()