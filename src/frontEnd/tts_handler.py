# tts_handler.py
# Place this file in src/frontEnd/ alongside Chatbot.py
# Install: sudo apt install espeak

import re
import subprocess
from PyQt5.QtCore import QThread


class TTSWorker(QThread):
    def __init__(self, text: str):
        super().__init__()
        self.text  = text
        self._proc = None

    def run(self):
        try:
            self._proc = subprocess.Popen(
                ["espeak", "-s", "150", "-a", "200", self.text],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            print(f"[TTS] espeak started, pid={self._proc.pid}")
            self._proc.wait()
            print(f"[TTS] espeak finished naturally")
        except FileNotFoundError:
            print("[TTS] espeak not found. Run: sudo apt install espeak")
        except Exception as e:
            print(f"[TTS] Error: {e}")
        finally:
            self._proc = None

    def stop(self):
        print(f"[TTS] stop() called, _proc={self._proc}")
        try:
            if self._proc and self._proc.poll() is None:
                print(f"[TTS] killing pid {self._proc.pid}")
                self._proc.kill()
                self._proc.wait()
                print(f"[TTS] killed!")
            else:
                print(f"[TTS] proc already done or None — nothing to kill")
        except Exception as e:
            print(f"[TTS] kill error: {e}")
        finally:
            self._proc = None
        self.terminate()
        self.wait(300)


def clean_for_tts(text: str) -> str:
    text = re.sub(r'```.*?```', 'Code block.', text, flags=re.DOTALL)
    text = re.sub(r'`([^`]+)`', r'\1', text)
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'#+\s*', '', text)
    text = re.sub(r'https?://\S+', 'link', text)
    text = re.sub(r'[#\*\_~<>]', '', text)
    text = re.sub(r'\n+', '. ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()