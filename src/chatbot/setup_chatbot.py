"""
One-time setup for eSim Copilot (Chatbot).
Safe to run multiple times.
"""

import os
import sys
import subprocess
import shutil
import urllib.request
import zipfile

BASE_DIR = os.path.dirname(__file__)
MARKER = os.path.join(BASE_DIR, ".chatbot_ready")

# ================= CONFIG =================

PYTHON_PACKAGES = [
    "ollama",
    "chromadb",
    "pillow",
    "paddleocr",
    "vosk",
    "sounddevice",
    "numpy",
]

OLLAMA_MODELS = [
    "llama3.1:8b",
    "minicpm-v",
    "nomic-embed-text",
]

VOSK_MODEL_URL = (
    "https://alphacephei.com/vosk/models/"
    "vosk-model-small-en-us-0.15.zip"
)

VOSK_DIR = os.path.join(BASE_DIR, "models", "vosk")

# ==========================================


def run(cmd):
    subprocess.check_call(cmd, shell=True)


def already_done():
    return os.path.exists(MARKER)


def mark_done():
    with open(MARKER, "w") as f:
        f.write("ready")


def install_python_deps():
    print("📦 Installing Python dependencies...")
    for pkg in PYTHON_PACKAGES:
        run(f"{sys.executable} -m pip install {pkg}")


def check_ollama():
    print("🧠 Checking Ollama...")
    try:
        import ollama
        ollama.list()
    except Exception:
        print("❌ Ollama not running")
        print("👉 Start it using: ollama serve")
        sys.exit(1)


def pull_ollama_models():
    print("⬇️ Pulling Ollama models (one-time)...")
    for model in OLLAMA_MODELS:
        run(f"ollama pull {model}")


def setup_vosk():
    print("🎙️ Setting up Vosk...")
    if os.path.exists(VOSK_DIR):
        print("✅ Vosk model already exists")
        return

    os.makedirs(VOSK_DIR, exist_ok=True)
    zip_path = os.path.join(VOSK_DIR, "vosk.zip")

    print("⬇️ Downloading Vosk model...")
    urllib.request.urlretrieve(VOSK_MODEL_URL, zip_path)

    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(VOSK_DIR)

    os.remove(zip_path)

    extracted = os.listdir(VOSK_DIR)[0]
    model_path = os.path.join(VOSK_DIR, extracted)

    print("\n⚠️ IMPORTANT:")
    print(f"Set environment variable:")
    print(f"VOSK_MODEL_PATH={model_path}\n")


def main():
    print("\n=== eSim Copilot One-Time Setup ===\n")

    if already_done():
        print("✅ Chatbot already set up. Nothing to do.")
        return

    install_python_deps()
    check_ollama()
    pull_ollama_models()
    setup_vosk()

    mark_done()
    print("\n🎉 eSim Copilot setup COMPLETE!")
    print("You can now launch eSim normally.")


if __name__ == "__main__":
    main()
