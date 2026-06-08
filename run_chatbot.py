"""
run_chatbot.py — Standalone launcher for the eSim AI Chatbot
=====================================================================
Run from the project root:
    python run_chatbot.py

Requirements:
    pip install PyQt5 ollama pillow

For voice input:
    pip install SpeechRecognition pyaudio

For offline voice (no internet):
    pip install faster-whisper

LLM backend:
    1. Install Ollama from https://ollama.com
    2. ollama serve
    3. ollama pull qwen2.5:3b     # text model (~2GB)
    4. ollama pull moondream      # vision model (~1.6GB, optional)
"""
import os
import sys

# Add src/ to Python path so all local imports resolve correctly
_HERE = os.path.dirname(os.path.abspath(__file__))
_SRC  = os.path.join(_HERE, 'src')
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

# Minimal Appconfig stub so Chatbot.py imports cleanly without the
# full eSim configuration layer (which expects an installed eSim).
# Only used when running chatbot standalone (not via Application.py).
import types
_conf_mod = types.ModuleType("configuration")
_app_mod  = types.ModuleType("configuration.Appconfig")

class _AppConfigStub:
    """Minimal stub — only attributes that Chatbot.py actually uses."""
    noteArea = {}
    procThread_list = []
    process_obj = []
    _APPLICATION = "eSim"
    _VERSION = "2.4"
    current_project = {"ProjectName": None}
    def print_info(self, *a): pass
    def print_error(self, *a): pass

_app_mod.Appconfig = _AppConfigStub
_conf_mod.Appconfig = _app_mod
sys.modules["configuration"] = _conf_mod
sys.modules["configuration.Appconfig"] = _app_mod

# Now safe to import the chatbot UI
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from frontEnd.Chatbot import ChatbotGUI  # noqa: E402


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("eSim AI Chatbot")
    app.setFont(QFont("Segoe UI", 10))

    # High-DPI support (Windows)
    try:
        from PyQt5.QtCore import Qt
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    except Exception:
        pass

    window = ChatbotGUI()
    window.setWindowTitle("eSim AI Assistant — Standalone")
    window.resize(520, 640)
    window.show()

    print("=" * 60)
    print("  eSim AI Chatbot — running standalone")
    print("=" * 60)
    print()
    print("  Status: Window opened [OK]")
    print()
    print("  To enable AI responses:")
    print("    1. Install Ollama: https://ollama.com")
    print("    2. Run:  ollama serve")
    print("    3. Run:  ollama pull qwen2.5:3b")
    print("    4. Restart this script")
    print()
    print("  The Live/Offline indicator in the top-right")
    print("  of the chat window shows Ollama's status.")
    print("=" * 60)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
