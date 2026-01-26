from PyQt5 import QtCore, QtWidgets, QtGui
import os


class Welcome(QtWidgets.QWidget):
    """
    This class contains content of dock area part of initial esim Window.
    It creates Welcome page of eSim.
    """

    def __init__(self, is_dark_theme=False):
        QtWidgets.QWidget.__init__(self)
        self.vlayout = QtWidgets.QVBoxLayout()
        self.browser = QtWidgets.QTextBrowser()
        self.current_zoom = 100  # Default zoom level
        self.base_font_size = 14  # Base font size in pixels
        self.is_dark_theme = is_dark_theme

        init_path = '../../'
        if os.name == 'nt':
            init_path = ''

        # Set base font size and family
        font = QtGui.QFont("Fira Sans", self.base_font_size)
        self.browser.setFont(font)
        
        # Load and scale the content
        self.html_path = init_path + "library/browser/welcome.html"
        self.load_and_scale_content()
        
        self.browser.setOpenExternalLinks(True)
        self.browser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        
        # Apply initial styling
        self.browser.setStyleSheet("""
            QTextBrowser {
                background: transparent;
                border: none;
                padding: 16px;
            }
        """)
        
        self.vlayout.addWidget(self.browser)
        self.setLayout(self.vlayout)
        self.show()
    
    def load_and_scale_content(self):
        """Load and scale the HTML content"""
        try:
            with open(self.html_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # Force styles for dark theme to ensure readability
            if self.is_dark_theme:
                dark_style = """
                <style type="text/css">
                    body {
                        background-color: #23273a !important;
                        color: #e8eaed !important;
                    }
                    h1 {
                        color: #40c4ff !important;
                    }
                    p, span {
                        color: #e8eaed !important;
                    }
                    a, a:link, a:visited, a:hover, a:active {
                        color: #40c4ff !important;
                    }
                    .highlight {
                        color: #40c4ff !important;
                    }
                </style>
                """
                content = content.replace('</head>', dark_style + '</head>')
            else:
                # Ensure light theme is properly applied if not dark
                content = content.replace('<body>', '<body class="light-theme">')

            # Calculate the scaled font size
            scaled_size = int(self.base_font_size * (self.current_zoom / 100.0))
            
            # Insert dynamic font size into the HTML
            content = content.replace('</head>',
                f'''
                <style>
                    body {{
                        font-size: {scaled_size}px !important;
                    }}
                    h1 {{
                        font-size: {scaled_size * 1.5}px !important;
                    }}
                    p {{
                        font-size: {scaled_size * 1.1}px !important;
                    }}
                    a, .highlight {{
                        font-size: inherit !important;
                    }}
                </style>
                </head>
                ''')
            
            self.browser.setHtml(content)
            
        except Exception as e:
            print(f"Error loading welcome content: {str(e)}")
    
    def increase_font_size(self):
        """Increase the font size of the welcome page"""
        if self.current_zoom < 200:  # Max 200% zoom
            self.current_zoom += 10
            self.load_and_scale_content()
    
    def decrease_font_size(self):
        """Decrease the font size of the welcome page"""
        if self.current_zoom > 50:  # Min 50% zoom
            self.current_zoom -= 10
            self.load_and_scale_content()
    
    def reset_font_size(self):
        """Reset the font size to default"""
        self.current_zoom = 100
        self.load_and_scale_content()
