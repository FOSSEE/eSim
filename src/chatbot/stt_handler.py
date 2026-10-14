import os
import json
import queue
import time

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

def _safe_json_text(json_str: str, key: str = "text") -> str:
    try:
        return json.loads(json_str).get(key, "").strip()
    except (json.JSONDecodeError, TypeError, AttributeError):
        return ""

def listen_to_mic(should_stop=lambda: False, max_silence_sec=3, samplerate=16000, phrase_limit_sec=8) -> str:
    """
    Offline STT using Vosk.
    Returns recognized text, or "" if cancelled / timed out.
    """
    if not _HAS_STT:
        raise RuntimeError("Speech-to-text is not installed or failed to load.")
    q = queue.Queue(maxsize=1000)
    rec = KaldiRecognizer(_get_model(), samplerate)

    started = False
    t0 = time.time()
    t_speech = None

    def callback(indata, frames, time_info, status):
        try:
            q.put_nowait(bytes(indata))
        except queue.Full:
            pass

    try:
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
                    text = _safe_json_text(rec.Result(), "text")
                    if text:
                        return text
                else:
                    partial = _safe_json_text(rec.PartialResult(), "partial")
                    if partial and not started:
                        started = True
                        t_speech = now

            return _safe_json_text(rec.FinalResult(), "text")
    except Exception as e:
        print(f"STT mic input stream error: {e}")
        return ""
