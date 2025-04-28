import subprocess
import os
import json
from PyQt5.QtCore import QThread, pyqtSignal

os.environ["QT_QPA_PLATFORM"] = "xcb"

class OllamaWorker(QThread):
    """Runs Ollama in a separate thread."""
    response_signal = pyqtSignal(str)  # Signal to send response back to the UI

    def __init__(self, user_text):
        super().__init__()
        self.user_text = user_text

    def run(self):
        try:
            messages = [
                {
                    "role": "system",
                    "content": ("You are a professional electronic engineer advising users or help debugging on "
                                "EDA tool eSim's KiCad, and NgSPICE simulation. "
                                "Explain concisely in at MOST 30 words or 5 sentences to minimize wait time.Do not exceed limit. "
                                "Here is the maintained chat history.")
                },
                {"role": "user", "content": self.user_text}
            ]
            
            response = subprocess.run(
                ["ollama", "run", "qwen2.5-coder:3b", json.dumps(messages)], 
                capture_output=True, text=True, check=True
            )

            bot_response = response.stdout.strip() or "No response received."
        
        except subprocess.CalledProcessError as e:
            bot_response = f"Error: Ollama execution failed - {e.stderr.strip()}"
        except Exception as e:
            bot_response = f"Error: {str(e)}"

        self.response_signal.emit(bot_response)  # Send response to main thread
