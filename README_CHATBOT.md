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

sudo apt update
sudo apt install -y \
  libxcb-xinerama0 \
  libxcb-cursor0 \
  libxkbcommon-x11-0 \
  libxcb-icccm4 \
  libxcb-image0 \
  libxcb-keysyms1 \
  libxcb-render-util0 \
  libxcb-xinput0 \
  libxcb-shape0 \
  libxcb-randr0 \
  libxcb-util1 \
  libgl1 \
  libglib2.0-0

## Clone the Repository

git clone <https://github.com/HARIOM-BEEP/eSim>
cd eSim-master

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
pip uninstall -y pip
python -m ensurepip
python -m pip install pip==22.3.1
python -m pip install setuptools==65.5.0 wheel==0.38.4

python -m pip install hdlparse==1.0.4 --no-build-isolation

pip install -r requirements.txt

pip install paddlepaddle==2.5.2 \
  -f https://www.paddlepaddle.org.cn/whl/linux/mkl/avx/stable.html

pip uninstall -y opencv-python opencv-contrib-python opencv-python-headless
pip install opencv-python-headless==4.6.0.66

## Before running eSim

unset QT_PLUGIN_PATH
export QT_QPA_PLATFORM=xcb

## Ingest manuals for RAG 
```bash
cd src
python ingest.py

## Running the Application
```bash
cd src/frontEnd
python Application.py

## Common Warnings (Safe to Ignore)

PaddleOCR init failed: show_log
QSocketNotifier: Can only be used with threads started with QThread
libpng iCCP: incorrect sRGB profile
PyQt sipPyTypeDict() deprecation warnings
