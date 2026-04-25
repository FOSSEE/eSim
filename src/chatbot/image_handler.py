import os
from paddleocr import PaddleOCR

try:
    # Minimal settings: We removed 'show_log' and 'use_gpu' to stop the errors
    ocr_engine = PaddleOCR(lang='en')
    HAS_PADDLE = True
    print("[INIT] PaddleOCR initialized (Safe Mode).")
except Exception as e:
    HAS_PADDLE = False
    print(f"[INIT] PaddleOCR init failed: {e}")

def extract_text_with_paddle(image_path):
    if not HAS_PADDLE: return ""
    try:
        result = ocr_engine.ocr(image_path, cls=True)
        detected_texts = [line[1][0] for line in result[0] if line[1][1] > 0.6]
        return " ".join(detected_texts)
    except:
        return ""

def analyze_and_extract(image_path):
    """This function is required by chatbot_core.py"""
    text = extract_text_with_paddle(image_path)
    return {
        "vision_summary": f"Detected text: {text}" if text else "No text detected",
        "components": [],
        "values": {}
    }
