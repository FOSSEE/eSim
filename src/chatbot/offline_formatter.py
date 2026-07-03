"""Offline (LLM-free) response formatters for the eSim AI Assistant.

When Ollama is unavailable, these functions format the deterministic
pipeline output into structured plain-text responses.  All diagnostic
data comes from the existing error and netlist analysis pipelines;
no LLM call is made.
"""

import re
from typing import Dict, List, Sequence, Tuple, Any

from chatbot.error_log_analysis import (
    extract_log_facts,
    rank_errors,
    _has_explicit_file_error,
    _filter_likely_causes,
)
from chatbot.error_solutions import get_solution_for_category
from chatbot.netlist_analysis import (
    ParsedNetlist,
    detect_circuit_blocks,
    format_netlist_table,
)


# ── Harmless log patterns (same as in build_error_analysis_prompt) ────────────
# These are filtered out before analysis to prevent false positives.

_HARMLESS_PATTERNS = [
    re.compile(r"unable to find definition of model esim_", re.IGNORECASE),
    re.compile(r"-\s*default assumed", re.IGNORECASE),
    re.compile(r"^\*\* ngspice-\d+", re.IGNORECASE),
    re.compile(r"^\*\* The U\. C\. Berkeley CAD Group", re.IGNORECASE),
    re.compile(r"^\*\* Copyright", re.IGNORECASE),
    re.compile(r"^\*\* Please get your ngspice manual", re.IGNORECASE),
    re.compile(r"^\*\* Please file your bug-reports", re.IGNORECASE),
    re.compile(r"^\*{6,}$"),
]

_OFFLINE_FOOTNOTE = (
    "\n\n---\n"
    "💡 **Note:** This analysis was generated using the deterministic "
    "pipeline without an LLM. *For a more detailed natural-language "
    "explanation, start **Ollama** with a local model and retry.*"
)

_NETLIST_OFFLINE_FOOTNOTE = (
    "\n\n---\n"
    "💡 **Note:** This analysis is based only on static SPICE netlist inspection. "
    "Circuit operation, voltages, currents, transient behavior, convergence, "
    "and performance can only be verified by running a simulation.\n\n"
    "*For a more detailed natural-language explanation, start **Ollama** with "
    "a local model and retry.*"
)


# ── Error analysis offline formatter ─────────────────────────────────────────

def format_error_analysis_offline(
    log_lines: Sequence[str],
) -> str:
    """Format error analysis results as structured text without an LLM.

    Runs the full deterministic error pipeline (regex matching, ranking,
    suppression, solution lookup) and formats the output directly.

    Returns:
        A plain-text response string ready to display in the chat UI.
    """
    # Filter out harmless NgSpice banners and default-model warnings
    filtered_lines: List[str] = [
        line for line in log_lines
        if not any(p.search(line) for p in _HARMLESS_PATTERNS)
    ]

    if not filtered_lines:
        return "⚠️ **No meaningful error output found in the log.**" + _OFFLINE_FOOTNOTE

    facts = extract_log_facts(filtered_lines)
    matches = facts["error_patterns"]
    ranked_errors = rank_errors(matches)

    if not ranked_errors:
        return (
            "⚠️ **No known error patterns were detected in the log.**\n\n"
            "*The simulation output may contain warnings or non-standard "
            "messages that the deterministic pipeline does not yet cover.*"
            + _OFFLINE_FOOTNOTE
        )

    full_text = "".join(filtered_lines)
    has_file_error = _has_explicit_file_error(full_text)

    root_causes = [r for r in ranked_errors if r.role == "Root Cause"]
    non_roots = [r for r in ranked_errors if r.role != "Root Cause"]
    total_errors = len(ranked_errors)

    sections: List[str] = []
    sections.append("### 🛠️ Error Analysis Results\n")

    # ── Root causes ──────────────────────────────────────────────────
    for idx, rc in enumerate(root_causes, 1):
        m = rc.match
        solution = get_solution_for_category(m.category)
        likely_causes = _filter_likely_causes(
            solution.get("likely_causes", []), has_file_error
        )

        role_label = "Root Cause" if rc.role == "Root Cause" else rc.role
        if total_errors > 1:
            sections.append(
                f"#### 🔴 Error {idx} of {total_errors}: **{m.category}** `({role_label})`"
            )
        else:
            sections.append(f"#### 🔴 Detected Error: **{m.category}** `({role_label})`")

        severity = solution.get('severity', 'unknown').upper()
        sections.append(f"- **Severity:** `{severity}`")
        sections.append("")
        sections.append(f"**📋 Diagnosis:**\n{m.diagnosis}")

        # Entity extraction (node name, model name, etc.)
        if m.extracted_facts:
            sections.append("")
            for key, value in m.extracted_facts.items():
                sections.append(f"- **Detected {key.title()}:** `{value}`")

        if likely_causes:
            sections.append("\n**❓ Likely Causes:**")
            for cause in likely_causes:
                sections.append(f"- {cause}")

        fixes = solution.get("fixes", [])
        if fixes:
            sections.append("\n**🔧 Recommended Fixes:**")
            for i, fix in enumerate(fixes, 1):
                sections.append(f"{i}. **{fix}**")

        esim_steps = solution.get("esim_steps", [])
        if esim_steps:
            sections.append("\n**📝 eSim Steps:**")
            for i, step in enumerate(esim_steps, 1):
                sections.append(f"{i}. {step}")

        prevention = solution.get("prevention", [])
        if prevention:
            sections.append("\n**🛡️ Prevention:**")
            for tip in prevention:
                sections.append(f"- *{tip}*")

        sections.append("")

    # ── Secondary / consequence issues ───────────────────────────────
    if non_roots:
        sections.append("#### ⚠️ Secondary Issues")
        for r in non_roots:
            label = f"**{r.match.category}** `({r.role})`"
            if r.suppressed_by:
                label += f" *(related to `{r.suppressed_by}`)*"
            solution = get_solution_for_category(r.match.category)
            fix = solution.get("fixes", [""])[0]
            sections.append(f"- {label}")
            if fix:
                sections.append(f"  - *Fix:* {fix}")
        sections.append("")

    # ── Circuit context ──────────────────────────────────────────────
    context_parts = []
    if facts.get("circuit_name"):
        context_parts.append(f"- **Circuit:** `{facts['circuit_name']}`")
    if facts.get("simulation_type"):
        context_parts.append(f"- **Simulation Type:** `{facts['simulation_type']}`")
    if facts.get("failed_nodes"):
        nodes_str = ", ".join(f"`{n}`" for n in facts['failed_nodes'])
        context_parts.append(f"- **Mentioned Nodes:** {nodes_str}")
    if facts.get("mentioned_components"):
        comps_str = ", ".join(f"`{c}`" for c in facts['mentioned_components'])
        context_parts.append(f"- **Mentioned Components:** {comps_str}")
    if context_parts:
        sections.append("#### 🔌 Circuit Context")
        sections.extend(context_parts)
        sections.append("")

    sections.append(_OFFLINE_FOOTNOTE)

    return "\n".join(sections)


# ── Netlist analysis offline formatter ───────────────────────────────────────

def _get_block_friendly_name(block_name: str) -> str:
    name_lower = block_name.lower()
    if "bridge rectifier" in name_lower:
        return "a bridge rectifier"
    elif "regulator" in name_lower:
        for model in ["7805", "7809", "7812"]:
            if model in name_lower:
                return f"an LM{model} regulator"
        return "a voltage regulator"
    elif "filter capacitor" in name_lower:
        return "a filter capacitor"
    elif "output load" in name_lower:
        return "an output load"
    else:
        clean_name = block_name.replace(" stage", "").replace(" STAGE", "").strip()
        return f"a {clean_name.lower()}"


def _generate_circuit_overview(
    parsed: ParsedNetlist, high_conf_blocks: List[Tuple[str, str, str]]
) -> str:
    if high_conf_blocks:
        has_rectifier = any("rectifier" in b[0].lower() for b in high_conf_blocks)
        has_regulator = any("regulator" in b[0].lower() for b in high_conf_blocks)
        has_filter = any("capacitor" in b[0].lower() for b in high_conf_blocks)

        detected_type = None
        if has_rectifier and has_regulator:
            detected_type = "AC to regulated DC power supply"
        elif has_rectifier and has_filter:
            detected_type = "AC to DC rectifier and filter circuit"
        elif has_rectifier:
            detected_type = "AC to DC rectifier circuit"
        elif has_regulator:
            detected_type = "DC voltage regulation circuit"

        friendly_names = [_get_block_friendly_name(b[0]) for b in high_conf_blocks]
        if len(friendly_names) == 1:
            blocks_sentence = f"The circuit contains {friendly_names[0]}."
        elif len(names_list := friendly_names) == 2:
            blocks_sentence = f"The circuit contains {names_list[0]} and {names_list[1]}."
        else:
            blocks_sentence = f"The circuit contains {', '.join(friendly_names[:-1])}, and {friendly_names[-1]}."

        if detected_type:
            return f"Detected circuit: {detected_type}.\n\n{blocks_sentence}"
        else:
            return blocks_sentence
    else:
        comp_type_map = {
            'R': 'resistors', 'C': 'capacitors', 'L': 'inductors',
            'V': 'voltage sources', 'I': 'current sources',
            'D': 'diodes', 'Q': 'bipolar transistors',
            'M': 'MOSFETs', 'J': 'JFETs', 'X': 'subcircuits'
        }
        present_prefixes = sorted(list(set(c.prefix for c in parsed.components if c.prefix in comp_type_map)))
        if present_prefixes:
            names = [comp_type_map[p] for p in present_prefixes]
            if len(names) == 1:
                return f"The circuit is a basic network consisting of {names[0]}."
            elif len(names) == 2:
                return f"The circuit is a basic network consisting of {names[0]} and {names[1]}."
            else:
                return f"The circuit is a general network consisting of {', '.join(names[:-1])}, and {names[-1]}."
        else:
            return "The netlist contains no standard circuit blocks or recognized components."


def _format_detected_block(block_name: str, relationship: str) -> str:
    name_lower = block_name.lower()
    lines = [f"- **{block_name}**"]

    if "rectifier" in name_lower:
        lines.append("  Converts the AC input into pulsating DC.")
        conn = relationship.replace("DC+ node is ", "DC+ = ").replace("DC- node is ", "DC− = ")
        lines.append(f"  Connection: {conn}")
    elif "regulator" in name_lower:
        if "7805" in name_lower:
            reg_model = "an LM7805"
        elif "7809" in name_lower:
            reg_model = "an LM7809"
        elif "7812" in name_lower:
            reg_model = "an LM7812"
        else:
            reg_model = "a voltage"
        lines.append(f"  Regulates the filtered DC using {reg_model} regulator.")
        conn = relationship.replace("nodes are ", "")
        lines.append(f"  Nodes: {conn.upper() if conn.replace(',', '').replace(' ', '').isalpha() else conn}")
    elif "capacitor" in name_lower:
        lines.append("  Smooths the rectified voltage.")
        lines.append(f"  {relationship.capitalize()}")
    elif "load" in name_lower:
        lines.append("  Represents the output load connected across the regulated output.")
    else:
        lines.append("  Circuit functional stage.")
        lines.append(f"  {relationship.capitalize()}")

    return "\n".join(lines)


def format_netlist_analysis_offline(
    parsed: ParsedNetlist,
    raw_lines: Sequence[str],
) -> str:
    """Format netlist analysis results as structured text without an LLM.

    Uses the existing ``format_netlist_table()`` for component and simulation
    setup formatting, then appends obvious issues and detected circuit blocks.

    Returns:
        A Markdown-formatted response string ready to display in the chat UI.
    """
    sections: List[str] = []

    # ── 1. Circuit Overview (New Section) ────────────────────────────
    blocks = detect_circuit_blocks(parsed)
    high_conf = [b for b in blocks if b[1] == "HIGH"]

    overview_text = _generate_circuit_overview(parsed, high_conf)
    sections.append("### Circuit Overview\n" + overview_text)

    # ── 2. Component table and simulation setup (already implemented) ────
    table_md = format_netlist_table(parsed)
    note_marker = "\n\n💡 **Note:** This overview is based on static netlist analysis. Run a simulation to verify circuit behavior and identify issues that may not be apparent from the netlist alone."
    if note_marker in table_md:
        table_md = table_md.split(note_marker)[0]
    sections.append(table_md)

    # ── 3. Obvious issues ───────────────────────────────────────────────
    issues: List[str] = []
    if not parsed.reference_node_0_present and not parsed.gnd_label_present:
        issues.append("Missing reference ground (node `0` or `GND`).")
    if not parsed.analysis_directives:
        issues.append(
            "No simulation directives (e.g., `.tran`, `.dc`, `.ac`) found."
        )
    if parsed.unresolved_subckt_calls:
        names = ", ".join(
            f"`{c.subcircuit}`" for c in parsed.unresolved_subckt_calls
        )
        issues.append(f"Unresolved subcircuits: {names}")
    missing_includes = [
        f"`{item.token}`" for item in parsed.includes if not item.exists
    ]
    if missing_includes:
        issues.append(
            f"Missing included files: {', '.join(missing_includes)}"
        )

    if issues:
        sections.append("\n### Issues Found")
        for issue in issues:
            sections.append(f"- **{issue}**")
    else:
        sections.append("\n### Issues Found")
        sections.append("- *No obvious issues detected.*")

    # ── 4. Detected circuit blocks ──────────────────────────────────────
    sections.append("\n### Detected Circuit Blocks")
    if high_conf:
        block_strings = [
            _format_detected_block(block_name, relationship)
            for block_name, _, relationship in high_conf
        ]
        sections.append("\n\n".join(block_strings))
    else:
        sections.append(
            "- *No standard circuit blocks detected with high confidence.*"
        )

    # ── 5. Model and subcircuit definitions ─────────────────────────────
    if parsed.model_names:
        models_str = ", ".join(f"`{m}`" for m in parsed.model_names)
        sections.append(
            f"\n**Defined Models:** {models_str}"
        )
    if parsed.subckt_definitions:
        subckts_str = ", ".join(f"`{s}`" for s in parsed.subckt_definitions)
        sections.append(
            f"**Defined Subcircuits:** {subckts_str}"
        )

    sections.append(_NETLIST_OFFLINE_FOOTNOTE)

    return "\n".join(sections)
