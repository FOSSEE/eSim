# eSim Copilot – AI-Assisted Electronics Simulation Tool

eSim Copilot is an AI-powered assistant integrated into **eSim**, designed to help users analyze electronic circuits, debug SPICE netlists, understand simulation errors, and interact using text, voice, and images.

This project combines **PyQt5**, **ngspice**, **Ollama (LLMs)**, **RAG (ChromaDB)**, **OCR**, and **offline speech-to-text** into a single desktop application.

---

## Key Features

-  AI assistant for electronics & eSim
-  Netlist analysis and error explanation
-  ngspice simulation integration
-  Circuit image analysis (OCR + vision models)
-  Offline speech-to-text (no internet required)
-  Knowledge base using RAG (manuals + docs)
-  Fully offline-capable (except model downloads)

## Supported Platform

- **Linux only** (Recommended: Ubuntu 22.04 / 23.04 / 24.04)
- Tested on **Ubuntu 22.04 & 24.04**

---

## Python Version (VERY IMPORTANT)

## Supported
- **Python 3.9 – 3.10 (RECOMMENDED)**

Check version:
```bash
python --version

## System Dependencies (Install First)
```bash

sudo apt update
sudo apt upgrade

sudo apt install ngspice
sudo apt install portaudio19-dev
sudo apt install libgl1 libglib2.0-0

## Ollama (LLM Backend)
```bash

curl -fsSL https://ollama.com/install.sh | sh
ollama serve
ollama pull qwen2.5:3b
ollama pull minicpm-v
ollama pull nomic-embed-text

## Offline Speech-to-Text (VOSK)
```bash

mkdir -p ~/vosk-models
cd ~/vosk-models
wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip

export VOSK_MODEL_PATH=~/vosk-models/vosk-model-small-en-us-0.15

echo 'export VOSK_MODEL_PATH=~/vosk-models/vosk-model-small-en-us-0.15' >> ~/.bashrc
source ~/.bashrc

## Python Virtual Environment (Recommended)
```bash

python3.10 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel

pip install -r requirements.txt

pip install hdlparse==1.0.4

## Ingest manuals for RAG 
```bash
cd src
python Ingest.py

## Running the Application
```bash
cd src/frontEnd
python Application.py

## Common Warnings (Safe to Ignore)

PaddleOCR init failed: show_log
QSocketNotifier: Can only be used with threads started with QThread
libpng iCCP: incorrect sRGB profile
PyQt sipPyTypeDict() deprecation warnings
