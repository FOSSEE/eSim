import sys
import os
import re,threading
from configuration.Appconfig import Appconfig
from chatbot.stt_handler import listen_to_mic
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit,
    QPushButton, QLabel, QFileDialog, QMessageBox, QApplication, QWidget
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
MANUALS_DIR = os.path.join(os.path.dirname(__file__), "manuals")
NETLIST_CONTRACT = ""

try:
    contract_path = os.path.join(MANUALS_DIR, "esim_netlist_analysis_output_contract.txt")
    with open(contract_path, "r", encoding="utf-8") as f:
        NETLIST_CONTRACT = f.read()
        print(f"[COPILOT] Loaded netlist contract from {contract_path}")
except Exception as e:
    print(f"[COPILOT] WARNING: Could not load netlist contract: {e}")
    NETLIST_CONTRACT = (
        "You are a SPICE netlist analyzer.\n"
        "Use the FACT lines to detect issues.\n"
        "Output sections:\n"
        "1. Syntax / SPICE rule errors\n"
        "2. Topology / connection problems\n"
        "3. Simulation setup issues (.ac/.tran/.op etc.)\n"
        "4. Summary\n"
        "Do NOT invent issues not present in FACT lines.\n"
    )

current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
if src_dir not in sys.path:
    sys.path.append(src_dir)

from chatbot.chatbot_core import handle_input, ESIMCopilotWrapper, clear_history

import subprocess
import tempfile

def _validate_netlist_with_ngspice(netlist_text: str) -> bool:
    """
    Run ngspice in batch mode to check for SYNTAX errors only.
    Returns True if syntax is valid, False for actual parse errors.
    Ignores model/library warnings.
    """
    try:
        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.cir', delete=False, encoding='utf-8'
        ) as tmp:
            tmp.write(netlist_text)
            tmp_path = tmp.name

        result = subprocess.run(
            ['ngspice', '-b', tmp_path],
            capture_output=True,
            text=True,
            timeout=5
        )

        try:
            os.unlink(tmp_path)
        except:
            pass

        stderr_lower = result.stderr.lower()
        
        syntax_errors = [
            'syntax error',
            'unrecognized',
            'parse error',
            'fatal',
        ]
        
        ignore_patterns = [
            'model',
            'library',
            'warning',
            'no such file',
            'cannot find',
        ]

        for line in stderr_lower.split('\n'):
            if any(pattern in line for pattern in ignore_patterns):
                continue
            if any(err in line for err in syntax_errors):
                print(f"[COPILOT] Syntax error: {line}")
                return False

        return True

    except Exception as e:
        print(f"[COPILOT] Validation exception: {e}")
        return True  


def _detect_missing_subcircuits(netlist_text: str) -> list:
    """
    Detect subcircuits that are referenced but not defined.
    Returns list of (subckt_name, [(line_num, instance_name), ...]) tuples.
    """
    import re
    
    referenced_subckts = {}
    defined_subckts = set()
    lines = netlist_text.split('\n')
    
    for line_num, line in enumerate(lines, start=1):
        line = line.strip()
        if not line or line.startswith('*'):
            continue
        
        if line.lower().startswith('.subckt'):
            tokens = line.split()
            if len(tokens) >= 2:
                defined_subckts.add(tokens[1].upper())
        
        elif line.lower().startswith('.include') or line.lower().startswith('.lib'):
            return []
        
        elif line[0].upper() == 'X':
            tokens = line.split()
            if len(tokens) < 2:
                continue
            
            instance_name = tokens[0]
            subckt_name = tokens[-1].upper()
            
            if '=' in subckt_name:
                for tok in reversed(tokens[1:]):
                    if '=' not in tok:
                        subckt_name = tok.upper()
                        break
            
            if subckt_name not in referenced_subckts:
                referenced_subckts[subckt_name] = []
            referenced_subckts[subckt_name].append((line_num, instance_name))
    
    missing = []
    for subckt, occurrences in referenced_subckts.items():
        if subckt not in defined_subckts:
            missing.append((subckt, occurrences))
    
    return missing


def _detect_voltage_source_conflicts(netlist_text: str) -> list:
    """
    Detect multiple voltage sources connected to the same node pair.
    Returns list of (node_pair, [(line_num, source_name, value), ...]) tuples.
    """
    import re
    
    voltage_sources = {}
    lines = netlist_text.split('\n')
    
    for line_num, line in enumerate(lines, start=1):
        line = line.strip()
        if not line or line.startswith('*') or line.startswith('.'):
            continue
        
        tokens = line.split()
        if len(tokens) < 4:
            continue
        
        elem_name = tokens[0]
        if elem_name[0].upper() != 'V':
            continue
        
        node_plus = tokens[1]
        node_minus = tokens[2]
        
        # Normalize node names
        node_plus = re.sub(r'[^\w\-_]', '', node_plus)
        node_minus = re.sub(r'[^\w\-_]', '', node_minus)
        
        if node_plus.lower() in ['0', 'gnd', 'ground', 'vss']:
            node_plus = '0'
        if node_minus.lower() in ['0', 'gnd', 'ground', 'vss']:
            node_minus = '0'
        
        node_pair = tuple(sorted([node_plus, node_minus]))
        
        # Extract value
        value = "?"
        for i, tok in enumerate(tokens[3:], start=3):
            tok_upper = tok.upper()
            if tok_upper in ['DC', 'AC', 'PULSE', 'SIN', 'PWL']:
                if i+1 < len(tokens):
                    value = tokens[i+1]
                break
            elif not tok_upper.startswith('.'):
                value = tok
                break
        
        if node_pair not in voltage_sources:
            voltage_sources[node_pair] = []
        voltage_sources[node_pair].append((line_num, elem_name, value))
    
    # Find node pairs with multiple sources
    conflicts = []
    for node_pair, sources in voltage_sources.items():
        if len(sources) > 1:
            conflicts.append((node_pair, sources))
    
    return conflicts

def _netlist_ground_info(netlist_text: str):
    """
    Return (has_node0, has_gnd_label) based ONLY on actual node pins,
    not on .tran/.ac parameters or numeric values.
    """
    import re

    has_node0 = False
    has_gnd_label = False

    lines = netlist_text.split('\n')
    for line in lines:
        line = line.strip()
        # Skip comments, control lines, empty lines
        if not line or line.startswith('*') or line.startswith('.'):
            continue

        tokens = line.split()
        if len(tokens) < 3:
            continue

        elem_name = tokens[0]
        elem_type = elem_name[0].upper()
        nodes = []

        # Extract nodes based on element type
        if elem_type in ['R', 'C', 'L']:
            nodes = [tokens[1], tokens[2]]
        elif elem_type in ['V', 'I']:
            nodes = [tokens[1], tokens[2]]
        elif elem_type == 'D':
            nodes = [tokens[1], tokens[2]]
        elif elem_type == 'Q':
            if len(tokens) >= 4:
                nodes = [tokens[1], tokens[2], tokens[3]]
        elif elem_type == 'M':
            if len(tokens) >= 5:
                nodes = [tokens[1], tokens[2], tokens[3], tokens[4]]
        elif elem_type == 'S':
            if len(tokens) >= 5:
                nodes = [tokens[1], tokens[2], tokens[3], tokens[4]]
        elif elem_type == 'W':
            if len(tokens) >= 4:
                nodes = [tokens[1], tokens[2]]
        elif elem_type in ['E', 'G', 'H', 'F']:
            # Controlled sources: check if VALUE-based or linear
            if len(tokens) >= 3:
                # Check if VALUE keyword exists
                has_value = any(tok.upper() == 'VALUE' for tok in tokens)
                if has_value:
                    # Behavioral source: only 2 output nodes
                    nodes = [tokens[1], tokens[2]]
                elif len(tokens) >= 5:
                    # Linear source: 4 nodes (output pair + control pair)
                    nodes = [tokens[1], tokens[2], tokens[3], tokens[4]]
                else:
                    # Fallback: at least output pair
                    nodes = [tokens[1], tokens[2]]

        elif elem_type == 'X':
            if len(tokens) >= 3:
                nodes = tokens[1:-1]

        for node in nodes:
            node = re.sub(r'[=\(\)].*$', '', node)
            node = re.sub(r'[^\w\-_]', '', node)
            if not node:
                continue

            nl = node.lower()
            if nl == '0':
                has_node0 = True
            if nl in ['gnd', 'ground', 'vss']:
                has_gnd_label = True

    return has_node0, has_gnd_label

def _detect_floating_nodes(netlist_text: str) -> list:
    """Detect nodes that appear only once (floating/unconnected)."""
    import re
    
    floating_nodes = []
    node_counts = {}
    lines = netlist_text.split('\n')
    
    for line_num, line in enumerate(lines, start=1):
        line = line.strip()
        if not line or line.startswith('*') or line.startswith('.'):
            continue
        
        tokens = line.split()
        if len(tokens) < 3:
            continue
        
        elem_name = tokens[0]
        elem_type = elem_name[0].upper()
        nodes = []
        
        # Extract ONLY nodes (not model names, keywords, or source names)
        if elem_type in ['R', 'C', 'L']:
            nodes = [tokens[1], tokens[2]]
        
        elif elem_type in ['V', 'I']:
            nodes = [tokens[1], tokens[2]]
        
        elif elem_type == 'D':
            nodes = [tokens[1], tokens[2]]
        
        elif elem_type == 'Q':
            if len(tokens) >= 4:
                nodes = [tokens[1], tokens[2], tokens[3]]
        
        elif elem_type == 'M':
            if len(tokens) >= 5:
                nodes = [tokens[1], tokens[2], tokens[3], tokens[4]]
        
        elif elem_type == 'S':
            if len(tokens) >= 5:
                nodes = [tokens[1], tokens[2], tokens[3], tokens[4]]
        
        elif elem_type == 'W':
            # W<name> n+ n- Vcontrol model
            # Vcontrol is a voltage source NAME, not a node
            if len(tokens) >= 3:
                nodes = [tokens[1], tokens[2]]
        
        elif elem_type == 'T':
            # T<name> n1+ n1- n2+ n2- Z0=val TD=val
            # Transmission line: 4 nodes
            if len(tokens) >= 5:
                nodes = [tokens[1], tokens[2], tokens[3], tokens[4]]
        
        elif elem_type == 'B':
            # B<name> n+ n- <I or V> = {expr}
            # Behavioral source: 2 output nodes
            if len(tokens) >= 3:
                nodes = [tokens[1], tokens[2]]
        
        elif elem_type in ['E', 'G']:
            # Voltage-controlled sources
            if len(tokens) >= 3:
                # Check if VALUE keyword exists (behavioral)
                line_upper = line.upper()
                if 'VALUE' in line_upper or '=' in line:
                    # Behavioral: only 2 output nodes
                    nodes = [tokens[1], tokens[2]]
                elif len(tokens) >= 5:
                    # Linear: 4 nodes (out+, out-, ctrl+, ctrl-)
                    nodes = [tokens[1], tokens[2], tokens[3], tokens[4]]
                else:
                    nodes = [tokens[1], tokens[2]]
        
        elif elem_type == 'H':
            if len(tokens) >= 3:
                nodes = [tokens[1], tokens[2]]
        
        elif elem_type == 'F':
            if len(tokens) >= 3:
                nodes = [tokens[1], tokens[2]]
        
        elif elem_type == 'X':
            # X<name> node1 node2 ... subckt_name [params]
            if len(tokens) >= 3:
                candidate_nodes = tokens[1:-1]
                nodes = [tok for tok in candidate_nodes if '=' not in tok]
        
        for node in nodes:
            node = re.sub(r'[=\(\)].*$', '', node)
            node = re.sub(r'[^\w\-_]', '', node)
            
            if not node or node[0].isdigit():
                continue
            
            if node.upper() in ['VALUE', 'V', 'I', 'IF', 'THEN', 'ELSE']:
                continue
            
            # Normalize ground references
            node_lower = node.lower()
            if node_lower in ['0', 'gnd', 'ground', 'vss']:
                node = '0'
            
            if node not in node_counts:
                node_counts[node] = []
            node_counts[node].append((line_num, elem_name))
    
    # Find nodes appearing only once (exclude ground)
    for node, occurrences in node_counts.items():
        if len(occurrences) == 1 and node != '0':
            line_num, elem = occurrences[0]
            floating_nodes.append((node, line_num, elem))
    
    return floating_nodes

def _detect_missing_models(netlist_text: str) -> list:
    """
    Detect device models that are referenced but not defined.
    Returns list of (model_name, [(line_num, elem_name), ...]) tuples.
    """
    import re
    
    referenced_models = {}
    defined_models = set()
    lines = netlist_text.split('\n')
    
    for line_num, line in enumerate(lines, start=1):
        line = line.strip()
        if not line or line.startswith('*'):
            continue
        
        # Check for .model definitions
        if line.lower().startswith('.model'):
            tokens = line.split()
            if len(tokens) >= 2:
                defined_models.add(tokens[1].upper())
        
        # Check for .include statements (external model libraries)
        elif line.lower().startswith('.include') or line.lower().startswith('.lib'):
            return []
        
        # Extract model references from device lines
        elif line[0].upper() in ['D', 'Q', 'M', 'J']:
            tokens = line.split()
            elem_name = tokens[0]
            elem_type = elem_name[0].upper()
            
            if elem_type == 'D' and len(tokens) >= 4:
                model = tokens[3].upper()
                if model not in referenced_models:
                    referenced_models[model] = []
                referenced_models[model].append((line_num, elem_name))
            
            elif elem_type == 'Q' and len(tokens) >= 5:
                model = tokens[-1].upper()
                if not model[0].isdigit():
                    if model not in referenced_models:
                        referenced_models[model] = []
                    referenced_models[model].append((line_num, elem_name))
            
            elif elem_type == 'M' and len(tokens) >= 6:
                model = tokens[5].upper()
                if model not in referenced_models:
                    referenced_models[model] = []
                referenced_models[model].append((line_num, elem_name))
        
        # Check for switch models
        elif line[0].upper() in ['S', 'W']:
            tokens = line.split()
            if len(tokens) >= 5:
                elem_name = tokens[0]
                model = tokens[-1].upper()
                if model not in referenced_models:
                    referenced_models[model] = []
                referenced_models[model].append((line_num, elem_name))
    
    # Find models that are referenced but not defined
    missing = []
    for model, occurrences in referenced_models.items():
        if model not in defined_models:
            missing.append((model, occurrences))
    
    return missing


class ChatWorker(QThread):
    response_ready = pyqtSignal(str)

    def __init__(self, user_input, copilot):
        super().__init__()
        self.user_input = user_input
        self.copilot = copilot

    def run(self):
        response = self.copilot.handle_input(self.user_input)
        self.response_ready.emit(response)

class MicWorker(QThread):
    result_ready = pyqtSignal(str)
    error_occurred = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._stop_requested = False
        self._lock = threading.Lock()

    def request_stop(self):
        with self._lock:
            self._stop_requested = True

    def should_stop(self):
        with self._lock:
            return self._stop_requested

    def run(self):
        try:
            text = listen_to_mic(should_stop=self.should_stop, max_silence_sec=3)
            self.result_ready.emit(text)
        except Exception as e:
            self.error_occurred.emit(f"[Error: {e}]")

class ChatbotGUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.copilot = ESIMCopilotWrapper()
        self.current_image_path = None
        self.worker = None
        self._mic_worker = None
        self._is_listening = False

        # Project context
        self._project_dir = None
        self._generation_id = 0  # used to ignore stale responses

        self.initUI()
    
    def set_project_context(self, project_dir: str):
        """Called by Application to tell chatbot which project is active."""
        if project_dir and os.path.isdir(project_dir):
            self._project_dir = project_dir
            proj_name = os.path.basename(project_dir)
            self.append_message(
                "eSim",
                f"Project context set to: {proj_name}\nPath: {project_dir}",
                is_user=False,
            )
        else:
            self._project_dir = None
            self.append_message(
                "eSim",
                "Project context cleared or invalid.",
                is_user=False,
            )

    def analyze_current_netlist(self):
        """Analyze the active project's netlist."""

        if self.is_bot_busy():
            return
        
        if not self._project_dir:
            try:
                from configuration.Appconfig import Appconfig
                obj_appconfig = Appconfig()
                active_project = obj_appconfig.current_project.get("ProjectName")
                if active_project and os.path.isdir(active_project):
                    self._project_dir = active_project
                    proj_name = os.path.basename(active_project)
                    print(f"[COPILOT] Auto-detected active project: {active_project}")
                    self.append_message(
                        "eSim",
                        f"Auto-detected project: {proj_name}\nPath: {active_project}",
                        is_user=False,
                    )
            except Exception as e:
                print(f"[COPILOT] Could not auto-detect project: {e}")

        if not self._project_dir:
            QMessageBox.warning(
                self,
                "No project",
                "No active eSim project set for the chatbot.",
            )
            return

        proj_name = os.path.basename(self._project_dir)

        try:
            all_files = os.listdir(self._project_dir)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Cannot read project directory:\n{e}")
            return

        cir_candidates = [f for f in all_files if f.endswith('.cir') or f.endswith('.cir.out')]

        if not cir_candidates:
            QMessageBox.warning(
                self,
                "Netlist not found",
                f"Could not find any .cir or .cir.out files in:\n{self._project_dir}",
            )
            return

        netlist_path = None
        preferred_out = proj_name + ".cir.out"
        if preferred_out in cir_candidates:
            netlist_path = os.path.join(self._project_dir, preferred_out)
        else:
            preferred_cir = proj_name + ".cir"
            if preferred_cir in cir_candidates:
                netlist_path = os.path.join(self._project_dir, preferred_cir)
            else:
                if len(cir_candidates) > 1:
                    from PyQt5.QtWidgets import QInputDialog
                    item, ok = QInputDialog.getItem(
                        self,
                        "Select netlist file",
                        "Multiple .cir/.cir.out files found in this project.\n"
                        "Select the one you want to analyze:",
                        cir_candidates,
                        0,
                        False,
                    )
                    if ok and item:
                        netlist_path = os.path.join(self._project_dir, item)
                elif len(cir_candidates) == 1:
                    netlist_path = os.path.join(self._project_dir, cir_candidates[0])

        if not netlist_path or not os.path.exists(netlist_path):
            QMessageBox.warning(self, "Netlist not found", "Could not determine which netlist to use.")
            return

        netlist_name = os.path.basename(netlist_path)
        self.append_message(
            "eSim",
            f"Using netlist file:\n{netlist_name}",
            is_user=False,
        )

        try:
            with open(netlist_path, "r", encoding="utf-8", errors="ignore") as f:
                netlist_text = f.read()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to read netlist:\n{e}")
            return

        # === RUN ALL DETECTORS ===
        print(f"[COPILOT] Analyzing netlist: {netlist_path}")
        is_syntax_valid = _validate_netlist_with_ngspice(netlist_text)
        print(f"[COPILOT] Ngspice syntax check: {'PASS' if is_syntax_valid else 'FAIL'}")

        floating_nodes = _detect_floating_nodes(netlist_text)
        if floating_nodes:
            print(f"[COPILOT] Found {len(floating_nodes)} floating node(s):")
            for node, line_num, elem in floating_nodes:
                print(f"  - Node '{node}' at line {line_num} ({elem})")

        missing_models = _detect_missing_models(netlist_text)
        if missing_models:
            print(f"[COPILOT] Found {len(missing_models)} missing model(s):")
            for model, occurrences in missing_models:
                print(f"  - Model '{model}' used {len(occurrences)} time(s) but not defined")

        missing_subckts = _detect_missing_subcircuits(netlist_text)
        if missing_subckts:
            print(f"[COPILOT] Found {len(missing_subckts)} missing subcircuit(s):")
            for subckt, occurrences in missing_subckts:
                print(f"  - Subcircuit '{subckt}' used {len(occurrences)} time(s) but not defined")

        voltage_conflicts = _detect_voltage_source_conflicts(netlist_text)
        if voltage_conflicts:
            print(f"[COPILOT] Found {len(voltage_conflicts)} voltage source conflict(s):")
            for node_pair, sources in voltage_conflicts:
                print(f"  - Nodes {node_pair}: {len(sources)} sources")
                for line_num, name, val in sources:
                    print(f"    * {name} (line {line_num}, value={val})")

        import re
        text_lower = netlist_text.lower()

        has_tran = ".tran" in text_lower
        has_ac = ".ac" in text_lower
        has_op = ".op" in text_lower

        has_node0, has_gnd_label = _netlist_ground_info(netlist_text)

        if not has_node0 and not has_gnd_label:
            print("[COPILOT] WARNING: No ground reference (node 0 or GND) found!")

        # Build descriptions
        if floating_nodes:
            floating_desc = "; ".join([f"{node} (line {line_num}, {elem})"
                                        for node, line_num, elem in floating_nodes])
        else:
            floating_desc = "NONE"

        if missing_models:
            missing_desc = "; ".join([f"{model} (used {len(occs)} times)"
                                        for model, occs in missing_models])
        else:
            missing_desc = "NONE"

        if missing_subckts:
            subckt_desc = "; ".join([f"{subckt} (used {len(occs)} times)"
                                    for subckt, occs in missing_subckts])
        else:
            subckt_desc = "NONE"

        if voltage_conflicts:
            conflict_parts = []
            for node_pair, sources in voltage_conflicts:
                src_desc = ", ".join([f"{name}={val}" for _, name, val in sources])
                conflict_parts.append(f"{node_pair}: {src_desc}")
            voltage_conflict_desc = "; ".join(conflict_parts)
        else:
            voltage_conflict_desc = "NONE"

        facts = [
            f"NET_SYNTAX_VALID={'YES' if is_syntax_valid else 'NO'}",
            f"NET_HAS_NODE_0={'YES' if has_node0 else 'NO'}",
            f"NET_HAS_GND_LABEL={'YES' if has_gnd_label else 'NO'}",
            f"NET_HAS_TRAN={'YES' if has_tran else 'NO'}",
            f"NET_HAS_AC={'YES' if has_ac else 'NO'}",
            f"NET_HAS_OP={'YES' if has_op else 'NO'}",
            f"FLOATING_NODES={floating_desc}",
            f"MISSING_MODELS={missing_desc}",
            f"MISSING_SUBCKTS={subckt_desc}",
            f"VOLTAGE_CONFLICTS={voltage_conflict_desc}",
        ]

        facts_block = "\n".join(f"[FACT {f}]" for f in facts)
        print(f"[COPILOT] FACTS being sent:\n{facts_block}")

        # === BUILD PROMPT (SIMPLIFIED USING CONTRACT FILE) ===

        full_query = (
            f"{NETLIST_CONTRACT}\n\n"
            "=== NETLIST FACTS (MACHINE-GENERATED) ===\n"
            "The following lines describe the analyzed netlist in a structured way.\n"
            "Each line has the form [FACT KEY=VALUE].\n"
            "You MUST rely ONLY on these FACTS, not on the raw netlist.\n\n"
            f"{facts_block}\n\n"
            "=== RAW NETLIST (FOR REFERENCE ONLY, DO NOT RE-ANALYZE TO FIND NEW ERRORS) ===\n"
            "[ESIM_NETLIST_START]\n"
            f"{netlist_text}\n"
            "[ESIM_NETLIST_END]\n\n"
            "REMINDERS:\n"
            "- Do NOT invent issues that are not present in the FACT lines.\n"
            "- If a FACT says NONE, you MUST NOT report any issue for that category.\n"
            "- Follow the output format and rules described in the contract above.\n"
        )


        # Show synthetic user message
        self.append_message(
            "You",
            f"Analyze current netlist of project '{proj_name}' for design mistakes, "
            "missing connections, or bad values.",
            is_user=True,
        )

        # Disable UI and run worker
        self.input_field.setDisabled(True)
        self.send_btn.setDisabled(True)
        if hasattr(self, "attach_btn"):
            self.attach_btn.setDisabled(True)
        if hasattr(self, "mic_btn"):
            self.mic_btn.setDisabled(True)
        if hasattr(self, "analyze_netlist_btn"):
            self.analyze_netlist_btn.setDisabled(True)
        if hasattr(self, "clear_btn"):
            self.clear_btn.setDisabled(True)
        self.loading_label.show()

        self._generation_id += 1
        current_gen = self._generation_id

        self.worker = ChatWorker(full_query, self.copilot)
        self.worker.response_ready.connect(
            lambda resp, gen=current_gen: self._handle_response_with_id(resp, gen)
        )
        self.worker.finished.connect(self.on_worker_finished)
        self.worker.start()


    def analyze_specific_netlist(self, netlist_path: str):
        """Analyze a specific netlist file (called from ProjectExplorer context menu)."""

        if self.is_bot_busy():
            return

        if not os.path.exists(netlist_path):
            QMessageBox.warning(
                self,
                "File not found",
                f"Netlist file does not exist:\n{netlist_path}",
            )
            return

        netlist_name = os.path.basename(netlist_path)
        self.append_message(
            "eSim",
            f"Analyzing specific netlist:\n{netlist_name}",
            is_user=False,
        )

        try:
            with open(netlist_path, "r", encoding="utf-8", errors="ignore") as f:
                netlist_text = f.read()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to read netlist:\n{e}")
            return

        # === RUN ALL DETECTORS (IDENTICAL TO analyze_current_netlist) ===
        print(f"[COPILOT] Analyzing netlist: {netlist_path}")
        is_syntax_valid = _validate_netlist_with_ngspice(netlist_text)
        print(f"[COPILOT] Ngspice syntax check: {'PASS' if is_syntax_valid else 'FAIL'}")

        floating_nodes = _detect_floating_nodes(netlist_text)
        if floating_nodes:
            print(f"[COPILOT] Found {len(floating_nodes)} floating node(s):")
            for node, line_num, elem in floating_nodes:
                print(f"  - Node '{node}' at line {line_num} ({elem})")

        missing_models = _detect_missing_models(netlist_text)
        if missing_models:
            print(f"[COPILOT] Found {len(missing_models)} missing model(s):")
            for model, occurrences in missing_models:
                print(f"  - Model '{model}' used {len(occurrences)} time(s) but not defined")

        missing_subckts = _detect_missing_subcircuits(netlist_text)
        if missing_subckts:
            print(f"[COPILOT] Found {len(missing_subckts)} missing subcircuit(s):")
            for subckt, occurrences in missing_subckts:
                print(f"  - Subcircuit '{subckt}' used {len(occurrences)} time(s) but not defined")

        voltage_conflicts = _detect_voltage_source_conflicts(netlist_text)
        if voltage_conflicts:
            print(f"[COPILOT] Found {len(voltage_conflicts)} voltage source conflict(s):")
            for node_pair, sources in voltage_conflicts:
                print(f"  - Nodes {node_pair}: {len(sources)} sources")
                for line_num, name, val in sources:
                    print(f"    * {name} (line {line_num}, value={val})")

        import re
        text_lower = netlist_text.lower()

        has_tran = ".tran" in text_lower
        has_ac = ".ac" in text_lower
        has_op = ".op" in text_lower

        has_node0, has_gnd_label = _netlist_ground_info(netlist_text)

        if not has_node0 and not has_gnd_label:
            print("[COPILOT] WARNING: No ground reference (node 0 or GND) found!")

        # Build descriptions (IDENTICAL TO analyze_current_netlist)
        if floating_nodes:
            floating_desc = "; ".join([f"{node} (line {line_num}, {elem})"
                                    for node, line_num, elem in floating_nodes])
        else:
            floating_desc = "NONE"

        if missing_models:
            missing_desc = "; ".join([f"{model} (used {len(occs)} times)"
                                    for model, occs in missing_models])
        else:
            missing_desc = "NONE"

        if missing_subckts:
            subckt_desc = "; ".join([f"{subckt} (used {len(occs)} times)"
                                    for subckt, occs in missing_subckts])
        else:
            subckt_desc = "NONE"

        if voltage_conflicts:
            conflict_parts = []
            for node_pair, sources in voltage_conflicts:
                src_desc = ", ".join([f"{name}={val}" for _, name, val in sources])
                conflict_parts.append(f"{node_pair}: {src_desc}")
            voltage_conflict_desc = "; ".join(conflict_parts)
        else:
            voltage_conflict_desc = "NONE"

        facts = [
            f"NET_SYNTAX_VALID={'YES' if is_syntax_valid else 'NO'}",
            f"NET_HAS_NODE_0={'YES' if has_node0 else 'NO'}",
            f"NET_HAS_GND_LABEL={'YES' if has_gnd_label else 'NO'}",
            f"NET_HAS_TRAN={'YES' if has_tran else 'NO'}",
            f"NET_HAS_AC={'YES' if has_ac else 'NO'}",
            f"NET_HAS_OP={'YES' if has_op else 'NO'}",
            f"FLOATING_NODES={floating_desc}",
            f"MISSING_MODELS={missing_desc}",
            f"MISSING_SUBCKTS={subckt_desc}",
            f"VOLTAGE_CONFLICTS={voltage_conflict_desc}",
        ]

        facts_block = "\n".join(f"[FACT {f}]" for f in facts)
        print(f"[COPILOT] FACTS being sent:\n{facts_block}")

        # === BUILD PROMPT (IDENTICAL TO analyze_current_netlist) ===
        # === BUILD PROMPT (SIMPLIFIED USING CONTRACT FILE) ===

        full_query = (
            f"{NETLIST_CONTRACT}\n\n"
            "=== NETLIST FACTS (MACHINE-GENERATED) ===\n"
            "The following lines describe the analyzed netlist in a structured way.\n"
            "Each line has the form [FACT KEY=VALUE].\n"
            "You MUST rely ONLY on these FACTS, not on the raw netlist.\n\n"
            f"{facts_block}\n\n"
            "=== RAW NETLIST (FOR REFERENCE ONLY, DO NOT RE-ANALYZE TO FIND NEW ERRORS) ===\n"
            "[ESIM_NETLIST_START]\n"
            f"{netlist_text}\n"
            "[ESIM_NETLIST_END]\n\n"
            "REMINDERS:\n"
            "- Do NOT invent issues that are not present in the FACT lines.\n"
            "- If a FACT says NONE, you MUST NOT report any issue for that category.\n"
            "- Follow the output format and rules described in the contract above.\n"
        )

        # Show synthetic user message
        self.append_message(
            "You",
            f"Analyze netlist '{netlist_name}' for design mistakes, "
            "missing connections, or bad values.",
            is_user=True,
        )

        # Disable UI and run worker
        self.input_field.setDisabled(True)
        self.send_btn.setDisabled(True)
        if hasattr(self, "attach_btn"):
            self.attach_btn.setDisabled(True)
        if hasattr(self, "mic_btn"):
            self.mic_btn.setDisabled(True)
        if hasattr(self, "analyze_netlist_btn"):
            self.analyze_netlist_btn.setDisabled(True)
        if hasattr(self, "clear_btn"):
            self.clear_btn.setDisabled(True)
        self.loading_label.show()

        self._generation_id += 1
        current_gen = self._generation_id

        self.worker = ChatWorker(full_query, self.copilot)
        self.worker.response_ready.connect(
            lambda resp, gen=current_gen: self._handle_response_with_id(resp, gen)
        )
        self.worker.finished.connect(self.on_worker_finished)
        self.worker.start()


    def stop_analysis(self):
        """Stop chat worker and mic worker safely."""
        try:
            # Stop mic
            if getattr(self, "_mic_worker", None) and self._mic_worker.isRunning():
                self._mic_worker.request_stop()
                self._mic_worker.quit()
                self._mic_worker.wait(200)
                if self._mic_worker.isRunning():
                    self._mic_worker.terminate()
            self._reset_mic_ui()

            # Stop chat worker
            if self.worker and self.worker.isRunning():
                self.worker.quit()
                self.worker.wait(500)
                if self.worker.isRunning():
                    self.worker.terminate()
        except Exception as e:
            print(f"Stop analysis error: {e}")

    def start_listening(self):
        # If already listening -> stop
        if self._mic_worker and self._mic_worker.isRunning():
            self._mic_worker.request_stop()
            return

        # Start listening (do NOT disable mic button)
        self.mic_btn.setStyleSheet("""
            QPushButton { background-color: #e74c3c; color: white; border-radius: 20px; font-size: 18px; }
        """)
        self.mic_btn.setEnabled(True)
        self.input_field.setPlaceholderText("Listening... (click mic to stop)")
        QApplication.processEvents()

        self._mic_worker = MicWorker()
        self._mic_worker.result_ready.connect(self._on_mic_result)
        self._mic_worker.error_occurred.connect(self._on_mic_error)
        self._mic_worker.finished.connect(self._reset_mic_ui)
        self._mic_worker.start()

    def _on_mic_result(self, text):
        self._reset_mic_ui()
        if text and text.strip():
            self.input_field.setText(text.strip())
            self.input_field.setFocus()

    def _on_mic_error(self, error_msg):
        """Handle speech recognition errors."""
        # Only show popup for REAL errors, not timeouts
        if "[Error:" in error_msg and "No speech" not in error_msg:
            QMessageBox.warning(self, "Microphone Error", error_msg)

    def _reset_mic_ui(self):
        self.mic_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                border: 1px solid #bdc3c7;
                border-radius: 20px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #ffebee;
                border-color: #e74c3c;
            }
        """)
        self.mic_btn.setEnabled(True)
        self.input_field.setPlaceholderText("Ask eSim Copilot...")
        
    def initUI(self):
        """Initialize the Chatbot GUI Layout."""

        # Main Layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)

        # --- HEADER AREA (Title + Netlist + Clear Button) ---
        header_layout = QHBoxLayout()

        title_label = QLabel("eSim Copilot")
        title_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #34495e;")
        header_layout.addWidget(title_label)

        header_layout.addStretch()  # Push buttons to the right

        # NEW: Analyze Netlist button
        self.analyze_netlist_btn = QPushButton("Netlist ▶")
        self.analyze_netlist_btn.setFixedHeight(30)
        self.analyze_netlist_btn.setToolTip("Analyze active project's netlist")
        self.analyze_netlist_btn.setCursor(Qt.PointingHandCursor)
        self.analyze_netlist_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border-radius: 15px;
                padding: 0 10px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        # This method should be defined in ChatbotGUI
        # def analyze_current_netlist(self): ...
        self.analyze_netlist_btn.clicked.connect(self.analyze_current_netlist)
        header_layout.addWidget(self.analyze_netlist_btn)

        # Clear button
        self.clear_btn = QPushButton("🗑️")
        self.clear_btn.setFixedSize(30, 30)
        self.clear_btn.setToolTip("Clear Chat History")
        self.clear_btn.setCursor(Qt.PointingHandCursor)
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 1px solid #ddd;
                border-radius: 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #ffebee;
                border-color: #ef9a9a;
            }
        """)
        self.clear_btn.clicked.connect(self.clear_chat)
        header_layout.addWidget(self.clear_btn)

        self.layout.addLayout(header_layout)

        # --- CHAT DISPLAY AREA ---
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setFont(QFont("Segoe UI", 10))
        self.chat_display.setStyleSheet("""
            QTextEdit {
                background-color: #f5f6fa;
                border: 1px solid #dcdcdc;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        self.layout.addWidget(self.chat_display)

        # PROGRESS INDICATOR (Hidden by default)
        self.loading_label = QLabel("⏳ eSim Copilot is thinking...")
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.setStyleSheet("""
            background-color: #fff3cd; 
            color: #856404; 
            border: 1px solid #ffeeba;
            border-radius: 5px;
            padding: 5px;
            font-weight: bold;
        """)
        self.loading_label.hide()
        self.layout.addWidget(self.loading_label)

        # --- INPUT AREA CONTAINER ---
        input_layout = QHBoxLayout()
        input_layout.setSpacing(8)

        # A. ATTACH BUTTON
        self.attach_btn = QPushButton("📎")
        self.attach_btn.setFixedSize(40, 40)
        self.attach_btn.setToolTip("Attach Circuit Image")
        self.attach_btn.setCursor(Qt.PointingHandCursor)
        self.attach_btn.setStyleSheet("""
            QPushButton {
                border: 1px solid #bdc3c7;
                border-radius: 20px;
                background-color: #ffffff;
                color: #555;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #ecf0f1;
                border-color: #95a5a6;
            }
        """)
        self.attach_btn.clicked.connect(self.browse_image)
        input_layout.addWidget(self.attach_btn)

        # B. TEXT INPUT FIELD
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Ask eSim Copilot...")
        self.input_field.setFixedHeight(40)
        self.input_field.setStyleSheet("""
            QLineEdit {
                border: 1px solid #bdc3c7;
                border-radius: 20px;
                padding-left: 15px;
                padding-right: 15px;
                background-color: #ffffff;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
        """)
        self.input_field.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.input_field)

        # --- MIC BUTTON ---
        self.mic_btn = QPushButton("🎤")
        self.mic_btn.setFixedSize(40, 40)
        self.mic_btn.setToolTip("Speak to type")
        self.mic_btn.setCursor(Qt.PointingHandCursor)
        self.mic_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                border: 1px solid #bdc3c7;
                border-radius: 20px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #ffebee; /* Light red hover */
                border-color: #e74c3c;
            }
        """)
        self.mic_btn.clicked.connect(self.start_listening)
        input_layout.addWidget(self.mic_btn)

        # C. SEND BUTTON
        self.send_btn = QPushButton("➤")
        self.send_btn.setFixedSize(40, 40)
        self.send_btn.setToolTip("Send Message")
        self.send_btn.setCursor(Qt.PointingHandCursor)
        self.send_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 16px;
                padding-bottom: 2px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1abc9c;
            }
        """)
        self.send_btn.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_btn)

        self.layout.addLayout(input_layout)

        # --- IMAGE STATUS ROW (label + remove button) ---
        status_layout = QHBoxLayout()
        status_layout.setSpacing(5)
        status_layout.setContentsMargins(0, 0, 0, 0)

        self.filename_status = QLabel("No image attached")
        self.filename_status.setStyleSheet("color: gray; font-size: 12px;")
        self.filename_status.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        status_layout.addWidget(self.filename_status)

        self.remove_btn = QPushButton("×")
        self.remove_btn.setFixedSize(25, 25)
        self.remove_btn.setStyleSheet("""
            QPushButton {
                background: #ff6b6b;
                color: white;
                border: none;
                border-radius: 12px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover { background: #ff5252; }
        """)
        self.remove_btn.clicked.connect(self.remove_image)
        self.remove_btn.hide()  # hidden by default
        status_layout.addWidget(self.remove_btn)

        status_widget = QWidget()
        status_widget.setLayout(status_layout)
        self.layout.addWidget(status_widget)

        self.setLayout(self.layout)

        # Initial message
        self.append_message(
            "eSim Copilot",
            "Hello! I am ready to help you analyze circuits.",
            is_user=False,
        )

    # ---------- IMAGE HANDLING ----------

    def browse_image(self):
        """Open file dialog to select image (Updates Status Label ONLY)."""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Circuit Image",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.tiff *.gif);;All Files (*)",
            options=options
        )

        if file_path:
            self.current_image_path = file_path  # Store path internally
            short_name = os.path.basename(file_path)

            # Update Status Row (Visual Feedback)
            self.filename_status.setText(f"📎 {short_name} attached")
            self.filename_status.setStyleSheet("color: green; font-weight: bold; font-size: 12px;")
            self.remove_btn.show()

            # Focus input so user can start typing question immediately
            self.input_field.setFocus()

    def is_bot_busy(self):
        """Check if a background worker is currently running."""
        if hasattr(self, "worker") and self.worker is not None:
            if self.worker.isRunning():
                QMessageBox.warning(self, "Busy", "Chatbot is currently busy processing a request.\nPlease wait.")
                return True
        return False


    def remove_image(self):
        """Clear selected image (status + input tag)."""
        self.current_image_path = None
        self.filename_status.setText("No image attached")
        self.filename_status.setStyleSheet("color: gray; font-size: 12px;")
        self.remove_btn.hide()
        
    # ---------- CHAT / HISTORY ----------

    def clear_chat(self):
        """Stop analysis, clear chat, and optionally export history."""
        # 1) Stop any ongoing analysis first
        self.stop_analysis()
        self._generation_id += 1

        # 2) Ask user about exporting history
        reply = QMessageBox.question(
            self,
            "Clear History",
            "Clear chat history?\nPress 'Yes' to export to a file first, 'No' to clear without saving.",
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
        )
        if reply == QMessageBox.Cancel:
            return
        if reply == QMessageBox.Yes:
            self.export_history()

        # 3) Clear UI
        self.chat_display.clear()

        # 4) Clear backend memory/context
        try:
            clear_history()
        except Exception:
            pass

        # 5) Reset welcome line
        self.append_message("eSim Copilot", "Chat cleared. Ready for new queries.", is_user=False)


    def export_history(self):
        """Export chat to text file."""
        text = self.chat_display.toPlainText()
        if not text.strip():
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Chat History",
            "chat_history.txt",
            "Text Files (*.txt)"
        )
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(text)
            QMessageBox.information(self, "Exported", f"History saved to:\n{file_path}")

    def send_message(self):
        user_text = self.input_field.text().strip()

        # Don't send if empty and no image
        if not user_text and not self.current_image_path:
            return

        full_query = user_text
        display_text = user_text

        if self.current_image_path:
            short_name = os.path.basename(self.current_image_path)

            # 1) BACKEND QUERY (hidden tag with FULL PATH)
            full_query = f"[Image: {self.current_image_path}] {user_text}".strip()

            # 2) USER-VISIBLE TEXT (show filename here, not in input box)
            question_part = user_text if user_text else ""
            if question_part:
                display_text = f"📎 {short_name}\n\n{question_part}"
            else:
                display_text = f"📎 {short_name}"

            # Reset image state & status row
            self.current_image_path = None
            self.filename_status.setText("No image attached")
            self.filename_status.setStyleSheet("color: gray; font-size: 12px;")
            self.remove_btn.hide()
        else:
            full_query = user_text
            display_text = user_text

        # Show user bubble with image name (if any)
        self.append_message("You", display_text, is_user=True)
        self.input_field.clear()

        # Disable while waiting
        self.input_field.setDisabled(True)
        self.send_btn.setDisabled(True)
        if hasattr(self, "attach_btn"):
            self.attach_btn.setDisabled(True)
        if hasattr(self, 'mic_btn'):
            self.mic_btn.setDisabled(True)

        # NEW: also disable Netlist and Clear during any answer
        if hasattr(self, "analyze_netlist_btn"):
            self.analyze_netlist_btn.setDisabled(True)
        if hasattr(self, "clear_btn"):
            self.clear_btn.setDisabled(True)

        self.loading_label.show()

        # NEW: bump generation id and use it to filter responses
        self._generation_id += 1
        current_gen = self._generation_id

        self.worker = ChatWorker(full_query, self.copilot)
        self.worker.response_ready.connect(
            lambda resp, gen=current_gen: self._handle_response_with_id(resp, gen)
        )
        self.worker.finished.connect(self.on_worker_finished)
        self.worker.start()


    def on_worker_finished(self):
        """Re-enable UI after worker completes."""
        self.input_field.setEnabled(True)
        self.send_btn.setEnabled(True)
        if hasattr(self, 'attach_btn'):
            self.attach_btn.setEnabled(True)
        if hasattr(self, 'mic_btn'):
            self.mic_btn.setEnabled(True)

        # NEW: re-enable Netlist and Clear
        if hasattr(self, "analyze_netlist_btn"):
            self.analyze_netlist_btn.setEnabled(True)
        if hasattr(self, "clear_btn"):
            self.clear_btn.setEnabled(True)

        self.loading_label.hide()
        self.input_field.setFocus()

    def _handle_response_with_id(self, response: str, gen_id: int):
        """Only accept responses from the current generation."""
        if gen_id != self._generation_id:
            # Stale response from a cancelled/cleared analysis -> ignore
            return
        self.append_message("eSim Copilot", response, is_user=False)

    def handle_response(self, response):
        # Kept for backward compatibility if used elsewhere,
        # but route everything through _handle_response_with_id with current id.
        self._handle_response_with_id(response, self._generation_id)


    @staticmethod 
    def format_text_to_html(text):
        """Helper to convert basic Markdown to HTML for the Qt TextEdit."""
        import html
        # 1. Escape existing HTML to prevent injection
        text = html.escape(text)
        
        # 2. Convert **bold** to <b>bold</b>
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
        
        # 3. Convert headers ### to <h3>
        text = re.sub(r'###\s*(.*)', r'<h3>\1</h3>', text)
        
        # 4. Convert newlines to <br> for HTML rendering
        text = text.replace('\n', '<br>')
        return text

    def append_message(self, sender, text, is_user):
        """Append message INSTANTLY (Text Only, No Image Rendering)."""
        if not text:
            return

        # 1. Define Headers
        if is_user:
            header = "<b style='color: #4cd137;'>You</b>"
        else:
            header = "<b style='color: #2f3640;'>eSim Copilot</b>"

        cursor = self.chat_display.textCursor()
        cursor.movePosition(QTextCursor.End)
        
        # 2. Insert Header
        cursor.insertHtml(f"<br>{header}<br>")

        # 3. Format Text (Bold, Newlines) but NO Image generation
        # Use the helper function if you added it inside the class
        formatted_text = self.format_text_to_html(text)
        
        # 4. Insert Text Instantly
        cursor.insertHtml(formatted_text)
        
        self.chat_display.setTextCursor(cursor)
        self.chat_display.ensureCursorVisible()

    # ---------- CLEAN SHUTDOWN ----------

    def closeEvent(self, event):
        """Stop analysis when the chatbot window/dock is closed."""
        # Ensure worker is stopped so it doesn't keep using CPU
        self.stop_analysis()

        # Clear backend context as well
        try:
            clear_history()
        except Exception:
            pass

        event.accept()

    def debug_error(self, error_log_path: str):
        """
        Called by Application when a simulation error happens.
        Reads ngspice_error.log and asks the copilot to explain + fix it in eSim.
        """
        if not error_log_path or not os.path.exists(error_log_path):
            QMessageBox.warning(
                self,
                "Error log missing",
                f"Could not find error log at:\n{error_log_path}",
            )
            return

        try:
            with open(error_log_path, "r", encoding="utf-8", errors="ignore") as f:
                log_text = f.read()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to read error log:\n{e}")
            return

        # Show trimmed log in the chat for user visibility
        tail_lines = "\n".join(log_text.splitlines()[-40:])  # last 40 lines
        display = (
            "Automatic ngspice error captured from eSim:\n\n"
            "```"
            f"{tail_lines}\n"
            "```"
        )
        self.append_message("eSim", display, is_user=False)

        # Build a focused query for the backend
        full_query = (
            "The following is an ngspice error log from an eSim simulation.\n"
            "1) Explain the exact root cause in simple terms.\n"
            "2) Give concrete, step‑by‑step instructions to fix it INSIDE eSim "
            "(KiCad schematic / sources / analysis settings).\n\n"
            "[NGSPICE_ERROR_LOG_START]\n"
            f"{log_text}\n"
            "[NGSPICE_ERROR_LOG_END]"
        )

        # Disable UI while analysis is running
        self.input_field.setDisabled(True)
        self.send_btn.setDisabled(True)
        if hasattr(self, "attach_btn"):
            self.attach_btn.setDisabled(True)
        if hasattr(self, "mic_btn"):
            self.mic_btn.setDisabled(True)
        if hasattr(self, "analyze_netlist_btn"):
            self.analyze_netlist_btn.setDisabled(True)
        if hasattr(self, "clear_btn"):
            self.clear_btn.setDisabled(True)

        self.loading_label.show()

        # NEW: bump generation and bind response with this gen
        self._generation_id += 1
        current_gen = self._generation_id

        self.worker = ChatWorker(full_query, self.copilot)
        self.worker.response_ready.connect(
            lambda resp, gen=current_gen: self._handle_response_with_id(resp, gen)
        )
        self.worker.finished.connect(self.on_worker_finished)
        self.worker.start()

from PyQt5.QtWidgets import QDockWidget
from PyQt5.QtCore import Qt

def createchatbotdock(parent=None):
    """
    Factory function for DockArea / Application integration.
    Returns a QDockWidget containing a ChatbotGUI instance.
    """
    dock = QDockWidget("eSim Copilot", parent)
    dock.setAllowedAreas(Qt.RightDockWidgetArea | Qt.LeftDockWidgetArea)

    chatbot_widget = ChatbotGUI(parent)
    dock.setWidget(chatbot_widget)
    return dock


# Standalone test
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ChatbotGUI()
    w.resize(500, 600)
    w.show()
    sys.exit(app.exec_())

def create_chatbot_dock(parent=None):
    """Factory function for DockArea integration."""
    from PyQt5.QtWidgets import QDockWidget
    from PyQt5.QtCore import Qt
    
    dock = QDockWidget("eSim Copilot", parent)
    dock.setAllowedAreas(Qt.RightDockWidgetArea | Qt.LeftDockWidgetArea)
    
    chatbot_widget = ChatbotGUI(parent)
    dock.setWidget(chatbot_widget)
    
    return dock
