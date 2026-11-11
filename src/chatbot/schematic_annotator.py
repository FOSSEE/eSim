import os
import re
import logging

logger = logging.getLogger(__name__)

def annotate_schematic_component(schematic_path: str, component_ref: str, warning_msg: str) -> bool:
    """
    Parses a KiCad 6+ .kicad_sch file, locates component_ref coordinates,
    and appends a red graphic warning text directly near the component.
    """
    if not os.path.exists(schematic_path):
        logger.error(f"Schematic file not found: {schematic_path}")
        return False

    try:
        with open(schematic_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Match symbol block: (symbol ... (at X Y R) ... (property "Reference" "REF" ...))
        pattern = rf'\(symbol\b[^)]*?\s+\(at\s+([\d.-]+)\s+([\d.-]+)(?:\s+[\d.-]+)?\).+?\(property\s+"Reference"\s+"{re.escape(component_ref)}"'
        match = re.search(pattern, content, re.DOTALL)

        if not match:
            logger.warning(f"Component reference {component_ref} not found in schematic.")
            return False

        x_pos = float(match.group(1))
        y_pos = float(match.group(2))

        # Offset marker 5.08mm right and 2.54mm above the component origin
        note_x = x_pos + 5.08
        note_y = y_pos - 2.54

        # KiCad S-expression graphic text definition
        annotation = (
            f'\n  (gr_text "⚠️ AI: {warning_msg}" '
            f'(at {note_x:.2f} {note_y:.2f} 0) '
            f'(layer "Notes") '
            f'(effects (font (size 1.2 1.2) (color 255 0 0 bold))))\n'
        )

        last_paren_idx = content.rfind(')')
        if last_paren_idx == -1:
            return False

        updated_content = content[:last_paren_idx] + annotation + content[last_paren_idx:]

        with open(schematic_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        logger.info(f"Successfully annotated {component_ref} in {schematic_path}")
        return True

    except Exception as e:
        logger.error(f"Failed to annotate schematic: {e}")
        return False


def clear_schematic_annotations(schematic_path: str) -> bool:
    """Removes all AI warning annotations from the KiCad schematic."""
    if not os.path.exists(schematic_path):
        return False

    try:
        with open(schematic_path, 'r', encoding='utf-8') as f:
            content = f.read()

        cleaned_content = re.sub(
            r'\s*\(gr_text\s+"⚠️ AI:[^"]*".*?\)\s*',
            '\n',
            content,
            flags=re.DOTALL
        )

        with open(schematic_path, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)

        logger.info(f"Cleared AI annotations from {schematic_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to clear schematic annotations: {e}")
        return False
