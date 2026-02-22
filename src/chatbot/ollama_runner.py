import os
import ollama
import json,time

# Model configuration
VISION_MODELS = {"primary": "minicpm-v:latest"}
TEXT_MODELS = {"default": "qwen2.5:3b"}
EMBED_MODEL = "nomic-embed-text" 

ollama_client = ollama.Client(
    host="http://localhost:11434",
    timeout=300.0,  
)

def run_ollama_vision(prompt: str, image_input: str | bytes) -> str:
    """Call minicpm-v:latest with Chain-of-Thought for better accuracy."""
    model = VISION_MODELS["primary"]
    
    try:
        import base64
        
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

        # === CHAIN OF THOUGHT ===
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
                    "images": [image_b64], # <--- MUST BE LIST OF BASE64 STRINGS
                },
            ],
            options={
                "temperature": 0.0,
                "num_ctx": 8192,
                "num_predict": 1024,
            },
        )

        content = resp["message"]["content"]
        
        # === PARSE JSON FROM MIXED OUTPUT ===
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
            "components": [], "values": {}
        })

def run_ollama(prompt: str, mode: str = "default") -> str:
    """
    OPTIMIZED: Run text model with focused parameters.
    """
    model = TEXT_MODELS.get(mode, TEXT_MODELS["default"])
    
    try:
        resp = ollama_client.chat(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an eSim and electronics expert. Be concise, accurate, and practical."
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


def get_embedding(text: str):
    """
    OPTIMIZED: Get text embeddings for RAG.
    """
    try:
        r = ollama_client.embeddings(model=EMBED_MODEL, prompt=text)
        return r["embedding"]
    except Exception as e:
        print(f"[EMBED ERROR] {e}")
        return None
