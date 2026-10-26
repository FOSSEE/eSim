import sys
from pathlib import Path

SKY130_HD_CELLS = {
    "sky130_fd_sc_hd__inv_1", "sky130_fd_sc_hd__inv_2", "sky130_fd_sc_hd__inv_4",
    "sky130_fd_sc_hd__inv_6", "sky130_fd_sc_hd__inv_8", "sky130_fd_sc_hd__inv_12",
    "sky130_fd_sc_hd__inv_16", "sky130_fd_sc_hd__buf_1", "sky130_fd_sc_hd__buf_2",
    "sky130_fd_sc_hd__buf_4", "sky130_fd_sc_hd__buf_6", "sky130_fd_sc_hd__buf_8",
    "sky130_fd_sc_hd__buf_12", "sky130_fd_sc_hd__buf_16", "sky130_fd_sc_hd__nand2_1",
    "sky130_fd_sc_hd__nand2_2", "sky130_fd_sc_hd__nand2_4", "sky130_fd_sc_hd__nand2_8",
    "sky130_fd_sc_hd__nand3_1", "sky130_fd_sc_hd__nand3_2", "sky130_fd_sc_hd__nand3_4",
    "sky130_fd_sc_hd__nand4_1", "sky130_fd_sc_hd__nand4_2", "sky130_fd_sc_hd__nor2_1",
    "sky130_fd_sc_hd__nor2_2", "sky130_fd_sc_hd__nor2_4", "sky130_fd_sc_hd__nor2_8",
    "sky130_fd_sc_hd__nor3_1", "sky130_fd_sc_hd__nor3_2", "sky130_fd_sc_hd__nor3_4",
    "sky130_fd_sc_hd__nor4_1", "sky130_fd_sc_hd__nor4_2", "sky130_fd_sc_hd__and2_0",
    "sky130_fd_sc_hd__and2_2", "sky130_fd_sc_hd__and2_4", "sky130_fd_sc_hd__and3_1",
    "sky130_fd_sc_hd__and3_2", "sky130_fd_sc_hd__and3_4", "sky130_fd_sc_hd__and4_1",
    "sky130_fd_sc_hd__and4_2", "sky130_fd_sc_hd__or2_0", "sky130_fd_sc_hd__or2_2",
    "sky130_fd_sc_hd__or2_4", "sky130_fd_sc_hd__or3_1", "sky130_fd_sc_hd__or3_2",
    "sky130_fd_sc_hd__or3_4", "sky130_fd_sc_hd__or4_1", "sky130_fd_sc_hd__or4_2",
    "sky130_fd_sc_hd__xor2_1", "sky130_fd_sc_hd__xor2_2", "sky130_fd_sc_hd__xnor2_1",
    "sky130_fd_sc_hd__xnor2_2", "sky130_fd_sc_hd__xor3_1", "sky130_fd_sc_hd__mux2_1",
    "sky130_fd_sc_hd__mux2_2", "sky130_fd_sc_hd__mux2_4", "sky130_fd_sc_hd__mux4_1",
    "sky130_fd_sc_hd__mux4_2", "sky130_fd_sc_hd__dfxtp_1", "sky130_fd_sc_hd__dfxtp_2",
    "sky130_fd_sc_hd__dfxtp_4", "sky130_fd_sc_hd__dfxbp_1", "sky130_fd_sc_hd__dfxbp_2",
    "sky130_fd_sc_hd__dfrtp_1", "sky130_fd_sc_hd__dfrtp_2", "sky130_fd_sc_hd__dfrtp_4",
    "sky130_fd_sc_hd__dfsbp_1", "sky130_fd_sc_hd__dfsbp_2", "sky130_fd_sc_hd__dfstp_1",
    "sky130_fd_sc_hd__dfstp_2", "sky130_fd_sc_hd__dfstp_4", "sky130_fd_sc_hd__dlxtp_1",
    "sky130_fd_sc_hd__dlxbp_1", "sky130_fd_sc_hd__dlrtp_1", "sky130_fd_sc_hd__dlrtp_2",
    "sky130_fd_sc_hd__dlrtp_4", "sky130_fd_sc_hd__a21o_1", "sky130_fd_sc_hd__a21o_2",
    "sky130_fd_sc_hd__a21oi_1", "sky130_fd_sc_hd__a21oi_2", "sky130_fd_sc_hd__a22o_1",
    "sky130_fd_sc_hd__a22oi_1", "sky130_fd_sc_hd__a31o_1", "sky130_fd_sc_hd__a31oi_1",
    "sky130_fd_sc_hd__o21a_1", "sky130_fd_sc_hd__o21ai_1", "sky130_fd_sc_hd__o22a_1",
    "sky130_fd_sc_hd__o22ai_1", "sky130_fd_sc_hd__conb_1", "sky130_fd_sc_hd__clkbuf_1",
    "sky130_fd_sc_hd__clkbuf_2", "sky130_fd_sc_hd__clkbuf_4", "sky130_fd_sc_hd__clkbuf_8",
    "sky130_fd_sc_hd__clkbuf_16", "sky130_fd_sc_hd__clkinv_1", "sky130_fd_sc_hd__clkinv_2",
    "sky130_fd_sc_hd__clkinv_4", "sky130_fd_sc_hd__clkinv_8", "sky130_fd_sc_hd__clkinv_16",
}

PDK_CELL_LIBS = {"sky130": SKY130_HD_CELLS}
ANALOG_PRIMITIVES = {"r", "c", "l", "v", "i", "d", "q", "m", "e", "f", "g", "h"}


class SpiceNetlist:
    def __init__(self, path):
        self.path = Path(path)
        self.title = ""
        self.subcircuits = []
        self.top_instances = []
        self.internal_subckt_names = set()
        self._parse()

    def _parse(self):
        with open(self.path, "r", errors="replace") as f:
            lines = f.readlines()
        joined = self._join_continuations(lines)
        # First pass: collect all internal subcircuit names
        for line in joined:
            stripped = line.strip()
            if stripped.lower().startswith(".subckt"):
                parts = stripped.split()
                if len(parts) > 1:
                    self.internal_subckt_names.add(parts[1].lower())
        # Second pass: parse instances
        current_subckt = None
        title_set = False
        for line in joined:
            stripped = line.strip()
            if not stripped or stripped.startswith("*"):
                continue
            lower = stripped.lower()
            if not title_set and not lower.startswith("."):
                self.title = stripped
                title_set = True
                continue
            if lower.startswith(".subckt"):
                parts = stripped.split()
                current_subckt = {"name": parts[1] if len(parts) > 1 else "unnamed", "ports": parts[2:], "instances": []}
                self.subcircuits.append(current_subckt)
            elif lower.startswith(".ends"):
                current_subckt = None
            elif lower.startswith(".end"):
                break
            elif not lower.startswith("."):
                inst = self._parse_instance(stripped)
                if inst:
                    if current_subckt is not None:
                        current_subckt["instances"].append(inst)
                    else:
                        self.top_instances.append(inst)

    @staticmethod
    def _join_continuations(lines):
        result = []
        for line in lines:
            if line.startswith("+") and result:
                result[-1] = result[-1].rstrip() + " " + line[1:].strip()
            else:
                result.append(line)
        return result

    @staticmethod
    def _parse_instance(line):
        parts = line.split()
        if not parts:
            return None
        name = parts[0]
        positional = [p for p in parts[1:] if "=" not in p]
        cell_name = positional[-1] if positional else ""
        return {"name": name, "type": name[0].lower(), "cell": cell_name, "raw": line}


class PDKValidator:
    def __init__(self, pdk="sky130"):
        if pdk not in PDK_CELL_LIBS:
            raise ValueError(f"Unknown PDK '{pdk}'.")
        self.pdk = pdk
        self.known_cells = PDK_CELL_LIBS[pdk]

    def validate(self, netlist):
        valid_cells, unmappable, analog_found, internal_calls = [], [], [], []
        all_instances = list(netlist.top_instances)
        for subckt in netlist.subcircuits:
            all_instances.extend(subckt["instances"])
        for inst in all_instances:
            ctype = inst["type"]
            cell = inst["cell"]
            if ctype == "x":
                if cell in self.known_cells:
                    valid_cells.append({"name": inst["name"], "cell": cell})
                elif cell.lower() in netlist.internal_subckt_names:
                    internal_calls.append({"name": inst["name"], "cell": cell})
                else:
                    unmappable.append({"name": inst["name"], "cell": cell, "reason": f"Not found in {self.pdk} standard cell library"})
            elif ctype in ANALOG_PRIMITIVES:
                analog_found.append({"name": inst["name"], "type": ctype})
            else:
                unmappable.append({"name": inst["name"], "cell": cell, "reason": f"Unknown component type '{ctype}'"})
        return {
            "netlist": str(netlist.path), "pdk": self.pdk,
            "valid_cells": valid_cells, "unmappable": unmappable,
            "analog_primitives": analog_found, "internal_calls": internal_calls,
            "summary": "PASS" if len(unmappable) == 0 else "FAIL",
        }

    @staticmethod
    def print_report(report):
        print(f"\n{'='*60}\nPDK Validation Report")
        print(f"  Netlist : {report['netlist']}\n  PDK     : {report['pdk']}\n  Result  : {report['summary']}")
        print(f"{'='*60}")
        if report["valid_cells"]:
            print(f"\n[OK] Mapped cells ({len(report['valid_cells'])}):")
            for c in report["valid_cells"]:
                print(f"   {c['name']:30s} -> {c['cell']}")
        if report.get("internal_calls"):
            print(f"\n[HIER] Internal subcircuit calls ({len(report['internal_calls'])}):")
            for c in report["internal_calls"]:
                print(f"   {c['name']:30s} -> {c['cell']} (user-defined)")
        if report["analog_primitives"]:
            print(f"\n[SKIP] Analog primitives ({len(report['analog_primitives'])}):")
            for a in report["analog_primitives"]:
                print(f"   {a['name']:30s} ({a['type'].upper()})")
        if report["unmappable"]:
            print(f"\n[FAIL] Unmappable ({len(report['unmappable'])}):")
            for u in report["unmappable"]:
                print(f"   {u['name']:30s} -> {u['reason']}")
        print()


def validate_netlist(cir_out_path, pdk="sky130"):
    return PDKValidator(pdk).validate(SpiceNetlist(cir_out_path))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pdk_validator.py <netlist.cir.out> [pdk]")
        sys.exit(1)
    report = validate_netlist(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "sky130")
    PDKValidator.print_report(report)
    sys.exit(0 if report["summary"] == "PASS" else 1)
