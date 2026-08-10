"""
netlist_to_verilog.py

Converts a validated eSim .cir.out netlist into synthesizable Verilog.
Works on top of pdk_validator to reuse the parsed netlist structure.
"""

import sys
from pathlib import Path
from pdk_validator import SpiceNetlist, ANALOG_PRIMITIVES


# Maps sky130 cell names to their Verilog primitive equivalents
# Format: cell_name -> (verilog_primitive, output_port, input_ports)
CELL_TO_VERILOG = {
    # Inverters
    "sky130_fd_sc_hd__inv_1":   ("not",  "Y", ["A"]),
    "sky130_fd_sc_hd__inv_2":   ("not",  "Y", ["A"]),
    "sky130_fd_sc_hd__inv_4":   ("not",  "Y", ["A"]),
    "sky130_fd_sc_hd__inv_8":   ("not",  "Y", ["A"]),
    # Buffers
    "sky130_fd_sc_hd__buf_1":   ("buf",  "X", ["A"]),
    "sky130_fd_sc_hd__buf_2":   ("buf",  "X", ["A"]),
    "sky130_fd_sc_hd__buf_4":   ("buf",  "X", ["A"]),
    "sky130_fd_sc_hd__buf_8":   ("buf",  "X", ["A"]),
    # NAND
    "sky130_fd_sc_hd__nand2_1": ("nand", "Y", ["A", "B"]),
    "sky130_fd_sc_hd__nand2_2": ("nand", "Y", ["A", "B"]),
    "sky130_fd_sc_hd__nand2_4": ("nand", "Y", ["A", "B"]),
    "sky130_fd_sc_hd__nand3_1": ("nand", "Y", ["A", "B", "C"]),
    "sky130_fd_sc_hd__nand3_2": ("nand", "Y", ["A", "B", "C"]),
    "sky130_fd_sc_hd__nand4_1": ("nand", "Y", ["A", "B", "C", "D"]),
    # NOR
    "sky130_fd_sc_hd__nor2_1":  ("nor",  "Y", ["A", "B"]),
    "sky130_fd_sc_hd__nor2_2":  ("nor",  "Y", ["A", "B"]),
    "sky130_fd_sc_hd__nor3_1":  ("nor",  "Y", ["A", "B", "C"]),
    "sky130_fd_sc_hd__nor4_1":  ("nor",  "Y", ["A", "B", "C", "D"]),
    # AND
    "sky130_fd_sc_hd__and2_0":  ("and",  "X", ["A", "B"]),
    "sky130_fd_sc_hd__and2_2":  ("and",  "X", ["A", "B"]),
    "sky130_fd_sc_hd__and2_4":  ("and",  "X", ["A", "B"]),
    "sky130_fd_sc_hd__and3_1":  ("and",  "X", ["A", "B", "C"]),
    "sky130_fd_sc_hd__and4_1":  ("and",  "X", ["A", "B", "C", "D"]),
    # OR
    "sky130_fd_sc_hd__or2_0":   ("or",   "X", ["A", "B"]),
    "sky130_fd_sc_hd__or2_2":   ("or",   "X", ["A", "B"]),
    "sky130_fd_sc_hd__or2_4":   ("or",   "X", ["A", "B"]),
    "sky130_fd_sc_hd__or3_1":   ("or",   "X", ["A", "B", "C"]),
    "sky130_fd_sc_hd__or4_1":   ("or",   "X", ["A", "B", "C", "D"]),
    # XOR
    "sky130_fd_sc_hd__xor2_1":  ("xor",  "X", ["A", "B"]),
    "sky130_fd_sc_hd__xor2_2":  ("xor",  "X", ["A", "B"]),
    "sky130_fd_sc_hd__xnor2_1": ("xnor", "Y", ["A", "B"]),
    "sky130_fd_sc_hd__xnor2_2": ("xnor", "Y", ["A", "B"]),
    # Flip-flops (D type, positive edge)
    "sky130_fd_sc_hd__dfxtp_1": ("dff",  "Q", ["D", "CLK"]),
    "sky130_fd_sc_hd__dfxtp_2": ("dff",  "Q", ["D", "CLK"]),
    "sky130_fd_sc_hd__dfxtp_4": ("dff",  "Q", ["D", "CLK"]),
    # Clock buffers (treated as regular buffers in Verilog)
    "sky130_fd_sc_hd__clkbuf_1": ("buf", "X", ["A"]),
    "sky130_fd_sc_hd__clkbuf_2": ("buf", "X", ["A"]),
    "sky130_fd_sc_hd__clkbuf_4": ("buf", "X", ["A"]),
    "sky130_fd_sc_hd__clkbuf_8": ("buf", "X", ["A"]),
}


def get_digital_ports(subckt_ports):
    # Filter out power/ground pins — not needed in synthesizable Verilog
    skip = {"vdd", "vcc", "gnd", "vss", "vpwr", "vgnd"}
    return [p for p in subckt_ports if p.lower() not in skip]


def infer_port_direction(port, instances):
    # If a port drives an instance input it's an input, if it comes from an output it's output
    # Simple heuristic: assume first ports are inputs, last is output
    # A proper implementation would do connectivity analysis
    driven_nets = set()
    for inst in instances:
        parts = inst["raw"].split()
        positional = [p for p in parts[1:] if "=" not in p]
        if len(positional) >= 2:
            # Last positional before power pins is the cell — nets are everything else
            cell = positional[-1]
            nets = positional[:-1]
            # First net after instance name is usually output for most gates
            if nets:
                driven_nets.add(nets[0])
    return driven_nets


def convert_subckt_to_verilog(subckt, internal_subckt_names):
    name = subckt["name"]
    ports = get_digital_ports(subckt["ports"])
    instances = subckt["instances"]

    # Collect all internal wire names
    all_nets = set()
    for inst in instances:
        parts = inst["raw"].split()
        positional = [p for p in parts[1:] if "=" not in p]
        # exclude cell name and power pins
        skip = {"vdd", "vcc", "gnd", "vss", "vpwr", "vgnd"}
        nets = [p for p in positional[:-1] if p.lower() not in skip]
        all_nets.update(nets)

    internal_wires = [n for n in all_nets if n not in ports]

    lines = []
    lines.append(f"module {name} (")
    lines.append(f"    {', '.join(ports)}")
    lines.append(f");")
    lines.append("")

    # Port declarations — simple heuristic: last port is output, rest are inputs
    if ports:
        for p in ports[:-1]:
            lines.append(f"    input  wire {p};")
        lines.append(f"    output wire {ports[-1]};")

    if internal_wires:
        lines.append("")
        for w in sorted(internal_wires):
            lines.append(f"    wire {w};")

    lines.append("")

    # Instance declarations
    for inst in instances:
        ctype = inst["type"]
        cell = inst["cell"]
        iname = inst["name"]

        # Skip analog primitives
        if ctype in ANALOG_PRIMITIVES:
            continue

        # Skip power sources
        if ctype == "v":
            continue

        parts = inst["raw"].split()
        positional = [p for p in parts[1:] if "=" not in p]
        skip_pins = {"vdd", "vcc", "gnd", "vss", "vpwr", "vgnd"}
        nets = [p for p in positional[:-1] if p.lower() not in skip_pins]

        if cell in internal_subckt_names:
            # Hierarchical instance — emit as module instantiation
            lines.append(f"    {cell} {iname} (")
            port_connects = [f"        .port{i}({n})" for i, n in enumerate(nets)]
            lines.append(",\n".join(port_connects))
            lines.append(f"    );")
        elif cell in CELL_TO_VERILOG:
            primitive, out_port, in_ports = CELL_TO_VERILOG[cell]

            if primitive == "dff":
                # Emit always block for flip-flop
                if len(nets) >= 2:
                    q_net, d_net, clk_net = nets[0], nets[1], nets[2] if len(nets) > 2 else "clk"
                    lines.append(f"    // {iname} : D flip-flop")
                    lines.append(f"    reg {q_net}_reg;")
                    lines.append(f"    always @(posedge {clk_net}) {q_net}_reg <= {d_net};")
                    lines.append(f"    assign {q_net} = {q_net}_reg;")
            else:
                # Gate primitive
                if nets:
                    out_net = nets[0]
                    in_nets = nets[1:] if len(nets) > 1 else nets
                    lines.append(f"    {primitive} {iname} ({out_net}, {', '.join(in_nets)});")
        else:
            lines.append(f"    // WARNING: {iname} uses unmapped cell '{cell}' - skipped")

    lines.append("")
    lines.append("endmodule")
    lines.append("")
    return "\n".join(lines)


def convert(cir_out_path, output_path=None):
    netlist = SpiceNetlist(cir_out_path)

    if not netlist.subcircuits:
        print("[netlist_to_verilog] No subcircuits found in netlist.")
        return None

    if output_path is None:
        output_path = str(Path(cir_out_path).with_suffix(".v"))

    verilog_blocks = []
    verilog_blocks.append(f"// Auto-generated Verilog from eSim netlist")
    verilog_blocks.append(f"// Source: {Path(cir_out_path).name}")
    verilog_blocks.append(f"// Tool  : eSim-ORFS netlist_to_verilog.py")
    verilog_blocks.append("")

    for subckt in netlist.subcircuits:
        print(f"[netlist_to_verilog] Converting subcircuit: {subckt['name']}")
        verilog_blocks.append(
            convert_subckt_to_verilog(subckt, netlist.internal_subckt_names)
        )

    verilog_output = "\n".join(verilog_blocks)
    Path(output_path).write_text(verilog_output)
    print(f"[netlist_to_verilog] Verilog written to: {output_path}")
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python netlist_to_verilog.py <netlist.cir.out> [output.v]")
        sys.exit(1)
    out = convert(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
    if out:
        print("\n--- Generated Verilog ---")
        print(Path(out).read_text())

