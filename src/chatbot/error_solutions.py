from typing import Dict, Any, List

ERROR_SOLUTIONS: Dict[str, Dict[str, Any]] = {
    "Singular Matrix": {
        "category": "Singular Matrix",
        "severity": "critical",
        "likely_causes": [
            "A node has no DC path to ground (floating node)",
            "Two or more ideal voltage sources are connected in a loop with zero series resistance",
            "A component pin is unconnected, creating an open circuit in the netlist",
            "An inductor or transformer winding has no parallel resistance to ground"
        ],
        "fixes": [
            "Verify every component pin is connected in the KiCad schematic",
            "Check for floating nodes — every node must have a resistive DC path to ground",
            "Add a small series resistor (0.1 ohm) to break any voltage source loop",
            "Add a high-value resistor (1G ohm) from floating nodes to ground if needed for simulation stability",
            "If the circuit is correct, add '.options gmin=1e-12' to increase minimum conductance"
        ],
        "esim_steps": [
            "In KiCad, run Inspect -> Electrical Rules Check (ERC) to find unconnected pins",
            "Fix all ERC errors, then go to Simulation -> Convert KiCad to NgSpice",
            "If the circuit is correct but still fails, open Simulation -> Spice Editor and add '.options gmin=1e-12 reltol=0.01'",
            "For stubborn cases, add '.nodeset V(node)=value' to provide initial operating point guesses"
        ],
        "prevention": [
            "Always place a GND symbol from the power library before wiring",
            "Never leave component pins floating — tie unused inputs through resistors to a known potential",
            "Run ERC in KiCad before every simulation"
        ]
    },
    "Timestep Too Small": {
        "category": "Timestep Too Small",
        "severity": "critical",
        "likely_causes": [
            "A source has zero rise/fall time, causing an infinitely fast edge the simulator cannot resolve",
            "Unrealistic component values (e.g., zero-ohm resistance, zero capacitance)",
            "Non-linear component models (diodes, transistors) creating sharp switching discontinuities",
            "Simulation step size is too large relative to the circuit's fastest time constant"
        ],
        "fixes": [
            "Check all sources for zero rise/fall times and set realistic values (e.g., 1ns minimum)",
            "Verify component values are physically realistic — no zero resistance or capacitance",
            "If the circuit is correct, increase TSTEP in the .tran statement to give the solver more room",
            "If still failing, add '.options method=gear' for better numerical stability",
            "As a last resort, relax tolerances: '.options reltol=0.01 abstol=1e-9'"
        ],
        "esim_steps": [
            "In KiCad, double-click each source and verify rise/fall times are non-zero",
            "Go to Simulation -> Convert KiCad to NgSpice to regenerate the netlist",
            "If the circuit is correct, open Simulation -> Spice Editor",
            "Modify the .tran line to use a larger step (e.g., .tran 1u 10m)",
            "Add '.options method=gear reltol=0.01' if needed"
        ],
        "prevention": [
            "Always set non-zero rise and fall times for pulse and PWL sources",
            "Use realistic parasitic values — real components always have some resistance and capacitance",
            "Start with a relaxed timestep and tighten only after a successful initial simulation"
        ]
    },
    "No DC Path to Ground": {
        "category": "No DC Path to Ground",
        "severity": "critical",
        "likely_causes": [
            "The circuit has no GND symbol (node 0) — NgSpice requires a ground reference",
            "A node is connected only through capacitors, which block DC",
            "A component pin is unconnected, isolating part of the circuit from ground"
        ],
        "fixes": [
            "Verify the circuit contains a GND reference symbol connected to the common return path",
            "For capacitively-coupled nodes, add a high-value resistor (1G ohm) to ground for DC bias",
            "Check all component pins for proper connections — look for unconnected wires"
        ],
        "esim_steps": [
            "In KiCad, press 'A' to add a component, search for 'GND' in the power library, and place it",
            "Connect the GND symbol to your circuit's common return path (negative terminal of main supply)",
            "Go to Simulation -> Convert KiCad to NgSpice and simulate again"
        ],
        "prevention": [
            "Start every new schematic by placing a GND symbol first",
            "Run Inspect -> Electrical Rules Check (ERC) to catch floating pins early",
            "Remember: every node in a SPICE netlist must have a DC path to node 0"
        ]
    },
    "Missing Model": {
        "category": "Missing Model",
        "severity": "critical",
        "likely_causes": [
            "The component references a .model name that is not defined anywhere in the netlist",
            "The .lib or .mod file containing the model was not included",
            "The model name in the component does not match the name in the .model definition (case-sensitive)"
        ],
        "fixes": [
            "Verify the model name on the component exactly matches the .model or .subckt definition",
            "Include the library file containing the model definition",
            "If no external model exists, use eSim's built-in standard library components"
        ],
        "esim_steps": [
            "Go to Simulation -> Convert KiCad to NgSpice -> Device Modeling tab",
            "Click 'Add' and upload the missing .lib or .mod file for the component",
            "Verify the model name shown in Device Modeling matches the component's value field",
            "If using a custom model, add '.lib /path/to/your/model.lib' via Simulation -> Spice Editor"
        ],
        "prevention": [
            "Before placing a component, check that its SPICE model is available (see eSim docs or Components/ICs.pdf)",
            "Verify model name assignments in component properties after placement",
            "Keep all custom .lib/.mod files in the project directory for portability"
        ]
    },
    "Invalid Model Syntax": {
        "category": "Invalid Model Syntax",
        "severity": "critical",
        "likely_causes": [
            "Incorrect parameter ordering in the .model statement",
            "Missing model type keyword (e.g., D for diode, NPN/PNP for BJT, NMOS/PMOS for MOSFET)",
            "Syntax errors such as missing parentheses or invalid parameter names"
        ],
        "fixes": [
            "Correct the .model syntax: .model <name> <type> (<param1=val1 param2=val2 ...>)",
            "Ensure the type keyword (D, NPN, PNP, NMOS, PMOS) immediately follows the model name",
            "Check for typos in parameter names by consulting the NgSpice manual for valid parameters"
        ],
        "esim_steps": [
            "Open Simulation -> Spice Editor to view the generated netlist",
            "Locate the .model statement and correct the syntax",
            "Save and re-run the simulation"
        ],
        "prevention": [
            "Use eSim's built-in Device Modeling tab to set models instead of editing .model lines manually",
            "Refer to the NgSpice manual for correct .model syntax for each device type"
        ]
    },
    "Init File Missing": {
        "category": "Init File Missing",
        "severity": "warning",
        "likely_causes": [
            "The NgSpice initialization file (.spiceinit or spinit) is missing or was accidentally deleted",
            "The eSim or NgSpice installation is incomplete"
        ],
        "fixes": [
            "Verify the init file exists at the expected path for your OS",
            "On Linux, check that /usr/share/ngspice/scripts/spinit exists",
            "On Windows, check the NgSpice installation directory for spinit"
        ],
        "esim_steps": [
            "On Linux, run: ls /usr/share/ngspice/scripts/spinit",
            "If missing, reinstall eSim to restore the default initialization files",
            "Do not manually edit spinit unless you understand NgSpice configuration"
        ],
        "prevention": [
            "Do not modify or delete files inside the NgSpice installation directory"
        ]
    },
    "Transient Analysis Failed": {
        "category": "Transient Analysis Failed",
        "severity": "critical",
        "likely_causes": [
            "A source has zero rise/fall time creating an infinitely steep edge",
            "Component values are unrealistic (e.g., zero resistance in series with an inductor)",
            "The simulation stop time (TSTOP) is too long relative to circuit dynamics, exhausting solver resources",
            "Positive feedback without limiting causes oscillation the solver cannot track"
        ],
        "fixes": [
            "Set non-zero rise/fall times on all pulse and PWL sources",
            "Check all component values for physical realism — no zero-ohm or near-zero values",
            "Reduce TSTOP or increase TSTEP to give the solver an easier time stepping",
            "If the circuit is correct, add '.options method=gear' for improved numerical stability",
            "For oscillating circuits, provide initial conditions with '.ic V(node)=value'"
        ],
        "esim_steps": [
            "In KiCad, double-click each source and verify parameters are realistic",
            "Go to Simulation -> Convert KiCad to NgSpice to regenerate the netlist",
            "Open Simulation -> Spice Editor and modify the .tran line (reduce TSTOP or increase TSTEP)",
            "If still failing, add '.options method=gear' in the Spice Editor"
        ],
        "prevention": [
            "Start with short simulation times and relaxed timesteps for new circuits",
            "Always use non-zero rise/fall times on switching sources",
            "Verify the DC operating point is valid before running transient analysis"
        ]
    },
    "Convergence Failure": {
        "category": "Convergence Failure",
        "severity": "critical",
        "likely_causes": [
            "Unrealistic component values preventing the solver from finding a valid operating point",
            "Positive feedback loops without saturation or limiting mechanisms",
            "Missing bias resistors on transistor bases or gates",
            "Highly non-linear circuits (e.g., oscillators, schmitt triggers) without initial conditions"
        ],
        "fixes": [
            "Check all component values for physical realism — no zero or near-infinite values",
            "Ensure all transistor bases/gates have proper bias paths (resistors to supply or ground)",
            "Provide initial conditions using '.ic V(node)=value' or '.nodeset V(node)=value'",
            "If the circuit design is correct, relax tolerances: '.options reltol=0.01 abstol=1e-9 vntol=1e-6'",
            "As a last resort, increase iteration limits: '.options itl1=200 itl4=50'"
        ],
        "esim_steps": [
            "In KiCad, verify all transistor bias networks are complete (no floating bases/gates)",
            "Go to Simulation -> Convert KiCad to NgSpice to regenerate the netlist",
            "Open Simulation -> Spice Editor and add '.nodeset V(node)=expected_voltage' for key nodes",
            "If still failing, add '.options reltol=0.01 abstol=1e-9 gmin=1e-12' in the Spice Editor"
        ],
        "prevention": [
            "Ensure the DC operating point is well-defined before running AC or transient analysis",
            "Use initial conditions for oscillators, flip-flops, and bistable circuits",
            "Start with simple circuits and add complexity incrementally"
        ]
    },
    "Too Many Iterations": {
        "category": "Too Many Iterations",
        "severity": "critical",
        "likely_causes": [
            "The DC operating point is ambiguous — the solver cannot decide between multiple valid states",
            "Bistable circuits (flip-flops, latches) without defined initial conditions",
            "Missing or incorrect bias resistors causing the solver to hunt for a stable point",
            "Extremely stiff circuits with widely varying time constants"
        ],
        "fixes": [
            "Provide initial conditions using '.nodeset V(node)=value' to guide the DC solver",
            "Verify all bias networks are complete — no floating gates or bases",
            "Check for unrealistic component ratios (e.g., 1 ohm in series with 1G ohm)",
            "If the circuit is correct, increase iteration limits: '.options itl1=300 itl4=100'"
        ],
        "esim_steps": [
            "Open Simulation -> Spice Editor",
            "Add '.nodeset V(output)=0' (or expected voltage) to help the solver find the operating point",
            "If that is not enough, add '.options itl1=300 itl4=100' to allow more solver iterations",
            "Save and re-run the simulation"
        ],
        "prevention": [
            "Always provide '.ic' or '.nodeset' for oscillators, flip-flops, and memory circuits",
            "Verify bias resistor values create a well-defined DC operating point",
            "Start with a DC analysis (.op) before running transient to confirm the operating point"
        ]
    },
    "Source Loop": {
        "category": "Source Loop",
        "severity": "critical",
        "likely_causes": [
            "Two or more ideal voltage sources are connected in a closed loop (conflicting voltages)",
            "Ideal current sources are connected in series (conflicting currents)",
            "An inductor forms a loop with a voltage source, creating a short at DC"
        ],
        "fixes": [
            "Add a small series resistor (1m ohm to 1 ohm) to break the voltage source loop",
            "For current sources in series, add a large parallel resistor (1G ohm) across one source",
            "For inductor-voltage source loops, add a small series resistance to the inductor"
        ],
        "esim_steps": [
            "In KiCad, identify the loop by tracing from one voltage source back to itself",
            "Insert a small resistor component in series with one of the sources in the loop",
            "Save and go to Simulation -> Convert KiCad to NgSpice"
        ],
        "prevention": [
            "Never connect ideal voltage sources directly in parallel",
            "Never connect ideal current sources directly in series",
            "Use realistic source models that include small internal resistance"
        ]
    },
    "Missing Subcircuit": {
        "category": "Missing Subcircuit",
        "severity": "critical",
        "likely_causes": [
            "A component (X-prefixed instance) references a .subckt name that is not defined in the netlist",
            "The .lib or .sub file containing the subcircuit definition was not included",
            "The subcircuit name on the component does not match the .subckt definition (case-sensitive)"
        ],
        "fixes": [
            "Verify the subcircuit name on the component exactly matches the .subckt definition in the library file",
            "Include the file containing the subcircuit using the Device Modeling tab or a .include directive",
            "Check that the number of pins on the component matches the .subckt port count"
        ],
        "esim_steps": [
            "Go to Simulation -> Convert KiCad to NgSpice -> Device Modeling tab",
            "Click 'Add' and upload the missing subcircuit file (.sub or .lib)",
            "Verify the subcircuit name in the file matches the component's model/value field",
            "Alternatively, open Simulation -> Spice Editor and add '.include /path/to/subcircuit.sub'"
        ],
        "prevention": [
            "Keep all subcircuit files (.sub, .lib) in the project directory",
            "Verify subcircuit availability before placing hierarchical or IC components",
            "Check pin count matches between KiCad symbol and .subckt definition"
        ]
    },
    "Invalid Parameter / Syntax Error": {
        "category": "Invalid Parameter / Syntax Error",
        "severity": "critical",
        "likely_causes": [
            "A component value contains letters instead of a valid number (e.g., 'AA' instead of '5')",
            "Missing required parameters for a source definition (e.g., SINE, PULSE missing arguments)",
            "Invalid SPICE value suffix (valid: k, meg, m, u, n, p, f)",
            "Extra or misplaced tokens in a component line"
        ],
        "fixes": [
            "Open the component properties and set the value to a valid number with proper suffix",
            "For sources, verify all required parameters are present (e.g., SINE needs offset, amplitude, frequency)",
            "Check that SPICE value suffixes are correct: k=1e3, meg=1e6, m=1e-3, u=1e-6, n=1e-9, p=1e-12",
            "Remove any extra spaces or invalid characters from component value fields"
        ],
        "esim_steps": [
            "In KiCad, double-click the flagged component to open its properties",
            "Set the Value field to a valid number (e.g., '1k' for 1 kilo-ohm, '10u' for 10 microfarad)",
            "For sources, verify parameters: e.g., SINE(0 5 1k) means offset=0, amplitude=5V, frequency=1kHz",
            "Save and go to Simulation -> Convert KiCad to NgSpice"
        ],
        "prevention": [
            "Double-check all source parameters (SINE, PULSE, PWL, DC) before converting to NgSpice",
            "Use eSim's built-in source configuration dialogs where available",
            "Refer to the NgSpice manual for required parameter lists for each source type"
        ]
    },
    "No Plot Data (Simulation Succeeded)": {
        "category": "No Plot Data (Simulation Succeeded)",
        "severity": "info",
        "likely_causes": [
            "The simulation completed successfully but no plot probes were added to the schematic",
            "NgSpice has no output variables to display because no measurements were requested"
        ],
        "fixes": [
            "Add voltage or current plot components to the schematic on the wires you want to measure",
            "Verify that plot components are properly connected to circuit nodes (not floating)"
        ],
        "esim_steps": [
            "In KiCad, press 'A' and search for 'plot_v1' (voltage probe) or 'plot_i2' (current probe)",
            "Place the probe on the wire or node you want to measure",
            "Save and go to Simulation -> Convert KiCad to NgSpice, then re-simulate"
        ],
        "prevention": [
            "Always add plot probes to nodes of interest before running a simulation",
            "For current measurement, place the current probe in series with the component"
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
        "fixes": [
            "Verify every component pin is connected in the schematic",
            "Verify the circuit contains a GND reference (node 0)",
            "Check for floating nodes and unrealistic component values"
        ],
        "esim_steps": [
            "Run Inspect -> Electrical Rules Check (ERC) in KiCad",
            "Fix any reported errors, then go to Simulation -> Convert KiCad to NgSpice"
        ],
        "prevention": []
    })

