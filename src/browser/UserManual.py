import sys
import csv
import subprocess
import os
import markdown
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QScrollArea, QFrame, QLabel, QPushButton, 
                            QLineEdit, QTextEdit, QSplitter, QMessageBox, QSizePolicy,
                            QTabWidget, QStyle, QToolButton, QTextBrowser)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtSignal, QSize, QThread, QUrl
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon
from browser.main import get_bot_response

class ExpandableQAWidget(QFrame):
   
    
    def __init__(self, question, answer, parent=None):
        super().__init__(parent)
        self.question = question
        self.answer = answer
        self.is_expanded = False
        
        self.setFrameStyle(QFrame.NoFrame)
        self.setLineWidth(0)
        self.setStyleSheet("""
            ExpandableQAWidget {
                background-color: transparent;
                border: none;
                margin: 0px;
                padding: 0px;
            }
        """)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.setup_ui()
        self.setup_animation()
        
    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 12)  # More bottom margin for spacing
        self.layout.setSpacing(0)
        
        # Main container for visuals, to handle border and background
        self.container = QFrame()
        self.container.setObjectName("container")
        self.container.setFrameStyle(QFrame.Box | QFrame.Plain)
        self.container.setLineWidth(1)
        self.container.setStyleSheet("""
            #container {
                background-color: #f9f9f9;
                border: 1.5px solid #d0d0d0;
                border-radius: 10px;
                margin: 0px;
                padding: 0px;
            }
        """)

        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(8, 18, 16, 18)  # Add left/right margin for arrow
        container_layout.setSpacing(8)
        
        # Question section (always visible)
        self.question_widget = QWidget()
        question_layout = QHBoxLayout(self.question_widget)
        question_layout.setContentsMargins(0, 0, 12, 0)  # Add more right margin for arrow
        question_layout.setSpacing(12)
        
        # Question label
        self.question_label = QLabel(self.question)
        self.question_label.setWordWrap(True)
        self.question_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.question_label.setStyleSheet("color: #2c3e50; background-color: transparent; border: none; padding: 8px 0px 8px 0px;")
        self.question_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.question_label.setMinimumWidth(0)
        self.question_label.setMaximumWidth(10000)
        
        # Expand/collapse indicator (modern arrow)
        self.indicator = QLabel()
        self.indicator.setFont(QFont("Arial", 18, QFont.Bold))
        self.indicator.setText("▶")
        self.indicator.setStyleSheet("color: #4a90e2; background-color: transparent; border: none; margin-right: 4px;")
        self.indicator.setFixedWidth(28)
        self.indicator.setFixedHeight(28)
        self.indicator.setAlignment(Qt.AlignCenter)
        
        question_layout.addWidget(self.question_label, 1)
        question_layout.addWidget(self.indicator, 0, Qt.AlignVCenter)
        
        container_layout.addWidget(self.question_widget)
        
        # Answer section (initially hidden and animated)
        self.answer_widget = QWidget()
        self.answer_widget.setVisible(False)
        self.answer_widget.setStyleSheet("background-color: transparent; border: none;")
        
        answer_layout = QVBoxLayout(self.answer_widget)
        answer_layout.setContentsMargins(0, 10, 0, 0)
        answer_layout.setSpacing(8)
        
        # Separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("background-color: #e0e0e0;")
        separator.setFixedHeight(1)
        answer_layout.addWidget(separator)
        
        # Answer label
        self.answer_label = QLabel(self.answer)
        self.answer_label.setWordWrap(True)
        self.answer_label.setFont(QFont("Segoe UI", 10))
        self.answer_label.setStyleSheet("color: #34495e; padding: 6px 0px 6px 0px; line-height: 1.6; background-color: transparent; border: none;")
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
        self.container.setStyleSheet(self.container.styleSheet() + "\n#container { border-color: #357abd; }")
        super().enterEvent(event)
    def leaveEvent(self, event):
        self.container.setStyleSheet("""
            #container {
                background-color: #f9f9f9;
                border: 1.5px solid #d0d0d0;
                border-radius: 10px;
                margin: 0px;
                padding: 0px;
            }
        """)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.toggle_expansion()
        super().mousePressEvent(event)
        
    def toggle_expansion(self):
        self.is_expanded = not self.is_expanded
        start_height = self.answer_widget.maximumHeight()
        if self.is_expanded:
            self.indicator.setText("▼")
            self.container.setStyleSheet(self.container.styleSheet() + "\n#container { background-color: #f3f7fa; border-color: #4a90e2; }")
            self.answer_widget.setVisible(True)
            end_height = self.answer_widget.sizeHint().height()
        else:
            self.indicator.setText("▶")
            self.container.setStyleSheet("""
                #container {
                    background-color: #f9f9f9;
                    border: 1.5px solid #d0d0d0;
                    border-radius: 10px;
                    margin: 0px;
                    padding: 0px;
                }
            """)
            end_height = 0
        self.animation.setStartValue(start_height)
        self.animation.setEndValue(end_height)
        self.animation.start()

class BotWorker(QThread):
    finished = pyqtSignal(str)
    def __init__(self, prompt, parent=None):
        super().__init__(parent)
        self.prompt = prompt
    def run(self):
        try:
            response = get_bot_response(self.prompt)
        except Exception as e:
            response = "I apologize, but I encountered an error while processing your request. Please try again."
        self.finished.emit(response)

class ChatBotWidget(QWidget):
    """Simple chatbot interface widget with eSIM app theme, now with async/markdown/timestamp features and backend integration"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.show_welcome_message()
        self.typing_label = None
        self.worker = None
        self.thread = None
        self.typing_message = None

    def setup_ui(self):
        self.setStyleSheet("background-color: #f8f9fa;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        # Chat header
        header = QLabel("💬 Support Chat")
        header.setFont(QFont("Segoe UI", 10, QFont.Bold))
        header.setStyleSheet("""
            color: #2c3e50; 
            padding: 8px; 
            background-color: #ecf0f1; 
            border: 1px solid #bdc3c7;
            border-radius: 4px;
            border-bottom-left-radius: 0px;
            border-bottom-right-radius: 0px;
        """)
        layout.addWidget(header)
        # Chat display area
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setFont(QFont("Segoe UI", 9))
        self.chat_display.setStyleSheet("""
            QTextEdit {
                border: 1px solid #bdc3c7;
                border-top: none;
                border-radius: 0px;
                padding: 8px;
                background-color: #ffffff;
            }
        """)
        layout.addWidget(self.chat_display)
        # Input area
        input_layout = QHBoxLayout()
        input_layout.setSpacing(5)
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Type your message here...")
        self.message_input.setFont(QFont("Segoe UI", 9))
        self.message_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                padding: 8px;
            }
            QLineEdit:focus {
                border-color: #4a90e2;
            }
        """)
        self.message_input.returnPressed.connect(self.send_message)
        self.send_button = QPushButton("Send")
        self.send_button.setFont(QFont("Segoe UI", 9, QFont.Bold))
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
            QPushButton:pressed {
                background-color: #2968a3;
            }
        """)
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.message_input)
        input_layout.addWidget(self.send_button)
        layout.addLayout(input_layout)
        layout.setStretchFactor(self.chat_display, 1)

    def show_welcome_message(self):
        welcome_text = ("<b>👋 Welcome to the eSIM Assistant!</b><br><br>"
                        "I'm here to help you with all your eSIM-related questions and tasks. "
                        "Whether you're activating, troubleshooting, or just curious—I've got you covered!")
        self.append_bot_message(welcome_text, is_welcome=True)

    def send_message(self):
        text = self.message_input.text().strip()
        if not text:
            return
        self.send_button.setEnabled(False)
        self.message_input.setEnabled(False)
        self.append_user_message(text)
        self.message_input.clear()
        self.show_typing_indicator()
        # Start worker thread for bot response
        self.worker = BotWorker(text)
        self.worker.finished.connect(self.on_bot_response)
        self.worker.start()

    def show_typing_indicator(self):
        # Remove any existing typing indicator before adding a new one
        self.remove_typing_indicator()
        if self.typing_message is None:
            # Use a unique HTML id for the typing indicator
            self.typing_message = QLabel('<span id="esim-typing-indicator"><i>eSIM Support is typing...</i></span>')
            self.typing_message.setStyleSheet("color: #4a90e2; font-style: italic; font-size: 15px; padding: 8px 0px 8px 0px;")
            self.chat_display.append("")
            self.chat_display.insertHtml(self.typing_message.text())
            self.chat_display.append("")
        self.scroll_to_bottom()

    def remove_typing_indicator(self):
        # Remove the typing message from the chat area using the unique HTML id
        if self.typing_message is not None:
            html = self.chat_display.toHtml()
            html = html.replace('<span id="esim-typing-indicator"><i>eSIM Support is typing...</i></span>', "")
            html = html.replace('<span id=\"esim-typing-indicator\"><i>eSIM Support is typing...</i></span>', "")
            self.chat_display.setHtml(html)
            self.typing_message = None

    def on_bot_response(self, response):
        self.remove_typing_indicator()
        if response.strip().lower().startswith('error:'):
            # Show error in red
            html = f'<span style="color:#e74c3c;"><b>Error:</b> {response[6:].strip()}</span>'
            self.append_bot_message(html)
        else:
            html = markdown.markdown(response)
            self.append_bot_message(html)
        self.send_button.setEnabled(True)
        self.message_input.setEnabled(True)
        self.message_input.setFocus()

    def append_user_message(self, text):
        timestamp = self.get_timestamp()
        html = f'<div style="text-align:right;"><b style="color:#2c3e50;">You:</b> {text}<br><span style="color:#888;font-size:11px;">{timestamp}</span></div>'
        self.chat_display.append(html)
        self.scroll_to_bottom()

    def append_bot_message(self, text, is_welcome=False):
        timestamp = self.get_timestamp()
        if not is_welcome:
            html = f'<div style="text-align:left;"><b style="color:#4a90e2;">eSIM Support:</b> {text}<br><span style="color:#888;font-size:11px;">{timestamp}</span></div>'
        else:
            html = f'<div style="text-align:left;">{text}</div>'
        self.chat_display.append(html)
        self.scroll_to_bottom()

    def scroll_to_bottom(self):
        scrollbar = self.chat_display.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def get_timestamp(self):
        from datetime import datetime
        return datetime.now().strftime("%H:%M")

class PDFManualWidget(QWidget):
    """Widget to display the eSim.html manual only"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Add maximize button
        maximize_btn = QPushButton("Open in New Window")
        maximize_btn.setFixedWidth(160)
        maximize_btn.clicked.connect(self.open_in_new_window)
        layout.addWidget(maximize_btn, alignment=Qt.AlignRight)

        # Manual Viewer ONLY
        self.manual_viewer = QTextBrowser()
        manual_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '../../library/browser/User-Manual/eSim.html')
        )
        if os.path.exists(manual_path):
            self.manual_viewer.setSource(QUrl.fromLocalFile(manual_path))
        else:
            self.manual_viewer.setHtml("<h2>eSim.html file not found.</h2>")
        self.manual_viewer.setOpenExternalLinks(True)
        layout.addWidget(self.manual_viewer, stretch=1)

    def open_in_new_window(self):
        self.new_window = QMainWindow(self)
        self.new_window.setWindowTitle("eSim User Manual")
        viewer = QTextBrowser()
        manual_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '../../library/browser/User-Manual/eSim.html')
        )
        if os.path.exists(manual_path):
            viewer.setSource(QUrl.fromLocalFile(manual_path))
        else:
            viewer.setHtml("<h2>eSim.html file not found.</h2>")
        viewer.setOpenExternalLinks(True)
        self.new_window.setCentralWidget(viewer)
        self.new_window.resize(900, 700)
        self.new_window.show()

class FosseHelpWidget(QWidget):
    """Main Help widget with FAQ section (FAQ search bar small and in header row, no icon)"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.qa_data = []
        self.setup_ui()
        self.load_faq_from_csv()
        
    def setup_ui(self):
        # Set widget background to match eSIM app theme
        self.setStyleSheet("""
            FosseHelpWidget {
                background-color: #f8f9fa;
            }
        """)
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        # FAQ Section
        faq_widget = self.create_faq_section()
        main_layout.addWidget(faq_widget)
        main_layout.addStretch()
    def create_faq_section(self):
        """Create the FAQ section with scrollable Q&A widgets (search bar in header, small, no icon)"""
        faq_widget = QWidget()
        faq_layout = QVBoxLayout(faq_widget)
        faq_layout.setContentsMargins(0, 0, 0, 0)
        faq_layout.setSpacing(0)
        # FAQ Header Row (label + small search bar at end)
        header_row = QHBoxLayout()
        header_row.setContentsMargins(24, 24, 24, 0)
        header_row.setSpacing(8)
        faq_header = QLabel("\ud83d\udccb Frequently Asked Questions")
        faq_header.setFont(QFont("Segoe UI", 16, QFont.Bold))
        faq_header.setStyleSheet("color: #2c3e50;")
        header_row.addWidget(faq_header)
        header_row.addStretch()
        # Small search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search FAQs...")
        self.search_bar.setFont(QFont("Segoe UI", 9))
        self.search_bar.setFixedWidth(160)
        self.search_bar.setFixedHeight(26)
        self.search_bar.setStyleSheet("""
            QLineEdit {
                border: 1.2px solid #e6e6e6;
                border-radius: 13px;
                padding: 2px 10px;
                background-color: #ffffff;
                font-size: 13px;
            }
            QLineEdit:focus {
                border-color: #4a90e2;
                background-color: #f8faff;
            }
        """)
        self.search_bar.textChanged.connect(self.filter_faqs)
        header_row.addWidget(self.search_bar, 0, Qt.AlignVCenter)
        faq_layout.addLayout(header_row)
        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setStyleSheet("background-color: #e6e6e6;")
        divider.setFixedHeight(2)
        faq_layout.addWidget(divider)
        # Scroll area for Q&A widgets
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #e0e0e0;
                width: 10px;
                margin: 0px 0px 0px 0px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #bdc3c7;
                min-height: 25px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: #95a5a6;
            }
            QScrollBar::handle:vertical:pressed {
                background: none;
            }
        """)
        # Container widget for Q&A items
        self.qa_container = QWidget()
        self.qa_container.setStyleSheet("background-color: transparent;")
        self.qa_layout = QVBoxLayout(self.qa_container)
        self.qa_layout.setSpacing(0)
        self.qa_layout.setContentsMargins(24, 0, 24, 24)
        self.qa_layout.addStretch()  # Add stretch to push items to top
        self.scroll_area.setWidget(self.qa_container)
        faq_layout.addWidget(self.scroll_area)
        return faq_widget
        
    def load_faq_from_csv(self):
        """Automatically load FAQ data from CSV file"""
        csv_filename = "resources/esim_faq_new.csv"
        
        try:
            with open(csv_filename, 'r', encoding='utf-8', newline='') as csvfile:
                # Use csv.Sniffer to detect delimiter
                sample = csvfile.read(1024)
                csvfile.seek(0)
                
                sniffer = csv.Sniffer()
                try:
                    delimiter = sniffer.sniff(sample).delimiter
                except:
                    delimiter = ','  # Default to comma
                
                reader = csv.reader(csvfile, delimiter=delimiter)
                
                # Skip header row if it exists
                first_row = next(reader, None)
                if first_row and (first_row[0].lower() in ['question', 'q'] or 'question' in first_row[0].lower()):
                    pass  # Skip header
                else:
                    # First row is data, add it back
                    if first_row and len(first_row) >= 2:
                        self.qa_data.append((first_row[0], first_row[1]))
                
                # Read the rest of the data
                for row in reader:
                    if len(row) >= 2 and row[0].strip() and row[1].strip():
                        self.qa_data.append((row[0].strip(), row[1].strip()))
            
            if self.qa_data:
                self.populate_qa_widgets()
            else:
                self.load_default_esim_faq()
                
        except FileNotFoundError:
            print(f"CSV file '{csv_filename}' not found. Loading default eSIM FAQ data.")
            self.load_default_esim_faq()
        except Exception as e:
            print(f"Error loading CSV file: {str(e)}. Loading default eSIM FAQ data.")
            self.load_default_esim_faq()
    
    def load_default_esim_faq(self):
        """Load default eSIM FAQ data"""
        esim_faq_data = []
        
        self.qa_data = esim_faq_data
        self.populate_qa_widgets()
        
    def populate_qa_widgets(self):
        """Create and add Q&A widgets to the scroll area"""
        # Clear existing widgets except the stretch
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
        # The last item is a spacer/stretch, so we iterate up to count - 1
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
    Enhanced User Manual class that combines the original PDF opening functionality
    with the comprehensive help GUI system
    """
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
        # Maintain compatibility with original class behavior
        # Auto-open PDF if needed (comment out if not desired)
        # self.open_pdf_manual()
    
    def setup_ui(self):
        """Setup the main UI with tabs for different help sections"""
        self.vlayout = QVBoxLayout()
        self.vlayout.setContentsMargins(0, 0, 0, 0)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setIconSize(QSize(20, 20))
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border-top: 1px solid #bdc3c7;
                background-color: #f8f9fa;
            }
        """)
        
        # Tab 1: FAQ
        help_widget = FosseHelpWidget()
        faq_icon = self.style().standardIcon(QStyle.SP_MessageBoxQuestion)
        self.tab_widget.addTab(help_widget, faq_icon, "FAQ")
        
        # Tab 2: PDF Manual
        pdf_widget = PDFManualWidget()
        pdf_icon = self.style().standardIcon(QStyle.SP_FileIcon)
        self.tab_widget.addTab(pdf_widget, pdf_icon, "User Manual (PDF)")
        
        # Tab 3: Support Chat
        chat_widget = ChatBotWidget()
        chat_icon = self.style().standardIcon(QStyle.SP_MessageBoxInformation)
        self.tab_widget.addTab(chat_widget, chat_icon, "Support Chat")

        self.vlayout.addWidget(self.tab_widget)
        self.setLayout(self.vlayout)
        
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
