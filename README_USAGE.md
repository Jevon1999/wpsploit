# WP AutoExploit Tool - Panduan Penggunaan

## 🎯 Fitur Utama

Tool ini mengintegrasikan **Nuclei Scanner** dengan **ExploitDB** untuk:
1. **Scan WordPress** menggunakan Nuclei templates
2. **Extract CVE** dari hasil scan
3. **Match CVE** dengan database ExploitDB
4. **Download exploit** secara otomatis dari GitLab ExploitDB
5. **Execute exploit** otomatis dengan parameter injection

## 📋 Prerequisites

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Install Nuclei
```bash
# Linux/WSL
wget -q https://github.com/projectdiscovery/nuclei/releases/latest/download/nuclei_linux_amd64.zip
unzip nuclei_linux_amd64.zip
chmod +x nuclei
sudo mv nuclei /usr/local/bin/

# Verifikasi
nuclei -version
```

### 3. Install Git (untuk clone ExploitDB)
```bash
sudo apt-get update
sudo apt-get install git
```

## 🚀 Cara Penggunaan

### Mode 1: Command Line (Quick Scan)
```bash
cd src
python main.py https://target-wordpress.com --exploit
```

### Mode 2: Interactive Mode
```bash
cd src
python main.py --interactive
```

Menu interaktif akan muncul:
```
=== WP AutoExploit Tool ===
1. Set Target URL
2. Scan Target
3. Show Vulnerabilities
4. Exploit Vulnerabilities
5. Save Results
0. Exit
```

### Mode 3: Scan Only (Tanpa Eksploitasi)
```bash
python main.py https://target-wordpress.com
```

### Options
```
--nuclei-path       : Path ke binary nuclei (default: nuclei)
--templates-dir     : Path ke nuclei templates (default: nuclei-wordfence-cve/nuclei-templates)
--output           : File output hasil (default: results.json)
--exploit          : Jalankan eksploitasi otomatis
--interactive      : Mode interaktif
--config           : Path ke config.json (default: config.json)
```

## ⚙️ Konfigurasi (config.json)

```json
{
    "exploitdb_gitlab": {
        "repo_url": "https://gitlab.com/exploit-database/exploitdb.git",
        "cache_dir": "cache/exploitdb",
        "auto_update": true,
        "update_interval_hours": 24
    },
    "exploit": {
        "timeout_seconds": 30,
        "max_retries": 3,
        "max_exploits_per_cve": 3
    }
}
```

## 📊 Output

### 1. Console Output
- Real-time logging dengan color coding:
  - 🟢 **GREEN**: Info/Success
  - 🔴 **RED**: Error
  - 🟡 **YELLOW**: Warning

### 2. Log File
- Lokasi: `logs/wp_autoexploit.log`
- Berisi detail lengkap semua operasi

### 3. Results JSON
- Lokasi: `results/exploit_results.json`
- Format:
```json
{
  "vuln_id": "CVE-2024-xxxx",
  "cve": "CVE-2024-xxxx",
  "url": "https://target.com",
  "status": "executed",
  "success": true,
  "output": "...",
  "exploit_id": "12345",
  "language": "python"
}
```

## 🔄 Workflow Internal

1. **Nuclei Scan** → Deteksi vulnerabilities di target
2. **CVE Extraction** → Parse CVE dari Nuclei output
3. **ExploitDB Sync** → Clone/update repo ExploitDB dari GitLab
4. **CVE Matching** → Cari exploits yang match dengan CVE
5. **Exploit Download** → Download kode exploit dari repo
6. **Parameter Injection** → Inject target URL ke dalam exploit code
7. **Execute** → Jalankan exploit dengan timeout/retry
8. **Result Tracking** → Capture output dan save ke file

## 🛡️ Keamanan & Best Practices

### ⚠️ PENTING:
- **HANYA gunakan di environment testing Anda sendiri**
- **JANGAN gunakan untuk target tanpa izin**
- Exploit akan **EXECUTED** secara otomatis
- Tool ini untuk **PENETRATION TESTING** dengan izin

### Recommendations:
1. Test di environment sandbox/VM terlebih dahulu
2. Review exploit code sebelum eksekusi (jika memungkinkan)
3. Monitor logs untuk memahami apa yang terjadi
4. Backup target sebelum testing

## 🐛 Troubleshooting

### Error: "Nuclei binary tidak ditemukan"
```bash
# Install ulang atau specify path
python main.py https://target.com --nuclei-path /path/to/nuclei
```

### Error: "Git operation failed"
```bash
# Clear cache dan retry
rm -rf cache/exploitdb/repo
python main.py https://target.com --exploit
```

### Error: "No WordPress exploits found"
- CVE mungkin belum ada exploit di ExploitDB
- Atau exploit tidak specific untuk WordPress
- Check manual di: https://www.exploit-db.com/

### Exploit execution timeout
- Adjust di `config.json`:
```json
"exploit": {
    "timeout_seconds": 60
}
```

## 📈 Status Codes

- `executed`: Exploit berhasil dijalankan
- `failed`: Exploit dijalankan tapi gagal
- `no_wordpress_exploit`: Tidak ada exploit WordPress untuk CVE
- `no_cve`: Tidak ada CVE ditemukan di vulnerability
- `download_failed`: Gagal download exploit code
- `all_exploits_failed`: Semua exploit dicoba tapi gagal

## 🔧 Development

### Structure
```
wpsploit/
├── src/
│   ├── main.py              # Entry point
│   ├── scanner.py           # Nuclei integration
│   ├── exploiter.py         # Exploit execution engine
│   ├── exploitdb_gitlab.py  # ExploitDB repo manager
│   ├── exploit_parser.py    # Exploit code parser
│   ├── cache_manager.py     # Cache handler
│   ├── settings.py          # Config loader
│   └── utils.py             # Logger & utilities
├── nuclei-wordfence-cve/    # Nuclei templates
├── cache/                   # ExploitDB cache
├── logs/                    # Log files
├── results/                 # Output results
└── config.json              # Configuration
```

## 📝 Changelog

### Version 2.0 (Current)
- ✅ Full ExploitDB GitLab integration
- ✅ Automatic exploit execution (Python/Bash/PHP/Ruby)
- ✅ Parameter injection untuk exploits
- ✅ Detailed logging & result tracking
- ✅ Retry mechanism & error handling
- ✅ CVE mapping & WordPress filtering
- ✅ Progress saving & summary report

## 📞 Support

Jika menemukan bug atau ingin menambah fitur:
1. Check logs di `logs/wp_autoexploit.log`
2. Review config di `config.json`
3. Test dengan verbose logging

## ⚖️ License & Disclaimer

Tool ini hanya untuk **EDUCATIONAL** dan **AUTHORIZED PENETRATION TESTING**.
Pengguna bertanggung jawab penuh atas penggunaan tool ini.
