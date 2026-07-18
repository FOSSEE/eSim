from lark import Lark, Transformer
from dataclasses import dataclass, field
from typing import Optional, List
from collections import Counter


@dataclass
class Component:
    type:  str
    node1: str
    node2: str
    value: str

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
    nodes: List[str]

@dataclass
class CktBlock:
    name:       str
    port_in:    Optional[PortIn]  = None
    port_out:   Optional[PortOut] = None
    components: List[Component]   = field(default_factory=list)
    uses:       List[UseStmt]     = field(default_factory=list)


grammar = r"""
    start: ckt_block+
    ckt_block: "ckt" NAME ":" statement+ "done"
    statement: port_in_decl
             | port_out_decl
             | component
             | use_stmt
    port_in_decl:  "port_in"  ":" NAME
    port_out_decl: "port_out" ":" NAME NAME?
    component: NAME COMP_TYPE NAME VALUE   -> explicit_component
             | COMP_TYPE NAME VALUE        -> implicit_component
    use_stmt: "use" NAME NAME+
    COMP_TYPE.2: "res" | "cap" | "ind"
               | "vol" | "mos" | "bjt" | "diode"
    NAME.1:  /[a-zA-Z_][a-zA-Z0-9_]*/
    VALUE:   /[0-9]+(\.[0-9]+)?[pnumkMGTfF]?/
    %import common.WS
    %ignore WS
"""

parser = Lark(grammar, parser='earley')


class ICELangTransformer(Transformer):

    def statement(self, items):
        return items[0]

    def explicit_component(self, items):
        return Component(
            type=str(items[1]).lower(),
            node1=str(items[0]).lower(),
            node2=str(items[2]).lower(),
            value=str(items[3])
        )

    def implicit_component(self, items):
        return Component(
            type=str(items[0]).lower(),
            node1="vin",
            node2=str(items[1]).lower(),
            value=str(items[2])
        )

    def port_in_decl(self, items):
        return PortIn(name=str(items[0]).lower())

    def port_out_decl(self, items):
        name = str(items[0]).lower()
        node = str(items[1]).lower() if len(items) > 1 else None
        return PortOut(name=name, node=node)

    def use_stmt(self, items):
        return UseStmt(
            circuit_name=str(items[0]).lower(),
            nodes=[str(n).lower() for n in items[1:]]
        )

    def ckt_block(self, items):
        name = str(items[0]).lower()
        port_in, port_out = None, None
        components, uses  = [], []
        for item in items[1:]:
            if isinstance(item, PortIn):
                port_in = item
            elif isinstance(item, PortOut):
                port_out = item
            elif isinstance(item, Component):
                components.append(item)
            elif isinstance(item, UseStmt):
                uses.append(item)
        return CktBlock(
            name=name,
            port_in=port_in,
            port_out=port_out,
            components=components,
            uses=uses
        )

    def start(self, items):
        return items


def analyse(ckt: CktBlock) -> list:
    errors = []

    all_nodes = []
    for comp in ckt.components:
        all_nodes.append(comp.node1)
        all_nodes.append(comp.node2)

    if "gnd" not in all_nodes:
        errors.append("No GND node found — circuit has no ground reference")

    if ckt.port_out and ckt.port_out.node:
        if ckt.port_out.node not in all_nodes:
            errors.append(
                f"port_out node '{ckt.port_out.node}' "
                f"never appears in any component"
            )

    node_count = Counter(all_nodes)
    for node, count in node_count.items():
        if count < 2 and node not in ("vin", "gnd"):
            errors.append(
                f"Node '{node}' only appears once — "
                f"possible floating connection"
            )

    if not ckt.components:
        errors.append("Circuit has no components")

    return errors


if __name__ == "__main__":
    test = """
ckt rc_filter:
    port_in: Vin
    port_out: Vout mc
    res mc 10k
    mc cap gnd 10F
done
"""
    tree = parser.parse(test.strip())
    print("-------> Parse Tree")
    print(tree.pretty())

    transformer = ICELangTransformer()
    result = transformer.transform(tree)

    print("-----> IR Objects")
    for ckt in result:
        print(f"\nCircuit : {ckt.name}")
        print(f"port_in  : {ckt.port_in}")
        print(f"port_out : {ckt.port_out}")
        for comp in ckt.components:
            print(f"component: {comp}")

    print("--------> Semantic Analysis")
    for ckt in result:
        errors = analyse(ckt)
        if errors:
            for e in errors:
                print(f"  ERROR: {e}")
        else:
            print(f"  {ckt.name} — all checks passed")
