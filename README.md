
<p align="center">

![Python](https://img.shields.io/badge/python-3.10+-blue)
![Security Tool](https://img.shields.io/badge/tool-web%20scanner-red)
![License](https://img.shields.io/badge/license-MIT-green)
![Maintained](https://img.shields.io/badge/maintained-yes-brightgreen)

</p>

# 🌀 WVVortex

Automated Web Vulnerability Scanner  
Created by **cybe07**

# 🌀 WVVortex
### Automated Web Vulnerability Scanner

WVVortex is a lightweight yet powerful **automated web vulnerability scanner** designed for security researchers, penetration testers, and bug bounty hunters.

It performs automated **reconnaissance, vulnerability detection, and reporting** against web applications.

The tool focuses on:

- fast scanning
- modular architecture
- automation of common security checks

---

# 🚀 Features

### Web Reconnaissance

- Web crawler for discovering internal URLs
- Technology detection
- Parameter discovery
- Hidden parameter fuzzing

### Vulnerability Detection

- Cross-Site Scripting (XSS)
- SQL Injection detection
- Missing security header detection

### Attack Surface Discovery

- Directory brute forcing
- Hidden parameter discovery
- Endpoint enumeration

### Reporting

WVVortex automatically generates:

- PDF security report
- JSON report for automation

### Performance

- Multithreaded directory scanning
- Optimized scanning workflow
- Modular architecture for easy extension

---

# 🧠 Scan Capabilities

| Feature | Supported |
|--------|-----------|
| Web Crawling | ✔ |
| Technology Detection | ✔ |
| Parameter Discovery | ✔ |
| Parameter Fuzzing | ✔ |
| Directory Bruteforce | ✔ |
| XSS Detection | ✔ |
| SQL Injection Detection | ✔ |
| Security Header Analysis | ✔ |
| PDF Report | ✔ |
| JSON Report | ✔ |

---

# ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/cybe07/WVVortex.git
cd WVVortex
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install the CLI tool:

```bash
pip install -e .
```

Now the tool can be executed globally.

---

# 🖥 Usage

Basic scan:

```bash
wvvortex -u http://target.com --full
```

Example:

```bash
wvvortex -u http://testphp.vulnweb.com --full --threads 30
```

---

# 🔧 CLI Options

| Flag | Description |
|-----|-------------|
| `-u` | Target URL |
| `--crawl` | Run crawler only |
| `--dir` | Run directory brute force |
| `--scan` | Run vulnerability scan |
| `--full` | Run full scan |
| `--threads` | Thread count for directory scanning |
| `--stealth` | Enable stealth mode |
| `-w` | Custom wordlist |

---

# 📊 Example Scan Result

```
Pages Crawled: 25
Missing Headers: 4
XSS Vulnerabilities: 1
SQL Injection Vulnerabilities: 1

Security Score: 35/100
Risk Level: HIGH
```

---

# 📄 Generated Reports

After a scan the following files are created:

```
output/report.pdf
output/report.json
```

These reports include:

- vulnerabilities discovered
- affected URLs
- detected technologies
- security score
- risk level

---

# 🏗 Architecture

The scanner uses a modular architecture.

```
scanner.py          → CLI engine
crawler.py          → URL discovery
param_discovery.py  → parameter discovery
param_fuzzer.py     → parameter fuzzing
dir_bruteforce.py   → directory enumeration
tech_detector.py    → technology detection
report_generator.py → PDF report generator
json_report.py      → JSON report generator
```

This allows developers to easily add new vulnerability modules.

---

# 🔮 Future Improvements

Planned improvements include:

- Blind SQL Injection detection
- LFI / RFI detection
- CSRF detection
- Authentication testing
- WAF detection
- Async scanning engine

---

# ⚠️ Disclaimer

This tool is intended **only for educational purposes and authorized security testing**.

Do **NOT scan systems without permission**.

The author is not responsible for misuse of this tool.

---

# 👨‍💻 Author

Cybe07

Cybersecurity Enthusiast  
Pentesting | Web Security | Red Teaming

---

# ⭐ Support

If you like this project:

⭐ Star the repository  
🍴 Fork the project  
🛠 Contribute improvements
