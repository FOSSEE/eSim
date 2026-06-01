# error_solutions.py
from typing import Dict,Any

ERROR_SOLUTIONS = {
    "no ground": {
        "description": "Missing ground reference (Node 0)",
        "severity": "critical",
        "fixes": [
            "Add GND symbol (0) to schematic",
            "Ensure all nodes have DC path to ground",
            "Add 1GΩ resistors from floating nodes to GND for simulation stability",
            "Use GND symbol from eSim power library"
        ],
        "eSim_command": "Add 'GND' symbol from 'power' library"
    },
    
    "floating pins": {
        "description": "Unconnected component pins",
        "severity": "moderate",
        "fixes": [
            "Connect all unused pins to appropriate nets",
            "For unused inputs: tie to VCC or GND through resistors",
            "For unused outputs: leave unconnected but label properly"
        ],
        "eSim_command": "Use 'Place Wire' tool to connect pins"
    },
    
    "disconnected wires": {
        "description": "Wires not properly connected to pins",
        "severity": "critical",
        "fixes": [
            "Zoom in and check wire endpoints touch pins",
            "Use junction dots at wire intersections",
            "Re-route wires to ensure proper connections"
        ],
        "eSim_command": "Press 'J' to add junction dots"
    },
    
    "missing spice model": {
        "description": "Component lacks SPICE model definition",
        "severity": "critical",
        "fixes": [
            "Add .lib statement: .lib /usr/share/esim/models.lib",
            "Check IC availability in Components/ICs.pdf",
            "Use eSim library components only",
            "Create custom model using Model Editor"
        ],
        "eSim_command": "Add '.lib /usr/share/esim/models.lib' in schematic"
    },
    
    "singular matrix": {
        "description": "Simulation convergence error",
        "severity": "critical",
        "fixes": [
            "Add 1GΩ resistors from ALL nodes → GND",
            "Add .options gmin=1e-12 reltol=0.01",
            "Use .nodeset for initial voltages",
            "Add 0.1Ω series resistors to voltage sources"
        ],
        "eSim_command": "Add '.options gmin=1e-12 reltol=0.01' in .cir file"
    },
    
    "missing component values": {
        "description": "Components without specified values",
        "severity": "moderate",
        "fixes": [
            "Double-click components to edit values",
            "Set R, C, L values before simulation",
            "For ICs: specify model number",
            "For sources: set voltage/current values"
        ],
        "eSim_command": "Double-click component → Edit Properties → Set Value"
    },
    
    "no load after rectifier": {
        "description": "Rectifier output has no load capacitor",
        "severity": "warning",
        "fixes": [
            "Add filter capacitor after rectifier (100-1000μF)",
            "Add load resistor to establish DC operating point",
            "Add voltage regulator for stable output"
        ],
        "eSim_command": "Add capacitor between rectifier output and GND"
    }
}

def get_error_solution(error_message: str) -> Dict[str, Any]:
    """Get detailed solution for specific error."""
    error_lower = error_message.lower()
    
    for error_key, solution in ERROR_SOLUTIONS.items():
        if error_key in error_lower:
            return solution
    
    # Default solution for unknown errors
    return {
        "description": "General schematic error",
        "severity": "unknown",
        "fixes": [
            "Check all connections are proper",
            "Verify component values are set",
            "Ensure ground symbol is present",
            "Check for duplicate component IDs"
        ],
        "eSim_command": "Run Design Rule Check (DRC) in KiCad"
    }
