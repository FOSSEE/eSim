from chatBot.chatbot_thread import OllamaWorker
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QTextEdit, QVBoxLayout, QLineEdit, QPushButton
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
import os
if os.name == 'nt':
    from frontEnd import pathmagic  # noqa:F401
    init_path = ''
else:
    import pathmagic  # noqa:F401
    init_path = '../../'

class ChatbotGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Chatbot")
        self.setFixedSize(400, 250)
        self.chat_history = []
        
        layout = QVBoxLayout(self)
        self.chat_display = QTextEdit(self, readOnly=True)
        layout.addWidget(self.chat_display)
        
        input_layout = QHBoxLayout()
        self.user_input = QLineEdit(self, placeholderText="Type your query here...")
        self.user_input.setStyleSheet("font-size: 14px;")
        self.user_input.returnPressed.connect(self.ask_ollama)
        input_layout.addWidget(self.user_input)
        
        self.clear_button = QPushButton(self, icon=QIcon(init_path + 'images/clear.png'))
        self.clear_button.setIconSize(QSize(18, 18))
        self.clear_button.setStyleSheet("font-size: 14px; padding: 5px;")
        self.clear_button.clicked.connect(self.clear_session)
        input_layout.addWidget(self.clear_button)
        
        layout.addLayout(input_layout)

    def ask_ollama(self):
        user_text = self.user_input.text().strip()
        if not user_text:
            return
        
        self.chat_history = (self.chat_history + [f"User: {user_text}"])[-4:]
        self.chat_display.append(f"You: {user_text}")
        
        self.worker = OllamaWorker(self.chat_history)
        self.worker.response_signal.connect(self.display_response)
        self.worker.start()
        
        self.user_input.clear()

    def display_response(self, bot_response):
        """Display the bot's response in the chat display."""
        self.chat_display.append(f"Bot: {bot_response}\n")
        self.chat_history.append(f"Bot: {bot_response}\n")
    
    def clear_session(self):
        """Clear the chat display."""
        self.chat_display.clear()
        self.chat_history=[]
    def debug_ollama(self):
        """Send log to Ollama and get response asynchronously."""
        self.chat_display.append(f"============Simulation Failed=============\n")
        user_text = self.user_input.text().strip()
        self.worker = OllamaWorker(user_text)
        self.worker.response_signal.connect(self.display_response)
        self.worker.start()
        self.user_input.clear()  # Clear input field

    def debug_error(self, log):
        self.chat_history = []
        if os.path.exists(log):
            with open(log, "r") as f:
                lines = f.readlines()

            # Limit the number of lines to a maximum of 6
            limited_lines = lines[:6]  

            combined_text = "\n".join(limited_lines)

            self.user_input.setText(combined_text)
            self.debug_ollama()
