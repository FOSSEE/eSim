import os
import json
import queue
import time

from .ollama_runner import CONFIG

try:
    import sounddevice as sd
    from vosk import Model, KaldiRecognizer
    _HAS_STT = True
except Exception:
    sd = None
    Model = None
    KaldiRecognizer = None
    _HAS_STT = False

_MODEL = None

DEFAULT_VOSK_DIR = os.path.join(
    os.path.expanduser("~"), ".local", "share",
    "esim-copilot", "vosk-model-small-en-us-0.15",
)

# ==================== CONFIG-DRIVEN DEFAULTS ====================

_STT_CFG = CONFIG.get("stt", {})
DEFAULT_SAMPLERATE = int(_STT_CFG.get("samplerate", 16000))
DEFAULT_MAX_SILENCE_SEC = int(_STT_CFG.get("max_silence_sec", 3))
DEFAULT_PHRASE_LIMIT_SEC = int(_STT_CFG.get("phrase_limit_sec", 8))


def _get_model():
    global _MODEL
    if not _HAS_STT:
        raise RuntimeError(
            "Speech-to-text is not available (missing vosk/sounddevice)."
        )
    model_path = os.environ.get("VOSK_MODEL_PATH", "").strip()
    if not model_path:
        model_path = DEFAULT_VOSK_DIR
    if not os.path.isdir(model_path):
        raise RuntimeError(
            f"Vosk model path not found. Set VOSK_MODEL_PATH or install at: {model_path}"
        )
    if _MODEL is None:
        _MODEL = Model(model_path)
    return _MODEL


def listen_to_mic(
    should_stop=lambda: False,
    max_silence_sec=None,
    samplerate=None,
    phrase_limit_sec=None,
) -> str:
    """
    Offline STT using Vosk. All timing knobs default to values in config.json
    (CONFIG.stt) so users can tune without touching the source.

    Returns recognized text, or "" if cancelled / timed out.
    """
    if not _HAS_STT:
        raise RuntimeError("Speech-to-text is not installed or failed to load.")

    if max_silence_sec is None:
        max_silence_sec = DEFAULT_MAX_SILENCE_SEC
    if samplerate is None:
        samplerate = DEFAULT_SAMPLERATE
    if phrase_limit_sec is None:
        phrase_limit_sec = DEFAULT_PHRASE_LIMIT_SEC

    q = queue.Queue()
    rec = KaldiRecognizer(_get_model(), samplerate)

    started = False
    t0 = time.time()
    t_speech = None

    def callback(indata, frames, time_info, status):
        q.put(bytes(indata))

    with sd.RawInputStream(
        samplerate=samplerate,
        channels=1,
        dtype="int16",
        blocksize=8000,
        callback=callback,
    ):
        while True:
            if should_stop():
                return ""

            now = time.time()

            # Stop after silence
            if not started and (now - t0) >= max_silence_sec:
                return ""

            if started and t_speech and (now - t_speech) >= phrase_limit_sec:
                break

            try:
                data = q.get(timeout=0.2)
            except queue.Empty:
                continue

            if rec.AcceptWaveform(data):
                text = json.loads(rec.Result()).get("text", "").strip()
                if text:
                    return text
            else:
                partial = json.loads(rec.PartialResult()).get("partial", "").strip()
                if partial and not started:
                    started = True
                    t_speech = now

        return json.loads(rec.FinalResult()).get("text", "").strip()