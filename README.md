# My Scripts Repository

Welcome to my **My Scripts Repository**!  This repository contains a collection of my scripts, ranging from cybersecurity tools to file monitoring utilities.

##  Overview
This repository serves as a hub for my personal scripts, tools, and utilities. These scripts are designed for automation, security research, and system monitoring. Below is a breakdown of the projects available in this repository.

## 📂 Projects

### 1️⃣ **File System Monitor** (`monitor_directory.py`)
A script that monitors changes (creation, modification, deletion) in a specified directory using the `watchdog` Python module.

- 📌 **Logs file system events** in `monitor.log`
- 🔍 Detects file modifications, creations, and deletions
- 🏷️ Uses Python's `watchdog` library

📜 **Usage:**
```bash
python monitor_directory.py
```

---

### 2️⃣ **AbuseIPDB Checker** (`abuseipdbTool.py`)
A script that checks if an IP address has been reported for abuse in the last 90 days using the **AbuseIPDB API**.

- 🔍 **Scans clipboard for IPs** and checks for abuse reports
- 🛡️ Uses API authentication for secure queries
- 📜 Logs results in the console

📜 **Usage:**
```bash
python abuseipdbTool.py
```

---

### 3️⃣ **VirusTotal File Scanner** (`ScanFile.py`)
A script that scans files using the **VirusTotal API v3**.

- 🛡️ **Checks if files have been scanned before** using SHA-256 hashes
- 🚀 **Uploads new files for scanning** if no previous results are found
- 🔍 **Displays scan results** with links to VirusTotal reports

📜 **Usage:**
```bash
python ScanFile.py
```

---

### 4️⃣ **VirusTotal Clipboard IP Scanner** (`VTClipboardIP.py`)
A script that monitors the clipboard for IP addresses and checks them against **VirusTotal’s database**.

- 🔍 **Automatically scans copied IP addresses**
- 📜 Displays results in a structured format
- 🛡️ Uses VirusTotal API for threat analysis

📜 **Usage:**
```bash
python VTClipboardIP.py
```

## 🔧 Requirements
Ensure you have Python installed (Python 3 recommended). Install dependencies using:
```bash
pip install -r requirements.txt
```



