import os
import json
import queue
import time

import sounddevice as sd
from vosk import Model, KaldiRecognizer

_MODEL = None

def _get_model():
    global _MODEL
    model_path = os.environ.get("VOSK_MODEL_PATH", "")
    if not model_path or not os.path.isdir(model_path):
        raise RuntimeError(f"VOSK_MODEL_PATH not set or not found: {model_path}")
    if _MODEL is None:
        _MODEL = Model(model_path)
    return _MODEL

def listen_to_mic(should_stop=lambda: False, max_silence_sec=3, samplerate=16000, phrase_limit_sec=8) -> str:
    """
    Offline STT using Vosk.
    Returns recognized text, or "" if cancelled / timed out.
    """
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
