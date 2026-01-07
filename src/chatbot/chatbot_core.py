# chatbot_core.py

import os
import re
import json
from typing import Dict, Any, Tuple, List

from .error_solutions import get_error_solution
from .image_handler import analyze_and_extract
from .ollama_runner import run_ollama
from .knowledge_base import search_knowledge

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
NOTE: This gets overwritten when you "Convert KiCad to NgSpice" again

Method 2 - Component Properties (PERMANENT):
1. Open KiCad schematic (double-click .proj in Project Explorer)
2. Find the component that uses the missing model (e.g., transistor Q1)
3. Right-click on it → Properties (or press E when hovering over it)
4. Click "Edit Spice Model" button in the Properties dialog
5. In the Spice Model field, paste the model definition:
   .model Q2N3904 NPN(Bf=200 Is=1e-14 Vaf=100)
6. Click OK → Save schematic (Ctrl+S)
7. eSim: Simulation → Convert KiCad to NgSpice
NOTE: This permanently associates the model with the component

Method 3 - Include Library:
1. Spice Editor → Open .cir.out
2. Add at top: .include /usr/share/ngspice/models/bjt.lib
3. Save → Simulate

HOW TO FIX MISSING SUBCIRCUITS:
1. Spice Editor → Open .cir.out
2. Add before .end:
   .subckt OPAMP_IDEAL inp inn out vdd vss
     Rin inp inn 1Meg
     E1 out 0 inp inn 100000
     Rout out 0 75
   .ends
3. Save → Simulate
OR: Replace with eSim library opamp (uA741, LM324)

HOW TO FIX FLOATING NODES:
1. Open KiCad schematic
2. Find the unconnected pin/node
3. Either connect it with wire (press W) or delete component
4. For sense points: Add Rleak node 0 1Meg
5. Save → Convert to NgSpice

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
Open KiCad: Double-click .proj file in Project Explorer

FILE LOCATIONS:
Project folder: ~/eSim-Workspace/<project_name>/
Netlist: <project_name>.cir.out
Schematic: <project_name>.proj
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

def detect_esim_errors(image_context: Dict[str, Any], user_input: str) -> str:
    """
    Display errors from hybrid analysis with SMART FILTERING to remove hallucinations.
    """
    if not image_context:
        return ""

    analysis = image_context.get("circuit_analysis", {})
    raw_errors = analysis.get("design_errors", [])
    warnings = analysis.get("design_warnings", [])

    # === SMART FILTERING ===
    components_str = str(image_context.get("components", [])).lower()
    summary_str = str(image_context.get("vision_summary", "")).lower()
    context_text = components_str + summary_str

    filtered_errors: List[str] = []
    for err in raw_errors:
        err_lower = err.lower()

        # 1. Filter "No ground" if ground is actually detected
        if "ground" in err_lower and (
            "gnd" in context_text or "ground" in context_text or " 0 " in context_text
        ):
            continue

        # 2. Filter "Floating node" if it refers to Vin/Vout labels
        if "floating" in err_lower and (
            "vin" in err_lower or "vout" in err_lower or "label" in err_lower
        ):
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
        output.append("\n**🔧 FIX:** Add 1GΩ resistors to all nodes → GND")
    if "timestep" in text:
        output.append("\n**🔧 FIX:** Reduce timestep or add 0.1Ω series R")

    if not output:
        return "**✅ No errors detected**"

    return "\n".join(output)


# ==================== UTILITIES ====================

VALID_EXTS = (".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".gif")


def _is_image_file(path: str) -> bool:
    if not path:
        return False
    clean = re.sub(r"\[Image:\s*(.*?)\]", r"\1", path).strip()
    return clean.lower().endswith(VALID_EXTS)


def _is_image_query(user_input: str) -> bool:
    if not user_input:
        return False
    if "[Image:" in user_input:
        return True
    if "|" in user_input:
        parts = user_input.split("|", 1)
        if len(parts) == 2 and _is_image_file(parts[1]):
            return True
    return _is_image_file(user_input)


def _parse_image_query(user_input: str) -> Tuple[str, str]:
    user_input = user_input.strip()

    match = re.search(r"\[Image:\s*(.*?)\]", user_input)
    if match:
        return user_input.replace(match.group(0), "").strip(), match.group(1).strip()

    if "|" in user_input:
        q, p = [x.strip() for x in user_input.split("|", 1)]
        if _is_image_file(p):
            return q, p
        if _is_image_file(q):
            return p, q

    if _is_image_file(user_input):
        return "", user_input

    return user_input, ""


def clean_response_raw(raw: str) -> str:
    cleaned = re.sub(r"<\|.*?\|>", "", raw.strip())
    cleaned = re.sub(r"\[Context:.*?\]", "", cleaned, flags=re.DOTALL)
    cleaned = re.sub(r"\[FACT .*?\]", "", cleaned, flags=re.MULTILINE)
    cleaned = re.sub(
        r"\[ESIM_NETLIST_START\].*?\[ESIM_NETLIST_END\]", "", cleaned, flags=re.DOTALL
    )
    return cleaned.strip()


def _history_to_text(history: List[Dict[str, str]] | None, max_turns: int = 6) -> str:
    """Convert history to readable text with MORE context (6 turns)."""
    if not history:
        return ""
    recent = history[-max_turns:]
    lines: List[str] = []
    for i, t in enumerate(recent, 1):
        u = (t.get("user") or "").strip()
        b = (t.get("bot") or "").strip()
        if u:
            lines.append(f"[Turn {i}] User: {u}")
        if b:
            # Truncate very long bot responses to save token space
            if len(b) > 300:
                b = b[:300] + "..."
            lines.append(f"[Turn {i}] Assistant: {b}")
    return "\n".join(lines).strip()


def _is_follow_up_question(user_input: str, history: List[Dict[str, str]] | None) -> bool:
    """
    Detect if this is a follow-up question that needs history context.
    Returns True if question lacks standalone context.
    """
    if not history:
        return False
    
    user_lower = user_input.lower().strip()
    words = user_lower.split()
    
    
    if len(words) <= 7:
        return True
    
    # Questions with pronouns (referring to previous context)
    pronouns = ["it", "that", "this", "those", "these", "they", "them"]
    if any(pronoun in words for pronoun in pronouns):
        return True
    
    # Continuation phrases
    continuations = [
        "what next", "next step", "after that", "and then", "then what",
        "what about", "how about", "what if", "but why", "why not"
    ]
    if any(phrase in user_lower for phrase in continuations):
        return True
    
    # Question words at start without enough context
    question_starters = ["why", "how", "where", "when", "what", "which"]
    if words[0] in question_starters and len(words) <= 5:
        return True
    
    return False


# ==================== QUESTION CLASSIFICATION ====================

def classify_question_type(user_input: str, has_image_context: bool,
                           history: List[Dict[str, str]] | None = None) -> str:
    """
    Classify question type for smart routing.
    Returns: 'greeting', 'simple', 'esim', 'image_query', 'follow_up_image', 
             'follow_up', 'netlist'
    """
    user_lower = user_input.lower()

    # Explicit netlist block
    if "[ESIM_NETLIST_START]" in user_input:
        return "netlist"

    # Image: new upload
    if _is_image_query(user_input):
        return "image_query"

    # Follow-up about image
    if has_image_context:
        follow_phrases = [
            "this circuit", "that circuit", "in this schematic",
            "components here", "what is the value", "how many",
            "the circuit", "this schematic","what","can","how"
        ]
        if any(p in user_lower for p in follow_phrases):
            return "follow_up_image"

    # Simple greeting
    greetings = ["hello", "hi", "hey", "howdy", "greetings"]
    user_words = user_lower.strip().split()
    if len(user_words) <= 3 and any(g in user_words for g in greetings):
        return "greeting"

    # Detect generic follow-up (needs history)
    if _is_follow_up_question(user_input, history):
        return "follow_up"

    # eSim-related keywords
    esim_keywords = [
        "esim", "kicad", "ngspice", "spice", "simulation", "netlist",
        "schematic", "convert", "gnd", "ground", ".model", ".subckt",
        "singular matrix", "floating", "timestep", "convergence"
    ]
    if any(keyword in user_lower for keyword in esim_keywords):
        return "esim"

    # Error-related
    error_keywords = [
        "error", "fix", "problem", "issue", "warning", "missing",
        "not working", "failed", "crash"
    ]
    if any(keyword in user_lower for keyword in error_keywords):
        return "esim"

    return "simple"


# ==================== HANDLERS ====================

def handle_greeting() -> str:
    return (
        "Hello! I'm eSim Copilot. I can help you with:\n"
        "• Circuit analysis and netlist debugging\n"
        "• Electronics concepts and SPICE simulation\n"
        "• Component selection and circuit design\n\n"
        "What would you like to know?"
    )


def handle_simple_question(user_input: str) -> str:
    prompt = (
        "You are an electronics expert. Answer this question concisely (2-3 sentences max).\n"
        "Use your general electronics knowledge. Do NOT make up eSim-specific commands.\n\n"
        f"Question: {user_input}\n\n"
        "Answer (brief and factual):"
    )
    return run_ollama(prompt, mode="default")


def handle_follow_up(user_input: str,
                     image_context: Dict[str, Any],
                     history: List[Dict[str, str]] | None = None) -> str:
    """
    Handle follow-up questions that depend on conversation history.
    This handler PRIORITIZES history over RAG.
    """
    history_text = _history_to_text(history, max_turns=6)
    
    if not history_text:
        return "I need more context. Could you provide more details about your question?"
    
    # Get minimal RAG context (only if keywords detected)
    rag_context = ""
    user_lower = user_input.lower()
    if any(kw in user_lower for kw in ["model", "spice", "ground", "error", "netlist"]):
        rag_context = search_knowledge(user_input, n_results=2)
    
    prompt = (
        "You are an eSim expert assistant. The user is asking a follow-up question.\n\n"
        "=== CONVERSATION HISTORY (MOST IMPORTANT) ===\n"
        f"{history_text}\n"
        "=============================================\n\n"
        f"=== CURRENT USER QUESTION (FOLLOW-UP) ===\n{user_input}\n\n"
    )
    
    if rag_context:
        prompt += f"=== REFERENCE MANUAL (if needed) ===\n{rag_context}\n\n"
    
    if image_context:
        prompt += (
            f"=== CURRENT CIRCUIT CONTEXT ===\n"
            f"Type: {image_context.get('circuit_analysis', {}).get('circuit_type', 'Unknown')}\n"
            f"Components: {image_context.get('components', [])}\n\n"
        )
    
    prompt += (
        "CRITICAL INSTRUCTIONS:\n"
        "1. The user's question refers to the CONVERSATION HISTORY above.\n"
        "2. Identify what 'it', 'that', 'this', or 'next step' refers to by reading the history.\n"
        "3. Answer based on the conversation context first, then use manual/workflows if needed.\n"
        "4. If the user asks 'why', explain based on what was just discussed.\n"
        "5. If the user asks 'what next' or 'next step', continue from the last instruction.\n"
        "6. Be specific and reference what you're talking about (e.g., 'In the previous step, I mentioned...').\n"
        "7. Keep answer concise (max 150 words).\n\n"
        "Answer:"
    )
    
    return run_ollama(prompt, mode="default")


def handle_esim_question(user_input: str,
                         image_context: Dict[str, Any],
                         history: List[Dict[str, str]] | None = None) -> str:
    """
    Handle eSim-specific questions with RAG + conversation history.
    """
    user_lower = user_input.lower()

    # Fast path: known ngspice error messages → structured fixes
    sol = get_error_solution(user_input)
    if sol and sol.get("description") != "General schematic error":
        fixes = "\n".join(f"- {f}" for f in sol.get("fixes", []))
        cmd = sol.get("eSim_command", "")
        answer = (
            f"**Detected issue:** {sol['description']}\n"
            f"**Severity:** {sol.get('severity', 'unknown')}\n\n"
            f"**Recommended fixes:**\n{fixes}\n\n"
        )
        if cmd:
            answer += f"**eSim action:** {cmd}\n"
        return answer

    # Build history text
    history_text = _history_to_text(history, max_turns=6)

    # RAG context
    rag_context = search_knowledge(user_input, n_results=5)

    image_context_str = ""
    if image_context:
        image_context_str = (
            f"\n=== CURRENT CIRCUIT ===\n"
            f"Type: {image_context.get('circuit_analysis', {}).get('circuit_type', 'Unknown')}\n"
            f"Components: {image_context.get('components', [])}\n"
            f"Values: {image_context.get('values', {})}\n"
        )

    prompt = (
        "You are an eSim expert. Answer using the workflows, manual, and conversation history.\n\n"
        f"{ESIM_WORKFLOWS}\n\n"
        f"=== MANUAL CONTEXT ===\n{rag_context}\n"
        f"{image_context_str}\n"
    )
    
    if history_text:
        prompt += f"=== CONVERSATION HISTORY ===\n{history_text}\n\n"
    
    prompt += (
        f"USER QUESTION: {user_input}\n\n"
        "INSTRUCTIONS:\n"
        "1. If the question refers to previous conversation, use the history.\n"
        "2. Use exact menu paths and shortcuts from the workflows when relevant.\n"
        "3. If the manual context does not contain the answer, say you need to check the manual.\n"
        "4. Keep the answer concise (max 150 words).\n\n"
        "Answer:"
    )

    return run_ollama(prompt, mode="default")


def handle_image_query(user_input: str) -> Tuple[str, Dict[str, Any]]:
    """
    Handle image analysis queries.
    Returns: (response_text, image_context_dict)
    """
    question, image_path = _parse_image_query(user_input)
    image_path = image_path.strip("'\"").strip()

    if not image_path or not os.path.exists(image_path):
        return f"Error: Image not found: {image_path}", {}

    extraction = analyze_and_extract(image_path)

    if extraction.get("error"):
        return f"Analysis Failed: {extraction['error']}", {}

    # No follow-up question → summary
    if not question:
        error_report = detect_esim_errors(extraction, "")

        summary = (
            "**Image Analysis Complete**\n"
            f"**Type:** {extraction.get('circuit_analysis', {}).get('circuit_type', 'Unknown')}\n"
            f"**Components:** {extraction.get('component_counts', {})}\n"
            f"**Description:** {extraction.get('vision_summary', '')}\n\n"
        )

        if extraction.get("components"):
            summary += f"**Detected Components:** {', '.join(extraction['components'])}\n"

        if extraction.get("values"):
            summary += "**Component Values:**\n"
            for comp, val in extraction["values"].items():
                summary += f"  • {comp}: {val}\n"

        summary += (
            "\n**Note:** Vision analysis may have errors. Use 'Analyze netlist' for precise results.\n"
        )

        if "🚨" in error_report or "⚠️" in error_report:
            summary += f"\n{error_report}"

        return summary, extraction

    # There is a textual question about this image
    return handle_follow_up_image_question(question, extraction), extraction


def handle_follow_up_image_question(user_input: str,
                                    image_context: Dict[str, Any]) -> str:
    """
    Answer questions about an analyzed image using ONLY extracted data.
    """
    image_context_str = (
        f"**Circuit Type:** {image_context.get('circuit_analysis', {}).get('circuit_type', 'Unknown')}\n"
        f"**Components Detected:** {image_context.get('components', [])}\n"
        f"**Component Values:** {image_context.get('values', {})}\n"
        f"**Component Counts:** {image_context.get('component_counts', {})}\n"
        f"**Description:** {image_context.get('vision_summary', '')}\n"
    )

    prompt = (
        "You are analyzing a circuit schematic. Answer using ONLY the circuit data below.\n\n"
        "=== ANALYZED CIRCUIT DATA ===\n"
        f"{image_context_str}\n"
        "==============================\n\n"
        f"USER QUESTION: {user_input}\n\n"
        "STRICT INSTRUCTIONS:\n"
        "1. Answer ONLY using the circuit data above - DO NOT use external knowledge.\n"
        "2. For counts: use 'Component Counts'.\n"
        "3. For values: use 'Component Values'.\n"
        "4. For lists: use 'Components Detected'.\n"
        "5. If data is missing, answer: 'The image analysis did not detect that information.'\n"
        "6. Keep answer brief (2-3 sentences).\n\n"
        "Answer:"
    )

    return run_ollama(prompt, mode="default")


def handle_netlist_analysis(user_input: str) -> str:
    """
    Handle netlist analysis prompts (FACT-based prompt from GUI).
    """
    raw_reply = run_ollama(user_input)
    return clean_response_raw(raw_reply)


# ==================== MAIN ROUTER ====================

def handle_input(user_input: str,
                 history: List[Dict[str, str]] | None = None) -> str:
    """
    Main router. Accepts optional conversation history for follow-up understanding.
    """
    global LAST_IMAGE_CONTEXT, LAST_BOT_REPLY

    user_input = (user_input or "").strip()
    if not user_input:
        return "Please enter a query."

    # Special case: raw netlist block
    if "[ESIM_NETLIST_START]" in user_input:
        raw_reply = run_ollama(user_input)
        cleaned = clean_response_raw(raw_reply)
        LAST_BOT_REPLY = cleaned
        return cleaned

    # Classify
    question_type = classify_question_type(
        user_input, bool(LAST_IMAGE_CONTEXT), history
    )
    print(f"[COPILOT] Question type: {question_type}")

    try:
        if question_type == "netlist":
            response = handle_netlist_analysis(user_input)

        elif question_type == "greeting":
            response = handle_greeting()

        elif question_type == "image_query":
            response, LAST_IMAGE_CONTEXT = handle_image_query(user_input)

        elif question_type == "follow_up_image":
            response = handle_follow_up_image_question(user_input, LAST_IMAGE_CONTEXT)

        elif question_type == "follow_up":
            # NEW: Dedicated follow-up handler
            response = handle_follow_up(user_input, LAST_IMAGE_CONTEXT, history)

        elif question_type == "simple":
            response = handle_simple_question(user_input)

        else:  # "esim" or fallback
            response = handle_esim_question(user_input, LAST_IMAGE_CONTEXT, history)

        LAST_BOT_REPLY = response
        return response

    except Exception as e:
        error_msg = f"Error processing question: {str(e)}"
        print(f"[COPILOT ERROR] {error_msg}")
        return error_msg


# ==================== WRAPPER ====================

class ESIMCopilotWrapper:
    def __init__(self) -> None:
        self.history: List[Dict[str, str]] = []

    def handle_input(self, user_input: str) -> str:
        reply = handle_input(user_input, self.history)
        self.history.append({"user": user_input, "bot": reply})
        if len(self.history) > 12:
            self.history = self.history[-12:]
        return reply

    def analyze_schematic(self, query: str) -> str:
        return self.handle_input(query)

# Global wrapper so history persists across calls from GUI
_GLOBAL_WRAPPER = ESIMCopilotWrapper()


def analyze_schematic(query: str) -> str:
    return _GLOBAL_WRAPPER.handle_input(query)
