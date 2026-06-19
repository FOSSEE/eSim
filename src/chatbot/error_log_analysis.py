"""Structured pre-processing for NgSpice simulation error logs.

Extracts deterministic facts from NgSpice output to provide structured
context for the LLM, reducing hallucination on weak local models.
"""

import re
from dataclasses import dataclass, field
from typing import Dict, List, Sequence, Tuple, Any, Optional

from chatbot.error_patterns import match_error_patterns, ErrorMatch
from chatbot.error_solutions import get_solution_for_category


# ── System prompt for error analysis ─────────────────────────────────────────

ERROR_ANALYSIS_SYSTEM_PROMPT = (
    "You are an expert circuit debugger inside eSim.\n\n"
    "TASK: Explain the pre-diagnosed error to the user in plain language.\n\n"
    "CRITICAL INSTRUCTIONS:\n"
    "- The error has ALREADY been diagnosed. Do NOT re-diagnose.\n"
    "- Use ONLY the [DETECTED ERROR] facts provided.\n"
    "- Focus on explaining WHY this error occurs in simple terms.\n"
    "- Reference the specific nodes/components mentioned.\n"
    "- Guide the user through the recommended fixes step-by-step.\n"
    "- Do NOT assume missing include files or filesystem problems unless "
    "explicitly stated in the error facts.\n"
    "- Keep your explanation concise (max 150 words).\n\n"
    "OUTPUT FORMAT:\n"
    "1. **Error** — One-line summary\n"
    "2. **Why** — Brief root cause explanation\n"
    "3. **Fix** — Step-by-step using the provided eSim steps\n"
)


# ── Ranked error with suppression metadata ───────────────────────────────────

@dataclass
class RankedError:
    """An error match annotated with its role and optional suppression info."""
    role: str                          # "Root Cause", "Secondary Issue", "Consequence"
    match: ErrorMatch
    suppressed_by: Optional[str] = None  # error_id of the suppressor, if any


# ── Suppression rules ────────────────────────────────────────────────────────
# Each rule: (suppressor_error_id, set_of_suppressed_error_ids)
# When the suppressor is present, the suppressed errors lose their root-cause
# status and are demoted to secondary/consequence.

_SUPPRESSION_RULES: List[Tuple[str, set]] = [
    # Invalid Model Syntax → suppresses Missing Model as root cause
    ("ERR006", {"ERR001"}),
    # Source Loop → suppresses Singular Matrix and Timestep Too Small as root causes
    ("ERR011", {"ERR004", "ERR005"}),
]

# Generic NgSpice messages that should never be promoted to root cause when
# a specific error (especially ERR002) is present.
_GENERIC_NOISE_PATTERNS = [
    re.compile(r"there\s+aren'?t\s+any\s+circuits\s+loaded", re.IGNORECASE),
    re.compile(r"no\s+valid\s+circuits", re.IGNORECASE),
    re.compile(r"simulation\s+failed!?", re.IGNORECASE),
    re.compile(r"circuit\s+not\s+parsed", re.IGNORECASE),
]

# Explicit include/file-error patterns — only when these appear should the
# LLM mention missing files.
_EXPLICIT_FILE_ERROR_PATTERNS = [
    re.compile(r"cannot\s+open\s+include\s+file", re.IGNORECASE),
    re.compile(r"can'?t\s+open\s+file", re.IGNORECASE),
    re.compile(r"include\s+file\s+not\s+found", re.IGNORECASE),
]


# ── Log fact extraction ──────────────────────────────────────────────────────

def extract_log_facts(log_lines: Sequence[str]) -> Dict[str, object]:
    """Extract structured facts from NgSpice log output."""
    full_text = "".join(log_lines)

    facts = {
        "total_lines": len(log_lines),
        "has_error": False,
        "error_patterns": [],
        "circuit_name": "",
        "simulation_type": "",
        "failed_nodes": [],
        "mentioned_components": [],
    }

    # Extract circuit name
    circuit_match = re.search(r"Circuit:\s*(.+)", full_text)
    if circuit_match:
        facts["circuit_name"] = circuit_match.group(1).strip()

    # Detect simulation type
    for sim_type in ("tran", "ac", "dc", "op", "noise"):
        if re.search(rf"\.{sim_type}\b", full_text, re.IGNORECASE):
            facts["simulation_type"] = sim_type
            break

    # Check for errors
    error_indicators = [
        "error", "failed", "singular", "convergence", "abort",
        "cannot", "not found", "undefined", "too small",
    ]
    facts["has_error"] = any(
        indicator in full_text.lower() for indicator in error_indicators
    )

    # Match known patterns
    facts["error_patterns"] = match_error_patterns(full_text)

    # Extract mentioned node names
    node_matches = re.findall(r"node\s+['\"]?(\S+)['\"]?", full_text, re.IGNORECASE)
    facts["failed_nodes"] = list(dict.fromkeys(node_matches))[:10]

    # Extract mentioned component references
    comp_matches = re.findall(
        r"\b([RCLVIDQMX]\d+)\b", full_text, re.IGNORECASE
    )
    facts["mentioned_components"] = list(dict.fromkeys(comp_matches))[:20]

    return facts


def rank_errors(matches: List[ErrorMatch]) -> List[RankedError]:
    """Rank errors with suppression logic.

    1. Apply explicit suppression rules (ERR006→ERR001, ERR011→ERR004/ERR005).
    2. Suppress generic noise when any specific error is present.
    3. All non-suppressed errors sharing the minimum causal_priority
       are labelled "Root Cause" (supports multiple root causes).
    4. Remaining errors are "Secondary Issue" (priority ≤ 2) or "Consequence".

    Each RankedError carries a ``suppressed_by`` field for traceability.
    """
    if not matches:
        return []

    present_ids = {m.error_id for m in matches}

    # Build suppression map: error_id → suppressor_error_id
    suppression_map: Dict[str, str] = {}
    for suppressor_id, suppressed_ids in _SUPPRESSION_RULES:
        if suppressor_id in present_ids:
            for sid in suppressed_ids:
                if sid in present_ids:
                    suppression_map[sid] = suppressor_id

    # Suppress generic noise when *any* specific pattern matched
    has_specific = any(
        m.error_id not in ("ERR008", "ERR013") for m in matches
    )

    # Partition into active and suppressed
    active: List[ErrorMatch] = []
    suppressed_entries: List[Tuple[ErrorMatch, str]] = []

    for m in matches:
        if m.error_id in suppression_map:
            suppressed_entries.append((m, suppression_map[m.error_id]))
        else:
            active.append(m)

    if not active:
        # Everything got suppressed — fall back to full list
        active = list(matches)
        suppressed_entries = []

    # Sort active by causal priority
    active.sort(key=lambda m: m.causal_priority)
    min_priority = active[0].causal_priority

    ranked: List[RankedError] = []

    for m in active:
        if m.causal_priority == min_priority:
            ranked.append(RankedError(role="Root Cause", match=m))
        elif m.causal_priority <= 2:
            ranked.append(RankedError(role="Secondary Issue", match=m))
        else:
            ranked.append(RankedError(role="Consequence", match=m))

    # Append suppressed errors as secondary/consequence with tracking
    for m, suppressor in suppressed_entries:
        if m.causal_priority <= 2:
            ranked.append(RankedError(
                role="Secondary Issue", match=m, suppressed_by=suppressor
            ))
        else:
            ranked.append(RankedError(
                role="Consequence", match=m, suppressed_by=suppressor
            ))

    return ranked


def _has_explicit_file_error(log_text: str) -> bool:
    """Return True only if the log explicitly mentions a missing file/include."""
    return any(p.search(log_text) for p in _EXPLICIT_FILE_ERROR_PATTERNS)


def _filter_likely_causes(
    causes: List[str], has_file_error: bool
) -> List[str]:
    """Remove include/file-related causes unless a file error was explicitly logged."""
    if has_file_error:
        return causes
    file_keywords = ("include", "library inclusion", "missing file", "open file")
    return [
        c for c in causes
        if not any(kw in c.lower() for kw in file_keywords)
    ]


def build_error_analysis_prompt(
    log_lines: Sequence[str],
    max_lines: int = 10,
) -> Tuple[str, List[Dict[str, Any]]]:
    """Build a structured prompt for the LLM from an NgSpice error log.

    Returns:
        A tuple of (prompt_string, list_of_tips_for_gui)
    """
    # Filter out harmless eSim default model warnings to prevent LLM hallucinations
    harmless_patterns = [
        re.compile(r"unable to find definition of model esim_", re.IGNORECASE),
        re.compile(r"-\s*default assumed", re.IGNORECASE),
        re.compile(r"^\*\* ngspice-\d+", re.IGNORECASE),
        re.compile(r"^\*\* The U\. C\. Berkeley CAD Group", re.IGNORECASE),
        re.compile(r"^\*\* Copyright", re.IGNORECASE),
        re.compile(r"^\*\* Please get your ngspice manual", re.IGNORECASE),
        re.compile(r"^\*\* Please file your bug-reports", re.IGNORECASE),
        re.compile(r"^\*{6,}$"),  # Matches the ****** banner separators
    ]

    filtered_lines: List[str] = []
    error_line_count = 0
    for line in log_lines:
        if not any(p.search(line) for p in harmless_patterns):
            filtered_lines.append(line)
            if "error" in line.lower() or "failed" in line.lower():
                error_line_count += 1

    facts = extract_log_facts(filtered_lines)
    matches: List[ErrorMatch] = facts["error_patterns"]
    ranked_errors = rank_errors(matches)

    full_text = "".join(filtered_lines)
    has_file_error = _has_explicit_file_error(full_text)

    # Coverage tracking
    matched_lines = len(set(m.matched_text for m in matches))
    if error_line_count == 0 and matched_lines > 0:
        coverage = "High"
    elif matched_lines >= error_line_count and error_line_count > 0:
        coverage = "High"
    elif matched_lines > 0:
        coverage = "Medium"
    else:
        coverage = "Low"

    sections: List[str] = []
    tips: List[Dict[str, Any]] = []

    # ── Detected Errors (all root causes) ────────────────────────────────
    root_causes = [r for r in ranked_errors if r.role == "Root Cause"]
    non_roots = [r for r in ranked_errors if r.role != "Root Cause"]

    if root_causes:
        if len(root_causes) > 1:
            sections.append("[CRITICAL ERRORS]")
            sections.append(
                "Multiple critical issues detected. "
                "Simulation cannot proceed until all are resolved."
            )
            sections.append("")

        for idx, rc in enumerate(root_causes, 1):
            m = rc.match
            solution = get_solution_for_category(m.category)
            likely_causes = _filter_likely_causes(
                solution.get("likely_causes", []), has_file_error
            )

            if len(root_causes) > 1:
                sections.append(f"--- Critical Error {idx} ---")
            sections.append("[DETECTED ERROR]")
            sections.append(f"Error ID: {m.error_id}")
            sections.append(f"Category: {m.category}")
            sections.append(f"Role: Root Cause")
            sections.append(f"Diagnosis: {m.diagnosis}")

            for k, v in m.extracted_facts.items():
                sections.append(f"Detected {k}: {v}")

            if likely_causes:
                sections.append("\nLikely Causes:")
                for cause in likely_causes:
                    sections.append(f"- {cause}")

            sections.append("\nRecommended Fixes:")
            for fix in solution.get("fixes", []):
                sections.append(f"- {fix}")

            sections.append("\neSim Steps:")
            for step in solution.get("esim_steps", []):
                sections.append(f"- {step}")

            if solution.get("prevention"):
                sections.append("\nPrevention:")
                for prev in solution["prevention"]:
                    sections.append(f"- {prev}")
            sections.append("[END DETECTED ERROR]")

            if solution.get("fixes"):
                tips.append({"fix": solution["fixes"][0]})

        if len(root_causes) > 1:
            sections.append("[END CRITICAL ERRORS]")

        # ── Secondary / Consequence issues ───────────────────────────────
        if non_roots:
            sections.append("\n[SECONDARY ISSUES]")
            for r in non_roots:
                label = f"{r.match.category} ({r.role})"
                if r.suppressed_by:
                    label += f" [suppressed by {r.suppressed_by}]"
                sections.append(f"- {label}")
            sections.append("[END SECONDARY ISSUES]")

    # ── Coverage tracking ────────────────────────────────────────────────
    sections.append("\n[COVERAGE TRACKING]")
    sections.append(f"Detected Patterns: {len(matches)}")
    sections.append(f"Coverage: {coverage}")
    sections.append("[END COVERAGE TRACKING]")

    # ── Circuit Context ──────────────────────────────────────────────────
    sections.append("\n[CIRCUIT CONTEXT]")
    if facts["circuit_name"]:
        sections.append(f"Circuit: {facts['circuit_name']}")
    if facts["simulation_type"]:
        sections.append(f"Simulation type: {facts['simulation_type']}")
    if facts["failed_nodes"]:
        sections.append(f"Mentioned nodes: {', '.join(facts['failed_nodes'])}")
    if facts["mentioned_components"]:
        sections.append(f"Mentioned components: {', '.join(facts['mentioned_components'])}")
    sections.append("[END CIRCUIT CONTEXT]")

    # ── Raw Error Snippet Fallback ───────────────────────────────────────
    sections.append("\n[RAW ERROR SNIPPET]")
    snippet_lines = filtered_lines[-max_lines:] if len(filtered_lines) > max_lines else filtered_lines
    sections.append("".join(snippet_lines).strip())
    sections.append("[END RAW ERROR SNIPPET]")

    return ("\n".join(sections), tips)

