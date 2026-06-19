from typing import Dict, Any, List

ERROR_SOLUTIONS: Dict[str, Dict[str, Any]] = {
    "Singular Matrix": {
        "category": "Singular Matrix",
        "severity": "critical",
        "likely_causes": [
            "A node has no DC path to ground (floating node)",
            "Voltage source loop with zero series resistance",
            "Improperly connected component creating an open circuit"
        ],
        "fixes": [
            "Add a high-value resistor (1GΩ) from each floating node to ground",
            "Add a small series resistor (0.1Ω) to voltage sources in loops",
            "Check all component connections in the KiCad schematic"
        ],
        "esim_steps": [
            "Open KiCad schematic → check for unconnected pins",
            "Add '.options gmin=1e-12 reltol=0.01' in the .cir.out file via Spice Editor",
            "Use '.nodeset V(node)=value' to provide initial guesses"
        ],
        "prevention": [
            "Always add ground (GND) symbol from the power library",
            "Never leave nodes floating — tie unused inputs through resistors",
            "Run ERC (Electrical Rules Check) in KiCad before simulating"
        ]
    },
    "Timestep Too Small": {
        "category": "Timestep Too Small",
        "severity": "critical",
        "likely_causes": [
            "Rapid voltage/current changes that the simulator cannot resolve",
            "Unrealistic component values (e.g., zero capacitance/resistance)",
            "Non-linear component models causing discontinuities"
        ],
        "fixes": [
            "Increase TSTEP in .tran statement",
            "Add integration method option: method=gear",
            "Relax tolerances: reltol=0.01 abstol=1e-9"
        ],
        "esim_steps": [
            "In eSim, go to Simulation → Spice Editor",
            "Add '.options method=gear reltol=0.01 abstol=1e-9'",
            "Adjust Transient settings to use a larger step size"
        ],
        "prevention": [
            "Avoid ideal switches or sources with zero rise/fall times",
            "Use realistic parasitic values for components"
        ]
    },
    "No DC Path to Ground": {
        "category": "No DC Path to Ground",
        "severity": "critical",
        "likely_causes": [
            "Missing ground reference (Node 0) in the circuit",
            "Capacitively coupled nodes with no DC path",
            "Unconnected component pins"
        ],
        "fixes": [
            "Add GND symbol (0) to schematic",
            "Add 1GΩ resistors from floating nodes to GND for simulation stability",
            "Ensure all nodes have a resistive path to ground"
        ],
        "esim_steps": [
            "In KiCad, press 'A', search for 'GND' (power library), and place it",
            "Connect the GND symbol to your circuit's common return path",
            "Convert KiCad to NgSpice and simulate again"
        ],
        "prevention": [
            "Start every schematic by placing a GND symbol",
            "Run DRC/ERC to catch floating pins early"
        ]
    },
    "Missing Model": {
        "category": "Missing Model",
        "severity": "critical",
        "likely_causes": [
            "Component lacks SPICE model definition",
            "Incorrect model name specified",
            "Missing library inclusion"
        ],
        "fixes": [
            "Provide a valid SPICE model for the component",
            "Include the appropriate model library",
            "Use eSim standard library components when possible"
        ],
        "esim_steps": [
            "Open 'KiCad to Ngspice' converter window",
            "Go to 'Device Modeling' tab",
            "Click 'Add' to upload the missing .lib or .mod file",
            "Alternatively, add '.lib /usr/share/esim/models.lib' in schematic text"
        ],
        "prevention": [
            "Check IC availability in Components/ICs.pdf before design",
            "Verify model assignments in component properties"
        ]
    },
    "Invalid Model Syntax": {
        "category": "Invalid Model Syntax",
        "severity": "critical",
        "likely_causes": [
            "Incorrect parameter ordering in .model statement",
            "Missing model type identifier (e.g., D for diode, NPN for transistor)"
        ],
        "fixes": [
            "Fix the .model syntax: .model <name> <type> <param1=val1 ...>",
            "Ensure type identifier immediately follows model name"
        ],
        "esim_steps": [
            "Open Spice Editor (Ctrl+E) in eSim",
            "Locate the .model statement and correct the syntax",
            "Save and re-run simulation"
        ],
        "prevention": [
            "Consult NgSpice manual for correct model syntax"
        ]
    },
    "Init File Missing": {
        "category": "Init File Missing",
        "severity": "warning",
        "likely_causes": [
            "NgSpice initialization file (.spiceinit or spinit) is missing or corrupted",
            "Incorrect NgSpice installation path"
        ],
        "fixes": [
            "Reinstall NgSpice or eSim",
            "Ensure .spiceinit exists in the user's home directory or NgSpice share directory"
        ],
        "esim_steps": [
            "Check eSim installation integrity",
            "If on Linux, verify /usr/share/ngspice/scripts/spinit exists"
        ],
        "prevention": [
            "Do not modify internal NgSpice installation files"
        ]
    },
    "Transient Analysis Failed": {
        "category": "Transient Analysis Failed",
        "severity": "critical",
        "likely_causes": [
            "Simulation could not converge at a specific time point",
            "Oscillations or extremely fast edges"
        ],
        "fixes": [
            "Reduce TSTOP or increase TSTEP",
            "Change integration method to Gear",
            "Check component values for realism"
        ],
        "esim_steps": [
            "Open Spice Editor",
            "Modify the .tran line parameters",
            "Add '.options method=gear'"
        ],
        "prevention": [
            "Start with relaxed simulation parameters for new circuits"
        ]
    },
    "Convergence Failure": {
        "category": "Convergence Failure",
        "severity": "critical",
        "likely_causes": [
            "Highly non-linear circuits",
            "Positive feedback loops without limits",
            "Unrealistic component values"
        ],
        "fixes": [
            "Relax tolerances (reltol, abstol, vntol)",
            "Increase iteration limits (itl1, itl4)",
            "Provide initial conditions (.nodeset or .ic)"
        ],
        "esim_steps": [
            "Open Spice Editor",
            "Add '.options reltol=0.01 abstol=1e-9 vntol=1e-6 gmin=1e-12'",
            "Add '.options itl1=200 itl4=50'"
        ],
        "prevention": [
            "Ensure DC operating point is well-defined"
        ]
    },
    "Too Many Iterations": {
        "category": "Too Many Iterations",
        "severity": "critical",
        "likely_causes": [
            "DC operating point or transient step requires more iterations than allowed",
            "Bistable circuits struggling to settle"
        ],
        "fixes": [
            "Increase ITL1 (DC iterations) and ITL4 (Transient iterations)",
            "Use .nodeset to help the solver find the DC point"
        ],
        "esim_steps": [
            "Open Spice Editor",
            "Add '.options itl1=300 itl4=100'"
        ],
        "prevention": [
            "Use initial conditions for oscillators or flip-flops"
        ]
    },
    "Source Loop": {
        "category": "Source Loop",
        "severity": "critical",
        "likely_causes": [
            "Ideal voltage sources connected in a closed loop",
            "Current sources in series",
            "Inductors forming a loop with voltage sources"
        ],
        "fixes": [
            "Add a small series resistor (e.g., 1mΩ) to break voltage source loops",
            "Add a large parallel resistor to break current source series"
        ],
        "esim_steps": [
            "Open KiCad schematic",
            "Insert a small resistor component in series with one of the voltage sources",
            "Save and convert KiCad to NgSpice"
        ],
        "prevention": [
            "Avoid connecting ideal sources directly in parallel/series",
            "Use realistic source models with internal resistance"
        ]
    },
    "Missing Subcircuit": {
        "category": "Missing Subcircuit",
        "severity": "critical",
        "likely_causes": [
            "A component references a .subckt that is not defined",
            "Missing .include directive for the subcircuit file"
        ],
        "fixes": [
            "Add the missing .subckt definition",
            "Include the file containing the subcircuit"
        ],
        "esim_steps": [
            "Go to KiCad to Ngspice converter -> Device Modeling tab",
            "Add the missing subcircuit file (.sub or .lib)",
            "Or open Spice Editor and add '.include path/to/file.sub'"
        ],
        "prevention": [
            "Ensure all custom hierarchical blocks or ICs have their subcircuits included"
        ]
    },
    "Invalid Parameter / Syntax Error": {
        "category": "Invalid Parameter / Syntax Error",
        "severity": "critical",
        "likely_causes": [
            "Letters used instead of numbers for values (e.g., 'AA' instead of a voltage)",
            "Missing required parameters for a source or component"
        ],
        "fixes": [
            "Correct the component value to a valid number",
            "Ensure proper SPICE value suffixes (k, m, u, etc.) are used correctly"
        ],
        "esim_steps": [
            "In KiCad, double-click the problematic component",
            "Edit Properties -> Set Value to a valid number",
            "Save and re-convert to NgSpice"
        ],
        "prevention": [
            "Check all source parameters (sine, pulse, etc.) carefully"
        ]
    },
    "No Plot Data (Simulation Succeeded)": {
        "category": "No Plot Data (Simulation Succeeded)",
        "severity": "info",
        "likely_causes": [
            "Simulation completed successfully, but no plot probes were added to the schematic",
            "NgSpice has no variables to plot"
        ],
        "fixes": [
            "Add plot components to the schematic to measure voltages or currents"
        ],
        "esim_steps": [
            "Go back to KiCad schematic",
            "Place 'Plot' components (e.g., plot_v1, plot_i2) on wires to measure",
            "Convert to NgSpice and simulate again"
        ],
        "prevention": [
            "Always add plot probes to nodes of interest before simulating"
        ]
    }
}

def get_solution_for_category(category: str) -> Dict[str, Any]:
    """Get detailed solution for specific error category.
    
    This replaces substring-based matching with exact category mapping
    to ensure deterministic solution retrieval.
    """
    return ERROR_SOLUTIONS.get(category, {
        "category": category,
        "severity": "unknown",
        "likely_causes": ["Unknown schematic or simulator error"],
        "fixes": ["Check all connections", "Verify component values", "Ensure ground symbol is present"],
        "esim_steps": ["Run Design Rule Check (DRC) in KiCad"],
        "prevention": []
    })
