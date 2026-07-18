from lark import Lark, Transformer
from dataclasses import dataclass, field
from typing import Optional, List, Dict
from collections import Counter


# --------->dataclasses 

@dataclass
class Component:
    type:  str
    nodes: List[str]
    value: str
    pins:  Dict[str, str] = field(default_factory=dict)

@dataclass
class PortIn:
    name: str

@dataclass
class PortOut:
    name: str
    node: Optional[str] = None

@dataclass
class UseStmt:
    circuit_name: str
    nodes:        List[str]

@dataclass
class DefineStmt:
    name:         str
    kicad_symbol: str
    spice_prefix: str
    pin_count:    int

@dataclass
class CktBlock:
    name:       str
    port_in:    Optional[PortIn]  = None
    port_out:   Optional[PortOut] = None
    components: List[Component]   = field(default_factory=list)
    uses:       List[UseStmt]     = field(default_factory=list)
    defines:    List[DefineStmt]  = field(default_factory=list)


# -------------grammar

grammar = r"""
    start: ckt_block+

    ckt_block: "ckt" NAME ":" statement+ "done"

    statement: port_in_decl
             | port_out_decl
             | component_stmt
             | define_stmt
             | use_stmt

    port_in_decl:  "port_in"  ":" NAME
    port_out_decl: "port_out" ":" NAME NAME?

    component_stmt: NAME token+

    define_stmt: "define" NAME
                 "kicad"  "=" QUOTED_STR
                 "spice"  "=" NAME
                 "pins"   "=" INT

    use_stmt: "use" NAME NAME+

    token: NAME  -> tok_name
         | VALUE -> tok_value

    QUOTED_STR: /\"[^\"]*\"/
    NAME:       /[a-zA-Z_][a-zA-Z0-9_]*/
    VALUE:      /[0-9]+(\.[0-9]+)?[pnumkMGTfF]?[a-zA-Z]*/
    INT:        /[0-9]+/

    %import common.WS
    %ignore WS
"""

parser = Lark(grammar, parser='earley')


# ----------->transformer 

class ICELangTransformer(Transformer):

    def tok_name(self, items):
        return ("name", str(items[0]))

    def tok_value(self, items):
        return ("value", str(items[0]))

    def component_stmt(self, items):
        from component_registry import lookup

        comp_type = str(items[0]).lower()
        tokens    = list(items[1:])

        entry = lookup(comp_type)

        if entry:
            pin_count  = entry["pin_count"]
            pin_names  = entry.get("pin_names",
                         [str(i+1) for i in range(pin_count)])
            name_tokens = [t[1] for t in tokens if t[0] == "name"]
            val_tokens  = [t[1] for t in tokens if t[0] == "value"]

            nodes = name_tokens[:pin_count]
            value = (val_tokens[0] if val_tokens
                     else name_tokens[pin_count]
                     if len(name_tokens) > pin_count else "")

            pins = {pin_names[i]: nodes[i]
                    for i in range(min(len(pin_names), len(nodes)))}
        else:
            all_tokens  = [t[1] for t in tokens]
            nodes = [t for t in all_tokens if not t[0].isdigit()]
            value = next((t for t in all_tokens
                          if t[0].isdigit()), "")
            pins  = {}

        return Component(
            type  = comp_type,
            nodes = [n.lower() for n in nodes],
            value = value,
            pins  = {k: v.lower() for k, v in pins.items()}
        )

    def define_stmt(self, items):
        from component_registry import register

        name         = str(items[0]).lower()
        kicad_symbol = str(items[1]).strip('"')
        spice_prefix = str(items[2]).upper()
        pin_count    = int(items[3])

        register(
            name         = name,
            kicad_symbol = kicad_symbol,
            spice_prefix = spice_prefix,
            pin_count    = pin_count,
            pin_names    = [str(i+1) for i in range(pin_count)]
        )

        return DefineStmt(
            name         = name,
            kicad_symbol = kicad_symbol,
            spice_prefix = spice_prefix,
            pin_count    = pin_count
        )

    def port_in_decl(self, items):
        return PortIn(name=str(items[0]).lower())

    def port_out_decl(self, items):
        name = str(items[0]).lower()
        node = str(items[1]).lower() if len(items) > 1 else None
        return PortOut(name=name, node=node)

    def use_stmt(self, items):
        return UseStmt(
            circuit_name = str(items[0]).lower(),
            nodes        = [str(n).lower() for n in items[1:]]
        )

    def statement(self, items):
        return items[0]

    def ckt_block(self, items):
        name       = str(items[0]).lower()
        port_in    = None
        port_out   = None
        components = []
        uses       = []
        defines    = []

        for item in items[1:]:
            if isinstance(item, PortIn):
                port_in = item
            elif isinstance(item, PortOut):
                port_out = item
            elif isinstance(item, Component):
                components.append(item)
            elif isinstance(item, UseStmt):
                uses.append(item)
            elif isinstance(item, DefineStmt):
                defines.append(item)

        return CktBlock(
            name       = name,
            port_in    = port_in,
            port_out   = port_out,
            components = components,
            uses       = uses,
            defines    = defines
        )

    def start(self, items):
        return list(items)


# -----------> semantic analyser 

def analyse(ckt: CktBlock) -> list:
    errors     = []
    all_nodes  = []

    for comp in ckt.components:
        all_nodes.extend(comp.nodes)

    if not any(n == "gnd" for n in all_nodes):
        errors.append(
            "No GND node found — circuit has no ground reference"
        )

    if ckt.port_out and ckt.port_out.node:
        if ckt.port_out.node not in all_nodes:
            errors.append(
                f"port_out node '{ckt.port_out.node}' "
                f"never appears in any component"
            )

    node_count = Counter(all_nodes)
    for node, count in node_count.items():
        if count < 2 and node not in ("vin", "gnd", "vcc", "vdd"):
            errors.append(
                f"Node '{node}' only appears once — "
                f"possible floating connection"
            )

    if not ckt.components:
        errors.append("Circuit has got no components!!")

    return errors


# ---------------> tests 

if __name__ == "__main__":

    test_cases = [
        ("RC filter", """
ckt rc_filter:
    port_in: Vin
    port_out: Vout mc
    res mc 10k
    mc cap gnd 100n
done
"""),
        ("Voltage source", """
ckt dc_circuit:
    port_in: Vin
    port_out: Vout mc
    vol Vin gnd 5V
    res mc 10k
    mc cap gnd 100n
done
"""),
        ("NPN amplifier", """
ckt npn_amplifier:
    port_in: Vin
    port_out: Vout out
    vol Vcc gnd 9V
    res base 100k
    base res gnd 10k
    bjt_npn base out gnd BC547
    res out 1k
    cap base Vin 10uF
done
"""),
        ("CMOS inverter", """
ckt cmos_inverter:
    port_in: Vin
    port_out: Vout out
    vol Vdd gnd 3.3V
    pmos Vin out Vdd Vdd PMOS_MODEL
    nmos Vin out gnd gnd NMOS_MODEL
done
"""),
        ("User defined component", """
ckt custom_circuit:
    define BC547 kicad="Device:Q_NPN_BCE" spice=Q pins=3
    port_in: Vin
    port_out: Vout out
    BC547 base out gnd
    res base Vin 100k
done
"""),
        ("Cascaded subcircuits", """
ckt rc_stage:
    port_in: Vin
    port_out: Vout mc
    res mc 10k
    mc cap gnd 100n
done

ckt dual_rc:
    port_in: Vin
    port_out: Vout mid2
    use rc_stage Vin mid1
    use rc_stage mid1 mid2
done
"""),
    ]

    transformer = ICELangTransformer()
    passed      = 0
    failed      = 0

    for test_name, source in test_cases:
        print(f"\n{'─'*50}")
        print(f"Test: {test_name}")
        print(f"{'─'*50}")
        try:
            tree   = parser.parse(source.strip())
            result = transformer.transform(tree)
            for ckt in result:
                print(f"  ckt      : {ckt.name}")
                if ckt.port_in:
                    print(f"  port_in  : {ckt.port_in.name}")
                if ckt.port_out:
                    print(f"  port_out : "
                          f"{ckt.port_out.name} @ {ckt.port_out.node}")
                for comp in ckt.components:
                    print(f"  {comp.type:15} "
                          f"nodes={comp.nodes} "
                          f"value={comp.value}")
                for use in ckt.uses:
                    print(f"  use {use.circuit_name} {use.nodes}")
                errors = analyse(ckt)
                if errors:
                    for e in errors:
                        print(f"  SEMANTIC: {e}")
                else:
                    print(f"  semantic : OK")
            passed += 1
        except Exception as e:
            print(f"  FAILED: {e}")
            failed += 1

    print(f"\n{'═'*50}")
    print(f"Results: {passed} passed  {failed} failed")
    print(f"{'═'*50}")
