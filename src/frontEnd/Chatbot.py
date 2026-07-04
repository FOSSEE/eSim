import os
import sys

# Import pathmagic first to ensure 'src' is in sys.path before any local imports
try:
    import pathmagic  # noqa:F401
except ImportError:
    try:
        from frontEnd import pathmagic  # noqa:F401
    except ImportError:
        # Fallback: manually add the src directory relative to this file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        src_dir = os.path.abspath(os.path.join(current_dir, '..'))
        if src_dir not in sys.path:
            sys.path.insert(0, src_dir)

if os.name == 'nt':
    init_path = ''
else:
    init_path = '../../'

from chatbot.chatbot_thread import (  # type: ignore
    OllamaWorker, OllamaVisionWorker, MicWorker,
    OllamaStatusWorker, ModelFetchWorker,
    detect_topic_switch, get_stt_backend,
    is_ollama_running,
    VISION_MODEL_KEYWORDS,  # EXTRACTED: shared constant, avoids duplicate keyword list
)
from chatbot.netlist_analysis import parse_spice_netlist, build_netlist_summary_prompt, NETLIST_SYSTEM_PROMPT
from chatbot.error_log_analysis import (
    build_error_analysis_prompt, ERROR_ANALYSIS_SYSTEM_PROMPT
)
from chatbot.offline_formatter import (
    format_error_analysis_offline,
    format_netlist_analysis_offline,
)
from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QTextBrowser, QVBoxLayout,
    QLineEdit, QPushButton, QLabel, QComboBox, QApplication,
    QFileDialog, QDialog, QListWidget, QListWidgetItem, QFrame,
    QScrollArea, QSlider, QInputDialog
)
from PyQt5.QtCore import QTimer, Qt, pyqtSignal, QSize
from PyQt5.QtGui import QTextCursor, QKeyEvent, QDragEnterEvent, QDropEvent
from configuration.Appconfig import Appconfig
from datetime import datetime
import re
import json
import uuid
import base64

# ── Storage paths ─────────────────────────────────────────────────────────────
_ESIM_DIR = os.path.join(os.path.expanduser('~'), '.esim')
_HISTORY_FILE = os.path.join(_ESIM_DIR, 'chatbot_history.json')
_SESSIONS_DIR = os.path.join(_ESIM_DIR, 'chat_sessions')

_IMG_FILTER = "Images (*.png *.jpg *.jpeg *.bmp *.gif *.tiff)"
_IMAGE_EXTS = {'.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.tif', '.webp'}

_MAX_ERROR_LOG_LINES = 60
_SAVE_DEBOUNCE_MS = 5000

WELCOME_MESSAGE = """
<div style="margin:16px 10px 8px 10px; text-align:center;">
    <div style="font-size:32px; margin-bottom:8px;">🤖</div>
    <div style="font-size:16px; font-weight:bold; color:#1a1a2e; margin-bottom:6px;">
        eSim AI Assistant
    </div>
    <div style="font-size:12px; color:#777; line-height:1.7; margin-bottom:16px;">
        Ask me anything about KiCad, NgSpice,<br>
        netlists, simulation errors, or circuit design.<br>
        Attach an image 📎 or speak 🎤 your question.
    </div>
    <div style="
        display:inline-block;
        background:#f5f5f5;
        border-radius:12px;
        padding:10px 18px;
        font-size:11px;
        color:#999;
        margin:0 auto;
    ">
        Use the sidebar to access past chats
    </div>
</div>
<br>
"""

_TYPING_FRAMES = [
    '&#x25CF;&nbsp;<span style="color:#ccc;">&#x25CF;</span>&nbsp;<span style="color:#ccc;">&#x25CF;</span>',
    '<span style="color:#ccc;">&#x25CF;</span>&nbsp;&#x25CF;&nbsp;<span style="color:#ccc;">&#x25CF;</span>',
    '<span style="color:#ccc;">&#x25CF;</span>&nbsp;<span style="color:#ccc;">&#x25CF;</span>&nbsp;&#x25CF;',
]


def _typing_bubble(frame=0):
    dots = _TYPING_FRAMES[frame % 3]
    return (
        '<table width="100%" cellpadding="0" cellspacing="0"><tr>'
        '<td align="left" style="padding:3px 0 1px 6px;">'
        '<table cellpadding="0" cellspacing="0"><tr>'
        '<td style="padding:0;">'
        '<div style="background-color:#f0f4f8;color:#0078d4;'
        'padding:11px 20px;border-radius:20px 20px 20px 5px;'
        'font-size:18px;line-height:1;border:1px solid #d0dce8;">'
        f'{dots}</div></td></tr></table></td>'
        '<td width="20%"></td></tr></table>'
    )


# ── Markdown renderer ─────────────────────────────────────────────────────────

def _render_inline(text):
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

    def _render_headings(t):
        lines = t.split('\n')
        out = []
        for line in lines:
            m = re.match(r'^(#{1,4})\s+(.*)', line)
            if m:
                level = len(m.group(1))
                sizes = {1: '18px', 2: '16px', 3: '14px', 4: '13px'}
                size = sizes.get(level, '13px')
                content = m.group(2)
                out.append(
                    f'<span style="font-size:{size};font-weight:bold;'
                    f'color:#1a1a2e;">{content}</span>'
                )
            else:
                out.append(line)
        return '\n'.join(out)
    text = _render_headings(text)

    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'__(.*?)__',     r'<b>\1</b>', text)
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    text = re.sub(r'_(.*?)_',   r'<i>\1</i>', text)
    text = re.sub(
        r'`([^`]+)`',
        r'<span style="font-family:Consolas,monospace;background-color:#e8ecf0;'
        r'padding:1px 4px;border-radius:3px;">\1</span>',
        text
    )
    text = re.sub(
        r'\[([^\]]+)\]\((https?://[^\)]+)\)',
        r'<a href="\2" style="color:#0078d4;">\1</a>',
        text
    )
    text = text.replace('\n', '<br>')
    return text


def _render_markdown(text):
    result = []
    pattern = re.compile(r'```(\w*)\n?(.*?)```', re.DOTALL)
    last_end = 0
    for match in pattern.finditer(text):
        before = text[last_end:match.start()]
        if before:
            result.append(_render_inline(before))
        lang = match.group(1) or 'code'
        code = (
            match.group(2)
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('\n', '<br>')
            .replace(' ', '&nbsp;')
        )
        label = f'<span style="color:#888;font-size:10px;">{lang}</span><br>' if lang else ''
        result.append(
            '<table width="98%" cellpadding="0" cellspacing="3"><tr>'
            '<td style="padding:0;">'
            '<div style="background-color:#1e1e1e;color:#d4d4d4;'
            'font-family:Consolas,Courier New,monospace;font-size:12px;'
            'padding:10px 14px;border-radius:10px;border-left:3px solid #0078d4;">'
            f'{label}{code}</div></td></tr></table>'
        )
        last_end = match.end()
    tail = text[last_end:]
    if tail:
        result.append(_render_inline(tail))
    return ''.join(result)


# ── Bubble helpers ────────────────────────────────────────────────────────────

def _get_time():
    return datetime.now().strftime("%H:%M")


def _escape_text_preserve_breaks(text: str) -> str:
    return (
        text.replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('\n', '<br>')
    )


def _image_thumbnail_html(b64_str: str, filename: str) -> str:
    safe_name = filename.replace('&', '&amp;').replace('<', '&lt;')
    return (
        '<table width="100%" cellpadding="0" cellspacing="0"><tr>'
        '<td width="10%"></td>'
        '<td align="right" style="padding:2px 10px 0 0;">'
        '<table cellpadding="0" cellspacing="2"><tr>'
        '<td style="background:#f0f6ff;border-radius:14px 14px 4px 14px;'
        'padding:6px;text-align:center;">'
        f'<img src="data:image/jpeg;base64,{b64_str}" '
        f'style="max-width:160px;max-height:120px;border-radius:8px;" />'
        f'<div style="font-size:9px;color:#888;margin-top:3px;">{safe_name}</div>'
        '</td></tr></table>'
        '</td></tr></table>'
    )


def _user_bubble(text, timestamp):
    safe = _escape_text_preserve_breaks(text)
    b64_text = base64.b64encode(text.encode('utf-8')).decode('utf-8')
    return (
        '<table width="100%" cellpadding="0" cellspacing="0"><tr>'
        '<td width="20%"></td>'
        '<td align="right" style="padding:4px 10px 0 0;">'
        '<table cellpadding="0" cellspacing="2"><tr>'
        '<td valign="bottom" style="padding:0 8px 12px 0;">'
        f'<a href="edit:///{b64_text}" style="text-decoration:none;font-size:12px;color:#b0b0b0;" title="Edit prompt">✏️</a>'
        '</td>'
        '<td style="'
        'background-color:#0095f6;'
        'color:white;'
        'padding:11px 16px;'
        'border-radius:20px 20px 5px 20px;'
        'font-size:13px;'
        'line-height:1.6;'
        '">'
        f'{safe}'
        '</td></tr>'
        f'<tr><td></td><td align="right" style="color:#bbb;font-size:10px;'
        f'padding:3px 2px 8px 0;">You &nbsp;·&nbsp; {timestamp}</td></tr>'
        '</table>'
        '</td></tr></table>'
    )


def _approx_token_count(text: str) -> int:
    return max(1, len(text) // 4)


def _bot_bubble(text, timestamp, response_idx=None):
    """Render a bot response bubble. If response_idx is given, include Retry/Copy links."""
    rendered = _render_markdown(text)

    if response_idx is not None:
        copy_href  = f'copy:///{response_idx}'
        retry_href = f'retry:///{response_idx}'
        token_est = _approx_token_count(text)
        footer = (
            '<tr><td>'
            '<table width="100%" cellpadding="0" cellspacing="0"><tr>'
            f'<td align="left" style="color:#999;font-size:10px;padding:3px 0 8px 2px;">'
            f'eSim AI &nbsp;·&nbsp; {timestamp} &nbsp;·&nbsp; ~{token_est} tokens</td>'
            f'<td align="right" style="padding:3px 4px 8px 0;">'
            f'<a href="{retry_href}" style="color:#e07000;font-size:10px;'
            f'text-decoration:none;">&#8635; Retry</a>'
            f'&nbsp;&nbsp;'
            f'<a href="{copy_href}" style="color:#0095f6;font-size:10px;'
            f'text-decoration:none;">Copy</a></td>'
            '</tr></table>'
            '</td></tr>'
        )
    else:
        footer = (
            f'<tr><td style="color:#999;font-size:10px;padding:3px 0 8px 2px;">'
            f'eSim AI &nbsp;·&nbsp; {timestamp}</td></tr>'
        )

    return (
        '<table width="100%" cellpadding="0" cellspacing="0"><tr>'
        '<td align="left" style="padding:4px 0 0 10px;">'
        '<table cellpadding="0" cellspacing="2"><tr>'
        '<td style="'
        'background-color:#f0f0f0;'
        'color:#1a1a2e;'
        'padding:11px 16px;'
        'border-radius:20px 20px 20px 5px;'
        'font-size:13px;'
        'line-height:1.6;'
        '">'
        f'{rendered}'
        '</td></tr>'
        f'{footer}'
        '</table>'
        '</td>'
        '<td width="20%"></td></tr></table>'
    )


def _system_bubble(text):
    return (
        '<table width="100%" cellpadding="0" cellspacing="0"><tr>'
        '<td align="center" style="padding:4px 8px;">'
        '<div style="background-color:#fff8e1;color:#7a5800;'
        'border:1px solid #ffc107;border-radius:14px;'
        'padding:7px 16px;font-size:11px;font-style:italic;">'
        f'{_escape_text_preserve_breaks(text)}</div></td></tr></table>'
    )


def _staged_images_bubble(filenames, timestamp):
    names_html = "".join(
        f'<span style="background:#e0eeff;color:#0055a5;'
        f'border-radius:8px;padding:2px 8px;margin:2px;font-size:11px;">'
        f'📎 {_escape_text_preserve_breaks(n)}</span> '
        for n in filenames
    )
    return (
        '<table width="100%" cellpadding="0" cellspacing="0"><tr>'
        '<td width="10%"></td>'
        '<td align="right" style="padding:2px 10px 0 0;">'
        '<table cellpadding="0" cellspacing="2"><tr>'
        '<td style="background-color:#f0f6ff;color:#0055a5;'
        'padding:10px 14px;border-radius:18px 18px 4px 18px;'
        'font-size:12px;line-height:1.8;">'
        f'{names_html}'
        '</td></tr>'
        f'<tr><td align="right" style="color:#bbb;font-size:10px;'
        f'padding:3px 2px 8px 0;">You &nbsp;·&nbsp; {timestamp}</td></tr>'
        '</table></td></tr></table>'
    )


def _topic_reset_banner():
    return (
        '<table width="100%" cellpadding="4" cellspacing="0"><tr>'
        '<td align="center" style="color:#aaa;font-size:10px;'
        'border-top:1px dashed #d0dce8;padding-top:6px;">'
        '— New topic —'
        '</td></tr></table>'
    )


def _netlist_header_bubble(filename, timestamp):
    safe = _escape_text_preserve_breaks(filename)
    return (
        '<table width="100%" cellpadding="0" cellspacing="0"><tr>'
        '<td width="5%"></td>'
        '<td align="right" style="padding:2px 6px;">'
        '<table cellpadding="0" cellspacing="0"><tr>'
        '<td style="padding:0;">'
        '<div style="background-color:#fff3e0;color:#b85c00;'
        'padding:6px 14px;border-radius:16px 16px 4px 16px;'
        'font-size:11px;border:1px solid #f0c080;">'
        f'📄 Netlist: {safe}</div>'
        '</td></tr>'
        f'<tr><td align="right" style="color:#aaa;font-size:10px;'
        f'padding:1px 2px 6px 0;">You &nbsp;·&nbsp; {timestamp}</td></tr>'
        '</table></td></tr></table>'
    )


def _parse_custom_url(url):
    scheme = url.scheme()
    host = url.host()
    path = url.path().strip('/')
    parts = []
    if host:
        parts.append(host)
    if path:
        parts.extend([p for p in path.split('/') if p])
    return scheme, parts


def _session_kind_badge(kind: str) -> str:
    colors = {
        "text": ("#eef4ff", "#2d6cdf"),
        "image": ("#eefaf0", "#1f8b4c"),
        "netlist": ("#fff4e8", "#b86a00"),
        "simulation_error": ("#fff0f0", "#c62828"),
    }
    bg, fg = colors.get(kind, ("#f0f0f0", "#666"))
    label = {
        "text": "Text",
        "image": "Image",
        "netlist": "Netlist",
        "simulation_error": "Sim Error",
    }.get(kind, kind.title())
    return (
        f'<span style="background:{bg};color:{fg};'
        f'border-radius:8px;padding:1px 7px;font-size:9px;">{label}</span>'
    )


def _is_image_file(path: str) -> bool:
    return os.path.splitext(path)[1].lower() in _IMAGE_EXTS


# ── Smart input field ─────────────────────────────────────────────────────────

class _HistoryLineEdit(QLineEdit):
    """Input field with command history (↑/↓) and clipboard image paste (Ctrl+V)."""

    image_pasted = pyqtSignal(str)  # emits temp file path of pasted image

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._sent_history = []
        self._hist_idx = -1

    def add_to_history(self, text):
        if text and (not self._sent_history or self._sent_history[-1] != text):
            self._sent_history.append(text)
        self._hist_idx = -1

    def keyPressEvent(self, event: QKeyEvent):
        # ── Ctrl+V: check for clipboard image before default paste ────
        if event.key() == Qt.Key_V and event.modifiers() & Qt.ControlModifier:
            clipboard = QApplication.clipboard()
            mime = clipboard.mimeData()
            if mime and mime.hasImage():
                image = clipboard.image()
                if not image.isNull():
                    import tempfile
                    tmp_dir = os.path.join(
                        os.path.expanduser('~'), '.esim', 'clipboard_images'
                    )
                    os.makedirs(tmp_dir, exist_ok=True)
                    tmp_path = os.path.join(
                        tmp_dir,
                        f"paste_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    )
                    image.save(tmp_path, "PNG")
                    self.image_pasted.emit(tmp_path)
                    return
            # Fall through to default paste for text
            super().keyPressEvent(event)
            return

        if event.key() == Qt.Key_Up and self._sent_history:
            if self._hist_idx == -1:
                self._draft = self.text()
                self._hist_idx = len(self._sent_history) - 1
            elif self._hist_idx > 0:
                self._hist_idx -= 1
            self.setText(self._sent_history[self._hist_idx])
            self.end(False)
        elif event.key() == Qt.Key_Down and self._hist_idx >= 0:
            self._hist_idx += 1
            if self._hist_idx >= len(self._sent_history):
                self._hist_idx = -1
                self.setText(getattr(self, '_draft', ''))
            else:
                self.setText(self._sent_history[self._hist_idx])
            self.end(False)
        else:
            super().keyPressEvent(event)


# ── History viewer ────────────────────────────────────────────────────────────

class ChatHistoryViewer(QDialog):
    def __init__(self, session: dict, parent=None):
        super().__init__(parent)
        raw_title = session.get('title', 'Chat')
        self.setWindowTitle(raw_title[:60])
        self.setMinimumSize(460, 560)
        self.resize(500, 640)
        self.setStyleSheet("QDialog { background:#f9f9f9; }")

        msgs = session.get('messages', [])
        n_usr = sum(1 for m in msgs if m.startswith("User:"))
        n_bot = sum(1 for m in msgs if m.startswith("Bot:"))
        created = session.get('created_at', '')
        updated = session.get('updated_at', '')
        kind = session.get('kind', 'text')

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        top_bar = QWidget()
        top_bar.setFixedHeight(54)
        top_bar.setStyleSheet("""
            QWidget {
                background:#ffffff;
                border-bottom:1px solid #ececec;
            }
        """)
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(16, 0, 12, 0)
        top_layout.setSpacing(10)

        title_lbl = QLabel(raw_title[:50] + ("…" if len(raw_title) > 50 else ""))
        title_lbl.setStyleSheet(
            "font-size:14px; font-weight:700; color:#1a1a2e; background:transparent;"
        )
        top_layout.addWidget(title_lbl, 1)

        meta_lbl = QLabel(f"{n_usr} msg{'s' if n_usr != 1 else ''}  ·  {updated[:10]}  ·  {kind}")
        meta_lbl.setStyleSheet("font-size:10px; color:#aaa; background:transparent;")
        top_layout.addWidget(meta_lbl)

        x_btn = QPushButton("✕")
        x_btn.setFixedSize(26, 26)
        x_btn.setStyleSheet("""
            QPushButton {
                font-size:11px; color:#888;
                background:transparent; border:none; border-radius:13px;
            }
            QPushButton:hover  { background:#f0f0f0; color:#333; }
            QPushButton:pressed{ background:#e0e0e0; }
        """)
        x_btn.clicked.connect(self.accept)
        top_layout.addWidget(x_btn)
        root.addWidget(top_bar)

        browser = QTextBrowser()
        browser.setOpenLinks(False)
        browser.setStyleSheet("""
            QTextBrowser {
                background:#f9f9f9;
                border:none;
                padding:10px 4px;
                font-family:'Segoe UI',Arial,sans-serif;
                font-size:13px;
            }
        """)
        html = ""
        for line in msgs:
            if line.startswith("User:"):
                html += _user_bubble(line[5:].strip(), "")
            elif line.startswith("Bot:"):
                html += _bot_bubble(line[4:].strip(), "")
        browser.setHtml(html if html else "<p style='color:#aaa;text-align:center;padding:20px;'>No messages</p>")
        QTimer.singleShot(120, lambda: browser.verticalScrollBar().setValue(browser.verticalScrollBar().maximum()))
        root.addWidget(browser)

        bot_bar = QWidget()
        bot_bar.setFixedHeight(52)
        bot_bar.setStyleSheet("""
            QWidget {
                background:#ffffff;
                border-top:1px solid #ececec;
            }
        """)
        bot_layout = QHBoxLayout(bot_bar)
        bot_layout.setContentsMargins(16, 0, 16, 0)

        info_lbl = QLabel(f"Created {created[:10]}  ·  {n_usr + n_bot} total messages")
        info_lbl.setStyleSheet("font-size:10px; color:#bbb; background:transparent;")
        bot_layout.addWidget(info_lbl)
        bot_layout.addStretch()

        done_btn = QPushButton("Done")
        done_btn.setFixedHeight(32)
        done_btn.setStyleSheet("""
            QPushButton {
                font-size:12px; font-weight:600;
                padding:4px 22px;
                background:#0095f6; color:white;
                border:none; border-radius:16px;
            }
            QPushButton:hover  { background:#0082d8; }
            QPushButton:pressed{ background:#006ab8; }
        """)
        done_btn.clicked.connect(self.accept)
        bot_layout.addWidget(done_btn)
        root.addWidget(bot_bar)


# ── Sidebar ───────────────────────────────────────────────────────────────────

class _DeleteConfirmDialog(QDialog):
    def __init__(self, title: str, parent=None):
        super().__init__(parent, Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMinimumWidth(320)
        outer = QWidget(self)
        outer.setObjectName("card")
        outer.setStyleSheet("""
            QWidget#card {
                background: #ffffff;
                border-radius: 20px;
                border: 1px solid #e0e0e0;
            }
        """)
        card_layout = QVBoxLayout(outer)
        card_layout.setContentsMargins(28, 24, 28, 20)
        card_layout.setSpacing(14)

        title_lbl = QLabel("Delete chat?")
        title_lbl.setStyleSheet("font-size:16px; font-weight:bold; color:#1a1a2e;")
        title_lbl.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title_lbl)

        body_lbl = QLabel(
            f'<span style="color:#555;font-size:13px;">'
            f'Delete &ldquo;<b>{_escape_text_preserve_breaks(title[:40])}</b>&rdquo;?<br>'
            f'<span style="color:#999;font-size:11px;">This cannot be undone.</span></span>'
        )
        body_lbl.setWordWrap(True)
        body_lbl.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(body_lbl)

        div = QFrame()
        div.setFrameShape(QFrame.HLine)
        div.setStyleSheet("color:#f0f0f0;")
        card_layout.addWidget(div)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedHeight(40)
        cancel_btn.setStyleSheet("""
            QPushButton {
                font-size:13px; font-weight:600;
                background:#f0f0f0; color:#333;
                border:none; border-radius:20px; padding:0 24px;
            }
            QPushButton:hover  { background:#e0e0e0; }
            QPushButton:pressed{ background:#d0d0d0; }
        """)
        cancel_btn.clicked.connect(self.reject)

        delete_btn = QPushButton("Delete")
        delete_btn.setFixedHeight(40)
        delete_btn.setStyleSheet("""
            QPushButton {
                font-size:13px; font-weight:600;
                background:#ff3b30; color:white;
                border:none; border-radius:20px; padding:0 24px;
            }
            QPushButton:hover  { background:#e0302a; }
            QPushButton:pressed{ background:#c02520; }
        """)
        delete_btn.clicked.connect(self.accept)

        btn_row.addWidget(cancel_btn)
        btn_row.addWidget(delete_btn)
        card_layout.addLayout(btn_row)

        main = QVBoxLayout(self)
        main.setContentsMargins(0, 0, 0, 0)
        main.addWidget(outer)


class _SessionItemWidget(QWidget):
    delete_requested = pyqtSignal(str)
    rename_requested = pyqtSignal(str)

    def __init__(self, session_id: str, title: str, date: str,
                 msg_count: int = 0, preview: str = "", kind: str = "text", parent=None):
        super().__init__(parent)
        self.session_id = session_id
        self.title = title
        self.kind = kind
        self.setMinimumHeight(78)
        self.setStyleSheet("QWidget { background: transparent; }")

        outer = QHBoxLayout(self)
        outer.setContentsMargins(10, 8, 8, 8)
        outer.setSpacing(10)

        avatar = QLabel(title[0].upper() if title else "C")
        avatar.setFixedSize(38, 38)
        avatar.setAlignment(Qt.AlignCenter)
        avatar.setStyleSheet("""
            QLabel {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0095f6, stop:1 #0055a5
                );
                color: white;
                font-size: 14px;
                font-weight: 700;
                border-radius: 19px;
            }
        """)
        outer.addWidget(avatar)

        text_col = QVBoxLayout()
        text_col.setSpacing(3)
        text_col.setContentsMargins(0, 0, 0, 0)

        title_row = QHBoxLayout()
        title_row.setSpacing(4)
        title_row.setContentsMargins(0, 0, 0, 0)
        title_lbl = QLabel(title[:22] + ("…" if len(title) > 22 else ""))
        title_lbl.setStyleSheet(
            "font-size:12px; font-weight:700; color:#1a1a2e; background:transparent;"
        )
        title_row.addWidget(title_lbl, 1)
        date_lbl = QLabel(date)
        date_lbl.setStyleSheet("font-size:10px; color:#bbb; background:transparent;")
        title_row.addWidget(date_lbl)
        text_col.addLayout(title_row)

        meta_row = QHBoxLayout()
        meta_row.setSpacing(4)
        meta_row.setContentsMargins(0, 0, 0, 0)
        kind_lbl = QLabel()
        kind_lbl.setText(_session_kind_badge(kind))
        kind_lbl.setTextFormat(Qt.RichText)
        kind_lbl.setStyleSheet("background:transparent;")
        meta_row.addWidget(kind_lbl)
        if msg_count > 0:
            count_lbl = QLabel(str(msg_count))
            count_lbl.setFixedSize(20, 16)
            count_lbl.setAlignment(Qt.AlignCenter)
            count_lbl.setStyleSheet("""
                QLabel {
                    background:#0095f6; color:white;
                    font-size:9px; font-weight:700;
                    border-radius:8px;
                }
            """)
            meta_row.addWidget(count_lbl)
        meta_row.addStretch()
        text_col.addLayout(meta_row)

        preview_text = (preview[:32] + "…") if len(preview) > 32 else preview
        preview_lbl = QLabel(preview_text if preview_text else "No messages yet")
        preview_lbl.setStyleSheet("font-size:11px; color:#888; background:transparent;")
        text_col.addWidget(preview_lbl)

        outer.addLayout(text_col, 1)

        btn_col = QVBoxLayout()
        btn_col.setSpacing(4)
        btn_col.setContentsMargins(0, 0, 0, 0)

        self._rename_btn = QPushButton("✎")
        self._rename_btn.setFixedSize(28, 28)
        self._rename_btn.setToolTip("Rename this chat")
        self._rename_btn.setStyleSheet("""
            QPushButton {
                font-size:12px;
                background:#f2f7ff;
                color:#0055a5;
                border:1px solid #d0e0ff;
                border-radius:14px;
            }
            QPushButton:hover { background:#e6f0ff; }
        """)
        self._rename_btn.clicked.connect(lambda: self.rename_requested.emit(self.session_id))
        btn_col.addWidget(self._rename_btn)

        self._del_btn = QPushButton("🗑")
        self._del_btn.setFixedSize(28, 28)
        self._del_btn.setToolTip("Delete this chat")
        self._del_btn.setStyleSheet("""
            QPushButton {
                font-size:12px;
                background:#fff0f0;
                color:#cc0000;
                border:1px solid #ffd0d0;
                border-radius:14px;
            }
            QPushButton:hover  { background:#ffe0e0; border:1px solid #ffb0b0; }
            QPushButton:pressed{ background:#ffc8c8; }
        """)
        self._del_btn.clicked.connect(self._on_delete_clicked)
        btn_col.addWidget(self._del_btn)
        btn_col.addStretch()
        outer.addLayout(btn_col)

    def sizeHint(self):
        return QSize(252, 78)

    def _on_delete_clicked(self):
        dlg = _DeleteConfirmDialog(self.title, self)
        if dlg.exec() == QDialog.Accepted:
            self.delete_requested.emit(self.session_id)


class ChatSidebar(QWidget):
    new_chat_requested = pyqtSignal()
    session_deleted = pyqtSignal(str)
    delete_all_requested = pyqtSignal()
    rename_requested = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(290)
        self._all_sessions_cache = []
        self.setStyleSheet("""
            QWidget {
                background:#ffffff;
                border-right:1px solid #ececec;
            }
        """)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        top = QWidget()
        top.setFixedHeight(52)
        top.setStyleSheet("""
            QWidget {
                background:#ffffff;
                border-bottom:1px solid #f0f0f0;
            }
        """)
        top_row = QHBoxLayout(top)
        top_row.setContentsMargins(14, 0, 10, 0)
        top_row.setSpacing(8)

        title_lbl = QLabel("Chats")
        title_lbl.setStyleSheet(
            "font-size:16px; font-weight:700; color:#1a1a2e; background:transparent;"
        )
        top_row.addWidget(title_lbl, 1)

        close_btn = QPushButton("✕")
        close_btn.setFixedSize(26, 26)
        close_btn.setStyleSheet("""
            QPushButton {
                font-size:11px; color:#888;
                background:transparent; border:none; border-radius:13px;
            }
            QPushButton:hover  { background:#f0f0f0; color:#333; }
            QPushButton:pressed{ background:#e0e0e0; }
        """)
        close_btn.clicked.connect(self.hide)
        top_row.addWidget(close_btn)
        root.addWidget(top)

        controls = QWidget()
        controls_layout = QVBoxLayout(controls)
        controls_layout.setContentsMargins(12, 8, 12, 8)
        controls_layout.setSpacing(8)

        self.new_btn = QPushButton("+ New Chat")
        self.new_btn.setFixedHeight(36)
        self.new_btn.setStyleSheet("""
            QPushButton {
                font-size:12px; font-weight:600;
                background:#0095f6; color:white;
                border:none; border-radius:18px;
            }
            QPushButton:hover  { background:#0082d8; }
            QPushButton:pressed{ background:#006ab8; }
        """)
        self.new_btn.clicked.connect(self.new_chat_requested)
        controls_layout.addWidget(self.new_btn)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search chats…")
        self.search_input.setFixedHeight(34)
        self.search_input.setStyleSheet("""
            QLineEdit {
                font-size:12px;
                padding:7px 12px;
                border:1px solid #e0e0e0;
                border-radius:17px;
                background:#f7f7f7;
                color:#1a1a2e;
            }
            QLineEdit:focus {
                border:1px solid #0095f6;
                background:#ffffff;
            }
        """)
        self.search_input.textChanged.connect(self._apply_filter)
        controls_layout.addWidget(self.search_input)

        delete_all_btn = QPushButton("Delete All Chats")
        delete_all_btn.setFixedHeight(30)
        delete_all_btn.setStyleSheet("""
            QPushButton {
                font-size:11px;
                font-weight:600;
                background:#fff0f0;
                color:#cc0000;
                border:1px solid #ffd0d0;
                border-radius:15px;
            }
            QPushButton:hover  { background:#ffe0e0; }
            QPushButton:pressed{ background:#ffc8c8; }
        """)
        delete_all_btn.clicked.connect(self.delete_all_requested)
        controls_layout.addWidget(delete_all_btn)
        root.addWidget(controls)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setFixedHeight(1)
        sep.setStyleSheet("QFrame { background:#f0f0f0; border:none; }")
        root.addWidget(sep)

        self.session_list = QListWidget()
        self.session_list.setSpacing(2)
        self.session_list.setStyleSheet("""
            QListWidget {
                background:#ffffff;
                border:none;
                outline:0;
                padding:6px;
            }
            QListWidget::item {
                border:none;
                padding:0;
                margin:0;
            }
            QListWidget::item:hover    { background:#f5f8ff; }
            QListWidget::item:selected { background:#eaf3ff; }
        """)
        root.addWidget(self.session_list)

        self._empty_lbl = QLabel("No saved chats yet.\nStart a conversation!")
        self._empty_lbl.setAlignment(Qt.AlignCenter)
        self._empty_lbl.setStyleSheet("""
            QLabel {
                color:#ccc; font-size:12px;
                padding:30px 10px;
                background:transparent;
            }
        """)
        self._empty_lbl.setWordWrap(True)
        self._empty_lbl.hide()
        root.addWidget(self._empty_lbl)

    def populate(self):
        self._all_sessions_cache = []
        self.session_list.clear()
        if not os.path.exists(_SESSIONS_DIR):
            self._empty_lbl.show()
            return
        for fname in os.listdir(_SESSIONS_DIR):
            if not fname.endswith('.json'):
                continue
            try:
                with open(os.path.join(_SESSIONS_DIR, fname), encoding='utf-8') as f:
                    s = json.load(f)
                self._all_sessions_cache.append(s)
            except Exception:
                pass
        self._all_sessions_cache.sort(key=lambda s: s.get('updated_at', ''), reverse=True)
        self._apply_filter()

    def _apply_filter(self):
        self.session_list.clear()
        query = self.search_input.text().strip().lower()
        filtered = []
        for s in self._all_sessions_cache:
            title = s.get('title', 'Chat')
            msgs = s.get('messages', [])
            preview = next((m[5:].strip() for m in msgs if m.startswith("User:")), "")
            kind = s.get('kind', 'text')
            haystack = f"{title} {preview} {kind}".lower()
            if not query or query in haystack:
                filtered.append(s)
        if not filtered:
            self._empty_lbl.show()
            return
        self._empty_lbl.hide()
        for s in filtered:
            sid = s['id']
            title = s.get('title', 'Chat')
            date = s.get('updated_at', '')[:10]
            msgs = s.get('messages', [])
            msg_count = sum(1 for m in msgs if m.startswith("User:"))
            preview = next((m[5:].strip() for m in msgs if m.startswith("User:")), "")
            kind = s.get('kind', 'text')
            item = QListWidgetItem()
            item.setData(Qt.UserRole, sid)
            widget = _SessionItemWidget(sid, title, date, msg_count, preview, kind, self.session_list)
            widget.delete_requested.connect(self._delete_session)
            widget.rename_requested.connect(self.rename_requested)
            item.setSizeHint(widget.sizeHint())
            self.session_list.addItem(item)
            self.session_list.setItemWidget(item, widget)

    def upsert_session(self, session: dict):
        sid = session.get('id')
        if not sid:
            return
        for i, s in enumerate(self._all_sessions_cache):
            if s.get('id') == sid:
                self._all_sessions_cache[i] = session
                break
        else:
            self._all_sessions_cache.insert(0, session)
        self._all_sessions_cache.sort(
            key=lambda s: s.get('updated_at', ''), reverse=True
        )
        self._apply_filter()

    def _delete_session(self, session_id: str):
        path = os.path.join(_SESSIONS_DIR, f"{session_id}.json")
        try:
            if os.path.exists(path):
                # Clean up clipboard images associated with this session before deleting it
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        session_data = json.load(f)
                    messages = session_data.get('messages', [])
                    tmp_dir = os.path.join(
                        os.path.expanduser('~'), '.esim', 'clipboard_images'
                    )
                    if os.path.isdir(tmp_dir):
                        for msg in messages:
                            matches = re.findall(r'paste_\d+_\d+\.png', msg)
                            for fname in matches:
                                img_path = os.path.join(tmp_dir, fname)
                                if os.path.isfile(img_path):
                                    try:
                                        os.remove(img_path)
                                    except Exception:
                                        pass
                except Exception as ex:
                    print(f"Error cleaning up session clipboard images: {ex}")
                
                os.remove(path)
        except Exception:
            pass
        self.session_deleted.emit(session_id)
        self.populate()


# ── Main Chatbot GUI ──────────────────────────────────────────────────────────

class ChatbotGUI(QWidget):
    _background_session_saved = pyqtSignal(dict)

    # Sentinel anchor names — used by find_*_anchor_cursor to locate the
    # typing/streaming bubble in the document regardless of reflow position.
    _TYPING_ANCHOR = '<a name="_typing_anchor_">&#8203;</a>'
    _STREAM_ANCHOR = '<a name="_stream_anchor_">&#8203;</a>'

    def __init__(self):
        super().__init__()
        self.setWindowTitle("eSim AI Assistant")
        self.setMinimumSize(420, 340)
        self.resize(430, 350)
        self.setAcceptDrops(True)

        self.chat_history = []
        self._retry_history = []
        self._bot_responses = {}
        self._response_counter = 0
        self._last_user_text = ""
        self._typing_frame = 0
        self._typing_start_pos = -1
        self._was_ollama_offline = True
        self._mic_active = False
        self._viewing_past_session = False
        self._staged_images = []
        self._temperature = 0.35
        self._num_predict = 1024
        self._current_session_id = str(uuid.uuid4())
        self._session_created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
        self._current_session_kind = "text"
        self._session_title_override = None
        self._is_generating = False
        self._images_store = {}
        self._last_image_paths = []

        # Streaming state (per-message; cleared in display_response)
        self._stream_buf = None
        self._stream_ts = None
        self._stream_idx = None

        self._save_pending = False
        self._save_debounce_timer = QTimer(self)
        self._save_debounce_timer.setSingleShot(True)
        self._save_debounce_timer.timeout.connect(self._flush_save)

        self._typing_anim_timer = QTimer(self)
        self._typing_anim_timer.timeout.connect(self._animate_typing_bubble)

        self._status_poll_timer = QTimer(self)
        self._status_poll_timer.timeout.connect(self._update_ollama_status)
        self._status_poll_timer.start(5000)

        self._toast = QLabel("  ✅  Copied!  ", self)
        self._toast.setStyleSheet("""
            QLabel {
                background-color:#1a1a2e; color:#ffffff;
                font-size:12px; font-weight:bold;
                border-radius:14px; padding:4px 14px;
            }
        """)
        self._toast.setAlignment(Qt.AlignCenter)
        self._toast.hide()

        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self._sidebar = ChatSidebar(self)
        self._sidebar.new_chat_requested.connect(self._new_chat)
        self._sidebar.session_deleted.connect(self._on_session_deleted)
        self._sidebar.delete_all_requested.connect(self._delete_all_chats)
        self._sidebar.rename_requested.connect(self._rename_session_by_id)
        self._sidebar.session_list.itemClicked.connect(self._on_session_clicked)
        self._sidebar.session_list.itemDoubleClicked.connect(self._open_session_viewer)
        self._sidebar.hide()
        root.addWidget(self._sidebar)

        self._background_session_saved.connect(self._sidebar_upsert_from_signal)

        chat_container = QWidget()
        chat_layout = QVBoxLayout(chat_container)
        chat_layout.setContentsMargins(8, 8, 8, 8)
        chat_layout.setSpacing(5)
        root.addWidget(chat_container, 1)

        header_layout = QHBoxLayout()
        header_layout.setSpacing(5)

        self._history_btn = QPushButton("≡")
        self._history_btn.setFixedSize(32, 32)
        self._history_btn.setToolTip("Chat history")
        self._history_btn.setStyleSheet("""
            QPushButton {
                font-size:16px; border:none;
                border-radius:8px; background:transparent; color:#555;
            }
            QPushButton:hover { background:#f0f0f0; color:#1a1a2e; }
            QPushButton:pressed { background:#e0e0e0; }
        """)
        self._history_btn.clicked.connect(self._toggle_sidebar)
        header_layout.addWidget(self._history_btn)

        self.model_combo = QComboBox(self)
        self.model_combo.setFixedHeight(30)
        self.model_combo.setStyleSheet("""
            QComboBox {
                font-size:12px; padding:2px 10px;
                border:1px solid #e0e0e0; border-radius:8px;
                background:#f7f7f7; color:#1a1a2e;
            }
            QComboBox:focus { border:1px solid #0095f6; background:#fff; }
            QComboBox::drop-down { border:none; width:18px; }
        """)
        self._populate_models()
        header_layout.addWidget(self.model_combo)

        self._refresh_models_btn = QPushButton("↻")
        self._refresh_models_btn.setFixedSize(28, 28)
        self._refresh_models_btn.setToolTip("Refresh available models")
        self._refresh_models_btn.setStyleSheet("""
            QPushButton {
                font-size:14px; border:none;
                border-radius:8px; background:transparent; color:#555;
            }
            QPushButton:hover { background:#f0f0f0; color:#1a1a2e; }
        """)
        self._refresh_models_btn.clicked.connect(self._populate_models)
        header_layout.addWidget(self._refresh_models_btn)

        self._rename_btn = QPushButton("✎")
        self._rename_btn.setFixedSize(28, 28)
        self._rename_btn.setToolTip("Rename current chat")
        self._rename_btn.setStyleSheet("""
            QPushButton {
                font-size:13px; border:none;
                border-radius:8px; background:transparent; color:#555;
            }
            QPushButton:hover { background:#f0f0f0; color:#1a1a2e; }
        """)
        self._rename_btn.clicked.connect(self._rename_current_chat)
        header_layout.addWidget(self._rename_btn)

        self._settings_btn = QPushButton("⚙")
        self._settings_btn.setFixedSize(28, 28)
        self._settings_btn.setToolTip("Model settings")
        self._settings_btn.setCheckable(True)
        self._settings_btn.setStyleSheet("""
            QPushButton {
                font-size:14px; border:none;
                border-radius:8px; background:transparent; color:#555;
            }
            QPushButton:hover   { background:#f0f0f0; color:#1a1a2e; }
            QPushButton:checked { background:#e8f0ff; color:#0095f6; }
        """)
        header_layout.addWidget(self._settings_btn)

        self._export_btn = QPushButton("⤓")
        self._export_btn.setFixedSize(28, 28)
        self._export_btn.setToolTip("Export current chat")
        self._export_btn.setStyleSheet("""
            QPushButton {
                font-size:13px; border:none;
                border-radius:8px; background:transparent; color:#555;
            }
            QPushButton:hover { background:#f0f0f0; color:#1a1a2e; }
        """)
        self._export_btn.clicked.connect(self._export_current_chat)
        header_layout.addWidget(self._export_btn)

        self._regen_btn = QPushButton("⟳")
        self._regen_btn.setFixedSize(28, 28)
        self._regen_btn.setToolTip("Regenerate last response")
        self._regen_btn.setStyleSheet("""
            QPushButton {
                font-size:13px; border:none;
                border-radius:8px; background:transparent; color:#555;
            }
            QPushButton:hover { background:#f0f0f0; color:#1a1a2e; }
        """)
        self._regen_btn.clicked.connect(self._regenerate_last_response)
        header_layout.addWidget(self._regen_btn)

        header_layout.addStretch()

        self.ollama_status_label = QLabel(self)
        self.ollama_status_label.setFixedHeight(24)
        header_layout.addWidget(self.ollama_status_label)
        self._update_ollama_status()

        header_sep = QFrame()
        header_sep.setFrameShape(QFrame.HLine)
        header_sep.setStyleSheet("color:#ececec; margin:0;")
        chat_layout.addLayout(header_layout)
        chat_layout.addWidget(header_sep)

        self.chat_display = QTextBrowser(self)
        self.chat_display.setOpenLinks(False)
        self.chat_display.setOpenExternalLinks(False)
        self.chat_display.setHtml(WELCOME_MESSAGE)
        self.chat_display.anchorClicked.connect(self._handle_link_click)
        self.chat_display.setStyleSheet("""
            QTextBrowser {
                background-color:#fafafa;
                border:none;
                padding:8px 4px;
                font-family:'Segoe UI',Arial,sans-serif;
                font-size:13px;
                selection-background-color:#cce4f7;
            }
            QScrollBar:vertical {
                background:transparent; width:6px;
            }
            QScrollBar::handle:vertical {
                background:#d0d0d0; border-radius:3px; min-height:24px;
            }
            QScrollBar::handle:vertical:hover { background:#a0a0a0; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height:0px;
            }
        """)
        chat_layout.addWidget(self.chat_display)

        status_layout = QHBoxLayout()
        self.status_label = QLabel("", self)
        self.status_label.setStyleSheet(
            "color:#0095f6; font-size:11px; padding:1px 4px; background:transparent;"
        )
        status_layout.addWidget(self.status_label)
        status_layout.addStretch()
        chat_layout.addLayout(status_layout)

        self._settings_panel = QWidget()
        self._settings_panel.setVisible(False)
        self._settings_panel.setStyleSheet("""
            QWidget {
                background:#f7f9fc;
                border-top:1px solid #ececec;
                border-bottom:1px solid #ececec;
            }
        """)
        self._settings_btn.toggled.connect(lambda on: self._settings_panel.setVisible(on))
        sp_layout = QHBoxLayout(self._settings_panel)
        sp_layout.setContentsMargins(12, 8, 12, 8)
        sp_layout.setSpacing(16)

        temp_col = QVBoxLayout()
        self._temp_label = QLabel(f"Precision  {self._temperature:.2f}")
        self._temp_label.setStyleSheet("font-size:10px; color:#555;")
        temp_col.addWidget(self._temp_label)
        self._temp_slider = QSlider(Qt.Horizontal)
        self._temp_slider.setRange(1, 100)
        self._temp_slider.setValue(int(self._temperature * 100))
        self._temp_slider.setFixedWidth(110)
        self._temp_slider.valueChanged.connect(self._on_temp_changed)
        temp_col.addWidget(self._temp_slider)
        sp_layout.addLayout(temp_col)

        tok_col = QVBoxLayout()
        self._tok_label = QLabel(f"Max tokens  {self._num_predict}")
        self._tok_label.setStyleSheet("font-size:10px; color:#555;")
        tok_col.addWidget(self._tok_label)
        self._tok_slider = QSlider(Qt.Horizontal)
        self._tok_slider.setRange(1, 40)
        self._tok_slider.setValue(self._num_predict // 128)
        self._tok_slider.setFixedWidth(110)
        self._tok_slider.valueChanged.connect(self._on_tok_changed)
        tok_col.addWidget(self._tok_slider)
        sp_layout.addLayout(tok_col)

        sp_layout.addStretch()
        reset_btn = QPushButton("Reset")
        reset_btn.setFixedHeight(26)
        reset_btn.setStyleSheet("""
            QPushButton {
                font-size:10px; padding:2px 12px;
                background:#f0f0f0; color:#555;
                border:none; border-radius:13px;
            }
        """)
        reset_btn.clicked.connect(self._reset_settings)
        sp_layout.addWidget(reset_btn)
        chat_layout.addWidget(self._settings_panel)

        input_layout = QHBoxLayout()

        self.attach_button = QPushButton("📎")
        self.attach_button.setFixedSize(38, 38)
        self.attach_button.setToolTip(
            "Attach image for analysis\n"
            "Tip: install Pillow (pip install Pillow) to auto-downscale\n"
            "large images for faster analysis"
        )
        self.attach_button.setStyleSheet("""
            QPushButton {
                font-size:16px; background:#f0f0f0;
                border:none; border-radius:19px;
            }
            QPushButton:hover  { background:#e0e8ff; }
        """)
        self.attach_button.clicked.connect(self._pick_image)
        input_layout.addWidget(self.attach_button)

        self.mic_button = QPushButton("🎤")
        self.mic_button.setFixedSize(38, 38)
        QTimer.singleShot(200, self._update_mic_tooltip)
        self.mic_button.setStyleSheet("""
            QPushButton {
                font-size:15px; background:#f0f0f0;
                border:none; border-radius:19px;
            }
            QPushButton:hover  { background:#d0f8d0; }
        """)
        self.mic_button.clicked.connect(self._on_mic_clicked)
        input_layout.addWidget(self.mic_button)

        self.user_input = _HistoryLineEdit(
            self, placeholderText="Message eSim AI…  (↑↓ for history)"
        )
        self.user_input.setMinimumHeight(42)
        self.user_input.setStyleSheet("""
            QLineEdit {
                font-size:14px; padding:10px 18px;
                border:1.5px solid #e0e0e0; border-radius:21px;
                background:#f7f7f7; color:#1a1a2e;
            }
            QLineEdit:focus {
                border:1.5px solid #0095f6;
                background:#ffffff;
            }
        """)
        self.user_input.returnPressed.connect(self.ask_ollama)
        self.user_input.image_pasted.connect(
            lambda path: self._stage_image_paths([path])
        )
        input_layout.addWidget(self.user_input)

        self.send_button = QPushButton("➤")
        self.send_button.setFixedSize(40, 40)
        self.send_button.setToolTip("Send Message")
        self.send_button.setStyleSheet("""
            QPushButton {
                font-size:18px; font-weight:600;
                background-color:#0095f6; color:white;
                border:none; border-radius:20px;
                padding-left: 2px;
            }
            QPushButton:hover  { background-color:#0082d8; }
        """)
        self.send_button.clicked.connect(self.ask_ollama)
        input_layout.addWidget(self.send_button)

        self.stop_button = QPushButton("Stop")
        self.stop_button.setFixedHeight(38)
        self.stop_button.setStyleSheet("""
            QPushButton {
                font-size:13px; font-weight:600; padding:5px 16px;
                background-color:#ff3b30; color:white;
                border:none; border-radius:19px;
            }
        """)
        self.stop_button.clicked.connect(self._stop_generating)
        self.stop_button.hide()
        input_layout.addWidget(self.stop_button)

        chat_layout.addLayout(input_layout)

        self._staging_area = QWidget()
        self._staging_area.setStyleSheet("QWidget { background:#f5f8ff; border-radius:10px; }")
        self._staging_area.setVisible(False)
        staging_outer = QVBoxLayout(self._staging_area)
        staging_outer.setContentsMargins(6, 6, 6, 4)
        staging_outer.setSpacing(4)

        staging_header = QHBoxLayout()
        staged_lbl = QLabel("Images to send:")
        staged_lbl.setStyleSheet("font-size:11px;color:#555;")
        staging_header.addWidget(staged_lbl)
        staging_header.addStretch()
        clear_all_btn = QPushButton("Remove all")
        clear_all_btn.setFixedHeight(20)
        clear_all_btn.setStyleSheet("""
            QPushButton {
                font-size:10px; color:#cc0000; background:transparent;
                border:none; padding:0 4px;
            }
            QPushButton:hover { text-decoration:underline; }
        """)
        clear_all_btn.clicked.connect(self._clear_staged_images)
        staging_header.addWidget(clear_all_btn)
        staging_outer.addLayout(staging_header)

        scroll = QScrollArea()
        scroll.setFixedHeight(72)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border:none; background:transparent; }")
        self._thumb_container = QWidget()
        self._thumb_row = QHBoxLayout(self._thumb_container)
        self._thumb_row.setContentsMargins(0, 0, 0, 0)
        self._thumb_row.setSpacing(6)
        self._thumb_row.addStretch()
        scroll.setWidget(self._thumb_container)
        staging_outer.addWidget(scroll)
        chat_layout.addWidget(self._staging_area)

        self.move_to_bottom_right()
        self._load_history()

    # ── Streaming helpers ─────────────────────────────────────────────

    def _start_worker(self, worker):
        """Hook a freshly-created worker to all signals and start it."""
        self.worker = worker
        self.worker.response_signal.connect(self.display_response)
        self.worker.status_signal.connect(self._on_status_update)
        if hasattr(self.worker, "chunk_signal"):
            self.worker.chunk_signal.connect(self._on_stream_chunk)
        self.worker.start()

    def _find_anchor_cursor(self, anchor_name: str):
        """Generic anchor finder, used for both typing and streaming anchors."""
        doc = self.chat_display.document()
        block = doc.begin()
        while block.isValid():
            it = block.begin()
            while not it.atEnd():
                frag = it.fragment()
                if frag.isValid():
                    fmt = frag.charFormat()
                    matched = False
                    try:
                        names = fmt.anchorNames()
                        matched = anchor_name in (names or [])
                    except AttributeError:
                        try:
                            matched = fmt.anchorName() == anchor_name
                        except AttributeError:
                            matched = False
                    if matched:
                        cursor = QTextCursor(doc)
                        cursor.setPosition(frag.position())
                        return cursor
                it += 1
            block = block.next()
        return None

    def _find_typing_anchor_cursor(self):
        return self._find_anchor_cursor("_typing_anchor_")

    def _find_stream_anchor_cursor(self):
        return self._find_anchor_cursor("_stream_anchor_")

    def _begin_streaming_bubble(self):
        """Drop the typing dots and open an empty bot bubble anchored for replacement."""
        self._remove_typing_bubble()
        self._stream_buf = ""
        self._stream_ts = _get_time()
        self._stream_idx = self._response_counter
        cursor = QTextCursor(self.chat_display.document())
        cursor.movePosition(QTextCursor.End)
        cursor.insertHtml(
            self._STREAM_ANCHOR
            + _bot_bubble("…", self._stream_ts, self._stream_idx)
        )
        self._scroll_to_bottom()

    def _on_stream_chunk(self, piece: str):
        """Append a streamed token to the in-progress bot bubble."""
        if self._stream_buf is None:
            self._begin_streaming_bubble()
        self._stream_buf += piece

        anchor_cursor = self._find_stream_anchor_cursor()
        if anchor_cursor is None:
            # Sentinel went missing — re-open the bubble with the buffer so far.
            buf = self._stream_buf
            self._reset_stream_state()
            self._begin_streaming_bubble()
            self._stream_buf = buf
            anchor_cursor = self._find_stream_anchor_cursor()
            if anchor_cursor is None:
                return

        # Select from anchor to end of document and rewrite the bubble in place.
        anchor_cursor.movePosition(QTextCursor.End, QTextCursor.KeepAnchor)
        anchor_cursor.removeSelectedText()
        anchor_cursor.insertHtml(
            self._STREAM_ANCHOR
            + _bot_bubble(self._stream_buf, self._stream_ts, self._stream_idx)
        )

        sb = self.chat_display.verticalScrollBar()
        if sb.maximum() - sb.value() < 60:
            sb.setValue(sb.maximum())

    def _reset_stream_state(self):
        self._stream_buf = None
        self._stream_ts = None
        self._stream_idx = None

    # ── Drag & drop ───────────────────────────────────────────────────

    def dragEnterEvent(self, event: QDragEnterEvent):
        mime = event.mimeData()
        if mime.hasUrls():
            for url in mime.urls():
                if url.isLocalFile() and _is_image_file(url.toLocalFile()):
                    event.acceptProposedAction()
                    return
        event.ignore()

    def dropEvent(self, event: QDropEvent):
        mime = event.mimeData()
        if not mime.hasUrls():
            event.ignore()
            return
        added = 0
        for url in mime.urls():
            if not url.isLocalFile():
                continue
            path = url.toLocalFile()
            if _is_image_file(path) and path not in self._staged_images:
                self._staged_images.append(path)
                added += 1
        if added:
            self._refresh_staging_strip()
            self.status_label.setText(f"📎 Added {added} image{'s' if added != 1 else ''} by drag-and-drop.")
            QTimer.singleShot(2500, lambda: self.status_label.setText(""))
        event.acceptProposedAction()

    # ── Sidebar / sessions ────────────────────────────────────────────

    def _toggle_sidebar(self):
        if self._sidebar.isVisible():
            self._sidebar.hide()
        else:
            self._sidebar.populate()
            self._sidebar.show()

    def _refresh_sidebar_if_open(self):
        if self._sidebar.isVisible():
            self._sidebar.populate()

    def _delete_all_chats(self):
        dlg = _DeleteConfirmDialog("all chats", self)
        if dlg.exec() != QDialog.Accepted:
            return
        try:
            if os.path.exists(_SESSIONS_DIR):
                for fname in os.listdir(_SESSIONS_DIR):
                    if fname.endswith(".json"):
                        os.remove(os.path.join(_SESSIONS_DIR, fname))
            # Clean up all clipboard images
            tmp_dir = os.path.join(
                os.path.expanduser('~'), '.esim', 'clipboard_images'
            )
            if os.path.isdir(tmp_dir):
                for fname in os.listdir(tmp_dir):
                    fpath = os.path.join(tmp_dir, fname)
                    if os.path.isfile(fpath):
                        try:
                            os.remove(fpath)
                        except Exception:
                            pass
        except Exception:
            pass
        self._sidebar.populate()

    def _open_session_viewer(self, item):
        session_id = item.data(Qt.UserRole)
        path = os.path.join(_SESSIONS_DIR, f"{session_id}.json")
        try:
            with open(path, encoding='utf-8') as f:
                session = json.load(f)
        except Exception:
            return
        dlg = ChatHistoryViewer(session, self)
        dlg.exec()

    def _rename_current_chat(self):
        title, ok = QInputDialog.getText(
            self, "Rename Chat", "New chat title:",
            text=self._session_title_override or self._derive_session_title()
        )
        if ok:
            title = title.strip()
            if title:
                self._session_title_override = title
                self._save_history()
                self.status_label.setText("✏️ Chat renamed.")
                QTimer.singleShot(2000, lambda: self.status_label.setText(""))

    def _rename_session_by_id(self, session_id: str):
        path = os.path.join(_SESSIONS_DIR, f"{session_id}.json")
        try:
            with open(path, encoding='utf-8') as f:
                session = json.load(f)
        except Exception:
            return
        current_title = session.get("title", "Chat")
        title, ok = QInputDialog.getText(
            self, "Rename Chat", "New chat title:", text=current_title
        )
        if not ok:
            return
        title = title.strip()
        if not title:
            return
        try:
            session["title"] = title
            with open(path, "w", encoding="utf-8") as f:
                json.dump(session, f, ensure_ascii=False, indent=2)
        except Exception:
            return
        if session_id == self._current_session_id:
            self._session_title_override = title
        self._sidebar.populate()

    def _derive_session_title(self):
        if self._session_title_override:
            return self._session_title_override
        return next(
            (m[5:].strip()[:50] for m in self.chat_history if m.startswith("User:")),
            "Chat"
        )

    def _rebuild_chat_html_from_history(self):
        self.chat_display.setHtml(WELCOME_MESSAGE)
        self._bot_responses = {}
        self._response_counter = 0
        for line in self.chat_history:
            if line.startswith("User:"):
                self.chat_display.append(_user_bubble(line[5:].strip(), ""))
            elif line.startswith("Bot:"):
                idx = self._response_counter
                text = line[4:].strip()
                self._bot_responses[idx] = text
                self.chat_display.append(_bot_bubble(text, "", idx))
                self._response_counter += 1
        self._scroll_to_bottom()

    def _on_session_clicked(self, item):
        session_id = item.data(Qt.UserRole)
        if (session_id == self._current_session_id
                and not self._viewing_past_session):
            return
        if self._is_generating:
            self._suspend_worker(
                session_id=self._current_session_id,
                history=self.chat_history,
                session_kind=self._current_session_kind,
                images_store=self._images_store,
            )
        self._save_debounce_timer.stop()
        self._save_pending = False
        self._save_current_session()

        path = os.path.join(_SESSIONS_DIR, f"{session_id}.json")
        session = None
        try:
            with open(path, encoding='utf-8') as f:
                session = json.load(f)
        except Exception:
            pass
        if session is None:
            for s in self._sidebar._all_sessions_cache:
                if s.get('id') == session_id:
                    session = s
                    break
        if session is None:
            return

        msgs    = session.get('messages', [])
        title   = session.get('title', 'Chat')
        created = session.get('created_at', '')
        kind    = session.get('kind', 'text')

        self._current_session_id      = session_id
        self._session_created_at      = created
        self._current_session_kind    = kind
        self._session_title_override  = title if title != "Chat" else None
        self.chat_history             = list(msgs)
        self._retry_history           = list(msgs)
        self._last_user_text          = next(
            (m[5:].strip() for m in reversed(msgs) if m.startswith("User:")), ""
        )

        saved_images = session.get("images", {})
        self._images_store = saved_images
        self._last_image_paths = []

        html = WELCOME_MESSAGE
        html += (
            '<table width="100%" cellpadding="0" cellspacing="0"><tr>'
            '<td align="center" style="padding:6px 8px;">'
            '<div style="background-color:#f0f4ff;color:#0055a5;'
            'border:1px solid #b0c4e8;border-radius:12px;'
            'padding:8px 16px;font-size:11px;">'
            f'Viewing saved chat: <b>{_escape_text_preserve_breaks(title[:50])}</b>'
            f'&nbsp;&nbsp;·&nbsp;&nbsp;{_escape_text_preserve_breaks(created)}'
            f'&nbsp;&nbsp;·&nbsp;&nbsp;{kind}'
            '<br><span style="color:#888;font-size:10px;">'
            'Scroll down to see full conversation</span>'
            '</div></td></tr></table><br>'
        )

        self._bot_responses = {}
        local_counter = 0

        all_saved_imgs = []
        for key in sorted(saved_images.keys()):
            all_saved_imgs.extend(saved_images[key])
        img_replay_idx = 0

        for line in msgs:
            if line.startswith("User:"):
                text = line[5:].strip()
                if text.startswith("[Image analysis request:"):
                    while img_replay_idx < len(all_saved_imgs):
                        fname, b64 = all_saved_imgs[img_replay_idx]
                        html += _image_thumbnail_html(b64, fname)
                        img_replay_idx += 1
                        if img_replay_idx >= len(all_saved_imgs):
                            break
                    user_text_part = text.split("\n", 1)[-1].strip()
                    if user_text_part and not user_text_part.startswith("[Image"):
                        html += _user_bubble(user_text_part, "")
                else:
                    html += _user_bubble(text, "")
            elif line.startswith("Bot:"):
                text = line[4:].strip()
                self._bot_responses[local_counter] = text
                html += _bot_bubble(text, "", local_counter)
                local_counter += 1

        self._response_counter = local_counter
        self.chat_display.setHtml(html)
        QTimer.singleShot(120, lambda: self.chat_display.verticalScrollBar().setValue(
            self.chat_display.verticalScrollBar().maximum()
        ))

        self.chat_history = list(msgs)
        self._retry_history = list(msgs)
        self._current_session_id = session_id
        self._session_created_at = session.get('created_at', datetime.now().strftime("%Y-%m-%d %H:%M"))
        self._current_session_kind = kind
        self._session_title_override = session.get('title', None)
        self._last_user_text = next(
            (m[5:].strip() for m in reversed(msgs) if m.startswith("User:")), ""
        )
        self._viewing_past_session = True

    def _abort_worker(self):
        if hasattr(self, 'worker') and self.worker.isRunning():
            self.worker.stop()
            try:
                self.worker.response_signal.disconnect()
                self.worker.status_signal.disconnect()
                if hasattr(self.worker, "chunk_signal"):
                    self.worker.chunk_signal.disconnect()
            except Exception:
                pass
            self.worker.wait(300)
        self._stop_thinking()
        self._reset_stream_state()

    def _sidebar_upsert_from_signal(self, session: dict):
        self._sidebar.upsert_session(session)

    def _suspend_worker(self, session_id: str, history: list,
                        session_kind: str, images_store: dict):
        if not (hasattr(self, 'worker') and self.worker.isRunning()):
            self._stop_thinking()
            return
        _sid     = session_id
        _history = list(history)
        _kind    = session_kind
        _images  = dict(images_store)
        _worker  = self.worker
        _signal  = self._background_session_saved

        def _on_background_response(bot_response: str):
            try:
                _history.append(f"Bot: {bot_response}")
                path = os.path.join(_SESSIONS_DIR, f"{_sid}.json")
                if os.path.exists(path):
                    with open(path, encoding="utf-8") as fp:
                        session = json.load(fp)
                else:
                    session = {
                        "id":         _sid,
                        "title":      next(
                            (m[5:].strip()[:50] for m in _history
                             if m.startswith("User:")), "Chat"
                        ),
                        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "kind":       _kind,
                        "images":     _images,
                    }
                session["messages"]   = _history[-40:]
                session["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                session["kind"]       = _kind
                os.makedirs(_SESSIONS_DIR, exist_ok=True)
                with open(path, "w", encoding="utf-8") as fp:
                    json.dump(session, fp, ensure_ascii=False, indent=2)
                _signal.emit(session)
            except Exception:
                pass

        try:
            _worker.response_signal.disconnect()
            _worker.status_signal.disconnect()
            if hasattr(_worker, "chunk_signal"):
                _worker.chunk_signal.disconnect()
        except Exception:
            pass
        _worker.response_signal.connect(_on_background_response)
        self._stop_thinking()
        self._reset_stream_state()

    def _new_chat(self):
        self._save_debounce_timer.stop()
        self._save_pending = False
        if self._is_generating:
            self._suspend_worker(
                session_id=self._current_session_id,
                history=self.chat_history,
                session_kind=self._current_session_kind,
                images_store=self._images_store,
            )
        else:
            self._save_current_session()

        self.chat_display.setHtml(WELCOME_MESSAGE)
        # MERGED: combined all state resetting into one reusable helper
        self._reset_session_state()

        try:
            if os.path.exists(_HISTORY_FILE):
                os.remove(_HISTORY_FILE)
        except Exception:
            pass

        self._sidebar.populate()

    def _on_session_deleted(self, deleted_id: str):
        if deleted_id == self._current_session_id or self._viewing_past_session:
            self._abort_worker()
            self._save_debounce_timer.stop()
            self._save_pending = False

            # MERGED: combined all state resetting into one reusable helper
            self._reset_session_state()
            try:
                if os.path.exists(_HISTORY_FILE):
                    os.remove(_HISTORY_FILE)
            except Exception:
                pass
            self.chat_display.setHtml(WELCOME_MESSAGE)

    # ── Export ────────────────────────────────────────────────────────

    def _export_current_chat(self):
        if not self.chat_history:
            self.status_label.setText("Nothing to export.")
            QTimer.singleShot(2500, lambda: self.status_label.setText(""))
            return
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Chat",
            os.path.join(os.path.expanduser("~"), "chat_export.txt"),
            "Text Files (*.txt);;Markdown Files (*.md)"
        )
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                for line in self.chat_history:
                    f.write(line.strip() + "\n\n")
            self.status_label.setText("✅ Chat exported.")
            QTimer.singleShot(2500, lambda: self.status_label.setText(""))
        except Exception as e:
            self.status_label.setText(f"❌ Export failed: {e}")
            QTimer.singleShot(3500, lambda: self.status_label.setText(""))

    # ── Ollama status ────────────────────────────────────────────────

    def _update_ollama_status(self):
        self._status_worker = OllamaStatusWorker()
        self._status_worker.result_signal.connect(self._on_status_result)
        self._status_worker.start()

    def _on_status_result(self, running: bool):
        if running:
            self.ollama_status_label.setText("🟢 Live")
            self.ollama_status_label.setStyleSheet("""
                QLabel {
                    font-size:11px; font-weight:bold; padding:2px 10px;
                    border-radius:12px; background-color:#e6f9ee;
                    color:#1a7f3c; border:1px solid #a3d9b5;
                }
            """)
            if self._was_ollama_offline:
                self._was_ollama_offline = False
                self._populate_models()
        else:
            self.ollama_status_label.setText("🔴 Offline")
            self.ollama_status_label.setStyleSheet("""
                QLabel {
                    font-size:11px; font-weight:bold; padding:2px 10px;
                    border-radius:12px; background-color:#fdecea;
                    color:#b71c1c; border:1px solid #f5c0bc;
                }
            """)
            self._was_ollama_offline = True

    # ── Typing bubble ─────────────────────────────────────────────────
    # (_TYPING_ANCHOR and _find_typing_anchor_cursor are defined at the
    # top of the class alongside the streaming helpers.)

    def _show_typing_bubble(self):
        self._typing_frame = 0
        cursor = QTextCursor(self.chat_display.document())
        cursor.movePosition(QTextCursor.End)
        cursor.insertHtml(self._TYPING_ANCHOR + _typing_bubble(0))
        self._scroll_to_bottom()
        self._typing_anim_timer.start(400)

    def _animate_typing_bubble(self):
        self._typing_frame = (self._typing_frame + 1) % 3
        anchor_cursor = self._find_typing_anchor_cursor()
        if anchor_cursor is None:
            self._typing_anim_timer.stop()
            return
        anchor_cursor.movePosition(QTextCursor.End, QTextCursor.KeepAnchor)
        anchor_cursor.insertHtml(self._TYPING_ANCHOR + _typing_bubble(self._typing_frame))
        sb = self.chat_display.verticalScrollBar()
        if sb.maximum() - sb.value() < 60:
            self._scroll_to_bottom()

    def _remove_typing_bubble(self):
        self._typing_anim_timer.stop()
        anchor_cursor = self._find_typing_anchor_cursor()
        if anchor_cursor is not None:
            anchor_cursor.movePosition(QTextCursor.End, QTextCursor.KeepAnchor)
            anchor_cursor.removeSelectedText()
        self._typing_start_pos = -1

    # ── Links ────────────────────────────────────────────────────────

    def _handle_link_click(self, url):
        scheme, parts = _parse_custom_url(url)
        if scheme == 'copy':
            if not parts:
                return
            try:
                idx = int(parts[-1])
            except ValueError:
                return
            text = self._bot_responses.get(idx, "")
            if text:
                QApplication.clipboard().setText(text)
                self._show_copy_toast()
        elif scheme == 'retry':
            if not parts:
                return
            try:
                idx = int(parts[-1])
            except ValueError:
                return
            self._retry_response(idx)

        elif scheme == 'edit':
            if not parts:
                return
            try:
                import base64
                b64_text = parts[-1]
                text = base64.b64decode(b64_text).decode('utf-8')
                self._editing_prompt_text = text
                self.user_input.setText(text)
                self.user_input.setFocus()
            except Exception:
                pass

        elif scheme == 'clear':
            self.clear_session()

    def _show_copy_toast(self):
        self._toast.setText("  ✅  Copied!  ")
        chat_rect = self.chat_display.geometry()
        tw, th = 110, 30
        x = chat_rect.x() + (chat_rect.width() - tw) // 2
        y = chat_rect.y() + chat_rect.height() - th - 16
        self._toast.setGeometry(x, y, tw, th)
        self._toast.show()
        self._toast.raise_()
        QTimer.singleShot(1600, self._toast.hide)

    # ── Images ───────────────────────────────────────────────────────

    def _pick_image(self):
        paths, _ = QFileDialog.getOpenFileNames(self, "Select Images", "", _IMG_FILTER)
        self._stage_image_paths(paths)

    def _stage_image_paths(self, paths):
        added = 0
        for path in paths:
            if path and _is_image_file(path) and path not in self._staged_images:
                self._staged_images.append(path)
                added += 1
        if added:
            self._refresh_staging_strip()

    def _refresh_staging_strip(self):
        while self._thumb_row.count() > 1:
            item = self._thumb_row.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        for path in self._staged_images:
            self._thumb_row.insertWidget(self._thumb_row.count() - 1, self._make_thumbnail(path))
        self._staging_area.setVisible(bool(self._staged_images))

    def _make_thumbnail(self, image_path: str) -> QWidget:
        from PyQt5.QtGui import QPixmap

        card = QWidget()
        card.setFixedSize(80, 64)
        card.setStyleSheet("""
            QWidget {
                background:#ffffff;
                border:1px solid #d0d8f0;
                border-radius:10px;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(4, 4, 4, 2)
        card_layout.setSpacing(2)

        thumb_lbl = QLabel()
        thumb_lbl.setAlignment(Qt.AlignCenter)
        thumb_lbl.setFixedHeight(36)
        pix = QPixmap(image_path)
        if not pix.isNull():
            orig_w, orig_h = pix.width(), pix.height()
            card.setToolTip(
                f"{os.path.basename(image_path)}\n{orig_w} × {orig_h} px"
            )
            pix = pix.scaled(68, 36, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            thumb_lbl.setPixmap(pix)
        else:
            thumb_lbl.setText("🖼")
            thumb_lbl.setStyleSheet("font-size:20px;background:transparent;")
        card_layout.addWidget(thumb_lbl)

        fname = os.path.basename(image_path)
        name_lbl = QLabel(fname[:10] + ("…" if len(fname) > 10 else ""))
        name_lbl.setAlignment(Qt.AlignCenter)
        name_lbl.setStyleSheet("font-size:9px;color:#555;background:transparent;")
        card_layout.addWidget(name_lbl)

        remove_btn = QPushButton("✕", card)
        remove_btn.setFixedSize(16, 16)
        remove_btn.move(62, 2)
        remove_btn.setStyleSheet("""
            QPushButton {
                font-size:9px; font-weight:bold;
                background:#ff3b30; color:white;
                border:none; border-radius:8px;
                padding:0;
            }
            QPushButton:hover { background:#cc2a22; }
        """)
        remove_btn.clicked.connect(lambda checked=False, p=image_path: self._remove_staged_image(p))
        return card

    def _remove_staged_image(self, path: str):
        if path in self._staged_images:
            self._staged_images.remove(path)
        self._refresh_staging_strip()
        self._cleanup_unused_clipboard_images()

    def _clear_staged_images(self):
        self._staged_images.clear()
        self._refresh_staging_strip()
        self._cleanup_unused_clipboard_images()

    def _cleanup_unused_clipboard_images(self):
        tmp_dir = os.path.join(
            os.path.expanduser('~'), '.esim', 'clipboard_images'
        )
        if not os.path.isdir(tmp_dir):
            return
        try:
            # Gather paths currently in use
            in_use = set()
            for p in getattr(self, '_staged_images', []):
                in_use.add(os.path.normpath(p))
            for p in getattr(self, '_last_image_paths', []):
                in_use.add(os.path.normpath(p))
            
            # List files in the directory and delete those not in use
            for fname in os.listdir(tmp_dir):
                fpath = os.path.join(tmp_dir, fname)
                if os.path.isfile(fpath):
                    if os.path.normpath(fpath) not in in_use:
                        try:
                            os.remove(fpath)
                        except Exception:
                            pass
        except Exception:
            pass

    def closeEvent(self, event):
        self._last_image_paths.clear()
        self._staged_images.clear()
        self._cleanup_unused_clipboard_images()
        super().closeEvent(event)

    def _auto_switch_model(self, keywords, preferred_names, label):
        """
        Shared helper for auto-switching models.
        Returns the index of the matched model, or -1 if none found.
        """
        current = self.model_combo.currentText()

        # Already on a matching model — no switch needed.
        if any(k in current.lower() for k in keywords):
            return self.model_combo.currentIndex()

        # Try preferred model names first (exact match).
        for preferred in preferred_names:
            idx = self.model_combo.findText(preferred)
            if idx >= 0:
                self.model_combo.setCurrentIndex(idx)
                self.chat_display.append(_system_bubble(
                    f"🔄 Auto-switched to {label} model: {preferred}"
                ))
                self._scroll_to_bottom()
                return idx

        # Fallback: any model containing one of the keywords.
        for i in range(self.model_combo.count()):
            name = self.model_combo.itemText(i)
            if any(k in name.lower() for k in keywords):
                self.model_combo.setCurrentIndex(i)
                self.chat_display.append(_system_bubble(
                    f"🔄 Auto-switched to {label} model: {name}"
                ))
                self._scroll_to_bottom()
                return i

        return -1

    def _warn_or_switch_to_vision_model(self) -> bool:
        """Ensure a vision model is active before sending images."""
        # MERGED: uses shared VISION_MODEL_KEYWORDS from chatbot_thread
        preferred = ["llava:latest", "llava", "llava:7b", "llava:13b", "bakllava", "moondream"]
        idx = self._auto_switch_model(VISION_MODEL_KEYWORDS, preferred, "vision")
        if idx >= 0:
            return True
        # No vision model found — block and explain.
        self.chat_display.append(_system_bubble(
            "⚠️ No vision model installed. Image analysis is not possible with the "
            "current model — a text-only model cannot see images and will give "
            "completely wrong answers.\n\n"
            "Install a vision model by running this in a terminal:\n"
            "  ollama pull llava\n\n"
            "Then restart eSim and select llava from the model dropdown."
        ))
        self._scroll_to_bottom()
        return False

    def _switch_to_text_model(self):
        """Auto-switch to qwen2.5 for text queries."""
        self._auto_switch_model(["qwen2.5"], [], "text")

    # ── Settings ─────────────────────────────────────────────────────

    def _on_temp_changed(self, value: int):
        self._temperature = round(value / 100, 2)
        self._temp_label.setText(f"Precision  {self._temperature:.2f}")

    def _on_tok_changed(self, value: int):
        self._num_predict = value * 128
        self._tok_label.setText(f"Max tokens  {self._num_predict}")

    def _reset_settings(self):
        self._temperature = 0.35
        self._num_predict = 1024
        self._temp_slider.setValue(35)
        self._tok_slider.setValue(8)

    # ── Mic ──────────────────────────────────────────────────────────

    def _update_mic_tooltip(self):
        backend = get_stt_backend()
        tips = {
            "whisper": "Speak your question\n✅ Offline STT active (faster-whisper)",
            "vosk": "Speak your question\n✅ Offline STT active (vosk)",
            "google": "Speak your question\n⚠ Online STT only (Google)",
            "none": "Speak your question\n❌ No STT installed",
        }
        self.mic_button.setToolTip(tips.get(backend, "Speak your question"))

    def _on_mic_clicked(self):
        if self._mic_active:
            return
        self._mic_active = True
        self.mic_button.setEnabled(False)
        self.status_label.setText("🎤 Starting microphone…")
        self._mic_worker = MicWorker()
        self._mic_worker.text_signal.connect(self._on_mic_text)
        self._mic_worker.error_signal.connect(self._on_mic_error)
        self._mic_worker.status_signal.connect(self._on_mic_status)
        self._mic_worker.start()

    def _on_mic_status(self, msg: str):
        self.status_label.setText(msg)

    def _on_mic_text(self, text: str):
        self._reset_mic_button()
        self.status_label.setText("")
        self.user_input.setText(text)
        self.user_input.setFocus()

    def _on_mic_error(self, msg: str):
        self._reset_mic_button()
        self.status_label.setText(msg)
        QTimer.singleShot(3500, lambda: self.status_label.setText(""))

    def _reset_mic_button(self):
        self._mic_active = False
        self.mic_button.setEnabled(True)

    # ── Netlist analysis ─────────────────────────────────────────────

    def analyse_netlist(self, netlist_path: str):
        """Alias kept for backward compatibility."""
        self.analyze_specific_netlist(netlist_path)

    def analyze_specific_netlist(self, netlist_path: str):
        """Analyse a .cir.out netlist using structured AI parsing.

        Uses the deterministic fact-extraction pipeline from
        chatbot.netlist_analysis to ground the LLM response,
        reducing hallucination on small local models.
        """
        if not os.path.exists(netlist_path):
            self.chat_display.append(
                f'<table width="100%"><tr><td style="color:#c00;font-size:12px;padding:6px;">'
                f'❌ Netlist file not found: {_escape_text_preserve_breaks(netlist_path)}</td></tr></table>'
            )
            return
        self._current_session_kind = "netlist"
        ts = _get_time()
        filename = os.path.basename(netlist_path)
        self.chat_display.append(_netlist_header_bubble(filename, ts))
        self._scroll_to_bottom()
        try:
            with open(netlist_path, 'r', errors='replace') as f:
                raw_lines = f.readlines()
        except Exception as e:
            self.chat_display.append(
                f'<table width="100%"><tr><td style="color:#c00;font-size:12px;padding:6px;">'
                f'❌ Could not read file: {_escape_text_preserve_breaks(str(e))}</td></tr></table>'
            )
            return

        # Use the structured parser to build a grounded prompt
        try:
            parsed = parse_spice_netlist(raw_lines, netlist_path)
        except Exception as e:
            self.chat_display.append(
                f'<table width="100%"><tr><td style="color:#c00;font-size:12px;padding:6px;">'
                f'Could not parse netlist: {_escape_text_preserve_breaks(str(e))}</td></tr></table>'
            )
            return

        # Offline fallback: if Ollama is unavailable, format the
        # deterministic analysis directly without an LLM call.
        if not is_ollama_running():
            offline_response = format_netlist_analysis_offline(
                parsed, raw_lines
            )
            self.chat_history = [f"User: [Netlist analysis: {filename}]"]
            self.display_response(offline_response)
            return

        # Online path: build a grounding prompt and send to the LLM.
        prompt = build_netlist_summary_prompt(parsed, raw_lines)

        self.chat_history = [f"User: {prompt}"][-20:]
        self._retry_history = list(self.chat_history)
        self._last_user_text = prompt
        self._start_thinking()

        # Launch the text worker with the structured prompt and strict low temperature
        self._launch_text_worker(self.chat_history, system_prompt=NETLIST_SYSTEM_PROMPT, temperature_override=0.1, netlist_formatter_context=parsed)

    # ── Topic switch ─────────────────────────────────────────────────

    def _check_topic_switch(self, new_text: str) -> bool:
        switched = detect_topic_switch(self._last_user_text, new_text)
        if switched and self.chat_history:
            self.chat_history = self.chat_history[-2:]
            self.chat_display.append(_topic_reset_banner())
            self._scroll_to_bottom()
            self._last_image_paths = []
        return switched

    # ── Persistence ──────────────────────────────────────────────────

    def _save_history(self):
        self._save_pending = True
        if not self._save_debounce_timer.isActive():
            self._save_debounce_timer.start(_SAVE_DEBOUNCE_MS)

    def _flush_save(self):
        if not self._save_pending:
            return
        self._save_pending = False
        try:
            os.makedirs(os.path.dirname(_HISTORY_FILE), exist_ok=True)
            with open(_HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.chat_history[-20:], f, ensure_ascii=False, indent=2)
            self._save_current_session()
            self._refresh_sidebar_if_open()
        except Exception:
            pass

    def _save_current_session(self):
        if not self.chat_history:
            return
        try:
            os.makedirs(_SESSIONS_DIR, exist_ok=True)
            session = {
                "id": self._current_session_id,
                "title": self._derive_session_title(),
                "created_at": self._session_created_at,
                "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "messages": self.chat_history[-40:],
                "kind": self._current_session_kind,
                "images": self._images_store,
                "settings": {
                    "temperature": self._temperature,
                    "num_predict": self._num_predict,
                },
            }
            path = os.path.join(_SESSIONS_DIR, f"{self._current_session_id}.json")
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(session, f, ensure_ascii=False, indent=2)
            self._sidebar.upsert_session(session)
        except Exception:
            pass

    def _load_history(self):
        if not os.path.exists(_HISTORY_FILE):
            return
        try:
            with open(_HISTORY_FILE, 'r', encoding='utf-8') as f:
                saved = json.load(f)
            if isinstance(saved, list) and saved:
                title = next(
                    (m[5:].strip()[:50] for m in saved if m.startswith("User:")),
                    "Previous session"
                )
                old_session = {
                    "id":         self._current_session_id,
                    "title":      title,
                    "created_at": self._session_created_at,
                    "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "messages":   saved[-40:],
                    "kind":       "text",
                    "settings": {
                        "temperature": self._temperature,
                        "num_predict": self._num_predict,
                    },
                }
                os.makedirs(_SESSIONS_DIR, exist_ok=True)
                sess_path = os.path.join(
                    _SESSIONS_DIR, f"{self._current_session_id}.json"
                )
                with open(sess_path, 'w', encoding='utf-8') as f:
                    json.dump(old_session, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
        finally:
            try:
                os.remove(_HISTORY_FILE)
            except Exception:
                pass
        self._current_session_id  = str(uuid.uuid4())
        self._session_created_at  = datetime.now().strftime("%Y-%m-%d %H:%M")

    # ── Models ───────────────────────────────────────────────────────

    def _populate_models(self):
        self.model_combo.clear()
        self.model_combo.addItem("Loading models…")
        self.model_combo.setEnabled(False)
        self._model_worker = ModelFetchWorker()
        self._model_worker.result_signal.connect(self._on_models_fetched)
        self._model_worker.start()

    def _on_models_fetched(self, model_names: list):
        self.model_combo.clear()

        if not model_names:
            # No models found — Ollama may be offline or has no models pulled.
            self.model_combo.addItem("No models found")
            self.model_combo.setEnabled(False)
            self.status_label.setText(
                "⚠️ No Ollama models found. Run 'ollama pull qwen2.5-coder' "
                "in a terminal to install one."
            )
            return

        for name in model_names:
            self.model_combo.addItem(name)

        # Try to default to any qwen2.5 variant
        chosen_idx = -1
        for i in range(self.model_combo.count()):
            name = self.model_combo.itemText(i)
            if "qwen2.5" in name.lower():
                chosen_idx = i
                break

        # If no qwen2.5, try some fallback preferred models
        if chosen_idx == -1:
            preferred_fallbacks = ['llava:13b', 'llava:7b', 'llava', 'bakllava']
            for preferred in preferred_fallbacks:
                idx = self.model_combo.findText(preferred)
                if idx >= 0:
                    chosen_idx = idx
                    break

        # If still nothing matched, just use the first available model
        if chosen_idx == -1 and self.model_combo.count() > 0:
            chosen_idx = 0

        if chosen_idx >= 0:
            self.model_combo.setCurrentIndex(chosen_idx)
        self.model_combo.setEnabled(True)

    # ── Thinking / retry / regenerate ────────────────────────────────

    def _start_thinking(self):
        self._is_generating = True
        self.user_input.setEnabled(False)
        self.attach_button.setEnabled(False)
        self.mic_button.setEnabled(False)
        self._staging_area.setEnabled(False)
        self.send_button.hide()
        self.stop_button.show()
        # MERGED: preserve streaming-state reset so live token rendering works
        self._reset_stream_state()
        self._show_typing_bubble()

    def _stop_thinking(self):
        self._is_generating = False
        self._remove_typing_bubble()
        self.status_label.setText("")
        self.user_input.setEnabled(True)
        self.attach_button.setEnabled(True)
        self.mic_button.setEnabled(True)
        self._staging_area.setEnabled(True)
        self.stop_button.hide()
        self.send_button.show()

    def _scroll_to_bottom(self):
        self.chat_display.verticalScrollBar().setValue(
            self.chat_display.verticalScrollBar().maximum()
        )

    def _reset_session_state(self):
        """EXTRACTED: Common session state resets to avoid code duplication across handlers."""
        self.chat_history = []
        self._retry_history = []
        self._bot_responses = {}
        self._response_counter = 0
        self._last_user_text = ""
        self._viewing_past_session = False
        self._clear_staged_images()
        self._images_store = {}
        self._last_image_paths = []
        self._current_session_kind = "text"
        self._current_tips = []
        self._session_title_override = None
        self._current_session_id = str(uuid.uuid4())
        self._session_created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
        # MERGED: also reset streaming-related state so the next message starts clean
        self._reset_stream_state()

    def _launch_text_worker(self, chat_history, system_prompt=None, temperature_override=None, netlist_formatter_context=None):
        """EXTRACTED: Launch OllamaWorker with correct configuration and signal mappings (streaming-aware)."""
        temp = temperature_override if temperature_override is not None else self._temperature
        self.worker = OllamaWorker(
            chat_history,
            model=self.model_combo.currentText(),
            temperature=temp,
            num_predict=self._num_predict,
            system_prompt=system_prompt,
            netlist_formatter_context=netlist_formatter_context
        )
        self.worker.response_signal.connect(self.display_response)
        self.worker.status_signal.connect(self._on_status_update)
        # MERGED: connect chunk stream so live token rendering still works.
        if hasattr(self.worker, "chunk_signal"):
            self.worker.chunk_signal.connect(self._on_stream_chunk)
        self.worker.start()

    def _launch_vision_worker(self, image_paths, extra_prompt):
        """EXTRACTED: Launch OllamaVisionWorker with correct configuration and signal mappings (streaming-aware)."""
        self.worker = OllamaVisionWorker(
            image_paths=image_paths,
            extra_prompt=extra_prompt,
            model=self.model_combo.currentText(),
        )
        self.worker.response_signal.connect(self.display_response)
        self.worker.status_signal.connect(self._on_status_update)
        # MERGED: connect chunk stream so live token rendering still works.
        if hasattr(self.worker, "chunk_signal"):
            self.worker.chunk_signal.connect(self._on_stream_chunk)
        self.worker.start()

    def _stop_generating(self):
        if hasattr(self, 'worker') and self.worker.isRunning():
            self.worker.stop()

    def _retry_response(self, response_idx: int):
        if self._is_generating:
            return
        bot_count = 0
        trim_to = None
        for i, line in enumerate(self.chat_history):
            if line.startswith("Bot:"):
                if bot_count == response_idx:
                    trim_to = i
                    break
                bot_count += 1
        if trim_to is None:
            for i in range(len(self.chat_history) - 1, -1, -1):
                if self.chat_history[i].startswith("Bot:"):
                    trim_to = i
                    break
        if trim_to is None or not any(
            l.startswith("User:") for l in self.chat_history[:trim_to]
        ):
            self.status_label.setText("Nothing to retry.")
            QTimer.singleShot(2000, lambda: self.status_label.setText(""))
            return
        self.chat_history = self.chat_history[:trim_to]
        self._retry_history = list(self.chat_history)
        self._rebuild_chat_html_from_history()
        self._start_thinking()
        last_user = next(
            (l for l in reversed(self.chat_history) if l.startswith("User:")), ""
        )
        followup_paths = [p for p in self._last_image_paths if os.path.exists(p)]
        if followup_paths and "[Image analysis request:" in last_user:
            prompt = last_user.split("\n", 1)[-1].strip() if "\n" in last_user else ""
            # EXTRACTED: helper method to launch OllamaVisionWorker
            self._launch_vision_worker(followup_paths, prompt)
        else:
            # EXTRACTED: helper method to launch OllamaWorker
            self._launch_text_worker(self._retry_history)

    # REMOVED: _retry_last() — legacy shim with no callers found in codebase

    def _regenerate_last_response(self):
        if not self.chat_history:
            return
        if self.chat_history and self.chat_history[-1].startswith("Bot:"):
            self.chat_history.pop()
        if not self.chat_history or not self.chat_history[-1].startswith("User:"):
            self.status_label.setText("No previous user prompt to regenerate.")
            QTimer.singleShot(2500, lambda: self.status_label.setText(""))
            return
        self._retry_history = list(self.chat_history)
        self._rebuild_chat_html_from_history()
        self._start_thinking()

        # EXTRACTED: helper method to launch OllamaWorker
        self._launch_text_worker(self._retry_history)

    def _on_status_update(self, msg: str):
        self.status_label.setText(msg)
        if "Starting Ollama" in msg or "Ollama started" in msg:
            self.chat_display.append(_system_bubble(msg))
            self._scroll_to_bottom()

    # ── Main chat logic ──────────────────────────────────────────────

    def ask_ollama(self):
        user_text = self.user_input.text().strip()
        staged_paths = list(self._staged_images)
        if not user_text and not staged_paths:
            return
        if self._is_generating:
            return

        # Guard: prevent sending when no valid model is available
        selected = self.model_combo.currentText()
        if not selected or selected == "No models found" or selected == "Loading models…":
            self.status_label.setText(
                "⚠️ No model available. Make sure Ollama is running "
                "and you have pulled a model."
            )
            self._populate_models()
            return

        if self._viewing_past_session:
            self._viewing_past_session = False

        editing_text = getattr(self, '_editing_prompt_text', None)
        if editing_text:
            # We are editing an existing prompt. Find it in history and truncate.
            for i in range(len(self.chat_history) - 1, -1, -1):
                msg = self.chat_history[i]
                if msg == f"User: {editing_text}" or msg.endswith(f"\n{editing_text}"):
                    self.chat_history = self.chat_history[:i]
                    self._rebuild_chat_html_from_history()
                    break
            self._editing_prompt_text = None

        ts = _get_time()

        if staged_paths:
            self._current_session_kind = "image"
            if not self._warn_or_switch_to_vision_model():
                self._clear_staged_images()
                return
            fnames = [os.path.basename(p) for p in staged_paths]
            if user_text:
                self.user_input.add_to_history(user_text)
            self.user_input.clear()
            vision_extra_prompt = user_text
            if user_text:
                user_history_text = (
                    f"[Image analysis request: {', '.join(fnames)}]\n{user_text}"
                )
            else:
                user_history_text = (
                    f"[Image analysis request: {', '.join(fnames)}]"
                )
            self.chat_history = (self.chat_history + [f"User: {user_history_text}"])[-20:]
            self._retry_history = list(self.chat_history)
            self._last_user_text = user_text if user_text else "image analysis"

            img_key = ts + "_" + self._current_session_id
            b64_list = []
            for p in staged_paths:
                try:
                    with open(p, "rb") as f_img:
                        raw = f_img.read()
                    try:
                        from PIL import Image as _PI
                        import io as _io2
                        img_obj = _PI.open(_io2.BytesIO(raw))
                        img_obj.thumbnail((320, 240))
                        if img_obj.mode not in ("RGB", "L"):
                            img_obj = img_obj.convert("RGB")
                        buf = _io2.BytesIO()
                        img_obj.save(buf, format="JPEG", quality=75)
                        raw = buf.getvalue()
                    except Exception:
                        pass
                    b64_list.append((os.path.basename(p), base64.b64encode(raw).decode()))
                except Exception:
                    pass
            if b64_list:
                self._images_store[img_key] = b64_list
            if b64_list:
                for fname, b64 in b64_list:
                    self.chat_display.append(_image_thumbnail_html(b64, fname))
            else:
                self.chat_display.append(_staged_images_bubble(fnames, ts))
            if user_text:
                self.chat_display.append(_user_bubble(user_text, ts))
            self._scroll_to_bottom()
            self._last_image_paths = list(staged_paths)
            self._clear_staged_images()

            # Guard: Ollama must be running for vision analysis
            if not is_ollama_running():
                offline_msg = (
                    "**Ollama is not running.**\n\n"
                    "Image analysis requires a running Ollama server with a vision model.\n\n"
                    "To start Ollama, open a terminal and run:\n"
                    "```\nollama serve\n```\n\n"
                    "Then send your message again."
                )
                self.display_response(offline_msg)
                return

            self._start_thinking()

            # EXTRACTED: helper method to launch OllamaVisionWorker
            self._launch_vision_worker(staged_paths, vision_extra_prompt)
            return

        self._check_topic_switch(user_text)

        # The user explicitly requested that any text-only search should
        # switch to the Qwen model. Since Qwen cannot process images,
        # we must drop any previous image context and use the text worker.
        self._last_image_paths.clear()

        self._current_session_kind = "text"
        self._switch_to_text_model()

        self.chat_history = (self.chat_history + [f"User: {user_text}"])[-20:]
        self.chat_display.append(_user_bubble(user_text, ts))
        self._scroll_to_bottom()
        self.user_input.add_to_history(user_text)
        self.user_input.clear()
        self._last_user_text = user_text
        self._retry_history = list(self.chat_history)

        # Guard: Ollama must be running for follow-up chat
        if not is_ollama_running():
            offline_msg = (
                "**Ollama is not running.**\n\n"
                "Follow-up questions and general chat require a running Ollama server.\n\n"
                "To start Ollama, open a terminal and run:\n"
                "```\nollama serve\n```\n\n"
                "Then send your message again.\n\n"
                "*Note: Error analysis and netlist analysis work offline "
                "using the deterministic pipeline — use the toolbar buttons above.*"
            )
            self.display_response(offline_msg)
            return

        self._start_thinking()

        # EXTRACTED: helper method to launch OllamaWorker
        self._launch_text_worker(self.chat_history)

    # ── Window / response / clear ────────────────────────────────────

    def move_to_bottom_right(self):
        screen = QApplication.primaryScreen().availableGeometry()
        widget = self.geometry()
        x = screen.width() - widget.width() - 10
        y = screen.height() - widget.height() - 50
        self.move(x, y)

    def display_response(self, bot_response):
        """
        Final-reply slot. If streaming was active, replace the in-progress
        bubble (located by anchor) with the authoritative final text.
        Otherwise just append a fresh bubble.
        """
        self._stop_thinking()
        ts = self._stream_ts or _get_time()

        if getattr(self, '_current_session_kind', None) == "simulation_error" and getattr(self, '_current_tips', None):
            for tip in self._current_tips:
                bot_response += f"\n\n💡 **eSim Tip:**\n*{tip['fix']}*"

        if self._stream_buf is not None:
            idx = self._stream_idx
            anchor_cursor = self._find_stream_anchor_cursor()
            if anchor_cursor is not None:
                anchor_cursor.movePosition(QTextCursor.End, QTextCursor.KeepAnchor)
                anchor_cursor.removeSelectedText()
                anchor_cursor.insertHtml(_bot_bubble(bot_response, ts, idx))
            else:
                # Anchor lost (shouldn't happen) — append as a fallback.
                self.chat_display.append(_bot_bubble(bot_response, ts, idx))
        else:
            idx = self._response_counter
            self.chat_display.append(_bot_bubble(bot_response, ts, idx))

        self._bot_responses[idx] = bot_response
        self._response_counter = max(self._response_counter, idx + 1)
        self.chat_history.append(f"Bot: {bot_response}")
        self._reset_stream_state()

        self._scroll_to_bottom()
        self._update_ollama_status()

        self._sidebar.upsert_session({
            "id":         self._current_session_id,
            "title":      self._derive_session_title(),
            "created_at": self._session_created_at,
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "messages":   self.chat_history[-40:],
            "kind":       self._current_session_kind,
        })
        self._save_history()

    def clear_session(self):
        self._save_debounce_timer.stop()
        self._save_pending = False
        session_file = os.path.join(_SESSIONS_DIR, f"{self._current_session_id}.json")
        try:
            if os.path.exists(session_file):
                os.remove(session_file)
        except Exception:
            pass
        self.chat_display.setHtml(WELCOME_MESSAGE)
        # MERGED: combined all state resetting into one reusable helper
        self._reset_session_state()

        try:
            if os.path.exists(_HISTORY_FILE):
                os.remove(_HISTORY_FILE)
        except Exception:
            pass
        self._refresh_sidebar_if_open()

    # ── Debug helpers ────────────────────────────────────────────────

    def debug_ollama(self, system_prompt=None, temperature_override=None):
        self._current_session_kind = "simulation_error"
        self.chat_display.append(
            '<table width="100%" cellpadding="0" cellspacing="0"><tr>'
            '<td style="padding:0;">'
            '<div style="background-color:#fff3cd;border-left:4px solid #e0a800;'
            'border-radius:10px;padding:8px 14px;font-size:12px;color:#7a5800;">'
            '<b>⚠️ Simulation Failed</b> — Analyzing error log…'
            '</div></td></tr></table>'
        )
        self._scroll_to_bottom()
        self._retry_history = list(self.chat_history)
        self._start_thinking()
        # EXTRACTED: helper method to launch OllamaWorker
        self._launch_text_worker(self.chat_history, system_prompt=system_prompt, temperature_override=temperature_override)
        self.user_input.clear()

    def debug_error(self, log):
        """Analyse an NgSpice error log using structured AI parsing.

        Uses the deterministic fact-extraction pipeline from
        chatbot.error_log_analysis to ground the LLM response,
        reducing hallucination on small local models.
        """
        self.setWindowFlags(self.windowFlags())
        self.show()
        self.raise_()
        self.activateWindow()
        self.chat_history = []
        self._current_session_kind = "simulation_error"
        if os.path.exists(log):
            with open(log, "r") as f:
                lines = [ln for ln in f.readlines() if ln.strip()]

            if not lines:
                self.chat_display.append(
                    '<table width="100%"><tr><td style="color:#c00;font-size:12px;padding:6px;">'
                    '❌ Error log is empty.</td></tr></table>'
                )
                return

            self.status_label.setText(
                f"Analysing error log ({len(lines)} lines)..."
            )

            # Offline fallback: if Ollama is unavailable, format the
            # deterministic analysis directly without an LLM call.
            if not is_ollama_running():
                offline_response = format_error_analysis_offline(lines)
                self._current_tips = []  # fixes are already in the response
                self.chat_history = [f"User: [Error log analysis]"]
                self.status_label.setText("")
                self.display_response(offline_response)
                return

            # Online path: build a grounding prompt and send to the LLM.
            prompt, tips = build_error_analysis_prompt(lines)
            self._current_tips = tips

            self.chat_history = [f"User: {prompt}"]
            
            # DEBUG DUMP
            try:
                with open(os.path.join(self.projDir, "debug_prompt.txt"), "w") as df:
                    df.write(prompt)
            except Exception:
                pass
            
            self.debug_ollama(system_prompt=ERROR_ANALYSIS_SYSTEM_PROMPT, temperature_override=0.1)
