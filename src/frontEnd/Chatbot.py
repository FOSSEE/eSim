# =============================================================================
# Chatbot.py  —  eSim AI Assistant
#
# UI  : ChatGPT/Claude-style interface (bubbles, sidebar with date groups)
# Backend: RAG / OCR / netlist-analysis / ESIMCopilotWrapper pipeline
# STT : faster-whisper (offline) → vosk → Google (online fallback)
#
# SESSION MODEL (how it works like GPT/Claude):
#   • Every conversation is a separate JSON file in ~/.esim/chat_sessions/
#   • _current_session_id always points to the active session
#   • Clicking a past session in the sidebar SWITCHES into it fully —
#     its messages load into self.chat_history and its ID becomes current
#   • New messages always append to self.chat_history and save to the
#     current session file — no cross-session contamination
#   • "New Chat" saves current session and creates a fresh one
# =============================================================================

import sys
import os
import re
import json
import uuid
import subprocess
import tempfile
from datetime import datetime, date, timedelta
from configuration.Appconfig import Appconfig

# ── PyQt5 ─────────────────────────────────────────────────────────────────────
from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QTextBrowser, QLineEdit,
    QPushButton, QLabel, QComboBox, QApplication, QFileDialog,
    QListWidget, QListWidgetItem, QFrame, QScrollArea,
    QSlider, QMessageBox, QInputDialog, QDockWidget
)
from PyQt5.QtCore import QSize, QTimer, Qt, pyqtSignal, QThread
from PyQt5.QtGui import QTextCursor, QKeyEvent, QPixmap

# ── Path setup ─────────────────────────────────────────────────────────────────
if os.name == 'nt':
    try:
        from frontEnd import pathmagic  # noqa
    except ImportError:
        pass
else:
    try:
        import pathmagic  # noqa
    except ImportError:
        pass

current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir     = os.path.dirname(current_dir)
if src_dir not in sys.path:
    sys.path.append(src_dir)

# ── Backend ────────────────────────────────────────────────────────────────────
from chatbot.chatbot_core import ESIMCopilotWrapper, clear_history

# ── STT ────────────────────────────────────────────────────────────────────────
try:
    import speech_recognition as sr
    _SR_AVAILABLE = True
except ImportError:
    _SR_AVAILABLE = False

try:
    from faster_whisper import WhisperModel
    _WHISPER_AVAILABLE = True
except ImportError:
    _WHISPER_AVAILABLE = False

try:
    import vosk
    import json as _json
    _VOSK_AVAILABLE = True
except ImportError:
    _VOSK_AVAILABLE = False

# ── Storage ────────────────────────────────────────────────────────────────────
_ESIM_DIR     = os.path.join(os.path.expanduser('~'), '.esim')
_SESSIONS_DIR = os.path.join(_ESIM_DIR, 'chat_sessions')
_LAST_SID_FILE = os.path.join(_ESIM_DIR, 'last_session_id.txt')
_IMG_FILTER   = "Images (*.png *.jpg *.jpeg *.bmp *.gif *.tiff)"

# ── Netlist contract ───────────────────────────────────────────────────────────
MANUALS_DIR = os.path.join(os.path.dirname(__file__), "manuals")
NETLIST_CONTRACT = ""
try:
    with open(os.path.join(MANUALS_DIR, "esim_netlist_analysis_output_contract.txt"),
              "r", encoding="utf-8") as f:
        NETLIST_CONTRACT = f.read()
    print("[COPILOT] Netlist contract loaded.")
except Exception as e:
    print(f"[COPILOT] WARNING: {e}")
    NETLIST_CONTRACT = (
        "You are a SPICE netlist analyzer.\n"
        "Use the FACT lines to detect issues.\n"
        "Output sections:\n"
        "1. Syntax / SPICE rule errors\n"
        "2. Topology / connection problems\n"
        "3. Simulation setup issues (.ac/.tran/.op etc.)\n"
        "4. Summary\n"
        "Do NOT invent issues not present in FACT lines.\n"
    )


# =============================================================================
#  NETLIST DETECTOR FUNCTIONS
# =============================================================================

def _validate_netlist_with_ngspice(netlist_text: str) -> bool:
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.cir',
                                         delete=False, encoding='utf-8') as tmp:
            tmp.write(netlist_text)
            tmp_path = tmp.name
        result = subprocess.run(['ngspice', '-b', tmp_path],
                                capture_output=True, text=True, timeout=5)
        try:
            os.unlink(tmp_path)
        except Exception:
            pass
        stderr_lower = result.stderr.lower()
        syntax_errors   = ['syntax error', 'unrecognized', 'parse error', 'fatal']
        ignore_patterns = ['model', 'library', 'warning', 'no such file', 'cannot find']
        for line in stderr_lower.split('\n'):
            if any(p in line for p in ignore_patterns):
                continue
            if any(e in line for e in syntax_errors):
                return False
        return True
    except Exception:
        return True


def _detect_missing_subcircuits(netlist_text: str) -> list:
    referenced, defined = {}, set()
    for ln, line in enumerate(netlist_text.split('\n'), 1):
        line = line.strip()
        if not line or line.startswith('*'):
            continue
        if line.lower().startswith('.subckt'):
            t = line.split()
            if len(t) >= 2:
                defined.add(t[1].upper())
        elif line.lower().startswith(('.include', '.lib')):
            return []
        elif line[0].upper() == 'X':
            t = line.split()
            if len(t) < 2:
                continue
            name = t[-1].upper()
            if '=' in name:
                for tok in reversed(t[1:]):
                    if '=' not in tok:
                        name = tok.upper(); break
            referenced.setdefault(name, []).append((ln, t[0]))
    return [(s, o) for s, o in referenced.items() if s not in defined]


def _detect_voltage_source_conflicts(netlist_text: str) -> list:
    vsources = {}
    for ln, line in enumerate(netlist_text.split('\n'), 1):
        line = line.strip()
        if not line or line.startswith('*') or line.startswith('.'):
            continue
        t = line.split()
        if len(t) < 4 or t[0][0].upper() != 'V':
            continue
        np_ = re.sub(r'[^\w\-_]', '', t[1])
        nm_ = re.sub(r'[^\w\-_]', '', t[2])
        np_ = '0' if np_.lower() in ['0', 'gnd', 'ground', 'vss'] else np_
        nm_ = '0' if nm_.lower() in ['0', 'gnd', 'ground', 'vss'] else nm_
        pair = tuple(sorted([np_, nm_]))
        val = "?"
        for i, tok in enumerate(t[3:], 3):
            tu = tok.upper()
            if tu in ['DC', 'AC', 'PULSE', 'SIN', 'PWL']:
                val = t[i + 1] if i + 1 < len(t) else "?"
                break
            elif not tu.startswith('.'):
                val = tok; break
        vsources.setdefault(pair, []).append((ln, t[0], val))
    return [(p, s) for p, s in vsources.items() if len(s) > 1]


def _netlist_ground_info(netlist_text: str):
    has0 = has_gnd = False
    for line in netlist_text.split('\n'):
        line = line.strip()
        if not line or line.startswith('*') or line.startswith('.'):
            continue
        t = line.split()
        if len(t) < 3:
            continue
        et = t[0][0].upper()
        nodes = []
        if et in ['R', 'C', 'L', 'V', 'I', 'D']:
            nodes = [t[1], t[2]]
        elif et == 'Q' and len(t) >= 4:
            nodes = [t[1], t[2], t[3]]
        elif et in ['M', 'S'] and len(t) >= 5:
            nodes = t[1:5]
        elif et == 'X' and len(t) >= 3:
            nodes = t[1:-1]
        for n in nodes:
            n = re.sub(r'[=\(\)].*$', '', n)
            n = re.sub(r'[^\w\-_]', '', n)
            if n.lower() == '0':
                has0 = True
            if n.lower() in ['gnd', 'ground', 'vss']:
                has_gnd = True
    return has0, has_gnd


def _detect_floating_nodes(netlist_text: str) -> list:
    counts = {}
    for ln, line in enumerate(netlist_text.split('\n'), 1):
        line = line.strip()
        if not line or line.startswith('*') or line.startswith('.'):
            continue
        t = line.split()
        if len(t) < 3:
            continue
        et = t[0][0].upper()
        nodes = []
        if et in ['R', 'C', 'L', 'V', 'I', 'D']:
            nodes = [t[1], t[2]]
        elif et == 'Q' and len(t) >= 4:
            nodes = t[1:4]
        elif et in ['M', 'S'] and len(t) >= 5:
            nodes = t[1:5]
        elif et in ['T', 'E', 'G'] and len(t) >= 5:
            nodes = t[1:5]
        elif et in ['H', 'F', 'B'] and len(t) >= 3:
            nodes = [t[1], t[2]]
        elif et == 'X' and len(t) >= 3:
            nodes = [x for x in t[1:-1] if '=' not in x]
        for n in nodes:
            n = re.sub(r'[=\(\)].*$', '', n)
            n = re.sub(r'[^\w\-_]', '', n)
            if not n or n[0].isdigit():
                continue
            if n.upper() in ['VALUE', 'V', 'I', 'IF', 'THEN', 'ELSE']:
                continue
            if n.lower() in ['0', 'gnd', 'ground', 'vss']:
                n = '0'
            counts.setdefault(n, []).append((ln, t[0]))
    return [(nd, occ[0][0], occ[0][1]) for nd, occ in counts.items()
            if len(occ) == 1 and nd != '0']


def _detect_missing_models(netlist_text: str) -> list:
    referenced, defined = {}, set()
    for ln, line in enumerate(netlist_text.split('\n'), 1):
        line = line.strip()
        if not line or line.startswith('*'):
            continue
        if line.lower().startswith('.model'):
            t = line.split()
            if len(t) >= 2:
                defined.add(t[1].upper())
        elif line.lower().startswith(('.include', '.lib')):
            return []
        elif line[0].upper() in ['D', 'Q', 'M', 'J']:
            t = line.split()
            et = t[0][0].upper()
            if et == 'D' and len(t) >= 4:
                referenced.setdefault(t[3].upper(), []).append((ln, t[0]))
            elif et == 'Q' and len(t) >= 5:
                m = t[-1].upper()
                if not m[0].isdigit():
                    referenced.setdefault(m, []).append((ln, t[0]))
            elif et == 'M' and len(t) >= 6:
                referenced.setdefault(t[5].upper(), []).append((ln, t[0]))
    return [(m, o) for m, o in referenced.items() if m not in defined]


# =============================================================================
#  STT
# =============================================================================

_whisper_model = None

def _get_whisper_model():
    global _whisper_model
    if _whisper_model is None:
        _whisper_model = WhisperModel("base", device="cpu", compute_type="int8")
    return _whisper_model

def _is_online() -> bool:
    try:
        import socket
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except OSError:
        return False

def get_stt_backend() -> str:
    if _is_online() and _SR_AVAILABLE:
        return "google"
    if _WHISPER_AVAILABLE:
        return "whisper"
    if _VOSK_AVAILABLE:
        return "vosk"
    if _SR_AVAILABLE:
        return "google"
    return "none"


# =============================================================================
#  WORKER THREADS
# =============================================================================

class ChatWorker(QThread):
    response_ready = pyqtSignal(str)

    def __init__(self, user_input, copilot):
        super().__init__()
        self.user_input      = user_input
        self.copilot         = copilot
        self._stop_requested = False

    def stop(self):
        self._stop_requested = True

    def run(self):
        try:
            response = self.copilot.handle_input(self.user_input)
            self.response_ready.emit(response)
        except Exception as e:
            self.response_ready.emit(f"❌ Error: {e}")


class MicWorker(QThread):
    text_signal   = pyqtSignal(str)
    error_signal  = pyqtSignal(str)
    status_signal = pyqtSignal(str)

    def run(self):
        backend = get_stt_backend()
        if backend == "none":
            self.error_signal.emit("No STT library. pip install faster-whisper SpeechRecognition pyaudio")
            return
        if not _SR_AVAILABLE:
            self.error_signal.emit("pip install SpeechRecognition pyaudio")
            return
        try:
            r = sr.Recognizer()
            r.energy_threshold         = 100
            r.dynamic_energy_threshold = True
            r.pause_threshold          = 1.5
            r.phrase_threshold         = 0.1
            r.non_speaking_duration    = 0.5
            with sr.Microphone() as source:
                self.status_signal.emit("🎤 Adjusting for noise…")
                r.adjust_for_ambient_noise(source, duration=0.3)
                self.status_signal.emit("🎤 Listening… speak now")
                audio = r.listen(source, timeout=10, phrase_time_limit=30)
        except sr.WaitTimeoutError:
            self.error_signal.emit("🎤 No speech detected."); return
        except OSError:
            self.error_signal.emit("🎤 Mic not found."); return
        except Exception as e:
            self.error_signal.emit(f"🎤 Mic error: {e}"); return

        if backend == "whisper":
            self._whisper(audio)
        elif backend == "vosk":
            self._vosk(audio)
        else:
            self._google(audio)

    def _whisper(self, audio):
        try:
            self.status_signal.emit("🎤 Transcribing offline…")
            model = _get_whisper_model()
            wav   = audio.get_wav_data(convert_rate=16000, convert_width=2)
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                tmp.write(wav); tmp_path = tmp.name
            try:
                segs, _ = model.transcribe(tmp_path, language="en", beam_size=1, vad_filter=True)
                text = " ".join(s.text for s in segs).strip()
            finally:
                try: os.remove(tmp_path)
                except: pass
            if text: self.text_signal.emit(text)
            else: self.error_signal.emit("🎤 Could not understand.")
        except Exception:
            if _SR_AVAILABLE: self._google(audio)
            else: self.error_signal.emit("🎤 Whisper error.")

    def _vosk(self, audio):
        try:
            dirs = [os.path.join(os.path.expanduser("~"), ".vosk", "model"),
                    os.path.join(os.path.expanduser("~"), "vosk-model"), "vosk-model"]
            model_dir = next((d for d in dirs if os.path.isdir(d)), None)
            if not model_dir: self._google(audio); return
            self.status_signal.emit("🎤 Transcribing (vosk)…")
            rec = vosk.KaldiRecognizer(vosk.Model(model_dir), 16000)
            rec.AcceptWaveform(audio.get_wav_data(convert_rate=16000, convert_width=2))
            text = _json.loads(rec.FinalResult()).get("text", "").strip()
            if text: self.text_signal.emit(text)
            else: self.error_signal.emit("🎤 Could not understand.")
        except Exception:
            self._google(audio)

    def _google(self, audio):
        try:
            self.status_signal.emit("🎤 Processing (online)…")
            text = sr.Recognizer().recognize_google(audio)
            if text: self.text_signal.emit(text)
            else: self.error_signal.emit("🎤 Could not understand.")
        except sr.UnknownValueError:
            self.error_signal.emit("🎤 Could not understand.")
        except Exception as e:
            self.error_signal.emit(f"🎤 Online STT failed: {e}")


# =============================================================================
#  UI HELPERS
# =============================================================================

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
    <div style="display:inline-block;background:#f5f5f5;border-radius:12px;
        padding:10px 18px;font-size:11px;color:#999;margin:0 auto;">
        Use the sidebar ≡ to access past chats
    </div>
</div><br>
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
        '<table cellpadding="0" cellspacing="0"><tr><td style="padding:0;">'
        '<div style="background-color:#f0f4f8;color:#0078d4;'
        'padding:11px 20px;border-radius:20px 20px 20px 5px;'
        'font-size:18px;line-height:1;border:1px solid #d0dce8;">'
        f'{dots}</div></td></tr></table></td>'
        '<td width="20%"></td></tr></table>'
    )


def _render_inline(text):
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'`([^`]+)`',
        r'<span style="font-family:Consolas,monospace;background-color:#e8ecf0;'
        r'padding:1px 4px;border-radius:3px;">\1</span>', text)
    return text.replace('\n', '<br>')


def _render_markdown(text):
    result, last = [], 0
    for m in re.compile(r'```(\w*)\n?(.*?)```', re.DOTALL).finditer(text):
        if text[last:m.start()]:
            result.append(_render_inline(text[last:m.start()]))
        lang = m.group(1) or 'code'
        code = (m.group(2)
                .replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
                .replace('\n','<br>').replace(' ','&nbsp;'))
        label = f'<span style="color:#888;font-size:10px;">{lang}</span><br>' if lang else ''
        result.append(
            '<table width="98%" cellpadding="0" cellspacing="3"><tr><td style="padding:0;">'
            '<div style="background-color:#1e1e1e;color:#d4d4d4;'
            'font-family:Consolas,Courier New,monospace;font-size:12px;'
            'padding:10px 14px;border-radius:10px;border-left:3px solid #0078d4;">'
            f'{label}{code}</div></td></tr></table>'
        )
        last = m.end()
    if text[last:]:
        result.append(_render_inline(text[last:]))
    return ''.join(result)


def _get_time():
    return datetime.now().strftime("%H:%M")


def _user_bubble(text, timestamp=""):
    safe = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    ts_part = f' &nbsp;·&nbsp; {timestamp}' if timestamp else ''
    return (
        '<table width="100%" cellpadding="0" cellspacing="0"><tr>'
        '<td width="20%"></td>'
        '<td align="right" style="padding:4px 10px 0 0;">'
        '<table cellpadding="0" cellspacing="2"><tr>'
        '<td style="background-color:#0095f6;color:white;'
        'padding:11px 16px;border-radius:20px 20px 5px 20px;'
        'font-size:13px;line-height:1.6;">'
        f'{safe}</td></tr>'
        f'<tr><td align="right" style="color:#bbb;font-size:10px;'
        f'padding:3px 2px 8px 0;">You{ts_part}</td></tr>'
        '</table></td></tr></table>'
    )


def _bot_bubble(text, timestamp="", response_idx=0):
    rendered  = _render_markdown(text)
    ts_part   = f' &nbsp;·&nbsp; {timestamp}' if timestamp else ''
    copy_href = f'copy://{response_idx}'
    up_href   = f'feedback://up/{response_idx}'
    down_href = f'feedback://down/{response_idx}'
    return (
        '<table width="100%" cellpadding="0" cellspacing="0"><tr>'
        '<td align="left" style="padding:4px 0 0 10px;">'
        '<table cellpadding="0" cellspacing="2"><tr>'
        '<td style="background-color:#f0f0f0;color:#1a1a2e;'
        'padding:11px 16px;border-radius:20px 20px 20px 5px;'
        'font-size:13px;line-height:1.6;">'
        f'{rendered}</td></tr>'
        '<tr><td>'
        '<table width="100%" cellpadding="0" cellspacing="0"><tr>'
        f'<td align="left" style="color:#999;font-size:10px;padding:3px 0 8px 2px;">'
        f'eSim AI{ts_part}</td>'
        f'<td align="right" style="padding:3px 4px 8px 0;">'
        f'<a href="{up_href}" style="color:#28a745;font-size:12px;text-decoration:none;margin-right:6px;">&#128077;</a>'
        f'<a href="{down_href}" style="color:#dc3545;font-size:12px;text-decoration:none;margin-right:8px;">&#128078;</a>'
        f'<a href="{copy_href}" style="color:#0095f6;font-size:10px;text-decoration:none;">Copy</a></td>'
        '</tr></table></td></tr></table>'
        '</td><td width="20%"></td></tr></table>'
    )


def _system_bubble(text):
    return (
        '<table width="100%" cellpadding="0" cellspacing="0"><tr>'
        '<td align="center" style="padding:4px 8px;">'
        '<div style="background-color:#fff8e1;color:#7a5800;'
        'border:1px solid #ffc107;border-radius:14px;'
        'padding:7px 16px;font-size:11px;font-style:italic;">'
        f'{text}</div></td></tr></table>'
    )


def _netlist_header_bubble(filename, timestamp):
    safe = filename.replace('&', '&amp;').replace('<', '&lt;')
    return (
        '<table width="100%" cellpadding="0" cellspacing="0"><tr>'
        '<td width="5%"></td>'
        '<td align="right" style="padding:2px 6px;">'
        '<table cellpadding="0" cellspacing="0"><tr><td style="padding:0;">'
        '<div style="background-color:#fff3e0;color:#b85c00;'
        'padding:6px 14px;border-radius:16px 16px 4px 16px;'
        'font-size:11px;border:1px solid #f0c080;">'
        f'📄 Netlist: {safe}</div></td></tr>'
        f'<tr><td align="right" style="color:#aaa;font-size:10px;'
        f'padding:1px 2px 6px 0;">You &nbsp;·&nbsp; {timestamp}</td></tr>'
        '</table></td></tr></table>'
    )


def _section_header_html(title):
    """Date group header for the chat display (not sidebar)."""
    return (
        '<table width="100%" cellpadding="4" cellspacing="0"><tr>'
        '<td align="center" style="color:#aaa;font-size:10px;'
        'border-top:1px dashed #d0dce8;padding-top:6px;">'
        f'— {title} —</td></tr></table>'
    )


# =============================================================================
#  SMART INPUT (Up/Down history)
# =============================================================================

class _HistoryLineEdit(QLineEdit):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self._sent_history = []
        self._hist_idx     = -1
        self._draft        = ''

    def add_to_history(self, text):
        if text and (not self._sent_history or self._sent_history[-1] != text):
            self._sent_history.append(text)
        self._hist_idx = -1

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Up and self._sent_history:
            if self._hist_idx == -1:
                self._draft    = self.text()
                self._hist_idx = len(self._sent_history) - 1
            elif self._hist_idx > 0:
                self._hist_idx -= 1
            self.setText(self._sent_history[self._hist_idx]); self.end(False)
        elif event.key() == Qt.Key_Down and self._hist_idx >= 0:
            self._hist_idx += 1
            if self._hist_idx >= len(self._sent_history):
                self._hist_idx = -1
                self.setText(self._draft)
            else:
                self.setText(self._sent_history[self._hist_idx])
            self.end(False)
        else:
            super().keyPressEvent(event)


# =============================================================================
#  SESSION ITEM WIDGET
# =============================================================================

class _SessionItemWidget(QWidget):
    delete_requested = pyqtSignal(str)

    def __init__(self, session_id, title, preview="", active=False, parent=None):
        super().__init__(parent)
        self.session_id = session_id
        self.title      = title
        self.setMinimumHeight(46)

        outer = QHBoxLayout(self)
        outer.setContentsMargins(14, 5, 8, 5)
        outer.setSpacing(0)

        text_col = QVBoxLayout()
        text_col.setSpacing(2)
        text_col.setContentsMargins(0, 0, 0, 0)

        color = "#0095f6" if active else "#1a1a2e"
        weight = "600" if active else "500"
        title_lbl = QLabel(title[:38] + ("…" if len(title) > 38 else ""))
        title_lbl.setStyleSheet(
            f"font-size:13px;font-weight:{weight};color:{color};background:transparent;"
        )
        text_col.addWidget(title_lbl)

        ptext = (preview[:44] + "…") if len(preview) > 44 else preview
        prev_lbl = QLabel(ptext or "")
        prev_lbl.setStyleSheet("font-size:11px;color:#aaa;background:transparent;")
        text_col.addWidget(prev_lbl)
        outer.addLayout(text_col, 1)

        del_btn = QPushButton("⋯")
        del_btn.setFixedSize(22, 22)
        del_btn.setStyleSheet("""
            QPushButton { font-size:13px;color:#ccc;background:transparent;border:none;border-radius:11px; }
            QPushButton:hover { background:#ffe0e0;color:#cc0000; }
        """)
        del_btn.clicked.connect(self._confirm_delete)
        outer.addWidget(del_btn)

    def _confirm_delete(self):
        if QMessageBox.question(self, "Delete", f"Delete '{self.title}'?",
                                QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            self.delete_requested.emit(self.session_id)


# =============================================================================
#  CHAT SIDEBAR
# =============================================================================

class ChatSidebar(QWidget):
    new_chat_requested = pyqtSignal()
    session_selected   = pyqtSignal(str)   # emits session_id
    session_deleted    = pyqtSignal(str)   # emits session_id

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(260)
        self._active_session_id = None
        self.setStyleSheet("QWidget { background:#ffffff; border-right:1px solid #ececec; }")

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Header
        top = QWidget()
        top.setFixedHeight(52)
        top.setStyleSheet("QWidget { background:#ffffff;border-bottom:1px solid #f0f0f0; }")
        top_row = QHBoxLayout(top)
        top_row.setContentsMargins(14, 0, 10, 0)
        top_row.setSpacing(8)
        lbl = QLabel("Chats")
        lbl.setStyleSheet("font-size:16px;font-weight:700;color:#1a1a2e;background:transparent;")
        top_row.addWidget(lbl, 1)
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(26, 26)
        close_btn.setStyleSheet("""
            QPushButton { font-size:11px;color:#888;background:transparent;border:none;border-radius:13px; }
            QPushButton:hover { background:#f0f0f0;color:#333; }
        """)
        close_btn.clicked.connect(self.hide)
        top_row.addWidget(close_btn)
        root.addWidget(top)

        # New chat button
        btn_w = QWidget()
        btn_w.setStyleSheet("QWidget { background:#ffffff; }")
        btn_l = QHBoxLayout(btn_w)
        btn_l.setContentsMargins(12, 8, 12, 8)
        self.new_btn = QPushButton("+ New Chat")
        self.new_btn.setFixedHeight(36)
        self.new_btn.setStyleSheet("""
            QPushButton { font-size:12px;font-weight:600;background:#0095f6;color:white;border:none;border-radius:18px; }
            QPushButton:hover { background:#0082d8; }
            QPushButton:pressed { background:#006ab8; }
        """)
        self.new_btn.clicked.connect(self.new_chat_requested)
        btn_l.addWidget(self.new_btn)
        root.addWidget(btn_w)

        sep = QFrame(); sep.setFrameShape(QFrame.HLine)
        sep.setFixedHeight(1)
        sep.setStyleSheet("QFrame { background:#f0f0f0;border:none; }")
        root.addWidget(sep)

        self.session_list = QListWidget()
        self.session_list.setSpacing(0)
        self.session_list.setStyleSheet("""
            QListWidget { background:#ffffff;border:none;outline:0; }
            QListWidget::item { border:none;padding:0; }
            QListWidget::item:hover { background:#f5f8ff; }
            QListWidget::item:selected { background:#eaf3ff; }
        """)
        self.session_list.itemClicked.connect(self._on_item_clicked)
        root.addWidget(self.session_list)

        self._empty_lbl = QLabel("No saved chats yet.\nStart a conversation!")
        self._empty_lbl.setAlignment(Qt.AlignCenter)
        self._empty_lbl.setStyleSheet("QLabel { color:#ccc;font-size:12px;padding:30px 10px;background:transparent; }")
        self._empty_lbl.setWordWrap(True)
        self._empty_lbl.hide()
        root.addWidget(self._empty_lbl)

    def set_active_session(self, session_id: str):
        self._active_session_id = session_id

    def populate(self):
        self.session_list.clear()
        if not os.path.exists(_SESSIONS_DIR):
            self._empty_lbl.show(); return

        sessions = []
        for fname in os.listdir(_SESSIONS_DIR):
            if not fname.endswith('.json'):
                continue
            try:
                with open(os.path.join(_SESSIONS_DIR, fname), encoding='utf-8') as f:
                    sessions.append(json.load(f))
            except Exception:
                pass

        if not sessions:
            self._empty_lbl.show(); return
        self._empty_lbl.hide()

        sessions.sort(key=lambda s: s.get('updated_at', ''), reverse=True)

        today_s     = date.today().strftime("%Y-%m-%d")
        yesterday_s = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        week_s      = (date.today() - timedelta(days=7)).strftime("%Y-%m-%d")
        month_s     = (date.today() - timedelta(days=30)).strftime("%Y-%m-%d")

        groups = [
            ("Today",            []),
            ("Yesterday",        []),
            ("Previous 7 days",  []),
            ("Previous 30 days", []),
            ("Older",            []),
        ]
        for s in sessions:
            d = s.get('updated_at', '')[:10]
            if d == today_s:         groups[0][1].append(s)
            elif d == yesterday_s:   groups[1][1].append(s)
            elif d >= week_s:        groups[2][1].append(s)
            elif d >= month_s:       groups[3][1].append(s)
            else:                    groups[4][1].append(s)

        for group_name, group_sessions in groups:
            if not group_sessions:
                continue
            # Section header (non-selectable)
            hdr = QListWidgetItem(self.session_list)
            hdr.setFlags(Qt.NoItemFlags)
            hdr.setSizeHint(QSize(240, 28))
            hdr_w = QLabel(group_name)
            hdr_w.setStyleSheet(
                "font-size:10px;font-weight:600;color:#aaa;letter-spacing:0.5px;"
                "padding:6px 14px 2px 14px;background:transparent;"
            )
            self.session_list.setItemWidget(hdr, hdr_w)

            for s in group_sessions:
                sid     = s['id']
                title   = s.get('title', 'New chat')
                msgs    = s.get('messages', [])
                preview = next((m[5:].strip() for m in msgs if m.startswith("User:")), "")
                active  = (sid == self._active_session_id)

                item = QListWidgetItem(self.session_list)
                item.setData(Qt.UserRole, sid)
                item.setSizeHint(QSize(240, 50))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)

                widget = _SessionItemWidget(sid, title, preview, active, self.session_list)
                widget.delete_requested.connect(self._delete_session)
                self.session_list.setItemWidget(item, widget)

    def _on_item_clicked(self, item):
        sid = item.data(Qt.UserRole)
        if sid:
            self.session_selected.emit(sid)

    def _delete_session(self, session_id: str):
        path = os.path.join(_SESSIONS_DIR, f"{session_id}.json")
        try:
            if os.path.exists(path):
                os.remove(path)
        except Exception:
            pass
        self.session_deleted.emit(session_id)
        self.populate()


# =============================================================================
#  SESSION MANAGER  — pure data, no UI
# =============================================================================

class SessionManager:
    """Handles all session file I/O so ChatbotGUI stays clean."""

    @staticmethod
    def load(session_id: str) -> dict:
        path = os.path.join(_SESSIONS_DIR, f"{session_id}.json")
        try:
            with open(path, encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}

    @staticmethod
    def save(session_id: str, title: str, created_at: str,
             messages: list, feedback: dict):
        try:
            os.makedirs(_SESSIONS_DIR, exist_ok=True)
            path = os.path.join(_SESSIONS_DIR, f"{session_id}.json")
            with open(path, 'w', encoding='utf-8') as f:
                json.dump({
                    "id":         session_id,
                    "title":      title,
                    "created_at": created_at,
                    "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "messages":   messages[-40:],
                    "feedback":   feedback,
                }, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    @staticmethod
    def delete(session_id: str):
        try:
            path = os.path.join(_SESSIONS_DIR, f"{session_id}.json")
            if os.path.exists(path):
                os.remove(path)
        except Exception:
            pass

    @staticmethod
    def save_last_sid(session_id: str):
        try:
            os.makedirs(_ESIM_DIR, exist_ok=True)
            with open(_LAST_SID_FILE, 'w') as f:
                f.write(session_id)
        except Exception:
            pass

    @staticmethod
    def load_last_sid() -> str:
        try:
            with open(_LAST_SID_FILE) as f:
                return f.read().strip()
        except Exception:
            return ""


# =============================================================================
#  MAIN ChatbotGUI
# =============================================================================

class ChatbotGUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("eSim AI Assistant")
        self.setMinimumSize(420, 350)

        self.copilot        = ESIMCopilotWrapper()
        self.worker         = None
        self._project_dir   = None
        self._generation_id = 0

        # ── Active session state ──────────────────────────────────────
        # These ALWAYS reflect the currently active session.
        # Switching sessions updates ALL of these atomically.
        self._current_session_id   = str(uuid.uuid4())
        self._session_created_at   = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.chat_history          = []   # list of "User: ..." / "Bot: ..." strings
        self._feedback             = {}

        # ── UI helpers ────────────────────────────────────────────────
        self._bot_responses    = {}   # idx → response text (for Copy/feedback)
        self._response_counter = 0
        self._last_user_text   = ""
        self._retry_history    = []
        self._typing_frame     = 0
        self._typing_start_pos = -1
        self._mic_active       = False
        self._staged_images    = []
        self._temperature      = 0.35
        self._num_predict      = 1024

        # ── Timers ────────────────────────────────────────────────────
        self._thinking_timer    = QTimer(self)
        self._thinking_timer.timeout.connect(self._animate_thinking)
        self._typing_anim_timer = QTimer(self)
        self._typing_anim_timer.timeout.connect(self._animate_typing_bubble)
        self._status_poll_timer = QTimer(self)
        self._status_poll_timer.timeout.connect(self._update_ollama_status)
        self._status_poll_timer.start(5000)

        # Toast
        self._toast = QLabel("  ✅  Copied!  ", self)
        self._toast.setStyleSheet("""
            QLabel { background-color:#1a1a2e;color:#ffffff;
                font-size:12px;font-weight:bold;border-radius:14px;padding:4px 14px; }
        """)
        self._toast.setAlignment(Qt.AlignCenter)
        self._toast.hide()

        self._build_ui()
        self._restore_last_session()

    # =========================================================================
    #  BUILD UI
    # =========================================================================

    def _build_ui(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Sidebar
        self._sidebar = ChatSidebar(self)
        self._sidebar.new_chat_requested.connect(self._new_chat)
        self._sidebar.session_selected.connect(self._switch_to_session)
        self._sidebar.session_deleted.connect(self._on_session_deleted)
        self._sidebar.hide()
        root.addWidget(self._sidebar)

        # Main area
        chat_container = QWidget()
        cl = QVBoxLayout(chat_container)
        cl.setContentsMargins(8, 8, 8, 8)
        cl.setSpacing(5)
        root.addWidget(chat_container, 1)

        # Header
        header = QHBoxLayout()
        header.setSpacing(5)

        hist_btn = QPushButton("≡")
        hist_btn.setFixedSize(32, 32)
        hist_btn.setToolTip("Chat history")
        hist_btn.setStyleSheet("""
            QPushButton { font-size:16px;border:none;border-radius:8px;background:transparent;color:#555; }
            QPushButton:hover { background:#f0f0f0;color:#1a1a2e; }
            QPushButton:pressed { background:#e0e0e0; }
        """)
        hist_btn.clicked.connect(self._toggle_sidebar)
        header.addWidget(hist_btn)

        self.model_combo = QComboBox(self)
        self.model_combo.setFixedHeight(30)
        self.model_combo.setStyleSheet("""
            QComboBox { font-size:12px;padding:2px 10px;border:1px solid #e0e0e0;
                border-radius:8px;background:#f7f7f7;color:#1a1a2e; }
            QComboBox:focus { border:1px solid #0095f6;background:#fff; }
            QComboBox::drop-down { border:none;width:18px; }
        """)
        self.model_combo.addItem("qwen2.5-coder:1.5b (RAG)")
        self.model_combo.addItem("tinyllama:1.1b (RAG)")
        self.model_combo.addItem("qwen2.5-coder:3b (RAG)")
        header.addWidget(self.model_combo)

        settings_btn = QPushButton("⚙")
        settings_btn.setFixedSize(28, 28)
        settings_btn.setCheckable(True)
        settings_btn.setStyleSheet("""
            QPushButton { font-size:14px;border:none;border-radius:8px;background:transparent;color:#555; }
            QPushButton:hover { background:#f0f0f0; }
            QPushButton:checked { background:#e8f0ff;color:#0095f6; }
        """)
        settings_btn.toggled.connect(lambda on: self._settings_panel.setVisible(on))
        header.addWidget(settings_btn)
        header.addStretch()

        self.analyze_netlist_btn = QPushButton("Netlist ▶")
        self.analyze_netlist_btn.setFixedHeight(28)
        self.analyze_netlist_btn.setToolTip("Analyze active project netlist")
        self.analyze_netlist_btn.setCursor(Qt.PointingHandCursor)
        self.analyze_netlist_btn.setStyleSheet("""
            QPushButton { font-size:11px;font-weight:600;padding:0 12px;
                background-color:#2ecc71;color:white;border:none;border-radius:14px; }
            QPushButton:hover { background-color:#27ae60; }
            QPushButton:pressed { background-color:#1e8449; }
            QPushButton:disabled { background-color:#a9dfbf;color:#fff; }
        """)
        self.analyze_netlist_btn.clicked.connect(self.analyze_current_netlist)
        header.addWidget(self.analyze_netlist_btn)

        self.ollama_status_label = QLabel(self)
        self.ollama_status_label.setFixedHeight(24)
        header.addWidget(self.ollama_status_label)
        self._update_ollama_status()

        sep = QFrame(); sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("color:#ececec;margin:0;")
        cl.addLayout(header)
        cl.addWidget(sep)

        # Chat display
        self.chat_display = QTextBrowser(self)
        self.chat_display.setOpenLinks(False)
        self.chat_display.setHtml(WELCOME_MESSAGE)
        self.chat_display.anchorClicked.connect(self._handle_link_click)
        self.chat_display.setStyleSheet("""
            QTextBrowser { background-color:#fafafa;border:none;padding:8px 4px;
                font-family:'Segoe UI',Arial,sans-serif;font-size:13px;
                selection-background-color:#cce4f7; }
            QScrollBar:vertical { background:transparent;width:6px;border-radius:3px; }
            QScrollBar::handle:vertical { background:#d0d0d0;border-radius:3px;min-height:24px; }
            QScrollBar::handle:vertical:hover { background:#a0a0a0; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height:0px; }
        """)
        cl.addWidget(self.chat_display)

        # Status row
        status_row = QHBoxLayout()
        self.status_label = QLabel("", self)
        self.status_label.setStyleSheet(
            "color:#0095f6;font-size:11px;padding:1px 4px;background:transparent;"
        )
        status_row.addWidget(self.status_label)
        status_row.addStretch()
        self.retry_button = QPushButton("Retry", self)
        self.retry_button.setFixedHeight(26)
        self.retry_button.setStyleSheet("""
            QPushButton { font-size:11px;padding:2px 10px;background:#fff3e0;
                color:#b85c00;border:1px solid #f0c080;border-radius:13px; }
            QPushButton:hover { background:#ffe0b2; }
        """)
        self.retry_button.clicked.connect(self._retry_last)
        self.retry_button.hide()
        status_row.addWidget(self.retry_button)
        cl.addLayout(status_row)

        # Settings panel
        self._settings_panel = QWidget()
        self._settings_panel.setVisible(False)
        self._settings_panel.setStyleSheet("""
            QWidget { background:#f7f9fc;border-top:1px solid #ececec;border-bottom:1px solid #ececec; }
        """)
        sp = QHBoxLayout(self._settings_panel)
        sp.setContentsMargins(12, 8, 12, 8)
        sp.setSpacing(16)

        temp_col = QVBoxLayout(); temp_col.setSpacing(2)
        self._temp_label = QLabel(f"Precision  {self._temperature:.2f}")
        self._temp_label.setStyleSheet("font-size:10px;color:#555;background:transparent;")
        temp_col.addWidget(self._temp_label)
        self._temp_slider = QSlider(Qt.Horizontal)
        self._temp_slider.setRange(1, 100)
        self._temp_slider.setValue(int(self._temperature * 100))
        self._temp_slider.setFixedWidth(110)
        self._temp_slider.valueChanged.connect(self._on_temp_changed)
        self._temp_slider.setStyleSheet("""
            QSlider::groove:horizontal { height:4px;background:#ddd;border-radius:2px; }
            QSlider::handle:horizontal { width:14px;height:14px;margin:-5px 0;background:#0095f6;border-radius:7px; }
            QSlider::sub-page:horizontal { background:#0095f6;border-radius:2px; }
        """)
        temp_col.addWidget(self._temp_slider)
        sp.addLayout(temp_col)

        tok_col = QVBoxLayout(); tok_col.setSpacing(2)
        self._tok_label = QLabel(f"Max tokens  {self._num_predict}")
        self._tok_label.setStyleSheet("font-size:10px;color:#555;background:transparent;")
        tok_col.addWidget(self._tok_label)
        self._tok_slider = QSlider(Qt.Horizontal)
        self._tok_slider.setRange(1, 40)
        self._tok_slider.setValue(self._num_predict // 128)
        self._tok_slider.setFixedWidth(110)
        self._tok_slider.valueChanged.connect(self._on_tok_changed)
        self._tok_slider.setStyleSheet("""
            QSlider::groove:horizontal { height:4px;background:#ddd;border-radius:2px; }
            QSlider::handle:horizontal { width:14px;height:14px;margin:-5px 0;background:#0095f6;border-radius:7px; }
            QSlider::sub-page:horizontal { background:#0095f6;border-radius:2px; }
        """)
        tok_col.addWidget(self._tok_slider)
        sp.addLayout(tok_col)
        sp.addStretch()
        reset_btn = QPushButton("Reset")
        reset_btn.setFixedHeight(26)
        reset_btn.setStyleSheet("""
            QPushButton { font-size:10px;padding:2px 12px;background:#f0f0f0;
                color:#555;border:none;border-radius:13px; }
            QPushButton:hover { background:#e0e0e0; }
        """)
        reset_btn.clicked.connect(self._reset_settings)
        sp.addWidget(reset_btn)
        cl.addWidget(self._settings_panel)

        # Input row
        input_row = QHBoxLayout()
        input_row.setSpacing(5)

        self.attach_button = QPushButton("📎")
        self.attach_button.setFixedSize(38, 38)
        self.attach_button.setToolTip("Attach image")
        self.attach_button.setStyleSheet("""
            QPushButton { font-size:16px;background:#f0f0f0;border:none;border-radius:19px; }
            QPushButton:hover { background:#e0e8ff; }
            QPushButton:disabled { background:#f5f5f5;color:#ccc; }
        """)
        self.attach_button.clicked.connect(self._pick_image)
        input_row.addWidget(self.attach_button)

        self.mic_button = QPushButton("🎤")
        self.mic_button.setFixedSize(38, 38)
        self.mic_button.setToolTip("Speak your question")
        self.mic_button.setStyleSheet("""
            QPushButton { font-size:15px;background:#f0f0f0;border:none;border-radius:19px; }
            QPushButton:hover { background:#d0f8d0; }
            QPushButton:disabled { background:#f5f5f5;color:#ccc; }
        """)
        self.mic_button.clicked.connect(self._on_mic_clicked)
        QTimer.singleShot(200, self._update_mic_tooltip)
        input_row.addWidget(self.mic_button)

        self.user_input = _HistoryLineEdit(
            self, placeholderText="Message eSim AI…  (↑↓ for history)"
        )
        self.user_input.setStyleSheet("""
            QLineEdit { font-size:13px;padding:9px 14px;border:1.5px solid #e0e0e0;
                border-radius:22px;background:#f7f7f7;color:#1a1a2e; }
            QLineEdit:focus { border:1.5px solid #0095f6;background:#ffffff; }
            QLineEdit:disabled { background:#efefef;color:#ccc; }
        """)
        self.user_input.returnPressed.connect(self.send_message)
        input_row.addWidget(self.user_input)

        self.send_button = QPushButton("Send")
        self.send_button.setFixedHeight(38)
        self.send_button.setStyleSheet("""
            QPushButton { font-size:13px;font-weight:600;padding:5px 20px;
                background-color:#0095f6;color:white;border:none;border-radius:19px; }
            QPushButton:hover { background-color:#0082d8; }
            QPushButton:disabled { background-color:#d0d0d0;color:#fff; }
        """)
        self.send_button.clicked.connect(self.send_message)
        input_row.addWidget(self.send_button)

        self.stop_button = QPushButton("Stop")
        self.stop_button.setFixedHeight(38)
        self.stop_button.setStyleSheet("""
            QPushButton { font-size:13px;font-weight:600;padding:5px 16px;
                background-color:#ff3b30;color:white;border:none;border-radius:19px; }
            QPushButton:hover { background-color:#e0302a; }
        """)
        self.stop_button.clicked.connect(self._stop_generating)
        self.stop_button.hide()
        input_row.addWidget(self.stop_button)

        self.clear_button = QPushButton("Clear")
        self.clear_button.setFixedHeight(38)
        self.clear_button.setStyleSheet("""
            QPushButton { font-size:13px;padding:5px 14px;background-color:#f0f0f0;
                color:#666;border:none;border-radius:19px; }
            QPushButton:hover { background-color:#ffe0e0;color:#cc0000; }
            QPushButton:disabled { background-color:#f5f5f5;color:#bbb; }
        """)
        self.clear_button.clicked.connect(self._clear_current_session_ui)
        input_row.addWidget(self.clear_button)
        cl.addLayout(input_row)

        # Image staging strip
        self._staging_area = QWidget()
        self._staging_area.setStyleSheet("QWidget { background:#f5f8ff;border-radius:10px; }")
        self._staging_area.setVisible(False)
        sa_layout = QVBoxLayout(self._staging_area)
        sa_layout.setContentsMargins(6, 6, 6, 4)
        sa_layout.setSpacing(4)
        sa_header = QHBoxLayout()
        sa_lbl = QLabel("Images to send:")
        sa_lbl.setStyleSheet("font-size:11px;color:#555;background:transparent;")
        sa_header.addWidget(sa_lbl)
        sa_header.addStretch()
        ca_btn = QPushButton("Remove all")
        ca_btn.setFixedHeight(20)
        ca_btn.setStyleSheet("""
            QPushButton { font-size:10px;color:#cc0000;background:transparent;border:none;padding:0 4px; }
            QPushButton:hover { text-decoration:underline; }
        """)
        ca_btn.clicked.connect(self._clear_staged_images)
        sa_header.addWidget(ca_btn)
        sa_layout.addLayout(sa_header)
        scroll = QScrollArea()
        scroll.setFixedHeight(72)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border:none;background:transparent; }")
        self._thumb_container = QWidget()
        self._thumb_container.setStyleSheet("background:transparent;")
        self._thumb_row = QHBoxLayout(self._thumb_container)
        self._thumb_row.setContentsMargins(0, 0, 0, 0)
        self._thumb_row.setSpacing(6)
        self._thumb_row.addStretch()
        scroll.setWidget(self._thumb_container)
        sa_layout.addWidget(scroll)
        cl.addWidget(self._staging_area)

    # =========================================================================
    #  SESSION SWITCHING  — the core of proper history isolation
    # =========================================================================

    def _restore_last_session(self):
        """On startup, restore the last active session (if any)."""
        last_sid = SessionManager.load_last_sid()
        if last_sid:
            data = SessionManager.load(last_sid)
            if data:
                self._load_session_data(last_sid, data)
                self._render_session(show_banner=False)
                return
        # No previous session — show welcome
        self.chat_display.setHtml(WELCOME_MESSAGE)

    def _switch_to_session(self, session_id: str):
        """Switch the active session to session_id. Called from sidebar click."""
        if session_id == self._current_session_id:
            # Already on this session — just close sidebar
            self._sidebar.hide()
            return

        # Save the current session before switching away
        self._save_current_session()

        # Load the target session
        data = SessionManager.load(session_id)
        if not data:
            return

        self._load_session_data(session_id, data)
        self._render_session(show_banner=True)

        # Update sidebar highlight
        self._sidebar.set_active_session(session_id)
        self._sidebar.populate()

        SessionManager.save_last_sid(session_id)

    def _load_session_data(self, session_id: str, data: dict):
        """Atomically load session data into all instance variables."""
        self._current_session_id = session_id
        self._session_created_at = data.get('created_at', datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.chat_history        = list(data.get('messages', []))
        self._feedback           = dict(data.get('feedback', {}))
        self._last_user_text     = next(
            (m[5:].strip() for m in reversed(self.chat_history) if m.startswith("User:")), ""
        )
        self._retry_history      = list(self.chat_history)

    def _render_session(self, show_banner: bool = False):
        """Re-render self.chat_history into the chat display."""
        html = WELCOME_MESSAGE
        if show_banner:
            title   = next((m[5:].strip()[:50] for m in self.chat_history
                            if m.startswith("User:")), "Chat")
            created = self._session_created_at
            html += (
                '<table width="100%" cellpadding="0" cellspacing="0"><tr>'
                '<td align="center" style="padding:6px 8px;">'
                '<div style="background-color:#f0f4ff;color:#0055a5;'
                'border:1px solid #b0c4e8;border-radius:12px;'
                'padding:8px 16px;font-size:11px;">'
                f'📂 Switched to: <b>{title}</b> &nbsp;·&nbsp; {created}'
                '</div></td></tr></table><br>'
            )

        for line in self.chat_history:
            if line.startswith("User:"):
                html += _user_bubble(line[5:].strip())
            elif line.startswith("Bot:"):
                idx = self._response_counter
                self._response_counter += 1
                self._bot_responses[idx] = line[4:].strip()
                html += _bot_bubble(line[4:].strip(), "", idx)

        self.chat_display.setHtml(html)
        QTimer.singleShot(120, lambda:
            self.chat_display.verticalScrollBar().setValue(
                self.chat_display.verticalScrollBar().maximum()
            )
        )

    # =========================================================================
    #  NEW CHAT / CLEAR
    # =========================================================================

    def _new_chat(self):
        """Save current session and start a fresh one."""
        self._save_current_session()

        self._current_session_id = str(uuid.uuid4())
        self._session_created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.chat_history        = []
        self._feedback           = {}
        self._bot_responses      = {}
        self._response_counter   = 0
        self._last_user_text     = ""
        self._retry_history      = []

        self.chat_display.setHtml(WELCOME_MESSAGE)
        self.retry_button.hide()
        self._clear_staged_images()

        self._sidebar.set_active_session(self._current_session_id)
        self._sidebar.populate()
        SessionManager.save_last_sid(self._current_session_id)

    def _clear_current_session_ui(self):
        """Clear messages from current session (keep session ID, reset messages)."""
        self.chat_history      = []
        self._feedback         = {}
        self._bot_responses    = {}
        self._response_counter = 0
        self._last_user_text   = ""
        self._retry_history    = []
        self.retry_button.hide()
        self._clear_staged_images()
        self.chat_display.setHtml(WELCOME_MESSAGE)
        # Overwrite session file with empty messages
        self._save_current_session()
        self._refresh_sidebar_if_open()

    # =========================================================================
    #  SEND MESSAGE
    # =========================================================================

    def send_message(self):
        user_text    = self.user_input.text().strip()
        staged_paths = list(self._staged_images)

        if not user_text and not staged_paths:
            return

        ts = _get_time()

        if staged_paths:
            fnames = [os.path.basename(p) for p in staged_paths]
            self.chat_display.append(_user_bubble("📎 " + ", ".join(fnames), ts))
            if user_text:
                self.chat_display.append(_user_bubble(user_text, ts))
            self._scroll_to_bottom()
            self.user_input.add_to_history(user_text)
            self.user_input.clear()
            self._clear_staged_images()
            self._dispatch(f"[Image: {staged_paths[0]}] {user_text}".strip())
            return

        # Topic switch detection
        if self._last_user_text:
            try:
                from chatbot.chatbot_thread import detect_topic_switch
                if detect_topic_switch(self._last_user_text, user_text) and self.chat_history:
                    self.chat_history = self.chat_history[-2:]
                    self.chat_display.append(
                        '<table width="100%" cellpadding="4" cellspacing="0"><tr>'
                        '<td align="center" style="color:#aaa;font-size:10px;'
                        'border-top:1px dashed #d0dce8;padding-top:6px;">'
                        '— New topic —</td></tr></table>'
                    )
            except ImportError:
                pass

        # Append to current session
        self.chat_history = (self.chat_history + [f"User: {user_text}"])[-20:]
        self.chat_display.append(_user_bubble(user_text, ts))
        self._scroll_to_bottom()
        self.user_input.add_to_history(user_text)
        self.user_input.clear()
        self._last_user_text = user_text
        self._retry_history  = list(self.chat_history)
        self._dispatch(user_text)

    # =========================================================================
    #  DISPATCH / RESPONSE
    # =========================================================================

    def _is_busy(self) -> bool:
        if self.worker and self.worker.isRunning():
            QMessageBox.warning(self, "Busy", "Please wait for current response.")
            return True
        return False

    def _dispatch(self, full_query: str):
        self._start_thinking()
        self._generation_id += 1
        gen = self._generation_id
        if self.worker and self.worker.isRunning():
            self.worker.quit()
            self.worker.wait(300)
        self.worker = ChatWorker(full_query, self.copilot)
        self.worker.response_ready.connect(lambda resp, g=gen: self._on_response(resp, g))
        self.worker.start()

    def _on_response(self, response: str, gen_id: int):
        self._stop_thinking()
        if gen_id != self._generation_id:
            return
        ts  = _get_time()
        idx = self._response_counter
        self._response_counter += 1
        self._bot_responses[idx] = response
        self.chat_display.append(_bot_bubble(response, ts, idx))
        self.chat_history.append(f"Bot: {response}\n")
        self._scroll_to_bottom()
        self._save_current_session()
        self._update_ollama_status()
        self._refresh_sidebar_if_open()
        if response.startswith("❌") or response.startswith("⚠️"):
            self.retry_button.show()
        else:
            self.retry_button.hide()

    # =========================================================================
    #  PERSISTENCE
    # =========================================================================

    def _save_current_session(self):
        title = next((m[5:].strip()[:50] for m in self.chat_history
                      if m.startswith("User:")), "New chat")
        SessionManager.save(
            self._current_session_id, title,
            self._session_created_at,
            self.chat_history, self._feedback
        )
        SessionManager.save_last_sid(self._current_session_id)

    # =========================================================================
    #  SESSION DELETED
    # =========================================================================

    def _on_session_deleted(self, deleted_id: str):
        if deleted_id == self._current_session_id:
            # The active session was deleted — start fresh
            self._new_chat()

    # =========================================================================
    #  NETLIST
    # =========================================================================

    def set_project_context(self, project_dir: str):
        if project_dir and os.path.isdir(project_dir):
            self._project_dir = project_dir
            self.chat_display.append(_system_bubble(f"Project: {os.path.basename(project_dir)}"))
        else:
            self._project_dir = None
            self.chat_display.append(_system_bubble("Project context cleared."))
        self._scroll_to_bottom()

    def _build_netlist_query(self, netlist_path: str):
        try:
            with open(netlist_path, "r", encoding="utf-8", errors="ignore") as f:
                netlist_text = f.read()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to read netlist:\n{e}")
            return None

        is_ok   = _validate_netlist_with_ngspice(netlist_text)
        floats  = _detect_floating_nodes(netlist_text)
        mmodels = _detect_missing_models(netlist_text)
        msubckt = _detect_missing_subcircuits(netlist_text)
        vconfl  = _detect_voltage_source_conflicts(netlist_text)
        tl      = netlist_text.lower()
        has_tran, has_ac, has_op = ".tran" in tl, ".ac" in tl, ".op" in tl
        has0, has_gnd = _netlist_ground_info(netlist_text)

        fd = "; ".join([f"{n}(line {l},{e})" for n,l,e in floats]) or "NONE"
        md = "; ".join([f"{m}(x{len(o)})" for m,o in mmodels]) or "NONE"
        sd = "; ".join([f"{s}(x{len(o)})" for s,o in msubckt]) or "NONE"
        vd = "; ".join([f"{p}: {','.join(f'{nm}={v}' for _,nm,v in srcs)}"
                        for p,srcs in vconfl]) if vconfl else "NONE"

        facts = "\n".join(f"[FACT {f}]" for f in [
            f"NET_SYNTAX_VALID={'YES' if is_ok else 'NO'}",
            f"NET_HAS_NODE_0={'YES' if has0 else 'NO'}",
            f"NET_HAS_GND_LABEL={'YES' if has_gnd else 'NO'}",
            f"NET_HAS_TRAN={'YES' if has_tran else 'NO'}",
            f"NET_HAS_AC={'YES' if has_ac else 'NO'}",
            f"NET_HAS_OP={'YES' if has_op else 'NO'}",
            f"FLOATING_NODES={fd}", f"MISSING_MODELS={md}",
            f"MISSING_SUBCKTS={sd}", f"VOLTAGE_CONFLICTS={vd}",
        ])
        return (
            f"{NETLIST_CONTRACT}\n\n=== NETLIST FACTS ===\n{facts}\n\n"
            f"=== RAW NETLIST ===\n[ESIM_NETLIST_START]\n{netlist_text}\n"
            "[ESIM_NETLIST_END]\n\nDo NOT invent issues not in FACT lines."
        )

    def analyze_current_netlist(self):
        if self._is_busy(): return
        if not self._project_dir:
            try:
                ac = Appconfig()
                ap = ac.current_project.get("ProjectName")
                if ap and os.path.isdir(ap):
                    self._project_dir = ap
            except Exception:
                pass
        if not self._project_dir:
            QMessageBox.warning(self, "No project", "No active project set."); return
        proj_name = os.path.basename(self._project_dir)
        try:
            all_files = os.listdir(self._project_dir)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Cannot read project:\n{e}"); return
        candidates = [f for f in all_files if f.endswith('.cir') or f.endswith('.cir.out')]
        if not candidates:
            QMessageBox.warning(self, "Not found", "No .cir files found."); return
        path = None
        for pref in [proj_name + ".cir.out", proj_name + ".cir"]:
            if pref in candidates:
                path = os.path.join(self._project_dir, pref); break
        if not path:
            if len(candidates) == 1:
                path = os.path.join(self._project_dir, candidates[0])
            else:
                item, ok = QInputDialog.getItem(self, "Select netlist", "Choose:", candidates, 0, False)
                if ok and item:
                    path = os.path.join(self._project_dir, item)
        if not path: return
        self.chat_display.append(_netlist_header_bubble(os.path.basename(path), _get_time()))
        self._scroll_to_bottom()
        query = self._build_netlist_query(path)
        if query: self._dispatch(query)

    def analyze_specific_netlist(self, netlist_path: str):
        if self._is_busy(): return
        if not os.path.exists(netlist_path):
            QMessageBox.warning(self, "Not found", f"File not found:\n{netlist_path}"); return
        self.chat_display.append(_netlist_header_bubble(os.path.basename(netlist_path), _get_time()))
        self._scroll_to_bottom()
        query = self._build_netlist_query(netlist_path)
        if query: self._dispatch(query)

    def debug_error(self, error_log_path: str):
        if not error_log_path or not os.path.exists(error_log_path): return
        try:
            with open(error_log_path, "r", encoding="utf-8", errors="ignore") as f:
                log_text = f.read()
        except Exception:
            return
        self.chat_display.append(_system_bubble("⚠️ Simulation error — analysing…"))
        self._scroll_to_bottom()
        self._dispatch(
            "The following is an ngspice error log from an eSim simulation.\n"
            "1) Explain the root cause simply.\n"
            "2) Give step-by-step fix instructions for eSim.\n\n"
            f"[NGSPICE_ERROR_LOG_START]\n{log_text}\n[NGSPICE_ERROR_LOG_END]"
        )

    # =========================================================================
    #  THINKING / TYPING BUBBLE
    # =========================================================================

    def _animate_thinking(self):
        pass

    def _start_thinking(self):
        self._thinking_timer.start(500)
        self.user_input.setEnabled(False)
        self.attach_button.setEnabled(False)
        self.mic_button.setEnabled(False)
        self.send_button.hide()
        self.stop_button.show()
        self.clear_button.setEnabled(False)
        if hasattr(self, "analyze_netlist_btn"):
            self.analyze_netlist_btn.setEnabled(False)
        self.retry_button.hide()
        self._show_typing_bubble()

    def _stop_thinking(self):
        self._thinking_timer.stop()
        self._remove_typing_bubble()
        self.status_label.setText("")
        self.user_input.setEnabled(True)
        self.attach_button.setEnabled(True)
        self.mic_button.setEnabled(True)
        self.stop_button.hide()
        self.send_button.show()
        self.clear_button.setEnabled(True)
        if hasattr(self, "analyze_netlist_btn"):
            self.analyze_netlist_btn.setEnabled(True)

    def _show_typing_bubble(self):
        self._typing_frame     = 0
        self._typing_start_pos = self.chat_display.document().characterCount() - 1
        cursor = QTextCursor(self.chat_display.document())
        cursor.movePosition(QTextCursor.End)
        cursor.insertHtml(_typing_bubble(0))
        self._scroll_to_bottom()
        self._typing_anim_timer.start(400)

    def _animate_typing_bubble(self):
        self._typing_frame = (self._typing_frame + 1) % 3
        cursor = QTextCursor(self.chat_display.document())
        cursor.setPosition(self._typing_start_pos)
        cursor.movePosition(QTextCursor.End, QTextCursor.KeepAnchor)
        cursor.insertHtml(_typing_bubble(self._typing_frame))
        self._scroll_to_bottom()

    def _remove_typing_bubble(self):
        self._typing_anim_timer.stop()
        if self._typing_start_pos >= 0:
            cursor = QTextCursor(self.chat_display.document())
            cursor.setPosition(self._typing_start_pos)
            cursor.movePosition(QTextCursor.End, QTextCursor.KeepAnchor)
            cursor.removeSelectedText()
            self._typing_start_pos = -1

    def _scroll_to_bottom(self):
        self.chat_display.verticalScrollBar().setValue(
            self.chat_display.verticalScrollBar().maximum()
        )

    def _stop_generating(self):
        if self.worker and self.worker.isRunning():
            self.worker.stop()

    def _retry_last(self):
        if not self._retry_history: return
        self.retry_button.hide()
        last_user = next((m[5:].strip() for m in reversed(self._retry_history)
                          if m.startswith("User:")), "")
        if last_user:
            self._dispatch(last_user)

    # =========================================================================
    #  OLLAMA STATUS
    # =========================================================================

    def _update_ollama_status(self):
        try:
            import socket
            socket.create_connection(("localhost", 11434), timeout=0.5).close()
            running = True
        except Exception:
            running = False
        if running:
            self.ollama_status_label.setText("🟢 Live")
            self.ollama_status_label.setStyleSheet("""
                QLabel { font-size:11px;font-weight:bold;padding:2px 10px;
                    border-radius:12px;background-color:#e6f9ee;color:#1a7f3c;border:1px solid #a3d9b5; }
            """)
        else:
            self.ollama_status_label.setText("🔴 Offline")
            self.ollama_status_label.setStyleSheet("""
                QLabel { font-size:11px;font-weight:bold;padding:2px 10px;
                    border-radius:12px;background-color:#fdecea;color:#b71c1c;border:1px solid #f5c0bc; }
            """)

    # =========================================================================
    #  SIDEBAR
    # =========================================================================

    def _toggle_sidebar(self):
        if self._sidebar.isVisible():
            self._sidebar.hide()
        else:
            self._sidebar.set_active_session(self._current_session_id)
            self._sidebar.populate()
            self._sidebar.show()

    def _refresh_sidebar_if_open(self):
        if self._sidebar.isVisible():
            self._sidebar.set_active_session(self._current_session_id)
            self._sidebar.populate()

    # =========================================================================
    #  LINK CLICK
    # =========================================================================

    def _handle_link_click(self, url):
        scheme = url.scheme()
        if scheme == 'copy':
            try:
                text = self._bot_responses.get(int(url.host()), "")
                if text:
                    QApplication.clipboard().setText(text)
                    self._show_toast("  ✅  Copied!  ")
            except Exception:
                pass
        elif scheme == 'feedback':
            direction = url.host()
            try:
                idx = int(url.path().strip('/').split('/')[0])
            except Exception:
                return
            self._feedback[idx] = direction
            self._show_toast(f"  {'👍' if direction=='up' else '👎'}  Thanks!  ")
            self._save_current_session()

    def _show_toast(self, text: str):
        self._toast.setText(text)
        cr = self.chat_display.geometry()
        tw, th = 120, 30
        self._toast.setGeometry(
            cr.x() + (cr.width() - tw) // 2,
            cr.y() + cr.height() - th - 16, tw, th
        )
        self._toast.show(); self._toast.raise_()
        QTimer.singleShot(1600, self._toast.hide)

    # =========================================================================
    #  IMAGE STAGING
    # =========================================================================

    def _pick_image(self):
        paths, _ = QFileDialog.getOpenFileNames(self, "Select Images", "", _IMG_FILTER)
        for path in paths:
            if path and path not in self._staged_images:
                self._staged_images.append(path)
        if self._staged_images:
            self._refresh_staging_strip()

    def _refresh_staging_strip(self):
        while self._thumb_row.count() > 1:
            item = self._thumb_row.takeAt(0)
            if item.widget(): item.widget().deleteLater()
        for path in self._staged_images:
            self._thumb_row.insertWidget(self._thumb_row.count() - 1, self._make_thumbnail(path))
        self._staging_area.setVisible(bool(self._staged_images))

    def _make_thumbnail(self, image_path: str) -> QWidget:
        card = QWidget(); card.setFixedSize(80, 64)
        card.setStyleSheet("QWidget { background:#ffffff;border:1px solid #d0d8f0;border-radius:10px; }")
        cl = QVBoxLayout(card); cl.setContentsMargins(4, 4, 4, 2); cl.setSpacing(2)
        thumb = QLabel(); thumb.setAlignment(Qt.AlignCenter); thumb.setFixedHeight(36)
        pix = QPixmap(image_path)
        if not pix.isNull():
            thumb.setPixmap(pix.scaled(68, 36, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            thumb.setText("🖼"); thumb.setStyleSheet("font-size:20px;background:transparent;")
        cl.addWidget(thumb)
        fname = os.path.basename(image_path)
        nl = QLabel(fname[:10] + ("…" if len(fname) > 10 else ""))
        nl.setAlignment(Qt.AlignCenter)
        nl.setStyleSheet("font-size:9px;color:#555;background:transparent;")
        cl.addWidget(nl)
        rem = QPushButton("✕", card); rem.setFixedSize(16, 16); rem.move(62, 2)
        rem.setStyleSheet("""
            QPushButton { font-size:9px;font-weight:bold;background:#ff3b30;color:white;
                border:none;border-radius:8px;padding:0; }
            QPushButton:hover { background:#cc2a22; }
        """)
        rem.clicked.connect(lambda checked, p=image_path: self._remove_staged_image(p))
        return card

    def _remove_staged_image(self, path: str):
        if path in self._staged_images: self._staged_images.remove(path)
        self._refresh_staging_strip()

    def _clear_staged_images(self):
        self._staged_images.clear(); self._refresh_staging_strip()

    # =========================================================================
    #  MIC
    # =========================================================================

    def _update_mic_tooltip(self):
        tips = {
            "whisper": "🎤 Speak  ✅ Offline (Whisper)",
            "google":  "🎤 Speak  🌐 Online (Google)",
            "vosk":    "🎤 Speak  ✅ Offline (vosk)",
            "none":    "🎤 No STT — pip install faster-whisper",
        }
        self.mic_button.setToolTip(tips.get(get_stt_backend(), "Speak"))

    def _on_mic_clicked(self):
        if self._mic_active: return
        self._mic_active = True
        self.mic_button.setEnabled(False)
        self.mic_button.setStyleSheet("""
            QPushButton { font-size:15px;background:#d0f8d0;border:2px solid #28a745;border-radius:18px; }
        """)
        self.status_label.setText("🎤 Starting microphone…")
        self._mic_worker = MicWorker()
        self._mic_worker.text_signal.connect(self._on_mic_text)
        self._mic_worker.error_signal.connect(self._on_mic_error)
        self._mic_worker.status_signal.connect(lambda msg: self.status_label.setText(msg))
        self._mic_worker.start()

    def _on_mic_text(self, text: str):
        self._reset_mic_button(); self.status_label.setText("")
        cur = self.user_input.text().strip()
        self.user_input.setText((cur + " " + text) if cur else text)
        self.user_input.setFocus()

    def _on_mic_error(self, msg: str):
        self._reset_mic_button(); self.status_label.setText(msg)
        QTimer.singleShot(3500, lambda: self.status_label.setText(""))

    def _reset_mic_button(self):
        self._mic_active = False
        self.mic_button.setEnabled(True)
        self.mic_button.setStyleSheet("""
            QPushButton { font-size:15px;background:#f0f0f0;border:none;border-radius:19px; }
            QPushButton:hover { background:#d0f8d0; }
        """)

    # =========================================================================
    #  SETTINGS
    # =========================================================================

    def _on_temp_changed(self, value: int):
        self._temperature = round(value / 100, 2)
        self._temp_label.setText(f"Precision  {self._temperature:.2f}")

    def _on_tok_changed(self, value: int):
        self._num_predict = value * 128
        self._tok_label.setText(f"Max tokens  {self._num_predict}")

    def _reset_settings(self):
        self._temperature = 0.35; self._num_predict = 1024
        self._temp_slider.setValue(35); self._tok_slider.setValue(8)

    # =========================================================================
    #  SHUTDOWN
    # =========================================================================

    def closeEvent(self, event):
        self._save_current_session()
        if self.worker and self.worker.isRunning():
            self.worker.quit(); self.worker.wait(500)
        try: clear_history()
        except Exception: pass
        event.accept()


# =============================================================================
#  DOCK FACTORY
# =============================================================================

def createchatbotdock(parent=None):
    dock = QDockWidget("🤖 eSim AI Assistant", parent)
    dock.setAllowedAreas(Qt.RightDockWidgetArea | Qt.LeftDockWidgetArea)
    dock.setWidget(ChatbotGUI(parent))
    return dock

def create_chatbot_dock(parent=None):
    return createchatbotdock(parent)


# =============================================================================
#  STANDALONE TEST
# =============================================================================

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ChatbotGUI()
    w.resize(700, 620)
    w.show()
    sys.exit(app.exec_())
