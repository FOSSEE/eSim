# eSim AI Chatbot - Generalized Installation and Setup Guide

## 1. Overview

Before you begin, ensure you have:

- **OS:** Windows 10/11 with WSL2, macOS, or Ubuntu Linux
- **RAM:** Minimum 8 GB
- **Disk Space:** At least 15 GB free
- **Internet:** Required for initial downloads

---

## 2. Install Required Dependencies (OS-Specific)

### Linux (Ubuntu/Debian)

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-venv python3-pip git curl \
portaudio19-dev python3-pyaudio \
libgl1 libglib2.0-0 \
libxcb-xinerama0 libxkbcommon-x11-0 libgl1-mesa-glx
```

### macOS

```bash
brew install python3 portaudio git
```

### Windows (WSL2)

Open **PowerShell as Administrator** and run:

```powershell
wsl --install
```

Then restart your system and follow the Linux steps above inside WSL.

---

## 3. Install Ollama

Download and install Ollama from:

https://ollama.com

Start Ollama:

```bash
ollama serve
```

---

## 4. Download AI Models

Run the following commands:

```bash
ollama pull qwen2.5-coder:3b
ollama pull qwen2.5-coder:1.5b
ollama pull nomic-embed-text
ollama pull minicpm-v
ollama pull tinyllama:1.1b
```

Verify installation:

```bash
ollama list
```

---

## 5. Clone the Repository

```bash
git clone https://github.com/username/Repository_name

cd Repository_name
```

---

## 6. Set Up Python Environment

### Linux/macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

### Windows

```powershell
python -m venv venv

venv\Scripts\activate
```

---

## 7. Install Python Packages

```bash
pip install --upgrade pip

pip install -r requirements.txt
```

---

## 8. Run the Chatbot

```bash
PYTHONPATH=src python3 -m frontEnd.Application
```

---

## 9. Daily Usage

```bash
cd esim-chatbot-pr34

source venv/bin/activate

ollama serve &

PYTHONPATH=src python3 -m frontEnd.Application
```

---
## 10. Voice output 

```bash
 sudo apt install -y espeak 
```

## 11. Troubleshooting

### GUI Won't Open

- Restart WSL
- Check display settings

### Missing Models

Run:

```bash
ollama pull <model-name>
```

### Microphone Issues

```bash
pip install pyaudio
```

### Qt Plugin Errors

- Verify Qt libraries are properly installed

---