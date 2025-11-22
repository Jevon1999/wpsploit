# 🎯 WP AutoExploit Tool

**Automated WordPress Vulnerability Scanner & Exploit Framework**

Tool lengkap untuk melakukan **automated penetration testing** pada WordPress dengan integrasi **Nuclei Scanner** dan **ExploitDB**.

---

## 🌟 Features

### ✅ **Fully Automated Workflow**
- 🔍 **Nuclei Scanning** - Scan WordPress menggunakan 10,000+ CVE templates
- 🎯 **CVE Extraction** - Extract CVE otomatis dari hasil scan
- 📊 **ExploitDB Integration** - Sync dengan GitLab ExploitDB repository
- 🔗 **Smart Matching** - Match CVE dengan WordPress-specific exploits
- 📥 **Auto Download** - Download exploit code secara otomatis
- 💉 **Parameter Injection** - Inject target URL ke exploit code
- ⚡ **Auto Execution** - Execute exploit dengan timeout & retry mechanism

### 🎨 **Advanced Features**
- 🔄 Multi-language support (Python, Bash, PHP, Ruby)
- 📝 Detailed logging (console + file)
- 💾 Result tracking & progress saving
- 🎛️ Interactive CLI mode
- ⚙️ Highly configurable
- 🛡️ Error handling & retry logic

---

## 📦 Installation

### 1️⃣ Automated Setup (Recommended)
```bash
chmod +x setup.sh
./setup.sh
```

### 2️⃣ Manual Setup
```bash
# Install Python dependencies
pip3 install -r requirements.txt

# Install Nuclei
wget https://github.com/projectdiscovery/nuclei/releases/latest/download/nuclei_linux_amd64.zip
unzip nuclei_linux_amd64.zip
sudo mv nuclei /usr/local/bin/
chmod +x /usr/local/bin/nuclei

# Create directories
mkdir -p cache/exploitdb logs results
```

---

## 🚀 Quick Start

### **Default: Interactive Mode** 🎮
Tools ini sekarang **DEFAULT INTERAKTIF**! Cukup jalankan:

```bash
python3 main.py
```

**Menu interaktif dengan ASCII banner akan langsung muncul!** ✨

### **Dengan Target URL**
```bash
python3 main.py https://target-wordpress.com
```
Masuk interactive mode dengan target sudah diset.

### **Command-Line Mode** (Advanced)
```bash
python3 main.py https://target-wordpress.com --no-interactive --exploit
```
Langsung scan & exploit tanpa menu.

---

## 💡 Usage Examples

### Example 1: Interactive Mode (DEFAULT) 🎮
```bash
python3 main.py
```
**Output:**
```
╔══════════════════════════════════════════════════════════════════════╗
║                        WP AUTOEXPLOIT                                ║
║      WordPress Automated Vulnerability Scanner & Exploit            ║
╚══════════════════════════════════════════════════════════════════════╝

╔════════════════════════════════════════════════════════════════════╗
║                         ⚡ MAIN MENU ⚡                             ║
╠════════════════════════════════════════════════════════════════════╣
║  [1] 🎯 Set Target URL         │ Define WordPress target          ║
║  [2] 🔍 Scan Target            │ Run Nuclei vulnerability         ║
║  [3] 📋 Show Vulnerabilities   │ List detected CVEs               ║
║  [4] ⚡ Exploit Vulnerabilities│ Auto-exploit with ExploitDB      ║
║  [5] 💾 Save Results           │ Export to JSON file              ║
║  [6] ⚙️  Settings               │ View configuration               ║
║  [7] ℹ️  About                  │ Information & help               ║
║  [0] 🚪 Exit                   │ Quit application                 ║
╚════════════════════════════════════════════════════════════════════╝

[?] Pilih opsi: 
```

### Example 2: Quick Workflow
```bash
# 1. Start tools
python3 main.py

# 2. Pilih [1] - Set target: https://wordpress-demo.com
# 3. Pilih [2] - Scan target (tunggu beberapa menit)
# 4. Pilih [3] - Lihat vulnerabilities ditemukan
# 5. Pilih [4] - Exploit (pilih A untuk semua, atau 1,2,3)
# 6. Pilih [5] - Save hasil ke JSON
```

### Example 3: Command-Line Mode
```bash
python3 main.py https://target.com --no-interactive --exploit
```
Langsung scan & exploit tanpa menu interaktif.

---

## 🔄 Workflow

```
Target URL → Nuclei Scan → Extract CVEs → Sync ExploitDB 
→ Match CVE → Download Code → Inject Params → Execute → Save Results
```

**Detailed workflow:**
1. **Input**: URL target WordPress
2. **Scanning**: Nuclei scan menggunakan Wordfence CVE templates
3. **Detection**: Parse hasil dan extract CVE
4. **Exploitation**: 
   - Search exploits di ExploitDB berdasarkan CVE
   - Filter WordPress-specific exploits
   - Download dan parse exploit code
   - Inject target URL ke dalam exploit
   - Execute dengan timeout dan retry
5. **Output**: Save detailed results ke JSON dan logs

---

## 📊 Output & Results

### **Console Output**
- 🟢 **GREEN** - Success/Info
- 🔴 **RED** - Errors
- 🟡 **YELLOW** - Warnings

### **Log File**
Location: `logs/wp_autoexploit.log`

### **Results JSON**
Location: `results/exploit_results.json`

---

## ⚙️ Configuration

Edit `config.json`:
```json
{
    "exploitdb_gitlab": {
        "auto_update": true,
        "update_interval_hours": 24
    },
    "exploit": {
        "timeout_seconds": 30,
        "max_retries": 3
    }
}
```

---

## 📁 Project Structure

```
wpsploit/
├── src/                          # Source code
│   ├── main.py                   # Entry point
│   ├── scanner.py                # Nuclei integration
│   ├── exploiter.py              # Exploit execution engine
│   ├── exploitdb_gitlab.py       # ExploitDB repo handler
│   ├── exploit_parser.py         # Exploit code parser
│   ├── cache_manager.py          # Cache management
│   ├── settings.py               # Config loader
│   └── utils.py                  # Logger & utilities
├── nuclei-wordfence-cve/         # Nuclei templates
├── config.json                   # Configuration
├── setup.sh                      # Automated setup
├── test_integration.py           # Integration tests
└── README_USAGE.md               # Detailed usage guide
```

---

## 🧪 Testing

```bash
# Run integration tests
python3 test_integration.py

# Demo exploit execution (safe)
python3 demo_exploit_execution.py
```

---

## 🛡️ Security & Legal

### ⚠️ **CRITICAL WARNINGS**
- **ONLY use on authorized targets**
- **This tool EXECUTES exploits automatically**
- **You are responsible for all consequences**

### ✅ **Legal Usage**
- ✅ Your own test environments
- ✅ Bug bounty programs (within scope)
- ✅ Authorized penetration tests

### ❌ **ILLEGAL Usage**
- ❌ Unauthorized websites
- ❌ Production systems without permission

---

## 🐛 Troubleshooting

See detailed troubleshooting in `README_USAGE.md`

Common issues:
- Nuclei not found → Install via setup.sh
- Git operation failed → Clear cache: `rm -rf cache/exploitdb/repo`
- No exploits found → CVE may not have ExploitDB entry yet

---

## 📝 Changelog

### **v2.0** (Current)
- ✅ Full ExploitDB GitLab integration
- ✅ Automatic exploit execution (Python/Bash/PHP/Ruby)
- ✅ Parameter injection system
- ✅ Advanced error handling & retry logic
- ✅ Detailed logging & progress tracking
- ✅ Interactive CLI mode

---

## 🎓 Credits

- **Nuclei** - ProjectDiscovery
- **ExploitDB** - Offensive Security
- **Wordfence CVE Templates** - Wordfence Team

---

**Made with ❤️ for Security Researchers**

⚠️ **Remember: With great power comes great responsibility!**