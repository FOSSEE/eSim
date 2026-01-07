import os
import json
import base64
import io
import time
from typing import Dict, Any
from PIL import Image
MAX_IMAGE_BYTES = int(0.5*1024 * 1024)  
from .ollama_runner import run_ollama_vision

# === IMPORT PADDLE OCR ===
try:
    from paddleocr import PaddleOCR
    import logging
    logging.getLogger("ppocr").setLevel(logging.ERROR)
    
    # CRITICAL FIX: Disabled MKLDNN and Angle Classification to prevent VM Crashes
    ocr_engine = PaddleOCR(
        use_angle_cls=False,    # <--- MUST BE FALSE TO STOP SIGABRT
        lang='en',
        use_gpu=False,          # Force CPU
        enable_mkldnn=False,    # <--- MUST BE FALSE FOR PADDLE v3 COMPATIBILITY
        use_mp=False,           # Disable multiprocessing
        show_log=False 
    )
    HAS_PADDLE = True
    print("[INIT] PaddleOCR initialized (Safe Mode).")
except Exception as e:
    HAS_PADDLE = False
    print(f"[INIT] PaddleOCR init failed: {e}")


def encode_image(image_path: str) -> str:
    """Convert image to base64 string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def optimize_image_for_vision(image_path: str) -> bytes:
    """
    Resize large images to reduce vision model processing time.
    Target: Max 1920x1080 while maintaining aspect ratio.
    """
    try:
        img = Image.open(image_path)

        if img.mode not in ('RGB', 'L'):
            img = img.convert('RGB')

        max_width = 1920
        max_height = 1080

        if img.width > max_width or img.height > max_height:
            # Calculate scaling factor
            scale = min(max_width / img.width, max_height / img.height)
            new_size = (int(img.width * scale), int(img.height * scale))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            print(f"[IMAGE] Resized from {img.width}x{img.height} to {new_size[0]}x{new_size[1]}")

        # Convert to bytes (PNG format prevents compression artifacts on text)
        buffer = io.BytesIO()
        img.save(buffer, format='PNG', optimize=True, quality=85)
        return buffer.getvalue()

    except Exception as e:
        print(f"[IMAGE] Optimization failed: {e}, using original")
        with open(image_path, 'rb') as f:
            return f.read()


def extract_text_with_paddle(image_path: str) -> str:
    """Extract text using PaddleOCR (Handles rotated/vertical text excellently)."""
    if not HAS_PADDLE:
        return ""
    try:
        result = ocr_engine.ocr(image_path, cls=True)
        detected_texts = []
        if result and result[0]:
            for line in result[0]:
                text = line[1][0]
                conf = line[1][1]

                if conf > 0.6:
                    detected_texts.append(text)

        full_text = " ".join(detected_texts)
        return full_text

    except Exception as e:
        print(f"[OCR] PaddleOCR Failed: {e}")
        return ""

def analyze_and_extract(image_path: str) -> Dict[str, Any]:
    """
    Analyze schematic with image optimization, PaddleOCR text injection, and timeout handling.
    Rejects images larger than 0.5 MB.
    """
    if not os.path.exists(image_path):
        return {
            "error": "Image file not found",
            "vision_summary": "",
            "component_counts": {},
            "circuit_analysis": {
                "circuit_type": "Unknown",
                "design_errors": [],
                "design_warnings": []
            },
            "components": [],
            "values": {}
        }

    try:
        file_size = os.path.getsize(image_path)
    except OSError as e:
        return {
            "error": f"Could not read image size: {e}",
            "vision_summary": "",
            "component_counts": {},
            "circuit_analysis": {
                "circuit_type": "Unknown",
                "design_errors": [],
                "design_warnings": []
            },
            "components": [],
            "values": {}
        }

    if file_size > MAX_IMAGE_BYTES:
        size_mb = round(file_size / (1024 * 1024), 2)
        return {
            "error": f"Image too large ({size_mb} MB). Max allowed size is 0.5 MB.",
            "vision_summary": "",
            "component_counts": {},
            "circuit_analysis": {
                "circuit_type": "Unknown",
                "design_errors": ["Image file size exceeded 0.5 MB limit"],
                "design_warnings": []
            },
            "components": [],
            "values": {}
        }

    # === OPTIMIZE IMAGE BEFORE SENDING ===
    print(f"[VISION] Processing image: {os.path.basename(image_path)}")
    image_bytes = optimize_image_for_vision(image_path)

    # === EXTRACT OCR TEXT (CRITICAL STEP) ===
    ocr_text = extract_text_with_paddle(image_path)

    if ocr_text:
        clean_ocr = ocr_text.strip()
        print(f"[VISION] PaddleOCR Hints injected: {clean_ocr[:100]}...")
    else:
        clean_ocr = "No readable text detected."

    # === PROMPT WITH CONTEXT ===
    prompt = f"""
ANALYZE THIS ELECTRONICS SCHEMATIC IMAGE.

CONTEXT FROM OCR SCAN (Text detected in image):
"{clean_ocr}"

INSTRUCTIONS:
1. Use the OCR text to identify component labels (e.g., if you see "D1" text, there is a Diode, R1,R2,R3... for resistor).
2. Look for rotated text labels near symbols.
3. Identify the circuit topology.

VERY IMPORTANT INSTRUCTIONS:
1. DON'T OVERCALCULATE MODEL COUNT LIKE MODEL COUNT + OCR COUNT
2. IF THERE IS ANY VALUE NOT PRESENT FOR ANY COMPONENT JUST ADD A QUESTION MARK IN FRONT OF IT

OUTPUT RULES:
1. Return ONLY valid JSON.
2. Structure:


RESPOND WITH JSON ONLY.
"""

    max_retries = 2
    for attempt in range(max_retries):
        try:
            print(f"[VISION] Attempt {attempt + 1}/{max_retries}...")

            response_text = run_ollama_vision(prompt, image_bytes)

            cleaned_json = response_text.replace("```json", "").replace("```", "").strip()

            if "{" in cleaned_json and "}" in cleaned_json:
                start = cleaned_json.index("{")
                end = cleaned_json.rindex("}") + 1
                cleaned_json = cleaned_json[start:end]

            data = json.loads(cleaned_json)

            required_keys = ["vision_summary", "component_counts", "circuit_analysis", "components", "values"]
            for key in required_keys:
                if key not in data:
                    raise ValueError(f"Missing required key: {key}")

            if not isinstance(data.get("circuit_analysis"), dict):
                data["circuit_analysis"] = {"circuit_type": "Unknown", "design_errors": [], "design_warnings": []}

            if "design_errors" not in data["circuit_analysis"]:
                data["circuit_analysis"]["design_errors"] = []

            if not data.get("component_counts") or all(v == 0 for v in data.get("component_counts", {}).values()):
                counts = {"R": 0, "C": 0, "U": 0, "Q": 0, "D": 0, "L": 0, "Misc": 0}
                for comp in data.get("components", []):
                    if isinstance(comp, str) and len(comp) > 0:
                        comp_type = comp[0].upper()
                        if comp_type in counts:
                            counts[comp_type] += 1
                        elif "DIODE" in comp.upper() or comp.startswith("D"):
                            counts["D"] = counts.get("D", 0) + 1
                data["component_counts"] = counts

            if data.get("components"):
                data["components"] = list(dict.fromkeys(data["components"]))

            print(f"[VISION] Success: {data.get('circuit_analysis', {}).get('circuit_type', 'Unknown')}")
            return data

        except Exception as e:
            print(f"[VISION] Attempt {attempt + 1} failed: {str(e)}")
            if attempt == max_retries - 1:
                return {
                    "error": f"Vision analysis failed: {str(e)}",
                    "vision_summary": "Unable to analyze circuit image",
                    "component_counts": {},
                    "circuit_analysis": {
                        "circuit_type": "Unknown",
                        "design_errors": ["Analysis timed out or failed"],
                        "design_warnings": []
                    },
                    "components": [],
                    "values": {}
                }
            else:
                import time
                time.sleep(2)


def analyze_image(image_path: str, question: str | None = None, preprocess: bool = True) -> str:
    """Helper for manual testing."""
    return str(analyze_and_extract(image_path))