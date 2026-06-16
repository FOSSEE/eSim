import sys
sys.path.insert(0, '.')

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

app = QApplication(sys.argv)

from frontEnd.Chatbot import ChatbotGUI
window = ChatbotGUI()
window.setWindowTitle("eSim AI Chatbot - Test")
window.resize(900, 700)
window.show()

sys.exit(app.exec())