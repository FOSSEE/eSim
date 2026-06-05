import os
import re
import socket
import subprocess
import time
import threading
import ollama
from PyQt5.QtCore import QThread, pyqtSignal

# ── Optional imports ──────────────────────────────────────────────────────────

try:
    import speech_recognition as sr
    _SR_AVAILABLE = True
except ImportError:
    _SR_AVAILABLE = False

try:
    from PIL import Image as _PilImage
    import io as _io
    _PIL_AVAILABLE = True
except ImportError:
    _PIL_AVAILABLE = False


# ── Image preprocessing ───────────────────────────────────────────────────────

# llava internally resizes images to 336×336 anyway.
# Downscaling large images before sending saves encoding time and reduces
# the number of tokens the model spends on the image.
_MAX_IMAGE_DIM = 512   # pixels on longest side — fast, good quality


def _downscale_image_bytes(raw_bytes: bytes) -> bytes:
    """
    Downscale image to _MAX_IMAGE_DIM on the longest side using PIL.
    Returns original bytes if PIL is unavailable or image is already small.
    """
    if not _PIL_AVAILABLE:
        return raw_bytes
    try:
        img = _PilImage.open(_io.BytesIO(raw_bytes))
        w, h = img.size
        if max(w, h) <= _MAX_IMAGE_DIM:
            return raw_bytes          # already small enough
        scale  = _MAX_IMAGE_DIM / max(w, h)
        new_w  = max(1, int(w * scale))
        new_h  = max(1, int(h * scale))
        img    = img.resize((new_w, new_h), _PilImage.LANCZOS)
        # Convert to RGB (handles RGBA/P mode PNGs)
        if img.mode not in ("RGB", "L"):
            img = img.convert("RGB")
        buf = _io.BytesIO()
        img.save(buf, format="JPEG", quality=85)
        return buf.getvalue()
    except Exception:
        return raw_bytes              # fall back to original on any error


# ── Connectivity / runtime helpers ───────────────────────────────────────────

def _check_internet(host="8.8.8.8", port=53, timeout=2):
    try:
        socket.setdefaulttimeout(timeout)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        sock.close()
        return True
    except Exception:
        return False


def get_stt_backend() -> str:
    """Returns 'google' if SpeechRecognition is installed, else 'none'."""
    if _SR_AVAILABLE:
        return "google"
    return "none"


def is_ollama_running():
    try:
        sock = socket.create_connection(("localhost", 11434), timeout=0.5)
        sock.close()
        return True
    except Exception:
        return False


def start_ollama(stop_flag=None):
    """
    Start Ollama server if needed.

    Accepts an optional stop_flag callable so the caller can cancel startup.
    The polling loop checks stop_flag() each second and exits early if cancelled.
    """
    if os.name == 'nt':
        subprocess.Popen('start cmd /k "ollama serve"', shell=True)
    else:
        subprocess.Popen(
            ['bash', '-c',
             'x-terminal-emulator -e "ollama serve" || '
             'gnome-terminal -- ollama serve || '
             'xterm -e "ollama serve"']
        )

    for _ in range(30):
        if stop_flag is not None and stop_flag():
            return False
        time.sleep(1)
        if is_ollama_running():
            return True
    return False


# ── Topic switch detection ───────────────────────────────────────────────────

_STOP_WORDS = {
    'a', 'an', 'the', 'is', 'in', 'it', 'of', 'to', 'do', 'i',
    'me', 'my', 'we', 'on', 'at', 'by', 'be', 'as', 'or', 'if',
    'how', 'what', 'why', 'can', 'for', 'with', 'this', 'that',
    'are', 'was', 'and', 'you', 'he', 'she', 'they', 'have', 'has',
}
_TOPIC_SWITCH_THRESHOLD = 0.15


def _word_set(text: str) -> set:
    words = re.findall(r'[a-z]+', text.lower())
    return {w for w in words if w not in _STOP_WORDS and len(w) > 2}


def detect_topic_switch(prev_text: str, curr_text: str) -> bool:
    if not prev_text:
        return False
    a, b = _word_set(prev_text), _word_set(curr_text)
    if not a or not b:
        return False
    return len(a & b) / len(a | b) < _TOPIC_SWITCH_THRESHOLD


# ── Model / service background workers ───────────────────────────────────────

class OllamaStatusWorker(QThread):
    result_signal = pyqtSignal(bool)

    def run(self):
        self.result_signal.emit(is_ollama_running())


class ModelFetchWorker(QThread):
    result_signal = pyqtSignal(list)

    def run(self):
        try:
            models_data = ollama.list()
            raw = (models_data.get('models', [])
                   if isinstance(models_data, dict)
                   else getattr(models_data, 'models', []))

            names = []
            for m in raw:
                name = (m.get('name') or m.get('model', '')
                        if isinstance(m, dict)
                        else getattr(m, 'model', str(m)))
                if name:
                    names.append(name)

            # Keep the vision model cache warm so image sends don't block
            _refresh_model_cache()

            self.result_signal.emit(names if names else ['qwen2.5-coder:3b'])
        except Exception:
            self.result_signal.emit(['qwen2.5-coder:3b'])


# ── Smart token budget ───────────────────────────────────────────────────────

_COMPLEX_KEYWORDS = {
    # netlist / SPICE
    'netlist', 'spice', 'ngspice', '.tran', '.ac', '.dc', '.model',
    'subcircuit', 'convergence', 'singular', 'timestep',
    # debugging
    'error', 'debug', 'fix', 'wrong', 'issue', 'problem', 'fail',
    'simulate', 'simulation', 'analyse', 'analyze',
    # circuit design
    'schematic', 'kicad', 'footprint', 'component', 'resistor',
    'capacitor', 'mosfet', 'transistor', 'opamp', 'voltage', 'current',
}

_SIMPLE_KEYWORDS = {
    'what is', 'define', 'explain', 'meaning', 'how does',
    'difference between', 'example of',
}


def _smart_num_predict(user_messages: list, user_override: int = 1024) -> int:
    """
    Choose a token budget based on message complexity rather than a flat cap.
    This is the single biggest speed improvement: most answers need far fewer
    tokens than the hard 1024 limit.

    Tiers (all well within correct/complete answer range for each type):
      simple question  →  256 tokens  (~1-2 min on slow CPU, ~20s on fast)
      technical        →  512 tokens  (~2-4 min on slow CPU, ~40s on fast)
      netlist/debug    →  768 tokens  (~3-6 min on slow CPU, ~60s on fast)

    If the user has manually set a lower budget via the settings slider,
    we always respect that as an upper bound.

    Combines up to 4 recent history lines (2 user turns + their bot replies)
    for a better complexity signal than looking at user messages alone.
    """
    # Combine the last 4 history lines (up to 2 user turns + their bot replies)
    combined = " ".join(
        line[5:].lower() for line in user_messages[-4:]
        if line.startswith("User:")
    )

    # Check for complex technical content
    is_complex = any(kw in combined for kw in _COMPLEX_KEYWORDS)
    # Check for simple definitional questions
    is_simple  = any(kw in combined for kw in _SIMPLE_KEYWORDS) and not is_complex
    # Long message = detailed question = needs detailed answer
    is_long    = len(combined) > 300

    if is_simple and not is_long:
        budget = 256
    elif is_complex or is_long:
        budget = 768
    else:
        budget = 384

    # Respect the user's slider setting as a ceiling
    return min(budget, user_override)


# ── System prompts ────────────────────────────────────────────────────────────

_SYSTEM_PROMPT = """You are an expert electronics engineer and the AI assistant embedded inside eSim, an open-source EDA tool developed by FOSSEE at IIT Bombay.

Your expertise includes:
- KiCad schematic capture, symbols, labels, ERC issues, footprints
- NgSpice simulations and SPICE netlists
- Circuit debugging and simulation troubleshooting
- FPGA, MCU, power, reset, SPI, pull-up/pull-down, decoupling and connector review
- Reading partial schematic screenshots from EDA tools
- eSim workflow: KiCad → netlist → NgSpice → analysis

Rules:
- Be practical, direct, and technically useful.
- Match response length to question complexity.
- For debugging, explain both WHY and HOW to fix the issue.
- When code or SPICE is needed, use a fenced code block.
- If the user provides a schematic image, analyze the visible block instead of giving a generic refusal.
- If uncertain, say likely / appears to be, but still provide analysis.
"""


_VISION_SYSTEM_PROMPT = """You are an expert electronics engineer and the AI assistant inside eSim, an open-source EDA tool by FOSSEE at IIT Bombay.

You are given one or more schematic images from eSim or KiCad. Your job is to answer the user's question about those images as accurately and helpfully as possible.

Rules:
- Read every visible label, net name, component reference, value, and pin number from the image.
- If the user asks a specific question (e.g. "how to build this in eSim", "what does this component do", "why is this connection wrong"), answer THAT question directly and completely.
- If no specific question is given, describe the circuit: identify its function, list components, and flag any design issues.
- Never refuse to analyse. If parts of the image are unclear, do your best and note any uncertainty.
- Be concise and practical. Match the length of your answer to the complexity of the question.
- When referring to components, use their visible reference designators (R1, C3, U2, etc.).
"""


# ── Text chat worker ──────────────────────────────────────────────────────────

class OllamaWorker(QThread):
    response_signal = pyqtSignal(str)
    status_signal = pyqtSignal(str)

    def __init__(self, chat_history, model="qwen2.5-coder:3b",
                 temperature=0.25, num_predict=1024):
        super().__init__()
        self.chat_history = chat_history
        self.model = model
        self.temperature = temperature
        self.num_predict = num_predict
        self._stop_requested = False

    def stop(self):
        self._stop_requested = True

    def run(self):
        try:
            if not is_ollama_running():
                self.status_signal.emit("Starting Ollama server — please wait…")
                started = start_ollama(stop_flag=lambda: self._stop_requested)
                if not started:
                    if self._stop_requested:
                        return  # user cancelled cleanly
                    self.response_signal.emit(
                        "❌ Could not start Ollama automatically.\n"
                        "Please open a terminal and run: ollama serve"
                    )
                    return
                self.status_signal.emit("Ollama started! Getting response…")
                time.sleep(1)

            # Keep last 10 history lines (5 turns).
            # Sending 20 lines fills most of the context window before the
            # question is even added, forcing the model to load more tokens.
            messages = [{"role": "system", "content": _SYSTEM_PROMPT}]
            for line in self.chat_history[-10:]:
                if line.startswith("User:"):
                    messages.append({"role": "user", "content": line[5:].strip()})
                elif line.startswith("Bot:"):
                    messages.append({"role": "assistant", "content": line[4:].strip()})

            # Smart token budget: short questions get fewer tokens so they
            # finish faster; complex questions still get enough for a full answer.
            budget = _smart_num_predict(self.chat_history, self.num_predict)

            stream = ollama.chat(
                model=self.model,
                messages=messages,
                stream=True,
                options={
                    "temperature": self.temperature,
                    "num_predict": budget,
                    # 2048 ctx handles 5 turns of history + question comfortably.
                    # Allocating 4096 forces Ollama to malloc a larger KV-cache,
                    # adding 2-4s overhead before token 1 is generated.
                    "num_ctx": 2048,
                    "repeat_penalty": 1.08,
                    # Keep model loaded in RAM between requests.
                    # Without this, Ollama unloads after 5 min and the next
                    # question pays a 30-60s reload cost.
                    "keep_alive": "10m",
                }
            )

            bot_response = ""
            for chunk in stream:
                if self._stop_requested:
                    bot_response += "\n\n⏹ Generation stopped."
                    break
                bot_response += chunk["message"]["content"]

            bot_response = bot_response.strip()
            if not bot_response:
                bot_response = (
                    "⚠️ Received an empty response. "
                    "The model may still be loading — please try again."
                )

        except Exception as e:
            bot_response = (
                f"❌ Error: {str(e)}\n"
                "Make sure Ollama is installed and 'ollama serve' is running."
            )

        self.response_signal.emit(bot_response)


# ── Vision model helpers ──────────────────────────────────────────────────────

def _is_vision_model(model_name: str) -> bool:
    if not model_name:
        return False
    m = model_name.lower()
    return any(k in m for k in [
        "llava", "bakllava", "vision", "moondream", "minicpm-v", "qwen2-vl"
    ])
# QThread reads/writes don't produce a data race.
_cache_lock = threading.Lock()
_installed_models_cache: list = []
_installed_models_cache_valid: bool = False


def _refresh_model_cache():
    global _installed_models_cache, _installed_models_cache_valid
    try:
        models_data = ollama.list()
        raw = (models_data.get('models', [])
               if isinstance(models_data, dict)
               else getattr(models_data, 'models', []))
        names = []
        for m in raw:
            name = (m.get('name') or m.get('model', '')
                    if isinstance(m, dict)
                    else getattr(m, 'model', str(m)))
            if name:
                names.append(name)
        with _cache_lock:
            _installed_models_cache       = names
            _installed_models_cache_valid = True
    except Exception:
        with _cache_lock:
            _installed_models_cache_valid = False


def _pick_best_vision_model(preferred: str = "") -> str:
    """
    Pick the fastest available vision model.
    Priority: user-selected (if vision-capable) → moondream → llava:7b → llava → llava:13b
    Smaller/faster models come FIRST so CPU inference is quick.
    Uses a cached model list — no blocking ollama.list() call at send time.
    """
    with _cache_lock:
        cache_valid = _installed_models_cache_valid
        cache_copy  = list(_installed_models_cache)

    if not cache_valid:
        _refresh_model_cache()
        with _cache_lock:
            cache_copy = list(_installed_models_cache)

    installed_map = {name.lower(): name for name in cache_copy}

    # If the user explicitly selected a vision model, respect that choice first
    if preferred and _is_vision_model(preferred):
        return preferred

    # Prefer smaller/faster models for speed on CPU
    speed_order = [
        "moondream",       # ~1.6 GB — fastest
        "llava:7b",        # ~4 GB  — good balance
        "llava",           # ~4 GB  — default tag (usually 7b)
        "bakllava",        # ~4 GB
        "llava:13b",       # ~8 GB  — slowest, last resort
    ]
    for cand in speed_order:
        if cand.lower() in installed_map:
            return installed_map[cand.lower()]

    # Fallback: any installed vision model
    for name in cache_copy:
        if _is_vision_model(name):
            return name

    # No vision-capable model is installed.
    # Return None so the caller can show a clear error instead of
    # sending the images to a text-only model that will hallucinate.
    return None


def _build_schematic_vision_prompt(extra_prompt: str, image_count: int) -> str:
    """
    Build the prompt sent to the vision model alongside the image(s).
    If the user typed a question, that question drives the response.
    If no question was given, request a general circuit analysis.
    """
    n = "this schematic" if image_count == 1 else f"these {image_count} schematics"
    if extra_prompt and extra_prompt.strip():
        # User asked something specific - make that the primary request.
        return (
            f"Looking at {n}: {extra_prompt.strip()}\n\n"
            "Base your answer on what is actually visible in the image."
        )
    else:
        # No question given - do a general analysis.
        return (
            f"Please analyse {n}. "
            "Identify the circuit's function, list all visible components with their "
            "reference designators and values, name the nets and signal rails, "
            "and flag any potential design issues you can see."
        )


# ── Vision worker ─────────────────────────────────────────────────────────────

class OllamaVisionWorker(QThread):
    response_signal = pyqtSignal(str)
    status_signal = pyqtSignal(str)

    def __init__(self, image_paths=None, extra_prompt: str = "",
                 model: str = "llava", image_path: str = ""):
        super().__init__()

        if image_paths:
            self.image_paths = image_paths if isinstance(image_paths, list) else [image_paths]
        elif image_path:
            self.image_paths = [image_path]
        else:
            self.image_paths = []

        self.extra_prompt = extra_prompt
        self.model = model
        self._stop_requested = False

    def stop(self):
        self._stop_requested = True

    def _chat_once(self, model_name: str, prompt: str, image_bytes_list):
        stream = ollama.chat(
            model=model_name,
            messages=[
                {"role": "system", "content": _VISION_SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": prompt,
                    "images": image_bytes_list,
                }
            ],
            stream=True,
            options={
                "temperature": 0.15,
                # llava: ~576 tokens/image patch + ~200 prompt + 512 predict.
                # 3072 gives comfortable headroom without the overhead of 4096.
                "num_ctx": 3072,
                "num_predict": 512,
                "repeat_penalty": 1.05,
                "keep_alive": "10m",
            }
        )

        response      = ""
        token_count   = 0
        for chunk in stream:
            if self._stop_requested:
                response += "\n\n\u23f9 Generation stopped."
                break
            piece       = chunk["message"]["content"]
            response   += piece
            token_count += 1

            # Emit progress every 20 tokens so the status label
            # shows the model is actively working
            if token_count % 20 == 0:
                self.status_signal.emit(
                    f"Generating… ({token_count} tokens so far)"
                )
        return response.strip()

    def run(self):
        try:
            if not is_ollama_running():
                self.status_signal.emit("Starting Ollama server — please wait…")
                started = start_ollama(stop_flag=lambda: self._stop_requested)
                if not started:
                    if self._stop_requested:
                        return
                    self.response_signal.emit(
                        "❌ Could not start Ollama automatically.\n"
                        "Please open a terminal and run: ollama serve"
                    )
                    return
                self.status_signal.emit("Ollama started!")
                time.sleep(1)

            if not self.image_paths:
                self.response_signal.emit("❌ No image paths provided.")
                return

            # Load and downscale images before sending.
            # llava resizes internally to 336px anyway; sending 4K images
            # just wastes encoding time. Downscaling to 512px is invisible
            # to the model but saves significant transfer overhead.
            image_bytes_list = []
            for path in self.image_paths:
                if not os.path.exists(path):
                    self.response_signal.emit(f"❌ Image file not found: {path}")
                    return
                with open(path, "rb") as f:
                    raw = f.read()
                image_bytes_list.append(_downscale_image_bytes(raw))

            image_count = len(image_bytes_list)
            n_label = "image" if image_count == 1 else f"{image_count} images"
            self.status_signal.emit(f"Analysing {n_label}…")

            vision_model = _pick_best_vision_model(self.model)

            if vision_model is None:
                # No vision-capable model is installed. A text model cannot
                # see images and will hallucinate plausible-sounding but
                # completely fabricated answers.
                self.response_signal.emit(
                    "❌ No vision model is installed.\n\n"
                    "Image analysis requires a vision-capable model. "
                    "Install one by running this in a terminal:\n"
                    "```bash\n"
                    "ollama pull llava\n"
                    "```\n"
                    "Then restart eSim and select `llava` from the model dropdown."
                )
                return

            self.status_signal.emit(f"Using model: {vision_model}")
            prompt = _build_schematic_vision_prompt(self.extra_prompt, image_count)

            response = self._chat_once(vision_model, prompt, image_bytes_list)

            if not response:
                response = "⚠️ Vision model returned an empty response. Try again."

        except Exception as e:
            err = str(e)
            if "model" in err.lower() and ("not found" in err.lower() or "pull" in err.lower()):
                response = (
                    "❌ Vision model not found.\n"
                    "Install one with:\n"
                    "```bash\n"
                    "ollama pull llava\n"
                    "# or\n"
                    "ollama pull llava:7b\n"
                    "```"
                )
            else:
                response = (
                    f"❌ Vision error: {err}\n"
                    "Make sure a vision model such as `llava` is installed."
                )

        self.response_signal.emit(response)


# ── Microphone worker ─────────────────────────────────────────────────────────

class MicWorker(QThread):
    text_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)
    status_signal = pyqtSignal(str)

    def run(self):
        """Record from microphone and transcribe using Google Speech Recognition."""
        if not _SR_AVAILABLE:
            self.error_signal.emit(
                "SpeechRecognition not installed.\nRun:  pip install SpeechRecognition pyaudio"
            )
            return

        try:
            recognizer = sr.Recognizer()
            recognizer.energy_threshold = 300
            recognizer.dynamic_energy_threshold = True

            with sr.Microphone() as source:
                self.status_signal.emit("🎤 Adjusting for ambient noise…")
                recognizer.adjust_for_ambient_noise(source, duration=0.6)
                self.status_signal.emit("🎤 Listening… speak now")
                audio = recognizer.listen(source, timeout=8, phrase_time_limit=25)

        except sr.WaitTimeoutError:
            self.error_signal.emit("🎤 No speech detected — please try again.")
            return
        except OSError:
            self.error_signal.emit("🎤 Microphone not found. Run: pip install pyaudio")
            return
        except Exception as e:
            self.error_signal.emit(f"🎤 Microphone error: {str(e)}")
            return

        self._transcribe_google(audio)

    def _transcribe_google(self, audio):
        try:
            recognizer = sr.Recognizer()
            self.status_signal.emit("🎤 Processing speech (online)…")
            text = recognizer.recognize_google(audio)
            if text:
                self.text_signal.emit(text)
            else:
                self.error_signal.emit("🎤 Could not understand — please try again.")
        except sr.UnknownValueError:
            self.error_signal.emit("🎤 Could not understand speech — please try again.")
        except sr.RequestError as e:
            self.error_signal.emit(
                f"🎤 Online STT failed: {e}\n"
                "Install offline STT: pip install faster-whisper"
            )
        except Exception as e:
            self.error_signal.emit(f"🎤 STT error: {str(e)}")
