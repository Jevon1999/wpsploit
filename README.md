# WP AutoExploit Tool

Alat untuk otomatis scan dan eksploit kerentanan WordPress menggunakan Nuclei templates dari Wordfence CVE.

## Instalasi

1. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Download Nuclei binary dari https://github.com/projectdiscovery/nuclei/releases

3. Pastikan nuclei ada di PATH atau tentukan path dengan --nuclei-path

## Penggunaan

### Mode Command Line
```
python src/main.py http://target-wordpress.com --exploit
```

Opsi:
- `url`: URL target WordPress
- `--nuclei-path`: Path ke nuclei binary (default: nuclei)
- `--templates-dir`: Direktori templates (default: nuclei-wordfence-cve/nuclei-templates)
- `--output`: File output hasil (default: results.json)
- `--exploit`: Jalankan eksploitasi otomatis

### Mode Interaktif
```
python src/main.py --interactive
```

Menu interaktif untuk:
- Set target URL
- Scan target
- Show vulnerabilities
- Exploit vulnerabilities
- Save results

## Alur Kerja

1. **Input**: URL target WordPress (via arg atau menu interaktif).
2. **Scanning**: Jalankan Nuclei untuk scan kerentanan menggunakan templates WordPress CVE.
3. **Detection**: Parse hasil scan untuk identifikasi kerentanan.
4. **Exploitation**: Jika diminta, jalankan modul eksploitasi untuk CVE yang didukung.
5. **Output**: Simpan hasil ke file JSON atau tampilkan di console/menu.

## Struktur Workspace

- `src/`: Kode sumber
  - `main.py`: Entry point, parsing argumen, mode interaktif/command line
  - `scanner.py`: Modul scanning dengan Nuclei
  - `exploiter.py`: Modul eksploitasi, mapping CVE ke fungsi
  - `ui.py`: Interface interaktif, menu CLI
  - `utils.py`: Utilities seperti Logger
- `nuclei-wordfence-cve/`: Templates Nuclei
- `requirements.txt`: Dependencies Python
- `README.md`: Dokumentasi ini

## Development Notes

Setiap file memiliki komentar tentang fungsi dan isi. Untuk tambah fitur:
- Tambah opsi menu di `ui.py`
- Implementasi eksploit baru di `exploiter.py`
- Update mapping di `get_exploit_function`

Referensi: https://github.com/InMyMine7/Beelzebub untuk inspirasi interface interaktif.

## Perhatian

- Gunakan hanya untuk testing yang sah.
- Eksploitasi dapat berbahaya dan ilegal jika tanpa izin.