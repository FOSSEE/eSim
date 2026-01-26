#!/usr/bin/env python3
import sys
from PyQt5 import QtWidgets

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    window.setWindowTitle("eSim Simple App")
    window.setGeometry(100, 100, 800, 600)
    
    # Create a central widget
    central_widget = QtWidgets.QWidget()
    window.setCentralWidget(central_widget)
    
    # Create a layout
    layout = QtWidgets.QVBoxLayout()
    central_widget.setLayout(layout)
    
    # Add a label
    label = QtWidgets.QLabel("eSim is running!")
    label.setStyleSheet("font-size: 24px; color: #1976d2;")
    layout.addWidget(label)
    
    # Add a button
    button = QtWidgets.QPushButton("Click Me")
    button.clicked.connect(lambda: label.setText("Button clicked!"))
    layout.addWidget(button)
    
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 