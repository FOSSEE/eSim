"""Deterministic pattern matching for common NgSpice simulation errors.

This module matches known error patterns in NgSpice log output and provides
structured diagnoses + fix suggestions. Results are included in the LLM
prompt so even weak local models can give accurate advice.
"""

import re
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Any


@dataclass
class ErrorMatch:
    error_id: str
    category: str
    causal_priority: int      # 1 = root cause, 2 = intermediate, 3 = consequence
    diagnosis: str
    matched_text: str
    extracted_facts: Dict[str, str] = field(default_factory=dict)


# ── Entity extraction helpers ────────────────────────────────────────────────

_NODE_PATTERN = re.compile(
    r"(?:node|net)\s+['\"]?([^'\"\s]+)['\"]?", re.IGNORECASE
)

# Matches: "can't find model 'NAME'" — captures NAME in group 1.
_CANT_FIND_MODEL_RE = re.compile(
    r"can'?t\s+find\s+model\s+['\"]?(\S+?)['\"]?(?:\s|$)", re.IGNORECASE
)

# Matches the component line that follows a model warning, e.g.:
#     d1 in2 net-_c1-pad1_ esim_diode
_COMPONENT_LINE_RE = re.compile(
    r"^\s+([a-zA-Z]\S*)\s+", re.MULTILINE
)

# Matches: "unknown subckt: x1 net-*c1-pad1* 0 out lm7805"
# group 1 = component name (e.g. x1), rest of tokens → last token = subckt name
_UNKNOWN_SUBCKT_RE = re.compile(
    r"unknown\s+subckt:\s+(\S+)\s+(.*)", re.IGNORECASE
)

# Matches: "subcircuit 'NAME' not found"
_SUBCKT_NOT_FOUND_RE = re.compile(
    r"subcircuit\s+['\"]?(\S+)['\"]?\s+not\s+found", re.IGNORECASE
)

# Matches: "Unknown model type XYZ - ignored"
_UNKNOWN_MODEL_TYPE_RE = re.compile(
    r"Unknown\s+model\s+type\s+(\S+)", re.IGNORECASE
)

# Matches voltage/current source names in log text (e.g. v1, vloop1, i2)
_VSOURCE_RE = re.compile(r"\b([vViI]\w+)\b")

# Matches: "unknown parameter 'foo'" or "no such parameter 'bar'"
_PARAM_NAME_RE = re.compile(
    r"(?:unknown\s+parameter|no\s+such\s+parameter)\s+['\"]?(\S+?)['\"]?(?:\s|$)",
    re.IGNORECASE,
)


def _extract_missing_model_facts(log_text: str, match_str: str) -> Dict[str, str]:
    """Extract model name and component from a Missing Model match.

    Component is set to 'Unknown' unless explicitly available in the
    immediate context (the indented line that follows the warning).
    """
    facts: Dict[str, str] = {}

    # Search in a window around the match in the full log text
    pos = log_text.find(match_str)
    if pos >= 0:
        # Get the full line containing the match + some context after
        line_start = log_text.rfind("\n", 0, pos) + 1
        context_window = log_text[line_start:pos + len(match_str) + 300]
    else:
        context_window = match_str

    # Try to get model name from "can't find model 'NAME'"
    m = _CANT_FIND_MODEL_RE.search(context_window)
    if m:
        facts["Model"] = m.group(1)
    else:
        # Fallback: "model NAME not found" style
        m2 = re.search(
            r"(?:model|device)\s+['\"]?(\S+)['\"]?", context_window, re.IGNORECASE
        )
        if m2:
            facts["Model"] = m2.group(1)

    # Try to find the component on the indented line *following* the warning.
    # NgSpice format:  "warning, can't find model ...\n    d1 in2 ..."
    if pos >= 0:
        after = log_text[pos + len(match_str):pos + len(match_str) + 200]
        comp_m = _COMPONENT_LINE_RE.match(after)
        if comp_m:
            # Only accept component if it's different from the model name
            comp_name = comp_m.group(1)
            if comp_name != facts.get("Model"):
                facts["Component"] = comp_name

    if "Component" not in facts:
        facts["Component"] = "Unknown"

    return facts


def _extract_subckt_facts_v2(log_text: str, match_str: str) -> Dict[str, str]:
    """Extract subcircuit and component names from an ERR002 match.

    Handles two NgSpice formats:
      1. "unknown subckt: x1 net-*c1* 0 out lm7805"
      2. "subcircuit 'NAME' not found"
    """
    facts: Dict[str, str] = {}

    # Search the full line in log_text for richer context
    pos = log_text.find(match_str)
    if pos >= 0:
        line_start = log_text.rfind("\n", 0, pos) + 1
        line_end = log_text.find("\n", pos)
        if line_end == -1:
            line_end = len(log_text)
        full_line = log_text[line_start:line_end]
    else:
        full_line = match_str

    # Format 1: "unknown subckt: <comp> <nodes...> <subckt_name>"
    m = _UNKNOWN_SUBCKT_RE.search(full_line)
    if m:
        facts["Component"] = m.group(1)
        # The subcircuit name is always the last token in the rest
        tokens = m.group(2).strip().split()
        if tokens:
            facts["Subcircuit"] = tokens[-1]
        return facts

    # Format 2: "subcircuit 'NAME' not found"
    m2 = _SUBCKT_NOT_FOUND_RE.search(full_line)
    if m2:
        facts["Subcircuit"] = m2.group(1)
        facts["Component"] = "Unknown"
        return facts

    return facts


def _extract_invalid_model_facts(log_text: str, match_str: str) -> Dict[str, str]:
    """Extract the invalid model type from an ERR006 match."""
    facts: Dict[str, str] = {}
    m = _UNKNOWN_MODEL_TYPE_RE.search(match_str)
    if m:
        facts["Invalid Type"] = m.group(1)
    return facts


def _extract_node_facts(log_text: str, match_str: str, match_pos: int) -> Dict[str, str]:
    """Extract the node name from a No DC Path match."""
    facts: Dict[str, str] = {}
    context = log_text[max(0, match_pos - 80):min(len(log_text), match_pos + 80)]
    m = _NODE_PATTERN.search(context)
    if m:
        facts["Node"] = m.group(1)
    return facts


def _extract_source_loop_facts(log_text: str, match_str: str) -> Dict[str, str]:
    """Extract voltage/current source names from Source Loop context."""
    facts: Dict[str, str] = {}
    # Search a wider window around the match for source names
    pos = log_text.find(match_str)
    if pos >= 0:
        window = log_text[max(0, pos - 200):min(len(log_text), pos + 200)]
    else:
        window = match_str
    sources = _VSOURCE_RE.findall(window)
    # De-duplicate while preserving order
    seen = set()
    unique = []
    for s in sources:
        sl = s.lower()
        if sl not in seen:
            seen.add(sl)
            unique.append(s)
    if unique:
        facts["Sources"] = ", ".join(unique)
    return facts


def _extract_param_facts(log_text: str, match_str: str) -> Dict[str, str]:
    """Extract parameter details from an ERR012 match.

    Distinguishes between 'unknown parameter', 'missing parameter',
    and 'invalid numeric value' based on what the log explicitly says.
    """
    facts: Dict[str, str] = {}

    # Search in the full line from the log for richer context
    pos = log_text.find(match_str)
    if pos >= 0:
        line_start = log_text.rfind("\n", 0, pos) + 1
        line_end = log_text.find("\n", pos)
        if line_end == -1:
            line_end = len(log_text)
        full_line = log_text[line_start:line_end]
    else:
        full_line = match_str

    match_lower = full_line.lower()
    if "unknown" in match_lower or "no such" in match_lower:
        facts["Reason"] = "Unknown parameter"
    elif "missing" in match_lower:
        facts["Reason"] = "Missing parameter"
    else:
        facts["Reason"] = "Invalid parameter"

    # Try to extract the offending parameter name
    m = _PARAM_NAME_RE.search(full_line)
    if m:
        facts["Parameter"] = m.group(1)

    return facts


# ── Pattern table ────────────────────────────────────────────────────────────
# Each entry: (compiled_regex, error_id, category, causal_priority, diagnosis, extractor)
# extractor signature: (log_text, match_str) -> Dict  OR  (log_text, match_str, pos) -> Dict

_ERROR_PATTERNS: List[Tuple[re.Pattern, str, str, int, str, Any]] = [
    (
        re.compile(r"singular matrix", re.IGNORECASE),
        "ERR004", "Singular Matrix", 2,
        "The circuit matrix is singular — NgSpice cannot solve the DC operating point.",
        None,
    ),
    (
        re.compile(r"timestep too small", re.IGNORECASE),
        "ERR005", "Timestep Too Small", 2,
        "Transient analysis failed because the simulator could not converge within the minimum timestep.",
        None,
    ),
    (
        re.compile(r"no dc path to ground", re.IGNORECASE),
        "ERR003", "No DC Path to Ground", 1,
        "A node has no DC path to ground (node 0). Every node must have a resistive path to ground.",
        _extract_node_facts,
    ),
    # ERR001 — Missing Model (priority 1, but may be suppressed by ERR006)
    (
        re.compile(
            r"(?:(?:model|device)\s+['\"]?\S+['\"]?\s+(?:not found|undefined|unknown)"
            r"|can'?t\s+find\s+model"
            r"|could\s+not\s+find\s+a\s+valid\s+modelname)",
            re.IGNORECASE,
        ),
        "ERR001", "Missing Model", 1,
        "A component references a model/device that is not defined in the netlist.",
        _extract_missing_model_facts,
    ),
    # ERR006 — Invalid Model Syntax (priority 1, suppresses ERR001 during ranking)
    (
        re.compile(
            r"(?:Unknown\s+model\s+type\s+\S+\s*(?:-\s*ignored)?"
            r"|Invalid\s+model"
            r"|Model\s+issue\s+on\s+line)",
            re.IGNORECASE,
        ),
        "ERR006", "Invalid Model Syntax", 1,
        "A .model statement has an invalid type or incorrect parameter ordering. "
        "The type must immediately follow the model name.",
        _extract_invalid_model_facts,
    ),
    (
        re.compile(r"can'?t\s+find\s+init\s+file", re.IGNORECASE),
        "ERR007", "Init File Missing", 1,
        "NgSpice cannot find its initialization file (.spiceinit or spinit).",
        None,
    ),
    (
        re.compile(r"doAnalyses:\s+TRAN\s+?.*failed", re.IGNORECASE),
        "ERR008", "Transient Analysis Failed", 3,
        "The transient (.tran) analysis did not complete successfully.",
        None,
    ),
    (
        re.compile(
            r"(?:non-?convergence|failed\s+to\s+converge|convergence\s+fail)",
            re.IGNORECASE,
        ),
        "ERR009", "Convergence Failure", 2,
        "The simulator could not converge to a solution.",
        None,
    ),
    (
        re.compile(r"too\s+many\s+iterations", re.IGNORECASE),
        "ERR010", "Too Many Iterations", 2,
        "The DC operating point or transient step needed more iterations than allowed.",
        None,
    ),
    (
        re.compile(
            r"(?:voltage|current)\s+source\s+loop|singular\s+matrix.*?#branch",
            re.IGNORECASE,
        ),
        "ERR011", "Source Loop", 1,
        "Voltage sources form a loop, or current sources feed each other without a path.",
        _extract_source_loop_facts,
    ),
    # ERR002 — Missing Subcircuit: two NgSpice phrasings
    (
        re.compile(
            r"(?:unknown\s+subckt:\s+\S+|subcircuit\s+['\"]?\S+['\"]?\s+not\s+found)",
            re.IGNORECASE,
        ),
        "ERR002", "Missing Subcircuit", 1,
        "A subcircuit instantiation (X component) references a .subckt that is not defined.",
        _extract_subckt_facts_v2,
    ),
    (
        re.compile(
            r"(?:no\s+such\s+parameter|parameter\s+is\s+missing|unknown\s+parameter)",
            re.IGNORECASE,
        ),
        "ERR012", "Invalid Parameter / Syntax Error", 1,
        "A component has an invalid or missing parameter.",
        _extract_param_facts,
    ),
    (
        re.compile(r"Simulation Completed Successfully!", re.IGNORECASE),
        "ERR013", "No Plot Data (Simulation Succeeded)", 0,
        "The simulation actually completed successfully with no errors, but there is no data to plot.",
        None,
    ),
]


def match_error_patterns(log_text: str) -> List[ErrorMatch]:
    """Match known NgSpice error patterns in the log text.

    Returns a list of ErrorMatch objects.
    """
    matches: List[ErrorMatch] = []
    seen_categories: set = set()

    for pattern, error_id, category, causal_priority, diagnosis, extractor in _ERROR_PATTERNS:
        m = pattern.search(log_text)
        if m and category not in seen_categories:
            seen_categories.add(category)
            matched = m.group(0)

            facts: Dict[str, str] = {}
            if extractor:
                if extractor is _extract_node_facts:
                    facts = extractor(log_text, matched, m.start())
                else:
                    facts = extractor(log_text, matched)

            matches.append(ErrorMatch(
                error_id=error_id,
                category=category,
                causal_priority=causal_priority,
                diagnosis=diagnosis,
                matched_text=matched,
                extracted_facts=facts,
            ))

    return matches

