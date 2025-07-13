import sys
import csv
import subprocess
import os

from PyQt5.QtCore import (
    Qt, QSize, QTimer, QPropertyAnimation, QEasingCurve, QRect, 
    QPoint, QUrl, QObject, pyqtSignal, pyqtSignal as Signal
)

from PyQt5.QtGui import (
    QFont, QColor, QPalette, QTextCursor, QTextCharFormat, QTextFormat, 
    QSyntaxHighlighter, QTextDocument, QDesktopServices, QIcon, 
    QPainter, QLinearGradient, QBrush
)

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QFrame, 
    QHBoxLayout, QScrollArea, QLabel, QPushButton, QLineEdit, 
    QTextEdit, QSplitter, QMessageBox, QSizePolicy, QTabWidget, 
    QStyle, QToolButton, QProxyStyle, QStyleFactory, QTextBrowser, 
    QFileDialog, QScrollBar, QSizeGrip
)

from .HTMLUserManual import HTMLUserManual

class HSeparator(QFrame):
    """A horizontal separator line"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)
        self.setLineWidth(1)
        self.setMidLineWidth(0)
        self.setFixedHeight(1)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

class ThemeManager(QObject):
    """Manages application theming with support for dark/light modes"""
    themeChanged = Signal(bool)  # True for dark, False for light
    
    def __init__(self):
        super().__init__()
        self._is_dark = False
        self._themes = {
            'dark': {
                'primary': '#4fc3f7',
                'primary_light': '#8bf6ff',
                'primary_dark': '#0093c4',
                'secondary': '#7c4dff',
                'background': '#121212',
                'surface': '#1e1e1e',
                'error': '#cf6679',
                'on_primary': '#000000',
                'on_secondary': '#000000',
                'on_background': '#ffffff',
                'on_surface': '#ffffff',
                'on_error': '#000000',
                'elevation': {
                    'dp0': '#121212',
                    'dp1': '#1e1e1e',
                    'dp2': '#212121',
                    'dp3': '#242424',
                    'dp4': '#272727',
                    'dp6': '#2c2c2c',
                    'dp8': '#2d2d2d',
                    'dp12': '#2e2e2e',
                    'dp16': '#2f2f2f',
                    'dp24': '#303030'
                },
                'text': {
                    'primary': 'rgba(255, 255, 255, 0.87)',
                    'secondary': 'rgba(255, 255, 255, 0.6)',
                    'hint': 'rgba(255, 255, 255, 0.38)',
                    'disabled': 'rgba(255, 255, 255, 0.38)',
                    'icon': 'rgba(255, 255, 255, 0.5)'
                },
                'divider': 'rgba(255, 255, 255, 0.12)'
            },
            'light': {
                'primary': '#1976d2',
                'primary_light': '#63a4ff',
                'primary_dark': '#004ba0',
                'secondary': '#ff4081',
                'background': '#f5f5f5',
                'surface': '#ffffff',
                'error': '#d32f2f',
                'on_primary': '#ffffff',
                'on_secondary': '#000000',
                'on_background': '#000000',
                'on_surface': '#000000',
                'on_error': '#ffffff',
                'elevation': {
                    'dp0': '#ffffff',
                    'dp1': '#fafafa',
                    'dp2': '#f5f5f5',
                    'dp3': '#eeeeee',
                    'dp4': '#e0e0e0',
                    'dp6': '#d6d6d6',
                    'dp8': '#cccccc',
                    'dp12': '#c2c2c2',
                    'dp16': '#b8b8b8',
                    'dp24': '#adadad'
                },
                'text': {
                    'primary': 'rgba(0, 0, 0, 0.87)',
                    'secondary': 'rgba(0, 0, 0, 0.6)',
                    'hint': 'rgba(0, 0, 0, 0.38)',
                    'disabled': 'rgba(0, 0, 0, 0.38)',
                    'icon': 'rgba(0, 0, 0, 0.54)'
                },
                'divider': 'rgba(0, 0, 0, 0.12)'
            }
        }
    
    @property
    def is_dark(self):
        return self._is_dark
    
    @is_dark.setter
    def is_dark(self, value):
        if self._is_dark != bool(value):
            self._is_dark = bool(value)
            self.themeChanged.emit(self._is_dark)
    
    def colors(self):
        """Get current theme colors"""
        return self._themes['dark' if self._is_dark else 'light']
    
    def get_palette(self):
        """Get QPalette for current theme"""
        colors = self.colors()
        palette = QPalette()
        
        if self._is_dark:
            palette.setColor(QPalette.Window, QColor(colors['background']))
            palette.setColor(QPalette.WindowText, QColor(colors['text']['primary']))
            palette.setColor(QPalette.Base, QColor(colors['surface']))
            palette.setColor(QPalette.AlternateBase, QColor(colors['elevation']['dp1']))
            palette.setColor(QPalette.ToolTipBase, QColor(colors['primary']))
            palette.setColor(QPalette.ToolTipText, QColor(colors['on_primary']))
            palette.setColor(QPalette.Text, QColor(colors['text']['primary']))
            palette.setColor(QPalette.Button, QColor(colors['surface']))
            palette.setColor(QPalette.ButtonText, QColor(colors['text']['primary']))
            palette.setColor(QPalette.BrightText, Qt.white)
            palette.setColor(QPalette.Link, QColor(colors['primary']))
            palette.setColor(QPalette.Highlight, QColor(colors['primary']))
            palette.setColor(QPalette.HighlightedText, QColor(colors['on_primary']))
            
            # Disabled colors
            palette.setColor(QPalette.Disabled, QPalette.WindowText, 
                           QColor(colors['text']['disabled']))
            palette.setColor(QPalette.Disabled, QPalette.Text, 
                           QColor(colors['text']['disabled']))
            palette.setColor(QPalette.Disabled, QPalette.ButtonText, 
                           QColor(colors['text']['disabled']))
        else:
            palette = QStyleFactory.create('fusion').standardPalette()
            palette.setColor(QPalette.Window, QColor(colors['background']))
            palette.setColor(QPalette.WindowText, QColor(colors['text']['primary']))
            palette.setColor(QPalette.Base, QColor(colors['surface']))
            palette.setColor(QPalette.AlternateBase, QColor(colors['elevation']['dp1']))
            palette.setColor(QPalette.ToolTipBase, QColor(colors['primary']))
            palette.setColor(QPalette.ToolTipText, QColor(colors['on_primary']))
            palette.setColor(QPalette.Text, QColor(colors['text']['primary']))
            palette.setColor(QPalette.Button, QColor(colors['surface']))
            palette.setColor(QPalette.ButtonText, QColor(colors['text']['primary']))
            palette.setColor(QPalette.BrightText, Qt.white)
            palette.setColor(QPalette.Link, QColor(colors['primary']))
            palette.setColor(QPalette.Highlight, QColor(colors['primary']))
            palette.setColor(QPalette.HighlightedText, QColor(colors['on_primary']))
        
        return palette
    
    def get_stylesheet(self):
        """Get stylesheet for current theme"""
        colors = self.colors()
        return f"""
            /* Main window and widgets */
            QWidget {{
                background-color: {colors['background']};
                color: {colors['text']['primary']};
                selection-background-color: {colors['primary']};
                selection-color: {colors['on_primary']};
                font-family: 'Segoe UI', 'Roboto', sans-serif;
            }}
            
            /* Buttons */
            QPushButton {{
                background-color: {colors['primary']};
                color: {colors['on_primary']};
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                min-width: 80px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: {colors['primary_light'] if self._is_dark else colors['primary_dark']};
            }}
            QPushButton:pressed {{
                background-color: {colors['primary_dark'] if self._is_dark else colors['primary_light']};
            }}
            QPushButton:disabled {{
                background-color: {colors['elevation']['dp1']};
                color: {colors['text']['disabled']};
            }}
            
            /* Line edits */
            QLineEdit, QTextEdit, QPlainTextEdit {{
                background-color: {colors['surface']};
                border: 1px solid {colors['text']['hint']};
                border-radius: 4px;
                padding: 8px;
                selection-background-color: {colors['primary']};
                selection-color: {colors['on_primary']};
            }}
            QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
                border: 2px solid {colors['primary']};
                padding: 7px; /* Compensate for larger border */
            }}
            
            /* Scroll bars */
            QScrollBar:vertical {{
                border: none;
                background: {colors['elevation']['dp1']};
                width: 10px;
                margin: 0px 0px 0px 0px;
            }}
            QScrollBar::handle:vertical {{
                background: {colors['text']['hint']};
                min-height: 20px;
                border-radius: 5px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {colors['primary']};
            }}
            
            /* Tabs */
            QTabWidget::pane {{
                border-top: 1px solid {colors['elevation']['dp4']};
                background: {colors['background']};
            }}
            QTabBar::tab {{
                background: transparent;
                color: {colors['text']['secondary']};
                padding: 8px 16px;
                border: none;
                border-bottom: 2px solid transparent;
            }}
            QTabBar::tab:selected, QTabBar::tab:hover {{
                color: {colors['primary']};
                border-bottom: 2px solid {colors['primary']};
            }}
            
            /* Custom widget styles */
            #container {{
                background-color: {colors['surface']};
                border: 1px solid {colors['elevation']['dp4']};
                border-radius: 8px;
            }}
            #container:hover {{
                border-color: {colors['primary']};
            }}
            
            /* Custom scroll area */
            QScrollArea {{
                border: none;
                background: transparent;
            }}
            
            /* Tool tips */
            QToolTip {{
                background-color: {colors['primary']};
                color: {colors['on_primary']};
                border: none;
                padding: 4px 8px;
                border-radius: 4px;
            }}
        """

class ExpandableQAWidget(QFrame):
    """Custom widget for expandable Q&A pairs with theme support"""
    
    def __init__(self, question, answer, parent=None):
        super().__init__(parent)
        self.question = question
        self.answer = answer
        self.is_expanded = False
        self.theme_manager = ThemeManager()
        
        self.setFrameStyle(QFrame.NoFrame)
        self.setLineWidth(0)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
        # Setup UI and animation
        self.setup_ui()
        self.setup_animation()
        
        # Connect theme changes
        self.theme_manager.themeChanged.connect(self.update_styles)
        self.update_styles()
    
    def update_styles(self, is_dark=None):
        """Update widget styles based on current theme"""
        colors = self.theme_manager.colors()
        
        # Base style for the widget
        self.setStyleSheet(f"""
            ExpandableQAWidget {{
                background-color: transparent;
                border: none;
                margin: 0px 0px 8px 0px;
                padding: 0px;
            }}
            #container {{
                background-color: {colors['surface']};
                border: 1px solid {colors['elevation']['dp4']};
                border-radius: 8px;
            }}
            #container:hover {{
                border-color: {colors['primary']};
            }}
            #question_label {{
                color: {colors['text']['primary']};
                font-weight: 500;
                font-size: 13px;
                padding: 0px;
                margin: 0px;
            }}
            #answer_label {{
                color: {colors['text']['secondary']};
                font-size: 13px;
                line-height: 1.5;
                padding: 8px 0px 0px 0px;
            }}
            #indicator {{
                color: {colors['primary']};
                font-size: 14px;
                min-width: 24px;
                padding: 0px;
                margin: 0px;
            }}
            #separator {{
                background-color: {colors['divider']};
                border: none;
                height: 1px;
                margin: 8px 0px;
            }}
        """)
        
    def setup_ui(self):
        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        # Main container for the card
        self.container = QFrame()
        self.container.setObjectName("container")
        self.container.setFrameStyle(QFrame.NoFrame)
        self.container.setLineWidth(0)

        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(20, 14, 20, 14)  # More padding for text
        container_layout.setSpacing(6)
        
        # Question section (always visible)
        self.question_widget = QWidget()
        question_layout = QHBoxLayout(self.question_widget)
        question_layout.setContentsMargins(0, 0, 0, 0)
        question_layout.setSpacing(8)
        
        # Question label
        self.question_label = QLabel(self.question)
        self.question_label.setObjectName("question_label")
        self.question_label.setWordWrap(True)
        self.question_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.question_label.setMinimumWidth(0)
        self.question_label.setMaximumWidth(10000)
        
        # Expand/collapse indicator (chevron)
        self.indicator = QLabel("\u25BC")  # ▼
        self.indicator.setObjectName("indicator")
        self.indicator.setAlignment(Qt.AlignCenter)
        self.indicator.setFixedWidth(24)
        
        question_layout.addWidget(self.question_label, 1)
        question_layout.addWidget(self.indicator, 0, Qt.AlignTop)
        
        container_layout.addWidget(self.question_widget)
        
        # Answer section (initially hidden and animated)
        self.answer_widget = QWidget()
        self.answer_widget.setVisible(False)
        self.answer_widget.setStyleSheet("background-color: transparent; border: none;")
        
        answer_layout = QVBoxLayout(self.answer_widget)
        answer_layout.setContentsMargins(0, 6, 0, 0)
        answer_layout.setSpacing(6)
        
        # Separator line
        separator = QFrame()
        separator.setObjectName("separator")
        separator.setFrameShape(QFrame.HLine)
        answer_layout.addWidget(separator)
        
        # Answer label
        self.answer_label = QLabel(self.answer)
        self.answer_label.setObjectName("answer_label")
        self.answer_label.setWordWrap(True)
        self.answer_label.setOpenExternalLinks(True)
        self.answer_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.answer_label.setMinimumWidth(0)
        self.answer_label.setMaximumWidth(10000)
        answer_layout.addWidget(self.answer_label)
        
        container_layout.addWidget(self.answer_widget)
        self.layout.addWidget(self.container)
        
    def setup_animation(self):
        self.answer_widget.setMaximumHeight(0)
        self.animation = QPropertyAnimation(self.answer_widget, b"maximumHeight")
        self.animation.setDuration(250)
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)

    def enterEvent(self, event):
        # Hover effect is handled by stylesheet
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        # Hover effect is handled by stylesheet
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.toggle_expansion()
        super().mousePressEvent(event)
        
    def toggle_expansion(self):
        self.is_expanded = not self.is_expanded
        if self.is_expanded:
            self.indicator.setText("\u25B2")  # ▲
            self.answer_widget.setVisible(True)
            end_height = self.answer_widget.sizeHint().height()
        else:
            self.indicator.setText("\u25BC")  # ▼
            end_height = 0
            
        # Update styles to reflect expanded state
        self.update_styles()
        start_height = self.answer_widget.maximumHeight()
        self.animation.setStartValue(start_height)
        self.animation.setEndValue(end_height)
        self.animation.start()

class ChatBotWidget(QWidget):
    """Simple chatbot interface widget with theme support"""
    
    def __init__(self, parent=None, theme_manager=None):
        super().__init__(parent)
        self.theme_manager = theme_manager or ThemeManager()
        self.setup_ui()
        
        # Connect theme changes
        self.theme_manager.themeChanged.connect(self.update_styles)
        self.update_styles()
        
    def setup_ui(self):
        # Main layout
        self.setObjectName("chat_widget")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Chat header
        self.header = QLabel("💬 Support Chat")
        self.header.setObjectName("chat_header")
        self.header.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.header.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.header.setContentsMargins(12, 8, 12, 8)
        
        # Chat display area
        self.chat_display = QTextEdit()
        self.chat_display.setObjectName("chat_display")
        self.chat_display.setReadOnly(True)
        self.chat_display.setFont(QFont("Segoe UI", 9))
        
        # Input area
        input_container = QWidget()
        input_container.setObjectName("input_container")
        input_layout = QHBoxLayout(input_container)
        input_layout.setContentsMargins(12, 8, 12, 12)
        input_layout.setSpacing(8)
        
        self.message_input = QLineEdit()
        self.message_input.setObjectName("message_input")
        self.message_input.setPlaceholderText("Type your message here...")
        self.message_input.setFont(QFont("Segoe UI", 9))
        self.message_input.returnPressed.connect(self.send_message)
        
        self.send_button = QPushButton("Send")
        self.send_button.setObjectName("send_button")
        self.send_button.setFont(QFont("Segoe UI", 9, QFont.Medium))
        self.send_button.setCursor(Qt.PointingHandCursor)
        self.send_button.clicked.connect(self.send_message)
        
        # Set fixed height for input area
        self.message_input.setMinimumHeight(36)
        self.send_button.setFixedHeight(36)
        self.send_button.setMinimumWidth(80)
        
        # Add widgets to layouts
        input_layout.addWidget(self.message_input)
        input_layout.addWidget(self.send_button)
        
        # Add widgets to main layout
        layout.addWidget(self.header)
        layout.addWidget(HSeparator())
        layout.addWidget(self.chat_display, 1)  # Take remaining space
        layout.addWidget(input_container)
        
        # Add welcome message
        self.add_bot_message("Hello! How can I help you with your eSIM today?")
    
    def update_styles(self, is_dark=None):
        """Update widget styles based on current theme"""
        colors = self.theme_manager.colors()
        is_dark = self.theme_manager.is_dark
        
        # Base style for the widget
        self.setStyleSheet(f"""
            #chat_widget {{
                background-color: {colors['background']};
                color: {colors['text']['primary']};
                border: none;
            }}
            #chat_header {{
                color: {colors['text']['primary']};
                background-color: {colors['elevation']['dp2']};
                border: none;
                border-radius: 0px;
                font-size: 13px;
                font-weight: 600;
                padding: 12px 16px;
            }}
            #chat_display {{
                background-color: {colors['surface']};
                color: {colors['text']['primary']};
                border: none;
                border-top: 1px solid {colors['divider']};
                border-bottom: 1px solid {colors['divider']};
                padding: 12px 16px;
                font-size: 13px;
                line-height: 1.5;
                selection-background-color: {colors['primary']};
                selection-color: {colors['on_primary']};
            }}
            #input_container {{
                background-color: {colors['surface']};
                border: none;
                padding: 0;
                margin: 0;
            }}
            #message_input {{
                background-color: {colors['elevation']['dp2']};
                color: {colors['text']['primary']};
                border: 1px solid {colors['divider']};
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 13px;
                selection-background-color: {colors['primary']};
                selection-color: {colors['on_primary']};
            }}
            #message_input:focus {{
                border: 1px solid {colors['primary']};
                background-color: {colors['surface']};
            }}
            #message_input::placeholder {{
                color: {colors['text']['hint']};
            }}
            #send_button {{
                background-color: {colors['primary']};
                color: {colors['on_primary']};
                border: none;
                border-radius: 6px;
                padding: 0 16px;
                font-weight: 500;
                min-width: 80px;
            }}
            #send_button:hover {{
                background-color: {colors['primary_dark']};
            }}
            #send_button:pressed {{
                background-color: {colors['primary_light']};
            }}
            #send_button:disabled {{
                background-color: {colors['elevation']['dp4']};
                color: {colors['text']['disabled']};
            }}
            /* Custom scrollbar */
            QScrollBar:vertical {{
                width: 8px;
                background: transparent;
            }}
            QScrollBar::handle:vertical {{
                background: {colors['elevation']['dp8']};
                min-height: 30px;
                border-radius: 4px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {colors['elevation']['dp12']};
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)
        
        # Update chat display styling
        self.chat_display.document().setDefaultStyleSheet(f"""
            body {{
                color: {colors['text']['primary']};
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 13px;
                line-height: 1.5;
            }}
            .user-message {{
                color: {colors['text']['primary']};
                margin: 8px 0;
                padding: 8px 0;
                border-bottom: 1px solid {colors['divider']};
            }}
            .bot-message {{
                color: {colors['primary']};
                margin: 8px 0;
                padding: 8px 0;
                border-bottom: 1px solid {colors['divider']};
            }}
            b {{
                color: {colors['primary']};
            }}
        """)
    
    def add_user_message(self, message):
        """Add a user message to the chat"""
        self.chat_display.append(f'<div class="user-message"><b>You:</b> {message}</div>')
        self.scroll_to_bottom()
    
    def add_bot_message(self, message):
        """Add a bot message to the chat"""
        self.chat_display.append(f'<div class="bot-message"><b>eSIM Support:</b> {message}</div>')
        self.scroll_to_bottom()
    
    def scroll_to_bottom(self):
        """Scroll the chat to the bottom"""
        scrollbar = self.chat_display.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        
    def send_message(self):
        """Send a message from the user and get a response"""
        message = self.message_input.text().strip()
        if not message:
            return
        # Add user message to chat
        self.add_user_message(message)
        # Clear input
        self.message_input.clear()
        # Get bot response
        response = self.get_bot_response(message.lower())
        # Simulate typing delay
        QTimer.singleShot(500, lambda: self.add_bot_message(response))
            
    def get_bot_response(self, message):
        """Simple response logic for eSIM"""
        responses = {
            "hello": "Hello! How can I assist you with your eSIM?",
            "hi": "Hi there! What can I help you with regarding your eSIM today?",
            "help": "I'm here to help with eSIM! You can ask me about activation, troubleshooting, data plans, or account management.",
            "activation": "To activate your eSIM, open the eSIM app, go to 'My Plans', and scan the QR code provided in your purchase confirmation email.",
            "data": "You can check your eSIM data usage in the main dashboard of the eSIM app under 'Usage Overview'.",
            "network": "If you're having network issues with eSIM, try: 1) Toggle airplane mode, 2) Restart your device, 3) Check if your plan is active in the app.",
            "support": "For additional eSIM support, contact us at support@esim.com or use the in-app support chat.",
            "plan": "eSIM offers flexible data plans for over 200+ countries. Check available plans in the 'Browse Plans' section of the app.",
            "coverage": "eSIM provides coverage in 200+ countries worldwide. Check coverage for your destination in the app's coverage map.",
            "refund": "eSIM offers refunds for unused plans within 30 days of purchase. Contact support for refund requests.",
            "price": "eSIM offers competitive pricing starting from $3 for short-term plans. Check current pricing in the app.",
        }
        
        for keyword, response in responses.items():
            if keyword in message:
                return response
                
        return "I understand you're asking about eSIM services. Could you please be more specific? You can ask about activation, data plans, network issues, coverage, pricing, or general support."

# Utility function to get the current theme from any widget

def get_current_theme(widget):
    """Traverse up the widget hierarchy to find a ThemeManager, or fallback to QApplication main window."""
    parent = widget
    while parent is not None:
        if hasattr(parent, 'theme_manager'):
            return parent.theme_manager.is_dark
        parent = parent.parent() if hasattr(parent, 'parent') else None
    # Fallback: try to get from QApplication's topLevelWidgets
    from PyQt5.QtWidgets import QApplication
    for w in QApplication.topLevelWidgets():
        if hasattr(w, 'theme_manager'):
            return w.theme_manager.is_dark
        if hasattr(w, 'is_dark_theme'):
            return w.is_dark_theme
    return False  # Default to light mode if not found

class PDFManualWidget(QWidget):
    """Widget to handle PDF manual opening functionality"""
    
    def __init__(self, parent=None, is_dark_theme=False):
        super().__init__(parent)
        self.is_dark_theme = is_dark_theme
        self.html_manual_window = None  # Keep reference to prevent GC
        self.setup_ui()
        
    def set_theme(self, is_dark_theme):
        self.is_dark_theme = is_dark_theme
        if self.html_manual_window is not None and self.html_manual_window.isVisible():
            self.html_manual_window.set_theme(is_dark_theme)
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Header
        header = QLabel("📖 User Manual")
        header.setFont(QFont("Segoe UI", 10, QFont.Bold))
        header.setStyleSheet("color: #2c3e50; padding: 5px 0px;")
        layout.addWidget(header)
        
        # Description
        description = QLabel("Access the complete eSIM user manual with detailed instructions, troubleshooting guides, and technical specifications.")
        description.setWordWrap(True)
        description.setFont(QFont("Segoe UI", 9))
        description.setStyleSheet("color: #34495e; padding: 10px; background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 3px;")
        layout.addWidget(description)
        
        # Open Manual Button
        self.open_manual_btn = QPushButton("📄 Open User Manual (PDF)")
        self.open_manual_btn.setFont(QFont("Segoe UI", 9, QFont.Bold))
        self.open_manual_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 12px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
        """)
        self.open_manual_btn.clicked.connect(self.open_html_manual)
        layout.addWidget(self.open_manual_btn)
        
        # Status label
        self.status_label = QLabel("")
        self.status_label.setFont(QFont("Segoe UI", 8))
        self.status_label.setStyleSheet("color: #6c757d; padding: 5px;")
        layout.addWidget(self.status_label)
        
        # Add stretch to push content to top
        layout.addStretch()
        
    def open_html_manual(self):
        """Open the HTML user manual in a separate window, always using the current theme from the main app."""
        is_dark = get_current_theme(self)
        if self.html_manual_window is None or not self.html_manual_window.isVisible():
            from .HTMLUserManual import HTMLUserManual
            self.html_manual_window = HTMLUserManual(is_dark_theme=is_dark)
            self.html_manual_window.setWindowTitle("eSIM User Manual (HTML)")
            self.html_manual_window.resize(900, 700)
            self.html_manual_window.show()
        else:
            self.html_manual_window.set_theme(is_dark)
            self.html_manual_window.raise_()
            self.html_manual_window.activateWindow()

class FosseHelpWidget(QWidget):
    """Main Help widget with FAQ section (FAQ search bar small and in header row, no icon)"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.qa_data = []
        self.setup_ui()
        self.load_faq_from_csv()
        
    def setup_ui(self):
        # Initialize theme manager
        self.theme_manager = ThemeManager()
        
        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Header widget
        self.header_widget = QWidget()
        self.header_widget.setObjectName("header_widget")
        header_layout = QHBoxLayout(self.header_widget)
        header_layout.setContentsMargins(16, 16, 16, 16)
        header_layout.setSpacing(16)
        
        # Title label
        self.title_label = QLabel("Frequently Asked Questions")
        self.title_label.setObjectName("title_label")
        
        # Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setObjectName("search_bar")
        self.search_bar.setPlaceholderText("Search FAQs...")
        self.search_bar.setClearButtonEnabled(True)
        self.search_bar.setFixedWidth(240)
        self.search_bar.setMinimumHeight(32)
        
        # Connect search functionality
        self.search_bar.textChanged.connect(self.filter_faqs)
        
        # Add widgets to header
        header_layout.addWidget(self.title_label, 1)
        header_layout.addWidget(self.search_bar, 0, Qt.AlignRight)
        
        # Separator line
        self.separator = HSeparator()
        self.separator.setObjectName("separator")
        
        # Scroll area for Q&A
        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName("scroll_area")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        
        # Container for Q&A widgets
        self.qa_container = QWidget()
        self.qa_container.setObjectName("qa_container")
        self.qa_layout = QVBoxLayout(self.qa_container)
        self.qa_layout.setContentsMargins(16, 12, 16, 24)
        self.qa_layout.setSpacing(12)
        self.qa_layout.addStretch()  # Add stretch to push content to top
        
        self.scroll_area.setWidget(self.qa_container)
        
        # Add widgets to main layout
        self.main_layout.addWidget(self.header_widget)
        self.main_layout.addWidget(self.separator)
        self.main_layout.addWidget(self.scroll_area, 1)  # Take remaining space
        
        # Set the main layout and connect theme changes
        self.setLayout(self.main_layout)
        self.theme_manager.themeChanged.connect(self.update_styles)
        self.update_styles()
    
    def update_styles(self, is_dark=None):
        """Update widget styles based on current theme"""
        colors = self.theme_manager.colors()
        
        # Base style for the widget
        self.setStyleSheet(f"""
            #fosse_help_widget {{
                background-color: {colors['background']};
                color: {colors['text']['primary']};
            }}
            #header_widget {{
                background-color: {colors['surface']};
                border: none;
            }}
            #title_label {{
                font-size: 16px;
                font-weight: 600;
                color: {colors['text']['primary']};
                margin: 0;
                padding: 0;
            }}
            #search_bar {{
                background-color: {colors['elevation']['dp2']};
                color: {colors['text']['primary']};
                border: 1px solid {colors['divider']};
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 13px;
                min-height: 32px;
                selection-background-color: {colors['primary']};
                selection-color: {colors['on_primary']};
            }}
            #search_bar:focus {{
                border: 1px solid {colors['primary']};
                background-color: {colors['surface']};
            }}
            #search_bar::placeholder {{
                color: {colors['text']['hint']};
            }}
            #separator {{
                background-color: {colors['divider']};
                height: 1px;
                border: none;
            }}
            #scroll_area, #qa_container {{
                background-color: {colors['background']};
                border: none;
            }}
            QScrollBar:vertical {{
                width: 8px;
                background: transparent;
            }}
            QScrollBar::handle:vertical {{
                background: {colors['elevation']['dp8']};
                min-height: 30px;
                border-radius: 4px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {colors['elevation']['dp12']};
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)
        
    def load_faq_from_csv(self):
        """Automatically load FAQ data from CSV file"""
        import csv
        csv_filename = "resources/esim_faq.csv"
        try:
            with open(csv_filename, 'r', encoding='utf-8', newline='') as csvfile:
                sample = csvfile.read(1024)
                csvfile.seek(0)
                sniffer = csv.Sniffer()
                try:
                    delimiter = sniffer.sniff(sample).delimiter
                except:
                    delimiter = ','
                reader = csv.reader(csvfile, delimiter=delimiter)
                first_row = next(reader, None)
                if first_row and (first_row[0].lower() in ['question', 'q'] or 'question' in first_row[0].lower()):
                    pass
                else:
                    if first_row and len(first_row) >= 2:
                        self.qa_data.append((first_row[0], first_row[1]))
                for row in reader:
                    if len(row) >= 2 and row[0].strip() and row[1].strip():
                        self.qa_data.append((row[0].strip(), row[1].strip()))
            if self.qa_data:
                self.populate_qa_widgets()
            else:
                self.load_default_esim_faq()
        except FileNotFoundError:
            self.load_default_esim_faq()
        except Exception as e:
            self.load_default_esim_faq()
    
    def load_default_esim_faq(self):
        """Load default eSIM FAQ data"""
        esim_faq_data = [
            ("How do I activate my eSIM?", "Open the eSIM app → 'My Plans' → 'Activate New Plan' → Scan QR code from your purchase email → Follow setup instructions. Your eSIM will be active within minutes."),
            ("Which devices work with eSIM?", "Compatible devices: iPhone XS/XR and newer, iPad Pro (3rd gen+), iPad Air (3rd gen+), iPad mini (5th gen+), Google Pixel 3+, Samsung Galaxy S20+, and most recent Android devices with eSIM support."),
            ("How many countries does eSIM cover?", "eSIM provides coverage in 200+ countries worldwide including Europe, Asia, Americas, Africa, and Oceania. Check specific coverage in the app's 'Browse Plans' section."),
            ("What data plans are available?", "Flexible plans available: Daily (100MB-1GB), Weekly (1GB-10GB), Monthly (3GB-50GB), Regional multi-country plans. Starting from $3 with no hidden fees."),
            ("How do I check my data usage?", "Open eSIM app → Main dashboard shows current usage under 'Usage Overview' → 'My Plans' section displays remaining data, plan expiry, and usage history."),
            ("Can I use eSIM with my regular SIM?", "Yes! eSIM works alongside your physical SIM card. Use dual SIM functionality - keep your home SIM for calls/texts and eSIM for data while traveling."),
            ("My eSIM won't connect. What should I do?", "Troubleshooting: 1) Check device compatibility 2) Verify coverage area 3) Restart device 4) Toggle airplane mode 5) Enable eSIM in Settings → Cellular 6) Contact 24/7 support if issues persist."),
            ("How do I add more data to my plan?", "In eSIM app: 'My Plans' → Select active plan → 'Top Up' or 'Extend Plan' → Choose additional data/time → Complete payment. Updates immediately without new QR code."),
            ("What is the refund policy?", "30-day money-back guarantee for unused plans. Full refund available if you haven't activated your plan or used less than 10MB of data. Contact support for refund requests."),
            ("How do I contact support?", "Multiple support channels: 1) In-app chat (24/7) 2) Email: support@esim.com 3) App help center 4) Website live chat. Multilingual support with 2-4 hour response time."),
        ]
        self.qa_data = esim_faq_data
        self.populate_qa_widgets()
        
    def populate_qa_widgets(self):
        """Create and add Q&A widgets to the scroll area"""
        # Clear existing widgets except the stretch
        if hasattr(self, 'qa_layout'):
            while self.qa_layout.count() > 1:
                child = self.qa_layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
        # Add new Q&A widgets
        for question, answer in self.qa_data:
            qa_widget = ExpandableQAWidget(question, answer)
            self.qa_layout.insertWidget(self.qa_layout.count() - 1, qa_widget)  # Insert before stretch

    def filter_faqs(self):
        """Filter the displayed FAQs based on the search bar text. Show 'No FAQs found.' if nothing matches."""
        search_text = self.search_bar.text().lower().strip()
        found = False
        if hasattr(self, 'qa_layout'):
            for i in range(self.qa_layout.count() - 1):
                item = self.qa_layout.itemAt(i)
                qa_widget = item.widget()
                if isinstance(qa_widget, ExpandableQAWidget):
                    question = qa_widget.question.lower()
                    answer = qa_widget.answer.lower()
                    if search_text in question or search_text in answer:
                        qa_widget.setVisible(True)
                        found = True
                    else:
                        qa_widget.setVisible(False)
        # Remove any previous 'not found' label
        if hasattr(self, '_not_found_label') and self._not_found_label:
            self.qa_layout.removeWidget(self._not_found_label)
            self._not_found_label.deleteLater()
            self._not_found_label = None
        # If nothing found, show a message
        if not found:
            self._not_found_label = QLabel("No FAQs found.")
            self._not_found_label.setStyleSheet("color: #888; font-size: 13px; padding: 24px 0px;")
            self._not_found_label.setAlignment(Qt.AlignCenter)
            self.qa_layout.insertWidget(self.qa_layout.count() - 1, self._not_found_label)
        else:
            self._not_found_label = None

class UserManual(QWidget):
    """
    Enhanced User Manual class with theme support that combines the original PDF opening functionality
    with the comprehensive help GUI system
    """
    
    def __init__(self, is_dark_theme=False, parent=None):
        super().__init__(parent)
        self.theme_manager = ThemeManager()
        # Set initial theme based on parameter
        if is_dark_theme != self.theme_manager.is_dark:
            self.theme_manager.is_dark = is_dark_theme
        self.is_dark_theme = is_dark_theme
        self.setup_ui()
        # Connect theme changes
        self.theme_manager.themeChanged.connect(self.update_styles)
        self.theme_manager.themeChanged.connect(self.propagate_theme)
        self.update_styles()
        # Maintain compatibility with original class behavior
        # Auto-open PDF if needed (comment out if not desired)
        # self.open_pdf_manual()
    def setup_ui(self):
        """Setup the main UI with tabs for different help sections"""
        self.vlayout = QVBoxLayout()
        self.vlayout.setContentsMargins(0, 0, 0, 0)
        self.vlayout.setSpacing(0)
        # Create tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setObjectName("tab_widget")
        self.tab_widget.setIconSize(QSize(20, 20))
        # Tab 1: FAQ
        self.help_widget = FosseHelpWidget()
        faq_icon = self.style().standardIcon(QStyle.SP_MessageBoxQuestion)
        self.tab_widget.addTab(self.help_widget, faq_icon, "FAQ")
        # Tab 2: HTML Manual (PDFManualWidget, but pass theme)
        self.manual_widget = PDFManualWidget(is_dark_theme=self.theme_manager.is_dark)
        manual_icon = self.style().standardIcon(QStyle.SP_FileIcon)
        self.tab_widget.addTab(self.manual_widget, manual_icon, "User Manual (PDF)")
        # Tab 3: Support Chat
        self.chat_widget = ChatBotWidget()
        chat_icon = self.style().standardIcon(QStyle.SP_MessageBoxInformation)
        self.tab_widget.addTab(self.chat_widget, chat_icon, "Support Chat")
        self.vlayout.addWidget(self.tab_widget)
        self.setLayout(self.vlayout)
    def update_styles(self, is_dark=None):
        """Update widget styles based on current theme"""
        colors = self.theme_manager.colors()
        
        # Base style for the widget
        self.setStyleSheet(f"""
            UserManual {{
                background-color: {colors['background']};
                color: {colors['text']['primary']};
                border: none;
            }}
            #tab_widget::pane {{
                border: 1px solid {colors['divider']};
                border-radius: 8px;
                margin: 0px;
                padding: 0px;
                background: {colors['surface']};
            }}
            QTabBar::tab {{
                background: {colors['elevation']['dp2']};
                color: {colors['text']['secondary']};
                border: 1px solid {colors['divider']};
                border-bottom: none;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                min-width: 100px;
                padding: 8px 16px;
                margin-right: 2px;
            }}
            QTabBar::tab:selected {{
                background: {colors['surface']};
                color: {colors['primary']};
                border-bottom: 2px solid {colors['primary']};
                margin-bottom: -1px;
                font-weight: 500;
            }}
            QTabBar::tab:!selected {{
                margin-top: 2px;
                border-bottom: 1px solid {colors['divider']};
            }}
            QTabBar::tab:hover:!selected {{
                background: {colors['elevation']['dp4']};
            }}
            QScrollArea, QScrollBar:vertical, QScrollBar:horizontal {{
                border: none;
                background: transparent;
            }}
            QScrollBar:vertical {{
                width: 10px;
                margin: 0px 0px 0px 0px;
            }}
            QScrollBar::handle:vertical {{
                background: {colors['elevation']['dp8']};
                min-height: 20px;
                border-radius: 5px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {colors['elevation']['dp12']};
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            QScrollBar:horizontal {{
                height: 10px;
                margin: 0px 0px 0px 0px;
            }}
            QScrollBar::handle:horizontal {{
                background: {colors['elevation']['dp8']};
                min-width: 20px;
                border-radius: 5px;
            }}
            QScrollBar::handle:horizontal:hover {{
                background: {colors['elevation']['dp12']};
            }}
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                width: 0px;
            }}
        """)
        
    def propagate_theme(self, is_dark):
        # Propagate theme to PDFManualWidget (and thus HTMLUserManual)
        if hasattr(self, 'manual_widget') and self.manual_widget is not None:
            self.manual_widget.set_theme(is_dark)
        
    def open_pdf_manual(self):
        """Original PDF opening functionality"""
        manual = 'library/browser/User-Manual/eSim_Manual_2.4.pdf'
        
        try:
            if os.name == 'nt':
                os.startfile(os.path.realpath(manual))
            else:
                manual_path = '../../' + manual
                subprocess.Popen(
                    ['xdg-open', os.path.realpath(manual_path)], shell=False
                )
        except Exception as e:
            print(f"Error opening PDF manual: {str(e)}")

class HelpSectionGUI(QMainWindow):
    """Standalone Help section GUI for testing"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("eSIM Help Center")
        self.setGeometry(100, 100, 700, 600)
        
        # Set application style to match eSIM app
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
            }
        """)
        
        # Use the enhanced UserManual widget as central widget
        user_manual = UserManual()
        self.setCentralWidget(user_manual)

def main():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show the standalone window for testing
    window = HelpSectionGUI()
    window.show()
    
    sys.exit(app.exec_())

# Integration instructions:
# 1. Replace your existing UserManual class with this enhanced version
# 2. It maintains the same interface: UserManual() creates the widget
# 3. The widget now includes both FAQ/Chat and PDF manual functionality
# 4. You can still call open_pdf_manual() method directly if needed

if __name__ == '__main__':
    main()