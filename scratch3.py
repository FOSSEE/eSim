import sys, base64
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QUrl

app = QApplication(sys.argv)
from src.frontEnd.Chatbot import ChatbotGUI

gui = ChatbotGUI()

img_key = "test_key"
with open("images/chatbot.png", "rb") as f:
    raw = f.read()
b64 = base64.b64encode(raw).decode('utf-8')
gui._images_store = {img_key: [("chatbot.png", b64)]}

url = QUrl(f"imageview://{img_key}/0")
print("Emitting link click...")
gui._handle_link_click(url)
print("Done!")
