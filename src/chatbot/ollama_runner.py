import os
import re
import logging
from typing import List
import ollama
from chatbot.graph_rag import eSimGraphRAG

logger = logging.getLogger(__name__)

# Singleton GraphRAG instance
_graph_rag = eSimGraphRAG()

def run_ollama(prompt: str, model_name: str = "qwen2.5:3b") -> str:
    """
    Executes Ollama generation with integrated GraphRAG context injection.
    """
    try:
        # Retrieve topological graph context
        graph_context = _graph_rag.get_topology_context(prompt)
        
        # Inject context into system/prompt prefix if present
        if graph_context:
            logger.info("Injecting GraphRAG topology context into prompt.")
            augmented_prompt = f"{graph_context}\nUser Request:\n{prompt}"
        else:
            augmented_prompt = prompt

        response = ollama.generate(model=model_name, prompt=augmented_prompt)
        return response.get("response", "")
    except Exception as e:
        logger.error(f"Ollama execution error: {e}")
        return f"[Ollama Error]: {str(e)}"

def run_ollama_vision(prompt: str, image_path: str, model_name: str = "qwen2.5-vl:3b") -> str:
    """Executes multimodal vision queries for KiCad schematics."""
    try:
        if not os.path.exists(image_path):
            return "Error: Schematic image file not found."

        response = ollama.generate(
            model=model_name,
            prompt=prompt,
            images=[image_path]
        )
        return response.get("response", "")
    except Exception as e:
        logger.error(f"Ollama vision execution error: {e}")
        return f"[Ollama Vision Error]: {str(e)}"

def get_embedding(text: str, model_name: str = "nomic-embed-text") -> List[float]:
    """Generates text embeddings via Ollama for ChromaDB indexing."""
    try:
        response = ollama.embeddings(model=model_name, prompt=text)
        return response.get("embedding", [])
    except Exception as e:
        logger.error(f"Ollama embedding error: {e}")
        return []
