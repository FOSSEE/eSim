from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPalette, QColor
import os
import re

class HTMLUserManual(QtWidgets.QWidget):
    """
    This class displays the user manual in a widget with proper theme switching.
    """

    def __init__(self, is_dark_theme=False):
        super().__init__()
        self.is_dark_theme = is_dark_theme
        self.original_html_content = None
        self.vlayout = QtWidgets.QVBoxLayout()
        self.browser = QtWidgets.QTextBrowser()
        self.vlayout.addWidget(self.browser)
        self.setLayout(self.vlayout)
        
        # Set margins for a more professional look
        self.vlayout.setContentsMargins(0, 0, 0, 0)
        
        self.load_original_html()
        self.set_manual_html()
        self.show()

    def load_original_html(self):
        """Load the original HTML content once and store it."""
        path_from_script = os.path.join(os.path.dirname(__file__), '..', '..', 'library', 'browser', 'User-Manual', 'eSim.html')
        try:
            with open(path_from_script, 'r', encoding='utf-8') as f:
                self.original_html_content = f.read()
            # Set search paths for images
            self.browser.setSearchPaths([os.path.dirname(path_from_script)])
        except FileNotFoundError:
            self.original_html_content = f"<html><body><h1>Error: User manual file not found</h1><p>Path: {os.path.realpath(path_from_script)}</p></body></html>"

    def get_base_styles(self):
        """Get the base styles that work for both themes."""
        return '''
        <style type="text/css" id="esim-base-styles">
            * {
                box-sizing: border-box;
                -webkit-font-smoothing: antialiased;
                -moz-osx-font-smoothing: grayscale;
            }
            
            html {
                scroll-behavior: smooth;
            }
            
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Inter', 'SF Pro Display', 'Roboto', system-ui, Arial, sans-serif;
                font-size: 16px;
                line-height: 1.7;
                margin: 0;
                padding: 32px 24px;
                font-weight: 400;
                letter-spacing: -0.01em;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                min-height: 100vh;
                position: relative;
            }
            
            body::before {
                content: '';
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                z-index: -1;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            }
            
            .center, .chapterHead, .likechapterHead, .sectionHead, .subsectionHead {
                text-align: center;
            }
            
            h1, h2, h3, h4, h5, h6, .chapterHead, .likechapterHead {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Inter', 'SF Pro Display', 'Roboto', system-ui, Arial, sans-serif;
                font-weight: 700;
                margin-top: 3em;
                margin-bottom: 1em;
                line-height: 1.25;
                letter-spacing: -0.025em;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            }
            
            h1:first-child, .chapterHead:first-child {
                margin-top: 0;
            }
            
            h1, .chapterHead { 
                font-size: 2.5em;
                font-weight: 800;
                margin-bottom: 1.2em;
            }
            
            h2, .likechapterHead { 
                font-size: 2em;
                font-weight: 700;
                margin-bottom: 1em;
            }
            
            h3, .sectionHead { 
                font-size: 1.5em;
                font-weight: 600;
            }
            
            h4, .subsectionHead { 
                font-size: 1.25em;
                font-weight: 600;
            }
            
            .tableofcontents {
                border-radius: 16px;
                padding: 36px 40px;
                margin: 48px auto;
                max-width: 800px;
                font-size: 1.05em;
                backdrop-filter: blur(20px) saturate(180%);
                border: 1px solid;
                position: relative;
                overflow: hidden;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            }
            
            .tableofcontents::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                z-index: -1;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            }
            
            .tableofcontents:hover {
                transform: translateY(-2px);
            }
            
            .chapterToc, .sectionToc, .subsectionToc {
                display: block;
                margin: 0.6em 0;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                border-radius: 8px;
                padding: 4px 8px;
            }
            
            .chapterToc { 
                font-size: 1.2em; 
                font-weight: 700;
                margin-left: 0; 
                margin-top: 1em;
                margin-bottom: 0.8em;
                padding: 8px 12px;
            }
            
            .sectionToc { 
                font-size: 1.05em; 
                font-weight: 600;
                margin-left: 1.8em;
                padding: 6px 10px;
            }
            
            .subsectionToc { 
                font-size: 0.95em; 
                font-weight: 500;
                margin-left: 3.5em;
                opacity: 0.85;
                padding: 4px 8px;
            }
            
            .tableofcontents span, .tableofcontents a {
                text-decoration: none;
                font-weight: inherit;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            }
            
            .chapterToc:hover, .sectionToc:hover, .subsectionToc:hover {
                transform: translateX(8px);
            }
            
            .tableofcontents a:hover {
                text-decoration: none;
            }
            
            img {
                max-width: 100%;
                height: auto;
                border-radius: 12px;
                margin: 20px 0;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                border: 1px solid;
            }
            
            img:hover {
                transform: scale(1.02);
            }
            
            p, .cmr-10, .cmtt-10x-x-109 {
                margin: 1em 0;
                line-height: 1.7;
            }
            
            .card {
                border-radius: 16px;
                padding: 36px 40px;
                margin: 48px auto;
                max-width: 960px;
                backdrop-filter: blur(20px) saturate(180%);
                border: 1px solid;
                position: relative;
                overflow: hidden;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            }
            
            .card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                z-index: -1;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            }
            
            .card:hover {
                transform: translateY(-2px);
            }
            
            a, a:link, a:visited {
                text-decoration: none;
                font-weight: 500;
                border-radius: 4px;
                padding: 2px 4px;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                position: relative;
            }
            
            a:hover, a:active {
                text-decoration: none;
                transform: translateY(-1px);
            }
            
            /* Code and technical elements */
            code, .cmtt-10x-x-109 {
                font-family: 'SF Mono', 'Monaco', 'Cascadia Code', 'Roboto Mono', 'Consolas', 'Courier New', monospace;
                font-size: 0.88em;
                padding: 4px 8px;
                border-radius: 6px;
                font-weight: 600;
                border: 1px solid;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            }
            
            code:hover, .cmtt-10x-x-109:hover {
                transform: scale(1.02);
            }
            
            /* Scrollbar styling */
            ::-webkit-scrollbar {
                width: 8px;
            }
            
            ::-webkit-scrollbar-track {
                border-radius: 10px;
            }
            
            ::-webkit-scrollbar-thumb {
                border-radius: 10px;
                transition: all 0.3s ease;
            }
            
            ::-webkit-scrollbar-thumb:hover {
                width: 12px;
            }
            
            /* Responsive design */
            @media (max-width: 768px) {
                body { 
                    padding: 20px 16px;
                    font-size: 15px;
                }
                
                .tableofcontents, .card { 
                    padding: 24px 20px; 
                    margin: 24px auto;
                    border-radius: 12px;
                }
                
                h1, .chapterHead { font-size: 2.2em; }
                h2, .likechapterHead { font-size: 1.8em; }
                h3, .sectionHead { font-size: 1.4em; }
                
                .chapterToc { font-size: 1.1em; }
                .sectionToc { margin-left: 1.2em; }
                .subsectionToc { margin-left: 2.4em; }
            }
        </style>
        '''

    def get_light_theme_styles(self):
        """Get styles specific to light theme."""
        return '''
        <style type="text/css" id="esim-light-theme">
            body {
                background: linear-gradient(135deg, #ffffff 0%, #f8fafc 50%, #f1f5f9 100%);
                color: #1a202c;
            }
            
            body::before {
                background: 
                    radial-gradient(circle at 20% 20%, rgba(59, 130, 246, 0.1) 0%, transparent 50%),
                    radial-gradient(circle at 80% 80%, rgba(147, 51, 234, 0.1) 0%, transparent 50%);
            }
            
            .tableofcontents, .card {
                background: rgba(255, 255, 255, 0.95) !important;
                border-color: rgba(226, 232, 240, 0.8) !important;
                box-shadow: 
                    0 20px 40px rgba(0, 0, 0, 0.08),
                    0 8px 16px rgba(0, 0, 0, 0.04),
                    inset 0 1px 0 rgba(255, 255, 255, 0.8) !important;
            }
            
            .tableofcontents::before, .card::before {
                background: linear-gradient(135deg, rgba(255, 255, 255, 0.9), rgba(248, 250, 252, 0.9));
            }
            
            .tableofcontents:hover, .card:hover {
                box-shadow: 
                    0 24px 48px rgba(0, 0, 0, 0.12),
                    0 12px 20px rgba(0, 0, 0, 0.06),
                    inset 0 1px 0 rgba(255, 255, 255, 0.9) !important;
            }
            
            h1, h2, h3, h4, h5, h6, .chapterHead, .likechapterHead {
                color: #1e40af !important;
                text-shadow: 0 1px 2px rgba(30, 64, 175, 0.1);
            }
            
            .tableofcontents span, .tableofcontents a,
            a, a:link, a:visited {
                color: #2563eb !important;
            }
            
            .chapterToc:hover, .sectionToc:hover, .subsectionToc:hover {
                background: rgba(37, 99, 235, 0.08) !important;
                color: #1d4ed8 !important;
            }
            
            a:hover, a:active {
                color: #1d4ed8 !important;
                background: rgba(29, 78, 216, 0.1) !important;
                box-shadow: 0 2px 8px rgba(29, 78, 216, 0.2);
            }
            
            .subsectionToc {
                color: #64748b !important;
            }
            
            code, .cmtt-10x-x-109 {
                background: linear-gradient(135deg, #f8fafc, #f1f5f9) !important;
                color: #7c3aed !important;
                border-color: rgba(226, 232, 240, 0.8) !important;
                box-shadow: 
                    0 1px 3px rgba(0, 0, 0, 0.1),
                    inset 0 1px 0 rgba(255, 255, 255, 0.8);
            }
            
            code:hover, .cmtt-10x-x-109:hover {
                background: linear-gradient(135deg, #f1f5f9, #e2e8f0) !important;
                box-shadow: 
                    0 2px 6px rgba(0, 0, 0, 0.15),
                    inset 0 1px 0 rgba(255, 255, 255, 0.9);
            }
            
            img {
                border-color: rgba(226, 232, 240, 0.6) !important;
                box-shadow: 
                    0 8px 24px rgba(0, 0, 0, 0.1),
                    0 4px 8px rgba(0, 0, 0, 0.05);
            }
            
            img:hover {
                box-shadow: 
                    0 12px 32px rgba(0, 0, 0, 0.15),
                    0 6px 12px rgba(0, 0, 0, 0.08);
            }
            
            ::-webkit-scrollbar-track {
                background: rgba(248, 250, 252, 0.8);
            }
            
            ::-webkit-scrollbar-thumb {
                background: linear-gradient(135deg, #cbd5e1, #94a3b8);
            }
            
            ::-webkit-scrollbar-thumb:hover {
                background: linear-gradient(135deg, #94a3b8, #64748b);
            }
        </style>
        '''

    def get_dark_theme_styles(self):
        """Get styles specific to dark theme."""
        return '''
        <style type="text/css" id="esim-dark-theme">
            body {
                background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
                color: #f1f5f9;
            }
            
            body::before {
                background: 
                    radial-gradient(circle at 20% 20%, rgba(56, 189, 248, 0.15) 0%, transparent 50%),
                    radial-gradient(circle at 80% 80%, rgba(168, 85, 247, 0.15) 0%, transparent 50%),
                    radial-gradient(circle at 50% 50%, rgba(16, 185, 129, 0.08) 0%, transparent 70%);
            }
            
            .tableofcontents, .card {
                background: rgba(15, 23, 42, 0.95) !important;
                border-color: rgba(51, 65, 85, 0.8) !important;
                box-shadow: 
                    0 20px 40px rgba(0, 0, 0, 0.4),
                    0 8px 16px rgba(0, 0, 0, 0.2),
                    inset 0 1px 0 rgba(148, 163, 184, 0.1) !important;
            }
            
            .tableofcontents::before, .card::before {
                background: linear-gradient(135deg, 
                    rgba(15, 23, 42, 0.9), 
                    rgba(30, 41, 59, 0.9),
                    rgba(51, 65, 85, 0.9));
            }
            
            .tableofcontents:hover, .card:hover {
                box-shadow: 
                    0 24px 48px rgba(0, 0, 0, 0.5),
                    0 12px 20px rgba(0, 0, 0, 0.3),
                    inset 0 1px 0 rgba(148, 163, 184, 0.15) !important;
            }
            
            h1, h2, h3, h4, h5, h6, .chapterHead, .likechapterHead {
                color: #38bdf8 !important;
                text-shadow: 
                    0 0 20px rgba(56, 189, 248, 0.3),
                    0 2px 4px rgba(0, 0, 0, 0.5);
            }
            
            .tableofcontents span, .tableofcontents a,
            a, a:link, a:visited {
                color: #60a5fa !important;
            }
            
            .chapterToc:hover, .sectionToc:hover, .subsectionToc:hover {
                background: rgba(56, 189, 248, 0.15) !important;
                color: #38bdf8 !important;
                box-shadow: 0 0 10px rgba(56, 189, 248, 0.3);
            }
            
            a:hover, a:active {
                color: #38bdf8 !important;
                background: rgba(56, 189, 248, 0.15) !important;
                box-shadow: 
                    0 0 10px rgba(56, 189, 248, 0.3),
                    0 2px 8px rgba(56, 189, 248, 0.2);
                text-shadow: 0 0 8px rgba(56, 189, 248, 0.5);
            }
            
            .subsectionToc {
                color: #94a3b8 !important;
            }
            
            code, .cmtt-10x-x-109 {
                background: linear-gradient(135deg, 
                    rgba(51, 65, 85, 0.8), 
                    rgba(71, 85, 105, 0.8)) !important;
                color: #a78bfa !important;
                border-color: rgba(71, 85, 105, 0.8) !important;
                box-shadow: 
                    0 2px 8px rgba(0, 0, 0, 0.3),
                    inset 0 1px 0 rgba(148, 163, 184, 0.1);
            }
            
            code:hover, .cmtt-10x-x-109:hover {
                background: linear-gradient(135deg, 
                    rgba(71, 85, 105, 0.9), 
                    rgba(100, 116, 139, 0.9)) !important;
                box-shadow: 
                    0 4px 12px rgba(0, 0, 0, 0.4),
                    inset 0 1px 0 rgba(148, 163, 184, 0.15),
                    0 0 8px rgba(167, 139, 250, 0.3);
            }
            
            img {
                border-color: rgba(51, 65, 85, 0.8) !important;
                box-shadow: 
                    0 8px 24px rgba(0, 0, 0, 0.4),
                    0 4px 8px rgba(0, 0, 0, 0.2);
            }
            
            img:hover {
                box-shadow: 
                    0 12px 32px rgba(0, 0, 0, 0.5),
                    0 6px 12px rgba(0, 0, 0, 0.3),
                    0 0 20px rgba(56, 189, 248, 0.2);
            }
            
            ::-webkit-scrollbar-track {
                background: rgba(15, 23, 42, 0.8);
            }
            
            ::-webkit-scrollbar-thumb {
                background: linear-gradient(135deg, #475569, #64748b);
            }
            
            ::-webkit-scrollbar-thumb:hover {
                background: linear-gradient(135deg, #64748b, #94a3b8);
            }
        </style>
        '''

    def clean_existing_styles(self, html_content):
        """Remove any existing injected styles more thoroughly."""
        # Remove styles with specific IDs
        html_content = re.sub(r'<style[^>]*id="esim-[^"]*"[^>]*>.*?</style>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove old style comments
        html_content = re.sub(r'<!--oldstyle.*?</style>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove any remaining injected styles (more aggressive cleanup)
        html_content = re.sub(r'<style[^>]*>.*?backdrop-filter.*?</style>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
        
        return html_content

    def set_manual_html(self):
        """Load and set the HTML content with the correct theme and professional styling."""
        if not self.original_html_content:
            self.browser.setText("Error: Could not load user manual content.")
            return

        # Start with the original HTML content
        html_content = self.original_html_content

        # Clean existing styles more thoroughly
        html_content = self.clean_existing_styles(html_content)

        # Prepare the complete stylesheet
        complete_styles = self.get_base_styles()
        
        if self.is_dark_theme:
            complete_styles += self.get_dark_theme_styles()
        else:
            complete_styles += self.get_light_theme_styles()

        # More robust style injection
        if '<head>' in html_content.lower():
            # Find the head tag (case insensitive)
            head_match = re.search(r'<head[^>]*>', html_content, re.IGNORECASE)
            if head_match:
                head_end = head_match.end()
                html_content = html_content[:head_end] + complete_styles + html_content[head_end:]
            else:
                # Fallback: inject before closing head tag
                html_content = re.sub(r'</head>', complete_styles + '</head>', html_content, flags=re.IGNORECASE)
        else:
            # If no head tag exists, create one
            if '<html>' in html_content.lower():
                html_content = re.sub(r'<html[^>]*>', r'\g<0><head>' + complete_styles + '</head>', html_content, flags=re.IGNORECASE)
            else:
                # No html tag either, just prepend styles
                html_content = complete_styles + html_content

        # Set the HTML content with base URL for relative paths
        self.browser.setHtml(html_content)
        self.browser.setOpenExternalLinks(True)

    def set_theme(self, is_dark_theme):
        """Update the theme and reload the HTML content."""
        if self.is_dark_theme != is_dark_theme:
            self.is_dark_theme = is_dark_theme
            self.set_manual_html()
            
            # Force a repaint to ensure styles are applied
            self.browser.repaint()
            QtCore.QCoreApplication.processEvents()

    def refresh_content(self):
        """Refresh the content by reloading from file."""
        self.load_original_html()
        self.set_manual_html()
        
    def apply_theme_immediately(self):
        """Force immediate theme application - useful for testing."""
        self.set_manual_html()
        self.browser.update()
        self.update()