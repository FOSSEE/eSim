# eSim Copilot Deployment – Complete Guide

**Date:** March 3, 2025  
**Branch:** `Chatbot_Enhancements` (from `pr-434`)  
**Goal:** First deployment of eSim AI Copilot on Ubuntu VM

This document explains every step, every file, every command, and every fix from this deployment session.

---

# Table of Contents

1. [Project Overview](#1-project-overview)
2. [Branch Setup](#2-branch-setup)
3. [Branch Changes & Commit History](#3-branch-changes--commit-history)
4. [Technical Breakdown of Fixes](#4-technical-breakdown-of-fixes)
5. [Ubuntu VM Setup](#5-ubuntu-vm-setup)
6. [Networking & SSH](#6-networking--ssh)
7. [Code Transfer to VM](#7-code-transfer-to-vm)
8. [Setup Script – Full 7-Step Flow](#8-setup-script--full-7-step-flow)
9. [Ollama & Models](#9-ollama--models)
10. [Launch & Usage](#10-launch--usage)
11. [Known Issues & Troubleshooting](#11-known-issues--troubleshooting)
12. [Push to GitHub](#12-push-to-github)

---

# 1. Project Overview

## What is eSim?
**eSim** is an open-source electronics simulation tool (FOSSEE/eSim) that uses:
- **ngspice** – SPICE circuit simulator
- **KiCad** – Schematic capture
- **PyQt5** – Desktop GUI

## What is eSim Copilot?
Enhanced assistant integrated into eSim, providing:
- **Text chat:** Ollama (LLM)
- **RAG:** ChromaDB
- **Vision:** PaddleOCR, MiniCPM-V
- **Speech-to-text:** Vosk

---

# 2. Branch Setup

```bash
# Created from Hariom's Copilot implementation
git fetch origin pull/434/head:pr-434
git checkout -b Chatbot_Enhancements pr-434
```

---

# 3. Branch Changes & Commit History

### Key File Changes
- **`scripts/setup_copilot_ubuntu.sh`**: New comprehensive setup script.
- **`scripts/launch_esim.sh`**: New utility to launch with correct Qt backend.
- **`src/frontEnd/Workspace.py`**: Fixed directory creation bug.
- **`src/chatbot/stt_handler.py`**: Made STT optional with graceful fallback.
- **`.gitattributes`**: Added to force LF on shell scripts.

### Recent Commits
- `71ed0f5c`: SESSION_SUMMARY: comprehensive guide with every item explained
- `4c67304d`: Ubuntu deployment, hdlparse fix, Workspace.py fix, launch script
- `67f08043`: Ubuntu deployment support, optional STT, ChromaDB path fix

---

# 4. Technical Breakdown of Fixes

### 4.1 hdlparse & setuptools Fix
**Problem:** `hdlparse==1.0.4` uses `use_2to3`, which was removed in `setuptools 58+`.
**Fix:** 
1. Manually install `setuptools==57.5.0`.
2. Install `hdlparse` with `--no-build-isolation` to force it to use the downgrade.
3. Use a `/tmp/pip-constraints.txt` with `setuptools<58` for all subsequent installs.

### 4.2 Workspace.py Crash
**Problem:** `FileNotFoundError` when writing `~/.esim/workspace.txt` because the `.esim` folder was missing.
**Fix:** Added `os.makedirs(esim_dir, exist_ok=True)` in `src/frontEnd/Workspace.py`.

### 4.3 Mandatory LF for Scripts
**Problem:** `bash\r: No such file or directory` due to Windows CRLF.
**Fix:** Created `.gitattributes` to enforce `*.sh text eol=lf`.

### 4.4 Graceful STT Fallback
**Problem:** App crashed if `vosk` or `sounddevice` were missing.
**Fix:** Wrapped imports in `try/except` and added `_HAS_STT` flag in `stt_handler.py`.

---

# 5. Ubuntu VM Setup
- **ISO:** Ubuntu 22.04 LTS
- **Hardware:** 4-8 GB RAM, 25 GB Disk
- **Network:** Bridged Adapter (preferred) or NAT with Port Forwarding (2222 -> 22)

---

# 6. Networking & SSH
```bash
sudo apt install -y openssh-server
sudo systemctl enable --now ssh
ip addr # Find IP
```

---

# 7. Code Transfer to VM
- **Method A (SCP):** `scp -r repos/eSim user@ip:~/work/`
- **Method B (Zip):** Use `./scripts/zip_for_vm.ps1` on Windows, then transfer zip.

---

# 8. Setup Script – Full 7-Step Flow
Run `./scripts/setup_copilot_ubuntu.sh`:
1. **System Packages:** Install `ngspice`, `kicad`, `portaudio`, `libxcb` (Qt dependencies).
2. **Virtualenv:** Create isolated `.venv`.
3. **Python Deps:** Pip upgrade, `setuptools` downgrade, and RAG/AI requirements.
4. **PaddlePaddle:** Install CPU version for OCR.
5. **Ollama:** Download and install LLM server.
6. **Models:** Pull `qwen2.5:3b`, `minicpm-v`, and `nomic-embed-text`.
7. **Vosk:** Download offline English model to `~/.local/share/esim-copilot/`.

---

# 9. Ollama & Models
- **API:** `http://127.0.0.1:11434`
- **Service:** Managed via `systemctl` or manual `ollama serve`.

---

# 10. Launch & Usage
```bash
./scripts/launch_esim.sh
```
*Note: Uses `QT_QPA_PLATFORM=xcb` for compatibility over SSH X11 forwarding.*

---

# 11. Known Issues & Troubleshooting
| Issue | Fix |
|---|---|
| `bash\r` | `sed -i 's/\r$//' scripts/setup_copilot_ubuntu.sh` |
| `hdlparse` error | Ensure `setuptools<58` is used. |
| No GUI | Enable X11 forwarding in MobaXterm. |

---

# 12. Push to GitHub
1. Fork `FOSSEE/eSim` on GitHub.
2. `git remote add myfork https://github.com/YOUR_USER/eSim.git`
3. `git push myfork Chatbot_Enhancements`
