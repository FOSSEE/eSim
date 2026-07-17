import sys
import os
import re
import subprocess


def parse_spice_netlist(netlist_path):
    """
    Parses an eSim/Ngspice-style .cir.out netlist.
    Extracts component instances (lines starting with X or U) and their
    connected nodes, so we can rebuild real connectivity in Verilog
    instead of emitting a fixed placeholder circuit.
    """
    instances = []   # list of dicts: {name, subckt, nodes: [..]}
    all_nodes = {}    # node_name -> number of times it appears

    with open(netlist_path, "r") as f:
        lines = f.readlines()

    for raw_line in lines:
        line = raw_line.strip()
        if not line or line.startswith("*") or line.startswith("."):
            continue

        # SPICE instance lines: X<name> node1 node2 ... <subckt_name>
        # or U<name> for digital primitives depending on eSim's netlist style
        if line[0].upper() in ("X", "U"):
            tokens = line.split()
            inst_name = tokens[0]
            subckt_name = tokens[-1]
            nodes = tokens[1:-1]

            instances.append({
                "name": inst_name,
                "subckt": subckt_name,
                "nodes": nodes
            })

            for n in nodes:
                all_nodes[n] = all_nodes.get(n, 0) + 1

    return instances, all_nodes


def infer_ports(all_nodes):
    """
    Nodes that only appear once across all instances are almost always
    the circuit's external I/O pins (everything else is internal wiring
    between components). This is a heuristic, not a substitute for
    schematic-level port annotation, but it works for typical single-level
    eSim digital netlists.
    """
    ports = [n for n, count in all_nodes.items() if count == 1]
    internal = [n for n, count in all_nodes.items() if count > 1]
    return ports, internal


def sanitize(name):
    """Verilog identifiers can't start with a digit or contain some SPICE chars."""
    clean = re.sub(r"[^a-zA-Z0-9_]", "_", name)
    if clean and clean[0].isdigit():
        clean = "n_" + clean
    return clean


def generate_verilog(project_name, instances, all_nodes):
    ports, internal = infer_ports(all_nodes)

    if not instances:
        # No parsable instances found — fail loudly instead of faking output
        raise ValueError(
            "No component instances (X.../U...) found in netlist. "
            "Check that the .cir.out file was generated correctly by "
            "'Convert KiCad to Ngspice' before running this bridge."
        )

    lines = []
    port_list = ", ".join(sanitize(p) for p in ports)
    lines.append(f"module {project_name} ({port_list});")

    for p in ports:
        # We can't reliably know direction from a flat netlist alone;
        # declare as inout and let the user/mentor refine per-pin direction.
        lines.append(f"  inout {sanitize(p)};")

    for n in internal:
        lines.append(f"  wire {sanitize(n)};")

    lines.append("")
    for inst in instances:
        pins = ", ".join(sanitize(n) for n in inst["nodes"])
        lines.append(f"  {sanitize(inst['subckt'])} {sanitize(inst['name'])} ({pins});")

    lines.append("endmodule")
    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Error: No netlist path provided.")
        sys.exit(1)

    netlist_path = sys.argv[1]

    if not os.path.exists(netlist_path):
        print(f"Error: Netlist file not found at {netlist_path}")
        sys.exit(1)

    project_dir = os.path.dirname(netlist_path)
    project_name = sanitize(os.path.basename(netlist_path).replace(".cir.out", ""))

    print(f"--- Starting OpenROAD Integration for '{project_name}' ---")

    # 1. Real netlist parsing (replaces the old hardcoded half-adder stub)
    instances, all_nodes = parse_spice_netlist(netlist_path)
    print(f"[*] Parsed {len(instances)} component instance(s), {len(all_nodes)} net(s)")

    try:
        verilog_code = generate_verilog(project_name, instances, all_nodes)
    except ValueError as e:
        print(f"[Error] {e}")
        sys.exit(1)

    verilog_file = os.path.join(project_dir, f"{project_name}.v")
    with open(verilog_file, "w") as f:
        f.write(verilog_code + "\n")
    print(f"[*] Generated Verilog RTL at: {verilog_file}")

    # 2. Auto-Generate the OpenROAD Flow Script (ORFS) config.mk
    config_file = os.path.join(project_dir, "config.mk")
    with open(config_file, "w") as f:
        f.write(f"export DESIGN_NAME = {project_name}\n")
        f.write(f"export PLATFORM    = sky130hd\n")
        f.write(f"export VERILOG_FILES = {verilog_file}\n")
        f.write("export CLOCK_PERIOD = 10.0\n")
    print(f"[*] Generated ORFS Config at: {config_file}")

    # 3. Launch OpenROAD Flow
    print("\n[*] Launching OpenROAD Flow... This might take a few minutes.")
    try:
        orfs_flow_path = os.path.expanduser("~/OpenROAD_Linux/flow")
        if not os.path.exists(orfs_flow_path):
            orfs_flow_path = os.path.expanduser("~/OpenROAD_Linux")

        result = subprocess.run(
            ['make', '-C', orfs_flow_path, f'DESIGN_CONFIG={config_file}'],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(f"\n[SUCCESS] OpenROAD Flow completed for {project_name}!")
            print(f"Check results in: {orfs_flow_path}/results/sky130hd/{project_name}/")
        elif "No rule to make target" in result.stderr or "No targets specified" in result.stderr:
            print(f"\n[Notice] eSim bridge executed for '{project_name}'!")
            print(f"         Verilog RTL and config.mk were successfully generated from the real netlist.")
            print(f"         No ORFS Makefile was found at {orfs_flow_path}.")
            print(f"         To generate GDSII, ensure OpenROAD-flow-scripts is installed.")
        else:
            print(f"\n[Flow Error] OpenROAD failed with return code {result.returncode}")
            print(f"Details:\n{result.stderr}")

    except Exception as e:
        print(f"\n[System Error] Could not trigger OpenROAD: {str(e)}")


if __name__ == "__main__":
    main()
