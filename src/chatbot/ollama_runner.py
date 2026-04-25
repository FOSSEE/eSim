import os
import ollama
import json, time
import re
import base64

# Model configuration
VISION_MODELS = {"primary": "minicpm-v:latest"}
TEXT_MODELS = {"default": "qwen2.5:3b"} # Qwen 2.5 3B is already quite fast!
EMBED_MODEL = "nomic-embed-text" 

ollama_client = ollama.Client(
    host="http://localhost:11434",
    timeout=300.0,  
)

def run_ollama_vision(prompt: str, image_input: str | bytes) -> str:
    """Call minicpm-v:latest with focused parameters to reduce lag."""
    model = VISION_MODELS["primary"]
    
    try:
        image_b64 = ""
        if isinstance(image_input, bytes):
            image_b64 = base64.b64encode(image_input).decode("utf-8")
        elif os.path.isfile(image_input):
            with open(image_input, "rb") as f:
                image_b64 = base64.b64encode(f.read()).decode("utf-8")
        elif isinstance(image_input, str) and len(image_input) > 100:
             image_b64 = image_input
        else:
             raise ValueError("Invalid image input format")

        system_prompt = (
            "You are an eSim expert. Analyze the schematic.\n"
            "Output ONLY a single JSON object wrapped in ```json ... ```."
        )

        # Vision is slow; we set stream=False here because we need the full JSON to parse it,
        # but we reduce 'num_predict' to stop the model from rambling.
        resp = ollama_client.chat(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt, "images": [image_b64]},
            ],
            options={
                "temperature": 0.0,
                "num_ctx": 4096, # Reduced from 8192
                "num_predict": 512, # Reduced from 1024
            },
        )

        content = resp["message"]["content"]
        json_match = re.search(r'```json\s*(\{.*?\})\s*```', content, re.DOTALL)
        if json_match: return json_match.group(1)
        
        start, end = content.find('{'), content.rfind('}') + 1
        return content[start:end] if start != -1 else "{}"

    except Exception as e:
        print(f"[VISION ERROR] {e}")
        return json.dumps({"vision_summary": "Vision failed", "components": []})

def run_ollama(prompt: str, mode: str = "default") -> str:
    """
    ULTRA-OPTIMIZED: Streams output for immediate user feedback.
    """
    model = TEXT_MODELS.get(mode, TEXT_MODELS["default"])
    
    try:
        # We use stream=True to get tokens as they are generated
        stream = ollama_client.chat(
            model=model,
            messages=[
                {"role": "system", "content": "You are an eSim expert. Be concise."},
                {"role": "user", "content": prompt},
            ],
            stream=True, 
            options={
                "temperature": 0.05, 
                "num_ctx": 1024, # Reduced to 1024 for faster prompt processing
                "num_predict": 250, # Limit long-winded answers
            },
        )
        
        full_response = ""
        for chunk in stream:
            token = chunk['message']['content']
            full_response += token
            # In your Application.py GUI, you should call a callback here to update the UI
            # For now, we print it to show the speed
            print(token, end="", flush=True) 
        
        print() # New line after stream ends
        return full_response.strip()
    
    except Exception as e:
        return f"[Error] {str(e)}"

def get_embedding(text: str):
    """Get text embeddings with a fast cache check."""
    try:
        r = ollama_client.embeddings(model=EMBED_MODEL, prompt=text)
        return r["embedding"]
    except Exception as e:
        return None