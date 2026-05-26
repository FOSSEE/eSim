import os
import ollama
import json
import time
from typing import Generator, Iterable, Optional

# ==================== CLIENT ====================

ollama_client = ollama.Client(
    host="http://localhost:11434",
    timeout=300.0,
)

# ==================== CONFIG (config.json) ====================

# Path resolution: prefer config.json sitting next to this file (inside the
# chatbot package). Fall back to the per-user settings directory.
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_PACKAGE_CONFIG_PATH = os.path.join(_THIS_DIR, "config.json")

_SETTINGS_DIR = os.path.join(
    os.path.expanduser("~"), ".local", "share", "esim-copilot"
)
_SETTINGS_PATH = os.path.join(_SETTINGS_DIR, "settings.json")
_USER_CONFIG_PATH = os.path.join(_SETTINGS_DIR, "config.json")

_DEFAULT_TEXT_MODEL = "qwen2.5:3b"
_DEFAULT_VISION_MODEL = "minicpm-v:latest"
EMBED_MODEL = "nomic-embed-text"

# Built-in defaults (used if config.json is missing). These mirror config.json
# so the runner still works in a degraded state.
_DEFAULT_CONFIG = {
    "models": {
        "text_model": _DEFAULT_TEXT_MODEL,
        "vision_model": _DEFAULT_VISION_MODEL,
        "embed_model": EMBED_MODEL,
    },
    "system_rules": {
        "text_system_prompt": (
            "You are eSim Copilot, an expert assistant for the eSim EDA tool. "
            "Be concise, accurate, and practical."
        ),
        "vision_system_prompt": (
            "You are an expert Electronics Engineer using eSim. "
            "Analyze the schematic image carefully and output JSON only."
        ),
    },
    "context_window": {
        "text_num_ctx": 4096,
        "text_num_predict": 512,
        "vision_num_ctx": 4096,
        "vision_num_predict": 1024,
        "follow_up_num_predict": 350,
    },
    "sampling": {
        "temperature": 0.05,
        "top_p": 0.9,
        "repeat_penalty": 1.1,
        "vision_temperature": 0.0,
    },
    "streaming": {"enabled": True},
    "history": {"max_turns": 12, "context_turns": 6},
    "image": {
        "max_size_mb": 0.5,
        "max_width": 1920,
        "max_height": 1080,
        "vision_max_retries": 2,
    },
    "rag": {"default_n_results": 5, "follow_up_n_results": 2},
    "stt": {"samplerate": 16000, "max_silence_sec": 3, "phrase_limit_sec": 8},
}


def _deep_merge(base: dict, override: dict) -> dict:
    """Recursively merge override into base (override wins)."""
    out = dict(base)
    for k, v in (override or {}).items():
        if k in out and isinstance(out[k], dict) and isinstance(v, dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def load_config() -> dict:
    """
    Load the customizable configuration layer.
    Priority: ~/.local/share/esim-copilot/config.json (user)
            > <package>/config.json (shipped)
            > built-in defaults.
    """
    cfg = dict(_DEFAULT_CONFIG)

    for path in (_PACKAGE_CONFIG_PATH, _USER_CONFIG_PATH):
        if os.path.isfile(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    cfg = _deep_merge(cfg, json.load(f))
            except Exception as e:
                print(f"[CONFIG] Failed to load {path}: {e}")
    return cfg


CONFIG = load_config()


def reload_config() -> dict:
    """Re-read config.json from disk (call after editing it)."""
    global CONFIG
    CONFIG = load_config()
    # Also keep the legacy model dicts in sync.
    VISION_MODELS["primary"] = CONFIG["models"].get("vision_model", _DEFAULT_VISION_MODEL)
    TEXT_MODELS["default"] = CONFIG["models"].get("text_model", _DEFAULT_TEXT_MODEL)
    return CONFIG


# ==================== LEGACY SETTINGS (kept for backward compat) ====================

def load_model_settings() -> dict:
    """Load persisted model preferences from disk (legacy settings.json)."""
    try:
        with open(_SETTINGS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_model_settings(text_model: str, vision_model: str) -> None:
    """Persist model preferences to disk (legacy settings.json)."""
    os.makedirs(_SETTINGS_DIR, exist_ok=True)
    try:
        with open(_SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump({"text_model": text_model, "vision_model": vision_model}, f, indent=2)
    except Exception as e:
        print(f"[SETTINGS] Failed to save: {e}")


def list_available_models() -> list:
    """Query Ollama for installed models. Returns list of model name strings."""
    try:
        resp = ollama_client.list()
        names = [m["name"] for m in resp.get("models", [])]
        return names if names else [_DEFAULT_TEXT_MODEL, _DEFAULT_VISION_MODEL]
    except Exception:
        return [_DEFAULT_TEXT_MODEL, _DEFAULT_VISION_MODEL, EMBED_MODEL]


# Merge legacy settings.json on top of config.json (legacy wins for model picks
# so old users keep their previous choices).
_legacy = load_model_settings()
_cfg_models = CONFIG.get("models", {})

VISION_MODELS = {"primary": _legacy.get("vision_model", _cfg_models.get("vision_model", _DEFAULT_VISION_MODEL))}
TEXT_MODELS   = {"default": _legacy.get("text_model",   _cfg_models.get("text_model",   _DEFAULT_TEXT_MODEL))}


def reload_model_settings() -> None:
    """Re-read settings from disk and update running dicts (called after save)."""
    s = load_model_settings()
    VISION_MODELS["primary"] = s.get("vision_model", CONFIG["models"].get("vision_model", _DEFAULT_VISION_MODEL))
    TEXT_MODELS["default"]   = s.get("text_model",   CONFIG["models"].get("text_model",   _DEFAULT_TEXT_MODEL))


# ==================== VISION ====================

def run_ollama_vision(prompt: str, image_input) -> str:
    """Call vision model with Chain-of-Thought for better accuracy."""
    model = VISION_MODELS["primary"]
    ctx = CONFIG["context_window"]
    samp = CONFIG["sampling"]
    sys_prompt = CONFIG["system_rules"].get(
        "vision_system_prompt",
        _DEFAULT_CONFIG["system_rules"]["vision_system_prompt"],
    )

    try:
        import base64

        image_b64 = ""
        if isinstance(image_input, bytes):
            image_b64 = base64.b64encode(image_input).decode("utf-8")
        elif isinstance(image_input, str) and os.path.isfile(image_input):
            with open(image_input, "rb") as f:
                image_b64 = base64.b64encode(f.read()).decode("utf-8")
        elif isinstance(image_input, str) and len(image_input) > 100:
            image_b64 = image_input
        else:
            raise ValueError("Invalid image input format")

        # Compose system prompt with the analysis schema requirements.
        system_prompt = (
            f"{sys_prompt}\n\n"
            "STEP 1: THINKING PROCESS\n"
            "- List visible components (e.g., 'I see 4 diodes in a bridge...').\n"
            "- Trace connections (e.g., 'Resistor R1 is in series...').\n"
            "- Check against the OCR text provided.\n\n"
            "STEP 2: JSON OUTPUT\n"
            "After your analysis, output a SINGLE JSON object wrapped in ```json ... ```.\n"
            "Structure:\n"
            "{\n"
            '  "vision_summary": "Summary string",\n'
            '  "component_counts": {"R": 0, "C": 0, "D": 0, "Q": 0, "U": 0},\n'
            '  "circuit_analysis": {\n'
            '    "circuit_type": "Rectifier/Amplifier/etc",\n'
            '    "design_errors": [],\n'
            '    "design_warnings": []\n'
            '  },\n'
            '  "components": ["R1", "D1"],\n'
            '  "values": {"R1": "1k"}\n'
            "}\n"
        )

        resp = ollama_client.chat(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": prompt,
                    "images": [image_b64],
                },
            ],
            options={
                "temperature": samp.get("vision_temperature", 0.0),
                "num_ctx": ctx.get("vision_num_ctx", 4096),
                "num_predict": ctx.get("vision_num_predict", 1024),
            },
        )

        content = resp["message"]["content"]

        import re
        json_match = re.search(r'```json\s*(\{.*?\})\s*```', content, re.DOTALL)
        if json_match:
            return json_match.group(1)

        start = content.find('{')
        end = content.rfind('}') + 1
        if start != -1 and end != -1:
            return content[start:end]

        return "{}"

    except Exception as e:
        print(f"[VISION ERROR] {e}")
        return json.dumps({
            "vision_summary": f"Vision failed: {str(e)[:50]}",
            "component_counts": {},
            "circuit_analysis": {"circuit_type": "Error", "design_errors": [], "design_warnings": []},
            "components": [],
            "values": {},
        })


# ==================== TEXT (with streaming) ====================

def _build_text_options(mode: str = "default") -> dict:
    """Build the Ollama `options` dict from config.json."""
    ctx = CONFIG["context_window"]
    samp = CONFIG["sampling"]
    num_predict = ctx.get("text_num_predict", 512)
    if mode == "follow_up":
        num_predict = ctx.get("follow_up_num_predict", num_predict)
    return {
        "temperature": samp.get("temperature", 0.05),
        "num_ctx": ctx.get("text_num_ctx", 4096),
        "num_predict": num_predict,
        "top_p": samp.get("top_p", 0.9),
        "repeat_penalty": samp.get("repeat_penalty", 1.1),
    }


def _text_messages(prompt: str) -> list:
    """Build the chat message list with the configurable system rule."""
    sys_prompt = CONFIG["system_rules"].get(
        "text_system_prompt",
        _DEFAULT_CONFIG["system_rules"]["text_system_prompt"],
    )
    return [
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": prompt},
    ]


def run_ollama(
    prompt: str,
    mode: str = "default",
    stream: Optional[bool] = None,
    on_chunk=None,
) -> str:
    """
    Run text model.

    - If `stream` is True (or None and CONFIG["streaming"]["enabled"] is True),
      tokens are streamed from Ollama and accumulated into the final string.
    - `on_chunk(text)` is called for each streamed chunk (useful for live UI).
    - Returns the full assembled response.
    """
    model = TEXT_MODELS.get(mode, TEXT_MODELS["default"])
    if stream is None:
        stream = bool(CONFIG.get("streaming", {}).get("enabled", True))

    try:
        if stream:
            collected = []
            for chunk in run_ollama_stream(prompt, mode=mode):
                collected.append(chunk)
                if on_chunk is not None:
                    try:
                        on_chunk(chunk)
                    except Exception as cb_e:
                        print(f"[STREAM CALLBACK] {cb_e}")
            return "".join(collected).strip()

        resp = ollama_client.chat(
            model=model,
            messages=_text_messages(prompt),
            options=_build_text_options(mode),
        )
        return resp["message"]["content"].strip()

    except Exception as e:
        return f"[Error] {str(e)}"


def run_ollama_stream(prompt: str, mode: str = "default") -> Generator[str, None, None]:
    """
    Generator that yields text chunks as they arrive from Ollama.
    Suitable for plugging into a Qt signal/slot or any streaming UI.
    """
    model = TEXT_MODELS.get(mode, TEXT_MODELS["default"])
    try:
        stream = ollama_client.chat(
            model=model,
            messages=_text_messages(prompt),
            options=_build_text_options(mode),
            stream=True,
        )
        for chunk in stream:
            piece = ""
            if isinstance(chunk, dict):
                piece = chunk.get("message", {}).get("content", "") or ""
            else:
                # ollama-python returns objects with .message.content too
                msg = getattr(chunk, "message", None)
                if msg is not None:
                    piece = getattr(msg, "content", "") or ""
            if piece:
                yield piece
    except Exception as e:
        yield f"[Error] {str(e)}"


# ==================== EMBEDDINGS ====================

def get_embedding(text: str):
    """Get text embeddings for RAG."""
    try:
        embed_model = CONFIG["models"].get("embed_model", EMBED_MODEL)
        r = ollama_client.embeddings(model=embed_model, prompt=text)
        return r["embedding"]
    except Exception as e:
        print(f"[EMBED ERROR] {e}")
        return None