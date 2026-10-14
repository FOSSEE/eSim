import os
import ollama
import json
import time

# ==================== CLIENT ====================

ollama_client = ollama.Client(
    host="http://localhost:11434",
    timeout=300.0,
)

# ==================== SETTINGS ====================

_SETTINGS_DIR = os.path.join(
    os.path.expanduser("~"), ".local", "share", "esim-copilot"
)
_SETTINGS_PATH = os.path.join(_SETTINGS_DIR, "settings.json")

_DEFAULT_TEXT_MODEL = "qwen2.5:3b"
_DEFAULT_VISION_MODEL = "minicpm-v:latest"
EMBED_MODEL = "nomic-embed-text"


def load_model_settings() -> dict:
    """Load persisted model preferences from disk."""
    try:
        with open(_SETTINGS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_model_settings(text_model: str, vision_model: str) -> None:
    """Persist model preferences to disk."""
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


# Load settings and initialise model dicts
_settings = load_model_settings()

VISION_MODELS = {"primary": _settings.get("vision_model", _DEFAULT_VISION_MODEL)}
TEXT_MODELS   = {"default": _settings.get("text_model",   _DEFAULT_TEXT_MODEL)}


def reload_model_settings() -> None:
    """Re-read settings from disk and update running dicts (called after save)."""
    s = load_model_settings()
    VISION_MODELS["primary"] = s.get("vision_model", _DEFAULT_VISION_MODEL)
    TEXT_MODELS["default"]   = s.get("text_model",   _DEFAULT_TEXT_MODEL)


# ==================== VISION ====================

def run_ollama_vision(prompt: str, image_input) -> str:
    """Call vision model with Chain-of-Thought for better accuracy."""
    model = VISION_MODELS["primary"]

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

        system_prompt = (
            "You are an expert Electronics Engineer using eSim.\n"
            "Analyze the schematic image carefully.\n\n"
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
                "temperature": 0.0,
                "num_ctx": 8192,
                "num_predict": 1024,
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


# ==================== TEXT ====================

def run_ollama(prompt: str, mode: str = "default") -> str:
    """Run text model with focused parameters."""
    model = TEXT_MODELS.get(mode, TEXT_MODELS["default"])

    try:
        resp = ollama_client.chat(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an eSim and electronics expert. Be concise, accurate, and practical.",
                },
                {"role": "user", "content": prompt},
            ],
            options={
                "temperature": 0.05,
                "num_ctx": 2048,
                "num_predict": 400,
                "top_p": 0.9,
                "repeat_penalty": 1.1,
            },
        )
        return resp["message"]["content"].strip()

    except Exception as e:
        return f"[Error] {str(e)}"


# ==================== EMBEDDINGS ====================

def get_embedding(text: str):
    """Get text embeddings for RAG."""
    try:
        r = ollama_client.embeddings(model=EMBED_MODEL, prompt=text)
        return r["embedding"]
    except Exception as e:
        print(f"[EMBED ERROR] {e}")
        return None
