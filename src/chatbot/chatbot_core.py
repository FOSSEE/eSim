# chatbot_core.py

import os
import re
import json
import numpy as np
from typing import Dict, Any, Tuple, List
from sklearn.metrics.pairwise import cosine_similarity
from .error_solutions import get_error_solution
from .image_handler import analyze_and_extract
from .ollama_runner import run_ollama
from .knowledge_base import search_knowledge
from .ollama_runner import get_embedding

import os
import json

# === LOAD CONFIGURATION ===
# This lets the user change rules without touching Python code
def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    try:
        with open(config_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        # Fallback if the user deletes the file by accident
        return {"system_rules": "Be concise.", "memory_history_limit": 5}

USER_CONFIG = load_config()
STRICT_CONCISE_RULES = USER_CONFIG.get("system_rules", "Be concise.")

# ==================== ESIM WORKFLOW KNOWLEDGE ====================

ESIM_WORKFLOWS = """
=== COMMON ESIM WORKFLOWS ===

HOW TO ADD GROUND:
1. In KiCad schematic, press 'A' key (Add Component)
2. Type "GND" in the search box
3. Select ground symbol from "power" library
4. Click to place it on schematic
5. Press 'W' to add wire and connect to circuit
6. Save (Ctrl+S) → eSim: Simulation → Convert KiCad to NgSpice

HOW TO ADD ANY COMPONENT:
1. In KiCad schematic, press 'A' key
2. Type component name (e.g., "Q2N3904", "1N4148", "uA741")
3. Select from appropriate library (eSim_Devices, eSim_Subckt, etc.)
4. Place on schematic and connect with wires
5. Save → Convert KiCad to NgSpice

HOW TO FIX MISSING SPICE MODELS (3 Methods):

Method 1 - Direct Netlist Edit (FASTEST, but temporary):
1. eSim: Tools → Spice Editor (or Ctrl+E)
2. Open your_project.cir.out file
3. Scroll to bottom (before .end line)
4. Add model definition:
   BJT: .model Q2N3904 NPN(Bf=200 Is=1e-14 Vaf=100)
   Diode: .model 1N4148 D(Is=1e-14 Rs=1)
   Zener: .model DZ5V1 D(Is=1e-14 Bv=5.1 Ibv=5m)
5. Save (Ctrl+S) → Run Simulation

Method 2 - Component Properties (PERMANENT):
1. Open KiCad schematic (double-click .proj in Project Explorer)
2. Right-click on component → Properties (or press E)
3. Click "Edit Spice Model" button
4. In the Spice Model field, paste the model definition.
5. Click OK → Save schematic (Ctrl+S) → Convert KiCad to NgSpice

Method 3 - Include Library:
1. Spice Editor → Open .cir.out
2. Add at top: .include /usr/share/ngspice/models/bjt.lib
3. Save → Simulate

HOW TO FIX MISSING SUBCIRCUITS:
1. Spice Editor → Open .cir.out
2. Add .subckt ... .ends block before .end.
OR: Replace with eSim library opamp (uA741, LM324)

HOW TO FIX FLOATING NODES:
1. Open KiCad schematic.
2. Connect pin with wire (W) or delete component.
3. For sense points: Add Rleak node 0 1Meg.
4. Save → Convert to NgSpice.

KICAD SHORTCUTS:
A = Add component
W = Add wire
M = Move item
R = Rotate item
C = Copy item
Delete = Remove item
Ctrl+S = Save

ESIM MENU PATHS:
Convert to NgSpice: Simulation → Convert KiCad to NgSpice
Run Simulation: Simulation → Simulate
Spice Editor: Tools → Spice Editor (Ctrl+E)
Model Editor: Tools → Model Editor
"""

LAST_BOT_REPLY: str = ""
LAST_IMAGE_CONTEXT: Dict[str, Any] = {}
LAST_NETLIST_ISSUES: Dict[str, Any] = {}

def get_history() -> Dict[str, Any]:
    return LAST_IMAGE_CONTEXT

def clear_history() -> None:
    global LAST_IMAGE_CONTEXT, LAST_NETLIST_ISSUES
    LAST_IMAGE_CONTEXT = {}
    LAST_NETLIST_ISSUES = {}

# ==================== ESIM ERROR LOGIC ====================

def answer_with_rag_fallback(user_input: str) -> str:
    rag_context = search_knowledge(user_input)
    
    if rag_context.strip():
        prompt = f"""
You are eSim Copilot. {STRICT_CONCISE_RULES}
Use ONLY this official eSim documentation:
{rag_context}

Question: {user_input}
Answer:"""
        return run_ollama(prompt)

    prompt = f"""
You are eSim Copilot. {STRICT_CONCISE_RULES}
Answer clearly: {user_input}
"""
    return run_ollama(prompt)

def detect_esim_errors(image_context: Dict[str, Any], user_input: str) -> str:
    if not image_context:
        return ""

    analysis = image_context.get("circuit_analysis", {})
    raw_errors = analysis.get("design_errors", [])
    warnings = analysis.get("design_warnings", [])

    components_str = str(image_context.get("components", [])).lower()
    summary_str = str(image_context.get("vision_summary", "")).lower()
    context_text = components_str + summary_str

    filtered_errors: List[str] = []
    for err in raw_errors:
        err_lower = err.lower()
        if "ground" in err_lower and ("gnd" in context_text or "ground" in context_text or " 0 " in context_text):
            continue
        if "floating" in err_lower and ("vin" in err_lower or "vout" in err_lower or "label" in err_lower):
            continue
        filtered_errors.append(err)

    output: List[str] = []
    if filtered_errors:
        output.append("**🚨 CRITICAL ERRORS:**")
        for err in filtered_errors:
            output.append(f"❌ {err}")

    if warnings:
        output.append("\n**⚠️ WARNINGS:**")
        for warn in warnings:
            output.append(f"⚠️ {warn}")

    text = user_input.lower()
    if "singular matrix" in text:
        output.append("\n**🔧 FIX:** Add 1GΩ resistors to all nodes → **GND**")
    if "timestep" in text:
        output.append("\n**🔧 FIX:** Reduce timestep or add 0.1Ω series R")

    return "\n".join(output) if output else "**✅ No errors detected**"

# ==================== UTILITIES ====================

VALID_EXTS = (".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".gif")

def _is_image_file(path: str) -> bool:
    if not path: return False
    clean = re.sub(r"\[Image:\s*(.*?)\]", r"\1", path).strip()
    return clean.lower().endswith(VALID_EXTS)

def _is_image_query(user_input: str) -> bool:
    if not user_input: return False
    if "[Image:" in user_input: return True
    if "|" in user_input:
        parts = user_input.split("|", 1)
        if len(parts) == 2 and _is_image_file(parts[1]): return True
    return _is_image_file(user_input)

def _parse_image_query(user_input: str) -> Tuple[str, str]:
    user_input = user_input.strip()
    match = re.search(r"\[Image:\s*(.*?)\]", user_input)
    if match: return user_input.replace(match.group(0), "").strip(), match.group(1).strip()
    if "|" in user_input:
        q, p = [x.strip() for x in user_input.split("|", 1)]
        if _is_image_file(p): return q, p
        if _is_image_file(q): return p, q
    if _is_image_file(user_input): return "", user_input
    return user_input, ""

def clean_response_raw(raw: str) -> str:
    cleaned = re.sub(r"<\|.*?\|>", "", raw.strip())
    cleaned = re.sub(r"\[Context:.*?\]", "", cleaned, flags=re.DOTALL)
    cleaned = re.sub(r"\[FACT .*?\]", "", cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r"\[ESIM_NETLIST_START\].*?\[ESIM_NETLIST_END\]", "", cleaned, flags=re.DOTALL)
    return cleaned.strip()

def _history_to_text(history: List[Dict[str, str]] | None, max_turns: int = 6) -> str:
    if not history: return ""
    recent = history[-max_turns:]
    lines: List[str] = []
    for i, t in enumerate(recent, 1):
        u = (t.get("user") or "").strip()
        b = (t.get("bot") or "").strip()
        if u: lines.append(f"[Turn {i}] User: {u}")
        if b: lines.append(f"[Turn {i}] Assistant: {b[:300]}...")
    return "\n".join(lines).strip()

def _is_follow_up_question(user_input: str, history: List[Dict[str, str]] | None) -> bool:
    if not history: return False
    user_lower = user_input.lower().strip()
    words = user_lower.split()
    if len(words) <= 7: return True
    pronouns = ["it", "that", "this", "those", "these", "they", "them"]
    if any(pronoun in words for pronoun in pronouns): return True
    continuation_phrases = ["what next", "next step", "after that", "and then"]
    if any(phrase in user_lower for phrase in continuation_phrases): return True
    return False

def is_semantic_topic_switch(user_input: str, history: list, threshold: float = 0.30) -> bool:
    if not history: return False
    last_assistant_msg = next((item.get("content") for item in reversed(history) if item.get("role") == "assistant"), None)
    if not last_assistant_msg: return False
    try:
        emb_new = np.array(get_embedding(user_input))
        emb_prev = np.array(get_embedding(last_assistant_msg))
        similarity = np.dot(emb_new, emb_prev) / (np.linalg.norm(emb_new) * np.linalg.norm(emb_prev))
        return similarity < threshold
    except: return False

# ==================== QUESTION CLASSIFICATION ====================

def classify_question_type(user_input: str, has_image_context: bool, history: List[Dict[str, str]] | None = None) -> str:
    user_lower = user_input.lower()
    if "[ESIM_NETLIST_START]" in user_input: return "netlist"
    if _is_image_query(user_input): return "image_query"
    if has_image_context and any(p in user_lower for p in ["this circuit", "that circuit", "schematic"]): return "follow_up_image"
    
    greetings = ["hello", "hi", "hey"]
    if len(user_lower.split()) <= 2 and any(g in user_lower for g in greetings): return "greeting"

    is_followup = _is_follow_up_question(user_input, history)
    if is_semantic_topic_switch(user_input, history): is_followup = False
    
    esim_keywords = ["esim", "kicad", "ngspice", "spice", "netlist", "convert", "gnd"]
    if any(kw in user_lower for kw in esim_keywords): return "esim"
    
    return "follow_up" if is_followup else "simple"

# ==================== HANDLERS ====================

def handle_greeting() -> str:
    return "Hello! I'm **eSim Copilot**. I can help with circuit analysis, **KiCad** workflows, and **NgSpice** debugging. What's your query?"

def handle_simple_question(user_input: str) -> str:
    return answer_with_rag_fallback(user_input)

def handle_follow_up(user_input: str, image_context: Dict[str, Any], history: List[Dict[str, str]] | None = None) -> str:
    history_text = _history_to_text(history)
    rag_context = search_knowledge(user_input, n_results=2) if any(kw in user_input.lower() for kw in ["model", "spice", "error"]) else ""
    
    prompt = (
        f"You are eSim Copilot. {STRICT_CONCISE_RULES}\n"
        f"=== HISTORY ===\n{history_text}\n"
        f"=== QUESTION ===\n{user_input}\n"
        "INSTRUCTIONS: Use history to resolve pronouns like 'it' or 'that'.\nAnswer:"
    )
    return run_ollama(prompt)

def handle_esim_question(user_input: str, image_context: Dict[str, Any], history: List[Dict[str, str]] | None = None) -> str:
    sol = get_error_solution(user_input)
    if sol and sol.get("description") != "General schematic error":
        return f"**Issue:** {sol['description']}\n**Fixes:**\n" + "\n".join(f"- {f}" for f in sol.get("fixes", []))

    rag_context = search_knowledge(user_input, n_results=5)
    prompt = (
        f"You are eSim Copilot. {STRICT_CONCISE_RULES}\n"
        f"{ESIM_WORKFLOWS}\n"
        f"=== MANUAL ===\n{rag_context}\n"
        f"USER QUESTION: {user_input}\n"
        "INSTRUCTIONS: Use shortcuts (A, W) and menu paths. If not in manual, say 'Info not in docs.'\nAnswer:"
    )
    return run_ollama(prompt)

def handle_image_query(user_input: str) -> Tuple[str, Dict[str, Any]]:
    question, image_path = _parse_image_query(user_input)
    image_path = image_path.strip("'\" ").strip()
    if not os.path.exists(image_path): return "Error: Image not found.", {}
    
    extraction = analyze_and_extract(image_path)
    if extraction.get("error"): return f"Analysis Failed: {extraction['error']}", {}
    
    if not question:
        error_report = detect_esim_errors(extraction, "")
        summary = f"**Image Analysis Complete**\n- **Type:** {extraction.get('circuit_analysis', {}).get('circuit_type', 'Unknown')}\n"
        summary += f"- **Components:** {extraction.get('component_counts', {})}\n\n{error_report}"
        return summary, extraction
        
    return handle_follow_up_image_question(question, extraction), extraction

def handle_follow_up_image_question(user_input: str, image_context: Dict[str, Any]) -> str:
    prompt = (
        f"You are eSim Copilot. {STRICT_CONCISE_RULES}\n"
        f"=== CIRCUIT DATA ===\n{image_context}\n"
        f"QUESTION: {user_input}\n"
        "INSTRUCTIONS: Answer ONLY using provided circuit data. Use brief bullets.\nAnswer:"
    )
    return run_ollama(prompt)

def handle_netlist_analysis(user_input: str) -> str:
    return clean_response_raw(run_ollama(user_input))

# ==================== MAIN ROUTER ====================

def handle_input(user_input: str, history: List[Dict[str, str]] | None = None) -> str:
    global LAST_IMAGE_CONTEXT, LAST_BOT_REPLY
    user_input = (user_input or "").strip()
    if not user_input: return "Please enter a query."

    q_type = classify_question_type(user_input, bool(LAST_IMAGE_CONTEXT), history)
    print(f"[COPILOT] Type: {q_type}")

    try:
        if q_type == "netlist": response = handle_netlist_analysis(user_input)
        elif q_type == "greeting": response = handle_greeting()
        elif q_type == "image_query": response, LAST_IMAGE_CONTEXT = handle_image_query(user_input)
        elif q_type == "follow_up_image": response = handle_follow_up_image_question(user_input, LAST_IMAGE_CONTEXT)
        elif q_type == "esim": response = handle_esim_question(user_input, LAST_IMAGE_CONTEXT, history)
        elif q_type == "follow_up": response = handle_follow_up(user_input, LAST_IMAGE_CONTEXT, history)
        else: response = handle_simple_question(user_input)

        LAST_BOT_REPLY = response
        return response
    except Exception as e:
        return f"Error: {str(e)}"

class ESIMCopilotWrapper:
    def __init__(self) -> None:
        self.history: List[Dict[str, str]] = []
        # Pull the memory limit from the config file
        self.max_history = USER_CONFIG.get("memory_history_limit", 5)

    def handle_input(self, user_input: str) -> str:
        reply = handle_input(user_input, self.history)
        self.history.append({"user": user_input, "bot": reply})
        
        # Use the config variable instead of a hardcoded number
        if len(self.history) > self.max_history: 
            self.history = self.history[-self.max_history:]
        return reply

_GLOBAL_WRAPPER = ESIMCopilotWrapper()
def analyze_schematic(query: str) -> str:
    return _GLOBAL_WRAPPER.handle_input(query)