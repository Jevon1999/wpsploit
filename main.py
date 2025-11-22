#!/usr/bin/env python3
"""
WP AutoExploit Tool - Main Entry Point
Fungsi: Entry point utama aplikasi. Menangani argumen command line dan mode interaktif.
Isi: Parsing argumen, inisialisasi logger, scanner, exploiter. Jika mode interaktif, panggil UI menu.
"""

import argparse
import sys
import logging
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from scanner import Scanner
from exploiter import Exploiter
from utils import Logger
from settings import Settings

def main():
    # Fungsi: Parse argumen command line
    # Isi: Setup argparse untuk opsi seperti URL, nuclei path, dll.
    parser = argparse.ArgumentParser(description="WP AutoExploit Tool - Automated WordPress Vulnerability Scanner & Exploit Framework")
    parser.add_argument("url", nargs='?', help="URL target WordPress (opsional, jika tidak ada akan masuk mode interaktif)")
    parser.add_argument("--nuclei-path", default="nuclei", help="Path ke binary nuclei")
    parser.add_argument("--templates-dir", default="nuclei-wordfence-cve/nuclei-templates", help="Direktori templates")
    parser.add_argument("--output", default="results.json", help="File output hasil")
    parser.add_argument("--exploit", action="store_true", help="Jalankan eksploitasi otomatis (untuk mode non-interaktif)")
    parser.add_argument("--config", default="config.json", help="Path ke file konfigurasi")
    parser.add_argument("--no-interactive", action="store_true", help="Disable mode interaktif (requires URL)")
    
    args = parser.parse_args()
    
    # Fungsi: Inisialisasi komponen dengan logging ke file
    # Isi: Buat instance Logger, Scanner, Exploiter
    settings = Settings(None, args.config)
    log_file = settings.get('logging.file', 'logs/wp_autoexploit.log')
    log_level = getattr(logging, settings.get('logging.level', 'INFO'))
    
    # Create logs directory
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    
    logger = Logger(level=log_level, log_file=log_file)
    settings.logger = logger
    
    logger.info("="*60)
    logger.info("WP AutoExploit Tool - Starting")
    logger.info("="*60)
    
    # Default ke interactive mode jika tidak ada URL atau tidak ada flag --no-interactive
    if not args.url and not args.no_interactive:
        # Fungsi: Jalankan mode interaktif (DEFAULT)
        # Isi: Panggil UI untuk menu interaktif
        from ui import InteractiveUI
        ui = InteractiveUI(logger, args.nuclei_path, args.templates_dir, args.output, settings)
        ui.run()
    elif args.url and args.no_interactive:
        # Fungsi: Mode command line (eksplisit)
        # Isi: Jalankan scan dan exploit langsung
        logger.info(f"Target: {args.url}")
        logger.info(f"Memulai scan dengan Nuclei...")
        
        scanner = Scanner(args.nuclei_path, args.templates_dir, logger)
        vulnerabilities = scanner.scan(args.url)
        
        if not vulnerabilities:
            logger.info("Tidak ada kerentanan ditemukan.")
            return
        
        logger.success(f"Ditemukan {len(vulnerabilities)} kerentanan!")
        
        if args.exploit:
            logger.info("Memulai eksploitasi otomatis...")
            exploiter = Exploiter(logger, settings)
            results = exploiter.exploit(vulnerabilities, args.url)
            
            # Save results
            import json
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=4, ensure_ascii=False)
            logger.success(f"Hasil disimpan ke {args.output}")
        else:
            logger.info("Vulnerabilities ditemukan:")
            for vuln in vulnerabilities:
                print(f"  - {vuln['template-id']}: {vuln['info']['name']}")
    elif args.url:
        # Jika ada URL tapi tidak ada --no-interactive, tetap masuk interactive dengan URL sudah diset
        from ui import InteractiveUI
        ui = InteractiveUI(logger, args.nuclei_path, args.templates_dir, args.output, settings)
        ui.current_url = args.url
        logger.info(f"Target diset ke: {args.url}")
        ui.run()
    else:
        logger.error("URL diperlukan untuk mode non-interaktif. Gunakan --no-interactive dengan URL atau jalankan tanpa argumen untuk mode interaktif.")
        sys.exit(1)
    
    logger.info("="*60)
    logger.info("WP AutoExploit Tool - Completed")
    logger.info("="*60)

if __name__ == "__main__":
    main()
